# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Amanda Lover Sex scene - converted from QSP to Ren'Py

label AmandaLoverSex:
    $ main_ui_begin_native_scene_state("Аманда")
    python:
        tmp_guy_known = 0
        tmp_guy_name = RandomNameCode("male")
        tmp_girl_name = RandomNameCode("female")
        
        if renpy.random.randint(1, 4) <= 3:
            tmp_guy_known = 1
            
        amanda_agree_sex = 0

    # Main scene intro
    "Вы подошли поближе и точно: это Аманда "
    
    if Amanda.corruption >= 40 and renpy.random.randint(1, 2) == 1:
        extend "идет под ручку "
    else:
        extend "болтает "
    
    extend "с каким-то хреном. Вы подошли поближе и присмотрелись: "
    
    if tmp_guy_known:
        extend "да это же [tmp_guy_name] "
        if renpy.random.randint(1, 5) <= 3:
            $ random_street = RandomStreetNameCode()
            extend "с улицы [random_street]!"
        else:
            extend ", парень с вашей улицы!"
    else:
        extend "не, этого вы в первый раз видите."

    menu:
        "Отправить ее обратно на работу":
            $ AmandaYellNotWork()
            if Amanda.var_int("prohibitwithguys", 0):
                "\"И это не говоря уже о том, что я запретил тебе приключения на свою манду искать!\" крикнули вы ей вслед."
            
            "А огорченный парень пошел куда-то своей дорогой. Хоть счастье было так близко и доступно, но уплыло из под носа."
            $ _adc_jump_label = AmandaDynamicTakeNextJump()
            if _adc_jump_label and renpy.has_label(_adc_jump_label):
                jump expression _adc_jump_label
            
        "Послушать о чем они говорят":
            "Вы прислушались к дискуссии:"
            
            if Amanda.corruption >= 62:
                "\"Да дам я тебе [tmp_guy_name], зачем же отказывать,\" говорит Аманда своему приятелю. \"Только быстрее, я не могу долго отлучаться. Пошли на старое место!\" и парочка следует куда-то в переулки."
                $ amanda_agree_sex = 2
                $ Amanda.set_var_int("sawwithguys", 1)
                
                menu:
                    "Идти за ними":
                        call amanda_lover_show_sex_scene("sex", tmp_guy_name)
                    "Пусть себе балуются, а я к трактиру":
                        $ AmandaLoverSexCalc(tmp_guy_name, amanda_agree_sex)
                        jump StreetTavern
            
            else:
                if int(Amanda.stats.get("pregnancy", 0) or 0) > 120:
                    if Amanda.corruption > 37:
                        "\"Знаешь что, [tmp_guy_name],\" улыбаясь заявляет Аманда своему дружку. \"Ты похоже станешь папой! Задержка, тошнота по утрам, пузо растет, сомнений нет.\"\n\"Да ладно тебе, Амандочка,\" отвечает тот, \"ты со мной одним что ли кувыркалась?\"\n\"Да может и не ты, вот родится, тогда посмотрим. Я так, чтобы ты если вдруг что не удивлялся.\"\n\"Да я и не удивляюсь. Ну, раз ты уже у нас залетная, то от лишних потрахушек второй раз не залетишь!\" и парень заржал над собственной шуткой. \"Пошли?\""

                        if Amanda.corruption >= 42:
                            "\"Семь бед один ответ! Пошли!\" и парочка следует куда-то в переулки."
                            $ amanda_agree_sex = 2
                            $ Amanda.set_var_int("sawwithguys", 1)

                            menu:
                                "Идти за ними":
                                    call amanda_lover_show_sex_scene("sex", tmp_guy_name)
                                "Пусть себе балуются, а я к трактиру":
                                    $ AmandaLoverSexCalc(tmp_guy_name, amanda_agree_sex)
                                    jump StreetTavern
                        else:
                            call amanda_lover_ask_shy_code
                else:
                    "\"[tmp_guy_name], ну я не уверена!\"\n\"Амандочка, что ж ты ломаешься, давай, соглашайся! Я тут и место рядом неплохое знаю.\" делает свой заход новоявленный ухажер."

                    if Amanda.corruption >= 57:
                        "\"Так я и не ломаюсь, с чего бы это мне от перепихона отказываться? Пошли скорее,\" и парочка следует куда-то в переулки."
                        $ amanda_agree_sex = 2
                        $ Amanda.set_var_int("sawwithguys", 1)

                        menu:
                            "Идти за ними":
                                call amanda_lover_show_sex_scene("sex", tmp_guy_name)
                            "Пусть себе балуются, а я к трактиру":
                                $ AmandaLoverSexCalc(tmp_guy_name, amanda_agree_sex)
                                jump StreetTavern

                    elif Amanda.corruption >= 45:
                        "\"Место он знает! Тоже мне, герой-соблазнитель!\"\n\"А что, я вот тебе, этого, цветочек принес,\" галантно парирует [tmp_guy_name], даря Аманде "

                        $ rand_var = renpy.random.randint(1, 4)
                        if rand_var == 1:
                            extend "ромашку без пары лепестков."
                        elif rand_var == 2:
                            extend "полузасохшую фиалку."
                        else:
                            extend "ворох увядших незабудок."

                        $ rand_var = renpy.random.randint(1, 3)
                        if rand_var == 1:
                            "\"Цветочек он принес?!\" отвечает чуть смягчившись Аманда, \"да иди ты со своим цветочком!\""
                            call amanda_lover_ask_cum_code
                        elif rand_var == 2:
                            "\"Нда, цветочек так себе,\" пробормотала Аманда. \"Ну да ладно, дорог не подарок, дорого внимание. Но могу только ротиком.\""
                            call amanda_lover_ask_minet_agree
                        else:
                            "\"Ну спасибо, хоть кто-то внимание проявил,\" отвечает Аманда.\nНда, не слишком-то целомудренно реагирует Аманда даже на самые немудренные ухаживания."
                            call amanda_lover_ask_cum_code
                    else:
                        call amanda_lover_ask_shy_code
            
            if amanda_agree_sex == 0:
                menu:
                    "Вернуться к трактиру":
                        jump StreetTavern
        
        "Пусть себе балуются, а я к трактиру":
            $ AmandaLoverSexCalc(tmp_guy_name)
            jump StreetTavern

