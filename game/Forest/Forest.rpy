# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.exports as renpy

    FOREST_BACKGROUND_OPTIONS = (
        "images/forest/forest_1.png",
        "images/forest/forest_2.png",
    )
    FOREST_TRAVEL_COST_MINUTES = 120
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

        def spawn(self):
            spawned_items = []
            for rule_index, rule in enumerate(self.spawn_rules):
                item_id = str(rule.get("item_id", "") or "").strip()
                frequency = max(1, int(rule.get("frequency", 1) or 1))
                units = max(1, int(rule.get("units", 1) or 1))
                if not item_id:
                    continue
                if procedural_randint(1, frequency, "forest_spawn_%s_%s" % (self.code_name, rule_index)) == 1:
                    spawned_items.append({
                        "item_id": item_id,
                        "units": units,
                    })
            self.custom_properties["spawned_items"] = list(spawned_items)
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

    def forest_room_spawn(room_obj):
        if room_obj is None:
            return []
        rules = list((getattr(room_obj, "custom_properties", {}) or {}).get("spawn_rules", []) or [])
        spawned_items = []
        for rule_index, rule in enumerate(rules):
            item_id = str(rule.get("item_id", "") or "").strip()
            frequency = max(1, int(rule.get("frequency", 1) or 1))
            units = max(1, int(rule.get("units", 1) or 1))
            if not item_id:
                continue
            if procedural_randint(1, frequency, "forest_spawn_%s_%s" % (room_obj.code_name, rule_index)) == 1:
                spawned_items.append({"item_id": item_id, "units": units})
        room_obj.custom_properties["spawned_items"] = list(spawned_items)
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
        return procedural_choice(list(FOREST_BACKGROUND_OPTIONS), "forest_background_%s" % str(rooms.current_code or "Forest"))

    def forest_random_wildlife_text():
        if procedural_randint(1, 3, "forest_wildlife_gate_%s" % str(rooms.current_code or "Forest")) != 1:
            return ""
        return procedural_choice(list(FOREST_WILDLIFE_TEXTS), "forest_wildlife_text_%s" % str(rooms.current_code or "Forest"))

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
        target = str(rooms.get("Forest").state.get("return_target", "StreetTavern") or "StreetTavern").strip() or "StreetTavern"
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
        return player.horse.owns_horse()

    def forest_travel_cost_minutes():
        if forest_has_horse() and player.horse.saddled:
            return 60
        return int(FOREST_TRAVEL_COST_MINUTES or 120)

    def travel_to_forest_actions(return_target="StreetTavern"):
        if rooms.get("Forest").is_first_visit():
            return []
        target = str(return_target or "StreetTavern")
        return [MenuItem("Идти в лес", [SetDict(rooms.get("Forest").state, "return_target", target), Call("TravelToForest")])]

    def forest_can_depart_now():
        try:
            return int(calendar_v2.hour or 0) < 12
        except Exception:
            return True

    def forest_departure_block_text():
        return "После полудня идти в лес уже поздно. На такую вылазку уйдет не меньше часа верхом и двух часов пешком."

    def forest_after_dusk():
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
        dusk_text = forest_after_dusk_return_text()
        base_text = str(scene_runtime.text or scene_runtime.location_text or "")
        if dusk_text not in base_text:
            if base_text.strip():
                scene_runtime.text = base_text + "\n\n" + dusk_text
            else:
                scene_runtime.text = dusk_text
        scene_runtime.location_text = scene_runtime.text

    ForestRoomDefinition = Forest(
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
        state={
            "return_target": "StreetTavern",
            "display_text": "",
        },
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="19:29", condition=forest_open_hours_visible),
    ) 

