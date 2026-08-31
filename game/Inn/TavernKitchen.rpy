# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def tavern_kitchen_has_worker(worker_name):
        info = people.get_info(worker_name)
        return int(info.job_value("jobkitchen", 0) or 0) if info is not None else 0

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
        return procedural_choice(candidates, key="tavern_kitchen_sandra_scene_%s" % current_game_day())

    def tavern_kitchen_picture():
        if str(people.location("sandra") or "") == "TavernKitchen":
            sandra_scene = tavern_kitchen_random_sandra_scene()
            if sandra_scene:
                return sandra_scene
        if str(people.location("melissa") or "") == "TavernKitchen":
            if procedural_randint(1, 4, key="tavern_kitchen_melissa_picture_%s_%s" % (current_game_day(), int(calendar_v2.clock_minutes() or 0))) == 1:
                melissa_basement = MelissaStaticData.image_path("tavern", "basement")
                if melissa_basement:
                    return melissa_basement
                if renpy.loadable("images/tavern/storage/storage_room.png"):
                    return "images/tavern/storage/storage_room.png"
                if renpy.loadable("images/tavern/kitchen/kitchen_room.png"):
                    return "images/tavern/kitchen/kitchen_room.png"
                return resolve_room_background_media(rooms.get("TavernKitchen"))
            melissa_kitchen = MelissaStaticData.image_sequence("kitchen", "work")
            if len(melissa_kitchen) > 0:
                return procedural_choice(melissa_kitchen, key="tavern_kitchen_melissa_work_%s_%s" % (current_game_day(), int(calendar_v2.clock_minutes() or 0)))
        return resolve_room_background_media(rooms.get("TavernKitchen"))

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
        return npc_schedule_becky_sandra_kitchen_visit_active() and str(people.location("sandra") or "") == "TavernKitchen" and int(player.item_count("energy_tea_001") or 0) > 0

    def tavern_kitchen_depositable_food_ids():
        item_ids = []
        for item_id, item_obj in dict(game_item_registry or {}).items():
            properties = dict(getattr(item_obj, "custom_properties", {}) or {})
            if bool(properties.get("kitchen_depositable", False)):
                item_ids.append(str(item_id or ""))
        return tuple(sorted(item_ids, key=lambda item_id: str(getattr(get_game_item(item_id), "name", item_id) or item_id)))

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
                "name": item_name,
            })
        return entries

    def tavern_kitchen_deposit_food(item_id="", quantity=0):
        item_key = str(item_id or "").strip()
        if item_key == "" or item_key not in tavern_kitchen_depositable_food_ids():
            return 0
        item_count = int(player.item_count(item_key) or 0)
        if item_count <= 0:
            return 0
        requested_count = max(0, int(quantity or 0))
        deposit_count = item_count if requested_count <= 0 else min(item_count, requested_count)
        removed = player.remove_item(item_key, deposit_count)
        if not removed:
            return 0
        stock = tavern_storage_supplies_stock()
        stock[item_key] = max(0, int(stock.get(item_key, 0) or 0)) + deposit_count
        tavern_kitchen_apply_deposit_effect(item_key, deposit_count)
        return deposit_count

    def tavern_kitchen_deposit_all_food():
        deposited = {}
        for item_id in tavern_kitchen_depositable_food_ids():
            item_count = int(player.item_count(item_id) or 0)
            if item_count <= 0:
                continue
            moved_count = tavern_kitchen_deposit_food(item_id, item_count)
            if moved_count > 0:
                deposited[item_id] = moved_count
        return deposited

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

    def tavern_kitchen_deposit_effect_text(item_id="", item_count=1):
        item_key = str(item_id or "").strip()
        if item_key == "honey_comb_001":
            return "Мед сразу откладывают для сладких добавок к завтракам и напиткам. Такие угощения заметно теплят настроение в доме и делают разговоры смелее."
        if item_key == "boar_meat_001":
            units = max(1, int(item_count or 1))
            boar_item = get_game_item(item_key)
            properties = dict(getattr(boar_item, "custom_properties", {}) or {}) if boar_item is not None else {}
            bones_per_unit = 0
            for output_id, output_count in tuple(properties.get("kitchen_deposit_outputs", ()) or ()):
                if str(output_id or "").strip() == "dog_bone_001":
                    bones_per_unit = max(0, int(output_count or 0))
                    break
            return "Кабанье мясо идет в общий котел: сытная еда заметно разогревает кровь у трактирной команды. После разделки вы забираете для пса кости x%s." % (bones_per_unit * units)
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
                npc_info = people.get_info(npc_id)
                if npc_info is not None:
                    npc_info.change_social(corruption_delta=2)
                    npc_info.change_mana(1, "kitchen_honey")
            return "honey"
        if item_key == "boar_meat_001":
            boar_item = get_game_item(item_key)
            properties = dict(getattr(boar_item, "custom_properties", {}) or {}) if boar_item is not None else {}
            arousal_bonus = max(0, int(properties.get("kitchen_deposit_team_arousal_bonus", 0) or 0)) * units
            corruption_bonus = int(properties.get("kitchen_deposit_team_corruption_bonus", 0) or 0)
            mana_bonus = int(properties.get("kitchen_deposit_team_mana_bonus", 0) or 0)
            tavern_kitchen_add_food_effect("boar_days", min(3, max(1, units)))
            for npc_id in ("sandra", "melissa", "amanda"):
                npc_info = people.get_info(npc_id)
                if npc_info is None:
                    continue
                npc_info.add_arousal(arousal_bonus)
                if corruption_bonus:
                    npc_info.change_social(corruption_delta=corruption_bonus)
                if mana_bonus:
                    npc_info.change_mana(mana_bonus, "kitchen_boar")
            for output_id, output_count in tuple(properties.get("kitchen_deposit_outputs", ()) or ()):
                output_key = str(output_id or "").strip()
                output_total = max(0, int(output_count or 0)) * units
                if output_key and output_total > 0:
                    player.add_item(output_key, output_total)
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
                npc_info = people.get_info(npc_id)
                if npc_info is not None:
                    npc_info.change_social(corruption_delta=1)
                    npc_info.change_mana(1, "kitchen_honey_daily")
            try:
                add_sex_event = TodaySexEvents_Add
            except Exception:
                add_sex_event = None
            if callable(add_sex_event) and procedural_randint(1, 3, key="tavern_kitchen_honey_mood_%s" % current_game_day()) == 1:
                add_sex_event(procedural_choice(["sandra", "melissa", "amanda"], key="tavern_kitchen_honey_mood_target_%s" % current_game_day()), 99, 99, "KitchenHoneyMood")
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
        return str(people.location("sandra") or "") == "TavernKitchen" and tavern_kitchen_food_stock_count() > 0 and int(Sandra.rel or 0) >= 5 and int(Sandra.asked_today or 0) == 0

    def tavern_kitchen_sandra_can_discuss_clients():
        return str(people.location("sandra") or "") == "TavernKitchen" and tavern_kitchen_food_stock_count() > 0 and int(Sandra.rel or 0) >= 5 and int(Sandra.asked_today or 0) == 0

    def tavern_kitchen_saved_text():
        return str(rooms.get("TavernKitchen").state.get("saved_text", "") or "")

    def tavern_kitchen_set_saved_text(text=""):
        rooms.get("TavernKitchen").state["saved_text"] = str(text or "")
        return rooms.get("TavernKitchen").state["saved_text"]

    TavernKitchenRoomDefinition = Room(
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
        state={
            "saved_text": "",
        },
    )

    def build_kitchen_description(include_notice=True, intro_text=""):
        room_obj = rooms.current if rooms.current is not None else rooms.get("TavernKitchen")
        room_item_ids = [get_object_id(row) for row in list(getattr(room_obj, "game_items", []) or [])]
        text_parts = []

        intro_value = str(intro_text or "").strip()
        if intro_value:
            text_parts.append(intro_value)

        # Dynamic crew from original NamesList
        kitchen_crew = NamesList("jobkitchen", "TavernKitchen")
        crew_names = str(kitchen_crew or "никто")
        if int(calendar_v2.hour or 0) < 12:
            text_parts.append("До полудня кухня живет скорее ритмом большого двора, чем трактирной службой. Здесь собирают завтрак, ставят воду, проверяют припасы и только готовятся к дневной работе.")
            text_parts.append("На кухне с утра возятся: " + str(tavern_household_present_names("TavernKitchen") or "никто") + ".")
            if int(calendar_v2.week or 0) == 7:
                text_parts.append("После службы здесь наверняка соберутся и на более основательную воскресную трапезу, но пока речь идет только о спокойном утреннем сборе.")
        else:
            text_parts.append("На кухне работают: " + crew_names + ".")
        if npc_schedule_becky_sandra_kitchen_visit_active():
            text_parts.append("Сегодня сюда заглянула Бекки Блэнкеншип. Она что-то негромко обсуждает с Сандрой у разделочного стола.")
        if tavern_sunday_dinner_available():
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

    def tavern_kitchen_action_items():
        sections = rooms.get("TavernKitchen").build_menu_sections()
        items = list(sections["movement"]) + list(sections["actions"])
        if tavern_breakfast_available():
            items.append(MenuItem("Позавтракать", Call("TavernKitchenBreakfast")))
        elif tavern_sunday_dinner_available():
            target = "TavernKitchenSundayDinnerMenu" if tavern_sunday_dinner_can_serve_spicy_tincture() else "TavernKitchenSundayDinner"
            items.append(MenuItem("Сесть за воскресный обед", Call(target)))
        else:
            items.append(MenuItem("Перекусить", Call("Eat", "горячую еду с кухни", 18, "Вы перекусываете на кухне горячей едой и немного приходите в себя.", "TavernKitchen", "")))
        if tavern_kitchen_has_depositable_food():
            items.append(MenuItem("Отнести в кладовую лесную добычу и припасы", Call("TavernKitchenDepositMenu")))
        if tavern_kitchen_can_share_tea_with_sandra_and_becky():
            items.append(MenuItem("Угостить Сандру и Бекки чаем", Call("TavernKitchenShareTeaWithSandraAndBecky")))
        if tavern_kitchen_sandra_can_discuss_breakfasts():
            items.append(MenuItem("Попросить Сандру почаще собирать всех на общий завтрак", Call("TavernKitchenAskSandraBreakfasts")))
        if tavern_kitchen_sandra_can_discuss_clients():
            items.append(MenuItem("Попросить Сандру мягче настроить домочадцев к гостям", Call("TavernKitchenAskSandraClients")))
        return items

