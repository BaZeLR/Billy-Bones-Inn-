# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowBeckyPortrait(girl_name="becky"):
    if Becky.tits_visible() and Becky.pussy_visible():
        call ShowImage(girl_name, "portraits", "naked" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:12:1")))
    elif Becky.tits_visible():
        call ShowImage(girl_name, "portraits", "nakedtits" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:14:2")))
    elif Becky.pussy_visible():
        call ShowImage(girl_name, "portraits", "nakedpussy" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:16:3")))
    else:
        call ShowImage(girl_name, "portraits", "portrait" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:18:4")))
    return
