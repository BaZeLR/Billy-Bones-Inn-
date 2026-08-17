# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import random
    import renpy.exports as renpy

    FOREST_BACKGROUND_OPTIONS = (
        "images/forest/forest_1.png",
        "images/forest/forest_2.png",
    )
    FOREST_TRAVEL_COST_MINUTES = 240
    FOREST_WILDLIFE_TEXTS = (
        "Где-то в кронах тревожно перекликаются лесные птицы.",
        "Между кустами мелькает заяц и тут же скрывается в подлеске.",
        "На влажной земле заметны свежие звериные следы.",
        "По стволу ближайшей сосны быстро шмыгает белка.",
        "В стороне слышится треск сучьев, будто кто-то из лесных зверей осторожно уходит глубже в чащу.",
    )

    class Forest(Room):
        def __init__(self, spawn_rules=None, **kwargs):
            Room.__init__(self, **kwargs)
            self.spawn_rules = list(spawn_rules or [])

        def spawn(self, force=False):
            day_value = int(dayspassed or 0)
            if not bool(force) and int(self.custom_properties.get("spawn_day", -1)) == day_value:
                return self.get_spawned_items()

            spawned_items = []
            for rule in self.spawn_rules:
                item_id = str(rule.get("item_id", "") or "").strip()
                frequency = max(1, int(rule.get("frequency", 1) or 1))
                units = max(1, int(rule.get("units", 1) or 1))
                if not item_id:
                    continue
                if random.randint(1, frequency) == 1:
                    spawned_items.append({
                        "item_id": item_id,
                        "units": units,
                    })
            self.custom_properties["spawned_items"] = list(spawned_items)
            self.custom_properties["spawn_day"] = day_value
            return list(spawned_items)

        def get_spawned_items(self):
            return list(self.custom_properties.get("spawned_items", []) or [])

        def remove_spawned_item(self, item_id):
            item_key = str(item_id or "").strip()
            kept_items = []
            removed_entry = None
            for entry in self.get_spawned_items():
                entry_id = str(entry.get("item_id", "") or "").strip()
                if removed_entry is None and entry_id == item_key:
                    removed_entry = dict(entry)
                    continue
                kept_items.append(dict(entry))
            self.custom_properties["spawned_items"] = kept_items
            return removed_entry

    def forest_room_spawn(room_obj, force=False):
        if room_obj is None:
            return []
        props = getattr(room_obj, "custom_properties", {}) or {}
        day_value = int(dayspassed or 0)
        if not bool(force) and int(props.get("spawn_day", -1)) == day_value:
            return list(props.get("spawned_items", []) or [])

        rules = list(props.get("spawn_rules", []) or [])
        spawned_items = []
        for rule in rules:
            item_id = str(rule.get("item_id", "") or "").strip()
            frequency = max(1, int(rule.get("frequency", 1) or 1))
            units = max(1, int(rule.get("units", 1) or 1))
            if not item_id:
                continue
            if random.randint(1, frequency) == 1:
                spawned_items.append({"item_id": item_id, "units": units})
        room_obj.custom_properties["spawned_items"] = list(spawned_items)
        room_obj.custom_properties["spawn_day"] = day_value
        return list(spawned_items)

    def forest_room_get_spawned_items(room_obj):
        if room_obj is None:
            return []
        return list((getattr(room_obj, "custom_properties", {}) or {}).get("spawned_items", []) or [])

    def forest_room_remove_spawned_item(room_obj, item_id):
        if room_obj is None:
            return None
        item_key = str(item_id or "").strip()
        kept_items = []
        removed_entry = None
        for entry in forest_room_get_spawned_items(room_obj):
            entry_id = str(entry.get("item_id", "") or "").strip()
            if removed_entry is None and entry_id == item_key:
                removed_entry = dict(entry)
                continue
            kept_items.append(dict(entry))
        room_obj.custom_properties["spawned_items"] = kept_items
        return removed_entry

    def forest_pick_background():
        return random.choice(list(FOREST_BACKGROUND_OPTIONS))

    def forest_random_wildlife_text():
        if random.randint(1, 3) != 1:
            return ""
        return random.choice(list(FOREST_WILDLIFE_TEXTS))

    def forest_build_entry_text(room_obj):
        if room_obj is None:
            return "Вы в лесу."
        desc_rows = room_obj.visible_descriptions()
        text_parts = [row.text for row in desc_rows if str(getattr(row, "text", "") or "").strip()]
        wildlife_text = forest_random_wildlife_text()
        if wildlife_text:
            text_parts.append(wildlife_text)
        if len(text_parts) <= 0:
            return "Вы в лесу."
        return "\n\n".join(text_parts)

    def forest_return_target():
        target = str(ForestReturnTarget or "StreetTavern").strip() or "StreetTavern"
        if renpy.has_label(target):
            return target
        return "StreetTavern"

    def forest_return_label_text():
        target = forest_return_target()
        if target == "Shed":
            return "Вернуться к сараю"
        if target == "TavernMyRoom":
            return "Вернуться в комнату"
        return "Вернуться к трактиру"

    def forest_has_horse():
        return bool(str(MyStallion or "").strip())

    def forest_travel_cost_minutes():
        if forest_has_horse() and int(HorseSaddled or 0) == 1:
            return 150
        return int(FOREST_TRAVEL_COST_MINUTES or 240)

    def forest_can_depart_now():
        try:
            calendar_v2.sync_state()
        except Exception:
            pass
        try:
            return int(calendar_v2.hour or 0) < 12
        except Exception:
            return True

    def forest_departure_block_text():
        return "После полудня идти в лес уже поздно. На такую вылазку уйдет не меньше четырех часов."

    def forest_after_dusk():
        try:
            calendar_v2.sync_state()
        except Exception:
            pass
        try:
            current_hour = int(calendar_v2.hour or 0) % 24
            current_minute = int(calendar_v2.minute or 0) % 60
            return current_hour > 19 or (current_hour == 19 and current_minute >= 30)
        except Exception:
            return False

    def forest_open_hours_visible():
        return not forest_after_dusk()

    def forest_after_dusk_return_text():
        return "Смеркается. В лесу уже нельзя задерживаться: нужно возвращаться к трактиру."

    def forest_apply_after_dusk_message():
        global MainTxt, CurLocDesc
        dusk_text = forest_after_dusk_return_text()
        base_text = str(MainTxt or CurLocDesc or "")
        if dusk_text not in base_text:
            if base_text.strip():
                MainTxt = base_text + "\n\n" + dusk_text
            else:
                MainTxt = dusk_text
        CurLocDesc = MainTxt

    ForestRoom = Forest(
        code_name="Forest",
        group_name=ROOM_GROUP_FOREST,
        display_name="Лес",
        bg_picture="images/forest/forest_1.png",
        descriptions=[
            RoomDescription(
                text="Вы в негустом лесу неподалеку от трактира. Между деревьями тянутся узкие тропинки, под ногами хрустит прошлогодняя листва, а вокруг хватает сухостоя, валежника и подходящих стволов для хозяйственных нужд.",
                priority=100,
            ),
            RoomDescription(
                text="Здесь можно найти деревья на дрова, осмотреться и вернуться назад с добычей.",
                priority=90,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
            RoomExit(label="Идти к роднику", target="ForestSpring"),
            RoomExit(label="Свернуть на скрытую тропу", target="ForestHiddenPath"),
            RoomExit(label="Пойти к водопаду", target="ForestWaterfall"),
            RoomExit(label="Выйти на малую поляну", target="ForestClearing"),
            RoomExit(label="Углубиться в темный лес", target="ForestDarkWoods"),
        ],
        game_items=[
            GameObject(
                object_id="forest_trees",
                name="Деревья",
                description="Вокруг хватает молодых деревьев, сухостоя и валежника, из которых можно выбрать подходящий материал для хозяйства.",
                actions=[
                    ObjectAction(
                        action_id="examine_trees",
                        label="Осмотреть деревья",
                        hook="text",
                        target="Некоторые деревья слишком сырые, другие трухлявые, но для хозяйства здесь точно найдется подходящее бревно.",
                    ),
                ],
            ),
            GameObject(
                object_id="forest_path",
                name="Тропинка",
                description="Узкая тропка ведет обратно к городу и к тем местам, где вы уже хорошо ориентируетесь.",
                actions=[
                    ObjectAction(
                        action_id="examine_path",
                        label="Осмотреть тропинку",
                        hook="text",
                        target="По этой тропке удобно возвращаться назад, пока не стемнело.",
                    ),
                ],
            ),
        ],
        spawn_rules=[
            {"item_id": "lumber_001", "frequency": 1, "units": 1},
            {"item_id": "mushroom_001", "frequency": 2, "units": 3},
            {"item_id": "berries_001", "frequency": 2, "units": 2},
            {"item_id": "honey_comb_001", "frequency": 4, "units": 1},
            {"item_id": "arrows_001", "frequency": 5, "units": 2},
        ],
        custom_properties={
            "object_menu_label": "ForestObjectMenu",
        },
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="19:29", condition=forest_open_hours_visible),
    ) 