label TavernKitchen:
    $ renpy.dynamic("_kitchen_request_girl", "_kitchen_request_type")
    $ renpy.dynamic("_kitchen_pending_event", "_kitchen_event_picture")
    $ rooms.enter("TavernKitchen")
    $ tavern_kitchen_hearth_wood_stock()
    $ scene_runtime.picture = tavern_kitchen_picture() or rooms.current.bg_picture or None
    call RoomEnterEventGate(rooms.current_code, False)
    $ main_ui_runtime.object_id = ""
    $ main_ui_runtime.girl_key = ""
    if player.tavern_management.breakfast.event_active:
        if str(tavern_kitchen_saved_text() or "").strip():
            $ scene_runtime.text = tavern_kitchen_saved_text()
        else:
            $ scene_runtime.text = "Вы все еще сидите за общим утренним столом."
        $ scene_runtime.location_text = scene_runtime.text
        jump TavernKitchenBreakfastMenu
    if npc_schedule_becky_sandra_kitchen_visit_active():
        $ Becky.sandra_kitchen_visit_period = int(calendar_v2.period or 0)

    $ _kitchen_pending_event = tavern_kitchen_pending_mandatory_event_code()
    if str(_kitchen_pending_event or "") == "WineForDance" and not tavern_breakfast_available():
        $ _kitchen_event_picture = tavern_kitchen_wine_donation_picture()
        if str(_kitchen_event_picture or "").strip():
            $ scene_runtime.picture = _kitchen_event_picture
        call DisplayTavernEventShort(calendar_v2.time_slot(), 1)
        $ scene_runtime.picture = tavern_kitchen_picture() or rooms.current.bg_picture or None

    $ scene_runtime.text = build_kitchen_description()
    $ scene_runtime.location_text = scene_runtime.text
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    $ main_ui_runtime.action_title = "Кухня"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    if story_event_available("TavernKitchen", "sandra_dress_initiative"):
        call SandraDressInitiativeEvent
    else:
        python:
            _kitchen_request_type, _kitchen_request_girl = household_pending_request_girl("TavernKitchen")
        if str(_kitchen_request_type or "") == "soap":
            call HouseholdSoapRequestEvent(_kitchen_request_girl)
    while True:
        call screen main_ui


