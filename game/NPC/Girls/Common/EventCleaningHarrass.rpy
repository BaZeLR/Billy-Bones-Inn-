# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_cleaning_harrass(eyewitness=0):
    $ Eyewitness = eyewitness
    $ YourReaction1 = 0
    $ CurEventDesc = ""
    $ girl_name = get_random_girl_by_job("jobcleaning")

    if girl_name:
        $ HarassType = procedural_randint(1, 4, key="procedural:NPC/Girls/Common/EventCleaningHarrass.rpy:procedural_randint:11:1")

        if HarassType == 1:
            $ CurEventDesc = "{} подошла к столу чтобы вытереть разлитое вино. Когда она наклонилась над столом, ее груди оказались в непосредственной близости к одному из сидящих за ним подмастерьев. Юнец не смог устоять перед соблазном и схватил оба шарика, начав с наслаждением их мять.".format(RealName.get(girl_name, girl_name))
            $ _harass_action = "tits"
        elif HarassType == 2:
            $ CurEventDesc = "Когда {} наклонилась, чтобы убрать мусор из под стола, какой-то грузчик ловко пристроился сзади, схватив ее за попу, и сделал несколько возвратно-поступательных движений под одобрительные возгласы своих дружков.".format(RealName.get(girl_name, girl_name))
            $ _harass_action = "ass"
        elif HarassType == 3:
            $ CurEventDesc = "{} залезла на лестницу, чтобы протереть одну из верхних полок. Проходящий мимо морячок не упустил такого удобного случая и запустил руки ей под платье.".format(RealName.get(girl_name, girl_name))
            $ _harass_action = "dress"
        else:
            $ CurEventDesc = "{} спокойно мыла пол, когда какой-то подвыпивший стражник ухватил ее за задницу и попытался поцеловать.".format(RealName.get(girl_name, girl_name))
            $ _harass_action = "ass"

        if eyewitness > 0:
            call HarassShowImage(girl_name, _harass_action, 0, eyewitness, "cleaning")
            call PartEventYourFirstReaction(girl_name, "event_cleaning_harrass_part2", eyewitness, HarassType)
            $ _reaction_menu = _return if isinstance(_return, dict) else {"title": "Что вы будете делать?", "items": []}
            $ stage_tavern_event_pages(CurEventDesc, _reaction_menu.get("title", ""), _reaction_menu.get("items", []))
            call QueuePagedPanelTextFromStore
            $ Result = MainTxt
        else:
            call event_cleaning_harrass_part2(girl_name, eyewitness, 1, HarassType)
            $ _part2_result = _return
            if isinstance(_part2_result, dict):
                $ CurEventDesc += _coerce_panel_text_value(_part2_result.get("text", ""))
            else:
                $ CurEventDesc += _coerce_panel_text_value(_part2_result)
            $ tavern_event_panel_raw_text = _normalize_tavern_event_text(CurEventDesc)
        $ Result = format_tavern_event_text(tavern_event_panel_raw_text)

    if not girl_name:
        $ tavern_event_panel_raw_text = _normalize_tavern_event_text(CurEventDesc)
        $ Result = format_tavern_event_text(tavern_event_panel_raw_text)
    return Result
