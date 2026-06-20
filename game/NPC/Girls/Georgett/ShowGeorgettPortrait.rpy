# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowGeorgettPortrait():
    $ Georgett.refresh_sex_visibility()

    if not Georgett.visible_tits() and not Georgett.visible_pussy():
        call ShowImage("georgett", "portraits", "portrait" + str(renpy.random.randint(1, 4)))
    elif not Georgett.visible_tits() and Georgett.visible_pussy():
        call ShowImage("georgett", "portraits", "strip01")
    elif Georgett.visible_tits() and not Georgett.visible_pussy():
        call ShowImage("georgett", "portraits", "strip10")
    elif Georgett.visible_tits() and Georgett.visible_pussy():
        $ CurSperm0 = Georgett.cum_state("cum_face_others") + Georgett.cum_state("cum_face_you")
        $ CurSperm1 = Georgett.cum_state("cum_tits_you") + Georgett.cum_state("cum_tits_others")
        $ CurSperm2 = Georgett.cum_state("cum_inside_you") + Georgett.cum_state("cum_inside_others")
        if CurSperm0 == 0 and CurSperm1 > 0 and CurSperm2 == 0:
            call ShowImage("georgett", "portraits", "stripsperm010")
        elif CurSperm0 == 0 and CurSperm1 > 0 and CurSperm2 > 0:
            call ShowImage("georgett", "portraits", "stripsperm011")
        elif CurSperm0 > 0 and CurSperm1 > 0 and CurSperm2 > 0:
            call ShowImage("georgett", "portraits", "stripsperm111")
        elif CurSperm0 == 0 and CurSperm1 == 0 and CurSperm2 == 0:
            call ShowImage("georgett", "portraits", "strip11")
    return
