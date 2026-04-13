label PartEventAfterHarrassment(GirlNamePEAH, GirlSlapped, YourReaction1):
    $ Result = "\n"
    $ _discussion_menu = {"title": "Ваши действия", "items": [MenuItem("Вернуться к делам", Jump("TavernMain"))]}

    if strcomp(HarassInstructions.get(GirlNamePEAH, ""), "^allow"):
        if sluttiness.get(GirlNamePEAH, 0) < 18:
            $ Result += "Красная как рак после всего произошедшего, к вам подбежала {}.\n-\"Ты видел?\" спросила она тяжело дыша. Неужели я на самом деле должна это все переносить?".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
            if Friends.get(GirlNamePEAH, 0) > 0 and renpy.random.randint(1, 3) == 1:
                $ Result += "\nПохоже, что ваше задание приводит к тому, что {} сильно на вас злится.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
                $ Friends[GirlNamePEAH] = Friends.get(GirlNamePEAH, 0) - 1
        else:
            $ Result += "{} спокойно прошла мимо вас, чуть виляя бедрами.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
    else:
        if (sluttiness.get(GirlNamePEAH, 0) < 30 or GirlSlapped > 0) and YourReaction1 == 2:
            $ Result += "Красная как рак после всего произошедшего, к вам подскочила {}.\n-\"Ты!\" закричала она - \"Я просто не могу поверить, что какой-то подонок лапал {} прямо у тебя на глазах, а ты просто стоял и пялился.\"".format(
                RealName.get(GirlNamePEAH, GirlNamePEAH),
                relationship_desc1(GirlNamePEAH),
            )
            if Friends.get(GirlNamePEAH, 0) > 0 and renpy.random.randint(1, 2) == 1:
                $ Result += "\nПохоже, что ваша реакция не очень-то понравилась {}.".format(RealName3.get(GirlNamePEAH, GirlNamePEAH))
                $ Friends[GirlNamePEAH] = Friends.get(GirlNamePEAH, 0) - 1
        elif YourReaction1 == 2:
            $ Result += "К вам подошла {}.\n-\"Озорник\", заметила она - \"Какой-то подонок лапал {} прямо у тебя на глазах, а ты стоял и смотрел. И похоже, тебе это даже нравилось.\"".format(
                RealName.get(GirlNamePEAH, GirlNamePEAH),
                relationship_desc1(GirlNamePEAH),
            )
        elif (sluttiness.get(GirlNamePEAH, 0) < 30 or GirlSlapped > 0) and YourReaction1 == 1:
            $ Result += "Красная как рак после всего произошедшего, к вам подскочила {}.\n-\"Где тебя носило!\" закричала она - \"Меня попытался облапать какой-то подонок, а тебя нигде не было чтобы мне помочь!\"".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
            if Friends.get(GirlNamePEAH, 0) > 0 and renpy.random.randint(1, 5) == 1:
                $ Result += "\nПохоже, что ваша реакция не очень-то понравилась {}.".format(RealName3.get(GirlNamePEAH, GirlNamePEAH))
                $ Friends[GirlNamePEAH] = Friends.get(GirlNamePEAH, 0) - 1
        elif YourReaction1 == 1:
            $ Result += "{} спокойно прошла мимо вас, чуть виляя бедрами.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
        else:
            $ Result += "{} спокойно прошла мимо вас, возвращаясь к работе.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))

    if GirlNamePEAH == "melissa":
        if (sluttiness.get(GirlNamePEAH, 0) < 30 or GirlSlapped > 0) and YourReaction1 in (1, 2):
            call HarassDiscussImage(GirlNamePEAH, 0)
        else:
            call HarassDiscussImage(GirlNamePEAH, 1)
    elif GirlNamePEAH == "amanda":
        call HarassDiscussImage(GirlNamePEAH, 1)

    call IntHarrassmentDiscuss(GirlNamePEAH, YourReaction1)
    if isinstance(_return, dict):
        $ _discussion_menu = _return

    $ Result = {"text": Result, "title": str(_discussion_menu.get("title", "Ваши действия") or "Ваши действия"), "items": list(_discussion_menu.get("items", [MenuItem("Вернуться к делам", Jump("TavernMain"))]) or [MenuItem("Вернуться к делам", Jump("TavernMain"))])}
    return Result