default ForestSavedText = ""
default ForestReturnTarget = "StreetTavern"
default ForestSubroomSavedText = ""


label TravelToForest(return_target="StreetTavern"):
    $ ForestReturnTarget = str(return_target or "StreetTavern").strip() or "StreetTavern"
    if not forest_can_depart_now():
        $ MainTxt = forest_departure_block_text()
        $ CurLocDesc = MainTxt
        jump expression ForestReturnTarget
    $ calendar_v2.sync_state()
    $ calendar_v2.advance_minutes(forest_travel_cost_minutes())
    call stat
    jump Forest
    return


label ForestReturnToOrigin:
    $ _forest_target = forest_return_target()
    call AdvanceMovementTime(_forest_target)
    return


label ForestReturnToTavernAfterDusk:
    $ ForestReturnTarget = "StreetTavern"
    $ MainTxt = forest_after_dusk_return_text()
    $ CurLocDesc = MainTxt
    call AdvanceMovementTime("StreetTavern")
    return


label Forest:
    $ CurLoc = "Forest"
    $ _forest_room = get_registered_room(CurLoc) or ForestRoom
    call RoomEnterEventGate(CurLoc, False)
    $ scene_image = forest_pick_background() or _forest_room.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = ""
    $ MainTxt = forest_build_entry_text(_forest_room)
    $ CurLocDesc = MainTxt
    $ ForestSavedText = MainTxt
    $ _forest_room.mark_visited()
    $ _forest_spawned = _forest_room.spawn()
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nСегодня здесь можно кое-что найти, если внимательно осмотреться."
        $ CurLocDesc = MainTxt
        $ ForestSavedText = MainTxt

    call ForestBuildActions
    $ _forest_ui_return = None
    while _forest_ui_return is None:
        call screen main_ui
        $ _forest_ui_return = _return
    jump Forest


