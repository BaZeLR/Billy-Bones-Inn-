init python:
    def robin_story_defaults():
        return {
        "KnowHim": 0, "KnowComplaint": 0, "KnowPlace": 0, "KnowWeapon": 0,
        "RobbedNum": 0, "Negotiate": 0, "KnowBigTitsVillage": 0,
        "MongolSafePass": 0, "PlayerDestroyedCamp": 0, "ZimmerPeaceful": 0,
        "MongolSafePassUsed": 0, "KunidellOpened": 0, "KunidellDeliveries": 0,
        "BlackwoodRoadSeen": 0, "BlackwoodRoadOpen": 0,
    }

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
        code_name = "robin"
        unknown_name = "Робин"

        def __init__(self, name="robin", **kwargs):
            super().__init__(name, **kwargs)
            self.location = "BlackwoodRoad"
            self.ensure_story_defaults()

        def ensure_story_defaults(self):
            if not isinstance(getattr(self, "var", None), dict):
                self.var = {}
            for k, v in robin_story_defaults().items():
                self.var.setdefault(k, v)
            self.promote_from_var(self.var)
            return self.var

        def update(self):
            self.name = self.code_name
            self.data = RobinStaticData
            self.ensure_story_defaults()
            return self

        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[str(key or "")] = value
            self.promote_from_var(self.var)
            return value

        def add_var_int(self, key, amount=1):
            return self.set_var_int(key, self.var_int(key, 0) + people_to_int(amount, 0))

        def set_var_min(self, key, value):
            return self.set_var_int(key, max(self.var_int(key, 0), people_to_int(value, 0)))

define RobinStaticData = RobinData()
default Robin = RobinInfo()

label InitRobin:
    call register_robin_secondary from _call_init_robin_register
    return


label register_robin_secondary:
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["robin"] = RobinStaticData
            Robin.location = "BlackwoodRoad"
            Robin.update()
            peopleInfo["robin"] = Robin
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("robin") and peopleInfo["robin"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["robin"])
    $ RobinProfile = "Робин (он же Робин Гуд, он же Худи/Гуди) — предводитель группы 'обездоленных' лесорубов на Шервудской (ныне Блэквудской) вырубке. Любит 'социяльную ответственность', пожертвования и стиль 'йо, браза'. После освобождения Монгола из колодок — потенциальный друг (через Монгола)."
    return


label _auto_register_robin:
    call register_robin_secondary from _call_robin_reg
    return
