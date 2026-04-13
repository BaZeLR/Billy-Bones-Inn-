# Auto-generated NPC infrastructure adapted to Engine Template JSON-per-NPC workflow.

init python:

    class PeopleData:
        def __init__(self, entry):
            self.entry = entry
            self.name = entry.get("id")
            self.cname = entry.get("display_name", self.name.capitalize())
            self.fullname = entry.get("native_name", self.cname)
            self.native_genitive = entry.get("native_genitive")
            self.native_dative = entry.get("native_dative")
            self.description = entry.get("description")
            self.role = entry.get("role", "primary")
            self.stats = entry.get("stats", {})
            self.skills = entry.get("skills", {})
            self.jobs = entry.get("jobs", {})
            self.default_clothing = entry.get("default_clothing", {})
            self.relationships = entry.get("relationships", {})
            self.current_location = entry.get("current_location")
            self.virgin = entry.get("virgin")
            self.age = entry.get("age")
            schedule = entry.get("schedule", {})
            weekday = schedule.get("weekday", [None] * 24)
            weekend = schedule.get("weekend", [None] * 24)
            if len(weekday) < 24:
                weekday = weekday + [None] * (24 - len(weekday))
            if len(weekend) < 24:
                weekend = weekend + [None] * (24 - len(weekend))
            self.weekday_sched = weekday[:24]
            self.weekend_sched = weekend[:24]
            icon_info = entry.get("icons", {})
            self.num_icons = icon_info.get("num_icons", 1)
            self.low_icon = icon_info.get("low_icon", 1)
            self.med_icon = icon_info.get("med_icon", 1)

        def getLocation(self, week_day, hour):
            return self.weekday_sched[hour] if week_day <= 5 else self.weekend_sched[hour]

        def isInLocation(self, location, week_day, hour):
            schedule = self.weekday_sched if week_day <= 5 else self.weekend_sched
            return location == schedule[hour]

        def selectIcon(self, week_day, hour):
            base_path = f"images/NPC/{self.cname}/icons"
            if hour <= 5:
                return f"{base_path}/sleep.jpg"
            rel = peopleInfo.get(self.name).rel if self.name in peopleInfo else 0
            if rel < 200:
                return f"{base_path}/{self.low_icon:02d}.jpg"
            if rel < 400:
                return f"{base_path}/{self.med_icon:02d}.jpg"
            return f"{base_path}/{min(self.num_icons, 1):02d}.jpg"

    class PeopleInfo:
        def __init__(self, data, rel=None):
            self.name = data.name
            self.data = data
            default_rel = data.relationships.get("player_friendship", 0)
            self.rel = default_rel if rel is None else rel
            self.talkToday = set()
            self.flirtToday = False
            self.giftToday = False
            self.gifts = set()

        def update(self):
            self.data = peopleData[self.name]

    def loadPeopleData(entries):
        return {entry.get("id"): PeopleData(entry) for entry in entries}

    def initPeople():
        global peopleInfo
        if "peopleInfo" not in globals() or not isinstance(peopleInfo, dict):
            peopleInfo = {}
        for name, pdata in peopleData.items():
            if name not in peopleInfo:
                peopleInfo[name] = PeopleInfo(pdata)
            else:
                peopleInfo[name].update()

init python:
    _people_entries = renpy.store.load_people_dataset()
    peopleData = loadPeopleData(_people_entries)
    initPeople()

default peopleInfo = {}
