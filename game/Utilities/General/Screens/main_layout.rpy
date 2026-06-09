# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default CurrentRoom = None
default current_action_title = "Actions"
default current_action_content = None
default current_action_items = []
default current_girl_key = ""
default current_object_id = ""
default current_room_code = ""
default scene_image = ""
default UI_mode = "scene"
default UI_selected_char = ""
default main_ui_inventory_dropdown_open = False
default main_ui_overlay = ""
default story_board_hover_event_thread = None
default story_board_hover_event_index = -1
default story_board_control_thread_name = ""

init python:
    import renpy.exports as renpy_module

    def main_ui_restart_interaction():
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def main_ui_set_action_panel(title="", items=None, content=None, ui_mode=None, selected_char=None, clear_specs=True, restart=True):
        global UI_mode, UI_selected_char, current_girl_key, current_action_content
        global current_action_title, current_action_items, main_ui_inventory_dropdown_open, action_menu_specs

        if str(title or "").strip():
            current_action_title = str(title or "")
        current_action_content = content
        current_action_items = list(items or [])
        main_ui_inventory_dropdown_open = False

        if ui_mode is not None:
            UI_mode = str(ui_mode or "scene")
        if selected_char is not None:
            UI_selected_char = str(selected_char or "")
            current_girl_key = str(selected_char or "")
        elif str(ui_mode or "") in ("scene", "event"):
            UI_selected_char = ""
            current_girl_key = ""
        if clear_specs:
            action_menu_specs = []
        if restart:
            main_ui_restart_interaction()

    def main_ui_call_label(label_name="", *label_args):
        label = str(label_name or "").strip()
        if not label:
            return
        has_label_fn = getattr(renpy_module, "has_label", None)
        if callable(has_label_fn) and not has_label_fn(label):
            return
        call_new_context_fn = getattr(renpy_module, "call_in_new_context", None)
        if callable(call_new_context_fn):
            return call_new_context_fn(label, *tuple(label_args or ()))
        raise Exception("Cannot call Ren'Py label from main UI: call_in_new_context is unavailable.")

    def main_ui_restore_room_scene_state():
        global UI_mode, UI_selected_char, current_girl_key, current_action_content
        global current_action_title, current_action_items, current_object_id, CurrentRoom, CurLoc
        global main_ui_inventory_dropdown_open, action_menu_specs, action_menu_entity_type
        global action_menu_entity_id, action_menu_where, action_menu_title, action_menu_entity_data
        global action_menu_actions, action_menu_selected

        UI_mode = "scene"
        UI_selected_char = ""
        current_girl_key = ""
        current_action_content = None
        current_object_id = ""
        main_ui_inventory_dropdown_open = False
        action_menu_entity_type = ""
        action_menu_entity_id = ""
        action_menu_where = ""
        action_menu_title = ""
        action_menu_entity_data = {}
        action_menu_actions = []
        action_menu_selected = ""
        action_menu_specs = []

        room_obj = CurrentRoom
        room_code = str(getattr(room_obj, "code_name", "") or CurLoc or "").strip()
        if room_code == "TavernKitchen" and bool(TavernBreakfastEventActive):
            tavern_breakfast_restore_ui_state()
            return
        refresh_targets = {}
        try:
            refresh_targets = dict(_action_refresh_target_labels(room_code) or {})
        except Exception:
            refresh_targets = {}
        if room_code == "TavernMain" or bool(str(refresh_targets.get("build", "") or "").strip()) or bool(str(refresh_targets.get("object", "") or "").strip()):
            main_ui_call_label("RefreshCurrentActionMenu", room_code, "", True)
            return
        current_action_title = "Действия в трактире" if room_code == "TavernMain" else "Действия"
        room_sections = room_obj.build_menu_sections() if room_obj is not None and hasattr(room_obj, "build_menu_sections") else {"movement": [], "actions": []}
        current_action_items = list(room_sections.get("movement", [])) + list(room_sections.get("actions", []))

        main_ui_restart_interaction()

    def main_ui_toggle_inventory_dropdown():
        global main_ui_inventory_dropdown_open

        main_ui_inventory_dropdown_open = not bool(main_ui_inventory_dropdown_open)
        main_ui_restart_interaction()

    def main_ui_close_inventory_dropdown():
        global main_ui_inventory_dropdown_open

        main_ui_inventory_dropdown_open = False
        main_ui_restart_interaction()

    def main_ui_open_inventory_section(section_id=""):
        global main_ui_inventory_dropdown_open

        main_ui_inventory_dropdown_open = False
        player_card_set_inventory_origin("room")
        player_card_show_inventory_section_state(section_id)

    def main_ui_entity_button_spec(entity_type="", entity_id="", entity_data=None):
        entity_key = str(entity_type or "").strip().lower()
        npc_key = str(entity_id or "").strip()
        state = {
            "id": "open_entity_menu",
            "entity_type": entity_key,
            "entity_id": npc_key,
            "where_id": str(CurLoc or ""),
            "entity_data": dict(entity_data or {}),
        }
        if npc_key.lower() == "you":
            state["id"] = "open_player_card"
        elif npc_key.lower() == "dog":
            state["id"] = "open_dog_menu"
        return state

    def main_ui_begin_talk_state(title="", selected_char=""):
        global UI_mode, UI_selected_char, current_girl_key, current_action_content, current_action_title

        UI_mode = "talk"
        current_action_content = None

        char_key = str(selected_char or "").strip()
        if char_key:
            UI_selected_char = char_key
            current_girl_key = char_key

        if str(title or "").strip():
            current_action_title = str(title)

        main_ui_restart_interaction()

    def main_ui_end_talk_state():
        main_ui_restore_room_scene_state()

    def main_ui_begin_native_scene_state(title=""):
        global UI_mode, current_action_title, current_action_content, current_action_items
        global UI_selected_char, current_girl_key

        UI_mode = "event"
        UI_selected_char = ""
        current_girl_key = ""
        current_action_content = None
        current_action_items = []
        if str(title or "").strip():
            current_action_title = str(title)

        main_ui_restart_interaction()

    def main_ui_end_native_scene_state():
        main_ui_restore_room_scene_state()

    def tractir_after_load_restore_ui():
        global current_action_content, current_action_items, CurrentRoom, current_room_code

        try:
            current_action_content = None
            current_action_items = []
        except Exception:
            pass

        try:
            if str(CurLoc or "") == "Intro":
                return
        except Exception:
            return

        try:
            restored_room = get_registered_room(str(CurLoc or ""))
            if restored_room is not None:
                CurrentRoom = restored_room
                current_room_code = str(getattr(restored_room, "code_name", "") or CurLoc or "")
            elif CurrentRoom is not None:
                current_room_code = str(getattr(CurrentRoom, "code_name", "") or CurLoc or "")
            else:
                current_room_code = str(CurLoc or "")
        except Exception:
            pass

        try:
            main_ui_restore_room_scene_state()
        except Exception:
            pass

    if tractir_after_load_restore_ui not in config.after_load_callbacks:
        config.after_load_callbacks.append(tractir_after_load_restore_ui)

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

    style mui_hud_subbutton is mui_hud_button:
        yminimum 34
        left_padding 18
        background Solid("#0e0e0e")
        hover_background Solid("#201a14")

    style mui_hud_subbutton_text is mui_hud_button_text:
        size 18

    style mui_status_label is default:
        size 18
        color "#a39a8b"
        xminimum 76

    style mui_status_value is default:
        size 18

