init 4 python:
    ClaraPantaloonsItem = GameItem(
        object_id="clara_pantaloons_001",
        name="панталоны Клариссы",
        description="Потерянные в винном подвале панталоны Клариссы. На внутренней стороне пояса углем нанесены приметы лесной тропы и знак старой водокачки.",
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
