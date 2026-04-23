init python:
    def _ibs_update_visibility(girl_name):
        check_visibility(girl_name)

    def _ibs_end_cock_state(girl_name):
        CockInMouth[girl_name] = 0
        CockInPussy[girl_name] = 0
        CockInTits[girl_name] = 0

    def _ibs_set_arousal(who, value):
        value = min(100, max(0, int(value or 0)))
        if str(who or "").lower() == "you":
            Arousal["You"] = value
            Arousal["you"] = value
            return
        Arousal[who] = value

    def _ibs_inc_arousal(who, amount):
        if str(who or "").lower() == "you":
            _ibs_set_arousal("You", int(Arousal.get("You", 0) or 0) + int(amount or 0))
            return
        Arousal[who] = min(100, max(0, int(Arousal.get(who, 0) or 0) + int(amount or 0)))

    def _ibs_eddie_observe_state(girl_name, obs_type=0):
        if int(GrupenSex.get("eddie", 0) or 0) <= 0:
            return ("", 0)
        if int(obs_type or 0) == 0 and int(TitsVisible.get(girl_name, 0) or 0):
            if int(sluttiness.get(girl_name, 0) or 0) < 55:
                return ("Бекки попыталась было прикрыть рукой свои тяжелые обнаженные груди от взгляда сына, но быстро одумалась.", 2)
            return ("Заметив, что ее сын любуется ее обнажившимися грудями, вдова повернулась к нему и начала играть с сосками.", 3)
        if int(obs_type or 0) == 1 and int(PussyVisible.get(girl_name, 0) or 0):
            if int(sluttiness.get(girl_name, 0) or 0) < 55:
                return ("Увидев, что ее сын пристально смотрит на ее щель, она плотно сжала ноги, но, вспомнив через несколько секунд, что о целомудрии имело смысл думать малость пораньше, немного расслабилась.", 4)
            return ("Заметив непристойный взгляд сына, направленный на ее голую промежность, вдова широко расставила ноги и стала играться с клитором. У Эдди разве что слюна со рта не закапала от такого зрелища.", 7)
        return ("Эдди с горящими глазами наблюдал за тем, как вы раздеваете его маму.", 0)