init python:
    def forest_room_saved_text(room=None):
        room_obj = room or rooms.current or rooms.get("Forest")
        return str(room_obj.state.get("display_text", "") or "")

    def forest_room_set_saved_text(text="", room=None):
        room_obj = room or rooms.current or rooms.get("Forest")
        room_obj.state["display_text"] = str(text or "")
        return room_obj.state["display_text"]

    def forest_action_items():
        if forest_after_dusk():
            return [MenuItem("Вернуться к трактиру", Call("ForestReturnToTavernAfterDusk"))]
        items = []
        if werecat_can_search("Forest"):
            items.append(MenuItem("Осмотреть лес внимательнее", Call("WerecatForestSearch", "Forest")))
        if fight_can_hunt_here("Forest"):
            items.append(MenuItem("Выслеживать добычу", Call("FightStartHuntCurrentRoom")))
        if player_can_train_shooting():
            items.append(MenuItem("Потренироваться в стрельбе", Call("ShootingPracticeMenu", "Forest")))
        if forest_trap_can_place("Forest"):
            items.append(MenuItem("Поставить ловушку", Call("ForestSetTrap")))
        elif forest_trap_can_check("Forest"):
            items.append(MenuItem("Проверить ловушку", Call("ForestCheckTrap")))
        if werecat_can_set_bait("Forest"):
            items.append(MenuItem("Поставить крысиную приманку", Call("WerecatSetTrap", "Forest")))
        elif werecat_can_check_bait("Forest"):
            items.append(MenuItem("Проверить странную приманку", Call("WerecatCheckTrap", "Forest")))
        for forest_object in rooms.get("Forest").visible_objects():
            items.append(MenuItem(forest_object.name, Call("ForestObjectMenu", forest_object.object_id)))
        for spawn_entry in rooms.get("Forest").get_spawned_items():
            item_id = str(spawn_entry.get("item_id", "") or "")
            units = max(1, int(spawn_entry.get("units", 1) or 1))
            item_obj = get_game_item(item_id, rooms.get("Forest"))
            if item_obj is not None:
                items.append(MenuItem(str(getattr(item_obj, "name", item_id) or item_id) + " x" + str(units), Call("ForestSpawnedItemMenu", item_id)))
        for forest_exit in rooms.get("Forest").visible_exits():
            if str(forest_exit.target or "") == "StreetTavern":
                items.append(MenuItem(forest_return_label_text(), Call("ForestReturnToOrigin")))
            else:
                items.append(MenuItem(forest_exit.label, movement_actions(forest_exit.target, 30)))
        return items

    def forest_subroom_action_items(room=None):
        room_obj = room or rooms.current
        room_code = str(getattr(room_obj, "code_name", "") or "")
        if forest_after_dusk():
            return [MenuItem("Вернуться к трактиру", Call("ForestReturnToTavernAfterDusk"))]
        items = [MenuItem("Осмотреться", Call("ForestSubroomExplore"))]
        if story_event_available(room_code, "clara_stash"):
            items.append(MenuItem("Найти тайник Клариссы", Call("checkTriggers", room_code, "clara_stash", 0)))
        if werecat_can_set_bait(room_code):
            items.append(MenuItem("Поставить крысиную приманку", Call("WerecatSetTrap", room_code)))
        elif werecat_can_check_bait(room_code):
            items.append(MenuItem("Проверить странную приманку", Call("WerecatCheckTrap", room_code)))
        if fight_can_hunt_here(room_code):
            items.append(MenuItem("Выслеживать добычу", Call("FightStartHuntCurrentRoom")))
        if player_can_train_shooting():
            items.append(MenuItem("Потренироваться в стрельбе", Call("ShootingPracticeMenu", room_code)))
        if forest_trap_can_place(room_code):
            items.append(MenuItem("Поставить ловушку", Call("ForestSetTrap")))
        elif forest_trap_can_check(room_code):
            items.append(MenuItem("Проверить ловушку", Call("ForestCheckTrap")))
        if room_code == "ForestLake":
            items.append(MenuItem("Искупаться в озере", Call("ForestLakeBath")))
            if forest_has_horse():
                items.append(MenuItem("Искупать коня", Call("ForestLakeWashHorse")))
        if str(people.location("clara") or "") == room_code:
            items.append(MenuItem("Кларисса", Call("IntClaraTalk", "clara")))
        for spawn_entry in forest_room_get_spawned_items(room_obj):
            item_id = str(spawn_entry.get("item_id", "") or "")
            units = max(1, int(spawn_entry.get("units", 1) or 1))
            item_obj = get_game_item(item_id, room_obj)
            if item_obj is not None:
                items.append(MenuItem(str(getattr(item_obj, "name", item_id) or item_id) + " x" + str(units), Call("ForestSubroomSpawnedItemMenu", item_id)))
        for forest_exit in room_obj.visible_exits():
            if str(forest_exit.target or "") == "StreetTavern":
                items.append(MenuItem(forest_return_label_text(), Call("ForestReturnToOrigin")))
            else:
                items.append(MenuItem(forest_exit.label, movement_actions(forest_exit.target, 30)))
        return items


