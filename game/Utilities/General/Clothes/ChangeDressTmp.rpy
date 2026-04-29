# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def change_dress_tmp(girl_name="", dress_name=""):
        girl = str(girl_name or "").strip()
        dress = str(dress_name or "").strip()
        if not girl or not dress:
            return
        topdress[girl] = DressTopPart.get(dress, "")
        bottomdress[girl] = DressBottomPart.get(dress, "")
        bodymodel_sync_character(girl)


label ChangeDressTmp(GirlNameDress="", DressName=""):
    if str(GirlNameDress or "") == "":
        python:
            _change_dress_tmp_args = _args if isinstance(_args, (list, tuple)) else ()
            if len(_change_dress_tmp_args) > 0:
                GirlNameDress = str(_change_dress_tmp_args[0] or "")
            if len(_change_dress_tmp_args) > 1:
                DressName = str(_change_dress_tmp_args[1] or "")

    $ change_dress_tmp(GirlNameDress, DressName)
    return
