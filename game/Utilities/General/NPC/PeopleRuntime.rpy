        def promote_from_var(self, vardict=None):
            super().promote_from_var(vardict)
            v = vardict if vardict is not None else self.var
            if isinstance(v, dict):
                for k in ("body_layers", "clothing", "sex_history", "pregnancy"):
                    if k in v and isinstance(v[k], (dict, list)):
                        setattr(self, k, v[k])
            return self
        def publish_visibility_state(self):
            name = people_normalize_id(getattr(self, "code_name", self.name))
            TitsVisible[name] = 1 if self.tits_visible() else 0
            PussyVisible[name] = 1 if self.pussy_visible() else 0
            ShortSkirtNoPanties[name] = 1 if self.short_skirt_no_panties() else 0
            self.publish_visibility_state()
            return self
    def npc_schedule_sync_currentloc(npc_id="", weekday_value=None, time_value=None):
        info = peopleInfo.get(people_normalize_id(npc_id), None)
        if info is None:
            return ""
        info.location = str(info.getLocation(weekday_value, time_value) or "")
        return info.location

    def npc_schedule_sync_all(weekday_value=None, time_value=None):
        for info in list(peopleInfo.values()):
            if info is not None:
                info.location = str(info.getLocation(weekday_value, time_value) or "")
        def publish_wardrobe_state(self):
            name = people_normalize_id(getattr(self, "code_name", self.name))
            wardrobe = getattr(self, "wardrobe", {})
            if not isinstance(wardrobe, dict):
                $ dog_sync_profile()
    $ werecat_sync_profile()
    return self
            underwear = wardrobe.get("current_underwear", {})
            if not isinstance(underwear, dict):
                underwear = {}
                wardrobe["current_underwear"] = underwear
            current_dress = str(wardrobe.get("current_dress", "") or "")
            dressdefault[name] = current_dress
            topdressdef[name] = DressTopPart.get(current_dress, "")
            bottomdressdef[name] = DressBottomPart.get(current_dress, "")
            bradef[name] = str(underwear.get("bra", "") or "")
            pantiesdef[name] = str(underwear.get("panties", "") or "")
            legsdef[name] = str(underwear.get("legs", "") or "")
            shoesdef[name] = str(underwear.get("shoes", "") or "")
            topdress[name] = topdressdef[name]
            bottomdress[name] = bottomdressdef[name]
            bra[name] = bradef[name]
            panties[name] = pantiesdef[name]
            legs[name] = legsdef[name]
            shoes[name] = shoesdef[name]
            topraised[name] = people_to_int(topraised.get(name, 0), 0)
            bottomraised[name] = people_to_int(bottomraised.get(name, 0), 0)
            wardrobe["current_layers"] = [row for row in [dressdefault[name], bradef[name], pantiesdef[name], legsdef[name], shoesdef[name]] if str(row or "")]
            return self
    def people_initial_location(person=""):
        return {
            "sandra": "TavernMain",
            "melissa": "TavernMain",
            "amanda": "TavernMain",
            "georgett": "",
            "liza": "",
            "becky": "GroceryStore",
            "irma": "DressShop",
            "inga": "BeckyHome",
            "clara": "WineStore",
            "eddie": "GroceryStore",
            "alber": "WineStore",
            "fran": "EllonaTemple",
            "gerhard": "Church",
            "lucas": "BeckyHome",
            "clara_fiance": "",
            "robin": "BlackwoodRoad",
            "mongol": "",
            "zimmer": "CityGuard",
            "draupnir": "StolyarWorkshop",
            "luisa": "HunterClub",
            "sergio": "ArtisansQuarter",
            "sergio_pet": "BarberShop",
        }.get(people_normalize_id(person), "")
            self.pregnancy_state = {}    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if isinstance(data, PeopleData):
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": int(entry.time_slots[0]) if list(entry.time_slots or []) else 0,
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if data is not None:
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": list(getattr(entry, "time_slots", []) or [None])[0],
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if data is not None:
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": list(getattr(entry, "time_slots", []) or [None])[0],
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
                self.relationship = self.rel        def promote_from_var(self, vardict=None):
            super().promote_from_var(vardict)
            v = vardict if vardict is not None else self.var
            if isinstance(v, dict):
                for k in ("body_layers", "clothing", "sex_history", "pregnancy"):
                    if k in v and isinstance(v[k], (dict, list)):
                        setattr(self, k, v[k])
            return self
        def publish_visibility_state(self):
            name = people_normalize_id(getattr(self, "code_name", self.name))
            TitsVisible[name] = 1 if self.tits_visible() else 0
            PussyVisible[name] = 1 if self.pussy_visible() else 0
            ShortSkirtNoPanties[name] = 1 if self.short_skirt_no_panties() else 0
            self.publish_visibility_state()
            return self
    def npc_schedule_sync_currentloc(npc_id="", weekday_value=None, time_value=None):
        info = peopleInfo.get(people_normalize_id(npc_id), None)
        if info is None:
            return ""
        info.location = str(info.getLocation(weekday_value, time_value) or "")
        return info.location

    def npc_schedule_sync_all(weekday_value=None, time_value=None):
        for info in list(peopleInfo.values()):
            if info is not None:
                info.location = str(info.getLocation(weekday_value, time_value) or "")
        def publish_wardrobe_state(self):
            name = people_normalize_id(getattr(self, "code_name", self.name))
            wardrobe = getattr(self, "wardrobe", {})
            if not isinstance(wardrobe, dict):
                $ dog_sync_profile()
    $ werecat_sync_profile()
    return self
            underwear = wardrobe.get("current_underwear", {})
            if not isinstance(underwear, dict):
                underwear = {}
                wardrobe["current_underwear"] = underwear
            current_dress = str(wardrobe.get("current_dress", "") or "")
            dressdefault[name] = current_dress
            topdressdef[name] = DressTopPart.get(current_dress, "")
            bottomdressdef[name] = DressBottomPart.get(current_dress, "")
            bradef[name] = str(underwear.get("bra", "") or "")
            pantiesdef[name] = str(underwear.get("panties", "") or "")
            legsdef[name] = str(underwear.get("legs", "") or "")
            shoesdef[name] = str(underwear.get("shoes", "") or "")
            topdress[name] = topdressdef[name]
            bottomdress[name] = bottomdressdef[name]
            bra[name] = bradef[name]
            panties[name] = pantiesdef[name]
            legs[name] = legsdef[name]
            shoes[name] = shoesdef[name]
            topraised[name] = people_to_int(topraised.get(name, 0), 0)
            bottomraised[name] = people_to_int(bottomraised.get(name, 0), 0)
            wardrobe["current_layers"] = [row for row in [dressdefault[name], bradef[name], pantiesdef[name], legsdef[name], shoesdef[name]] if str(row or "")]
            return self
    def people_initial_location(person=""):
        return {
            "sandra": "TavernMain",
            "melissa": "TavernMain",
            "amanda": "TavernMain",
            "georgett": "",
            "liza": "",
            "becky": "GroceryStore",
            "irma": "DressShop",
            "inga": "BeckyHome",
            "clara": "WineStore",
            "eddie": "GroceryStore",
            "alber": "WineStore",
            "fran": "EllonaTemple",
            "gerhard": "Church",
            "lucas": "BeckyHome",
            "clara_fiance": "",
            "robin": "BlackwoodRoad",
            "mongol": "",
            "zimmer": "CityGuard",
            "draupnir": "StolyarWorkshop",
            "luisa": "HunterClub",
            "sergio": "ArtisansQuarter",
            "sergio_pet": "BarberShop",
        }.get(people_normalize_id(person), "")
            self.pregnancy_state = {}    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if isinstance(data, PeopleData):
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": int(entry.time_slots[0]) if list(entry.time_slots or []) else 0,
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if data is not None:
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": list(getattr(entry, "time_slots", []) or [None])[0],
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if data is not None:
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": list(getattr(entry, "time_slots", []) or [None])[0],
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
                self.relationship = self.rel        def promote_from_var(self, vardict=None):
            super().promote_from_var(vardict)
            v = vardict if vardict is not None else self.var
            if isinstance(v, dict):
                for k in ("body_layers", "clothing", "sex_history", "pregnancy"):
                    if k in v and isinstance(v[k], (dict, list)):
                        setattr(self, k, v[k])
            return self
        def publish_visibility_state(self):
            name = people_normalize_id(getattr(self, "code_name", self.name))
            TitsVisible[name] = 1 if self.tits_visible() else 0
            PussyVisible[name] = 1 if self.pussy_visible() else 0
            ShortSkirtNoPanties[name] = 1 if self.short_skirt_no_panties() else 0
            self.publish_visibility_state()
            return self
    def npc_schedule_sync_currentloc(npc_id="", weekday_value=None, time_value=None):
        info = peopleInfo.get(people_normalize_id(npc_id), None)
        if info is None:
            return ""
        info.location = str(info.getLocation(weekday_value, time_value) or "")
        return info.location

    def npc_schedule_sync_all(weekday_value=None, time_value=None):
        for info in list(peopleInfo.values()):
            if info is not None:
                info.location = str(info.getLocation(weekday_value, time_value) or "")
        def publish_wardrobe_state(self):
            name = people_normalize_id(getattr(self, "code_name", self.name))
            wardrobe = getattr(self, "wardrobe", {})
            if not isinstance(wardrobe, dict):
                $ dog_sync_profile()
    $ werecat_sync_profile()
    return self
            underwear = wardrobe.get("current_underwear", {})
            if not isinstance(underwear, dict):
                underwear = {}
                wardrobe["current_underwear"] = underwear
            current_dress = str(wardrobe.get("current_dress", "") or "")
            dressdefault[name] = current_dress
            topdressdef[name] = DressTopPart.get(current_dress, "")
            bottomdressdef[name] = DressBottomPart.get(current_dress, "")
            bradef[name] = str(underwear.get("bra", "") or "")
            pantiesdef[name] = str(underwear.get("panties", "") or "")
            legsdef[name] = str(underwear.get("legs", "") or "")
            shoesdef[name] = str(underwear.get("shoes", "") or "")
            topdress[name] = topdressdef[name]
            bottomdress[name] = bottomdressdef[name]
            bra[name] = bradef[name]
            panties[name] = pantiesdef[name]
            legs[name] = legsdef[name]
            shoes[name] = shoesdef[name]
            topraised[name] = people_to_int(topraised.get(name, 0), 0)
            bottomraised[name] = people_to_int(bottomraised.get(name, 0), 0)
            wardrobe["current_layers"] = [row for row in [dressdefault[name], bradef[name], pantiesdef[name], legsdef[name], shoesdef[name]] if str(row or "")]
            return self
    def people_initial_location(person=""):
        return {
            "sandra": "TavernMain",
            "melissa": "TavernMain",
            "amanda": "TavernMain",
            "georgett": "",
            "liza": "",
            "becky": "GroceryStore",
            "irma": "DressShop",
            "inga": "BeckyHome",
            "clara": "WineStore",
            "eddie": "GroceryStore",
            "alber": "WineStore",
            "fran": "EllonaTemple",
            "gerhard": "Church",
            "lucas": "BeckyHome",
            "clara_fiance": "",
            "robin": "BlackwoodRoad",
            "mongol": "",
            "zimmer": "CityGuard",
            "draupnir": "StolyarWorkshop",
            "luisa": "HunterClub",
            "sergio": "ArtisansQuarter",
            "sergio_pet": "BarberShop",
        }.get(people_normalize_id(person), "")
            self.pregnancy_state = {}    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if isinstance(data, PeopleData):
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": int(entry.time_slots[0]) if list(entry.time_slots or []) else 0,
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if data is not None:
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": list(getattr(entry, "time_slots", []) or [None])[0],
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return data.daily_schedule_build(True if day_marker is not None else False, weekday_value)

    def npc_daily_schedule_build_all(force=False):
        for data in list(peopleData.values()):
            if data is not None:
                data.daily_schedule_build(force)
    def npc_daily_schedule_entries(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.daily_schedule_build(False) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": list(getattr(entry, "time_slots", []) or [None])[0],
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows
                self.relationship = self.rel# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default peopleData = {}
default peopleInfo = {}
default girls = []
default secondary_npcs = []

init -1000 python:
    peopleData = {}
    peopleInfo = {}
    girls = []
    secondary_npcs = []

# =============================================================================
# BASE CLASSES (templates) - placed here in the normal people runtime file
# as requested ("classes as definitions of templates will leave in people").
# Using init -1000 python: (documented Ren'Py priority) so they are available
# before any later init python blocks in the per-NPC Init*.rpy files run.
# Specific per-NPC classes (Amanda, Becky, etc.) stay defined in their own
# game/NPC/*/Init*.rpy files. Instantiation also stays there.
# No magic 00_ files. Only this existing people rpy + the per-NPC Inits.
# =============================================================================
init -1000 python:
    import json

    def people_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def people_to_bool(value, default=False):
        if value is None:
            return bool(default)
        return bool(value)

    def people_clamp(value, low=0, high=100):
        return max(people_to_int(low, 0), min(people_to_int(high, 100), people_to_int(value, low)))

    def people_normalize_id(person=""):
        return str(person or "").strip().lower()

    class NPCScheduleEntry(object):
        def __init__(self, location="", weekdays=None, time_slots=None, start_hour=None, end_hour=None, awake=True, talkable=True, venue_open_required=False, condition=None, priority=0, label=""):
            self.location = str(location or "").strip()
            self.weekdays = list(weekdays or [])
            self.time_slots = list(time_slots or [])
            self.start_hour = None if start_hour is None else max(0, min(23, int(start_hour or 0)))
            self.end_hour = None if end_hour is None else max(0, min(24, int(end_hour or 0)))
            self.awake = bool(awake)
            self.talkable = bool(talkable)
            self.venue_open_required = bool(venue_open_required)
            self.condition = condition
            self.priority = int(priority or 0)
            self.label = str(label or "").strip()

        def selected_location(self):
            return str(self.location or "")

        def matches(self, weekday_value=None, time_value=None):
            week_value = int(week if weekday_value is None else weekday_value or 0)
            hour_value = int(calendar_v2.hour if time_value is None else time_value or 0) % 24
            slot_value = int(calendar_v2.slot_from_hour(hour_value))
            if self.weekdays and week_value not in self.weekdays:
                return False
            if self.start_hour is not None and self.end_hour is not None:
                if self.start_hour <= self.end_hour:
                    if not (self.start_hour <= hour_value < self.end_hour):
                        return False
                elif not (hour_value >= self.start_hour or hour_value < self.end_hour):
                    return False
            if self.time_slots and slot_value not in self.time_slots:
                return False
            return room_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))

    class NPCHourScheduleEntry(NPCScheduleEntry):
        def __init__(self, npc_id="", location="", location_choices=None, weekdays=None, start="00:00", end="23:59", awake=True, talkable=True, condition=None, priority=600, label="", source="json"):
            start_text = str(start or "0").strip()
            end_text = str(end or "23").strip()
            start_hour = int((start_text.split(":", 1)[0] if ":" in start_text else start_text) or 0)
            end_hour = int((end_text.split(":", 1)[0] if ":" in end_text else end_text) or 23)
            if ":" in end_text:
                try:
                    end_minute = int(end_text.split(":", 1)[1] or 0)
                except Exception:
                    end_minute = 0
                if end_minute > 0:
                    end_hour = min(24, end_hour + 1)
            super(NPCHourScheduleEntry, self).__init__(location, weekdays, [], start_hour, end_hour, awake, talkable, False, condition, priority, label)
            self.npc_id = str(npc_id or "").strip()
            self.location_choices = list(location_choices or [])
            self.source = str(source or "json")

        def selected_location(self):
            choices = []
            for row in list(self.location_choices or []):
                data = dict(row or {})
                loc = str(data.get("location", "") or "").strip()
                if not loc:
                    continue
                probability = float(data.get("probability", data.get("weight", 1.0)) or 0.0)
                if probability > 0:
                    choices.append({"location": loc, "probability": probability})
            if not choices:
                return str(self.location or "")
            total_probability = sum([max(0.0, float(row.get("probability", 0.0) or 0.0)) for row in choices])
            if total_probability <= 0:
                return ""
            scale = 10000
            if total_probability <= 1.000001:
                roll = procedural_randint(1, scale, "npc_hour_%s_%s_%s_%s" % (self.npc_id, self.label, calendar_v2.daysInGame, self.start_hour))
                cursor = 0
                for row in choices:
                    cursor += int(round(max(0.0, float(row.get("probability", 0.0) or 0.0)) * scale))
                    if roll <= cursor:
                        return str(row.get("location", "") or "")
                return ""
            roll = procedural_randint(1, int(round(total_probability * scale)), "npc_hour_%s_%s_%s_%s" % (self.npc_id, self.label, calendar_v2.daysInGame, self.start_hour))
            cursor = 0
            for row in choices:
                cursor += int(round(max(0.0, float(row.get("probability", 0.0) or 0.0)) * scale))
                if roll <= cursor:
                    return str(row.get("location", "") or "")
            return str(choices[-1].get("location", "") or "")

        def matches(self, weekday_value=None, time_value=None):
            week_value = int(week if weekday_value is None else weekday_value or 0)
            if self.weekdays and week_value not in self.weekdays:
                return False
            hour_value = int(calendar_v2.hour if time_value is None else time_value or 0) % 24
            if self.start_hour <= self.end_hour:
                if not (self.start_hour <= hour_value < self.end_hour):
                    return False
            else:
                if not (hour_value >= self.start_hour or hour_value < self.end_hour):
                    return False
            if not str(self.selected_location() or "").strip():
                return False
            return room_rule_true(self.condition)

    def npc_daily_schedule_slot(slot=0, location="", awake=True, talkable=True, label="", priority=500):
        return {"slot": int(slot or 0), "location": str(location or "").strip(), "awake": bool(awake), "talkable": bool(talkable), "label": str(label or "").strip(), "priority": int(priority or 500)}

    def npc_daily_schedule_choice(location="", weight=1, awake=True, talkable=True, label="", condition=None, monthly_key="", monthly_limit=0):
        return {"location": str(location or "").strip(), "weight": max(0, int(weight or 0)), "awake": bool(awake), "talkable": bool(talkable), "label": str(label or "").strip(), "condition": condition, "monthly_key": str(monthly_key or "").strip(), "monthly_limit": int(monthly_limit or 0)}

    def npc_daily_schedule_random_slot(slot=0, choices=None, weekdays=None, label="", priority=500):
        return {"slot": int(slot or 0), "choices": list(choices or []), "weekdays": list(weekdays or []), "label": str(label or "").strip(), "priority": int(priority or 500)}

    class PeopleData(object):
        def __init__(self, name, cname="", fullname="", genitive="", dative="",
                    topics=None, portrait="", birth_date=None,
                    default_location="", description="", schedule_entries=None,
                    gift_preferences=None):
            self.name = people_normalize_id(name)
            self.cname = str(cname or fullname or self.name)
            self.fullname = str(fullname or cname or self.name)
            self.genitive = str(genitive or self.fullname)
            self.dative = str(dative or self.fullname)
            self.topics = list(topics or [])
            self.portrait = str(portrait or "")
            self.birth_date = dict(birth_date or {})
            self.default_location = str(default_location or "")
            self.description = str(description or "")
            self.schedule_entries = list(schedule_entries or [])
            self.daily_schedule_template = {"default_slots": [], "random_slots": []}
            self.daily_schedule_plan_day = -1
            self.daily_schedule_plan = []
            self.schedule_monthly_counters = {}
            self.schedule_monthly_counters = {}
            self.schedule_monthly_counters = {}
            self.schedule_monthly_counters = {}
            self.schedule_monthly_counters = {}
            self.schedule_monthly_counters = {}
            self.interval_schedule_entries = []
            self.interval_schedule_loaded = False
            self.interval_schedule_load_error = ""
            self.gift_preferences = list(gift_preferences or [])

        def age_years(self):
            if not self.birth_date:
                return 0
            birth_cycle = people_to_int(self.birth_date.get("cycle", 0), 0)
            if birth_cycle <= 0:
                return 0
            current_cycle = people_to_int(getattr(calendar_v2, "cycle", year), year)
            age_value = current_cycle - birth_cycle
            birth_period = people_to_int(self.birth_date.get("period", 1), 1)
            birth_day = people_to_int(self.birth_date.get("day", 1), 1)
            current_period = people_to_int(getattr(calendar_v2, "period", month), month)
            current_day = people_to_int(getattr(calendar_v2, "day", day), day)
            if (current_period, current_day) < (birth_period, birth_day):
                age_value -= 1
            return max(0, age_value)

        def getLocation(self, wday=None, hour=None):
            entry = self.schedule_resolve(wday, hour)
            if entry is not None:
                return str(entry.selected_location() if hasattr(entry, "selected_location") else getattr(entry, "location", "") or "")
            if self.interval_schedule_loaded and self.interval_schedule_entries:
                return ""
            return str(self.default_location or people_initial_location(self.name) or "")

        def set_schedule(self, entries=None):
            self.schedule_entries = list(entries or [])
            return self.schedule_entries

        def add_schedule_entry(self, entry=None):
            if entry is not None:
                self.schedule_entries.append(entry)
            return self.schedule_entries

        def set_daily_schedule(self, default_slots=None, random_slots=None):
            self.daily_schedule_template = {
                "default_slots": list(default_slots or []),
                "random_slots": list(random_slots or []),
            }
            self.daily_schedule_plan_day = -1
            self.daily_schedule_plan = []
            return self.daily_schedule_template

        def daily_schedule_choice_allowed(self, choice):
            row = dict(choice or {})
            if not str(row.get("location", "") or "").strip():
                return False
            condition = row.get("condition", None)
            if condition is not None and not room_rule_true(condition):
                return False
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if monthly_key and monthly_limit > 0:
                current_month = int(year or 0) * 100 + int(month or 0)
                row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
                if int(row_count.get("month", -1) or -1) != current_month:
                    row_count = {"month": current_month, "count": 0}
                if int(row_count.get("count", 0) or 0) >= monthly_limit:
                    return False
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if monthly_key and monthly_limit > 0:
                current_month = int(year or 0) * 100 + int(month or 0)
                row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
                if int(row_count.get("month", -1) or -1) != current_month:
                    row_count = {"month": current_month, "count": 0}
                    self.schedule_monthly_counters[monthly_key] = row_count
                if int(row_count.get("count", 0) or 0) >= monthly_limit:
                    return False
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if monthly_key and monthly_limit > 0:
                current_month = int(year or 0) * 100 + int(month or 0)
                row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
                if int(row_count.get("month", -1) or -1) != current_month:
                    row_count = {"month": current_month, "count": 0}
                    self.schedule_monthly_counters[monthly_key] = row_count
                if int(row_count.get("count", 0) or 0) >= monthly_limit:
                    return False
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if monthly_key and monthly_limit > 0:
                current_month = int(year or 0) * 100 + int(month or 0)
                row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
                if int(row_count.get("month", -1) or -1) != current_month:
                    row_count = {"month": current_month, "count": 0}
                    self.schedule_monthly_counters[monthly_key] = row_count
                if int(row_count.get("count", 0) or 0) >= monthly_limit:
                    return False
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if monthly_key and monthly_limit > 0:
                current_month = int(year or 0) * 100 + int(month or 0)
                row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
                if int(row_count.get("month", -1) or -1) != current_month:
                    row_count = {"month": current_month, "count": 0}
                    self.schedule_monthly_counters[monthly_key] = row_count
                if int(row_count.get("count", 0) or 0) >= monthly_limit:
                    return False
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if monthly_key and monthly_limit > 0:
                current_month = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
                row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
                if int(row_count.get("month", -1) or -1) != current_month:
                    row_count = {"month": current_month, "count": 0}
                    self.schedule_monthly_counters[monthly_key] = row_count
                if int(row_count.get("count", 0) or 0) >= monthly_limit:
                    return False
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if monthly_key and monthly_limit > 0:
                current_month = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
                row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
                if int(row_count.get("month", -1) or -1) != current_month:
                    row_count = {"month": current_month, "count": 0}
                if int(row_count.get("count", 0) or 0) >= monthly_limit:
                    return False
            return True

        def daily_schedule_mark_choice(self, choice):
            row = dict(choice or {})
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if not monthly_key or monthly_limit <= 0:
                return
            current_month = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
            row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
            row_count["month"] = current_month
            row_count["count"] = int(row_count.get("count", 0) or 0) + 1
            self.schedule_monthly_counters[monthly_key] = row_count

        def daily_schedule_mark_choice(self, choice):
            row = dict(choice or {})
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if not monthly_key or monthly_limit <= 0:
                return
            current_month = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
            row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
            row_count["month"] = current_month
            row_count["count"] = int(row_count.get("count", 0) or 0) + 1
            self.schedule_monthly_counters[monthly_key] = row_count

        def daily_schedule_mark_choice(self, choice):
            row = dict(choice or {})
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if not monthly_key or monthly_limit <= 0:
                return
            current_month = int(year or 0) * 100 + int(month or 0)
            row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
            row_count["month"] = current_month
            row_count["count"] = int(row_count.get("count", 0) or 0) + 1
            self.schedule_monthly_counters[monthly_key] = row_count

        def daily_schedule_mark_choice(self, choice):
            row = dict(choice or {})
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if not monthly_key or monthly_limit <= 0:
                return
            current_month = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
            row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
            row_count["month"] = current_month
            row_count["count"] = int(row_count.get("count", 0) or 0) + 1
            self.schedule_monthly_counters[monthly_key] = row_count

        def daily_schedule_mark_choice(self, choice):
            row = dict(choice or {})
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if not monthly_key or monthly_limit <= 0:
                return
            current_month = int(year or 0) * 100 + int(month or 0)
            row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
            row_count["month"] = current_month
            row_count["count"] = int(row_count.get("count", 0) or 0) + 1
            self.schedule_monthly_counters[monthly_key] = row_count

        def daily_schedule_mark_choice(self, choice):
            row = dict(choice or {})
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if not monthly_key or monthly_limit <= 0:
                return
            current_month = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
            row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
            row_count["month"] = current_month
            row_count["count"] = int(row_count.get("count", 0) or 0) + 1
            self.schedule_monthly_counters[monthly_key] = row_count

        def daily_schedule_mark_choice(self, choice):
            row = dict(choice or {})
            monthly_key = str(row.get("monthly_key", "") or "").strip()
            monthly_limit = int(row.get("monthly_limit", 0) or 0)
            if not monthly_key or monthly_limit <= 0:
                return
            current_month = int(year or 0) * 100 + int(month or 0)
            row_count = dict(self.schedule_monthly_counters.get(monthly_key, {}) or {})
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
            row_count["month"] = current_month
            row_count["count"] = int(row_count.get("count", 0) or 0) + 1
            self.schedule_monthly_counters[monthly_key] = row_count

        def daily_schedule_pick_choice(self, choices):
            allowed = [dict(choice or {}) for choice in list(choices or []) if self.daily_schedule_choice_allowed(choice)]
            if not allowed:
                return None
            total_weight = sum([max(0, int(row.get("weight", 1) or 1)) for row in allowed])
            if total_weight <= 0:
                return allowed[0]
            roll = procedural_randint(1, total_weight, "daily_schedule_%s_%s_%s" % (self.name, int(calendar_v2.daysInGame or 0), total_weight))
            cursor = 0
            for row in allowed:
                cursor += max(0, int(row.get("weight", 1) or 1))
                if roll <= cursor:
                    self.daily_schedule_mark_choice(row)
                    return row
            self.daily_schedule_mark_choice(allowed[-1])
            return allowed[-1]

        def daily_schedule_entry_from_row(self, row, slot_value=None):
            data = dict(row or {})
            slot = int(data.get("slot", slot_value if slot_value is not None else 0) or 0)
            return NPCScheduleEntry(
                location=str(data.get("location", "") or ""),
                weekdays=[int(week or 0)],
                time_slots=[slot],
                awake=bool(data.get("awake", True)),
                talkable=bool(data.get("talkable", True)),
                priority=int(data.get("priority", 500) or 500),
                label=str(data.get("label", "") or ""),
            )

        def daily_schedule_build(self, force=False, weekday_value=None):
            day_value = int(calendar_v2.daysInGame or 0)
            if not force and int(self.daily_schedule_plan_day or -1) == day_value:
                return list(self.daily_schedule_plan or [])
            template = dict(self.daily_schedule_template or {})
            week_value = int(week if weekday_value is None else weekday_value or 0)
            slot_rows = {}
            for row in list(template.get("default_slots", []) or []):
                data = dict(row or {})
                weekdays = list(data.get("weekdays", []) or [])
                if weekdays and week_value not in weekdays:
                    continue
                condition = data.get("condition", None)
                if condition is not None and not room_rule_true(condition):
                    continue
                slot_rows[int(data.get("slot", 0) or 0)] = data
            for random_row in list(template.get("random_slots", []) or []):
                data = dict(random_row or {})
                weekdays = list(data.get("weekdays", []) or [])
                if weekdays and week_value not in weekdays:
                    continue
                choice = self.daily_schedule_pick_choice(data.get("choices", []))
                if choice is None:
                    continue
                slot = int(data.get("slot", 0) or 0)
                choice["slot"] = slot
                choice["priority"] = int(data.get("priority", 500) or 500)
                slot_rows[slot] = choice
            self.daily_schedule_plan = [self.daily_schedule_entry_from_row(slot_rows[row], row) for row in sorted(slot_rows.keys())]
            self.daily_schedule_plan_day = day_value
            return list(self.daily_schedule_plan or [])

        def interval_location_choices_from_json(self, data):
            raw_location = data.get("location", "")
            probabilities = data.get("location_probabilities", data.get("location probability", data.get("locaation probability", [])))
            try:
                probability_rows = list(probabilities or [])
            except Exception:
                probability_rows = []
            if isinstance(raw_location, str):
                raw_locations = [raw_location] if probability_rows else []
            else:
                raw_locations = list(raw_location or [])
            if not raw_locations:
                return []
            fallback_probability = 1.0 / len(raw_locations)
            choices = []
            for index, loc in enumerate(raw_locations):
                try:
                    probability = float(probability_rows[index])
                except Exception:
                    probability = fallback_probability
                choices.append({"location": str(loc or "").strip(), "probability": probability})
            return choices

        def interval_schedule_entry_from_json(self, row):
            data = dict(row or {})
            location_choices = self.interval_location_choices_from_json(data)
            raw_location = data.get("location", "")
            return NPCHourScheduleEntry(
                npc_id=self.name,
                location="" if location_choices else str(raw_location or ""),
                location_choices=location_choices,
                weekdays=list(data.get("weekdays", []) or []),
                start=str(data.get("start", "00:00") or "00:00"),
                end=str(data.get("end", "23:59") or "23:59"),
                awake=bool(data.get("awake", True)),
                talkable=bool(data.get("talkable", True)),
                condition=data.get("condition", None),
                priority=int(data.get("priority", 600) or 600),
                label=str(data.get("label", "") or ""),
                source=str(data.get("source", "json") or "json"),
            )

        def load_interval_schedule(self, force=False):
            if self.interval_schedule_loaded and not force:
                return list(self.interval_schedule_entries or [])
            self.interval_schedule_entries = []
            self.interval_schedule_load_error = ""
            path = str(getattr(self, "schedule_source", "") or "").strip()
            if not path:
                path = "NPC/Schedules/%s.json" % self.name
            if path.startswith("schedules/"):
                path = "NPC/Schedules/" + path.split("/", 1)[1]
            if not renpy.loadable(path):
                self.interval_schedule_loaded = True
                return []
            try:
                raw = renpy.file(path).read()
                if hasattr(raw, "decode"):
                    raw = raw.decode("utf-8")
                payload = json.loads(raw)
                rows = []
                for row in list(dict(payload or {}).get("entries", []) or []):
                    entry = self.interval_schedule_entry_from_json(row)
                    if entry.location or entry.location_choices:
                        rows.append(entry)
                self.interval_schedule_entries = rows
            except Exception as ex:
                self.interval_schedule_load_error = "%s: %s" % (path, ex)
                self.interval_schedule_entries = previous_entries
                self.interval_schedule_entries = previous_entries
                self.interval_schedule_entries = previous_entries
                self.interval_schedule_entries = previous_entries
            self.interval_schedule_loaded = True
            return list(self.interval_schedule_entries or [])

        def schedule_entries_for_today(self):
            interval_entries = self.load_interval_schedule(False)
            return list(interval_entries or []) + list(self.daily_schedule_build(False) or []) + list(self.schedule_entries or [])

        def schedule_resolve(self, weekday_value=None, time_value=None):
            entries = sorted(self.schedule_entries_for_today(), key=lambda row: int(getattr(row, "priority", 0) or 0), reverse=True)
            for entry in entries:
                if entry.matches(weekday_value, time_value):
                    return entry
            return None

        def schedule_state(self, weekday_value=None, time_value=None):
            entry = self.schedule_resolve(weekday_value, time_value)
            if entry is None:
                return {"location": "", "awake": True, "talkable": True, "venue_open_required": False, "label": "", "interval": "", "source": ""}
            if getattr(entry, "start_hour", None) is not None and getattr(entry, "end_hour", None) is not None:
                interval_text = "%02d-%02d" % (int(getattr(entry, "start_hour", 0) or 0), int(getattr(entry, "end_hour", 0) or 0))
            else:
                interval_text = ",".join([str(row) for row in list(getattr(entry, "time_slots", []) or [])])
            return {
                "location": str(entry.selected_location() if hasattr(entry, "selected_location") else getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "venue_open_required": bool(getattr(entry, "venue_open_required", False)),
                "label": str(getattr(entry, "label", "") or ""),
                "interval": interval_text,
                "source": str(getattr(entry, "source", "rpy") or "rpy"),
            }

        def isInLocation(self, location, wday=None, hour=None):
            return str(self.getLocation(wday, hour) or "") == str(location or "")

        def selectIcon(self, wday=None, hour=None):
            candidate = str(self.portrait or "")
            if candidate:
                try:
                    if renpy.loadable(candidate):
                        return candidate
                except Exception:
                    return candidate
            try:
                portrait = str(girl_card_portrait_path(self.name) or "")
                if portrait and renpy.loadable(portrait):
                    return portrait
            except Exception:
                pass
            return str(self.portrait or "")

        @classmethod
        def from_dict(cls, name, payload):
            row = dict(payload or {})
            row.setdefault("name", name)
            return cls(**row)

    def people_schedule_data(npc_id=""):
        key = people_normalize_id(npc_id)
        if not key:
            return None
        data = peopleData.get(key, None)
        if data is not None:
            return data
        info = peopleInfo.get(key, None)
        if info is not None:
            data = getattr(info, "data", None)
            if data is not None:
                return data
        return None

    def npc_schedule_set(npc_id="", entries=None):
        data = people_schedule_data(npc_id)
        if data is not None:
            data.set_schedule(entries)

    def npc_schedule_add(npc_id="", entry=None):
        data = people_schedule_data(npc_id)
        if data is not None:
            data.add_schedule_entry(entry)

    def npc_schedule_list(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.schedule_entries or [])

    def npc_daily_schedule_set(npc_id="", default_slots=None, random_slots=None):
        data = people_schedule_data(npc_id)
        if data is not None:
            data.set_daily_schedule(default_slots, random_slots)

    def npc_daily_schedule_invalidate(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is not None:
            data.invalidate_daily_schedule()

    def npc_daily_schedule_invalidate_all():
        for data in list(peopleData.values()):
            if data is not None:
                data.invalidate_daily_schedule()

    def npc_interval_schedule_load_file(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return False
        before = len(list(data.interval_schedule_entries or []))
        rows = data.load_interval_schedule(True)
        return len(rows) > 0 or before > 0

    def npc_interval_schedule_load_all(force=False):
        for data in list(peopleData.values()):
            if data is not None:
                data.load_interval_schedule(force)

    def npc_interval_schedule_list(npc_id=""):
        data = people_schedule_data(npc_id)
        if data is None:
            return []
        return list(data.load_interval_schedule(False) or [])

    def npc_interval_schedule_has_contract(npc_id=""):
        return len(npc_interval_schedule_list(npc_id)) > 0

    def npc_schedule_resolve(npc_id="", weekday_value=None, time_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return None
        return data.schedule_resolve(weekday_value, time_value)

    def npc_schedule_location(npc_id="", weekday_value=None, time_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return ""
        return data.getLocation(weekday_value, time_value)

    def npc_is_awake(npc_id="", weekday_value=None, time_value=None):
        entry = npc_schedule_resolve(npc_id, weekday_value, time_value)
        if entry is None:
            return True
        return bool(getattr(entry, "awake", True))

    def npc_can_talk_now(npc_id="", weekday_value=None, time_value=None):
        entry = npc_schedule_resolve(npc_id, weekday_value, time_value)
        if entry is None:
            return True
        return bool(getattr(entry, "awake", True)) and bool(getattr(entry, "talkable", True))

    def npc_schedule_state(npc_id="", weekday_value=None, time_value=None):
        data = people_schedule_data(npc_id)
        if data is None:
            return {"location": "", "awake": True, "talkable": True, "venue_open_required": False, "label": "", "interval": "", "source": ""}
        return data.schedule_state(weekday_value, time_value)

    def _npc_display_name(npc_id=""):
        key = people_normalize_id(npc_id)
        if not key:
            return ""
        info = peopleInfo.get(key, None)
        if info is None:
            return key
        return str(info.display_name() or key)

    def getLocation(person="", weekday_value=None, time_value=None):
        key = people_normalize_id(person)
        if not key:
            return ""
        info = peopleInfo.get(key, None)
        if info is None:
            return ""
        return str(info.getLocation(weekday_value, time_value) or "")

    def getNPCids(location="", weekday_value=None, time_value=None):
        room_key = str(location or "").strip()
        if not room_key:
            return []
        present = []
        for npc_id, info in peopleInfo.items():
            npc_key = people_normalize_id(npc_id)
            if npc_key and info is not None and str(info.getLocation(weekday_value, time_value) or "") == room_key:
                present.append(npc_key)
        return sorted(present, key=lambda row: _npc_display_name(row).lower())

    def getNPCnames(location="", weekday_value=None, time_value=None):
        return [_npc_display_name(npc_id) for npc_id in getNPCids(location, weekday_value, time_value)]

    def isLocationEmpty(location="", weekday_value=None, time_value=None):
        return len(getNPCids(location, weekday_value, time_value)) <= 0

    def tavern_team_default_schedule_entries(work_location="TavernMain", sleep_location="TavernMyRoom", weekend_location="TavernMain"):
        return [
            NPCScheduleEntry(location=work_location, weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, priority=100, label="morning"),
            NPCScheduleEntry(location=work_location, weekdays=[1, 2, 3, 4, 5, 6], time_slots=[1, 2], awake=True, talkable=True, priority=100, label="working_day"),
            NPCScheduleEntry(location=work_location, weekdays=[1, 2, 3, 4, 6], time_slots=[3], awake=True, talkable=True, priority=90, label="late_evening"),
            NPCScheduleEntry(location=weekend_location, weekdays=[7], time_slots=[0, 1, 2, 3], awake=True, talkable=True, priority=80, label="sunday"),
            NPCScheduleEntry(location=sleep_location, weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
        ]

    class PeopleInfo(object):
        def __init__(self, name, rel=0, talkToday=None, flirtToday=False, giftToday=False,
                    gifts=None, var=None, unknown_name=""):
            self.name = people_normalize_id(name)
            self.rel = people_to_int(rel, 0)
            self.talkToday = set(talkToday or [])
            self.gifts = set(gifts or [])
            self.flirtToday = False
            self.giftToday = False
            self.flirtToday = False
            self.giftToday = False
            self.flirtToday = False
            self.giftToday = False
            self.talked_today = 0
            self.flirtToday = people_to_bool(flirtToday, False)
            self.giftToday = people_to_bool(giftToday, False)
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.openness = 0
            self.corruption = 0
            self.known = False
            self.unknown_name = str(unknown_name or getattr(self.__class__, "unknown_name", "") or "")
            self.location = ""
            self.data = None
            self.var = var if var is not None else {}
            self.sex_state = {}
            # Hidden per-girl lunar fertility dict (for Amanda, Melissa, Clara, Sandra)
            self.lunar_fertility = {"offset": 0, "last_phase": 0, "strength": 1.0}
            # Hidden per-girl lunar fertility dict (for Amanda, Melissa, Clara, Sandra)
            self.lunar_fertility = {"offset": 0, "last_phase": 0, "strength": 1.0}
            # Hidden per-girl lunar fertility dict (for Amanda, Melissa, Clara, Sandra)
            self.lunar_fertility = {"offset": 0, "last_phase": 0, "strength": 1.0}

        def update(self):
            self.name = people_normalize_id(self.name)
            if not getattr(self, "unknown_name", ""):
                self.unknown_name = str(getattr(self.__class__, "unknown_name", "") or "")
            if isinstance(peopleData, dict) and self.name in peopleData:
                self.data = peopleData[self.name]
            elif self.data is None:
                self.data = PeopleData(self.name)
            self.flirtToday = people_to_int(getattr(self, "flirted_today", 0), 0) > 0
            self.giftToday = people_to_int(getattr(self, "gifted_today", 0), 0) > 0
            return self

        def mark_talked(self, amount=1):
            value = people_to_int(amount, 1)
            self.talked_today = people_to_int(getattr(self, "talked_today", 0), 0) + value
            return self

        def mark_asked(self, amount=1):
            value = people_to_int(amount, 1)
            self.asked_today = people_to_int(getattr(self, "asked_today", 0), 0) + value
            return self

        def mark_fucked(self, amount=1):
            value = people_to_int(amount, 1)
            self.fucked_today = people_to_int(getattr(self, "fucked_today", 0), 0) + value
            return self

        def ensure_sex_state(self):
            if not isinstance(getattr(self, "sex_state", None), dict):
                self.sex_state = {}
            self.sex_state.setdefault("arousal", 0)
            self.sex_state.setdefault("somebody_cums", 0)
            self.sex_state.setdefault("cock_position", "none")
            self.sex_state.setdefault("partner_positions", {})
            self.sex_state.setdefault("cum_inside_you", 0)
            self.sex_state.setdefault("cum_face_you", 0)
            self.sex_state.setdefault("cum_tits_you", 0)
            self.sex_state.setdefault("cum_mouth_you", 0)
            self.sex_state.setdefault("cum_inside_others", 0)
            self.sex_state.setdefault("cum_face_others", 0)
            self.sex_state.setdefault("cum_tits_others", 0)
            self.sex_state.setdefault("cum_mouth_others", 0)
            return self.sex_state

        def set_cock_position(self, position="none", actor="You"):
            position_key = str(position or "none").strip().lower()
            if position_key not in ("none", "pussy", "mouth", "tits", "ass"):
                position_key = "none"
            actor_key = str(actor or "You").strip() or "You"
            state = self.sex_clothing_state()
            state["partner_positions"][actor_key] = position_key
            if actor_key.lower() == "you":
                state["cock_position"] = position_key
            return position_key

        def cock_position(self, actor="You"):
            actor_key = str(actor or "You").strip() or "You"
            state = self.sex_clothing_state()
            return str(state.get("partner_positions", {}).get(actor_key, state.get("cock_position", "none")) or "none")

        def cock_in(self, position="none", actor="You"):
            return self.cock_position(actor) == str(position or "none").strip().lower()

        def arousal_value(self):
            return people_clamp(self.ensure_sex_state().get("arousal", 0), 0, 100)

        def set_arousal(self, value):
            self.ensure_sex_state()["arousal"] = people_clamp(value, 0, 100)
            return self.sex_state["arousal"]

        def add_arousal(self, amount=0, cap=100):
            return self.set_arousal(min(people_to_int(cap, 100), self.arousal_value() + people_to_int(amount, 0)))

        def sex_busy(self):
            return people_to_int(self.ensure_sex_state().get("somebody_cums", 0), 0) != 0

        def set_sex_busy(self, value):
            self.ensure_sex_state()["somebody_cums"] = 1 if value else 0
            return self.sex_state["somebody_cums"]

        def cum_state(self, key):
            return people_to_int(self.ensure_sex_state().get(str(key or ""), 0), 0)

        def set_cum_state(self, key, value=1):
            state = self.sex_clothing_state()
            state[str(key or "")] = 1 if people_to_int(value, 0) else 0
            return state[str(key or "")]

        def clear_cum(self, *keys):
            state = self.ensure_sex_state()
            selected = list(keys or ())
            clear_all = not selected
            if not selected:
                selected = [
                    "cum_inside_you", "cum_face_you", "cum_tits_you", "cum_mouth_you",
                    "cum_inside_others", "cum_face_others", "cum_tits_others", "cum_mouth_others",
                ]
            for key in selected:
                state[str(key)] = 0
            if clear_all:
                self.set_cock_position("none")
            return state

        def current_underwear(self, key, default=""):
            wardrobe = getattr(self, "wardrobe", {}) or {}
            underwear = wardrobe.get("current_underwear", {}) if isinstance(wardrobe, dict) else {}
            if not isinstance(underwear, dict):
                return default
            return str(underwear.get(str(key or ""), default) or "")

        def has_panties(self):
            return self.current_underwear("panties", "") != ""

        def set_current_underwear(self, key, value=""):
            if not isinstance(getattr(self, "wardrobe", None), dict):
                self.wardrobe = {}
            underwear = self.wardrobe.setdefault("current_underwear", {})
            if not isinstance(underwear, dict):
                underwear = {}
                self.wardrobe["current_underwear"] = underwear
            underwear[str(key or "")] = str(value or "")
            return underwear[str(key or "")]

        def job_value(self, key, default=0):
            jobs = getattr(self, "jobs", {})
            if not isinstance(jobs, dict):
                return default
            return jobs.get(str(key or ""), default)

        def set_job_value(self, key, value=0):
            if not isinstance(getattr(self, "jobs", None), dict):
                self.jobs = {}
            self.jobs[str(key or "")] = value
            return value

        def reset_skill_gains(self):
            self.skill_gains_today = {}
            return self.skill_gains_today

        def record_skill_gain(self, key, amount=1):
            if not isinstance(getattr(self, "skill_gains_today", None), dict):
                self.skill_gains_today = {}
            skill_key = str(key or "")
            self.skill_gains_today[skill_key] = people_to_int(self.skill_gains_today.get(skill_key, 0), 0) + people_to_int(amount, 1)
            return self.skill_gains_today[skill_key]

        def sex_stat(self, key, default=0):
            stats = getattr(self, "stats", None)
            if not isinstance(stats, dict):
                self.stats = {}
                stats = self.stats
            return stats.get(str(key or ""), default)

        def set_sex_stat(self, key, value):
            if not isinstance(getattr(self, "stats", None), dict):
                self.stats = {}
            self.stats[str(key or "")] = value
            return value

        def add_sex_stat(self, key, amount=1):
            current = people_to_int(self.sex_stat(key, 0), 0)
            return self.set_sex_stat(key, current + people_to_int(amount, 1))

        def pregnancy_days(self):
            return people_to_int(self.sex_stat("pregnancy", 0), 0)

        def record_orgasm_given(self):
            count = self.add_sex_stat("orgasms_given", 1)
            self.set_sex_stat("last_orgasm_day", people_to_int(calendar_v2.daysInGame, 0))
            return count

        def record_sex_history(self, partner="You", place="", cum_target="", day_value=None):
            if not isinstance(getattr(self, "detailed_sex_history", None), list):
                self.detailed_sex_history = []
            day = people_to_int(day_value if day_value is not None else calendar_v2.daysInGame, 0)
            row = {
                "day": day,
                "partner": str(partner or ""),
                "place": str(place or ""),
                "cum_target": str(cum_target or ""),
            }
            self.detailed_sex_history.append(row)
            return row

        def player_cum(self, place="outside"):
            place_key = str(place or "outside").strip().lower()
            if place_key not in ("inside", "mouth", "tits", "face"):
                place_key = "outside"
            state = self.ensure_sex_state()
            try:
                intimacy = player.intimacy
                intimacy.record_cum(calendar_v2.daysInGame)
            except Exception:
                pass
            self.add_sex_stat("sexacts", 1)
            self.mark_fucked(1)
            if place_key == "inside":
                state["cum_inside_you"] = 1
                self.add_sex_stat("cuminside", 1)
                if self.pregnancy_days() == 0:
                    chance = min(800, people_to_int(self.sex_stat("ConceptionChance", 0), 0) * 3)
                    if chance > 0 and procedural_randint(1, 1000, "pregnancy_%s_%s" % (self.code_name, people_to_int(calendar_v2.daysInGame, 0))) <= chance:
                        self.set_sex_stat("pregnancy", 1)
                        self.set_sex_stat("pregfather", "Вы")
            elif place_key == "mouth":
                state["cum_mouth_you"] = 1
            elif place_key == "tits":
                state["cum_tits_you"] = 1
            elif place_key == "face":
                state["cum_face_you"] = 1
            self.record_sex_history("You", str(state.get("location", "") or ""), place_key)
            self.set_cock_position("none")
            self.set_sex_busy(True)
            return state

        def change_social(self, friend_delta=0, open_delta=0, corruption_delta=0):
            relationship_cap = max(20, people_to_int(getattr(self, "relationship_cap", 20), 20))
            self.rel = max(0, min(relationship_cap, people_to_int(getattr(self, "rel", 0), 0) + people_to_int(friend_delta, 0)))
            if hasattr(self, "relationship"):
            if hasattr(self, "relationship"):
            if hasattr(self, "relationship"):
            if hasattr(self, "relationship"):
            if hasattr(self, "relationship"):
            self.openness = max(0, min(20, people_to_int(getattr(self, "openness", 0), 0) + people_to_int(open_delta, 0)))
            self.corruption = max(0, min(100, people_to_int(getattr(self, "corruption", 0), 0) + people_to_int(corruption_delta, 0)))
            return self

        def apply_social_chance(self, friend_limit=0, friend_chance=0, friend_delta=0, corruption_limit=0, corruption_chance=0, corruption_delta=0, reason="social"):
            friend_delta = people_to_int(friend_delta, 0)
            corruption_delta = people_to_int(corruption_delta, 0)
            friend_limit = people_to_int(friend_limit, 0)
            corruption_limit = people_to_int(corruption_limit, 0)
            friend_chance = max(0, people_to_int(friend_chance, 0))
            corruption_chance = max(0, people_to_int(corruption_chance, 0))
            if friend_delta != 0 and self.rel < friend_limit and (friend_chance <= 1 or procedural_randint(1, friend_chance, key="procedural:Utilities/General/NPC/PeopleRuntime.rpy:procedural_randint:888:1") == 1):
                self.change_social(friend_delta=friend_delta)
            if corruption_delta != 0 and self.corruption < corruption_limit and (corruption_chance <= 1 or procedural_randint(1, corruption_chance, key="procedural:Utilities/General/NPC/PeopleRuntime.rpy:procedural_randint:890:2") == 1):
                self.change_social(corruption_delta=corruption_delta)
            if friend_delta > 0 or corruption_delta > 0:
                self.change_mana(1, reason)
            elif friend_delta < 0 or corruption_delta < 0:
                self.change_mana(-1, reason)
            return {"rel": self.rel, "corruption": self.corruption, "mana": self.mana}

        def change_rebellion(self, amount=0, reason=""):
            self.player.stats.rebellion = max(0, min(100, people_to_int(getattr(self, "rebellion", 0), 0) + people_to_int(amount, 0)))
            if isinstance(getattr(self, "reaction_state", None), dict):
                self.reaction_state["last_rebellion_reason"] = str(reason or "")
            return self.player.stats.rebellion

        def change_anger(self, amount=0, reason=""):
            self.anger_with_player = max(0, min(100, people_to_int(getattr(self, "anger_with_player", 0), 0) + people_to_int(amount, 0)))
            if isinstance(getattr(self, "reaction_state", None), dict):
                self.reaction_state["last_anger_reason"] = str(reason or "")
            return self.anger_with_player

        def change_fear(self, amount=0, reason=""):
            self.fear = max(0, min(100, people_to_int(getattr(self, "fear", 0), 0) + people_to_int(amount, 0)))
            if isinstance(getattr(self, "reaction_state", None), dict):
                self.reaction_state["last_fear_reason"] = str(reason or "")
            return self.fear

        def change_mana(self, amount=0, reason=""):
            before = people_to_int(getattr(self, "mana", 0), 0)
            self.mana = max(0, min(100, before + people_to_int(amount, 0)))
            if isinstance(getattr(self, "reaction_state", None), dict):
                self.reaction_state["last_mana_delta"] = self.mana - before
                self.reaction_state["last_mana_reasons"] = [str(reason or "")] if str(reason or "") else []
            return self.mana

        def mana_bad_probability(self):
            return max(0.0, min(1.0, 1.0 - (float(people_to_int(getattr(self, "mana", 0), 0)) / 100.0)))

        def reward_need_fulfilled(self, amount=1, reason="need_fulfilled"):
            return self.change_mana(abs(people_to_int(amount, 1)), reason)

        def punish_need_unfulfilled(self, amount=1, reason="need_unfulfilled"):
            return self.change_mana(-abs(people_to_int(amount, 1)), reason)

        def harass_instruction(self):
            if not isinstance(getattr(self, "var", None), dict):
                self.var = {}
            return str(self.var.get("harass_instruction", "") or "")

        def set_harass_instruction(self, value=""):
            if not isinstance(getattr(self, "var", None), dict):
                self.var = {}
            self.var["harass_instruction"] = str(value or "")
            return self.var["harass_instruction"]

        def reset_daily(self, full=False):
            """Reset per-girl daily interaction counters.
            Called from people_reset_daily_interactions() during sleep/NextDay.
            These flags conceptually belong to each girl (talked/flirted/gifted/asked/fucked her today),
            not as pure player-global state.
            """
            self.drunk = 0
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0

            if full:
                # Future: reset other daily per-girl state here if needed (e.g. some girl-specific today flags)
                pass

            return self

        def getLocation(self, wday=None, hour=None):
            try:
                if bool(TavernBreakfastEventActive) and TavernBreakfastPresentIds is not None:
                    breakfast_ids = [people_normalize_id(row) for row in list(TavernBreakfastPresentIds or [])]
                    if self.name in breakfast_ids:
                        return "TavernKitchen"
            authored_location = str(getattr(self, "location", "") or "").strip()
            if authored_location:
                return authored_location
            authored_location = str(getattr(self, "location", "") or "").strip()
            if authored_location:
                return authored_location
            authored_location = str(getattr(self, "location", "") or "").strip()
            if authored_location:
                return authored_location
            data_owner = getattr(self, "data", None)
                if data_owner is None:
                    return ""
                return str(data_owner.getLocation(wday, hour) or "")
            except Exception:
                return str(self.location or "")

        def isInLocation(self, location, wday=None, hour=None):
            return str(self.getLocation(wday, hour) or "") == str(location or "")

        def social_action_allowed(self, action="", item_id=""):
            action_key = str(action or "").strip().lower()
            if action_key in ("look", "talk"):
                return True
            try:
                allowed, reason = relationship_social_action_allowed(self.name, action_key, item_id)
                return bool(allowed)
            except Exception:
                return False

    class BaseNPC(PeopleInfo):
        """Base for all NPCs (secondaries + simple)."""
        def __init__(self, name, **kwargs):
            super().__init__(name, **kwargs)
            if not self.unknown_name:
                self.unknown_name = str(getattr(self.__class__, "unknown_name", "") or "")
            self.jobs = {}
            self.skills = {}
            self.clothing = {}
            self.body_state = {}
            self.sex_history = []
            self.story_flags = {}
            self.knows_mc = {}

        def promote_from_var(self, vardict=None):
            v = vardict if vardict is not None else self.var
            if not isinstance(v, dict):
                return self
            for key in list(v.keys()):
                if key.lower() in ("knowhim", "knowcomplaint", "mongolsafepass", "playerhandledrobin",
                                "missionupdatedbyplayer", "stocksreleased", "sawmomsex", "visitedhome",
                                "homesex", "eddiegeorg"):
                    self.story_flags[key] = v[key]
            if "napVars" in v and isinstance(v["napVars"], dict):
                self.story_flags.update(v["napVars"])
            return self
            self.clothing = {}
            self.body_state = {}
            self.sex_history = []
            self.story_flags = {}
            self.knows_mc = {}

        def promote_from_var(self, vardict=None):
            v = vardict if vardict is not None else self.var
            if not isinstance(v, dict):
                return self
            for key in list(v.keys()):
                if key.lower() in ("knowhim", "knowcomplaint", "mongolsafepass", "playerhandledrobin",
                                "missionupdatedbyplayer", "stocksreleased", "sawmomsex", "visitedhome",
                                "homesex", "eddiegeorg"):
                    self.story_flags[key] = v[key]
            if "napVars" in v and isinstance(v["napVars"], dict):
                self.story_flags.update(v["napVars"])
            return self
            self.clothing = {}
            self.body_state = {}
            self.sex_history = []
            self.story_flags = {}
            self.knows_mc = {}

        def promote_from_var(self, vardict=None):
            v = vardict if vardict is not None else self.var
            if not isinstance(v, dict):
                return self
            for key in list(v.keys()):
                if key.lower() in ("knowhim", "knowcomplaint", "mongolsafepass", "playerhandledrobin",
                                "missionupdatedbyplayer", "stocksreleased", "sawmomsex", "visitedhome",
                                "homesex", "eddiegeorg"):
                    self.story_flags[key] = v[key]
            if "napVars" in v and isinstance(v["napVars"], dict):
                self.story_flags.update(v["napVars"])
            return self

        def mark_known(self):
            self.known = True
            return True

        def display_name(self):
            if self.known:
                return str(people_display_name(self.name) or self.name)
            return str(getattr(self, "unknown_name", "") or self.name)

    class Girl(BaseNPC):
        """Girls with body layers, pregnancy, detailed history, lunar fertility."""
        def __init__(self, name, **kwargs):
            super().__init__(name, **kwargs)
            self.body_layers = {}
            self.insertion_state = {}
            self.clothing_layers = {}
            self.detailed_sex_history = []
            if not getattr(self, 'lunar_fertility', None):
                self.lunar_fertility = {"offset": hash(name) % 7, "last_phase": 0, "strength": 1.0}

        def sex_clothing_state(self):
            state = self.ensure_sex_state()
            state.setdefault("top_removed", 0)
            state.setdefault("bottom_removed", 0)
            state.setdefault("bra_removed", 0)
            state.setdefault("panties_removed", 0)
            state.setdefault("top_raised", 0)
            state.setdefault("bottom_raised", 0)
            state.setdefault("lick_pussy", 0)
            return state

        def current_dress(self):
            wardrobe = getattr(self, "wardrobe", {}) or {}
            if not isinstance(wardrobe, dict):
                return ""
            return str(wardrobe.get("current_dress", "") or "")

        def scene_dress(self):
            state = self.ensure_sex_state()
            if "dress_override" in state:
                return str(state.get("dress_override", "") or "")
            return self.current_dress()

        def scene_dress(self):
            state = self.ensure_sex_state()
            if "dress_override" in state:
                return str(state.get("dress_override", "") or "")
            return self.current_dress()

        def scene_dress(self):
            state = self.ensure_sex_state()
            if "dress_override" in state:
                return str(state.get("dress_override", "") or "")
            return self.current_dress()

        def scene_dress(self):
            state = self.ensure_sex_state()
            if "dress_override" in state:
                return str(state.get("dress_override", "") or "")
            return self.current_dress()

        def scene_dress(self):
            state = self.ensure_sex_state()
            if "dress_override" in state:
                return str(state.get("dress_override", "") or "")
            return self.current_dress()

        def scene_dress(self):
            state = self.ensure_sex_state()
            if "dress_override" in state:
                return str(state.get("dress_override", "") or "")
            return self.current_dress()

        def scene_dress(self):
            state = self.ensure_sex_state()
            if "dress_override" in state:
                return str(state.get("dress_override", "") or "")
            return self.current_dress()

        def clothing_layer(self, layer):
            layer_key = str(layer or "").strip().lower()
            state = self.sex_clothing_state()
            dress = self.current_dress()
            if layer_key == "top":
                if people_to_int(state.get("top_removed", 0), 0):
                    return ""
                return str(DressTopPart.get(dress, "") or "")
            if layer_key == "bottom":
                if people_to_int(state.get("bottom_removed", 0), 0):
                    return ""
                return str(DressBottomPart.get(dress, "") or "")
            if layer_key == "bra":
                if people_to_int(state.get("bra_removed", 0), 0):
                    return ""
                return self.current_underwear("bra", "")
            if layer_key == "panties":
                if people_to_int(state.get("panties_removed", 0), 0):
                    return ""
                return self.current_underwear("panties", "")
            return ""

        def clothing_slut(self, layer):
            return people_to_int(DressPartSlut.get(self.clothing_layer(layer), 0), 0)

        def layer_raised(self, layer):
            layer_key = str(layer or "").strip().lower()
            if layer_key not in ("top", "bottom"):
                return 0
            return people_to_int(self.sex_clothing_state().get("%s_raised" % layer_key, 0), 0)

        def set_layer_raised(self, layer, value=1):
            layer_key = str(layer or "").strip().lower()
            if layer_key not in ("top", "bottom"):
                return 0
            state = self.sex_clothing_state()
            state["%s_raised" % layer_key] = 1 if people_to_int(value, 0) else 0
            return state["%s_raised" % layer_key]

        def remove_clothing_layer(self, layer):
            layer_key = str(layer or "").strip().lower()
            if layer_key not in ("top", "bottom", "bra", "panties"):
                return ""
            removed = self.clothing_layer(layer_key)
            self.sex_clothing_state()["%s_removed" % layer_key] = 1
            return removed

        def reset_sex_clothing_state(self):
            state = self.sex_clothing_state()
            for key in ("top_removed", "bottom_removed", "bra_removed", "panties_removed", "top_raised", "bottom_raised"):
                state[key] = 0
            return self

        def tits_visible(self):
            return self.clothing_layer("bra") == "" and (self.clothing_layer("top") == "" or self.layer_raised("top"))

        def pussy_visible(self):
            return self.clothing_layer("panties") == "" and (self.clothing_layer("bottom") == "" or self.layer_raised("bottom"))

        def short_skirt_no_panties(self):
            return self.clothing_layer("panties") == "" and not self.layer_raised("bottom") and self.clothing_slut("bottom") >= 4

        def record_lick_pussy(self):
            state = self.sex_clothing_state()
            state["lick_pussy"] = people_to_int(state.get("lick_pussy", 0), 0) + 1
            return state["lick_pussy"]

        def lick_pussy_count(self):
            return people_to_int(self.sex_clothing_state().get("lick_pussy", 0), 0)

        def decision_profile(self):
            return build_girl_decision_profile(self.code_name)

        def decide(self, action_name="", profile=None, roll=None):
            result = girl_decide(self.code_name, action_name, profile, roll)
            self.record_reaction(action_name, str(dict(result or {}).get("reaction", "neutral") or "neutral"), None, result)
            return result

        def decision_good_probability(self, action_name="", profile=None):
            return girl_decision_good_probability(self.code_name, action_name, profile)

        def record_reaction(self, action_name="", reaction="", score=None, context=None):
            reaction_key = str(reaction or "neutral")
            score_value = people_to_int(score, girl_decision_reaction_score(reaction_key))
            if not isinstance(getattr(self, "reaction_state", None), dict):
                self.reaction_state = {}
            if not isinstance(getattr(self, "reaction_log", None), list):
                self.reaction_log = []
            self.reaction_state["last_reaction"] = reaction_key
            self.reaction_state["last_reaction_day"] = people_to_int(calendar_v2.daysInGame, 0)
            self.reaction_state["last_reaction_context"] = str(action_name or "")
            self.reaction_state["last_reaction_score"] = score_value
            self.reaction_state["pending_decision"] = ""
            self.reaction_log.append({
                "day": self.reaction_state["last_reaction_day"],
                "action": str(action_name or ""),
                "reaction": reaction_key,
                "score": score_value,
            })
            if len(self.reaction_log) > 20:
                self.reaction_log = self.reaction_log[-20:]
            return score_value

        def last_decision_reaction(self, action_name=""):
            action_key = str(action_name or "").strip().lower()
            if action_key:
                return dict(GirlDecisionLast.get("%s:%s" % (self.code_name, action_key), {}) or {})
            if isinstance(getattr(self, "reaction_log", None), list) and self.reaction_log:
                return dict(self.reaction_log[-1])
            return {}

        def apply_decision_reaction(self, decision=None, mana_reason="decision"):
            row = dict(decision or self.last_decision_reaction() or {})
            reaction = str(row.get("reaction", "neutral") or "neutral")
            action_name = str(row.get("action", "") or "")
            score = self.record_reaction(action_name, reaction, girl_decision_reaction_score(reaction), row)
            if score > 0:
                self.change_mana(1, mana_reason)
            elif score < 0:
                self.change_mana(-1, mana_reason)
            return score

    def _register_people_lists():
        """Fill girls / secondary_npcs from peopleInfo after registrations."""
        global girls, secondary_npcs
        if not isinstance(girls, list):
            girls = []
        if not isinstance(secondary_npcs, list):
            secondary_npcs = []
        try:
            pinfo = peopleInfo if isinstance(peopleInfo, dict) else {}
            girl_keys = set([people_normalize_id(row) for row in list(getattr(renpy.store, "AllGirlNames", []) or [])])
            secondary_keys = set([people_normalize_id(row) for row in list(getattr(renpy.store, "SECONDARY_NPC_KEYS", []) or [])])
            for key, info in pinfo.items():
                norm_key = people_normalize_id(key)
                if (norm_key in girl_keys or isinstance(info, Girl)) and info not in girls:
                    girls.append(info)
                elif (norm_key in secondary_keys or (isinstance(info, BaseNPC) and not isinstance(info, Girl))) and info not in secondary_npcs:
                    secondary_npcs.append(info)
        except Exception:
            pass
        return girls, secondary_npcs

# Normal init python for the remaining runtime helpers (classes + core helpers already defined early above in this same file).
init python:
    def people_known_ids_from_current_state():
        keys = set()
        if isinstance(peopleData, dict):
            keys.update([people_normalize_id(row) for row in list(peopleData.keys())])
        if isinstance(peopleInfo, dict):
            keys.update([people_normalize_id(row) for row in list(peopleInfo.keys())])
        try:
            keys.update([people_normalize_id(row) for row in list(AllGirlNames)])
        except Exception:
            pass
        return sorted([row for row in keys if row])

    def people_portrait_for(person):
        key = people_normalize_id(person)
        try:
            return str(girl_card_portrait_path(key) or "")
        except Exception:
            return ""

    def build_people_dataset_from_current_state():
        dataset = {}

        for person in people_known_ids_from_current_state():
            existing_data = peopleData.get(person, None) if isinstance(peopleData, dict) else None
            if isinstance(existing_data, PeopleData):
                dataset[person] = existing_data
                continue
            try:
                schedule_entries = npc_schedule_list(person)
            except Exception:
                schedule_entries = []
            dataset[person] = {
                "name": person,
                "cname": person,
                "fullname": person,
                "genitive": person,
                "dative": person,
                "portrait": people_portrait_for(person),
                "birth_date": {},
                "default_location": str(people_initial_location(person) or ""),
                "description": "",
                "schedule_entries": schedule_entries,
                "gift_preferences": [],
            }

        return dataset

    def loadPeopleData(idata=None):
        rows = idata if idata is not None else build_people_dataset_from_current_state()
        if isinstance(rows, dict) and "people" in rows:
            rows = rows.get("people", {})
        loaded = {}
        if isinstance(rows, dict):
            iterable = rows.items()
        else:
            iterable = [(row.get("name", ""), row) for row in list(rows or []) if isinstance(row, dict)]
        for name, payload in iterable:
            key = people_normalize_id(name)
            if not key:
                continue
            if isinstance(payload, PeopleData):
                payload.name = key
                loaded[key] = payload
            else:
                loaded[key] = PeopleData.from_dict(key, payload)
        return loaded

    def initPeople(idata=None):
        global peopleData, peopleInfo
        existing_people_data = peopleData if isinstance(peopleData, dict) else {}
        loaded_people_data = loadPeopleData(idata)
        for person, data in list(existing_people_data.items()):
            if isinstance(data, PeopleData) and data.__class__ is not PeopleData:
                loaded_people_data[people_normalize_id(person)] = data
        peopleData = loaded_people_data
        if not isinstance(peopleInfo, dict):
            peopleInfo = {}

        for person in sorted(peopleData.keys()):
            info = peopleInfo.get(person, None)
            if isinstance(info, PeopleInfo):
                info.name = person
                info.update()
            else:
                info = PeopleInfo(person)
            peopleInfo[person] = info

        # Populate canonical girls + secondary_npcs lists (defined in the early block above in this same file)
        try:
            _register_people_lists()
        except Exception:
            pass
        # Also direct append for anything that registered itself in its Init*.rpy
        try:
            if isinstance(girls, list):
                for k, info in peopleInfo.items():
                    if isinstance(info, Girl) and info not in girls:
                        girls.append(info)
            if isinstance(secondary_npcs, list):
                for k, info in peopleInfo.items():
                    if isinstance(info, BaseNPC) and not isinstance(info, Girl) and info not in secondary_npcs:
                        secondary_npcs.append(info)
        except Exception:
            pass

        return peopleInfo

    def getPersonData(person=""):
        key = people_normalize_id(person)
        if not key:
            return None
        if isinstance(peopleData, dict):
            return peopleData.get(key, None)
        return None

    def getPersonInfo(person=""):
        key = people_normalize_id(person)
        if not key:
            return None
        info = peopleInfo.get(key, None) if isinstance(peopleInfo, dict) else None
        if isinstance(info, PeopleInfo):
            return info.update()
        return None

    def people_sync_person(person=""):
        key = people_normalize_id(person)
        if not key:
            return None
        info = peopleInfo.get(key, None) if isinstance(peopleInfo, dict) else None
        if isinstance(info, PeopleInfo):
            return info.update()
        return None

    def people_sync_all():
        if isinstance(peopleInfo, dict):
            for person in list(peopleInfo.keys()):
                people_sync_person(person)
            _register_people_lists()
        return peopleInfo

    def people_reset_daily_interactions(names=None):
        if not isinstance(peopleInfo, dict):
            return peopleInfo
        if names is None:
            reset_names = set([people_normalize_id(row) for row in list(peopleInfo.keys())])
        else:
            reset_names = set([people_normalize_id(row) for row in list(names or [])])
        for person in sorted([row for row in reset_names if row]):
            info = peopleInfo.get(person, None)
            if isinstance(info, PeopleInfo):
                info.reset_daily(True)
        return peopleInfo

    def people_display_name(person=""):
        data = getPersonData(person)
        if data is not None:
            return str(data.cname or data.fullname or data.name)
        return people_normalize_id(person)

    def people_name(person="", grammatical_case="nominative", fallback=""):
        key = people_normalize_id(person)
        data = getPersonData(key)
        if data is None:
            return str(fallback or key)
        case_key = str(grammatical_case or "nominative").strip().lower()
        if case_key == "genitive":
            return str(data.genitive or data.fullname or data.cname or key)
        if case_key == "dative":
            return str(data.dative or data.fullname or data.cname or key)
        return str(data.cname or data.fullname or key)

    def people_name(person="", grammatical_case="nominative", fallback=""):
        key = people_normalize_id(person)
        data = getPersonData(key)
        if data is None:
            return str(fallback or key)
        case_key = str(grammatical_case or "nominative").strip().lower()
        if case_key == "genitive":
            return str(data.genitive or data.fullname or data.cname or key)
        if case_key == "dative":
            return str(data.dative or data.fullname or data.cname or key)
        return str(data.cname or data.fullname or key)

    def people_name(person="", grammatical_case="nominative", fallback=""):
        key = people_normalize_id(person)
        data = getPersonData(key)
        if data is None:
            return str(fallback or key)
        case_key = str(grammatical_case or "nominative").strip().lower()
        if case_key == "genitive":
            return str(data.genitive or data.fullname or data.cname or key)
        if case_key == "dative":
            return str(data.dative or data.fullname or data.cname or key)
        return str(data.cname or data.fullname or key)

    def people_name(person="", grammatical_case="nominative", fallback=""):
        key = people_normalize_id(person)
        data = getPersonData(key)
        if data is None:
            return str(fallback or key)
        case_key = str(grammatical_case or "nominative").strip().lower()
        if case_key == "genitive":
            return str(data.genitive or data.fullname or data.cname or key)
        if case_key == "dative":
            return str(data.dative or data.fullname or data.cname or key)
        return str(data.cname or data.fullname or key)

    def people_age(person="", fallback=0):
        data = getPersonData(person)
        if data is None:
            return people_to_int(fallback, 0)
        age_value = data.age(calendar_v2.cycle, calendar_v2.period, calendar_v2.day)
        return people_to_int(age_value, fallback)

    def people_birth_date(person=""):
        data = getPersonData(person)
        return dict(data.birth_date or {}) if data is not None else {}

    def people_gift_preferences(person=""):
        data = getPersonData(person)
        return list(data.gift_preferences or []) if data is not None else []

    def people_known_ids():
        if isinstance(peopleInfo, dict):
            return sorted([people_normalize_id(row) for row in list(peopleInfo.keys()) if people_normalize_id(row)])
        return []

label InitPeople:
    $ initPeople()
    return


label InitGameNPCs:
    call InitSandra
    call InitMelissa
    call InitAmanda
    call InitBecky
    call InitIrma
    call InitClara
    call InitGeorgett
    call InitLiza
    call InitInga
    call register_inga_secondary
    $ init_secondary_npc_profiles()
    call register_inga_secondary
    $ init_secondary_npc_profiles()
    call InitRobin
    call InitZimmer
    call InitEddie
    call register_alber_secondary
    call InitFrancheska
    call register_luisa_secondary
    call register_sergio_secondary
    call register_gerhard_secondary
    call register_lucas_secondary
    call register_clara_fiance_secondary
    call register_sergio_pet_secondary
    call InitDraupnir
    call InitMongol
    call InitDog
    call InitWerecat
    $ initPeople()
    $ npc_interval_schedule_load_all(True)
    return
