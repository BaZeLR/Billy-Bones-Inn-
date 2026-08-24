label story_amanda_tavern_seduction_0:
    show screen main_ui
    call ShowImage("amanda", "", "amanda_portrait.jpg")
    "В зале Аманда задержалась у стойки дольше обычного. Она будто ждала, пока вы заметите ее новое платье, поправила волосы и улыбнулась слишком невинно."
    "Это еще не прямое приглашение, но уже и не простая болтовня работницы с хозяином."
    menu:
        "Подыграть":
            "Вы ответили ей в том же тоне. Аманда вспыхнула, но не отступила, только ниже опустила голос и пообещала вечером быть послушнее, если вы тоже будете к ней внимательнее."
            $ Amanda.change_mana(1, "tavern_seduction_attention")
            $ Amanda.apply_social_chance(0, 0, 1, 2, 0, 0, "tavern_seduction_attention")
            return True
        "Позвать наверх" if int(Amanda.rel or 0) >= 12 and int(Amanda.corruption or 0) >= 35:
            "Вы тихо предложили ей оставить зал на пару минут. Аманда посмотрела на лестницу, прикусила губу и пошла первой."
            jump TavernAmandaRoom
        "Вернуть к работе":
            $ Amanda.yell_not_work()
            return True


label story_amanda_legare_tavern_visit_0:
    show screen main_ui
    call ShowImage("alber", "", "portrait")
    "Ближе к вечеру в трактир заглянул месье Легаре. Он заказал кувшин вина не у стойки, а так, чтобы Аманда сама подошла к его столу."
    "Аманда старалась держаться деловито, но ее улыбка выдавала, что этот визит не совсем случайный."
    menu:
        "Понаблюдать":
            "Вы не вмешались. Легаре говорил тихо и обходительно, Аманда отвечала коротко, но задерживалась у его стола каждый раз чуть дольше, чем требовала работа."
            $ Amanda.legare_affection = min(20, Amanda.legare_affection + 1)
            return True
        "Отозвать Аманду":
            "Вы позвали Аманду к стойке и нашли ей работу подальше от столика Легаре. Она подчинилась, но бросила на вас недовольный взгляд."
            $ Amanda.legare_affection = max(0, Amanda.legare_affection - 1)
            $ Amanda.change_mana(-1, "blocked_legare_tavern_visit")
            return True
        "Прямо запретить":
            "Вы велели Аманде не крутиться у стола Легаре. Виноторговец вежливо поднял руки, будто ни при чем, а Аманда побледнела от злости и стыда."
            $ Amanda.legare_forbidden = True
            $ Amanda.legare_affection = max(0, Amanda.legare_affection - 2)
            $ Amanda.change_mana(-2, "forbid_legare_tavern_visit")
            return True


label story_amanda_street_legare_sighting_0:
    $ renpy.dynamic("_amanda_legare_event")
    show screen main_ui
    $ _amanda_legare_event = None
    call ShowImage("amanda", "", "amanda_portrait.jpg")
    if str(rooms.current_code or "") == "MarketPlace":
        "Между лавками вы заметили Аманду. Она шла быстро, то и дело оглядываясь, а впереди у винных рядов ее явно ждал месье Легаре."
    else:
        "У выхода из трактира Аманда скользнула вдоль стены так осторожно, будто сама понимала, насколько неубедительно выглядит ее тайная прогулка."
        "За углом мелькнул знакомый силуэт Легаре."
    menu:
        "Проследить за ней":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun") <= 0:
                return False
            $ _amanda_legare_event = GetSexEventFromTable("amanda", calendar_v2.time_slot(), "legarerun")
            jump AfterDanceSexLegare
        "Оставить ее в покое":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun") <= 0:
                return False
            $ _amanda_legare_event = GetSexEventFromTable("amanda", calendar_v2.time_slot(), "legarerun")
            "Вы решили не устраивать сцену на улице. Аманда скоро скрылась за поворотом, почти наверняка догнав Легаре."
            $ Amanda.resolve_legare_let_go()
            return True
        "Отправить ее обратно на работу":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun") <= 0:
                return False
            $ _amanda_legare_event = GetSexEventFromTable("amanda", calendar_v2.time_slot(), "legarerun")
            $ Amanda.yell_not_work()
            return True


label story_amanda_street_lover_encounter_0:
    show screen main_ui
    call ShowImage("amanda", "", "amanda_portrait.jpg")
    "На улице вы заметили Аманду рядом с каким-то молодым горожанином. Он что-то торопливо доказывал, а она смеялась и не спешила уходить."
    menu:
        "Подойти ближе":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "lovermeet") <= 0:
                return False
            $ GetSexEventFromTable("amanda", calendar_v2.time_slot(), "lovermeet")
            jump AmandaLoverSex
        "Окликнуть Аманду и вернуть к работе":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "lovermeet") <= 0:
                return False
            $ GetSexEventFromTable("amanda", calendar_v2.time_slot(), "lovermeet")
            $ Amanda.yell_not_work()
            return True
        "Не вмешиваться":
            "Вы прошли мимо. Если Аманда решила искать себе приключения, то этот разговор еще можно будет отложить до вечера."
            return True
