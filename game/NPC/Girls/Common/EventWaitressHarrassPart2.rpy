# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_waitress_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1, cur_event_desc_part2="", girl_run_away=0, girl_slapped=0, _girl_info=None, girl_slut=0):
    call PartEventGirlHarrassmentReaction(girl_name, "waitress", eyewitness, your_reaction1)
    $ cur_event_desc_part2, girl_run_away, girl_slapped = _return

    if girl_slapped > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 1, eyewitness, "waitress")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 1, eyewitness, "waitress")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 1, eyewitness, "waitress")
        else:
            call HarassShowImage(girl_name, "tits", 1, eyewitness, "waitress")
    elif girl_run_away > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 2, eyewitness, "waitress")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 2, eyewitness, "waitress")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 2, eyewitness, "waitress")
        else:
            call HarassShowImage(girl_name, "tits", 2, eyewitness, "waitress")

    if girl_run_away == 0:
        $ cur_event_desc_part2 += "\n"
        $ _girl_info = people.get_info(girl_name)
        $ girl_slut = int(getattr(_girl_info, "corruption", 0) or 0)

        if girl_slut < 50:
            if harass_type == 1:
                $ cur_event_desc_part2 += "{} терпеливо дождалась, пока морячку не надоест тискать ее сиськи, а после взяла заказ как ни в чем ни бывало.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "tits", 4, eyewitness, "waitress")
            elif harass_type == 2:
                $ cur_event_desc_part2 += "{} взвизгнула, вильнула попкой и продолжила свой путь как ни в чем ни бывало.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "ass", 4, eyewitness, "waitress")
            elif harass_type == 3:
                $ cur_event_desc_part2 += "{} терпеливо дождалась, не отвечая на поцелуй, пока мастеровому не надоест и после продолжила свой путь.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "dress", 4, eyewitness, "waitress")
            else:
                $ cur_event_desc_part2 += "{} спокойно сидела на коленях у типчика, стойко перенося его неуклюжие ухватки. Дождавшись подходящего момента она встала и вернулась к работе.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "tits", 4, eyewitness, "waitress")
        else:
            if harass_type == 1:
                $ cur_event_desc_part2 += "\"Что, нравится, морячок?\" - спросила {}. \"Ну потрогай, только недолго, мне работать дальше надо.\" И пока новоявленный поклонник тискал ее грудь, {} взяла заказ, как ни в чем ни бывало.".format(people_display_name(girl_name), people_display_name(girl_name))
                call HarassShowImage(girl_name, "tits", 5, eyewitness, "waitress")
            elif harass_type == 2:
                $ cur_event_desc_part2 += "{} соблазнительно вильнула попкой, оглянулась, быстро поцеловала приставалу и продолжила свой путь.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "ass", 5, eyewitness, "waitress")
            elif harass_type == 3:
                $ cur_event_desc_part2 += "{} страстно ответила на поцелуй, плотно прижимаясь всем телом к мастеровому. Спустя несколько минут тот нехотя разжал объятия и {} продолжила свой путь.".format(people_display_name(girl_name), people_display_name(girl_name))
                call HarassShowImage(girl_name, "dress", 5, eyewitness, "waitress")
            else:
                $ cur_event_desc_part2 += "{} с готовностью ответила на поцелуй и даже устроилась поудобнее, чтобы типчику удобнее было ее лапать. Через пару минут она прошептала ему на ухо что ей пора дальше работать и он нехотя отпустил девушку.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "tits", 5, eyewitness, "waitress")

    call PartEventCustomerHarrassmentReaction(girl_name, girl_run_away, girl_slapped)
    $ cur_event_desc_part2 += _return

    if eyewitness > 0:
        $ scene_runtime.text = format_tavern_event_text(cur_event_desc_part2)
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        call PartEventAfterHarrassment(girl_name, girl_slapped, your_reaction1)
        return

    return cur_event_desc_part2
