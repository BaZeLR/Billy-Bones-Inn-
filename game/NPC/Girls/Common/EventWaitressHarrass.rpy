# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_waitress_harrass(eyewitness=0):
    $ Eyewitness = eyewitness
    $ YourReaction1 = 0
    $ CurEventDesc = ""
    $ girl_name = get_random_girl_by_job("jobwaitress")

    if girl_name:
        $ HarassType = procedural_randint(1, 4, key="procedural:NPC/Girls/Common/EventWaitressHarrass.rpy:procedural_randint:11:1")

        if HarassType == 1:
            $ CurEventDesc = "{} подошла к столу за который только что уселась компания моряков. Не успела она открыть рот, чтобы поинтересоваться заказом, как ближайший моряк ухватил ее одной рукой за грудь, а другой за задницу и одобрительно присвистнул.".format(RealName.get(girl_name, girl_name))
            $ _harass_action = "tits"
        elif HarassType == 2:
            $ CurEventDesc = "Когда {} проходила мимо какого-то грузчика, тот ее, недолго думая, щипнул за попу.".format(RealName.get(girl_name, girl_name))
            $ _harass_action = "ass"
        elif HarassType == 3:
            $ CurEventDesc = "{} спокойно шла к кухне за заказом, как вдруг к ней подскочил какой-то мастеровой и впился в ее губы смачным поцелуем. Шаловливые же ручки работяги не замедлили облапать попку {}, прижимая девицу крепче к себе.".format(RealName.get(girl_name, girl_name), RealName2.get(girl_name, girl_name))
            $ _harass_action = "dress"
        else:
            $ CurEventDesc = "{} принесла кружки с вином и тарелки с жарким на стол какой-то подозрительной компании. Не успела она расставить все по своим местам, как какой-то ушлый типчик посадил ее к себе на колени и стал лапать ее грудь.".format(RealName.get(girl_name, girl_name))
            $ _harass_action = "tits"

        if eyewitness > 0:
            call HarassShowImage(girl_name, _harass_action, 0, eyewitness, "waitress")
            call PartEventYourFirstReaction(girl_name, "event_waitress_harrass_part2", eyewitness, HarassType)
            $ _reaction_menu = _return if isinstance(_return, dict) else {"title": "Что вы будете делать?", "items": []}
            $ stage_tavern_event_pages(CurEventDesc, _reaction_menu.get("title", ""), _reaction_menu.get("items", []))
            call QueuePagedPanelTextFromStore
            $ Result = MainTxt
        else:
            call event_waitress_harrass_part2(girl_name, eyewitness, 1, HarassType)
            $ _part2_result = _return
            if isinstance(_part2_result, dict):
                $ CurEventDesc += str(_part2_result.get("text", "") or "")
            else:
                $ CurEventDesc += str(_part2_result or "")
            $ tavern_event_panel_raw_text = _normalize_tavern_event_text(CurEventDesc)
            $ Result = format_tavern_event_text(tavern_event_panel_raw_text)

    if not girl_name:
        $ tavern_event_panel_raw_text = _normalize_tavern_event_text(CurEventDesc)
        $ Result = format_tavern_event_text(tavern_event_panel_raw_text)
    return Result
