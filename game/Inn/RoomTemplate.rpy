default roomFirstVisit = {}

init -40 python:
    def get_registered_room(room_code=""):
        room_key = str(room_code or "").strip()
        if room_key == "":
            return None
        for maybe_room in list(globals().values()):
            try:
                maybe_code = object.__getattribute__(maybe_room, "code_name")
            except Exception:
                continue
            if str(maybe_code or "").strip() == room_key:
                return maybe_room
        return None


    def restore_room_runtime(room_code="", payload=None):
        restored = get_registered_room(room_code)
        if restored is None:
            restored = Room(code_name=room_code, display_name=room_code)

        payload = dict(payload or {})
        if "custom_properties" in payload:
            restored.custom_properties = dict(payload.get("custom_properties", {}) or {})
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
                    npc_state["known_condition"] = room_rule_serialize(npc_state.get("known_condition", None))
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

        def __reduce__(self):
            payload = {
                "custom_properties": dict(getattr(self, "custom_properties", {}) or {}),
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
