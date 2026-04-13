default cah_character_id = ""
default cah_talk_label = ""
default cah_talk_args = ()
default cah_examine_id = ""
default cah_can_examine = True
default cah_can_talk = True

default npc_menu_character_id = ""
default npc_menu_display_name = ""
default npc_menu_talk_label = ""
default npc_menu_talk_args = ()
default npc_menu_examine_id = ""
default npc_menu_where = ""
default npc_menu_prev_picture = ""
default npc_menu_prev_scene = ""

init -40 python:
    import renpy.exports as renpy

    def _character_action_text(value, default=""):
        if callable(value):
            try:
                value = value()
            except TypeError:
                value = default
            except Exception:
                value = default
        return str(value or default or "")

    def _character_action_display_name(character_id):
        key = str(character_id or "").strip()
        if not key:
            return ""
        try:
            return str(RealName.get(key, key) or key)
        except Exception:
            return key

    def _character_action_npc_known(npc):
        if not isinstance(npc, dict):
            return True
        if "known_condition" not in npc:
            return True
        return room_rule_true(npc.get("known_condition", None))

    def _character_action_npc_display_name(npc):
        if not isinstance(npc, dict):
            return ""

        if _character_action_npc_known(npc):
            name_value = _character_action_text(npc.get("display_name", ""), "")
            if name_value:
                return name_value
            name_value = _character_action_text(npc.get("name", ""), "")
            if name_value:
                return name_value
            return _character_action_text(npc.get("npc_id", ""), "")

        unknown_name = _character_action_text(npc.get("unknown_name", ""), "")
        if unknown_name:
            return unknown_name

        unknown_gender = str(npc.get("unknown_gender", "") or "").strip().lower()
        if unknown_gender == "woman":
            return "Незнакомка"
        if unknown_gender == "man":
            return "Незнакомец"
        return "Незнакомец"

    def _character_action_npc_talk_args(npc):
        if not isinstance(npc, dict):
            return ()
        talk_args = npc.get("talk_args", ())
        if callable(talk_args):
            try:
                talk_args = talk_args()
            except Exception:
                talk_args = ()
        return tuple(talk_args or ())

    def _character_action_npc_can_examine(npc, character_id=""):
        if not isinstance(npc, dict):
            return bool(str(character_id or "").strip())

        npc_id = str(character_id or npc.get("npc_id", "") or "").strip()
        examine_target = _character_action_text(npc.get("examine_id", npc_id), npc_id)
        if not str(examine_target or "").strip():
            return False

        if not _character_action_npc_known(npc) and bool(npc.get("hide_examine_until_known", True)):
            return False

        return room_rule_true(npc.get("can_examine", True))

    def _character_action_show_portrait(character_id):
        # Keep compatibility hook; no forced image changes in the hub.
        try:
            global current_girl_key
            current_girl_key = str(character_id or "")
        except Exception:
            pass

    def show_npc_action_main_ui_state(character_id="", talk_label="", talk_args=(), examine_id="", where_id="", display_name="", can_examine=True):
        store = renpy.store
        store.npc_menu_character_id = str(character_id or "")
        store.npc_menu_display_name = str(display_name or "")
        store.npc_menu_talk_label = str(talk_label or "")
        store.npc_menu_talk_args = tuple(talk_args or ())
        store.npc_menu_examine_id = str(examine_id or character_id or "")
        store.npc_menu_where = str(where_id or store.CurLoc or "")

        npc_name = store.npc_menu_display_name or _character_action_display_name(store.npc_menu_character_id)
        npc_can_examine = bool(can_examine and store.npc_menu_examine_id and _character_action_examine_label(store.npc_menu_character_id))
        npc_can_talk = bool(store.npc_menu_talk_label and renpy.has_label(store.npc_menu_talk_label))

        store.current_action_title = npc_name or "Персонаж"
        store.current_action_content = None
        store.current_action_items = []

        if npc_can_examine:
            if store.npc_menu_character_id.lower() == "you":
                store.current_action_items.append(MenuItem("Осмотреть", Function(show_player_card_main_ui_state)))
            elif store.npc_menu_character_id.lower() == "dog":
                store.current_action_items.append(MenuItem("Осмотреть", Function(show_dog_card_main_ui_state)))
            else:
                store.current_action_items.append(MenuItem("Осмотреть", Function(show_girl_card_main_ui_state, store.npc_menu_examine_id)))
        if npc_can_talk:
            store.current_action_items.append(MenuItem("Поговорить", Function(main_ui_call_label, "NPCActionMenuTalk")))
        store.current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "NPCActionMenuBack")))

        restart_fn = getattr(renpy, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def _character_action_examine_label(character_id):
        cid = str(character_id or "").strip().lower()
        if cid == "you":
            return "ShowPlayerCard"
        if cid == "dog":
            return "ShowDogCard"
        if renpy.has_label("ShowGirlCard"):
            return "ShowGirlCard"
        return ""

    def _character_action_grid_entries(room):
        entries = [{
            "id": "you",
            "name": "Стефан",
            "display_name": "Стефан",
            "talk_label": "",
            "talk_args": (),
            "examine_id": "you",
            "can_examine": True,
        }]
        if room is None or not hasattr(room, "visible_npcs"):
            return entries

        for npc in room.visible_npcs():
            if not isinstance(npc, dict):
                continue
            npc_id = str(npc.get("npc_id", "") or "").strip()
            if not npc_id:
                continue
            npc_talk_label = npc.get("talk_label", "")
            if callable(npc_talk_label):
                try:
                    npc_talk_label = npc_talk_label()
                except Exception:
                    npc_talk_label = ""
            npc_examine_id = npc.get("examine_id", npc_id)
            if callable(npc_examine_id):
                try:
                    npc_examine_id = npc_examine_id()
                except Exception:
                    npc_examine_id = npc_id
            npc_auto_card = bool(npc.get("auto_card", False))
            entries.append({
                "id": npc_id,
                "name": _character_action_npc_display_name(npc),
                "display_name": _character_action_npc_display_name(npc),
                "talk_label": str(npc_talk_label or ""),
                "talk_args": _character_action_npc_talk_args(npc),
                "examine_id": str(npc_examine_id or npc_id),
                "can_examine": bool(_character_action_npc_can_examine(npc, npc_id)),
                "auto_card": npc_auto_card,
            })
        room_code = str(getattr(room, "code_name", "") or "")
        if room_code and dog_is_available_here(room_code):
            entries.append({
                "id": "dog",
                "name": dog_display_name(),
                "display_name": dog_display_name(),
                "talk_label": "IntDogTalk",
                "talk_args": (room_code,),
                "examine_id": "dog",
                "can_examine": True,
                "auto_card": True,
            })
        return entries[:9]

label CharacterActionHub(
    character_id="",
    talk_label="",
    talk_args=(),
    examine_id="",
    can_examine=True,
    can_talk=True,
):
    $ _name = _character_action_display_name(character_id)
    $ _examine_target = str(examine_id or character_id)
    $ _character_action_show_portrait(character_id)

    label character_action_hub_loop:
        $ _examine_label = _character_action_examine_label(character_id)
        $ _can_examine = bool(can_examine and _examine_target and _examine_label)
        $ _can_talk = bool(can_talk and talk_label and renpy.has_label(talk_label))
        menu:
            "Что вы хотите сделать с [_name]?"

            "Осмотреть" if _can_examine:
                $ _turn_state = consume_turn_for_action("examine", CurLoc)
                if _turn_state.get("day_advanced", False):
                    return
                if _examine_label == "ShowPlayerCard":
                    call CallPlayerCardModal
                else:
                    call CallGirlCardModal(_examine_target)
                $ _character_action_show_portrait(character_id)
                jump character_action_hub_loop

            "Поговорить" if _can_talk:
                $ _turn_state = consume_turn_for_action("talk", CurLoc)
                if _turn_state.get("day_advanced", False):
                    return
                $ _talk_label = str(talk_label or "")
                $ _talk_args = tuple(talk_args or ())
                if _talk_label and renpy.has_label(_talk_label):
                    if len(_talk_args) <= 0:
                        call expression _talk_label
                    elif len(_talk_args) == 1:
                        call expression _talk_label pass (_talk_args[0],)
                    elif len(_talk_args) == 2:
                        call expression _talk_label pass (_talk_args[0], _talk_args[1])
                    elif len(_talk_args) == 3:
                        call expression _talk_label pass (_talk_args[0], _talk_args[1], _talk_args[2])
                    else:
                        call expression _talk_label pass (_talk_args[0], _talk_args[1], _talk_args[2], _talk_args[3])
                $ _character_action_show_portrait(character_id)
                jump character_action_hub_loop

            "Назад":
                return

    return


label CharacterActionHubResume:
    call CharacterActionHub(cah_character_id, cah_talk_label, cah_talk_args, cah_examine_id, cah_can_examine, cah_can_talk)
    return


label CallGirlCardModal(girl_name=""):
    if str(girl_name or "") == "":
        return
    call screen girl_card_overlay(girl_name, "__return__")
    return


label CallPlayerCardModal:
    call screen player_card_overlay("__return__")
    return


label NPCActionMenu(character_id="", talk_label="", talk_args=(), examine_id="", where_id="", display_name="", can_examine=True):
    $ show_npc_action_main_ui_state(character_id, talk_label, talk_args, examine_id, where_id, display_name, can_examine)
    return


label NPCActionMenuExamine:
    if npc_menu_character_id.lower() == "you":
        call CallPlayerCardModal
    else:
        call CallGirlCardModal(npc_menu_examine_id)
    $ main_ui_restore_room_scene_state()
    return


label NPCActionMenuTalk:
    if len(npc_menu_talk_args) <= 0:
        call expression npc_menu_talk_label
    elif len(npc_menu_talk_args) == 1:
        call expression npc_menu_talk_label pass (npc_menu_talk_args[0],)
    elif len(npc_menu_talk_args) == 2:
        call expression npc_menu_talk_label pass (npc_menu_talk_args[0], npc_menu_talk_args[1])
    elif len(npc_menu_talk_args) == 3:
        call expression npc_menu_talk_label pass (npc_menu_talk_args[0], npc_menu_talk_args[1], npc_menu_talk_args[2])
    else:
        call expression npc_menu_talk_label pass (npc_menu_talk_args[0], npc_menu_talk_args[1], npc_menu_talk_args[2], npc_menu_talk_args[3])
    return


label NPCActionMenuBack:
    $ main_ui_restore_room_scene_state()
    return
