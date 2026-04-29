# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.store as store
    import renpy.exports as renpy

    def add_others_sperm_apply(girl_name, chance):
        girl = str(girl_name or "")
        if girl == "":
            return 0

        chance_i = max(1, int(chance or 1))

        cum_inside_others = getattr(store, "CumInsideOthers", None)
        if not isinstance(cum_inside_others, dict):
            cum_inside_others = {}
            store.CumInsideOthers = cum_inside_others

        cum_face_others = getattr(store, "CumFaceOthers", None)
        if not isinstance(cum_face_others, dict):
            cum_face_others = {}
            store.CumFaceOthers = cum_face_others

        cum_tits_others = getattr(store, "CumTitsOthers", None)
        if not isinstance(cum_tits_others, dict):
            cum_tits_others = {}
            store.CumTitsOthers = cum_tits_others

        cum_inside_others[girl] = 0
        cum_face_others[girl] = 0
        cum_tits_others[girl] = 0

        if renpy.random.randint(1, chance_i * 2) == 1:
            cum_face_others[girl] = 1
        if renpy.random.randint(1, chance_i) == 1:
            cum_tits_others[girl] = 1
        if renpy.random.randint(1, chance_i * 2) == 1:
            cum_inside_others[girl] = 1
        return 0


label AddOthersSperm(girl_name="", chance=1):
    $ add_others_sperm_apply(girl_name, chance)
    return
