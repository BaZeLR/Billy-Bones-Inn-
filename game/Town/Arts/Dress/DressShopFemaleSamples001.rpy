# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    DressShopFemaleSamplesObject = GameObject(
        object_id="female_samples_001",
        name="Женские образцы",
        description="Женские платья и прочие образцы одежды висят вдоль левой стены.",
        picture="images/irma/portraits/portrait3.png",
        actions=[
            ObjectAction(
                action_id="open_female_catalog",
                label="Посмотреть женские платья",
                hook="call",
                target="DressShopOpenCatalog",
                args=("female",),
            ),
        ],
        container=True,
        carriable=False,
        stackable=False,
    )
