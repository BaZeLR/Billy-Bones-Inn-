init python:
    def _aah_slut_friends_increase(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness):
        try:
            return slut_friends_increase(
                girl, limit_friend, friend_chance, inc_decr_friends,
                limit_sluttiness, sluttiness_chance, inc_decr_sluttiness
            )
        except Exception:
            if renpy.has_label("SlutFriendsIncrease"):
                return renpy.call(
                    "SlutFriendsIncrease",
                    girl, limit_friend, friend_chance, inc_decr_friends,
                    limit_sluttiness, sluttiness_chance, inc_decr_sluttiness
                )
            return None

    def _aah_pregnancy_check(girl, place, count, dad):
        try:
            return PregnancyCheck(girl, place, count, dad)
        except Exception:
            if renpy.has_label("PregnancyCheck"):
                return renpy.call("PregnancyCheck", girl, place, count, dad)
            return None


label AmandaAtHomeCode:
    python:
        AmandaVar.setdefault("kickyoufromroomcount", 0)
        AmandaVar.setdefault("kickyoufromroom", 0)
        AmandaVar.setdefault("kickedwithmomhelp", 0)
        AmandaVar.setdefault("prohibitliza", 0)
        AmandaVar.setdefault("alberprohibit", 0)
        AmandaVar.setdefault("alberfriends", 0)
        AmandaVar.setdefault("gloryscold", 0)
        AmandaVar.setdefault("prohibitwithguys", 0)
        AmandaVar.setdefault("suckyou", 0)
        AmandaVar.setdefault("fuckyou", 0)
        AmandaVar.setdefault("knownotvirgin", 0)
        AmandaVar.setdefault("beddeflower", 0)
        AmandaVar.setdefault("knowlegaresex", 0)
        AmandaVar.setdefault("sawlegaresex", 0)
        AmandaVar.setdefault("knowsexactive", 0)

        Friends.setdefault("amanda", 0)
        Friends.setdefault("sandra", 0)
        Friends.setdefault("melissa", 0)
        sluttiness.setdefault("amanda", 0)
        sluttiness.setdefault("liza", 0)
        virginity.setdefault("amanda", 1)
        pregnancy.setdefault("amanda", 0)
        LickPussy.setdefault("amanda", 0)
        GiveOrgasms.setdefault("amanda", 0)
        topdress.setdefault("amanda", "")
        bottomdress.setdefault("amanda", "")
        panties.setdefault("amanda", "")
    return


label CodeAmandaKickFromRoom(reason=""):
    if AmandaVar["kickyoufromroomcount"] >= 3:
        if reason == "afterdeny":
            "Аманда дернулась, отпихивая вас обеими руками. \"Ах!\" — завизжала она. \"Значит по-хорошему ты не понимаешь!\""
        else:
            "Аманда проснулась от уже знакомых и неприятных ощущений. \"Опять ты!\" — завизжала она."
        "Прежде чем вы успели что-либо сделать, девушка заорала во весь голос: \"Помогите! Насилуют!\""
        "Двери распахнулись: в комнату ворвалась мать, а за ней Мелисса. Осыпанные ударами, вы с позором ретировались в зал."
        $ AmandaVar["kickedwithmomhelp"] = 1
        python:
            _aah_slut_friends_increase("amanda", 0, 1, -3, 0, 0, 0)
            _aah_slut_friends_increase("sandra", 0, 1, -7, 0, 0, 0)
            _aah_slut_friends_increase("melissa", 0, 1, -5, 0, 0, 0)
    else:
        if reason == "afterdeny":
            "Аманда дернулась, отпихивая вас обеими руками."
        else:
            "Аманда резко дернулась, проснулась и уставилась на вас в ужасе."
        "\"Да ты что делаешь, Стефан?! Вон отсюда, пока я не закричала!\""
        "В растерянности вы ретировались в главный зал."

    $ AmandaVar["kickyoufromroomcount"] += 1
    $ AmandaVar["kickyoufromroom"] = 1
    python:
        _aah_slut_friends_increase("amanda", 0, 1, -5, 18, 1, -3)
    jump TavernMain


