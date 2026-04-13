init python:
    import renpy.store as store
    import renpy.exports as renpy_module

    def add_clean_screen_apply():
        # Legacy compatibility shim. In the current main_ui flow there is no
        # separate overflow-clearing screen stack to maintain.
        if hasattr(store, "MainTxt"):
            store.CurLocDesc = getattr(store, "MainTxt", "")
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()
        return 0

    def clean_screen_overflow_apply(lines=1):
        # Legacy no-op. Old QSP conversions still call this label heavily, but
        # current Ren'Py UI does not consume CounterToClean at all.
        return 0


label AddCleanScreen:
    $ add_clean_screen_apply()
    return


label add_clean_screen:
    call AddCleanScreen
    return


label AddCleanScreenButton:
    return


label CleanScreenOverflow(args0=1):
    $ clean_screen_overflow_apply(args0)
    return


label clean_screen_overflow(args0=1):
    $ clean_screen_overflow_apply(args0)
    return
