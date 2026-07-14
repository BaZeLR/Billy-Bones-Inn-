# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowAmandaPortrait():
    $ _amanda_portrait_picture = "images/amanda/amanda_portrait.jpg"
    if str(_amanda_portrait_picture or "").strip():
        $ scene_image = _amanda_portrait_picture
        $ _layout_last_picture = _amanda_portrait_picture
        vscene _amanda_portrait_picture
    return
