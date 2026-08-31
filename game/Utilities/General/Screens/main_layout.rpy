# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default main_ui_runtime = MainUIRuntimeState()

init python:
    import renpy.exports as renpy_module

    class MainUIRuntimeState(object):
        def __init__(self):
            self.action_title = "Actions"
            self.action_content = None
            self.action_items = []
            self.girl_key = ""
            self.talk_picture = ""
            self.object_id = ""
            self.mode = "scene"
            self.selected_char = ""
            self.inventory_dropdown_open = False
            self.overlay = ""
            self.inventory_view_mode = "profile"
            self.inventory_view_section = ""
            self.inventory_view_item = ""
            self.inventory_origin = "profile"
            self.story_board_person = "melissa"
            self.talk_origin = None
            self.card_origin = None
            self.scene_origin = None
            self.tavern_report_person = ""
            self.tavern_report_origin = None

        def clear_contexts(self):
            self.talk_origin = None
            self.card_origin = None
            self.scene_origin = None
            self.tavern_report_person = ""
            self.tavern_report_origin = None

    def main_ui_context_snapshot():
        return {
            "mode": str(main_ui_runtime.mode or "scene"),
            "selected_char": str(main_ui_runtime.selected_char or ""),
            "girl_key": str(main_ui_runtime.girl_key or ""),
            "talk_picture": str(main_ui_runtime.talk_picture or ""),
            "title": str(main_ui_runtime.action_title or ""),
            "content": main_ui_runtime.action_content,
            "items": list(main_ui_runtime.action_items or []),
            "object_id": str(main_ui_runtime.object_id or ""),
            "main_text": scene_runtime.text,
            "location_text": scene_runtime.location_text,
            "picture": str(scene_runtime.picture or ""),
        }

    def main_ui_restore_context(snapshot=None):
        state = dict(snapshot or {})
        main_ui_runtime.mode = str(state.get("mode", "scene") or "scene")
        main_ui_runtime.selected_char = str(state.get("selected_char", "") or "")
        main_ui_runtime.girl_key = str(state.get("girl_key", "") or "")
        main_ui_runtime.talk_picture = str(state.get("talk_picture", "") or "")
        main_ui_runtime.action_title = str(state.get("title", "Actions") or "Actions")
        main_ui_runtime.action_content = state.get("content", None)
        main_ui_runtime.action_items = list(state.get("items", []) or [])
        main_ui_runtime.object_id = str(state.get("object_id", "") or "")
        scene_runtime.text = state.get("main_text", scene_runtime.text)
        scene_runtime.location_text = state.get("location_text", scene_runtime.location_text)
        scene_runtime.picture = str(state.get("picture", scene_runtime.picture) or "")

    def main_ui_restart_interaction():
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def main_ui_toggle_inventory_dropdown():

        main_ui_runtime.inventory_dropdown_open = not bool(main_ui_runtime.inventory_dropdown_open)
        main_ui_restart_interaction()

    def main_ui_close_inventory_dropdown():

        main_ui_runtime.inventory_dropdown_open = False
        main_ui_restart_interaction()

    def main_ui_open_inventory_section(section_id=""):

        main_ui_runtime.inventory_dropdown_open = False
        main_ui_begin_card_state()
        player_card_set_inventory_origin("room")
        player_card_show_inventory_section_state(section_id)

    def main_ui_talk_picture_path(girl_name=""):
        key = str(girl_name or "").strip().lower()
        candidates = []

        if key == "amanda":
            candidates.append(AmandaStaticData.portrait)
        elif key == "melissa":
            try:
                candidates.append(MelissaStaticData.image_path("portrait", "default"))
            except Exception:
                pass
            candidates.extend([
                "images/melissa/tavern/portrait.png",
                "images/melissa/melissa_portrait_0.jpg",
                "images/melissa/melissa_portrait_1.jpg",
                "images/melissa/melissa_card.jpg",
            ])
        elif key == "sandra":
            candidates.extend([
                "images/sandra/portrait2.jpg",
                "images/sandra/portrait3.jpg",
                "images/sandra/talk_0.png",
                "images/sandra/sandra_card.jpg",
            ])
        elif key in ("clara", "clarissa"):
            candidates.extend([
                "images/clara/portrait1.jpg",
                "images/clara/portrait.png",
                "images/clara/portrait2.jpg",
            ])
        else:
            npc_data = people.get_data(key)
            if npc_data is not None:
                candidates.append(getattr(npc_data, "portrait", ""))
            try:
                candidates.append(girl_card_portrait_path(key))
            except Exception:
                pass

        for candidate in candidates:
            path = str(candidate or "").strip()
            if path and renpy_module.loadable(path):
                return path
        return ""

    def main_ui_begin_talk_state(title="", selected_char=""):

        if str(main_ui_runtime.mode or "") != "talk" and main_ui_runtime.talk_origin is None:
            main_ui_runtime.talk_origin = main_ui_context_snapshot()
        main_ui_runtime.mode = "talk"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []

        char_key = str(selected_char or "").strip()
        if char_key:
            main_ui_runtime.selected_char = char_key
            main_ui_runtime.girl_key = char_key
            main_ui_runtime.talk_picture = main_ui_talk_picture_path(char_key)

        if str(title or "").strip():
            main_ui_runtime.action_title = str(title)

        renpy_module.show_screen("main_ui")
        main_ui_restart_interaction()

    def main_ui_begin_card_state():
        if main_ui_runtime.card_origin is None:
            main_ui_runtime.card_origin = main_ui_context_snapshot()

    def main_ui_end_card_state():
        origin = main_ui_runtime.card_origin
        main_ui_runtime.card_origin = None
        if origin is not None:
            main_ui_restore_context(origin)
        main_ui_restart_interaction()

    def main_ui_end_talk_state():
        origin = main_ui_runtime.talk_origin
        main_ui_runtime.talk_origin = None
        main_ui_runtime.card_origin = None
        if origin is not None:
            main_ui_restore_context(origin)
        else:
            main_ui_runtime.mode = "scene"
            main_ui_runtime.selected_char = ""
            main_ui_runtime.girl_key = ""
            main_ui_runtime.talk_picture = ""
        main_ui_restart_interaction()

    def main_ui_begin_native_scene_state(title=""):

        if main_ui_runtime.scene_origin is None:
            main_ui_runtime.scene_origin = main_ui_context_snapshot()
        main_ui_runtime.mode = "event"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.talk_picture = ""
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []
        if str(title or "").strip():
            main_ui_runtime.action_title = str(title)

        main_ui_restart_interaction()

    def main_ui_end_native_scene_state():
        origin = main_ui_runtime.scene_origin
        main_ui_runtime.scene_origin = None
        if origin is not None:
            main_ui_restore_context(origin)
        main_ui_restart_interaction()

    def tractir_after_load_restore_ui():

        try:
            main_ui_runtime.action_content = None
            main_ui_runtime.action_items = []
            main_ui_runtime.clear_contexts()
        except Exception:
            pass

        try:
            if str(rooms.current_code or "") == "Intro":
                return
        except Exception:
            return

        try:
            restored_room = rooms.get(str(rooms.current_code or ""))
            if restored_room is not None:
                main_ui_runtime.mode = "scene"
                main_ui_runtime.selected_char = ""
                main_ui_runtime.girl_key = ""
                main_ui_runtime.talk_picture = ""
                main_ui_runtime.object_id = ""
                main_ui_runtime.action_title = "Действия в трактире" if str(rooms.current_code or "") == "TavernMain" else "Действия"
                main_ui_runtime.action_items = build_room_action_items(restored_room)
        except Exception:
            pass

