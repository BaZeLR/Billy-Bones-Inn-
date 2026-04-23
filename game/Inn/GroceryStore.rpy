# GroceryStore location - converted from legacy script
init 4 python:
    MilkPitcherItem = GameItem(
        object_id="milk_pitcher_001",
        name="крынка молока",
        description="Свежая крынка молока из утреннего надоя. Ее можно сразу пустить на общий стол или отдать на кухню.",
        price=6,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "grocery_good",
            "grocery_kind": "milk",
        },
    )

init python:
    import random
    import renpy.exports as renpy

    def grocery_store_npc_on_shift(npc_id="", weekday_value=None, time_slot=None):
        npc_key = str(npc_id or "").strip().lower()
        if npc_key == "":
            return False
        week_now = int(week if weekday_value is None else weekday_value or 0)
        time_now = int(time if time_slot is None else time_slot or 0)
        scheduled_location = str(npc_schedule_location(npc_key, week_now, time_now) or "")
        if scheduled_location:
            return scheduled_location == "GroceryStore"
        return str(CurrentLoc.get(npc_key, "") or "") == "GroceryStore"

    def grocery_store_active_grocer_id():
        if grocery_store_npc_on_shift("eddie"):
            return "eddie"
        if grocery_store_npc_on_shift("inga"):
            return "inga"
        if grocery_store_npc_on_shift("becky"):
            return "becky"
        return ""

    def grocery_store_eddie_visible():
        return grocery_store_active_grocer_id() == "eddie"

    def grocery_store_becky_visible():
        return grocery_store_active_grocer_id() == "becky"

    def grocery_store_inga_visible():
        return grocery_store_active_grocer_id() == "inga"

    def grocery_store_service_available(_obj=None):
        return grocery_store_active_grocer_id() != ""

    def grocery_store_lard_visible(_obj=None):
        return player_has_soap_recipe_book()

    def grocery_store_fancy_night_bowl_visible(_obj=None):
        return int(AmandaVar.get("gave_night_bowl", 0) or 0) == 1 and int(AmandaVar.get("got_fancy_night_bowl", 0) or 0) == 0

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

    def grocery_store_eddie_picture():
        candidates = []
        if BeckyVar.get("EddieRobbedDay", 0) > 0 and BeckyVar.get("EddieRobbedDay", 0) + 12 >= dayspassed:
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
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def grocery_store_becky_picture():
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
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def grocery_store_inga_picture():
        candidates = [
            str(girl_card_portrait_path("inga") or ""),
            "images/inga/StreetSex/minet1.jpg",
        ]
        loadable = [row for row in candidates if str(row or "").strip() and renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def grocery_store_main_text():
        parts = [str(GroceryStoreRoom.descriptions[0].text or "").strip()]
        active_grocer = grocery_store_active_grocer_id()

        if active_grocer == "eddie":
            parts.append("Сейчас утро, и за прилавком стоит Эдди, старший сын вдовы. Это здоровый рыжий парень примерно вашего возраста.")
            if BeckyVar.get("EddieRobbedDay", 0) > 0 and BeckyVar.get("EddieRobbedDay", 0) + 12 >= dayspassed:
                parts.append("Вы заметили, что у Эдди красуется большой синяк под глазом и распухло ухо.")
            parts.append("Вы можете с ним поболтать.")
        elif active_grocer == "inga":
            parts.append("Утреннюю смену у прилавка сегодня держит Ингенборг. Старшая дочка Бекки выглядит как молодая копия своей матери и уверенно распоряжается в семейной лавке.")
            parts.append("Вы можете с ней поболтать.")
        elif active_grocer == "becky":
            parts.append("За прилавком стоит сама Бекки Блэнкеншип. Это высокая рыжая женщина с полной грудью, ей на вид немного меньше сорока. Ее муж умер от болезни примерно за год до того, как ваш отец купил \"Дикого Жеребца\".")
            parts.append("Вы можете с ней поболтать.")
            if dayspassed > 30 and dayspassed <= 70:
                parts.append("Вы знаете, что ваша мама с ней недавно подружилась.")
            elif dayspassed > 70:
                parts.append("Она с вашей мамой - лучшие подруги.")
        else:
            parts.append("Лавка открыта, но за прилавком сейчас никого нет: видно, хозяйка и ее сын заняты в другом месте.")

        return "\n\n".join([row for row in parts if str(row or "").strip()])

    def grocery_store_restore_scene_state():
        store = renpy.store
        room_text = grocery_store_main_text()
        store.MainTxt = room_text
        store.CurLocDesc = room_text
        main_ui_restore_room_scene_state()

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
            RoomExit(label="Вернуться на рынок", target="MarketPlace"),
        ],
        game_items=[
            GameObject(
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
            ),
            GameObject(
                object_id="cold_room",
                name="Ледниковая комната",
                description="Через приоткрытую дверь виден холодный ледник с запасами мяса.",
                actions=[
                    ObjectAction(action_id="examine_cold_room", label="Осмотреть ледник", hook="text", target="Внутри прохладно и темно, на крюках висят туши, подготовленные к продаже."),
                ],
            ),
        ],
        npcs=[
            {"npc_id": "eddie", "name": "Эдди", "condition": grocery_store_eddie_visible, "talk_label": "IntEddieTalk"},
            {"npc_id": "inga", "name": "Ингенборг", "condition": grocery_store_inga_visible, "talk_label": "IntIngaTalk"},
            {"npc_id": "becky", "name": "Бекки", "condition": grocery_store_becky_visible, "talk_label": "IntBeckyTalk"},
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            time_slots=[0, 1, 2, 3],
            closed_text="В это время лавка закрыта.",
        ),
        custom_properties={
            "shop_feature": "provisions",
            "object_menu_label": "GroceryStoreObjectMenu",
        },
    )

