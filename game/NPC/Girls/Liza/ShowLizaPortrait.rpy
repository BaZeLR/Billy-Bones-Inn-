# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowLizaPortrait(girl_name="liza", cur_sperm_face=0, cur_sperm_tits=0, cur_sperm_inside=0):
    if Liza.tits_visible() and not Liza.pussy_visible():
        call ShowImage(girl_name, "portraits", "nakedtits" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/ShowLizaPortrait.rpy:procedural_randint:9:1")))
    elif Liza.tits_visible() and Liza.pussy_visible():
        python:
            cur_sperm_face = Liza.cum_state("cum_face_others") + Liza.cum_state("cum_face_you") + Liza.cum_state("cum_mouth_others") + Liza.cum_state("cum_mouth_you")
            cur_sperm_tits = Liza.cum_state("cum_tits_you") + Liza.cum_state("cum_tits_others")
            cur_sperm_inside = Liza.cum_state("cum_inside_you") + Liza.cum_state("cum_inside_others")
        if cur_sperm_face > 0 and cur_sperm_tits > 0 and cur_sperm_inside > 0:
            call ShowImage(girl_name, "portraits", "cumall")
        elif cur_sperm_tits > 0:
            call ShowImage(girl_name, "portraits", "cumtits")
        elif cur_sperm_face > 0:
            call ShowImage(girl_name, "portraits", "cumface")
        else:
            call ShowImage(girl_name, "portraits", "naked")
    else:
        call ShowImage(girl_name, "portraits", "naked")
    return
