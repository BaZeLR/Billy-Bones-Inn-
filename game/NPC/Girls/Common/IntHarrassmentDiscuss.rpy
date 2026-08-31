# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntHarrassmentDiscuss(GirlNameMHD, YourReaction1, _girl_info=None, _harass_instruction="", _girl_dative="", _girl_unhappy=False):
    $ _girl_info = people.get_info(GirlNameMHD)
    $ _harass_instruction = _girl_info.harass_instruction() if _girl_info is not None else ""
    $ _girl_dative = people_name(GirlNameMHD, 'dative')
    $ _girl_unhappy = _girl_info is not None and YourReaction1 in (1, 2) and (int(getattr(_girl_info, "corruption", 0) or 0) < 30 or int(getattr(_girl_info, "anger_with_player", 0) or 0) > 0)
    show screen main_ui
    menu:
        "Сказать что она не должна позволять себя лапать":
            call IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, 1)

        "Объяснить [_girl_dative], что она должна быть чуть вежливее" if not strcomp(_harass_instruction, "^allow"):
            call IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, 2)

        "Еще раз все объяснить [_girl_dative]" if strcomp(_harass_instruction, "^allow"):
            call IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, 3)

        "Сказать [_girl_dative], чтобы она поступала как считает нужным" if _harass_instruction != "":
            call IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, 4)

        "Сказать, что вы обдумаете проблему" if _girl_unhappy:
            call IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, 6)

        "Выгнать наглого клиента" if _girl_unhappy:
            call IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, 7)

        "Промолчать":
            call IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, 5)
    return