label ReturnMainUISceneMode:
    $ main_ui_restore_room_scene_state()
    return


screen current_action_panel():
    if list(action_menu_specs or []):
        use npc_action_menu(action_menu_specs)
    elif current_action_content:
        use expression current_action_content
    elif current_action_items:
        use choice_panel(current_action_items)
    elif str(UI_mode or "") in ("mc", "char", "dog", "fight", "event"):
        null
    elif str(getattr(CurrentRoom, "code_name", "") or CurLoc or "").strip() == "TavernKitchen" and bool(TavernBreakfastEventActive):
        null
    elif CurrentRoom is not None:
        $ action_items = build_room_action_items(CurrentRoom)
        use choice_panel(action_items)
    else:
        text "Выберите действие." size 20


screen npc_action_menu(specs):
    vbox:
        for spec in list(specs or []):
            $ _spec_id = str(spec.get("id", "") or "").strip()
            $ _spec_text = str(spec.get("text", "") or "").strip()
            if _spec_text:
                if _spec_id == "close_inventory":
                    textbutton _spec_text action Function(main_ui_close_inventory_dropdown):
                        text_size 20
                elif _spec_id == "look":
                    textbutton _spec_text action Call("ActionMenuRunSpec", _spec_id, str(spec.get("entity_type", "") or ""), str(spec.get("entity_id", "") or ""), str(spec.get("where_id", "") or "")):
                        text_size 20
                elif _spec_id == "talk":
                    textbutton _spec_text action Call("ActionMenuRunSpec", _spec_id, str(spec.get("entity_type", "") or ""), str(spec.get("entity_id", "") or ""), str(spec.get("where_id", "") or "")):
                        text_size 20
                elif _spec_id == "flirt":
                    textbutton _spec_text action Call("ActionMenuRunSpec", _spec_id, str(spec.get("entity_type", "") or ""), str(spec.get("entity_id", "") or ""), str(spec.get("where_id", "") or "")):
                        text_size 20
                elif _spec_id == "gift":
                    textbutton _spec_text action Call("ActionMenuRunSpec", _spec_id, str(spec.get("entity_type", "") or ""), str(spec.get("entity_id", "") or ""), str(spec.get("where_id", "") or "")):
                        text_size 20
                elif _spec_id == "back":
                    textbutton _spec_text action Function(action_menu_handle_back_state):
                        text_size 20


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
                        selected int(time or 0) == _slot_id
                        action Function(debug_builder_set_time_slot_control, _slot_id)

            hbox:
                spacing 8
                text "Weekday" size 15 xsize 72
                textbutton "<":
                    id "debug_builder_week_prev"
                    alt "debug_builder_week_prev"
                    text_size 16
                    action Function(debug_builder_step_weekday, -1)
                text str(week_name or week or "") size 15 xminimum 120
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
                text str(month_name or month or "") size 15 xminimum 160
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
    modal True
    zorder 0

    key "dismiss" action NullAction()
    if CurLoc == "Intro":
        key "game_menu" action NullAction()
    else:
        key "game_menu" action ShowMenu("save")
        key "K_l" action SetVariable("main_ui_overlay", "people")
        key "K_t" action SetVariable("main_ui_overlay", "story")
        key "K_i" action Function(main_ui_toggle_inventory_dropdown)
        key "K_p" action Function(show_player_card_main_ui_state)
        if config.developer:
            key "K_F8" action Jump("dev_after_report_checkpoint")

    $ _room = CurrentRoom
    $ _room_name = _room.display_name if _room is not None else str(CurLoc or location or "")
    $ _desc = str(_coerce_panel_text_value(MainTxt if MainTxt is not None else CurLocDesc) or "")
    $ _picture = resolve_main_ui_picture(_room)
    $ _npcs = _room.visible_npcs() if _room is not None and hasattr(_room, "visible_npcs") else []
    $ _char_entries = _character_action_grid_entries(_room)
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

                if CurLoc == "Intro":
                    textbutton "Приступить к управлению трактиром":
                        text_size 20
                        action Jump("TavernMain")
                else:
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
                                    use main_ui_status_item("money", money, "#f0d08a")

                                vbox:
                                    xfill True
                                    spacing 6
                                    use main_ui_hud_button("Трактир", [
                                        Function(main_ui_close_inventory_dropdown),
                                        Hide("girl_card_overlay"),
                                        Hide("player_card_overlay"),
                                        Hide("tavern_report_card_overlay"),
                                        Call("ShowTavernReport", "__main_ui__"),
                                    ], str(UI_mode or "") == "tavern", "main_ui_tavern_button")
                                    use main_ui_hud_button("Время", [Function(main_ui_close_inventory_dropdown), SetVariable("main_ui_overlay", "time")], str(main_ui_overlay or "") == "time", "main_ui_time_button")
                                    use main_ui_hud_button("Сюжеты", [Function(main_ui_close_inventory_dropdown), Function(story_board_refresh), SetVariable("main_ui_overlay", "story")], str(main_ui_overlay or "") == "story", "main_ui_story_button")
                                    use main_ui_hud_button("Итоги", [Function(main_ui_close_inventory_dropdown), SetVariable("main_ui_overlay", "progress")], str(main_ui_overlay or "") == "progress", "main_ui_progress_button")
                                    use main_ui_hud_button("Кто где", [Function(main_ui_close_inventory_dropdown), SetVariable("main_ui_overlay", "people")], str(main_ui_overlay or "") == "people", "main_ui_people_button")
                                    use main_ui_hud_button("Инвентарь", Function(main_ui_toggle_inventory_dropdown), bool(main_ui_inventory_dropdown_open), "main_ui_inventory_button")

                                    if bool(main_ui_inventory_dropdown_open):
                                        for _inv_section in player_card_inventory_section_ids():
                                            textbutton player_card_inventory_section_button_caption(_inv_section):
                                                style "mui_hud_subbutton"
                                                action [
                                                    Hide("girl_card_overlay"),
                                                    Hide("player_card_overlay"),
                                                    Hide("tavern_report_card_overlay"),
                                                    Function(main_ui_open_inventory_section, _inv_section),
                                                ]

                            null height 6

                            text "дрова [int(_chores.get('bring_woods', 0) or 0)]/[player_chore_target('bring_woods')]   колка [int(_chores.get('chop_wood', 0) or 0)]/[player_chore_target('chop_wood')]   огонь [int(_chores.get('make_fire', 0) or 0)]/[player_chore_target('make_fire')]" size 17 xalign 0.5 color "#aaaaaa"
                            text "зола [int(_chores.get('clean_ashes', 0) or 0)]/[player_chore_target('clean_ashes')]   вода [int(_chores.get('boil_water', 0) or 0)]/[player_chore_target('boil_water')]   комнаты [int(_chores.get('clean_upstairs_rooms', 0) or 0)]/[player_chore_target('clean_upstairs_rooms')]" size 17 xalign 0.5 color "#aaaaaa"

                    if str(CurLoc or "") == "DebugBuilderRoom":
                        use debug_builder_state_controls(_chores)

                    frame:
                        xfill True
                        yminimum 300
                        padding (10, 10)
                        background "#000000ff"
                        has vbox
                        spacing 10

                        text current_action_title size 22 xalign 0.5

                        viewport:
                            xfill True
                            yfill True
                            draggable True
                            mousewheel True
                            vbox:
                                spacing 6
                                use current_action_panel

                    if str(UI_mode or "") != "event":
                        frame:
                            xfill True
                            yminimum 230
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
                                                $ _entity_data = dict(_entry.get("entity_data", {}) or {})
                                                $ _npc_spec = main_ui_entity_button_spec(_entity_type, _npc_id, _entity_data)
                                                if str(_npc_spec.get("id", "") or "") == "open_player_card":
                                                    textbutton _npc_name:
                                                        id "main_ui_entity_button_player_you"
                                                        alt "main_ui_entity_button_player_you"
                                                        xminimum 150
                                                        text_size 18
                                                        action [
                                                            Function(main_ui_close_inventory_dropdown),
                                                            Hide("girl_card_overlay"),
                                                            Hide("player_card_overlay"),
                                                            Hide("tavern_report_card_overlay"),
                                                            Function(show_player_card_main_ui_state),
                                                        ]
                                                elif str(_npc_spec.get("id", "") or "") == "open_dog_menu":
                                                    textbutton _npc_name:
                                                        id "main_ui_entity_button_dog_dog"
                                                        alt "main_ui_entity_button_dog_dog"
                                                        xminimum 150
                                                        text_size 18
                                                        action [
                                                            Function(main_ui_close_inventory_dropdown),
                                                            Hide("girl_card_overlay"),
                                                            Hide("player_card_overlay"),
                                                            Call("OpenEntityActionMenu", str(_npc_spec.get("entity_type", "") or ""), str(_npc_spec.get("entity_id", "") or ""), str(_npc_spec.get("where_id", "") or ""), dict(_npc_spec.get("entity_data", {}) or {})),
                                                        ]
                                                else:
                                                    textbutton _npc_name:
                                                        id "main_ui_entity_button_{}_{}".format(_entity_type, _npc_id)
                                                        alt "main_ui_entity_button_{}_{}".format(_entity_type, _npc_id)
                                                        xminimum 150
                                                        text_size 18
                                                        action [
                                                            Function(main_ui_close_inventory_dropdown),
                                                            Hide("girl_card_overlay"),
                                                            Hide("player_card_overlay"),
                                                            Call("OpenNpcActionMenu", str(_npc_spec.get("entity_id", "") or ""), str(_npc_spec.get("where_id", "") or ""), dict(_npc_spec.get("entity_data", {}) or {})),
                                                        ]
                                            else:
                                                # Move null outside textbutton block
                                                null width 150 height 34
                                else:
                                    text "Никого нет." size 20

    if str(main_ui_overlay or "") == "story":
        use story_thread_board_panel
    elif str(main_ui_overlay or "") == "people":
        use people_locate_panel
    elif str(main_ui_overlay or "") == "time":
        use time_change_card_overlay("__main_ui_overlay__")
    elif str(main_ui_overlay or "") == "progress":
        use tractir_progress_panel


