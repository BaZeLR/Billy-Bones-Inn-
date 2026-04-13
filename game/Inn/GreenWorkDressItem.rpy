init 4 python:
    GreenWorkDressItem = GameItem(
        object_id="dress_greenworkdress",
        name="Зелено-голубое повседневное платье",
        description="Это платье подходит для повседневного ношения. Оно в меру скромно, в меру привлекательно. Голубого цвета юбка полностью закрывает ноги, но зеленая блузка из тонкой ткани подчеркивает приятные округлости тела и оставляет руки открытыми. Впрочем вырез у блузки неглубок",
        price=300,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "greenworkdress",
            "wear_target": "female",
        },
    )
