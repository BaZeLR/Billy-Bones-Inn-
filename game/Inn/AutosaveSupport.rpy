default _tractir_progress_revision = 0
default _tractir_last_autosave_reason = ""

init -114 python:
    import renpy.exports as renpy

    def mark_tractir_progress(reason=""):
        global _tractir_progress_revision, _tractir_last_autosave_reason

        _tractir_progress_revision = int(_tractir_progress_revision or 0) + 1
        if str(reason or "").strip():
            _tractir_last_autosave_reason = str(reason)
        return _tractir_progress_revision

    def _tractir_retain_live_progress():
        try:
            renpy.retain_after_load()
            return True
        except Exception:
            return False

    def request_tractir_autosave(reason="", take_screenshot=False, force=False):
        # Compatibility shim only.
        # This project is driven by room pause loops and screen actions.
        # Retain in-statement mutations so save/load and script reload restore
        # the current live state instead of the older room-entry checkpoint.
        mark_tractir_progress(reason)
        return _tractir_retain_live_progress()

    def checkpoint_tractir_progress(reason="", take_screenshot=False, force=False):
        mark_tractir_progress(reason)
        return _tractir_retain_live_progress()
