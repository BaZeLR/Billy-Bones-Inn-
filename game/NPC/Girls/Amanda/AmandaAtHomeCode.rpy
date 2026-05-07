# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _aah_slut_friends_increase(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness):
        return slut_friends_increase(
            girl, limit_friend, friend_chance, inc_decr_friends,
            limit_sluttiness, sluttiness_chance, inc_decr_sluttiness
        )

    def _aah_pregnancy_check(girl, place, count, dad):
        return PregnancyCheck(girl, place, count, dad)


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
        "Двери распахнулись: в комнату ворвалась тетушка Сандра, а за ней Мелисса. Осыпанные ударами, вы с позором ретировались в зал."
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
    "Так Аманда и продолжила срывать с вас покровы — пока только словесно."
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
                "\"Даже не знаю, что на меня нашло,\" — удивленно сказали вы. \"Ну подумаешь, Аманда с портовой шлюхой подружилась и та ее жизни учит. Что здесь такого? Даже не знаю, чего это я так рассердился. Все ж нормально.\""
                $ _amanda_confirm_msg = CodeAmandaHappyConfirm()
                "[_amanda_confirm_msg]"
                python:
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["prohibitliza"] = 0
                jump CodeAmandaSorryChoices

            "Взять назад слова про месье Легаре" if AmandaVar["alberprohibit"] and AmandaVar["alberfriends"] >= 5:
                "\"Да ладно тебе,\" — сказали вы. \"Про Легаре это я вспылил. Если он тебе так нравится, то можешь с ним видеться. Ну и что, что он женат и у него дети старше тебя. Подумаешь...\""
                $ _amanda_confirm_msg = CodeAmandaHappyConfirm()
                "[_amanda_confirm_msg]"
                python:
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["alberprohibit"] = 0
                jump CodeAmandaSorryChoices

            "Взять назад слова про глорихол" if AmandaVar["gloryscold"]:
                "\"Ну хорошо, хорошо,\" — примирительно сказали вы. \"Если хочешь у незнакомцев члены через дырку сосать, то соси, любой нормальный мужчина тебе и слова поперек бы не сказал, это я просто вспылил, что уж там.\""
                $ _amanda_confirm_msg = CodeAmandaHappyConfirm()
                "[_amanda_confirm_msg]"
                python:
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["gloryscold"] = 0
                jump CodeAmandaSorryChoices

            "Взять назад слова про путанье с парнями" if AmandaVar["prohibitwithguys"]:
                "\"Ну хорошо, хорошо,\" — примирительно сказали вы. \"Если ты даешь каждому встречному-поперечному парню, да так что они уже в очередь становятся, то это твоя личная жизнь. Зря я к тебе придирался, пока не нагуляешься ведь не успокоишься!\""
                $ _amanda_confirm_msg = CodeAmandaHappyConfirm()
                "[_amanda_confirm_msg]"
                python:
                    _aah_slut_friends_increase("amanda", 18, 1, 1, 45, 2, 1)
                $ AmandaVar["prohibitwithguys"] = 0
                jump CodeAmandaSorryChoices
    else:
        "\"Вот так лучше,\" — заявила вам крайне довольная собой Аманда. \"Можешь и ты по-человечески себя вести. Когда захочешь.\""
        "\"А в мою комнату ты, значит, ворвался дабы...\""
        "Тут вы не выдержали и заткнули болтушку поцелуем."
        "Аманда с готовностью ответила на ваш поцелуй, а потом, отстранившись на секунду от вас, промолвила: \"Ну вот, теперь совсем другое дело, ты исправился и заслужил вознаграждение!\""
        "И с этими словами она опять вернулась к целованию вас, на этот раз взасос. Удивленный и обрадованный таким развитием событий, вы не замедлили вернуть ей поцелуй, переплетясь с ней языками."
        call CodeAmandaSexStart
    return