label TravelToForest:
    if not forest_can_depart_now():
        $ scene_runtime.text = forest_departure_block_text()
        $ scene_runtime.location_text = scene_runtime.text
        jump expression rooms.get("Forest").state["return_target"]
    $ calendar_v2.advance_minutes(forest_travel_cost_minutes())
    call stat
    jump Forest
    return


label ForestReturnToOrigin:
    $ renpy.dynamic("_forest_target")
    $ _forest_target = forest_return_target()
    $ apply_movement_time(forest_travel_cost_minutes(), _forest_target)
    jump expression _forest_target


label ForestReturnToTavernAfterDusk:
    $ rooms.get("Forest").state["return_target"] = "StreetTavern"
    $ scene_runtime.text = forest_after_dusk_return_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ apply_movement_time(forest_travel_cost_minutes(), "StreetTavern")
    jump StreetTavern


label Forest:
    $ renpy.dynamic("_forest_spawned")
    $ rooms.enter("Forest")
    $ scene_runtime.picture = forest_pick_background()
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.object_id = ""
    $ scene_runtime.text = forest_build_entry_text(rooms.current)
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.get("Forest"))
    $ rooms.current.mark_visited()
    $ _forest_spawned = rooms.get("Forest").spawn()
    if len(_forest_spawned) > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nСегодня здесь можно кое-что найти, если внимательно осмотреться."
        $ scene_runtime.location_text = scene_runtime.text
        $ forest_room_set_saved_text(scene_runtime.text, rooms.get("Forest"))

    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    if forest_after_dusk():
        $ forest_apply_after_dusk_message()
    $ main_ui_runtime.action_items = forest_action_items()
    while True:
        call screen main_ui


label ForestObjectMenu(object_id=""):
    $ renpy.dynamic("_forest_object", "_room_object", "_forest_action", "_forest_args")
    $ _forest_object = None
    python:
        for _room_object in rooms.get("Forest").visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _forest_object = _room_object
                break

    if _forest_object is None:
        $ main_ui_runtime.action_items = forest_action_items()
        return

    $ scene_runtime.text = _forest_object.description
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = _forest_object.name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []

    python:
        for _forest_action in _forest_object.visible_actions():
            if _forest_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_forest_action.label, Call("ForestObjectText", object_id, _forest_action.action_id)))
            elif _forest_action.hook == "call" and str(_forest_action.target or "") != "":
                _forest_args = tuple(getattr(_forest_action, "args", ()) or ())
                main_ui_runtime.action_items.append(MenuItem(_forest_action.label, Call(_forest_action.target, *_forest_args)))
            elif _forest_action.hook == "jump" and str(_forest_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_forest_action.label, Jump(_forest_action.target)))

    $ main_ui_runtime.action_items.append(MenuItem("Назад", [
        SetField(scene_runtime, "text", forest_room_saved_text(rooms.get("Forest"))),
        SetField(scene_runtime, "location_text", forest_room_saved_text(rooms.get("Forest"))),
        SetField(main_ui_runtime, "action_title", "Действия"),
        SetField(main_ui_runtime, "action_content", None),
        SetField(main_ui_runtime, "action_items", forest_action_items()),
        Function(main_ui_restart_interaction),
    ]))
    return


label ForestObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_forest_name", "_forest_text", "_room_action", "_room_object")
    python:
        _forest_text = ""
        _forest_name = ""
        for _room_object in rooms.get("Forest").visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _forest_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _forest_text = str(_room_action.target or "")
                    break
            break
        if _forest_text:
            scene_runtime.text = _forest_text
            scene_runtime.location_text = _forest_text
            main_ui_runtime.action_title = _forest_name or "Действия"
    call ForestObjectMenu(object_id)
    return


