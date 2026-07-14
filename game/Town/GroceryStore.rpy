    def grocery_store_restore_scene_state():
        global MainTxt, CurLocDesc
        room_text = grocery_store_main_text()
        MainTxt = room_text
        CurLocDesc = room_text
        main_ui_restore_room_scene_state()
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        $ _grocery_ui_return = None
        while _grocery_ui_return is None:
            call screen main_ui
            $ _grocery_ui_return = _return
        jump GroceryStore

    # Assign grocer name
    if grocery_store_active_grocer_id() == "eddie":
        $ GrocerName = 'Эдди'
    elif grocery_store_active_grocer_id() == "inga":
        $ GrocerName = 'Ингенборг'
    elif grocery_store_active_grocer_id() == "becky":
        $ GrocerName = 'Бекки'
    else:
        $ GrocerName = 'хозяин лавки'
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        call screen main_ui
        $ current_action_items.append(MenuItem("Назад", Call("GroceryStoreObjectMenu", "food_stock")))
    return
        def grocery_store_restore_scene_state():
        global MainTxt, CurLocDesc
        room_text = grocery_store_main_text()
        MainTxt = room_text
        CurLocDesc = room_text
        main_ui_restore_room_scene_state()
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        $ _grocery_ui_return = None
        while _grocery_ui_return is None:
            call screen main_ui
            $ _grocery_ui_return = _return
        jump GroceryStore

    # Assign grocer name
    if grocery_store_active_grocer_id() == "eddie":
        $ GrocerName = 'Эдди'
    elif grocery_store_active_grocer_id() == "inga":
        $ GrocerName = 'Ингенборг'
    elif grocery_store_active_grocer_id() == "becky":
        $ GrocerName = 'Бекки'
    else:
        $ GrocerName = 'хозяин лавки'
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        call screen main_ui
        $ current_action_items.append(MenuItem("Назад", Call("GroceryStoreObjectMenu", "food_stock")))
    return
        def grocery_store_restore_scene_state():
        global MainTxt, CurLocDesc
        room_text = grocery_store_main_text()
        MainTxt = room_text
        CurLocDesc = room_text
        main_ui_restore_room_scene_state()
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        $ _grocery_ui_return = None
        while _grocery_ui_return is None:
            call screen main_ui
            $ _grocery_ui_return = _return
        jump GroceryStore

    # Assign grocer name
    if grocery_store_active_grocer_id() == "eddie":
        $ GrocerName = 'Эдди'
    elif grocery_store_active_grocer_id() == "inga":
        $ GrocerName = 'Ингенборг'
    elif grocery_store_active_grocer_id() == "becky":
        $ GrocerName = 'Бекки'
    else:
        $ GrocerName = 'хозяин лавки'
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        call screen main_ui
        $ current_action_items.append(MenuItem("Назад", Call("GroceryStoreObjectMenu", "food_stock")))
    return
    # ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# GroceryStore location - converted from legacy script
