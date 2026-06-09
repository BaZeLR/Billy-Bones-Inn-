# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label GeorgettBeckyVisit:
    python:
        BeckyVar.setdefault("EddieGeorg", 0)
        BeckyVar.setdefault("visitedhome", 0)
        BeckyVar.setdefault("BeckyOpenMinet", 0)
        IngaVar.setdefault("Knowher", 0)
        EddieVar.setdefault("SawMomSex", 0)
        sluttiness.setdefault("becky", 0)
        sluttiness.setdefault("inga", 0)
        sluttiness.setdefault("georgett", 0)
        Friends.setdefault("eddie", 0)
        Friends.setdefault("becky", 0)
        Friends.setdefault("inga", 0)
        Friends.setdefault("georgett", 0)

        georgedinnersex = 1
        BeckyGuestSexDesc = ""

    "Ужин уже практически закончился, как вдруг послышался негромкий стук в дверь."
    if BeckyVar.get("EddieGeorg", 0) == 1:
        "Эдди, услышав его, вскочил и побежал отпирать дверь. И вот на пороге показалась ваша старая знакомая — Жоржетта."
        "\"Госпожа Блэнкеншип, вы же сказали Инге чтобы она не стеснялась, приводила своего Лукаса к нам, мол дело молодое? Я так понял, что это и ко мне относится. Вот подружка моя, Жоржетта,\" — скороговоркой протарабанил Эдди."
        "\"Эдди, ну да, то что относится к Инге относится и к тебе, но ведь твоя подруга вроде намного старше тебя?\" — в смятении ответила ему Ребекка."
        "\"Ну и что, может мне как раз и нравятся женщины твоего возраста,\" — нагло ответил Эдди."
        "\"Ну а раз ты советовала нам не стеснятся, то мы и не будем, не правда ли, дорогуша?\""
        "\"Конечно,\" ответила Жоржетта, и встала перед Эдди на колени."
    else:
        "\"Эй, Эдди, похоже твоя подружка пришла,\" — воскликнул Лукас. \"Смотри не разорись,\" добавил он."
        "Эдди, не обращая внимания на его сарказм, вскочил и побежал отпирать дверь. Стучала Жоржетта."
        "Без особых прелюдий Жоржетта, встав перед Эдди на колени, решительно приспустила с парня штаны."

    "Жоржетта обнажила его быстро твердеющий член и, дав всем полюбоваться, сначала облизала головку, а потом профессионально начала делать минет."
    "Происходящее не оставило окружающих безучастными. Лукас шепнул пару слов Ингенборг, встал, расстегнул штаны, и Инга начала отсасывать своему жениху."
    "Дыхание Ребекки участилось, щеки покрылись румянцем, рука автоматически полезла вниз. Вдова явно была в растерянности."
    $ BeckyVar["visitedhome"] = max(BeckyVar.get("visitedhome", 0), 6)
    call ShowImageSeq("becky", "dinner", "AllMinet", 2)

    python:
        KidsWatch = renpy.random.randint(1, 6)
        desc = "<br><br>"
        if KidsWatch <= 3:
            desc = "Вдруг вы заметили, что дверь в столовую приоткрыта и за вами кто-то подсматривает. "
            if KidsWatch == 1:
                desc += "Это был Ивар, младший сын вдовы. Он не отрываясь смотрел, как отсасывают его мама и старшая сестра, а его рука залезла в штаны."
            elif KidsWatch == 2:
                desc += "Это была юная Эмма, средняя дочка Бекки. Она наблюдает за вашей оргией с интересом, восхищением и возбуждением."
            else:
                desc += "Это была Эмма с маленькой Лаурой, младшей дочкой Бекки. Лаура явно поражена происходящим, а Эмма шепотом комментирует увиденное."
            desc += "<br><br>"

        if renpy.random.randint(1, 2) == 1:
            desc += "Тем временем кончил и Эдди: в последний момент он выдернул член изо рта Жоржетты и залил ей лицо спермой. Та ничуть не смутилась и дочистила его ртом. "
        else:
            desc += "Тем временем кончил и Эдди, прямо в ротик Жоржетты. Шлюшка выпила все до капли! "

        if renpy.random.randint(1, 2) == 1:
            desc += "<br>За Эдди настал черед Лукаса. Прижав голову Инги к своей промежности, он накончал ей полный рот. "
        else:
            desc += "<br>Глядя на Эдди, спустил и Лукас, обкончав Беккиной дочке все лицо и даже немного рыжие волосы. "

        BeckyGuestSexDesc = desc

    jump GeorgettBeckyVisit_menu


