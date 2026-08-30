# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_cleaning_harrass(eyewitness=0, result="", cur_event_desc="", harass_type=1, girl_name="", harass_action="", part2_result=None):
    $ girl_name = get_random_girl_by_job("jobcleaning", "TavernMain" if eyewitness > 0 else None)

    if girl_name:
        $ harass_type = procedural_randint(1, 4, key="procedural:NPC/Girls/Common/EventCleaningHarrass.rpy:procedural_randint:11:1")

        if harass_type == 1:
            $ cur_event_desc = "{} подошла к столу чтобы вытереть разлитое вино. Когда она наклонилась над столом, ее груди оказались в непосредственной близости к одному из сидящих за ним подмастерьев. Юнец не смог устоять перед соблазном и схватил оба шарика, начав с наслаждением их мять.".format(people_display_name(girl_name))
            $ harass_action = "tits"
        elif harass_type == 2:
            $ cur_event_desc = "Когда {} наклонилась, чтобы убрать мусор из под стола, какой-то грузчик ловко пристроился сзади, схватив ее за попу, и сделал несколько возвратно-поступательных движений под одобрительные возгласы своих дружков.".format(people_display_name(girl_name))
            $ harass_action = "ass"
        elif harass_type == 3:
            $ cur_event_desc = "{} залезла на лестницу, чтобы протереть одну из верхних полок. Проходящий мимо морячок не упустил такого удобного случая и запустил руки ей под платье.".format(people_display_name(girl_name))
            $ harass_action = "dress"
        else:
            $ cur_event_desc = "{} спокойно мыла пол, когда какой-то подвыпивший стражник ухватил ее за задницу и попытался поцеловать.".format(people_display_name(girl_name))
            $ harass_action = "ass"

        if eyewitness > 0:
            $ main_ui_begin_native_scene_state("Событие в трактире")
            call HarassShowImage(girl_name, harass_action, 0, eyewitness, "cleaning")
            $ scene_runtime.text = format_tavern_event_text(cur_event_desc + "\n\nЧто вы будете делать?")
            $ scene_runtime.location_text = scene_runtime.text
            call PartEventYourFirstReaction(girl_name, "event_cleaning_harrass_part2", eyewitness, harass_type)
            $ result = scene_runtime.text
            $ main_ui_end_native_scene_state()
        else:
            call event_cleaning_harrass_part2(girl_name, eyewitness, 1, harass_type)
            $ part2_result = _return
            if isinstance(part2_result, dict):
                $ cur_event_desc += _coerce_panel_text_value(part2_result.get("text", ""))
            else:
                $ cur_event_desc += _coerce_panel_text_value(part2_result)
            $ result = format_tavern_event_text(_normalize_tavern_event_text(cur_event_desc))

    if not girl_name:
        $ result = format_tavern_event_text(_normalize_tavern_event_text(cur_event_desc))
    return result
