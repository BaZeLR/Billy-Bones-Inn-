# Secondary NPC registration (PeopleInfo + direct knowsMC model)
# Most secondary classes live here. Larger NPCs can own their own Init*.rpy
# files, following the same pattern used for girls.
# Instantiation + list append stays in the thin label registrations.
# References:
# - textLocRef\InitSecondaryNPC.txt (legacy defaults)
# - devdocs/people.rpy (historical model)
# - game/Utilities/General/NPC/PeopleRuntime.rpy (BaseNPC + init -999 + secondary_npcs list)
# - User request: finish all secondaries including Luisa and Sergio.
#
# Robin (the "Robin Hood" parody leader of the обездоленные in the Blackwood/Sherwood cut)
# Dialog ready in textLocRef\IntRobinTalk.txt
# Pictures ready (portrait, robin1, robin2 sequences used in SherwoodTravel + IntRobinTalk)

default LuisaVar = {}
default SergioVar = {}
default GerhardVar = {}
default LucasVar = {}
default ClaraFianceVar = {}
default SergioPetVar = {}
default RobbersHeadNameTmp = ""
default Talked = {}
default cancumdaily_npc = {}
default KnowMongol = 0
default StolenHorseDays = 0

init python:
    # Ensure the secondary keys list exists
    if 'SECONDARY_NPC_KEYS' not in dir():
        SECONDARY_NPC_KEYS = []

    # All known secondary NPCs.
    for _sec_key in ["robin", "zimmer", "eddie", "alber", "fran", "mongol", "luisa", "sergio", "draupnir", "gerhard", "lucas", "clara_fiance", "sergio_pet"]:
        if _sec_key not in SECONDARY_NPC_KEYS:
            SECONDARY_NPC_KEYS.append(_sec_key)

    # --- Var defaults (legacy tables kept for compat) ---
    if 'LuisaVar' not in dir() or not isinstance(LuisaVar, dict):
        LuisaVar = {}
    for k, v in {
        "met": 0,
        "lasttalkday": -1,
    }.items():
        LuisaVar.setdefault(k, v)
    if 'SergioVar' not in dir() or not isinstance(SergioVar, dict):
        SergioVar = {}
    for k, v in {
        "met": 0,
        "lasttalkday": -1,
        "clara_fiance_visit_seen": 0,
    }.items():
        SergioVar.setdefault(k, v)
    if 'LucasVar' not in dir() or not isinstance(LucasVar, dict):
        LucasVar = {}
    for k, v in {
        "met": 0,
        "last_seen_with_inga_day": -1,
    }.items():
        LucasVar.setdefault(k, v)
    if 'ClaraFianceVar' not in dir() or not isinstance(ClaraFianceVar, dict):
        ClaraFianceVar = {}
    for k, v in {
        "met": 0,
        "last_seen_day": -1,
    }.items():
        ClaraFianceVar.setdefault(k, v)
    if 'SergioPetVar' not in dir() or not isinstance(SergioPetVar, dict):
        SergioPetVar = {}
    for k, v in {
        "met": 0,
        "last_seen_day": -1,
    }.items():
        SergioPetVar.setdefault(k, v)
    if 'GerhardVar' not in dir() or not isinstance(GerhardVar, dict):
        GerhardVar = {}
    for k, v in {
        "confession_intro_done": 0,
        "sermon_story_stage": 0,
        "becky_advice_stage": 0,
        "georgett_confession_stage": 0,
        "liza_confession_stage": 0,
        "lasttalkday": -1,
    }.items():
        GerhardVar.setdefault(k, v)

    # --- All secondary class definitions live here in the normal Init file (init python block) ---
    # Per user request: specific classes in the per-NPC init file, inheriting BaseNPC from the people rpy file.
    # Everything uses .var for legacy XXXVar dicts + promote_from_var for story flags.

    class LuisaData(PeopleData):
        code_name = "luisa"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Луиза",
                fullname="Толстушка Луиза",
                genitive="Луизы",
                dative="Луизе",
                default_location="HunterClub",
                description="Луиза - полная городская знакомая из охотничьей лавки и городских социальных сцен.",
                age=28,
            )

    class LuisaInfo(BaseNPC):
        """Fat Luisa: secondary female NPC for hunter store and social scenes."""
        unknown_name = "Луиза"

        def __init__(self, name="luisa", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", LuisaVar)
            for k, v in {
                "met": 0,
                "lasttalkday": -1,
            }.items():
                self.var.setdefault(k, v)
            self.location = "HunterClub"
            self.promote_from_var(self.var)

    class SergioData(PeopleData):
        code_name = "sergio"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Серджио",
                fullname="Серджио",
                genitive="Серджио",
                dative="Серджио",
                default_location="ArtisansQuarter",
                description="Серджио - цирюльник из квартала ремесленников, связан с тайными визитами столичного жениха Клариссы.",
                age=35,
            )

    class SergioInfo(BaseNPC):
        """Sergio (secondary artisan / town NPC, discount/quest hooks)."""
        unknown_name = "Серджио"

        def __init__(self, name="sergio", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", SergioVar)
            for k, v in {
                "met": 0,
                "lasttalkday": -1,
                "clara_fiance_visit_seen": 0,
            }.items():
                self.var.setdefault(k, v)
            self.location = "ArtisansQuarter"
            self.promote_from_var(self.var)

    class LucasData(PeopleData):
        code_name = "lucas"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Лукас",
                fullname="Лукас",
                genitive="Лукаса",
                dative="Лукасу",
                default_location="BeckyHome",
                description="Лукас - ухажер и жених Ингенборг Блэнкеншип.",
                age=23,
            )

    class LucasInfo(BaseNPC):
        """Lucas: Inga's boyfriend/fiance and pregnancy father in Becky-home scenes."""
        unknown_name = "Лукас"

        def __init__(self, name="lucas", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", LucasVar)
            for k, v in {
                "met": 0,
                "last_seen_with_inga_day": -1,
            }.items():
                self.var.setdefault(k, v)
            self.location = "BeckyHome"
            self.promote_from_var(self.var)

    class ClaraFianceData(PeopleData):
        code_name = "clara_fiance"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Столичный жених",
                fullname="Столичный жених Клариссы",
                genitive="столичного жениха Клариссы",
                dative="столичному жениху Клариссы",
                default_location="",
                description="Столичный жених Клариссы - молодой дворянин из договоренности семьи Легаре.",
                age=24,
            )

    class ClaraFianceInfo(BaseNPC):
        """Clara's fiance: identity only; Clara's thread owns discovery flags."""
        unknown_name = "Столичный жених"

        def __init__(self, name="clara_fiance", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", ClaraFianceVar)
            for k, v in {
                "met": 0,
                "last_seen_day": -1,
            }.items():
                self.var.setdefault(k, v)
            self.location = ""
            self.promote_from_var(self.var)

    class SergioPetData(PeopleData):
        code_name = "sergio_pet"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Питомец Серджио",
                fullname="Питомец Серджио",
                genitive="питомца Серджио",
                dative="питомцу Серджио",
                default_location="BarberShop",
                description="Питомец Серджио - второстепенная сущность для будущих сцен цирюльни.",
                age=0,
            )

    class SergioPetInfo(BaseNPC):
        """Sergio's pet: secondary runtime object for barber-shop scenes."""
        unknown_name = "Питомец Серджио"

        def __init__(self, name="sergio_pet", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", SergioPetVar)
            for k, v in {
                "met": 0,
                "last_seen_day": -1,
            }.items():
                self.var.setdefault(k, v)
            self.location = "BarberShop"
            self.promote_from_var(self.var)

    class GerhardData(PeopleData):
        code_name = "gerhard"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Брат Герхард",
                fullname="Брат Герхард",
                genitive="брата Герхарда",
                dative="брату Герхарду",
                default_location="Church",
                description="Брат Герхард - священник городского храма, принимает исповеди и ведет воскресные наставления.",
                age=48,
                portrait="images/gerhard/portrait.png",
            )

    class GerhardInfo(BaseNPC):
        """Brother Gerhardt: church priest, confession and sermon story flags."""
        unknown_name = "Брат Герхард"

        def __init__(self, name="gerhard", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", GerhardVar)
            for k, v in {
                "confession_intro_done": 0,
                "sermon_story_stage": 0,
                "becky_advice_stage": 0,
                "georgett_confession_stage": 0,
                "liza_confession_stage": 0,
                "lasttalkday": -1,
            }.items():
                self.var.setdefault(k, v)
            self.location = "Church"
            self.promote_from_var(self.var)

    def secondary_npc_default_profiles():
        return {
            "eddie": {
                "names": ("Эдди", "Эдди", "Эдди"),
                "age": 17,
                "location": "GroceryStore",
                "description": "Эдди - сын Ребекки, подросток и помощник в бакалейной лавке. Связан с событиями Бекки, Жоржетты и Лукаса.",
                "known": False,
            },
            "alber": {
                "names": ("Альбер", "Альбера", "Альберу"),
                "age": 36,
                "location": "WineStore",
                "description": "Мессир Альбер Легаре - хозяин винного погребка, женат, у него большая семья.",
                "known": False,
            },
            "fran": {
                "names": ("Франческа", "Франчески", "Франческе"),
                "age": 52,
                "location": "EllonaTemple",
                "description": "Франческа - жрица Эллоны, встречает прихожан в храме и помогает роженицам.",
                "known": False,
                "var": FranVar,
            },
            "robin": {
                "names": ("Робин", "Робина", "Робину"),
                "age": 30,
                "location": "BlackwoodRoad",
                "description": "Робин - предводитель лесных обездоленных.",
                "known": False,
                "var": RobinVar,
            },
            "mongol": {
                "names": ("Монгол", "Монгола", "Монголу"),
                "age": 39,
            "location": "",
            "description": "Монгол - торговец лошадьми на рынке.",
            "known": False,
        },
            "zimmer": {
                "names": ("Десятник Циммерман", "Десятника Циммермана", "Десятнику Циммерману"),
                "age": 58,
                "location": "CityGuard",
                "description": "Десятник Циммерман - начальник городской стражи.",
                "known": False,
            },
            "draupnir": {
                "names": ("Драупнир", "Драупнира", "Драупниру"),
                "age": 45,
                "location": "StolyarWorkshop",
                "description": "Драупнир - гном-столяр из квартала ремесленников. Дерет дорого, но вывески, отверстия, глорихолы, зольные бочки и будки делает на совесть.",
                "known": False,
                "var": DraupnirVar,
            },
            "luisa": {
                "names": ("Луиза", "Луизы", "Луизе"),
                "age": 28,
                "location": "HunterClub",
                "description": "Луиза - полная городская знакомая из охотничьей лавки и городских социальных сцен.",
                "known": False,
                "var": LuisaVar,
            },
            "sergio": {
                "names": ("Серджио", "Серджио", "Серджио"),
                "age": 35,
                "location": "ArtisansQuarter",
                "description": "Серджио - цирюльник из квартала ремесленников.",
                "known": False,
                "var": SergioVar,
            },
            "lucas": {
                "names": ("Лукас", "Лукаса", "Лукасу"),
                "age": 23,
                "location": "BeckyHome",
                "description": "Лукас - ухажер и жених Ингенборг Блэнкеншип.",
                "known": False,
                "var": LucasVar,
            },
            "clara_fiance": {
                "names": ("Столичный жених", "столичного жениха", "столичному жениху"),
                "age": 24,
                "location": "",
                "description": "Столичный жених Клариссы - молодой дворянин из договоренности семьи Легаре.",
                "known": False,
                "var": ClaraFianceVar,
            },
            "sergio_pet": {
                "names": ("Питомец Серджио", "питомца Серджио", "питомцу Серджио"),
                "age": 0,
                "location": "BarberShop",
                "description": "Питомец Серджио - второстепенная сущность для будущих сцен цирюльни.",
                "known": False,
                "var": SergioPetVar,
            },
            "gerhard": {
                "names": ("Брат Герхард", "брата Герхарда", "брату Герхарду"),
                "age": 48,
                "location": "Church",
                "description": "Брат Герхард - священник городского храма, принимает исповеди и ведет воскресные наставления.",
                "known": False,
                "var": GerhardVar,
            },
        }

    def init_secondary_npc_profiles():
        profiles = secondary_npc_default_profiles()
        for npc_key, row in profiles.items():
            n1, n2, n3 = row.get("names", (npc_key, npc_key, npc_key))
            RealName[npc_key] = str(n1)
            RealName2[npc_key] = str(n2)
            RealName3[npc_key] = str(n3)
            age_girls[npc_key] = int(row.get("age", 0) or 0)
            girltextdesc[npc_key] = str(row.get("description", "") or "")
            CurrentLoc[npc_key] = str(row.get("location", "") or "")
            Friends[npc_key] = int(Friends.get(npc_key, 0) or 0)
            knowsMC[npc_key] = bool(row.get("known", False))
            kids[npc_key] = int(kids.get(npc_key, 0) or 0)
            beauty[npc_key] = int(beauty.get(npc_key, 0) or 0)
            sluttiness[npc_key] = int(sluttiness.get(npc_key, 0) or 0)
            otkroven[npc_key] = int(otkroven.get(npc_key, 0) or 0)
            cooking[npc_key] = int(cooking.get(npc_key, 0) or 0)
            cleaning[npc_key] = int(cleaning.get(npc_key, 0) or 0)
            waitress[npc_key] = int(waitress.get(npc_key, 0) or 0)
            jobkitchen[npc_key] = int(jobkitchen.get(npc_key, 0) or 0)
            jobcleaning[npc_key] = int(jobcleaning.get(npc_key, 0) or 0)
            jobwaitress[npc_key] = int(jobwaitress.get(npc_key, 0) or 0)
            jobwhore[npc_key] = int(jobwhore.get(npc_key, 0) or 0)
            jobgloryhole[npc_key] = int(jobgloryhole.get(npc_key, 0) or 0)
            var_table = row.get("var", {})
            if npc_key == "robin":
                peopleData[npc_key] = RobinStaticData
            if npc_key == "zimmer":
                peopleData[npc_key] = ZimmerStaticData
            if npc_key == "eddie":
                peopleData[npc_key] = EddieStaticData
            if npc_key == "alber":
                peopleData[npc_key] = AlberStaticData
            if npc_key == "fran":
                peopleData[npc_key] = FranStaticData
            if npc_key == "gerhard":
                peopleData[npc_key] = GerhardStaticData
            if npc_key == "draupnir":
                peopleData[npc_key] = DraupnirStaticData
            if npc_key == "mongol":
                peopleData[npc_key] = MongolStaticData
            if npc_key == "luisa":
                peopleData[npc_key] = LuisaStaticData
            if npc_key == "sergio":
                peopleData[npc_key] = SergioStaticData
            if npc_key == "lucas":
                peopleData[npc_key] = LucasStaticData
            if npc_key == "clara_fiance":
                peopleData[npc_key] = ClaraFianceStaticData
            if npc_key == "sergio_pet":
                peopleData[npc_key] = SergioPetStaticData
            if npc_key == "alber":
                peopleInfo[npc_key] = Alber
                peopleInfo[npc_key].update()
            elif npc_key in peopleInfo and isinstance(peopleInfo[npc_key], PeopleInfo):
                peopleInfo[npc_key].var = var_table
                peopleInfo[npc_key].update()
        return profiles

define GerhardStaticData = GerhardData()
default Gerhard = GerhardInfo()
define LuisaStaticData = LuisaData()
default Luisa = LuisaInfo()
define SergioStaticData = SergioData()
default Sergio = SergioInfo()
define LucasStaticData = LucasData()
default Lucas = LucasInfo()
define ClaraFianceStaticData = ClaraFianceData()
default ClaraFiance = ClaraFianceInfo()
define SergioPetStaticData = SergioPetData()
default SergioPet = SergioPetInfo()

label register_gerhard_secondary:
    $ knowsMC.setdefault("gerhard", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["gerhard"] = GerhardStaticData
            Gerhard.var = GerhardVar
            Gerhard.location = "Church"
            Gerhard.update()
            peopleInfo["gerhard"] = Gerhard
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("gerhard") and peopleInfo["gerhard"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["gerhard"])
    return


label _auto_register_gerhard:
    call register_gerhard_secondary from _call_gerhard_reg
    return


label register_luisa_secondary:
    $ knowsMC.setdefault("luisa", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["luisa"] = LuisaStaticData
            Luisa.var = LuisaVar
            Luisa.location = "HunterClub"
            Luisa.update()
            peopleInfo["luisa"] = Luisa
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("luisa") and peopleInfo["luisa"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["luisa"])
    $ LuisaProfile = "Луиза — второстепенная женская NPC (охотничья лавка и городские социальные сцены)."
    return


label register_sergio_secondary:
    $ knowsMC.setdefault("sergio", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["sergio"] = SergioStaticData
            Sergio.var = SergioVar
            Sergio.location = "ArtisansQuarter"
            Sergio.update()
            peopleInfo["sergio"] = Sergio
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("sergio") and peopleInfo["sergio"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["sergio"])
    $ SergioProfile = "Серджио — второстепенный ремесленник/городской NPC (скидки, квестовые хуки)."
    return


label _auto_register_luisa:
    call register_luisa_secondary from _call_luisa_reg
    return


label _auto_register_sergio:
    call register_sergio_secondary from _call_sergio_reg
    return


label register_lucas_secondary:
    $ knowsMC.setdefault("lucas", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["lucas"] = LucasStaticData
            Lucas.var = LucasVar
            Lucas.location = "BeckyHome"
            Lucas.update()
            peopleInfo["lucas"] = Lucas
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("lucas") and peopleInfo["lucas"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["lucas"])
    return


label register_clara_fiance_secondary:
    $ knowsMC.setdefault("clara_fiance", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["clara_fiance"] = ClaraFianceStaticData
            ClaraFiance.var = ClaraFianceVar
            ClaraFiance.location = ""
            ClaraFiance.update()
            peopleInfo["clara_fiance"] = ClaraFiance
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("clara_fiance") and peopleInfo["clara_fiance"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["clara_fiance"])
    return


label register_sergio_pet_secondary:
    $ knowsMC.setdefault("sergio_pet", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["sergio_pet"] = SergioPetStaticData
            SergioPet.var = SergioPetVar
            SergioPet.location = "BarberShop"
            SergioPet.update()
            peopleInfo["sergio_pet"] = SergioPet
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("sergio_pet") and peopleInfo["sergio_pet"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["sergio_pet"])
    return


label _auto_register_lucas:
    call register_lucas_secondary from _call_lucas_reg
    return


label _auto_register_clara_fiance:
    call register_clara_fiance_secondary from _call_clara_fiance_reg
    return


label _auto_register_sergio_pet:
    call register_sergio_pet_secondary from _call_sergio_pet_reg
    return