label IntBeckySex(GirlNameIBS="becky", GirlLocIBS="home", GirlModeIBS=""):
    hide screen main_ui
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
        CumFaceYou.setdefault(GirlNameIBS, 0)
        CumFaceOthers.setdefault(GirlNameIBS, 0)
        CumTitsYou.setdefault(GirlNameIBS, 0)
        CumTitsOthers.setdefault(GirlNameIBS, 0)
        CumInsideYou.setdefault(GirlNameIBS, 0)
        CumInsideOthers.setdefault(GirlNameIBS, 0)
        Arousal.setdefault("You", 0)
        Arousal.setdefault("you", Arousal.get("You", 0))
        Arousal.setdefault(GirlNameIBS, 0)
        Arousal.setdefault("eddie", 0)
        GiveOrgasms.setdefault(GirlNameIBS, 0)
        LickPussy.setdefault(GirlNameIBS, 0)
        GrupenSex.setdefault("eddie", 0)
        BeckyVar.setdefault("visitedhome", 0)
        sluttiness.setdefault(GirlNameIBS, 0)
        pregnancy.setdefault(GirlNameIBS, 0)
        SomebodyCums = int(SomebodyCums or 0)
        CurGiveOrgasms = GiveOrgasms.get(GirlNameIBS, 0)
        _ibs_update_visibility(GirlNameIBS)
    call ShowBeckyPortrait

    label int_becky_sex_menu:
        python:
            if isinstance(cametoday, (int, float)):
                _cametoday = cametoday
            elif isinstance(cametoday, dict):
                _cametoday = cametoday.get("You", cametoday.get("you", 0))
            else:
                _cametoday = 0

            if isinstance(cancumdaily, (int, float)):
                _cancumdaily = cancumdaily
            elif isinstance(cancumdaily, dict):
                _cancumdaily = cancumdaily.get("You", cancumdaily.get("you", 1))
            else:
                _cancumdaily = 1

        menu:
            "Осмотреть":
                if renpy.has_label("GirlsDesc"):
                    call GirlsDesc(GirlNameIBS)
                else:
                    "[RealName.get(GirlNameIBS, GirlNameIBS)] внимательно смотрит на вас."
                jump int_becky_sex_menu

            "Снять блузку" if topdress.get(GirlNameIBS, "") != "" and SomebodyCums == 0:
                "Хотя блузка [RealName2.get(GirlNameIBS, GirlNameIBS)] и так скрывала не слишком много, вы решили ее полностью снять. Расстегнув последние крючки и застежки, вы окончательно стянули этот явно лишний предмет."
                $ topdress[GirlNameIBS] = ""
                $ topraised[GirlNameIBS] = 0
                $ _ibs_update_visibility(GirlNameIBS)
                $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 0)
                if str(_ibs_observe_text or "").strip():
                    "[_ibs_observe_text]"
                $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Растегнуть блузку" if topdress.get(GirlNameIBS, "") != "" and topraised.get(GirlNameIBS, 0) == 0 and SomebodyCums == 0:
                "Вы начали ласкать груди Бекки сквозь одежду, а потом медленно распахнули блузку спереди, открывая обзор на грудь."
                $ topraised[GirlNameIBS] = 1
                $ _ibs_update_visibility(GirlNameIBS)
                $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 0)
                if str(_ibs_observe_text or "").strip():
                    "[_ibs_observe_text]"
                $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Снять лифчик" if bra.get(GirlNameIBS, "") != "" and (topdress.get(GirlNameIBS, "") == "" or topraised.get(GirlNameIBS, 0)) and SomebodyCums == 0:
                "Выше пояса на вдове теперь остается лишь лифчик. Вы заходите ей за спину и неторопливо расстегиваете его, освобождая тяжелые груди."
                $ bra[GirlNameIBS] = ""
                $ _ibs_update_visibility(GirlNameIBS)
                $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 0)
                if str(_ibs_observe_text or "").strip():
                    "[_ibs_observe_text]"
                $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Поднять подол" if bottomdress.get(GirlNameIBS, "") != "" and bottomraised.get(GirlNameIBS, 0) == 0 and SomebodyCums == 0:
                "Вы задрали подол платья, открывая ее бедра и нижнее белье для нескромного осмотра."
                $ bottomraised[GirlNameIBS] = 1
                $ _ibs_update_visibility(GirlNameIBS)
                $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 1)
                if str(_ibs_observe_text or "").strip():
                    "[_ibs_observe_text]"
                $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Снять платье" if bottomdress.get(GirlNameIBS, "") != "" and SomebodyCums == 0:
                "Решив, что одного задранного подола мало, вы развязали завязки и окончательно стянули с Бекки платье."
                $ bottomdress[GirlNameIBS] = ""
                $ bottomraised[GirlNameIBS] = 0
                $ _ibs_update_visibility(GirlNameIBS)
                $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 1)
                if str(_ibs_observe_text or "").strip():
                    "[_ibs_observe_text]"
                $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Снять панталончики" if panties.get(GirlNameIBS, "") != "" and SomebodyCums == 0:
                "Вы решаете избавиться от последнего препятствия и аккуратно стягиваете с нее панталончики, окончательно открывая киску нескромным взорам."
                $ panties[GirlNameIBS] = ""
                $ _ibs_update_visibility(GirlNameIBS)
                $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 1)
                if str(_ibs_observe_text or "").strip():
                    "[_ibs_observe_text]"
                $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Вытереть сперму с лица" if (CumFaceYou.get(GirlNameIBS, 0) or CumFaceOthers.get(GirlNameIBS, 0)) and SomebodyCums == 0:
                "Вы попросили вдовушку убрать с лица результаты ее предыдущих похождений. [RealName.get(GirlNameIBS, GirlNameIBS)] покраснела, достала платочек и вытерла лицо и волосы от спермы."
                $ CumFaceYou[GirlNameIBS] = 0
                $ CumFaceOthers[GirlNameIBS] = 0
                $ _ibs_update_visibility(GirlNameIBS)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Вытереть сперму с грудей" if (CumTitsYou.get(GirlNameIBS, 0) or CumTitsOthers.get(GirlNameIBS, 0)) and TitsVisible.get(GirlNameIBS, 0) and SomebodyCums == 0:
                "Вы попросили вдовушку убрать с сисечек результаты ее предыдущих похождений. [RealName.get(GirlNameIBS, GirlNameIBS)] достала платочек и, чуть стыдливо улыбаясь, вытерла свои дыньки от спермы."
                $ CumTitsYou[GirlNameIBS] = 0
                $ CumTitsOthers[GirlNameIBS] = 0
                $ _ibs_update_visibility(GirlNameIBS)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Вытереть сперму с бедер" if (CumInsideYou.get(GirlNameIBS, 0) or CumInsideOthers.get(GirlNameIBS, 0)) and PussyVisible.get(GirlNameIBS, 0) and SomebodyCums == 0:
                "Вы предложили развратной вдовушке убрать с влагалища и бедер результаты ее предыдущих похождений. [RealName.get(GirlNameIBS, GirlNameIBS)] достала платочек и, виновато посматривая на вас, вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                $ CumInsideYou[GirlNameIBS] = 0
                $ CumInsideOthers[GirlNameIBS] = 0
                $ _ibs_update_visibility(GirlNameIBS)
                call ShowBeckyPortrait
                jump int_becky_sex_menu

            "Целовать" if SomebodyCums == 0:
                if EddieCockInPussy.get(GirlNameIBS, 0) > 0:
                    "Вы впились в уста Бекки, пока ее сзади сношает сын."
                else:
                    "Бекки страстно целует вас в засос, переплетаясь языками."
                if CumFaceYou.get(GirlNameIBS, 0) > 0:
                    "На язык вам попадают следы вашего семени."
                elif CumFaceOthers.get(GirlNameIBS, 0) > 0:
                    "Вы чувствуете солоноватый привкус чужой спермы."
                python:
                    _ibs_inc_arousal(GirlNameIBS, 9)
                    _ibs_inc_arousal("You", 7)
                call ShowCurrentSex(GirlNameIBS)
                call ShowImage(GirlNameIBS, "sex", "kiss")
                jump int_becky_sex_menu

            "Лапать" if SomebodyCums == 0:
                if EddieCockInMouth.get(GirlNameIBS, 0) == 1:
                    "Полюбовавшись на делающую Эдди минет Бекки, вы решили, пользуясь предоставившейся возможностью, приласкать бедную вдову."
                if EddieCockInTits.get(GirlNameIBS, 0) == 1:
                    "Полюбовавшись на то как Бекки ласкает член сына своими сисями, вы решили в свою очередь немного приласкать бедную вдову."
                if EddieCockInPussy.get(GirlNameIBS, 0) == 1:
                    "Вы решили заняться массивными дойками Ребекки, пока Эдди сношает ее сзади."

                if EddieCockInTits.get(GirlNameIBS, 0) == 0:
                    if TitsVisible.get(GirlNameIBS, 0) == 0:
                        if DressPartSlut.get(topdress.get(GirlNameIBS, ""), 0) == 3 and bra.get(GirlNameIBS, "") == "":
                            "Вы начали гладить внушительные шары [RealName2.get(GirlNameIBS, GirlNameIBS)] через тонкую ткань ее блузки."
                        elif DressPartSlut.get(topdress.get(GirlNameIBS, ""), 0) >= 4 and bra.get(GirlNameIBS, "") == "":
                            "Ваши руки забрались под декольте [RealName2.get(GirlNameIBS, GirlNameIBS)] и, не обнаружив там лифчика, начали гладить ее груди и теребить напрягшиеся сосочки."
                        elif DressPartSlut.get(topdress.get(GirlNameIBS, ""), 0) >= 4 and bra.get(GirlNameIBS, "") != "":
                            "Ваши руки забрались под декольте [RealName2.get(GirlNameIBS, GirlNameIBS)] и начали мять ее груди через лифчик."
                        else:
                            "Вы начали гладить и мять внушительные сиськи [RealName2.get(GirlNameIBS, GirlNameIBS)] через одежду."
                        $ _becky_grope_pic = "grope" + str(renpy.random.randint(1, 2))
                        call ShowImage(GirlNameIBS, "sex", _becky_grope_pic)
                    else:
                        if CumTitsYou.get(GirlNameIBS, 0) > 0:
                            "Вы припали ртом к объемистым грудям [RealName2.get(GirlNameIBS, GirlNameIBS)], лаская языком ее чувствительные соски и слизывая с них свою сперму."
                        elif CumTitsOthers.get(GirlNameIBS, 0) > 0:
                            "Вы припали ртом к объемистым грудям [RealName2.get(GirlNameIBS, GirlNameIBS)], лаская языком ее чувствительные соски и слизывая с них чью-то сперму."
                        else:
                            "Вы припали ртом к объемистым грудям [RealName2.get(GirlNameIBS, GirlNameIBS)], лаская языком ее чувствительные соски."
                        call ShowImage(GirlNameIBS, "sex", "gropetits")

                if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                    if PussyVisible.get(GirlNameIBS, 0) == 1:
                        "Вы медленно опустили руку вниз, к ее истекающей соками похотливой вульвочке, и начали ее нежно массировать."
                        call ShowImage(GirlNameIBS, "sex", "gropenaked")
                    else:
                        if bottomraised.get(GirlNameIBS, 0) == 0 and bottomdress.get(GirlNameIBS, "") != "":
                            if DressPartSlut.get(bottomdress.get(GirlNameIBS, ""), 0) >= 4:
                                if panties.get(GirlNameIBS, "") != "":
                                    "Вы сунули руку под короткую юбчонку вашей любовницы и начали натирать ее киску сквозь панталончики."
                                else:
                                    "Вы сунули руку под короткую юбчонку вашей любовницы и стали наминать ее не стесненную бельем киску."
                            else:
                                if panties.get(GirlNameIBS, "") != "":
                                    "Вы наклонились и сунули похотливую ручонку под длинную юбку вашей любовницы, медленно, лаская ее ножки, поднялись наверх, к заветному месту и начали натирать ее киску сквозь панталончики."
                                else:
                                    "Вы наклонились и сунули похотливую ручонку под длинную юбку вашей любовницы, медленно, лаская ее ножки, поднялись наверх, к заветному месту и стали наминать ее не стесненную бельем киску."
                        else:
                            "Вы начали натирать ее похотливую киску сквозь панталончики."
                        call ShowImage(GirlNameIBS, "sex", "grope2")

                    if panties.get(GirlNameIBS, "") == "":
                        if CumInsideYou.get(GirlNameIBS, 0) > 0:
                            "Вы почувствовали свою сперму в пещерке [RealName2.get(GirlNameIBS, GirlNameIBS)]."
                        elif CumInsideOthers.get(GirlNameIBS, 0) > 0:
                            "Ваши пальцы заскользили по пещерке [RealName2.get(GirlNameIBS, GirlNameIBS)], похоже кто-то уже кончил в нее."
                $ _ibs_inc_arousal(GirlNameIBS, 15)
                call ShowCurrentSex(GirlNameIBS)
                jump int_becky_sex_menu

            "Лизать киску" if PussyVisible.get(GirlNameIBS, 0) and SomebodyCums == 0 and EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                if EddieCockInMouth.get(GirlNameIBS, 0) == 1:
                    "[RealName.get(GirlNameIBS, GirlNameIBS)], продолжая делать сыну минет, раздвинула ножки и предоставила вам свою похотливую щель в полное распоряжение. Чем вы и не замедлили воспользоваться, начав старательно ласкать ее своим язычком."
                    $ _ibs_inc_arousal("eddie", 10)
                elif EddieCockInTits.get(GirlNameIBS, 0) == 1:
                    "[RealName.get(GirlNameIBS, GirlNameIBS)], наклонившись продолжает трахать член сына своими дойками, тем самым предоставляя вам свою щелку в полное распоряжение. Чем вы и не замедлили воспользоваться, начав старательно ласкать ее своим языком."
                    $ _ibs_inc_arousal("eddie", 15)
                else:
                    "[RealName.get(GirlNameIBS, GirlNameIBS)] радостно предоставила вам свое похотливое влагалище. Вы начали старательно ласкать развратную вдовушку своим языком. [RealName.get(GirlNameIBS, GirlNameIBS)] прижимает вашу голову к себе обеими руками и сладко постанывает при каждом движении вашего языка."
                if CumInsideYou.get(GirlNameIBS, 0) > 0:
                    "Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameIBS, GirlNameIBS)]."
                elif CumInsideOthers.get(GirlNameIBS, 0) > 0:
                    "Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameIBS, GirlNameIBS)], кто-то уже успел оттрахать шуструю вдовицу до вас."
                $ LickPussy[GirlNameIBS] += 1
                if LickPussy.get(GirlNameIBS, 0) == 4:
                    "\"Стефан, такой молодой, а уже знаешь что нужно даме, негодник!\", смеясь говорит [RealName.get(GirlNameIBS, GirlNameIBS)], трепя вас за шевелюру. \"Продолжай же, продолжай!\""
                    $ Friends[GirlNameIBS] = Friends.get(GirlNameIBS, 0) + 1
                $ _ibs_inc_arousal(GirlNameIBS, 26)
                call ShowCurrentSex(GirlNameIBS)
                call ShowImage(GirlNameIBS, "sex", "lick")
                jump int_becky_sex_menu

            "Предложить отсосать" if _cametoday < _cancumdaily and SomebodyCums == 0 and EddieCockInMouth.get(GirlNameIBS, 0) == 0 and EddieCockInTits.get(GirlNameIBS, 0) == 0:
                if EddieCockInPussy.get(GirlNameIBS, 0) > 0:
                    if CockInMouth.get(GirlNameIBS, 0) == 0:
                        "Вы посмотрели немного на то, как задорно вдовушка сношается со своим сыночком, и решили поучаствовать в этом празднике жизни. Бекки не стала огорчать вас отказом и с готовностью приняла вашего дружка в свой ротик."
                    else:
                        "Вы вместе с Эдди продолжаете сношать Бекки в два смычка: он в киску, а вы в ротик."
                    $ _ibs_inc_arousal("eddie", 15)
                    $ _ibs_inc_arousal(GirlNameIBS, 20)
                else:
                    if CockInMouth.get(GirlNameIBS, 0):
                        "[RealName.get(GirlNameIBS, GirlNameIBS)] стоит перед вами на коленях и продолжает."
                    else:
                        "[RealName.get(GirlNameIBS, GirlNameIBS)] опустилась перед вами на коленки и стала."
                if Arousal.get("You", 0) < 20:
                    "Облизывать ваш вялый член."
                    call ShowImage(GirlNameIBS, "sex", "minet1")
                elif Arousal.get("You", 0) < 40:
                    "Облизывать головку вашего напрягшегося члена."
                    call ShowImage(GirlNameIBS, "sex", "minet2")
                elif sluttiness.get(GirlNameIBS, 0) < 40:
                    "Неумело, но с энтузиазмом сосать ваш член."
                    call ShowImage(GirlNameIBS, "sex", "minet3")
                elif Arousal.get("You", 0) < 60:
                    "Умело сосать ваш член."
                    call ShowImage(GirlNameIBS, "sex", "minet3")
                else:
                    "Заглатывать ваш член по самые яйца."
                    call ShowImage(GirlNameIBS, "sex", "minet4")
                $ CockInMouth[GirlNameIBS] = 1
                $ CockInPussy[GirlNameIBS] = 0
                $ CockInTits[GirlNameIBS] = 0
                if EddieCockInPussy.get(GirlNameIBS, 0) == 0 and GrupenSex.get("eddie", 0) > 0:
                    $ _becky_minetalone_pic = "minetalone" + str(renpy.random.randint(1, 3))
                    call ShowImage(GirlNameIBS, "sex", _becky_minetalone_pic)
                if sluttiness.get(GirlNameIBS, 0) < 40:
                    $ _ibs_inc_arousal("You", 14)
                else:
                    $ _ibs_inc_arousal("You", 20)
                if EddieCockInPussy.get(GirlNameIBS, 0) > 0:
                    call ShowImage(GirlNameIBS, "sexeddie", "doubleeddie")
                call ShowCurrentSex(GirlNameIBS)
                jump int_becky_sex_menu

            "Трахать между грудей" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and TitsVisible.get(GirlNameIBS, 0) and pregnancy.get(GirlNameIBS, 0) < 130 and EddieCockInTits.get(GirlNameIBS, 0) == 0 and EddieCockInMouth.get(GirlNameIBS, 0) == 0:
                if EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                    if CockInTits.get(GirlNameIBS, 0):
                        "Вы лежите на кровати, а вдовица, наклонившись над вами, трахает ваш член своими огромными дойками. Время от времени ей удается поймать головку вашего члена ротиком."
                    else:
                        "Вы легли на кровать, а [RealName.get(GirlNameIBS, GirlNameIBS)] наклонилась над вами, зажав ваш член между своих больших грудей. Затем она руками свела свои дойки вместе и начала слегка покачиваться, трахая вас своими сиськами. Иногда ей даже удается на секунду поймать головку вашего члена ртом."
                else:
                    if CockInTits.get(GirlNameIBS, 0):
                        "Пока Эдди трахает маму сзади, она в свою очередь трахает ваш член своими большими сиськами. Толчки Эдди задают темп всей вашей компании. Время от времени ей удается поймать головку вашего члена ротиком."
                    else:
                        "Воспользовавшись тем, что Эдди трахал маму сзади, вы ловко подлезли под вдову. [RealName.get(GirlNameIBS, GirlNameIBS)] сразу поняла, чего вы от нее хотите и немного опустилась, запустив ваш член между своих огромных грудей. Вы тоже времени даром не теряли и руками свели ее груди поближе друг к другу. Двигаясь взад и вперед под толчками сына она одновременно трахает и ваш член своими сиськами. Иногда ей даже удается на секунду поймать головку ртом."
                    $ _ibs_inc_arousal("eddie", 15)
                    $ _ibs_inc_arousal(GirlNameIBS, 20)
                $ CockInTits[GirlNameIBS] = 1
                $ CockInMouth[GirlNameIBS] = 0
                $ CockInPussy[GirlNameIBS] = 0
                $ _ibs_inc_arousal("You", 15)
                call ShowCurrentSex(GirlNameIBS)
                jump int_becky_sex_menu

            "Трахать" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and Arousal.get(GirlNameIBS, 0) >= 20 and PussyVisible.get(GirlNameIBS, 0) and EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                if pregnancy.get(GirlNameIBS, 0) < 130 and GrupenSex.get("eddie", 0) == 0:
                    if CockInPussy.get(GirlNameIBS, 0) == 0:
                        "Вы страстно впились поцелуем в губы [RealName2.get(GirlNameIBS, GirlNameIBS)]. Не прекращая целовать ее вы с некоторым трудом приподняли ее в воздух и насадили прямо на свой вздыбленный член. [RealName.get(GirlNameIBS, GirlNameIBS)] сладко охнула и, обхватив вас руками и ногами, стала подниматься и опускаться на вашем друге."
                        $ _becky_fuckstart_pic = "fuckstart" + str(renpy.random.randint(1, 8))
                        call ShowImage(GirlNameIBS, "sex", _becky_fuckstart_pic)
                    else:
                        "Вы, благодаря своей прекрасной физической форме, трахаете не столь легкую вдову на весу, обняв под ягодицы. После каждого толчка она опускается на ваш член всем своим весом, так что он входит в нее по самые яйца, чуть ли не доставая до матки. [RealName.get(GirlNameIBS, GirlNameIBS)] постанывает от наслаждения каждый раз как вы входите в нее."
                        $ _becky_fuck_pic = "fuck" + str(renpy.random.randint(1, 9))
                        call ShowImage(GirlNameIBS, "sex", _becky_fuck_pic)
                else:
                    if EddieCockInMouth.get(GirlNameIBS, 0) == 1:
                        if CockInPussy.get(GirlNameIBS, 0) == 0:
                            "Вы посмотрели на то, как Ребекка отсасывает сыну а потом перевели взгляд на ее истекающую соками дырочку. \"Ну, если это не приглашение, то я заморский гоблин-шахтер,\" подумали вы и резко вошли в любезно подставленную вам щель. Вдова охнула, но быстро приноровилась к вашим возвратно-поступательным движениям, не прекращая делать Эдди минет."
                            $ _becky_rakomstart_pic = "rakomstart" + str(renpy.random.randint(1, 3))
                            call ShowImage(GirlNameIBS, "sex", _becky_rakomstart_pic)
                        else:
                            "Вы трахаете Бекки сзади, массируя руками ее ягодицы, а она, в свою очередь, продолжает делать минет сыну. Должно быть ей трудно заниматься двумя делами сразу но справляется. Умница!"
                        $ _ibs_inc_arousal("eddie", 15)
                        $ _becky_rakom_pic = "rakom" + str(renpy.random.randint(1, 4))
                        call ShowImage(GirlNameIBS, "sex", _becky_rakom_pic)
                    elif EddieCockInTits.get(GirlNameIBS, 0) == 1:
                        if CockInPussy.get(GirlNameIBS, 0) == 0:
                            "Ребекка наклонилась над сыночком и трахает его член своими грудями, выставив свою истекающую соками дырочку на ваше обозрение. \"Ну, если это не приглашение, то я верховный маг высших эльфов,\" подумали вы и резко вошли в любезно подставленную вам щель, начав задавать темп вашей небольшой оргии. Вдове ваша помощь пришлась по нраву, она начала подмахивать вам, одновременно продолжая работать над членом сына."
                            $ _becky_rakomstart_pic = "rakomstart" + str(renpy.random.randint(1, 3))
                            call ShowImage(GirlNameIBS, "sex", _becky_rakomstart_pic)
                        else:
                            "Вы трахаете Бекки сзади, массируя руками ее ягодицы, а она, в свою очередь, трахает член Эдди своими дыньками. Ваши толчки задают ей темп, упрощая задачу. Как вы любите помогать людям!"
                        $ _ibs_inc_arousal("eddie", 15)
                        $ _becky_rakom_pic = "rakom" + str(renpy.random.randint(1, 4))
                        call ShowImage(GirlNameIBS, "sex", _becky_rakom_pic)
                    else:
                        if CockInPussy.get(GirlNameIBS, 0) == 0:
                            "Вы страстно впились поцелуем в губы [RealName2.get(GirlNameIBS, GirlNameIBS)]. С трудом оторвавшись от ее губ, вы развернули ее раком и вошли в ее разгоряченное лоно одним движением. Вдовушка охнула и, поймав темп ваших толчков, стала вам умело подмахивать."
                            $ _becky_rakomstart_pic = "rakomstart" + str(renpy.random.randint(1, 3))
                            call ShowImage(GirlNameIBS, "sex", _becky_rakomstart_pic)
                        else:
                            "Вы трахаете вдову раком на ее кровати. Она умело подмахивает вам, и ваш член входит в нее по самые яйца. Судя по всему [RealName3.get(GirlNameIBS, GirlNameIBS)] это приятно не меньше вашего, она постанывает от наслаждения при каждом толчке."
                            $ _becky_rakom_pic = "rakom" + str(renpy.random.randint(1, 4))
                            call ShowImage(GirlNameIBS, "sex", _becky_rakom_pic)
                if pregnancy.get(GirlNameIBS, 0) > 130:
                    "Вы чувствуете как ребенок в животе у [RealName2.get(GirlNameIBS, GirlNameIBS)] двигается каждый раз когда ваш член входит во влагалище его или ее развратной мамочки."
                $ CockInPussy[GirlNameIBS] = 1
                $ CockInMouth[GirlNameIBS] = 0
                $ CockInTits[GirlNameIBS] = 0
                $ _ibs_inc_arousal("You", 20)
                $ _ibs_inc_arousal(GirlNameIBS, 26)
                call ShowCurrentSex(GirlNameIBS)
                jump int_becky_sex_menu

            "Кончить в ротик" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and (CockInMouth.get(GirlNameIBS, 0) or CockInTits.get(GirlNameIBS, 0)) and EddieCockInMouth.get(GirlNameIBS, 0) == 0:
                "Чувствуя приближение концовки вы прижали голову [RealName2.get(GirlNameIBS, GirlNameIBS)] к себе как можно сильней, загоняя свой член ей в горло. Вдова восприняла это как должное, без видимых усилий заглотив ваш член целиком. В следующее мгновение вы разрядились, заливая горло и рот [RealName2.get(GirlNameIBS, GirlNameIBS)] своим семенем. Вдова сглотнула и с улыбкой облизала губы, убрав с них остатки вашей спермы. Вы вытащили свой обмякший член из заполненного спермой ротика."
                if EddieCockInPussy.get(GirlNameIBS, 0) == 1:
                    "Эдди с восторгом наблюдал за этой сценой, не переставая потрахивать мать."
                    $ _ibs_inc_arousal("eddie", 10)
                $ _ibs_set_arousal("You", 0)
                $ PregnancyCheck(GirlNameIBS, "mouth", 1, "Вы")
                $ _ibs_end_cock_state(GirlNameIBS)
                $ SomebodyCums = 1
                call ShowCurrentSex(GirlNameIBS)
                call ShowImage(GirlNameIBS, "sex", "cummouth")
                jump int_becky_sex_after_cum

            "Кончить на лицо" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and EddieCockInMouth.get(GirlNameIBS, 0) == 0 and EddieCockInTits.get(GirlNameIBS, 0) == 0:
                "Вы вытащили ваш член и в следующее мгновение поток спермы выстрелил в переносицу [RealName2.get(GirlNameIBS, GirlNameIBS)] прямо между глаз. Продолжение струи легло на щеку, третья струя залила подбородок. Ваша подружка стала еще красивее чем была: лицо всё в сперме, струйки спускаются на шею, стекают по подбородку и капают на полные сиськи. Что за прелесть!"
                $ _ibs_set_arousal("You", 0)
                $ PregnancyCheck(GirlNameIBS, "face", 1, "Вы")
                $ CumFaceYou[GirlNameIBS] = 1
                $ _ibs_end_cock_state(GirlNameIBS)
                $ SomebodyCums = 1
                call ShowCurrentSex(GirlNameIBS)
                jump int_becky_sex_after_cum

            "Кончить на груди" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and TitsVisible.get(GirlNameIBS, 0) and EddieCockInMouth.get(GirlNameIBS, 0) == 0 and EddieCockInTits.get(GirlNameIBS, 0) == 0:
                "Вы вытащили свой член из [RealName2.get(GirlNameIBS, GirlNameIBS)] и залили своей спермой ее монументальный бюст."
                $ _ibs_set_arousal("You", 0)
                $ PregnancyCheck(GirlNameIBS, "tits", 1, "Вы")
                $ CumTitsYou[GirlNameIBS] = 1
                $ _ibs_end_cock_state(GirlNameIBS)
                $ SomebodyCums = 1
                call ShowCurrentSex(GirlNameIBS)
                jump int_becky_sex_after_cum

            "Кончить внутрь" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and CockInPussy.get(GirlNameIBS, 0):
                if EddieCockInMouth.get(GirlNameIBS, 0) == 1:
                    "Приняв ее неразборчивое мычание за приглашение вы загнали свой член по самые яйца в ее похотливое влагалище и разрядились глубоко внутри [RealName.get(GirlNameIBS, GirlNameIBS)]. Бекки, почувствовав что вы кончили в нее промычала что-то неразборчивое, продолжая делать минет сынишке."
                    $ _ibs_inc_arousal("eddie", 10)
                else:
                    if pregnancy.get(GirlNameIBS, 0) < 120:
                        "Вы решили пойти на встречу просьбе вдовицы и, загнав свой член по самые яйца в ее похотливое влагалище, разрядились глубоко в [RealName.get(GirlNameIBS, GirlNameIBS)]. Стоило вам вытащить из нее свой обмякший член, как распутница провела пальчиком по своей измазанной семенем киске и, смотря вам в глаза, облизала его и с улыбкой сказала вам:"
                        "\"Стефанчик, какой ты нахальный. Пытаешься бедную одинокую вдову в положение ввести. Наглец!\""
                    else:
                        "Вы решили пойти на встречу просьбе вдовицы и, загнав свой член по самые яйца в ее беременное влагалище, разрядились глубоко в [RealName.get(GirlNameIBS, GirlNameIBS)], как будто пытаясь сделать ее еще более беременной. Стоило вам вытащить из нее свой обмякший член, как распутница погладила по свой округлившийся животик и сказала вам:"
                        "\"Какие же вы, мужчины, нахальные. Воспользовались слабостью бедной вдовы и оставили ее в тягости. Но и этого вам мало, и дальше моей слабостью пользуетесь. Ох, наглец!\""
                $ _ibs_set_arousal("You", 0)
                $ _ibs_set_arousal(GirlNameIBS, int(Arousal.get(GirlNameIBS, 0) or 0) + 3)
                $ PregnancyCheck(GirlNameIBS, "inside", 1, "Вы")
                $ CumInsideYou[GirlNameIBS] = 1
                $ _ibs_end_cock_state(GirlNameIBS)
                $ SomebodyCums = 1
                call ShowCurrentSex(GirlNameIBS)
                jump int_becky_sex_after_cum

            "Попрощаться и уйти" if SomebodyCums == 0:
                if CurGiveOrgasms == GiveOrgasms.get(GirlNameIBS, 0):
                    "Вы сказали [RealName.get(GirlNameIBS, GirlNameIBS)] что вам нужно идти. Она была поражена:"
                    "\"Стефанчик, но мы же ведь только начали! Что случилось?! Я что, тебе разонравилась?!\""
                    "Но вы были непреклонны и направились к выходу, оставив за спиной неудовлетворенную вдову."
                    if GrupenSex.get("eddie", 0) > 0:
                        "\"Впрочем,\" услышали вы уже в дверях, \"у меня еще сыночек мой любимый старшенький есть,\" и, оглянувшись перед тем как закрыть за собой дверь, вы увидели что Бекки тянет Эдди поближе к себе. \"Ты ведь не оставишь маму мучаться как этот мужлан, нет?\""
                        $ PregnancyCheck(GirlNameIBS, "inside", 1, "eddie")
                    $ slut_friends_increase(GirlNameIBS, 3, 1, -1, 0, 0, 0)
                    $ _becky_angry_pic = "angry" + str(renpy.random.randint(1, 2))
                    call ShowImage(GirlNameIBS, "sex", _becky_angry_pic)
                else:
                    "Вы поцеловали [RealName.get(GirlNameIBS, GirlNameIBS)], удовлетворенно развалившуюся на кровати, заверили ее что она была бесподобна, но сейчас вам надо возвращаться домой."
                    "\"Стефанчик, жаль, но раз надо то надо. Спасибо тебе, что порадовал меня, не побрезговал мной старой.\""
                    "Вы заверили ее что отнюдь не считаете ее старой, наоборот, она в самом соку, и, получив приглашение заходить еще, отправились к выходу."
                    if GrupenSex.get("eddie", 0) > 0:
                        if isinstance(cametoday, dict) and isinstance(cancumdaily, dict) and cametoday.get("eddie", 0) < cancumdaily.get("eddie", 0):
                            "Эдди помахал вам вслед рукой, он-то еще уходить явно не собирался."
                        else:
                            "Эдди помахал вам на прощание рукой и тоже стал одеваться."
                    $ slut_friends_increase(GirlNameIBS, 16, 2, 1, 42, 1, 1)
                    $ _becky_happy_pic = "happy" + str(renpy.random.randint(1, 5))
                    call ShowImage(GirlNameIBS, "sex", _becky_happy_pic)

                $ _ibs_set_arousal("You", 0)
                $ _ibs_set_arousal(GirlNameIBS, 0)
                $ _ibs_end_cock_state(GirlNameIBS)
                $ BeckyVar["visitedhome"] = max(BeckyVar.get("visitedhome", 0), 2)
                call ShowCurrentSex(GirlNameIBS)
                call DressUp(GirlNameIBS)
                $ SomebodyCums = 0
                $ calendar_advance_slots(1)
                if str(GirlLocIBS or "").strip().lower() == "home":
                    jump BeckyHomeAfterSex
                menu:
                    "Вернуться к трактиру":
                        if renpy.has_label("StreetTavern"):
                            jump StreetTavern
                        return
                    "Идти к выходу":
                        if renpy.has_label("MarketPlace"):
                            jump MarketPlace
                        return

            "Закончить":
                return

    label int_becky_sex_after_cum:
        menu:
            "Продолжить":
                $ SomebodyCums = 0
                jump int_becky_sex_menu

            "Закончить":
                $ SomebodyCums = 0
                if str(GirlLocIBS or "").strip().lower() == "home":
                    jump BeckyHomeAfterSex
                return


label int_becky_sex(girl_name="becky"):
    call IntBeckySex(girl_name)
    return
