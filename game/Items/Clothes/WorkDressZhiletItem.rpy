# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    WorkDressZhiletItem = GameItem(
        object_id="dress_workdresszhilet",
        name="Бежевое повседневное платье с жилеткой",
        description="Это платье подходит для повседневного ношения. Оно в меру скромно, в меру привлекательно. Бежевого цвета юбка полностью закрывает ноги, но белая блузка из тонкой ткани подчеркивает приятные округлости тела и оставляет руки открытыми. Поверх блузки одет бархатный бордовый жилет с большим круглым вырезом на груди",
        price=350,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "workdresszhilet",
            "wear_target": "female",
        },
    )
