# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default _tractir_progress_revision = 0
default _tractir_last_autosave_reason = ""

init -114 python:
    def mark_tractir_progress(reason=""):
        global _tractir_progress_revision, _tractir_last_autosave_reason

        _tractir_progress_revision = int(_tractir_progress_revision or 0) + 1
        if str(reason or "").strip():
            _tractir_last_autosave_reason = str(reason)
        return _tractir_progress_revision

    def request_tractir_autosave(reason="", take_screenshot=False, force=False):
        return mark_tractir_progress(reason)

    def checkpoint_tractir_progress(reason="", take_screenshot=False, force=False):
        return mark_tractir_progress(reason)
