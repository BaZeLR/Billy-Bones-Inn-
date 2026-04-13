# Converted from TavernShowImage.txt

label TavernShowImage:
    python:
        rand_var = renpy.random.randint(1, 3)

    if rand_var == 1:
        if int(jobkitchen.get("melissa", 0) or 0) != 0:
            if renpy.random.randint(1, 4) == 1:
                if renpy.loadable("images/melissa/tavern/basement.png"):
                    call ShowImage("", "", "images/melissa/tavern/basement.png")
                else:
                    call ShowImage("", "", "images/amanda/melissa_in storage.mp4")
            else:
                if renpy.random.randint(0, 1) == 0:
                    call ShowImage("", "", "images/melissa/tavern/melissa_kitchen_0.png")
                else:
                    call ShowImage("", "", "images/melissa/tavern/melissa_kitchen_1.png")
        else:
            $ _melissa_waitress = "images/melissa/tavern/waitress_" + str(renpy.random.randint(0, 4)) + (".png" if renpy.random.randint(0, 4) in (0, 4) else ".jpg")
            if not renpy.loadable(_melissa_waitress):
                python:
                    _fallback_candidates = [
                        "images/melissa/tavern/waitress_0.png",
                        "images/melissa/tavern/waitress_1.jpg",
                        "images/melissa/tavern/waitress_2.jpg",
                        "images/melissa/tavern/waitress_3.jpg",
                        "images/melissa/tavern/waitress_4.png",
                    ]
                    _fallback_candidates = [row for row in _fallback_candidates if renpy.loadable(row)]
                    _melissa_waitress = _fallback_candidates[0] if len(_fallback_candidates) > 0 else ""
            if str(_melissa_waitress or "").strip():
                call ShowImage("", "", _melissa_waitress)
    elif rand_var == 2:
        $ _img = "waitress" + str(renpy.random.randint(1, 5))
        call ShowImage("amanda", "tavern", _img)
    else:
        $ _img = "waitress" + str(renpy.random.randint(1, 4))
        call ShowImage("sandra", "tavern", _img)

    return
