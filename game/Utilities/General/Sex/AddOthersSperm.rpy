# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def add_others_sperm_apply(girl_name, chance):
        girl = getPersonInfo(girl_name)
        if girl is None:
            return 0

        chance_i = max(1, int(chance or 1))
        girl.clear_cum("cum_inside_others", "cum_face_others", "cum_tits_others")

        if procedural_randint(1, chance_i * 2, "others_sperm_face_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
            girl.set_cum_state("cum_face_others", 1)
        if procedural_randint(1, chance_i, "others_sperm_tits_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
            girl.set_cum_state("cum_tits_others", 1)
        if procedural_randint(1, chance_i * 2, "others_sperm_inside_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
            girl.set_cum_state("cum_inside_others", 1)
        return 0


label AddOthersSperm(girl_name="", chance=1):
    $ add_others_sperm_apply(girl_name, chance)
    return