label CodeAmandaListScold:
    if AmandaVar["prohibitliza"]:
        "С Лизкой, значит, и словом не перемолвись — дурное влияние, мол."
    if AmandaVar["alberprohibit"] and AmandaVar["alberfriends"] >= 5:
        "Про Легаре вы ей запрещали, а теперь сами пришли в ее комнату ночью."
    if AmandaVar["gloryscold"]:
        "У глорихола вы ее отчитали, а теперь сами пристаете."
    if AmandaVar["prohibitwithguys"]:
        "С парнями ей нельзя, а вам, значит, можно."
    "Так сестренка и продолжила срывать с вас покровы — пока только словесно."
    return


label CodeAmandaSorryChoices:
    $ _has_revert_options = AmandaVar["prohibitliza"] or (AmandaVar["alberprohibit"] and AmandaVar["alberfriends"] >= 5) or AmandaVar["gloryscold"] or AmandaVar["prohibitwithguys"]

    if _has_revert_options:
        menu:
            "Плюнуть и вернуться в зал":
                "\"Аманда, ты все не так поняла,\" — заявили вы и демонстративно вышли."
                python:
                    _aah_slut_friends_increase("amanda", 10, 1, -1, 25, 1, -1)
                $ AmandaVar["kickyoufromroom"] = 1
                jump TavernMain

            "Не обращать внимание на ее слова и поцеловать покрепче":
                call CodeAmandaKickFromRoom("afterdeny")

            "Взять назад слова про Лизетту" if AmandaVar["prohibitliza"]:
                "\"Ладно, насчет Лизетты я вспылил,\" — примирительно сказали вы."
                python:
                    _msg = CodeAmandaHappyConfirm()
                    if isinstance(_msg, str) and _msg:
                        renpy.say(None, _msg)
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["prohibitliza"] = 0
                jump CodeAmandaSorryChoices

            "Взять назад слова про месье Легаре" if AmandaVar["alberprohibit"] and AmandaVar["alberfriends"] >= 5:
                "\"Ладно, насчет Легаре тоже перегнул,\" — сказали вы."
                python:
                    _msg = CodeAmandaHappyConfirm()
                    if isinstance(_msg, str) and _msg:
                        renpy.say(None, _msg)
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["alberprohibit"] = 0
                jump CodeAmandaSorryChoices

            "Взять назад слова про глорихол" if AmandaVar["gloryscold"]:
                "\"Ладно, насчет глорихола я тоже был резок,\" — признали вы."
                python:
                    _msg = CodeAmandaHappyConfirm()
                    if isinstance(_msg, str) and _msg:
                        renpy.say(None, _msg)
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["gloryscold"] = 0
                jump CodeAmandaSorryChoices

            "Взять назад слова про путанье с парнями" if AmandaVar["prohibitwithguys"]:
                "\"Ладно, насчет парней я тоже был слишком строг,\" — сказали вы."
                python:
                    _msg = CodeAmandaHappyConfirm()
                    if isinstance(_msg, str) and _msg:
                        renpy.say(None, _msg)
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["prohibitwithguys"] = 0
                jump CodeAmandaSorryChoices
    else:
        "\"Вот так лучше,\" — довольная собой Аманда позволила вам заткнуть ее поцелуем."
        call CodeAmandaSexStart
    return


label CodeAmandaSexStart:
    $ AmandaVar["kickyoufromroom"] = 0

    if tmpSexType == 0:
        "Вдоволь нацеловавшись, Аманда отстранилась."
        if virginity["amanda"]:
            "\"Я еще девушка и пока хочу такой остаться... но могу тебе отсосать.\""
        else:
            "\"Я могу сейчас отсосать, но пока не готова на большее.\""

        menu:
            "Попенять на ее связь с Легаре" if AmandaVar["knowlegaresex"] or AmandaVar["sawlegaresex"]:
                "\"С Легаре можешь, а со мной нет?\" — обиженно сказали вы."
                call CodeAmandaSexPush

            "Попрекнуть ее активной половой жизнью" if AmandaVar["knowsexactive"]:
                "\"Со всеми, значит, можешь, а меня динамить?\""
                call CodeAmandaSexPush

            "Указать на ее беременность" if pregnancy["amanda"] > 120:
                "\"С таким пузиком поздно строить из себя недотрогу.\""
                call CodeAmandaSexPush

            "Указать, что она уже не девочка" if AmandaVar["knownotvirgin"]:
                "\"Я знаю, что ты уже не целочка.\""
                call CodeAmandaSexPush

            "Напомнить, что вы уже трахались" if AmandaVar["fuckyou"]:
                "\"Мы уже были вместе, так что не ломайся.\""
                call CodeAmandaSexPush

            "Дальше":
                call CodeAmandaSexAgreeLeave("minet")
        return

    elif tmpSexType == 1:
        "\"Стефан, ты будешь у меня первым... только будь нежен,\" — тихо сказала Аманда."
        if tmpSleepDress > 0:
            "Вы начали ласкать ее обнаженную грудь, а потом спустились ниже."
        if tmpSleepDress < 2:
            call CodeAmandaSexBedUndress
        else:
            call CodeAmandaSexBedDeflower(0)
        return

    else:
        python:
            _aah_slut_friends_increase("amanda", 20, 1, 1, 50, 5, 1)
        if tmpSleepDress > 0:
            "Не теряя времени, вы начали ласкать ее обнаженные груди."
        call CodeAmandaSexBedUndress
        return


