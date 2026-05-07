# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 5 python:
    def tavern_my_room_chest_can_open(obj=None):
        chest_obj = obj
        if chest_obj is None:
            return False
        return int(chest_obj.state.get("open", 0) or 0) == 0 and int(chest_obj.state.get("locked", 0) or 0) == 0

    def tavern_my_room_chest_can_close(obj=None):
        chest_obj = obj
        if chest_obj is None:
            return False
        return int(chest_obj.state.get("open", 0) or 0) == 1

    TavernMyRoomChestObject = GameObject(
        object_id="chest_001",
        name="Ларь",
        description="Старый ларь, в котором хранится ваша одежда.",
        container=True,
        state={"open": 0, "visible": 1, "locked": 0},
        actions=[
            ObjectAction(
                action_id="open_chest",
                label="Открыть ларь",
                hook="call",
                target="TavernMyRoomOpenChest",
                condition=tavern_my_room_chest_can_open,
            ),
            ObjectAction(
                action_id="close_chest",
                label="Закрыть ларь",
                hook="call",
                target="TavernMyRoomCloseChest",
                condition=tavern_my_room_chest_can_close,
            ),
            ObjectAction(
                action_id="examine_chest",
                label="Осмотреть ларь",
                hook="text",
                target="Старый деревянный ларь с вашей одеждой.",
            ),
        ],
        carriable=False,
        stackable=False,
    )