label ForestBuildActions:
    $ _forest_room = get_registered_room(CurLoc) or ForestRoom
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    if forest_after_dusk():
        $ forest_apply_after_dusk_message()
        $ current_action_items = [MenuItem("Вернуться к трактиру", Call("ForestReturnToTavernAfterDusk"))]
        return
    if werecat_can_search("Forest"):
        $ current_action_items.append(MenuItem("Осмотреть лес внимательнее", Call("WerecatForestSearch", "Forest")))
    if fight_can_hunt_here("Forest"):
        $ current_action_items.append(MenuItem("Выслеживать добычу", Call("FightStartHuntCurrentRoom")))
    if player_can_train_shooting():
        $ current_action_items.append(MenuItem("Потренироваться в стрельбе", Call("ShootingPracticeMenu", "Forest")))
    if forest_trap_can_place("Forest"):
        $ current_action_items.append(MenuItem("Поставить ловушку", Call("ForestSetTrap")))
    elif forest_trap_can_check("Forest"):
        $ current_action_items.append(MenuItem("Проверить ловушку", Call("ForestCheckTrap")))
    if werecat_can_set_bait("Forest"):
        $ current_action_items.append(MenuItem("Поставить крысиную приманку", Call("WerecatSetTrap", "Forest")))
    elif werecat_can_check_bait("Forest"):
        $ current_action_items.append(MenuItem("Проверить странную приманку", Call("WerecatCheckTrap", "Forest")))
    python:
        for _forest_object in _forest_room.visible_objects():
            current_action_items.append(MenuItem(_forest_object.name, Call("ForestObjectMenu", _forest_object.object_id)))
        for _spawn_entry in _forest_room.get_spawned_items():
            _spawn_item_id = str(_spawn_entry.get("item_id", "") or "")
            _spawn_units = max(1, int(_spawn_entry.get("units", 1) or 1))
            _spawn_item = get_game_item(_spawn_item_id, _forest_room)
            if _spawn_item is not None:
                _spawn_name = str(getattr(_spawn_item, "name", _spawn_item_id) or _spawn_item_id)
                current_action_items.append(MenuItem(_spawn_name + " x" + str(_spawn_units), Call("ForestSpawnedItemMenu", _spawn_item_id)))
        for _forest_exit in _forest_room.visible_exits():
            if str(_forest_exit.target or "") == "StreetTavern":
                current_action_items.append(MenuItem(forest_return_label_text(), Call("ForestReturnToOrigin")))
            else:
                current_action_items.append(MenuItem(_forest_exit.label, Call("MoveToRoom", _forest_exit.target, getattr(_forest_exit, "minutes_to_pass", 5))))
    return


