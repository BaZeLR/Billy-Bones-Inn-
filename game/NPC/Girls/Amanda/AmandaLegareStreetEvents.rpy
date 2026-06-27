init python:
    def amanda_story_seen_today(key):
        return int(Amanda.story_value(key, -1) or -1) == int(dayspassed or 0)

    def amanda_mark_story_seen_today(key):
        Amanda.set_story_value(key, int(dayspassed or 0))
        return True

    def amanda_tavern_seduction_ready():
        return (
            str(getLocation("amanda") or "") == "TavernMain"
            and not amanda_story_seen_today("tavern_seduction_seen_day")
            and int(Amanda.rel or 0) >= 8
            and int(Amanda.corruption or 0) >= 25
            and Amanda.var_int("kickyoufromroom", 0) == 0
        )

    def amanda_legare_tavern_visit_ready():
        return (
            str(getLocation("amanda") or "") == "TavernMain"
            and str(getLocation("alber") or "") == "TavernMain"
            and not amanda_story_seen_today("legare_tavern_visit_seen_day")
            and Amanda.var_int("alberfriends", 0) >= 5
            and Amanda.var_int("alberprohibit", 0) == 0
        )

    def amanda_street_legare_sighting_ready(location_name=""):
        return (
            str(location_name or CurLoc or "") in ("StreetTavern", "MarketPlace")
            and not amanda_story_seen_today("street_legare_sighting_seen_day")
            and CheckIfSexEventExist("amanda", time, "legarerun") > 0
        )

    def amanda_street_lover_encounter_ready(location_name=""):
        return (
            str(location_name or CurLoc or "") in ("StreetTavern", "MarketPlace")
            and not amanda_story_seen_today("street_lover_encounter_seen_day")
            and CheckIfSexEventExist("amanda", time, "lovermeet") > 0
        )


label story_amanda_tavern_seduction_0:
    $ amanda_mark_story_seen_today("tavern_seduction_seen_day")
    call ShowImage("amanda", "", "portrait")
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
            jump TavernMain


label story_amanda_legare_tavern_visit_0:
    $ amanda_mark_story_seen_today("legare_tavern_visit_seen_day")
    call ShowImage("alber", "", "portrait")
    "Ближе к вечеру в трактир заглянул месье Легаре. Он заказал кувшин вина не у стойки, а так, чтобы Аманда сама подошла к его столу."
    "Аманда старалась держаться деловито, но ее улыбка выдавала, что этот визит не совсем случайный."
    menu:
        "Понаблюдать":
            "Вы не вмешались. Легаре говорил тихо и обходительно, Аманда отвечала коротко, но задерживалась у его стола каждый раз чуть дольше, чем требовала работа."
            $ Amanda.set_var_int("alberfriends", min(20, Amanda.var_int("alberfriends", 0) + 1))
            return True
        "Отозвать Аманду":
            "Вы позвали Аманду к стойке и нашли ей работу подальше от столика Легаре. Она подчинилась, но бросила на вас недовольный взгляд."
            $ Amanda.set_var_int("alberfriends", max(0, Amanda.var_int("alberfriends", 0) - 1))
            $ Amanda.change_mana(-1, "blocked_legare_tavern_visit")
            return True
        "Прямо запретить":
            "Вы велели Аманде не крутиться у стола Легаре. Виноторговец вежливо поднял руки, будто ни при чем, а Аманда побледнела от злости и стыда."
            $ Amanda.set_var_int("alberprohibit", 1)
            $ Amanda.set_var_int("alberfriends", max(0, Amanda.var_int("alberfriends", 0) - 2))
            $ Amanda.change_mana(-2, "forbid_legare_tavern_visit")
            return True


label story_amanda_street_legare_sighting_0:
    $ amanda_mark_story_seen_today("street_legare_sighting_seen_day")
    $ _amanda_legare_event = None
    call ShowImage("amanda", "", "portrait")
    if str(CurLoc or "") == "MarketPlace":
        "Между лавками вы заметили Аманду. Она шла быстро, то и дело оглядываясь, а впереди у винных рядов ее явно ждал месье Легаре."
    else:
        "У выхода из трактира Аманда скользнула вдоль стены так осторожно, будто сама понимала, насколько неубедительно выглядит ее тайная прогулка."
        "За углом мелькнул знакомый силуэт Легаре."
    menu:
        "Проследить за ней":
            $ _amanda_legare_event = GetSexEventFromTable("amanda", time, "legarerun")
            jump AfterDanceSexLegare
        "Оставить ее в покое":
            $ _amanda_legare_event = GetSexEventFromTable("amanda", time, "legarerun")
            "Вы решили не устраивать сцену на улице. Аманда скоро скрылась за поворотом, почти наверняка догнав Легаре."
            $ apply_legare_amanda_let_go_code()
            return True
        "Отправить ее обратно на работу":
            $ _amanda_legare_event = GetSexEventFromTable("amanda", time, "legarerun")
            $ Amanda.yell_not_work()
            jump StreetTavern


label story_amanda_street_lover_encounter_0:
    $ amanda_mark_story_seen_today("street_lover_encounter_seen_day")
    call ShowImage("amanda", "", "portrait")
    "На улице вы заметили Аманду рядом с каким-то молодым горожанином. Он что-то торопливо доказывал, а она смеялась и не спешила уходить."
    menu:
        "Подойти ближе":
            $ GetSexEventFromTable("amanda", time, "lovermeet")
            jump AmandaLoverSex
        "Окликнуть Аманду и вернуть к работе":
            $ GetSexEventFromTable("amanda", time, "lovermeet")
            $ Amanda.yell_not_work()
            jump StreetTavern
        "Не вмешиваться":
            "Вы прошли мимо. Если Аманда решила искать себе приключения, то этот разговор еще можно будет отложить до вечера."
            return True