init -5:
    style mui_text is default
    style mui_text:
        size 20

    style mui_button_text is button_text
    style mui_button_text:
        size 20

    style mui_hud_button is button:
        xfill True
        yminimum 42
        padding (10, 4)
        background Solid("#141414")
        hover_background Solid("#242018")
        selected_background Solid("#322613")

    style mui_hud_button_text is button_text:
        size 20
        color "#d6c8ad"
        hover_color "#ffffff"
        selected_color "#f0d08a"
        selected_hover_color "#ffffff"

    style mui_action_button is mui_hud_button:
        yminimum 34
        padding (8, 2)

    style mui_action_button_text is mui_hud_button_text:
        size 18

    style mui_hud_subbutton is mui_hud_button:
        yminimum 34
        left_padding 18
        background Solid("#0e0e0e")
        hover_background Solid("#201a14")

    style mui_hud_subbutton_text is mui_hud_button_text:
        size 18

    style mui_inventory_item_button is button:
        yminimum 54
        padding (14, 8)
        background Solid("#d8c7a6dd")
        hover_background Solid("#eadbbcff")
        insensitive_background Solid("#b5a78dcc")

    style mui_inventory_item_name is default:
        size 20
        color "#2d1d12"
        hover_color "#120b07"

    style mui_inventory_item_quantity is default:
        size 20
        bold True
        color "#704c20"
        hover_color "#3f280f"

    style mui_status_label is default:
        size 18
        color "#a39a8b"
        xminimum 76

    style mui_status_value is default:
        size 18

