init python:
    def _adsl_i(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _adsl_pick_sex_type():
        try:
            return max(0, min(5, int(AmandaLegareSetSexType())))
        except Exception:
            return 0

    def _adsl_nesluh():
        try:
            return int(AmandaNesluhCalc())
        except Exception:
            return 0

    def _adsl_react_on_you_see():
        if _adsl_i(AmandaVar.get("knowyouseesex", 0), 0) == 0:
            return

        roll = renpy.random.randint(1, 4)
        if roll == 1:
            renpy.say(None, "Вспомнив о вас, Аманда обернулась и подмигнула в сторону бочек.")
        elif roll == 2:
            renpy.say(None, "Аманда обернулась к укрытию и демонстративно провела рукой между ног.")
        elif roll == 3:
            renpy.say(None, "Сестренка явно помнит, что вы наблюдаете, и посылает вам воздушный поцелуй.")

    def _adsl_minet_finish():
        if renpy.random.randint(1, 2) == 1:
            renpy.say(None, "Легаре не предупредил Аманду и кончил ей прямо в рот.")
            if _adsl_i(sluttiness.get("amanda", 0), 0) >= 40 or _adsl_i(sexacts.get("amanda", 0), 0) > 12:
                renpy.say(None, "Аманда проглотила почти все, лишь несколько струек осталось на лице.")
            else:
                renpy.say(None, "Она растерялась, но быстро начала сглатывать семя.")
        else:
            renpy.say(None, "Легаре вытащил член и обрызгал спермой лицо вашей сестры.")

        AmandaVar["sucklegare"] = 1
        AmandaVar["alberfriends"] = _adsl_i(AmandaVar.get("alberfriends", 0), 0) + 1
        SlutFriendsIncrease("amanda", 0, 0, 0, 40, 1, 1)
        PregnancyCheck("amanda", "mouthface", 1, "legare")

    def _adsl_sex_finish(tmpLegareSexType):
        if renpy.random.randint(1, 3) <= 2:
            renpy.say(None, "Легаре засадил Аманде глубже и замер, кончая прямо в нее.")
            if _adsl_i(cuminside.get("amanda", 0), 0) < 2:
                renpy.say(None, "Аманда наивно разглядывает капли на пальцах и спрашивает про детей.")
            if _adsl_i(pregnancy.get("amanda", 0), 0) > 120:
                renpy.say(None, "Аманда шутит, что беременнее уже не станет.")
            elif _adsl_i(sluttiness.get("amanda", 0), 0) >= 48:
                renpy.say(None, "Ей откровенно нравится ощущение тепла внутри.")
            elif tmpLegareSexType == 2:
                renpy.say(None, "Аманда переживает из-за первого раза, а Легаре ее успокаивает.")
            else:
                renpy.say(None, "Аманда укоряет Легаре за риск, а он обещает в следующий раз быть осторожнее.")

            if tmpLegareSexType in (2, 3):
                ShowImage("amanda", "albersex", "cuminside" + str(renpy.random.randint(1, 2)))
            elif tmpLegareSexType == 4:
                ShowImage("amanda", "albersex", "spermpussymouth")
            else:
                ShowImage("amanda", "albersex", "spermpussy")

            PregnancyCheck("amanda", "inside", 1, "legare")
            AmandaVar["alberfriends"] = _adsl_i(AmandaVar.get("alberfriends", 0), 0) + 1
            SlutFriendsIncrease("amanda", 0, 0, 0, 50, 1, 2)
        else:
            renpy.say(None, "Легаре вытащил и кончил Аманде на ягодицы.")
            if _adsl_i(cuminside.get("amanda", 0), 0) < 2:
                renpy.say(None, "Аманда снова интересуется, от этого ли появляются дети.")
            if _adsl_i(pregnancy.get("amanda", 0), 0) > 120:
                renpy.say(None, "С беременным животом она относится к этому спокойно.")
            elif _adsl_i(sluttiness.get("amanda", 0), 0) >= 48:
                renpy.say(None, "Аманда признается, что ей было бы приятнее получить все внутрь.")
            else:
                renpy.say(None, "Она радуется, что Легаре не кончил внутрь.")

            PregnancyCheck("amanda", "outside", 1, "legare")
            AmandaVar["alberfriends"] = _adsl_i(AmandaVar.get("alberfriends", 0), 0) + 2
            SlutFriendsIncrease("amanda", 0, 0, 0, 50, 1, 2)

        AmandaVar["fucklegare"] = 1


label AfterDanceSexLegare(CurSexStep=0, tmpLegareSexType=-1, FollowMode=""):
    if CurSexStep == 0 and _adsl_i(tmpLegareSexType, -1) < 0:
        $ tmpLegareSexType = _adsl_pick_sex_type()
        if tmpLegareSexType == 4 and pregnancy.get("amanda", 0) <= 120 and renpy.random.randint(1, 4) <= 3:
            $ tmpLegareSexType = 5

    if CurSexStep == 0:
        if FollowMode == "alone":
            "Вы проследили за Амандой и увидели, как она пришла на задний двор лавки Легаре."
        else:
            "Легаре привел вашу сестру на задний двор своего магазинчика."
        "Вы устроились за бочками и начали наблюдать."
        if sluttiness.get("amanda", 0) >= 30:
            "Аманда охотно отвечает на поцелуи."
        else:
            "После короткой паузы Аманда все же отвечает на его поцелуй."
        call ShowImage("amanda", "albersex", "kiss")

    elif CurSexStep == 1:
        "Вы слышите долгий разговор про жену Легаре, слухи и то, что им здесь якобы никто не помешает."
        $ AlberVar["hearabouthiswife"] = 1

    elif CurSexStep == 2:
        if tmpLegareSexType == 0:
            if pregnancy.get("amanda", 0) < 120:
                "Легаре показывает Аманде член и подталкивает ее к ласкам."
                call ShowImage("amanda", "alberseduce", "showcock")
            else:
                "Аманда заявляет, что с животом согласна только на минет, и сразу берется за дело."
        elif tmpLegareSexType == 1:
            "Аманда просит повторить прошлый вариант и начинает делать ему минет."
            call ShowImage("amanda", "alberseduce", "suck")
            $ AmandaVar["sucklegare"] = 1
        elif tmpLegareSexType == 2:
            "Аманда нервничает из-за первого раза, но Легаре быстро переходит к ласкам."
            call ShowImage("amanda", "albersex", "grope" + str(renpy.random.randint(1, 2)))
        elif tmpLegareSexType == 3:
            "Аманда соглашается на секс, Легаре разогревает ее ласками."
            call ShowImage("amanda", "albersex", "grope" + str(renpy.random.randint(1, 2)))
        elif tmpLegareSexType == 4:
            "Аманда предлагает сначала минет, а потом секс, и снимает платье."
            call ShowImage("amanda", "albersex", "gropenaked")
        else:
            "После поцелуев они быстро переходят к откровенным ласкам."
            call ShowImage("amanda", "albersex", "grope" + str(renpy.random.randint(1, 2)))
        $ AmandaVar["knowlegaresex"] = 1
        $ AmandaVar["sawlegaresex"] = 1

    elif CurSexStep == 3:
        if tmpLegareSexType == 0:
            "Аманда встает перед Легаре на колени и старательно начинает делать минет."
            call ShowImage("amanda", "alberseduce", "suck")
            $ AmandaVar["sucklegare"] = 1
        elif tmpLegareSexType == 1:
            "Усилия Аманды дают результат, Легаре близок к разрядке."
            $ _adsl_minet_finish()
        elif tmpLegareSexType == 2:
            "Легаре раздевает вашу сестру, делает ей куни и лишает девственности."
            $ AmandaVar["fucklegare"] = 1
            $ virginity["amanda"] = 0
            $ AmandaVar["deflowerlegare"] = 1
            $ AmandaVar["knowdeflowerlegare"] = 1
            $ AmandaVar["knownotvirgin"] = 1
            call ShowImage("amanda", "albersex", "fuckbarrelstart")
        elif tmpLegareSexType == 3:
            "Аманда и Легаре раздеваются, он берет ее на бочке сзади."
            $ AmandaVar["fucklegare"] = 1
            $ AmandaVar["knownotvirgin"] = 1
            call ShowImage("amanda", "albersex", "fuckbarrelstart")
        elif tmpLegareSexType == 4:
            "Аманда быстро доводит Легаре ртом до оргазма."
            $ AmandaVar["sucklegare"] = 1
            $ _adsl_minet_finish()
        else:
            "Платье и белье слетают, Легаре сношает Аманду у стены."
            if bra.get("amanda", "") != "":
                "Лифчик тоже долго не задержался."
            $ AmandaVar["knownotvirgin"] = 1
            $ AmandaVar["fucklegare"] = 1
            call ShowImage("amanda", "albersex", "fuckwall")
        $ _adsl_react_on_you_see()

    elif CurSexStep == 4:
        if tmpLegareSexType == 0:
            "Возбужденный Легаре быстро подходит к финалу."
            $ _adsl_minet_finish()
        elif tmpLegareSexType == 1:
            "Аманда и Легаре приводят себя в порядок и собираются идти обратно к трактиру."
        elif tmpLegareSexType == 2:
            "Легаре ускоряет темп, Аманда начинает подмахивать и получает оргазм."
            call ShowImage("amanda", "albersex", "fuckbarrel" + str(renpy.random.randint(1, 3)))
        elif tmpLegareSexType == 3:
            "Легаре допрашивает Аманду о том, кто лишил ее девственности; ее ответы его только больше заводят."
            call ShowImage("amanda", "albersex", "fuckbarrel" + str(renpy.random.randint(1, 3)))
        elif tmpLegareSexType == 4:
            "После минета Аманда подставляется под новый заход, Легаре снова входит в нее."
            if pregnancy.get("amanda", 0) >= 120:
                "Беременный живот Аманда гладит рукой, пока Легаре продолжает."
            "Аманда быстро доходит до оргазма на его члене."
            $ AmandaVar["knownotvirgin"] = 1
            $ AmandaVar["fucklegare"] = 1
            call ShowImage("amanda", "albersex", "fuck" + str(renpy.random.randint(1, 2)))
        else:
            "Аманда меняет позу и снова принимает Легаре, оба уже на пике."
            call ShowImage("amanda", "albersex", "fuck" + str(renpy.random.randint(1, 2)))
        $ _adsl_react_on_you_see()

    elif CurSexStep == 5:
        if tmpLegareSexType == 0:
            "После минета Аманда спрашивает, понравилось ли Легаре, и они уходят к трактиру."
        elif tmpLegareSexType >= 2:
            $ _adsl_sex_finish(tmpLegareSexType)
            $ _adsl_react_on_you_see()
            if tmpLegareSexType == 2:
                $ AmandaVar["alberfriends"] = _adsl_i(AmandaVar.get("alberfriends", 0), 0) + 2
                call SlutFriendsIncrease("amanda", 0, 0, 0, 50, 1, 2)

    elif CurSexStep == 6:
        if tmpLegareSexType == 2:
            "Аманда делится с Легаре переживаниями о первом разе, он рассыпается в комплиментах."
        elif tmpLegareSexType == 3:
            "Они обсуждают, как сильно обоим понравилось, и одеваются."
        else:
            "Легаре и Аманда обмениваются комплиментами и собираются уходить."

    $ MaxStep = 6
    if tmpLegareSexType == 0:
        $ MaxStep = 5
    elif tmpLegareSexType == 1:
        $ MaxStep = 4

    menu:
        "Послушать о чем они болтают" if CurSexStep == 0 and AlberVar.get("hearabouthiswife", 0) == 0:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Смотреть чего будет дальше" if CurSexStep == 0 and AlberVar.get("hearabouthiswife", 0) != 0:
            call AfterDanceSexLegare(CurSexStep + 2, tmpLegareSexType, FollowMode)
            return

        "Смотреть чего будет дальше" if CurSexStep == 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Дать им кончить" if CurSexStep == 2 and tmpLegareSexType == 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Подсматривать дальше" if CurSexStep == 2 and tmpLegareSexType != 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Дать им кончить" if CurSexStep == 3 and tmpLegareSexType == 0:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "И что дальше?" if CurSexStep == 3 and tmpLegareSexType == 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Еще посмотреть" if CurSexStep == 3 and tmpLegareSexType >= 2:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "И что дальше?" if CurSexStep == 4 and tmpLegareSexType == 0:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Дать им кончить" if CurSexStep == 4 and tmpLegareSexType >= 2:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "И что дальше?" if CurSexStep == 5 and tmpLegareSexType >= 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Прервать это непотребство" if CurSexStep < MaxStep - 1 and AmandaVar.get("knowyouseesex", 0) == 0:
            $ AmandaVar["alberprohibit"] = 1
            $ AmandaVar["knowyousawlegaresex"] = 1
            $ AmandaVar["knowyouseesex"] = 1
            $ AmandaVar["alberfriends"] = _adsl_i(AmandaVar.get("alberfriends", 0), 0) - 1
            $ AmandaNesluh = _adsl_nesluh()

            if AmandaNesluh == 2:
                "Аманда злится на вас, обвиняет в ревности и отказывается прекращать."
                if AmandaVar.get("glorydeflower", 0) > 0 or AmandaVar.get("fuckyou", 0) > 0:
                    "Она напоминает, что с вами у нее уже было куда больше, чем просто подглядывания."
                $ SlutFriendsIncrease("amanda", 0, 0, 0, 60, 1, 3)

                menu:
                    "Ничего не поделаешь, смотреть дальше":
                        call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
                        return
                    "Я на это смотреть не могу и пойду отсюда":
                        if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                            $ LegareAmandaLetGoCode(1, tmpLegareSexType)
                        $ calendar_advance_slots(1)
                        if renpy.has_label("StreetTavern"):
                            jump StreetTavern
                        return

            elif AmandaNesluh == 1:
                "Ваша тирада не помогает: Аманда предлагает Легаре уйти в дом, и они скрываются."
                $ SlutFriendsIncrease("amanda", 7, 1, -1, 55, 1, 2)
                if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                    $ LegareAmandaLetGoCode(1, tmpLegareSexType)
                $ calendar_advance_slots(1)
                if renpy.has_label("StreetTavern"):
                    jump StreetTavern
                return

            else:
                "Аманда пугается вашего крика, спешно одевается и убегает в трактир."
                $ AmandaVar["alberfriends"] = _adsl_i(AmandaVar.get("alberfriends", 0), 0) - 2
                $ SlutFriendsIncrease("amanda", 3, 1, -2, 20, 1, -3)
                $ calendar_advance_slots(1)
                if renpy.has_label("StreetTavern"):
                    jump StreetTavern
                return

        "Дать знать им о том, что вы наблюдаете за ними" if CurSexStep < MaxStep - 1 and AmandaVar.get("knowyouseesex", 0) == 0 and AmandaVar.get("knowyousawlegaresex", 0):
            $ AmandaVar["knowyouseesex"] = 1
            "Вы специально шумите за бочками, давая понять, что подглядываете."

            if sluttiness.get("amanda", 0) > 45 or (sluttiness.get("amanda", 0) > 32 and renpy.random.randint(1, 3) == 1):
                "Парочку это почти не смущает, и они продолжают."
                $ SlutFriendsIncrease("amanda", 0, 0, 0, 55, 1, 2)
                menu:
                    "Ничего не поделаешь, смотреть дальше":
                        call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
                        return
                    "Плюнуть и идти обратно в трактир":
                        if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                            $ LegareAmandaLetGoCode(1, tmpLegareSexType)
                        $ calendar_advance_slots(1)
                        if renpy.has_label("StreetTavern"):
                            jump StreetTavern
                        return
            else:
                "Аманда смущается и уводит Легаре в дом."
                if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                    $ LegareAmandaLetGoCode(1, tmpLegareSexType)
                $ calendar_advance_slots(1)
                if renpy.has_label("StreetTavern"):
                    jump StreetTavern
                return

        "Я на это смотреть не могу и пойду отсюда" if CurSexStep < MaxStep - 1 and AmandaVar.get("knowyouseesex", 0) == 1:
            if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                $ LegareAmandaLetGoCode(1, tmpLegareSexType)
            $ calendar_advance_slots(1)
            if renpy.has_label("StreetTavern"):
                jump StreetTavern
            return

        "Ухожу, даже и не собираюсь на это смотреть" if CurSexStep < MaxStep and AmandaVar.get("knowyouseesex", 0) == 0:
            if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                $ LegareAmandaLetGoCode(1, tmpLegareSexType)
            $ calendar_advance_slots(1)
            if renpy.has_label("StreetTavern"):
                jump StreetTavern
            return

        "Пойду-ка и я" if (CurSexStep == 4 and tmpLegareSexType == 1) or (CurSexStep == 5 and tmpLegareSexType == 0) or (CurSexStep >= 6):
            if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                $ LegareAmandaLetGoCode(1, tmpLegareSexType)
            $ calendar_advance_slots(1)
            if renpy.has_label("StreetTavern"):
                jump StreetTavern
            return

    return
