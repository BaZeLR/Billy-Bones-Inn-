# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label EventAmandaLizettTalk(eyewitness=0):
    $ YourReaction1 = 0
    $ NotToSpeak = 0
    $ Result = ""

    if jobWhoreAvail.get("liza", 0):
        if AmandaVar.get("prohibitliza", 0) == 1:
            $ Result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Ой, нельзя мне с тобой говорить, мастер Стефан запретил!\""
            if renpy.random.randint(1, max(2, 10 - AmandaVar.get("lizafriends", 0) * 3 // 2)) == 1:
                $ Result += "\n\"Ну да ладно\", добавляет она, \"его вроде здесь нет, так что давай немножко поболтаем!\""
            else:
                $ Result += "\nИ девицы расходятся по своим делам."
                $ NotToSpeak = 1
        elif AmandaVar.get("prohibitliza", 0) == 2:
            $ Result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Ой, ты что, знаешь как мастер Стефан ругаться будет, если узнает что мы с тобой болтаем!\""
            if renpy.random.randint(1, max(4, 20 - AmandaVar.get("lizafriends", 0) * 2)) == 1:
                $ Result += "\n\"Ну ладно, его нет, а с тобой болтать интересно, так что рискнем!\" - добавляет она после секундных раздумий."
            else:
                $ Result += "\nИ девицы расходятся по своим делам."
                $ NotToSpeak = 1
        else:
            if (sluttiness.get("amanda", 0) <= 5 and renpy.random.randint(1, 2) == 1) or (sluttiness.get("amanda", 0) <= 10 and sluttiness.get("amanda", 0) > 5 and renpy.random.randint(1, 4) == 1):
                $ Result = "Проходя по трактиру вы вдруг услышали как Аманда говорит Лизетте:\n\"Не хочу я с тобой болтать, ты такая распущенная и такие пошлые вещи рассказываешь!\""
                $ NotToSpeak = 1
            else:
                $ Result = "Проходя по трактиру вы вдруг услышали как Лизетта весело болтает с Амандой."

        if eyewitness > 0:
            $ current_action_title = "Что предпринять"
            $ current_action_content = None
            $ _amanda_talk_choices = []

            if AmandaVar.get("prohibitliza", 0) > 0 and NotToSpeak == 1:
                $ _amanda_talk_choices.append(MenuItem("Похвалить Аманду, за то, что не стала болтать с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalkApply", 1, eyewitness)]))

            if AmandaVar.get("prohibitliza", 0) > 0 and NotToSpeak == 0:
                $ _amanda_talk_choices.append(MenuItem("Строго наругать Аманду за то, та болтает с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalkApply", 2, eyewitness)]))

            if AmandaVar.get("prohibitliza", 0) == 0 and NotToSpeak == 0:
                $ _amanda_talk_choices.append(MenuItem("Сказать Аманде, чтобы не болтала с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalkApply", 3, eyewitness)]))

            if AmandaVar.get("prohibitliza", 0) == 0 and NotToSpeak == 1:
                $ _amanda_talk_choices.append(MenuItem("Сказать Аманде, что она правильно не стала болтать с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalkApply", 4, eyewitness)]))

            if AmandaVar.get("prohibitliza", 0) > 0 and NotToSpeak == 1:
                $ _amanda_talk_choices.append(MenuItem("Сказать Аманде, что вы погорячились, когда запретили ей говорить с Лизеттой", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalkApply", 5, eyewitness)]))

            if NotToSpeak == 0:
                $ _amanda_talk_choices.append(MenuItem("Подслушать", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalkApply", 6, eyewitness)]))

            if NotToSpeak == 1:
                $ _amanda_talk_choices.append(MenuItem("Вернуться к своим делам", [SetVariable("current_action_items", []), Call("EventAmandaLizettTalkApply", 7, eyewitness)]))

            $ current_action_items = _amanda_talk_choices
            $ Result += "\n\nЧто вы намеренны предпринять?"
        elif NotToSpeak == 0:
            call EventAmandaLizettTalk2(eyewitness)
            if _return:
                $ Result += _return
    else:
        $ Result = ""

    if eyewitness == 0:
        $ Result = ""
    else:
        call ShowImage("amanda", "tavern", "lizatalk{}".format(renpy.random.randint(1, 2)))

    return Result

label EventAmandaLizettTalkApply(reaction_code=7, eyewitness=0):
    $ YourReaction1 = reaction_code

    if reaction_code == 1:
        "Вы похвалили Аманду за то, что она послушалась вас и не стала болтать с Лизеттой. На ее лице читалось явное облегчение от того, что она не попалась."
    elif reaction_code == 2:
        $ AmandaVar["prohibitliza"] = 2
        $ NotToSpeak = 1
        "Вы подошли к болтушкам и начали сурово отчитывать Аманду за то, что она не выполнила вашего наказа. Аманда расплакалась и убежала в слезах."
        call SlutFriendsIncrease("amanda", 4, 1, -1, 0, 0, 0)
    elif reaction_code == 3:
        $ AmandaVar["prohibitliza"] = 1
        $ NotToSpeak = 1
        "Вы подошли к болтушкам и вмешались в их разговор, отозвав Аманду в сторону, якобы по неотложному делу. Как только вы остались вдвоем вы сказали Аманде, чтобы она не болтала с Лизеттой, так как та распущенная девчонка и хорошему не научит. Аманда выслушала вас и пообещала с Лизеттой не говорить."
    elif reaction_code == 4:
        $ AmandaVar["prohibitliza"] = 1
        $ NotToSpeak = 1
        "Вы подошли к Аманде и сказали, что случайно слышали ее разговор с Лизеттой. Вы отметили, что она абсолютно правильно не стала с ней болтать и что вы тоже не советуете ей трепаться с юной шлюхой. При слове \"шлюха\" Аманда зарделась и пообещала с Лизеттой больше не говорить."
    elif reaction_code == 5:
        $ AmandaVar["prohibitliza"] = 0
        "Вы подошли к Аманде и сказали, что погорячились, вы не хотите на нее давить и она имеет полное право говорить с кем хочет. Аманда поблагодарила вас за доверие и пошла по своим делам."
    elif reaction_code == 6:
        "Вы решили подслушать, что будет дальше."
        call EventAmandaLizettTalk2(eyewitness)
        if _return:
            "[_return]"

    jump TavernMain
