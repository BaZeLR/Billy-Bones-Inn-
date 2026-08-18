# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default BarberShopSavedText = ""
default BarberFirstTipSeen = 0
default BarberInvitePending = {}
default BarberVisitLastDay = {}

init python:
    BARBER_MALE_HAIRCUT_PRICE = 90
    BARBER_FEMALE_HAIRCUT_PRICE = 120
    BARBER_OLIVE_OIL_PRICE = 11
    BARBER_LUXURY_SOAP_BUY_PRICE = 22
    BARBER_READINESS_MAX = 20
    BARBER_NPC_READINESS_GAIN = {
        "sandra": 2,
        "melissa": 3,
        "amanda": 3,
        "becky": 2,
        "clara": 2,
    }

    def barber_shop_readiness_gain(npc_id=""):
        key = str(npc_id or "").strip().lower()
        return max(1, int(BARBER_NPC_READINESS_GAIN.get(key, 2) or 2))

    def _barber_progress_stage_from_readiness(readiness_value=0):
        value = max(0, min(BARBER_READINESS_MAX, int(readiness_value or 0)))
        if value < 4:
            return 0
        if value < 8:
            return 1
        if value < 12:
            return 2
        if value < 16:
            return 3
        return 4

    def npc_barber_progress_state(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if key == "":
            return {}
        state = npc_appearance_state(key)
        if not isinstance(state, dict):
            return {}
        grooming = state.setdefault("grooming", {})
        grooming.setdefault("barber_visit_count", 0)
        grooming.setdefault("barber_readiness", 0)
        grooming.setdefault("barber_last_progress_day", -1)

        # Old saves only knew the last barber day. Import one historical visit
        # without retroactively changing social stats.
        raw_legacy_day = BarberVisitLastDay.get(key, -1) if isinstance(BarberVisitLastDay, dict) else -1
        try:
            legacy_day = int(raw_legacy_day)
        except Exception:
            legacy_day = -1
        try:
            visit_count = int(grooming.get("barber_visit_count", 0) or 0)
        except Exception:
            visit_count = 0
        if legacy_day >= 0 and visit_count <= 0:
            grooming["barber_visit_count"] = 1
            grooming["barber_readiness"] = min(BARBER_READINESS_MAX, barber_shop_readiness_gain(key))
            grooming["barber_last_progress_day"] = legacy_day
        return grooming

    def npc_barber_visit_count(girl_name=""):
        progression = npc_barber_progress_state(girl_name)
        try:
            return max(0, int(progression.get("barber_visit_count", 0) or 0))
        except Exception:
            return 0

    def npc_barber_readiness(girl_name=""):
        progression = npc_barber_progress_state(girl_name)
        try:
            return max(0, min(BARBER_READINESS_MAX, int(progression.get("barber_readiness", 0) or 0)))
        except Exception:
            return 0

    def npc_barber_stage(girl_name=""):
        return _barber_progress_stage_from_readiness(npc_barber_readiness(girl_name))

    def npc_record_barber_visit(girl_name=""):
        key = str(girl_name or "").strip().lower()
        progression = npc_barber_progress_state(key)
        if key == "" or not progression:
            return {
                "counted": False,
                "visit_count": 0,
                "readiness": 0,
                "stage": 0,
                "stage_delta": 0,
                "friend_delta": 0,
                "openness_delta": 0,
                "corruption_delta": 0,
            }

        # Physical grooming is refreshed every completed service. Social
        # progression, however, is counted at most once per game day.
        npc_apply_grooming(key, "barber_full")
        current_day = int(dayspassed or 0)
        last_progress_day = int(progression.get("barber_last_progress_day", -1) or -1)
        visit_count = max(0, int(progression.get("barber_visit_count", 0) or 0))
        readiness = max(0, min(BARBER_READINESS_MAX, int(progression.get("barber_readiness", 0) or 0)))
        before_stage = _barber_progress_stage_from_readiness(readiness)

        if last_progress_day == current_day:
            return {
                "counted": False,
                "visit_count": visit_count,
                "readiness": readiness,
                "stage": before_stage,
                "stage_delta": 0,
                "friend_delta": 0,
                "openness_delta": 0,
                "corruption_delta": 0,
            }

        visit_count += 1
        readiness = min(BARBER_READINESS_MAX, readiness + barber_shop_readiness_gain(key))
        after_stage = _barber_progress_stage_from_readiness(readiness)
        stage_delta = max(0, after_stage - before_stage)

        # Openness grows only when a new readiness stage is crossed. Corruption
        # begins later: stages 2, 3 and 4 each unlock one gradual point.
        corruption_delta = sum(1 for milestone in (2, 3, 4) if before_stage < milestone <= after_stage)
        progression["barber_visit_count"] = visit_count
        progression["barber_readiness"] = readiness
        progression["barber_last_progress_day"] = current_day
        return {
            "counted": True,
            "visit_count": visit_count,
            "readiness": readiness,
            "stage": after_stage,
            "stage_delta": stage_delta,
            "friend_delta": 1,
            "openness_delta": stage_delta,
            "corruption_delta": corruption_delta,
        }

    def barber_shop_guest_progress_text(npc_id="", progress=None):
        key = str(npc_id or "").strip().lower()
        progress = dict(progress or {})
        stage = max(0, min(4, int(progress.get("stage", npc_barber_stage(key)) or 0)))
        counted = bool(progress.get("counted", True))
        if not counted:
            return "Сегодняшний уход лишь освежает уже достигнутый результат; отношение к нему за один день заметно не меняется."

        texts = {
            "amanda": [
                "Аманда пока воспринимает визит скорее как забавную перемену и с любопытством разглядывает результат в зеркале.",
                "Аманда уже явно наслаждается тем, что ухоженный вид привлекает внимание, и охотнее обсуждает с Серджио, что ей идет.",
                "Аманда начинает сама выбирать детали ухода так, чтобы они подчеркивали фигуру и заставляли окружающих задерживать взгляд чуть дольше.",
                "Для Аманды эти визиты превращаются в часть игры с вниманием: она становится смелее в выборе ухода и куда меньше стесняется обсуждать личные предпочтения.",
                "Аманда уже совершенно сознательно использует уход как средство соблазнения и без смущения выбирает то, что делает ее образ наиболее вызывающим.",
            ],
            "melissa": [
                "Мелисса немного смущена непривычным вниманием к собственной внешности, хотя результат ей явно нравится.",
                "Мелисса начинает чувствовать себя увереннее после таких визитов и уже не так неловко обсуждает уход за собой.",
                "Мелисса с любопытством спрашивает о новых способах ухода и все чаще сама решает, что именно хотела бы изменить или подчеркнуть.",
                "Привычное смущение заметно отступает: Мелисса спокойно говорит о довольно личных деталях ухода и позволяет себе выбирать более смелые варианты.",
                "Мелисса уже воспринимает ухоженность как собственное удовольствие и уверенно выбирает то, что заставляет ее чувствовать себя особенно привлекательной.",
            ],
            "sandra": [
                "Сандра пока относится к процедуре практично: чисто, аккуратно и достаточно, чтобы снова заниматься делами.",
                "Сандра начинает замечать комплименты после визитов и, хоть отмахивается от них, явно становится внимательнее к собственной внешности.",
                "Она уже позволяет Серджио тратить время не только на практичность: хороший уход начинает нравиться Сандре сам по себе.",
                "Сандра все спокойнее принимает внимание к своей зрелой женственности и уже сама просит подчеркнуть некоторые детали вместо того, чтобы просто привести себя в порядок.",
                "Для Сандры уход окончательно становится личным удовольствием; хозяйская строгость остается, но она больше не делает вид, будто ей безразлично собственное чувственное впечатление.",
            ],
            "becky": [
                "Бекки принимает уход без лишней церемонии: ей приятно выглядеть свежее, но никакого открытия в собственной привлекательности она не видит.",
                "Бекки охотно обсуждает с Серджио, какие детали лучше подчеркивают ее зрелую красоту, и явно получает удовольствие от результата.",
                "Ее и без того спокойная телесная уверенность становится более намеренной: Бекки выбирает уход уже не только ради удобства, но и ради того эффекта, который он производит.",
                "Бекки относится к процедуре как к еще одному приятному чувственному удовольствию и без стеснения объясняет, чего хочет от своего образа.",
                "Она прекрасно знает, какой эффект производит, и теперь использует профессиональный уход с той же естественной уверенностью, с какой относится к собственным желаниям.",
            ],
            "clara": [
                "Кларисса и без того привыкла к хорошему уходу, поэтому оценивает работу Серджио прежде всего как придирчивая знаточица.",
                "Кларисса начинает обсуждать с Серджио более тонкие детали стиля и с удовольствием превращает обычный визит в маленький эксперимент.",
                "Ее выбор становится личнее и игривее: дорогая аккуратность все чаще используется не только ради моды, но и ради впечатления.",
                "Кларисса уже без смущения просит о более смелых деталях, сохраняя при этом ту же безупречную, почти аристократическую ухоженность.",
                "Она доводит игру с образом до совершенства: внешне все по-прежнему изысканно, но теперь каждая деталь рассчитана на вполне определенное, чувственное впечатление.",
            ],
        }
        rows = texts.get(key, [])
        if not rows:
            return "Регулярный профессиональный уход постепенно делает ее увереннее и открытее в разговорах о собственной внешности."
        return rows[stage]

    def barber_shop_discount_percent():
        try:
            return max(0, min(90, int(Clara.var.get("sergio_discount", 0) or 0)))
        except Exception:
            return 0

    def barber_shop_discounted_price(base_price):
        price = max(0, int(base_price or 0))
        discount = barber_shop_discount_percent()
        if discount <= 0:
            return price
        return max(1, (price * (100 - discount) + 99) // 100)

    def barber_shop_picture_path():
        picture_path = "images/barber shop/barber shop.jpg"
        if renpy.loadable(picture_path):
            return picture_path
        return "images/general/LocArtisansQuarter1.jpg"

    def barber_shop_is_open():
        calendar_v2.sync_state()
        weekday = int(calendar_v2.week or 0)
        current_minutes = int(calendar_v2.hour or 0) * 60 + int(calendar_v2.minute or 0)
        if weekday in (1, 3):
            return 12 * 60 <= current_minutes <= 17 * 60 + 59
        if weekday == 6:
            return 8 * 60 <= current_minutes <= 11 * 60 + 59
        return False

    def barber_shop_haircut_price(customer_gender="male"):
        if str(customer_gender or "").strip().lower() in ("female", "woman", "girl"):
            return barber_shop_discounted_price(BARBER_FEMALE_HAIRCUT_PRICE)
        return barber_shop_discounted_price(BARBER_MALE_HAIRCUT_PRICE)

    def barber_shop_player_haircut_price():
        return barber_shop_haircut_price("male")

    def barber_shop_player_recent_haircut():
        try:
            return int(player_haircut_elapsed_days() or 0) < 7
        except Exception:
            return False

    def barber_shop_pending_npc_id():
        if not isinstance(BarberInvitePending, dict):
            return ""
        for npc_id in ("sandra", "melissa", "amanda", "becky", "clara"):
            if int(BarberInvitePending.get(npc_id, 0) or 0) == 1:
                return npc_id
        return ""

    def barber_shop_pending_npc_name():
        npc_id = barber_shop_pending_npc_id()
        if npc_id == "":
            return ""
        return str(RealName.get(npc_id, npc_id) or npc_id)

    def barber_shop_can_buy_olive_oil():
        return True

    def barber_shop_can_refine_luxury_soap():
        return int(_player_item_count_by_id("soap_001") or 0) > 0 and int(_player_item_count_by_id("olive_oil_001") or 0) > 0

    def barber_shop_can_sell_luxury_soap():
        return int(_player_item_count_by_id("luxury_soap_001") or 0) > 0

    def barber_shop_can_serve_pending_guest():
        return barber_shop_pending_npc_id() != ""

    def barber_shop_status_text():
        discount = barber_shop_discount_percent()
        discount_text = " После истории с убитым женихом Серджио держит слово и делает вам скидку в %d процентов." % discount if discount > 0 else ""
        if barber_shop_is_open():
            return "Сегодня Серджио на месте: ножницы щелкают, бритва поблескивает, а сам хозяин уже готов засыпать вас новостями." + discount_text
        return "Ставни цирюльни прикрыты. Серджио принимает посетителей только {b}по понедельникам и средам после полудня{/b}, а также {b}в субботу утром{/b}." + discount_text

    def barber_shop_intro_text():
        return (
            "Вы заходите в цирюльню Серджио Пета. В тесноватой, но ухоженной лавке пахнет мылом, травяной водой и нагретым металлом. "
            "На стенах висят зеркала, на полке выстроились баночки с притираниями, а в центре комнаты стоит большое кресло с кожаными подлокотниками.\n\n"
            "Сам Серджио, сухопарый и усатый болтун, встречает вас с таким видом, будто ждал именно этого часа. Он любит поговорить, знает половину городских слухов "
            "и подает каждую сплетню так, словно это глава из какой-нибудь фривольной новеллы.\n\n"
            "Мужская стрижка у него стоит {b}%d мараведи{/b}, женская {b}%d мараведи{/b}."
        ) % (barber_shop_haircut_price("male"), barber_shop_haircut_price("female"))

    def barber_shop_talk_text():
        if int(BarberFirstTipSeen or 0) == 0:
            return (
                "Серджио с самого порога понижает голос и ухмыляется: \"Запомните первую хорошую шутку цирюльника, сударь. "
                "Домашнее мыло не только грязь смывает. Если дама моется им как следует, все у нее становится и чище, и аккуратнее, и уже, где надо. "
                "А если в мыло еще втереть хорошее оливковое масло, получится уже не простая деревенская болванка, а вещь почти роскошная. Такое я и сам куплю охотно.\""
            )
        rumors = [
            "Серджио подает вам чистое полотенце, прищуривается и почти шепчет: \"Ох, сударь, в нашем городе новости растут быстрее волос. Только успевай подравнивать и одно, и другое. Вот взять хотя бы купчиху с рынка: клянется, что продает уксус, а сама каждое утро бегает к виноделам и краснеет так, будто грешила не языком, а всем телом сразу.\"",
            "Серджио щелкает ножницами в воздухе и расплывается в улыбке: \"Город, мой добрый друг, устроен просто. Днем все торгуют честью, ночью торгуются уже без нее. Я-то знаю: ко мне приходят и приказчики, и вдовушки, и стражники. Сядут в кресло, выдохнут, а дальше сплетни текут сами, как вино из плохо заткнутой бочки.\"",
            "Цирюльник заговорщически склоняется ближе: \"Слух, если его хорошенько причесать, всегда выглядит правдоподобно. Сегодня вот судачат, что один почтенный господин исправно ходит по лавкам будто бы по делам, а сам выбирает не товары, а тех, кто за прилавком. И ведь лицо у него при этом такое, словно он святее церковной свечки.\"",
        ]
        return str(procedural_choice(rumors, key="procedural:Town/Arts/BarberShop.rpy:procedural_choice:112:1"))

    BarberShopRoom = Room(
        code_name="BarberShop",
        group_name=ROOM_GROUP_CITY,
        display_name="Цирюльня Серджио Пета",
        bg_picture="images/barber shop/barber shop.jpg",
        descriptions=[
            RoomDescription(
                text=barber_shop_intro_text(),
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в квартал ремесленников", target="ArtisansQuarter"),
        ],
        game_items=[],
        schedule=RoomSchedule(
            closed_text="Сейчас цирюльня закрыта.",
            condition=barber_shop_is_open,
        ),
    )


label BarberShop:
    $ CurrentRoom = BarberShopRoom
    $ CurLoc = "BarberShop"
    $ location = CurLoc
    $ scene_image = barber_shop_picture_path()
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = ""
    $ GirlDressBlock = 0

    if BarberShopRoom.is_open():
        $ MainTxt = barber_shop_intro_text() + "\n\n" + barber_shop_status_text()
    else:
        $ MainTxt = barber_shop_intro_text() + "\n\n" + barber_shop_status_text()
    $ CurLocDesc = MainTxt
    $ BarberShopSavedText = MainTxt
    call ShowImage("", "", barber_shop_picture_path())

    if story_event_available("BarberShop", "clara_fiance"):
        call checkTriggers("BarberShop", "clara_fiance", 0)
        call screen main_ui
        jump BarberShop

    if not BarberShopRoom.is_open():
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        while True:
            call screen main_ui

    call BarberShopBuildActions
    while True:
        call screen main_ui


label BarberShopBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Подстричься за %d мараведи" % int(barber_shop_player_haircut_price() or 0), Call("BarberShopHaircut")))
    if barber_shop_can_buy_olive_oil():
        $ current_action_items.append(MenuItem("Купить оливковое масло за %d мараведи" % int(barber_shop_discounted_price(BARBER_OLIVE_OIL_PRICE) or 0), Call("BarberShopBuyOliveOil")))
    if barber_shop_can_refine_luxury_soap():
        $ current_action_items.append(MenuItem("Улучшить мыло оливковым маслом", Call("BarberShopRefineLuxurySoap")))
    if barber_shop_can_sell_luxury_soap():
        $ current_action_items.append(MenuItem("Продать роскошное мыло Серджио", Call("BarberShopSellLuxurySoap")))
    if barber_shop_can_serve_pending_guest():
        $ current_action_items.append(MenuItem("Оплатить визит %s к цирюльнику" % barber_shop_pending_npc_name(), Call("BarberShopServePendingGuest")))
    python:
        for _room_exit in BarberShopRoom.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, Jump(_room_exit.target)))
    return


label BarberShopTalk:
    $ Sergio.mark_known()
    $ MainTxt = barber_shop_talk_text()
    if int(BarberFirstTipSeen or 0) == 0:
        $ BarberFirstTipSeen = 1
    $ CurLocDesc = MainTxt
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return


label BarberShopHaircut:
    $ _restriction_text = str(action_restriction_text(None, 5, (4, 5), None) or "")
    if str(_restriction_text or "").strip() != "":
        $ MainTxt = _restriction_text
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return

    if barber_shop_player_recent_haircut():
        $ MainTxt = "Я совсем недавно уже приводил волосы в порядок. Серджио только хмыкает и говорит, что сейчас максимум можно испортить хорошую стрижку, а не улучшить ее."
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return

    $ _barber_price = int(barber_shop_player_haircut_price() or 0)
    if int(money or 0) < _barber_price:
        $ MainTxt = "Серджио сочувственно разводит руками: \"С такими карманами, сударь, мне остается только пожалеть ваши волосы. Возвращайтесь, когда при вас будет хотя бы %d мараведи.\" " % _barber_price
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return

    $ money -= _barber_price
    $ calendar_v2.advance_minutes(30)
    $ player_state().appearance.mark_haircut(int(dayspassed or 0))
    $ player_state().appearance.apply_to_store()
    $ update_stat_state()
    $ MainTxt = "Серджио долго щелкает ножницами, приглаживает волосы душистой водой и, не умолкая, пересказывает вам свежие городские сплетни. Когда он заканчивает, вы выглядите куда опрятнее, а карман худеет на %d мараведи." % _barber_price
    $ CurLocDesc = MainTxt
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return


label BarberShopBuyOliveOil:
    $ _olive_oil_price = int(barber_shop_discounted_price(BARBER_OLIVE_OIL_PRICE) or 0)
    if int(money or 0) < _olive_oil_price:
        $ MainTxt = "Серджио покачивает маленький пузатый пузырек и сочувственно хмыкает: \"Оливковое масло у меня не из воздуха берется. Возвращайтесь с %d мараведи.\" " % _olive_oil_price
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return
    $ money -= _olive_oil_price
    $ _player_add_item_by_id("olive_oil_001", 1)
    $ MainTxt = "Серджио продает вам маленький пузырек оливкового масла и советует беречь его не только для кухни: \"Хорошее масло и волосы пригладит, и мыло благороднее сделает.\""
    $ CurLocDesc = MainTxt
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return


label BarberShopRefineLuxurySoap:
    if not barber_shop_can_refine_luxury_soap():
        $ MainTxt = "У вас нет под рукой и домашнего мыла, и оливкового масла одновременно."
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return
    $ _player_remove_item_by_id("soap_001", 1)
    $ _player_remove_item_by_id("olive_oil_001", 1)
    $ _player_add_item_by_id("luxury_soap_001", 1)
    $ calendar_v2.advance_minutes(20)
    $ MainTxt = "Серджио показывает, как осторожно втереть оливковое масло в уже готовое мыло. Брусок становится глаже, пахнет мягче и выглядит куда дороже простого домашнего куска. У вас теперь есть роскошное мыло."
    $ CurLocDesc = MainTxt
    call stat
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return


label BarberShopSellLuxurySoap:
    if not barber_shop_can_sell_luxury_soap():
        $ MainTxt = "Продавать сейчас нечего."
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return
    $ _player_remove_item_by_id("luxury_soap_001", 1)
    $ money += int(BARBER_LUXURY_SOAP_BUY_PRICE or 0)
    $ MainTxt = "Серджио довольно крутит брусок в пальцах, нюхает его и без лишних торгов выкладывает вам %d мараведи. \"Вот это уже товар, а не просто мыло. Такое и я с удовольствием поставлю у себя на полку,\" признает он." % int(BARBER_LUXURY_SOAP_BUY_PRICE or 0)
    $ CurLocDesc = MainTxt
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return


label BarberShopServePendingGuest:
    $ _barber_guest = barber_shop_pending_npc_id()
    if str(_barber_guest or "") == "":
        $ MainTxt = "Сейчас никто из ваших знакомых не ждет визита к Серджио."
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return
    $ _barber_guest_name = str(RealName.get(_barber_guest, _barber_guest) or _barber_guest)
    $ _barber_guest_price = int(barber_shop_haircut_price("female") or 0)
    if int(money or 0) < _barber_guest_price:
        $ MainTxt = "Серджио разводит руками: \"За %s я возьмусь с радостью, но мои ножницы не работают в долг. Нужны %d мараведи.\" " % (_barber_guest_name, _barber_guest_price)
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return
    $ money -= _barber_guest_price
    $ calendar_v2.advance_minutes(45)
    $ BarberInvitePending[_barber_guest] = 0
    $ _barber_progress = npc_record_barber_visit(_barber_guest)
    $ BarberVisitLastDay[_barber_guest] = int(dayspassed or 0)
    $ _barber_guest_info = getPersonInfo(_barber_guest)
    if _barber_guest_info is not None:
        $ _barber_guest_info.change_social(friend_delta=int(_barber_progress.get("friend_delta", 0) or 0), open_delta=int(_barber_progress.get("openness_delta", 0) or 0), corruption_delta=int(_barber_progress.get("corruption_delta", 0) or 0))
    $ beauty[_barber_guest] = min(100, int(beauty.get(_barber_guest, 0) or 0) + 3)
    if _barber_guest == "sandra":
        $ cooking[_barber_guest] = min(100, int(cooking.get(_barber_guest, 0) or 0) + 1)
        $ cleaning[_barber_guest] = min(100, int(cleaning.get(_barber_guest, 0) or 0) + 1)
    elif _barber_guest == "melissa":
        $ cleaning[_barber_guest] = min(100, int(cleaning.get(_barber_guest, 0) or 0) + 1)
        $ waitress[_barber_guest] = min(100, int(waitress.get(_barber_guest, 0) or 0) + 1)
    elif _barber_guest == "amanda":
        $ waitress[_barber_guest] = min(100, int(waitress.get(_barber_guest, 0) or 0) + 2)
    $ tavernfame = int(tavernfame or 0) + 1
    $ _barber_progress_text = barber_shop_guest_progress_text(_barber_guest, _barber_progress)
    $ MainTxt = "Вы приводите %s к Серджио и оплачиваете визит. Цирюльник долго возится с волосами, душистой водой и острыми ножницами, при этом без остановки болтая о женщинах, тканях, нижнем белье и о том, как ухоженный вид меняет весь дом. Когда все заканчивается, %s выглядит заметно ухоженнее и явно уходит от Серджио с новыми мыслями о себе." % (_barber_guest_name, _barber_guest_name)
    if str(_barber_progress_text or "").strip() != "":
        $ MainTxt += "\n\n" + str(_barber_progress_text)
    $ CurLocDesc = MainTxt
    call stat
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return
