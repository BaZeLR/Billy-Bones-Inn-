default TavernKitchenNoticeText = ""
default TavernKitchenNoticePending = False
default TavernKitchenSavedText = ""
default BeckyKitchenVisitActive = 0
        if include_notice and bool(TavernKitchenNoticePending) and str(TavernKitchenNoticeText or "").strip():
            text_parts.append(str(TavernKitchenNoticeText or "").strip())
default TavernKitchenNoticeText = ""
default TavernKitchenNoticePending = False
default TavernKitchenSavedText = ""
default BeckyKitchenVisitActive = 0
        if include_notice and bool(TavernKitchenNoticePending) and str(TavernKitchenNoticeText or "").strip():
            text_parts.append(str(TavernKitchenNoticeText or "").strip())
default TavernKitchenNoticeText = ""
default TavernKitchenNoticePending = False
default TavernKitchenSavedText = ""
default BeckyKitchenVisitActive = 0
        if include_notice and bool(TavernKitchenNoticePending) and str(TavernKitchenNoticeText or "").strip():
            text_parts.append(str(TavernKitchenNoticeText or "").strip())
# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def tavern_kitchen_has_worker(worker_name):
        return int(jobkitchen.get(worker_name, 0))

init python:
    import re
    import renpy.exports as renpy

    def tavern_kitchen_random_sandra_scene():
        candidates = []
        for picture_index in range(5):
            picture_path = "images/tavern/kitchen/kitchen_sandra_%s.jpg" % picture_index
            if renpy.loadable(picture_path):
                candidates.append(picture_path)
        if len(candidates) == 0:
            return ""
        return procedural_choice(candidates, key="tavern_kitchen_sandra_scene_%s" % int(dayspassed or 0))

    def tavern_kitchen_picture():
        if str(getLocation("sandra") or "") == "TavernKitchen":
            sandra_scene = tavern_kitchen_random_sandra_scene()
            if sandra_scene:
                return sandra_scene
        if str(getLocation("melissa") or "") == "TavernKitchen":
            if procedural_randint(1, 4, key="tavern_kitchen_melissa_picture_%s_%s" % (int(dayspassed or 0), int(clock_minutes or 0))) == 1:
                melissa_basement = Melissa.image_path("tavern", "basement")
                if melissa_basement:
                    return melissa_basement
                if renpy.loadable("images/tavern/storage/storage_room.png"):
                    return "images/tavern/storage/storage_room.png"
                if renpy.loadable("images/tavern/kitchen/kitchen_room.png"):
                    return "images/tavern/kitchen/kitchen_room.png"
                return resolve_room_background_media(TavernKitchenRoom)
            melissa_kitchen = Melissa.image_sequence("kitchen", "work")
            if len(melissa_kitchen) > 0:
                return procedural_choice(melissa_kitchen, key="tavern_kitchen_melissa_work_%s_%s" % (int(dayspassed or 0), int(clock_minutes or 0)))
        return resolve_room_background_media(TavernKitchenRoom)

    def tavern_kitchen_pending_mandatory_event_code():
        return tavern_work_pending_mandatory_code("", "TavernKitchen")

    def tavern_kitchen_wine_donation_picture():
        sandra_scene = tavern_kitchen_random_sandra_scene()
        if sandra_scene:
            return sandra_scene
        fallback_candidates = [
            "images/sandra/tavern/kitchen_sandra_0.jpg",
            "images/sandra/tavern/kitchen_sandra_1.jpg",
            "images/sandra/tavern/kitchen_sandra_2.jpg",
            "images/sandra/tavern/kitchen_sandra_3.jpg",
            "images/sandra/tavern/kitchen_sandra_4.jpg",
            "images/sandra/sandra_kitchen.png",
        ]
        for picture_path in fallback_candidates:
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def tavern_kitchen_can_share_tea_with_sandra_and_becky():
        return npc_schedule_becky_sandra_kitchen_visit_active() and str(getLocation("sandra") or "") == "TavernKitchen" and int(player.item_count("energy_tea_001") or 0) > 0

    def tavern_kitchen_depositable_food_ids():
        return ("berries_001", "mushroom_001", "honey_comb_001", "boar_meat_001", "milk_pitcher_001")

    def tavern_kitchen_food_stock_count(item_id=""):
        item_key = str(item_id or "").strip()
        stock = tavern_storage_supplies_stock()
        if item_key == "":
            return sum(max(0, int(row or 0)) for row in list(stock.values()))
        return max(0, int(stock.get(item_key, 0) or 0))

    def tavern_kitchen_food_stock_summary():
        parts = []
        for item_id in tavern_kitchen_depositable_food_ids():
            item_count = tavern_kitchen_food_stock_count(item_id)
            if item_count <= 0:
                continue
            item_obj = get_game_item(item_id)
            item_name = str(getattr(item_obj, "name", item_id) or item_id)
            parts.append("%s x%s" % (item_name, item_count))
        return ", ".join(parts)

    def tavern_kitchen_has_depositable_food():
        for item_id in tavern_kitchen_depositable_food_ids():
            if int(player.item_count(item_id) or 0) > 0:
                return True
        return False

    def tavern_kitchen_deposit_entries():
        entries = []
        for item_id in tavern_kitchen_depositable_food_ids():
            item_count = int(player.item_count(item_id) or 0)
            if item_count <= 0:
                continue
            item_obj = get_game_item(item_id)
            item_name = str(getattr(item_obj, "name", item_id) or item_id)
            entries.append({
                "item_id": item_id,
                "count": item_count,
                "caption": "Отнести в кладовую %s x%s" % (item_name, item_count),
            })
        return entries

    def tavern_kitchen_deposit_food(item_id=""):
        item_key = str(item_id or "").strip()
        if item_key == "":
            return 0
        item_count = int(player.item_count(item_key) or 0)
        if item_count <= 0:
            return 0
        removed = player.remove_item(item_key, item_count)
        if not removed:
            return 0
        stock = tavern_storage_supplies_stock()
        stock[item_key] = max(0, int(stock.get(item_key, 0) or 0)) + item_count
        tavern_kitchen_apply_deposit_effect(item_key, item_count)
        return item_count

    def tavern_kitchen_take_food_from_stock(preferred_ids=None):
        preferred = list(preferred_ids or [])
        if len(preferred) <= 0:
            preferred = list(tavern_kitchen_depositable_food_ids())
        stock = tavern_storage_supplies_stock()
        for item_id in preferred:
            item_key = str(item_id or "").strip()
            if tavern_kitchen_food_stock_count(item_key) <= 0:
                continue
            stock[item_key] = max(0, int(stock.get(item_key, 0) or 0) - 1)
            if int(stock.get(item_key, 0) or 0) <= 0:
                stock.pop(item_key, None)
            return item_key
        return ""

    def tavern_kitchen_food_item_name(item_id=""):
        item_obj = get_game_item(str(item_id or "").strip())
        if item_obj is None:
            return str(item_id or "").strip()
        return str(getattr(item_obj, "name", item_id) or item_id)

    def tavern_kitchen_food_effect_days(effect_key=""):
        effects = tavern_storage_supplies_effects()
        return max(0, int(effects.get(str(effect_key or ""), 0) or 0))

    def tavern_kitchen_add_food_effect(effect_key="", days_value=1):
        key = str(effect_key or "").strip()
        if key == "":
            return 0
        effects = tavern_storage_supplies_effects()
        effects[key] = max(0, int(effects.get(key, 0) or 0)) + max(1, int(days_value or 1))
        return int(effects.get(key, 0) or 0)

    def tavern_kitchen_deposit_effect_text(item_id=""):
        item_key = str(item_id or "").strip()
        if item_key == "honey_comb_001":
            return "Мед сразу откладывают для сладких добавок к завтракам и напиткам. Такие угощения заметно теплят настроение в доме и делают разговоры смелее."
        if item_key == "boar_meat_001":
            return "Кабанье мясо идет в общий котел: сытная еда экономит основные припасы, но гостям под нее обычно требуется чуть больше вина."
        if item_key == "milk_pitcher_001":
            return "Свежее молоко сразу убирают в прохладу: с медом оно отлично пойдет и в кашу, и в сладкие утренние блюда."
        if item_key in ("berries_001", "mushroom_001"):
            return "Эти припасы не будут лежать мертвым грузом: их понемногу пустят в еду день за днем."
        return ""

    def tavern_kitchen_apply_deposit_effect(item_id="", item_count=0):
        item_key = str(item_id or "").strip()
        units = max(0, int(item_count or 0))
        if units <= 0:
            return ""
        if item_key == "honey_comb_001":
            tavern_kitchen_add_food_effect("honey_days", min(3, max(1, units)))
            for npc_id in ("sandra", "melissa", "amanda"):
                npc_info = peopleInfo.get(npc_id, None) if isinstance(peopleInfo, dict) else None
                if npc_info is not None:
                    npc_info.change_social(corruption_delta=2)
                    npc_info.change_mana(1, "kitchen_honey")
            return "honey"
        if item_key == "boar_meat_001":
            tavern_kitchen_add_food_effect("boar_days", min(3, max(1, units)))
            for npc_id in ("sandra", "melissa", "amanda"):
                npc_info = peopleInfo.get(npc_id, None) if isinstance(peopleInfo, dict) else None
                if npc_info is not None:
                    npc_info.change_social(corruption_delta=1)
                    npc_info.change_mana(1, "kitchen_boar")
            return "boar"
        if item_key == "milk_pitcher_001":
            tavern_kitchen_add_food_effect("milk_days", min(3, max(1, units)))
            return "milk"
        return ""

    def tavern_kitchen_consume_stock_units(units=0, preferred_ids=None):
        target = max(0, int(units or 0))
        if target <= 0:
            return 0
        stock = tavern_storage_supplies_stock()
        preferred = list(preferred_ids or ("boar_meat_001", "honey_comb_001", "berries_001", "mushroom_001", "milk_pitcher_001"))
        consumed = 0
        for item_id in preferred:
            item_key = str(item_id or "").strip()
            while consumed < target and tavern_kitchen_food_stock_count(item_key) > 0:
                stock[item_key] = max(0, int(stock.get(item_key, 0) or 0) - 1)
                consumed += 1
                if int(stock.get(item_key, 0) or 0) <= 0:
                    stock.pop(item_key, None)
            if consumed >= target:
                break
        return consumed

    def tavern_kitchen_boar_bonus_active():
        return tavern_kitchen_food_effect_days("boar_days") > 0

    def tavern_kitchen_honey_bonus_active():
        return tavern_kitchen_food_effect_days("honey_days") > 0

    def tavern_kitchen_milk_bonus_active():
        return tavern_kitchen_food_effect_days("milk_days") > 0

    def tavern_kitchen_fertility_bonus_active():
        return tavern_kitchen_honey_bonus_active() and tavern_kitchen_milk_bonus_active()

    def tavern_kitchen_daily_product_savings(base_products=0):
        base = max(0, int(base_products or 0))
        if base <= 0 or tavern_kitchen_food_stock_count() <= 0:
            return 0
        savings_percent = 20
        if tavern_kitchen_boar_bonus_active():
            savings_percent += 10
        target_units = max(1, (base * savings_percent + 99) // 100)
        return tavern_kitchen_consume_stock_units(min(target_units, tavern_kitchen_food_stock_count()))

    def tavern_kitchen_apply_daily_food_effects():
        effects = tavern_storage_supplies_effects()
        lines = []
        if tavern_kitchen_honey_bonus_active():
            for npc_id in ("sandra", "melissa", "amanda"):
                npc_info = peopleInfo.get(npc_id, None) if isinstance(peopleInfo, dict) else None
                if npc_info is not None:
                    npc_info.change_social(corruption_delta=1)
                    npc_info.change_mana(1, "kitchen_honey_daily")
            try:
                add_sex_event = TodaySexEvents_Add
            except Exception:
                add_sex_event = None
            if callable(add_sex_event) and procedural_randint(1, 3, key="tavern_kitchen_honey_mood_%s" % int(dayspassed or 0)) == 1:
                add_sex_event(procedural_choice(["sandra", "melissa", "amanda"], key="tavern_kitchen_honey_mood_target_%s" % int(dayspassed or 0)), 99, 99, "KitchenHoneyMood")
            lines.append("Медовые угощения за день заметно смягчили настроение в доме.")
        if tavern_kitchen_fertility_bonus_active():
            lines.append("Молоко с медом делает общую еду мягче, сытнее и будто бы здоровее: в доме даже начинают шутить, что от такой кухни женщин тянет к детям быстрее обычного.")
        if tavern_kitchen_boar_bonus_active():
            lines.append("Кабанье мясо сделало кухню сытнее: припасов ушло меньше, зато вина гости просили охотнее.")
        for effect_key in list(effects.keys()):
            effects[effect_key] = max(0, int(effects.get(effect_key, 0) or 0) - 1)
            if int(effects.get(effect_key, 0) or 0) <= 0:
                effects.pop(effect_key, None)
        return lines

    def tavern_kitchen_sandra_can_discuss_breakfasts():
        return str(getLocation("sandra") or "") == "TavernKitchen" and tavern_kitchen_food_stock_count() > 0 and int(Sandra.rel or 0) >= 5 and int(Sandra.asked_today or 0) == 0

    def tavern_kitchen_sandra_can_discuss_clients():
        return str(getLocation("sandra") or "") == "TavernKitchen" and tavern_kitchen_food_stock_count() > 0 and int(Sandra.rel or 0) >= 5 and int(Sandra.asked_today or 0) == 0

    TavernKitchenRoom = Room(
        code_name="TavernKitchen",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Кухня",
        bg_picture="bg TavernKitchen",
        descriptions=[
            RoomDescription(
                text="Вы заходите в кухню трактира. Здесь пахнет едой и дымом от очага.",
                first_time=True,
                priority=200,
            ),
            RoomDescription(
                text="Кухня оборудована очагом (hearth), котлом для кипячения воды (cauldron) и другими предметами.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в зал", target="TavernMain"),
            RoomExit(label="Идти в склад", target="TavernStorage"),
            RoomExit(label="Выйти на задний двор", target="Backyard"),
        ],
        game_items=[
            "hearth_001",
            "cauldron_001",
        ],
        custom_properties={},
    )

    def build_kitchen_description(include_notice=True, intro_text=""):
        room_obj = CurrentRoom if CurrentRoom is not None else TavernKitchenRoom
        room_item_ids = [get_object_id(row) for row in list(getattr(room_obj, "game_items", []) or [])]
        text_parts = []

        intro_value = str(intro_text or "").strip()
        if intro_value:
            text_parts.append(intro_value)

        # Dynamic crew from original NamesList
        kitchen_crew = NamesList("jobkitchen", "TavernKitchen")
        crew_names = str(kitchen_crew or "никто")
        if int(hour or 0) < 12:
            text_parts.append("До полудня кухня живет скорее ритмом большого двора, чем трактирной службой. Здесь собирают завтрак, ставят воду, проверяют припасы и только готовятся к дневной работе.")
            text_parts.append("На кухне с утра возятся: " + str(tavern_household_present_names("TavernKitchen") or "никто") + ".")
            if int(week or 0) == 7:
                text_parts.append("После службы здесь наверняка соберутся и на более основательную воскресную трапезу, но пока речь идет только о спокойном утреннем сборе.")
        else:
            text_parts.append("На кухне работают: " + crew_names + ".")
        $ BeckyKitchenVisitActive = 1 if becky_kitchen_visit_active() else 0
    if BeckyKitchenVisitActive:
            text_parts.append("Сегодня сюда заглянула Бекки Блэнкеншип. Она что-то негромко обсуждает с Сандрой у разделочного стола.")
        if int(week or 0) == 7 and int(time or 0) == 1:
            text_parts.append("Судя по запахам и приготовленным блюдам, Сандра решила устроить для всей трактирной челяди воскресный обед поосновательнее обычного.")
        if tavern_kitchen_food_stock_count() > 0:
            text_parts.append("В кладовой уже отложены принесенные вами припасы для кухни: %s." % tavern_kitchen_food_stock_summary())

        hearth_count = len([row for row in room_item_ids if row == "hearth_001"])
        if hearth_count > 0:
            text_parts.append("Очаг готов к использованию.")

        cauldron_count = len([row for row in room_item_ids if row == "cauldron_001"])
        if cauldron_count > 0:
            text_parts.append("Котел для кипячения воды на месте.")

        text_parts.append(werecat_visible_text("TavernKitchen"))

        return "\n".join([row for row in text_parts if str(row or "").strip()])

label TavernKitchen:
    $ CurrentRoom = TavernKitchenRoom
    $ CurLoc = "TavernKitchen"
    $ tavern_kitchen_hearth_wood_stock()
    $ scene_image = tavern_kitchen_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    call RoomEnterEventGate(CurLoc, False)
    $ current_object_id = ""
    $ current_girl_key = ""
    if player.tavern_management.breakfast.event_active:
        if str(TavernKitchenSavedText or "").strip():
            $ MainTxt = str(TavernKitchenSavedText or "")
        else:
            $ MainTxt = "Вы все еще сидите за общим утренним столом."
        $ CurLocDesc = MainTxt
        jump TavernKitchenBreakfastMenu
    $ BeckyKitchenVisitActive = 1 if becky_kitchen_visit_active() else 0
    if BeckyKitchenVisitActive:
        $ Becky.var["SandraKitchenVisitMonth"] = int(month or 0)

    $ _kitchen_wine_event_text = ""
    $ _kitchen_pending_event = tavern_kitchen_pending_mandatory_event_code()
    if str(_kitchen_pending_event or "") == "WineForDance" and not tavern_breakfast_available():
        $ _kitchen_event_picture = tavern_kitchen_wine_donation_picture()
        if str(_kitchen_event_picture or "").strip():
            $ scene_image = _kitchen_event_picture
            $ _layout_last_picture = _kitchen_event_picture
        call DisplayTavernEventShort(time, 1)
        $ _kitchen_wine_event_text = str(_return or "")

    if str(_kitchen_wine_event_text or "").strip():
        $ MainTxt = _kitchen_wine_event_text
        $ CurLocDesc = MainTxt
        $ TavernKitchenSavedText = MainTxt
        $ current_action_content = None
        if str(CurEventCode or "") != "WineForDance" or len(list(current_action_items or [])) <= 0:
            call TavernKitchenBuildActions
    else:
        $ MainTxt = build_kitchen_description()
        $ CurLocDesc = MainTxt
        $ TavernKitchenSavedText = MainTxt
        $ current_action_title = "Кухня"
        $ current_action_content = None
        call TavernKitchenBuildActions
        if sandra_revealing_dress_initiative_ready():
            call SandraDressInitiativeEvent
        else:
            python:
                _kitchen_request_type, _kitchen_request_girl = household_pending_request_girl("TavernKitchen")
            if str(_kitchen_request_type or "") == "soap":
                call HouseholdSoapRequestEvent(_kitchen_request_girl)
    while True:
        $ TavernKitchenNoticePending = False
    $ _kitchen_ui_return = None
    while _kitchen_ui_return is None:
        call screen main_ui
        $ _kitchen_ui_return = _return
    jump TavernKitchen


label TavernKitchenBuildActions:
    if TavernBreakfastEventActive:
        return
    $ tavern_kitchen_hearth_wood_stock()
    $ current_action_title = "Кухня"
    $ current_action_content = None
    $ room_menu = CurrentRoom.build_menu_sections()
    $ current_action_items = room_menu["movement"] + room_menu["actions"]
    if tavern_breakfast_available():
        $ current_action_items.append(MenuItem("Позавтракать", Call("TavernKitchenBreakfast")))
    elif tavern_sunday_dinner_available():
        if tavern_sunday_dinner_can_serve_spicy_tincture():
            $ current_action_items.append(MenuItem("Сесть за воскресный обед", Call("TavernKitchenSundayDinnerMenu")))
        else:
            $ current_action_items.append(MenuItem("Сесть за воскресный обед", Call("TavernKitchenSundayDinner")))
    else:
        $ current_action_items.append(MenuItem("Перекусить", Call("Eat", "горячую еду с кухни", 18, "Вы перекусываете на кухне горячей едой и немного приходите в себя.", "TavernKitchen", "")))
    if tavern_kitchen_has_depositable_food():
        $ current_action_items.append(MenuItem("Отнести в кладовую лесную добычу и припасы", Call("TavernKitchenDepositMenu")))
    if tavern_kitchen_can_share_tea_with_sandra_and_becky():
        $ current_action_items.append(MenuItem("Угостить Сандру и Бекки чаем", Call("TavernKitchenShareTeaWithSandraAndBecky")))
    if tavern_kitchen_sandra_can_discuss_breakfasts():
        $ current_action_items.append(MenuItem("Попросить Сандру почаще собирать всех на общий завтрак", Call("TavernKitchenAskSandraBreakfasts")))
    if tavern_kitchen_sandra_can_discuss_clients():
        $ current_action_items.append(MenuItem("Попросить Сандру мягче настроить домочадцев к гостям", Call("TavernKitchenAskSandraClients")))
    python:
        try:
            renpy.restart_interaction()
        except Exception:
            pass


label TavernKitchenShareTeaWithSandraAndBecky:
    if not tavern_kitchen_can_share_tea_with_sandra_and_becky():
        $ MainTxt = "Сейчас для этого не время."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ MainTxt = Sandra.apply_kitchen_tea_with_becky()
    if str(getLocation("sandra") or "") == "TavernKitchen":
        $ _tea_scene = tavern_kitchen_random_sandra_scene()
        if str(_tea_scene or "").strip():
            $ _layout_last_picture = _tea_scene
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBuildActions
    return


label TavernKitchenDepositMenu:
    $ current_action_title = "Кладовые припасы"
    $ current_action_content = None
    $ current_action_items = []
    $ MainTxt = "Вы прикидываете, что из лесной добычи и запасов можно отнести в кладовую для кухонного хозяйства."
    if tavern_kitchen_food_stock_count() > 0:
        $ MainTxt = str(MainTxt or "") + "\nСейчас в кладовой уже лежат: %s." % tavern_kitchen_food_stock_summary()
    $ CurLocDesc = MainTxt
    python:
        for _deposit_row in tavern_kitchen_deposit_entries():
            current_action_items.append(MenuItem(str(_deposit_row.get("caption", "") or ""), Call("TavernKitchenDepositApply", str(_deposit_row.get("item_id", "") or ""))))
        if len(list(current_action_items or [])) <= 0:
            MainTxt = "Сейчас у вас при себе нет ничего подходящего для кухонных запасов."
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Call("TavernKitchenBuildActions")))
    return


