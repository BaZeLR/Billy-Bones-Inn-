init python:
    class NostarData(PeopleData):
        code_name = "nostar"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Леди Ностар Линк",
                fullname="Леди Ностар Линк",
                genitive="леди Ностар Линк",
                dative="леди Ностар Линк",
                default_location="NostarHouse",
                description="Леди Ностар Линк — богатая, остроумная и своенравная жительница квартала знати. Пропажа её шиншиллы Розарио не даёт ей покоя.",
                portrait="images/nostar/lady_nostar.png",
                schedule_entries=[
                    NPCScheduleEntry(
                        location="NostarHouse",
                        weekdays=[1, 2, 3, 4, 5, 6, 7],
                        start_hour=9,
                        end_hour=21,
                        label="receiving_visitors",
                    ),
                ],
            )

    class NostarInfo(BaseNPC):
        talk_label = "IntNostarTalk"
        unknown_name = "Знатная дама"

        def __init__(self, name="nostar", **kwargs):
            super().__init__(name, **kwargs)
            self.data = NostarStaticData
            self.known = False

        def update(self):
            super(NostarInfo, self).update()
            self.data = NostarStaticData
            return self


define NostarStaticData = NostarData()
default Nostar = NostarInfo()


label register_nostar_secondary:
    $ people.register(NostarStaticData, Nostar)
    return