screen current_action_panel(native_choice=None):
    if native_choice is not None:
        $ _native_choice_items = list(native_choice.scope.get("items", []) or [])
        use choice_panel(_native_choice_items)
    elif str(main_ui_runtime.mode or "") in ("dog", "werecat") and main_ui_runtime.card_origin is not None:
        textbutton "Назад":
            style "mui_hud_button"
            text_style "mui_hud_button_text"
            action Function(main_ui_end_card_state)
    elif str(main_ui_runtime.mode or "") == "event":
        null
    elif main_ui_runtime.action_content:
        use expression main_ui_runtime.action_content
    elif main_ui_runtime.action_items:
        use choice_panel(main_ui_runtime.action_items)
    elif str(getattr(rooms.current, "code_name", "") or rooms.current_code or "").strip() == "TavernKitchen" and bool(player.tavern_management.breakfast.event_active):
        null
    elif rooms.current is not None:
        $ action_items = build_room_action_items(rooms.current)
        use choice_panel(action_items)
    else:
        text "Выберите действие." size 20

screen main_ui_status_item(label, value, value_color="#f0e6d2"):
    hbox:
        xfill True
        spacing 4
        text str(label or "") + ":" style "mui_status_label"
        text str(value or "") style "mui_status_value" color value_color


screen main_ui_hud_button(caption, action_value, selected_value=False, button_id=""):
    textbutton str(caption or ""):
        id button_id
        alt button_id
        style "mui_hud_button"
        selected bool(selected_value)
        action action_value


screen BGIMAGE(media_ref=None):
    $ _bg_source = media_ref if media_ref else media_displayable(BGDeclare())
    if _bg_source:
        add Transform(_bg_source, fit="contain", xalign=0.5, yalign=0.0)
    else:
        add Solid("#000000")

screen debug_builder_state_controls(chores):
    frame:
        xfill True
        padding (10, 8)
        background "#101010ff"

        vbox:
            spacing 6
            text "DEBUG STATE" size 18 bold True xalign 0.5

            hbox:
                spacing 6
                text "Time" size 15 xsize 58
                for _slot_id in range(0, 8):
                    textbutton str(_slot_id):
                        id "debug_builder_time_slot_%d" % _slot_id
                        alt "debug_builder_time_slot_%d" % _slot_id
                        text_size 14
                        selected int(calendar_v2.time_slot()) == _slot_id
                        action Function(debug_builder_set_time_slot_control, _slot_id)

            hbox:
                spacing 8
                text "Weekday" size 15 xsize 72
                textbutton "<":
                    id "debug_builder_week_prev"
                    alt "debug_builder_week_prev"
                    text_size 16
                    action Function(debug_builder_step_weekday, -1)
                text str(calendar_v2.hud_data()["week_name_en"]) size 15 xminimum 120
                textbutton ">":
                    id "debug_builder_week_next"
                    alt "debug_builder_week_next"
                    text_size 16
                    action Function(debug_builder_step_weekday, 1)

            hbox:
                spacing 8
                text "Period" size 15 xsize 72
                textbutton "<":
                    id "debug_builder_month_prev"
                    alt "debug_builder_month_prev"
                    text_size 16
                    action Function(debug_builder_step_month, -1)
                text str(calendar_v2.hud_data()["period_name_en"]) size 15 xminimum 160
                textbutton ">":
                    id "debug_builder_month_next"
                    alt "debug_builder_month_next"
                    text_size 16
                    action Function(debug_builder_step_month, 1)

            viewport:
                xfill True
                ymaximum 120
                draggable True
                mousewheel True

                vbox:
                    spacing 3
                    for _chore_key in PLAYER_CHORE_KEYS:
                        hbox:
                            spacing 5
                            text str(_pc_chore_display_name(_chore_key)) size 14 xsize 130
                            text "[int(chores.get(_chore_key, 0) or 0)]/[player_chore_target(_chore_key)]" size 14 xsize 45
                            textbutton "-":
                                id "debug_builder_chore_dec_%s" % _chore_key
                                alt "debug_builder_chore_dec_%s" % _chore_key
                                text_size 14
                                action Function(debug_builder_step_chore, _chore_key, -1)
                            textbutton "+":
                                id "debug_builder_chore_inc_%s" % _chore_key
                                alt "debug_builder_chore_inc_%s" % _chore_key
                                text_size 14
                                action Function(debug_builder_step_chore, _chore_key, 1)





