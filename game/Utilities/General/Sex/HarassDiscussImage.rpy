# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label HarassDiscussImage(girl="", value=0):
    python:
        if girl == "melissa":
            if value == 0:
                renpy.call("ShowImage", girl, "grope", "scoldangry")
            elif value == 1:
                renpy.call("ShowImage", girl, "grope", "scoldneutral")
            else:
                renpy.call("ShowImage", girl, "grope", "scoldok")
        elif girl == "amanda":
            renpy.call("ShowImage", girl, "grope", "scold")
    return
