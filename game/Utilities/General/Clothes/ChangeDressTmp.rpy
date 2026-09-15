# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def change_dress_tmp(girl_name="", dress_name=""):
        girl_key = str(girl_name or "").strip()
        dress = str(dress_name or "").strip()
        girl = people.get_info(girl_key)
        if girl is None or not dress:
            return
        girl.wear_temporary_dress(dress)