screen main_ui():
    zorder 0

    if rooms.current_code == "Intro":
        key "game_menu" action NullAction()
    else:
        key "game_menu" action ShowMenu("save")
        key "K_l" action SetField(main_ui_runtime, "overlay", "people")
        key "K_t" action SetField(main_ui_runtime, "overlay", "story")
        key "K_i" action Function(main_ui_toggle_inventory_dropdown)
        key "K_p" action Function(show_player_card_main_ui_state)
        if config.developer:
            key "K_F8" action Jump("dev_after_report_checkpoint")

    $ _room = rooms.current
    $ _room_name = _room.display_name if _room is not None else str(rooms.current_code or "")
    $ _desc = str(_coerce_panel_text_value(scene_runtime.text if scene_runtime.text is not None else scene_runtime.location_text) or "")
    $ _say_displayable = renpy.get_screen("say")
    $ _say_scope = getattr(_say_displayable, "scope", {}) if _say_displayable is not None else {}
    $ _say_text = str(_say_scope.get("what", "") or "") if hasattr(_say_scope, "get") else ""
    $ _desc = "" if _say_text != "" and _say_text == _desc else _desc
    $ _picture = resolve_main_ui_picture(_room)
    $ current_location = str(rooms.current_code or getattr(_room, "code_name", "") or "")
    $ _npc_ids_here = list(people.ids_at(current_location) or []) if current_location else []
    $ _char_entries = [{"entity_type": "player", "id": "you", "title": "Стефан", "where_id": current_location, "entity_data": {}}]
    python:
        for npc_id in _npc_ids_here:
            npc_key = str(npc_id or "").strip()
            if not npc_key:
                continue
            npc_data = people.action_data_for_room(npc_key, current_location)
            if npc_data is None:
                continue
            _char_entries.append({
                "entity_type": "npc",
                "id": npc_key,
                "title": str(npc_data.get("title", "") or npc_key),
                "where_id": current_location,
                "entity_data": dict(npc_data),
            })
    $ _char_slots = list(_char_entries[:9]) + [None] * max(0, 9 - len(_char_entries[:9]))
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _chores = get_player_chores_ui_state()
    $ _calendar_hud = calendar_v2.hud_data()

    fixed:
        xfill True
        ysize _usable_h
        add Solid("#000000")

        hbox:
            xpos 12
            ypos 12
            spacing 12

            vbox:
                xmaximum int((config.screen_width - 36) * 0.72)
                ymaximum _usable_h - 24
                yfill True
                spacing 10
                use main_ui_left_panel(_room_name, _desc, _picture)

            vbox:
                xmaximum int((config.screen_width - 36) * 0.28)
                ymaximum _usable_h - 24
                yfill True
                spacing 10

                if rooms.current_code != "Intro":
                    frame:
                        xfill True
                        yminimum 220
                        padding (14, 10)
                        background "#000000ff"

                        vbox:
                            spacing 2
                            xfill True

                            hbox:
                                xfill True
                                text "TIME" size 21 bold True
                                null width 12
                                text "TAVERN" size 23 bold True xalign 1.0

                            null height 8

                            hbox:
                                spacing 50
                                xfill True

                                vbox:
                                    xsize 160
                                    spacing 4
                                    use main_ui_status_item("time", _calendar_hud["time_name_ru"])
                                    use main_ui_status_item("weekday", _calendar_hud["week_name_ru"])
                                    use main_ui_status_item("day", _calendar_hud["day"])
                                    use main_ui_status_item("days in game", _calendar_hud["days_in_game"])
                                    use main_ui_status_item("period", _calendar_hud["period_name_ru"])
                                    use main_ui_status_item("cycle", _calendar_hud["cycle"])
                                    null height 4
                                    use main_ui_status_item("money", player.economy.money, "#f0d08a")

                                vbox:
                                    xfill True
                                    spacing 6
                                    use main_ui_hud_button("Трактир", [
                                        Function(main_ui_close_inventory_dropdown),
                                        Call("ShowTavernReport", "__main_ui__"),
                                    ], str(main_ui_runtime.mode or "") == "tavern", "main_ui_tavern_button")
                                    use main_ui_hud_button("Время", [Function(main_ui_close_inventory_dropdown), SetField(main_ui_runtime, "overlay", "time")], str(main_ui_runtime.overlay or "") == "time", "main_ui_time_button")
                                    use main_ui_hud_button("Сюжеты", [Function(main_ui_close_inventory_dropdown), SetField(main_ui_runtime, "overlay", "story")], str(main_ui_runtime.overlay or "") == "story", "main_ui_story_button")
                                    use main_ui_hud_button("Итоги", [Function(main_ui_close_inventory_dropdown), SetField(main_ui_runtime, "overlay", "progress")], str(main_ui_runtime.overlay or "") == "progress", "main_ui_progress_button")
                                    use main_ui_hud_button("Кто где", [Function(main_ui_close_inventory_dropdown), SetField(main_ui_runtime, "overlay", "people")], str(main_ui_runtime.overlay or "") == "people", "main_ui_people_button")
                                    use main_ui_hud_button("Инвентарь", Function(main_ui_toggle_inventory_dropdown), bool(main_ui_runtime.inventory_dropdown_open), "main_ui_inventory_button")
                                    if config.developer:
                                        use main_ui_hud_button("Debug", [
                                            Function(main_ui_close_inventory_dropdown),
                                            Jump("DebugBuilderRoom"),
                                        ], str(rooms.current_code or "") == "DebugBuilderRoom", "main_ui_debug_builder_button")

                                    if bool(main_ui_runtime.inventory_dropdown_open):
                                        for _inv_section in player_card_inventory_section_ids():
                                            textbutton player_card_inventory_section_button_caption(_inv_section):
                                                id ("main_ui_inventory_section_%s" % _inv_section)
                                                style "mui_hud_subbutton"
                                                action [
                                                    Function(main_ui_open_inventory_section, _inv_section),
                                                ]

                            null height 6

                            text "дрова [int(_chores.get('bring_woods', 0) or 0)]/[player_chore_target('bring_woods')]   колка [int(_chores.get('chop_wood', 0) or 0)]/[player_chore_target('chop_wood')]   огонь [int(_chores.get('make_fire', 0) or 0)]/[player_chore_target('make_fire')]" size 17 xalign 0.5 color "#aaaaaa"
                            text "зола [int(_chores.get('clean_ashes', 0) or 0)]/[player_chore_target('clean_ashes')]   вода [int(_chores.get('boil_water', 0) or 0)]/[player_chore_target('boil_water')]   комнаты [int(_chores.get('clean_upstairs_rooms', 0) or 0)]/[player_chore_target('clean_upstairs_rooms')]" size 17 xalign 0.5 color "#aaaaaa"

                    if str(rooms.current_code or "") == "DebugBuilderRoom":
                        use debug_builder_state_controls(_chores)

                    frame:
                        xfill True
                        yminimum 300
                        padding (10, 10)
                        background "#000000ff"
                        $ _native_choice_screen = renpy.get_screen("choice")
                        $ _native_choice_label = _native_choice_screen.scope.get("label", None) if _native_choice_screen is not None else None
                        vbox:
                            spacing 10

                            text (_native_choice_label or main_ui_runtime.action_title) size 22 xalign 0.5

                            vbox:
                                xfill True
                                spacing 6
                                use current_action_panel(_native_choice_screen)

                    if str(main_ui_runtime.mode or "") != "event":
                        null yfill True

                        frame:
                            xfill True
                            yminimum 180
                            padding (10, 8)
                            background "#000000ff"
                            vbox:
                                spacing 8
                                text "Персонажи" size 20

                                if _char_entries:
                                    grid 3 3:
                                        spacing 6
                                        for _entry_index, _entry in enumerate(_char_slots):
                                            if _entry:
                                                $ _npc_name = str(_entry.get("title", "") or "")
                                                $ _npc_id = str(_entry.get("id", "") or "")
                                                $ _entity_type = str(_entry.get("entity_type", "npc") or "npc")
                                                $ _where_id = str(_entry.get("where_id", "") or rooms.current_code or "")
                                                $ _entity_data = dict(_entry.get("entity_data", {}) or {})
                                                $ _talk_label = str(_entity_data.get("talk_label", "") or "").strip()
                                                $ _talk_args = tuple(_entity_data.get("talk_args", ()) or ())
                                                if _npc_id.lower() == "you":
                                                    textbutton _npc_name:
                                                        id "main_ui_entity_button_player_you"
                                                        alt "main_ui_entity_button_player_you"
                                                        xminimum 150
                                                        text_size 18
                                                        action [
                                                            Function(main_ui_close_inventory_dropdown),
                                                            Function(show_player_card_main_ui_state),
                                                        ]
                                                elif _npc_id.lower() == "dog":
                                                    textbutton _npc_name:
                                                        id "main_ui_entity_button_dog_dog"
                                                        alt "main_ui_entity_button_dog_dog"
                                                        xminimum 150
                                                        text_size 18
                                                        action [
                                                            Function(main_ui_close_inventory_dropdown),
                                                            Call("IntDogTalk", _where_id),
                                                        ]
                                                elif _npc_id.lower() == "draupnir" and int(player.tavern_management.slogan_state or 0) == 1:
                                                    textbutton _npc_name:
                                                        id "main_ui_entity_button_npc_draupnir_repairing"
                                                        alt "main_ui_entity_button_npc_draupnir_repairing"
                                                        xminimum 150
                                                        text_size 18
                                                        sensitive False
                                                        action NullAction()
                                                else:
                                                    textbutton _npc_name:
                                                        id "main_ui_entity_button_{}_{}".format(_entity_type, _npc_id)
                                                        alt "main_ui_entity_button_{}_{}".format(_entity_type, _npc_id)
                                                        xminimum 150
                                                        text_size 18
                                                        sensitive bool(_talk_label and renpy.has_label(_talk_label))
                                                        action [
                                                            Function(main_ui_close_inventory_dropdown),
                                                            Call(_talk_label, *_talk_args),
                                                        ]
                                            else:
                                                # Move null outside textbutton block
                                                null width 150 height 34
                                else:
                                    text "Никого нет." size 20

    if str(main_ui_runtime.overlay or "") == "story":
        use story_thread_board_panel
    elif str(main_ui_runtime.overlay or "") == "time":
        use time_change_panel
    elif str(main_ui_runtime.overlay or "") == "people":
        use people_locate_panel
    elif str(main_ui_runtime.overlay or "") == "progress":
        use tractir_progress_panel


