# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy

    def scene_panel_item(caption="", mode="call", target="", args=None, mutations=None, minutes=0, text="", picture="", title="", next_items=None, return_room=True):
        return MenuItem(
            str(caption or ""),
            Call(
                "SceneActionPanelApply",
                str(mode or "call"),
                str(target or ""),
                tuple(args or ()),
                list(mutations or []),
                int(minutes or 0),
                str(text or ""),
                str(picture or ""),
                str(title or ""),
                list(next_items or []),
                bool(return_room),
            ),
        )

    def scene_panel_return_item(caption="Вернуться к текущему месту"):
        return scene_panel_item(caption, mode="return", return_room=True)

    def scene_panel_jump_item(caption="", target="", minutes=0, mutations=None):
        return scene_panel_item(caption, mode="jump", target=target, minutes=minutes, mutations=mutations)

    def scene_panel_call_item(caption="", target="", args=None, minutes=0, mutations=None, text="", picture="", title="", next_items=None, return_room=True):
        return scene_panel_item(caption, mode="call", target=target, args=args, minutes=minutes, mutations=mutations, text=text, picture=picture, title=title, next_items=next_items, return_room=return_room)

    def scene_panel_set_item(caption="", variable="", value=0, text="", title="", next_items=None):
        return scene_panel_item(caption, mode="panel", mutations=[{"name": variable, "op": "set", "value": value}], text=text, title=title, next_items=next_items)

    def scene_panel_add_item(caption="", variable="", value=0, text="", title="", next_items=None, low=None, high=None):
        mutation = {"name": variable, "op": "add", "value": value}
        if low is not None:
            mutation["min"] = low
        if high is not None:
            mutation["max"] = high
        return scene_panel_item(caption, mode="panel", mutations=[mutation], text=text, title=title, next_items=next_items)

    def scene_panel_mutate(mutation):
        if not isinstance(mutation, dict):
            return
        name = str(mutation.get("name", "") or "").strip()
        if name == "":
            return
        op = str(mutation.get("op", "set") or "set").strip().lower()
        value = mutation.get("value", 0)
        low = mutation.get("min", None)
        high = mutation.get("max", None)

        try:
            current = getattr(renpy.store, name)
        except Exception:
            current = 0

        if op == "add":
            try:
                next_value = int(current or 0) + int(value or 0)
            except Exception:
                next_value = value
        elif op == "sub":
            try:
                next_value = int(current or 0) - int(value or 0)
            except Exception:
                next_value = value
        else:
            next_value = value

        if low is not None or high is not None:
            try:
                next_value = int(next_value or 0)
                if low is not None:
                    next_value = max(int(low or 0), next_value)
                if high is not None:
                    next_value = min(int(high or 0), next_value)
            except Exception:
                pass

        setattr(renpy.store, name, next_value)


label SceneActionPanel(picture="", text="", title="Ваши действия", items=None, ui_mode="event", content_screen=""):
    if str(picture or "").strip():
        vscene picture
    $ MainTxt = str(text or "")
    $ CurLocDesc = MainTxt
    $ _scene_content_screen = str(content_screen or "").strip() or None
    $ main_ui_set_action_panel(str(title or "Ваши действия"), list(items or []), _scene_content_screen, str(ui_mode or "event"), restart=False)
    call ReturnToMainUI
    return


label SceneActionPanelApply(mode="call", target="", args=(), mutations=None, minutes=0, text="", picture="", title="", next_items=None, return_room=True):
    $ _scene_mode = str(mode or "call").strip().lower()
    $ _scene_target = str(target or "").strip()
    $ _scene_args = tuple(args or ())
    $ _scene_mutations = list(mutations or [])
    $ _scene_minutes = int(minutes or 0)

    python:
        for _scene_mutation in _scene_mutations:
            scene_panel_mutate(_scene_mutation)

    if _scene_minutes > 0:
        $ calendar_v2.advance_minutes(_scene_minutes)

    if str(picture or "").strip():
        vscene picture

    if str(text or "").strip():
        $ MainTxt = str(text or "")
        $ CurLocDesc = MainTxt

    call stat

    if _scene_mode == "jump" and _scene_target:
        jump expression _scene_target

    if _scene_mode == "location" and _scene_target:
        jump expression _scene_target

    if _scene_mode == "call" and _scene_target:
        if len(_scene_args) <= 0:
            call expression _scene_target
        elif len(_scene_args) == 1:
            call expression _scene_target pass (_scene_args[0],)
        elif len(_scene_args) == 2:
            call expression _scene_target pass (_scene_args[0], _scene_args[1])
        elif len(_scene_args) == 3:
            call expression _scene_target pass (_scene_args[0], _scene_args[1], _scene_args[2])
        else:
            call expression _scene_target pass (_scene_args[0], _scene_args[1], _scene_args[2], _scene_args[3])

    if len(list(next_items or [])) > 0:
        $ main_ui_set_action_panel(str(title or "Ваши действия"), list(next_items or []), None, "event", restart=False)
        call ReturnToMainUI
        return

    if _scene_mode == "panel":
        $ main_ui_set_action_panel(str(title or "Ваши действия"), [], None, "event", restart=False)
        call ReturnToMainUI
        return

    if _scene_mode in ("return", "current", "room"):
        $ main_ui_restore_room_scene_state()
        call ReturnToMainUI
        return

    if bool(return_room):
        $ main_ui_restore_room_scene_state()
        call ReturnToMainUI
        return

    return