label IntHarrassmentDiscussOutcome(GirlNameMHD, YourReaction1, choice_code=5, _discussion_text="", _girl_info=None, _girl_corruption=0, _harass_instruction=""):
    $ _discussion_text = ""
    $ _girl_info = people.get_info(GirlNameMHD)
    $ _girl_corruption = int(getattr(_girl_info, "corruption", 0) or 0)
    $ _harass_instruction = _girl_info.harass_instruction() if _girl_info is not None else ""
    if choice_code == 1:
        if _harass_instruction == "notallow" and YourReaction1 == 3:
            $ _discussion_text = "Вы извинились что не помогли {} в этот раз, но повторили еще раз, что она не должна позволять себя никому лапать. А вы, если будете рядом, в другой раз постараетесь ей помочь.".format(people_name(GirlNameMHD, 'dative'))
        elif _harass_instruction == "notallow":
            $ _discussion_text = "Вы еще раз сказали {}, что она не должна позволять себя никому лапать. А вы, если будете рядом, ей поможете.".format(people_name(GirlNameMHD, 'dative'))
        else:
            $ _discussion_text = "\"{}!\" сказали вы. Ты не должна позволять себя никому лапать. Будь вежлива с посетителями, но держи дистанцию.".format(people_display_name(GirlNameMHD))

        if _girl_corruption >= 40:
            call HarassDiscussImage(GirlNameMHD, 1)
            $ _discussion_text += "\n\n{} восприняла ваши слова с удивлением и даже некоторым разочарованием.".format(people_display_name(GirlNameMHD))
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=-1)
                $ _girl_info.change_mana(-1, "harass_forbid_attention")
                $ _girl_info.change_rebellion(1, "harass_forbid_attention")
        else:
            call HarassDiscussImage(GirlNameMHD, 2)
            $ _discussion_text += "\n\n{} восприняла ваши слова с облегчением.".format(people_display_name(GirlNameMHD))
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=-1)
                $ _girl_info.change_mana(1, "harass_forbid_attention")
                $ _girl_info.change_rebellion(-1, "harass_forbid_attention")

        if _girl_info is not None:
            $ _girl_info.set_harass_instruction("notallow")
    elif choice_code == 2:
        if _harass_instruction == "notallow":
            $ _discussion_text = "Вы сказали {} что вы тщательно обдумали ситуацию и поменяли свое решение. Черезчур жесткая реакция отпугивает посетителей, а если к вам никто не будет ходить, то вы разоритесь. Поэтому ей надо быть чуть помягче, не быть такой недотрогой и больше позволять. Не все, нет, далеко не все, но если кто-то вдруг положит руку на ее задницу, то она вовсе не должна орать как резанная или бросаться в драку.".format(people_name(GirlNameMHD, 'dative'))
        else:
            $ _discussion_text = "Вы сказали {} что такая ее реакция хотя и вполне понятна и естественна, но отпугивает посетителей. Она же сама понимает, что если к вам никто не будет ходить то вы разоритесь. Поэтому вы попросили ее, чтобы она не была такой недотрогой и не делала трагедии если вдруг кто-то положит руку на ее задницу. И уж тем более в таких случаях он не должна бросаться в драку.".format(people_name(GirlNameMHD, 'dative'))

        if _girl_corruption >= 40:
            call HarassDiscussImage(GirlNameMHD, 2)
            $ _discussion_text += "\n\n{} восприняла ваши слова как должное, заметив что она и сама думает точно также.".format(people_display_name(GirlNameMHD))
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=1)
                $ _girl_info.change_mana(1, "harass_allow_attention")
                $ _girl_info.change_rebellion(-1, "harass_allow_attention")
        else:
            call HarassDiscussImage(GirlNameMHD, 0)
            $ _discussion_text += "\n\n{} слушала вас с грустным и обиженным выражением лица, но в конце концов согласилась с вашей аргументацией и пообещала стараться.".format(people_display_name(GirlNameMHD))
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=1)
                $ _girl_info.change_mana(-1, "harass_allow_attention")
                $ _girl_info.change_rebellion(1, "harass_allow_attention")

        if _girl_info is not None:
            $ _girl_info.set_harass_instruction("allow")
    elif choice_code == 3:
        $ _discussion_text = "Вы терпеливо повторили {} все, что вы говорили раньше. Вы объяснили что если к вам никто не будет ходить то вы разоритесь. Поэтому еще раз сказали, что для блага семьи будет лучше, если она не будет недотрогой и не будет делать трагедии из щипка за попу или положенной на грудь руки. И уж тем более в таких случаях он не должна бросаться в драку.".format(people_name(GirlNameMHD, 'dative'))

        if _girl_corruption >= 40:
            call HarassDiscussImage(GirlNameMHD, 2)
            $ _discussion_text += "\n\n{} восприняла ваши слова как должное, заметив что она и сама думает точно также.".format(people_display_name(GirlNameMHD))
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=1)
                $ _girl_info.change_mana(1, "harass_allow_attention_repeat")
                $ _girl_info.change_rebellion(-1, "harass_allow_attention_repeat")
        else:
            call HarassDiscussImage(GirlNameMHD, 0)
            $ _discussion_text += "\n\n{} слушала вас с грустным и обиженным выражением лица, но в конце концов согласилась с вашей аргументацией и пообещала стараться.".format(people_display_name(GirlNameMHD))
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=1)
                $ _girl_info.change_mana(-1, "harass_allow_attention_repeat")
                $ _girl_info.change_rebellion(1, "harass_allow_attention_repeat")

        if _girl_info is not None:
            $ _girl_info.set_harass_instruction("allow")
    elif choice_code == 4:
        $ _discussion_text = "Вы сказали {}, что вы решили что сколько она позволяет посетителям должно быть полностью ее решением. Если она хочет позволять им многое - то пускай, а если она расценивает распущенные руки как наглость - то может раздавать пощечины, не стесняясь. Вы поддержите ее в любом случае, но решение как поступать - должно быть ее, вы не хотите навязывать своего мнения.".format(people_name(GirlNameMHD, 'dative'))
        call HarassDiscussImage(GirlNameMHD, 2)
        $ _discussion_text += "\n\n{} восприняла ваши слова с благодарностью за оказанное ей доверие.".format(people_display_name(GirlNameMHD))
        if _girl_info is not None:
            $ _girl_info.set_harass_instruction("")
            $ _girl_info.change_social(friend_delta=1)
            $ _girl_info.change_mana(1, "harass_free_choice")
            $ _girl_info.change_rebellion(-1, "harass_free_choice")
    elif choice_code == 6:
        $ _discussion_text = "Вы не стали отделываться приказом и пообещали {}, что обдумаете, как защитить девушек от наглых рук, не превращая трактир в постоянное поле боя. Пока решение не принято, вы попросили сразу звать вас, если посетитель снова перейдет черту.".format(people_name(GirlNameMHD, 'dative'))
        call HarassDiscussImage(GirlNameMHD, 2)
        if _girl_info is not None:
            $ _girl_info.change_social(friend_delta=1)
            $ _girl_info.change_mana(1, "harass_promised_solution")
            $ _girl_info.change_anger(-1, "harass_promised_solution")
    elif choice_code == 7:
        $ _discussion_text = "Вы находите наглого посетителя, отрываете его от стола и выставляете за дверь. Затем вы говорите {}, что в вашем трактире никто не покупает право унижать ее вместе с кружкой эля.".format(people_name(GirlNameMHD, 'dative'))
        call HarassDiscussImage(GirlNameMHD, 2)
        if _girl_info is not None:
            $ _girl_info.set_harass_instruction("notallow")
            $ _girl_info.change_social(friend_delta=1)
            $ _girl_info.change_mana(2, "harass_customer_ejected")
            $ _girl_info.change_rebellion(-1, "harass_customer_ejected")
            $ _girl_info.change_anger(-1, "harass_customer_ejected")
        $ player.change_tavern_fame(-1)
    else:
        $ _discussion_text = "Вы решили ничего не говорить {}, а пойти лучше дальше по своим делам.".format(people_name(GirlNameMHD, 'dative'))

    $ scene_runtime.text = format_tavern_event_text(_discussion_text)
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к делам":
            return
