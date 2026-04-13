init 4 python:
    MushroomItem = GameItem(
        object_id="mushroom_001",
        name="грибы",
        description="Среди мха и сырой листвы можно набрать съедобных лесных грибов.",
        actions=[
            ObjectAction(
                action_id="eat_mushroom",
                label="Съесть грибы",
                hook="call",
                target="UseMushroomItem",
            ),
        ],
        price=3,
        carriable=True,
        stackable=True,
        state={
            "visible": 1,
            "curLoc": "Forest",
        },
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "mushroom",
            "gift_value": 1,
            "social_fun_bonus": 1,
            "curLoc": "Forest",
        },
    )


label UseMushroomItem:
    if int(_player_item_count_by_id("mushroom_001") or 0) <= 0:
        $ MainTxt = "Грибов у вас при себе не осталось."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryMenu
        return

    $ _player_remove_item_by_id("mushroom_001", 1)
    $ energy = _player_clamp(int(energy or 0) + 6, 0, 100)
    $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
    $ MainTxt = "Вы быстро прожариваете на углях пару грибов и съедаете их. Это не пир, но силы заметно прибавляются."
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("mushroom_001", True)
    return
