# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    DressShopFemaleSamplesObject = GameObject(
        object_id="female_samples_001",
        name="Женские образцы",
        description="Женские платья и прочие образцы одежды висят вдоль левой стены.",
        container=True,
        carriable=False,
        stackable=False,
        custom_properties={"rack_type": "female"},
    )
