# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_kitchen_cauldron_description():
        if _pc_hot_water_is_ready(TavernKitchenCauldronObject):
            return "В котле есть горячая вода. Ее должно хватить до следующего дня."
        return "Большой котел для кипячения воды. Сейчас в нем нет горячей воды."

    TavernKitchenCauldronObject = GameObject(
        object_id="cauldron_001",
        name="Котел",
        description="Большой котел для кипячения воды.",
        picture="images/tavern/kitchen/kitchen_stove.png",
        container=False,
        actions=[
            ObjectAction(
                action_id="boil_water",
                label="Вскипятить воду",
                hook="call",
                target="BoilWater",
                args=("cauldron_001", "TavernKitchen", "", "cauldron_001"),
            ),
        ],
        state={"hot_water_until_minute": 0, "hot_water_units": 0},
        carriable=False,
        stackable=False,
    )
