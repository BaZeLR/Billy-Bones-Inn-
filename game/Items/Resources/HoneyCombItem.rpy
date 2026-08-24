# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    HoneyCombItem = GameItem(
        object_id="honey_comb_001",
        name="соты с медом",
        description="Небольшой кусок медовых сот, который можно найти в лесу, если повезет.",
        actions=[
            ObjectAction(
                action_id="eat_honey_comb",
                label="Съесть медовые соты",
                hook="call",
                target="UseHoneyCombItem",
            ),
        ],
        picture="images/forest/bee_hive.png",
        price=8,
        carriable=True,
        stackable=True,
        state={
            "visible": 1,
            "curLoc": "Forest",
        },
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "honey_comb",
            "gift_value": 1,
            "social_fun_bonus": 2,
            "social_openness_bonus": 1,
            "curLoc": "Forest",
        },
    )


label UseHoneyCombItem:
    if int(player.item_count("honey_comb_001") or 0) <= 0:
        $ MainTxt = "Медовых сот у вас при себе не осталось."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryMenu
        return

    $ player.remove_item("honey_comb_001", 1)
    $ energy = _player_clamp(int(energy or 0) + 7, 0, 100)
    $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ MainTxt = "Вы разламываете соты и с удовольствием жуете сладкий мед. Это быстро поднимает и силы, и настроение."
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("honey_comb_001", True)
    return
