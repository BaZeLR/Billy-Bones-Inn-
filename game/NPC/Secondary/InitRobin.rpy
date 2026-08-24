init python:
    class RobinData(PeopleData):
        code_name = "robin"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Робин",
                fullname="Робин Гуд",
                genitive="Робина Гуда",
                dative="Робину Гуду",
                default_location="BlackwoodRoad",
                description="Робин Гуд - предводитель обездоленных лесорубов на Блэквудской вырубке.",
                birth_date={"day": 1, "period": 1, "cycle": 1070},
                portrait="images/Robin/portrait1.jpg",
            )

    class RobinInfo(BaseNPC):
        """Robin: Blackwood leader, Mongol safe pass, Zimmer mission."""
        talk_label = "IntRobinTalk"
        code_name = "robin"
        unknown_name = "Робин"

        def __init__(self, name="robin", **kwargs):
            super().__init__(name, **kwargs)
            self.identity_known = False
            self.complaint_explained = False
            self.place_explained = False
            self.weapon_source_explained = False
            self.robbery_count = 0
            self.negotiation_stage = 0
            self.knows_big_tits_village = False
            self.mongol_safe_pass = False
            self.kunidell_opened = False
            self.kunidell_deliveries = 0
            self.blackwood_road_open = False

        def update(self):
            self.name = self.code_name
            self.data = RobinStaticData
            return self

define RobinStaticData = RobinData()
default Robin = RobinInfo()

label register_robin_secondary:
    python:
        people.register(RobinStaticData, Robin)
    return
