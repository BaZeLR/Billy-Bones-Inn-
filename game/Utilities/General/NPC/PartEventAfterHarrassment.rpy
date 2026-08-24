# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label PartEventAfterHarrassment(GirlNamePEAH, GirlSlapped, YourReaction1, result="", _girl_info=None, _girl_corruption=0, _girl_rel=0, _harass_instruction=""):
    $ result = "\n"
    $ _girl_info = people.get_info(GirlNamePEAH)
    $ _girl_corruption = int(getattr(_girl_info, "corruption", 0) or 0)
    $ _girl_rel = int(getattr(_girl_info, "rel", 0) or 0)
    $ _harass_instruction = _girl_info.harass_instruction() if _girl_info is not None else ""

    if strcomp(_harass_instruction, "^allow"):
        if _girl_corruption < 18:
            $ result += "Красная как рак после всего произошедшего, к вам подбежала {}.\n-\"Ты видел?\" спросила она тяжело дыша. Неужели я на самом деле должна это все переносить?".format(people_display_name(GirlNamePEAH))
            if _girl_rel > 0 and procedural_randint(1, 3, key="procedural:Utilities/General/NPC/PartEventAfterHarrassment.rpy:procedural_randint:15:1") == 1:
                $ result += "\nПохоже, что ваше задание приводит к тому, что {} сильно на вас злится.".format(people_display_name(GirlNamePEAH))
                $ _girl_info.change_social(friend_delta=-1)
                $ _girl_info.change_anger(1, "harass_allow_instruction")
                $ _girl_info.change_rebellion(1, "harass_allow_instruction")
        else:
            $ result += "{} спокойно прошла мимо вас, чуть виляя бедрами.".format(people_display_name(GirlNamePEAH))
    else:
        if (_girl_corruption < 30 or GirlSlapped > 0) and YourReaction1 == 2:
            $ result += "Красная как рак после всего произошедшего, к вам подскочила {}.\n-\"Ты!\" закричала она - \"Я просто не могу поверить, что какой-то подонок лапал {} прямо у тебя на глазах, а ты просто стоял и пялился.\"".format(
                people_display_name(GirlNamePEAH),
                relationship_desc1(GirlNamePEAH),
            )
            if _girl_rel > 0 and procedural_randint(1, 2, key="procedural:Utilities/General/NPC/PartEventAfterHarrassment.rpy:procedural_randint:28:2") == 1:
                $ result += "\nПохоже, что ваша реакция не очень-то понравилась {}.".format(people_name(GirlNamePEAH, 'dative'))
                $ _girl_info.change_social(friend_delta=-1)
                $ _girl_info.change_anger(1, "harass_player_watched")
                $ _girl_info.change_mana(-1, "harass_player_watched")
        elif YourReaction1 == 2:
            $ result += "К вам подошла {}.\n-\"Озорник\", заметила она - \"Какой-то подонок лапал {} прямо у тебя на глазах, а ты стоял и смотрел. И похоже, тебе это даже нравилось.\"".format(
                people_display_name(GirlNamePEAH),
                relationship_desc1(GirlNamePEAH),
            )
        elif (_girl_corruption < 30 or GirlSlapped > 0) and YourReaction1 == 1:
            $ result += "Красная как рак после всего произошедшего, к вам подскочила {}.\n-\"Где тебя носило!\" закричала она - \"Меня попытался облапать какой-то подонок, а тебя нигде не было чтобы мне помочь!\"".format(people_display_name(GirlNamePEAH))
            if _girl_rel > 0 and procedural_randint(1, 5, key="procedural:Utilities/General/NPC/PartEventAfterHarrassment.rpy:procedural_randint:40:3") == 1:
                $ result += "\nПохоже, что ваша реакция не очень-то понравилась {}.".format(people_name(GirlNamePEAH, 'dative'))
                $ _girl_info.change_social(friend_delta=-1)
                $ _girl_info.change_anger(1, "harass_player_ignored")
                $ _girl_info.change_mana(-1, "harass_player_ignored")
        elif YourReaction1 == 1:
            $ result += "{} спокойно прошла мимо вас, чуть виляя бедрами.".format(people_display_name(GirlNamePEAH))
        else:
            $ result += "{} спокойно прошла мимо вас, возвращаясь к работе.".format(people_display_name(GirlNamePEAH))

    if GirlNamePEAH == "melissa":
        if (_girl_corruption < 30 or GirlSlapped > 0) and YourReaction1 in (1, 2):
            call HarassDiscussImage(GirlNamePEAH, 0)
        else:
            call HarassDiscussImage(GirlNamePEAH, 1)
    elif GirlNamePEAH == "amanda":
        call HarassDiscussImage(GirlNamePEAH, 1)

    $ scene_runtime.text = format_tavern_event_text(result)
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    call IntHarrassmentDiscuss(GirlNamePEAH, YourReaction1)
    return
