init 4 python:
    NobleCostumeItem = GameItem(
        object_id="dress_nobbledress",
        name="Костюм дворянина",
        description="Костюм дворянина состоит из очень узких облегающих штанов, снабженных гульфиком, призванным подчеркнуть выдающуюся мужскую стать его обладателя. Штаны поддерживаются богато расшитым золотом широким поясом с серебрянной пряжкой. Сверху благородные носят бархатный дублет с золотой отторочкой поверх рубашки из лучшего шелка. Это лучший и очень дорогой костюм",
        price=5000,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "nobbledress",
            "wear_target": "player",
        },
    )