label TavernKitchenShareTeaWithSandraAndBecky:
    $ renpy.dynamic("_tea_scene")
    if not tavern_kitchen_can_share_tea_with_sandra_and_becky():
        $ scene_runtime.text = "Сейчас для этого не время."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
        return
    $ player.remove_item("energy_tea_001", 1)
    $ Sandra.rel = min(20, int(Sandra.rel or 0) + 1)
    $ Sandra.fun = min(100, int(Sandra.fun or 0) + 1)
    $ Becky.rel = max(0, min(20, int(Becky.rel or 0) + 1))
    $ Becky.fun = max(0, min(100, int(Becky.fun or 0) + 1))
    $ player.change_stat("fun", 1)
    $ scene_runtime.text = "Вы завариваете бодрящий чай и угощаете им Сандру с Бекки. Разговор за столом быстро теплеет: Сандра благодарит вас за внимание к хозяйству, а Бекки охотно подхватывает кухонные сплетни и делится парой полезных замечаний о трактирных делах."
    if str(people.location("sandra") or "") == "TavernKitchen":
        $ _tea_scene = tavern_kitchen_random_sandra_scene()
        if str(_tea_scene or "").strip():
            $ scene_runtime.picture = _tea_scene
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    return


label story_amanda_kitchen_window_favor_0:
    $ main_ui_begin_native_scene_state("Аманда: услуга за молчание")
    show screen main_ui
    $ Amanda.attic_window_favor_stage = 2
    $ Amanda.attic_mock_stopped = True
    vscene "images/amanda/kitchen_help.png"
    $ scene_runtime.text = "Стоит вам спуститься на кухню, как Аманда перехватывает вас у самого входа и быстро отводит к краю очага, пока остальные не успели прислушаться. Она все еще краснеет после сцены у окна, но смотрит прямо.\n\n\"Ты ведь не станешь за завтраком рассказывать, чем я там занималась?\" тихо спрашивает она. Вы обещаете сохранить ее тайну, но напоминаете, что за такое молчание она остается должна вам одну услугу. Аманда кривит губы, затем коротко кивает: \"Ладно. Одну. Только без рассказов за столом.\""
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Предложить Аманде вернуть услугу сейчас":
            call AmandaKitchenWindowFavorRepayment

        "Оставить услугу за ней":
            $ scene_runtime.text = "Вы отвечаете, что пока не станете торопить ее. Аманда заметно расслабляется, но ваш долг не оспаривает: \"Хорошо. Тогда сама скажешь, когда захочешь получить свое.\""
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
    $ main_ui_end_native_scene_state()
    $ scene_runtime.picture = tavern_kitchen_picture() or rooms.get("TavernKitchen").bg_picture or None
    return True


