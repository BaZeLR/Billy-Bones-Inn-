            self.promote_from_var(self.var)

label _auto_register_francheska:
    call register_francheska_secondary from _call_francheska_reg
    return            self.promote_from_var(self.var)

label _auto_register_francheska:
    call register_francheska_secondary from _call_francheska_reg
    return            self.promote_from_var(self.var)

label _auto_register_francheska:
    call register_francheska_secondary from _call_francheska_reg
    returndefault FranVar = {}
default FranBusy = {}

default FranVar = {}
default FranBusy = {}

default FranVar = {}
default FranBusy = {}

init python:
    if 'FranVar' not in dir() or not isinstance(FranVar, dict):
        FranVar = {}
    for k, v in {
        "meet": 0, "ellonaask": 0, "graceask": 0, "conchitaask": 0,
        "dukeask": 0, "starkask": 0, "stateask": 0, "kingask": 0,
        "rebelask": 0, "alienask": 0, "lasttalkday": -1,
        "sunday_stories_seen_day": -1,
    }.items():
        FranVar.setdefault(k, v)

    if 'FranVar' not in dir() or not isinstance(FranVar, dict):
        FranVar = {}
    for k, v in {
        "meet": 0, "ellonaask": 0, "graceask": 0, "conchitaask": 0,
        "dukeask": 0, "starkask": 0, "stateask": 0, "kingask": 0,
        "rebelask": 0, "alienask": 0, "lasttalkday": -1,
        "sunday_stories_seen_day": -1,
    }.items():
        FranVar.setdefault(k, v)

    if 'FranVar' not in dir() or not isinstance(FranVar, dict):
        FranVar = {}
    for k, v in {
        "meet": 0, "ellonaask": 0, "graceask": 0, "conchitaask": 0,
        "dukeask": 0, "starkask": 0, "stateask": 0, "kingask": 0,
        "rebelask": 0, "alienask": 0, "lasttalkday": -1,
        "sunday_stories_seen_day": -1,
    }.items():
        FranVar.setdefault(k, v)

    class FranData(PeopleData):
        code_name = "fran"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Франческа",
                fullname="Франческа",
                genitive="Франчески",
                dative="Франческе",
                default_location="EllonaTemple",
                description="Франческа - старая жрица Эллоны, встречает прихожан в храме и помогает роженицам.",
                birth_date={"day": 1, "period": 1, "cycle": 1048},
                portrait="images/ellona/Fran1.jpg",
            )

    class FrancheskaInfo(BaseNPC):
        """Francheska: Ellona temple priestess, talk flags, birth-room state."""
        unknown_name = "Старая жрица"

        def __init__(self, name="fran", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", FranVar)
            for k, v in {
                "meet": 0,
                "ellonaask": 0,
                "graceask": 0,
                "conchitaask": 0,
                "dukeask": 0,
                "starkask": 0,
                "stateask": 0,
                "kingask": 0,
                "rebelask": 0,
                "alienask": 0,
                "lasttalkday": -1,
                "sunday_stories_seen_day": -1,
            }.items():
                self.var.setdefault(k, v)
            self.location = "EllonaTemple"
            self.location = "EllonaTemple"

        def getLocation(self, wday=None, hour=None):
            if self.busy_now():
                self.location = "EllonaBirthRoom"
                return self.location
            current_room = str(CurLoc or "").strip()
            if current_room in ("EllonaTemple", "EllonaBirthRoom"):
                self.location = current_room
            else:
                self.location = "EllonaTemple"
            return self.location

        def current_minutes(self):
            try:
                return int(clock_minutes or 0) % 1440
            except Exception:
                return 0

        def current_slot(self):
            hour_value = self.current_minutes() // 60
            if 6 <= hour_value < 8:
                return 0
            if 8 <= hour_value < 11:
                return 1
            if 11 <= hour_value < 13:
                return 2
            if 13 <= hour_value < 16:
                return 3
            if 16 <= hour_value < 18:
                return 4
            if 18 <= hour_value < 21:
                return 5
            if 21 <= hour_value < 23:
                return 6
            return 7

        def busy_now(self):
            return int(FranBusy.get(self.current_slot(), 0) or 0) != 0

        def visible_now(self):
            return not self.busy_now()

        def birth_room_available(self):
            return self.visible_now()

        def known_now(self):
            return self.visible_now() and bool(self.var.get("meet", 0))

        def unknown_now(self):
            return self.visible_now() and not bool(self.var.get("meet", 0))

        def sleep_note_now(self):
            minute_value = self.current_minutes()
            return self.visible_now() and (minute_value < 8 * 60 or minute_value >= 21 * 60)

        def sunday_stories_available(self):
            minute_value = self.current_minutes()
            return (
                int(week or 0) == 7
                and 8 * 60 <= minute_value <= 12 * 60
                and self.visible_now()
                and int(self.var.get("sunday_stories_seen_day", -1) or -1) < int(current_game_day() or 0)
            )

        def mark_sunday_stories_seen(self):
            self.var["sunday_stories_seen_day"] = int(current_game_day() or 0)
            return self.var["sunday_stories_seen_day"]

        def mark_met(self):
            self.var["meet"] = 1
            self.mark_known()
            return True

    def francheska_busy_now():
        return Francheska.busy_now()

    def francheska_known_now():
        return Francheska.known_now()

    def francheska_unknown_now():
        return Francheska.unknown_now()

    def francheska_sleep_note_now():
        return Francheska.sleep_note_now()

    def francheska_birth_room_available():
        return Francheska.birth_room_available()

define FranStaticData = FranData()
default Francheska = FrancheskaInfo()

label InitFrancheska:
    call register_francheska_secondary from _call_init_francheska_register
    return


label InitFrancheska:
    call register_francheska_secondary from _call_init_francheska_register
    return


label InitFrancheska:
    call register_francheska_secondary from _call_init_francheska_register
    return


label register_francheska_secondary:
    python:
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            peopleData["fran"] = FranStaticData
            Francheska.var = FranVar
            Francheska.location = "EllonaTemple"
            Francheska.var = FranVar
            Francheska.var = FranVar
            Francheska.location = "EllonaTemple"
            Francheska.location = "EllonaTemple"
            Francheska.location = "EllonaTemple"
            Francheska.location = "EllonaTemple"
            Francheska.update()
            peopleInfo["fran"] = Francheska
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("fran") and peopleInfo["fran"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["fran"])
    return
