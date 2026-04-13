init 4 python:
    BerriesItem = GameItem(
        object_id="berries_001",
        name="ягоды",
        description="На лесных кустах можно насобирать горсть спелых ягод.",
        actions=[
            ObjectAction(
                action_id="eat_berries",
                label="Съесть ягоды",
                hook="call",
                target="UseBerriesItem",
            ),
        ],
        price=2,
        carriable=True,
        stackable=True,
        state={
            "visible": 1,
            "curLoc": "Forest",
        },
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "berries",
            "gift_value": 1,
            "social_fun_bonus": 1,
            "curLoc": "Forest",
        },
    )


label UseBerriesItem:
    if int(_player_item_count_by_id("berries_001") or 0) <= 0:
        $ MainTxt = "Ягод у вас при себе не осталось."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryMenu
        return

    $ _player_remove_item_by_id("berries_001", 1)
    $ energy = _player_clamp(int(energy or 0) + 5, 0, 100)
    $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ MainTxt = "Вы съедаете горсть ягод. Сладкая лесная кислинка слегка бодрит вас и поднимает настроение."
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("berries_001", True)
    return
