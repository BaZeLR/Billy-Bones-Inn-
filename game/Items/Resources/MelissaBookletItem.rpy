init 4 python:
    def melissa_drawings_booklet_visible():
        return (
            str(CurLoc or "") == "TavernMelissaRoom"
            and int(Melissa.var.get("drawings_found", 0) or 0) > 0
            and int(player.item_count("melissa_drawings_booklet_001") or 0) <= 0
        )

    MelissaBookletItem = GameItem(
        object_id="melissa_drawings_booklet_001",
        name="пачка непристойных рисунков",
        description="Спрятанная пачка смелых рисунков из комнаты Мелиссы. Бумага потерта на сгибах, будто ее не раз перелистывали в одиночестве.",
        condition=melissa_drawings_booklet_visible,
        actions=[
            ObjectAction(
                action_id="take_melissa_booklet",
                label="Взять буклет",
                hook="call",
                target="MelissaBookletTake",
            ),
            ObjectAction(
                action_id="open_melissa_booklet",
                label="Открыть буклет",
                hook="call",
                target="MelissaBookletOpenPreview",
            ),
            ObjectAction(
                action_id="read_melissa_booklet",
                label="Прочитать буклет",
                hook="call",
                target="ReadMelissaBooklet",
                args=(False,),
            ),
            ObjectAction(
                action_id="leave_melissa_booklet",
                label="Оставить его там, где лежал",
                hook="call",
                target="MelissaBookletLeaveThere",
            ),
            ObjectAction(
                action_id="continue_melissa_booklet_search",
                label="Продолжить поиски",
                hook="call",
                target="MelissaBookletContinueSearch",
            ),
        ],
        picture="images/melissa/bedRoomSearch/underBedBooklet.png",
        carriable=True,
        readable=True,
        stackable=False,
        custom_properties={
            "item_kind": "book",
            "category": "personal",
            "owner": "melissa",
            "source_thread": "melissaBatProblem",
        },
    )
