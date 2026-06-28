# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntEddieBeckySex(GirlNameIBS="becky"):
    python:
        topdress.setdefault(GirlNameIBS, "")
        bottomdress.setdefault(GirlNameIBS, "")
        bra.setdefault(GirlNameIBS, "")
        panties.setdefault(GirlNameIBS, "")
        topraised.setdefault(GirlNameIBS, 0)
        bottomraised.setdefault(GirlNameIBS, 0)
        TitsVisible.setdefault(GirlNameIBS, 0)
        PussyVisible.setdefault(GirlNameIBS, 0)
        CockInMouth.setdefault(GirlNameIBS, 0)
        CockInPussy.setdefault(GirlNameIBS, 0)
        CockInTits.setdefault(GirlNameIBS, 0)
        EddieCockInPussy.setdefault(GirlNameIBS, 0)
        EddieCockInMouth.setdefault(GirlNameIBS, 0)
        EddieCockInTits.setdefault(GirlNameIBS, 0)
        CumInsideYou.setdefault(GirlNameIBS, 0)
        CumInsideOthers.setdefault(GirlNameIBS, 0)
        GrupenSex.setdefault("eddie", 0)
        pregnancy.setdefault(GirlNameIBS, 0)
        SomebodyCums = int(SomebodyCums or 0)
        if not isinstance(cametoday_npc, dict):
            cametoday_npc = {}

        def _iebs_set_arousal(who, value):
            value = min(100, max(0, int(value or 0)))
            if str(who or "").lower() == "you":
                player_state(False).intimacy.set_arousal(value, "You")
                player_state(False).intimacy.apply_to_store()
                return
            info = getPersonInfo(who)
            if info is not None and hasattr(info, "set_arousal"):
                info.set_arousal(value)

        def _iebs_arousal(who):
            if str(who or "").lower() == "you":
                return int(player_state(False).intimacy.arousal_value("You") or 0)
            info = getPersonInfo(who)
            return int(info.arousal_value() or 0) if info is not None and hasattr(info, "arousal_value") else 0

        def _iebs_inc_arousal(who, amount):
            _iebs_set_arousal(who, _iebs_arousal(who) + int(amount or 0))

        def _iebs_set_eddie_pos(pos):
            EddieCockInMouth[GirlNameIBS] = 1 if pos == 2 else 0
            EddieCockInPussy[GirlNameIBS] = 1 if pos == 1 else 0
            EddieCockInTits[GirlNameIBS] = 1 if pos == 3 else 0

    label int_eddie_becky_sex_menu:
        python:
            if isinstance(cametoday_npc, dict):
                _cametoday_eddie = cametoday_npc.get("eddie", cametoday_npc.get("Eddie", 0))
            else:
                _cametoday_eddie = 0

            if isinstance(cancumdaily, dict):
                _cancumdaily_eddie = cancumdaily.get("eddie", cancumdaily.get("Eddie", 1))
            elif isinstance(cancumdaily, (int, float)):
                _cancumdaily_eddie = int(cancumdaily)
            else:
                _cancumdaily_eddie = 1

        menu:
            "Целовать хозяйку" if SomebodyCums == 0 and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                if CockInPussy.get(GirlNameIBS, 0) > 0:
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
                jump int_eddie_becky_sex_menu

            "Лапать хозяйку" if SomebodyCums == 0:
                if CockInMouth.get(GirlNameIBS, 0) == 1:
                    "Глядя на то, как Бекки отсасывает вам, Эдди начал лапать хозяйку."
                elif CockInPussy.get(GirlNameIBS, 0) == 1:
                    "Глядя на то, как вы сношаете Бекки, к ней подкатился и ее управляющий."
                elif CockInTits.get(GirlNameIBS, 0) == 1:
                    "Увидев, как Бекки трахает ваш член грудями, Эдди тоже возбудился."
                else:
                    "Эдди начал жадно лапать хозяйку, распаляя ее все сильнее."

                if CockInTits.get(GirlNameIBS, 0) == 0:
                    if TitsVisible.get(GirlNameIBS, 0) == 0:
                        "Эдди ласкает грудь Бекки через одежду."
                    else:
                        "Эдди облизывает массивные груди хозяйки и слегка покусывает соски."
                if CockInPussy.get(GirlNameIBS, 0) == 0:
                    if PussyVisible.get(GirlNameIBS, 0) == 1:
                        "Потом он потянулся к истекающей соками щели Бекки и начал ее нежно ласкать."
                    else:
                        "Потом он полез руками под одежду к промежности хозяйки."

                call ShowImage("becky", "sexeddie", "grope")
                python:
                    _iebs_inc_arousal(GirlNameIBS, 15)
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Полизать Бекки" if PussyVisible.get(GirlNameIBS, 0) and SomebodyCums == 0 and CockInPussy.get(GirlNameIBS, 0) == 0:
                if CockInMouth.get(GirlNameIBS, 0) == 1:
                    "Вы продолжаете сношать Бекки в рот, а внимание Эдди привлекла ее мокрая киска."
                    python:
                        _iebs_inc_arousal("You", 10)
                if CockInTits.get(GirlNameIBS, 0) == 1:
                    "Похотливая вдова продолжает трахать вас грудями, а ее управляющий опускается между ее ног."
                    python:
                        _iebs_inc_arousal("You", 20)
                if CumInsideYou.get(GirlNameIBS, 0) > 0 or CumInsideOthers.get(GirlNameIBS, 0) > 0:
                    "Сочащаяся из влагалища сперма не отпугнула Эдди, он припал к щели Бекки и вылизал ее."
                    $ CumInsideYou[GirlNameIBS] = 0
                    $ CumInsideOthers[GirlNameIBS] = 0
                else:
                    "Эдди развел ноги хозяйки в стороны и начал лизать ей клитор."
                python:
                    _iebs_inc_arousal(GirlNameIBS, 26)
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Дать Бекки отсосать" if _cametoday_eddie < _cancumdaily_eddie and SomebodyCums == 0 and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                if CockInPussy.get(GirlNameIBS, 0) > 0:
                    if EddieCockInMouth.get(GirlNameIBS, 0) == 0:
                        "Эдди, решив присоединиться, поднес член к губам Бекки, и та с готовностью взяла его в рот."
                    else:
                        "Вы продолжаете трахать Бекки на пару с Эдди: вы в киску, он в ротик."
                    python:
                        _iebs_inc_arousal("You", 15)
                        _iebs_inc_arousal(GirlNameIBS, 20)
                else:
                    if EddieCockInMouth.get(GirlNameIBS, 0) == 0:
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

                if CockInPussy.get(GirlNameIBS, 0) > 0:
                    call ShowImage("becky", "sexeddie", "doubleyou")
                else:
                    call ShowImage("becky", "sexeddie", "minet")
                python:
                    _iebs_inc_arousal("eddie", 20)
                    _iebs_set_eddie_pos(2)
                call CockPosition(GirlNameIBS, 2, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Трахнуть сиси Бекки" if _cametoday_eddie < _cancumdaily_eddie and SomebodyCums == 0 and _iebs_arousal("eddie") >= 20 and TitsVisible.get(GirlNameIBS, 0) and pregnancy.get(GirlNameIBS, 0) < 130 and CockInTits.get(GirlNameIBS, 0) == 0 and CockInMouth.get(GirlNameIBS, 0) == 0:
                if CockInPussy.get(GirlNameIBS, 0) == 0:
                    if EddieCockInTits.get(GirlNameIBS, 0):
                        "Эдди лежит и балдеет, пока Бекки трахает его член своими грудями."
                    else:
                        "Эдди лег на кровать, а хозяйка лавки опустилась над ним и зажала его член между грудей."
                else:
                    if EddieCockInTits.get(GirlNameIBS, 0):
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
                jump int_eddie_becky_sex_menu

            "Трахать" if _cametoday_eddie < _cancumdaily_eddie and SomebodyCums == 0 and _iebs_arousal("eddie") >= 20 and _iebs_arousal(GirlNameIBS) >= 20 and PussyVisible.get(GirlNameIBS, 0) and CockInPussy.get(GirlNameIBS, 0) == 0:
                if CockInMouth.get(GirlNameIBS, 0) == 1:
                    if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                        "Эдди посмотрел как Ребекка делает вам минет, подошел к хозяйке сзади и приставил свой член к ее щели. Бекки, почуствовав член управляющего, приглашающе вильнула попой и Эдди одним движением вошел в нее."
                    else:
                        "Эдди трахает свою хозяйку сзади, загоняя свой член в нее по самые яйца а она, тем временем, продолжает вам отсасывать, практически не сбиваясь с темпа. Ну что за мастерица!"
                    call ShowImage("becky", "sexeddie", "doubleeddie")
                    python:
                        _iebs_inc_arousal("You", 15)
                elif CockInTits.get(GirlNameIBS, 0) == 1:
                    if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                        "Эдди посмотрел как Ребекка трахает ваш член своими грудями, на ее заманчиво оттопыренную задницу с обнаженной киской, и принял решение. Сорванец подошел к хозяйке сзади и приставил свой член к ее щели. Бекки, почуствовав член управляющего, приглашающе вильнула попой и Эдди одним движением вошел в нее."
                    else:
                        "Бекки трахает ваш член своими грудями а Эдди, в свою очередь, сношает ее сзади, задавая темп."
                    python:
                        _iebs_inc_arousal("You", 15)
                else:
                    if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                        "Ребекка провела рукой по поднявшемуся члену Эдди: \"Давай, мой управляющий. Чего же ты ждешь, разве не видишь что я уже вся горю?\" - бесстыдно сказала она становясь перед ним раком. Тот не заставил себя долго упрашивать и начал сношать хозяйку сзади."
                        $ _eddie_fuck_picture = "fuckstart" + str(procedural_randint(1, 3, key="procedural:NPC/Secondary/IntEddieBeckySex.rpy:procedural_randint:207:1"))
                        call ShowImage("becky", "sexeddie", _eddie_fuck_picture)
                    else:
                        "Эдди продолжает трахать Ребекку, ее большие сиськи болтаются при каждом его толчке. Вдова громко стонет от наслаждения при каждом движении члена управляющего в ее киске."
                        $ _eddie_fuck_picture = "fuck" + str(procedural_randint(1, 4, key="procedural:NPC/Secondary/IntEddieBeckySex.rpy:procedural_randint:211:2"))
                        call ShowImage("becky", "sexeddie", _eddie_fuck_picture)

                if pregnancy.get(GirlNameIBS, 0) > 130:
                    "Ребенок в животе Бекки шевелится, реагируя на движения члена Эдди."

                python:
                    _iebs_inc_arousal(GirlNameIBS, 26)
                    _iebs_inc_arousal("eddie", 20)
                    _iebs_set_eddie_pos(1)
                call CockPosition(GirlNameIBS, 1, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить в рот" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and (EddieCockInMouth.get(GirlNameIBS, 0) or EddieCockInTits.get(GirlNameIBS, 0)) and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                "Эдди прижал голову Бекки к себе и начал заполнять ее рот своим семенем."
                "Когда он ее отпустил, разбитная вдова начисто облизала член Эдди."
                if CockInPussy.get(GirlNameIBS, 0) == 1:
                    "При этом сладострастная торговка не забывала еще и вам подмахивать, приближая и ваш собственный оргазм."
                    python:
                        _iebs_inc_arousal("You", 10)
                $ _iebs_set_arousal("eddie", 0)
                call PregnancyCheck(GirlNameIBS, "mouth", 1, "eddie")
                python:
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить на лицо" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                "Почувствовав что кончает, Эдди вытащил член из Бекки и залил ее смазливое личико своим семенем. Бекки вытерла сперму с зажмуренных глаз и ошарашенно заморгала: сперма ее управляющего покрывала ее личико и капала на ее монументальный бюст. Отдельные белые капли застряли даже в ее рыжей шевелюре."
                $ _iebs_set_arousal("eddie", 0)
                call PregnancyCheck(GirlNameIBS, "face", 1, "eddie")
                python:
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить на груди" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and TitsVisible.get(GirlNameIBS, 0) and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                "Эдди направил свой член на сиси Бекки и метко выстрелил несколькими струями спермы на обе ее груди, попав точно в ареолы. \"Такому меткому стрелку прямая дорога в королевскую гвардию,\" невпопад подумали вы."
                $ _iebs_set_arousal("eddie", 0)
                call PregnancyCheck(GirlNameIBS, "tits", 1, "eddie")
                python:
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить в Бекки" if _cametoday_eddie < _cancumdaily_eddie and _iebs_arousal("eddie") >= 100 and EddieCockInPussy.get(GirlNameIBS, 0):
                if pregnancy.get(GirlNameIBS, 0) < 120 and getPersonInfo(GirlNameIBS).corruption < 65:
                    if CockInMouth.get(GirlNameIBS, 0) == 1:
                        "Эдди увеличил темп, и Бекки, выплюнув ваш член, с ужасом спросила, не спускает ли он в нее."
                    else:
                        "Эдди увеличил темп, и Бекки с ужасом спросила, не спускает ли он в нее."
                    "Оттолкнуть Эдди она успела, но было поздно: семя уже вытекало из ее киски."
                else:
                    "Эдди выполнил просьбу Бекки и залил ее щелку молодым семенем."
                    if CockInMouth.get(GirlNameIBS, 0) == 1:
                        "Бекки промычала что-то неразборчивое, так как вы продолжали трахать ее в рот."
                        python:
                            _iebs_inc_arousal("You", 10)
                    if pregnancy.get(GirlNameIBS, 0) >= 120:
                        "\"Ну мальчики, нагуляла я с вами животик, так вы и дальше пользуетесь моей слабостью,\" — сладострастно улыбнулась Бекки."

                $ _iebs_set_arousal("eddie", 0)
                python:
                    _iebs_inc_arousal(GirlNameIBS, 5)
                    _iebs_set_eddie_pos(0)
                call PregnancyCheck(GirlNameIBS, "inside", 1, "eddie")
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Закончить":
                return

    return
