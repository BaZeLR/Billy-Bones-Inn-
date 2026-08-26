# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# GroceryStore location - converted from legacy script
init python:
    import renpy.exports as renpy

    def grocery_store_active_grocer_id():
        if str(people.location("eddie") or "") == "GroceryStore":
            return "eddie"
        if str(people.location("inga") or "") == "GroceryStore":
            return "inga"
        if str(people.location("becky") or "") == "GroceryStore":
            return "becky"
        return ""

    def grocery_store_grocer_data():
        npc_id = grocery_store_active_grocer_id()
        if not npc_id:
            return {"id": "", "title": "Торговец"}
        info = people.get_info(npc_id)
        data = info.action_data("GroceryStore") if info is not None else {}
        return {"id": npc_id, "title": str(data.get("title", "") or "Торговец")}

    def grocery_store_service_available(_obj=None):
        return grocery_store_active_grocer_id() != ""

    def grocery_store_lard_visible(_obj=None):
        return player_has_soap_recipe_book()

    def grocery_store_fancy_night_bowl_visible(_obj=None):
        return Amanda.night_bowl_given and not Amanda.fancy_night_bowl_received

    def grocery_store_lard_action_visible(_obj=None):
        return grocery_store_service_available() and grocery_store_lard_visible()

    def grocery_store_fancy_night_bowl_action_visible(_obj=None):
        return grocery_store_service_available() and grocery_store_fancy_night_bowl_visible()

    def grocery_store_pick_picture(candidates, randomize=False):
        loadable = [row for row in candidates if str(row or "").strip() and renpy.loadable(row)]
        if len(loadable) <= 0:
            return ""
        if randomize:
            return procedural_choice(loadable, key="procedural:Town/GroceryStore.rpy:procedural_choice:57:1")
        return loadable[0]

    def grocery_store_eddie_picture(randomize=False):
        candidates = []
        if Becky.eddie_robbed_day > 0 and Becky.eddie_robbed_day + 12 >= current_game_day():
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
        parts = [str(rooms.get("GroceryStore").descriptions[0].text or "").strip()]

        notice = str(rooms.get("GroceryStore").state.pop("notice", "") or "")
        if notice:
            parts.append(notice)
        return "\n\n".join([row for row in parts if str(row or "").strip()])

    def grocery_store_set_notice(text=""):
        rooms.get("GroceryStore").state["notice"] = str(text or "")

    def grocery_store_find_visible_object(object_id):
        object_key = str(object_id or "")
        for room_object in rooms.get("GroceryStore").visible_objects():
            if str(getattr(room_object, "object_id", "") or "") == object_key:
                return room_object
        return None

    def grocery_store_action_items():
        items = []
        for room_object in rooms.get("GroceryStore").visible_objects():
            items.append(MenuItem(room_object.name, Call("GroceryStoreObjectMenu", room_object.object_id)))
        items.extend(rooms.get("GroceryStore").build_exit_items())
        return items

    GroceryStoreFoodStockObject = GameObject(
        object_id="food_stock",
        name="Провизия",
        description="Мешки с овощами, мясо и прочая снедь для торговли и поставок в трактир.",
        actions=[
            ObjectAction(action_id="buy_provisions", label="Купить провизию", hook="call", target="GroceryStoreBuyStockMenu", condition=grocery_store_service_available),
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

    GroceryStoreRoomDefinition = Room(
        code_name="GroceryStore",
        group_name=ROOM_GROUP_CITY,
        display_name="Продуктовая лавка",
        bg_picture="images/general/grocery_shop.png",
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
            "first_visit_seen": False,
        },
    )

label GroceryStore:
    $ renpy.dynamic("_grocery_room", "_grocery_store_event_played")
    scene black
    $ rooms.enter("GroceryStore")
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.talk_picture = ""
    $ main_ui_runtime.clear_contexts()
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ _grocery_room = rooms.get("GroceryStore")
    $ scene_runtime.picture = _grocery_room.bg_picture
    vscene scene_runtime.picture
    # Check if the store is closed
    if not _grocery_room.is_open():
        $ scene_runtime.text = _grocery_room.schedule.closed_text
        $ scene_runtime.location_text = scene_runtime.text
        $ scene_runtime.picture = "images/general/closedVenue default.png"
        vscene scene_runtime.picture
        $ main_ui_runtime.action_items = rooms.get("GroceryStore").build_exit_items()
        while True:
            call screen main_ui
    
    $ scene_runtime.text = grocery_store_main_text()
    $ scene_runtime.location_text = scene_runtime.text

    if grocery_store_active_grocer_id() == "becky":
        call BeckyLoversInStore
        $ _grocery_store_event_played = bool(_return)
        if _grocery_store_event_played:
            $ main_ui_runtime.mode = "scene"
            $ scene_runtime.picture = _grocery_room.bg_picture
            vscene scene_runtime.picture
            $ scene_runtime.text = _grocery_room.descriptions[0].text
            $ scene_runtime.location_text = scene_runtime.text
        call check_daily_event('becky')
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = grocery_store_action_items()
    $ rooms.get("GroceryStore").custom_properties["first_visit_seen"] = True
    while True:
        call screen main_ui


label GroceryStoreObjectMenu(object_id="", preserve_text=False):
    $ renpy.dynamic("_grocery_object")
    $ renpy.dynamic("_grocery_action")
    $ _grocery_object = grocery_store_find_visible_object(object_id)
    if _grocery_object is None:
        $ main_ui_runtime.action_items = grocery_store_action_items()
        return
    $ main_ui_runtime.object_id = str(object_id or "")
    $ main_ui_runtime.action_title = str(_grocery_object.name or "")
    $ main_ui_runtime.action_content = None
    if not preserve_text:
        if str(object_id or "") == "food_stock":
            $ scene_runtime.picture = grocery_store_grocer_picture()
            if str(scene_runtime.picture or "").strip():
                vscene scene_runtime.picture
        $ scene_runtime.text = str(_grocery_object.description or "")
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = []
    python:
        for _grocery_action in _grocery_object.visible_actions():
            if _grocery_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_grocery_action.label, Call("GroceryStoreObjectText", object_id, _grocery_action.action_id)))
            elif _grocery_action.hook == "jump" and str(_grocery_action.target or ""):
                main_ui_runtime.action_items.append(MenuItem(_grocery_action.label, Jump(_grocery_action.target)))
            elif _grocery_action.hook == "call" and str(_grocery_action.target or ""):
                main_ui_runtime.action_items.append(MenuItem(_grocery_action.label, Call(_grocery_action.target, *tuple(_grocery_action.args or ()))))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", [SetField(scene_runtime, "picture", rooms.get("GroceryStore").bg_picture), SetField(scene_runtime, "text", rooms.get("GroceryStore").descriptions[0].text), SetField(scene_runtime, "location_text", rooms.get("GroceryStore").descriptions[0].text), SetField(main_ui_runtime, "action_title", "Действия"), SetField(main_ui_runtime, "action_content", None), SetField(main_ui_runtime, "action_items", grocery_store_action_items()), SetField(main_ui_runtime, "object_id", "")]))
    return


label GroceryStoreObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_grocery_object")
    $ renpy.dynamic("_grocery_action")
    $ _grocery_object = grocery_store_find_visible_object(object_id)
    if _grocery_object is not None:
        python:
            for _grocery_action in _grocery_object.visible_actions():
                if str(_grocery_action.action_id or "") == str(action_id or ""):
                    scene_runtime.text = str(_grocery_action.target or "")
                    scene_runtime.location_text = scene_runtime.text
                    break
    call GroceryStoreObjectMenu(object_id, True)
    return


label GroceryStoreBuyStockMenu(preserve_text=False):
    $ main_ui_runtime.action_title = "Покупка провизии"
    $ main_ui_runtime.action_content = None
    if not preserve_text:
        $ scene_runtime.text = "В этой лавке вы можете купить провизию для вашего трактира, по 6 мараведи за мешок."
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = [MenuItem("Ничего не покупать", Call("GroceryStoreObjectMenu", "food_stock", True))]
    if player.economy.money >= 6:
        $ main_ui_runtime.action_items.append(MenuItem("Купить один мешок", Call("GroceryStoreBuyStockApply", 6, 10, 1)))
    if player.economy.money >= 6 * 5:
        $ main_ui_runtime.action_items.append(MenuItem("Купить пять мешков", Call("GroceryStoreBuyStockApply", 6 * 5, 50, 5)))
    if player.economy.money >= 6 * 20:
        $ main_ui_runtime.action_items.append(MenuItem("Купить двадцать мешков", Call("GroceryStoreBuyStockApply", 6 * 20, 200, 20)))
    if player.economy.money >= 6 * 50:
        $ main_ui_runtime.action_items.append(MenuItem("Купить пятьдесят мешков", Call("GroceryStoreBuyStockApply", 6 * 50, 500, 50)))
    if player.economy.money >= 6 * 200:
        $ main_ui_runtime.action_items.append(MenuItem("Купить двести мешков", Call("GroceryStoreBuyStockApply", 6 * 200, 2000, 200)))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", Call("GroceryStoreObjectMenu", "food_stock", True)))

    return


