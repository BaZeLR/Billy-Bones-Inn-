default _tractir_progress_revision = 0
default _tractir_last_autosave_revision = -1
default _tractir_last_autosave_signature = ""
default _tractir_last_autosave_reason = ""
default _tractir_last_autosave_error = ""

init -114 python:
    import renpy
    import renpy.loadsave as renpy_loadsave

    def tractir_autosave_signature():
        store = renpy.store
        parts = [
            str(getattr(store, "CurLoc", "") or ""),
            str(getattr(store, "current_room_code", "") or ""),
            str(getattr(store, "current_object_id", "") or ""),
            str(getattr(store, "UI_mode", "") or ""),
            str(getattr(store, "day", 0) or 0),
            str(getattr(store, "week", 0) or 0),
            str(getattr(store, "hour", 0) or 0),
            str(getattr(store, "minute", 0) or 0),
            str(getattr(store, "time", 0) or 0),
        ]
        return "|".join(parts)

    def mark_tractir_progress(reason=""):
        store = renpy.store
        current_value = int(getattr(store, "_tractir_progress_revision", 0) or 0)
        store._tractir_progress_revision = current_value + 1
        if str(reason or "").strip():
            store._tractir_last_autosave_reason = str(reason)
        return store._tractir_progress_revision

    def request_tractir_autosave(reason="", take_screenshot=False, force=False):
        store = renpy.store

        if not renpy.config.has_autosave:
            return False
        if getattr(store, "main_menu", False):
            return False
        if not getattr(store, "_autosave", True):
            return False
        if getattr(store, "_in_replay", False):
            return False
        if str(getattr(store, "CurLoc", "") or "") == "Intro":
            return False

        current_signature = tractir_autosave_signature()
        current_revision = int(getattr(store, "_tractir_progress_revision", 0) or 0)
        last_revision = int(getattr(store, "_tractir_last_autosave_revision", -1) or -1)
        last_signature = str(getattr(store, "_tractir_last_autosave_signature", "") or "")

        if (not force) and current_revision <= last_revision and current_signature == last_signature:
            return False

        try:
            renpy_loadsave.force_autosave(take_screenshot=take_screenshot, block=True)
            store._tractir_last_autosave_revision = current_revision
            store._tractir_last_autosave_signature = current_signature
            store._tractir_last_autosave_error = ""
            if str(reason or "").strip():
                store._tractir_last_autosave_reason = str(reason)
            return True
        except Exception as exc:
            store._tractir_last_autosave_error = str(exc)
            return False

    def checkpoint_tractir_progress(reason="", take_screenshot=False, force=False):
        mark_tractir_progress(reason)
        return request_tractir_autosave(reason, take_screenshot, force)
