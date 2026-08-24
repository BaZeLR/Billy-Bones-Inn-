# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -20 python:
    def bedroom_door_default_locked(room_code=""):
        room_key = str(room_code or "").strip()
        if room_key == "TavernSandraRoom":
            return not (int(Sandra.rel or 0) >= 10 or int(threads["sandraWeeklyEvaluation"].num or 0) > 0)
        return False

    def bedroom_door_locked(room_code="", default_locked=None):
        room_key = str(room_code or "").strip()
        if room_key == "":
            return bool(default_locked)
        room = rooms.get(room_key)
        if room is not None and "door_locked" in room.state:
            return bool(room.state.get("door_locked", False))
        if default_locked is not None:
            return bool(default_locked)
        return bedroom_door_default_locked(room_key)

    def set_bedroom_door_locked(room_code="", locked=False):
        room_key = str(room_code or "").strip()
        if room_key == "":
            return False
        room = rooms.get(room_key)
        if room is None:
            return False
        room.state["door_locked"] = bool(locked)
        return bool(room.state["door_locked"])

    def bedroom_door_status_text(room_code="", owner_name=""):
        room_key = str(room_code or "").strip()
        owner = str(owner_name or "этой комнаты").strip()
        if bedroom_door_locked(room_key):
            return "Дверь в комнату %s сейчас заперта. Пока ее не откроют изнутри или пока вы не заслужите доверия хозяйки, пройти сюда не выйдет." % owner
        return "Дверь в комнату %s сейчас не заперта. Обычная деревянная дверь, которую можно прикрыть изнутри на простую защелку." % owner

    def bedroom_door_object(object_id="", room_code="", owner_name=""):
        room_key = str(room_code or "").strip()
        owner = str(owner_name or "хозяйки").strip()
        object_key = str(object_id or "").strip()
        return GameObject(
            object_id=object_key,
            name="Дверь",
            description="Дверь в комнату %s." % owner,
            actions=[
                ObjectAction(
                    action_id="inspect_door",
                    label="Осмотреть дверь",
                    hook="call",
                    target="BedroomDoorInspect",
                    args=(room_key, owner, object_key),
                ),
            ],
            locked=False,
            custom_properties={"room_code": room_key, "owner_name": owner},
        )

    def bedroom_door_object_text(room_object=None):
        if room_object is None:
            return ""
        props = dict(getattr(room_object, "custom_properties", {}) or {})
        room_key = str(props.get("room_code", "") or "")
        owner = str(props.get("owner_name", "") or "")
        if room_key == "":
            return str(getattr(room_object, "description", "") or "")
        return bedroom_door_status_text(room_key, owner)


label BedroomDoorInspect(room_code="", owner_name="", object_id=""):
    $ scene_runtime.text = bedroom_door_status_text(room_code, owner_name)
    $ scene_runtime.location_text = scene_runtime.text
    if str(rooms.current_code or "") == "TavernAmandaRoom":
        call tavern_amanda_room_object_menu(object_id)
    elif str(rooms.current_code or "") == "TavernMelissaRoom":
        call TavernMelissaRoomObjectMenu(object_id)
    elif str(rooms.current_code or "") == "TavernSandraRoom":
        call TavernSandraRoomObjectMenu(object_id)
    return
