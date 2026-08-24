# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowGeorgettPortrait(cur_sperm_face=0, cur_sperm_tits=0, cur_sperm_inside=0):
    if not Georgett.tits_visible() and not Georgett.pussy_visible():
        call ShowImage("georgett", "portraits", "portrait" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Georgett/ShowGeorgettPortrait.rpy:procedural_randint:8:1")))
    elif not Georgett.tits_visible() and Georgett.pussy_visible():
        call ShowImage("georgett", "portraits", "strip01")
    elif Georgett.tits_visible() and not Georgett.pussy_visible():
        call ShowImage("georgett", "portraits", "strip10")
    elif Georgett.tits_visible() and Georgett.pussy_visible():
        $ cur_sperm_face = Georgett.cum_state("cum_face_others") + Georgett.cum_state("cum_face_you")
        $ cur_sperm_tits = Georgett.cum_state("cum_tits_you") + Georgett.cum_state("cum_tits_others")
        $ cur_sperm_inside = Georgett.cum_state("cum_inside_you") + Georgett.cum_state("cum_inside_others")
        if cur_sperm_face == 0 and cur_sperm_tits > 0 and cur_sperm_inside == 0:
            call ShowImage("georgett", "portraits", "stripsperm010")
        elif cur_sperm_face == 0 and cur_sperm_tits > 0 and cur_sperm_inside > 0:
            call ShowImage("georgett", "portraits", "stripsperm011")
        elif cur_sperm_face > 0 and cur_sperm_tits > 0 and cur_sperm_inside > 0:
            call ShowImage("georgett", "portraits", "stripsperm111")
        elif cur_sperm_face == 0 and cur_sperm_tits == 0 and cur_sperm_inside == 0:
            call ShowImage("georgett", "portraits", "strip11")
    return
