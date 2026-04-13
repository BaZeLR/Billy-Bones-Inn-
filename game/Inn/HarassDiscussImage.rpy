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