label GroceryStore:
    scene black
    call EnterLocation("GroceryStore")
    $ CurrentRoom = GroceryStoreRoom
    $ CurLoc = "GroceryStore"
    $ location = CurLoc
    $ scene_image = grocery_store_background_picture()
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ BeckyVar.setdefault("EddieRobbedDay", 0)
    $ _grocery_room = GroceryStoreRoom
    # Check if the store is closed
    if not _grocery_room.is_open(week, time):
        $ MainTxt = _grocery_room.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        jump GroceryStoreView
    
    $ MainTxt = grocery_store_main_text()
    $ CurLocDesc = MainTxt

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        jump GroceryStoreView
    
    # Assign grocer name
    if grocery_store_active_grocer_id() == "eddie":
        $ GrocerName = 'Эдди'
    elif grocery_store_active_grocer_id() == "becky":
        $ GrocerName = 'Бекки'
    else:
        $ GrocerName = 'хозяин лавки'
    
    # Character interaction
    if grocery_store_active_grocer_id() == "eddie":
        $ _grocery_picture = grocery_store_eddie_picture()
        if str(_grocery_picture or "").strip():
            call ShowImage("", "", _grocery_picture)
    elif grocery_store_active_grocer_id() == "becky":
        call BeckyLoversInStore
        $ _grocery_picture = grocery_store_becky_picture()
        if str(_grocery_picture or "").strip():
            call ShowImage("", "", _grocery_picture)
        # Dynamic calls for breastfeeding and kids list
        python:
            DescribeBreastFeeding('becky', 3)
            ShowFullKidsListByAge('becky', 'inga')
        call CheckDailyEvent('becky')
    $ CurLocDesc = MainTxt
    call GroceryStoreBuildActions
    jump GroceryStoreView


label GroceryStoreView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump GroceryStoreView


label GroceryStoreBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _grocery_object in GroceryStoreRoom.visible_objects():
            current_action_items.append(MenuItem(_grocery_object.name, Call("GroceryStoreObjectMenu", _grocery_object.object_id)))

    if grocery_store_active_grocer_id() == "eddie":
        $ current_action_items.append(MenuItem("Поговорить с Эдди", Call("IntEddieTalk")))
    elif grocery_store_active_grocer_id() == "becky":
        $ current_action_items.append(MenuItem("Поговорить с Бекки", Call("IntBeckyTalk")))

    $ current_action_items.append(MenuItem("Вернуться на рынок", Jump("MarketPlace")))
    return


label GroceryStoreObjectMenu(object_id=""):
    $ _grocery_payload = grocery_store_object_menu_payload(object_id)
    if _grocery_payload is None:
        call GroceryStoreBuildActions
        return

    $ MainTxt = _grocery_payload["description"]
    $ CurLocDesc = MainTxt
    $ current_action_title = _grocery_payload["name"]
    $ current_action_content = None
    $ current_action_items = list(_grocery_payload["items"])
    $ current_action_items.append(MenuItem("Назад", Call("GroceryStoreRestore")))
    return


label GroceryStoreObjectText(object_id="", action_id=""):
    python:
        grocery_text, grocery_name = grocery_store_object_text_payload(object_id, action_id)
        if grocery_text:
            MainTxt = grocery_text
            CurLocDesc = grocery_text
            current_action_title = grocery_name or "Действия"
    call GroceryStoreObjectMenu(object_id)
    return


label GroceryStoreBuyMenu:
    $ current_action_title = "Покупка провизии"
    $ current_action_content = None
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
    $ current_action_items.append(MenuItem("Назад", Call("GroceryStoreRestore")))
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
    call GroceryStoreBuildActions
    return


label GroceryStoreBuyFancyNightBowl:
    $ current_action_title = "Красивая ночная миска"
    $ current_action_content = None
    $ MainTxt = "Среди простой хозяйственной утвари вы замечаете аккуратную расписную ночную миску. Она выглядит куда приятнее той грубой посудины, к которой привыкла Аманда."
    $ CurLocDesc = MainTxt
    $ current_action_items = []
    if int(_player_item_count_by_id("fancy_night_bowl_001") or 0) <= 0 and int(money or 0) >= 9:
        $ current_action_items.append(MenuItem("Купить красивую ночную миску за 9 мараведи", Call("GroceryStoreBuyFancyNightBowlApply")))
    elif int(_player_item_count_by_id("fancy_night_bowl_001") or 0) > 0:
        $ MainTxt = MainTxt + "\n\nТакую миску вы уже купили."
        $ CurLocDesc = MainTxt
    else:
        $ MainTxt = MainTxt + "\n\nНа такую покупку сейчас не хватает денег."
        $ CurLocDesc = MainTxt
    $ current_action_items.append(MenuItem("Назад", Call("GroceryStoreRestore")))
    return


label GroceryStoreBuyFancyNightBowlApply:
    if int(_player_item_count_by_id("fancy_night_bowl_001") or 0) > 0:
        $ MainTxt = "У вас уже есть такая миска."
    elif int(money or 0) < 9:
        $ MainTxt = "У вас не хватает денег на эту покупку."
    else:
        $ money -= 9
        $ _player_add_item_by_id("fancy_night_bowl_001", 1)
        $ MainTxt = "[GrocerName] отыскивает для вас миску получше, заворачивает ее в тряпицу и вручает покупку. Теперь у вас есть вещь, которую не стыдно подарить Аманде."
        call stat
    $ CurLocDesc = MainTxt
    call GroceryStoreBuildActions
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
    call GroceryStoreBuildActions
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
    call GroceryStoreBuildActions
    return


label GroceryStoreRestore:
    $ grocery_store_restore_scene_state()
    call GroceryStoreBuildActions
    return
