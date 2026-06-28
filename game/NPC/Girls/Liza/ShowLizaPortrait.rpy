# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowLizaPortrait():
    $ GirlName = "liza"
    $ Liza.publish_visibility_state()

    if Liza.tits_visible() and not Liza.pussy_visible():
        call ShowImage(GirlName, "portraits", "nakedtits" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/ShowLizaPortrait.rpy:procedural_randint:9:1")))
    elif Liza.tits_visible() and Liza.pussy_visible():
        python:
            CurSperm0 = Liza.cum_state("cum_face_others") + Liza.cum_state("cum_face_you") + Liza.cum_state("cum_mouth_others") + Liza.cum_state("cum_mouth_you")
            CurSperm1 = Liza.cum_state("cum_tits_you") + Liza.cum_state("cum_tits_others")
            CurSperm2 = Liza.cum_state("cum_inside_you") + Liza.cum_state("cum_inside_others")
        if CurSperm0 > 0 and CurSperm1 > 0 and CurSperm2 > 0:
            call ShowImage(GirlName, "portraits", "cumall")
        elif CurSperm1 > 0:
            call ShowImage(GirlName, "portraits", "cumtits")
        elif CurSperm0 > 0:
            call ShowImage(GirlName, "portraits", "cumface")
        else:
            call ShowImage(GirlName, "portraits", "naked")
    return
