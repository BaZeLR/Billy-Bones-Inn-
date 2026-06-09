default saveVersion = 1

define currentVersion = 2

init -100 python:
    def beforeLoadTractirSave():
        if "ensure_game_item_registry" in globals():
            ensure_game_item_registry()

    def syncTractirRuntimeState():
        if "ensure_game_item_registry" in globals():
            ensure_game_item_registry()
        if "sync_item_runtime_state" in globals():
            sync_item_runtime_state()
        if "sync_player_state_from_store" in globals():
            sync_player_state_from_store()
        if "TavernRatProblem" in globals() and isinstance(globals().get("WerecatVar", None), dict):
            if int(globals().get("TavernRatProblem", 0) or 0) == 0 and int(WerecatVar.get("rats_problem_active", 0) or 0) == 1:
                globals()["TavernRatProblem"] = 1
            WerecatVar["rats_problem_active"] = int(globals().get("TavernRatProblem", 0) or 0)

    def updateSave():
        global saveVersion

        try:
            loaded_version = int(saveVersion or 1)
        except Exception:
            loaded_version = 1

        if loaded_version < 2:
            updateSave_V1()
            loaded_version = 2

        syncTractirRuntimeState()
        saveVersion = int(currentVersion or loaded_version)

    def updateSave_V1():
        syncTractirRuntimeState()


label before_load:
    $ beforeLoadTractirSave()
    return


label after_load:
    $ updateSave()
    $ renpy.block_rollback()
    return
