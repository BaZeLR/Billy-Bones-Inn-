label ShowBeckyPortrait():
    $ GirlName = "becky"
    python:
        TitsVisible.setdefault(GirlName, 0)
        PussyVisible.setdefault(GirlName, 0)
        check_visibility(GirlName)

    if TitsVisible.get(GirlName, 0) and PussyVisible.get(GirlName, 0):
        call ShowImage(GirlName, "portraits", "naked" + str(renpy.random.randint(1, 3)))
    elif TitsVisible.get(GirlName, 0):
        call ShowImage(GirlName, "portraits", "nakedtits" + str(renpy.random.randint(1, 2)))
    elif PussyVisible.get(GirlName, 0):
        call ShowImage(GirlName, "portraits", "nakedpussy" + str(renpy.random.randint(1, 2)))
    else:
        $ _becky_portrait = renpy.random.choice([
            "images/becky/portraits/portrait_1.png",
            "images/becky/portraits/portrait_2.png",
            "images/becky/portraits/portrait_3.png",
            "images/becky/portraits/portrait_4.png",
        ])
        call ShowImage("", "", _becky_portrait)
    return
