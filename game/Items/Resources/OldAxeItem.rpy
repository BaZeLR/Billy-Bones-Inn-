# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    OldAxeItem = GameItem(
        object_id="old_axe_001",
        name="старый топор",
        description="Старый, но еще годный топор для рубки и колки дров.",
        actions=[
            ObjectAction(action_id="take_old_axe", label="Взять топор", hook="call", target="Take", args=("old_axe_001", "Shed", "Вы снимаете со стены старый топор и забираете его с собой.")),
        ],
        price=12,
        carriable=True,
        usable=True,
        weapon=True,
        state={
            "visible": 1,
            "curLoc": "Shed",
        },
        custom_properties={
            "item_kind": "tool",
            "tool_kind": "axe",
            "attack_points": 10,
            "speed_penalty": 1,
            "curLoc": "Shed",
        },
    )
