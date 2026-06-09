# Secondary NPC registration (PeopleInfo + direct knowsMC model)
# All secondary classes (Robin, Zimmer, Mongol, Eddie, Alber, Francheska, Luisa, Sergio + others)
# are now defined as class XXX(BaseNPC): inside this single Init file under init python:
# (following the exact pattern used for girls in their per-NPC Init*.rpy files).
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

default EddieVar = {}
default AlberVar = {}
default FranVar = {}
default FranBusy = {}
default DraupnirVar = {}
default MongolVar = {}
default ZimmerVar = {}
default RobinVar = {}
default LuisaVar = {}
default SergioVar = {}
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
    for _sec_key in ["robin", "zimmer", "eddie", "alber", "fran", "mongol", "luisa", "sergio", "draupnir"]:
        if _sec_key not in SECONDARY_NPC_KEYS:
            SECONDARY_NPC_KEYS.append(_sec_key)

    # --- Var defaults (legacy tables kept for compat) ---
    if 'RobinVar' not in dir() or not isinstance(RobinVar, dict):
        RobinVar = {}
    for k, v in {
        "KnowHim": 0, "KnowComplaint": 0, "KnowPlace": 0, "KnowWeapon": 0,
        "RobbedNum": 0, "Negotiate": 0, "KnowBigTitsVillage": 0,
        "MongolSafePass": 0, "PlayerDestroyedCamp": 0, "ZimmerPeaceful": 0,
    }.items():
        RobinVar.setdefault(k, v)

    if 'ZimmerVar' not in dir() or not isinstance(ZimmerVar, dict):
        ZimmerVar = {}
    for k, v in {
        "ComplainHorse": 0, "SherwoodStory": 0, "ComplainRobin": 0,
        "RobinInvestigationDay": 0, "MissionUpdatedByPlayer": 0, "PlayerHandledRobin": 0,
    }.items():
        ZimmerVar.setdefault(k, v)

    if 'MongolVar' not in dir() or not isinstance(MongolVar, dict):
        MongolVar = {}
    MongolVar.setdefault("StocksReleased", 0)
    MongolVar.setdefault("WillTryToSteal", 0)
    MongolVar.setdefault("StocksFoodDay", -1)

    if 'EddieVar' not in dir() or not isinstance(EddieVar, dict):
        EddieVar = {}
    if 'AlberVar' not in dir() or not isinstance(AlberVar, dict):
        AlberVar = {}
    if 'FranVar' not in dir() or not isinstance(FranVar, dict):
        FranVar = {}
    for k, v in {
        "meet": 0, "ellonaask": 0, "graceask": 0, "conchitaask": 0,
        "dukeask": 0, "starkask": 0, "stateask": 0, "rebelask": 0,
        "alienask": 0, "lasttalkday": -1,
    }.items():
        FranVar.setdefault(k, v)

    # Luisa and Sergio (explicitly requested) - minimal tables for now, expanded as needed
    if 'LuisaVar' not in dir() or not isinstance(LuisaVar, dict):
        LuisaVar = {}
    if 'SergioVar' not in dir() or not isinstance(SergioVar, dict):
        SergioVar = {}

    # Draupnir (blacksmith / artisan) - was missing from previous migration, causing NameError
    if 'DraupnirVar' not in dir() or not isinstance(DraupnirVar, dict):
        DraupnirVar = {}
    DraupnirVar.setdefault("SloganAsked", 0)
    DraupnirVar.setdefault("HoleAsked", 0)
    DraupnirVar.setdefault("GloryHoleAsked", 0)
    DraupnirVar.setdefault("SoapBarrelAsked", 0)
    DraupnirVar.setdefault("DogBoothAsked", 0)
    DraupnirVar.setdefault("MongolLockpickOrderDay", -1)

    # --- All secondary class definitions live here in the normal Init file (init python block) ---
    # Per user request: specific classes in the per-NPC init file, inheriting BaseNPC from the people rpy file.
    # Everything uses .var for legacy XXXVar dicts + promote_from_var for story flags.

    class Robin(BaseNPC):
        """Robin (Blackwood/Sherwood leader, MongolSafePass, Zimmer mission)."""
        def __init__(self, name="robin", **kwargs):
            super().__init__(name, **kwargs)
            if 'RobinVar' in dir() and isinstance(RobinVar, dict):
                self.var = RobinVar
                self.promote_from_var(RobinVar)

    class Zimmer(BaseNPC):
        """Zimmer (city guard captain, Robin investigation, Blackwood mission)."""
        def __init__(self, name="zimmer", **kwargs):
            super().__init__(name, **kwargs)
            if 'ZimmerVar' in dir() and isinstance(ZimmerVar, dict):
                self.var = ZimmerVar
                self.promote_from_var(ZimmerVar)

    class Mongol(BaseNPC):
        """Mongol (horse trader, stocks prisoner, theft events)."""
        def __init__(self, name="mongol", **kwargs):
            super().__init__(name, **kwargs)
            if 'MongolVar' in dir() and isinstance(MongolVar, dict):
                self.var = MongolVar
                self.promote_from_var(MongolVar)

    class Eddie(BaseNPC):
        """Eddie (Becky's son, group scenes, Georgett crossover)."""
        def __init__(self, name="eddie", **kwargs):
            super().__init__(name, **kwargs)
            if 'EddieVar' in dir() and isinstance(EddieVar, dict):
                self.var = EddieVar
                self.promote_from_var(EddieVar)

    class Alber(BaseNPC):
        """Alber (artisan / barber shop)."""
        def __init__(self, name="alber", **kwargs):
            super().__init__(name, **kwargs)
            if 'AlberVar' in dir() and isinstance(AlberVar, dict):
                self.var = AlberVar
                self.promote_from_var(AlberVar)

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
        return loadable[renpy.random.randint(0, len(loadable) - 1)] if len(loadable) > 0 else ""

    class Francheska(BaseNPC):
        """Francheska (Ellona temple priestess, talk and birth-room scenes)."""
        def __init__(self, name="fran", **kwargs):
            super().__init__(name, **kwargs)
            if 'FranVar' in dir() and isinstance(FranVar, dict):
                self.var = FranVar
                self.promote_from_var(FranVar)

    class Luisa(BaseNPC):
        """Luisa (secondary female NPC - social/church contexts)."""
        def __init__(self, name="luisa", **kwargs):
            super().__init__(name, **kwargs)
            if 'LuisaVar' in dir() and isinstance(LuisaVar, dict):
                self.var = LuisaVar
                self.promote_from_var(LuisaVar)

    class Sergio(BaseNPC):
        """Sergio (secondary artisan / town NPC, discount/quest hooks)."""
        def __init__(self, name="sergio", **kwargs):
            super().__init__(name, **kwargs)
            if 'SergioVar' in dir() and isinstance(SergioVar, dict):
                self.var = SergioVar
                self.promote_from_var(SergioVar)

    class Draupnir(BaseNPC):
        """Draupnir (blacksmith/artisan in StolyarWorkshop, gloryhole/soap related quests)."""
        def __init__(self, name="draupnir", **kwargs):
            super().__init__(name, **kwargs)
            if 'DraupnirVar' in dir() and isinstance(DraupnirVar, dict):
                self.var = DraupnirVar
                self.promote_from_var(DraupnirVar)

    _secondary_class_map = {
        "robin": Robin,
        "zimmer": Zimmer,
        "eddie": Eddie,
        "alber": Alber,
        "fran": Francheska,
        "mongol": Mongol,
        "luisa": Luisa,
        "sergio": Sergio,
        "draupnir": Draupnir,
    }
    _secondary_var_map = {
        "robin": RobinVar,
        "zimmer": ZimmerVar,
        "eddie": EddieVar,
        "alber": AlberVar,
        "fran": FranVar,
        "mongol": MongolVar,
        "luisa": LuisaVar,
        "sergio": SergioVar,
        "draupnir": DraupnirVar,
    }
    if 'peopleInfo' not in dir() or not isinstance(peopleInfo, dict):
        peopleInfo = {}
    if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
        secondary_npcs = []
    for _sec_key in list(SECONDARY_NPC_KEYS or []):
        _sec_cls = _secondary_class_map.get(_sec_key, BaseNPC)
        _sec_var = _secondary_var_map.get(_sec_key, {})
        if _sec_key not in peopleInfo or not isinstance(peopleInfo.get(_sec_key), _sec_cls):
            peopleInfo[_sec_key] = _sec_cls(var=_sec_var)
        else:
            peopleInfo[_sec_key].var = _sec_var
        if peopleInfo[_sec_key] not in secondary_npcs:
            secondary_npcs.append(peopleInfo[_sec_key])

    def secondary_npc_default_profiles():
        return {
            "eddie": {
                "names": ("Эдди", "Эдди", "Эдди"),
                "age": 19,
                "location": "GroceryStore",
                "description": "Эдди - сирота, которого Бекки подобрала, выучила делу и поставила управляющим семейной лавкой.",
                "known": False,
                "var": EddieVar,
            },
            "alber": {
                "names": ("Альбер", "Альбера", "Альберу"),
                "age": 36,
                "location": "WineStore",
                "description": "Мессир Альбер Легаре - хозяин винного погребка, женат, у него большая семья.",
                "known": False,
                "var": AlberVar,
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
                "location": "Forest",
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
                "var": MongolVar,
            },
            "zimmer": {
                "names": ("Циммер", "Циммера", "Циммеру"),
                "age": 41,
                "location": "CityGuard",
                "description": "Циммер - служащий городской стражи.",
                "known": False,
                "var": ZimmerVar,
            },
            "draupnir": {
                "names": ("Драупнир", "Драупнира", "Драупниру"),
                "age": 45,
                "location": "StolyarWorkshop",
                "description": "Драупнир - мастер из ремесленного квартала.",
                "known": False,
                "var": DraupnirVar,
            },
            "luisa": {
                "names": ("Луиза", "Луизы", "Луизе"),
                "age": 28,
                "location": "Church",
                "description": "Луиза - городская знакомая из церковных и социальных сцен.",
                "known": False,
                "var": LuisaVar,
            },
            "sergio": {
                "names": ("Серджио", "Серджио", "Серджио"),
                "age": 35,
                "location": "",
                "description": "Серджио - цирюльник из квартала ремесленников.",
                "known": False,
                "var": SergioVar,
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
            if npc_key in peopleInfo and isinstance(peopleInfo[npc_key], PeopleInfo):
                peopleInfo[npc_key].var = var_table
                peopleInfo[npc_key].update()
        return profiles

# Registration function call pattern (called from main init after legacy TXT inits)
label register_robin_secondary:
    $ knowsMC.setdefault("robin", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "robin" not in peopleInfo:
                try:
                    info = Robin(var=RobinVar)  # class defined at top of this file (init python)
                    peopleInfo["robin"] = info
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("robin") and peopleInfo["robin"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["robin"])
    $ RobinProfile = "Робин (он же Робин Гуд, он же Худи/Гуди) — предводитель группы 'обездоленных' лесорубов на Шервудской (ныне Блэквудской) вырубке. Любит 'социяльную ответственность', пожертвования и стиль 'йо, браза'. После освобождения Монгола из колодок — потенциальный друг (через Монгола)."
    return


label register_zimmer_secondary:
    $ knowsMC.setdefault("zimmer", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "zimmer" not in peopleInfo:
                try:
                    info = Zimmer(var=ZimmerVar)  # class defined at top of this file
                    peopleInfo["zimmer"] = info
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("zimmer") and peopleInfo["zimmer"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["zimmer"])
    $ ZimmerProfile = "Десятник Циммерман — старый, низкий, носатый, кучерявый начальник городской стражи (десятник). Немного картавит. Любит 'порядок', но очень осторожен (семья, дети, любовницы). Принимает жалобы на конокрадов (лошади) и разбойников в Шервуде/Блэквуде (за деньги). Готов 'поиcкать' Робина, но не арестовывать (не наша земля, слишком опасно). Ключевой NPC для Zimmer mission в Blackwood arc."
    return


# Auto-call on load (safe pattern)
label _auto_register_robin:
    call register_robin_secondary from _call_robin_reg
    return

label _auto_register_zimmer:
    call register_zimmer_secondary from _call_zimmer_reg
    return


# Additional secondary registrations with per-NPC classes (Eddie, Alber, etc.)
# Per user request: classes defined in the Init file for this NPC group.
label register_eddie_secondary:
    $ knowsMC.setdefault("eddie", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "eddie" not in peopleInfo:
                try:
                    peopleInfo["eddie"] = Eddie(var=globals().get("EddieVar", {}))  # class at top of file
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("eddie") and peopleInfo["eddie"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["eddie"])
    $ EddieProfile = "Эдди — сын Ребекки, подросток. Участвует в событиях дома с Жоржеттой и Лукасом (GeorgettBeckyVisit.txt)."
    return


label register_alber_secondary:
    $ knowsMC.setdefault("alber", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "alber" not in peopleInfo:
                try:
                    peopleInfo["alber"] = Alber(var=globals().get("AlberVar", {}))  # class at top of file
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("alber") and peopleInfo["alber"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["alber"])
    return


label register_francheska_secondary:
    $ knowsMC.setdefault("fran", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "fran" not in peopleInfo:
                try:
                    peopleInfo["fran"] = Francheska(var=globals().get("FranVar", {}))
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("fran") and peopleInfo["fran"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["fran"])
    return


label _auto_register_eddie:
    call register_eddie_secondary from _call_eddie_reg
    return


label _auto_register_alber:
    call register_alber_secondary from _call_alber_reg
    return


label _auto_register_francheska:
    call register_francheska_secondary from _call_francheska_reg
    return


# === NEW: Luisa and Sergio (explicitly requested to finish all secondaries) ===
label register_luisa_secondary:
    $ knowsMC.setdefault("luisa", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "luisa" not in peopleInfo:
                try:
                    peopleInfo["luisa"] = Luisa(var=globals().get("LuisaVar", {}))
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("luisa") and peopleInfo["luisa"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["luisa"])
    $ LuisaProfile = "Луиза — второстепенная женская NPC (социальные и церковные сцены)."
    return


label register_sergio_secondary:
    $ knowsMC.setdefault("sergio", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "sergio" not in peopleInfo:
                try:
                    peopleInfo["sergio"] = Sergio(var=globals().get("SergioVar", {}))
                except Exception:
                    pass
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


label register_draupnir_secondary:
    $ knowsMC.setdefault("draupnir", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "draupnir" not in peopleInfo:
                try:
                    peopleInfo["draupnir"] = Draupnir(var=globals().get("DraupnirVar", {}))
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("draupnir") and peopleInfo["draupnir"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["draupnir"])
    $ DraupnirProfile = "Драупнир — гном-кузнец, работает в Столярной мастерской. Связан с квестами по gloryhole и мылу."
    return


label _auto_register_draupnir:
    call register_draupnir_secondary from _call_draupnir_reg
    return


# Also ensure Mongol gets registered early (has heavy Var usage)
label register_mongol_secondary:
    $ knowsMC.setdefault("mongol", False)
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            if "mongol" not in peopleInfo:
                try:
                    peopleInfo["mongol"] = Mongol(var=globals().get("MongolVar", {}))
                except Exception:
                    pass
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("mongol") and peopleInfo["mongol"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["mongol"])
    return


label _auto_register_mongol:
    call register_mongol_secondary from _call_mongol_reg
    return
