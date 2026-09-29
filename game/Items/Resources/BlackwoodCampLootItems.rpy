init 4 python:
    BlackwoodSmoothPlugItem = GameItem(
        object_id="blackwood_smooth_plug_001",
        name="полированная пробка",
        description="Гладкая игрушка для взрослых из тёмного дерева, найденная в сундуке покинутого лагеря Робина.",
        carriable=True,
        stackable=False,
        custom_properties={"item_kind": "curio", "source_thread": "robinCampLoot"},
    )

    BlackwoodCarvedToyItem = GameItem(
        object_id="blackwood_carved_toy_001",
        name="резная игрушка для взрослых",
        description="Аккуратно вырезанная и отполированная вещица из лагерной добычи Робина.",
        carriable=True,
        stackable=False,
        custom_properties={"item_kind": "curio", "source_thread": "robinCampLoot"},
    )

    BlackwoodPigmentsItem = GameItem(
        object_id="blackwood_pigments_001",
        name="коробка ярких красок",
        description="Небольшая коробка с редкими цветными пигментами и кистями, оставленная в разбойничьем лагере.",
        carriable=True,
        stackable=False,
        custom_properties={"item_kind": "art_supplies", "source_thread": "robinCampLoot"},
    )

    BlackwoodLingerieItem = GameItem(
        object_id="blackwood_lingerie_001",
        name="тонкое кружевное бельё",
        description="Дорогое бельё в бумажной обёртке, уцелевшее среди трофеев Робина.",
        carriable=True,
        stackable=False,
        custom_properties={"item_kind": "clothing_gift", "source_thread": "robinCampLoot"},
    )
