init python:
    def amanda_liza_glory_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default)

    def amanda_liza_talk_work_ready():
        return tavern_work_planned_for("AmandaLizaTalk", CurLoc, time)

    def amanda_liza_glory_invite_ready():
        current_day = amanda_liza_glory_int(dayspassed, 0)
        invite_day = amanda_liza_glory_int(Amanda.var.get("glory_liza_invite_day", -1), -1)
        return (
            str(CurLoc or "") == "TavernMain"
            and amanda_liza_glory_int(Amanda.var.get("glory_liza_invite_seen", 0), 0) == 1
            and amanda_liza_glory_int(Amanda.var.get("glorytried", 0), 0) == 0
            and amanda_liza_glory_int(Amanda.var.get("liza_glory_hint_seen_day", -1), -1) >= 0
            and invite_day <= current_day
            and invite_day >= current_day - 1
            and amanda_liza_glory_int(Amanda.var.get("liza_glory_invite_event_seen_day", -1), -1) != current_day
            and amanda_liza_glory_int(TavernGloryHole, 0) == 2
        )

    def amanda_glory_tavern_aftermath_ready():
        current_day = amanda_liza_glory_int(dayspassed, 0)
        last_day = amanda_liza_glory_int(Amanda.var.get("glory_last_event_day", -1), -1)
        return (
            str(CurLoc or "") == "TavernMain"
            and last_day >= 0
            and last_day >= current_day - 1
            and amanda_liza_glory_int(Amanda.var.get("glory_tavern_aftermath_seen_day", -1), -1) != current_day
            and amanda_liza_glory_int(Amanda.var.get("glorytried", 0), 0) == 1
        )

    def amanda_night_after_glory_ready():
        current_day = amanda_liza_glory_int(dayspassed, 0)
        last_day = amanda_liza_glory_int(Amanda.var.get("glory_last_event_day", -1), -1)
        return (
            str(CurLoc or "") == "TavernAmandaRoom"
            and amanda_liza_glory_int(time, 0) >= 4
            and last_day >= 0
            and last_day >= current_day - 2
            and amanda_liza_glory_int(Amanda.var.get("night_after_glory_seen_day", -1), -1) != current_day
            and amanda_liza_glory_int(Amanda.var.get("glorytried", 0), 0) == 1
        )


label story_amanda_liza_talk_work_0:
    $ SignalBlockTime = 1
    $ _amanda_liza_work_row = tavern_work_pop_planned_code("AmandaLizaTalk", time, True, "TavernMain")
    if not _amanda_liza_work_row:
        return False
    $ amanda_mark_story_seen_today("liza_talk_seen_day")
    call EventAmandaLizettTalk(1)
    $ TavernEventOngoing = str(_return or "")
    if str(TavernEventOngoing or "").strip():
        $ MainTxt = TavernEventOngoing
        $ CurLocDesc = MainTxt
        call screen main_ui
        return True
    return False


label story_amanda_liza_glory_invite_0:
    $ SignalBlockTime = 1
    $ Amanda.var["liza_glory_invite_event_seen_day"] = int(dayspassed or 0)
    call ShowImage("amanda", "tavern", "lizatalk1")
    "После разговора с Лизеттой Аманда весь вечер вертится возле зала и то и дело косится в сторону ширмы глорихола."
    "Она делает вид, будто просто ищет работу, но слишком быстро краснеет, когда замечает ваш взгляд."
    menu:
        "Пойти к глорихолу":
            jump TavernGloryHole
        "Не вмешиваться":
            "Вы оставляете ее решение за ней. Если Аманда правда решится, следы этого разговора еще всплывут."
            return True


label story_amanda_glory_tavern_aftermath_0:
    $ SignalBlockTime = 1
    $ Amanda.var["glory_tavern_aftermath_seen_day"] = int(dayspassed or 0)
    call ShowImage("amanda", "tavern", "lizatalk2")
    if int(Amanda.var.get("gloryscold", 0) or 0) > 0:
        "В зале Аманда держится от ширмы подальше. Лизетта пытается что-то шепнуть ей на ухо, но Аманда только мотает головой и снова хватается за работу."
    elif int(Amanda.var.get("glorysuck", 0) or 0) > 0:
        "Аманда и Лизетта переглядываются через зал так, будто у них появился общий секрет. При вас Аманда молчит, но улыбку спрятать не может."
    elif int(Amanda.var.get("glorywalkout", 0) or 0) > 0:
        "Аманда старается вести себя обычно, но каждый раз, проходя мимо ширмы, сбивается с шага. Лизетта только хихикает и подталкивает ее локтем."
    else:
        "После смены у глорихола Аманда стала внимательнее слушать Лизетту и чаще задерживаться рядом с ней, будто проверяет себя на смелость."
    return True


label story_amanda_night_after_glory_0:
    $ SignalBlockTime = 1
    $ Amanda.var["night_after_glory_seen_day"] = int(dayspassed or 0)
    call ShowImage("amanda", "room", "night")
    if int(Amanda.var.get("gloryscold", 0) or 0) > 0:
        "Ночью Аманда встречает вас настороженно. Разговор у глорихола еще стоит между вами, и она явно ждет, будете ли вы снова давить на нее."
    elif int(Amanda.var.get("glorysuck", 0) or 0) > 0:
        "Аманда делает вид, что уже почти спит, но когда вы входите, не отворачивается. После истории у глорихола молчание между вами стало другим."
    else:
        "В комнате Аманда долго не ложится. Она смущенно поправляет покрывало и избегает смотреть вам в глаза, будто дневной разговор с Лизеттой догнал ее только сейчас."
    return True