label CodeAmandaSexBedUndress:
    if tmpSleepDress == 0:
        menu:
            "Снять ночнушку":
                "Вы стянули с Аманды ночнушку, обнажив ее грудь."
                $ tmpSleepDress = 1
                $ topdress["amanda"] = ""
                $ bottomdress["amanda"] = ""
                jump CodeAmandaSexBedUndress

    if tmpSleepDress == 1:
        menu:
            "Снять панталончики":
                "Вы стянули с нее панталончики, и она охотно помогла вам."
                $ panties["amanda"] = ""
                $ tmpSleepDress = 2
                jump CodeAmandaSexBedUndress

    if tmpSleepDress >= 2:
        if tmpSexType == 1:
            call CodeAmandaSexBedDeflower(0)
        else:
            menu:
                "Перейти к делу":
                    call CodeAmandaSexScene
    return


label CodeAmandaSexBedDeflower(tmpCurSexStep=0):
    if tmpCurSexStep == 0:
        menu:
            "Сделать сначала куни":
                "Вы раздвинули ей ножки и довели языком до сильного возбуждения."
                python:
                    _aah_slut_friends_increase("amanda", 20, 1, 1, 50, 1, 1)
                $ LickPussy["amanda"] += 1
                call CodeAmandaSexBedDeflower(1)

            "Сломать сестре целку":
                "Вы вошли в нее одним движением, прорвав плеву. Сначала ей было больно."
                $ AmandaVar["fuckyou"] = 1
                $ AmandaVar["knownotvirgin"] = 1
                $ virginity["amanda"] = 0
                $ AmandaVar["beddeflower"] = 1
                python:
                    _aah_slut_friends_increase("amanda", 12, 1, 1, 30, 1, 1)
                call CodeAmandaSexBedDeflower(2)
        return

    if tmpCurSexStep == 1:
        menu:
            "Лишить Аманду девственности":
                "После куни она была мягче и вскоре поймала свой первый оргазм на вашем члене."
                $ GiveOrgasms["amanda"] += 1
                $ AmandaVar["fuckyou"] = 1
                $ AmandaVar["knownotvirgin"] = 1
                $ virginity["amanda"] = 0
                $ AmandaVar["beddeflower"] = 1
                python:
                    _aah_slut_friends_increase("amanda", 20, 1, 3, 55, 1, 3)
                call CodeAmandaSexBedDeflower(3)
        return

    if tmpCurSexStep == 2 or tmpCurSexStep == 3:
        menu:
            "Кончить на животик":
                "В последний момент вы вытащили член и кончили ей на живот."
                python:
                    _aah_slut_friends_increase("amanda", 20, 1, 1, 0, 0, 0)
                    _aah_pregnancy_check("amanda", "mouthface", 1, "Вы")
                if tmpCurSexStep == 3:
                    call CodeAmandaSexBedDeflower(7)
                else:
                    call CodeAmandaSexBedDeflower(6)

            "Кончить в сестренку":
                "Вы не стали вытаскивать и кончили прямо в нее."
                python:
                    _aah_slut_friends_increase("amanda", 10, 1, -1, 55, 1, 1)
                    _aah_pregnancy_check("amanda", "inside", 1, "Вы")
                if tmpCurSexStep == 3:
                    call CodeAmandaSexBedDeflower(5)
                else:
                    call CodeAmandaSexBedDeflower(4)
        return

    if tmpCurSexStep == 4 or tmpCurSexStep == 6:
        "\"Почти ничего не почувствовала...\" — призналась Аманда после этого первого опыта."
    else:
        "\"Блин, Стефан, а секс это правда классно!\" — восхищенно сказала Аманда."
        python:
            _aah_slut_friends_increase("amanda", 20, 1, 2, 55, 1, 3)

    "\"Ладно, позабавились и будет. Я хочу выспаться,\" — серьезно добавила она."
    menu:
        "Распрощаться и вернуться в зал":
            "Вы поцеловали ее на прощание и вышли из комнаты."
            $ AmandaVar["kickyoufromroom"] = 1
            jump TavernMain
    return


