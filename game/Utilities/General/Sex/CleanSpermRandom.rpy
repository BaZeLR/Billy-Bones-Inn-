# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def CleanSpermRandom(girl_name):
        girl = people.get_info(girl_name)
        if girl is None:
            return 0

        girl.clear_cum("cum_inside_others", "cum_face_others", "cum_tits_others")
        s = int(getattr(girl, "corruption", 0) or 0)

        if s > 70:
            if procedural_randint(1, 3, "clean_sperm_face_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_face_others", "cum_face_you")
            if procedural_randint(1, 6, "clean_sperm_tits_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_tits_others", "cum_tits_you")
            if procedural_randint(1, 10, "clean_sperm_inside_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_inside_others", "cum_inside_you")
        elif s > 40:
            if procedural_randint(1, 2, "clean_sperm_face_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_face_others", "cum_face_you")
            if procedural_randint(1, 3, "clean_sperm_tits_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_tits_others", "cum_tits_you")
            if procedural_randint(1, 7, "clean_sperm_inside_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_inside_others", "cum_inside_you")
        elif s > 20:
            if procedural_randint(1, 10, "clean_sperm_face_%s_%s" % (girl.code_name, int(current_game_day() or 0))) <= 9:
                girl.clear_cum("cum_face_others", "cum_face_you")
            if procedural_randint(1, 2, "clean_sperm_tits_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_tits_others", "cum_tits_you")
            if procedural_randint(1, 3, "clean_sperm_inside_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_inside_others", "cum_inside_you")
        else:
            girl.clear_cum("cum_face_others", "cum_face_you", "cum_tits_others", "cum_tits_you")
            if procedural_randint(1, 2, "clean_sperm_inside_%s_%s" % (girl.code_name, int(current_game_day() or 0))) == 1:
                girl.clear_cum("cum_inside_others", "cum_inside_you")

        return 0


label CleanSpermRandom(girl_name=""):
    $ renpy.dynamic("_tmp_clean_sperm_random")
    $ _tmp_clean_sperm_random = CleanSpermRandom(girl_name)
    return