screen main_ui_left_panel(room_name, desc, picture):
    if str(UI_mode or "scene") == "mc" and str(player_inventory_view_mode or "profile") == "profile":
        use main_ui_player_card_panel()
    elif str(UI_mode or "scene") == "tavern":
        use main_ui_tavern_report_panel()
    elif str(UI_mode or "scene") == "dog":
        use main_ui_dog_card_panel()
    elif str(UI_mode or "scene") == "werecat":
        use main_ui_werecat_card_panel()
    elif str(UI_mode or "scene") == "fight":
        use main_ui_fight_panel()
    elif str(UI_mode or "scene") == "char" and str(UI_selected_char or current_girl_key or "") != "":
        use main_ui_girl_card_panel(str(UI_selected_char or current_girl_key or ""))
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

                if str(CurLoc or "") == "DebugBuilderRoom":
                    viewport:
                        xfill True
                        yfill True
                        draggable True
                        mousewheel True
                        scrollbars "vertical"

                        text desc size 20
                else:
                    text desc size 20


screen main_ui_player_card_panel():
    $ _title = player_card_panel_title()
    $ _portrait = player_card_portrait_path()
    $ _stats_left = player_card_stat_rows_left()
    $ _stats_right = player_card_stat_rows_right()
    $ _lines = player_card_panel_lines()
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

                if str(player_inventory_view_mode or "profile") == "profile":
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
                    text _line size 16 color "#2d1d12"

                null height 8

                if len(list(FightEnemyParty or [])) <= 0:
                    textbutton "Назад":
                        xminimum 220
                        text_size 22
                        text_bold True
                        text_color "#5c0f1b"
                        text_hover_color "#7d1a2c"
                        action Function(main_ui_restore_room_scene_state)


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
            ysize _left_h - 48
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

                null height 8

                textbutton "Назад":
                    xminimum 220
                    text_size 22
                    text_bold True
                    text_color "#5c0f1b"
                    text_hover_color "#7d1a2c"
                    action Function(main_ui_restore_room_scene_state)


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
            ysize _left_h - 48
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

                null height 8

                textbutton "Назад":
                    xminimum 220
                    text_size 22
                    text_bold True
                    text_color "#5c0f1b"
                    text_hover_color "#7d1a2c"
                    action Function(main_ui_restore_room_scene_state)


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
            ysize _left_h - 48
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

                null height 8

                textbutton "Назад":
                    xminimum 220
                    text_size 22
                    text_bold True
                    text_color "#5c0f1b"
                    text_hover_color "#7d1a2c"
                    action Function(main_ui_restore_room_scene_state)