label GeorgettBeckyVisit_menu:
    if georgedinnersex <= 0:
        return

    menu:
        "Осмотреть Жоржетту" if georgedinnersex > 0:
            call GirlsDesc("georgett")
            jump GeorgettBeckyVisit_menu

        "Смотреть что будет дальше" if georgedinnersex == 1:
            
            "Ваш взгляд перебегал с Жоржетты на Ингенборг, с Инги на Бекки. Лукас и Эдди млели от того, что с ними вытворяли их дамы."
            "Первым кончил Эдди, выдернул член в последний момент и залил лицо Жоржетты. Та без смущения дочистила его ртом."
            "За Эдди настал черед Лукаса. Прижав голову Инги к своей промежности, он накончал ей полный рот."
            "Вдова, не отрываясь, смотрела на Эдди и Ингу, ее руки неосознанно мяли собственную грудь."
            "Вдруг, поняв что все закончилось, Бекки пришла в себя и строго сказала первое, что пришло ей на ум: \"Дети, если вы закончили, то помогите убрать со стола.\""
            call ShowImageSeq("becky", "dinner", "SurpMinet", 2)
            $ PregnancyCheck("inga", "mouth", 1, "Лукас")
            $ PregnancyCheck("georgett", "mouthface", 1, "eddie")
            call SlutFriendsIncrease("inga", 0, 0, 0, 50, 1, 1)
            call SlutFriendsIncrease("becky", 0, 0, 0, 50, 1, 1)
            call SlutFriendsIncrease("georgett", 0, 0, 0, 60, 1, 1)
            $ georgedinnersex = 0
            return

        "Расстегнуть штаны и позвать Бекки" if georgedinnersex == 1 and cametoday < cancumdaily:
            $ beckyminetagree = renpy.random.randint(1, 3)

            if sluttiness.get("becky", 0) < 40:
                $ beckyminetagree = 3
            elif BeckyVar.get("BeckyOpenMinet", 0) > 0 and sluttiness.get("becky", 0) + dinnerbeckyorgasm * 5 > 44:
                $ beckyminetagree = 1
            elif sluttiness.get("becky", 0) + dinnerbeckyorgasm * 5 > 46 and beckyminetagree == 2:
                $ beckyminetagree = 1
            elif sluttiness.get("becky", 0) > 50:
                $ beckyminetagree = 1

            if sluttiness.get("becky", 0) <= 55:
                "Решив не отставать от Эдди с Лукасом, вы решительным движением сбросили штаны и показали Бекки на свой член."
                if beckyminetagree > 1:
                    scene
                    "\"Да ты что, Стефан, обалдел?!\" — воскликнула вдова."
                    if BeckyVar.get("BeckyOpenMinet", 0) > 0:
                        "\"Если я один раз тебе уступила, это не значит, что всегда буду отсасывать по мановению пальчика. Ты зарываешься. На сегодня — пока.\""
                    else:
                        "\"Да, я сказала Инге и Эдди не стесняться, но к тебе это не относилось. Сейчас тебе лучше уйти.\""
                    "В расстроенных чувствах вы натянули штаны обратно, помахали рукой остальным и направились на улицу."
                    call SlutFriendsIncrease("becky", 10, 2, -1, 35, 2, -1)
                    $ PregnancyCheck("inga", "mouth", 1, "Лукас")
                    $ PregnancyCheck("georgett", "mouthface", 1, "eddie")
                    call SlutFriendsIncrease("inga", 0, 0, 0, 50, 1, 1)
                    call SlutFriendsIncrease("georgett", 0, 0, 0, 60, 1, 1)
                    $ calendar_v2.advance_minutes(60)
                    $ georgedinnersex = 0
                    jump MarketPlace
                    return
                else:
                    "Несколько секунд Бекки мялась, однако все-таки наклонилась к вашему дружку и начала облизывать головку."
                    "Постепенно распаляясь, Бекки начала умело делать вам минет."
                    "Млея от наслаждения, вы вдруг заметили полный похоти взгляд, которым Эдди одарил свою хозяйку."
                    call ShowImageSeq("becky", "dinner", "BeckyMinet", 2)
            else:
                "Вы поймали взгляд вдовы, направленный на ваши вздувшиеся бугром штаны."
                "Облизав губы в предвкушении, Ребекка, не смущаясь присутствием Эдди и Инги, встала перед вами на колени, приспустила штаны и начала облизывать ваш поднявшийся орган."
                "Млея от наслаждения, вы заметили полный похоти взгляд, которым Эдди одарил свою хозяйку, и взгляд, который она ему вернула."
                call ShowImageSeq("becky", "dinner", "BeckyMinet", 2)

            $ BeckyVar["BeckyOpenMinet"] = max(1, BeckyVar.get("BeckyOpenMinet", 0))
            call SlutFriendsIncrease("becky", 20, 2, 1, 55, 1, 1)
            $ PregnancyCheck("inga", "mouth", 1, "Лукас")
            $ PregnancyCheck("georgett", "mouthface", 1, "eddie")
            call SlutFriendsIncrease("inga", 0, 0, 0, 55, 1, 1)
            call SlutFriendsIncrease("georgett", 0, 0, 0, 65, 1, 1)
            $ georgedinnersex += 1
            jump GeorgettBeckyVisit_menu

        "Кончить на лицо" if georgedinnersex == 2 and cametoday < cancumdaily:
            
            "Вытащив в последний момент член изо рта любовницы, вы залили спермой ей все лицо."
            $ renpy.say(None, BeckyGuestSexDesc)
            "Вдова, не смущаясь, встретилась взглядом с Ингой и Эдди, подмигнула им и только затем вытерла лицо от белых капель вашего семени."
            "А потом строго сказала первое, что пришло ей на ум: \"Дети, если вы закончили, то помогите убрать со стола.\""
            $ PregnancyCheck("becky", "mouthface", 1, "Вы")
            $ georgedinnersex = 0
            return

        "Кончить в ротик" if georgedinnersex == 2 and cametoday < cancumdaily:
            
            "Ощутив приближающийся оргазм, вы не стали вытаскивать член из горячего ротика Ребекки и даже не предупредили ее."
            "Вдова не смутилась: не поперхнувшись, сглотнула ваше семя и только тогда отпустила начавший обмякать член."
            $ renpy.say(None, BeckyGuestSexDesc)
            "Бекки поймала взгляд Эдди, чуток покраснела, но все-таки, глядя ему в глаза, облизала ваш член от остатков спермы, встала и строго сказала: \"Ну раз мы закончили, то помогите убрать со стола.\""
            $ PregnancyCheck("becky", "mouth", 1, "Вы")
            $ georgedinnersex = 0
            return

    return
