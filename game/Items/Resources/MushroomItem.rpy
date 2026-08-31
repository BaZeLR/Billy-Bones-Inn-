# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    MushroomItem = GameItem(
        object_id="mushroom_001",
        name="грибы",
        description="Среди мха и сырой листвы можно набрать съедобных лесных грибов.",
        actions=[
            ObjectAction(
                action_id="eat",
                label="Съесть грибы",
                hook="call",
                target="UseFoodItem",
                args=("mushroom_001",),
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
            "kitchen_depositable": True,
            "consume_action": "eat",
            "consume_minutes": 15,
            "consume_energy": 6,
            "consume_fun": 1,
            "consume_text": "Вы быстро прожариваете на углях пару грибов и съедаете их. Это не пир, но силы заметно прибавляются.",
            "gift_value": 1,
            "social_fun_bonus": 1,
            "curLoc": "Forest",
        },
    )