init python:
    import renpy.exports as renpy

    def grocery_store_active_grocer_id():
        if str(getLocation("eddie") or "") == "GroceryStore":
            return "eddie"
        if str(getLocation("inga") or "") == "GroceryStore":
            return "inga"
        if str(getLocation("becky") or "") == "GroceryStore":
            return "becky"
        return ""

    def grocery_store_service_available(_obj=None):
        return grocery_store_active_grocer_id() != ""

    def grocery_store_lard_visible(_obj=None):
        return player_has_soap_recipe_book()

    def grocery_store_fancy_night_bowl_visible(_obj=None):
        return Amanda.var_int("gave_night_bowl", 0) == 1 and Amanda.var_int("got_fancy_night_bowl", 0) == 0

    def grocery_store_lard_action_visible(_obj=None):
        return grocery_store_service_available() and grocery_store_lard_visible()

    def grocery_store_fancy_night_bowl_action_visible(_obj=None):
        return grocery_store_service_available() and grocery_store_fancy_night_bowl_visible()

    def grocery_store_background_picture():
        active_grocer = grocery_store_active_grocer_id()
        if active_grocer == "eddie":
            picture = grocery_store_eddie_picture()
        elif active_grocer == "inga":
            picture = grocery_store_inga_picture()
        elif active_grocer == "becky":
            picture = grocery_store_becky_picture()
        else:
            picture = ""
        if str(picture or "").strip():
            return picture
        if active_grocer == "eddie":
            return "images/eddie/portraits/portrait_0.png"
        if active_grocer == "inga":
            return "images/inga/StreetSex/minet1.jpg"
        if active_grocer == "becky":
            return "images/becky/portraits/portrait_1.png"
        return "images/general/becky_inStore.png"

    def grocery_store_pick_picture(candidates, randomize=False):
        loadable = [row for row in candidates if str(row or "").strip() and renpy.loadable(row)]
        if len(loadable) <= 0:
            return ""
        if randomize:
            return procedural_choice(loadable, key="procedural:Town/GroceryStore.rpy:procedural_choice:57:1")
        return loadable[0]

    def grocery_store_eddie_picture(randomize=False):
        candidates = []
        if Becky.var.get("EddieRobbedDay", 0) > 0 and Becky.var.get("EddieRobbedDay", 0) + 12 >= current_game_day():
            candidates.append("images/eddie/portraits/fingal.png")
        candidates.extend([
            "images/eddie/portraits/portrait_0.png",
            "images/eddie/portraits/portrait_1.png",
            "images/eddie/portraits/portrait_2.png",
            "images/eddie/portraits/surprised.png",
            "images/eddie/portraits/embarassed.png",
            "images/general/Eddie.jpg",
            "images/general/eddie_2.png",
            "images/general/Eddie fingal.png",
        ])
        return grocery_store_pick_picture(candidates, randomize)

    def grocery_store_becky_picture(randomize=False):
        candidates = [
            "images/becky/portraits/portrait_1.png",
            "images/becky/portraits/portrait_2.png",
            "images/becky/portraits/portrait_3.png",
            "images/becky/portraits/portrait_4.png",
            "images/becky/portraits/portrait_close.png",
            "images/becky/portraits/portrate_1.png",
            "images/general/becky_inStore.png",
            "images/general/backy in store_1.png",
        ]
        return grocery_store_pick_picture(candidates, randomize)

    def grocery_store_inga_picture(randomize=False):
        candidates = [
            str(girl_card_portrait_path("inga") or ""),
            "images/inga/StreetSex/minet1.jpg",
        ]
        return grocery_store_pick_picture(candidates, randomize)

    def grocery_store_grocer_picture(npc_id=""):
        npc_key = str(npc_id or grocery_store_active_grocer_id() or "").strip().lower()
        if npc_key == "eddie":
            return grocery_store_eddie_picture(True)
        if npc_key == "inga":
            return grocery_store_inga_picture(True)
        if npc_key == "becky":
            return grocery_store_becky_picture(True)
        return ""

    def grocery_store_main_text():
        parts = [str(GroceryStoreRoom.descriptions[0].text or "").strip()]
        active_grocer = grocery_store_active_grocer_id()

        if active_grocer == "eddie":
            parts.append("Сейчас утро, и за прилавком стоит Эдди, управляющий лавкой Блэнкеншип. Это здоровый рыжий парень примерно вашего возраста; Бекки когда-то подобрала его сиротой и взяла помощником.")
            if Becky.var.get("EddieRobbedDay", 0) > 0 and Becky.var.get("EddieRobbedDay", 0) + 12 >= current_game_day():
                parts.append("Вы заметили, что у Эдди красуется большой синяк под глазом и распухло ухо.")
            parts.append("Вы можете с ним поболтать.")
        elif active_grocer == "inga":
            parts.append("Утреннюю смену у прилавка сегодня держит Ингенборг. Старшая дочка Бекки выглядит как молодая копия своей матери и уверенно распоряжается в семейной лавке.")
            parts.append("Вы можете с ней поболтать.")
        elif active_grocer == "becky":
            parts.append("За прилавком стоит сама Бекки Блэнкеншип. Это высокая рыжая женщина с полной грудью, ей на вид немного меньше сорока. Ее муж умер от болезни примерно за год до того, как ваш дядя купил \"Дикого Жеребца\".")
            parts.append("Вы можете с ней поболтать.")
            if current_game_day() > 30 and current_game_day() <= 70:
                parts.append("Вы знаете, что Сандра с ней недавно подружилась.")
            elif current_game_day() > 70:
                parts.append("Она с Сандрой - лучшие подруги.")
        else:
            parts.append("Лавка открыта, но за прилавком сейчас никого нет: видно, хозяйка и ее управляющий заняты в другом месте.")

        return "\n\n".join([row for row in parts if str(row or "").strip()])

    def grocery_store_find_visible_object(object_id):
        object_key = str(object_id or "")
        for room_object in GroceryStoreRoom.visible_objects():
            if str(getattr(room_object, "object_id", "") or "") == object_key:
                return room_object
        return None

    def grocery_store_object_menu_payload(object_id):
        room_object = grocery_store_find_visible_object(object_id)
        if room_object is None:
            return None

        menu_items = []
        for room_action in room_object.visible_actions():
            if room_action.hook == "text":
                menu_items.append(MenuItem(room_action.label, Call("GroceryStoreObjectText", object_id, room_action.action_id)))
            elif room_action.hook == "jump" and str(room_action.target or "") != "":
                menu_items.append(MenuItem(room_action.label, Jump(room_action.target)))
            elif room_action.hook == "call" and str(room_action.target or "") != "":
                action_args = tuple(getattr(room_action, "args", ()) or ())
                menu_items.append(MenuItem(room_action.label, Call(room_action.target, *action_args)))

        return {
            "name": str(getattr(room_object, "name", "") or ""),
            "description": str(getattr(room_object, "description", "") or ""),
            "items": menu_items,
        }

    def grocery_store_object_text_payload(object_id, action_id):
        room_object = grocery_store_find_visible_object(object_id)
        if room_object is None:
            return "", ""

        object_name = str(getattr(room_object, "name", "") or "")
        action_key = str(action_id or "")
        for room_action in room_object.visible_actions():
            if str(getattr(room_action, "action_id", "") or "") == action_key:
                return str(room_action.target or ""), object_name

        return "", object_name

    GroceryStoreFoodStockObject = GameObject(
        object_id="food_stock",
        name="Провизия",
        description="Мешки с овощами, мясо и прочая снедь для торговли и поставок в трактир.",
        actions=[
            ObjectAction(action_id="buy_provisions", label="Купить провизию", hook="call", target="GroceryStoreBuyMenu", condition=grocery_store_service_available),
            ObjectAction(action_id="buy_lard", label="Купить свиное сало", hook="call", target="GroceryStoreBuyLard", condition=grocery_store_lard_action_visible),
            ObjectAction(action_id="buy_milk", label="Купить крынку молока", hook="call", target="GroceryStoreBuyMilk", condition=grocery_store_service_available),
            ObjectAction(action_id="buy_fancy_night_bowl", label="Купить красивую ночную миску", hook="call", target="GroceryStoreBuyFancyNightBowl", condition=grocery_store_fancy_night_bowl_action_visible),
            ObjectAction(action_id="examine_food_stock", label="Осмотреть товар", hook="text", target="Мешки, капуста, туши в леднике. Все как и положено в приличной продуктовой лавке."),
        ],
    )

    GroceryStoreColdRoomObject = GameObject(
        object_id="cold_room",
        name="Ледниковая комната",
        description="Через приоткрытую дверь виден холодный ледник с запасами мяса.",
        actions=[
            ObjectAction(action_id="examine_cold_room", label="Осмотреть ледник", hook="text", target="Внутри прохладно и темно, на крюках висят туши, подготовленные к продаже."),
        ],
    )

    GroceryStoreRoom = Room(
        code_name="GroceryStore",
        group_name=ROOM_GROUP_CITY,
        display_name="Продуктовая лавка",
        bg_picture="images/general/becky_inStore.png",
        descriptions=[
            RoomDescription(
                text="Вы в лавке вдовы Блэнкеншип. По всей лавке навалены мешки с овощами, сложены кочаны капусты, сквозь приоткрытую дверь, ведущую в ледниковую комнату, видны коровьи и свиные туши.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на рынок", target="MarketPlace", minutes_to_pass=10),
        ],
        game_items=[
            GroceryStoreFoodStockObject,
            GroceryStoreColdRoomObject,
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            start="06:00",
            end="17:59",
            closed_text="В это время лавка закрыта.",
        ),
        custom_properties={
            "shop_feature": "provisions",
            "object_menu_label": "GroceryStoreObjectMenu",
        },
    )

