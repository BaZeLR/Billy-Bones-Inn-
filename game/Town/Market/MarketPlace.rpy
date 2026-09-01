# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    MARKETPLACE_CLOSED_PICTURE = "images/market/LocMarketPlaceClosed.jpg"

    def marketplace_blind_pirate_event_ready():
        return rooms.get("MarketPlace").is_open()

    def marketplace_becky_home_visible():
        minute_now = int(calendar_v2.clock_minutes() or 0) % 1440
        if int(calendar_v2.week or 0) == 5 and rooms.get("FridayDance").dance_count >= 5:
            return rooms.get("FridayDance").becky_home_invited
        return Becky.home_visit_stage >= 2 and int(calendar_v2.week or 0) != 5 and 13 * 60 <= minute_now <= 15 * 60 + 59

    def marketplace_mongol_visible():
        return bool(Mongol.is_market_visible())

    def marketplace_stocks_visible():
        return story_event_available("menu_CityGuard", "mongol_stocks")

    def marketplace_exit_minutes(target_room=""):
        if str(target_room or "").strip() == "StreetTavern":
            return navigation_group_travel_minutes()
        return 10

    def marketplace_action_items():
        items = list(rooms.get("MarketPlace").build_action_items())
        for room_exit in rooms.get("MarketPlace").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target, marketplace_exit_minutes(room_exit.target))))
        return items

    MarketPlaceRoomDefinition = Room(
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
        game_items=[],
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
        },
    )

label MarketPlace:
    $ renpy.dynamic("_market_room")
    scene black
    $ rooms.enter("MarketPlace")
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.talk_picture = ""
    $ main_ui_runtime.clear_contexts()
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ _market_room = rooms.get("MarketPlace")
    vscene _market_room.bg_picture
    $ findAvailableEvents(forced=True)
    call checkTriggers("MarketPlace", "enter", 0)

    # Check if it's Friday and time for the dance
    if rooms.get("FridayDance").market_entry_is_active():
        jump FridayDance

    # Check if it's Sunday or too late
    if int(calendar_v2.week or 0) == 7:
        $ scene_runtime.text = "Сегодня воскресенье и рынок закрыт."
        if marketplace_becky_home_visible():
            $ scene_runtime.text += "\n\nЛавка Бекки уже закрыта, но к этому часу вы можете пройти к ней домой через боковую улочку."
        $ scene_runtime.location_text = scene_runtime.text
        $ scene_runtime.picture = MARKETPLACE_CLOSED_PICTURE
        vscene scene_runtime.picture
        $ main_ui_runtime.action_items = [MenuItem("Вернуться к трактиру", movement_actions("StreetTavern", navigation_group_travel_minutes()))]
        if marketplace_stocks_visible():
            $ main_ui_runtime.action_items.insert(0, MenuItem("Подойти к караулке и колодкам", movement_actions("CityGuard", 10)))
        if marketplace_becky_home_visible():
            $ main_ui_runtime.action_items.insert(0, MenuItem("Идти в гости в дом к вдове Блэнкеншип", movement_actions("BeckyHomeFront", 10)))
        while True:
            call screen main_ui
    elif not _market_room.is_open():
        $ scene_runtime.text = _market_room.schedule.closed_text
        if marketplace_becky_home_visible():
            $ scene_runtime.text += "\n\nЛавка Бекки уже закрыта, но к этому часу вы можете пройти к ней домой через боковую улочку."
        $ scene_runtime.location_text = scene_runtime.text
        $ scene_runtime.picture = MARKETPLACE_CLOSED_PICTURE
        vscene scene_runtime.picture
        $ main_ui_runtime.action_items = [MenuItem("Вернуться к трактиру", movement_actions("StreetTavern", navigation_group_travel_minutes()))]
        if marketplace_stocks_visible():
            $ main_ui_runtime.action_items.insert(0, MenuItem("Подойти к караулке и колодкам", movement_actions("CityGuard", 10)))
        if marketplace_becky_home_visible():
            $ main_ui_runtime.action_items.insert(0, MenuItem("Идти в гости в дом к вдове Блэнкеншип", movement_actions("BeckyHomeFront", 10)))
        while True:
            call screen main_ui

    # Restore the room-owned scene after an entry event changes its media.
    vscene _market_room.bg_picture

    # Main marketplace description
    $ scene_runtime.text = _market_room.descriptions[0].text + "\n\n" + _market_room.descriptions[1].text
    if dog.is_stray_here("MarketPlace"):
        $ scene_runtime.text += "\n\nУ одной из лавок вертится бродячий пес, внимательно следящий за руками торговцев и покупателей."
    $ scene_runtime.location_text = scene_runtime.text

    # Random encounter with Mongol
    if marketplace_mongol_visible():
        $ Mongol.reset_market_trade()

        if not Mongol.known:
            $ scene_runtime.text = "Обведя взглядом рынок, в дальнем углу вы заметили мужика в красной рубахе, высоких сапогах, серьгой в ухе и с цветной косынкой на голове. Рядом с ним стояла оседланная лошадь, повод от которой был у него в руке. Встретив ваш взгляд, мужик широко улыбнулся, блеснув золотым зубом, и призывно замахал вам рукой."
            $ scene_runtime.location_text = scene_runtime.text

        else:
            if player.horse.stolen_days == 0 or procedural_randint(1, 3, key="procedural:Town/Market/MarketPlace.rpy:procedural_randint:193:1") <= 2:
                $ scene_runtime.text = "Обведя взглядом рынок, в дальнем углу вы заметили своего старого знакомого Монгола. Как обычно, рядом с ним была очередная лошадка. Увидев вас, Монгол улыбнулся, блеснув золотым зубом, и призывно замахал вам рукой."
                $ scene_runtime.location_text = scene_runtime.text
                call ShowImageSeq("mongol", "", "portrait", 3)
            else:
                $ scene_runtime.text = "Обведя взглядом рынок, в дальнем углу вы заметили своего старого знакомого Монгола. Как обычно, рядом с ним была лошадка. И эта лошадка почему-то показалась вам очень знакомой. Завидев вас, Монгол почему-то отвернулся и быстро скрылся в каком-то переулке."
                $ scene_runtime.location_text = scene_runtime.text

    # Additional actions
    $ scene_runtime.text = scene_runtime.text + "\n\n" + _market_room.descriptions[2].text
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = marketplace_action_items()
    while True:
        call screen main_ui


