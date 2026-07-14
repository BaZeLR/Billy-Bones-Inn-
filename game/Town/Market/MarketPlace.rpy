    def marketplace_closed_action_items():
        items = []

        if marketplace_stocks_visible():
            items.append(MenuItem("Подойти к караулке и колодкам", Call("MoveToRoom", "CityGuard", 10)))

        if marketplace_becky_home_visible():
            items.append(MenuItem("Идти в гости в дом к вдове Блэнкеншип", Call("MoveToRoom", "BeckyHomeFront", 10)))

        items.append(MenuItem("Вернуться к трактиру", Call("MoveToRoom", "StreetTavern", navigation_group_travel_minutes())))
        return items
            $ market_mongol_visible = 1
            $ market_mongol_mode = "first"                $ market_mongol_visible = 1
                $ market_mongol_mode = "repeat"    def marketplace_closed_action_items():
        items = []

        if marketplace_stocks_visible():
            items.append(MenuItem("Подойти к караулке и колодкам", Call("MoveToRoom", "CityGuard", 10)))

        if marketplace_becky_home_visible():
            items.append(MenuItem("Идти в гости в дом к вдове Блэнкеншип", Call("MoveToRoom", "BeckyHomeFront", 10)))

        items.append(MenuItem("Вернуться к трактиру", Call("MoveToRoom", "StreetTavern", navigation_group_travel_minutes())))
        return items
            $ market_mongol_visible = 1
            $ market_mongol_mode = "first"                $ market_mongol_visible = 1
                $ market_mongol_mode = "repeat"    def marketplace_closed_action_items():
        items = []

        if marketplace_stocks_visible():
            items.append(MenuItem("Подойти к караулке и колодкам", Call("MoveToRoom", "CityGuard", 10)))

        if marketplace_becky_home_visible():
            items.append(MenuItem("Идти в гости в дом к вдове Блэнкеншип", Call("MoveToRoom", "BeckyHomeFront", 10)))

        items.append(MenuItem("Вернуться к трактиру", Call("MoveToRoom", "StreetTavern", navigation_group_travel_minutes())))
        return items
            $ market_mongol_visible = 1
            $ market_mongol_mode = "first"                $ market_mongol_visible = 1
                $ market_mongol_mode = "repeat"# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    MARKETPLACE_CLOSED_PICTURE = "images/market/LocMarketPlaceClosed.jpg"

    def marketplace_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def marketplace_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def marketplace_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def marketplace_blind_pirate_event_available():
        return (
            int(BlindPirateMarketEventSeen or 0) == 0
            and MarketPlaceRoom.is_open()
        )

    def marketplace_becky_home_visible():
        minute_now = int(calendar_v2.clock_minutes() or 0) % 1440
        return Becky.var.get("visitedhome", 0) >= 2 and week != 5 and 13 * 60 <= minute_now <= 15 * 60 + 59

    def marketplace_mongol_visible():
        return bool(Mongol.is_market_visible())

    def marketplace_stocks_visible():
        minute_now = int(calendar_v2.clock_minutes() or 0) % 1440
        if marketplace_int(Mongol.var.get("StocksArrestDay", -1), -1) >= 0 and marketplace_int(Mongol.var.get("StocksSeen", 0), 0) == 0:
            return True
        return (
            (marketplace_int(Mongol.var.get("StocksSeen", 0), 0) == 1 and marketplace_int(Mongol.var.get("StocksFoodDay", -1), -1) < 0 and minute_now >= 16 * 60)
            or (
                marketplace_int(DraupnirVar.get("MongolLockpickOrderDay", -1), -1) >= 0
                and marketplace_int(Mongol.var.get("StocksReleased", 0), 0) == 0
                and minute_now >= 16 * 60
                and int(calendar_v2.daysInGame or 0) > marketplace_int(Mongol.var.get("StocksFoodDay", -1), -1)
            )
        )

    def marketplace_exit_minutes(target_room=""):
        if str(target_room or "").strip() == "StreetTavern":
            return navigation_group_travel_minutes()
        return 10

    def marketplace_action_items():
        items = list(MarketPlaceRoom.build_action_items())
        for room_exit in MarketPlaceRoom.visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target, marketplace_exit_minutes(room_exit.target))))
        return items

    MarketPlaceRoom = Room(
        code_name="MarketPlace",
        group_name=ROOM_GROUP_CITY,
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
            RoomExit(label="Идти в продуктовую лавку вдовы Блэнкеншип", target="GroceryStore", minutes_to_pass=10),
            RoomExit(label="Идти в винный погребок Легаре", target="WineStore", minutes_to_pass=10),
            RoomExit(label="Зайти в охотничий клуб", target="HunterClub", minutes_to_pass=10),
            RoomExit(label="Зайти к стражникам", target="CityGuard", minutes_to_pass=10),
            RoomExit(label="Идти в гости в дом к вдове Блэнкеншип", target="BeckyHomeFront", condition=marketplace_becky_home_visible, minutes_to_pass=10),
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
        ],
        action_menus=[
            RoomAction(action_id="mongol_stocks", label="Подойти к караулке и колодкам", hook="jump", target="CityGuard", condition=marketplace_stocks_visible),
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            start="06:00",
            end="18:59",
            closed_text="Сейчас уже поздно и рынок закрыт.",
        ),
        custom_properties={
            "friday_dance_location": True,
            "object_menu_label": "MarketPlaceObjectMenu",
        },
    )

