# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Event Location: FridayDance (Market Square Friday Night Event)
# Converted from legacy script. Handles chained events and dynamic menu logic.
# To be called from the main event dispatcher or location system.

init python:
    def friday_dance_slot_is_active():
        calendar_sync_state()
        return int(week or 0) == 5 and int(time or 0) == 3

    def friday_dance_market_entry_is_active():
        return friday_dance_slot_is_active() and int(FridayDancesCount or 0) < 5

label FridayDance(add_dance_phrase_tmp=""):
    hide screen main_ui
    call EnterLocation("FridayDance")
    $ DanceStep = 0
    $ GirlsCounter = 0
    $ CurrentActions = ""
    $ AddDancePhraseTmp = add_dance_phrase_tmp
    $ BeckyVar["danceinvitehome"] = 0

    if not friday_dance_slot_is_active():
        jump StreetTavern

    call ShowImage("", "", "images/market/LocFridayDance.jpg")

    if navigation_only_mode_enabled():
        "Вы находитесь на рыночной площади в пятничный вечер, когда здесь проходят городские танцы."
        "[navigation_only_message()]"
        "[navigation_only_time_note()]"
        menu:
            "Вернуться к трактиру":
                jump StreetTavern
        return

    if FridayDancesCount < 5:
        "Вы находитесь на рыночной площади. Сейчас вечер пятницы и площадь расчищена от лотков и палаток, которые занимают ее в обычное время. На стенах домов, на колоннах, в общем всюду, висят факелы освещающие праздник хоть и тусклым и колеблющимся, но светом. А народу, похоже, собралось больше чем днем. Кажется полгорода пришло сюда послушать музыку, которую играет маленький оркестр, стоящий на возвышении в центре площади. Ну и конечно потанцевать, куда же без этого. "
        call FridayDanceCounterShow
        if DanceSponsor == 1:
            "В северо-восточном углу площади, под навесом с изображением вставшего на дыбы жеребца, такого же как на вывеске вашего трактира, раздают вино и закуску. Бесплатная выпивка приманивает толпы народа, которые, после посещения вашего ларька, отправляются праздновать дальше уже под шофе, что придает веселью дополнительный колорит."
            $ GirlsCounter = 0
            while GirlsCounter < len(AllGirlNames):
                $ get_girl_drunk(AllGirlNames[GirlsCounter])
                $ GirlsCounter += 1
        "Вы видите всех своих знакомых. Что вы собираетесь делать?"
        menu friday_dance_menu:
            "Понаблюдать за танцующими" if FridayDancesCount < 5 and DanceStep == 0:
                $ rand_friday_dance = renpy.random.randint(1, 8)
                if rand_friday_dance == 1:
                    $ result = "Вы замечаете как молодая пара, танцуя, сливается в страстном поцелуе."
                elif rand_friday_dance == 2:
                    $ result = "Вы смотрите на танцующие парочки. Ваше внимание привлекает одна пара: парень потихоньку перемещает руку с талии на задницу девушки, она же в ответ прижимается к нему еще теснее."
                elif rand_friday_dance == 3 and DanceSponsor == 1:
                    $ result = "Ваша внимание привлекает одна пара: такое впечатление что они забыли о том, что находятся не наедине. Парень во время танца мнет ягодицы своей партнерши, а та, в свою очередь трется о него своей полной грудью. Вы присмотрелись внимательней, и заметили, что раскрасневшаяся шалунья пытается незаметно тереть бугор на оттопыренных штанах парня. Во время очередного круга парень впивается в губы девушки и она ему страстно отвечает."
                elif rand_friday_dance == 4 and DanceSponsor == 1:
                    $ result = "Вы замечаете ушлого парня, который танцует сразу с двумя девицами, по всей видимости сестрами. И позволяет себе много вольностей, то как бы нечаяно заденет за грудь, то потискает попу через юбку, то чмокнет в губы. Сестрицам такой подход по видимому нравятся, они весело смеются и обнимают своего ухажера."
                else:
                    $ result = "Вы наблюдаете за тем, как народ весело отплясывает под разухабистые мелодии."
                call ShowImage("", "", "images/market/LocFridayDance.jpg")
                $ FridayDancesCount += 1
                "[result]"
                call FridayDanceCounterShow
                jump FridayDance
            "Найти Аманду" if FridayDancesCount < 5 and DanceStep == 0 and AmandaVar.get('leftdances',0) == 0:
                $ AmandaVar['albernowdances'] = 0
                if GetDanceFromTable('amanda', 'legare', FridayDancesCount) > 0:
                    $ AmandaVar['albernowdances'] = 1
                    call EventAmandaLegareCreateDance
                $ FridayDancesCount += 1
                if AmandaVar.get('EscapeUnnoticed',0) == 1:
                    $ result = "Вы попробовали найти Аманду, но к своему удивлению не смогли этого сделать. На площади ее не было. Вокруг площади тоже. Может она отправилась домой, а может ее этот хрен Легаре за собой уволок, а может еще что стряслось, но так или иначе вы упустили Аманду."
                    $ AmandaVar['leftdances'] = 1
                elif AmandaVar.get('albernowdances',0) == 1:
                    $ result = "Вы прошлись по площади, ища Аманду, и обнаружили ее c мессиром Легаре."
                    call ShowImage("amanda", "dance", "legare_step_0")
                    $ DanceStep = 1
                else:
                    $ result = "Вы прошлись по площади, ища Аманду, и нашли ее скромно стоящей около одной из колонн."
                    call ShowImage("amanda", "dance", "wait" + str(renpy.random.randint(1, 2)))
                    $ DanceStep = 1
                "[result]"
                if AmandaVar.get('EscapeUnnoticed',0) == 1:
                    call FridayDanceCounterShow
                    jump FridayDance
                call IntAmandaDance
                jump FridayDance
            "Найти Бекки Блэнкеншип" if FridayDancesCount < 5 and DanceStep == 0 and BeckyVar.get('leftdances',0) == 0:
                "Вы прошлись по площади, ища вдовушку Блэнкеншип, и нашли ее болтающей с другими торговками."
                call ShowImage("becky", "dance", "wait")
                $ DanceStep = 1
                $ FridayDancesCount += 1
                call int_becky_dance
                jump FridayDance
            "Заметить Мелиссу и Клариссу среди танцующих" if FridayDancesCount < 5 and DanceStep == 0 and clara_visible_at_friday_dance():
                $ FridayDancesCount += 1
                if clara_can_start_social_events():
                    $ result = "Среди танцующих вы замечаете Мелиссу и Клариссу. Девушки смеются, кружатся под музыку и явно чувствуют себя на празднике совершенно свободно. Кларисса, заметив ваш взгляд, на миг улыбается вам поверх плеча подруги."
                else:
                    $ result = "Среди танцующих вы замечаете Мелиссу и Клариссу. Девушки весело кружатся под музыку и о чем-то шепчутся между собой, а вы пока лишь наблюдаете за ними со стороны."
                "[result]"
                call FridayDanceCounterShow
                jump FridayDance
    else:
        "Праздник закончился и народ расходится."
        
    menu:
        "Вернуться к трактиру":
            jump StreetTavern
            
    # Clean up screen and show any additional phrase
    
    if AddDancePhraseTmp != "":
        "[AddDancePhraseTmp]"
        
    return

label CheckIfAmandaGoneDance:
    if GetDanceJustLeft("amanda", "legare", FridayDancesCount) > 0 or AmandaVar["LegareGo"] == 1:
        if renpy.random.randint(1, 2) == 1:
            $ AmandaVar["leftdances"] = 1
            "Неожиданно вы заметили, что Аманда торопиться куда-то прочь под ручку с мессиром Легаре."
            call LegareAmandaGoMenu
        else:
            $ apply_legare_amanda_let_go_code()
            $ AmandaVar["EscapeUnnoticed"] = 1
    return


label FridayDanceCounterShow:
    if FridayDancesCount < 5:
        "Осталось еще [5-FridayDancesCount] танцев, до того как все разойдутся."
    else:
        "Праздник закончился и народ расходится."
    call CheckIfAmandaGoneDance
    return