screen fight_side_status_column(title="", rows=None, energy_label="Энергия"):
    frame:
        xminimum 255
        xmaximum 300
        yfill True
        padding (12, 10)
        background "#ead9b8"

        vbox:
            spacing 8
            text str(title or "") size 22 color "#1e130c" xalign 0.5

            for _row in list(rows or []):
                frame:
                    xfill True
                    padding (10, 8)
                    background "#f5ead3"

                    vbox:
                        spacing 3
                        text str(_row.get("name", "") or "") size 20 color "#301c10"
                        text str(_row.get("subtitle", "") or "") size 15 color "#6a4b32"
                        text "Здоровье: [int(_row.get('health', 0) or 0)] / [int(_row.get('health_max', 0) or 0)]" size 16 color "#301c10"
                        text "[str(energy_label or 'Энергия')]: [int(_row.get('energy', 0) or 0)] / [int(_row.get('energy_max', 0) or 0)]" size 16 color "#301c10"
                        if list(_row.get("status", []) or []):
                            text "Состояние: [', '.join(list(_row.get('status', []) or []))]" size 15 color "#7c2a1b"

screen fight_center_status_panel(picture="", result_text="", log_rows=None):
    vbox:
        xfill True
        spacing 10

        frame:
            xfill True
            ymaximum 300
            padding (10, 10)
            background "#ead9b8"

            if picture:
                add Transform(picture, fit="contain", xalign=0.5, yalign=0.0)
            else:
                text "Сцена боя" size 22 color "#1e130c" xalign 0.5

        frame:
            xfill True
            padding (12, 10)
            background "#f5ead3"

            vbox:
                spacing 4
                text "Снаряжение" size 20 color "#1e130c"
                text "Оружие: [str(EquippedWeapon or 'нет')]" size 16 color "#301c10"
                text "Броня: [str(EquippedArmor or 'нет')]" size 16 color "#301c10"
                text "Заряжено: [('да' if int(FightWeaponLoaded or 0) == 1 else 'нет')]" size 16 color "#301c10"
                text "Боеприпас: [fight_loaded_ammo_name(FightLoadedAmmo)]" size 16 color "#301c10"
                text "Запас стрел: [int(PlayerFightSupply.get('arrows', 0) or 0)]   дроби: [int(PlayerFightSupply.get('droplets', 0) or 0)]" size 16 color "#301c10"

        frame:
            xfill True
            yminimum 160
            padding (12, 10)
            background "#ead9b8"

            vbox:
                spacing 6
                text "Результат действия" size 20 color "#1e130c"
                text str(result_text or "") size 17 color "#2d1d12"

        if list(log_rows or []):
            frame:
                xfill True
                yminimum 140
                padding (12, 10)
                background "#f5ead3"

                vbox:
                    spacing 4
                    text "Журнал боя" size 20 color "#1e130c"
                    for _row in list(log_rows or []):
                        text str(_row or "") size 15 color "#2d1d12"