label ForestObjectMenu(object_id=""):
    $ _forest_object = None
    python:
        for _room_object in ForestRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _forest_object = _room_object
                break

    if _forest_object is None:
        call ForestBuildActions
        return

    $ MainTxt = _forest_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _forest_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _forest_action in _forest_object.visible_actions():
            if _forest_action.hook == "text":
                current_action_items.append(MenuItem(_forest_action.label, Call("ForestObjectText", object_id, _forest_action.action_id)))
            elif _forest_action.hook == "call" and str(_forest_action.target or "") != "":
                _forest_args = tuple(getattr(_forest_action, "args", ()) or ())
                current_action_items.append(MenuItem(_forest_action.label, Call(_forest_action.target, *_forest_args)))
            elif _forest_action.hook == "jump" and str(_forest_action.target or "") != "":
                current_action_items.append(MenuItem(_forest_action.label, Jump(_forest_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("ForestRestore")))
    return


label ForestObjectText(object_id="", action_id=""):
    python:
        _forest_text = ""
        _forest_name = ""
        for _room_object in ForestRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _forest_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _forest_text = str(_room_action.target or "")
                    break
            break
        if _forest_text:
            MainTxt = _forest_text
            CurLocDesc = _forest_text
            current_action_title = _forest_name or "Действия"
    call ForestObjectMenu(object_id)
    return


label ForestRestore:
    $ MainTxt = ForestSavedText
    $ CurLocDesc = MainTxt
    call ForestBuildActions
    return


label WerecatForestSearch(room_code=""):
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    if not werecat_can_search(_werecat_room):
        if _werecat_room == "Forest":
            call ForestBuildActions
        else:
            call ForestSubroomBuildActions
        return
    $ _werecat_search = werecat_register_search(_werecat_room)
    if str(_werecat_room or "") == "Forest":
        $ ForestSavedText = str(_werecat_search.get("text", "") or "")
    else:
        $ ForestSubroomSavedText = str(_werecat_search.get("text", "") or "")
    $ MainTxt = str(_werecat_search.get("text", "") or "")
    $ CurLocDesc = MainTxt
    if bool(_werecat_search.get("found_tracks", False)) and str(werecat_info_picture_path() or "").strip():
        hide screen main_ui
        vscene werecat_info_picture_path()
        "[MainTxt]"
    if _werecat_room == "Forest":
        call ForestBuildActions
    else:
        call ForestSubroomBuildActions
    return


label ForestSpawnedItemMenu(item_id=""):
    $ _spawn_item = get_game_item(item_id, ForestRoom)
    if _spawn_item is None:
        call ForestBuildActions
        return

    python:
        _spawn_units = 1
        for _entry in ForestRoom.get_spawned_items():
            if str(_entry.get("item_id", "") or "") == str(item_id or ""):
                _spawn_units = max(1, int(_entry.get("units", 1) or 1))
                break

    $ MainTxt = str(_spawn_item.description or "")
    $ CurLocDesc = MainTxt
    $ _spawn_picture = str(getattr(_spawn_item, "picture", "") or "").strip()
    if _spawn_picture:
        $ scene_image = _spawn_picture
        $ _layout_last_picture = _spawn_picture
        vscene _spawn_picture
    $ current_action_title = _spawn_item.name
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Подобрать (" + str(_spawn_units) + ")", Call("ForestTakeSpawnedItem", item_id)),
        MenuItem("Назад", Call("ForestRestore")),
    ]
    return


