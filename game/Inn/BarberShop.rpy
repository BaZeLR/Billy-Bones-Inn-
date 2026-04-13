default BarberShopSavedText = ""

init python:
    BARBER_MALE_HAIRCUT_PRICE = 90
    BARBER_FEMALE_HAIRCUT_PRICE = 120

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
        rumors = [
            "Серджио подает вам чистое полотенце, прищуривается и почти шепчет: \"Ох, сударь, в нашем городе новости растут быстрее волос. Только успевай подравнивать и одно, и другое. Вот взять хотя бы купчиху с рынка: клянется, что продает уксус, а сама каждое утро бегает к виноделам и краснеет так, будто грешила не языком, а всем телом сразу.\"",
            "Серджио щелкает ножницами в воздухе и расплывается в улыбке: \"Город, мой добрый друг, устроен просто. Днем все торгуют честью, ночью торгуются уже без нее. Я-то знаю: ко мне приходят и приказчики, и вдовушки, и стражники. Сядут в кресло, выдохнут, а дальше сплетни текут сами, как вино из плохо заткнутой бочки.\"",
            "Цирюльник заговорщически склоняется ближе: \"Слух, если его хорошенько причесать, всегда выглядит правдоподобно. Сегодня вот судачат, что один почтенный господин исправно ходит по лавкам будто бы по делам, а сам выбирает не товары, а тех, кто за прилавком. И ведь лицо у него при этом такое, словно он святее церковной свечки.\"",
        ]
        return str(renpy.random.choice(rumors))

    BarberShopRoom = Room(
        code_name="BarberShop",
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
        npcs=[],
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
    python:
        for _room_exit in BarberShopRoom.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, Jump(_room_exit.target)))
    return


label BarberShopTalk:
    $ MainTxt = barber_shop_talk_text()
    $ CurLocDesc = MainTxt
    call ShowImage("", "", barber_shop_picture_path())
    call BarberShopBuildActions
    return


label BarberShopHaircut:
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
