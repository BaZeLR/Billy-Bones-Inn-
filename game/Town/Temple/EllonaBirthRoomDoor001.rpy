# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def ellona_birth_room_door_open(obj=None):
        door_obj = obj
        if door_obj is None:
            return False
        return int(door_obj.state.get("locked", 0) or 0) == 0 and Francheska.birth_room_available()

    EllonaBirthRoomDoorObject = GameObject(
        object_id="birth_room_door_001",
        name="Дверь в родильную",
        description="Дверь в помещение, где принимают роды.",
        portal=True,
        state={"locked": 0, "visible": 1},
        actions=[
            ObjectAction(
                action_id="enter_birth_room",
                label="Зайти в помещение для родов",
                hook="jump",
                target="EllonaBirthRoom",
                condition=ellona_birth_room_door_open,
            ),
            ObjectAction(
                action_id="examine_birth_room_door",
                label="Осмотреть дверь",
                hook="text",
                target="За дверью находится помещение для родов, где Франческа помогает роженицам.",
            ),
        ],
        carriable=False,
        stackable=False,
    )
