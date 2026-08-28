# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    BARBER_MALE_HAIRCUT_PRICE = 90
    BARBER_FEMALE_HAIRCUT_PRICE = 120
    BARBER_OLIVE_OIL_PRICE = 11
    BARBER_LUXURY_SOAP_BUY_PRICE = 22

    def barber_shop_discount_percent():
        try:
            return max(0, min(90, int(tractir_progress.sergio_discount_percent or 0)))
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

    def barber_shop_is_open_at(weekday_value=None, time_value=None):
        weekday = int(calendar_v2.week if weekday_value is None else weekday_value or 0)
        current_minutes = npc_schedule_clock_minute(time_value)
        if weekday in (1, 3):
            return 12 * 60 <= current_minutes <= 17 * 60 + 59
        if weekday == 6:
            return 8 * 60 <= current_minutes <= 11 * 60 + 59
        return False

    def barber_shop_is_open():
        return barber_shop_is_open_at()

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
        for npc_id in ("sandra", "melissa", "amanda", "becky", "clara"):
            if int(household.barber_appointments.get(npc_id, 0) or 0) == 1:
                return npc_id
        return ""

    def barber_shop_pending_npc_name():
        npc_id = barber_shop_pending_npc_id()
        if npc_id == "":
            return ""
        return str(people_display_name(npc_id) or npc_id)

    def barber_shop_can_buy_olive_oil():
        return True

    def barber_shop_can_refine_luxury_soap():
        return int(player.item_count("soap_001") or 0) > 0 and int(player.item_count("olive_oil_001") or 0) > 0

    def barber_shop_can_sell_luxury_soap():
        return int(player.item_count("luxury_soap_001") or 0) > 0

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
        if not bool(rooms.get("BarberShop").state.get("first_tip_seen", False)):
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

    BarberShopRoomDefinition = Room(
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
            RoomExit(label="Вернуться в квартал ремесленников", target="ArtisansQuarter", minutes_to_pass=10),
        ],
        game_items=[],
        schedule=RoomSchedule(
            closed_text="Сейчас цирюльня закрыта.",
            condition=barber_shop_is_open,
        ),
    )


label BarberShop:
    $ rooms.enter("BarberShop")
    $ scene_runtime.picture = barber_shop_picture_path()
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.object_id = ""
    $ dress_shop.girl_dress_block = 0

    if rooms.get("BarberShop").is_open():
        $ scene_runtime.text = barber_shop_intro_text() + "\n\n" + barber_shop_status_text()
    else:
        $ scene_runtime.text = barber_shop_intro_text() + "\n\n" + barber_shop_status_text()
    $ scene_runtime.location_text = scene_runtime.text
    call ShowImage("", "", barber_shop_picture_path())

    if story_event_available("BarberShop", "clara_fiance"):
        call checkTriggers("BarberShop", "clara_fiance", 0)

    if not rooms.get("BarberShop").is_open():
        $ main_ui_runtime.action_items = rooms.get("BarberShop").build_exit_items()
        while True:
            call screen main_ui

    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = rooms.get("BarberShop").build_exit_items()
    while True:
        call screen main_ui


label BarberShopTalk:
    $ renpy.dynamic("_barber_haircut_price", "_barber_oil_price", "_barber_guest_name")
    $ Sergio.mark_known()
    $ main_ui_begin_talk_state("Разговор с Серджио", "sergio")
    $ scene_runtime.text = barber_shop_talk_text()
    if not bool(rooms.get("BarberShop").state.get("first_tip_seen", False)):
        $ rooms.get("BarberShop").state["first_tip_seen"] = True
    $ scene_runtime.location_text = scene_runtime.text
    call ShowImage("", "", barber_shop_picture_path())
    while True:
        $ _barber_haircut_price = int(barber_shop_player_haircut_price() or 0)
        $ _barber_oil_price = int(barber_shop_discounted_price(BARBER_OLIVE_OIL_PRICE) or 0)
        $ _barber_guest_name = barber_shop_pending_npc_name()
        menu:
            "Поболтать с Серджио":
                $ scene_runtime.text = barber_shop_talk_text()
                $ scene_runtime.location_text = scene_runtime.text

            "Подстричься за [_barber_haircut_price] мараведи":
                call BarberShopHaircut

            "Купить оливковое масло за [_barber_oil_price] мараведи" if barber_shop_can_buy_olive_oil():
                call BarberShopBuyOliveOil

            "Улучшить мыло оливковым маслом" if barber_shop_can_refine_luxury_soap():
                call BarberShopRefineLuxurySoap

            "Продать роскошное мыло Серджио" if barber_shop_can_sell_luxury_soap():
                call BarberShopSellLuxurySoap

            "Оплатить визит [_barber_guest_name] к цирюльнику" if barber_shop_can_serve_pending_guest():
                call BarberShopServePendingGuest

            "Назад":
                $ main_ui_end_talk_state()
                return


label BarberShopHaircut:
    $ renpy.dynamic("_restriction_text", "_barber_price")
    $ _restriction_text = str(action_restriction_text(None, 5, (4, 5), None) or "")
    if str(_restriction_text or "").strip() != "":
        $ scene_runtime.text = _restriction_text
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return

    if barber_shop_player_recent_haircut():
        $ scene_runtime.text = "Я совсем недавно уже приводил волосы в порядок. Серджио только хмыкает и говорит, что сейчас максимум можно испортить хорошую стрижку, а не улучшить ее."
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return

    $ _barber_price = int(barber_shop_player_haircut_price() or 0)
    if int(player.economy.money or 0) < _barber_price:
        $ scene_runtime.text = "Серджио сочувственно разводит руками: \"С такими карманами, сударь, мне остается только пожалеть ваши волосы. Возвращайтесь, когда при вас будет хотя бы %d мараведи.\" " % _barber_price
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return

    $ player.spend_money(_barber_price)
    $ calendar_v2.advance_minutes(30)
    $ player.appearance.mark_haircut()
    $ update_stat_state()
    $ scene_runtime.text = "Серджио долго щелкает ножницами, приглаживает волосы душистой водой и, не умолкая, пересказывает вам свежие городские сплетни. Когда он заканчивает, вы выглядите куда опрятнее, а карман худеет на %d мараведи." % _barber_price
    $ scene_runtime.location_text = scene_runtime.text
    call ShowImage("", "", barber_shop_picture_path())
    return


