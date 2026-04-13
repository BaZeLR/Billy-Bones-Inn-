init python:
    def RobbedHorseTakeCode():
        global MyStallion, MongolVar, RobinVar
        MyStallion = ''
        MongolVar['WillTryToSteal'] = 0
        RobinVar['KnowBigTitsVillage'] = max(RobinVar['KnowBigTitsVillage'], 1)

    def RobbedAndGoCode():
        global money, BeckyVar, time, RobinVar
        renpy.say(None, 'Идти дальше в Куниделл смысла не было никакого и вы направили свои стопы обратно домой.')
        money = max(0, money-50)
        BeckyVar['RobbedByRobin'] = max(1, BeckyVar['RobbedByRobin'])
        calendar_set_time_slot(4)
        if RobinVar['Negotiate'] == 1:
            RobinVar['Negotiate'] += 1
        RobinVar['RobbedNum'] += 1
        renpy.call('stat')
        renpy.call('TavernMain')

label SherwoodTravel:
    call EnterLocation("SherwoodTravel")
    if navigation_only_mode_enabled():
        "Насвистывая, вы идете по дороге к Куниделлу через вырубку Шервуда."
        "[navigation_only_message()]"
        "[navigation_only_time_note()]"
        menu:
            "Вернутся обратно в Коитополис":
                jump TavernMain
        return
    # OnHorse is passed as an argument
    python:
        _arg_list = _args or ()
        OnHorse = _arg_list[0] if len(_arg_list) > 0 else 0
        RobbersHeadNameTmp = 'Робин Гуд' if RobinVar['KnowHim'] else 'предводитель'
    $ travel_action = 'Ехать' if OnHorse == 1 else 'Идти'
    $ travel_verb = 'едете' if OnHorse == 1 else 'идете'
    "Насвистывая, вы [travel_verb] по дороге к Куниделлу. Через несколько часов поля и перелески уступают место вырубке. И так не сильно наезженная, дорога превращается практически в тропинку, петляющую между пнями и зарослями молодого кустарника."
    if RobinVar['RobbedNum'] == 0:
        "Вдруг вдалеке вы замечаете группу мужчин в зеленых трико."
    elif RobinVar['KnowHim'] == 0:
        "Вдруг вдалеке вы замечаете уже знакомых вам грабителей."
    else:
        "Вдруг вдалеке вы замечаете ваших старых знакомых, несчастных безработных лесорубов, во главе с Робин Гудом."
    menu:
        "[travel_action] дальше":
            call IntRobinTalk
            python:
                renpy.hide_screen('all')
            if RobinVar['RobbedNum'] == 0:
                "Семь бед - один ответ! ... (сюжетный текст)"
                if OnHorse == 1:
                    "Ну и лошадь конечно, она нам тоже пригодится."
                menu:
                    "Попрощаться":
                        python:
                            renpy.hide_screen('all')
                        "Ну ладно, с вами поговорить - одно удовольствие, ... (сюжетный текст)"
                        if money >= 50:
                            "Хорошо еще что вы взяли с собой только 50 мараведи!"
                        if OnHorse == 1:
                            "Еще один лесоруб заботливо взял из ваших рук поводья вашей лошади. ... (сюжетный текст)"
                            python:
                                RobbedHorseTakeCode()
                        python:
                            RobbedAndGoCode()
            else:
                "При виде вас [RobbersHeadNameTmp] и его друзья очень удивились. ... (сюжетный текст)"
                menu:
                    "Ага, вот ваши денежки":
                        python:
                            renpy.hide_screen('all')
                        "Широко, хотя и немного вымученно, улыбаясь, вы вывернули карманы."
                        if money >= 50:
                            "Хорошо еще что вы взяли с собой только 50 мараведи!"
                        "Обездоленные радостно переглянулись. ... (сюжетный текст)"
                        if OnHorse == 1:
                            "В последний момент один из разбойников выхватил у вас повод, ... (сюжетный текст)"
                            python:
                                RobbedHorseTakeCode()
                        "Да, как-то глупо получилось, подумали вы. И зачем я еще раз сюда поперся?"
                        if OnHorse == 1:
                            "Да еще и с конем?"
                        python:
                            RobbedAndGoCode()
            show Robin portrait2
            call AddCleanScreen
    menu:
        "Вернутся обратно в Коитополис":
            if RobinVar['RobbedNum'] == 0:
                $ BeckyVar['SherwoodSuspect'] += 2
                $ BeckyVar['KnowSherwood'] = 1
                "Решив что встреча со странными мужиками в трико на пустынной вырубке"
            elif RobinVar['KnowHim'] == 0:
                "Решив что, по здравому размышлению, встреча с грабителями"
            else:
                "Решив что новая встреча с вашим старым другом Робином, да еще и на пустынной вырубке,"
            "ничего хорошего вам не принесет, вы развернулись и пустились в обратный путь. Может вас преследовали, может нет, но вы благополучно выбрались с вырубки на обжитую местность. Уже смеркалось, поэтому вам ничего не оставалось, как направиться обратно в Коитополис, куда вы и добрались без приключений. На сегодня ваше путешествие закончено."
            $ calendar_set_time_slot(4)
            python:
                renpy.hide_screen('all')
            menu:
                "Домой":
                    jump TavernMain
    return
# ...existing code...
