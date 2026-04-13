label ShowLizaPortrait():
    $ GirlName = "liza"
    $ check_visibility(GirlName)

    if TitsVisible.get(GirlName, 0) == 1 and PussyVisible.get(GirlName, 0) == 0:
        call ShowImage(GirlName, "portraits", "nakedtits" + str(renpy.random.randint(1, 2)))
    elif TitsVisible.get(GirlName, 0) == 1 and PussyVisible.get(GirlName, 0) == 1:
        python:
            CurSperm0 = CumFaceOthers.get(GirlName, 0) + CumFaceYou.get(GirlName, 0)
            CurSperm1 = CumTitsYou.get(GirlName, 0) + CumTitsOthers.get(GirlName, 0)
            CurSperm2 = CumInsideYou.get(GirlName, 0) + CumInsideOthers.get(GirlName, 0)
        if CurSperm0 > 0 and CurSperm1 > 0 and CurSperm2 > 0:
            call ShowImage(GirlName, "portraits", "cumall")
        elif CurSperm1 > 0:
            call ShowImage(GirlName, "portraits", "cumtits")
        elif CurSperm0 > 0:
            call ShowImage(GirlName, "portraits", "cumface")
        else:
            call ShowImage(GirlName, "portraits", "naked")
    return
