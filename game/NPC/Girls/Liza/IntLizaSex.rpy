# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntLizaSex(GirlNameILSS="liza", GirlLocILSS="street"):
    $ SomebodyCums = 0
    python:
        if GirlNameILSS not in topdress:
            topdress[GirlNameILSS] = ""
        if GirlNameILSS not in bottomdress:
            bottomdress[GirlNameILSS] = ""
        if GirlNameILSS not in panties:
            panties[GirlNameILSS] = ""
        if GirlNameILSS not in topraised:
            topraised[GirlNameILSS] = 0
        if GirlNameILSS not in bottomraised:
            bottomraised[GirlNameILSS] = 0
        if GirlNameILSS not in TitsVisible:
            TitsVisible[GirlNameILSS] = 0
        if GirlNameILSS not in PussyVisible:
            PussyVisible[GirlNameILSS] = 0
        if GirlNameILSS not in CockInMouth:
            CockInMouth[GirlNameILSS] = 0
        if GirlNameILSS not in CockInPussy:
            CockInPussy[GirlNameILSS] = 0
        if GirlNameILSS not in CockInTits:
            CockInTits[GirlNameILSS] = 0
        if GirlNameILSS not in CumFaceYou:
            CumFaceYou[GirlNameILSS] = 0
        if GirlNameILSS not in CumFaceOthers:
            CumFaceOthers[GirlNameILSS] = 0
        if GirlNameILSS not in CumTitsYou:
            CumTitsYou[GirlNameILSS] = 0
        if GirlNameILSS not in CumTitsOthers:
            CumTitsOthers[GirlNameILSS] = 0
        if GirlNameILSS not in CumInsideYou:
            CumInsideYou[GirlNameILSS] = 0
        if GirlNameILSS not in CumInsideOthers:
            CumInsideOthers[GirlNameILSS] = 0
        if "You" not in Arousal:
            Arousal["You"] = 0
        if GirlNameILSS not in Arousal:
            Arousal[GirlNameILSS] = 0
        if GirlNameILSS not in LickPussy:
            LickPussy[GirlNameILSS] = 0
        if GirlNameILSS not in Friends:
            Friends[GirlNameILSS] = 0
        if GirlNameILSS not in sluttiness:
            sluttiness[GirlNameILSS] = 0
        if GirlNameILSS not in pregnancy:
            pregnancy[GirlNameILSS] = 0
    call CockPosition(GirlNameILSS, 0, "You")
    call CheckVisibility(GirlNameILSS)

    label int_liza_sex_menu:
        python:
            if isinstance(cametoday, (int, float)):
                _cametoday = int(cametoday)
            elif isinstance(cametoday, dict):
                _cametoday = int(cametoday.get("You", cametoday.get("you", 0)) or 0)
            else:
                _cametoday = 0

            if isinstance(cancumdaily, (int, float)):
                _cancumdaily = int(cancumdaily)
            elif isinstance(cancumdaily, dict):
                _cancumdaily = int(cancumdaily.get("You", cancumdaily.get("you", 1)) or 1)
            else:
                _cancumdaily = 1
            _player_ready_to_cum = int(Arousal.get("You", Arousal.get("you", 0)) or 0) >= 100
            _can_player_cum = _cametoday < _cancumdaily or _player_ready_to_cum

            _sex_ctx = "sextraktir" if GirlLocILSS == "tavern" else "sexstreet"

        menu:
            "Осмотреть":
                if renpy.has_label("GirlsDesc"):
                    call GirlsDesc(GirlNameILSS)
                jump int_liza_sex_menu

            "Снять блузку" if topdress.get(GirlNameILSS, "") != "" and SomebodyCums == 0:
                "Вы сняли с [RealName2.get(GirlNameILSS, GirlNameILSS)] блузку, обнажив ее до пояса."
                $ topdress[GirlNameILSS] = ""
                call CheckVisibility(GirlNameILSS)
                call CockPosition(GirlNameILSS, 0)
                call ShowLizaPortrait
                jump int_liza_sex_menu

            "Растегнуть блузку" if topdress.get(GirlNameILSS, "") != "" and topraised.get(GirlNameILSS, 0) == 0 and SomebodyCums == 0:
                "Вы расстегнули блузку [RealName2.get(GirlNameILSS, GirlNameILSS)], выпустив на волю ее маленькие крепкие мячики."
                $ topraised[GirlNameILSS] = 1
                call CheckVisibility(GirlNameILSS)
                call CockPosition(GirlNameILSS, 0)
                call ShowLizaPortrait
                jump int_liza_sex_menu

            "Задрать юбочку" if bottomdress.get(GirlNameILSS, "") != "" and bottomraised.get(GirlNameILSS, 0) == 0 and SomebodyCums == 0:
                if panties.get(GirlNameILSS, "") != "":
                    "Вы задрали красотке юбочку до пояса, обнаружив под ней маленькие кружевные панталончики."
                else:
                    "Вы прошептали свое нескромное пожелание. [RealName.get(GirlNameILSS, GirlNameILSS)] покраснела, но задрала подол платьичка."
                $ bottomraised[GirlNameILSS] = 1
                call CheckVisibility(GirlNameILSS)
                call CockPosition(GirlNameILSS, 0)
                call ShowLizaPortrait
                jump int_liza_sex_menu

            "Снять панталончики" if panties.get(GirlNameILSS, "") != "" and SomebodyCums == 0:
                if bottomraised.get(GirlNameILSS, 0) == 0 and bottomdress.get(GirlNameILSS, "") != "":
                    "Вы засунули руки под подол платья и стащили с нее панталончики до щиколоток."
                else:
                    "Вы аккуратно стянули с нее панталончики, открывая киску нескромным взорам."
                $ panties[GirlNameILSS] = ""
                call CheckVisibility(GirlNameILSS)
                call CockPosition(GirlNameILSS, 0)
                call ShowLizaPortrait
                jump int_liza_sex_menu

            "Вытереть сперму с лица" if (CumFaceYou.get(GirlNameILSS, 0) or CumFaceOthers.get(GirlNameILSS, 0)) and SomebodyCums == 0:
                "Вы предложили шлюшке убрать с лица результаты ее предыдущих похождений. [RealName.get(GirlNameILSS, GirlNameILSS)] покраснела, достала платочек и вытерла лицо и волосы от спермы."
                $ CumFaceYou[GirlNameILSS] = 0
                $ CumFaceOthers[GirlNameILSS] = 0
                call CheckVisibility(GirlNameILSS)
                call CockPosition(GirlNameILSS, 0)
                call ShowLizaPortrait
                jump int_liza_sex_menu

            "Вытереть сперму с грудей" if (CumTitsYou.get(GirlNameILSS, 0) or CumTitsOthers.get(GirlNameILSS, 0)) and TitsVisible.get(GirlNameILSS, 0) and SomebodyCums == 0:
                "Вы предложили шлюшке убрать с сисечек результаты ее предыдущих похождений. [RealName.get(GirlNameILSS, GirlNameILSS)] достала платочек и, кокетливо улыбаясь, вытерла свои маленькие грудки от спермы."
                $ CumTitsYou[GirlNameILSS] = 0
                $ CumTitsOthers[GirlNameILSS] = 0
                call CheckVisibility(GirlNameILSS)
                call CockPosition(GirlNameILSS, 0)
                call ShowLizaPortrait
                jump int_liza_sex_menu

            "Вытереть сперму с бедер" if (CumInsideYou.get(GirlNameILSS, 0) or CumInsideOthers.get(GirlNameILSS, 0)) and PussyVisible.get(GirlNameILSS, 0) and SomebodyCums == 0:
                "Вы предложили девчушке убрать с влагалища и бедер результаты ее предыдущих похождений. [RealName.get(GirlNameILSS, GirlNameILSS)] достала платочек и, виновато посматривая на вас, вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                $ CumInsideYou[GirlNameILSS] = 0
                $ CumInsideOthers[GirlNameILSS] = 0
                call CheckVisibility(GirlNameILSS)
                call CockPosition(GirlNameILSS, 0)
                call ShowLizaPortrait
                jump int_liza_sex_menu

            "Целовать" if SomebodyCums == 0:
                "[RealName.get(GirlNameILSS, GirlNameILSS)] со всей страстью молодости целует вас в засос, переплетаясь языками."
                if CumFaceYou.get(GirlNameILSS, 0) > 0:
                    "На язык вам попадают капли вашего семени, которым вы обкончали ее раньше."
                elif CumFaceOthers.get(GirlNameILSS, 0) > 0:
                    "Вы чувствуете солоноватый привкус чужой спермы. Шустрая девчонка уже успела у кого-то отсосать до вас!"
                if Arousal.get(GirlNameILSS, 0) < 50:
                    $ Arousal[GirlNameILSS] = Arousal.get(GirlNameILSS, 0) + 8
                if Arousal.get("You", 0) < 50:
                    $ Arousal["You"] = Arousal.get("You", 0) + 8
                call CockPosition(GirlNameILSS, 0)
                call ShowCurrentSex(GirlNameILSS)
                jump int_liza_sex_menu

            "Лапать" if SomebodyCums == 0:
                if TitsVisible.get(GirlNameILSS, 0) == 0:
                    "Вы начали гладить маленькие сисечки через тонкую ткань блузки."
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameILSS, "sexstreet", "grope")
                else:
                    "Вы припали ртом к обнаженным мячикам, лаская чувствительные соски."
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameILSS, "sexstreet", "gropetits")

                if PussyVisible.get(GirlNameILSS, 0) == 1:
                    "Вы медленно опустили руку вниз и начали нежно массировать ее вульву."
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameILSS, "sexstreet", "gropepussy")
                else:
                    "Вы ласкаете ее киску через одежду."

                if Arousal.get(GirlNameILSS, 0) < 60:
                    $ Arousal[GirlNameILSS] = Arousal.get(GirlNameILSS, 0) + 12
                call CockPosition(GirlNameILSS, 0)
                call ShowCurrentSex(GirlNameILSS)
                jump int_liza_sex_menu

            "Лизать киску" if PussyVisible.get(GirlNameILSS, 0) and SomebodyCums == 0:
                "[RealName.get(GirlNameILSS, GirlNameILSS)] радостно предоставила вам свое похотливое влагалище. Вы начали старательно ласкать развратницу языком. [RealName.get(GirlNameILSS, GirlNameILSS)] прижимает вашу голову к себе обеими руками и сладко попискивает при каждом движении вашего языка."
                if CumInsideYou.get(GirlNameILSS, 0) > 0:
                    "Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameILSS, GirlNameILSS)]."
                elif CumInsideOthers.get(GirlNameILSS, 0) > 0:
                    "Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameILSS, GirlNameILSS)], кто-то уже успел оттрахать эту девочку до вас."
                $ LickPussy[GirlNameILSS] = LickPussy.get(GirlNameILSS, 0) + 1
                if LickPussy.get(GirlNameILSS, 0) == 7:
                    "\"Ой, дяденька, какой ты хороший!\"  говорит [RealName.get(GirlNameILSS, GirlNameILSS)]. \"Многие дяденьки сразу начинают меня сношать, а ведь я так люблю когда мне там внизу лижут!\""
                    $ Friends[GirlNameILSS] = Friends.get(GirlNameILSS, 0) + 1
                $ Arousal[GirlNameILSS] = Arousal.get(GirlNameILSS, 0) + 26
                call CockPosition(GirlNameILSS, 0)
                call ShowCurrentSex(GirlNameILSS)
                if renpy.has_label("ShowImage"):
                    if GirlLocILSS == "tavern":
                        call ShowImage(GirlNameILSS, "sextraktir", "lick")
                    else:
                        call ShowImage(GirlNameILSS, "sexstreet", "lick" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:199:1")))
                jump int_liza_sex_menu

            "Предложить отсосать" if _can_player_cum and SomebodyCums == 0:
                if CockInMouth.get(GirlNameILSS, 0):
                    "[RealName.get(GirlNameILSS, GirlNameILSS)] сидит перед вами на коленках и продолжает "
                else:
                    "[RealName.get(GirlNameILSS, GirlNameILSS)] опустилась перед вами на коленки и стала "
                if Arousal.get("You", 0) < 20:
                    "облизывать ваш вялый член."
                elif Arousal.get("You", 0) < 40:
                    "облизывать головку вашего напрягшегося члена."
                elif sluttiness.get(GirlNameILSS, 0) < 40:
                    "неумело, но с энтузиазмом сосать ваш член."
                elif Arousal.get("You", 0) < 60:
                    "умело сосать ваш член."
                else:
                    "заглатывать ваш член по самые яйца."
                if sluttiness.get(GirlNameILSS, 0) < 40:
                    $ Arousal["You"] = Arousal.get("You", 0) + 14
                else:
                    $ Arousal["You"] = Arousal.get("You", 0) + 20
                $ CockInMouth[GirlNameILSS] = 1
                $ CockInPussy[GirlNameILSS] = 0
                $ CockInTits[GirlNameILSS] = 0
                call ShowCurrentSex(GirlNameILSS)
                if renpy.has_label("ShowImage"):
                    if GirlLocILSS == "tavern":
                        call ShowImage(GirlNameILSS, "sextraktir", "minet" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:227:2")))
                    else:
                        call ShowImage(GirlNameILSS, "sexstreet", "minet" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:229:3")))
                jump int_liza_sex_menu

            "Трахать" if _can_player_cum and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and Arousal.get(GirlNameILSS, 0) >= 20 and PussyVisible.get(GirlNameILSS, 0):
                if pregnancy.get(GirlNameILSS, 0) < 130:
                    if CockInPussy.get(GirlNameILSS, 0) == 0:
                        "Вы впились в губы девушки и насадили ее на вздыбленный член."
                        if renpy.has_label("ShowImage"):
                            if GirlLocILSS == "tavern":
                                call ShowImage(GirlNameILSS, "sextraktir", "fuckstart" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:238:4")))
                            else:
                                call ShowImage(GirlNameILSS, "sexstreet", "fuck" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:240:5")))
                    else:
                        "Вы продолжаете трахать молоденькую мулатку на весу, и она стонет от наслаждения."
                        if renpy.has_label("ShowImage"):
                            if GirlLocILSS == "tavern":
                                call ShowImage(GirlNameILSS, "sextraktir", "fuck" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:245:6")))
                            else:
                                call ShowImage(GirlNameILSS, "sexstreet", "fuck" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:247:7")))
                else:
                    if CockInPussy.get(GirlNameILSS, 0) == 0:
                        "Из-за выросшего животика она встает раком, а вы начинаете сношать ее сзади."
                        if renpy.has_label("ShowImage"):
                            if GirlLocILSS == "tavern":
                                call ShowImage(GirlNameILSS, "sextraktir", "fuckstart" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:253:8")))
                            else:
                                call ShowImage(GirlNameILSS, "sexstreet", "rakomstart" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:255:9")))
                    else:
                        "Вы наращиваете темп, чувствуя как ребенок в ее животе шевелится при каждом толчке."
                        if renpy.has_label("ShowImage"):
                            if GirlLocILSS == "tavern":
                                call ShowImage(GirlNameILSS, "sextraktir", "fuck" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:260:10")))
                            else:
                                call ShowImage(GirlNameILSS, "sexstreet", "rakom" + str(procedural_randint(1, 6, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:262:11")))

                $ Arousal["You"] = Arousal.get("You", 0) + 20
                $ Arousal[GirlNameILSS] = Arousal.get(GirlNameILSS, 0) + 26
                $ CockInPussy[GirlNameILSS] = 1
                $ CockInMouth[GirlNameILSS] = 0
                $ CockInTits[GirlNameILSS] = 0
                call ShowCurrentSex(GirlNameILSS)
                jump int_liza_sex_menu

            "Кончить в ротик" if _can_player_cum and Arousal.get("You", 0) >= 100 and (CockInMouth.get(GirlNameILSS, 0) or CockInTits.get(GirlNameILSS, 0)):
                "Вы прижали голову мулатки к себе и разрядились ей в рот, залив горло и подбородок семенем."
                $ Arousal["You"] = 0
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameILSS, "mouthface", 1, "Вы")
                call CockPosition(GirlNameILSS, 0)
                $ CumFaceYou[GirlNameILSS] = 1
                $ SomebodyCums = 1
                if renpy.has_label("ShowImage"):
                    if GirlLocILSS == "tavern":
                        call ShowImage(GirlNameILSS, "sextraktir", "cummouth")
                    else:
                        call ShowImage(GirlNameILSS, "sexstreet", "cummouth")
                jump int_liza_sex_menu

            "Кончить на лицо" if _can_player_cum and Arousal.get("You", 0) >= 100:
                "Вы вытащили член и несколькими струями залили лицо девушки."
                $ Arousal["You"] = 0
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameILSS, "face", 1, "Вы")
                call CockPosition(GirlNameILSS, 0)
                $ CumFaceYou[GirlNameILSS] = 1
                $ SomebodyCums = 1
                if renpy.has_label("ShowImage"):
                    call ShowImage(GirlNameILSS, "sexstreet", "cumface")
                jump int_liza_sex_menu

            "Кончить на груди" if _can_player_cum and Arousal.get("You", 0) >= 100 and TitsVisible.get(GirlNameILSS, 0):
                "Вы вытащили член и залили спермой ее маленькие грудки."
                $ Arousal["You"] = 0
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameILSS, "tits", 1, "Вы")
                call CockPosition(GirlNameILSS, 0)
                $ CumTitsYou[GirlNameILSS] = 1
                $ SomebodyCums = 1
                if renpy.has_label("ShowImage"):
                    call ShowImage(GirlNameILSS, "sexstreet", "cumtits")
                jump int_liza_sex_menu

            "Кончить внутрь" if _can_player_cum and Arousal.get("You", 0) >= 100 and CockInPussy.get(GirlNameILSS, 0):
                if sluttiness.get(GirlNameILSS, 0) < 50 and pregnancy.get(GirlNameILSS, 0) < 120:
                    "Вы проигнорировали просьбу и начали заливать ее киску семенем."
                    "\"Дяденька Стефан, и вы тоже меня не послушали!\" — обреченно проговорила девушка."
                else:
                    "Вы, насадив худенькую смуглянку на член, начали заливать ее киску горячим семенем."
                $ Arousal["You"] = 0
                $ Arousal[GirlNameILSS] = Arousal.get(GirlNameILSS, 0) + 3
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameILSS, "inside", 1, "Вы")
                call CockPosition(GirlNameILSS, 0)
                $ CumInsideYou[GirlNameILSS] = 1
                $ SomebodyCums = 1
                if renpy.has_label("ShowImage"):
                    if GirlLocILSS == "tavern":
                        call ShowImage(GirlNameILSS, "sextraktir", "cumpussy")
                    else:
                        call ShowImage(GirlNameILSS, "sexstreet", "cumpussy")
                jump int_liza_sex_menu

            "Продолжить" if SomebodyCums == 1:
                $ SomebodyCums = 0
                jump int_liza_sex_menu

            "Закончить":
                $ SomebodyCums = 0
                return