screen main_ui_fight_panel():
    $ _title = "БОЙ"
    $ _picture = resolve_main_ui_picture(CurrentRoom)
    $ _enemy_rows = fight_enemy_display_rows()
    $ _company_rows = fight_company_display_rows()
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

                text _title size 30 color "#1e130c" xalign 0.5

                hbox:
                    xfill True
                    spacing 14

                    use fight_side_status_column("ВАША СТОРОНА", _company_rows, "Энергия")

                    use fight_center_status_panel(_picture, str(MainTxt or CurLocDesc or ""), list(FightSideLog or []))

                    use fight_side_status_column("ПРОТИВНИКИ", _enemy_rows, "Напор")

                textbutton "Назад":
                    xminimum 220
                    text_size 22
                    text_bold True
                    text_color "#5c0f1b"
                    text_hover_color "#7d1a2c"
                    action Function(main_ui_restore_room_scene_state)


screen main_ui_tavern_report_panel():
    $ _report = BuildTavernReport()
    $ _person = str(TavernReportSelectedPerson or "")
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

                                textbutton _tavern_job_button_caption(jobkitchentomorrow, _worker, "Кухня"):
                                    xminimum 120
                                    text_size 18
                                    text_bold True
                                    text_color "#6d1020"
                                    action Call("TavernReportApplyOverviewAction", _worker, "kitchen", "__main_ui__")

                                textbutton _tavern_job_button_caption(jobcleaningtomorrow, _worker, "Уборка"):
                                    xminimum 130
                                    text_size 18
                                    text_bold True
                                    text_color "#6d1020"
                                    action Call("TavernReportApplyOverviewAction", _worker, "cleaning", "__main_ui__")

                                textbutton _tavern_job_button_caption(jobwaitresstomorrow, _worker, "Зал"):
                                    xminimum 120
                                    text_size 18
                                    text_bold True
                                    text_color "#6d1020"
                                    action Call("TavernReportApplyOverviewAction", _worker, "waitress", "__main_ui__")

                null height 8

                textbutton "Закрыть":
                    xminimum 220
                    text_size 22
                    text_bold True
                    text_color "#5c0f1b"
                    text_hover_color "#7d1a2c"
                    action Function(main_ui_restore_room_scene_state)