label GroceryStore:
    scene black
    $ CurrentRoom = GroceryStoreRoom
    $ CurLoc = "GroceryStore"
    $ scene_image = grocery_store_background_picture()
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ _grocery_room = GroceryStoreRoom
    # Check if the store is closed
    if not _grocery_room.is_open():
        $ MainTxt = _grocery_room.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ scene_image = "images/general/closedVenue default.png"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        while True:
            call screen main_ui
    
    $ MainTxt = grocery_store_main_text()
    $ CurLocDesc = MainTxt

    # Character interaction
    if grocery_store_active_grocer_id() == "eddie":
        $ _grocery_picture = grocery_store_eddie_picture()
        if str(_grocery_picture or "").strip():
            $ scene_image = _grocery_picture
            $ _layout_last_picture = scene_image
            vscene scene_image
    elif grocery_store_active_grocer_id() == "inga":
        $ _grocery_picture = grocery_store_inga_picture()
        if str(_grocery_picture or "").strip():
            $ scene_image = _grocery_picture
            $ _layout_last_picture = scene_image
            vscene scene_image
    elif grocery_store_active_grocer_id() == "becky":
        call BeckyLoversInStore
        $ _grocery_picture = grocery_store_becky_picture()
        if str(_grocery_picture or "").strip():
            $ scene_image = _grocery_picture
            $ _layout_last_picture = scene_image
            vscene scene_image
        # Dynamic calls for breastfeeding and kids list
        python:
            DescribeBreastFeeding('becky', 3)
            ShowFullKidsListByAge('becky', 'inga')
        call check_daily_event('becky')
    $ CurLocDesc = MainTxt
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _grocery_object in GroceryStoreRoom.visible_objects():
            current_action_items.append(MenuItem(_grocery_object.name, Function(grocery_store_open_object_menu_state, _grocery_object.object_id)))
    $ current_action_items.extend(GroceryStoreRoom.build_exit_items())
    $ GroceryStoreRoom.custom_properties["first_visit_seen"] = True
    while True:
        call screen main_ui


