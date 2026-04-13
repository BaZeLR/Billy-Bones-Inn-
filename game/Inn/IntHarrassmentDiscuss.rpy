label IntHarrassmentDiscuss(GirlNameMHD, YourReaction1):
    $ HarrassmentAlreadyDiscussed = 0
    $ _harass_choices = [MenuItem("Сказать что она не должна позволять себя лапать", [SetVariable("current_action_items", []), Call("IntHarrassmentDiscussApply", GirlNameMHD, YourReaction1, 1)])]

    if not strcomp(HarassInstructions.get(GirlNameMHD, ""), "^allow"):
        $ _harass_choices.append(MenuItem("Объяснить {} что она должна быть чуть вежливее".format(RealName3.get(GirlNameMHD, GirlNameMHD)), [SetVariable("current_action_items", []), Call("IntHarrassmentDiscussApply", GirlNameMHD, YourReaction1, 2)]))

    if strcomp(HarassInstructions.get(GirlNameMHD, ""), "^allow"):
        $ _harass_choices.append(MenuItem("Еще раз все объяснить {}".format(RealName3.get(GirlNameMHD, GirlNameMHD)), [SetVariable("current_action_items", []), Call("IntHarrassmentDiscussApply", GirlNameMHD, YourReaction1, 3)]))

    if HarassInstructions.get(GirlNameMHD, "") != "":
        $ _harass_choices.append(MenuItem("Сказать {} чтобы она поступала как считает нужным".format(RealName3.get(GirlNameMHD, GirlNameMHD)), [SetVariable("current_action_items", []), Call("IntHarrassmentDiscussApply", GirlNameMHD, YourReaction1, 4)]))

    $ _harass_choices.append(MenuItem("Промолчать", [SetVariable("current_action_items", []), Call("IntHarrassmentDiscussApply", GirlNameMHD, YourReaction1, 5)]))
    $ Result = {"title": "Что сказать", "items": _harass_choices}
    return Result

