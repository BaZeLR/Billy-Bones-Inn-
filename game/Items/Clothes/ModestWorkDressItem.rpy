# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    ModestWorkDressItem = GameItem(
        object_id="dress_modestworkdress",
        name="Скромное рабочее платье",
        description="Это платье должна иметь каждая себя уважающая скромная и работящая девушка. Оно красиво и в тоже время целомудренно. Сшитое из прекрасной голубой ткани с оборочками, оно полностью закрывает все тело, включая руки. Никаких скабрезных элементов, типа декольте, в нем нет. В комплекте к нему идет белый передничек",
        price=200,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "modestworkdress",
            "wear_target": "female",
        },
    )