label AmandaKitchenWindowFavorRepayment:
    $ renpy.dynamic("_amanda_favor_came_before")
    if int(Amanda.attic_window_favor_stage or 0) != 2:
        $ scene_runtime.text = "Эта услуга между вами уже закрыта."
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        return
    if int(player.intimacy.came_today or 0) >= int(player.intimacy.can_cum_daily or 0):
        $ scene_runtime.text = "Вы уже слишком вымотаны, чтобы требовать такую услугу сейчас. Аманда усмехается и напоминает, что долг никуда не делся."
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        return
    $ scene_runtime.text = "Вы киваете в сторону тихого угла кухни и предлагаете Аманде вернуть услугу так, чтобы ваш язык был занят чем-нибудь приятнее пересказа ее утреннего секрета. Она вспыхивает, но после короткой паузы согласно кивает."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ _amanda_favor_came_before = int(player.intimacy.came_today or 0)
    call IntAmandaSex("amanda", "kitchen", "minet")
    if int(player.intimacy.came_today or 0) > int(_amanda_favor_came_before or 0):
        $ Amanda.attic_window_favor_stage = 3
        $ Amanda.attic_window_breakfast_bj_day = current_game_day()
        $ scene_runtime.text = "Когда Аманда заканчивает, она быстро приводит себя в порядок и испытующе смотрит на вас. \"Все. Услугу вернула. А про окно за завтраком — ни слова,\" напоминает она. Теперь этот долг между вами закрыт."
    else:
        $ scene_runtime.text = "Вы все же не доводите дело до конца. Аманда поправляет одежду и пожимает плечами: раз услуга не получена, долг пока остается за ней."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    return