label ActionMenuRunSpec(spec_id="", entity_type="", entity_id="", where_id=""):
    $ _spec_key = str(spec_id or "").strip().lower()
    $ _entity_type = str(entity_type or "").strip().lower()
    $ _entity_id = str(entity_id or "").strip()
    $ _where_id = str(where_id or CurLoc or "").strip()
    if _spec_key == "look":
        $ action_menu_specs = []
        if _entity_type == "npc":
            $ NpcActionLookState(_entity_id, _where_id, dict(action_menu_entity_data or {}))
        elif _entity_type == "dog":
            $ DogActionLookState(_where_id)
        else:
            $ action_menu_handle_look_state()
        return
    if _spec_key == "talk":
        $ action_menu_specs = []
        if _entity_type == "npc":
            $ NpcActionTalkState(_entity_id, _where_id, dict(action_menu_entity_data or {}))
        elif _entity_type == "dog":
            $ DogActionTalkState(_where_id)
        else:
            $ action_menu_handle_talk_state()
        return
    if _spec_key == "flirt":
        $ action_menu_specs = []
        call SocialTalkTopicMenu(_entity_id, "flirt", social_topic_return_label(_entity_id))
        return
    if _spec_key == "gift":
        $ action_menu_specs = []
        if _entity_id == "clara":
            call IntClaraGiftMenu(_entity_id)
        else:
            call PlayerCardGiftToFixedTargetMenu(_entity_id)
        return
    if _spec_key.startswith("amanda_ai:") and _entity_id == "amanda":
        $ action_menu_specs = []
        if not bool(globals().get("AmandaAIIntegrationEnabled", False)):
            return
        $ _amanda_ai_intent = _spec_key.split(":", 1)[1]
        call AmandaAIIntentRoomEvent(_where_id, _amanda_ai_intent)
        return
    if _spec_key == "dog_bone":
        $ action_menu_specs = []
        call IntDogTalkApply(_where_id, "bone")
        return
    if _spec_key == "dog_call":
        $ action_menu_specs = []
        call IntDogTalkApply(_where_id, "call_stray")
        return
    if _spec_key == "dog_pet":
        $ action_menu_specs = []
        call IntDogTalkApply(_where_id, "pet_stray")
        return
    if _spec_key == "dog_play_stray":
        $ action_menu_specs = []
        call IntDogTalkApply(_where_id, "play_stray")
        return
    if _spec_key == "dog_stray_bone":
        $ action_menu_specs = []
        call IntDogTalkApply(_where_id, "stray_bone")
        return
    if _spec_key == "dog_adopt":
        $ action_menu_specs = []
        call IntDogTalkApply(_where_id, "adopt")
        return
    return
