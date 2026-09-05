# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init -40 python:
    import copy

    roomDefinitions = {}
    ROOM_GROUP_TAVERN = "tavern"
    ROOM_GROUP_CITY = "city"
    ROOM_GROUP_FOREST = "forest"
    ROOM_GROUP_OTHER = "other"

    roomGroupOverrides = {
        "Backyard": ROOM_GROUP_TAVERN,
        "Shed": ROOM_GROUP_TAVERN,
        "StreetTavern": ROOM_GROUP_CITY,
        "MarketPlace": ROOM_GROUP_CITY,
        "PortStreets": ROOM_GROUP_CITY,
        "Church": ROOM_GROUP_CITY,
        "BarberShop": ROOM_GROUP_CITY,
        "DressShop": ROOM_GROUP_CITY,
        "GroceryStore": ROOM_GROUP_CITY,
        "HunterClub": ROOM_GROUP_CITY,
        "WineStore": ROOM_GROUP_CITY,
        "BeckyHome": ROOM_GROUP_CITY,
        "BeckyHomeFront": ROOM_GROUP_CITY,
        "EllonaTemple": ROOM_GROUP_CITY,
        "TempleCloister": ROOM_GROUP_CITY,
        "Cemetery": ROOM_GROUP_CITY,
        "StolyarWorkshop": ROOM_GROUP_CITY,
        "FridayDance": ROOM_GROUP_CITY,
        "Forest": ROOM_GROUP_FOREST,
        "ForestClearing": ROOM_GROUP_FOREST,
        "ForestLake": ROOM_GROUP_FOREST,
        "ForestSpring": ROOM_GROUP_FOREST,
        "ForestWaterfall": ROOM_GROUP_FOREST,
        "ForestHiddenPath": ROOM_GROUP_FOREST,
        "ForestDarkWoods": ROOM_GROUP_FOREST,
        "ForestCave": ROOM_GROUP_FOREST,
    }

    class RoomRegistry(object):
        """Saved owner of the one runtime Room instance for each room code."""

        def __init__(self):
            self.runtime = {}
            self.current_code = "TavernMain"
            self.repair()

        def register(self, room_obj):
            if room_obj is None:
                raise ValueError("RoomRegistry.register requires a Room")
            room_code = str(getattr(room_obj, "code_name", "") or "").strip()
            if room_code == "":
                raise ValueError("Registered room must have a stable code_name")
            self.runtime[room_code] = room_obj
            return room_obj

        def get(self, room_code=""):
            return self.runtime.get(str(room_code or "").strip(), None)

        @property
        def current(self):
            return self.get(self.current_code)

        def enter(self, room_code=""):
            self.current_code = str(room_code or "").strip()
            return self.current

        def keys(self):
            return self.runtime.keys()

        def values(self):
            return self.runtime.values()

        def items(self):
            return self.runtime.items()

        def repair(self):
            if not hasattr(self, "current_code"):
                self.current_code = "TavernMain"
            for room_code, definition in list(roomDefinitions.items()):
                if room_code not in self.runtime:
                    self.register(definition.runtime_copy())
            return self

        def __len__(self):
            return len(self.runtime)

        def __contains__(self, room_code):
            return str(room_code or "").strip() in self.runtime

        def __getitem__(self, room_code):
            return self.runtime[str(room_code or "").strip()]

    def infer_room_group(room_code=""):
        room_key = str(room_code or "").strip()
        if room_key == "":
            return ROOM_GROUP_OTHER
        if room_key in roomGroupOverrides:
            return str(roomGroupOverrides.get(room_key, ROOM_GROUP_OTHER) or ROOM_GROUP_OTHER)
        if room_key.startswith("Tavern"):
            return ROOM_GROUP_TAVERN
        if room_key.startswith("Forest"):
            return ROOM_GROUP_FOREST
        return ROOM_GROUP_OTHER

    def room_group(room_code=""):
        room_key = str(room_code or "").strip()
        if room_key == "":
            return ROOM_GROUP_OTHER
        room_obj = rooms.get(room_key)
        if room_obj is not None:
            group_value = str(getattr(room_obj, "group_name", "") or "").strip().lower()
            if group_value:
                return group_value
        return infer_room_group(room_key)

    def room_in_group(room_code="", group_name=""):
        expected = str(group_name or "").strip().lower()
        if expected == "":
            return False
        return room_group(room_code) == expected

    def rooms_in_group(group_name=""):
        expected = str(group_name or "").strip().lower()
        if expected == "":
            return []
        out = []
        for room_key in list(rooms.keys()):
            if room_in_group(room_key, expected):
                out.append(room_key)
        return sorted(out)

    def normalize_room_item_rows(rows=None):
        normalized = []
        for row in list(rows or []):
            item_id = get_object_id(row)
            if item_id:
                normalized.append(item_id)
        return normalized


    def restore_room_runtime(room_code="", payload=None):
        restored = rooms.get(room_code)
        if restored is None:
            restored = object.__new__(Room)
            restored.code_name = str(room_code or "").strip()
            restored.room_id = restored.code_name
            restored.display_name = restored.code_name
            restored.bg_picture = ""
            restored.descriptions = []
            restored.exits = []
            restored.game_items = []
            restored.action_menus = []
            restored.schedule = None
            restored.state = {}
            restored.custom_properties = {}
            restored.group_name = infer_room_group(restored.code_name)
            restored.is_hidden = False
            restored.is_locked = False
            restored.open_override = None

        payload = dict(payload or {})
        legacy_objects = payload.pop("objects", None)
        if "game_items" in payload or legacy_objects is not None:
            restored.game_items = normalize_room_item_rows(payload.get("game_items", legacy_objects or []))
        if "is_hidden" in payload:
            restored.is_hidden = bool(payload.get("is_hidden", False))
        if "is_locked" in payload:
            restored.is_locked = bool(payload.get("is_locked", False))
        if "open_override" in payload:
            restored.open_override = payload.get("open_override", None)
        if "state" in payload:
            restored.state = dict(payload.get("state", {}) or {})
        return restored

    class RoomExit(object):
        def __init__(self, label="", target="", condition=None, minutes_to_pass=5):
            self.label = str(label or "").strip()
            self.target = str(target or "").strip()
            self.condition = register_room_rule(condition)
            self.minutes_to_pass = int(minutes_to_pass or 5)  # Time to pass through exit

        def is_visible(self):
            return room_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))

    class RoomDescription(object):
        def __init__(self, text="", condition=None, first_time=False, priority=0):
            self.text = str(text or "")
            self.condition = register_room_rule(condition)
            self.first_time = bool(first_time)
            self.priority = int(priority or 0)

        def is_visible(self, is_first_visit=False):
            if self.first_time and not is_first_visit:
                return False
            return room_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))

    class RoomSchedule(object):
        def __init__(self, weekdays=None, closed_text="", condition=None, start="", end=""):
            self.weekdays = list(weekdays or [])
            self.closed_text = str(closed_text or "")
            self.condition = register_room_rule(condition)
            self.start = str(start or "")
            self.end = str(end or "")

        def _clock_value(self, value, default=0):
            text = str(value or "").strip()
            try:
                if text == "":
                    return int(default or 0)
                if ":" in text:
                    hour_text, minute_text = text.split(":", 1)
                    return (max(0, min(23, int(hour_text or 0))) * 60) + max(0, min(59, int(minute_text or 0)))
                return max(0, min(23, int(text or 0))) * 60
            except Exception:
                return int(default or 0)

        def is_open(self, week_value=None, time_value=None):
            if not room_rule_true(self.condition):
                return False
            if week_value is None:
                week_value = calendar_v2.week
            if self.weekdays and int(week_value or 0) not in self.weekdays:
                return False
            start_text = str(getattr(self, "start", "") or "")
            end_text = str(getattr(self, "end", "") or "")
            if start_text or end_text:
                if time_value is None:
                    current_value = (int(calendar_v2.hour or 0) % 24) * 60 + (int(calendar_v2.minute or 0) % 60)
                else:
                    explicit_value = int(time_value or 0)
                    current_value = explicit_value * 60 if 0 <= explicit_value <= 23 else explicit_value % 1440
                start_value = self._clock_value(start_text, 0)
                end_value = self._clock_value(end_text, 1439)
                if start_value <= end_value:
                    if not (start_value <= current_value <= end_value):
                        return False
                else:
                    if not (current_value >= start_value or current_value <= end_value):
                        return False
            return True

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            state["weekdays"] = list(state.get("weekdays", []) or [])
            state["start"] = str(state.get("start", "") or "")
            state["end"] = str(state.get("end", "") or "")
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))


    class Room(object):
        def __init__(
            self,
            code_name="",
            display_name="",
            bg_picture="",
            descriptions=None,
            exits=None,
            game_items=None,
            action_menus=None,
            schedule=None,
            state=None,
            custom_properties=None,
            group_name="",
            is_hidden=False,
            is_locked=False,
            open_override=None,
        ):
            self.code_name = str(code_name or "").strip()
            self.room_id = self.code_name
            self.display_name = str(display_name or self.code_name).strip()
            self.bg_picture = str(bg_picture or "").strip()
            self.descriptions = list(descriptions or [])
            self.exits = list(exits or [])
            self.game_items = normalize_room_item_rows(game_items or [])
            self.action_menus = list(action_menus or [])
            self.schedule = schedule
            self.state = dict(state or {})
            self.state.setdefault("visited", False)
            self.custom_properties = dict(custom_properties or {})
            self.group_name = str(group_name or infer_room_group(self.code_name)).strip().lower()
            self.is_hidden = bool(is_hidden)
            self.is_locked = bool(is_locked)
            self.open_override = open_override
            roomDefinitions[self.code_name] = self

        def runtime_copy(self):
            restored = object.__new__(self.__class__)
            restored.__dict__.update(dict(self.__dict__))
            restored.descriptions = list(self.descriptions or [])
            restored.exits = list(self.exits or [])
            restored.game_items = list(self.game_items or [])
            restored.action_menus = list(self.action_menus or [])
            restored.state = copy.deepcopy(dict(self.state or {}))
            restored.custom_properties = copy.deepcopy(dict(self.custom_properties or {}))
            return restored

        def is_first_visit(self):
            return not bool(self.state.get("visited", False))

        def mark_visited(self):
            self.state["visited"] = True

        def visible_descriptions(self):
            first_visit_now = self.is_first_visit()
            rows = [row for row in self.descriptions if hasattr(row, "is_visible") and row.is_visible(first_visit_now)]
            rows.sort(key=lambda row: int(getattr(row, "priority", 0) or 0), reverse=True)
            return rows

        def visible_exits(self):
            out = []
            for row in self.exits:
                if not hasattr(row, "is_visible") or not row.is_visible():
                    continue
                target_room = rooms.get(getattr(row, "target", ""))
                if target_room is not None and bool(getattr(target_room, "is_hidden", False)):
                    continue
                out.append(row)
            return out

        def visible_objects(self):
            out = []
            for row in self.game_items:
                room_object = row
                if isinstance(row, str):
                    room_object = get_game_object(row)
                    if room_object is None:
                        room_object = get_game_item(row)
                if room_object is not None and hasattr(room_object, "is_visible") and room_object.is_visible():
                    out.append(room_object)
            return out

        def visible_game_items(self):
            return self.visible_objects()

        def visible_actions(self):
            return [row for row in self.action_menus if hasattr(row, "is_visible") and row.is_visible()]

        def is_open(self, week_value=None, time_value=None):
            if self.open_override is not None:
                return bool(self.open_override)
            if self.schedule is None:
                return True
            if hasattr(self.schedule, "is_open"):
                return self.schedule.is_open(week_value, time_value)
            return True

        # ---------- NEW SHARED BUILDERS ----------

        def build_exit_items(self):
            items = []
            for ex in self.visible_exits():
                items.append(MenuItem(
                    ex.label,
                    movement_actions(ex.target, getattr(ex, "minutes_to_pass", 5))
                ))
            return items

        def build_object_items(self):
            items = []
            room_object_menu_label = str(self.custom_properties.get("object_menu_label", "") or "")

            for obj in self.visible_objects():
                object_props = getattr(obj, "custom_properties", {}) or {}
                object_menu_label = str(object_props.get("object_menu_label", "") or room_object_menu_label)
                if not object_menu_label:
                    continue
                items.append(MenuItem(
                    obj.name,
                    [
                        SetField(main_ui_runtime, "action_title", obj.name),
                        SetField(main_ui_runtime, "object_id", obj.object_id),
                        Call(object_menu_label, obj.object_id),
                    ]
                ))
            return items

        def build_extra_action_items(self):
            items = []
            for room_action in self.visible_actions():
                menu_item = room_action_menu_item(room_action)
                if menu_item is not None:
                    items.append(menu_item)
            return items

        def build_action_items(self):
            items = []
            visible_objects = self.visible_objects()
            items.extend(self.build_object_items())
            room_actions = self.visible_actions()
            for room_action in room_actions:
                menu_item = room_action_menu_item(room_action)
                if menu_item is not None:
                    items.append(menu_item)
            excluded_actions = [str(getattr(row, "action_id", "") or "").strip() for row in room_actions]
            excluded_actions.extend([str(getattr(row, "object_id", "") or "").strip() for row in visible_objects])
            items.extend(story_event_action_items(self.code_name, excluded_actions))
            return items

        def build_menu_sections(self):
            return {
                "movement": self.build_exit_items(),
                "actions": self.build_action_items(),
            }

        def __getstate__(self):
            state = dict(self.__dict__)
            state.pop("npcs", None)
            state["descriptions"] = list(state.get("descriptions", []) or [])
            state["exits"] = list(state.get("exits", []) or [])
            state["game_items"] = normalize_room_item_rows(state.get("game_items", []))
            state.pop("objects", None)
            state["action_menus"] = list(state.get("action_menus", []) or [])
            state["state"] = dict(state.get("state", {}) or {})
            state["custom_properties"] = dict(state.get("custom_properties", {}) or {})
            state["is_hidden"] = bool(state.get("is_hidden", False))
            state["is_locked"] = bool(state.get("is_locked", False))
            return state

        def __setstate__(self, state):
            restored = dict(state or {})
            legacy_objects = restored.pop("objects", None)
            self.__dict__.update(restored)
            self.game_items = normalize_room_item_rows(getattr(self, "game_items", legacy_objects or []))
            self.state = dict(getattr(self, "state", {}) or {})

        def __reduce__(self):
            state = self.__getstate__()
            payload = {
                "game_items": normalize_room_item_rows(state.get("game_items", [])),
                "is_hidden": bool(state.get("is_hidden", False)),
                "is_locked": bool(state.get("is_locked", False)),
                "open_override": state.get("open_override", None),
                "state": dict(state.get("state", {}) or {}),
            }
            return (restore_room_runtime, (str(getattr(self, "code_name", "") or ""), payload))

default rooms = RoomRegistry()
