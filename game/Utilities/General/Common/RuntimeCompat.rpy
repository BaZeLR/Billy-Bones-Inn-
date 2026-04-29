# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# RuntimeCompat.rpy
# Compatibility bridge has been retired.
# Domain logic and wrappers were moved to dedicated files:
# - Intro.rpy
# - CleanScreenFlow.rpy
# - AddOthersSperm.rpy
# - ShowImage.rpy
# - CheckVisibility.rpy
# - GetGirlDrunk.rpy
# - KidsPeekSexCompat.rpy
# - IntBeckyTalkTopics.rpy

label GetGirlDrunk(girl_name=""):
    call get_girl_drunk(girl_name)
    return

label girls_desc(girl_name=""):
    call GirlsDesc(girl_name)
    return

label amanda_legare_dance_sequence():
    call AmandaLegareDanceSequence
    return

label change_tomorrow_whore_job(girl_name=None):
    call ChangeTommorowWhoreJob(girl_name)
    return

label change_tomorrow_hall_job(girl_name=None):
    call ChangeTommorowHallJob(girl_name)
    return