screen main_ui_left_panel(room_name, desc, picture):
    if str(main_ui_runtime.mode or "scene") == "mc":
        use main_ui_player_card_panel()
    elif str(main_ui_runtime.mode or "scene") == "tavern":
        use main_ui_tavern_report_panel()
    elif str(main_ui_runtime.mode or "scene") == "dog":
        use main_ui_dog_card_panel()
    elif str(main_ui_runtime.mode or "scene") == "werecat":
        use main_ui_werecat_card_panel()
    elif str(main_ui_runtime.mode or "scene") == "fight":
        use main_ui_fight_panel()
    elif str(main_ui_runtime.mode or "scene") == "talk" and str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "") != "":
        use main_ui_talk_panel(str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or ""), room_name, desc)
    elif str(main_ui_runtime.mode or "scene") in ("char", "event") and str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "") != "":
        use main_ui_girl_card_panel(str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or ""))
    else:
        vbox:
            xfill True
            yfill True
            spacing 8

            text room_name size 20

            fixed:
                xfill True
                ymaximum int((config.screen_height - int(getattr(gui, "textbox_height", 278)) - 24) * 0.72)
                use BGIMAGE(picture)

            frame:
                xfill True
                yminimum 350
                ymaximum 420
                padding (12, 10)
                background "#000000ff"

                if str(rooms.current_code or "") == "DebugBuilderRoom":
                    viewport:
                        xfill True
                        yfill True
                        draggable True
                        mousewheel True

                        text desc size 20
                else:
                    text desc size 20


