    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = CurrentRoom.build_exit_items()
        while True:
            call screen main_ui
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = CurrentRoom.build_exit_items()
        while True:
            call screen main_ui
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = CurrentRoom.build_exit_items()
        while True:
            call screen main_ui
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = CurrentRoom.build_exit_items()
        while True:
            call screen main_ui
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = CurrentRoom.build_exit_items()
        while True:
            call screen main_ui
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = CurrentRoom.build_exit_items()
        while True:
            call screen main_ui
# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# WineStore.rpy
# Converted from WineStore.txt
# Handles the wine store location and menu logic

init python:
    def wine_store_seller_id():
        if str(getLocation("clara") or "") == "WineStore" and bool(npc_can_talk_now("clara")):
            return "clara"
        if str(getLocation("alber") or "") == "WineStore" and bool(npc_can_talk_now("alber")):
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
            picture = clara_wine_store_talk_picture()
        elif seller_id == "alber":
            picture = alber_random_portrait()
        else:
            picture = str(WineStoreRoom.bg_picture or "")
        if str(picture or "").strip():
            return picture
        return "images/clara/wineSellar_clara_talk.png"

    def wine_store_entry_text():
        base_text = WineStoreRoom.descriptions[0].text
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
            if Alber.var_int("FightYouAmanda", 0) == 0:
                base_text += "\n\nЗа прилавком стоит сам хозяин погребка, мессир Альбер Легаре. Это высокий импозантный мужчина тридцати с лишним лет. Вы знаете, что он женат и у него семья. Его старшая дочка, Кларисса, помогает ему в погребке по утрам."
            else:
                fight_text = "вашу ругань" if Alber.var_int("FightYouAmanda", 0) == 2 else "ваш с ним небольшой дружеский спарринг"
                base_text += "\n\nЗа прилавком стоит сам хозяин, месье Легаре. И он очень мрачно смотрит на вас. Похоже, он принял %s близко к сердцу." % fight_text
            base_text += "\n\nВы можете с ним поболтать."
        else:
            base_text += "\n\nСейчас у прилавка никого нет."
        return base_text

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

    WineStoreRoom = Room(
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
            start="08:00",
            end="18:00",
            closed_text="В это время погребок закрыт.",
        ),
        custom_properties={
            "shop_feature": "wine",
        },
    )

label WineStore:
    scene black
    $ CurrentRoom = WineStoreRoom
    $ CurLoc = CurrentRoom.code_name
    $ scene_image = wine_store_scene_picture()
    $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    if not CurrentRoom.is_open():
        $ MainTxt = CurrentRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ scene_image = "images/general/closedVenue default.png"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ current_action_items = CurrentRoom.build_exit_items()
        while True:
            call screen main_ui

    call RoomEnterEventGate(CurLoc, False)
    $ MainTxt = wine_store_entry_text()
    $ CurLocDesc = MainTxt
    vscene scene_image

    $ CurLocDesc = MainTxt
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _wine_object_row in CurrentRoom.visible_objects():
            current_action_items.append(MenuItem(_wine_object_row.name, Call("WineStoreObjectMenu", _wine_object_row.object_id)))
    if story_event_available("WineStore", "clara_paintings"):
        $ current_action_items.append(MenuItem("Поговорить с Клариссой о рисунках", Call("checkTriggers", "WineStore", "clara_paintings", 0)))
    $ current_action_items.extend(CurrentRoom.build_exit_items())
    $ CurrentRoom.mark_visited()
    while True:
        call screen main_ui


