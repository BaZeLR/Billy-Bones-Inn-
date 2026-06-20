# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
            p1 = '"Вот Стефанчик, и ты можешь быть разумным. Если захочешь," '
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
        rel = _adc_i(Amanda.rel, 0)
        corr = _adc_i(Amanda.corruption, 0)

        if Amanda.var_int("prohibitliza", 0) or (Amanda.var_int("alberprohibit", 0) and Amanda.var_int("alberfriends", 0) >= 5) or Amanda.var_int("gloryscold", 0):
            if Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0):
                if (rel >= 12 and corr >= 40) or corr >= 50:
                    tmpGropeReact = 4
                    if corr >= 55 and renpy.random.randint(1, 3) == 1:
                        tmpGropeReact = 3
                elif corr <= 25 and rel <= 10:
                    tmpGropeReact = 2
                elif corr <= 30 and rel <= 5:
                    tmpGropeReact = 2
                else:
                    tmpGropeReact = 3
            else:
                if (rel >= 14 and corr >= 45) or corr >= 55:
                    tmpGropeReact = 4
                    if corr >= 55 and renpy.random.randint(1, 3) == 1:
                        tmpGropeReact = 3
                elif corr <= 30 and rel <= 12:
                    tmpGropeReact = 2
                elif corr <= 35 and rel <= 8:
                    tmpGropeReact = 2
                else:
                    tmpGropeReact = 3
        else:
            if Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0):
                if rel >= 2 and corr >= 45:
                    tmpGropeReact = 4
                elif rel >= 5 and corr >= 35:
                    tmpGropeReact = 4
                elif rel >= 10 and corr >= 25:
                    tmpGropeReact = 4
                elif rel >= 15 and corr >= 21:
                    tmpGropeReact = 4
                elif rel >= 2 and corr >= 35:
                    tmpGropeReact = 1
                elif rel >= 5 and corr >= 25:
                    tmpGropeReact = 1
                elif rel >= 10 and corr >= 21:
                    tmpGropeReact = 1
            else:
                if rel >= 5 and corr >= 45:
                    tmpGropeReact = 4
                elif rel >= 10 and corr >= 35:
                    tmpGropeReact = 4
                elif rel >= 15 and corr >= 25:
                    tmpGropeReact = 4
                elif rel >= 5 and corr >= 35:
                    tmpGropeReact = 1
                elif rel >= 10 and corr >= 25:
                    tmpGropeReact = 1

        Result = tmpGropeReact
        return tmpGropeReact

    def AmandaLegareSetSexType():
        global Result

        if Amanda.var_int("sucklegare", 0) == 0:
            tmpLegareSexType = 0
        else:
            if Amanda.var_int("fucklegare", 0) == 0:
                if Amanda.stats.get("virginity", True):
                    if Amanda.var_int("alberfriends", 0) >= 15 and Amanda.corruption >= 35 and _adc_i(Amanda.stats.get("sexacts", 0), 0) >= 5:
                        tmpLegareSexType = 2
                    else:
                        tmpLegareSexType = 1
                else:
                    if Amanda.var_int("alberfriends", 0) >= 12 and Amanda.corruption >= 32 and _adc_i(Amanda.stats.get("sexacts", 0), 0) >= 4:
                        tmpLegareSexType = 3
                    else:
                        tmpLegareSexType = 1
            else:
                if (Amanda.var_int("alberfriends", 0) >= 10 and Amanda.corruption >= 30) or (Amanda.var_int("alberfriends", 0) >= 5 and Amanda.corruption >= 40):
                    tmpLegareSexType = 4
                else:
                    tmpLegareSexType = 1

        if _adc_i(Amanda.stats.get("pregnancy", 0), 0) >= 120 and tmpLegareSexType == 3:
            tmpLegareSexType = 4

        Result = tmpLegareSexType
        return tmpLegareSexType

    def AmandaNesluhCalc():
        global Result

        AmandaNesluh = 0
        AmandaNesluhBonus = 0

        if Amanda.var_int("glorydeflower", 0) > 0 or Amanda.var_int("fuckyou", 0) > 0:
            AmandaNesluhBonus += 6
        if Amanda.var_int("gloryscold", 0) > 0:
            AmandaNesluhBonus -= 3
        if Amanda.var_int("glorysuck", 0) > 0 or Amanda.var_int("suckyou", 0) > 0:
            AmandaNesluhBonus += 3
        if Amanda.var_int("glorywalkout", 0) > 0:
            AmandaNesluhBonus += 2
        if Amanda.var_int("alberfriends", 0) >= 7:
            AmandaNesluhBonus += 1
        if Amanda.var_int("alberfriends", 0) >= 9:
            AmandaNesluhBonus += 1
        if Amanda.var_int("alberfriends", 0) >= 12:
            AmandaNesluhBonus += 2
        if Amanda.corruption >= 23:
            AmandaNesluhBonus += 1
        if Amanda.corruption >= 30:
            AmandaNesluhBonus += 2
        if Amanda.corruption >= 40:
            AmandaNesluhBonus += 4
        if Amanda.corruption >= 50:
            AmandaNesluhBonus += 3
        if Amanda.var_int("sucklegare", 0) > 0:
            AmandaNesluhBonus += 2
        if Amanda.var_int("fucklegare", 0) > 0:
            AmandaNesluhBonus += 3
        if Amanda.var_int("deflowerlegare", 0) > 0:
            AmandaNesluhBonus += 3

        AmandaNesluhBonus = min(14, max(1, AmandaNesluhBonus))
        if renpy.random.randint(1, 15) <= AmandaNesluhBonus:
            AmandaNesluh = 1
        if (Amanda.var_int("glorydeflower", 0) or Amanda.var_int("fuckyou", 0)) and AmandaNesluh == 1 and renpy.random.randint(1, 4) <= 3:
            AmandaNesluh = 2
        elif (Amanda.var_int("glorysuck", 0) or Amanda.var_int("suckyou", 0)) and AmandaNesluh == 1 and renpy.random.randint(1, 4) <= 1:
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
        if Amanda.corruption >= 57:
            tmpSexType = 2
        elif _adc_i(Amanda.stats.get("pregnancy", 0), 0) > 120:
            if Amanda.corruption >= 42:
                tmpSexType = 2
            elif Amanda.corruption >= 40:
                tmpSexType = 1
        else:
            if Amanda.corruption >= 45:
                if renpy.random.randint(1, 3) == 1:
                    tmpSexType = 1
                elif renpy.random.randint(1, 9) <= 4:
                    tmpSexType = 2
            elif Amanda.corruption >= 40:
                tmpSexType = 1

        if _adc_i(forced_type, 0) > 0:
            tmpSexType = _adc_i(forced_type, 0)
        if tmpSexType == 2 and renpy.random.randint(1, 2) == 1:
            tmpSexType = 3

        if tmpSexType == 3:
            Amanda.pregnancy_check("outside", 1, tmpGuyName, 0, "Соседский парень")
            Amanda.change_social(corruption_delta=1)
        elif tmpSexType == 2:
            Amanda.pregnancy_check("inside", 1, tmpGuyName, 0, "Соседский парень")
            Amanda.change_social(corruption_delta=1)
        elif tmpSexType == 1:
            Amanda.pregnancy_check("mouth", 1, tmpGuyName, 0, "Соседский парень")
            Amanda.change_social(corruption_delta=1)

        Result = tmpSexType
        return tmpSexType

    def AmandaYellNotWork():
        global AmandaDynamicNextJump

        renpy.say(None, "Не стерпев что Аманда отлынивает от работы, вы подскочили к ней, взяли за плечо и начали орать:")
        if Amanda.var_int("warnnotwork", 0):
            renpy.say(None, "\"Опять ты шляешься по улице вместо того, чтобы работать! А я ведь тебя предупреждал!\"")
            renpy.say(None, "\"Но перерыв...\" попыталась оправдаться Аманда.")
        else:
            renpy.say(None, "\"Ты что это по улице шляешься? У нас, между прочим, посетители есть.\"")
            renpy.say(None, "\"А что такого? У меня перерыв.\" ответила вам она.")
        renpy.say(None, "\"Не выдумывай! Нет у тебя никакого перерыва. А даже если бы и был, то считай что он уже закончился. Марш на работу!\"")

        Amanda.set_var_int("warnnotwork", 1)

        if renpy.random.randint(1, 3) == 1:
            renpy.say(None, "\"Нет так нет,\" недобро ответила вам она. \"Работать я работаю, как умею.\"")
            renpy.say(None, "И, напевая себе под нос: \"Так чего же нам стараться, поработаем с прохладцей,\" она пошла обратно.")
            Amanda.skills["cooking"] = max(10, _adc_i(Amanda.skills.get("cooking", 0), 0) - 3)
            Amanda.skills["cleaning"] = max(10, _adc_i(Amanda.skills.get("cleaning", 0), 0) - 3)
            Amanda.skills["waitress"] = max(10, _adc_i(Amanda.skills.get("waitress", 0), 0) - 3)
        else:
            renpy.say(None, "Расстроившись, но не найдя что вам возразить, Аманда пошлепала обратно в трактир.")

        Amanda.change_social(friend_delta=(1 if Amanda.rel >= 6 else -2))
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
                renpy.say(None, "Неожиданно вы заметили что Аманда, одна из девушек трактира, потихоньку, и насколько это возможно незаметно, пробирается к выходу.")
            elif CurLocName == "MarketPlace":
                renpy.say(None, "Неожиданно вы замечаете пробирающуюся между лавками, палатками и лотками Аманду. Кажется, она не очень хочет чтобы ее заметили и поэтому постоянно озирается, прячется за лотками, старается быть в тени. Хотя достигает она таким поведением результатов прямо противоположных ожидаемым - все на рынке оглядываются на нее.")
            else:
                renpy.say(None, "Неожиданно вы замечаете пробирающуюся вдоль стеночки Аманду. Кажется, она не очень хочет чтобы ее заметили и поэтому постоянно озирается, передвигается от угла к углу, старается спрятаться в тени домов. Хотя достигает она таким поведением результатов прямо противоположных ожидаемым - прохожие все как один оглядываются на нее.")

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
                apply_legare_amanda_let_go_code()
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