label CodeAmandaSexStart:
    $ AmandaVar["kickyoufromroom"] = 0

    if tmpSexType == 0:
        "Вдоволь начмокавшись, она оторвалась от вас, сказав:"
        if virginity["amanda"]:
            "\"Ты же знаешь, я ведь еще девушка и хочу такой пока остаться.\""
            "Вы начали было ее уговаривать, но она просто отмахнулась от ваших разглагольствований:"
            "\"Нет, ты не понимаешь, я хочу, но слишком боюсь. Дай мне время. А пока я могу тебе пососать, если хочешь, только не торопи меня.\""
        else:
            "\"Я тебе могу сейчас отсосать, но я пока не готова на большее. Не, я так не могу еще.\""

        menu:
            "Попенять на ее связь с Легаре" if AmandaVar["knowlegaresex"] or AmandaVar["sawlegaresex"]:
                "\"Ага, значит с этим месье, как его, Легаре ты путаешься,\" — обиженно заявили вы, — \"а я для тебя недостаточно хорош. Так получается?!\""
                call CodeAmandaSexPush

            "Попрекнуть ее активной половой жизнью" if AmandaVar["knowsexactive"]:
                "\"Ага, значит со всякими там разными тебе трахаться хочется и можется,\" — обиженно заявили вы, — \"а меня можно динамить. Отлично выходит.\""
                call CodeAmandaSexPush

            "Указать на ее беременность" if pregnancy["amanda"] > 120:
                "\"Кто бы говорил, кто бы говорил,\" — рассмеялись вы. — \"Смотри какое пузо себе уже нагуляла. Поздно ворота затворять, коли лошадь украли. Так давай, отворяй ворота, красавица!\""
                call CodeAmandaSexPush

            "Указать, что она уже не девочка" if AmandaVar["knownotvirgin"]:
                "\"Не вымахивайся,\" — обиженно, но в то же время просительно сказали вы. — \"Я прекрасно знаю, что ты уже не целочка. Так что давай перепихнемся, ну чего тебе стоит?\""
                call CodeAmandaSexPush

            "Напомнить, что вы уже трахались" if AmandaVar["fuckyou"]:
                "\"Аманда, так мы же с тобой уже трахались, свои маленькие ножки ты тогда без вопросов раздвигала,\" — заявили вы с наигранным весельем, — \"так что я не понимаю, что ты сейчас выкаблучиваешься. Давай еще разочек перепихнемся, как раньше.\""
                call CodeAmandaSexPush

            "Дальше":
                call CodeAmandaSexAgreeLeave("minet")
        return

    elif tmpSexType == 1:
        "Вдруг Аманда отстранилась от вас, посерьезнела и, доверчиво глядя прямо вам в глаза, просто сказала:"
        "\"Стефан, ты будешь у меня первым, пожалуйста, будь нежен.\""
        "Обрадованный таким развитием событий, вы не замедлили еще раз поцеловать Аманду взасос, заверяя ее в правильности сделанного выбора."
        if tmpSleepDress > 0:
            "Тем временем ваши руки ласкали ее обнаженные груди, а потом вы сместились ниже, начав щекотать ее напрягшиеся сосочки своим языком."
        if tmpSleepDress < 2:
            call CodeAmandaSexBedUndress
        else:
            call CodeAmandaSexBedDeflower(0)
        return

    else:
        python:
            _aah_slut_friends_increase("amanda", 20, 1, 1, 50, 5, 1)
        if tmpSleepDress > 0:
            "Не теряя времени, вы начали ласкать ее обнаженные груди, а потом, сместившись ниже, пощекотали ее напрягшиеся сосочки своим языком."
        call CodeAmandaSexBedUndress
        return


