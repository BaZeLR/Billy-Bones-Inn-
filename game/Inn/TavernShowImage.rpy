# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Converted from TavernShowImage.txt

label TavernShowImage:
    $ rand_var = rand_int(1, 3)

    if rand_var == 1:
        $ _jobkitchen = jobkitchen if isinstance(jobkitchen, dict) else {}
        if int(_jobkitchen.get("melissa", 0) or 0) != 0:
            if rand_int(1, 4) == 1:
                python:
                    for p in Melissa.image_sequence("tavern", "basement") + [
                        "images/tavern/storage/storage_room.png",
                        "images/tavern/kitchen/kitchen_room.png",
                    ]:
                        if renpy.loadable(p):
                            ShowImage("", "", p)
                            break
            else:
                $ _melissa_kitchen_pics = Melissa.image_sequence("kitchen", "work")
                if len(_melissa_kitchen_pics) > 0:
                    call ShowImage("", "", _melissa_kitchen_pics[rand_int(0, len(_melissa_kitchen_pics) - 1)])
        else:
            # Randomly pick from the full stack of Melissa waitress pictures every time.
            # No "main candidate + fallback" — we want variety across play sessions.
            python:
                available = Melissa.image_sequence("tavern", "waitress")
                if available:
                    idx = rand_int(0, len(available) - 1)
                    ShowImage("", "", available[idx])
    elif rand_var == 2:
        call ShowImage("amanda", "tavern", "waitress" + str(rand_int(1, 5)))
    else:
        call ShowImage("sandra", "tavern", "waitress" + str(rand_int(1, 4)))

    return