default BlindPirateMarketEventSeen = 0
default BlindPirateBreakfastPending = 0
default MarketPlaceSavedText = ""
default market_mongol_visible = 0
default market_mongol_mode = ""
default market_mongol_alley_girl = ""

default BlindPirateMarketEventSeen = 0
default BlindPirateBreakfastPending = 0
default MarketPlaceSavedText = ""
default market_mongol_visible = 0
default market_mongol_mode = ""
default market_mongol_alley_girl = ""

default BlindPirateMarketEventSeen = 0
default BlindPirateBreakfastPending = 0
default MarketPlaceSavedText = ""
default market_mongol_visible = 0
default market_mongol_mode = ""
default market_mongol_alley_girl = ""

label MarketPlace:
    scene black
    $ dog_prepare_current_spawn()
    $ CurrentRoom = MarketPlaceRoom
    $ CurLoc = "MarketPlace"
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ KnowMongol = int(KnowMongol or 0)
    $ KnowMongol = int(KnowMongol or 0)
    $ KnowMongol = int(KnowMongol or 0)
    $ _market_room = MarketPlaceRoom
    $ market_mongol_visible = 0
    $ market_mongol_mode = ""
    $ market_mongol_alley_girl = ""
    $ MarketPlaceSavedText = ""
    $ market_mongol_visible = 0
    $ market_mongol_mode = ""
    $ market_mongol_alley_girl = ""
    $ MarketPlaceSavedText = ""
    $ market_mongol_visible = 0
    $ market_mongol_mode = ""
    $ market_mongol_alley_girl = ""
    $ MarketPlaceSavedText = ""
    if marketplace_blind_pirate_event_available():
        call MarketPlaceBlindPirateEvent
        $ _layout_last_picture = _market_room.bg_picture

    call RoomEnterEventGate(CurLoc, False)

    # Check if it's Friday and time for the dance
    if friday_dance_market_entry_is_active():
        jump FridayDance

    # Check if it's Sunday or too late
    if week == 7:
        $ MainTxt = "Сегодня воскресенье и рынок закрыт."
        if marketplace_becky_home_visible():
            $ MainTxt += "\n\nЛавка Бекки уже закрыта, но к этому часу вы можете пройти к ней домой через боковую улочку."
        $ CurLocDesc = MainTxt
        $ scene_image = "images/general/closedVenue default.png"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ current_action_items = [MenuItem("Вернуться к трактиру", Call("MoveToRoom", "StreetTavern", navigation_group_travel_minutes()))]
        if marketplace_stocks_visible():
            $ current_action_items.insert(0, MenuItem("Подойти к караулке и колодкам", Call("MoveToRoom", "CityGuard", 10)))
        if marketplace_becky_home_visible():
            $ current_action_items.insert(0, MenuItem("Идти в гости в дом к вдове Блэнкеншип", Call("MoveToRoom", "BeckyHomeFront", 10)))
        while True:
            call screen main_ui
    elif not _market_room.is_open():
        $ MainTxt = _market_room.schedule.closed_text
        if marketplace_becky_home_visible():
            $ MainTxt += "\n\nЛавка Бекки уже закрыта, но к этому часу вы можете пройти к ней домой через боковую улочку."
        $ CurLocDesc = MainTxt
        $ scene_image = "images/general/closedVenue default.png"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ current_action_items = [MenuItem("Вернуться к трактиру", Call("MoveToRoom", "StreetTavern", navigation_group_travel_minutes()))]
        if marketplace_stocks_visible():
            $ current_action_items.insert(0, MenuItem("Подойти к караулке и колодкам", Call("MoveToRoom", "CityGuard", 10)))
        if marketplace_becky_home_visible():
            $ current_action_items.insert(0, MenuItem("Идти в гости в дом к вдове Блэнкеншип", Call("MoveToRoom", "BeckyHomeFront", 10)))
        while True:
            call screen main_ui

    # Main marketplace description
    $ MainTxt = _market_room.descriptions[0].text + "\n\n" + _market_room.descriptions[1].text
    if dog_is_here("MarketPlace"):
        $ MainTxt += "\n\nУ одной из лавок вертится бродячий пес, внимательно следящий за руками торговцев и покупателей."
    $ CurLocDesc = MainTxt
    $ _layout_last_picture = _market_room.bg_picture

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = []
        python:
            for _market_exit in _market_room.visible_exits():
                current_action_items.append(MenuItem(_market_exit.label, Call("MoveToRoom", _market_exit.target, marketplace_exit_minutes(_market_exit.target))))
        call screen main_ui
        jump MarketPlace

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = []
        python:
            for _market_exit in _market_room.visible_exits():
                current_action_items.append(MenuItem(_market_exit.label, Call("MoveToRoom", _market_exit.target, marketplace_exit_minutes(_market_exit.target))))
        call screen main_ui
        jump MarketPlace

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = []
        python:
            for _market_exit in _market_room.visible_exits():
                current_action_items.append(MenuItem(_market_exit.label, Call("MoveToRoom", _market_exit.target, marketplace_exit_minutes(_market_exit.target))))
        call screen main_ui
        jump MarketPlace

    # Random encounter with Mongol
    if marketplace_mongol_visible():
        $ Mongol.reset_market_trade()

        if int(KnowMongol or 0) == 0:
            $ MainTxt = "Обведя взглядом рынок, в дальнем углу вы заметили мужика в красной рубахе, высоких сапогах, серьгой в ухе и с цветной косынкой на голове. Рядом с ним стояла оседланная лошадь, повод от которой был у него в руке. Встретив ваш взгляд, мужик широко улыбнулся, блеснув золотым зубом, и призывно замахал вам рукой."
            $ CurLocDesc = MainTxt

        else:
            if player.horse.stolen_days == 0 or procedural_randint(1, 3, key="procedural:Town/Market/MarketPlace.rpy:procedural_randint:193:1") <= 2:
                $ MainTxt = "Обведя взглядом рынок, в дальнем углу вы заметили своего старого знакомого Монгола. Как обычно, рядом с ним была очередная лошадка. Увидев вас, Монгол улыбнулся, блеснув золотым зубом, и призывно замахал вам рукой."
                $ CurLocDesc = MainTxt
                call ShowImageSeq("mongol", "", "portrait", 3)
            else:
                $ MainTxt = "Обведя взглядом рынок, в дальнем углу вы заметили своего старого знакомого Монгола. Как обычно, рядом с ним была лошадка. И эта лошадка почему-то показалась вам очень знакомой. Завидев вас, Монгол почему-то отвернулся и быстро скрылся в каком-то переулке."
                $ CurLocDesc = MainTxt

    # Additional actions
    $ MainTxt = MainTxt + "\n\n" + _market_room.descriptions[2].text
    $ CurLocDesc = MainTxt
    call MarketPlaceBuildActions
    while True:
        call screen main_ui