label TavernKitchenDepositMenu:
    $ renpy.dynamic("_deposit_row", "_deposit_item_id", "_deposit_name", "_deposit_count")
    $ main_ui_runtime.action_title = "Кладовые припасы"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ scene_runtime.text = "Вы прикидываете, что из лесной добычи и запасов можно отнести в кладовую для кухонного хозяйства."
    if tavern_kitchen_food_stock_count() > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\nСейчас в кладовой уже лежат: %s." % tavern_kitchen_food_stock_summary()
    $ scene_runtime.location_text = scene_runtime.text
    python:
        if len(tavern_kitchen_deposit_entries()) > 0:
            main_ui_runtime.action_items.append(MenuItem("Отнести все съедобные припасы", Call("TavernKitchenDepositAll")))
        for _deposit_row in tavern_kitchen_deposit_entries():
            _deposit_item_id = str(_deposit_row.get("item_id", "") or "")
            _deposit_name = str(_deposit_row.get("name", _deposit_item_id) or _deposit_item_id)
            _deposit_count = max(1, int(_deposit_row.get("count", 1) or 1))
            main_ui_runtime.action_items.append(MenuItem("Отнести одну порцию: %s (при себе x%s)" % (_deposit_name, _deposit_count), Call("TavernKitchenDepositApply", _deposit_item_id, 1)))
            if _deposit_count > 1:
                main_ui_runtime.action_items.append(MenuItem("Отнести весь запас: %s x%s" % (_deposit_name, _deposit_count), Call("TavernKitchenDepositApply", _deposit_item_id, _deposit_count)))
        if len(list(main_ui_runtime.action_items or [])) <= 0:
            scene_runtime.text = "Сейчас у вас при себе нет ничего подходящего для кухонных запасов."
            scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "text", tavern_kitchen_saved_text()),
            SetField(scene_runtime, "location_text", tavern_kitchen_saved_text()),
            SetField(main_ui_runtime, "action_title", "Кухня"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_kitchen_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label TavernKitchenDepositApply(item_id="", quantity=0):
    $ renpy.dynamic("_kitchen_item_id", "_kitchen_item_name", "_kitchen_deposited", "_kitchen_deposit_effect_text")
    $ _kitchen_item_id = str(item_id or "").strip()
    $ _kitchen_item_name = tavern_kitchen_food_item_name(_kitchen_item_id)
    $ _kitchen_deposited = tavern_kitchen_deposit_food(_kitchen_item_id, quantity)
    if int(_kitchen_deposited or 0) <= 0:
        $ scene_runtime.text = "Нечего отдавать."
    else:
        $ scene_runtime.text = "Вы относите в кладовую %s x%s." % (_kitchen_item_name, _kitchen_deposited)
        if str(people.location("sandra") or "") == "TavernKitchen":
            $ scene_runtime.text = str(scene_runtime.text or "") + "\nСандра деловито осматривает припасы у кладовой, одобрительно кивает и сразу начинает прикидывать, как лучше пустить их в дело."
        $ _kitchen_deposit_effect_text = tavern_kitchen_deposit_effect_text(_kitchen_item_id, _kitchen_deposited)
        if str(_kitchen_deposit_effect_text or "").strip():
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n" + str(_kitchen_deposit_effect_text or "")
    if tavern_kitchen_food_stock_count() > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\nТеперь в кладовых запасах лежат: %s." % tavern_kitchen_food_stock_summary()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    return


label TavernKitchenDepositAll:
    $ renpy.dynamic("_kitchen_all_deposited", "_kitchen_all_parts", "_kitchen_all_item_id", "_kitchen_all_count")
    $ _kitchen_all_deposited = tavern_kitchen_deposit_all_food()
    if len(_kitchen_all_deposited) <= 0:
        $ scene_runtime.text = "Нечего отдавать."
    else:
        python:
            _kitchen_all_parts = []
            for _kitchen_all_item_id, _kitchen_all_count in _kitchen_all_deposited.items():
                _kitchen_all_parts.append("%s x%s" % (tavern_kitchen_food_item_name(_kitchen_all_item_id), int(_kitchen_all_count or 0)))
            scene_runtime.text = "Вы относите в кладовую все съедобные припасы: %s." % ", ".join(_kitchen_all_parts)
        if str(people.location("sandra") or "") == "TavernKitchen":
            $ scene_runtime.text = str(scene_runtime.text or "") + "\nСандра деловито осматривает принесенные запасы и сразу начинает прикидывать, как лучше пустить их в дело."
    if tavern_kitchen_food_stock_count() > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\nТеперь в кладовых запасах лежат: %s." % tavern_kitchen_food_stock_summary()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    return


label TavernKitchenAskSandraBreakfasts:
    $ renpy.dynamic("_kitchen_used_item")
    if not tavern_kitchen_sandra_can_discuss_breakfasts():
        $ scene_runtime.text = "Сейчас не лучший момент для такого разговора."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
        return
    $ _kitchen_used_item = tavern_kitchen_take_food_from_stock(["boar_meat_001", "honey_comb_001", "berries_001", "mushroom_001"])
    $ Sandra.asked_today = int(Sandra.asked_today or 0) + 1
    $ Sandra.talked_today = int(Sandra.talked_today or 0) + 1
    $ Sandra.rel = min(20, int(Sandra.rel or 0) + 1)
    $ Sandra.fun = min(100, int(Sandra.fun or 0) + 2)
    $ Melissa.rel = max(0, min(20, int(Melissa.rel or 0) + 1))
    $ Melissa.fun = max(0, min(100, int(Melissa.fun or 0) + 1))
    $ Amanda.rel = max(0, min(20, int(Amanda.rel or 0) + 1))
    $ Amanda.fun = max(0, min(100, int(Amanda.fun or 0) + 1))
    $ player.change_stat("fun", 2)
    $ scene_runtime.text = "Вы просите Сандру почаще собирать домочадцев за общий утренний стол и не давать всем разбредаться без толку. Сандра выслушивает вас без лишних слов, потом переводит взгляд на оставленные припасы и кивает.\n\n\"Ладно. Если уж на кухне есть из чего готовить, я поговорю с девочками. Общий завтрак дому не повредит, а там и работа ровнее пойдет,\" решает она."
    if str(_kitchen_used_item or "").strip():
        $ scene_runtime.text += "\nДля ближайшего такого стола Сандра сразу откладывает %s." % tavern_kitchen_food_item_name(_kitchen_used_item)
    $ scene_runtime.location_text = scene_runtime.text
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    if player.tavern_management.breakfast.event_active:
        jump TavernKitchenBreakfastMenu
    else:
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    return


label TavernKitchenAskSandraClients:
    $ renpy.dynamic("_kitchen_used_item")
    if not tavern_kitchen_sandra_can_discuss_clients():
        $ scene_runtime.text = "Сейчас не лучший момент для такого разговора."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
        return
    $ _kitchen_used_item = tavern_kitchen_take_food_from_stock(["berries_001", "honey_comb_001", "boar_meat_001", "mushroom_001"])
    $ Sandra.asked_today = int(Sandra.asked_today or 0) + 1
    $ Sandra.talked_today = int(Sandra.talked_today or 0) + 1
    $ Sandra.rel = min(20, int(Sandra.rel or 0) + 1)
    $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 1
    $ scene_runtime.text = "Вы просите Сандру поговорить с домочадцами и держаться с гостями немного мягче обычного. Сандра щурится, явно взвешивая сказанное, а потом нехотя соглашается.\n\n\"Если уж хочешь, чтобы в трактире было больше довольных рож, я скажу девочкам не срываться на людях почем зря. Но и ты смотри, чтобы работа не шла через пень-колоду,\" бурчит она."
    if str(_kitchen_used_item or "").strip():
        $ scene_runtime.text += "\nЗаодно Сандра решает пустить %s на что-нибудь поприятнее для посетителей." % tavern_kitchen_food_item_name(_kitchen_used_item)
    $ scene_runtime.location_text = scene_runtime.text
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    if player.tavern_management.breakfast.event_active:
        jump TavernKitchenBreakfastMenu
    else:
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    return


