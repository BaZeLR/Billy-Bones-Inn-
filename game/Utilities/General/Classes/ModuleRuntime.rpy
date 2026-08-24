# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label BeginPaidSexModule(girl_name="", actor_location="", _module_actor_info=None):
    if str(girl_name or "") == "":
        return
    $ _module_actor_info = people.get_info(girl_name)
    $ _module_actor_info.set_arousal(_module_actor_info.sex_stat("PussyWetStart", 0))
    call CockPosition(girl_name, 0, "You")
    call check_visibility(girl_name)
    return


label FinishPaidSexModule(girl_name="", actor_location=""):
    if str(girl_name or "") != "":
        call DressUp(girl_name)
    call AdvanceTimeOnly(40)
    return
