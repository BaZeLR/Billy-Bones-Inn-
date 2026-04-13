default fire_state = 0
default hot_water_state = 0

default TavernKitchenNoticeText = ""
default TavernKitchenNoticePending = False
default TavernKitchenSavedText = ""
default BeckyKitchenVisitActive = 0
default TavernBreakfastLastDay = -1
default TavernBreakfastSoapAnnouncedDay = -1
default KitchenWildFoodStock = {}

init 4 python:
    def tavern_kitchen_has_worker(worker_name):
        return int(jobkitchen.get(worker_name, 0))

init python:
    import random
    import renpy.exports as renpy

    def tavern_kitchen_random_sandra_scene():
        candidates = []
        for picture_index in range(5):
            picture_path = "images/tavern/kitchen/kitchen_sandra_%s.jpg" % picture_index
            if renpy.loadable(picture_path):
                candidates.append(picture_path)
        if len(candidates) == 0:
            return ""
        return random.choice(candidates)

    def tavern_kitchen_picture():
        if _kitchen_worker_is_present("sandra"):
            sandra_scene = tavern_kitchen_random_sandra_scene()
            if sandra_scene:
                return sandra_scene
        if _kitchen_worker_is_present("melissa"):
            if random.randint(1, 4) == 1:
                if renpy.loadable("images/melissa/tavern/basement.png"):
                    return "images/melissa/tavern/basement.png"
                return "images/amanda/melissa_in storage.mp4"
            melissa_kitchen = [
                "images/melissa/tavern/melissa_kitchen_0.png",
                "images/melissa/tavern/melissa_kitchen_1.png",
            ]
            melissa_kitchen = [row for row in melissa_kitchen if renpy.loadable(row)]
            if len(melissa_kitchen) > 0:
                return melissa_kitchen[random.randint(0, len(melissa_kitchen) - 1)]
        return resolve_room_background_media(TavernKitchenRoom)

    def tavern_kitchen_pending_mandatory_event_code():
        mandatory_count = int(EventsCount.get(10, 0) or 0)
        if mandatory_count <= 0:
            return ""
        event_idx = mandatory_count - 1
        return str(NewEvents.get("10_" + str(event_idx), "") or "")

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

    def tavern_breakfast_available():
        return int(hour or 0) < 12 and int(TavernBreakfastLastDay or -1) != int(dayspassed or 0)

    def tavern_breakfast_present_ids():
        return list(household_breakfast_attendee_ids() or [])

    def tavern_breakfast_present_names():
        names = []
        for npc_id in tavern_breakfast_present_ids():
            names.append(_action_display_name(npc_id))
        return names

    def tavern_breakfast_dialogue_lines():
        lines = []
        present_ids = tavern_breakfast_present_ids()

        if "sandra" in present_ids:
            lines.append("Сандра привычно командует утренней возней и следит, чтобы никто не сидел без дела.")
            lines.append("Сандра ворчит, что хороший дом держится на привычке вставать вовремя, а не на пустых обещаниях сделать все потом.")
        if "melissa" in present_ids:
            lines.append("Мелисса за завтраком становится разговорчивее обычного и успевает вставить пару тихих замечаний почти в любой разговор.")
            lines.append("Мелисса негромко замечает, что утро в трактире ей нравится куда больше шумного вечера: в такие часы дом еще живет скорее общим хозяйством, чем трактирной суетой.")
        if "amanda" in present_ids:
            lines.append("Аманда клюет завтрак быстрее всех и все время норовит отвлечься на болтовню.")
            lines.append("Аманда с набитым ртом уверяет, что если кормить ее так каждое утро, то она готова даже меньше жаловаться на работу.")
        if "becky" in present_ids:
            lines.append("Бекки охотно подхватывает кухонные сплетни и сразу оживляет стол.")
            lines.append("Бекки усмехается, что именно за такими утренними столами и решается, кто в доме на самом деле всем заправляет.")
        if int(week or 0) == 3 and "sandra" in present_ids:
            lines.append("За завтраком Сандра напоминает, что к середине недели надо бы пополнить запасы вина и хорошей еды, иначе в трактире скоро станет совсем уныло.")
        if tavern_breakfast_can_offer_dance_sponsorship() and "sandra" in present_ids:
            lines.append("Сандра заодно осторожно спрашивает, не хотите ли вы и в этом году скинуться на пятничные танцы от лица трактира.")
        if len(list(SoapStoredBatches or [])) > 0 and int(TavernBreakfastSoapAnnouncedDay or -1) != int(dayspassed or 0):
            lines.append("За столом вы объявляете, что новая партия мыла наконец вылежалась и уже готова. Домашние заметно оживляются от этой новости.")
            if "sandra" in present_ids:
                lines.append("Сандра сразу замечает, что в доме наконец будет пахнуть по-человечески, а не только кухней, дымом и работой.")
            if "melissa" in present_ids:
                lines.append("Мелисса тихо радуется, что теперь можно будет без стыда пускать приличных гостей в комнаты наверху.")
            if "amanda" in present_ids:
                lines.append("Аманда смеется, что теперь у нее есть шанс пахнуть не только тестом, дымом и беготней по залу.")
        lines.extend(list(household_breakfast_absence_lines() or []))
        return lines

    def tavern_breakfast_apply_social_bonus():
        present_ids = tavern_breakfast_present_ids()
        for npc_id in present_ids:
            Friends[npc_id] = min(20, int(Friends.get(npc_id, 0) or 0) + 1)
        return present_ids

    def tavern_kitchen_can_share_tea_with_sandra_and_becky():
        return int(BeckyKitchenVisitActive or 0) == 1 and _kitchen_worker_is_present("sandra") and int(_player_item_count_by_id("energy_tea_001") or 0) > 0

    def tavern_kitchen_depositable_food_ids():
        return ("berries_001", "mushroom_001", "honey_comb_001", "boar_meat_001")

    def tavern_kitchen_food_stock_count(item_id=""):
        item_key = str(item_id or "").strip()
        stock = KitchenWildFoodStock if isinstance(KitchenWildFoodStock, dict) else {}
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
            if int(_player_item_count_by_id(item_id) or 0) > 0:
                return True
        return False

    def tavern_kitchen_deposit_entries():
        entries = []
        for item_id in tavern_kitchen_depositable_food_ids():
            item_count = int(_player_item_count_by_id(item_id) or 0)
            if item_count <= 0:
                continue
            item_obj = get_game_item(item_id)
            item_name = str(getattr(item_obj, "name", item_id) or item_id)
            entries.append({
                "item_id": item_id,
                "count": item_count,
                "caption": "Отдать на кухню %s x%s" % (item_name, item_count),
            })
        return entries

    def tavern_kitchen_deposit_food(item_id=""):
        item_key = str(item_id or "").strip()
        if item_key == "":
            return 0
        item_count = int(_player_item_count_by_id(item_key) or 0)
        if item_count <= 0:
            return 0
        removed = _player_remove_item_by_id(item_key, item_count)
        if not removed:
            return 0
        if not isinstance(KitchenWildFoodStock, dict):
            globals()["KitchenWildFoodStock"] = {}
        KitchenWildFoodStock[item_key] = max(0, int(KitchenWildFoodStock.get(item_key, 0) or 0)) + item_count
        return item_count

    def tavern_kitchen_take_food_from_stock(preferred_ids=None):
        preferred = list(preferred_ids or [])
        if len(preferred) <= 0:
            preferred = list(tavern_kitchen_depositable_food_ids())
        if not isinstance(KitchenWildFoodStock, dict):
            return ""
        for item_id in preferred:
            item_key = str(item_id or "").strip()
            if tavern_kitchen_food_stock_count(item_key) <= 0:
                continue
            KitchenWildFoodStock[item_key] = max(0, int(KitchenWildFoodStock.get(item_key, 0) or 0) - 1)
            if int(KitchenWildFoodStock.get(item_key, 0) or 0) <= 0:
                KitchenWildFoodStock.pop(item_key, None)
            return item_key
        return ""

    def tavern_kitchen_food_item_name(item_id=""):
        item_obj = get_game_item(str(item_id or "").strip())
        if item_obj is None:
            return str(item_id or "").strip()
        return str(getattr(item_obj, "name", item_id) or item_id)

    def tavern_kitchen_sandra_can_discuss_breakfasts():
        return _kitchen_worker_is_present("sandra") and tavern_kitchen_food_stock_count() > 0 and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0

    def tavern_kitchen_sandra_can_discuss_clients():
        return _kitchen_worker_is_present("sandra") and tavern_kitchen_food_stock_count() > 0 and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0

    TavernKitchenRoom = Room(
        code_name="TavernKitchen",
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
        npcs=[],  # Filled dynamically from jobkitchen
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={"object_menu_label": "TavernKitchenObjectMenu"},
    )

    def _kitchen_has_job(npc_id):
        mapping = jobkitchen if isinstance(jobkitchen, dict) else {}
        return int(mapping.get(npc_id, 0) or 0) != 0

    def _kitchen_worker_is_present(npc_id):
        return _kitchen_has_job(npc_id) and _tavern_is_in_room(npc_id, "TavernKitchen")

    def _kitchen_display_name(npc_id):
        try:
            return _tavern_name(npc_id)
        except Exception:
            return str(npc_id).capitalize()

    def _kitchen_talk_label(npc_id):
        label = "Int" + str(npc_id).capitalize() + "Talk"
        if renpy.has_label(label):
            return label
        return ""

    def kitchen_becky_visit_visible():
        return int(BeckyKitchenVisitActive or 0) == 1

    def build_kitchen_npc_entries():
        entries = []
        for npc_key in ("sandra", "melissa", "amanda"):
            if not npc_key:
                continue
            if _tavern_is_in_room(npc_key, "TavernKitchen"):
                entries.append({
                    "npc_id": npc_key,
                    "name": _kitchen_display_name(npc_key),
                    "talk_label": _kitchen_talk_label(npc_key),
                    "auto_card": True,
                })
        if int(BeckyKitchenVisitActive or 0) == 1:
            entries.append({
                "npc_id": "becky",
                "name": "Бекки",
                "talk_label": "IntBeckyTalk",
                "auto_card": True,
                "condition": kitchen_becky_visit_visible,
            })
        return entries

    def build_kitchen_description(include_notice=True, intro_text=""):
        room_obj = CurrentRoom if CurrentRoom is not None else TavernKitchenRoom
        room_item_ids = [get_object_id(row) for row in list(getattr(room_obj, "game_items", []) or [])]
        text_parts = []

        intro_value = str(intro_text or "").strip()
        if intro_value:
            text_parts.append(intro_value)

        if include_notice and bool(TavernKitchenNoticePending) and str(TavernKitchenNoticeText or "").strip():
            text_parts.append(str(TavernKitchenNoticeText or "").strip())

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
        if int(BeckyKitchenVisitActive or 0) == 1:
            text_parts.append("Сегодня сюда заглянула Бекки Блэнкеншип. Она что-то негромко обсуждает с Сандрой у разделочного стола.")
        if int(week or 0) == 7 and int(time or 0) == 1:
            text_parts.append("Судя по запахам и приготовленным блюдам, Сандра решила устроить для всей трактирной челяди воскресный обед поосновательнее обычного.")
        if tavern_kitchen_food_stock_count() > 0:
            text_parts.append("На кухне уже отложены принесенные вами припасы: %s." % tavern_kitchen_food_stock_summary())

        hearth_count = len([row for row in room_item_ids if row == "hearth_001"])
        if hearth_count > 0:
            text_parts.append("Очаг готов к использованию.")

        cauldron_count = len([row for row in room_item_ids if row == "cauldron_001"])
        if cauldron_count > 0:
            text_parts.append("Котел для кипячения воды на месте.")

        return "\n\n".join([row for row in text_parts if str(row or "").strip()])

    ##    room_obj = CurrentRoom if CurrentRoom is not None else TavernKitchenRoom
    #   items = []
    #    seen_object_ids = set()

        # Dynamic NPCs from kitchen list
    #    kitchen_crew = NamesList("jobkitchen") or []
    #    for worker in kitchen_crew:
    #        items.append(MenuItem(worker, Call("Int" + worker.capitalize() + "Talk")))  # Talk to crew

    #   for row in list(getattr(room_obj, "game_items", []) or []):
    #        object_id = get_object_id(row)
    #        if not object_id or object_id in seen_object_ids:
    #            continue
    #        seen_object_ids.add(object_id)
    #        game_item = get_game_item(object_id, room_obj)
    #        if game_item is None:
    #            continue
    #        for item_action in game_item.visible_actions():
    #            action_args = tuple(getattr(item_action, "args", ()) or ())
    #            if item_action.hook == "call" and str(item_action.target or "") != "":
    #                items.append(MenuItem(item_action.label, Call(item_action.target, *action_args)))
    #            elif item_action.hook == "jump" and str(item_action.target or "") != "":
    #                items.append(MenuItem(item_action.label, Jump(item_action.target)))
    ##                items.append(MenuItem(item_action.label, Call("Examine", object_id, "TavernKitchen", item_action.target, object_id)))

    #    items.append(MenuItem("Вернуться в зал", Jump("TavernMain")))
    #    items.append(MenuItem("Идти в склад", Jump("TavernStorage")))
    #    items.append(MenuItem("Выйти на задний двор", Jump("Backyard")))
    #    return items


