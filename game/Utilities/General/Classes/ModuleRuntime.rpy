# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default active_module_kind = ""
default active_module_return_label = ""
default active_module_return_room = ""
default active_module_actor = ""
default SomebodyCums = 0

init -42 python:
    def set_active_module(kind_code="", return_label="", return_room="", actor_id=""):
        renpy.store.active_module_kind = str(kind_code or "")
        renpy.store.active_module_return_label = str(return_label or "")
        renpy.store.active_module_return_room = str(return_room or "")
        renpy.store.active_module_actor = str(actor_id or "")

    def clear_active_module():
        set_active_module("", "", "", "")


label BeginPaidSexModule(girl_name="", return_room=""):
    hide screen main_ui
    $ set_active_module("sex", "", return_room, girl_name)
    if str(girl_name or "") == "":
        return
    $ Arousal[girl_name] = PussyWetStart.get(girl_name, 0)
    call CockPosition(girl_name, 0, "You")
    call CheckVisibility(girl_name)
    return


label FinishPaidSexModule(girl_name="", return_room=""):
    $ SomebodyCums = 0
    if str(girl_name or "") != "":
        call DressUp(girl_name)
    $ _module_return_room = str(return_room or active_module_return_room or "TavernMain")
    $ clear_active_module()
    call AdvanceTime(_module_return_room)
    return
