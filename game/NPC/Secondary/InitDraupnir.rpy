default DraupnirVar = {}

init python:
    if 'DraupnirVar' not in dir() or not isinstance(DraupnirVar, dict):
        DraupnirVar = {}
    for k, v in {
        "SloganAsked": 0,
        "HoleAsked": 0,
        "GloryHoleAsked": 0,
        "SoapBarrelAsked": 0,
        "DogBoothAsked": 0,
        "MongolLockpickOrderDay": -1,
    }.items():
        DraupnirVar.setdefault(k, v)

    class DraupnirData(PeopleData):
        code_name = "draupnir"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Драупнир",
                fullname="Мастер Драупнир",
                genitive="Драупнира",
                dative="Драупниру",
                default_location="StolyarWorkshop",
                description="Драупнир - гном-столяр из квартала ремесленников. Дерет дорого, но вывески, отверстия, глорихолы, зольные бочки и будки делает на совесть.",
                age=45,
                portrait="images/draupnir/dwarf1.jpg",
            )

    class DraupnirInfo(BaseNPC):
        """Draupnir: carpenter/artisan in StolyarWorkshop, gloryhole/soap/dog-booth quests."""
        unknown_name = "Драупнир"

        def __init__(self, name="draupnir", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", DraupnirVar)
            for k, v in {
                "SloganAsked": 0,
                "HoleAsked": 0,
                "GloryHoleAsked": 0,
                "SoapBarrelAsked": 0,
                "DogBoothAsked": 0,
                "MongolLockpickOrderDay": -1,
            }.items():
                self.var.setdefault(k, v)
            self.location = "StolyarWorkshop"
            self.promote_from_var(self.var)

define DraupnirStaticData = DraupnirData()
default Draupnir = DraupnirInfo()

label InitDraupnir:
    call register_draupnir_secondary from _call_init_draupnir_register
    return


label register_draupnir_secondary:
    $ knowsMC.setdefault("draupnir", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["draupnir"] = DraupnirStaticData
            Draupnir.var = DraupnirVar
            Draupnir.location = "StolyarWorkshop"
            Draupnir.update()
            peopleInfo["draupnir"] = Draupnir
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("draupnir") and peopleInfo["draupnir"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["draupnir"])
    $ DraupnirProfile = "Драупнир — гном-столяр, работает в Столярной мастерской. Связан с квестами по gloryhole, мылу, вывеске и будке."
    return


label _auto_register_draupnir:
    call register_draupnir_secondary from _call_draupnir_reg
    return
