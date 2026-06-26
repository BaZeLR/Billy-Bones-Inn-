# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -200 python:
    import os
    import shutil

    def tractir_ensure_sync_persistent_file():
        savedir = str(getattr(renpy.config, "savedir", "") or "")
        if not savedir:
            return False

        sync_dir = os.path.join(savedir, "sync")
        root_persistent = os.path.join(savedir, "persistent")
        sync_persistent = os.path.join(sync_dir, "persistent")

        os.makedirs(sync_dir, exist_ok=True)
        if os.path.exists(sync_persistent):
            return True

        if os.path.exists(root_persistent):
            shutil.copyfile(root_persistent, sync_persistent)
        else:
            open(sync_persistent, "ab").close()

        return True

    def tractir_reload_runtime_safety():
        return tractir_ensure_sync_persistent_file()

    if tractir_ensure_sync_persistent_file not in config.start_callbacks:
        config.start_callbacks.append(tractir_ensure_sync_persistent_file)
    if tractir_ensure_sync_persistent_file not in config.after_load_callbacks:
        config.after_load_callbacks.append(tractir_ensure_sync_persistent_file)