# Supporting functions and scene code
label amanda_lover_show_sex_scene(scene_type, guy_name):
    $ main_ui_begin_native_scene_state("Аманда")
    python:
        amanda_lover_build = renpy.random.randint(1, 2)
        amanda_lover_build_get_in = renpy.random.randint(1, 3)
        amanda_lover_build_cum_in = 1
        if scene_type != "minet":
            amanda_lover_build_cum_in = renpy.random.randint(2, 3)

    if amanda_lover_build == 1:
        "[guy_name] и Аманда шли недолго, через пару поворотов галантный кавалер пропустил Аманду первой в какую-то калиточку, а потом зашел туда сам. Легким шагом, делая вид что прогуливаетесь, вы подвалили к этой калиточке и дернули ее на себя."
    else:
        "[guy_name] и Аманда шли довольно долго, так что вы чуть было не потеряли их в лабиринте улочек. Наконец они пришли к какому-то зданию, по виду конюшне. Парочка проскользнула в какую-то дверь, закрыв ее за собой. Легким шагом, делая вид что прогуливаетесь, вы подкрались к этой двери и дернули ее на себя."
    
    "Она не поддалась. Вы дернули ее от себя с тем же результатом.\nУжасная догадка осенила вас: Заперто!\n"
    
    if amanda_lover_build == 1:
        "Но вы не растерялись, а кинулись бегом вокруг забора, пока не нашли участок пониже."
    else:
        "Но вы не растерялись, а обошли здание кругом, внимательно его осматривая, пока наконец не обнаружили приоткрытое окошко и удобно стоящие рядом ящики."
    
    if amanda_lover_build_get_in == 1:
        "Но воспользоваться им вам не удалось: в улочку именно в этот момент зашел патруль городской стражи. Не хватало вам еще чтобы вас приняли за вора. Когда же они прошли, вы начали все-таки карабкаться на стену но было уже поздно."
        
        if amanda_lover_build == 1:
            "Послышался скрежет открывающейся калитки и быстрые шаги. Ломиться же в пустой чужой двор смысла не имеет."
        else:
            "Послышался скрежет открывающейся двери и удаляющиеся шаги. Ломиться же в чужую конюшню смысла не имеет."
    
    else:
        if amanda_lover_build == 1:
            "Ловко подпрыгнув, вы уцепились за край забора, подтянулись, и заглянули во дворик."
            
            if scene_type == "minet":
                "[guy_name] стоит, прислонившись к телеге, а Аманда стоит перед ним на коленях и отсасывает. Вдруг он попробовал было вытащить свой член из ее рта, но она протестующе замычала, принимая весь заряд его семени в рот.\nЗакончив сглатывать, она подняла на него глаза и сказала: \"Но-но, головой надо думать иногда! Если бы твоя сперма попала мне на платье, то как бы потом я его отстирывала? Говорят, что в республике Атлантида именно так уличили в измене жене тамошнего дожа!\"\nНда, не ожидали вы от Аманды такой эрудиции."
                $ ShowImageSeq("amanda", "RandomSex", "minet", 5)
            else:
                "[guy_name] разложил Аманду на телеге и невозбранно трахает ее. Той, похоже, это нравится. Впрочем, вы похоже застали уже самое окончание совокупления, если так можно выразиться."
                $ ShowImage("amanda", "RandomSex", "sex")
        else:
            "Подставив пару ящиков, вы залезли достаточно высоко чтобы осторожно заглянуть в окно. Там вы увидели то, что и ожидали."
            
            if scene_type == "minet":
                "[guy_name] развалился на куче сена, а Аманда, склонившись над ним, делала ему приятное. Собственно вы застали самый финал, когда Аманда получила полный заряд прямо в рот. И что характерно, все проглотила."
                $ ShowImageSeq("amanda", "RandomSex", "minet", 5)
            else:
                "[guy_name] уложил Аманду на куче сена и трахает ее, а та ему с энтузиазмом подмахивает. Причем похоже, что дело близится к концу. Так и есть!"
                $ ShowImage("amanda", "RandomSex", "sex")
        
        if amanda_lover_build_cum_in == 2:
            "[guy_name] даже и не озаботился вытащить свой член из Аманды и кончил прямо в нее."
            
            if int(Amanda.stats.get("pregnancy", 0) or 0) >= 120:
                "Впрочем, более беременной чем сейчас он ее вряд ли сделает, так что можно считать что молодежь достаточна осторожна в сексе."
            elif Amanda.corruption >= 52:
                "Парень похоже ожидал нагоняя за свой поступок, но Аманда на это и внимания не обратила."
            else:
                "\n\"Блин, [guy_name], ты же обещал!\" воскликнула Аманда пытаясь пальцами убрать как можно семени из своего влагалища.\n\"Ну мало ли что я на ком обещал!\" расхототался в ответ молодой подонок, но через секунду все-таки сбавил тон: \"Ну ладно, Амандочка, миласик, я не нарошно, это случайно вышло, ты не подумай чего!\""
        
        elif amanda_lover_build_cum_in == 3:
            "[guy_name] на всякий случай в последний момент вышел из Аманды и излился ей на живот."
            
            if int(Amanda.stats.get("pregnancy", 0) or 0) >= 120:
                "\"Да мог бы и внутрь, разницы уже нет,\" сказала ему Аманда, размазывая семя по надутому животу. Но можно и так, девчонки говорят, что семя коже полезно и от растяжек помогает.\""
            else:
                "\"О, крем!\" сказала Аманда, размазывая сперму по коже. \"Девчонки говорят, что семя для кожи очень полезно!\""
        
        if amanda_lover_build > 1:
            "\n\n\"Видишь, я говорил - приходи со мной на сеновал, не пожалеешь!\" гордо заявляет [guy_name], \"а ты еще смеялась, мол я лучше с кузнецом приду!\"\n\"С каким еще кузнецом?! Я такого не говорила, что ты выдумываешь?\"\n\"Ой, я тебя перепута..., впрочем неважно,\" оставил в недоумении свою подругу [guy_name]."
        
        "\n\nВам уже поздно вмешиваться, парочка собирается и идет к выходу. Устраивать скандал сейчас тоже вроде как не с руки, если надо, то можно поговорить с Амандой в более спокойной обстановке."
    
    # Pregnancy check based on cum location
    if amanda_lover_build_cum_in == 3:
        $ Amanda.pregnancy_check("outside", 1, guy_name, 0, "Соседский парень")
        $ Amanda.change_social(corruption_delta=1)
    elif amanda_lover_build_cum_in == 2:
        $ Amanda.pregnancy_check("inside", 1, guy_name, 0, "Соседский парень")
        $ Amanda.change_social(corruption_delta=1)
    else:
        $ Amanda.pregnancy_check("mouth", 1, guy_name, 0, "Соседский парень")
        $ Amanda.change_social(corruption_delta=1)
    
    # Potential arrest scenario
    if amanda_lover_build_get_in > 1 and renpy.random.randint(1, 7) == 1:
        "Только вы собрались было вернуться к трактиру, как кто-то похлопал вас сзади по плечу."
        
        menu:
            "Обернуться":
                "Вы обернулись и увидели пару стражников укоризненно смотрящих на вас. \"Воруем?\" спросил первый. \"Или еще только готовимся?\" добавил второй.\nВы попробовали было уверить их в том, что вы ни сном, ни духом ничего такого не планировали."
                call ArrestCode
    
    menu:
        "Вернуться в трактир":
            jump StreetTavern

