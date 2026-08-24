# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def room_action_menu_item(room_action):
        if room_action is None:
            return None

        caption = str(getattr(room_action, "label", "") or "").strip()
        if caption == "":
            return None

        hook = str(getattr(room_action, "hook", "jump") or "jump").strip()
        target = str(getattr(room_action, "target", "") or "").strip()
        action_args = tuple(getattr(room_action, "args", ()) or ())

        if hook in ("ui_call", "context_call") and target != "":
            return MenuItem(caption, Call(target, *action_args))
        if hook == "call" and target != "":
            return MenuItem(caption, Call(target, *action_args))
        if hook == "jump" and target != "":
            return MenuItem(caption, Jump(target))
        if hook == "movement" and target != "":
            return MenuItem(caption, movement_actions(target))
        if hook == "text":
            return MenuItem(caption, [
                SetField(scene_runtime, "text", target),
                SetField(scene_runtime, "location_text", target),
                Function(main_ui_restart_interaction),
            ])

        return None

    def build_room_action_items(room):
        items = []

        if room is None:
            return items

        room_object_menu_label = str(room.custom_properties.get("object_menu_label", "") or "")
        for obj in room.visible_objects():
            object_props = getattr(obj, "custom_properties", {}) or {}
            object_menu_label = str(object_props.get("object_menu_label", "") or room_object_menu_label)
            if not object_menu_label:
                continue
            items.append(MenuItem(
                obj.name,
                [
                    SetField(main_ui_runtime, "action_title", obj.name),
                    SetField(main_ui_runtime, "object_id", obj.object_id),
                    Call(object_menu_label, obj.object_id),
                ]
            ))

        for room_action in room.visible_actions():
            menu_item = room_action_menu_item(room_action)
            if menu_item is not None:
                items.append(menu_item)

        for exit_obj in room.visible_exits():
            items.append(MenuItem(
                exit_obj.label,
                movement_actions(exit_obj.target, getattr(exit_obj, "minutes_to_pass", 5))
            ))
        return items
