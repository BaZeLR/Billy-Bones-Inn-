# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# DressForNight.rpy
# Converted from legacy script. Sets a girl's clothing state for the night (naked, panties, or nightshirt).
# All logic and assignments preserved and mapped to Ren'Py idioms.

label dress_for_night(girl_name, mode):
    $ renpy.dynamic("_night_girl", "_night_state")
    # mode: 0 = nightshirt, 1 = panties, 2 = naked
    $ girl_name = str(girl_name or "").strip()
    $ _night_girl = people.get_info(girl_name)
    if _night_girl is None:
        return
    $ _night_state = _night_girl.sex_clothing_state()
    $ _night_girl.reset_sex_clothing_state()
    $ _night_state["bra_removed"] = 1
    $ _night_state["panties_removed"] = 1 if int(mode or 0) >= 2 else 0
    if mode == 0:
        $ _night_state["dress_override"] = "nightshirt"
    else:
        $ _night_state["dress_override"] = ""
    return

# Usage: call dress_for_night('liza', 0)  # 0=nightshirt, 1=panties, 2=naked