# Amanda responds shyly
label amanda_lover_ask_shy_code:
    if Amanda.stats.get("virginity", True):
        "\"Дурак, я же тебе говорила что я еще девушка и берегу пока себя,\" отбривает наглеца Аманда."
    else:
        "\"Я тебе уже говорила, что нет. Не за ту ты меня принимаешь,\" отбривает наглеца Аманда."
    
    if Amanda.corruption < 40:
        "\"Иди поищи кого еще, поподатливей!\"\nИ с этими словами она гордо разворачивается и идет обратно к трактиру."
    else:
        "Но тут же все портит, добавляя: \"могу только ротиком.\""
        call amanda_lover_ask_minet_agree
    return

# Amanda asks about cumming
label amanda_lover_ask_cum_code:
    "\n\"А ты обещаешь что не кончишь раньше меня?\"\n\"Конечно обещаю, да что я, да я, я всегда о девушке в первую очередь волнуюсь. Не веришь - [tmp_girl_name] подтвердит.\" торопливо обещает [tmp_guy_name].\n\"Да я вот потому и сомневаюсь, что [tmp_girl_name] подтвердила. Только не совсем то.\""
    
    if renpy.random.randint(1, 3) == 1:
        "\"Да врет она все!\"\n\"Совсем ты запутался, то подтвердит, то врет. Ну ладно, бывай!\" обламывает Аманда незадачливого ухажера и идет обратно к трактиру."
    else:
        "\"Да нет, с ней пару накладок конечно было, но теперь я уже научился!\" ловко вывертывается [tmp_guy_name].\n\"А в меня кончать не будешь, вытащишь?\" продолжает уточнять дотошная девица.\n\"Конечно, как скажешь!\" [tmp_guy_name] соглашается на все с готовностью.\n\"А что это в таком случае [RandomNameCode('female')] с пузом ходит? И от кого же это [RandomNameCode('female')] родила в прошлом месяце?\" осведомляется Аманда.\n\"А откуда же мне знать? Я один что ли был? Но делал все как скажут.\" вывернулся парень."
        
        if renpy.random.randint(1, 3) == 1:
            "\"А [tmp_girl_name] эта сама говорила чтоб в нее кончал, мол люблю когда там хлюпает.\" добавил он не совсем складно.\n\"Так ты не кончал или она сама мол просила, ты уж определись. А когда определишься, тогда и поговорим!\" обламывает Аманда незадачливого ухажера и идет обратно к трактиру."
        else:
            "\"Ну ладно, поверю тебе, пошли!\" и парочка следует куда-то в переулки."
            call amanda_lover_ask_sex_agree
    return

