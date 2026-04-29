# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def morning_sickness_daily_event_ready(girl_name="", location_name="TavernKitchen", time_value=None):
        girl_key = str(girl_name or "").strip()
        loc_key = str(location_name or CurLoc or "").strip().lower()
        current_time = time if time_value is None else time_value
        for row in list(DailyEventsList or []):
            if str(row.get("GirlName", "") or "").strip() != girl_key:
                continue
            if str(row.get("EventType", "") or "").strip() != "MorningSickness":
                continue
            row_loc = str(row.get("Location", "") or "").strip().lower()
            if row_loc not in ("", "alllocs", loc_key):
                continue
            if not _daily_match_time(current_time, row.get("Time", 0), row.get("TimeCheckExpr", "=")):
                continue
            return True
        return False

    def tavern_breakfast_morning_sickness_girl():
        if int(time or 0) != 0:
            return ""
        for girl in ("sandra", "melissa", "amanda"):
            girl_key = str(girl or "").strip()
            if morning_sickness_daily_event_ready(girl_key, "TavernKitchen", time):
                return girl_key
        return ""

label MorningSickness(girl_name):
    hide screen main_ui
    hide screen girl_card_overlay
    hide screen player_card_overlay
    python:
        import random

        CumInsideLastDays = int(cuminside.get(girl_name, 0) or 0)

        if int(pregnancy.get(girl_name, 0) or 0) > 14:
            Zaderzhka = int(pregnancy.get(girl_name, 0) or 0) - 14
        elif int(pregnancy.get(girl_name, 0) or 0) > 0:
            Zaderzhka = 0
        else:
            Zaderzhka = 0
            if random.randint(1, 3) == 1:
                Zaderzhka = random.randint(1, 20)

        ZaletOpinion = 0
        if int(kids.get(girl_name, 0) or 0) > 0:
            if CumInsideLastDays > 2 + random.randint(1, 8):
                if Zaderzhka == 0:
                    ZaletOpinion = 1
                elif Zaderzhka >= 3 + random.randint(1, 5):
                    ZaletOpinion = 3
                else:
                    ZaletOpinion = 2
            elif CumInsideLastDays == 0:
                ZaletOpinion = 1 if Zaderzhka > 0 else 0
            else:
                if Zaderzhka == 0:
                    ZaletOpinion = 0
                elif Zaderzhka >= 10 + random.randint(1, 8):
                    ZaletOpinion = 3
                elif Zaderzhka >= 8:
                    ZaletOpinion = 2
                else:
                    ZaletOpinion = 1
        else:
            if CumInsideLastDays > 6 + random.randint(3, 12):
                if Zaderzhka < 5:
                    ZaletOpinion = 0
                elif Zaderzhka >= 10 + random.randint(2, 10):
                    ZaletOpinion = 2
                else:
                    ZaletOpinion = 1
            elif CumInsideLastDays == 0:
                ZaletOpinion = 1 if Zaderzhka >= 7 else 0
            else:
                ZaletOpinion = 1 if Zaderzhka >= 10 + random.randint(2, 10) else 0

        MSickAskedDelay = False
        MSickZaletCommentMade = False
        girl_display_name = RealName.get(girl_name, girl_name)

    "Вы мирно шли по своим делам, когда вдруг вам навстречу, зажав рот руками, пробежала бледная [girl_display_name]. Даже не заметив вас, она ломанулась куда-то дальше, скорее всего на свежий воздух."
    call girls_desc(girl_name)

    menu:
        "Проверить, что это с ней":
            "Немного обеспокоившись, вы последовали за ней. Далеко ходить не пришлось: как только [girl_display_name] выскочила за порог, ее тут же стошнило в ближайшую канаву.\n\nВытерев рот платком, она пошла обратно и тут увидела вас. \"Стефан, ты чего это за мной следишь?\" возмутилась она. \"Любопытство сгубило кошку, знаешь такое? Ты бы еще в уборной дырку бы проковырял! Не видишь что ли, подташнивает меня слегка.\""
            call SlutFriendsIncrease(girl_name, 1, 3, -1, 0, 0, 0)
        "Бросилась - значит надо ей":
            "Всего через несколько минут [girl_display_name] вернулась. Здоровый оттенок лица вернулся к ней, хотя некоторая бледность сохранилась.\n\n\"Чего-й то, Стефанчик, меня стошнило слегка,\" поделилась она с вами."

    call morning_sickness_step2(girl_name, ZaletOpinion, Zaderzhka, CumInsideLastDays, MSickAskedDelay, MSickZaletCommentMade)
    return


