# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# DressForNight.rpy
# Converted from legacy script. Sets a girl's clothing state for the night (naked, panties, or nightshirt).
# All logic and assignments preserved and mapped to Ren'Py idioms.

label dress_for_night(girl_name, mode):
    # mode: 0 = nightshirt, 1 = panties, 2 = naked
    $ legs[girl_name] = ''
    $ shoes[girl_name] = ''
    $ topraised[girl_name] = 0
    $ bottomraised[girl_name] = 0
    $ bra[girl_name] = ''
    if mode <= 1:
        $ panties[girl_name] = pantiesdef[girl_name]
    else:
        $ panties[girl_name] = ''
    if mode == 0:
        $ topdress[girl_name] = DressTopPart['nightshirt']
        $ bottomdress[girl_name] = DressBottomPart['nightshirt']
    else:
        $ topdress[girl_name] = ''
        $ bottomdress[girl_name] = ''
    $ bodymodel_sync_character(girl_name)
    return

# Usage: call dress_for_night('liza', 0)  # 0=nightshirt, 1=panties, 2=naked


label DressForNight(girl_name, mode):
    call dress_for_night(girl_name, mode)
    return