label IntHarrassmentDiscussApply(GirlNameMHD, YourReaction1, choice_code=5):
    $ _discussion_text = ""
    if choice_code == 1:
        if HarassInstructions.get(GirlNameMHD, "") == "notallow" and YourReaction1 == 3:
            $ _discussion_text = "Вы извинились что не помогли {} в этот раз, но повторили еще раз, что она не должна позволять себя никому лапать. А вы, если будете рядом, в другой раз постараетесь ей помочь.".format(RealName3.get(GirlNameMHD, GirlNameMHD))
        elif HarassInstructions.get(GirlNameMHD, "") == "notallow":
            $ _discussion_text = "Вы еще раз сказали {}, что она не должна позволять себя никому лапать. А вы, если будете рядом, ей поможете.".format(RealName3.get(GirlNameMHD, GirlNameMHD))
        else:
            $ _discussion_text = "\"{}!\" сказали вы. Ты не должна позволять себя никому лапать. Будь вежлива с посетителями, но держи дистанцию.".format(RealName.get(GirlNameMHD, GirlNameMHD))

        if sluttiness.get(GirlNameMHD, 0) >= 40:
            call HarassDiscussImage(GirlNameMHD, 1)
            $ _discussion_text += "\n\n{} восприняла ваши слова с удивлением и даже некоторым разочарованием.".format(RealName.get(GirlNameMHD, GirlNameMHD))
        else:
            call HarassDiscussImage(GirlNameMHD, 2)
            $ _discussion_text += "\n\n{} восприняла ваши слова с облегчением.".format(RealName.get(GirlNameMHD, GirlNameMHD))

        $ HarassInstructions[GirlNameMHD] = "notallow"
        $ HarrassmentAlreadyDiscussed = 1

    elif choice_code == 2:
        if HarassInstructions.get(GirlNameMHD, "") == "notallow":
            $ _discussion_text = "Вы сказали {} что вы тщательно обдумали ситуацию и поменяли свое решение. Черезчур жесткая реакция отпугивает посетителей, а если к вам никто не будет ходить, то вы разоритесь. Поэтому ей надо быть чуть помягче, не быть такой недотрогой и больше позволять. Не все, нет, далеко не все, но если кто-то вдруг положит руку на ее задницу, то она вовсе не должна орать как резанная или бросаться в драку.".format(RealName3.get(GirlNameMHD, GirlNameMHD))
        else:
            $ _discussion_text = "Вы сказали {} что такая ее реакция хотя и вполне понятна и естественна, но отпугивает посетителей. Она же сама понимает, что если к вам никто не будет ходить то вы разоритесь. Поэтому вы попросили ее, чтобы она не была такой недотрогой и не делала трагедии если вдруг кто-то положит руку на ее задницу. И уж тем более в таких случаях он не должна бросаться в драку.".format(RealName3.get(GirlNameMHD, GirlNameMHD))

        if sluttiness.get(GirlNameMHD, 0) >= 40:
            call HarassDiscussImage(GirlNameMHD, 2)
            $ _discussion_text += "\n\n{} восприняла ваши слова как должное, заметив что она и сама думает точно также.".format(RealName.get(GirlNameMHD, GirlNameMHD))
        else:
            call HarassDiscussImage(GirlNameMHD, 0)
            $ _discussion_text += "\n\n{} слушала вас с грустным и обиженным выражением лица, но в конце концов согласилась с вашей аргументацией и пообещала стараться.".format(RealName.get(GirlNameMHD, GirlNameMHD))

        $ HarassInstructions[GirlNameMHD] = "allow"
        $ HarrassmentAlreadyDiscussed = 1

    elif choice_code == 3:
        $ _discussion_text = "Вы терпеливо повторили {} все, что вы говорили раньше. Вы объяснили что если к вам никто не будет ходить то вы разоритесь. Поэтому еще раз сказали, что для блага семьи будет лучше, если она не будет недотрогой и не будет делать трагедии из щипка за попу или положенной на грудь руки. И уж тем более в таких случаях он не должна бросаться в драку.".format(RealName3.get(GirlNameMHD, GirlNameMHD))

        if sluttiness.get(GirlNameMHD, 0) >= 40:
            call HarassDiscussImage(GirlNameMHD, 2)
            $ _discussion_text += "\n\n{} восприняла ваши слова как должное, заметив что она и сама думает точно также.".format(RealName.get(GirlNameMHD, GirlNameMHD))
        else:
            call HarassDiscussImage(GirlNameMHD, 0)
            $ _discussion_text += "\n\n{} слушала вас с грустным и обиженным выражением лица, но в конце концов согласилась с вашей аргументацией и пообещала стараться.".format(RealName.get(GirlNameMHD, GirlNameMHD))

        $ HarassInstructions[GirlNameMHD] = "allow"
        $ HarrassmentAlreadyDiscussed = 1

    elif choice_code == 4:
        $ _discussion_text = "Вы сказали {}, что вы решили что сколько она позволяет посетителям должно быть полностью ее решением. Если она хочет позволять им многое - то пускай, а если она расценивает распущенные руки как наглость - то может раздавать пощечины, не стесняясь. Вы поддержите ее в любом случае, но решение как поступать - должно быть ее, вы не хотите навязывать своего мнения.".format(RealName3.get(GirlNameMHD, GirlNameMHD))
        call HarassDiscussImage(GirlNameMHD, 2)
        $ _discussion_text += "\n\n{} восприняла ваши слова с благодарностью за оказанное ей доверие.".format(RealName.get(GirlNameMHD, GirlNameMHD))
        $ HarassInstructions[GirlNameMHD] = ""
        $ HarrassmentAlreadyDiscussed = 1

    else:
        $ _discussion_text = "Вы решили ничего не говорить {}, а пойти лучше дальше по своим делам.".format(RealName3.get(GirlNameMHD, GirlNameMHD))

    $ stage_tavern_event_pages(_discussion_text, "Ваши действия", [MenuItem("Вернуться к делам", Jump("TavernMain"))])
    call QueuePagedPanelTextFromStore
    call ReturnToMainUI
    return
