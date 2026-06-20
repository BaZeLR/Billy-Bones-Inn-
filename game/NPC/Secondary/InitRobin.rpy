default RobinVar = {}

init python:
    if 'RobinVar' not in dir() or not isinstance(RobinVar, dict):
        RobinVar = {}
    for k, v in {
        "KnowHim": 0, "KnowComplaint": 0, "KnowPlace": 0, "KnowWeapon": 0,
        "RobbedNum": 0, "Negotiate": 0, "KnowBigTitsVillage": 0,
        "MongolSafePass": 0, "PlayerDestroyedCamp": 0, "ZimmerPeaceful": 0,
        "MongolSafePassUsed": 0, "KunidellOpened": 0, "KunidellDeliveries": 0,
        "BlackwoodRoadSeen": 0, "BlackwoodRoadOpen": 0,
    }.items():
        RobinVar.setdefault(k, v)

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
                age=30,
                portrait="images/Robin/portrait1.jpg",
            )

    class RobinInfo(BaseNPC):
        """Robin: Blackwood leader, Mongol safe pass, Zimmer mission."""
        unknown_name = "Робин"

        def __init__(self, name="robin", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", RobinVar)
            for k, v in {
                "KnowHim": 0,
                "KnowComplaint": 0,
                "KnowPlace": 0,
                "KnowWeapon": 0,
                "RobbedNum": 0,
                "Negotiate": 0,
                "KnowBigTitsVillage": 0,
                "MongolSafePass": 0,
                "MongolSafePassUsed": 0,
                "KunidellOpened": 0,
                "KunidellDeliveries": 0,
                "PlayerDestroyedCamp": 0,
                "ZimmerPeaceful": 0,
                "BlackwoodRoadSeen": 0,
                "BlackwoodRoadOpen": 0,
            }.items():
                self.var.setdefault(k, v)
            self.location = "BlackwoodRoad"
            self.promote_from_var(self.var)

define RobinStaticData = RobinData()
default Robin = RobinInfo()

label InitRobin:
    call register_robin_secondary from _call_init_robin_register
    return


label register_robin_secondary:
    $ knowsMC.setdefault("robin", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["robin"] = RobinStaticData
            Robin.var = RobinVar
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
