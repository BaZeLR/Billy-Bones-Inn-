init python:
    def eddie_story_defaults():
        return {
            "TalkedAboutWhores": 0,
            "SawWithGeorgett": 0,
            "TalkedAboutGeorgett": 0,
            "SawMomSex": 0,
            "FingalTalk": 0,
            "FingalTalkDestination": 0,
            "FingalTalkComplain": 0,
            "RidiculeFollow": 0,
            "OthersSawWithMom": 0,
            "WhoreVisitFreq": 6,
        }

    class EddieData(PeopleData):
        code_name = "eddie"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Эдди",
                fullname="Эдди",
                genitive="Эдди",
                dative="Эдди",
                default_location="GroceryStore",
                description="Эдди - сын Ребекки, подросток и помощник в бакалейной лавке. Связан с событиями Бекки, Жоржетты и Лукаса.",
                age=17,
                portrait="images/eddie/portraits/portrait_0.png",
            )

    class EddieInfo(BaseNPC):
        """Eddie: Becky's son, group scenes, Georgett crossover."""
        unknown_name = "Незнакомец"

        def __init__(self, name="eddie", **kwargs):
            super().__init__(name, **kwargs)
            self.data = EddieStaticData
            self.age = 17
            self.known = False
            self.location = "GroceryStore"
            self.var = {}
            self.ensure_story_defaults()

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = EddieStaticData
            self.location = "GroceryStore"
            self.ensure_story_defaults()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in eddie_story_defaults().items():
                self.var.setdefault(key, value)
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

define EddieStaticData = EddieData()
default Eddie = EddieInfo()

label InitEddie:
    call register_eddie_secondary from _call_init_eddie_register
    return


label register_eddie_secondary:
    $ knowsMC.setdefault("eddie", False)
    python:
        peopleData["eddie"] = EddieStaticData
        Eddie.update()
        peopleInfo["eddie"] = Eddie
        if Eddie not in secondary_npcs:
            secondary_npcs.append(Eddie)
    $ EddieProfile = "Эдди — сын Ребекки, подросток. Участвует в событиях дома с Жоржеттой и Лукасом (GeorgettBeckyVisit.txt)."
    return


label _auto_register_eddie:
    call register_eddie_secondary from _call_eddie_reg
    return
