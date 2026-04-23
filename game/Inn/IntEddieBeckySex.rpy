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
        Arousal.setdefault(GirlNameIBS, 0)
        Arousal.setdefault("You", 0)
        Arousal.setdefault("you", Arousal.get("You", 0))
        Arousal.setdefault("eddie", 0)
        Arousal.setdefault("Eddie", Arousal.get("eddie", 0))
        GrupenSex.setdefault("eddie", 0)
        pregnancy.setdefault(GirlNameIBS, 0)
        sluttiness.setdefault(GirlNameIBS, 0)
        SomebodyCums = int(SomebodyCums or 0)
        if not isinstance(cametoday_npc, dict):
            cametoday_npc = {}

        def _iebs_sync_eddie_arousal():
            if "Eddie" in Arousal and "eddie" not in Arousal:
                Arousal["eddie"] = Arousal["Eddie"]
            if "eddie" in Arousal:
                Arousal["Eddie"] = Arousal["eddie"]

        def _iebs_inc_arousal(who, amount):
            key = "eddie" if str(who).lower() == "eddie" else who
            Arousal[key] = min(100, max(0, Arousal.get(key, 0) + amount))
            _iebs_sync_eddie_arousal()

        def _iebs_set_eddie_pos(pos):
            EddieCockInMouth[GirlNameIBS] = 1 if pos == 2 else 0
            EddieCockInPussy[GirlNameIBS] = 1 if pos == 1 else 0
            EddieCockInTits[GirlNameIBS] = 1 if pos == 3 else 0

        _iebs_sync_eddie_arousal()

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
            "Целовать маму" if SomebodyCums == 0 and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                if CockInPussy.get(GirlNameIBS, 0) > 0:
                    "Эдди, ничуть не смущаясь тем, что вы продолжаете сношать его маму, целует ее взасос. Та отвечает сыну взаимностью, не прекращая при этом и вам подмахивать."
                else:
                    "Эдди и Бекки целуются отнюдь не как сын с матерью, а страстно и взасос. Шаловливые ручки Эдди лапают мамины сиси."
                call ShowImage("becky", "sexeddie", "kiss")
                python:
                    _iebs_inc_arousal(GirlNameIBS, 10)
                    _iebs_inc_arousal("eddie", 10)
                    _iebs_set_eddie_pos(2)
                call CockPosition(GirlNameIBS, 2, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Лапать маму" if SomebodyCums == 0:
                if CockInMouth.get(GirlNameIBS, 0) == 1:
                    "Глядя на то, как Бекки отсасывает вам, Эдди начал лапать мать."
                elif CockInPussy.get(GirlNameIBS, 0) == 1:
                    "Глядя на то, как вы сношаете Бекки, к ней подкатился и ее сыночек."
                elif CockInTits.get(GirlNameIBS, 0) == 1:
                    "Увидев, как Бекки трахает ваш член грудями, Эдди тоже возбудился."
                else:
                    "Эдди начал жадно лапать мать, распаляя ее все сильнее."

                if CockInTits.get(GirlNameIBS, 0) == 0:
                    if TitsVisible.get(GirlNameIBS, 0) == 0:
                        "Эдди ласкает мамину грудь через одежду."
                    else:
                        "Эдди облизывает массивные мамины груди и слегка покусывает соски."
                if CockInPussy.get(GirlNameIBS, 0) == 0:
                    if PussyVisible.get(GirlNameIBS, 0) == 1:
                        "Потом он потянулся к истекающей соками маминой щели и начал ее нежно ласкать."
                    else:
                        "Потом он полез руками под одежду к маминой промежности."

                call ShowImage("becky", "sexeddie", "grope")
                python:
                    _iebs_inc_arousal(GirlNameIBS, 15)
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Полизать маме" if PussyVisible.get(GirlNameIBS, 0) and SomebodyCums == 0 and CockInPussy.get(GirlNameIBS, 0) == 0:
                if CockInMouth.get(GirlNameIBS, 0) == 1:
                    "Вы продолжаете сношать Бекки в рот, а внимание ее сыночка привлекло место, из которого он когда-то родился."
                    python:
                        _iebs_inc_arousal("You", 10)
                if CockInTits.get(GirlNameIBS, 0) == 1:
                    "Похотливая вдова продолжает трахать вас грудями, а ее сыночек опускается между ее ног."
                    python:
                        _iebs_inc_arousal("You", 20)
                if CumInsideYou.get(GirlNameIBS, 0) > 0 or CumInsideOthers.get(GirlNameIBS, 0) > 0:
                    "Сочащаяся из влагалища сперма не отпугнула Эдди, он припал к маминой щели и вылизал ее."
                    $ CumInsideYou[GirlNameIBS] = 0
                    $ CumInsideOthers[GirlNameIBS] = 0
                else:
                    "Эдди развел мамины ноги в стороны и начал лизать ей клитор."
                python:
                    _iebs_inc_arousal(GirlNameIBS, 26)
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Дать маме отсосать" if _cametoday_eddie < _cancumdaily_eddie and SomebodyCums == 0 and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                if CockInPussy.get(GirlNameIBS, 0) > 0:
                    if EddieCockInMouth.get(GirlNameIBS, 0) == 0:
                        "Эдди, решив присоединиться, поднес член к губам Бекки, и та с готовностью взяла его в рот."
                    else:
                        "Вы продолжаете трахать Бекки на пару с ее сыночком: вы в киску, он в ротик."
                    python:
                        _iebs_inc_arousal("You", 15)
                        _iebs_inc_arousal(GirlNameIBS, 20)
                else:
                    if EddieCockInMouth.get(GirlNameIBS, 0) == 0:
                        "Эдди подошел к Бекки и показал на свой член. Та наклонилась и начала его сосать."
                    else:
                        "Разгульная вдова продолжает умело отсасывать Эдди."

                if Arousal.get("eddie", 0) < 20:
                    "Она лишь облизывает его вялый член."
                elif Arousal.get("eddie", 0) < 40:
                    "Она облизывает головку напрягшегося члена сына."
                elif Arousal.get("eddie", 0) < 60:
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

            "Трахнуть мамины сиси" if _cametoday_eddie < _cancumdaily_eddie and SomebodyCums == 0 and Arousal.get("eddie", 0) >= 20 and TitsVisible.get(GirlNameIBS, 0) and pregnancy.get(GirlNameIBS, 0) < 130 and CockInTits.get(GirlNameIBS, 0) == 0 and CockInMouth.get(GirlNameIBS, 0) == 0:
                if CockInPussy.get(GirlNameIBS, 0) == 0:
                    if EddieCockInTits.get(GirlNameIBS, 0):
                        "Эдди лежит и балдеет, пока мама трахает его член своими грудями."
                    else:
                        "Эдди лег на кровать, а его мама опустилась над ним и зажала его член между грудей."
                else:
                    if EddieCockInTits.get(GirlNameIBS, 0):
                        "Пока Эдди трахает маму грудями, ваши толчки задают темп."
                    else:
                        "Эдди подлез под вас и вложил свой член между маминых сисек."
                    python:
                        _iebs_inc_arousal("You", 15)
                        _iebs_inc_arousal(GirlNameIBS, 20)
                python:
                    _iebs_inc_arousal("eddie", 15)
                    _iebs_set_eddie_pos(3)
                call CockPosition(GirlNameIBS, 3, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Трахать" if _cametoday_eddie < _cancumdaily_eddie and SomebodyCums == 0 and Arousal.get("eddie", 0) >= 20 and Arousal.get(GirlNameIBS, 0) >= 20 and PussyVisible.get(GirlNameIBS, 0) and CockInPussy.get(GirlNameIBS, 0) == 0:
                if CockInMouth.get(GirlNameIBS, 0) == 1:
                    if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                        "Эдди посмотрел как Ребекка делает вам минет, подошел к маме сзади и приставил свой член к щели, из которой он когда-то появился на свет. Бекки, почуствовав член сына, приглашающе вильнула попой и Эдди одним движением вошел в нее."
                    else:
                        "Эдди трахает свою мать сзади, загоняя свой член в нее по самые яйца а она, тем временем, продолжает вам отсасывать, практически не сбиваясь с темпа. Ну что за мастерица!"
                    call ShowImage("becky", "sexeddie", "doubleeddie")
                    python:
                        _iebs_inc_arousal("You", 15)
                elif CockInTits.get(GirlNameIBS, 0) == 1:
                    if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                        "Эдди посмотрел как Ребекка трахает ваш член своими грудями, на ее заманчиво оттопыренную задницу с обнаженной киской, и принял решение. Сорванец подошел к маме сзади и приставил свой член к щели, из которой он когда-то появился на свет. Бекки, почуствовав член сына, приглашающе вильнула попой и Эдди одним движением вошел в нее."
                    else:
                        "Бекки трахает ваш член своими грудями а Эдди, в свою очередь, сношает ее сзади, задавая темп."
                    python:
                        _iebs_inc_arousal("You", 15)
                else:
                    if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                        "Ребекка провела рукой по поднявшемуся члену Эдди: \"Давай, сыночек. Чего же ты ждешь, разве не видишь что я уже вся горю?\" - бесстыдно сказала она становясь раком перед сыном. Тот не заставил себя долго упрашивать и начал сношать мать сзади."
                        $ _eddie_fuck_picture = "fuckstart" + str(renpy.random.randint(1, 3))
                        call ShowImage("becky", "sexeddie", _eddie_fuck_picture)
                    else:
                        "Эдди продолжает трахать Ребекку, ее большие сиськи болтаются при каждом его толчке. Вдова громко стонет от наслаждения при каждом движении члена сына в ее киске."
                        $ _eddie_fuck_picture = "fuck" + str(renpy.random.randint(1, 4))
                        call ShowImage("becky", "sexeddie", _eddie_fuck_picture)

                if pregnancy.get(GirlNameIBS, 0) > 130:
                    "Ребенок в животе Бекки шевелится, реагируя на движения члена сына."

                python:
                    _iebs_inc_arousal(GirlNameIBS, 26)
                    _iebs_inc_arousal("eddie", 20)
                    _iebs_set_eddie_pos(1)
                call CockPosition(GirlNameIBS, 1, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить в рот" if _cametoday_eddie < _cancumdaily_eddie and Arousal.get("eddie", 0) >= 100 and (EddieCockInMouth.get(GirlNameIBS, 0) or EddieCockInTits.get(GirlNameIBS, 0)) and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                "Эдди прижал голову матери к себе и начал заполнять ее рот своим семенем."
                "Когда он ее отпустил, разбитная вдова начисто облизала член сына."
                if CockInPussy.get(GirlNameIBS, 0) == 1:
                    "При этом сладострастная торговка не забывала еще и вам подмахивать, приближая и ваш собственный оргазм."
                    python:
                        _iebs_inc_arousal("You", 10)
                $ Arousal["eddie"] = 0
                $ Arousal["Eddie"] = 0
                call PregnancyCheck(GirlNameIBS, "mouth", 1, "eddie")
                python:
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить на лицо" if _cametoday_eddie < _cancumdaily_eddie and Arousal.get("eddie", 0) >= 100 and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                "Почувствовав что кончает, Эдди вытащил член из мамы и залил ее смазливое личико своим семенем. Бекки вытерла сперму с зажмуренных глаз и ошарашенно заморгала: сперма ее сыночка покрывала ее личико и капала на ее монументальный бюст. Отдельные белые капли застряли даже в ее рыжей шевелюре."
                $ Arousal["eddie"] = 0
                $ Arousal["Eddie"] = 0
                call PregnancyCheck(GirlNameIBS, "face", 1, "eddie")
                python:
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить на груди" if _cametoday_eddie < _cancumdaily_eddie and Arousal.get("eddie", 0) >= 100 and TitsVisible.get(GirlNameIBS, 0) and CockInMouth.get(GirlNameIBS, 0) == 0 and CockInTits.get(GirlNameIBS, 0) == 0:
                "Эдди направил свой член на мамины сиси и метко выстрелил несколькими струями спермы на обе ее груди, попав точно в ареолы. \"Такому меткому стрелку прямая дорога в королевскую гвардию,\" невпопад подумали вы."
                $ Arousal["eddie"] = 0
                $ Arousal["Eddie"] = 0
                call PregnancyCheck(GirlNameIBS, "tits", 1, "eddie")
                python:
                    _iebs_set_eddie_pos(0)
                call CockPosition(GirlNameIBS, 0, "eddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_eddie_becky_sex_menu

            "Кончить в маму" if _cametoday_eddie < _cancumdaily_eddie and Arousal.get("eddie", 0) >= 100 and EddieCockInPussy.get(GirlNameIBS, 0):
                if pregnancy.get(GirlNameIBS, 0) < 120 and sluttiness.get(GirlNameIBS, 0) < 65:
                    if CockInMouth.get(GirlNameIBS, 0) == 1:
                        "Эдди увеличил темп, и Бекки, выплюнув ваш член, с ужасом спросила, не спускает ли он в нее."
                    else:
                        "Эдди увеличил темп, и Бекки с ужасом спросила, не спускает ли он в нее."
                    "Толкнуть сына она успела, но было поздно: семя уже вытекало из ее киски."
                else:
                    "Эдди выполнил мамину просьбу и залил ее щелку молодым семенем."
                    if CockInMouth.get(GirlNameIBS, 0) == 1:
                        "Бекки промычала что-то неразборчивое, так как вы продолжали трахать ее в рот."
                        python:
                            _iebs_inc_arousal("You", 10)
                    if pregnancy.get(GirlNameIBS, 0) >= 120:
                        "\"Ну мальчики, нагуляла я с вами животик, так вы и дальше пользуетесь моей слабостью,\" — сладострастно улыбнулась Бекки."

                $ Arousal["eddie"] = 0
                $ Arousal["Eddie"] = 0
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


label int_eddie_becky_sex(girl_name="becky"):
    call IntEddieBeckySex(girl_name)
    return
