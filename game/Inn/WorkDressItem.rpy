init 4 python:
    WorkDressItem = GameItem(
        object_id="dress_workdress",
        name="Бежевое повседневное платье",
        description="Это платье подходит для повседневного ношения. Оно в меру скромно, в меру привлекательно. Бежевого цвета юбка полностью закрывает ноги, но белая блузка из тонкой ткани подчеркивает приятные округлости тела и оставляет руки открытыми. Впрочем вырез у блузки неглубок",
        price=300,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "workdress",
            "wear_target": "female",
        },
    )
