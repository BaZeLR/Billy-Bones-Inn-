# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def adjust_otkroven(girl_name):
        info = getPersonInfo(girl_name)
        if info is None:
            return
        rel_value = people_to_int(getattr(info, "rel", 0), 0)
        open_value = 0
        if girl_name == 'georgett':
            if rel_value >= 5 and open_value <= 3:
                open_value = 3
            if rel_value >= 8 and open_value <= 5:
                open_value = 5
            if rel_value >= 9 and open_value <= 6:
                open_value = 6
            if rel_value >= 10 and open_value <= 7:
                open_value = 7
        elif girl_name == 'liza':
            if rel_value >= 4 and open_value <= 3:
                open_value = 3
            if rel_value >= 7 and open_value <= 5:
                open_value = 5
            if rel_value >= 6 and open_value <= 6:
                open_value = 6
            if rel_value >= 8 and open_value <= 7:
                open_value = 7
        elif girl_name in ['amanda', 'melissa', 'sandra']:
            if rel_value >= 6 and open_value <= 3:
                open_value = 3
            if rel_value >= 8 and open_value <= 5:
                open_value = 5
            if rel_value >= 11 and open_value <= 6:
                open_value = 6
            if rel_value >= 13 and open_value <= 7:
                open_value = 7
        else:
            if rel_value >= 6 and open_value <= 3:
                open_value = 3
            if rel_value >= 8 and open_value <= 5:
                open_value = 5
            if rel_value >= 11 and open_value <= 6:
                open_value = 6
            if rel_value >= 13 and open_value <= 7:
                open_value = 7
        info.openness = open_value
