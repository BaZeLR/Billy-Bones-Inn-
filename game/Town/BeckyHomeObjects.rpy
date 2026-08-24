# ================================================================================
# Becky home room objects.
# GameObject definitions own object text and object actions.
# rooms.get("BeckyHome") / rooms.get("BeckyHomeFront") only list these object ids.
# ================================================================================

init python:
    BeckyHomeBedObject = GameObject(
        object_id="becky_home_bed",
        name="Большая кровать",
        description="Широкая кровать, занимающая центр комнаты Бекки.",
        picture="images/becky/sex/inroom1.jpg",
        actions=[
            ObjectAction(
                action_id="examine_bed",
                label="Осмотреть кровать",
                hook="text",
                target="Большая кровать, занимающая центр спальни Бекки.",
            ),
        ],
        carriable=False,
        stackable=False,
    )

    BeckyHomeChestsObject = GameObject(
        object_id="becky_home_chests",
        name="Сундуки вдоль стен",
        description="Вдоль стен стоят массивные сундуки, скамья и пара стульев.",
        picture="images/becky/Home/house1.jpg",
        actions=[
            ObjectAction(
                action_id="examine_chests",
                label="Осмотреть сундуки",
                hook="text",
                target="Массивные сундуки и мебель делают обстановку спальни простой, но добротной.",
            ),
        ],
        carriable=False,
        stackable=False,
    )

    BeckyHomeDinnerTableObject = GameObject(
        object_id="becky_home_dinner_table",
        name="Накрытый стол",
        description="Если Бекки принимает вас как гостя, стол у нее накрыт на совесть.",
        picture="images/becky/dinner/DinnerStart.jpg",
        actions=[
            ObjectAction(
                action_id="examine_table",
                label="Осмотреть стол",
                hook="text",
                target="Для обычного домашнего ужина здесь все устроено удивительно щедро.",
                condition=becky_home_table_visible,
            ),
        ],
        carriable=False,
        stackable=False,
    )

