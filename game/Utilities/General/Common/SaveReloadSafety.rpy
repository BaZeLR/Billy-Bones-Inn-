# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -200 python:
    def tractir_reload_runtime_safety():
        # Keep reload-time safety side-effect free.
        # The UI uses ui_tr()/ensure_ui_translation_callable() directly, so there
        # is no need to rebind the global translation marker during Shift+R.
        return True
