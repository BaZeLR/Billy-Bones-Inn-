# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def CleanSpermRandom(girl_name):
        girl = str(girl_name or "")
        if not girl:
            return 0

        sluttiness = renpy.store.sluttiness
        CumInsideOthers = renpy.store.CumInsideOthers
        CumFaceOthers = renpy.store.CumFaceOthers
        CumTitsOthers = renpy.store.CumTitsOthers
        CumInsideYou = renpy.store.CumInsideYou
        CumFaceYou = renpy.store.CumFaceYou
        CumTitsYou = renpy.store.CumTitsYou

        CumInsideOthers[girl] = 0
        CumFaceOthers[girl] = 0
        CumTitsOthers[girl] = 0

        s = int(sluttiness.get(girl, 0) or 0)

        if s > 70:
            if renpy.random.randint(1, 3) == 1:
                CumFaceOthers[girl] = 0
                CumFaceYou[girl] = 0
            if renpy.random.randint(1, 6) == 1:
                CumTitsOthers[girl] = 0
                CumTitsYou[girl] = 0
            if renpy.random.randint(1, 10) == 1:
                CumInsideOthers[girl] = 0
                CumInsideYou[girl] = 0
        elif s > 40:
            if renpy.random.randint(1, 2) == 1:
                CumFaceOthers[girl] = 0
                CumFaceYou[girl] = 0
            if renpy.random.randint(1, 3) == 1:
                CumTitsOthers[girl] = 0
                CumTitsYou[girl] = 0
            if renpy.random.randint(1, 7) == 1:
                CumInsideOthers[girl] = 0
                CumInsideYou[girl] = 0
        elif s > 20:
            if renpy.random.randint(1, 10) <= 9:
                CumFaceOthers[girl] = 0
                CumFaceYou[girl] = 0
            if renpy.random.randint(1, 2) == 1:
                CumTitsOthers[girl] = 0
                CumTitsYou[girl] = 0
            if renpy.random.randint(1, 3) == 1:
                CumInsideOthers[girl] = 0
                CumInsideYou[girl] = 0
        else:
            CumFaceOthers[girl] = 0
            CumFaceYou[girl] = 0
            CumTitsOthers[girl] = 0
            CumTitsYou[girl] = 0
            if renpy.random.randint(1, 2) == 1:
                CumInsideOthers[girl] = 0
                CumInsideYou[girl] = 0

        return 0


label CleanSpermRandom(girl_name=""):
    $ _tmp_clean_sperm_random = CleanSpermRandom(girl_name)
    return
