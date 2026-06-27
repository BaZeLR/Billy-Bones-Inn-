# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowAmandaPortrait():
    if Amanda.tits_visible() and Amanda.pussy_visible() and CurLoc == "TavernAmandaRoom":
        if player_state(False).intimacy.arousal_value("You") < 20:
            call ShowImage("amanda", "sexroom", "naked" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/ShowAmandaPortrait.rpy:procedural_randint:10:1")))
        else:
            call ShowImage("amanda", "sexroom", "nakedexcited" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/ShowAmandaPortrait.rpy:procedural_randint:12:2")))
    else:
        call ShowImage("amanda", "", "portrait")
    return