# Event: the ruined Blind Pirate owner is marched through the market.
# Choice:
# - observe and continue: advances the same thread to its breakfast chapter
label story_city_blind_pirate_fall_0:
    $ scene_runtime.text = 'Рыночный шум вдруг меняет голос. Там, где еще секунду назад спорили о цене муки и бранились из-за тухлой рыбы, толпа сама собой расползается в стороны, словно кто-то провел по ней тяжелым ножом. Меж плеч и корзин медленно выкатывается телега с железной клеткой. Колеса стучат по камню так глухо и тяжело, будто везут не человека, а уже готовую беду.'
    show screen main_ui
    vscene "images/market/blindPirate.png"
    "[scene_runtime.text]"

    $ scene_runtime.text = 'Внутри, скорчившись на сырой соломе, сидит мужчина. Лицо у него серое, провалившееся, жалкое; не лицо хозяина, а лицо человека, с которого разом содрали и достаток, и честь, и сон. В клетку летят гнилые репы, мятые кочаны, склизкие огрызки. Кто-то хохочет, кто-то орет проклятья, кто-то, напротив, отворачивается, словно стыдясь чужого несчастья, но все равно идет следом смотреть. А позади клетки, спотыкаясь и заливаясь плачем, бегут две женщины: одна совсем молоденькая, другая постарше, лет тридцати с небольшим. Обе уже выбились из сил, но все еще не могут оторвать глаз от телеги, как будто одним этим взглядом можно удержать человека от дороги к портовым галерам.'
    "[scene_runtime.text]"

    $ scene_runtime.text = '«Эх, вот она как судьба-то ломает», - говорит кто-то рядом, уже без злобы, вполголоса, будто в церкви. - «Еще вчера был хозяином "Слепого Пирата" - самого бойкого трактира в городе. У него столы ломились, клиенты дрались за место, а теперь его самого гонят на галеры герцогини Кончиты за долги. Трактир выгорел до головешек, дом разорен, а весь его бабий и дворовый люд пошел по миру.»'
    "[scene_runtime.text]"

    $ scene_runtime.text = 'Вы слушаете и чувствуете, как холодок проходит по спине. Рыночный гам снова становится просто шумом, но теперь в нем слышится уже не одно веселье. Слишком ясно становится, на какой тонкой доске стоит любой трактир и как легко под хорошим хозяином вдруг может разверзнуться пустота.'
    "[scene_runtime.text]"

    menu:
        "Осмотреться на рынке":
            $ threads["cityBlindPirateFall"].advance()
            return True


label MarketPlaceApproachMongol(mode_code=""):
    $ renpy.dynamic("_mongol_horse_price")
    $ scene_runtime.picture = "images/mongol/gipsy.png"
    $ _mongol_horse_price = Mongol.horse_price
    vscene scene_runtime.picture
    if mode_code == "first":
        $ Mongol.mark_known()
        $ scene_runtime.text = "Увидев, что вы направляетесь к нему, мужик обрадовался еще больше, хлопнул себя по ляжкам и воскликнул: 'Ай-нэ-нэ!'\n\nПротянув вам руку он представился: 'Монголом меня кличут. Я тут парувэла, в смысле коняшку продаю.'\n\n'Купишь ты коня прекрасного очень дешево, всего за %d мараведи! Ну что, по рукам?'" % int(_mongol_horse_price)
        $ scene_runtime.location_text = scene_runtime.text
    else:
        $ scene_runtime.text = "'Стефан, друг мой, посмотри какой у меня замечательный конь! Тебе я его всего за %d мараведи отдам!'" % int(_mongol_horse_price)
        $ scene_runtime.location_text = scene_runtime.text
    call MongolTalk
    return


label MarketPlaceTalkMongol:
    if not Mongol.known:
        call MarketPlaceApproachMongol("first")
    else:
        call MarketPlaceApproachMongol("repeat")
    return
