init 4 python:
    ClaraPantaloonsItem = GameItem(
        object_id="clara_pantaloons_001",
        name="панталоны Клариссы",
        description="Панталоны Клариссы, найденные между бочками в подвале винного погребка после ее сцены с Легаре. Они сохранили ее запах и могут помочь псу взять след.",
        carriable=True,
        stackable=False,
        custom_properties={
            "item_kind": "quest_clue",
            "owner": "clara",
            "source_thread": "claraPaintingsPath",
        },
    )

    ShovelItem = GameItem(
        object_id="shovel_001",
        name="походная лопата",
        description="Короткая крепкая лопата. Не слишком удобна для большого хозяйства, зато ее легко взять с собой в лес.",
        price=24,
        carriable=True,
        stackable=False,
        custom_properties={
            "item_kind": "tool",
            "tool_kind": "shovel",
        },
    )
