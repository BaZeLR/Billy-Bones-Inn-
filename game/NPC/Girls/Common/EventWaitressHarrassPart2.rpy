    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_waitress_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1):
    $ Eyewitness = eyewitness
    $ YourReaction1 = your_reaction1
    $ HarassType = harass_type

    call PartEventGirlHarrassmentReaction(girl_name, "waitress", eyewitness)
    $ CurEventDescPart2 = _return

    if GirlSlapped > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 1, eyewitness, "waitress")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 1, eyewitness, "waitress")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 1, eyewitness, "waitress")
        else:
            call HarassShowImage(girl_name, "tits", 1, eyewitness, "waitress")
    elif GirlRunAway > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 2, eyewitness, "waitress")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 2, eyewitness, "waitress")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 2, eyewitness, "waitress")
        else:
            call HarassShowImage(girl_name, "tits", 2, eyewitness, "waitress")

    if GirlRunAway == 0:
        $ CurEventDescPart2 += "\n"
        $ _girl_info = getPersonInfo(girl_name)
        $ girl_slut = int(getattr(_girl_info, "corruption", 0) or 0)

        if girl_slut < 50:
            if harass_type == 1:
                $ CurEventDescPart2 += "{} терпеливо дождалась, пока морячку не надоест тискать ее сиськи, а после взяла заказ как ни в чем ни бывало.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "tits", 4, eyewitness, "waitress")
            elif harass_type == 2:
                $ CurEventDescPart2 += "{} взвизгнула, вильнула попкой и продолжила свой путь как ни в чем ни бывало.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "ass", 4, eyewitness, "waitress")
            elif harass_type == 3:
                $ CurEventDescPart2 += "{} терпеливо дождалась, не отвечая на поцелуй, пока мастеровому не надоест и после продолжила свой путь.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "dress", 4, eyewitness, "waitress")
            else:
                $ CurEventDescPart2 += "{} спокойно сидела на коленях у типчика, стойко перенося его неуклюжие ухватки. Дождавшись подходящего момента она встала и вернулась к работе.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "tits", 4, eyewitness, "waitress")
        else:
            if harass_type == 1:
                $ CurEventDescPart2 += "\"Что, нравится, морячок?\" - спросила {}. \"Ну потрогай, только недолго, мне работать дальше надо.\" И пока новоявленный поклонник тискал ее грудь, {} взяла заказ, как ни в чем ни бывало.".format(RealName.get(girl_name, girl_name), RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "tits", 5, eyewitness, "waitress")
            elif harass_type == 2:
                $ CurEventDescPart2 += "{} соблазнительно вильнула попкой, оглянулась, быстро поцеловала приставалу и продолжила свой путь.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "ass", 5, eyewitness, "waitress")
            elif harass_type == 3:
                $ CurEventDescPart2 += "{} страстно ответила на поцелуй, плотно прижимаясь всем телом к мастеровому. Спустя несколько минут тот нехотя разжал объятия и {} продолжила свой путь.".format(RealName.get(girl_name, girl_name), RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "dress", 5, eyewitness, "waitress")
            else:
                $ CurEventDescPart2 += "{} с готовностью ответила на поцелуй и даже устроилась поудобнее, чтобы типчику удобнее было ее лапать. Через пару минут она прошептала ему на ухо что ей пора дальше работать и он нехотя отпустил девушку.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "tits", 5, eyewitness, "waitress")

    call PartEventCustomerHarrassmentReaction(girl_name)
    $ CurEventDescPart2 += _return

    if eyewitness > 0:
        call PartEventAfterHarrassment(girl_name, GirlSlapped, your_reaction1)
        if isinstance(_return, dict):
            $ CurEventDescPart2 += _coerce_panel_text_value(_return.get("text", ""))
            $ _next_title = str(_return.get("title", _next_title) or _next_title)
            $ _next_items = list(_return.get("items", _next_items) or _next_items)
        else:
            $ CurEventDescPart2 += _coerce_panel_text_value(_return)

    if eyewitness > 0:
        $ Result = {"text": CurEventDescPart2, "title": _next_title, "items": _next_items}
    else:
        $ Result = CurEventDescPart2
    return Result
