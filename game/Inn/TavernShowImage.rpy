# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Converted from TavernShowImage.txt

label TavernShowImage:
    $ rand_var = rand_int(1, 3)

    if rand_var == 1:
        $ _jobkitchen = getattr(renpy.store, 'jobkitchen', {})
        if int(_jobkitchen.get("melissa", 0) or 0) != 0:
            if rand_int(1, 4) == 1:
                python:
                    for p in [
                        "images/melissa/tavern/basement.png",
                        "images/tavern/storage/storage_room.png",
                        "images/tavern/kitchen/kitchen_room.png",
                    ]:
                        if renpy.loadable(p):
                            ShowImage("", "", p)
                            break
            else:
                $ _k = rand_int(0, 1)
                call ShowImage("", "", "images/melissa/tavern/melissa_kitchen_" + str(_k) + ".png")
        else:
            # Randomly pick from the full stack of Melissa waitress pictures every time.
            # No "main candidate + fallback" — we want variety across play sessions.
            python:
                waitress_pics = [
                    "images/melissa/tavern/waitress_0.png",
                    "images/melissa/tavern/waitress_1.jpg",
                    "images/melissa/tavern/waitress_2.jpg",
                    "images/melissa/tavern/waitress_3.jpg",
                    "images/melissa/tavern/waitress_4.png",
                ]
                available = [p for p in waitress_pics if renpy.loadable(p)]
                if available:
                    idx = rand_int(0, len(available) - 1)
                    ShowImage("", "", available[idx])
    elif rand_var == 2:
        call ShowImage("amanda", "tavern", "waitress" + str(rand_int(1, 5)))
    else:
        call ShowImage("sandra", "tavern", "waitress" + str(rand_int(1, 4)))

    return
