# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -49 python:
    game_item_registry = {}

    def restore_game_item_runtime(object_id="", payload=None):
        restored = get_game_item(object_id)
        if restored is None:
            restored = GameItem(object_id=object_id)

        payload = dict(payload or {})
        if "state" in payload:
            restored.state = dict(payload.get("state", {}) or {})
        if "hidden" in payload:
            restored.hidden = bool(payload.get("hidden", False))
        if "locked" in payload:
            restored.locked = bool(payload.get("locked", False))
        if "owner" in payload:
            restored.owner = str(payload.get("owner", "") or "")
        return restored


    class GameItem(GameObject):
        """Inventory/catalog specialization using the canonical object behavior."""

        def __init__(self, *args, **kwargs):
            super(GameItem, self).__init__(*args, **kwargs)
            if self.object_id:
                game_item_registry[self.object_id] = self

        def __reduce__(self):
            payload = {
                "state": dict(getattr(self, "state", {}) or {}),
                "hidden": bool(getattr(self, "hidden", False)),
                "locked": bool(getattr(self, "locked", False)),
                "owner": str(getattr(self, "owner", "") or ""),
            }
            return (restore_game_item_runtime, (str(getattr(self, "object_id", "") or ""), payload))