label BarberShopBuyOliveOil:
    $ renpy.dynamic("_olive_oil_price")
    $ _olive_oil_price = int(barber_shop_discounted_price(BARBER_OLIVE_OIL_PRICE) or 0)
    if int(player.economy.money or 0) < _olive_oil_price:
        $ scene_runtime.text = "Серджио покачивает маленький пузатый пузырек и сочувственно хмыкает: \"Оливковое масло у меня не из воздуха берется. Возвращайтесь с %d мараведи.\" " % _olive_oil_price
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return
    $ player.spend_money(_olive_oil_price)
    $ player.add_item("olive_oil_001", 1)
    $ scene_runtime.text = "Серджио продает вам маленький пузырек оливкового масла и советует беречь его не только для кухни: \"Хорошее масло и волосы пригладит, и мыло благороднее сделает.\""
    $ scene_runtime.location_text = scene_runtime.text
    call ShowImage("", "", barber_shop_picture_path())
    return


label BarberShopRefineLuxurySoap:
    if not barber_shop_can_refine_luxury_soap():
        $ scene_runtime.text = "У вас нет под рукой и домашнего мыла, и оливкового масла одновременно."
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return
    $ player.remove_item("soap_001", 1)
    $ player.remove_item("olive_oil_001", 1)
    $ player.add_item("luxury_soap_001", 1)
    $ calendar_v2.advance_minutes(20)
    $ scene_runtime.text = "Серджио показывает, как осторожно втереть оливковое масло в уже готовое мыло. Брусок становится глаже, пахнет мягче и выглядит куда дороже простого домашнего куска. У вас теперь есть роскошное мыло."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call ShowImage("", "", barber_shop_picture_path())
    return


label BarberShopSellLuxurySoap:
    if not barber_shop_can_sell_luxury_soap():
        $ scene_runtime.text = "Продавать сейчас нечего."
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return
    $ player.remove_item("luxury_soap_001", 1)
    $ player.add_money(int(BARBER_LUXURY_SOAP_BUY_PRICE or 0))
    $ scene_runtime.text = "Серджио довольно крутит брусок в пальцах, нюхает его и без лишних торгов выкладывает вам %d мараведи. \"Вот это уже товар, а не просто мыло. Такое и я с удовольствием поставлю у себя на полку,\" признает он." % int(BARBER_LUXURY_SOAP_BUY_PRICE or 0)
    $ scene_runtime.location_text = scene_runtime.text
    call ShowImage("", "", barber_shop_picture_path())
    return


label BarberShopServePendingGuest:
    $ renpy.dynamic("_barber_guest", "_barber_guest_name", "_barber_guest_price", "_barber_guest_info")
    $ _barber_guest = barber_shop_pending_npc_id()
    if str(_barber_guest or "") == "":
        $ scene_runtime.text = "Сейчас никто из ваших знакомых не ждет визита к Серджио."
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return
    $ _barber_guest_name = people_display_name(_barber_guest)
    $ _barber_guest_price = int(barber_shop_haircut_price("female") or 0)
    if int(player.economy.money or 0) < _barber_guest_price:
        $ scene_runtime.text = "Серджио разводит руками: \"За %s я возьмусь с радостью, но мои ножницы не работают в долг. Нужны %d мараведи.\" " % (_barber_guest_name, _barber_guest_price)
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImage("", "", barber_shop_picture_path())
        return
    $ player.spend_money(_barber_guest_price)
    $ calendar_v2.advance_minutes(45)
    $ household.barber_visit_last_day[_barber_guest] = current_game_day()
    $ household.barber_appointments.pop(_barber_guest, None)
    $ _barber_guest_info = people.get_info(_barber_guest)
    if _barber_guest_info is not None:
        $ _barber_guest_info.change_social(friend_delta=1, open_delta=1, corruption_delta=2)
        $ _barber_guest_info.set_sex_stat("beauty", min(100, int(_barber_guest_info.sex_stat("beauty", 0) or 0) + 3))
        if _barber_guest == "sandra":
            $ _barber_guest_info.change_skill("cooking", 1)
            $ _barber_guest_info.change_skill("cleaning", 1)
        elif _barber_guest == "melissa":
            $ _barber_guest_info.change_skill("cleaning", 1)
            $ _barber_guest_info.change_skill("waitress", 1)
        elif _barber_guest == "amanda":
            $ _barber_guest_info.change_skill("waitress", 2)
    $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 1
    $ scene_runtime.text = "Вы приводите %s к Серджио и оплачиваете визит. Цирюльник долго возится с волосами, душистой водой и острыми ножницами, при этом без остановки болтая о женщинах, тканях, нижнем белье и о том, как ухоженный вид меняет весь дом. Когда все заканчивается, %s выглядит заметно ухоженнее и явно уходит от Серджио с новыми мыслями о себе." % (_barber_guest_name, _barber_guest_name)
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call ShowImage("", "", barber_shop_picture_path())
    return
