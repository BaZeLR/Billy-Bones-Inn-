# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

label IntZimmerTalk:
    $ renpy.dynamic("_zimmer_name", "_clara_booklet_thread", "_zimmer_talk_new")
    $ Zimmer.mark_known()
    $ _zimmer_name = "zimmer"
    $ _clara_booklet_thread = threads.get("claraBookletMarket")
    $ _zimmer_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != "zimmer"
    $ main_ui_begin_talk_state("Разговор с Циммерманом", _zimmer_name)
    if _zimmer_talk_new:
        $ scene_runtime.text = "Десятник Циммерман внимательно смотрит на вас, ожидая, что вы скажете."
        $ scene_runtime.location_text = scene_runtime.text

    while True:
        $ _clara_booklet_thread = threads.get("claraBookletMarket")
        menu:
            "Посмотреть на десятника":
                call IntZimmerTalkLook
            "Сообщить о краже лошади" if int(Zimmer.talked_today or 0) < 2 and player.horse.stolen_days > 0 and Zimmer.horse_complaint_stage == 0:
                call IntZimmerTalkHorseReport
            "Узнать, как продвигаются поиски украденной лошади" if int(Zimmer.talked_today or 0) < 2 and player.horse.stolen_days > 0 and Zimmer.horse_complaint_stage == 1:
                call IntZimmerTalkHorseProgress
            "Спросить о Шервудском лесе" if int(Zimmer.talked_today or 0) < 2 and Becky.knows_blackwood and Zimmer.sherwood_story_stage == 0:
                call IntZimmerTalkSherwoodStory1
            "И что с лесом теперь?" if int(Zimmer.talked_today or 0) < 2 and Becky.knows_blackwood and Zimmer.sherwood_story_stage == 1:
                call IntZimmerTalkSherwoodStory2
            "Пожаловаться на Робин Гуда" if int(Zimmer.talked_today or 0) < 2 and Robin.robbery_count > 0 and Zimmer.robin_complaint_stage == 0:
                call IntZimmerTalkRobinReport
            "Отдать сотню мараведи" if int(Zimmer.talked_today or 0) < 2 and Zimmer.robin_complaint_stage == 1 and player.economy.money >= 100:
                call IntZimmerTalkPay100
            "Поторговаться" if int(Zimmer.talked_today or 0) < 2 and Zimmer.robin_complaint_stage == 1 and player.economy.money >= 100:
                call IntZimmerTalkHaggle
            "Узнать как там расследование" if int(Zimmer.talked_today or 0) < 2 and Zimmer.robin_complaint_stage == 2:
                call IntZimmerTalkInvestigation
            "Похвастаться вином для ночной стражи" if int(Zimmer.talked_today or 0) < 2 and _clara_booklet_thread is not None and int(_clara_booklet_thread.num or 0) == 7 and not Mongol.guard_captain_known and int(player.tavern_management.winenum or 0) > 0:
                call IntZimmerTalkMongolWineDistraction
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return


