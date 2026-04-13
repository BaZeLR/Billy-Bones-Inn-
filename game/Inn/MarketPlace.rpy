init python:
    def marketplace_becky_home_visible():
        return BeckyVar.get("visitedhome", 0) >= 2 and week != 5 and time == 3

    def marketplace_mongol_visible():
        return MyStallion == ""

    def marketplace_mongol_known():
        return int(KnowMongol or 0) != 0

    def marketplace_clara_visible():
        return clara_visible_in_location("MarketPlace")

    def marketplace_action_items():
        items = []

        if dog_is_here("MarketPlace"):
            items.append(MenuItem(dog_room_action_caption("MarketPlace"), Call("IntDogTalk", "MarketPlace")))

        for market_object in MarketPlaceRoom.visible_objects():
            if str(getattr(market_object, "object_id", "") or "") in ("grocery_route", "wine_route"):
                continue
            items.append(MenuItem(market_object.name, Call("MarketPlaceObjectMenu", market_object.object_id)))

        if market_mongol_visible:
            if market_mongol_mode == "first":
                items.append(MenuItem("Подойти к мужику", Call("MarketPlaceApproachMongol", "first")))
            else:
                items.append(MenuItem("Подойти к Монголу", Call("MarketPlaceApproachMongol", "repeat")))

        for market_exit in MarketPlaceRoom.visible_exits():
            if str(getattr(market_exit, "target", "") or "") in ("CityGuard",):
                continue
            items.append(MenuItem(market_exit.label, Jump(market_exit.target)))

        return items

    MarketPlaceRoom = Room(
        code_name="MarketPlace",
        display_name="Рыночная площадь",
        bg_picture="images/market/LocMarketPlace1.jpg",
        descriptions=[
            RoomDescription(
                text="Вы пришли на шумный городской рынок. Разнообразные лавки, лотки, палатки занимают всю рыночную площадь. Однако вас сейчас интересуют только две лавки - лавка вдовы Блэнкеншип, торгующей продуктами, и погребок месье Легаре, виноторговца.",
                priority=200,
            ),
            RoomDescription(
                text="В дальнем конце площади виден вход в караульную городской стражи. Рядом с ней, за неприметной дверью, есть небольшая приемная где принимают жалобы от горожан.",
                priority=190,
            ),
            RoomDescription(
                text="{b}Вечером в пятницу на площади проводятся {i}танцы{/i}, на которые собирается почти весь город.{/b}",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Идти в продуктовую лавку вдовы Блэнкеншип", target="GroceryStore"),
            RoomExit(label="Идти в винный погребок Легаре", target="WineStore"),
            RoomExit(label="Зайти в охотничий клуб", target="HunterClub"),
            RoomExit(label="Зайти к стражникам", target="CityGuard"),
            RoomExit(label="Идти в гости в дом к вдове Блэнкеншип", target="BeckyHomeFront", condition=marketplace_becky_home_visible),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[
            GameObject(
                object_id="market_stalls",
                name="Рыночные лотки",
                description="Плотно наставленные лавки и лотки образуют шумное сердце городского рынка.",
                actions=[
                    ObjectAction(action_id="examine_market_stalls", label="Осмотреть лотки", hook="text", target="Торговцы расхваливают товар наперебой, покупатели торгуются, а вокруг стоит привычный рыночный шум."),
                ],
            ),
            GameObject(
                object_id="grocery_route",
                name="Лавка Блэнкеншип",
                description="Одна из двух главных лавок на площади, куда вы регулярно заглядываете за провизией.",
                actions=[
                    ObjectAction(action_id="go_grocery", label="Идти в продуктовую лавку", hook="jump", target="GroceryStore"),
                ],
            ),
            GameObject(
                object_id="wine_route",
                name="Погребок Легаре",
                description="Винный погребок Легаре стоит прямо на площади и снабжает трактир вином.",
                actions=[
                    ObjectAction(action_id="go_wine", label="Идти в винный погребок", hook="jump", target="WineStore"),
                ],
            ),
            GameObject(
                object_id="guard_office",
                name="Приемная стражи",
                description="Неприметная дверь рядом с караулкой ведет в приемную городской стражи.",
                actions=[
                    ObjectAction(action_id="go_guard", label="Зайти к стражникам", hook="jump", target="CityGuard"),
                    ObjectAction(action_id="examine_guard_office", label="Осмотреть вход", hook="text", target="Неприметная дверь рядом с караулкой ведет в небольшую приемную, где принимают жалобы горожан."),
                ],
            ),
            GameObject(
                object_id="hunter_club_route",
                name="Охотничий клуб",
                description="За крепкой дверью рядом с лавками расположен небольшой охотничий клуб, где можно купить лесные припасы и сбыть добычу.",
                actions=[
                    ObjectAction(action_id="go_hunter_club", label="Зайти в охотничий клуб", hook="jump", target="HunterClub"),
                    ObjectAction(action_id="examine_hunter_club", label="Осмотреть дверь", hook="text", target="Тяжелая дверь украшена старой волчьей шкурой и парой кабаньих клыков. Похоже, внутри торгуют охотничьим добром и трофеями."),
                ],
            ),
        ],
        npcs=[
            {"npc_id": "clara", "name": "Кларисса", "condition": marketplace_clara_visible, "talk_label": "IntClaraTalk"},
            {"npc_id": "mongol", "name": "Монгол", "condition": marketplace_mongol_visible, "talk_label": "MarketPlaceTalkMongol", "known_condition": marketplace_mongol_known, "unknown_name": "Мужик в красной рубахе", "hide_examine_until_known": True},
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            time_slots=[0, 1, 2],
            closed_text="Сейчас уже поздно и рынок закрыт.",
        ),
        custom_properties={
            "friday_dance_location": True,
            "object_menu_label": "MarketPlaceObjectMenu",
        },
    )

label MarketPlace:
    scene black
    call EnterLocation("MarketPlace")
    $ dog_prepare_current_spawn()
    $ CurrentRoom = MarketPlaceRoom
    $ CurLoc = "MarketPlace"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ KnowMongol = int(KnowMongol or 0)
    $ _market_room = MarketPlaceRoom
    $ market_mongol_visible = 0
    $ market_mongol_mode = ""
    $ market_mongol_alley_girl = ""
    $ MarketPlaceSavedText = ""

    # Check if it's Friday and time for the dance
    if friday_dance_market_entry_is_active():
        jump FridayDance

    # Check if it's Sunday or too late
    if week == 7:
        $ MainTxt = "Сегодня воскресенье и рынок закрыт."
        $ CurLocDesc = MainTxt
        call ShowImage("general", "", "LocMarketPlaceClosed")
        $ current_action_items = []
        if marketplace_becky_home_visible():
            $ current_action_items.append(MenuItem("Идти в гости в дом к вдове Блэнкеншип", Jump("BeckyHomeFront")))
        $ current_action_items.append(MenuItem("Вернуться к трактиру", Jump("StreetTavern")))
        jump MarketPlaceView
    elif not _market_room.is_open(week, time):
        $ MainTxt = _market_room.schedule.closed_text
        $ CurLocDesc = MainTxt
        call ShowImage("general", "", "LocMarketPlaceClosed")
        $ current_action_items = []
        if marketplace_becky_home_visible():
            $ current_action_items.append(MenuItem("Идти в гости в дом к вдове Блэнкеншип", Jump("BeckyHomeFront")))
        $ current_action_items.append(MenuItem("Вернуться к трактиру", Jump("StreetTavern")))
        jump MarketPlaceView

    # Main marketplace description
    $ MainTxt = _market_room.descriptions[0].text + "\n\n" + _market_room.descriptions[1].text
    if dog_is_here("MarketPlace"):
        $ MainTxt += "\n\nУ одной из лавок вертится бродячий пес, внимательно следящий за руками торговцев и покупателей."
    if marketplace_clara_visible():
        $ MainTxt += "\n\nСреди покупателей и лавочников вы замечаете Клариссу Легаре. Похоже, она вышла на рынок по каким-то своим делам."
    $ CurLocDesc = MainTxt
    call ShowImageSeq("general", "", "LocMarketPlace", 2)

    call CheckDailyEvent("", "_story_enter", CurLoc, time)

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = []
        python:
            for _market_exit in _market_room.visible_exits():
                current_action_items.append(MenuItem(_market_exit.label, Jump(_market_exit.target)))
        jump MarketPlaceView

    # Random encounter with Mongol
    if renpy.random.randint(1, 4) == 1 and MyStallion == "":
        $ MongolVar['HorsePrice'] = 1000
        if MongolVar['ZimmerKnow']:
            $ MongolVar['HorsePrice'] += 100
        $ MongolVar['DiscountAsk'] = 0

        if KnowMongol == 0:
            $ MainTxt = "Обведя взглядом рынок, в дальнем углу вы заметили мужика в красной рубахе, высоких сапогах, серьгой в ухе и с цветной косынкой на голове. Рядом с ним стояла оседланная лошадь, повод от которой был у него в руке. Встретив ваш взгляд, мужик широко улыбнулся, блеснув золотым зубом, и призывно замахал вам рукой."
            $ CurLocDesc = MainTxt
            $ market_mongol_visible = 1
            $ market_mongol_mode = "first"

        else:
            if StolenHorseDays == 0 or renpy.random.randint(1, 3) <= 2:
                $ MainTxt = "Обведя взглядом рынок, в дальнем углу вы заметили своего старого знакомого Монгола. Как обычно, рядом с ним была очередная лошадка. Увидев вас, Монгол улыбнулся, блеснув золотым зубом, и призывно замахал вам рукой."
                $ CurLocDesc = MainTxt
                call ShowImageSeq("mongol", "", "portrait", 3)
                $ market_mongol_visible = 1
                $ market_mongol_mode = "repeat"
            else:
                $ MainTxt = "Обведя взглядом рынок, в дальнем углу вы заметили своего старого знакомого Монгола. Как обычно, рядом с ним была лошадка. И эта лошадка почему-то показалась вам очень знакомой. Завидев вас, Монгол почему-то отвернулся и быстро скрылся в каком-то переулке."
                $ CurLocDesc = MainTxt

    # Additional actions
    $ MainTxt = MainTxt + "\n\n" + _market_room.descriptions[2].text
    $ CurLocDesc = MainTxt
    $ MarketPlaceSavedText = MainTxt
    call MarketPlaceBuildActions
    jump MarketPlaceView


label MarketPlaceView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump MarketPlaceView


label MarketPlaceBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = marketplace_action_items()
    return


label MarketPlaceObjectMenu(object_id=""):
    $ _market_object = None
    python:
        for _room_object in MarketPlaceRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _market_object = _room_object
                break

    if _market_object is None:
        call MarketPlaceBuildActions
        return

    $ MainTxt = _market_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _market_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _market_action in _market_object.visible_actions():
            if _market_action.hook == "text":
                current_action_items.append(MenuItem(_market_action.label, Call("MarketPlaceObjectText", object_id, _market_action.action_id)))
            elif _market_action.hook == "call" and str(_market_action.target or "") != "":
                _market_args = tuple(getattr(_market_action, "args", ()) or ())
                current_action_items.append(MenuItem(_market_action.label, Call(_market_action.target, *_market_args)))
            elif _market_action.hook == "jump" and str(_market_action.target or "") != "":
                current_action_items.append(MenuItem(_market_action.label, Jump(_market_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("MarketPlaceRestore")))
    return


label MarketPlaceObjectText(object_id="", action_id=""):
    python:
        _object_text = ""
        _object_name = ""
        for _room_object in MarketPlaceRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _object_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _object_text = str(_room_action.target or "")
                    break
            break
        if _object_text:
            MainTxt = _object_text
            CurLocDesc = _object_text
            current_action_title = _object_name or "Действия"
    call MarketPlaceObjectMenu(object_id)
    return


label MarketPlaceApproachMongol(mode_code=""):
    if mode_code == "first":
        $ KnowMongol = 1
        $ MainTxt = "Увидев, что вы направляетесь к нему, мужик обрадовался еще больше, хлопнул себя по ляжкам и воскликнул: 'Ай-нэ-нэ!'\n\nПротянув вам руку он представился: 'Монголом меня кличут. Я тут парувэла, в смысле коняшку продаю.'\n\n'Купишь ты коня прекрасного очень дешево, всего за [MongolVar['HorsePrice']] мараведи! Ну что, по рукам?'"
        $ CurLocDesc = MainTxt
        call ShowImageSeq("mongol", "", "portrait", 3)
    else:
        $ MainTxt = "'Стефан, друг мой, посмотри какой у меня замечательный конь! Тебе я его всего за [MongolVar['HorsePrice']] мараведи отдам!'"
        $ CurLocDesc = MainTxt
        call ShowImageSeq("mongol", "", "portrait", 3)
    call MongolTalk
    return


label MarketPlaceTalkMongol:
    if int(KnowMongol or 0) == 0:
        call MarketPlaceApproachMongol("first")
    else:
        call MarketPlaceApproachMongol("repeat")
    return


label MarketPlaceRestore:
    $ MainTxt = MarketPlaceSavedText
    $ CurLocDesc = MainTxt
    call ShowImageSeq("general", "", "LocMarketPlace", 2)
    call MarketPlaceBuildActions
    return
