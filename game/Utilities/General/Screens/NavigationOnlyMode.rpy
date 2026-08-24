    def _disable_navigation_only_mode_after_load():
        store.NAVIGATION_ONLY_MODE = False

    if _disable_navigation_only_mode_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_disable_navigation_only_mode_after_load)