label TavernKitchen:
    call EnterLocation("TavernKitchen")
    $ CurrentRoom = TavernKitchenRoom
    $ CurLoc = "TavernKitchen"
    $ location = CurLoc
    $ tavern_kitchen_hearth_wood_stock()
    $ scene_image = tavern_kitchen_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ current_object_id = ""
    $ current_girl_key = ""
    $ BeckyKitchenVisitActive = 1 if becky_monthly_sandra_kitchen_visit_due() and _tavern_is_in_room("sandra", "TavernKitchen") else 0
    if BeckyKitchenVisitActive:
        $ BeckyVar["SandraKitchenVisitMonth"] = int(month or 0)

    $ TavernKitchenRoom.npcs = build_kitchen_npc_entries()
    $ CurrentRoom.npcs = TavernKitchenRoom.npcs

    $ _kitchen_wine_event_text = ""
    $ _kitchen_pending_event = tavern_kitchen_pending_mandatory_event_code()
    if str(_kitchen_pending_event or "") == "WineForDance" and _tavern_is_in_room("sandra", "TavernKitchen"):
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
    else:
        $ MainTxt = build_kitchen_description()
        $ CurLocDesc = MainTxt
        $ TavernKitchenSavedText = MainTxt
        call TavernKitchenBuildActions
        if sandra_revealing_dress_initiative_ready():
            call SandraDressInitiativeEvent
    $ TavernKitchenNoticePending = False
    jump TavernKitchenView


