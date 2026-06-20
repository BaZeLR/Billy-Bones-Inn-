init python:
    def alber_story_defaults():
        return {
            "sawwithliza": 0,
            "talkedaboutliza": 0,
            "WhoreVisitFreq": 3,
            "hearabouthiswife": 0,
            "FightYouAmanda": 0,
            "clara_paintings_enemy": 0,
            "LegareProvokeYou": 0,
        }

    class AlberData(PeopleData):
        code_name = "alber"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Альбер",
                fullname="Альбер Легаре",
                genitive="Альбера Легаре",
                dative="Альберу Легаре",
                default_location="WineStore",
                description="Мессир Альбер Легаре - хозяин винного погребка, женат, у него большая семья.",
                age=36,
            )
            self.portrait = "images/Alber/portrait1.png"

    class AlberInfo(BaseNPC):
        """Alber Legare: wine merchant, Amanda/Liza fallout, Friday dance hooks."""
        unknown_name = "Альбер"
        uses_own_var_state = True

        def __init__(self, name="alber", **kwargs):
            super().__init__(name, **kwargs)
            self.data = AlberStaticData
            self.age = 36
            self.known = False
            self.location = "WineStore"
            self.rel = people_to_int(kwargs.get("rel", 0), 0)
            self.relationship = self.rel
            self.talked_today = 0
            self.var = dict(kwargs.get("var", {}) or {})
            self.ensure_story_defaults()

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = AlberStaticData
            self.location = "WineStore"
            self.ensure_story_defaults()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for k, v in alber_story_defaults().items():
                self.var.setdefault(k, v)
            self.promote_from_var(self.var)
            return self.var

        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            self.promote_from_var(self.var)
            return value

        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value

        def add_relation(self, amount=1, cap=20):
            self.rel = max(0, min(people_to_int(cap, 20), people_to_int(self.rel, 0) + people_to_int(amount, 0)))
            self.relationship = self.rel
            return self.rel

        def finish_talk(self):
            self.talked_today = people_to_int(self.talked_today, 0) + 1
            return self.talked_today

        def talk_count(self):
            return people_to_int(self.talked_today, 0)

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
        return loadable[procedural_randint(0, len(loadable) - 1, "alber_portrait_%s" % int(dayspassed or 0))] if len(loadable) > 0 else ""

    def alber_tavern_visit_ready():
        return (
            Amanda.var_int("alberfriends", 0) >= 5
            and Amanda.var_int("alberprohibit", 0) == 0
            and int(week or 0) != 5
        )

init 20 python:
    npc_schedule_set("alber", [
        NPCScheduleEntry(location="WineStore", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[1, 2], awake=True, talkable=True, priority=180, label="wine_store_day"),
        NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[3], awake=True, talkable=True, condition=alber_tavern_visit_ready, priority=260, label="amanda_tavern_visit"),
        NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, priority=260, label="friday_dance"),
        NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=180, label="sunday_church"),
    ])

define AlberStaticData = AlberData()
default Alber = AlberInfo()

label register_alber_secondary:
    $ knowsMC.setdefault("alber", False)
    python:
        peopleData["alber"] = AlberStaticData
        Alber.update()
        peopleInfo["alber"] = Alber
        if Alber not in secondary_npcs:
            secondary_npcs.append(Alber)
    return


label _auto_register_alber:
    call register_alber_secondary from _call_alber_reg
    return
