label IntZimmerTalk:
    $ main_ui_begin_talk_state("Разговор с Циммерманом", "zimmer")
    $ current_action_title = "Разговор с Циммерманом"
    $ current_action_content = None
    $ MainTxt = "Десятник Циммерман внимательно смотрит на вас, ожидая, что вы скажете."
    $ CurLocDesc = MainTxt
    call IntZimmerTalkRefresh
    return


label IntZimmerTalkRefresh:
    $ main_ui_begin_talk_state("Разговор с Циммерманом", "zimmer")
    $ current_action_title = "Разговор с Циммерманом"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Посмотреть на десятника", Function(main_ui_call_label, "IntZimmerTalkApply", "look")))

    if Talked.get("Zimmer", 0) < 2 and StolenHorseDays > 0 and ZimmerVar.get("ComplainHorse", 0) == 0:
        $ current_action_items.append(MenuItem("Сообщить о краже лошади", Function(main_ui_call_label, "IntZimmerTalkApply", "horse_report")))

    if Talked.get("Zimmer", 0) < 2 and StolenHorseDays > 0 and ZimmerVar.get("ComplainHorse", 0) == 1:
        $ current_action_items.append(MenuItem("Узнать, как продвигаются поиски украденной лошади", Function(main_ui_call_label, "IntZimmerTalkApply", "horse_progress")))

    if Talked.get("Zimmer", 0) < 2 and BeckyVar.get("KnowSherwood", 0) == 1 and ZimmerVar.get("SherwoodStory", 0) == 0:
        $ current_action_items.append(MenuItem("Спросить о Шервудском лесе", Function(main_ui_call_label, "IntZimmerTalkApply", "sherwood_story_1")))

    if Talked.get("Zimmer", 0) < 2 and BeckyVar.get("KnowSherwood", 0) == 1 and ZimmerVar.get("SherwoodStory", 0) == 1:
        $ current_action_items.append(MenuItem("И что с лесом теперь?", Function(main_ui_call_label, "IntZimmerTalkApply", "sherwood_story_2")))

    if Talked.get("Zimmer", 0) < 2 and RobinVar.get("RobbedNum", 0) > 0 and ZimmerVar.get("ComplainRobin", 0) == 0:
        $ current_action_items.append(MenuItem("Пожаловаться на Робин Гуда", Function(main_ui_call_label, "IntZimmerTalkApply", "robin_report")))

    if Talked.get("Zimmer", 0) < 2 and ZimmerVar.get("ComplainRobin", 0) == 1 and money >= 100:
        $ current_action_items.append(MenuItem("Отдать сотню мараведи", Function(main_ui_call_label, "IntZimmerTalkApply", "pay_100")))
        $ current_action_items.append(MenuItem("Поторговаться", Function(main_ui_call_label, "IntZimmerTalkApply", "haggle")))

    if Talked.get("Zimmer", 0) < 2 and ZimmerVar.get("ComplainRobin", 0) == 2:
        $ current_action_items.append(MenuItem("Узнать как там расследование", Function(main_ui_call_label, "IntZimmerTalkApply", "investigation")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntZimmerTalkApply(choice_code=""):
    if str(choice_code or "") == "look":
        $ MainTxt = "Десятник Циммерман не очень-то похож на подтянутых молодцев с расписных досок. Бравый десятник стар, низок ростом, носат, кучеряв и слегка картавит."
        call ShowImage("Zimmer", "", "Portrait1")
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "horse_report":
        $ MainTxt = "\"Ай-яй, молодой человек, какие ужасы вы рассказываете!\" поразился десятник Циммерман. \"Прямо из конюшни увели! Ну надо же, какая наглость!\nИ ведь не первый раз уже! Ничего, не волнуйтесь, будем искать. А тем временем замок, что ли смените. Или сторожите лошадь вашу.\""
        $ MongolVar["ZimmerKnow"] = 1
        $ ZimmerVar["ComplainHorse"] = 1
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "horse_progress":
        $ MainTxt = "\"Ничего, не волнуйтесь, ищем. Это наша работа!\""
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "sherwood_story_1":
        $ MainTxt = "\"Шервудский лес?\" переспросил старый десятник. \"О, молодой человек, это был прекрасный лес. Пока эльфы эти его не испортили.\""
        $ MainTxt += "\n\n\"И как же они его испортили?\" удивились вы. \"Эльфы же любят лес?\""
        $ MainTxt += "\n\n\"Так они его любят, что там мол и деревца не сруби. В стародавние времена эти лопухие наших лесорубов прямо по опушкам развешивали, мол не руби. Но нрав у Ее Милости крутой, она их от таких шуток отучила. Но этот Шервудский лес по договору все равно был их, так что рубить деревья там запрещалось. Оно конечно и верно, лес-то их, но что же, из-за этого недоразумения уже и воз дров не наруби? Ну или там парочку-троечку? Это ж ерунда, от леса не убудет.\""
        $ MainTxt += "\n\n\"Мой десяток там лес с нашей стороны охранял. Эх молодой человек, золотое это было время, скажу я вам. Я тогда себе, не поверите, два дома отстроил и коляску с парой лошадей купил. Зажил по человечески, сыночков своих хорошо пристроил.\""
        $ MainTxt += "\n\n\"А потом бац - и заявляются эти лопухие. Говорят мол нет леса, все вырубили. Приходим и действительно, одни пни стоят. Его Светлость маркиз Рамон, как ряды пеньков увидел, так разозлиться изволил, подать сюда этих охранников изволил покричать.\""
        $ MainTxt += "\n\n\"И что же вам его Светлость сказать изволил?\" заинтересованно спросили вы."
        $ MainTxt += "\n\n\"Мне? Ничего. Заболел я тяжело, старость не радость. Не смог я поговорить с его Светлостью. А докторишкам, не поверишь, пришлось и коляску с лошадьми, и второй дом отдать. Кровососы! Так и не смог я объяснить его Светлости, что это наверняка эльфы весь лес вырубили. Лицемеры ушастые! Ведь мы, со своей стороны, уж так сторожили, так сторожили!\""
        $ ZimmerVar["SherwoodStory"] = 1
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "sherwood_story_2":
        $ MainTxt = "\"А что с ним? Эти ушастики из Куниделла большой шум подняли. Мол как так, был лес и нет. Но что теперь сделаешь? Никто там за порядком не следит, наша стража - потому что это эльфийская земля, не положенно, а эльфы - потому, что им мол в мертвом лесу находиться, видите ли, неприятно. Так теперь там лихие люди порой шастают, нет на них никакой управы.\""
        $ BeckyVar["SherwoodSuspect"] = BeckyVar.get("SherwoodSuspect", 0) + 5
        $ ZimmerVar["SherwoodStory"] = 2
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "robin_report":
        $ MainTxt = "\"Ай-ай молодой человек, какие вы ужасы рассказываете. Грабеж? И где вы говорите это произошло? На Шервудской вырубке? Очень, очень жаль. Мы должны защищать добрых горожан нашего славного Коитополиса, однако ж эта вырубка находится далековато. Так что порядок мы там, сами понимаете, поддерживать не можем. Правда, если вы решите компенсировать нам расходы, связанные с расследованием, мы можем и поискать грабителей. Путь неблизкий, но из сочуствия и уважения к вам я готов таки удовлетворится сотней мараведи.\""
        call ShowImage("Zimmer", "", "Talk")
        $ ZimmerVar["ComplainRobin"] = 1
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "pay_100":
        $ MainTxt = "\"Таки вы сделали правильный выбор, молодой человек, старый Циммерман все сделает. Завтра же поищу негодяев,\" заверил вас десятник, ловко пряча монеты в карман."
        call ShowImage("Zimmer", "", "Talk")
        $ ZimmerVar["ComplainRobin"] = 2
        $ ZimmerVar["RobinInvestigationDay"] = dayspassed + renpy.random.randint(9, 14)
        $ money -= 100
        call stat
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "haggle":
        $ MainTxt = "\"Господин Циммерман, вы же сами понимаете, я жертва ограбления, денег у меня мало. Вы уж войдите в мое бедственное положение. Помогите сиротинушке! 50 мараведи?\""
        if money >= 500:
            $ MainTxt += "\n\n\"Не дурите старого Циммермана, молодой человек. Я же прекрасно знаю, сколько у вас на самом деле денег,\" отбрил вас десятник."
        else:
            $ MainTxt += "\n\nДесятник осмотрел вас скептически, но все таки сказал:\n\"98 мараведи\"\n\"60\"\n\"97\"\n\"70\"\n\"Ладно, 95\"\n\"80, больше нет!\"\n\"Вы меня совсем по миру пустить хотите, молодой человек, 90! Больше уступить не могу!\"\n\"Согласен!\" радостно заорали вы, и быстро, пока он не передумал отсчитали монеты.\n\"Все моя доброта,\" понуро заявил Циммерман, \"Завтра же пойду и поищу негодяев.\"\nЧерез некоторое время радость от удачной сделки улеглась и вам почему-то стало казаться, что вас накололи.\n\"Странно, с чего бы это?\" подумали вы."
            $ ZimmerVar["ComplainRobin"] = 2
            $ ZimmerVar["RobinInvestigationDay"] = dayspassed + renpy.random.randint(9, 14)
            $ money -= 90
            call stat
        call ShowImage("Zimmer", "", "Talk")
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    if str(choice_code or "") == "investigation":
        if ZimmerVar.get("RobinInvestigationDay", 0) > dayspassed:
            $ MainTxt = "\"Не волнуйтесь молодой человек. Ваше дело в надежных руках! Если старый Циммерман сказал, что найдет негодяев, будьте таки уверены, он их найдет!\" заверил вас бравый десятник."
        else:
            $ MainTxt = "\"Молодой человек!\" торжественно сказал десятник. \"Ваше сообщение полностью подтвердилось! Как я и обещал, я сходил к Шервудкому лесу. И шо вы таки думаете? Все как вы и говорили. Разбойнички именно там и обнаружились. Всей бандой, голубчики.\""
            $ MainTxt += "\n\n\"Так вы их наконец-то арестовали?\" радостно воскликнули вы. Про свои деньги вы осмотрительно решили спросить попозже."
            $ MainTxt += "\n\n\"Как так арестовал?\" удивился Циммерман. \"За кого вы меня принимаете, молодой человек? За светлейшего и храбрейшего рыцаря дона Байярда? Я старый человек. У меня семья, дети, любовницы, дети от любовниц. А вы видели сколько там бандитов? Это таки совершенейшие головорезы, скажу я вам. Нет, мы с вами, молодой человек, договаривались, что я поищу бандитов. Я их таки нашел, уговор я выполнил.\""
            $ MainTxt += "\n\n\"Но стражи же много?\" неуверенно начали вы."
            $ MainTxt += "\n\n\"У них тоже у всех семьи. А лес этот вовсе и не наших землях. Я, молодой человек, дожил до седин отнюдь не из-за мальчишеского задора. Я их нашел, как и уговаривались, но арестовать мы бандитов сейчас не можем. Впрочем если вы их сможете поймать и привести, стража Куниделла будет в долгу перед вами.\""
            $ MainTxt += "\n\nВам почему-то захотелось вдарить десятнику Циммерману. Однако титаническим усилием воли вы сдержались, благо драка с десятником была чревата последствиями. Да и в самом деле, успокоили себя вы, ведь стража сделала, что могла? Сделала. Разве их вина, что она не смогла поймать разбойников? Ну конечно же не их! Так чего же сердится?"
            $ ZimmerVar["ComplainRobin"] = ZimmerVar.get("ComplainRobin", 0) + 1
        call ShowImage("Zimmer", "", "Talk")
        $ Talked["Zimmer"] = Talked.get("Zimmer", 0) + 1
        $ CurLocDesc = MainTxt
        call IntZimmerTalkRefresh
        return

    call CityGuardRestore
    return