label TavernKitchenDepositApply(item_id=""):
    $ _kitchen_item_id = str(item_id or "").strip()
    $ _kitchen_item_name = tavern_kitchen_food_item_name(_kitchen_item_id)
    $ _kitchen_deposited = tavern_kitchen_deposit_food(_kitchen_item_id)
    if int(_kitchen_deposited or 0) <= 0:
        $ MainTxt = "Нечего отдавать."
    else:
        $ MainTxt = "Вы относите в кладовую %s x%s." % (_kitchen_item_name, _kitchen_deposited)
        if str(getLocation("sandra") or "") == "TavernKitchen":
            $ MainTxt = str(MainTxt or "") + "\nСандра деловито осматривает припасы у кладовой, одобрительно кивает и сразу начинает прикидывать, как лучше пустить их в дело."
        $ _kitchen_deposit_effect_text = tavern_kitchen_deposit_effect_text(_kitchen_item_id)
        if str(_kitchen_deposit_effect_text or "").strip():
            $ MainTxt = str(MainTxt or "") + "\n" + str(_kitchen_deposit_effect_text or "")
    if tavern_kitchen_food_stock_count() > 0:
        $ MainTxt = str(MainTxt or "") + "\nТеперь в кладовых запасах лежат: %s." % tavern_kitchen_food_stock_summary()
    $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
    return


label TavernKitchenAskSandraBreakfasts:
    if not tavern_kitchen_sandra_can_discuss_breakfasts():
        $ MainTxt = "Сейчас не лучший момент для такого разговора."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ _kitchen_used_item = tavern_kitchen_take_food_from_stock(["boar_meat_001", "honey_comb_001", "berries_001", "mushroom_001"])
    $ MainTxt = Sandra.apply_kitchen_regular_breakfast_request(_kitchen_used_item)
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    if player.tavern_management.breakfast.event_active:
        jump TavernKitchenBreakfastMenu
    else:
        call TavernKitchenBuildActions
    return


label TavernKitchenAskSandraClients:
    if not tavern_kitchen_sandra_can_discuss_clients():
        $ MainTxt = "Сейчас не лучший момент для такого разговора."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ _kitchen_used_item = tavern_kitchen_take_food_from_stock(["berries_001", "honey_comb_001", "boar_meat_001", "mushroom_001"])
    $ MainTxt = Sandra.apply_kitchen_client_manners_request(_kitchen_used_item)
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    if player.tavern_management.breakfast.event_active:
        jump TavernKitchenBreakfastMenu
    else:
        call TavernKitchenBuildActions
    return