label GroceryStoreObjectMenu(object_id="", preserve_text=False):
    $ _grocery_object = grocery_store_find_visible_object(object_id)
    if _grocery_object is None:
        $ current_action_items = []
    python:
        for _grocery_object in GroceryStoreRoom.visible_objects():
            current_action_items.append(MenuItem(_grocery_object.name, Function(grocery_store_open_object_menu_state, _grocery_object.object_id)))
    $ current_action_items.extend(GroceryStoreRoom.build_exit_items())
        return
    $ current_object_id = str(object_id or "")
    $ current_action_title = str(_grocery_object.name or "")
    $ current_action_content = None
    if not preserve_text:
        $ MainTxt = str(_grocery_object.description or "")
        $ CurLocDesc = MainTxt
    $ current_action_items = []
    python:
        for _grocery_action in _grocery_object.visible_actions():
            if _grocery_action.hook == "text":
                current_action_items.append(MenuItem(_grocery_action.label, Call("GroceryStoreObjectText", object_id, _grocery_action.action_id)))
            elif _grocery_action.hook == "jump" and str(_grocery_action.target or ""):
                current_action_items.append(MenuItem(_grocery_action.label, Jump(_grocery_action.target)))
            elif _grocery_action.hook == "call" and str(_grocery_action.target or ""):
                current_action_items.append(MenuItem(_grocery_action.label, Call(_grocery_action.target, *tuple(_grocery_action.args or ()))))
    $ current_action_items.append(MenuItem("Назад", [SetVariable("current_action_title", "Действия"), SetVariable("current_action_content", None), SetVariable("current_action_items", grocery_store_action_items()), Function(main_ui_restart_interaction)]))
    return


label GroceryStoreObjectText(object_id="", action_id=""):
    $ _grocery_object = grocery_store_find_visible_object(object_id)
    if _grocery_object is not None:
        python:
            for _grocery_action in _grocery_object.visible_actions():
                if str(_grocery_action.action_id or "") == str(action_id or ""):
                    MainTxt = str(_grocery_action.target or "")
                    CurLocDesc = MainTxt
                    break
    call GroceryStoreObjectMenu(object_id, True)
    return


label GroceryStoreBuyStockMenu(preserve_text=False):
    $ current_action_title = "Покупка провизии"
    $ current_action_content = None
    if not preserve_text:
        $ MainTxt = "В этой лавке вы можете купить провизию для вашего трактира, по 6 мараведи за мешок."
        $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Ничего не покупать", Call("GroceryStoreBuyApply", 0, 0, 0))]
    if money >= 6:
        $ current_action_items.append(MenuItem("Купить один мешок", Call("GroceryStoreBuyApply", 6, 10, 1)))
    if money >= 6 * 5:
        $ current_action_items.append(MenuItem("Купить пять мешков", Call("GroceryStoreBuyApply", 6 * 5, 50, 5)))
    if money >= 6 * 20:
        $ current_action_items.append(MenuItem("Купить двадцать мешков", Call("GroceryStoreBuyApply", 6 * 20, 200, 20)))
    if money >= 6 * 50:
        $ current_action_items.append(MenuItem("Купить пятьдесят мешков", Call("GroceryStoreBuyApply", 6 * 50, 500, 50)))
    if money >= 6 * 200:
        $ current_action_items.append(MenuItem("Купить двести мешков", Call("GroceryStoreBuyApply", 6 * 200, 2000, 200)))

    return