label CodeAmandaSexBedUndress:
    if tmpSleepDress == 0:
        menu:
            "Снять ночнушку":
                "Тем временем ваши руки сами потянулись к подолу ее ночнушки и потянули его вверх. Аманда с готовностью подняла руки, позволяя вам стянуть с нее рубашку, обнажив ее маленькие острые грудки с торчащими от возбуждения сосочками. К коим вы и не замедлили припасть."
                $ tmpSleepDress = 1
                $ topdress["amanda"] = ""
                $ bottomdress["amanda"] = ""
                jump CodeAmandaSexBedUndress

    if tmpSleepDress == 1:
        menu:
            "Снять панталончики":
                "Продолжая ласкать ее сисечки, вы начали потихоньку стягивать с постанывающей от наслаждения Аманды ее панталончики. Чтобы помочь вам, она задрала свои очаровательные ножки. Совместными усилиями вы избавились от этой помехи, закинув их в угол."
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
                "Вы уложили голенькую девушку на кровати и, раздвинув ей ножки, припали к ее пока еще девственной расщелине. Под вашим быстрым язычком Аманда совсем потекла, ее стоны участились. Вам оставалось лишь надеяться на то, что стены достаточно толстые и никто не придет проведать вас."
                python:
                    _aah_slut_friends_increase("amanda", 20, 1, 1, 50, 1, 1)
                $ LickPussy["amanda"] += 1
                call CodeAmandaSexBedDeflower(1)

            "Лишить Аманду девственности":
                "Решив, что она и так готова, вы приставили свой торчащий колом член к влагалищу Аманды и посмотрели на нее. Она выглядела неуверенно, но все-таки слегка кивнула вам, и вы незамедлительно вошли в нее, прорвав ее плеву одним ударом, лишая ее девичества. Аманда слегка застонала от боли. Подождав немного, чтобы она привыкла к новым ощущениям, вы начали двигаться в ней, сначала медленно, а потом быстрее и быстрее. Однако было заметно, что она лишь терпит вас, не получая удовольствия. Впрочем, в конце концов ее боль улеглась и сменилась слабой улыбкой. Может, если бы вы чуть дольше продержались, Аманде бы и вовсе захорошело, но дольше вы не можете, вы готовы кончить."
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
                "Решив, что она готова, вы приставили свой торчащий колом член к ее влагалищу и посмотрели на Аманду. Она слабо кивнула, и вы резко вошли в нее, прорвав ее плеву одним ударом, лишая ее девичества. Аманда лишь слабо ойкнула. Подождав немного, чтобы она привыкла к новым ощущениям, вы начали двигаться в ней, сначала медленно, а потом быстрее и быстрее. Она сначала никак не реагировала на ваши толчки, но постепенно начала подмахивать. А потом и вовсе вошла в раж, крепко обняв и прижав к себе ногами, стала стараться насадиться на ваш член как можно плотнее. И вот наконец все тело Аманды содрогнулось в ее первом, но не последнем оргазме на мужском члене. Вы тоже уже готовы кончить."
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
                "Не желая рисковать, вы в последний момент вытащили свой член и кончили Аманде на животик."
                if tmpCurSexStep == 3:
                    "С трудом пришедшая в себя после оргазма Аманда собрала пару капель пальцем и начала рассматривать."
                else:
                    "Любопытная Аманда сразу собрала пару капель пальцем и начала рассматривать."
                "\"Молодец, что сдержался и в меня не кончил. А то бы я могла залететь, и что бы мы сказали дома?\" — мудро заметила девушка."
                python:
                    _aah_slut_friends_increase("amanda", 20, 1, 1, 0, 0, 0)
                    _aah_pregnancy_check("amanda", "mouthface", 1, "Вы")
                if tmpCurSexStep == 3:
                    call CodeAmandaSexBedDeflower(7)
                else:
                    call CodeAmandaSexBedDeflower(6)

            "Кончить в Аманду":
                "Даже и не подумав вытащить свой член из Аманды, вы начали кончать, заполнив ее матку спермой. Наконец ваш член выпустил последнюю струю, обмяк и выскользнул из Аманды. Из девушки на простыни обильно потекло ваше семя, перемешанное с ее девственной кровью и собственным соком."
                if tmpCurSexStep == 3:
                    "С трудом пришедшая в себя после оргазма Аманда собрала пару капель пальцем и начала рассматривать."
                else:
                    "Любопытная Аманда сразу собрала пару капель пальцем и начала рассматривать."
                "\"Ну и ну, сколько же ты в меня спустил!\" — недовольно заявила она. \"А если я залечу, ты об этом подумал? Нет? Ну-ну, можешь уже начинать думать, что мы скажем дома.\""
                python:
                    _aah_slut_friends_increase("amanda", 10, 1, -1, 55, 1, 1)
                    _aah_pregnancy_check("amanda", "inside", 1, "Вы")
                if tmpCurSexStep == 3:
                    call CodeAmandaSexBedDeflower(5)
                else:
                    call CodeAmandaSexBedDeflower(4)
        return

    if tmpCurSexStep == 4 or tmpCurSexStep == 6:
        "\"И что девчонки говорили так волнующе о сексе,\" — слегка задумавшись, добавила Аманда. \"Я почти ничего и не почувствовала, только больно сперва было.\""
        "\"Ну, это первый раз так, потом будет приятнее!\" — нашлись с ответом вы."
        "\"Может и будет...\" — в тоне Аманды было маловато убежденности."
    else:
        "\"Блин, Стефан, а ведь секс это действительно классно!\" — восхищенно добавила Аманда. \"Знала бы — дала бы тебе раньше!\""
        "\"Это не со всеми так классно, а только с теми, кто знает, как доставить девушке удовольствие, с мастерами этого дела, с виртуозами, так сказать, с истинными подвижниками, если так можно выразиться, с мастерами, хотя я это уже говорил...\""
        "\"Ну в общем, со мной!\" — скромно закончили вы, поняв, что уже начинаете путаться."
        python:
            _aah_slut_friends_increase("amanda", 20, 1, 2, 55, 1, 3)

    "\"Ладно, позабавились и будет,\" — вдруг посерьезнела Аманда. \"Я еще выспаться хочу, да и прибраться малость не помешает.\""
    menu:
        "Распрощаться и вернуться в зал":
            "Поняв, что она права, вы поцеловали ее на прощание и покинули комнату, в которую чуть ранее столь удачно зашли."
            $ AmandaVar["kickyoufromroom"] = 1
            jump TavernMain
    return


