init 4 python:
    def chopped_wood_in_shed(_obj=None):
        return CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "Shed" and _room_has_item_by_id(CurrentRoom, "chopped_wood_001")

    ChoppedWoodItem = GameItem(
        object_id="chopped_wood_001",
        name="колотые дрова",
        description="Охапка колотых дров для растопки и кипячения воды.",
        actions=[
            ObjectAction(
                action_id="examine_chopped_wood",
                label="Осмотреть дрова",
                hook="call",
                target="Examine",
                args=("chopped_wood_001", "Shed", "Колотые дрова для печи и камина.", "chopped_wood_001"),
            ),
            ObjectAction(
                action_id="take_chopped_wood",
                label="Взять дрова",
                hook="call",
                target="Take",
                args=("chopped_wood_001", "Shed", "", "chopped_wood_001"),
                condition=chopped_wood_in_shed,
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
            "resource_kind": "chopped_wood",
            "curLoc": "Shed",
            "units_per_lumber": 10,
        },
    )