label ForestTakeSpawnedItem(item_id=""):
    $ _taken_entry = ForestRoom.remove_spawned_item(item_id)
    $ _taken_item = get_game_item(item_id, ForestRoom)
    if _taken_entry is None or _taken_item is None:
        call ForestRestore
        return

    $ _taken_units = max(1, int(_taken_entry.get("units", 1) or 1))
    python:
        if bool(getattr(_taken_item, "carriable", False)):
            for _unused_taken_unit in range(_taken_units):
                _player_add_item_by_id(get_object_id(_taken_item))
    $ MainTxt = "Вы подбираете: [(_taken_item.name)] x[(_taken_units)]."
    $ CurLocDesc = MainTxt
    $ ForestSavedText = MainTxt
    call ForestBuildActions
    return


label ForestSubroomBuildActions:
    $ current_action_title = CurrentRoom.display_name
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Осмотреться", Call("ForestSubroomExplore")),
    ]
    if forest_after_dusk():
        $ forest_apply_after_dusk_message()
        $ current_action_items = [MenuItem("Вернуться к трактиру", Call("ForestReturnToTavernAfterDusk"))]
        return
    if werecat_can_set_bait(str(getattr(CurrentRoom, "code_name", "") or "")):
        $ current_action_items.append(MenuItem("Поставить крысиную приманку", Call("WerecatSetTrap", str(getattr(CurrentRoom, "code_name", "") or ""))))
    elif werecat_can_check_bait(str(getattr(CurrentRoom, "code_name", "") or "")):
        $ current_action_items.append(MenuItem("Проверить странную приманку", Call("WerecatCheckTrap", str(getattr(CurrentRoom, "code_name", "") or ""))))
    if fight_can_hunt_here(str(getattr(CurrentRoom, "code_name", "") or "")):
        $ current_action_items.append(MenuItem("Выслеживать добычу", Call("FightStartHuntCurrentRoom")))
    if player_can_train_shooting():
        $ current_action_items.append(MenuItem("Потренироваться в стрельбе", Call("ShootingPracticeMenu", str(getattr(CurrentRoom, "code_name", "") or ""))))
    if forest_trap_can_place(str(getattr(CurrentRoom, "code_name", "") or "")):
        $ current_action_items.append(MenuItem("Поставить ловушку", Call("ForestSetTrap")))
    elif forest_trap_can_check(str(getattr(CurrentRoom, "code_name", "") or "")):
        $ current_action_items.append(MenuItem("Проверить ловушку", Call("ForestCheckTrap", str(getattr(CurrentRoom, "code_name", "") or ""))))
    if str(getattr(CurrentRoom, "code_name", "") or "") == "ForestLake":
        $ current_action_items.append(MenuItem("Искупаться в озере", Call("ForestLakeBath")))
        if forest_has_horse():
            $ current_action_items.append(MenuItem("Искупать коня", Call("ForestLakeWashHorse")))
    if str(getLocation("clara") or "") == str(getattr(CurrentRoom, "code_name", "") or ""):
        $ current_action_items.append(MenuItem("Кларисса", Call("IntClaraTalk", "clara")))
    python:
        for _spawn_entry in forest_room_get_spawned_items(CurrentRoom):
            _spawn_item_id = str(_spawn_entry.get("item_id", "") or "")
            _spawn_units = max(1, int(_spawn_entry.get("units", 1) or 1))
            _spawn_item = get_game_item(_spawn_item_id, CurrentRoom)
            if _spawn_item is not None:
                _spawn_name = str(getattr(_spawn_item, "name", _spawn_item_id) or _spawn_item_id)
                current_action_items.append(MenuItem(_spawn_name + " x" + str(_spawn_units), Call("ForestSubroomSpawnedItemMenu", _spawn_item_id)))
        for _forest_exit in CurrentRoom.visible_exits():
            if str(_forest_exit.target or "") == "StreetTavern":
                current_action_items.append(MenuItem(forest_return_label_text(), Call("ForestReturnToOrigin")))
            else:
                current_action_items.append(MenuItem(_forest_exit.label, Call("AdvanceMovementTime", _forest_exit.target)))
    return


