# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    SlutDressItem = GameItem(
        object_id="dress_slutdress",
        name="Короткое платьичко",
        description="Это платье было созданно для того, чтобы притягивать взоры мужчин. Короткая черная юбочка едва прикрывает попу, а черная же блузка с сетчатым вырезом еле-еле прикрывает груди. Более того, если под нее не одеть лифа, то будут видны ареолы. А если одеть - то лиф. Только очень уверенная в себе девушка, твердо знающая чего она хочет, выйдет на улицу в таком платье",
        price=300,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "slutdress",
            "wear_target": "female",
        },
    )
