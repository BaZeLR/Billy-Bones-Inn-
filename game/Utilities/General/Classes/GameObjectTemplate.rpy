# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================


init -50 python:

    def room_rule_serialize(rule):
        if rule is None:
            return None
        if isinstance(rule, dict):
            return dict(rule)
        if callable(rule):
            rule_name = str(getattr(rule, "__name__", "") or "").strip()
            if rule_name and rule_name != "<lambda>":
                return {"__rule_type__": "callable_name", "name": rule_name}
            return None
        return rule


    def room_rule_resolve(rule):
        if isinstance(rule, dict) and str(rule.get("__rule_type__", "") or "") == "callable_name":
            rule_name = str(rule.get("name", "") or "").strip()
            if rule_name == "":
                return None
            if rule_name in globals():
                return globals().get(rule_name, None)
            if hasattr(renpy.store, rule_name):
                return getattr(renpy.store, rule_name)
            return None
        return rule


    def room_rule_true(rule, *args):
        rule = room_rule_resolve(rule)
        if rule is None:
            return True
        if callable(rule):
            try:
                return bool(rule(*args))
            except TypeError:
                return bool(rule())
        return bool(rule)


    def restore_game_object_runtime(object_id="", payload=None):
        restored = get_game_object(object_id)
        if restored is None:
            restored = get_game_item(object_id)
        if restored is None:
            restored = GameObject(object_id=object_id)

        payload = dict(payload or {})
        if "state" in payload:
            restored.state = dict(payload.get("state", {}) or {})
        if "custom_properties" in payload:
            restored.custom_properties = dict(payload.get("custom_properties", {}) or {})
        if "hidden" in payload:
            restored.hidden = bool(payload.get("hidden", False))
        if "locked" in payload:
            restored.locked = bool(payload.get("locked", False))
        if "owner" in payload:
            restored.owner = str(payload.get("owner", "") or "")
        return restored


    class RoomAction(object):
        def __init__(self, action_id="", label="", hook="jump", target="", args=None, condition=None, custom_properties=None):
            self.action_id = str(action_id or "").strip()
            self.label = str(label or "").strip()
            self.hook = str(hook or "jump").strip()
            self.target = str(target or "").strip()
            self.args = tuple(args or ())
            self.condition = condition
            self.custom_properties = dict(custom_properties or {})

        def is_visible(self, *args):
            return room_rule_true(self.condition, *args)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))


    class ObjectAction(RoomAction):
        pass


    class GameObject(object):
        def __init__(
            self,
            object_id="",
            name="",
            description="",
            actions=None,
            contents=None,
            state=None,
            condition=None,
            picture="",
            owner="",
            price=0,
            carriable=False,
            wearable=False,
            container=False,
            hidden=False,
            locked=False,
            insertable=False,
            portal=False,
            readable=False,
            usable=False,
            weapon=False,
            stackable=False,
            custom_properties=None,
        ):
            self.object_id = str(object_id or "").strip()
            self.code_name = self.object_id
            self.name = str(name or "").strip()
            self.description = str(description or "")
            self.actions = list(actions or [])
            self.contents = list(contents or [])
            self.state = dict(state or {})
            self.condition = condition
            self.picture = str(picture or "").strip()
            self.owner = str(owner or "").strip()
            self.price = int(price or 0)
            self.carriable = bool(carriable)
            self.wearable = bool(wearable)
            self.container = bool(container or bool(self.contents))
            self.hidden = bool(hidden)
            self.locked = bool(locked)
            self.insertable = bool(insertable)
            self.portal = bool(portal)
            self.readable = bool(readable)
            self.usable = bool(usable)
            self.weapon = bool(weapon)
            self.stackable = bool(stackable)
            self.custom_properties = dict(custom_properties or {})

        def is_visible(self):
            if self.hidden:
                return False
            visible_state = self.state.get("visible", None)
            if visible_state is not None and not bool(visible_state):
                return False
            return room_rule_true(self.condition)

        def is_locked(self):
            return bool(self.locked or self.state.get("locked", 0))

        def visible_actions(self):
            return [action for action in self.actions if hasattr(action, "is_visible") and action.is_visible(self)]

        def visible_contents(self):
            return [item for item in self.contents if room_rule_true(getattr(item, "condition", None))]

        def has_contents(self):
            return len(self.visible_contents()) > 0

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            state["actions"] = list(state.get("actions", []) or [])
            state["contents"] = list(state.get("contents", []) or [])
            state["state"] = dict(state.get("state", {}) or {})
            state["custom_properties"] = dict(state.get("custom_properties", {}) or {})
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))

        def __reduce__(self):
            payload = {
                "state": dict(getattr(self, "state", {}) or {}),
                "custom_properties": dict(getattr(self, "custom_properties", {}) or {}),
                "hidden": bool(getattr(self, "hidden", False)),
                "locked": bool(getattr(self, "locked", False)),
                "owner": str(getattr(self, "owner", "") or ""),
            }
            return (restore_game_object_runtime, (str(getattr(self, "object_id", "") or ""), payload))


    RoomObject = GameObject


    def get_object_id(value):
        if value is None:
            return ""
        if hasattr(value, "object_id"):
            return str(getattr(value, "object_id", "") or "").strip()
        if hasattr(value, "code_name"):
            return str(getattr(value, "code_name", "") or "").strip()
        if isinstance(value, str):
            return value.strip()
        return ""


    def get_game_object(object_id):
        object_id = get_object_id(object_id)
        if not object_id:
            return None
        for game_object in list(gameObjects or []):
            if get_object_id(game_object) == object_id:
                return game_object
        return None


    def get_game_item(item_id, room_obj=None):
        item_id = get_object_id(item_id)
        if not item_id:
            return None

        if "ensure_game_item_registry" in globals():
            ensure_game_item_registry()

        if "_all_game_item_objects" in globals():
            for game_item in list(_all_game_item_objects() or []):
                if get_object_id(game_item) == item_id:
                    return game_item

        if room_obj is not None and hasattr(room_obj, "game_items"):
            for row in list(getattr(room_obj, "game_items", []) or []):
                row_id = get_object_id(row)
                if row_id == item_id:
                    if hasattr(row, "name"):
                        return row
                    room_item = get_game_object(item_id)
                    if room_item is not None:
                        return room_item

        return get_game_object(item_id)