label ForestSubroomExplore:
    $ _spawned_now = forest_room_get_spawned_items(CurrentRoom)
    if werecat_can_search(str(getattr(CurrentRoom, "code_name", "") or "")):
        $ _werecat_search = werecat_register_search(str(getattr(CurrentRoom, "code_name", "") or ""))
        $ MainTxt = str(ForestSubroomSavedText or "")
        if str(_werecat_search.get("text", "") or "").strip():
            $ MainTxt = str(MainTxt or "") + "\n\n" + str(_werecat_search.get("text", "") or "")
        if bool(_werecat_search.get("found_tracks", False)) and str(werecat_info_picture_path() or "").strip():
            call ShowImage("", "", werecat_info_picture_path())
    elif len(_spawned_now) > 0:
        $ MainTxt = ForestSubroomSavedText + "\n\nВнимательно осмотревшись, вы замечаете, что здесь можно кое-что собрать."
    else:
        $ MainTxt = ForestSubroomSavedText + "\n\nВы внимательно осматриваете окрестности, но ничего особенно полезного на глаза не попадается."
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    call ForestSubroomBuildActions
    return


label ForestSubroomSpawnedItemMenu(item_id=""):
    $ _spawn_item = get_game_item(item_id, CurrentRoom)
    if _spawn_item is None:
        call ForestSubroomBuildActions
        return

    python:
        _spawn_units = 1
        for _entry in forest_room_get_spawned_items(CurrentRoom):
            if str(_entry.get("item_id", "") or "") == str(item_id or ""):
                _spawn_units = max(1, int(_entry.get("units", 1) or 1))
                break

    $ MainTxt = str(_spawn_item.description or "")
    $ CurLocDesc = MainTxt
    $ _spawn_picture = str(getattr(_spawn_item, "picture", "") or "").strip()
    if _spawn_picture:
        $ scene_image = _spawn_picture
        $ _layout_last_picture = _spawn_picture
        vscene _spawn_picture
    $ current_action_title = _spawn_item.name
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Подобрать (" + str(_spawn_units) + ")", Call("ForestSubroomTakeSpawnedItem", item_id)),
        MenuItem("Назад", Call("ForestSubroomRestore")),
    ]
    return


label ForestSubroomTakeSpawnedItem(item_id=""):
    $ _taken_entry = forest_room_remove_spawned_item(CurrentRoom, item_id)
    $ _taken_item = get_game_item(item_id, CurrentRoom)
    if _taken_entry is None or _taken_item is None:
        call ForestSubroomRestore
        return

    $ _taken_units = max(1, int(_taken_entry.get("units", 1) or 1))
    python:
        if bool(getattr(_taken_item, "carriable", False)):
            for _unused_taken_unit in range(_taken_units):
                _player_add_item_by_id(get_object_id(_taken_item))
    $ MainTxt = "Вы подбираете: [(_taken_item.name)] x[(_taken_units)]."
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    call ForestSubroomBuildActions
    return


label ForestLakeBath:
    python:
        global fun
        calendar_v2.advance_minutes(60)
        player_state().appearance.wash()
        player_state().appearance.apply_to_store()
        fun = _player_clamp(fun + 10, 0, 100)
        update_stat_state()
    $ MainTxt = "Вы раздеваетесь, заходите в прохладную воду и хорошенько смываете с себя дорожную пыль и пот. После купания вы чувствуете себя заметно свежее."
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    call stat
    call ForestSubroomBuildActions
    return


label ForestLakeWashHorse:
    if not forest_has_horse():
        call ForestSubroomBuildActions
        return
    python:
        calendar_v2.advance_minutes(60)
        tavernfame = _player_clamp(tavernfame + 1, -20, 20)
        update_stat_state()
    $ MainTxt = "Вы осторожно заводите [MyStallion] в воду и тщательно смываете с него дорожную грязь и пыль. Конь фыркает, встряхивает гривой и выглядит заметно бодрее."
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    call stat
    call ForestSubroomBuildActions
    return


label ForestSubroomRestore:
    $ MainTxt = ForestSubroomSavedText
    $ CurLocDesc = MainTxt
    call ForestSubroomBuildActions
    return
