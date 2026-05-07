# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default peopleData = {}
default peopleInfo = {}

init python:
    def people_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def people_to_bool(value, default=False):
        if value is None:
            return bool(default)
        return bool(value)

    def people_get_map(name, default=None):
        try:
            value = globals().get(name, default)
            if isinstance(value, dict):
                return value
        except Exception:
            pass
        return default if isinstance(default, dict) else {}

    def people_normalize_id(person=""):
        return str(person or "").strip().lower()

    class PeopleData(object):
        def __init__(
            self,
            name,
            cname="",
            fullname="",
            genitive="",
            dative="",
            topics=None,
            num_icons=0,
            low_icon="",
            med_icon="",
            portrait="",
            default_location="",
            description="",
            age=0,
            schedule_entries=None,
            gift_preferences=None,
        ):
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
            time_value = time if hour is None else hour
            try:
                location = npc_schedule_location(self.name, weekday_value, time_value)
                if location:
                    return str(location)
            except Exception:
                pass
            try:
                return str(CurrentLoc.get(self.name, self.default_location) or self.default_location or "")
            except Exception:
                return str(self.default_location or "")

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
        def __init__(self, name, rel=0, talkToday=None, flirtToday=False, giftToday=False, gifts=None):
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
            self.openness = 0
            self.corruption = 0
            self.known = False
            self.location = ""
            self.data = None
            self.update()

        def update(self):
            self.name = people_normalize_id(self.name)
            try:
                self.data = peopleData.get(self.name, PeopleData(self.name))
            except Exception:
                self.data = PeopleData(self.name)
            self.sync_from_maps()
            return self

        def sync_from_maps(self):
            self.rel = people_to_int(people_get_map("Friends").get(self.name, self.rel), self.rel)
            self.openness = people_to_int(people_get_map("otkroven").get(self.name, self.openness), self.openness)
            self.corruption = people_to_int(people_get_map("sluttiness").get(self.name, self.corruption), self.corruption)
            self.known = people_to_bool(people_get_map("knowsMC").get(self.name, self.known), self.known)
            self.talkCountToday = people_to_int(people_get_map("TalkedToday").get(self.name, self.talkCountToday), self.talkCountToday)
            self.flirtCountToday = people_to_int(people_get_map("FlirtedToday").get(self.name, self.flirtCountToday), self.flirtCountToday)
            self.giftCountToday = people_to_int(people_get_map("GiftedToday").get(self.name, self.giftCountToday), self.giftCountToday)
            self.askedCountToday = people_to_int(people_get_map("AskedToday").get(self.name, self.askedCountToday), self.askedCountToday)
            try:
                self.location = str(getLocation(self.name) or "")
            except Exception:
                self.location = str(people_get_map("CurrentLoc").get(self.name, self.location) or self.location or "")
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
            if self.location:
                people_get_map("CurrentLoc")[self.name] = str(self.location)
            return self

        def reset_daily(self, sync_maps=True):
            self.talkToday = set()
            self.talkCountToday = 0
            self.flirtCountToday = 0
            self.giftCountToday = 0
            self.askedCountToday = 0
            self.flirtToday = False
            self.giftToday = False
            if sync_maps:
                for map_name in ["Talked", "TalkedToday", "FlirtedToday", "GiftedToday", "AskedToday"]:
                    row = people_get_map(map_name)
                    if isinstance(row, dict):
                        row[self.name] = 0
            return self

        def getLocation(self, wday=None, hour=None):
            try:
                self.location = self.data.getLocation(wday, hour)
            except Exception:
                self.location = str(people_get_map("CurrentLoc").get(self.name, self.location) or self.location or "")
            return self.location

        def isInLocation(self, location, wday=None, hour=None):
            return str(self.getLocation(wday, hour) or "") == str(location or "")

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
                "default_location": str(locations.get(person, "") or ""),
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
        peopleData = loadPeopleData(idata)
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

            people_get_map("Friends").setdefault(person, info.rel)
            people_get_map("otkroven").setdefault(person, info.openness)
            people_get_map("sluttiness").setdefault(person, info.corruption)
            people_get_map("knowsMC").setdefault(person, info.known)
            people_get_map("TalkedToday").setdefault(person, info.talkCountToday)
            people_get_map("FlirtedToday").setdefault(person, info.flirtCountToday)
            people_get_map("GiftedToday").setdefault(person, info.giftCountToday)
            people_get_map("AskedToday").setdefault(person, info.askedCountToday)
            people_get_map("CurrentLoc").setdefault(person, peopleData[person].default_location)

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
            if not peopleInfo:
                initPeople()
            for person in list(peopleInfo.keys()):
                people_sync_person(person)
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
