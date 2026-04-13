default _amanda_dynamic_blocks_initialized = True
default AmandaDynamicNextJump = ""

init python:
    def _adc_i(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def AmandaDynamicTakeNextJump():
        global AmandaDynamicNextJump

        next_label = str(AmandaDynamicNextJump or "")
        AmandaDynamicNextJump = ""
        return next_label

    def CodeAmandaHappyConfirm():
        global Result

        tmpRand = renpy.random.randint(1, 4)
        if tmpRand == 1:
            p1 = '"Вот братик, и ты можешь быть разумным. Если захочешь," '
        elif tmpRand == 2:
            p1 = '"Ну вот теперь ты говоришь дело," '
        elif tmpRand == 3:
            p1 = '"Это ты мудро сказал, не то что прошлый раз," '
        else:
            p1 = '"Вот теперь сразу видно, то все обдумал и говоришь серьезно, а не истеришь как тогда," '

        tmpRand = renpy.random.randint(1, 3)
        if tmpRand == 1:
            p2 = "радостно ответила вам Аманда. "
        elif tmpRand == 2:
            p2 = "обрадованно воскликнула Аманда. "
        else:
            p2 = "сказала Аманда, довольная своей маленькой победой. "

        Result = p1 + p2
        return Result

    def AmandaSexOfferReaction():
        global Result

        tmpGropeReact = 0

        if AmandaVar.get("prohibitliza", 0) or (AmandaVar.get("alberprohibit", 0) and _adc_i(AmandaVar.get("alberfriends", 0), 0) >= 5) or AmandaVar.get("gloryscold", 0):
            if AmandaVar.get("suckyou", 0) or AmandaVar.get("fuckyou", 0):
                if (_adc_i(Friends.get("amanda", 0), 0) >= 12 and _adc_i(sluttiness.get("amanda", 0), 0) >= 40) or _adc_i(sluttiness.get("amanda", 0), 0) >= 50:
                    tmpGropeReact = 4
                    if _adc_i(sluttiness.get("amanda", 0), 0) >= 55 and renpy.random.randint(1, 3) == 1:
                        tmpGropeReact = 3
                elif _adc_i(sluttiness.get("amanda", 0), 0) <= 25 and _adc_i(Friends.get("amanda", 0), 0) <= 10:
                    tmpGropeReact = 2
                elif _adc_i(sluttiness.get("amanda", 0), 0) <= 30 and _adc_i(Friends.get("amanda", 0), 0) <= 5:
                    tmpGropeReact = 2
                else:
                    tmpGropeReact = 3
            else:
                if (_adc_i(Friends.get("amanda", 0), 0) >= 14 and _adc_i(sluttiness.get("amanda", 0), 0) >= 45) or _adc_i(sluttiness.get("amanda", 0), 0) >= 55:
                    tmpGropeReact = 4
                    if _adc_i(sluttiness.get("amanda", 0), 0) >= 55 and renpy.random.randint(1, 3) == 1:
                        tmpGropeReact = 3
                elif _adc_i(sluttiness.get("amanda", 0), 0) <= 30 and _adc_i(Friends.get("amanda", 0), 0) <= 12:
                    tmpGropeReact = 2
                elif _adc_i(sluttiness.get("amanda", 0), 0) <= 35 and _adc_i(Friends.get("amanda", 0), 0) <= 8:
                    tmpGropeReact = 2
                else:
                    tmpGropeReact = 3
        else:
            if AmandaVar.get("suckyou", 0) or AmandaVar.get("fuckyou", 0):
                if _adc_i(Friends.get("amanda", 0), 0) >= 2 and _adc_i(sluttiness.get("amanda", 0), 0) >= 45:
                    tmpGropeReact = 4
                elif _adc_i(Friends.get("amanda", 0), 0) >= 5 and _adc_i(sluttiness.get("amanda", 0), 0) >= 35:
                    tmpGropeReact = 4
                elif _adc_i(Friends.get("amanda", 0), 0) >= 10 and _adc_i(sluttiness.get("amanda", 0), 0) >= 25:
                    tmpGropeReact = 4
                elif _adc_i(Friends.get("amanda", 0), 0) >= 15 and _adc_i(sluttiness.get("amanda", 0), 0) >= 21:
                    tmpGropeReact = 4
                elif _adc_i(Friends.get("amanda", 0), 0) >= 2 and _adc_i(sluttiness.get("amanda", 0), 0) >= 35:
                    tmpGropeReact = 1
                elif _adc_i(Friends.get("amanda", 0), 0) >= 5 and _adc_i(sluttiness.get("amanda", 0), 0) >= 25:
                    tmpGropeReact = 1
                elif _adc_i(Friends.get("amanda", 0), 0) >= 10 and _adc_i(sluttiness.get("amanda", 0), 0) >= 21:
                    tmpGropeReact = 1
            else:
                if _adc_i(Friends.get("amanda", 0), 0) >= 5 and _adc_i(sluttiness.get("amanda", 0), 0) >= 45:
                    tmpGropeReact = 4
                elif _adc_i(Friends.get("amanda", 0), 0) >= 10 and _adc_i(sluttiness.get("amanda", 0), 0) >= 35:
                    tmpGropeReact = 4
                elif _adc_i(Friends.get("amanda", 0), 0) >= 15 and _adc_i(sluttiness.get("amanda", 0), 0) >= 25:
                    tmpGropeReact = 4
                elif _adc_i(Friends.get("amanda", 0), 0) >= 5 and _adc_i(sluttiness.get("amanda", 0), 0) >= 35:
                    tmpGropeReact = 1
                elif _adc_i(Friends.get("amanda", 0), 0) >= 10 and _adc_i(sluttiness.get("amanda", 0), 0) >= 25:
                    tmpGropeReact = 1

        Result = tmpGropeReact
        return tmpGropeReact

    def AmandaLegareSetSexType():
        global Result

        if _adc_i(AmandaVar.get("sucklegare", 0), 0) == 0:
            tmpLegareSexType = 0
        else:
            if _adc_i(AmandaVar.get("fucklegare", 0), 0) == 0:
                if _adc_i(virginity.get("amanda", 1), 1) == 1:
                    if _adc_i(AmandaVar.get("alberfriends", 0), 0) >= 15 and _adc_i(sluttiness.get("amanda", 0), 0) >= 35 and _adc_i(sexacts.get("amanda", 0), 0) >= 5:
                        tmpLegareSexType = 2
                    else:
                        tmpLegareSexType = 1
                else:
                    if _adc_i(AmandaVar.get("alberfriends", 0), 0) >= 12 and _adc_i(sluttiness.get("amanda", 0), 0) >= 32 and _adc_i(sexacts.get("amanda", 0), 0) >= 4:
                        tmpLegareSexType = 3
                    else:
                        tmpLegareSexType = 1
            else:
                if (_adc_i(AmandaVar.get("alberfriends", 0), 0) >= 10 and _adc_i(sluttiness.get("amanda", 0), 0) >= 30) or (_adc_i(AmandaVar.get("alberfriends", 0), 0) >= 5 and _adc_i(sluttiness.get("amanda", 0), 0) >= 40):
                    tmpLegareSexType = 4
                else:
                    tmpLegareSexType = 1

        if _adc_i(pregnancy.get("amanda", 0), 0) >= 120 and tmpLegareSexType == 3:
            tmpLegareSexType = 4

        Result = tmpLegareSexType
        return tmpLegareSexType

    def AmandaNesluhCalc():
        global Result

        AmandaNesluh = 0
        AmandaNesluhBonus = 0

        if _adc_i(AmandaVar.get("glorydeflower", 0), 0) > 0 or _adc_i(AmandaVar.get("fuckyou", 0), 0) > 0:
            AmandaNesluhBonus += 6
        if _adc_i(AmandaVar.get("gloryscold", 0), 0) > 0:
            AmandaNesluhBonus -= 3
        if _adc_i(AmandaVar.get("glorysuck", 0), 0) > 0 or _adc_i(AmandaVar.get("suckyou", 0), 0) > 0:
            AmandaNesluhBonus += 3
        if _adc_i(AmandaVar.get("glorywalkout", 0), 0) > 0:
            AmandaNesluhBonus += 2
        if _adc_i(AmandaVar.get("alberfriends", 0), 0) >= 7:
            AmandaNesluhBonus += 1
        if _adc_i(AmandaVar.get("alberfriends", 0), 0) >= 9:
            AmandaNesluhBonus += 1
        if _adc_i(AmandaVar.get("alberfriends", 0), 0) >= 12:
            AmandaNesluhBonus += 2
        if _adc_i(sluttiness.get("amanda", 0), 0) >= 23:
            AmandaNesluhBonus += 1
        if _adc_i(sluttiness.get("amanda", 0), 0) >= 30:
            AmandaNesluhBonus += 2
        if _adc_i(sluttiness.get("amanda", 0), 0) >= 40:
            AmandaNesluhBonus += 4
        if _adc_i(sluttiness.get("amanda", 0), 0) >= 50:
            AmandaNesluhBonus += 3
        if _adc_i(AmandaVar.get("sucklegare", 0), 0) > 0:
            AmandaNesluhBonus += 2
        if _adc_i(AmandaVar.get("fucklegare", 0), 0) > 0:
            AmandaNesluhBonus += 3
        if _adc_i(AmandaVar.get("deflowerlegare", 0), 0) > 0:
            AmandaNesluhBonus += 3

        AmandaNesluhBonus = min(14, max(1, AmandaNesluhBonus))
        if renpy.random.randint(1, 15) <= AmandaNesluhBonus:
            AmandaNesluh = 1
        if (_adc_i(AmandaVar.get("glorydeflower", 0), 0) or _adc_i(AmandaVar.get("fuckyou", 0), 0)) and AmandaNesluh == 1 and renpy.random.randint(1, 4) <= 3:
            AmandaNesluh = 2
        elif (_adc_i(AmandaVar.get("glorysuck", 0), 0) or _adc_i(AmandaVar.get("suckyou", 0), 0)) and AmandaNesluh == 1 and renpy.random.randint(1, 4) <= 1:
            AmandaNesluh = 2

        Result = AmandaNesluh
        return AmandaNesluh

    def AmandaLoverSexCalc(guy_name="", forced_type=0):
        global Result

        if str(guy_name) != "":
            tmpGuyName = str(guy_name)
        else:
            tmpGuyName = RandomNameCode("male")

        tmpSexType = 0
        if _adc_i(sluttiness.get("amanda", 0), 0) >= 57:
            tmpSexType = 2
        elif _adc_i(pregnancy.get("amanda", 0), 0) > 120:
            if _adc_i(sluttiness.get("amanda", 0), 0) >= 42:
                tmpSexType = 2
            elif _adc_i(sluttiness.get("amanda", 0), 0) >= 40:
                tmpSexType = 1
        else:
            if _adc_i(sluttiness.get("amanda", 0), 0) >= 45:
                if renpy.random.randint(1, 3) == 1:
                    tmpSexType = 1
                elif renpy.random.randint(1, 9) <= 4:
                    tmpSexType = 2
            elif _adc_i(sluttiness.get("amanda", 0), 0) >= 40:
                tmpSexType = 1

        if _adc_i(forced_type, 0) > 0:
            tmpSexType = _adc_i(forced_type, 0)
        if tmpSexType == 2 and renpy.random.randint(1, 2) == 1:
            tmpSexType = 3

        if tmpSexType == 3:
            PregnancyCheck("amanda", "outside", 1, tmpGuyName, 0, "Соседский парень")
            SlutFriendsIncrease("amanda", 0, 0, 0, 62, 1, 1)
        elif tmpSexType == 2:
            PregnancyCheck("amanda", "inside", 1, tmpGuyName, 0, "Соседский парень")
            SlutFriendsIncrease("amanda", 0, 0, 0, 65, 1, 1)
        elif tmpSexType == 1:
            PregnancyCheck("amanda", "mouth", 1, tmpGuyName, 0, "Соседский парень")
            SlutFriendsIncrease("amanda", 0, 0, 0, 48, 1, 1)

        Result = tmpSexType
        return tmpSexType

    def AmandaYellNotWork():
        global AmandaDynamicNextJump

        renpy.say(None, "Не стерпев что сестренка отлынивает от работы, вы подскочили к ней, взяли за плечо и начали орать:")
        if _adc_i(AmandaVar.get("warnnotwork", 0), 0):
            renpy.say(None, "\"Опять ты шляешься по улице вместо того, чтобы работать! А я ведь тебя предупреждал!\"")
            renpy.say(None, "\"Но перерыв...\" попыталась оправдаться Аманда.")
        else:
            renpy.say(None, "\"Ты что это по улице шляешься? У нас, между прочим, посетители есть.\"")
            renpy.say(None, "\"А что такого? У меня перерыв.\" ответила вам она.")
        renpy.say(None, "\"Не выдумывай! Нет у тебя никакого перерыва. А даже если бы и был, то считай что он уже закончился. Марш на работу!\"")

        AmandaVar["warnnotwork"] = 1

        if renpy.random.randint(1, 3) == 1:
            renpy.say(None, "\"Нет так нет,\" недобро ответила вам она. \"Работать я работаю, как умею.\"")
            renpy.say(None, "И, напевая себе под нос: \"Так чего же нам стараться, поработаем с прохладцей,\" она пошла обратно.")
            cooking["amanda"] = max(10, _adc_i(cooking.get("amanda", 0), 0) - 3)
            cleaning["amanda"] = max(10, _adc_i(cleaning.get("amanda", 0), 0) - 3)
            waitress["amanda"] = max(10, _adc_i(waitress.get("amanda", 0), 0) - 3)
        else:
            renpy.say(None, "Расстроившись, но не найдя что вам возразить, Аманда пошлепала обратно в трактир.")

        SlutFriendsIncrease("amanda", 6, 1, -2, 0, 0, 0)
        AmandaDynamicNextJump = "StreetTavern"
        return 0

    def CheckIfRunToLegare():
        global Result
        global SignalBlockTime
        global AmandaDynamicNextJump

        try:
            CurLocName = str(CurLoc or "")
        except NameError:
            CurLocName = ""
        try:
            cur_time = _adc_i(time, 0)
        except NameError:
            cur_time = 0

        ChanceToNotice = 5
        if CurLocName == "TavernMain":
            ChanceToNotice = 3
        elif CurLocName == "MarketPlace":
            ChanceToNotice = 7

        Result = 0
        if renpy.random.randint(1, ChanceToNotice) == 1 and _adc_i(GetSexEventFromTable("amanda", cur_time, "legarerun"), 0) > 0:
            SignalBlockTime = 1
            if CurLocName == "TavernMain":
                renpy.say(None, "Неожиданно вы заметили что Аманда, ваша младшая сестренка, потихоньку, и насколько это возможно незаметно, пробирается к выходу.")
            elif CurLocName == "MarketPlace":
                renpy.say(None, "Неожиданно вы пробирающуюся между лавками, палатками и лотками вашу сестренку Аманду. Кажется, она не очень хочет чтобы ее заметили и поэтому постоянно озирается, прячется за лотками, старается быть в тени. Хотя достигает она таким поведением результатов прямо противоположных ожидаемым - все на рынке оглядываются на нее.")
            else:
                renpy.say(None, "Неожиданно вы пробирающуюся вдоль стеночки вашу сестренку Аманду. Кажется, она не очень хочет чтобы ее заметили и поэтому постоянно озирается, передвигается от угла к углу, старается спрятаться в тени домов. Хотя достигает она таким поведением результатов прямо противоположных ожидаемым - прохожие все как один оглядываются на нее.")

            ShowImage("amanda", "", "portrait")
            choice = renpy.display_menu([
                ("Проследить за ней", "follow"),
                ("Оставить ее в покое", "leave"),
                ("Отправить ее обратно на работу", "work"),
            ])

            if choice == "follow":
                AmandaDynamicNextJump = "AfterDanceSexLegare"
            elif choice == "leave":
                renpy.say(None, "\"Спешит куда-то? Ну и пусть себе спешит, не мое дело,\" подумали вы. А Аманда скоро скрылась за углом.")
                LegareAmandaLetGoCode()
                AmandaDynamicNextJump = CurLocName
            else:
                if CurLocName == "TavernMain":
                    renpy.say(None, "Вы выскочили из трактира вслед за Амандой и увидели что она намылилась куда-то далеко.")
                AmandaYellNotWork()

            Result = 1

        return Result

    def CheckIfMeetLover():
        global Result
        global SignalBlockTime
        global AmandaDynamicNextJump

        try:
            cur_time = _adc_i(time, 0)
        except NameError:
            cur_time = 0

        Result = 0
        if renpy.random.randint(1, 5) == 1 and _adc_i(CheckIfSexEventExist("amanda", cur_time, "lovermeet"), 0) > 0:
            SignalBlockTime = 1
            renpy.say(None, "Проходя мимо трактира вы вдруг заметили на улице знакомую фигуру.")

            if renpy.random.randint(1, 2) == 1:
                choice = renpy.display_menu([
                    ("Посмотреть поближе", "look"),
                    ("Идти дальше", "go"),
                ])
                if choice == "look":
                    renpy.say(None, "Вы подошли поближе но оказалось что вы обознались.")
                else:
                    renpy.say(None, "\"Да мало ли кто это может быть? У меня есть дела поважнее!\" подумали вы и пошли дальше.")
            else:
                GetSexEventFromTable("amanda", cur_time, "lovermeet")
                choice = renpy.display_menu([
                    ("Посмотреть поближе", "look"),
                    ("Идти дальше", "go"),
                ])
                if choice == "look":
                    AmandaDynamicNextJump = "AmandaLoverSex"
                else:
                    renpy.say(None, "\"Да мало ли кто это может быть? У меня есть дела поважнее!\" подумали вы и пошли дальше.")

            Result = 1

        return Result

label AmandaDynamicCommonBlocks:
    return