# Amanda agrees to blow job
label amanda_lover_ask_minet_agree:
    "\"Ну ладно, пошли,\" соглашается довольный [tmp_guy_name]\n\"Только быстро, а то мне опять на работу пора,\" малость приумеряет его радость Аманда и парочка следует куда-то в переулки."
    
    $ amanda_agree_sex = 1
    $ Amanda.set_var_int("sawwithguys", 1)
    
    menu:
        "Идти за ними":
            call amanda_lover_show_sex_scene("minet", tmp_guy_name)
        
        "Пусть себе балуются, а я к трактиру":
            $ AmandaLoverSexCalc(tmp_guy_name, amanda_agree_sex)
            jump StreetTavern
        
        "Отправить ее обратно на работу":
            $ AmandaYellNotWork()
            if Amanda.var_int("prohibitwithguys", 0):
                "\"И это не говоря уже о том, что я запретил тебе приключения на свою манду искать!\" крикнули вы ей вслед."
            
            "А огорченный парень пошел куда-то своей дорогой. Хоть счастье было так близко и доступно, но уплыло из под носа."
            $ _adc_jump_label = AmandaDynamicTakeNextJump()
            if _adc_jump_label and renpy.has_label(_adc_jump_label):
                jump expression _adc_jump_label
    return

# Amanda agrees to sex
label amanda_lover_ask_sex_agree:
    $ amanda_agree_sex = 2
    $ Amanda.set_var_int("sawwithguys", 1)
    
    menu:
        "Идти за ними":
            call amanda_lover_show_sex_scene("sex", tmp_guy_name)
            
        "Пусть себе балуются, а я к трактиру":
            $ AmandaLoverSexCalc(tmp_guy_name, amanda_agree_sex)
            jump StreetTavern
            
        "Отправить ее обратно на работу":
            $ AmandaYellNotWork()
            if Amanda.var_int("prohibitwithguys", 0):
                "\"И это не говоря уже о том, что я запретил тебе приключения на свою манду искать!\" крикнули вы ей вслед."
            
            "А огорченный парень пошел куда-то своей дорогой. Хоть счастье было так близко и доступно, но уплыло из под носа."
            $ _adc_jump_label = AmandaDynamicTakeNextJump()
            if _adc_jump_label and renpy.has_label(_adc_jump_label):
                jump expression _adc_jump_label
    return
