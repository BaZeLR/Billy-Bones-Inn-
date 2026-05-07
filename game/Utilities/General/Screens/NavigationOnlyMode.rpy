# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default NAVIGATION_ONLY_MODE = False

init -200 python:
    import renpy.store as store

    def navigation_only_mode_enabled():
        # Navigation-only scaffolding is disabled for gameplay parity.
        return False

    def navigation_only_message():
        return "Режим навигации: взаимодействия и прочие действия временно отключены."

    def navigation_only_time_note():
        slot = int(getattr(store, "time", 0) or 0)
        if slot <= 0:
            part = "утро"
        elif slot == 1:
            part = "полдень"
        elif slot == 2:
            part = "день"
        elif slot == 3:
            part = "вечер"
        else:
            part = "ночь"
        return "Текущее время суток: {0}.".format(part)

    def _disable_navigation_only_mode_after_load():
        store.NAVIGATION_ONLY_MODE = False

    if _disable_navigation_only_mode_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_disable_navigation_only_mode_after_load)