# Event: the ruined Blind Pirate owner is marched through the market.
# Choice:
# - observe and continue: records chapter 1, schedules the breakfast follow-up, completes the thread
label story_city_blind_pirate_fall_0:
    show screen main_ui
    vscene "images/market/blindPirate.png"

    "Рыночный шум вдруг меняет голос. Там, где еще секунду назад спорили о цене муки и бранились из-за тухлой рыбы, толпа сама собой расползается в стороны, словно кто-то провел по ней тяжелым ножом. Меж плеч и корзин медленно выкатывается телега с железной клеткой. Колеса стучат по камню так глухо и тяжело, будто везут не человека, а уже готовую беду."

    "Внутри, скорчившись на сырой соломе, сидит мужчина. Лицо у него серое, провалившееся, жалкое; не лицо хозяина, а лицо человека, с которого разом содрали и достаток, и честь, и сон. В клетку летят гнилые репы, мятые кочаны, склизкие огрызки. А позади клетки, спотыкаясь и заливаясь плачем, бегут две женщины."

    "«Эх, вот она как судьба-то ломает», — говорит кто-то рядом вполголоса. — «Еще вчера был хозяином \"Слепого Пирата\" — самого бойкого трактира в городе. А теперь его гонят на галеры за долги. Трактир выгорел, дом разорен, а весь его люд пошел по миру»."

    "Вы слушаете и чувствуете, как холодок проходит по спине. Слишком ясно становится, на какой тонкой доске стоит любой трактир."

    menu:
        "Осмотреться на рынке":
            $ player.history["blind_pirate_stage"] = 1
            $ event_runtime.active_thread.complete()
            jump MarketPlace


label MarketPlaceBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ action_menu_specs = []
    $ current_action_items = MarketPlaceRoom.build_action_items()
    python:
        for _market_exit in MarketPlaceRoom.visible_exits():
            current_action_items.append(MenuItem(_market_exit.label, Call("MoveToRoom", _market_exit.target, marketplace_exit_minutes(_market_exit.target))))
    return


label MarketPlaceBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ action_menu_specs = []
    $ current_action_items = MarketPlaceRoom.build_action_items()
    python:
        for _market_exit in MarketPlaceRoom.visible_exits():
            current_action_items.append(MenuItem(_market_exit.label, Call("MoveToRoom", _market_exit.target, marketplace_exit_minutes(_market_exit.target))))
    return


label MarketPlaceBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ action_menu_specs = []
    $ current_action_items = MarketPlaceRoom.build_action_items()
    python:
        for _market_exit in MarketPlaceRoom.visible_exits():
            current_action_items.append(MenuItem(_market_exit.label, Call("MoveToRoom", _market_exit.target, marketplace_exit_minutes(_market_exit.target))))
    return


label MarketPlaceObjectMenu(object_id="", preserve_text=False):
    $ _market_object = None
    python:
        for _room_object in MarketPlaceRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _market_object = _room_object
                break

    if _market_object is None:
        call MarketPlaceBuildActions
        return

    if not preserve_text:
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

    $ current_action_items.append(MenuItem("Назад", Jump("MarketPlace")))
    return


label MarketPlaceObjectText(object_id="", action_id=""):
    $ _market_title = "Действия"
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
            _market_title = _object_name or "Действия"
    call MarketPlaceObjectMenu(object_id, True)
    $ current_action_title = _market_title
    return


label MarketPlaceObjectMenu(object_id="", preserve_text=False):
    $ _market_object = None
    python:
        for _room_object in MarketPlaceRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _market_object = _room_object
                break

    if _market_object is None:
        call MarketPlaceBuildActions
        return

    if not preserve_text:
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

    $ current_action_items.append(MenuItem("Назад", Jump("MarketPlace")))
    return


label MarketPlaceObjectText(object_id="", action_id=""):
    $ _market_title = "Действия"
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
            _market_title = _object_name or "Действия"
    call MarketPlaceObjectMenu(object_id, True)
    $ current_action_title = _market_title
    return


label MarketPlaceObjectMenu(object_id="", preserve_text=False):
    $ _market_object = None
    python:
        for _room_object in MarketPlaceRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _market_object = _room_object
                break

    if _market_object is None:
        call MarketPlaceBuildActions
        return

    if not preserve_text:
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

    $ current_action_items.append(MenuItem("Назад", Jump("MarketPlace")))
    return


label MarketPlaceObjectText(object_id="", action_id=""):
    $ _market_title = "Действия"
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
            _market_title = _object_name or "Действия"
    call MarketPlaceObjectMenu(object_id, True)
    $ current_action_title = _market_title
    return


label MarketPlaceApproachMongol(mode_code=""):
    $ scene_image = "images/mongol/gipsy.png"
    $ _layout_last_picture = scene_image
    $ _mongol_horse_price = Mongol.var_int("HorsePrice", 1000)
    vscene scene_image
    if mode_code == "first":
        $ KnowMongol = 1
        $ MainTxt = "Увидев, что вы направляетесь к нему, мужик обрадовался еще больше, хлопнул себя по ляжкам и воскликнул: 'Ай-нэ-нэ!'\n\nПротянув вам руку он представился: 'Монголом меня кличут. Я тут парувэла, в смысле коняшку продаю.'\n\n'Купишь ты коня прекрасного очень дешево, всего за [_mongol_horse_price] мараведи! Ну что, по рукам?'"
        $ CurLocDesc = MainTxt
    else:
        $ MainTxt = "'Стефан, друг мой, посмотри какой у меня замечательный конь! Тебе я его всего за [_mongol_horse_price] мараведи отдам!'"
        $ CurLocDesc = MainTxt
    call MongolTalk
    return


label MarketPlaceTalkMongol:
    if int(KnowMongol or 0) == 0:
        call MarketPlaceApproachMongol("first")
    else:
        call MarketPlaceApproachMongol("repeat")
    return