label TavernKitchenView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernKitchenView


label TavernKitchenBuildActions:
    $ tavern_kitchen_hearth_wood_stock()
    $ TavernKitchenRoom.npcs = build_kitchen_npc_entries()
    $ CurrentRoom.npcs = TavernKitchenRoom.npcs
    $ current_action_title = "Кухня"
    $ current_action_content = None
    $ room_menu = CurrentRoom.build_menu_sections()
    $ current_action_items = room_menu["movement"] + room_menu["actions"]
    if tavern_breakfast_available():
        $ current_action_items.append(MenuItem("Позавтракать", Call("TavernKitchenBreakfast")))
    elif int(week or 0) == 7 and int(hour or 0) >= 12 and int(hour or 0) < 17:
        $ current_action_items.append(MenuItem("Сесть за воскресный обед", Call("TavernKitchenSundayDinner")))
    else:
        $ current_action_items.append(MenuItem("Перекусить", Call("Eat", "горячую еду с кухни", 18, "Вы перекусываете на кухне горячей едой и немного приходите в себя.", "TavernKitchen", "")))
    if tavern_kitchen_has_depositable_food():
        $ current_action_items.append(MenuItem("Отдать на кухню лесную добычу и припасы", Call("TavernKitchenDepositMenu")))
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
    return


