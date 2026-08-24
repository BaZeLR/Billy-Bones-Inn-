# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# WineStore.rpy
# Converted from WineStore.txt
# Handles the wine store location and menu logic

init python:
    def wine_store_open_now():
        current_week = int(calendar_v2.week or 0)
        current_minutes = int(calendar_v2.hour or 0) * 60 + int(calendar_v2.minute or 0)
        if current_week == 5:
            return 6 * 60 <= current_minutes <= 15 * 60
        return 6 * 60 <= current_minutes <= 17 * 60

    def wine_store_seller_id():
        if str(people.location("clara") or "") == "WineStore" and bool(people.can_talk("clara")):
            return "clara"
        if str(people.location("alber") or "") == "WineStore" and bool(people.can_talk("alber")):
            return "alber"
        return ""

    def wine_store_seller_name():
        seller_id = wine_store_seller_id()
        if seller_id == "clara":
            return "Кларисса"
        if seller_id == "alber":
            return "Альбер"
        return "продавец"

    def wine_store_scene_picture():
        seller_id = wine_store_seller_id()
        if seller_id == "clara":
            picture = Clara.wine_store_talk_picture()
        elif seller_id == "alber":
            picture = alber_random_portrait()
        else:
            picture = str(rooms.get("WineStore").bg_picture or "")
        if str(picture or "").strip():
            return picture
        return "images/clara/wineSellar_clara_talk.png"

    def wine_store_entry_text():
        base_text = rooms.get("WineStore").descriptions[0].text
        seller_id = wine_store_seller_id()
        if seller_id == "clara":
            base_text += "\n\nСейчас утро, и за прилавком стоит Кларисса, старшая дочь мессира Легаре. Это привлекательная блондинка чуть младше вас."
            if current_game_day() > 40 and current_game_day() <= 90:
                base_text += "\n\nВы знаете, что Мелисса с ней недавно подружилась."
            elif current_game_day() > 90:
                base_text += "\n\nОна с Мелиссой - лучшие подруги."
            base_text += "\n\nВы можете с ней поболтать."
            if not Clara.can_start_social_events():
                base_text += "\n\nПравда, вам кажется, что Кларисса относится к вам пока лишь как к знакомому покупателю."
        elif seller_id == "alber":
            if Alber.amanda_conflict_stage == 0:
                base_text += "\n\nЗа прилавком стоит сам хозяин погребка, мессир Альбер Легаре. Это высокий импозантный мужчина тридцати с лишним лет. Вы знаете, что он женат и у него семья. Его старшая дочка, Кларисса, помогает ему в погребке по утрам."
            else:
                fight_text = "вашу ругань" if Alber.amanda_conflict_stage == 2 else "ваш с ним небольшой дружеский спарринг"
                base_text += "\n\nЗа прилавком стоит сам хозяин, месье Легаре. И он очень мрачно смотрит на вас. Похоже, он принял %s близко к сердцу." % fight_text
            base_text += "\n\nВы можете с ним поболтать."
        else:
            base_text += "\n\nСейчас у прилавка никого нет."
        notice = str(rooms.get("WineStore").state.pop("notice", "") or "")
        return base_text + ("\n\n" + notice if notice else "")

    def wine_store_set_notice(text=""):
        rooms.get("WineStore").state["notice"] = str(text or "")

    def wine_store_find_object(object_id=""):
        object_key = str(object_id or "")
        for room_object in rooms.get("WineStore").visible_objects():
            if str(getattr(room_object, "object_id", "") or "") == object_key:
                return room_object
        return None

    def wine_store_action_items():
        items = []
        for room_object in rooms.get("WineStore").visible_objects():
            items.append(MenuItem(room_object.name, Call("WineStoreObjectMenu", room_object.object_id)))
        if story_event_available("WineStore", "clara_paintings"):
            items.append(MenuItem("Поговорить с Клариссой о рисунках", Call("checkTriggers", "WineStore", "clara_paintings", 0)))
        items.extend(rooms.get("WineStore").build_exit_items())
        return items

    WineStoreWineStockObject = GameObject(
        object_id="wine_stock",
        name="Бочки с вином",
        description="Ряды бочек и бутылок, из которых пополняются запасы вашего трактира.",
        actions=[
            ObjectAction(action_id="buy_wine", label="Купить вино", hook="call", target="WineStoreBuyStockMenu"),
            ObjectAction(action_id="examine_wine", label="Осмотреть товар", hook="text", target="Повсюду бочки, бутылки и винный дух. Сразу видно, что здесь торгуют всерьез."),
        ],
    )

    WineStoreCellarObject = GameObject(
        object_id="cellar",
        name="Подвал",
        description="Дальше вглубь уходит еще более тесный и заставленный подвал.",
        actions=[
            ObjectAction(action_id="examine_cellar", label="Осмотреть подвал", hook="text", target="Подвал забит винными запасами еще плотнее, чем сама лавка."),
        ],
    )

    WineStoreRoomDefinition = Room(
        code_name="WineStore",
        display_name="Винный погребок",
        bg_picture="images/clara/wineSellar_clara_talk.png",
        group_name=ROOM_GROUP_CITY,
        descriptions=[
            RoomDescription(
                text="Вы в винном погребке мессира Легаре. По всему погребку стоят бочки с разными винами. У задней стены расположен вход в подвал, еще больше забитый стеллажами с бутылками и огромными бочками с вином, стоящими одна на другой.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на рынок", target="MarketPlace", minutes_to_pass=10),
        ],
        game_items=[
            WineStoreWineStockObject,
            WineStoreCellarObject,
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            start="06:00",
            end="17:00",
            condition=wine_store_open_now,
            closed_text="В это время погребок закрыт.",
        ),
        custom_properties={
            "shop_feature": "wine",
        },
    )

