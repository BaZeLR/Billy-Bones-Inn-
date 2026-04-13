init python:
    def georgett_sex_remove_blouse_state(girl_name="georgett"):
        girl_key = str(girl_name or "georgett")
        topdress[girl_key] = ""
        check_visibility(girl_key)

    def georgett_sex_unbutton_blouse_state(girl_name="georgett"):
        girl_key = str(girl_name or "georgett")
        topraised[girl_key] = 1
        check_visibility(girl_key)

    def georgett_sex_raise_skirt_state(girl_name="georgett"):
        girl_key = str(girl_name or "georgett")
        bottomraised[girl_key] = 1
        check_visibility(girl_key)


label IntGeorgettSexSetup(GirlNameIGSS="georgett", GirlLocIGSS="street"):
    $ SomebodyCums = 0
    python:
        if GirlNameIGSS not in topdress:
            topdress[GirlNameIGSS] = ""
        if GirlNameIGSS not in bottomdress:
            bottomdress[GirlNameIGSS] = ""
        if GirlNameIGSS not in bra:
            bra[GirlNameIGSS] = ""
        if GirlNameIGSS not in panties:
            panties[GirlNameIGSS] = ""
        if GirlNameIGSS not in topraised:
            topraised[GirlNameIGSS] = 0
        if GirlNameIGSS not in bottomraised:
            bottomraised[GirlNameIGSS] = 0
        if GirlNameIGSS not in TitsVisible:
            TitsVisible[GirlNameIGSS] = 0
        if GirlNameIGSS not in PussyVisible:
            PussyVisible[GirlNameIGSS] = 0
        if GirlNameIGSS not in CockInMouth:
            CockInMouth[GirlNameIGSS] = 0
        if GirlNameIGSS not in CockInPussy:
            CockInPussy[GirlNameIGSS] = 0
        if GirlNameIGSS not in CockInTits:
            CockInTits[GirlNameIGSS] = 0
        if GirlNameIGSS not in CumFaceYou:
            CumFaceYou[GirlNameIGSS] = 0
        if GirlNameIGSS not in CumFaceOthers:
            CumFaceOthers[GirlNameIGSS] = 0
        if GirlNameIGSS not in CumTitsYou:
            CumTitsYou[GirlNameIGSS] = 0
        if GirlNameIGSS not in CumTitsOthers:
            CumTitsOthers[GirlNameIGSS] = 0
        if GirlNameIGSS not in CumInsideYou:
            CumInsideYou[GirlNameIGSS] = 0
        if GirlNameIGSS not in CumInsideOthers:
            CumInsideOthers[GirlNameIGSS] = 0
        if "You" not in Arousal:
            Arousal["You"] = 0
        if GirlNameIGSS not in Arousal:
            Arousal[GirlNameIGSS] = 0
        if GirlNameIGSS not in LickPussy:
            LickPussy[GirlNameIGSS] = 0
        if GirlNameIGSS not in Friends:
            Friends[GirlNameIGSS] = 0
        if GirlNameIGSS not in pregnancy:
            pregnancy[GirlNameIGSS] = 0
    if (str(topdress.get(GirlNameIGSS, "") or "") == ""
            and str(bottomdress.get(GirlNameIGSS, "") or "") == ""
            and str(legs.get(GirlNameIGSS, "") or "") == ""
            and str(shoes.get(GirlNameIGSS, "") or "") == ""
            and str(dressdefault.get(GirlNameIGSS, "") or "") != ""):
        call DressUp(GirlNameIGSS)
    call CockPosition(GirlLocIGSS, 0, "You")
    call CheckVisibility(GirlNameIGSS)
    return


label IntGeorgettSexRemoveBlouse(GirlNameIGSS="georgett"):
    "Вы сняли с [RealName2.get(GirlNameIGSS, GirlNameIGSS)] блузку, обнажив ее до пояса."
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        "[_lactate_tits_desc]"
    $ georgett_sex_remove_blouse_state(GirlNameIGSS)
    call CockPosition(GirlNameIGSS, 0)
    call ShowGeorgettPortrait
    return