label TavernKitchenBreakfast:
    if not tavern_breakfast_available():
        $ MainTxt = "На сегодня вы уже завтракали."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ calendar_advance_minutes(30)
    call ShowImage("tavern", "kitchen", "kitchen_breakfast")
    python:
        _breakfast_lines = [
            "Вы садитесь на кухне и завтракаете горячей кашей, свежим хлебом и чем-то согревающим.",
            "За столом собираются: " + (", ".join(tavern_breakfast_present_names()) if len(tavern_breakfast_present_names()) > 0 else "пока что только вы сами") + ".",
        ]
        _breakfast_lines.extend(tavern_breakfast_dialogue_lines())
        MainTxt = "\n\n".join([row for row in _breakfast_lines if str(row or "").strip()])
        CurLocDesc = MainTxt
    $ _eat_result = player_eat_meal("утреннюю кашу и свежий хлеб", 16)
    if str(_eat_result.get("text", "") or "").strip():
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_eat_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
    $ _breakfast_social_ids = tavern_breakfast_apply_social_bonus()
    if len(list(_breakfast_social_ids or [])) > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nСовместный завтрак заметно сближает вас с теми, кто сидит с вами за столом."
        $ CurLocDesc = MainTxt
    if len(list(SoapStoredBatches or [])) > 0 and int(TavernBreakfastSoapAnnouncedDay or -1) != int(dayspassed or 0):
        $ TavernBreakfastSoapAnnouncedDay = int(dayspassed or 0)
        $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ TavernKitchenSavedText = MainTxt
    call stat
    if tavern_breakfast_can_offer_dance_sponsorship():
        $ current_action_title = "Решение о танцах"
        $ current_action_content = None
        $ current_action_items = []
        if wine_for_dance_can_sponsor():
            $ current_action_items.append(MenuItem("Отправить вино и начать готовить закуску", Call("EventWineForDanceApply", 1)))
        else:
            $ current_action_items.append(MenuItem("Посокрушаться о нехватке запасов", Call("EventWineForDanceApply", 2)))
        $ current_action_items.append(MenuItem("Отказаться", Call("EventWineForDanceApply", 3)))
        return
    call TavernKitchenBuildActions
    return


