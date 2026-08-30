# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_waitress_harrass(eyewitness=0, result="", cur_event_desc="", harass_type=1, girl_name="", harass_action="", part2_result=None):
    $ girl_name = get_random_girl_by_job("jobwaitress", "TavernMain" if eyewitness > 0 else None)

    if girl_name:
        $ harass_type = procedural_randint(1, 4, key="procedural:NPC/Girls/Common/EventWaitressHarrass.rpy:procedural_randint:11:1")

        if harass_type == 1:
            $ cur_event_desc = "{} подошла к столу за который только что уселась компания моряков. Не успела она открыть рот, чтобы поинтересоваться заказом, как ближайший моряк ухватил ее одной рукой за грудь, а другой за задницу и одобрительно присвистнул.".format(people_display_name(girl_name))
            $ harass_action = "tits"
        elif harass_type == 2:
            $ cur_event_desc = "Когда {} проходила мимо какого-то грузчика, тот ее, недолго думая, щипнул за попу.".format(people_display_name(girl_name))
            $ harass_action = "ass"
        elif harass_type == 3:
            $ cur_event_desc = "{} спокойно шла к кухне за заказом, как вдруг к ней подскочил какой-то мастеровой и впился в ее губы смачным поцелуем. Шаловливые же ручки работяги не замедлили облапать попку {}, прижимая девицу крепче к себе.".format(people_display_name(girl_name), people_name(girl_name, 'genitive'))
            $ harass_action = "dress"
        else:
            $ cur_event_desc = "{} принесла кружки с вином и тарелки с жарким на стол какой-то подозрительной компании. Не успела она расставить все по своим местам, как какой-то ушлый типчик посадил ее к себе на колени и стал лапать ее грудь.".format(people_display_name(girl_name))
            $ harass_action = "tits"

        if eyewitness > 0:
            $ main_ui_begin_native_scene_state("Событие в трактире")
            call HarassShowImage(girl_name, harass_action, 0, eyewitness, "waitress")
            $ scene_runtime.text = format_tavern_event_text(cur_event_desc + "\n\nЧто вы будете делать?")
            $ scene_runtime.location_text = scene_runtime.text
            call PartEventYourFirstReaction(girl_name, "event_waitress_harrass_part2", eyewitness, harass_type)
            $ result = scene_runtime.text
            $ main_ui_end_native_scene_state()
        else:
            call event_waitress_harrass_part2(girl_name, eyewitness, 1, harass_type)
            $ part2_result = _return
            if isinstance(part2_result, dict):
                $ cur_event_desc += str(part2_result.get("text", "") or "")
            else:
                $ cur_event_desc += str(part2_result or "")
            $ result = format_tavern_event_text(_normalize_tavern_event_text(cur_event_desc))

    if not girl_name:
        $ result = format_tavern_event_text(_normalize_tavern_event_text(cur_event_desc))
    return result