label CodeAmandaSexScene:
    "Движимый неуемной похотью, вы прокрались в комнату Аманды среди ночи и разбудили ее грязными приставаниями. К вашему удивлению, она вас не выгнала, а наоборот, с радостью приняла, расточая авансы и делая недвусмысленные намеки."

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
        "\"Стефан, ты что, оглох?\" — не слишком вежливо ответила вам Аманда. \"Если тебе бочка на голову упала или там ты споткнулся и о камень головушкой приложился, то так и скажи. Повторяю еще раз: я еще девушка! И с тобой я девственность свою терять не намерена. Теперь понятно?\""
        if Friends["amanda"] >= 10:
            "\"Значит так, считаем, что этого разговора не было, мое предложение еще в силе. И?\" — примирительно сказала Аманда."
            call CodeAmandaSexAgreeLeave("minet")
        else:
            "\"Я тебе хотела приятное сделать, а ты меня попрекать решил? Спокойной ночи, дверь прямо за тобой.\" И с этими словами Аманда накрылась одеялом и отвернулась от вас."
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
        "Ваши упреки подействовали на Аманду. Пристыженная, она ответила: \"Ты прав. Что ж, то, что я другим позволяла, должна позволить и тебе. Не поспоришь.\""
        "И все-таки в ее тоне вы уловили грустные нотки."
        python:
            _aah_slut_friends_increase("amanda", 2, 1, -1, 50, 3, 1)
        $ tmpSexType = 2
        call CodeAmandaSexBedUndress
    elif tmpReactPush == 1:
        "\"Ага, ты меня еще попрекать будешь, моралист фигов!\" — ответила вам Аманда. \"Если тебе мое предложение не по нутру — то дверь вон там. Выбирай.\""
        python:
            _aah_slut_friends_increase("amanda", 2, 1, -1, 0, 0, 0)
        call CodeAmandaSexAgreeLeave("minet")
    else:
        "\"Ах, так ты пришел сюда за мою нравственность бороться? А я-то думала...\" — картинно развела руками Аманда."
        "\"Что ж, раз так, то будем считать, что я урок уяснила и буду работать над своим поведением. Ну а пока — спокойной ночи!\" С этими словами Аманда накрылась одеялом и отвернулась от вас."
        python:
            _aah_slut_friends_increase("amanda", 2, 1, -1, 30, 1, -1)
        call CodeAmandaSexAgreeLeave("")
    return


label CodeAmandaSexAgreeLeave(mode=""):
    menu:
        "Скрепя сердце ограничиться минетом" if mode == "minet":
            "Решив пока удовлетвориться малым, вы не стали отказывать даме в ее просьбе и галантно расстегнули штаны, придвинув свое сокровенное к губам Аманды."
            python:
                _aah_slut_friends_increase("amanda", 20, 3, 1, 35, 5, 1)
            if renpy.has_label("ShowImageSeq"):
                call ShowImageSeq("amanda", "sexroom", "minet", 12)
            call CodeAmandaSexScene

        "Распрощаться и вернуться в зал":
            "\"Ну нет так нет!\" — гордо сказали вы. \"Не очень-то и хотелось! Значит вот как ты ко мне относишься? Я думал, что у тебя хоть капелька совести есть. Что ж, раз так, то оставляю тебя подумать над своим поведением.\""
            "И, оставив Аманду размышлять над тем, как связаны отказ от ваших домогательств с предполагаемым отсутствием у нее совести, вы покинули ее комнату."
            python:
                _aah_slut_friends_increase("amanda", 10, 1, -1, 25, 1, -1)
            $ AmandaVar["kickyoufromroom"] = 1
            jump TavernMain

        "Проигнорировать ее лепет и продолжить приставать":
            "Решив, что это она не всерьез, вы решительным хозяйским движением ухватили ее одной рукой за сиську, а другой полезли Аманде между ног."
            call CodeAmandaKickFromRoom("afterdeny")
    return
