default BarberShopSavedText = ""
default BarberFirstTipSeen = 0
default BarberInvitePending = {}
default BarberVisitLastDay = {}

init python:
    BARBER_MALE_HAIRCUT_PRICE = 90
    BARBER_FEMALE_HAIRCUT_PRICE = 120
    BARBER_OLIVE_OIL_PRICE = 11
    BARBER_LUXURY_SOAP_BUY_PRICE = 22

    def barber_shop_picture_path():
        picture_path = "images/barber shop/barber shop.jpg"
        if renpy.loadable(picture_path):
            return picture_path
        return "images/general/LocArtisansQuarter1.jpg"

    def barber_shop_is_open():
        weekday = int(week or 0)
        time_slot = int(time or 0)
        return (weekday in (1, 3) and time_slot == 2) or (weekday == 6 and time_slot == 0)

    def barber_shop_haircut_price(customer_gender="male"):
        if str(customer_gender or "").strip().lower() in ("female", "woman", "girl"):
            return int(BARBER_FEMALE_HAIRCUT_PRICE or 120)
        return int(BARBER_MALE_HAIRCUT_PRICE or 90)

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
        if barber_shop_is_open():
            return "Сегодня Серджио на месте: ножницы щелкают, бритва поблескивает, а сам хозяин уже готов засыпать вас новостями."
        return "Ставни цирюльни прикрыты. Серджио принимает посетителей только {b}по понедельникам и средам после полудня{/b}, а также {b}в субботу утром{/b}."

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
        return str(renpy.random.choice(rumors))

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
    call EnterLocation("BarberShop")
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

    if BarberShopRoom.is_open(week, time):
        $ MainTxt = barber_shop_intro_text() + "\n\n" + barber_shop_status_text()
    else:
        $ MainTxt = barber_shop_intro_text() + "\n\n" + barber_shop_status_text()
    $ CurLocDesc = MainTxt
    $ BarberShopSavedText = MainTxt
    call ShowImage("", "", barber_shop_picture_path())

    if not BarberShopRoom.is_open(week, time):
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        jump BarberShopView

    call BarberShopBuildActions
    jump BarberShopView


label BarberShopView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump BarberShopView


label BarberShopBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Поговорить с Серджио", Call("BarberShopTalk")))
    $ current_action_items.append(MenuItem("Подстричься за %d мараведи" % int(barber_shop_player_haircut_price() or 0), Call("BarberShopHaircut")))
    if barber_shop_can_buy_olive_oil():
        $ current_action_items.append(MenuItem("Купить оливковое масло за %d мараведи" % int(BARBER_OLIVE_OIL_PRICE or 0), Call("BarberShopBuyOliveOil")))
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
    $ calendar_advance_minutes(30)
    $ PlayerHaircutDaySt = int(dayspassed or 0)
    $ dayssincehaircut = 0
    $ update_stat_state()
    $ MainTxt = "Серджио долго щелкает ножницами, приглаживает волосы душистой водой и, не умолкая, пересказывает вам свежие городские сплетни. Когда он заканчивает, вы выглядите куда опрятнее, а карман худеет на %d мараведи." % _barber_price
    $ CurLocDesc = MainTxt
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return


label BarberShopBuyOliveOil:
    if int(money or 0) < int(BARBER_OLIVE_OIL_PRICE or 0):
        $ MainTxt = "Серджио покачивает маленький пузатый пузырек и сочувственно хмыкает: \"Оливковое масло у меня не из воздуха берется. Возвращайтесь с %d мараведи.\" " % int(BARBER_OLIVE_OIL_PRICE or 0)
        $ CurLocDesc = MainTxt
        call ShowImage("", "", barber_shop_picture_path())
        call BarberShopBuildActions
        return
    $ money -= int(BARBER_OLIVE_OIL_PRICE or 0)
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
    $ calendar_advance_minutes(20)
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
    $ calendar_advance_minutes(45)
    $ BarberInvitePending[_barber_guest] = 0
    $ BarberVisitLastDay[_barber_guest] = int(dayspassed or 0)
    $ Friends[_barber_guest] = min(20, int(Friends.get(_barber_guest, 0) or 0) + 1)
    $ beauty[_barber_guest] = min(100, int(beauty.get(_barber_guest, 0) or 0) + 3)
    $ otkroven[_barber_guest] = min(20, int(otkroven.get(_barber_guest, 0) or 0) + 1)
    $ sluttiness[_barber_guest] = min(100, int(sluttiness.get(_barber_guest, 0) or 0) + 2)
    if _barber_guest == "sandra":
        $ cooking[_barber_guest] = min(100, int(cooking.get(_barber_guest, 0) or 0) + 1)
        $ cleaning[_barber_guest] = min(100, int(cleaning.get(_barber_guest, 0) or 0) + 1)
    elif _barber_guest == "melissa":
        $ cleaning[_barber_guest] = min(100, int(cleaning.get(_barber_guest, 0) or 0) + 1)
        $ waitress[_barber_guest] = min(100, int(waitress.get(_barber_guest, 0) or 0) + 1)
    elif _barber_guest == "amanda":
        $ waitress[_barber_guest] = min(100, int(waitress.get(_barber_guest, 0) or 0) + 2)
    $ tavernfame = int(tavernfame or 0) + 1
    $ MainTxt = "Вы приводите %s к Серджио и оплачиваете визит. Цирюльник долго возится с волосами, душистой водой и острыми ножницами, при этом без остановки болтая о женщинах, тканях, нижнем белье и о том, как ухоженный вид меняет весь дом. Когда все заканчивается, %s выглядит заметно ухоженнее и явно уходит от Серджио с новыми мыслями о себе." % (_barber_guest_name, _barber_guest_name)
    $ CurLocDesc = MainTxt
    call stat
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return
