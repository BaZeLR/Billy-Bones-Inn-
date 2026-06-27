# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label EventAmandaLizettTalk(eyewitness=0):
    $ YourReaction1 = 0
    $ NotToSpeak = 0
    $ Result = ""

    if jobWhoreAvail.get("liza", 0):
        if Amanda.var_int("prohibitliza", 0) == 1:
            $ Result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Ой, нельзя мне с тобой говорить, мастер Стефан запретил!\""
            if procedural_randint(1, max(2, 10 - Amanda.var_int("lizafriends", 0) * 3 // 2), key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:12:1") == 1:
                $ Result += "\n\"Ну да ладно\", добавляет она, \"его вроде здесь нет, так что давай немножко поболтаем!\""
            else:
                $ Result += "\nИ девицы расходятся по своим делам."
                $ NotToSpeak = 1
        elif Amanda.var_int("prohibitliza", 0) == 2:
            $ Result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Ой, ты что, знаешь как мастер Стефан ругаться будет, если узнает что мы с тобой болтаем!\""
            if procedural_randint(1, max(4, 20 - Amanda.var_int("lizafriends", 0) * 2), key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:19:2") == 1:
                $ Result += "\n\"Ну ладно, его нет, а с тобой болтать интересно, так что рискнем!\" - добавляет она после секундных раздумий."
            else:
                $ Result += "\nИ девицы расходятся по своим делам."
                $ NotToSpeak = 1
        else:
            if (Amanda.corruption <= 5 and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:25:3") == 1) or (Amanda.corruption <= 10 and Amanda.corruption > 5 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:25:4") == 1):
                $ Result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Не хочу я с тобой болтать, ты такая распущенная и такие пошлые вещи рассказываешь!\""
                $ NotToSpeak = 1
            else:
                $ Result = "Проходя по трактиру вы вдруг услышали как Лизетта весело болтает с Амандой."

        if eyewitness > 0:
            $ Result += "\n\nЧто вы намеренны предпринять?"
        elif NotToSpeak == 0:
            call EventAmandaLizettTalk2(eyewitness)
            if _return:
                $ Result += _return
    else:
        $ Result = ""

    if eyewitness > 0:
        call ShowImage("amanda", "tavern", "lizatalk{}".format(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk.rpy:procedural_randint:41:5")))
        "[Result]"
        menu:
            "Похвалить Аманду, за то, что не стала болтать с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0 and NotToSpeak == 1:
                call EventAmandaLizettTalkApply(1, eyewitness)
            "Строго наругать Аманду за то, та болтает с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0 and NotToSpeak == 0:
                call EventAmandaLizettTalkApply(2, eyewitness)
            "Сказать Аманде, чтобы не болтала с Лизеттой" if Amanda.var_int("prohibitliza", 0) == 0 and NotToSpeak == 0:
                call EventAmandaLizettTalkApply(3, eyewitness)
            "Сказать Аманде, что она правильно не стала болтать с Лизеттой" if Amanda.var_int("prohibitliza", 0) == 0 and NotToSpeak == 1:
                call EventAmandaLizettTalkApply(4, eyewitness)
            "Сказать Аманде, что вы погорячились, когда запретили ей говорить с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0 and NotToSpeak == 1:
                call EventAmandaLizettTalkApply(5, eyewitness)
            "Подслушать" if NotToSpeak == 0:
                call EventAmandaLizettTalkApply(6, eyewitness)
            "Вернуться к своим делам" if NotToSpeak == 1:
                call EventAmandaLizettTalkApply(7, eyewitness)
        return ""

    $ Result = ""

    return Result

label EventAmandaLizettTalkApply(reaction_code=7, eyewitness=0):
    $ YourReaction1 = reaction_code

    if reaction_code == 1:
        "Вы похвалили Аманду за то, что она послушалась вас и не стала болтать с Лизеттой. На ее лице читалось явное облегчение от того, что она не попалась."
    elif reaction_code == 2:
        $ Amanda.set_var_int("prohibitliza", 2)
        $ NotToSpeak = 1
        "Вы подошли к болтушкам и начали сурово отчитывать Аманду за то, что она не выполнила вашего наказа. Аманда расплакалась и убежала в слезах."
        $ Amanda.apply_social_chance(4, 1, -1, 0, 0, 0, "liza_talk_scold")
    elif reaction_code == 3:
        $ Amanda.set_var_int("prohibitliza", 1)
        $ NotToSpeak = 1
        "Вы подошли к болтушкам и вмешались в их разговор, отозвав Аманду в сторону, якобы по неотложному делу. Как только вы остались вдвоем вы сказали Аманде, чтобы она не болтала с Лизеттой, так как та распущенная девчонка и хорошему не научит. Аманда выслушала вас и пообещала с Лизеттой не говорить."
    elif reaction_code == 4:
        $ Amanda.set_var_int("prohibitliza", 1)
        $ NotToSpeak = 1
        "Вы подошли к Аманде и сказали, что случайно слышали ее разговор с Лизеттой. Вы отметили, что она абсолютно правильно не стала с ней болтать и что вы тоже не советуете ей трепаться с юной шлюхой. При слове \"шлюха\" Аманда зарделась и пообещала с Лизеттой больше не говорить."
    elif reaction_code == 5:
        $ Amanda.set_var_int("prohibitliza", 0)
        "Вы подошли к Аманде и сказали, что погорячились, вы не хотите на нее давить и она имеет полное право говорить с кем хочет. Аманда поблагодарила вас за доверие и пошла по своим делам."
    elif reaction_code == 6:
        "Вы решили подслушать, что будет дальше."
        call EventAmandaLizettTalk2(eyewitness)
        if _return:
            "[_return]"

    jump TavernMain