screen main_ui_talk_panel(girl_name="", room_name="", desc=""):
    $ _girl_key = girl_card_resolved_key(girl_name)
    $ _title = str(main_ui_runtime.action_title or ("Разговор с %s" % girl_card_display_name(_girl_key)))
    $ _talk_origin_picture = str(dict(main_ui_runtime.talk_origin or {}).get("picture", "") or "")
    $ _scene_picture = str(scene_runtime.picture or "")
    $ _portrait = _scene_picture if _scene_picture and _scene_picture != _talk_origin_picture else str(main_ui_runtime.talk_picture or main_ui_talk_picture_path(_girl_key) or "")
    $ _text = str(scene_runtime.text or scene_runtime.location_text or desc or "")
    $ _usable_h = max(360, int(config.screen_height) - int(getattr(gui, "textbox_height", 278)))
    $ _picture_h = int((_usable_h - 24) * 0.68)

    vbox:
        xfill True
        yfill True
        spacing 8

        text _title size 20

        fixed:
            xfill True
            ymaximum _picture_h
            if str(_portrait or "").strip():
                add Transform(_portrait, fit="contain", xalign=0.5, yalign=0.0)
            else:
                use BGIMAGE(None)

        frame:
            xfill True
            yminimum 260
            ymaximum 420
            padding (12, 10)
            background "#000000ff"

            viewport:
                id ("main_ui_talk_text_%s" % hash(_text))
                xfill True
                yfill True
                yinitial 0.0
                draggable True
                mousewheel True

                text _text size 20