label morning_sickness_step2(girl_name, ZaletOpinion, Zaderzhka, CumInsideLastDays, MSickAskedDelay=False, MSickZaletCommentMade=False):
    hide screen main_ui
    hide screen girl_card_overlay
    hide screen player_card_overlay
    python:
        import random
        girl_display_name = RealName.get(girl_name, girl_name)
        ms_long_delay_limit = 20 + random.randint(1, 8)
        ms_mid_delay_limit = 10 + random.randint(1, 4)

    if ZaletOpinion == 3:
        "\"Вот же ежик гальюнный, наверное опять залетела. Меня и в прошлый раз также тошнило. Так я и знала, надо было осторожней быть, хотя чего уж там,\""
    elif ZaletOpinion == 2:
        "\"Вот ведь помет помойной крысы! Вдруг и вправду залетела? Вот это номер. Доигралась!\""
    elif ZaletOpinion == 1:
        "\"Наверное съела что-то. А вдруг это я залетела? Да нет, вряд ли, если дни правильно посчитать, то не выходит. Значит съела. Мне то вчерашнее мясо сразу не понравилось.\""
    else:
        "\"Наверное съела чего-то не то,\""

    "поделилась с вами своей догадкой [girl_display_name]."

    label morning_sickness_step2_menu:
        menu:
            "Месячные были?" if not MSickAskedDelay:
                if Zaderzhka > ms_long_delay_limit:
                    "\"Да уже больше месяца задержка. А может даже больше двух, не помню. Ты считаешь, что я забрюхатела?\""
                elif ZaletOpinion == 3:
                    "\"Да и аспид с этой задержкой. Я и так подозреваю, что залетела. Значит, ты тоже так считаешь?\""
                elif Zaderzhka > ms_mid_delay_limit:
                    "\"Да пару недель уже задержка. А может и чуть больше. Ты чего, думаешь, что я понесла?\""
                else:
                    "\"Да нет у меня никакой такой задержки. Ты что, намекаешь на то, что я забрюхатела?\""

                if ZaletOpinion <= 1:
                    "\"Да не, чушь это. Я не могу быть беременной. Этого не может быть.\""
                elif ZaletOpinion < 3:
                    "\"Да не, вряд ли, не пугай меня так, Стефан. Не может такого быть. Уверена, это просто завтрак несвежий. Или ужин.\""
                else:
                    "\"Ну твою ж кису. Точно, забрюхатела. Все сходится."
                    call morning_sickness_pregnancy_comment(girl_name, CumInsideLastDays, MSickZaletCommentMade)
                    $ MSickZaletCommentMade = True
                $ MSickAskedDelay = True
                jump morning_sickness_step2_menu

            "Я думаю ты залетела":
                if ZaletOpinion == 3:
                    "\"Точно. Залетела. Все сходится."
                    call morning_sickness_pregnancy_comment(girl_name, CumInsideLastDays, MSickZaletCommentMade)
                    $ MSickZaletCommentMade = True
                elif ZaletOpinion == 0:
                    "\"Да что ж ты за человек-то такой! Не живется тебе спокойно, только и ищешь возможность гадость какую сказать и меня расстроить. Не знаешь что сказать - помолчал бы лучше. Говорю тебе - это я просто съела чего-й то не то.\""
                    call SlutFriendsIncrease(girl_name, 5, 1, -1, 0, 0, 0)
                else:
                    "\"Да не пугай ты меня. Может обойдется все. И так тошнит, тут ты еще всякую чушь несешь.\""
                    call SlutFriendsIncrease(girl_name, 5, 3, -1, 0, 0, 0)
                call morning_sickness_end(girl_name)
                return

            "Да ладно, не волнуйся, это завтрак несвежий был":
                if ZaletOpinion == 3:
                    "\"Ну ты и дубина, Стефанчик! Обычно умный, а порой просто дуб дубом! Мне ли не знать признаки беременности? Какой, в жопу единорога, завтрак? Затяжелела я!\""
                elif ZaletOpinion == 0:
                    "\"Смешной ты. Конечно завтрак. Чтобы это еще могло быть?\""
                else:
                    "\"Ну, будем надеяться. Успокоил ты меня, а я уж испугалась было.\""
                    call SlutFriendsIncrease(girl_name, 15, 2, 1, 0, 0, 0)
                call morning_sickness_end(girl_name)
                return

    return


label morning_sickness_pregnancy_comment(girl_name, CumInsideLastDays, already_said=False):
    python:
        import random
        ms_many_sex_limit = 15 + random.randint(1, 10)
    if already_said:
        "\""
        return

    if int(CumInsideLastDays or 0) > ms_many_sex_limit:
        "Да оно и не удивительно, если столько трахаться как я."
    else:
        "Вот же свезло, несколько раз всего перепихнулась, и на тебе."

    if str(girl_name or "") in ("amanda", "melissa"):
        " Блин, а что тетушка Сандра скажет, ты ей пока не говори, хорошо?\""
    else:
        "\""
    return


label morning_sickness_end(girl_name):
    $ girl_display_name = RealName.get(girl_name, girl_name)
    "\"Ну да ладно, заболталась я с тобой, а мне бежать надо.\" И [girl_display_name] отправилась по своим делам."
    return
