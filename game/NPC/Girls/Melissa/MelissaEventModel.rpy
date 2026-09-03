# Melissa-specific story event records.

init -24 python:
    class MelissaAmandaRoomShareEvent(Event):
        def __init__(self):
            super(MelissaAmandaRoomShareEvent, self).__init__(
                (
                    "story_melissa_amanda_room_locked",
                    None,
                    None,
                    None,
                    1,
                    None,
                    None,
                    None,
                    "TavernAmandaRoom",
                    "melissa_amanda_locked",
                    0,
                ),
                "",
                False,
            )
            self.code_name = "amanda_room_share"
            self.repeatable = True
            self.source_refs = ["TavernAmandaRoom.txt"]

        def checkConditions(self):
            return (
                str(Melissa.temp_room_code or "") == "TavernAmandaRoom"
                and not people.is_awake("amanda")
                and not bool(Melissa.drawings_found)
                and int(threads["melissaBatProblem"].num or 0) >= 6
                and int(threads["melissaBatProblem"].num or 0) < 8
            )


    MelissaAmandaRoomShare = MelissaAmandaRoomShareEvent()