screen main_ui_player_card_panel():
    $ _title = player_card_panel_title()
    $ _portrait = player_card_portrait_path()
    $ _stats_left = player_card_stat_rows_left()
    $ _stats_right = player_card_stat_rows_right()
    $ _lines = player_card_panel_lines()
    $ _inventory_mode = str(main_ui_runtime.inventory_view_mode or "profile")
    $ _inventory_ids = list(player_card_inventory_ids(False) or []) if _inventory_mode == "inventory" else (list(player_card_inventory_section_item_ids(main_ui_runtime.inventory_view_section) or []) if _inventory_mode == "section" else [])
    $ _inventory_rows = [_inventory_ids[index:index + 2] for index in range(0, len(_inventory_ids), 2)]
    $ _usable_h = max(360, int(config.screen_height) - int(getattr(gui, "textbox_height", 278)))
    $ _left_h = _usable_h - 24
    $ _inventory_column_width = int((((config.screen_width - 36) * 0.72) - 72) / 2)

    fixed:
        xfill True
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        viewport:
            xpos 28
            ypos 24
            xsize int((config.screen_width - 36) * 0.72) - 56
            ysize _left_h - 96
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                if _inventory_mode == "profile":
                    hbox:
                        spacing 12

                        add im.Scale(_portrait, 180, 240)

                        hbox:
                            spacing 24

                            vbox:
                                xminimum 220
                                spacing 3
                                for _row in _stats_left:
                                    text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                            vbox:
                                xminimum 220
                                spacing 3
                                for _row in _stats_right:
                                    text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                for _line in _lines:
                    text _line size (18 if _inventory_mode in ("inventory", "section") else 16) color "#2d1d12"

                if _inventory_mode in ("inventory", "section") and len(_inventory_rows) > 0:
                    null height 4
                    vbox:
                        spacing 10
                        for _inventory_row in _inventory_rows:
                            hbox:
                                spacing 16
                                for _item_id in _inventory_row:
                                    $ _item_name = player_card_inventory_menu_caption(_item_id, False)
                                    $ _item_quantity = int(player_card_inventory_count(_item_id) or 0)
                                    button:
                                        id ("main_ui_inventory_item_%s" % _item_id)
                                        style "mui_inventory_item_button"
                                        xsize _inventory_column_width
                                        action Call("PlayerCardInventoryItemMenu", _item_id)

                                        hbox:
                                            xfill True
                                            text _item_name:
                                                style "mui_inventory_item_name"
                                                xsize _inventory_column_width - 100
                                            text "x%s" % _item_quantity:
                                                style "mui_inventory_item_quantity"
                                                xsize 60
                                                xalign 1.0

                                if len(_inventory_row) < 2:
                                    null width _inventory_column_width