label IntZimmerTalkLook:
    $ scene_runtime.text = "Десятник Циммерман не очень-то похож на подтянутых молодцев с расписных досок. Бравый десятник стар, низок ростом, носат, кучеряв и слегка картавит."
    vscene "images/zimmer/portrait1.png"
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkHorseReport:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "\"Ай-яй, молодой человек, какие ужасы вы рассказываете!\" поразился десятник Циммерман. \"Прямо из конюшни увели! Ну надо же, какая наглость!\nИ ведь не первый раз уже! Ничего, не волнуйтесь, будем искать. А тем временем замок, что ли смените. Или сторожите лошадь вашу.\""
    $ Mongol.zimmer_knows_horse_theft = True
    $ Zimmer.horse_complaint_stage = 1
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkHorseProgress:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "\"Ничего, не волнуйтесь, ищем. Это наша работа!\""
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkSherwoodStory1:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "\"Шервудский лес?\" переспросил старый десятник. \"О, молодой человек, это был прекрасный лес. Пока эльфы эти его не испортили.\""
    $ scene_runtime.text += "\n\n\"И как же они его испортили?\" удивились вы. \"Эльфы же любят лес?\""
    $ scene_runtime.text += "\n\n\"Так они его любят, что там мол и деревца не сруби. В стародавние времена эти лопухие наших лесорубов прямо по опушкам развешивали, мол не руби. Но нрав у Ее Милости крутой, она их от таких шуток отучила. Но этот Шервудский лес по договору все равно был их, так что рубить деревья там запрещалось. Оно конечно и верно, лес-то их, но что же, из-за этого недоразумения уже и воз дров не наруби? Ну или там парочку-троечку? Это ж ерунда, от леса не убудет.\""
    $ scene_runtime.text += "\n\n\"Мой десяток там лес с нашей стороны охранял. Эх молодой человек, золотое это было время, скажу я вам. Я тогда себе, не поверите, два дома отстроил и коляску с парой лошадей купил. Зажил по человечески, сыночков своих хорошо пристроил.\""
    $ scene_runtime.text += "\n\n\"А потом бац - и заявляются эти лопухие. Говорят мол нет леса, все вырубили. Приходим и действительно, одни пни стоят. Его Светлость маркиз Рамон, как ряды пеньков увидел, так разозлиться изволил, подать сюда этих охранников изволил покричать.\""
    $ scene_runtime.text += "\n\n\"И что же вам его Светлость сказать изволил?\" заинтересованно спросили вы."
    $ scene_runtime.text += "\n\n\"Мне? Ничего. Заболел я тяжело, старость не радость. Не смог я поговорить с его Светлостью. А докторишкам, не поверишь, пришлось и коляску с лошадьми, и второй дом отдать. Кровососы! Так и не смог я объяснить его Светлости, что это наверняка эльфы весь лес вырубили. Лицемеры ушастые! Ведь мы, со своей стороны, уж так сторожили, так сторожили!\""
    $ Zimmer.sherwood_story_stage = 1
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkSherwoodStory2:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "\"А что с ним? Эти ушастики из Куниделла большой шум подняли. Мол как так, был лес и нет. Но что теперь сделаешь? Никто там за порядком не следит, наша стража - потому что это эльфийская земля, не положенно, а эльфы - потому, что им мол в мертвом лесу находиться, видите ли, неприятно. Так теперь там лихие люди порой шастают, нет на них никакой управы.\""
    $ Becky.sherwood_suspicion += 5
    $ Zimmer.sherwood_story_stage = 2
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkRobinReport:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "\"Ай-ай молодой человек, какие вы ужасы рассказываете. Грабеж? И где вы говорите это произошло? На Шервудской вырубке? Очень, очень жаль. Мы должны защищать добрых горожан нашего славного Коитополиса, однако ж эта вырубка находится далековато. Так что порядок мы там, сами понимаете, поддерживать не можем. Правда, если вы решите компенсировать нам расходы, связанные с расследованием, мы можем и поискать грабителей. Путь неблизкий, но из сочуствия и уважения к вам я готов таки удовлетворится сотней мараведи.\""
    vscene "images/zimmer/talk.png"
    $ Zimmer.robin_complaint_stage = 1
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkPay100:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "\"Таки вы сделали правильный выбор, молодой человек, старый Циммерман все сделает. Завтра же поищу негодяев,\" заверил вас десятник, ловко пряча монеты в карман."
    vscene "images/zimmer/talk.png"
    $ Zimmer.robin_complaint_stage = 2
    $ Zimmer.robin_investigation_day = current_game_day() + procedural_randint(9, 14, "zimmer_robin_investigation_%s" % current_game_day())
    $ player.spend_money(100)
    call stat
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkHaggle:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "\"Господин Циммерман, вы же сами понимаете, я жертва ограбления, денег у меня мало. Вы уж войдите в мое бедственное положение. Помогите сиротинушке! 50 мараведи?\""
    if player.economy.money >= 500:
        $ scene_runtime.text += "\n\n\"Не дурите старого Циммермана, молодой человек. Я же прекрасно знаю, сколько у вас на самом деле денег,\" отбрил вас десятник."
    else:
        $ scene_runtime.text += "\n\nДесятник осмотрел вас скептически, но все таки сказал:\n\"98 мараведи\"\n\"60\"\n\"97\"\n\"70\"\n\"Ладно, 95\"\n\"80, больше нет!\"\n\"Вы меня совсем по миру пустить хотите, молодой человек, 90! Больше уступить не могу!\"\n\"Согласен!\" радостно заорали вы, и быстро, пока он не передумал отсчитали монеты.\n\"Все моя доброта,\" понуро заявил Циммерман, \"Завтра же пойду и поищу негодяев.\"\nЧерез некоторое время радость от удачной сделки улеглась и вам почему-то стало казаться, что вас накололи.\n\"Странно, с чего бы это?\" подумали вы."
        $ Zimmer.robin_complaint_stage = 2
        $ Zimmer.robin_investigation_day = current_game_day() + procedural_randint(9, 14, "zimmer_robin_haggle_%s" % current_game_day())
        $ player.spend_money(90)
        call stat
    vscene "images/zimmer/talk.png"
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkInvestigation:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    if Zimmer.robin_investigation_day > current_game_day():
        $ scene_runtime.text = "\"Не волнуйтесь молодой человек. Ваше дело в надежных руках! Если старый Циммерман сказал, что найдет негодяев, будьте таки уверены, он их найдет!\" заверил вас бравый десятник."
    else:
        $ scene_runtime.text = "\"Молодой человек!\" торжественно сказал десятник. \"Ваше сообщение полностью подтвердилось! Как я и обещал, я сходил к Шервудкому лесу. И шо вы таки думаете? Все как вы и говорили. Разбойнички именно там и обнаружились. Всей бандой, голубчики.\""
        $ scene_runtime.text += "\n\n\"Так вы их наконец-то арестовали?\" радостно воскликнули вы. Про свои деньги вы осмотрительно решили спросить попозже."
        $ scene_runtime.text += "\n\n\"Как так арестовал?\" удивился Циммерман. \"За кого вы меня принимаете, молодой человек? За светлейшего и храбрейшего рыцаря дона Байярда? Я старый человек. У меня семья, дети, любовницы, дети от любовниц. А вы видели сколько там бандитов? Это таки совершенейшие головорезы, скажу я вам. Нет, мы с вами, молодой человек, договаривались, что я поищу бандитов. Я их таки нашел, уговор я выполнил.\""
        $ scene_runtime.text += "\n\n\"Но стражи же много?\" неуверенно начали вы."
        $ scene_runtime.text += "\n\n\"У них тоже у всех семьи. А лес этот вовсе и не наших землях. Я, молодой человек, дожил до седин отнюдь не из-за мальчишеского задора. Я их нашел, как и уговаривались, но арестовать мы бандитов сейчас не можем. Впрочем если вы их сможете поймать и привести, стража Куниделла будет в долгу перед вами.\""
        $ scene_runtime.text += "\n\nВам почему-то захотелось вдарить десятнику Циммерману. Однако титаническим усилием воли вы сдержались, благо драка с десятником была чревата последствиями. Да и в самом деле, успокоили себя вы, ведь стража сделала, что могла? Сделала. Разве их вина, что она не смогла поймать разбойников? Ну конечно же не их! Так чего же сердится?"
        $ Zimmer.robin_complaint_stage += 1
    vscene "images/zimmer/talk.png"
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntZimmerTalkMongolWineDistraction:
    $ renpy.dynamic("_zimmer_name")
    $ _zimmer_name = "zimmer"
    $ scene_runtime.text = "Вы как бы между делом рассказываете Циммерману, что в трактире остался отличный бочонок, который не стыдно отправить доблестным ночным стражникам у караулки. Десятник заметно оживляется и тут же начинает рассуждать, как важно поддерживать людей на посту.\n\n\"Вот это, молодой человек, правильное понимание общественного порядка,\" важно кивает он. \"У хорошего хозяина и стража сыта, и город спокоен.\""
    vscene "images/zimmer/talk.png"
    $ Mongol.guard_captain_known = True
    $ Zimmer.change_social(friend_delta=1)
    $ Zimmer.mark_talked(1)
    $ scene_runtime.location_text = scene_runtime.text
    return
