# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label PartEventAfterHarrassment(GirlNamePEAH, GirlSlapped, YourReaction1):
    $ Result = "\n"
    $ _discussion_menu = {"title": "Ваши действия", "items": [MenuItem("Вернуться к делам", Jump("TavernMain"))]}
    $ _discussion_menu = {"title": "Ваши действия", "items": [MenuItem("Вернуться к делам", Jump("TavernMain"))]}
    $ _discussion_menu = {"title": "Ваши действия", "items": [MenuItem("Вернуться к делам", Jump("TavernMain"))]}
    $ _girl_info = getPersonInfo(GirlNamePEAH)
    $ _girl_corruption = int(getattr(_girl_info, "corruption", 0) or 0)
    $ _girl_rel = int(getattr(_girl_info, "rel", 0) or 0)
    $ _harass_instruction = _girl_info.harass_instruction() if _girl_info is not None else ""

    if strcomp(_harass_instruction, "^allow"):
        if _girl_corruption < 18:
            $ Result += "Красная как рак после всего произошедшего, к вам подбежала {}.\n-\"Ты видел?\" спросила она тяжело дыша. Неужели я на самом деле должна это все переносить?".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
            if _girl_rel > 0 and procedural_randint(1, 3, key="procedural:Utilities/General/NPC/PartEventAfterHarrassment.rpy:procedural_randint:15:1") == 1:
                $ Result += "\nПохоже, что ваше задание приводит к тому, что {} сильно на вас злится.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
                $ _girl_info.change_social(friend_delta=-1)
                $ _girl_info.change_anger(1, "harass_allow_instruction")
                $ _girl_info.change_rebellion(1, "harass_allow_instruction")
        else:
            $ Result += "{} спокойно прошла мимо вас, чуть виляя бедрами.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
    else:
        if (_girl_corruption < 30 or GirlSlapped > 0) and YourReaction1 == 2:
            $ Result += "Красная как рак после всего произошедшего, к вам подскочила {}.\n-\"Ты!\" закричала она - \"Я просто не могу поверить, что какой-то подонок лапал {} прямо у тебя на глазах, а ты просто стоял и пялился.\"".format(
                RealName.get(GirlNamePEAH, GirlNamePEAH),
                relationship_desc1(GirlNamePEAH),
            )
            if _girl_rel > 0 and procedural_randint(1, 2, key="procedural:Utilities/General/NPC/PartEventAfterHarrassment.rpy:procedural_randint:28:2") == 1:
                $ Result += "\nПохоже, что ваша реакция не очень-то понравилась {}.".format(RealName3.get(GirlNamePEAH, GirlNamePEAH))
                $ _girl_info.change_social(friend_delta=-1)
                $ _girl_info.change_anger(1, "harass_player_watched")
                $ _girl_info.change_mana(-1, "harass_player_watched")
        elif YourReaction1 == 2:
            $ Result += "К вам подошла {}.\n-\"Озорник\", заметила она - \"Какой-то подонок лапал {} прямо у тебя на глазах, а ты стоял и смотрел. И похоже, тебе это даже нравилось.\"".format(
                RealName.get(GirlNamePEAH, GirlNamePEAH),
                relationship_desc1(GirlNamePEAH),
            )
        elif (_girl_corruption < 30 or GirlSlapped > 0) and YourReaction1 == 1:
            $ Result += "Красная как рак после всего произошедшего, к вам подскочила {}.\n-\"Где тебя носило!\" закричала она - \"Меня попытался облапать какой-то подонок, а тебя нигде не было чтобы мне помочь!\"".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
            if _girl_rel > 0 and procedural_randint(1, 5, key="procedural:Utilities/General/NPC/PartEventAfterHarrassment.rpy:procedural_randint:40:3") == 1:
                $ Result += "\nПохоже, что ваша реакция не очень-то понравилась {}.".format(RealName3.get(GirlNamePEAH, GirlNamePEAH))
                $ _girl_info.change_social(friend_delta=-1)
                $ _girl_info.change_anger(1, "harass_player_ignored")
                $ _girl_info.change_mana(-1, "harass_player_ignored")
        elif YourReaction1 == 1:
            $ Result += "{} спокойно прошла мимо вас, чуть виляя бедрами.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))
        else:
            $ Result += "{} спокойно прошла мимо вас, возвращаясь к работе.".format(RealName.get(GirlNamePEAH, GirlNamePEAH))

    if GirlNamePEAH == "melissa":
        if (_girl_corruption < 30 or GirlSlapped > 0) and YourReaction1 in (1, 2):
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
