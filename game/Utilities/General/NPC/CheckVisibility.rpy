# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# CheckVisibility.rpy
# Converted from legacy script. Checks visibility of tits, pussy, and short skirt with no panties for a girl.
# All logic and assignments preserved and mapped to Ren'Py idioms.

init python:
    def check_visibility(girl_name):
        global TitsVisible, PussyVisible, ShortSkirtNoPanties
        if not isinstance(globals().get("TitsVisible", None), dict):
            TitsVisible = {}
        if not isinstance(globals().get("PussyVisible", None), dict):
            PussyVisible = {}
        if not isinstance(globals().get("ShortSkirtNoPanties", None), dict):
            ShortSkirtNoPanties = {}
        dress_part_slut = globals().get("DressPartSlut", {}) or {}
        TitsVisible[girl_name] = 0
        PussyVisible[girl_name] = 0
        ShortSkirtNoPanties[girl_name] = 0
        if bra.get(girl_name, '') == '' and (topdress.get(girl_name, '') == '' or topraised.get(girl_name, 0)):
            TitsVisible[girl_name] = 1
        if panties.get(girl_name, '') == '' and (bottomdress.get(girl_name, '') == '' or bottomraised.get(girl_name, 0)):
            PussyVisible[girl_name] = 1
        if panties.get(girl_name, '') == '' and int(bottomraised.get(girl_name, 0) or 0) == 0 and dress_part_slut.get(bottomdress.get(girl_name, ''), 0) >= 4:
            ShortSkirtNoPanties[girl_name] = 1

# Usage: check_visibility('liza')
# This will update the TitsVisible, PussyVisible, and ShortSkirtNoPanties dicts for the given girl.


label check_visibility(girl_name=""):
    $ check_visibility(girl_name)
    return


label CheckVisibility(girl_name=""):
    $ check_visibility(girl_name)
    return
