# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -49 python:

    def restore_game_item_runtime(object_id="", payload=None):
        restored = get_game_item(object_id)
        if restored is None:
            restored = GameItem(object_id=object_id)

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

    class GameItem(object):
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
            return (restore_game_item_runtime, (str(getattr(self, "object_id", "") or ""), payload))
