init -200 python:
    import renpy

    def tractir_restore_translation_marker():
        import renpy.minstore as renpy_minstore

        store = renpy.store
        if getattr(store, "_", None) is not renpy_minstore._:
            store._ = renpy_minstore._

    tractir_restore_translation_marker()

    for _tractir_reload_callback_list in (
        config.start_callbacks,
        config.after_load_callbacks,
        config.interact_callbacks,
        config.python_callbacks,
    ):
        if tractir_restore_translation_marker not in _tractir_reload_callback_list:
            _tractir_reload_callback_list.append(tractir_restore_translation_marker)
    del _tractir_reload_callback_list
