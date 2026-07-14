        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            self.var[str(key or "")] = people_to_int(value, 0)
            return self.var[str(key or "")]
            self.location = "StolyarWorkshop"            Draupnir.location = Draupnir.getLocation()

label _auto_register_draupnir:
    call register_draupnir_secondary from _call_draupnir_reg
    return        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            self.var[str(key or "")] = people_to_int(value, 0)
            return self.var[str(key or "")]
            self.location = "StolyarWorkshop"            Draupnir.location = Draupnir.getLocation()

label _auto_register_draupnir:
    call register_draupnir_secondary from _call_draupnir_reg
    return        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            self.var[str(key or "")] = people_to_int(value, 0)
            return self.var[str(key or "")]
            self.location = "StolyarWorkshop"            Draupnir.location = Draupnir.getLocation()

label _auto_register_draupnir:
    call register_draupnir_secondary from _call_draupnir_reg
    returndefault DraupnirVar = {}

default DraupnirVar = {}

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
                birth_date={"day": 1, "period": 1, "cycle": 1055},
                portrait="images/draupnir/dwarf1.jpg",
            )

        def getLocation(self, wday=None, hour=None):
            if int(player.tavern_management.slogan_state or 0) == 1:
                return "StreetTavern"
            return super(DraupnirData, self).getLocation(wday, hour)

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
            self.location = "StolyarWorkshop"
            self.promote_from_var(self.var)
            self.location = "StolyarWorkshop"
            self.promote_from_var(self.var)

        def social_action_allowed(self, action="", item_id=""):
            if int(player.tavern_management.slogan_state or 0) == 1:
                return False
            return super(DraupnirInfo, self).social_action_allowed(action, item_id)

define DraupnirStaticData = DraupnirData()
default Draupnir = DraupnirInfo()

label InitDraupnir:
    call register_draupnir_secondary from _call_init_draupnir_register
    return


label InitDraupnir:
    call register_draupnir_secondary from _call_init_draupnir_register
    return


label InitDraupnir:
    call register_draupnir_secondary from _call_init_draupnir_register
    return


label register_draupnir_secondary:
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["draupnir"] = DraupnirStaticData
            Draupnir.var = DraupnirVar
            Draupnir.location = Draupnir.getLocation()
            Draupnir.var = DraupnirVar
            Draupnir.location = Draupnir.getLocation()
            Draupnir.update()
            peopleInfo["draupnir"] = Draupnir
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("draupnir") and peopleInfo["draupnir"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["draupnir"])
    $ DraupnirProfile = "Драупнир — гном-столяр, работает в Столярной мастерской. Связан с квестами по gloryhole, мылу, вывеске и будке."
    return
