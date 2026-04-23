init python:
    def marketplace_blind_pirate_event_available():
        return (
            int(BlindPirateMarketEventSeen or 0) == 0
            and int(dayspassed or 0) < 7
            and int(week or 0) != 7
            and int(time or 0) in (0, 1, 2)
        )

    def marketplace_becky_home_visible():
        return BeckyVar.get("visitedhome", 0) >= 2 and week != 5 and time == 3

    def marketplace_mongol_visible():
        return MyStallion == ""

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
            items.append(MenuItem(market_exit.label, Jump(market_exit.target)))

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
            {"npc_id": "clara", "condition": marketplace_clara_visible},
            {"npc_id": "mongol", "condition": marketplace_mongol_visible, "unknown_name": "Мужик в красной рубахе", "gender": "man", "can_examine_unknown": False},
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            time_slots=[0, 1, 2, 3],
            closed_text="Сейчас уже поздно и рынок закрыт.",
        ),
        custom_properties={
            "friday_dance_location": True,
            "object_menu_label": "MarketPlaceObjectMenu",
        },
    )

default BlindPirateMarketEventSeen = 0
default BlindPirateBreakfastPending = 0

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
    call CheckDailyEvent("", "_story_enter", CurLoc, time)

    # Check if it's Friday and time for the dance
    if friday_dance_market_entry_is_active():
        jump FridayDance

    # Check if it's Sunday or too late
    if week == 7:
        $ MainTxt = "Сегодня воскресенье и рынок закрыт."
        if marketplace_becky_home_visible():
            $ MainTxt += "\n\nЛавка Бекки уже закрыта, но к этому часу вы можете пройти к ней домой через боковую улочку."
        $ CurLocDesc = MainTxt
        call ShowImage("general", "", "LocMarketPlaceClosed")
        $ current_action_items = []
        if (int(MongolVar.get("StocksSeen", 0) or 0) == 1 and int(MongolVar.get("StocksFoodDay", -1) or -1) < 0 and int(time or 0) >= 4) or (int(DraupnirVar.get("MongolLockpickOrderDay", -1) or -1) >= 0 and int(MongolVar.get("StocksReleased", 0) or 0) == 0 and int(time or 0) >= 4 and int(dayspassed or 0) > int(MongolVar.get("StocksFoodDay", -1) or -1)):
            $ current_action_items.append(MenuItem("Подойти к караулке и колодкам", Jump("CityGuard")))
        if marketplace_becky_home_visible():
            $ current_action_items.append(MenuItem("Идти в гости в дом к вдове Блэнкеншип", Jump("BeckyHomeFront")))
        $ current_action_items.append(MenuItem("Вернуться к трактиру", Jump("StreetTavern")))
        jump MarketPlaceView
    elif not _market_room.is_open(week, time):
        $ MainTxt = _market_room.schedule.closed_text
        if marketplace_becky_home_visible():
            $ MainTxt += "\n\nЛавка Бекки уже закрыта, но к этому часу вы можете пройти к ней домой через боковую улочку."
        $ CurLocDesc = MainTxt
        call ShowImage("general", "", "LocMarketPlaceClosed")
        $ current_action_items = []
        if (int(MongolVar.get("StocksSeen", 0) or 0) == 1 and int(MongolVar.get("StocksFoodDay", -1) or -1) < 0 and int(time or 0) >= 4) or (int(DraupnirVar.get("MongolLockpickOrderDay", -1) or -1) >= 0 and int(MongolVar.get("StocksReleased", 0) or 0) == 0 and int(time or 0) >= 4 and int(dayspassed or 0) > int(MongolVar.get("StocksFoodDay", -1) or -1)):
            $ current_action_items.append(MenuItem("Подойти к караулке и колодкам", Jump("CityGuard")))
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

    if marketplace_blind_pirate_event_available():
        call MarketPlaceBlindPirateEvent
        call ShowImageSeq("general", "", "LocMarketPlace", 2)

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


label MarketPlaceBlindPirateEvent:
    $ BlindPirateMarketEventSeen = 1
    $ BlindPirateBreakfastPending = 1
    python:
        _blind_pirate_picture = "images/market/blindPirate.png"
        if renpy.loadable(_blind_pirate_picture):
            scene_image = _blind_pirate_picture
            _layout_last_picture = _blind_pirate_picture
        MainTxt = 'Рыночный шум вдруг меняет голос. Там, где еще секунду назад спорили о цене муки и бранились из-за тухлой рыбы, толпа сама собой расползается в стороны, словно кто-то провел по ней тяжелым ножом. Меж плеч и корзин медленно выкатывается телега с железной клеткой. Колеса стучат по камню так глухо и тяжело, будто везут не человека, а уже готовую беду.\n\nВнутри, скорчившись на сырой соломе, сидит мужчина. Лицо у него серое, провалившееся, жалкое; не лицо хозяина, а лицо человека, с которого разом содрали и достаток, и честь, и сон. В клетку летят гнилые репы, мятые кочаны, склизкие огрызки. Кто-то хохочет, кто-то орет проклятья, кто-то, напротив, отворачивается, словно стыдясь чужого несчастья, но все равно идет следом смотреть. А позади клетки, спотыкаясь и заливаясь плачем, бегут две женщины: одна совсем молоденькая, другая постарше, лет тридцати с небольшим. Обе уже выбились из сил, но все еще не могут оторвать глаз от телеги, как будто одним этим взглядом можно удержать человека от дороги к портовым галерам.\n\n«Эх, вот она как судьба-то ломает», - говорит кто-то рядом, уже без злобы, вполголоса, будто в церкви. - «Еще вчера был хозяином "Слепого Пирата" - самого бойкого трактира в городе. У него столы ломились, клиенты дрались за место, а теперь его самого гонят на галеры герцогини Кончиты за долги. Трактир выгорел до головешек, дом разорен, а весь его бабий и дворовый люд пошел по миру.»\n\nВы слушаете и чувствуете, как холодок проходит по спине. Рыночный гам снова становится просто шумом, но теперь в нем слышится уже не одно веселье. Слишком ясно становится, на какой тонкой доске стоит любой трактир и как легко под хорошим хозяином вдруг может разверзнуться пустота.'
        CurLocDesc = MainTxt
        current_action_title = "Случай на рынке"
        current_action_content = None
        current_action_items = [MenuItem("Осмотреться на рынке", Return())]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    show screen main_ui
    $ renpy.pause(hard=True)
    return


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
    if renpy.loadable("images/mongol/gipsy.png"):
        call ShowImage("", "", "images/mongol/gipsy.png")
    if mode_code == "first":
        $ KnowMongol = 1
        $ MainTxt = "Увидев, что вы направляетесь к нему, мужик обрадовался еще больше, хлопнул себя по ляжкам и воскликнул: 'Ай-нэ-нэ!'\n\nПротянув вам руку он представился: 'Монголом меня кличут. Я тут парувэла, в смысле коняшку продаю.'\n\n'Купишь ты коня прекрасного очень дешево, всего за [MongolVar['HorsePrice']] мараведи! Ну что, по рукам?'"
        $ CurLocDesc = MainTxt
    else:
        $ MainTxt = "'Стефан, друг мой, посмотри какой у меня замечательный конь! Тебе я его всего за [MongolVar['HorsePrice']] мараведи отдам!'"
        $ CurLocDesc = MainTxt
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
