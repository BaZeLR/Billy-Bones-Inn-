# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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

    class PeopleRegistry(object):
        """Single owner for static person definitions and saved NPC instances."""

        def __init__(self):
            self.definitions = {}
            self.runtime = {}

        def register(self, static_data, runtime_object):
            if static_data is None or runtime_object is None:
                raise ValueError("PeopleRegistry.register requires static data and a runtime object")
            data_key = people_normalize_id(getattr(static_data, "name", ""))
            runtime_key = people_normalize_id(getattr(runtime_object, "name", ""))
            key = data_key or runtime_key
            if not key:
                raise ValueError("Registered person must have a stable id")
            if data_key and runtime_key and data_key != runtime_key:
                raise ValueError("Static/runtime person ids do not match: %s != %s" % (data_key, runtime_key))

            static_data.name = key
            runtime_object.name = key
            runtime_object.data = static_data
            self.definitions[key] = static_data
            self.runtime[key] = runtime_object
            runtime_object.update()
            runtime_object.data = static_data
            return runtime_object

        def get_data(self, person=""):
            return self.definitions.get(people_normalize_id(person), None)

        def get_info(self, person=""):
            return self.runtime.get(people_normalize_id(person), None)

        def ids(self):
            return sorted([key for key in self.runtime.keys() if people_normalize_id(key)])

        def items(self):
            return [(key, self.runtime[key]) for key in self.ids()]

        def values(self):
            return [row[1] for row in self.items()]

        def data_values(self):
            return [self.definitions[key] for key in sorted(self.definitions.keys())]

        def girl_items(self):
            return [(key, info) for key, info in self.items() if info.registry_group == "girl"]

        def girl_values(self):
            return [row[1] for row in self.girl_items()]

        def secondary_items(self):
            return [(key, info) for key, info in self.items() if info.registry_group == "secondary"]

        def secondary_values(self):
            return [row[1] for row in self.secondary_items()]

        def location(self, person="", weekday_value=None, time_value=None):
            info = self.get_info(person)
            if info is None:
                return ""
            return str(info.getLocation(weekday_value, time_value) or "")

        def ids_at(self, location="", weekday_value=None, time_value=None):
            room_key = str(location or "").strip()
            if not room_key:
                return []
            present = [
                key for key, info in self.items()
                if info is not None and str(info.getLocation(weekday_value, time_value) or "") == room_key
            ]
            return sorted(present, key=lambda key: str(self.get_info(key).display_name() or key).lower())

        def action_data_for_room(self, person="", room_code=""):
            key = people_normalize_id(person)
            room_key = str(room_code or "").strip()
            if not key or not room_key:
                return None
            room = rooms.get(room_key)
            if room is not None and not room.is_open():
                return None
            info = self.get_info(key)
            if info is None or not info.interaction_visible(room_key):
                return None
            return info.action_data(room_key)

        def schedule_entry(self, person="", weekday_value=None, time_value=None):
            data = self.get_data(person)
            if data is None:
                return None
            return data.schedule_resolve(weekday_value, time_value)

        def is_awake(self, person="", weekday_value=None, time_value=None):
            entry = self.schedule_entry(person, weekday_value, time_value)
            return True if entry is None else bool(entry.awake)

        def can_talk(self, person="", weekday_value=None, time_value=None):
            entry = self.schedule_entry(person, weekday_value, time_value)
            return True if entry is None else bool(entry.awake) and bool(entry.talkable)

        def schedule_state(self, person="", weekday_value=None, time_value=None):
            data = self.get_data(person)
            if data is None:
                return {"location": "", "awake": True, "talkable": True, "label": "", "interval": "", "source": ""}
            return data.schedule_state(weekday_value, time_value)

        def repair(self):
            for key, info in self.items():
                data = self.get_data(key)
                if data is None:
                    raise ValueError("Missing static data for registered person: %s" % key)
                info.name = key
                info.data = data
                info.update()
                info.data = data
            return self

        def __len__(self):
            return len(self.runtime)

        def __contains__(self, person):
            return people_normalize_id(person) in self.runtime

    def npc_schedule_clock_minute(time_value=None):
        if time_value is None:
            return int(calendar_v2.clock_minutes() or 0) % 1440
        value = int(time_value or 0)
        if 0 <= value <= 23:
            return value * 60
        return value % 1440

    class NPCScheduleEntry(object):
        def __init__(self, location="", weekdays=None, start_hour=0, end_hour=24, awake=True, talkable=True, condition=None, priority=0, label="", start_minute=None, end_minute=None):
            self.location = str(location or "").strip()
            self.weekdays = list(weekdays or [])
            self.start_minute = int(start_hour or 0) * 60 if start_minute is None else int(start_minute or 0)
            self.end_minute = int(end_hour or 0) * 60 if end_minute is None else int(end_minute or 0)
            self.awake = bool(awake)
            self.talkable = bool(talkable)
            self.condition = condition
            self.priority = int(priority or 0)
            self.label = str(label or "").strip()

        def selected_location(self):
            return str(self.location or "")

        def matches(self, weekday_value=None, time_value=None):
            week_value = int(calendar_v2.week if weekday_value is None else weekday_value or 0)
            minute_value = npc_schedule_clock_minute(time_value)
            if self.weekdays and week_value not in self.weekdays:
                return False
            if self.start_minute <= self.end_minute:
                if not (self.start_minute <= minute_value < self.end_minute):
                    return False
            elif not (minute_value >= self.start_minute or minute_value < self.end_minute):
                return False
            return room_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

    class NPCHourScheduleEntry(NPCScheduleEntry):
        def __init__(self, npc_id="", location="", location_choices=None, weekdays=None, start="00:00", end="23:59", awake=True, talkable=True, condition=None, priority=600, label="", source="json"):
            start_text = str(start or "0").strip()
            end_text = str(end or "23").strip()
            start_parts = start_text.split(":", 1)
            end_parts = end_text.split(":", 1)
            start_minute = int(start_parts[0] or 0) * 60 + int(start_parts[1] or 0) if len(start_parts) > 1 else int(start_parts[0] or 0) * 60
            end_minute = int(end_parts[0] or 0) * 60 + int(end_parts[1] or 0) if len(end_parts) > 1 else int(end_parts[0] or 0) * 60
            end_minute += 1
            super(NPCHourScheduleEntry, self).__init__(location, weekdays, awake=awake, talkable=talkable, condition=condition, priority=priority, label=label, start_minute=start_minute, end_minute=end_minute)
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
                roll = procedural_randint(1, scale, "npc_hour_%s_%s_%s_%s" % (self.npc_id, self.label, calendar_v2.daysInGame, self.start_minute))
                cursor = 0
                for row in choices:
                    cursor += int(round(max(0.0, float(row.get("probability", 0.0) or 0.0)) * scale))
                    if roll <= cursor:
                        return str(row.get("location", "") or "")
                return ""
            roll = procedural_randint(1, int(round(total_probability * scale)), "npc_hour_%s_%s_%s_%s" % (self.npc_id, self.label, calendar_v2.daysInGame, self.start_minute))
            cursor = 0
            for row in choices:
                cursor += int(round(max(0.0, float(row.get("probability", 0.0) or 0.0)) * scale))
                if roll <= cursor:
                    return str(row.get("location", "") or "")
            return str(choices[-1].get("location", "") or "")

        def matches(self, weekday_value=None, time_value=None):
            if not super(NPCHourScheduleEntry, self).matches(weekday_value, time_value):
                return False
            if not str(self.selected_location() or "").strip():
                return False
            return True

    def npc_daily_schedule_interval(start_hour=0, end_hour=24, location="", awake=True, talkable=True, label="", priority=500):
        return {"start_minute": int(start_hour or 0) * 60, "end_minute": int(end_hour or 0) * 60, "location": str(location or "").strip(), "awake": bool(awake), "talkable": bool(talkable), "label": str(label or "").strip(), "priority": int(priority or 500)}

    def npc_daily_schedule_choice(location="", weight=1, awake=True, talkable=True, label="", condition=None):
        return {"location": str(location or "").strip(), "weight": max(0, int(weight or 0)), "awake": bool(awake), "talkable": bool(talkable), "label": str(label or "").strip(), "condition": condition}

    def npc_daily_schedule_random_interval(start_hour=0, end_hour=24, choices=None, weekdays=None, label="", priority=500):
        return {"start_minute": int(start_hour or 0) * 60, "end_minute": int(end_hour or 0) * 60, "choices": list(choices or []), "weekdays": list(weekdays or []), "label": str(label or "").strip(), "priority": int(priority or 500)}

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
            self.daily_schedule_template = {"default_intervals": [], "random_intervals": []}
            self.daily_schedule_plan_day = -1
            self.daily_schedule_plan = []
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
            current_cycle = people_to_int(getattr(calendar_v2, "cycle", CALENDAR_START_CYCLE), CALENDAR_START_CYCLE)
            age_value = current_cycle - birth_cycle
            birth_period = people_to_int(self.birth_date.get("period", 1), 1)
            birth_day = people_to_int(self.birth_date.get("day", 1), 1)
            current_period = people_to_int(getattr(calendar_v2, "period", 1), 1)
            current_day = people_to_int(getattr(calendar_v2, "day", 1), 1)
            if (current_period, current_day) < (birth_period, birth_day):
                age_value -= 1
            return max(0, age_value)

        def getLocation(self, wday=None, hour=None):
            entry = self.schedule_resolve(wday, hour)
            if entry is not None:
                return str(entry.selected_location() or "")
            if self.interval_schedule_loaded and self.interval_schedule_entries:
                return ""
            return str(self.default_location or "")

        def set_schedule(self, entries=None):
            self.schedule_entries = list(entries or [])
            return self.schedule_entries

        def add_schedule_entry(self, entry=None):
            if entry is not None:
                self.schedule_entries.append(entry)
            return self.schedule_entries

        def set_daily_schedule(self, default_intervals=None, random_intervals=None):
            self.daily_schedule_template = {
                "default_intervals": list(default_intervals or []),
                "random_intervals": list(random_intervals or []),
            }
            self.invalidate_daily_schedule()
            return self.daily_schedule_template

        def ensure_schedule_runtime_state(self):
            if not isinstance(getattr(self, "schedule_entries", None), list):
                self.schedule_entries = []
            if not isinstance(getattr(self, "daily_schedule_template", None), dict):
                self.daily_schedule_template = {"default_intervals": [], "random_intervals": []}
            if not hasattr(self, "daily_schedule_plan_day"):
                self.daily_schedule_plan_day = -1
            if not isinstance(getattr(self, "daily_schedule_plan", None), list):
                self.daily_schedule_plan = []
            if not isinstance(getattr(self, "interval_schedule_entries", None), list):
                self.interval_schedule_entries = []
            if not hasattr(self, "interval_schedule_loaded"):
                self.interval_schedule_loaded = False
            if not hasattr(self, "interval_schedule_load_error"):
                self.interval_schedule_load_error = ""
            return self

        def invalidate_daily_schedule(self):
            self.ensure_schedule_runtime_state()
            self.daily_schedule_plan_day = -1
            self.daily_schedule_plan = []
            return self

        def daily_schedule_choice_allowed(self, choice):
            row = dict(choice or {})
            if not str(row.get("location", "") or "").strip():
                return False
            condition = row.get("condition", None)
            if condition is not None and not room_rule_true(condition):
                return False
            return True

        def daily_schedule_pick_choice(self, choices, choice_key=""):
            allowed = [dict(choice or {}) for choice in list(choices or []) if self.daily_schedule_choice_allowed(choice)]
            if not allowed:
                return None
            total_weight = sum([max(0, int(row.get("weight", 1) or 1)) for row in allowed])
            if total_weight <= 0:
                return allowed[0]
            roll = procedural_randint(1, total_weight, "daily_schedule_%s_%s_%s_%s" % (self.name, int(calendar_v2.daysInGame or 0), str(choice_key or ""), total_weight))
            cursor = 0
            for row in allowed:
                cursor += max(0, int(row.get("weight", 1) or 1))
                if roll <= cursor:
                    return row
            return allowed[-1]

        def daily_schedule_entry_from_row(self, row, weekday_value=None):
            data = dict(row or {})
            return NPCScheduleEntry(
                location=str(data.get("location", "") or ""),
                weekdays=[int(calendar_v2.week if weekday_value is None else weekday_value or 0)],
                awake=bool(data.get("awake", True)),
                talkable=bool(data.get("talkable", True)),
                priority=int(data.get("priority", 500) or 500),
                label=str(data.get("label", "") or ""),
                start_minute=int(data.get("start_minute", 0) or 0),
                end_minute=int(data.get("end_minute", 1440) or 0),
            )

        def daily_schedule_build(self, weekday_value=None):
            day_value = int(calendar_v2.daysInGame or 0)
            current_week = int(calendar_v2.week or 0)
            week_value = int(current_week if weekday_value is None else weekday_value or 0)
            cache_current_day = week_value == current_week
            plan_day = int(self.daily_schedule_plan_day if self.daily_schedule_plan_day is not None else -1)
            if cache_current_day and plan_day == day_value:
                return list(self.daily_schedule_plan or [])
            template = dict(self.daily_schedule_template or {})
            interval_rows = {}
            for row in list(template.get("default_intervals", []) or []):
                data = dict(row or {})
                weekdays = list(data.get("weekdays", []) or [])
                if weekdays and week_value not in weekdays:
                    continue
                condition = data.get("condition", None)
                if condition is not None and not room_rule_true(condition):
                    continue
                interval_key = (int(data.get("start_minute", 0) or 0), int(data.get("end_minute", 1440) or 0))
                interval_rows[interval_key] = data
            for random_row in list(template.get("random_intervals", []) or []):
                data = dict(random_row or {})
                weekdays = list(data.get("weekdays", []) or [])
                if weekdays and week_value not in weekdays:
                    continue
                start_minute = int(data.get("start_minute", 0) or 0)
                end_minute = int(data.get("end_minute", 1440) or 0)
                choice_key = "%s:%s:%s:%s" % (week_value, start_minute, end_minute, str(data.get("label", "") or ""))
                choice = self.daily_schedule_pick_choice(data.get("choices", []), choice_key)
                if choice is None:
                    continue
                choice["start_minute"] = start_minute
                choice["end_minute"] = end_minute
                choice["priority"] = int(data.get("priority", 500) or 500)
                interval_rows[(start_minute, end_minute)] = choice
            plan = [self.daily_schedule_entry_from_row(interval_rows[row], week_value) for row in sorted(interval_rows.keys())]
            if cache_current_day:
                self.daily_schedule_plan = plan
                self.daily_schedule_plan_day = day_value
            return list(plan)

        def interval_location_choices_from_json(self, data):
            raw_location = data.get("location", "")
            probability_rows = list(data.get("location_probabilities", []) or [])
            if isinstance(raw_location, str):
                raw_locations = [raw_location] if probability_rows else []
            else:
                raw_locations = list(raw_location or [])
            if not raw_locations:
                return []
            fallback_probability = 1.0 / len(raw_locations)
            choices = []
            for index, loc in enumerate(raw_locations):
                probability = float(probability_rows[index]) if index < len(probability_rows) else fallback_probability
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
            self.ensure_schedule_runtime_state()
            if self.interval_schedule_loaded and not force:
                return list(self.interval_schedule_entries or [])
            self.interval_schedule_load_error = ""
            path = str(getattr(self, "schedule_source", "") or "").strip()
            if not path:
                self.interval_schedule_loaded = True
                self.interval_schedule_entries = []
                return []
            if path.startswith("schedules/"):
                path = "NPC/Schedules/" + path.split("/", 1)[1]
            if not renpy.loadable(path):
                self.interval_schedule_loaded = True
                self.interval_schedule_load_error = "%s: not loadable" % path
                self.interval_schedule_entries = []
                if str(getattr(self, "schedule_source", "") or "").strip():
                    raise ValueError(self.interval_schedule_load_error)
                return []
            raw = renpy.file(path).read().decode("utf-8")
            payload = json.loads(raw)
            rows = []
            for row in list(dict(payload or {}).get("entries", []) or []):
                entry = self.interval_schedule_entry_from_json(row)
                if entry.location or entry.location_choices:
                    rows.append(entry)
            self.interval_schedule_entries = rows
            self.interval_schedule_loaded = True
            return list(self.interval_schedule_entries or [])

        def schedule_entries_for_today(self, weekday_value=None):
            interval_entries = self.load_interval_schedule(False)
            return list(interval_entries or []) + list(self.daily_schedule_build(weekday_value) or []) + list(self.schedule_entries or [])

        def schedule_resolve(self, weekday_value=None, time_value=None):
            entries = sorted(self.schedule_entries_for_today(weekday_value), key=lambda row: int(getattr(row, "priority", 0) or 0), reverse=True)
            for entry in entries:
                if entry.matches(weekday_value, time_value):
                    return entry
            return None

        def schedule_state(self, weekday_value=None, time_value=None):
            entry = self.schedule_resolve(weekday_value, time_value)
            if entry is None:
                return {"location": "", "awake": True, "talkable": True, "label": "", "interval": "", "source": ""}
            interval_text = "%02d:%02d-%02d:%02d" % (
                int(getattr(entry, "start_minute", 0) or 0) // 60,
                int(getattr(entry, "start_minute", 0) or 0) % 60,
                (int(getattr(entry, "end_minute", 0) or 0) % 1440) // 60,
                int(getattr(entry, "end_minute", 0) or 0) % 60,
            )
            return {
                "location": str(entry.selected_location() or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
                "interval": interval_text,
                "source": str(getattr(entry, "source", "rpy") or "rpy"),
            }

        def isInLocation(self, location, wday=None, hour=None):
            return str(self.getLocation(wday, hour) or "") == str(location or "")

        def selectIcon(self, wday=None, hour=None):
            candidate = str(self.portrait or "")
            if candidate and renpy.loadable(candidate):
                return candidate
            portrait = str(girl_card_portrait_path(self.name) or "")
            if portrait and renpy.loadable(portrait):
                return portrait
            return str(self.portrait or "")

        @classmethod
        def from_dict(cls, name, payload):
            row = dict(payload or {})
            row.setdefault("name", name)
            return cls(**row)

    def npc_interval_schedule_load_all(force=False):
        for data in people.data_values():
            if data is not None:
                data.load_interval_schedule(force)

    def npc_schedule_after_load():
        for data in people.data_values():
            if not isinstance(data, PeopleData):
                continue
            data.ensure_schedule_runtime_state()
            data.invalidate_daily_schedule()
            data.load_interval_schedule(True)

    if npc_schedule_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(npc_schedule_after_load)

    class PeopleInfo(object):
        STORY_DEFAULTS = {}
        OPENNESS_RELATIONSHIP_STEPS = ((6, 3), (8, 5), (11, 6), (13, 7))
        talk_label = ""
        talk_args = ()
        registry_group = "secondary"

        def __init__(self, name, rel=0, talkToday=None, flirtToday=False, giftToday=False,
                    gifts=None, var=None, unknown_name=""):
            self.name = people_normalize_id(name)
            self.rel = people_to_int(rel, 0)
            self.talkToday = set(talkToday or [])
            self.gifts = set(gifts or [])
            self.talked_today = 0
            self.flirted_today = 1 if people_to_bool(flirtToday, False) else 0
            self.gifted_today = 1 if people_to_bool(giftToday, False) else 0
            self.asked_today = 0
            self.fucked_today = 0
            self.sex_state = {}
            self.set_sex_busy(False)
            self.drunk = 0
            self.openness = 0
            self.rebel_baseline = 0
            self.corruption = 0
            self.known = False
            self.unknown_name = str(unknown_name or getattr(self.__class__, "unknown_name", "") or "")
            self.data = None
            self.var = var if var is not None else {}
            self.harass_instruction_state = ""

        def update(self):
            self.name = people_normalize_id(self.name)
            if hasattr(self, "location"):
                delattr(self, "location")
            if not getattr(self, "unknown_name", ""):
                self.unknown_name = str(getattr(self.__class__, "unknown_name", "") or "")
            registered_data = people.get_data(self.name)
            if registered_data is not None:
                self.data = registered_data
            return self

        def action_data(self, where_id=""):
            return {
                "npc_id": self.name,
                "talk_label": str(self.talk_label or ""),
                "talk_args": tuple(self.talk_args or ()),
                "title": self.display_name(),
                "where_id": str(where_id or ""),
            }

        def interaction_visible(self, room_code=""):
            return bool(str(room_code or "").strip())

        def talk_available_in_room(self, room_code=""):
            room_key = str(room_code or rooms.current_code or "").strip()
            if not room_key:
                return False
            breakfast = player.tavern_management.breakfast
            if room_key == "TavernKitchen" and bool(breakfast.event_active):
                present_ids = [people_normalize_id(row) for row in list(breakfast.present_ids or [])]
                return self.name in present_ids
            return (
                bool(people.can_talk(self.name))
                and str(self.getLocation() or "") == room_key
                and people.action_data_for_room(self.name, room_key) is not None
                and bool(self.social_action_allowed("talk"))
            )

        def var_state(self):
            state = getattr(self, "var", None)
            return state if isinstance(state, dict) else {}

        def var_value(self, key, default=None):
            return self.var_state().get(str(key or ""), default)

        def set_var(self, key, value):
            if not isinstance(getattr(self, "var", None), dict):
                self.var = {}
            self.var[str(key or "")] = value
            return value

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in self.STORY_DEFAULTS.items():
                if isinstance(value, dict):
                    default_value = dict(value)
                elif isinstance(value, list):
                    default_value = list(value)
                elif isinstance(value, set):
                    default_value = set(value)
                else:
                    default_value = value
                self.var.setdefault(key, default_value)
            return self.var

        def reset_skill_gains(self):
            self.skill_gains_today = {}
            return self.skill_gains_today

        def record_skill_gain(self, key, amount=1):
            if not isinstance(getattr(self, "skill_gains_today", None), dict):
                self.skill_gains_today = {}
            skill_key = str(key or "")
            self.skill_gains_today[skill_key] = people_to_int(self.skill_gains_today.get(skill_key, 0), 0) + people_to_int(amount, 1)
            return self.skill_gains_today[skill_key]

        def var_int(self, key, default=0):
            return people_to_int(self.var_value(key, default), default)

        def set_var_int(self, key, value):
            return self.set_var(key, people_to_int(value, 0))

        def add_var_int(self, key, amount=1):
            return self.set_var_int(key, self.var_int(key, 0) + people_to_int(amount, 0))

        def story_value(self, key, default=0):
            return self.var_value(key, default)

        def set_story_value(self, key, value):
            return self.set_var(key, value)

        def set_story_value_min(self, key, value):
            current = self.var_int(key, 0)
            return self.set_var_int(key, max(current, people_to_int(value, 0)))

        @property
        def flirtToday(self):
            return people_to_int(getattr(self, "flirted_today", 0), 0) > 0

        @flirtToday.setter
        def flirtToday(self, value):
            self.flirted_today = 1 if people_to_bool(value, False) else 0

        @property
        def giftToday(self):
            return people_to_int(getattr(self, "gifted_today", 0), 0) > 0

        @giftToday.setter
        def giftToday(self, value):
            self.gifted_today = 1 if people_to_bool(value, False) else 0

        def mark_talked(self, amount=1):
            value = people_to_int(amount, 1)
            self.talked_today = people_to_int(getattr(self, "talked_today", 0), 0) + value
            return self

        def talk_count(self):
            return people_to_int(getattr(self, "talked_today", 0), 0)

        def can_talk_today(self, limit=2):
            return self.talk_count() < people_to_int(limit, 2)

        def finish_talk(self):
            self.talked_today = self.talk_count() + 1
            return self.talked_today

        def add_relation(self, amount=1, cap=20):
            self.rel = max(
                0,
                min(
                    people_to_int(cap, 20),
                    people_to_int(getattr(self, "rel", 0), 0) + people_to_int(amount, 0),
                ),
            )
            return self.rel

        def mark_asked(self, amount=1):
            value = people_to_int(amount, 1)
            self.asked_today = people_to_int(getattr(self, "asked_today", 0), 0) + value
            return self

        def mark_asked_topic(self, topic_flag, relation_gain=1):
            flag = str(topic_flag or "")
            first_time = people_to_int(self.story_value(flag, 0), 0) == 0
            if first_time:
                self.set_story_value(flag, 1)
                if relation_gain:
                    self.add_relation(relation_gain)
            self.mark_asked()
            return first_time

        def mark_fucked(self, amount=1):
            value = people_to_int(amount, 1)
            self.fucked_today = people_to_int(getattr(self, "fucked_today", 0), 0) + value
            return self

        def ensure_sex_state(self):
            if not isinstance(getattr(self, "sex_state", None), dict):
                self.sex_state = {}
            self.sex_state.setdefault("arousal", 0)
            self.sex_state.setdefault("somebody_cums", 0)
            if not isinstance(self.sex_state.get("partner_positions"), dict):
                self.sex_state["partner_positions"] = {}
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
            try:
                position_key = {0: "none", 1: "pussy", 2: "mouth", 3: "tits", 4: "ass"}.get(int(position or 0), "none")
            except (TypeError, ValueError):
                position_key = str(position or "none").strip().lower()
                if position_key not in ("none", "pussy", "mouth", "tits", "ass"):
                    position_key = "none"
            actor_key = str(actor or "you").strip().lower()
            state = self.ensure_sex_state()
            if position_key == "none":
                state["partner_positions"].pop(actor_key, None)
            else:
                state["partner_positions"][actor_key] = position_key
            return position_key

        def cock_position(self, actor="You"):
            actor_key = str(actor or "you").strip().lower()
            state = self.sex_state if isinstance(getattr(self, "sex_state", None), dict) else {}
            return str(state.get("partner_positions", {}).get(actor_key, "none") or "none")

        def cock_in(self, position="none", actor="You"):
            return self.cock_position(actor) == str(position or "none").strip().lower()

        def arousal_value(self):
            state = self.sex_state if isinstance(getattr(self, "sex_state", None), dict) else {}
            return people_clamp(state.get("arousal", 0), 0, 100)

        def set_arousal(self, value):
            self.ensure_sex_state()["arousal"] = people_clamp(value, 0, 100)
            return self.sex_state["arousal"]

        def add_arousal(self, amount=0, cap=100):
            return self.set_arousal(min(people_to_int(cap, 100), self.arousal_value() + people_to_int(amount, 0)))

        def sex_busy(self):
            state = self.sex_state if isinstance(getattr(self, "sex_state", None), dict) else {}
            return people_to_int(state.get("somebody_cums", 0), 0) != 0

        def set_sex_busy(self, value):
            self.ensure_sex_state()["somebody_cums"] = 1 if value else 0
            return self.sex_state["somebody_cums"]

        def cum_state(self, key):
            state = self.sex_state if isinstance(getattr(self, "sex_state", None), dict) else {}
            return people_to_int(state.get(str(key or ""), 0), 0)

        def set_cum_state(self, key, value=1):
            state = self.ensure_sex_state()
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

        def sex_stat(self, key, default=0):
            stats = getattr(self, "stats", None)
            if not isinstance(stats, dict):
                return default
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
            player.intimacy.record_cum(calendar_v2.daysInGame)
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
            self.openness = max(0, min(20, people_to_int(getattr(self, "openness", 0), 0) + people_to_int(open_delta, 0)))
            self.corruption = max(0, min(100, people_to_int(getattr(self, "corruption", 0), 0) + people_to_int(corruption_delta, 0)))
            return self

        def reset_openness_from_relationship(self):
            self.openness = 0
            relationship = people_to_int(self.rel, 0)
            for relationship_minimum, openness_value in self.OPENNESS_RELATIONSHIP_STEPS:
                if relationship >= relationship_minimum and self.openness <= openness_value:
                    self.openness = openness_value
            return self.openness

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
            self.rebellion = max(0, min(100, people_to_int(getattr(self, "rebellion", 0), 0) + people_to_int(amount, 0)))
            if isinstance(getattr(self, "reaction_state", None), dict):
                self.reaction_state["last_rebellion_reason"] = str(reason or "")
            return self.rebellion

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
            return str(self.harass_instruction_state or "")

        def set_harass_instruction(self, value=""):
            self.harass_instruction_state = str(value or "")
            return self.harass_instruction_state

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
            if bool(player.tavern_management.breakfast.event_active) and player.tavern_management.breakfast.present_ids is not None:
                breakfast_ids = [people_normalize_id(row) for row in list(player.tavern_management.breakfast.present_ids or [])]
                if self.name in breakfast_ids:
                    return "TavernKitchen"
            data_owner = getattr(self, "data", None)
            if data_owner is None:
                return ""
            scheduled_location = str(data_owner.getLocation(wday, hour) or "")
            if bool(getattr(self, "uses_tavern_client_room", False)) and scheduled_location == "TavernMain":
                if str(rooms.get("TavernMain").state.get("client_room_girl", "") or "") == self.name:
                    return "TavernClientRoom"
            return scheduled_location

        def isInLocation(self, location, wday=None, hour=None):
            return str(self.getLocation(wday, hour) or "") == str(location or "")

        def social_action_allowed(self, action="", item_id=""):
            action_key = str(action or "").strip().lower()
            if action_key in ("look", "talk"):
                return True
            allowed, reason = relationship_social_action_allowed(self.name, action_key, item_id)
            return bool(allowed)

    class BaseNPC(PeopleInfo):
        """Base for all NPCs (secondaries + simple)."""
        def __init__(self, name, **kwargs):
            super().__init__(name, **kwargs)
            if not self.unknown_name:
                self.unknown_name = str(getattr(self.__class__, "unknown_name", "") or "")
            self.jobs = {}
            self.skills = {}

        def skill_value(self, key, default=0):
            return people_to_int(self.skills.get(str(key or ""), default), default)

        def set_skill(self, key, value):
            self.skills[str(key or "")] = max(0, min(100, people_to_int(value, 0)))
            return self.skills[str(key or "")]

        def change_skill(self, key, amount=0):
            return self.set_skill(key, self.skill_value(key, 0) + people_to_int(amount, 0))

        def mark_known(self):
            self.known = True
            return True

        def display_name(self):
            if self.known:
                return str(people_display_name(self.name) or self.name)
            return str(getattr(self, "unknown_name", "") or self.name)

    class Girl(BaseNPC):
        """Girls with body layers, pregnancy, detailed history, lunar fertility."""
        registry_group = "girl"
        def __init__(self, name, **kwargs):
            super().__init__(name, **kwargs)
            self.detailed_sex_history = []

        def getLocation(self, wday=None, hour=None):
            if bool(household.barber_appointments.get(self.name, 0)) and barber_shop_is_open_at(wday, hour):
                return "BarberShop"
            return super(Girl, self).getLocation(wday, hour)

        def can_work_tavern(self):
            return people_to_int(self.jobs.get("jobWhoreAvail", 0), 0) > 0

        def set_hired(self, hired=True):
            hired_value = bool(hired)
            self.jobs["jobWhoreAvail"] = 1 if hired_value else 0
            self.jobs["jobwhore"] = 1 if hired_value else 0
            return hired_value

        def can_use_gloryhole(self):
            return people_to_int(self.jobs.get("jobGloryHoleAvail", 0), 0) > 0

        def portstreet_visible_now(self):
            return self.portstreet_work_active() and not self.portstreet_client_event_available()

        def mark_portstreet_clients_seen(self):
            self.var["portstreet_clients_seen_today"] = 1
            return self.set_story_value("seeclients", 1)

        def church_after_sermon_event_available(self):
            return (
                church_after_cermon_action_visible()
                and self.can_trigger_after_sermon_event()
                and CheckIfSexEventExist(self.code_name, 99, "Priest") > 0
            )

        def sex_clothing_state(self):
            state = getattr(self, "sex_state", None)
            return state if isinstance(state, dict) else {}

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

        def clothing_layer(self, layer):
            layer_key = str(layer or "").strip().lower()
            state = self.sex_clothing_state()
            dress = self.scene_dress()
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
            self.ensure_sex_state()["%s_removed" % layer_key] = 1
            return removed

        def reset_sex_clothing_state(self):
            state = self.ensure_sex_state()
            for key in ("top_removed", "bottom_removed", "bra_removed", "panties_removed", "top_raised", "bottom_raised"):
                state[key] = 0
            state.pop("dress_override", None)
            return self

        def tits_visible(self):
            return self.clothing_layer("bra") == "" and (self.clothing_layer("top") == "" or self.layer_raised("top"))

        def pussy_visible(self):
            return self.clothing_layer("panties") == "" and (self.clothing_layer("bottom") == "" or self.layer_raised("bottom"))

        def short_skirt_no_panties(self):
            return self.clothing_layer("panties") == "" and not self.layer_raised("bottom") and self.clothing_slut("bottom") >= 4

        def record_lick_pussy(self):
            state = self.ensure_sex_state()
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
                return dict(self.var.get("decision_results", {}).get(action_key, {}) or {})
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

default people = PeopleRegistry()

# Normal init python for the remaining runtime helpers (classes + core helpers already defined early above in this same file).
init python:
    def people_reset_daily_interactions(names=None):
        if names is None:
            reset_names = set(people.ids())
        else:
            reset_names = set([people_normalize_id(row) for row in list(names or [])])
        for person in sorted([row for row in reset_names if row]):
            info = people.get_info(person)
            if isinstance(info, PeopleInfo):
                info.reset_daily(True)
        return people

    def people_display_name(person=""):
        data = people.get_data(person)
        if data is not None:
            return str(data.cname or data.fullname or data.name)
        return people_normalize_id(person)

    def people_name(person="", grammatical_case="nominative", fallback=""):
        key = people_normalize_id(person)
        data = people.get_data(key)
        if data is None:
            return str(fallback or key)
        case_key = str(grammatical_case or "nominative").strip().lower()
        if case_key == "genitive":
            return str(data.genitive or data.fullname or data.cname or key)
        if case_key == "dative":
            return str(data.dative or data.fullname or data.cname or key)
        return str(data.cname or data.fullname or key)

    def people_age(person="", fallback=0):
        data = people.get_data(person)
        if data is None:
            return people_to_int(fallback, 0)
        age_value = data.age_years()
        return people_to_int(age_value, fallback)

    def people_birth_date(person=""):
        data = people.get_data(person)
        return dict(data.birth_date or {}) if data is not None else {}

    def people_gift_preferences(person=""):
        data = people.get_data(person)
        return list(data.gift_preferences or []) if data is not None else []

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
    call register_robin_secondary
    call register_zimmer_secondary
    call register_eddie_secondary
    call register_alber_secondary
    call register_francheska_secondary
    call register_luisa_secondary
    call register_sergio_secondary
    call register_gerhard_secondary
    call register_draupnir_secondary
    call register_mongol_secondary
    call InitDog
    call InitWerecat
    $ people.repair()
    $ npc_interval_schedule_load_all(True)
    return
