# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def lumber_in_shed(_obj=None):
        return CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "Shed" and _room_has_item_by_id(CurrentRoom, "lumber_001")

    def lumber_ready_for_chop(_obj=None):
        return lumber_in_shed(_obj) and player_has_equipped_weapon("old_axe_001")

    LumberItem = GameItem(
        object_id="lumber_001",
        name="бревно",
        description="Тяжелое бревно, которое можно принести из леса и сложить в сарае.",
        actions=[
            ObjectAction(
                action_id="chop_lumber",
                label="Колоть бревно",
                hook="call",
                target="Chop",
                args=("lumber_001", "Shed", "", "lumber_001"),
                condition=lumber_ready_for_chop,
            ),
        ],
        price=0,
        carriable=True,
        stackable=True,
        state={
            "visible": 1,
            "curLoc": "Shed",
        },
        custom_properties={
            "item_kind": "resource",
            "resource_kind": "lumber",
            "curLoc": "Shed",
        },
    )
