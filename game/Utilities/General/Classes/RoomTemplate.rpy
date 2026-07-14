default roomFirstVisit = {}label MoveToRoom(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ move_cost = int(movement_minutes or 0)

    if _time_advancement_allowed():
        if move_cost > 0:
            $ calendar_v2.advance_minutes(move_cost)

    $ CurLoc = movement_target
    $ location = movement_target

    if renpy.has_label(movement_target):
        jump expression movement_target

    "DEBUG: missing target label [movement_target]"
    jump TavernMainlabel MoveToRoom(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ move_cost = int(movement_minutes or 0)

    if _time_advancement_allowed():
        $ calendar_v2.sync_state()
        if move_cost > 0:
            $ calendar_v2.advance_minutes(move_cost)

    $ CurLoc = movement_target
    $ location = movement_target

    if renpy.has_label(movement_target):
        jump expression movement_target

    "DEBUG: missing target label [movement_target]"
    jump TavernMaindefault roomFirstVisit = {}label MoveToRoom(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ move_cost = int(movement_minutes or 0)

    if _time_advancement_allowed():
        $ calendar_v2.sync_state()
        if move_cost > 0:
            $ calendar_v2.advance_minutes(move_cost)

    $ CurLoc = movement_target
    $ location = movement_target

    if renpy.has_label(movement_target):
        jump expression movement_target

    "DEBUG: missing target label [movement_target]"
    jump TavernMainlabel MoveToRoom(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ move_cost = int(movement_minutes or 0)

    if _time_advancement_allowed():
        $ calendar_v2.sync_state()
        if move_cost > 0:
            $ calendar_v2.advance_minutes(move_cost)

    $ CurLoc = movement_target
    $ location = movement_target

    if renpy.has_label(movement_target):
        jump expression movement_target

    "DEBUG: missing target label [movement_target]"
    jump TavernMaindefault roomFirstVisit = {}label MoveToRoom(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ move_cost = int(movement_minutes or 0)

    if _time_advancement_allowed():
        $ calendar_v2.sync_state()
        if move_cost > 0:
            $ calendar_v2.advance_minutes(move_cost)

    $ CurLoc = movement_target
    $ location = movement_target

    if renpy.has_label(movement_target):
        jump expression movement_target

    "DEBUG: missing target label [movement_target]"
    jump TavernMainlabel MoveToRoom(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ move_cost = int(movement_minutes or 0)

    if _time_advancement_allowed():
        $ calendar_v2.sync_state()
        if move_cost > 0:
            $ calendar_v2.advance_minutes(move_cost)

    $ CurLoc = movement_target
    $ location = movement_target

    if renpy.has_label(movement_target):
        jump expression movement_target

    "DEBUG: missing target label [movement_target]"
    jump TavernMain# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init -40 python:
    roomRegistry = {}
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
        room_obj = get_registered_room(room_key)
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
        for room_key in list(roomRegistry.keys()):
            if room_in_group(room_key, expected):
                out.append(room_key)
        return sorted(out)

    def register_room_runtime(room_obj=None):
        global roomRegistry

        if room_obj is None:
            return None

        room_code = str(getattr(room_obj, "code_name", "") or "").strip()
        if room_code == "":
            return room_obj

        roomRegistry[room_code] = room_obj
        return room_obj

    def get_registered_room(room_code=""):
        global roomRegistry

        room_key = str(room_code or "").strip()
        if room_key == "":
            return None
        return roomRegistry.get(room_key, None)


    def normalize_room_item_rows(rows=None):
        normalized = []
        for row in list(rows or []):
            item_id = get_object_id(row)
            if item_id:
                normalized.append(item_id)
        return normalized


    def restore_room_runtime(room_code="", payload=None):
        restored = get_registered_room(room_code)
        if restored is None:
            restored = object.__new__(Room)
            restored.code_name = str(room_code or "").strip()
            restored.room_id = restored.code_name
            restored.display_name = restored.code_name
            restored.bg_picture = ""
            restored.descriptions = []
            restored.exits = []
            restored.game_items = []
            restored.objects = restored.game_items
            restored.action_menus = []
            restored.schedule = None
            restored.custom_properties = {}
            restored.group_name = infer_room_group(restored.code_name)
            restored.is_hidden = False
            restored.is_locked = False
            restored.open_override = None

        payload = dict(payload or {})
        if "game_items" in payload:
            restored.game_items = normalize_room_item_rows(payload.get("game_items", []))
            restored.objects = restored.game_items
        if "is_hidden" in payload:
            restored.is_hidden = bool(payload.get("is_hidden", False))
        if "is_locked" in payload:
            restored.is_locked = bool(payload.get("is_locked", False))
        if "open_override" in payload:
            restored.open_override = payload.get("open_override", None)
        return restored

    class RoomExit(object):
        def __init__(self, label="", target="", condition=None, minutes_to_pass=5):
            self.label = str(label or "").strip()
            self.target = str(target or "").strip()
            self.condition = condition
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
            self.condition = condition
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
            self.condition = condition
            self.start = str(start or "")
            self.end = str(end or "")

        def _hour_value(self, value, default=0):
            text = str(value or "").strip()
            try:
                if ":" in text:
                    text = text.split(":", 1)[0]
                return max(0, min(23, int(text or default)))
            except Exception:
                return int(default or 0)

        def _end_hour_value(self, value, default=23):
            text = str(value or "").strip()
            hour_value = self._hour_value(text, default)
            if ":" in text:
                try:
                    minute_value = int(text.split(":", 1)[1] or 0)
                except Exception:
                    minute_value = 0
                if minute_value > 0:
                    return min(24, hour_value + 1)
            return hour_value

        def is_open(self, week_value=None):
            if not room_rule_true(self.condition):
                return False
            if week_value is None:
                calendar_v2.sync_state()
                week_value = calendar_v2.week
            if self.weekdays and int(week_value or 0) not in self.weekdays:
                return False
            start_text = str(getattr(self, "start", "") or "")
            end_text = str(getattr(self, "end", "") or "")
            if start_text or end_text:
                calendar_v2.sync_state()
                calendar_v2.sync_state()
                calendar_v2.sync_state()
                calendar_v2.sync_state()
                hour_value = int(calendar_v2.hour or 0) % 24
                start_value = self._hour_value(start_text, 0)
                end_value = self._end_hour_value(end_text, 23)
                if start_value <= end_value:
                    if not (start_value <= hour_value < end_value):
                        return False
                else:
                    if not (hour_value >= start_value or hour_value < end_value):
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
            objects=None,
            game_items=None,
            action_menus=None,
            schedule=None,
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
            self.game_items = normalize_room_item_rows(game_items or objects or [])
            self.objects = self.game_items
            self.action_menus = list(action_menus or [])
            self.schedule = schedule
            self.custom_properties = dict(custom_properties or {})
            self.group_name = str(group_name or infer_room_group(self.code_name)).strip().lower()
            self.is_hidden = bool(is_hidden)
            self.is_locked = bool(is_locked)
            self.open_override = open_override
            register_room_runtime(self)

        def is_first_visit(self):
            return not bool(roomFirstVisit.get(self.code_name, False))

        def mark_visited(self):
            roomFirstVisit[self.code_name] = True

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
                target_room = get_registered_room(getattr(row, "target", ""))
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

        def is_open(self, week_value=None):
            if self.open_override is not None:
                return bool(self.open_override)
            if self.schedule is None:
                return True
            if hasattr(self.schedule, "is_open"):
                return self.schedule.is_open(week_value)
            return True

        # ---------- NEW SHARED BUILDERS ----------

        def build_exit_items(self):
            items = []
            for ex in self.visible_exits():
                items.append(MenuItem(
                    ex.label,
                    Call("MoveToRoom", ex.target, getattr(ex, "minutes_to_pass", 5))
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
                        SetVariable("current_action_title", obj.name),
                        SetVariable("current_object_id", obj.object_id),
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
            items.extend(self.build_object_items())
            room_actions = self.visible_actions()
            for room_action in room_actions:
                menu_item = room_action_menu_item(room_action)
                if menu_item is not None:
                    items.append(menu_item)
            excluded_actions = [str(getattr(row, "action_id", "") or "").strip() for row in room_actions]
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
            state["objects"] = state["game_items"]
            state["action_menus"] = list(state.get("action_menus", []) or [])
            state["custom_properties"] = dict(state.get("custom_properties", {}) or {})
            state["is_hidden"] = bool(state.get("is_hidden", False))
            state["is_locked"] = bool(state.get("is_locked", False))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))
            self.game_items = normalize_room_item_rows(getattr(self, "game_items", []))
            self.objects = self.game_items

        def __reduce__(self):
            state = self.__getstate__()
            payload = {
                "game_items": normalize_room_item_rows(state.get("game_items", [])),
                "is_hidden": bool(state.get("is_hidden", False)),
                "is_locked": bool(state.get("is_locked", False)),
                "open_override": state.get("open_override", None),
            }
            return (restore_room_runtime, (str(getattr(self, "code_name", "") or ""), payload))


