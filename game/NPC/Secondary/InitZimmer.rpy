init python:
    class ZimmerData(PeopleData):
        code_name = "zimmer"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Десятник Циммерман",
                fullname="Десятник Циммерман",
                genitive="Десятника Циммермана",
                dative="Десятнику Циммерману",
                default_location="",
                description="Десятник Циммерман - старый начальник городской стражи, осторожный, носатый, кучерявый и всегда готовый объяснить, почему дело сложнее, чем кажется.",
                birth_date={"day": 1, "period": 1, "cycle": 1042},
                portrait="images/zimmer/portrait1.png",
                schedule_entries=[
                    NPCScheduleEntry(
                        location="CityGuard",
                        weekdays=[2],
                        start_hour=11,
                        end_hour=13,
                        label="tuesday_reception",
                    ),
                    NPCScheduleEntry(
                        location="CityGuard",
                        weekdays=[5],
                        start_hour=6,
                        end_hour=8,
                        label="friday_reception",
                    ),
                ],
            )

    class ZimmerInfo(BaseNPC):
        """Zimmer: city guard captain, Robin investigation, Blackwood mission."""
        talk_label = "IntZimmerTalk"
        unknown_name = "Десятник Циммерман"

        def __init__(self, name="zimmer", **kwargs):
            super().__init__(name, **kwargs)
            self.data = ZimmerStaticData
            self.known = False
            self.horse_complaint_stage = 0
            self.sherwood_story_stage = 0
            self.robin_complaint_stage = 0
            self.robin_investigation_day = 0
            self.street_patrol_pass = False

        def update(self):
            super(ZimmerInfo, self).update()
            self.data = ZimmerStaticData
            return self

define ZimmerStaticData = ZimmerData()
default Zimmer = ZimmerInfo()

label register_zimmer_secondary:
    python:
        people.register(ZimmerStaticData, Zimmer)
    return
