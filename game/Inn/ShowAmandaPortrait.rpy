label ShowAmandaPortrait():
    $ GirlName = "amanda"
    python:
        Arousal.setdefault("You", 0)
        TitsVisible.setdefault(GirlName, 0)
        PussyVisible.setdefault(GirlName, 0)
        check_visibility(GirlName)

    if TitsVisible.get(GirlName, 0) and PussyVisible.get(GirlName, 0) and CurLoc == "TavernAmandaRoom":
        if Arousal.get("You", 0) < 20:
            call ShowImage(GirlName, "sexroom", "naked" + str(renpy.random.randint(1, 3)))
        else:
            call ShowImage(GirlName, "sexroom", "nakedexcited" + str(renpy.random.randint(1, 2)))
    else:
        call ShowImage(GirlName, "", "portrait")
    return