label TavernKitchenSundayDinner:
    call ShowImage("tavern", "kitchen", "kitchen_sundaydinnerAll_0")
    $ MainTxt = "К полудню кухня собирает всех на более основательную воскресную трапезу. На некоторое время трактирная суета отступает, и весь дом живет одним общим столом."
    $ CurLocDesc = MainTxt
    $ _eat_result = player_eat_meal("воскресный обед для всей челяди", 22)
    if str(_eat_result.get("text", "") or "").strip():
        $ MainTxt = str(_eat_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBuildActions
    return


label TavernKitchenShareTeaWithSandraAndBecky:
    if not tavern_kitchen_can_share_tea_with_sandra_and_becky():
        $ MainTxt = "Сейчас для этого не время."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ _player_remove_item_by_id("energy_tea_001", 1)
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["becky"] = min(20, int(Friends.get("becky", 0) or 0) + 1)
    $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
    if _kitchen_worker_is_present("sandra"):
        $ _tea_scene = tavern_kitchen_random_sandra_scene()
        if str(_tea_scene or "").strip():
            $ _layout_last_picture = _tea_scene
    $ MainTxt = "Вы завариваете бодрящий чай и угощаете им Сандру с Бекки. Разговор за столом быстро теплеет: Сандра благодарит вас за внимание к хозяйству, а Бекки охотно подхватывает кухонные сплетни и делится парой полезных замечаний о трактирных делах."
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBuildActions
    return


label TavernKitchenDepositMenu:
    $ current_action_title = "Кухонные припасы"
    $ current_action_content = None
    $ current_action_items = []
    $ MainTxt = "Вы прикидываете, что из лесной добычи и запасов можно сразу оставить на кухне для общего хозяйства."
    if tavern_kitchen_food_stock_count() > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nСейчас у Сандры уже лежат: %s." % tavern_kitchen_food_stock_summary()
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
        $ MainTxt = "Вы оставляете на кухне %s x%s." % (_kitchen_item_name, _kitchen_deposited)
        if _kitchen_worker_is_present("sandra"):
            $ MainTxt = str(MainTxt or "") + "\n\nСандра деловито осматривает припасы, одобрительно кивает и сразу начинает прикидывать, как лучше пустить их в дело."
    if tavern_kitchen_food_stock_count() > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nТеперь в кухонных запасах лежат: %s." % tavern_kitchen_food_stock_summary()
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
    $ AskedToday["sandra"] = int(AskedToday.get("sandra", 0) or 0) + 1
    $ Talked["sandra"] = int(Talked.get("sandra", 0) or 0) + 1
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
    $ MainTxt = "Вы просите Сандру почаще собирать домочадцев за общий утренний стол и не давать всем разбредаться без толку. Сандра выслушивает вас без лишних слов, потом переводит взгляд на оставленные припасы и кивает.\n\n\"Ладно. Если уж на кухне есть из чего готовить, я поговорю с девочками. Общий завтрак дому не повредит, а там и работа ровнее пойдет,\" решает она."
    if str(_kitchen_used_item or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\nДля ближайшего такого стола Сандра сразу откладывает %s." % tavern_kitchen_food_item_name(_kitchen_used_item)
    $ CurLocDesc = MainTxt
    call TavernKitchenBuildActions
    return


label TavernKitchenAskSandraClients:
    if not tavern_kitchen_sandra_can_discuss_clients():
        $ MainTxt = "Сейчас не лучший момент для такого разговора."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ _kitchen_used_item = tavern_kitchen_take_food_from_stock(["berries_001", "honey_comb_001", "boar_meat_001", "mushroom_001"])
    $ AskedToday["sandra"] = int(AskedToday.get("sandra", 0) or 0) + 1
    $ Talked["sandra"] = int(Talked.get("sandra", 0) or 0) + 1
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ tavernfame = int(tavernfame or 0) + 1
    $ MainTxt = "Вы просите Сандру поговорить с домочадцами и держаться с гостями немного мягче обычного. Сандра щурится, явно взвешивая сказанное, а потом нехотя соглашается.\n\n\"Если уж хочешь, чтобы в трактире было больше довольных рож, я скажу девочкам не срываться на людях почем зря. Но и ты смотри, чтобы работа не шла через пень-колоду,\" бурчит она."
    if str(_kitchen_used_item or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\nЗаодно Сандра решает пустить %s на что-нибудь поприятнее для посетителей." % tavern_kitchen_food_item_name(_kitchen_used_item)
    $ CurLocDesc = MainTxt
    call TavernKitchenBuildActions
    return


label TavernKitchenObjectMenu(object_id=""):
    $ tavern_kitchen_hearth_wood_stock()
    if str(object_id or "") != "":
        $ current_object_id = object_id
    $ object_id = current_object_id
    $ _kitchen_object = None
    python:
        for _room_object in CurrentRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _kitchen_object = _room_object
                break

    if _kitchen_object is None:
        call TavernKitchenBuildActions
        return

    $ current_action_title = str(_kitchen_object.name or "Действия")
    $ current_action_content = None
    $ current_action_items = []
    if str(getattr(_kitchen_object, "picture", "") or "").strip() and renpy.loadable(str(getattr(_kitchen_object, "picture", "") or "").strip()):
        $ _layout_last_picture = str(getattr(_kitchen_object, "picture", "") or "").strip()
    if str(object_id or "") == "hearth_001":
        $ MainTxt = tavern_kitchen_hearth_description()
    elif str(object_id or "") == "cauldron_001":
        $ MainTxt = tavern_kitchen_cauldron_description()
    else:
        $ MainTxt = str(_kitchen_object.description or "")
    $ CurLocDesc = MainTxt

    python:
        for _kitchen_action in _kitchen_object.visible_actions():
            _kitchen_args = tuple(getattr(_kitchen_action, "args", ()) or ())
            if _kitchen_action.hook == "text":
                current_action_items.append(MenuItem(_kitchen_action.label, Call("TavernKitchenObjectText", object_id, _kitchen_action.action_id)))
            elif _kitchen_action.hook == "call" and str(_kitchen_action.target or "") != "":
                current_action_items.append(MenuItem(_kitchen_action.label, Call(_kitchen_action.target, *_kitchen_args)))
            elif _kitchen_action.hook == "jump" and str(_kitchen_action.target or "") != "":
                current_action_items.append(MenuItem(_kitchen_action.label, Jump(_kitchen_action.target)))
        current_action_items.append(MenuItem("Назад", Call("TavernKitchenRestore")))
    return


label TavernKitchenObjectText(object_id="", action_id=""):
    python:
        _kitchen_text = ""
        _kitchen_name = ""
        for _room_object in CurrentRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _kitchen_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _kitchen_text = str(_room_action.target or "")
                    break
            break
        if _kitchen_text:
            MainTxt = _kitchen_text
            CurLocDesc = _kitchen_text
            current_action_title = _kitchen_name or "Действия"
    call TavernKitchenObjectMenu(object_id)
    return


label TavernKitchenRestore:
    $ MainTxt = str(TavernKitchenSavedText or build_kitchen_description())
    $ CurLocDesc = MainTxt
    call TavernKitchenBuildActions
    return