label GroceryStoreBuyApply(cost=0, add_amount=0, bag_count=0):
    if int(bag_count or 0) == 0:
        $ MainTxt = "Вы решили пока ничего не покупать."
        call stat
    else:
        $ productnum += int(add_amount or 0)
        $ money -= int(cost or 0)
        if int(bag_count or 0) == 1:
            $ MainTxt = "Вы купили мешок продуктов. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        elif int(bag_count or 0) == 5:
            $ MainTxt = "Вы купили пять мешков продуктов. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        elif int(bag_count or 0) == 20:
            $ MainTxt = "Вы купили двадцать мешков продуктов. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        elif int(bag_count or 0) == 50:
            $ MainTxt = "Вы купили пятьдесят мешков продуктов. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        else:
            $ MainTxt = "Вы купили двести мешков продуктов. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        call stat
    $ CurLocDesc = MainTxt
    call GroceryStoreBuyMenu(True)
    return


label GroceryStoreBuyFancyNightBowl(preserve_text=False):
    $ current_action_title = "Красивая ночная миска"
    $ current_action_content = None
    if not preserve_text:
        $ MainTxt = "Среди простой хозяйственной утвари вы замечаете аккуратную расписную ночную миску. Она выглядит куда приятнее той грубой посудины, к которой привыкла Аманда."
        $ CurLocDesc = MainTxt
    $ current_action_items = []
    if int(player.item_count("fancy_night_bowl_001") or 0) <= 0 and int(player.economy.money or 0) >= 9:
        $ current_action_items.append(MenuItem("Купить красивую ночную миску за 9 мараведи", Call("GroceryStoreBuyFancyNightBowlApply")))
    elif int(player.item_count("fancy_night_bowl_001") or 0) > 0:
        $ MainTxt = MainTxt + "\n\nТакую миску вы уже купили."
        $ CurLocDesc = MainTxt
    else:
        $ MainTxt = MainTxt + "\n\nНа такую покупку сейчас не хватает денег."
        $ CurLocDesc = MainTxt
    $ current_action_items.append(MenuItem("Назад", Call("GroceryStoreObjectMenu", "food_stock")))
    return


label GroceryStoreBuyFancyNightBowlApply:
    if int(player.item_count("fancy_night_bowl_001") or 0) > 0:
        $ MainTxt = "У вас уже есть такая миска."
    elif int(money or 0) < 9:
        $ MainTxt = "У вас не хватает денег на эту покупку."
    else:
        $ money -= 9
        $ _player_add_item_by_id("fancy_night_bowl_001", 1)
        $ MainTxt = "[GrocerName] отыскивает для вас миску получше, заворачивает ее в тряпицу и вручает покупку. Теперь у вас есть вещь, которую не стыдно подарить Аманде."
        call stat
    $ CurLocDesc = MainTxt
    call GroceryStoreBuyFancyNightBowl(True)
    return


label GroceryStoreBuyLard:
    if int(money or 0) < 5:
        $ MainTxt = "[GrocerName] говорит, что кусок хорошего свиного сала обойдется вам в 5 мараведи, а сейчас у вас таких денег под рукой нет."
    else:
        $ money -= 5
        $ _player_add_item_by_id("pig_lard_001", 1)
        $ MainTxt = "Вы покупаете у [GrocerName] кусок свиного сала. Его можно пустить на стряпню или на мыло."
        call stat
    $ CurLocDesc = MainTxt
    call GroceryStoreObjectMenu("food_stock", True)
    return


label GroceryStoreBuyMilk:
    if int(money or 0) < 6:
        $ MainTxt = "[GrocerName] говорит, что свежая крынка молока стоит 6 мараведи, а сейчас у вас таких денег под рукой нет."
    else:
        $ money -= 6
        $ _player_add_item_by_id("milk_pitcher_001", 1)
        $ MainTxt = "Вы покупаете у [GrocerName] свежую крынку молока. Такое молоко сразу просится на кухню: с медом и кашей из него выйдет особенно мягкий общий стол."
        call stat
    $ CurLocDesc = MainTxt
    call GroceryStoreObjectMenu("food_stock", True)
    return

