init python:
    def build_room_action_items(room):
        items = []

        if room is None:
            return items

        object_menu_label = str(room.custom_properties.get("object_menu_label", "") or "")
        if object_menu_label:
            for obj in room.visible_objects():
                items.append(MenuItem(
                    obj.name,
                    [
                        SetVariable("current_action_title", obj.name),
                        SetVariable("current_object_id", obj.object_id),
                        Call(object_menu_label, obj.object_id),
                    ]
                ))

        for exit_obj in room.visible_exits():
            items.append(MenuItem(
                exit_obj.label,
                Call("AdvanceMovementTime", exit_obj.target)
            ))
        return items
