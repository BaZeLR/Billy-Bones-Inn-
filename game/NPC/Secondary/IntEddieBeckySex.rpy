# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntEddieBeckySex(GirlNameIBS="becky"):
    $ renpy.dynamic("_eddie_fuck_picture")
    $ renpy.dynamic("_cametoday_eddie", "_cancumdaily_eddie")
    python:
        Becky.ensure_sex_state()
        Eddie.stats.setdefault("group_sex", 0)

        def _iebs_set_arousal(who, value):
            value = min(100, max(0, int(value or 0)))
            if str(who or "").lower() == "you":
                player.intimacy.set_arousal(value)
                return
            info = people.get_info(who)
            if info is not None:
                info.set_arousal(value)

        def _iebs_arousal(who):
            if str(who or "").lower() == "you":
                return int(player.intimacy.arousal_value() or 0)
            info = people.get_info(who)
            return int(info.arousal_value() or 0) if info is not None else 0

        def _iebs_inc_arousal(who, amount):
            _iebs_set_arousal(who, _iebs_arousal(who) + int(amount or 0))

        def _iebs_set_eddie_pos(pos):
            Becky.set_cock_position({1: "pussy", 2: "mouth", 3: "tits"}.get(pos, "none"), "eddie")

    label int_eddie_becky_sex_menu:
        while True:
            python:
                _cametoday_eddie = int(Eddie.sex_stat("came_today", 0) or 0)
                _cancumdaily_eddie = max(1, int(Eddie.sex_stat("can_cum_daily", 1) or 1))

            menu:
                "Целовать хозяйку" if not Becky.sex_busy() and Becky.cock_in("mouth", "You") == 0 and Becky.cock_in("tits", "You") == 0:
                    if Becky.cock_in("pussy", "You") > 0:
                        "Эдди, ничуть не смущаясь тем, что вы продолжаете сношать его хозяйку, целует ее взасос. Та отвечает управляющему взаимностью, не прекращая при этом и вам подмахивать."
                    else:
                        "Эдди и Бекки целуются страстно и взасос. Шаловливые ручки Эдди лапают грудь хозяйки лавки."
                    call ShowImage("becky", "sexeddie", "kiss")
                    python:
                        _iebs_inc_arousal(GirlNameIBS, 10)
                        _iebs_inc_arousal("eddie", 10)
                        _iebs_set_eddie_pos(2)
                    call CockPosition(GirlNameIBS, 2, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Лапать хозяйку" if not Becky.sex_busy():
                    if Becky.cock_in("mouth", "You") == 1:
                        "Глядя на то, как Бекки отсасывает вам, Эдди начал лапать хозяйку."
                    elif Becky.cock_in("pussy", "You") == 1:
                        "Глядя на то, как вы сношаете Бекки, к ней подкатился и ее управляющий."
                    elif Becky.cock_in("tits", "You") == 1:
                        "Увидев, как Бекки трахает ваш член грудями, Эдди тоже возбудился."
                    else:
                        "Эдди начал жадно лапать хозяйку, распаляя ее все сильнее."

                    if Becky.cock_in("tits", "You") == 0:
                        if not Becky.tits_visible():
                            "Эдди ласкает грудь Бекки через одежду."
                        else:
                            "Эдди облизывает массивные груди хозяйки и слегка покусывает соски."
                    if Becky.cock_in("pussy", "You") == 0:
                        if Becky.pussy_visible():
                            "Потом он потянулся к истекающей соками щели Бекки и начал ее нежно ласкать."
                        else:
                            "Потом он полез руками под одежду к промежности хозяйки."

                    call ShowImage("becky", "sexeddie", "grope")
                    python:
                        _iebs_inc_arousal(GirlNameIBS, 15)
                        _iebs_set_eddie_pos(0)
                    call CockPosition(GirlNameIBS, 0, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Полизать Бекки" if Becky.pussy_visible() and not Becky.sex_busy() and Becky.cock_in("pussy", "You") == 0:
                    if Becky.cock_in("mouth", "You") == 1:
                        "Вы продолжаете сношать Бекки в рот, а внимание Эдди привлекла ее мокрая киска."
                        python:
                            _iebs_inc_arousal("You", 10)
                    if Becky.cock_in("tits", "You") == 1:
                        "Похотливая вдова продолжает трахать вас грудями, а ее управляющий опускается между ее ног."
                        python:
                            _iebs_inc_arousal("You", 20)
                    if Becky.cum_state("cum_inside_you") > 0 or Becky.cum_state("cum_inside_others") > 0:
                        "Сочащаяся из влагалища сперма не отпугнула Эдди, он припал к щели Бекки и вылизал ее."
                        $ Becky.clear_cum("cum_inside_you", "cum_inside_others")
                    else:
                        "Эдди развел ноги хозяйки в стороны и начал лизать ей клитор."
                    python:
                        _iebs_inc_arousal(GirlNameIBS, 26)
                        _iebs_set_eddie_pos(0)
                    call CockPosition(GirlNameIBS, 0, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Дать Бекки отсосать" if _cametoday_eddie < _cancumdaily_eddie and not Becky.sex_busy() and Becky.cock_in("mouth", "You") == 0 and Becky.cock_in("tits", "You") == 0:
                    if Becky.cock_in("pussy", "You") > 0:
                        if Becky.cock_in("mouth", "eddie") == 0:
                            "Эдди, решив присоединиться, поднес член к губам Бекки, и та с готовностью взяла его в рот."
                        else:
                            "Вы продолжаете трахать Бекки на пару с Эдди: вы в киску, он в ротик."
                        python:
                            _iebs_inc_arousal("You", 15)
                            _iebs_inc_arousal(GirlNameIBS, 20)
                    else:
                        if Becky.cock_in("mouth", "eddie") == 0:
                            "Эдди подошел к Бекки и показал на свой член. Та наклонилась и начала его сосать."
                        else:
                            "Разгульная вдова продолжает умело отсасывать Эдди."

                    if _iebs_arousal("eddie") < 20:
                        "Она лишь облизывает его вялый член."
                    elif _iebs_arousal("eddie") < 40:
                        "Она облизывает головку напрягшегося члена Эдди."
                    elif _iebs_arousal("eddie") < 60:
                        "Она умело отсасывает Эдди."
                    else:
                        "Она заглатывает член Эдди по самые яйца."

                    if Becky.cock_in("pussy", "You") > 0:
                        call ShowImage("becky", "sexeddie", "doubleyou")
                    else:
                        call ShowImage("becky", "sexeddie", "minet")
                    python:
                        _iebs_inc_arousal("eddie", 20)
                        _iebs_set_eddie_pos(2)
                    call CockPosition(GirlNameIBS, 2, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Трахнуть сиси Бекки" if _cametoday_eddie < _cancumdaily_eddie and not Becky.sex_busy() and _iebs_arousal("eddie") >= 20 and Becky.tits_visible() and Becky.pregnancy_days() < 130 and Becky.cock_in("tits", "You") == 0 and Becky.cock_in("mouth", "You") == 0:
                    if Becky.cock_in("pussy", "You") == 0:
                        if Becky.cock_in("tits", "eddie"):
                            "Эдди лежит и балдеет, пока Бекки трахает его член своими грудями."
                        else:
                            "Эдди лег на кровать, а хозяйка лавки опустилась над ним и зажала его член между грудей."
                    else:
                        if Becky.cock_in("tits", "eddie"):
                            "Пока Эдди трахает Бекки грудями, ваши толчки задают темп."
                        else:
                            "Эдди подлез под вас и вложил свой член между сисек Бекки."
                        python:
                            _iebs_inc_arousal("You", 15)
                            _iebs_inc_arousal(GirlNameIBS, 20)
                    python:
                        _iebs_inc_arousal("eddie", 15)
                        _iebs_set_eddie_pos(3)
                    call CockPosition(GirlNameIBS, 3, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Трахать" if _cametoday_eddie < _cancumdaily_eddie and not Becky.sex_busy() and _iebs_arousal("eddie") >= 20 and _iebs_arousal(GirlNameIBS) >= 20 and Becky.pussy_visible() and Becky.cock_in("pussy", "You") == 0:
                    if Becky.cock_in("mouth", "You") == 1:
                        if Becky.cock_in("pussy", "eddie") == 0:
                            "Эдди посмотрел как Ребекка делает вам минет, подошел к хозяйке сзади и приставил свой член к ее щели. Бекки, почуствовав член управляющего, приглашающе вильнула попой и Эдди одним движением вошел в нее."
                        else:
                            "Эдди трахает свою хозяйку сзади, загоняя свой член в нее по самые яйца а она, тем временем, продолжает вам отсасывать, практически не сбиваясь с темпа. Ну что за мастерица!"
                        call ShowImage("becky", "sexeddie", "doubleeddie")
                        python:
                            _iebs_inc_arousal("You", 15)
                    elif Becky.cock_in("tits", "You") == 1:
                        if Becky.cock_in("pussy", "eddie") == 0:
                            "Эдди посмотрел как Ребекка трахает ваш член своими грудями, на ее заманчиво оттопыренную задницу с обнаженной киской, и принял решение. Сорванец подошел к хозяйке сзади и приставил свой член к ее щели. Бекки, почуствовав член управляющего, приглашающе вильнула попой и Эдди одним движением вошел в нее."
                        else:
                            "Бекки трахает ваш член своими грудями а Эдди, в свою очередь, сношает ее сзади, задавая темп."
                        python:
                            _iebs_inc_arousal("You", 15)
                    else:
                        if Becky.cock_in("pussy", "eddie") == 0:
                            "Ребекка провела рукой по поднявшемуся члену Эдди: \"Давай, мой управляющий. Чего же ты ждешь, разве не видишь что я уже вся горю?\" - бесстыдно сказала она становясь перед ним раком. Тот не заставил себя долго упрашивать и начал сношать хозяйку сзади."
                            $ _eddie_fuck_picture = "fuckstart" + str(procedural_randint(1, 3, key="procedural:NPC/Secondary/IntEddieBeckySex.rpy:procedural_randint:207:1"))
                            call ShowImage("becky", "sexeddie", _eddie_fuck_picture)
                        else:
                            "Эдди продолжает трахать Ребекку, ее большие сиськи болтаются при каждом его толчке. Вдова громко стонет от наслаждения при каждом движении члена управляющего в ее киске."
                            $ _eddie_fuck_picture = "fuck" + str(procedural_randint(1, 4, key="procedural:NPC/Secondary/IntEddieBeckySex.rpy:procedural_randint:211:2"))
                            call ShowImage("becky", "sexeddie", _eddie_fuck_picture)

                    if Becky.pregnancy_days() > 130:
                        "Ребенок в животе Бекки шевелится, реагируя на движения члена Эдди."

                    python:
                        _iebs_inc_arousal(GirlNameIBS, 26)
                        _iebs_inc_arousal("eddie", 20)
                        _iebs_set_eddie_pos(1)
                    call CockPosition(GirlNameIBS, 1, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Кончить в рот" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and (Becky.cock_in("mouth", "eddie") or Becky.cock_in("tits", "eddie")) and Becky.cock_in("mouth", "You") == 0 and Becky.cock_in("tits", "You") == 0:
                    "Эдди прижал голову Бекки к себе и начал заполнять ее рот своим семенем."
                    "Когда он ее отпустил, разбитная вдова начисто облизала член Эдди."
                    if Becky.cock_in("pussy", "You") == 1:
                        "При этом сладострастная торговка не забывала еще и вам подмахивать, приближая и ваш собственный оргазм."
                        python:
                            _iebs_inc_arousal("You", 10)
                    $ _iebs_set_arousal("eddie", 0)
                    call PregnancyCheck(GirlNameIBS, "mouth", 1, "eddie")
                    python:
                        _iebs_set_eddie_pos(0)
                    call CockPosition(GirlNameIBS, 0, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Кончить на лицо" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and Becky.cock_in("mouth", "You") == 0 and Becky.cock_in("tits", "You") == 0:
                    "Почувствовав что кончает, Эдди вытащил член из Бекки и залил ее смазливое личико своим семенем. Бекки вытерла сперму с зажмуренных глаз и ошарашенно заморгала: сперма ее управляющего покрывала ее личико и капала на ее монументальный бюст. Отдельные белые капли застряли даже в ее рыжей шевелюре."
                    $ _iebs_set_arousal("eddie", 0)
                    call PregnancyCheck(GirlNameIBS, "face", 1, "eddie")
                    python:
                        _iebs_set_eddie_pos(0)
                    call CockPosition(GirlNameIBS, 0, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Кончить на груди" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and Becky.tits_visible() and Becky.cock_in("mouth", "You") == 0 and Becky.cock_in("tits", "You") == 0:
                    "Эдди направил свой член на сиси Бекки и метко выстрелил несколькими струями спермы на обе ее груди, попав точно в ареолы. \"Такому меткому стрелку прямая дорога в королевскую гвардию,\" невпопад подумали вы."
                    $ _iebs_set_arousal("eddie", 0)
                    call PregnancyCheck(GirlNameIBS, "tits", 1, "eddie")
                    python:
                        _iebs_set_eddie_pos(0)
                    call CockPosition(GirlNameIBS, 0, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Кончить в Бекки" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and Becky.cock_in("pussy", "eddie"):
                    if Becky.pregnancy_days() < 120 and Becky.corruption < 65:
                        if Becky.cock_in("mouth", "You") == 1:
                            "Эдди увеличил темп, и Бекки, выплюнув ваш член, с ужасом спросила, не спускает ли он в нее."
                        else:
                            "Эдди увеличил темп, и Бекки с ужасом спросила, не спускает ли он в нее."
                        "Оттолкнуть Эдди она успела, но было поздно: семя уже вытекало из ее киски."
                    else:
                        "Эдди выполнил просьбу Бекки и залил ее щелку молодым семенем."
                        if Becky.cock_in("mouth", "You") == 1:
                            "Бекки промычала что-то неразборчивое, так как вы продолжали трахать ее в рот."
                            python:
                                _iebs_inc_arousal("You", 10)
                        if Becky.pregnancy_days() >= 120:
                            "\"Ну мальчики, нагуляла я с вами животик, так вы и дальше пользуетесь моей слабостью,\" — сладострастно улыбнулась Бекки."

                    $ _iebs_set_arousal("eddie", 0)
                    python:
                        _iebs_inc_arousal(GirlNameIBS, 5)
                        _iebs_set_eddie_pos(0)
                    call PregnancyCheck(GirlNameIBS, "inside", 1, "eddie")
                    call CockPosition(GirlNameIBS, 0, "eddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Закончить":
                    $ Becky.set_cock_position("none", "eddie")
                    return

        return