screen main_ui_girl_card_panel(girl_name=""):
    $ _girl_key = girl_card_resolved_key(girl_name)
    $ _title = girl_card_display_name(_girl_key)
    $ _portrait = girl_card_portrait_path(_girl_key)
    $ _stats = girl_card_stat_rows(_girl_key)
    $ _lines = girl_card_body_lines(_girl_key)
    $ _usable_h = max(360, int(config.screen_height) - int(getattr(gui, "textbox_height", 278)))
    $ _left_h = _usable_h - 24

    fixed:
        xfill True
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        viewport:
            xpos 28
            ypos 24
            xsize int((config.screen_width - 36) * 0.72) - 56
            ysize _left_h - 96
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                hbox:
                    spacing 12

                    add im.Scale(_portrait, 180, 240)

                    vbox:
                        spacing 3
                        for _row in _stats:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                for _line in _lines:
                    text _line size 16 color "#2d1d12"

screen main_ui_dog_card_panel():
    $ _title = dog_card_title()
    $ _portrait = dog_card_portrait_path()
    $ _stats = dog_card_stat_rows()
    $ _lines = dog_card_lines()
    $ _usable_h = max(360, int(config.screen_height) - int(getattr(gui, "textbox_height", 278)))
    $ _left_h = _usable_h - 24

    fixed:
        xfill True
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        viewport:
            xpos 28
            ypos 24
            xsize int((config.screen_width - 36) * 0.72) - 56
            ysize _left_h - 96
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                hbox:
                    spacing 12

                    add im.Scale(_portrait, 180, 240)

                    vbox:
                        spacing 3
                        for _row in _stats:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                for _line in _lines:
                    text _line size 16 color "#2d1d12"

screen main_ui_werecat_card_panel():
    $ _title = werecat_card_title()
    $ _portrait = werecat_picture_path()
    $ _stats = werecat_card_stat_rows()
    $ _lines = werecat_card_lines()
    $ _usable_h = max(360, int(config.screen_height) - int(getattr(gui, "textbox_height", 278)))
    $ _left_h = _usable_h - 24

    fixed:
        xfill True
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        viewport:
            xpos 28
            ypos 24
            xsize int((config.screen_width - 36) * 0.72) - 56
            ysize _left_h - 96
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                hbox:
                    spacing 12

                    add im.Scale(_portrait, 180, 240)

                    vbox:
                        spacing 3
                        for _row in _stats:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                for _line in _lines:
                    text _line size 16 color "#2d1d12"

screen main_ui_tavern_report_panel():
    $ _report = BuildTavernReport()
    $ _person = str(main_ui_runtime.tavern_report_person or "")
    $ _title = _tavern_name(_person) if _person else "ТРАКТИР"
    $ _body = _tavern_worker_label(_person) if _person else _tavern_report_label(_report)
    $ _usable_h = max(360, int(config.screen_height) - int(getattr(gui, "textbox_height", 278)))
    $ _left_h = _usable_h - 24

    fixed:
        xfill True
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        viewport:
            xpos 28
            ypos 24
            xsize int((config.screen_width - 36) * 0.72) - 56
            ysize _left_h - 48
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5
                text _body size 18 color "#2d1d12"

                if not _person and _report["team_keys"]:
                    null height 4
                    text "Завтрашняя смена" size 22 color "#1e130c"

                    vbox:
                        spacing 6

                        for _worker in _report["team_keys"]:
                            hbox:
                                spacing 8
                                xfill True

                                textbutton _tavern_name(_worker):
                                    xminimum 180
                                    text_size 20
                                    text_bold True
                                    text_color "#6d1020"
                                    action Call("ShowTavernReportPerson", _worker, "__main_ui__")

                                textbutton _tavern_job_button_caption("jobkitchentomorrow", _worker, "Кухня"):
                                    id "tavern_schedule_%s_kitchen" % _worker
                                    xminimum 120
                                    text_size 18
                                    text_bold True
                                    text_color "#6d1020"
                                    action Function(toggle_hall_job_with_limit, "jobkitchentomorrow", _worker)

                                textbutton _tavern_job_button_caption("jobcleaningtomorrow", _worker, "Уборка"):
                                    id "tavern_schedule_%s_cleaning" % _worker
                                    xminimum 130
                                    text_size 18
                                    text_bold True
                                    text_color "#6d1020"
                                    action Function(toggle_hall_job_with_limit, "jobcleaningtomorrow", _worker)

                                textbutton _tavern_job_button_caption("jobwaitresstomorrow", _worker, "Зал"):
                                    id "tavern_schedule_%s_waitress" % _worker
                                    xminimum 120
                                    text_size 18
                                    text_bold True
                                    text_color "#6d1020"
                                    action Function(toggle_hall_job_with_limit, "jobwaitresstomorrow", _worker)

