# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowBeckyPortrait():
    $ GirlName = "becky"
    python:
        TitsVisible.setdefault(GirlName, 0)
        PussyVisible.setdefault(GirlName, 0)
        check_visibility(GirlName)

    if TitsVisible.get(GirlName, 0) and PussyVisible.get(GirlName, 0):
        call ShowImage(GirlName, "portraits", "naked" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:12:1")))
    elif TitsVisible.get(GirlName, 0):
        call ShowImage(GirlName, "portraits", "nakedtits" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:14:2")))
    elif PussyVisible.get(GirlName, 0):
        call ShowImage(GirlName, "portraits", "nakedpussy" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:16:3")))
    else:
        call ShowImage(GirlName, "portraits", "portrait" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/ShowBeckyPortrait.rpy:procedural_randint:18:4")))
    return