label WerecatForestSearch(room_code=""):
    $ renpy.dynamic("_werecat_room", "_werecat_search")
    $ _werecat_room = str(room_code or rooms.current_code or "").strip()
    if not werecat_can_search(_werecat_room):
        if _werecat_room == "Forest":
            $ main_ui_runtime.action_items = forest_action_items()
        else:
            $ main_ui_runtime.action_items = forest_subroom_action_items()
        return
    $ _werecat_search = werecat_register_search(_werecat_room)
    if str(_werecat_room or "") == "Forest":
        $ forest_room_set_saved_text(_werecat_search.get("text", ""), rooms.get("Forest"))
    else:
        $ forest_room_set_saved_text(_werecat_search.get("text", ""), rooms.current)
    $ scene_runtime.text = str(_werecat_search.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    if bool(_werecat_search.get("found_tracks", False)) and str(werecat_info_picture_path() or "").strip():
        vscene werecat_info_picture_path()
    "[scene_runtime.text]"
    if _werecat_room == "Forest":
        $ main_ui_runtime.action_items = forest_action_items()
    else:
        $ main_ui_runtime.action_items = forest_subroom_action_items()
    show screen main_ui
    return


label ForestSpawnedItemMenu(item_id=""):
    $ renpy.dynamic("_spawn_item", "_spawn_picture", "_entry", "_spawn_units")
    $ _spawn_item = get_game_item(item_id, rooms.get("Forest"))
    if _spawn_item is None:
        $ main_ui_runtime.action_items = forest_action_items()
        return

    python:
        _spawn_units = 1
        for _entry in rooms.get("Forest").get_spawned_items():
            if str(_entry.get("item_id", "") or "") == str(item_id or ""):
                _spawn_units = max(1, int(_entry.get("units", 1) or 1))
                break

    $ scene_runtime.text = str(_spawn_item.description or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ _spawn_picture = str(getattr(_spawn_item, "picture", "") or "").strip()
    if _spawn_picture:
        $ scene_runtime.picture = _spawn_picture
        vscene _spawn_picture
    $ main_ui_runtime.action_title = _spawn_item.name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [
        MenuItem("Подобрать (" + str(_spawn_units) + ")", Call("ForestTakeSpawnedItem", item_id)),
        MenuItem("Назад", [
            SetField(scene_runtime, "text", forest_room_saved_text(rooms.get("Forest"))),
            SetField(scene_runtime, "location_text", forest_room_saved_text(rooms.get("Forest"))),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", forest_action_items()),
            Function(main_ui_restart_interaction),
        ]),
    ]
    return


label ForestTakeSpawnedItem(item_id=""):
    $ renpy.dynamic("_taken_entry", "_taken_item", "_taken_units", "_unused_taken_unit")
    $ _taken_entry = rooms.get("Forest").remove_spawned_item(item_id)
    $ _taken_item = get_game_item(item_id, rooms.get("Forest"))
    if _taken_entry is None or _taken_item is None:
        $ main_ui_runtime.action_items = forest_action_items()
        return

    $ _taken_units = max(1, int(_taken_entry.get("units", 1) or 1))
    python:
        if bool(getattr(_taken_item, "carriable", False)):
            for _unused_taken_unit in range(_taken_units):
                player.add_item(get_object_id(_taken_item))
    $ scene_runtime.text = "Вы подбираете: %s x%d." % (str(_taken_item.name), int(_taken_units))
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.get("Forest"))
    $ main_ui_runtime.action_items = forest_action_items()
    return


label ForestSubroomExplore:
    $ renpy.dynamic("_spawned_now", "_werecat_search")
    $ _spawned_now = forest_room_get_spawned_items(rooms.current)
    if werecat_can_search(str(getattr(rooms.current, "code_name", "") or "")):
        $ _werecat_search = werecat_register_search(str(getattr(rooms.current, "code_name", "") or ""))
        $ scene_runtime.text = forest_room_saved_text(rooms.current)
        if str(_werecat_search.get("text", "") or "").strip():
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n" + str(_werecat_search.get("text", "") or "")
        if bool(_werecat_search.get("found_tracks", False)) and str(werecat_info_picture_path() or "").strip():
            call ShowImage("", "", werecat_info_picture_path())
    elif len(_spawned_now) > 0:
        $ scene_runtime.text = forest_room_saved_text(rooms.current) + "\n\nВнимательно осмотревшись, вы замечаете, что здесь можно кое-что собрать."
    else:
        $ scene_runtime.text = forest_room_saved_text(rooms.current) + "\n\nВы внимательно осматриваете окрестности, но ничего особенно полезного на глаза не попадается."
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_items = forest_subroom_action_items()
    return

label ForestSubroomSpawnedItemMenu(item_id=""):
    $ renpy.dynamic("_spawn_item", "_spawn_picture", "_entry", "_spawn_units")
    $ _spawn_item = get_game_item(item_id, rooms.current)
    if _spawn_item is None:
        $ main_ui_runtime.action_items = forest_subroom_action_items()
        return

    python:
        _spawn_units = 1
        for _entry in forest_room_get_spawned_items(rooms.current):
            if str(_entry.get("item_id", "") or "") == str(item_id or ""):
                _spawn_units = max(1, int(_entry.get("units", 1) or 1))
                break

    $ scene_runtime.text = str(_spawn_item.description or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ _spawn_picture = str(getattr(_spawn_item, "picture", "") or "").strip()
    if _spawn_picture:
        $ scene_runtime.picture = _spawn_picture
        vscene _spawn_picture
    $ main_ui_runtime.action_title = _spawn_item.name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [
        MenuItem("Подобрать (" + str(_spawn_units) + ")", Call("ForestSubroomTakeSpawnedItem", item_id)),
        MenuItem("Назад", [
            SetField(scene_runtime, "text", forest_room_saved_text(rooms.current)),
            SetField(scene_runtime, "location_text", forest_room_saved_text(rooms.current)),
            SetField(main_ui_runtime, "action_title", str(getattr(rooms.current, "display_name", "Действия") or "Действия")),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", forest_subroom_action_items(rooms.current)),
            Function(main_ui_restart_interaction),
        ]),
    ]
    return


label ForestSubroomTakeSpawnedItem(item_id=""):
    $ renpy.dynamic("_taken_entry", "_taken_item", "_taken_units", "_unused_taken_unit")
    $ _taken_entry = forest_room_remove_spawned_item(rooms.current, item_id)
    $ _taken_item = get_game_item(item_id, rooms.current)
    if _taken_entry is None or _taken_item is None:
        $ main_ui_runtime.action_items = forest_subroom_action_items(rooms.current)
        return

    $ _taken_units = max(1, int(_taken_entry.get("units", 1) or 1))
    python:
        if bool(getattr(_taken_item, "carriable", False)):
            for _unused_taken_unit in range(_taken_units):
                player.add_item(get_object_id(_taken_item))
    $ scene_runtime.text = "Вы подбираете: %s x%d." % (str(_taken_item.name), int(_taken_units))
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_items = forest_subroom_action_items()
    return


label ForestLakeBath:
    python:
        calendar_v2.advance_minutes(60)
        player.appearance.wash()
        player.change_stat("fun", 10)
        update_stat_state()
    $ scene_runtime.text = "Вы раздеваетесь, заходите в прохладную воду и хорошенько смываете с себя дорожную пыль и пот. После купания вы чувствуете себя заметно свежее."
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    call stat
    $ main_ui_runtime.action_items = forest_subroom_action_items()
    return


label ForestLakeWashHorse:
    if not forest_has_horse():
        $ main_ui_runtime.action_items = forest_subroom_action_items()
        return
    python:
        calendar_v2.advance_minutes(60)
        player.economy.tavern_fame = _player_clamp(player.economy.tavern_fame + 1, -20, 20)
        update_stat_state()
    $ scene_runtime.text = "Вы осторожно заводите %s в воду и тщательно смываете с него дорожную грязь и пыль. Конь фыркает, встряхивает гривой и выглядит заметно бодрее." % player.horse.name
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_items = forest_subroom_action_items()
    return


