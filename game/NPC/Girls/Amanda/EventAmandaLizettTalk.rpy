# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label EventAmandaLizettTalk(eyewitness=0, result="", not_to_speak=0):
    $ result = ""

    if Liza.can_work_tavern():
        if Amanda.var_int("prohibitliza", 0) == 1:
            $ result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Ой, нельзя мне с тобой говорить, мастер Стефан запретил!\""
            if procedural_randint(1, max(2, 10 - Amanda.var_int("lizafriends", 0) * 3 // 2), key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:12:1") == 1:
                $ result += "\n\"Ну да ладно\", добавляет она, \"его вроде здесь нет, так что давай немножко поболтаем!\""
            else:
                $ result += "\nИ девицы расходятся по своим делам."
                $ not_to_speak = 1
        elif Amanda.var_int("prohibitliza", 0) == 2:
            $ result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Ой, ты что, знаешь как мастер Стефан ругаться будет, если узнает что мы с тобой болтаем!\""
            if procedural_randint(1, max(4, 20 - Amanda.var_int("lizafriends", 0) * 2), key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:19:2") == 1:
                $ result += "\n\"Ну ладно, его нет, а с тобой болтать интересно, так что рискнем!\" - добавляет она после секундных раздумий."
            else:
                $ result += "\nИ девицы расходятся по своим делам."
                $ not_to_speak = 1
        else:
            if (Amanda.corruption <= 5 and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:25:3") == 1) or (Amanda.corruption <= 10 and Amanda.corruption > 5 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:25:4") == 1):
                $ result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Не хочу я с тобой болтать, ты такая распущенная и такие пошлые вещи рассказываешь!\""
                $ not_to_speak = 1
            else:
                $ result = "Проходя по трактиру вы вдруг услышали как Лизетта весело болтает с Амандой."

        if eyewitness > 0:
            $ result += "\n\nЧто вы намеренны предпринять?"
        elif not_to_speak == 0:
            call EventAmandaLizettTalk2(eyewitness)
            if _return:
                $ result += _return
    else:
        $ result = ""

    if eyewitness > 0:
        call ShowImage("amanda", "tavern", "lizatalk{}".format(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:41:5")))
        "[result]"
        menu:
            "Похвалить Аманду, за то, что не стала болтать с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0 and not_to_speak == 1:
                "Вы похвалили Аманду за то, что она послушалась вас и не стала болтать с Лизеттой. На ее лице читалось явное облегчение от того, что она не попалась."
            "Строго наругать Аманду за то, та болтает с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0 and not_to_speak == 0:
                $ Amanda.set_var_int("prohibitliza", 2)
                $ not_to_speak = 1
                "Вы подошли к болтушкам и начали сурово отчитывать Аманду за то, что она не выполнила вашего наказа. Аманда расплакалась и убежала в слезах."
                $ Amanda.apply_social_chance(4, 1, -1, 0, 0, 0, "liza_talk_scold")
            "Сказать Аманде, чтобы не болтала с Лизеттой" if Amanda.var_int("prohibitliza", 0) == 0 and not_to_speak == 0:
                $ Amanda.set_var_int("prohibitliza", 1)
                $ not_to_speak = 1
                "Вы подошли к болтушкам и вмешались в их разговор, отозвав Аманду в сторону, якобы по неотложному делу. Как только вы остались вдвоем вы сказали Аманде, чтобы она не болтала с Лизеттой, так как та распущенная девчонка и хорошему не научит. Аманда выслушала вас и пообещала с Лизеттой не говорить."
            "Сказать Аманде, что она правильно не стала болтать с Лизеттой" if Amanda.var_int("prohibitliza", 0) == 0 and not_to_speak == 1:
                $ Amanda.set_var_int("prohibitliza", 1)
                $ not_to_speak = 1
                "Вы подошли к Аманде и сказали, что случайно слышали ее разговор с Лизеттой. Вы отметили, что она абсолютно правильно не стала с ней болтать и что вы тоже не советуете ей трепаться с юной шлюхой. При слове \"шлюха\" Аманда зарделась и пообещала с Лизеттой больше не говорить."
            "Сказать Аманде, что вы погорячились, когда запретили ей говорить с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0 and not_to_speak == 1:
                $ Amanda.set_var_int("prohibitliza", 0)
                "Вы подошли к Аманде и сказали, что погорячились, вы не хотите на нее давить и она имеет полное право говорить с кем хочет. Аманда поблагодарила вас за доверие и пошла по своим делам."
            "Подслушать" if not_to_speak == 0:
                "Вы решили подслушать, что будет дальше."
                call EventAmandaLizettTalk2(eyewitness)
                if _return:
                    "[_return]"
            "Вернуться к своим делам" if not_to_speak == 1:
                pass
        return ""

    $ result = ""

    return result
