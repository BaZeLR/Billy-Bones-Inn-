# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# CheckVisibility.rpy
# Visibility is derived directly from the NPC wardrobe and sex-clothing state.

init python:
    def check_visibility(girl_name):
        info = people.get_info(girl_name)
        if info is None:
            return {"tits": False, "pussy": False, "short_skirt_no_panties": False}
        return {
            "tits": bool(info.tits_visible()),
            "pussy": bool(info.pussy_visible()),
            "short_skirt_no_panties": bool(info.short_skirt_no_panties()),
        }

label check_visibility(girl_name=""):
    $ check_visibility(girl_name)
    return