label IntGeorgettSexUnbuttonBlouse(GirlNameIGSS="georgett"):
    "Вы расстегнули блузку [RealName2.get(GirlNameIGSS, GirlNameIGSS)], выпустив ее большие груди на волю."
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        "[_lactate_tits_desc]"
    $ georgett_sex_unbutton_blouse_state(GirlNameIGSS)
    call CockPosition(GirlNameIGSS, 0)
    call ShowGeorgettPortrait
    return


label IntGeorgettSexRaiseSkirt(GirlNameIGSS="georgett"):
    "Вы задрали юбочку до пояса, с удовлетворением отметив, что шлюшка под ней ничего не носит."
    $ georgett_sex_raise_skirt_state(GirlNameIGSS)
    call CockPosition(GirlNameIGSS, 0)
    call ShowGeorgettPortrait
    return


label IntGeorgettSex(GirlNameIGSS="georgett", GirlLocIGSS="street"):
    call IntGeorgettSexSetup(GirlNameIGSS, GirlLocIGSS)

    label int_georgett_sex_menu:
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

        menu:
            "Осмотреть":
                if renpy.has_label("GirlsDesc"):
                    call GirlsDesc(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Снять блузку" if topdress.get(GirlNameIGSS, "") != "" and SomebodyCums == 0:
                call IntGeorgettSexRemoveBlouse(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Растегнуть блузку" if topdress.get(GirlNameIGSS, "") != "" and topraised.get(GirlNameIGSS, 0) == 0 and SomebodyCums == 0:
                call IntGeorgettSexUnbuttonBlouse(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Задрать юбочку" if bottomdress.get(GirlNameIGSS, "") != "" and bottomraised.get(GirlNameIGSS, 0) == 0 and SomebodyCums == 0:
                call IntGeorgettSexRaiseSkirt(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Вытереть сперму с лица" if (CumFaceYou.get(GirlNameIGSS, 0) or CumFaceOthers.get(GirlNameIGSS, 0)) and SomebodyCums == 0:
                "Вы предложили шлюшке убрать с лица результаты ее предыдущих похождений. [RealName.get(GirlNameIGSS, GirlNameIGSS)] достала платочек и вытерла лицо и волосы от спермы."
                $ CumFaceYou[GirlNameIGSS] = 0
                $ CumFaceOthers[GirlNameIGSS] = 0
                call CheckVisibility(GirlNameIGSS)
                call CockPosition(GirlNameIGSS, 0)
                call ShowGeorgettPortrait
                jump int_georgett_sex_menu

            "Вытереть сперму с грудей" if (CumTitsYou.get(GirlNameIGSS, 0) or CumTitsOthers.get(GirlNameIGSS, 0)) and TitsVisible.get(GirlNameIGSS, 0) and SomebodyCums == 0:
                "Вы предложили шлюшке убрать с сисечек результаты ее предыдущих похождений. [RealName.get(GirlNameIGSS, GirlNameIGSS)] достала платочек и вытерла свои груди от спермы."
                $ CumTitsYou[GirlNameIGSS] = 0
                $ CumTitsOthers[GirlNameIGSS] = 0
                call CheckVisibility(GirlNameIGSS)
                call CockPosition(GirlNameIGSS, 0)
                call ShowGeorgettPortrait
                jump int_georgett_sex_menu

            "Вытереть сперму с бедер" if (CumInsideYou.get(GirlNameIGSS, 0) or CumInsideOthers.get(GirlNameIGSS, 0)) and PussyVisible.get(GirlNameIGSS, 0) and SomebodyCums == 0:
                "Вы предложили шлюшке убрать с влагалища и бедер результаты ее предыдущих похождений. [RealName.get(GirlNameIGSS, GirlNameIGSS)] достала платочек и вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                $ CumInsideYou[GirlNameIGSS] = 0
                $ CumInsideOthers[GirlNameIGSS] = 0
                call CheckVisibility(GirlNameIGSS)
                call CockPosition(GirlNameIGSS, 0)
                call ShowGeorgettPortrait
                jump int_georgett_sex_menu

            "Целовать" if SomebodyCums == 0:
                "[RealName.get(GirlNameIGSS, GirlNameIGSS)] целует вас в засос, переплетаясь языками."
                if CumFaceYou.get(GirlNameIGSS, 0) > 0:
                    "На язык вам попадают капли вашего семени, которым вы обкончали ее раньше."
                elif CumFaceOthers.get(GirlNameIGSS, 0) > 0:
                    "Вы чувствуете солоноватый привкус чужой спермы. Шалунья уже успела у кого-то отсосать до вас!"
                if Arousal.get(GirlNameIGSS, 0) < 50:
                    $ Arousal[GirlNameIGSS] = Arousal.get(GirlNameIGSS, 0) + 7
                if Arousal.get("You", 0) < 50:
                    $ Arousal["You"] = Arousal.get("You", 0) + 7
                call CockPosition(GirlNameIGSS, 0)
                call ShowCurrentSex(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Лапать" if SomebodyCums == 0:
                if TitsVisible.get(GirlNameIGSS, 0) == 0:
                    "Вы начали мять сиськи через тонкую ткань ее блузки."
                else:
                    $ _grope_text = "Вы припали ртом к обнаженным грудям [RealName2.get(GirlNameIGSS, GirlNameIGSS)], лаская ртом ее чувствительные соски"
                    if CumTitsYou.get(GirlNameIGSS, 0) > 0:
                        $ _grope_text += " и слизывая с них свою сперму."
                    elif CumTitsOthers.get(GirlNameIGSS, 0) > 0:
                        $ _grope_text += " и слизывая с них чью-то сперму."
                    else:
                        $ _grope_text += "."
                    "[_grope_text]"
                $ _lactate_tits_fondle = LactateTitsFondle(GirlNameIGSS)
                if str(_lactate_tits_fondle or "").strip():
                    "[_lactate_tits_fondle]"
                if PussyVisible.get(GirlNameIGSS, 0) == 1:
                    "Вы медленно опустили руку вниз, к ее вульвочке, и начали ее нежно массировать."
                else:
                    "Вы сунули руку под короткую юбочку и стали наминать ее вульву."
                if CumInsideYou.get(GirlNameIGSS, 0) > 0:
                    "Вы почуствовали свою сперму в пещерке [RealName2.get(GirlNameIGSS, GirlNameIGSS)]."
                elif CumInsideOthers.get(GirlNameIGSS, 0) > 0:
                    "Ваши пальцы заскользили по пещерке [RealName2.get(GirlNameIGSS, GirlNameIGSS)], похоже кто-то уже кончил в нее."
                if TitsVisible.get(GirlNameIGSS, 0) == 0 and PussyVisible.get(GirlNameIGSS, 0) == 0:
                    call ShowImage(GirlNameIGSS, "sex", "grope")
                if Arousal.get(GirlNameIGSS, 0) < 60:
                    $ Arousal[GirlNameIGSS] = min(60, Arousal.get(GirlNameIGSS, 0) + 12)
                call CockPosition(GirlNameIGSS, 0)
                call ShowCurrentSex(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Лизать киску" if PussyVisible.get(GirlNameIGSS, 0) and SomebodyCums == 0:
                if GirlLocIGSS == "tavern":
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] легла на кровать и бесстыдно раздвинула ножки. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком."
                else:
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] стоя облокотилась спиной на стену, развинув бедра. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком."
                if CumInsideYou.get(GirlNameIGSS, 0) > 0:
                    "Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameIGSS, GirlNameIGSS)]."
                elif CumInsideOthers.get(GirlNameIGSS, 0) > 0:
                    "Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameIGSS, GirlNameIGSS)], кто-то уже успел оттрахать эту куколку до вас."
                $ LickPussy[GirlNameIGSS] = LickPussy.get(GirlNameIGSS, 0) + 1
                if LickPussy.get(GirlNameIGSS, 0) == 4:
                    "\"Ой, какой ты милый!\"  говорит [RealName.get(GirlNameIGSS, GirlNameIGSS)]. \"Многие мои клиенты особо не утруждаются чтобы сделать девушке приятное, но ты, я вижу, не из таких.\""
                    $ Friends[GirlNameIGSS] = Friends.get(GirlNameIGSS, 0) + 1
                $ Arousal[GirlNameIGSS] = Arousal.get(GirlNameIGSS, 0) + 20
                call CockPosition(GirlNameIGSS, 0)
                call ShowCurrentSex(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Предложить отсосать" if _cametoday < _cancumdaily and SomebodyCums == 0:
                if CockInMouth.get(GirlNameIGSS, 0):
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] сидит перед вами на корточках и продолжает "
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameIGSS, "sex", "minet2")
                else:
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] опустилась перед вами на корточки и стала "
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameIGSS, "sex", "minet1")
                if Arousal.get("You", 0) < 20:
                    "облизывать ваш вялый член."
                elif Arousal.get("You", 0) < 40:
                    "облизывать головку вашего напрягшегося члена."
                elif Arousal.get("You", 0) < 60:
                    "умело сосать ваш член."
                else:
                    "заглатывать ваш член по самые яйца."
                $ Arousal["You"] = Arousal.get("You", 0) + 20
                $ CockInMouth[GirlNameIGSS] = 1
                $ CockInPussy[GirlNameIGSS] = 0
                $ CockInTits[GirlNameIGSS] = 0
                call ShowCurrentSex(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Трахать между грудей" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and TitsVisible.get(GirlNameIGSS, 0) and pregnancy.get(GirlNameIGSS, 0) < 150:
                if GirlLocIGSS == "tavern":
                    if CockInTits.get(GirlNameIGSS, 0):
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] лежит изогнувшись на кровати, выставив вперед оба своих выдающихся достоинства, чтобы вы могли их трахнуть. Вы сношаете ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                    else:
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] легла спиной на кровать, частично свесившись, и изогнулась, выставив вперед оба своих выдающихся достоинства. Ваш член скользнул в ложбинку между ее холмов, и [RealName.get(GirlNameIGSS, GirlNameIGSS)] прижала свои сисечки руками одна к другой."
                        "Вы начали трахать ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                else:
                    if CockInTits.get(GirlNameIGSS, 0):
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] сидит перед вами на корточках, выставив вперед оба своих выдающихся достоинства. Вы трахаете ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                    else:
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] опустилась перед вами на корточки и изогнулась, выставив вперед оба своих выдающихся достоинства. Ваш член скользнул в ложбинку между ее холмов, и [RealName.get(GirlNameIGSS, GirlNameIGSS)] прижала свои сисечки руками одна к другой."
                        "Вы начали трахать ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                $ _lactate_tits_fuck = LactateTitsFuck(GirlNameIGSS)
                if str(_lactate_tits_fuck or "").strip():
                    "[_lactate_tits_fuck]"
                $ Arousal["You"] = Arousal.get("You", 0) + 20
                $ CockInTits[GirlNameIGSS] = 1
                $ CockInMouth[GirlNameIGSS] = 0
                $ CockInPussy[GirlNameIGSS] = 0
                call ShowCurrentSex(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Трахать" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and Arousal.get(GirlNameIGSS, 0) >= 20 and PussyVisible.get(GirlNameIGSS, 0):
                if GirlLocIGSS == "tavern":
                    if CockInPussy.get(GirlNameIGSS, 0) == 0:
                        "Вы легли на кровать и усадили девицу прямо на возбужденный член, засадив по самые яйца."
                        if renpy.has_label("ShowImage"):
                            if topdress.get(GirlNameIGSS, "") == "":
                                call ShowImage(GirlNameIGSS, "sex", "cowgirl3")
                            else:
                                call ShowImage(GirlNameIGSS, "sex", "cowgirl1")
                    else:
                        "Она страстно скачет на вас, пока вы мнете ее ягодицы и сиськи."
                        if renpy.has_label("ShowImage"):
                            if topdress.get(GirlNameIGSS, "") == "":
                                call ShowImage(GirlNameIGSS, "sex", "cowgirl4")
                            else:
                                call ShowImage(GirlNameIGSS, "sex", "cowgirl2")
                else:
                    if CockInPussy.get(GirlNameIGSS, 0) == 0:
                        "Она уперлась ладонями в стену и выставила киску. Вы немедленно засадили ей по самые яйца."
                        if renpy.has_label("ShowImage"):
                            call ShowImage(GirlNameIGSS, "sex", "doggy1")
                    else:
                        "Вы продолжаете страстно трахать девушку, нежно мять ее ягодицы и сиськи."
                        if renpy.has_label("ShowImage"):
                            call ShowImage(GirlNameIGSS, "sex", "doggy" + str(renpy.random.randint(2, 3)))
                if pregnancy.get(GirlNameIGSS, 0) >= 150:
                    "Вы чувствуете, как ребенок в ее животе шевелится при каждом толчке."
                $ _lactate_pussy_fuck = LactatePussyFuck(GirlNameIGSS)
                if str(_lactate_pussy_fuck or "").strip():
                    "[_lactate_pussy_fuck]"
                $ Arousal["You"] = Arousal.get("You", 0) + 20
                $ Arousal[GirlNameIGSS] = Arousal.get(GirlNameIGSS, 0) + 14
                $ CockInPussy[GirlNameIGSS] = 1
                $ CockInMouth[GirlNameIGSS] = 0
                $ CockInTits[GirlNameIGSS] = 0
                call ShowCurrentSex(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Кончить в ротик" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and (CockInMouth.get(GirlNameIGSS, 0) or CockInTits.get(GirlNameIGSS, 0)):
                "Ваш дружок напрягся и струя за струей заполнил ее ротик семенем."
                "[RealName.get(GirlNameIGSS, GirlNameIGSS)] судорожно заглатывала сперму и высунула язычок, показывая, что проглотила все."
                $ Arousal["You"] = 0
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameIGSS, "mouth", 1, "Вы")
                call CockPosition(GirlNameIGSS, 0)
                $ SomebodyCums = 1
                if renpy.has_label("ShowImage"):
                    call ShowImage(GirlNameIGSS, "sex", "cummouth")
                jump int_georgett_sex_menu

            "Кончить на лицо" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100:
                "Вы вытащили дружка в последний момент и густые струи семени ударили по ее щечкам и кудрям."
                $ Arousal["You"] = 0
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameIGSS, "face", 1, "Вы")
                call CockPosition(GirlNameIGSS, 0)
                $ SomebodyCums = 1
                if renpy.has_label("ShowImage"):
                    call ShowImage(GirlNameIGSS, "sex", "cummouth")
                jump int_georgett_sex_menu

            "Кончить на груди" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and TitsVisible.get(GirlNameIGSS, 0):
                "Вы вытащили член и немедленно разрядились на ее груди и живот."
                "[RealName.get(GirlNameIGSS, GirlNameIGSS)] провела пальцем по груди и облизала его, глядя вам в глаза."
                $ Arousal["You"] = 0
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameIGSS, "tits", 1, "Вы")
                call CockPosition(GirlNameIGSS, 0)
                $ SomebodyCums = 1
                jump int_georgett_sex_menu

            "Кончить внутрь" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and CockInPussy.get(GirlNameIGSS, 0):
                "Вы зарычали и кончили. Густые струи вашего семени хлынули в ее влагалище."
                "[RealName.get(GirlNameIGSS, GirlNameIGSS)] сладострастно застонала: \"Да, милый, прямо в маточку твое семя ударило, сладко-то как.\""
                "Обмякший член вывалился из ненасытной щелки, и из нее потекла вязкая белая струйка."
                $ Arousal["You"] = 0
                $ Arousal[GirlNameIGSS] = Arousal.get(GirlNameIGSS, 0) + 3
                if renpy.has_label("PregnancyCheck"):
                    call PregnancyCheck(GirlNameIGSS, "inside", 1, "Вы")
                call CockPosition(GirlNameIGSS, 0)
                $ SomebodyCums = 1
                if renpy.has_label("ShowImage"):
                    call ShowImage(GirlNameIGSS, "sex", "doggyinside")
                jump int_georgett_sex_menu

            "Продолжить" if SomebodyCums == 1:
                $ SomebodyCums = 0
                jump int_georgett_sex_menu

            "Закончить":
                $ SomebodyCums = 0
                return