label WineStore:
    $ renpy.dynamic("_wine_room")
    scene black
    $ rooms.enter("WineStore")
    $ scene_runtime.picture = wine_store_scene_picture()
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ _wine_room = rooms.get("WineStore")

    if not _wine_room.is_open():
        $ scene_runtime.text = rooms.current.schedule.closed_text
        $ scene_runtime.location_text = scene_runtime.text
        $ scene_runtime.picture = "images/general/closedVenue default.png"
        vscene scene_runtime.picture
        $ main_ui_runtime.action_items = rooms.current.build_exit_items()
        while True:
            call screen main_ui

    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.text = wine_store_entry_text()
    $ scene_runtime.location_text = scene_runtime.text
    vscene scene_runtime.picture

    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = wine_store_action_items()
    $ rooms.current.mark_visited()
    while True:
        call screen main_ui


label WineStoreObjectMenu(object_id="", preserve_text=False):
    $ renpy.dynamic("_wine_object")
    $ renpy.dynamic("_wine_action", "_wine_item")
    $ _wine_object = wine_store_find_object(object_id)
    if _wine_object is None:
        $ main_ui_runtime.action_items = wine_store_action_items()
        return
    $ main_ui_runtime.object_id = str(object_id or "")
    $ main_ui_runtime.action_title = str(_wine_object.name or "")
    $ main_ui_runtime.action_content = None
    if not preserve_text:
        $ scene_runtime.text = str(_wine_object.description or "")
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = []
    python:
        for _wine_action in _wine_object.visible_actions():
            if _wine_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_wine_action.label, Call("WineStoreObjectText", object_id, _wine_action.action_id)))
            else:
                _wine_item = room_action_menu_item(_wine_action)
                if _wine_item is not None:
                    main_ui_runtime.action_items.append(_wine_item)
    $ main_ui_runtime.action_items.append(MenuItem("Назад", [SetField(main_ui_runtime, "action_title", "Действия"), SetField(main_ui_runtime, "action_content", None), SetField(main_ui_runtime, "action_items", wine_store_action_items()), Function(main_ui_restart_interaction)]))
    return


label WineStoreObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_wine_object")
    $ renpy.dynamic("_wine_action")
    $ _wine_object = wine_store_find_object(object_id)
    if _wine_object is not None:
        python:
            for _wine_action in _wine_object.visible_actions():
                if str(_wine_action.action_id or "") == str(action_id or ""):
                    scene_runtime.text = str(_wine_action.target or "")
                    scene_runtime.location_text = scene_runtime.text
                    break
    call WineStoreObjectMenu(object_id, True)
    return


label WineStoreBuyStockMenu(result_text=""):
    $ main_ui_runtime.action_title = "Покупка вина"
    $ main_ui_runtime.action_content = None
    if str(result_text or "").strip():
        $ scene_runtime.text = str(result_text or "")
    else:
        $ scene_runtime.text = "В этом погребке вы можете купить вино для вашего трактира, по 14 мараведи за бочонок."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = [MenuItem("Ничего не покупать", Call("WineStoreBuyStockApply", 0, 0, 0))]
    if player.economy.money >= 14:
        $ main_ui_runtime.action_items.append(MenuItem("Купить один бочонок", Call("WineStoreBuyStockApply", 14, 10, 1)))
    if player.economy.money >= 14 * 5:
        $ main_ui_runtime.action_items.append(MenuItem("Купить пять бочонков", Call("WineStoreBuyStockApply", 14 * 5, 50, 5)))
    if player.economy.money >= 14 * 20:
        $ main_ui_runtime.action_items.append(MenuItem("Купить двадцать бочонков", Call("WineStoreBuyStockApply", 14 * 20, 200, 20)))
    if player.economy.money >= 14 * 50:
        $ main_ui_runtime.action_items.append(MenuItem("Купить пятьдесят бочонков", Call("WineStoreBuyStockApply", 14 * 50, 500, 50)))
    if player.economy.money >= 14 * 200:
        $ main_ui_runtime.action_items.append(MenuItem("Купить двести бочонков", Call("WineStoreBuyStockApply", 14 * 200, 2000, 200)))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", Call("WineStoreObjectMenu", "wine_stock", True)))
    return


label WineStoreBuyStockApply(cost=0, add_amount=0, barrel_count=0):
    if int(barrel_count or 0) == 0:
        $ scene_runtime.text = "Вы решили пока ничего не покупать."
    else:
        $ player.tavern_management.winenum += int(add_amount or 0)
        $ player.spend_money(int(cost or 0))
        if int(barrel_count or 0) == 1:
            $ scene_runtime.text = "Вы купили бочонок вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        elif int(barrel_count or 0) == 5:
            $ scene_runtime.text = "Вы купили пять бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        elif int(barrel_count or 0) == 20:
            $ scene_runtime.text = "Вы купили двадцать бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        elif int(barrel_count or 0) == 50:
            $ scene_runtime.text = "Вы купили пятьдесят бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        else:
            $ scene_runtime.text = "Вы купили двести бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        call stat
    $ scene_runtime.location_text = scene_runtime.text
    $ wine_store_set_notice(scene_runtime.text)
    call WineStoreObjectMenu("wine_stock", True)
    return