label GroceryStoreBuyStockApply(cost=0, add_amount=0, bag_count=0):
    $ renpy.dynamic("_grocer_title")
    $ _grocer_title = str(grocery_store_grocer_data().get("title", "") or "Торговец")
    if int(bag_count or 0) == 0:
        $ scene_runtime.text = "Вы решили пока ничего не покупать."
        call stat
    else:
        $ player.tavern_management.productnum += int(add_amount or 0)
        $ player.spend_money(int(cost or 0))
        if int(bag_count or 0) == 1:
            $ scene_runtime.text = "Вы купили мешок продуктов. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % _grocer_title
        elif int(bag_count or 0) == 5:
            $ scene_runtime.text = "Вы купили пять мешков продуктов. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % _grocer_title
        elif int(bag_count or 0) == 20:
            $ scene_runtime.text = "Вы купили двадцать мешков продуктов. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % _grocer_title
        elif int(bag_count or 0) == 50:
            $ scene_runtime.text = "Вы купили пятьдесят мешков продуктов. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % _grocer_title
        else:
            $ scene_runtime.text = "Вы купили двести мешков продуктов. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % _grocer_title
        call stat
    $ scene_runtime.location_text = scene_runtime.text
    $ grocery_store_set_notice(scene_runtime.text)
    call GroceryStoreBuyStockMenu(True)
    return


label GroceryStoreBuyFancyNightBowl(preserve_text=False):
    $ main_ui_runtime.action_title = "Красивая ночная миска"
    $ main_ui_runtime.action_content = None
    if not preserve_text:
        $ scene_runtime.text = "Среди простой хозяйственной утвари вы замечаете аккуратную расписную ночную миску. Она выглядит куда приятнее той грубой посудины, к которой привыкла Аманда."
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = []
    if int(player.item_count("fancy_night_bowl_001") or 0) <= 0 and int(player.economy.money or 0) >= 9:
        $ main_ui_runtime.action_items.append(MenuItem("Купить красивую ночную миску за 9 мараведи", Call("GroceryStoreBuyFancyNightBowlApply")))
    elif int(player.item_count("fancy_night_bowl_001") or 0) > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nТакую миску вы уже купили."
        $ scene_runtime.location_text = scene_runtime.text
    else:
        $ scene_runtime.text = scene_runtime.text + "\n\nНа такую покупку сейчас не хватает денег."
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items.append(MenuItem("Назад", Call("GroceryStoreObjectMenu", "food_stock", True)))
    return


label GroceryStoreBuyFancyNightBowlApply:
    $ renpy.dynamic("_grocer_title")
    $ _grocer_title = str(grocery_store_grocer_data().get("title", "") or "Торговец")
    if int(player.item_count("fancy_night_bowl_001") or 0) > 0:
        $ scene_runtime.text = "У вас уже есть такая миска."
    elif int(player.economy.money or 0) < 9:
        $ scene_runtime.text = "У вас не хватает денег на эту покупку."
    else:
        $ player.spend_money(9)
        $ player.add_item("fancy_night_bowl_001", 1)
        $ scene_runtime.text = "%s отыскивает для вас миску получше, заворачивает ее в тряпицу и вручает покупку. Теперь у вас есть вещь, которую не стыдно подарить Аманде." % _grocer_title
        call stat
    $ scene_runtime.location_text = scene_runtime.text
    call GroceryStoreBuyFancyNightBowl(True)
    return


label GroceryStoreBuyLard:
    $ renpy.dynamic("_grocer_title")
    $ _grocer_title = str(grocery_store_grocer_data().get("title", "") or "Торговец")
    if int(player.economy.money or 0) < 5:
        $ scene_runtime.text = "%s говорит, что кусок хорошего свиного сала обойдется вам в 5 мараведи, а сейчас у вас таких денег под рукой нет." % _grocer_title
    else:
        $ player.spend_money(5)
        $ player.add_item("pig_lard_001", 1)
        $ scene_runtime.text = "Вы покупаете у %s кусок свиного сала. Его можно пустить на стряпню или на мыло." % _grocer_title
        call stat
    $ scene_runtime.location_text = scene_runtime.text
    call GroceryStoreObjectMenu("food_stock", True)
    return


label GroceryStoreBuyMilk:
    $ renpy.dynamic("_grocer_title")
    $ _grocer_title = str(grocery_store_grocer_data().get("title", "") or "Торговец")
    if int(player.economy.money or 0) < 6:
        $ scene_runtime.text = "%s говорит, что свежая крынка молока стоит 6 мараведи, а сейчас у вас таких денег под рукой нет." % _grocer_title
    else:
        $ player.spend_money(6)
        $ player.add_item("milk_pitcher_001", 1)
        $ scene_runtime.text = "Вы покупаете у %s свежую крынку молока. Такое молоко сразу просится на кухню: с медом и кашей из него выйдет особенно мягкий общий стол." % _grocer_title
        call stat
    $ scene_runtime.location_text = scene_runtime.text
    call GroceryStoreObjectMenu("food_stock", True)
    return

