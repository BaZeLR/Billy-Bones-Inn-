# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default peopleData = {}
default peopleInfo = {}
default girls = []
default secondary_npcs = []

# =============================================================================
# BASE CLASSES (templates) - placed here in the normal people runtime file
# as requested ("classes as definitions of templates will leave in people").
# Using init -999 python: (documented Ren'Py priority) so they are available
# before any later init python blocks in the per-NPC Init*.rpy files run.
# Specific per-NPC classes (Amanda, Becky, etc.) stay defined in their own
# game/NPC/*/Init*.rpy files. Instantiation also stays there.
# No magic 00_ files. Only this existing people rpy + the per-NPC Inits.
# =============================================================================
init -999 python:

    def people_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def people_to_bool(value, default=False):
        if value is None:
            return bool(default)
        return bool(value)

    def people_normalize_id(person=""):
        return str(person or "").strip().lower()

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
            "robin": "Forest",
            "mongol": "",
            "zimmer": "CityGuard",
            "draupnir": "StolyarWorkshop",
            "sergio": "",
        }.get(people_normalize_id(person), "")

    class PeopleData(object):
        def __init__(self, name, cname="", fullname="", genitive="", dative="",
                     topics=None, num_icons=0, low_icon="", med_icon="", portrait="",
                     default_location="", description="", age=0, schedule_entries=None,
                     gift_preferences=None):
            self.name = people_normalize_id(name)
            self.cname = str(cname or fullname or self.name)
            self.fullname = str(fullname or cname or self.name)
            self.genitive = str(genitive or self.fullname)
            self.dative = str(dative or self.fullname)
            self.topics = list(topics or [])
            self.num_icons = people_to_int(num_icons, 0)
            self.low_icon = str(low_icon or "")
            self.med_icon = str(med_icon or "")
            self.portrait = str(portrait or "")
            self.default_location = str(default_location or "")
            self.description = str(description or "")
            self.age = people_to_int(age, 0)
            self.schedule_entries = list(schedule_entries or [])
            self.gift_preferences = list(gift_preferences or [])

        def getLocation(self, wday=None, hour=None):
            weekday_value = week if wday is None else wday
            time_value = None if hour is None else hour
            try:
                location_value = npc_schedule_location(self.name, weekday_value, time_value)
                if location_value:
                    return str(location_value)
            except Exception:
                pass
            try:
                if npc_interval_schedule_has_contract(self.name):
                    return ""
            except Exception:
                pass
            try:
                return str(self.default_location or people_initial_location(self.name) or "")
            except Exception:
                return str(self.default_location or people_initial_location(self.name) or "")

        def isInLocation(self, location, wday=None, hour=None):
            return str(self.getLocation(wday, hour) or "") == str(location or "")

        def selectIcon(self, wday=None, hour=None):
            for candidate in [self.portrait, self.med_icon, self.low_icon]:
                candidate = str(candidate or "")
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

    class PeopleInfo(object):
        def __init__(self, name, rel=0, talkToday=None, flirtToday=False, giftToday=False,
                     gifts=None, var=None):
            self.name = people_normalize_id(name)
            self.rel = people_to_int(rel, 0)
            self.talkToday = set(talkToday or [])
            self.flirtToday = people_to_bool(flirtToday, False)
            self.giftToday = people_to_bool(giftToday, False)
            self.gifts = set(gifts or [])
            self.talkCountToday = 0
            self.flirtCountToday = 0
            self.giftCountToday = 0
            self.askedCountToday = 0
            self.fuckedCountToday = 0
            self.drunk = 0
            self.openness = 0
            self.corruption = 0
            self.known = False
            self.location = ""
            self.data = None
            self.var = var if var is not None else {}
            # Hidden per-girl lunar fertility dict (for Amanda, Melissa, Clara, Sandra)
            self.lunar_fertility = {"offset": 0, "last_phase": 0, "strength": 1.0}

        def update(self):
            self.name = people_normalize_id(self.name)
            try:
                self.data = peopleData.get(self.name, PeopleData(self.name))
            except Exception:
                self.data = PeopleData(self.name)
            self.sync_from_maps()
            return self

        def sync_from_maps(self):
            try:
                fmap = globals().get("Friends", {}) or {}
                self.rel = people_to_int(fmap.get(self.name, self.rel), self.rel)
            except Exception:
                pass
            try:
                smap = globals().get("sluttiness", {}) or {}
                self.corruption = people_to_int(smap.get(self.name, self.corruption), self.corruption)
            except Exception:
                pass
            try:
                omap = globals().get("otkroven", {}) or {}
                self.openness = people_to_int(omap.get(self.name, self.openness), self.openness)
            except Exception:
                pass
            try:
                kmap = globals().get("knowsMC", {}) or {}
                self.known = people_to_bool(kmap.get(self.name, self.known), self.known)
            except Exception:
                pass
            try:
                self.talkCountToday = people_to_int(people_get_map("TalkedToday").get(self.name, self.talkCountToday), self.talkCountToday)
                self.flirtCountToday = people_to_int(people_get_map("FlirtedToday").get(self.name, self.flirtCountToday), self.flirtCountToday)
                self.giftCountToday = people_to_int(people_get_map("GiftedToday").get(self.name, self.giftCountToday), self.giftCountToday)
                self.askedCountToday = people_to_int(people_get_map("AskedToday").get(self.name, self.askedCountToday), self.askedCountToday)
                self.fuckedCountToday = people_to_int(people_get_map("FuckedToday").get(self.name, self.fuckedCountToday), self.fuckedCountToday)
                self.drunk = people_to_int(people_get_map("Drunk").get(self.name, self.drunk), self.drunk)
            except Exception:
                pass
            try:
                self.location = str(self.getLocation() or "")
            except Exception:
                self.location = str(self.location or "")
            self.flirtToday = self.flirtCountToday > 0
            self.giftToday = self.giftCountToday > 0
            return self

        def apply_to_maps(self):
            people_get_map("Friends")[self.name] = people_to_int(self.rel, 0)
            people_get_map("otkroven")[self.name] = people_to_int(self.openness, 0)
            people_get_map("sluttiness")[self.name] = people_to_int(self.corruption, 0)
            people_get_map("knowsMC")[self.name] = bool(self.known)
            people_get_map("TalkedToday")[self.name] = people_to_int(self.talkCountToday, 0)
            people_get_map("FlirtedToday")[self.name] = people_to_int(self.flirtCountToday, 0)
            people_get_map("GiftedToday")[self.name] = people_to_int(self.giftCountToday, 0)
            people_get_map("AskedToday")[self.name] = people_to_int(self.askedCountToday, 0)
            people_get_map("FuckedToday")[self.name] = people_to_int(self.fuckedCountToday, 0)
            people_get_map("Drunk")[self.name] = people_to_int(self.drunk, 0)
            if self.location:
                people_get_map("CurrentLoc")[self.name] = str(self.location)
            return self

        def reset_daily(self, full=False):
            """Reset per-girl daily interaction counters.
            Called from people_reset_daily_interactions() during sleep/NextDay.
            These flags conceptually belong to each girl (talked/flirted/gifted/asked/fucked her today),
            not as pure player-global state.
            """
            self.talkCountToday = 0
            self.flirtCountToday = 0
            self.giftCountToday = 0
            self.askedCountToday = 0
            self.fuckedCountToday = 0
            self.drunk = 0
            self.flirtToday = False
            self.giftToday = False

            # Keep legacy global dicts in sync for compatibility (most code still uses them directly)
            for dname, attr in [
                ("TalkedToday", "talkCountToday"),
                ("FlirtedToday", "flirtCountToday"),
                ("GiftedToday", "giftCountToday"),
                ("AskedToday", "askedCountToday"),
                ("FuckedToday", "fuckedCountToday"),
                ("Drunk", "drunk"),
            ]:
                try:
                    d = globals().get(dname)
                    if isinstance(d, dict):
                        d[self.name] = 0
                except Exception:
                    pass

            if full:
                # Future: reset other daily per-girl state here if needed (e.g. some girl-specific today flags)
                pass

            return self

        def getLocation(self, wday=None, hour=None):
            try:
                if self.data is None:
                    self.data = peopleData.get(self.name, PeopleData(self.name))
                self.location = str(self.data.getLocation(wday, hour) or "")
            except Exception:
                self.location = str(self.location or "")
            return self.location

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
        """Base for all NPCs (secondaries + simple). Keeps .var for legacy XXXVar tables."""
        def __init__(self, name, **kwargs):
            super().__init__(name, **kwargs)
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

    class Girl(BaseNPC):
        """Girls with body layers, pregnancy, detailed history, lunar fertility."""
        def __init__(self, name, **kwargs):
            super().__init__(name, **kwargs)
            self.body_layers = {}
            self.insertion_state = {}
            self.clothing_layers = {}
            self.pregnancy_state = {}
            self.detailed_sex_history = []
            if not getattr(self, 'lunar_fertility', None):
                self.lunar_fertility = {"offset": hash(name) % 7, "last_phase": 0, "strength": 1.0}

        def promote_from_var(self, vardict=None):
            super().promote_from_var(vardict)
            v = vardict if vardict is not None else self.var
            if isinstance(v, dict):
                for k in ("body_layers", "clothing", "sex_history", "pregnancy"):
                    if k in v and isinstance(v[k], (dict, list)):
                        setattr(self, k, v[k])
            return self

    def _register_people_lists():
        """Fill girls / secondary_npcs from peopleInfo after registrations."""
        global girls, secondary_npcs
        if not isinstance(girls, list):
            girls = []
        if not isinstance(secondary_npcs, list):
            secondary_npcs = []
        try:
            pinfo = globals().get("peopleInfo", {}) or {}
            girl_keys = set([people_normalize_id(row) for row in list(globals().get("AllGirlNames", []) or [])])
            secondary_keys = set([people_normalize_id(row) for row in list(globals().get("SECONDARY_NPC_KEYS", []) or [])])
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
    def people_get_map(name, default=None):
        try:
            value = globals().get(name, default)
            if isinstance(value, dict):
                return value
        except Exception:
            pass
        return default if isinstance(default, dict) else {}

    def people_known_ids_from_current_state():
        keys = set()
        for map_name in ["RealName", "CurrentLoc", "NPCSchedules", "Friends", "sluttiness", "otkroven", "knowsMC", "age_girls", "girltextdesc"]:
            try:
                keys.update([people_normalize_id(row) for row in list(people_get_map(map_name).keys())])
            except Exception:
                pass
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
        real_names = people_get_map("RealName")
        real_names2 = people_get_map("RealName2")
        real_names3 = people_get_map("RealName3")
        ages = people_get_map("age_girls")
        descriptions = people_get_map("girltextdesc")
        locations = people_get_map("CurrentLoc")
        gift_preferences = people_get_map("GiftPreferences")
        dataset = {}

        for person in people_known_ids_from_current_state():
            try:
                schedule_entries = npc_schedule_list(person)
            except Exception:
                schedule_entries = []
            dataset[person] = {
                "name": person,
                "cname": str(real_names.get(person, person) or person),
                "fullname": str(real_names.get(person, person) or person),
                "genitive": str(real_names2.get(person, real_names.get(person, person)) or person),
                "dative": str(real_names3.get(person, real_names.get(person, person)) or person),
                "portrait": people_portrait_for(person),
                "default_location": str(locations.get(person, "") or people_initial_location(person) or ""),
                "description": str(descriptions.get(person, "") or ""),
                "age": people_to_int(ages.get(person, 0), 0),
                "schedule_entries": schedule_entries,
                "gift_preferences": list(gift_preferences.get(person, []) or []),
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
                info = PeopleInfo(person, people_get_map("Friends").get(person, 0))
            peopleInfo[person] = info

            # Attach the legacy per-NPC dict (AmandaVar, RobinVar, etc.) as .var
            # so that old code using XXXVar[...] can gradually move to info.var[...]
            var_name = person[0].upper() + person[1:] + "Var"
            if var_name in globals() and isinstance(globals()[var_name], dict):
                info.var = globals()[var_name]

            people_get_map("Friends").setdefault(person, info.rel)
            people_get_map("otkroven").setdefault(person, info.openness)
            people_get_map("sluttiness").setdefault(person, info.corruption)
            people_get_map("knowsMC").setdefault(person, info.known)
            people_get_map("TalkedToday").setdefault(person, info.talkCountToday)
            people_get_map("FlirtedToday").setdefault(person, info.flirtCountToday)
            people_get_map("GiftedToday").setdefault(person, info.giftCountToday)
            people_get_map("AskedToday").setdefault(person, info.askedCountToday)
            people_get_map("FuckedToday").setdefault(person, info.fuckedCountToday)
            people_get_map("Drunk").setdefault(person, info.drunk)
            people_get_map("CurrentLoc").setdefault(person, peopleData[person].default_location)

        # Populate canonical girls + secondary_npcs lists (defined in the early block above in this same file)
        try:
            _register_people_lists()
        except Exception:
            pass
        # Also direct append for anything that registered itself in its Init*.rpy
        try:
            if 'girls' in globals() and isinstance(girls, list):
                for k, info in peopleInfo.items():
                    if isinstance(info, Girl) and info not in girls:
                        girls.append(info)
            if 'secondary_npcs' in globals() and isinstance(secondary_npcs, list):
                for k, info in peopleInfo.items():
                    if isinstance(info, BaseNPC) and not isinstance(info, Girl) and info not in secondary_npcs:
                        secondary_npcs.append(info)
        except Exception:
            pass

        return peopleInfo

    def people_after_load_update():
        try:
            initPeople()
        except Exception:
            pass

    if people_after_load_update not in config.after_load_callbacks:
        config.after_load_callbacks.append(people_after_load_update)

    def getPersonData(person=""):
        key = people_normalize_id(person)
        if not key:
            return None
        try:
            if key not in peopleData:
                initPeople()
            return peopleData.get(key, None)
        except Exception:
            return None

    def getPersonInfo(person=""):
        key = people_normalize_id(person)
        if not key:
            return None
        try:
            if key not in peopleInfo:
                initPeople()
            info = peopleInfo.get(key, None)
            if isinstance(info, PeopleInfo):
                return info.update()
        except Exception:
            pass
        return None

    def people_sync_person(person=""):
        key = people_normalize_id(person)
        if not key:
            return None
        try:
            if key not in peopleInfo:
                initPeople()
            info = peopleInfo.get(key, None)
            if isinstance(info, PeopleInfo):
                return info.update()
        except Exception:
            pass
        return None

    def people_sync_all():
        try:
            known_now = people_known_ids_from_current_state()
            if not peopleInfo or not peopleData or any(row not in peopleData for row in known_now):
                initPeople()
            for sec_key in [people_normalize_id(row) for row in list(globals().get("SECONDARY_NPC_KEYS", []) or [])]:
                if sec_key and sec_key not in peopleInfo:
                    peopleInfo[sec_key] = BaseNPC(sec_key)
            for person in list(peopleInfo.keys()):
                people_sync_person(person)
            _register_people_lists()
        except Exception:
            pass
        return peopleInfo

    def people_reset_daily_interactions(names=None):
        try:
            if not peopleInfo:
                initPeople()
            if names is None:
                reset_names = set(people_known_ids())
                reset_names.update([people_normalize_id(row) for row in list(peopleInfo.keys())])
            else:
                reset_names = set([people_normalize_id(row) for row in list(names or [])])
            for person in sorted([row for row in reset_names if row]):
                info = peopleInfo.get(person, None)
                if not isinstance(info, PeopleInfo):
                    info = PeopleInfo(person, people_get_map("Friends").get(person, 0))
                    peopleInfo[person] = info
                info.reset_daily(True)
        except Exception:
            pass
        return peopleInfo

    def people_display_name(person=""):
        data = getPersonData(person)
        if data is not None:
            return str(data.cname or data.fullname or data.name)
        key = people_normalize_id(person)
        try:
            return str(RealName.get(key, key) or key)
        except Exception:
            return key

    def people_known_ids():
        try:
            if not peopleInfo:
                initPeople()
            return sorted([people_normalize_id(row) for row in list(peopleInfo.keys()) if people_normalize_id(row)])
        except Exception:
            return people_known_ids_from_current_state()

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
    $ init_secondary_npc_profiles()
    call register_robin_secondary
    call register_zimmer_secondary
    call register_eddie_secondary
    call register_alber_secondary
    call register_francheska_secondary
    call register_luisa_secondary
    call register_sergio_secondary
    call register_draupnir_secondary
    call register_mongol_secondary
    python:
        for _girl_id in list(AllGirlNames or []):
            _girl_key = str(_girl_id or "").strip().lower()
            HarassInstructions.setdefault(_girl_key, "")
            Drunk.setdefault(_girl_key, 0)
    $ initPeople()
    $ people_sync_all()
    return
