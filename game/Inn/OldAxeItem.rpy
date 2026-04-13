init 4 python:
    OldAxeItem = GameItem(
        object_id="old_axe_001",
        name="старый топор",
        description="Старый, но еще годный топор для рубки и колки дров.",
        actions=[
            ObjectAction(
                action_id="examine_old_axe",
                label="Осмотреть топор",
                hook="call",
                target="Examine",
                args=("old_axe_001", "Shed", "Лезвие затупилось, древко потрескалось, но для колки дров этот топор еще годится."),
            ),
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
            "curLoc": "Shed",
        },
    )
