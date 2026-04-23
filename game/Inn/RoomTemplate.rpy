default roomFirstVisit = {}

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
            props = getattr(room_obj, "custom_properties", None)
            if isinstance(props, dict):
                group_value = str(props.get("group_name", "") or "").strip().lower()
                if group_value:
                    return group_value
        return infer_room_group(room_key)

    def current_room_group():
        room_key = str(getattr(CurrentRoom, "code_name", "") or CurLoc or "").strip()
        return room_group(room_key)

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


    def restore_room_runtime(room_code="", payload=None):
        restored = get_registered_room(room_code)
        if restored is None:
            restored = Room(code_name=room_code, display_name=room_code)

        payload = dict(payload or {})
        if "custom_properties" in payload:
            merged_properties = dict(getattr(restored, "custom_properties", {}) or {})
            merged_properties.update(dict(payload.get("custom_properties", {}) or {}))
            restored.custom_properties = merged_properties
        if "game_items" in payload:
            restored.game_items = list(payload.get("game_items", []) or [])
            restored.objects = restored.game_items
        if "npcs" in payload:
            restored.npcs = list(payload.get("npcs", []) or [])
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

    class RoomScene(object):
        def __init__(self, scene_id="", picture="", text="", condition=None):
            self.scene_id = str(scene_id or "").strip()
            self.picture = str(picture or "").strip()
            self.text = str(text or "")
            self.condition = condition

        def is_visible(self):
            return room_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))

    class RoomTrigger(object):
        def __init__(self, trigger_id="", condition=None, event_id="", hook="", target="", args=None, once=False):
            self.trigger_id = str(trigger_id or "").strip()
            self.condition = condition
            self.event_id = str(event_id or "").strip()
            self.hook = str(hook or "").strip()
            self.target = str(target or "").strip()
            self.args = tuple(args or ())
            self.once = bool(once)

        def is_ready(self):
            return room_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))


    class RoomSchedule(object):
        def __init__(self, weekdays=None, time_slots=None, closed_text="", condition=None):
            self.weekdays = list(weekdays or [])
            self.time_slots = list(time_slots or [])
            self.closed_text = str(closed_text or "")
            self.condition = condition

        def is_open(self, week_value, time_value):
            if not room_rule_true(self.condition):
                return False
            if self.weekdays and int(week_value or 0) not in self.weekdays:
                return False
            if self.time_slots and int(time_value or 0) not in self.time_slots:
                return False
            return True

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            state["weekdays"] = list(state.get("weekdays", []) or [])
            state["time_slots"] = list(state.get("time_slots", []) or [])
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
            npcs=None,
            action_menus=None,
            schedule=None,
            scenes=None,
            triggers=None,
            custom_properties=None,
            group_name="",
        ):
            self.code_name = str(code_name or "").strip()
            self.room_id = self.code_name
            self.display_name = str(display_name or self.code_name).strip()
            self.bg_picture = str(bg_picture or "").strip()
            self.picture = self.bg_picture
            self.descriptions = list(descriptions or [])
            self.exits = list(exits or [])
            self.game_items = list(game_items or objects or [])
            self.objects = self.game_items
            self.npcs = list(npcs or [])
            self.action_menus = list(action_menus or [])
            self.schedule = schedule
            self.scenes = list(scenes or [])
            self.triggers = list(triggers or [])
            self.custom_properties = dict(custom_properties or {})
            self.group_name = str(group_name or self.custom_properties.get("group_name", "") or infer_room_group(self.code_name)).strip().lower()
            if self.group_name:
                self.custom_properties["group_name"] = self.group_name
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
            return [row for row in self.exits if hasattr(row, "is_visible") and row.is_visible()]

        def visible_objects(self):
            out = []
            for row in self.game_items:
                room_object = row
                if isinstance(row, str):
                    room_object = get_game_object(row)
                if room_object is not None and hasattr(room_object, "is_visible") and room_object.is_visible():
                    out.append(room_object)
            return out

        def visible_game_items(self):
            return self.visible_objects()

        def visible_npcs(self):
            out = []
            for npc in self.npcs:
                if isinstance(npc, dict):
                    if room_rule_true(npc.get("condition", None)):
                        out.append(npc)
                    continue
                if hasattr(npc, "condition"):
                    if room_rule_true(getattr(npc, "condition", None)):
                        out.append(npc)
                    continue
                if isinstance(npc, str) and str(npc).strip():
                    out.append(npc)
            return out

        def visible_actions(self):
            return [row for row in self.action_menus if hasattr(row, "is_visible") and row.is_visible()]

        def visible_scenes(self):
            return [row for row in self.scenes if hasattr(row, "is_visible") and row.is_visible()]

        def ready_triggers(self):
            return [row for row in self.triggers if hasattr(row, "is_ready") and row.is_ready()]

        def is_open(self, week_value, time_value):
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
                    Call("MoveToRoom", ex.target, getattr(ex, "minutes_to_pass", 5))
                ))
            return items

        def build_object_items(self):
            items = []
            object_menu_label = str(self.custom_properties.get("object_menu_label", "") or "")
            if not object_menu_label:
                return items

            for obj in self.visible_objects():
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
            # Hook for room-specific additions.
            return []

        def build_action_items(self):
            items = []
            items.extend(self.build_object_items())
            items.extend(self.build_extra_action_items())
            return items

        def build_menu_sections(self):
            return {
                "movement": self.build_exit_items(),
                "actions": self.build_action_items(),
            }

        def __getstate__(self):
            state = dict(self.__dict__)
            serialized_npcs = []
            for npc in list(state.get("npcs", []) or []):
                if isinstance(npc, dict):
                    npc_state = dict(npc)
                    npc_state["condition"] = room_rule_serialize(npc_state.get("condition", None))
                    serialized_npcs.append(npc_state)
                else:
                    serialized_npcs.append(npc)
            state["npcs"] = serialized_npcs
            state["descriptions"] = list(state.get("descriptions", []) or [])
            state["exits"] = list(state.get("exits", []) or [])
            state["game_items"] = list(state.get("game_items", []) or [])
            state["objects"] = list(state.get("objects", []) or [])
            state["action_menus"] = list(state.get("action_menus", []) or [])
            state["scenes"] = list(state.get("scenes", []) or [])
            state["triggers"] = list(state.get("triggers", []) or [])
            state["custom_properties"] = dict(state.get("custom_properties", {}) or {})
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))
            register_room_runtime(self)

        def __reduce__(self):
            state = self.__getstate__()
            payload = {
                "custom_properties": dict(state.get("custom_properties", {}) or {}),
                "game_items": list(state.get("game_items", []) or []),
                "npcs": list(state.get("npcs", []) or []),
            }
            return (restore_room_runtime, (str(getattr(self, "code_name", "") or ""), payload))
label MoveToRoom(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ move_cost = int(movement_minutes or 0)

    if _time_advancement_allowed():
        $ ensure_calendar_state()
        if move_cost > 0:
            $ calendar_advance_minutes(move_cost)

    $ CurLoc = movement_target
    $ location = movement_target

    if renpy.has_label(movement_target):
        jump expression movement_target

    "DEBUG: missing target label [movement_target]"
    jump TavernMain