label WineStoreObjectMenu(object_id="", preserve_text=False):
    $ _wine_object = wine_store_find_object(object_id)
    if _wine_object is None:
        $ current_action_items = []
    python:
        for _wine_object_row in CurrentRoom.visible_objects():
            current_action_items.append(MenuItem(_wine_object_row.name, Call("WineStoreObjectMenu", _wine_object_row.object_id)))
    if story_event_available("WineStore", "clara_paintings"):
        $ current_action_items.append(MenuItem("Поговорить с Клариссой о рисунках", Call("checkTriggers", "WineStore", "clara_paintings", 0)))
    $ current_action_items.extend(CurrentRoom.build_exit_items())
        return
    $ current_object_id = str(object_id or "")
    $ current_action_title = str(_wine_object.name or "")
    $ current_action_content = None
    if not preserve_text:
        $ MainTxt = str(_wine_object.description or "")
        $ CurLocDesc = MainTxt
    $ current_action_items = []
    python:
        for _wine_action in _wine_object.visible_actions():
            if _wine_action.hook == "text":
                current_action_items.append(MenuItem(_wine_action.label, Call("WineStoreObjectText", object_id, _wine_action.action_id)))
            else:
                _wine_item = room_action_menu_item(_wine_action)
                if _wine_item is not None:
                    current_action_items.append(_wine_item)
    $ current_action_items.append(MenuItem("Назад", [SetVariable("current_action_title", "Действия"), SetVariable("current_action_content", None), SetVariable("current_action_items", wine_store_action_items()), Function(main_ui_restart_interaction)]))
    return


label WineStoreObjectText(object_id="", action_id=""):
    $ _wine_object = wine_store_find_object(object_id)
    if _wine_object is not None:
        python:
            for _wine_action in _wine_object.visible_actions():
                if str(_wine_action.action_id or "") == str(action_id or ""):
                    MainTxt = str(_wine_action.target or "")
                    CurLocDesc = MainTxt
                    break
    call WineStoreObjectMenu(object_id, True)
    return


label WineStoreBuyStockMenu(result_text=""):
    $ current_action_title = "Покупка вина"
    $ current_action_content = None
    if str(result_text or "").strip():
        $ MainTxt = str(result_text or "")
    else:
        $ MainTxt = "В этом погребке вы можете купить вино для вашего трактира, по 14 мараведи за бочонок."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Ничего не покупать", Call("WineStoreBuyStockApply", 0, 0, 0))]
    if money >= 14:
        $ current_action_items.append(MenuItem("Купить один бочонок", Call("WineStoreBuyStockApply", 14, 10, 1)))
    if money >= 14 * 5:
        $ current_action_items.append(MenuItem("Купить пять бочонков", Call("WineStoreBuyStockApply", 14 * 5, 50, 5)))
    if money >= 14 * 20:
        $ current_action_items.append(MenuItem("Купить двадцать бочонков", Call("WineStoreBuyStockApply", 14 * 20, 200, 20)))
    if money >= 14 * 50:
        $ current_action_items.append(MenuItem("Купить пятьдесят бочонков", Call("WineStoreBuyStockApply", 14 * 50, 500, 50)))
    if money >= 14 * 200:
        $ current_action_items.append(MenuItem("Купить двести бочонков", Call("WineStoreBuyStockApply", 14 * 200, 2000, 200)))
    $ current_action_items.append(MenuItem("Назад", Call("WineStoreObjectMenu", "wine_stock")))
    return


label WineStoreBuyStockApply(cost=0, add_amount=0, barrel_count=0):
    if int(barrel_count or 0) == 0:
        $ MainTxt = "Вы решили пока ничего не покупать."
    else:
        $ winenum += int(add_amount or 0)
        $ money -= int(cost or 0)
        if int(barrel_count or 0) == 1:
            $ MainTxt = "Вы купили бочонок вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        elif int(barrel_count or 0) == 5:
            $ MainTxt = "Вы купили пять бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        elif int(barrel_count or 0) == 20:
            $ MainTxt = "Вы купили двадцать бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        elif int(barrel_count or 0) == 50:
            $ MainTxt = "Вы купили пятьдесят бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        else:
            $ MainTxt = "Вы купили двести бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_seller_name()
        call stat
    $ CurLocDesc = MainTxt
    call WineStoreBuyStockMenu(MainTxt)
    return
