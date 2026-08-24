init python:
    class EddieData(PeopleData):
        code_name = "eddie"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Эдди",
                fullname="Эдди",
                genitive="Эдди",
                dative="Эдди",
                default_location="",
                description="Эдди - сын Ребекки, подросток и помощник в бакалейной лавке. Связан с событиями Бекки, Жоржетты и Лукаса.",
                birth_date={"day": 1, "period": 1, "cycle": 1083},
                portrait="images/eddie/portraits/portrait_0.png",
            )
            self.schedule_source = "schedules/eddie.json"

    class EddieInfo(BaseNPC):
        """Eddie: Becky's son, group scenes, Georgett crossover."""
        talk_label = "IntEddieTalk"
        unknown_name = "Незнакомец"
        whore_visit_frequency = 6

        def __init__(self, name="eddie", **kwargs):
            super().__init__(name, **kwargs)
            self.data = EddieStaticData
            self.known = False
            self.told_about_tavern_whores = False
            self.seen_with_georgett = False
            self.talked_about_georgett = False
            self.saw_mother_sex = False
            self.fingal_talk_stage = 0
            self.asked_fingal_destination = False
            self.asked_fingal_guard_complaint = False
            self.ridiculed_follow_attempt = False
            self.others_saw_with_mother = False

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = EddieStaticData
            return self

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() == "BeckyHome":
                return rooms.get("BeckyHomeFront").state["arrival_mode"] in ("SvalnyiGreh", "")
            return super(EddieInfo, self).interaction_visible(room_code)

        def action_data(self, where_id=""):
            data = super(EddieInfo, self).action_data(where_id)
            if str(where_id or "").strip() == "GroceryStore":
                if not self.known:
                    data["title"] = "Торговец"
                data["picture_path"] = grocery_store_grocer_picture(self.name)
                data["talk_picture"] = data["picture_path"]
            return data

define EddieStaticData = EddieData()
default Eddie = EddieInfo()

label register_eddie_secondary:
    python:
        people.register(EddieStaticData, Eddie)
    return
