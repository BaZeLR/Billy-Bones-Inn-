label EventAmandaLizettTalk2(eyewitness=0):
    $ YourReaction2 = 0
    $ _amanda_liza_row = get_random_amanda_liza_talk_row()
    if _amanda_liza_row:
        $ Result = _amanda_liza_format_text(_amanda_liza_row.get("Phrase", ""))
        $ _amanda_liza_reaction_values = _amanda_liza_reaction_args(_amanda_liza_row.get("Code", ""))
        if _amanda_liza_reaction_values:
            call PartEventGirlReactionTalk("amanda", "liza", "AmandaVar['lizafriends']", _amanda_liza_reaction_values[0], _amanda_liza_reaction_values[1], _amanda_liza_reaction_values[2])
            if _return:
                $ Result += str(_return)
    else:
        $ Result = "[Случайная фраза из AmandaLizaTalk]"

    if eyewitness > 0:
        $ current_action_title = "Что сказать"
        $ current_action_content = None
        $ _amanda_talk2_choices = []

        if AmandaVar.get("prohibitliza", 0) > 0:
            $ _amanda_talk2_choices.append(MenuItem("Строго наругать Аманду за то, та болтает с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalk2Apply", 1)]))

        if AmandaVar.get("prohibitliza", 0) == 0:
            $ _amanda_talk2_choices.append(MenuItem("Сказать Аманде, чтобы не болтала с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalk2Apply", 2)]))

        if AmandaVar.get("prohibitliza", 0) > 0:
            $ _amanda_talk2_choices.append(MenuItem("Сказать Аманде, что вы погорячились, когда запретили ей говорить с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalk2Apply", 3)]))

        $ _amanda_talk2_choices.append(MenuItem("Вернуться к своим делам", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalk2Apply", 4)]))
        $ current_action_items = _amanda_talk2_choices
        $ Result += "\n\nПосле разговора Аманда с Лизеттой разошлись. Намеренны ли вы что-то сказать проходящей мимо Аманде?"

    return Result

label EventAmandaLizettTalk2Apply(reaction_code=4):
    $ YourReaction2 = reaction_code

    if reaction_code == 1:
        $ AmandaVar["prohibitliza"] = 2
        "Вы поймали проходящую мимо сестренку и строго ее отчитали за то, что она болтала с Лизеттой несмотря на запрет. Аманда расплакалась и убежала в слезах."
        call SlutFriendsIncrease("amanda", 3, 1, -1, 0, 0, 0)
    elif reaction_code == 2:
        $ AmandaVar["prohibitliza"] = 1
        "Вы поймали проходящую мимо сестренку и сказали ей, чтобы она не болтала с Лизеттой, так как та распущенная девчонка и хорошему не научит. Аманда выслушала вас и пообещала с Лизеттой не говорить."
    elif reaction_code == 3:
        $ AmandaVar["prohibitliza"] = 0
        "Вы поймали проходящую мимо сестренку и сказали ей, что погорячились, вы не хотите на нее давить и она имеет полное право говорить с кем хочет. Аманда поблагодарила вас за доверие и пошла по своим делам."
        if Friends.get("amanda", 0) < 5 and renpy.random.randint(1, 4) == 1:
            "Ей очень понравилось, что вы ей так доверяете."
            call SlutFriendsIncrease("amanda", 6, 1, 1, 0, 0, 0)

    jump TavernMain
