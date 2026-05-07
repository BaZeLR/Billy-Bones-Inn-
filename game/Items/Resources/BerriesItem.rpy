# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    BerriesItem = GameItem(
        object_id="berries_001",
        name="ягоды",
        description="На лесных кустах можно насобирать горсть спелых ягод.",
        actions=[
            ObjectAction(
                action_id="eat",
                label="Съесть ягоды",
                hook="call",
                target="UseFoodItem",
                args=("berries_001",),
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
            "consume_action": "eat",
            "consume_minutes": 10,
            "consume_energy": 5,
            "consume_fun": 3,
            "consume_text": "Вы съедаете горсть ягод. Сладкая лесная кислинка слегка бодрит вас и поднимает настроение.",
            "gift_value": 1,
            "social_fun_bonus": 1,
            "curLoc": "Forest",
        },
    )
