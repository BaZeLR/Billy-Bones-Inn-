init python:
    class AlberData(PeopleData):
        code_name = "alber"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Альбер",
                fullname="Альбер Легаре",
                genitive="Альбера Легаре",
                dative="Альберу Легаре",
                default_location="",
                description="Мессир Альбер Легаре - хозяин винного погребка, женат, у него большая семья.",
                birth_date={"day": 1, "period": 1, "cycle": 1064},
            )
            self.portrait = "images/Alber/portrait1.png"
            self.schedule_source = "schedules/alber.json"

    class AlberInfo(BaseNPC):
        """Alber Legare: wine merchant, Amanda/Liza fallout, Friday dance hooks."""
        talk_label = "IntAlberTalk"
        unknown_name = "Альбер"
        whore_visit_frequency = 3

        def __init__(self, name="alber", **kwargs):
            super().__init__(name, **kwargs)
            self.data = AlberStaticData
            self.known = False
            self.rel = people_to_int(kwargs.get("rel", 0), 0)
            self.talked_today = 0
            self.liza_encounter_seen = False
            self.talked_about_liza = False
            self.heard_about_wife = False
            self.amanda_conflict_stage = 0

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = AlberStaticData
            return self

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() == "WineStore":
                return str(self.getLocation() or "") == "WineStore" and bool(people.can_talk(self.name))
            return super(AlberInfo, self).interaction_visible(room_code)

    def alber_random_portrait():
        candidates = [
            "images/Alber/portrait1.png",
            "images/Alber/portrat2.png",
            "images/Alber/portrait3.png",
            "images/Alber/portrait4.png",
            "images/Alber/portrait5.jpg",
            "images/Alber/portrait6.jpg",
            "images/Alber/portrait7.jpg",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return loadable[procedural_randint(0, len(loadable) - 1, "alber_portrait_%s" % int(current_game_day() or 0))] if len(loadable) > 0 else ""

    def alber_tavern_visit_ready():
        return (
            Amanda.legare_affection >= 5
            and not Amanda.legare_forbidden
            and int(calendar_v2.week or 0) != 5
        )

define AlberStaticData = AlberData()
default Alber = AlberInfo()

label register_alber_secondary:
    python:
        people.register(AlberStaticData, Alber)
    return
