# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy

    def cock_position_apply(girl_name, position_=0, other_dude_name=""):
        girl = str(girl_name or "")
        if not girl:
            return 0

        dude = str(other_dude_name or "")
        if dude == "":
            dude = "You"

        try:
            pos = int(position_ or 0)
        except Exception:
            pos = 0

        in_pussy = 1 if pos == 1 else 0
        in_mouth = 1 if pos == 2 else 0
        in_tits = 1 if pos == 3 else 0

        pussy_attr = dude + "CockInPussy"
        mouth_attr = dude + "CockInMouth"
        tits_attr = dude + "CockInTits"

        pussy_dict = getattr(renpy.store, pussy_attr, None)
        mouth_dict = getattr(renpy.store, mouth_attr, None)
        tits_dict = getattr(renpy.store, tits_attr, None)

        if not isinstance(pussy_dict, dict):
            pussy_dict = {}
            setattr(renpy.store, pussy_attr, pussy_dict)
        if not isinstance(mouth_dict, dict):
            mouth_dict = {}
            setattr(renpy.store, mouth_attr, mouth_dict)
        if not isinstance(tits_dict, dict):
            tits_dict = {}
            setattr(renpy.store, tits_attr, tits_dict)

        pussy_dict[girl] = in_pussy
        mouth_dict[girl] = in_mouth
        tits_dict[girl] = in_tits
        return 0


label CockPosition(girl_name="", position_=0, other_dude_name=""):
    $ _tmp_cock_position_apply = cock_position_apply(girl_name, position_, other_dude_name)
    return


label cock_position(girl_name="", position_=0, other_dude_name=""):
    $ _tmp_cock_position_apply2 = cock_position_apply(girl_name, position_, other_dude_name)
    return