label CodeAmandaSexScene:
    "Движимый похотью, вы прокрались к Аманде ночью. Она приняла вас и явно ждала продолжения."

    if renpy.has_label("IntAmandaSex"):
        if tmpSexType == 0:
            call IntAmandaSex("amanda", "home", "minet")
        else:
            call IntAmandaSex("amanda", "home")
    else:
        "Сцена продолжилась в близости до полного удовлетворения."

    if renpy.has_label("GirlsDesc"):
        call GirlsDesc("amanda")

    if tmpSexType == 0:
        menu:
            "Вернуться в общий зал":
                $ AmandaVar["kickyoufromroom"] = 1
                jump TavernMain
    return


label CodeAmandaSexPush:
    $ tmpReactPush = 0

    if virginity["amanda"]:
        "\"Я еще девушка и не собираюсь терять девственность с братом,\" — резко ответила Аманда."
        if Friends["amanda"] >= 10:
            "\"Считаем, что этого разговора не было. Мое предложение в силе.\""
            call CodeAmandaSexAgreeLeave("minet")
        else:
            "Аманда накрылась одеялом и отвернулась."
            call CodeAmandaSexAgreeLeave("")
        python:
            _aah_slut_friends_increase("amanda", 2, 1, -1, 35, 1, -1)
        return

    if Friends["amanda"] >= 15:
        $ tmpReactPush = 1
        if renpy.random.randint(1, 3) == 1:
            $ tmpReactPush = 2
    elif Friends["amanda"] >= 10:
        if renpy.random.randint(1, 6) == 1:
            $ tmpReactPush = 2
        elif renpy.random.randint(1, 3) <= 2:
            $ tmpReactPush = 1
    elif Friends["amanda"] >= 5:
        if renpy.random.randint(1, 2) == 1:
            $ tmpReactPush = 1

    if tmpReactPush == 2:
        "Ваши упреки подействовали: Аманда нехотя согласилась."
        python:
            _aah_slut_friends_increase("amanda", 2, 1, -1, 50, 3, 1)
        $ tmpSexType = 2
        call CodeAmandaSexBedUndress
    elif tmpReactPush == 1:
        "\"Если не нравится мое предложение — дверь вон там,\" — отрезала она."
        python:
            _aah_slut_friends_increase("amanda", 2, 1, -1, 0, 0, 0)
        call CodeAmandaSexAgreeLeave("minet")
    else:
        "Аманда решила, что разговор окончен, и предложила вам уйти."
        python:
            _aah_slut_friends_increase("amanda", 2, 1, -1, 30, 1, -1)
        call CodeAmandaSexAgreeLeave("")
    return


label CodeAmandaSexAgreeLeave(mode=""):
    menu:
        "Скрепя сердце ограничиться минетом" if mode == "minet":
            "Вы решили пока удовлетвориться малым."
            python:
                _aah_slut_friends_increase("amanda", 20, 3, 1, 35, 5, 1)
            if renpy.has_label("ShowImageSeq"):
                call ShowImageSeq("amanda", "sexroom", "minet", 12)
            call CodeAmandaSexScene

        "Распрощаться и вернуться в зал":
            "\"Ну нет так нет,\" — заявили вы и вышли."
            python:
                _aah_slut_friends_increase("amanda", 10, 1, -1, 25, 1, -1)
            $ AmandaVar["kickyoufromroom"] = 1
            jump TavernMain

        "Проигнорировать ее лепет и продолжить приставать":
            "Вы решили не останавливаться и полезли к сестре между ног."
            call CodeAmandaKickFromRoom("afterdeny")
    return
