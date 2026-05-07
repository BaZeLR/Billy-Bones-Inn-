# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowGeorgettPortrait():
    $ GirlName = "georgett"
    $ check_visibility(GirlName)

    if TitsVisible.get(GirlName, 0) == 0 and PussyVisible.get(GirlName, 0) == 0:
        call ShowImage(GirlName, "portraits", "portrait" + str(renpy.random.randint(1, 4)))
    elif TitsVisible.get(GirlName, 0) == 0 and PussyVisible.get(GirlName, 0) == 1:
        call ShowImage(GirlName, "portraits", "strip01")
    elif TitsVisible.get(GirlName, 0) == 1 and PussyVisible.get(GirlName, 0) == 0:
        call ShowImage(GirlName, "portraits", "strip10")
    elif TitsVisible.get(GirlName, 0) == 1 and PussyVisible.get(GirlName, 0) == 1:
        python:
            CurSperm0 = CumFaceOthers.get(GirlName, 0) + CumFaceYou.get(GirlName, 0)
            CurSperm1 = CumTitsYou.get(GirlName, 0) + CumTitsOthers.get(GirlName, 0)
            CurSperm2 = CumInsideYou.get(GirlName, 0) + CumInsideOthers.get(GirlName, 0)
        if CurSperm0 == 0 and CurSperm1 > 0 and CurSperm2 == 0:
            call ShowImage(GirlName, "portraits", "stripsperm010")
        elif CurSperm0 == 0 and CurSperm1 > 0 and CurSperm2 > 0:
            call ShowImage(GirlName, "portraits", "stripsperm011")
        elif CurSperm0 > 0 and CurSperm1 > 0 and CurSperm2 > 0:
            call ShowImage(GirlName, "portraits", "stripsperm111")
        elif CurSperm0 == 0 and CurSperm1 == 0 and CurSperm2 == 0:
            call ShowImage(GirlName, "portraits", "strip11")
    return
