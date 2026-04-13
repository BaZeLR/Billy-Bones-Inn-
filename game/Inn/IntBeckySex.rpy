init python:
    def _ibs_call_label_or_fn(name, *args):
        fn = getattr(renpy.store, name, None)
        if callable(fn):
            try:
                return fn(*args)
            except Exception:
                return None
        if renpy.has_label(name):
            try:
                return renpy.call(name, *args)
            except Exception:
                return None
        return None

    def _ibs_return_to_location_after_sex(girl_loc=""):
        location_key = str(girl_loc or "").strip().lower()
        if location_key == "home" and renpy.has_label("BeckyHomeAfterSex"):
            renpy.call("BeckyHomeAfterSex")
            return True
        return False


label IntBeckySex(GirlNameIBS="becky", GirlLocIBS="home", GirlModeIBS=""):
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

        def _ibs_check_visibility():
            TitsVisible[GirlNameIBS] = 1 if (topdress.get(GirlNameIBS, "") == "" and bra.get(GirlNameIBS, "") == "") else 0
            if bottomdress.get(GirlNameIBS, "") == "":
                PussyVisible[GirlNameIBS] = 1 if panties.get(GirlNameIBS, "") == "" else 0
            else:
                PussyVisible[GirlNameIBS] = 1 if (bottomraised.get(GirlNameIBS, 0) and panties.get(GirlNameIBS, "") == "") else 0

        def _ibs_end_cock_state():
            CockInMouth[GirlNameIBS] = 0
            CockInPussy[GirlNameIBS] = 0
            CockInTits[GirlNameIBS] = 0

        def _ibs_inc_arousal(who, amount):
            Arousal[who] = min(100, max(0, Arousal.get(who, 0) + amount))

        def _ibs_eddie_observe(obs_type=0):
            if GrupenSex.get("eddie", 0) <= 0:
                return
            if obs_type == 0 and TitsVisible.get(GirlNameIBS, 0):
                if sluttiness.get(GirlNameIBS, 0) < 55:
                    renpy.say(None, "Бекки попыталась прикрыть обнаженные груди от взгляда сына, но быстро одумалась.")
                    _ibs_inc_arousal("eddie", 2)
                else:
                    renpy.say(None, "Заметив взгляд сына на груди, вдова повернулась к нему и начала играть с сосками.")
                    _ibs_inc_arousal("eddie", 3)
            elif obs_type == 1 and PussyVisible.get(GirlNameIBS, 0):
                if sluttiness.get(GirlNameIBS, 0) < 55:
                    renpy.say(None, "Увидев взгляд сына на ее щель, вдова на секунду сжала ноги, а потом расслабилась.")
                    _ibs_inc_arousal("eddie", 4)
                else:
                    renpy.say(None, "Заметив непристойный взгляд сына на голую промежность, вдова широко расставила ноги.")
                    _ibs_inc_arousal("eddie", 7)
            else:
                renpy.say(None, "Эдди с горящими глазами наблюдает за тем, как вы раздеваете его маму.")

        _ibs_check_visibility()

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
                "Вы окончательно сняли верхнюю часть одежды с [RealName2.get(GirlNameIBS, GirlNameIBS)]."
                $ topdress[GirlNameIBS] = ""
                $ topraised[GirlNameIBS] = 0
                python:
                    _ibs_check_visibility()
                    _ibs_eddie_observe(0)
                jump int_becky_sex_menu

            "Растегнуть блузку" if topdress.get(GirlNameIBS, "") != "" and topraised.get(GirlNameIBS, 0) == 0 and SomebodyCums == 0:
                "Вы распахнули блузку, открывая обзор на грудь."
                $ topraised[GirlNameIBS] = 1
                python:
                    _ibs_eddie_observe(0)
                jump int_becky_sex_menu

            "Снять лифчик" if bra.get(GirlNameIBS, "") != "" and (topdress.get(GirlNameIBS, "") == "" or topraised.get(GirlNameIBS, 0)) and SomebodyCums == 0:
                "Вы сняли с вдовы лифчик."
                $ bra[GirlNameIBS] = ""
                python:
                    _ibs_check_visibility()
                    _ibs_eddie_observe(0)
                jump int_becky_sex_menu

            "Поднять подол" if bottomdress.get(GirlNameIBS, "") != "" and bottomraised.get(GirlNameIBS, 0) == 0 and SomebodyCums == 0:
                "Вы задрали подол, приоткрывая ее бедра."
                $ bottomraised[GirlNameIBS] = 1
                python:
                    _ibs_check_visibility()
                    _ibs_eddie_observe(1)
                jump int_becky_sex_menu

            "Снять платье" if bottomdress.get(GirlNameIBS, "") != "" and SomebodyCums == 0:
                "Вы стянули с Бекки платье."
                $ bottomdress[GirlNameIBS] = ""
                $ bottomraised[GirlNameIBS] = 0
                python:
                    _ibs_check_visibility()
                    _ibs_eddie_observe(1)
                jump int_becky_sex_menu

            "Снять панталончики" if panties.get(GirlNameIBS, "") != "" and SomebodyCums == 0:
                "Вы сняли с нее панталончики."
                $ panties[GirlNameIBS] = ""
                python:
                    _ibs_check_visibility()
                    _ibs_eddie_observe(1)
                jump int_becky_sex_menu

            "Вытереть сперму с лица" if (CumFaceYou.get(GirlNameIBS, 0) or CumFaceOthers.get(GirlNameIBS, 0)) and SomebodyCums == 0:
                "Вдова достала платочек и вытерла лицо и волосы от спермы."
                $ CumFaceYou[GirlNameIBS] = 0
                $ CumFaceOthers[GirlNameIBS] = 0
                jump int_becky_sex_menu

            "Вытереть сперму с грудей" if (CumTitsYou.get(GirlNameIBS, 0) or CumTitsOthers.get(GirlNameIBS, 0)) and TitsVisible.get(GirlNameIBS, 0) and SomebodyCums == 0:
                "Бекки, чуть стыдливо улыбаясь, вытерла грудь от спермы."
                $ CumTitsYou[GirlNameIBS] = 0
                $ CumTitsOthers[GirlNameIBS] = 0
                jump int_becky_sex_menu

            "Вытереть сперму с бедер" if (CumInsideYou.get(GirlNameIBS, 0) or CumInsideOthers.get(GirlNameIBS, 0)) and PussyVisible.get(GirlNameIBS, 0) and SomebodyCums == 0:
                "Бекки вытерла бедра и лобок от спермы."
                $ CumInsideYou[GirlNameIBS] = 0
                $ CumInsideOthers[GirlNameIBS] = 0
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
                jump int_becky_sex_menu

            "Лапать" if SomebodyCums == 0:
                "Вы ласкаете вдову, все сильнее распаляя ее."
                python:
                    _ibs_inc_arousal(GirlNameIBS, 12)
                    _ibs_inc_arousal("You", 8)
                jump int_becky_sex_menu

            "Лизать киску" if PussyVisible.get(GirlNameIBS, 0) and SomebodyCums == 0 and EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                "Вы опустились между ее ног и начали делать куни."
                $ LickPussy[GirlNameIBS] += 1
                python:
                    _ibs_inc_arousal(GirlNameIBS, 24)
                    _ibs_inc_arousal("You", 8)
                jump int_becky_sex_menu

            "Предложить отсосать" if _cametoday < _cancumdaily and SomebodyCums == 0 and EddieCockInMouth.get(GirlNameIBS, 0) == 0 and EddieCockInTits.get(GirlNameIBS, 0) == 0:
                if EddieCockInPussy.get(GirlNameIBS, 0) > 0:
                    "Вы с Эдди продолжаете сношать Бекки в два смычка: он в киску, а вы в ротик."
                    python:
                        _ibs_inc_arousal("eddie", 15)
                        _ibs_inc_arousal(GirlNameIBS, 20)
                else:
                    "Бекки опустилась перед вами на колени и начала сосать ваш член."
                $ CockInMouth[GirlNameIBS] = 1
                $ CockInPussy[GirlNameIBS] = 0
                $ CockInTits[GirlNameIBS] = 0
                python:
                    _ibs_inc_arousal("You", 20)
                jump int_becky_sex_menu

            "Трахать между грудей" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and TitsVisible.get(GirlNameIBS, 0) and pregnancy.get(GirlNameIBS, 0) < 130 and EddieCockInTits.get(GirlNameIBS, 0) == 0 and EddieCockInMouth.get(GirlNameIBS, 0) == 0:
                if EddieCockInPussy.get(GirlNameIBS, 0) > 0:
                    "Пока Эдди трахает маму сзади, она трахает ваш член своими большими сиськами."
                    python:
                        _ibs_inc_arousal("eddie", 15)
                        _ibs_inc_arousal(GirlNameIBS, 20)
                else:
                    "Вы уложили вдову поудобнее и начали трахать членом между ее грудей."
                $ CockInTits[GirlNameIBS] = 1
                $ CockInMouth[GirlNameIBS] = 0
                $ CockInPussy[GirlNameIBS] = 0
                python:
                    _ibs_inc_arousal("You", 15)
                jump int_becky_sex_menu

            "Трахать" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and Arousal.get(GirlNameIBS, 0) >= 20 and PussyVisible.get(GirlNameIBS, 0) and EddieCockInPussy.get(GirlNameIBS, 0) == 0:
                if EddieCockInMouth.get(GirlNameIBS, 0) == 1 or EddieCockInTits.get(GirlNameIBS, 0) == 1:
                    "Пока Бекки занята сыном, вы входите в нее сзади и задаете темп вашей небольшой оргии."
                    python:
                        _ibs_inc_arousal("eddie", 15)
                else:
                    "Вы развернули вдову и вошли в ее горячее лоно одним движением."
                $ CockInPussy[GirlNameIBS] = 1
                $ CockInMouth[GirlNameIBS] = 0
                $ CockInTits[GirlNameIBS] = 0
                python:
                    _ibs_inc_arousal("You", 20)
                    _ibs_inc_arousal(GirlNameIBS, 26)
                jump int_becky_sex_menu

            "Кончить в ротик" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and (CockInMouth.get(GirlNameIBS, 0) or CockInTits.get(GirlNameIBS, 0)) and EddieCockInMouth.get(GirlNameIBS, 0) == 0:
                "Прижав голову Бекки, вы кончили ей в рот. Она проглотила и облизнула губы."
                if EddieCockInPussy.get(GirlNameIBS, 0) == 1:
                    "Эдди с восторгом наблюдал за этой сценой, не переставая потрахивать мать."
                    python:
                        _ibs_inc_arousal("eddie", 10)
                $ Arousal["You"] = 0
                $ _ibs_call_label_or_fn("PregnancyCheck", GirlNameIBS, "mouth", 1, "Вы")
                python:
                    _ibs_end_cock_state()
                $ SomebodyCums = 1
                $ _ibs_call_label_or_fn("ShowImage", GirlNameIBS, "sex", "cummouth")
                jump int_becky_sex_after_cum

            "Кончить на лицо" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and EddieCockInMouth.get(GirlNameIBS, 0) == 0 and EddieCockInTits.get(GirlNameIBS, 0) == 0:
                "Вы вытащили член и залили лицо Бекки спермыми струями."
                $ Arousal["You"] = 0
                $ _ibs_call_label_or_fn("PregnancyCheck", GirlNameIBS, "face", 1, "Вы")
                $ CumFaceYou[GirlNameIBS] = 1
                python:
                    _ibs_end_cock_state()
                $ SomebodyCums = 1
                jump int_becky_sex_after_cum

            "Кончить на груди" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and TitsVisible.get(GirlNameIBS, 0) and EddieCockInMouth.get(GirlNameIBS, 0) == 0 and EddieCockInTits.get(GirlNameIBS, 0) == 0:
                "Вы вытащили член и залили спермой ее монументальный бюст."
                $ Arousal["You"] = 0
                $ _ibs_call_label_or_fn("PregnancyCheck", GirlNameIBS, "tits", 1, "Вы")
                $ CumTitsYou[GirlNameIBS] = 1
                python:
                    _ibs_end_cock_state()
                $ SomebodyCums = 1
                jump int_becky_sex_after_cum

            "Кончить внутрь" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and CockInPussy.get(GirlNameIBS, 0):
                if EddieCockInMouth.get(GirlNameIBS, 0) == 1:
                    "Вы загнали член по самые яйца и разрядились глубоко внутри, пока Бекки продолжала делать Эдди минет."
                    python:
                        _ibs_inc_arousal("eddie", 10)
                else:
                    "Вы загнали член глубже и кончили прямо внутрь Бекки."
                $ Arousal["You"] = 0
                $ Arousal[GirlNameIBS] = min(100, Arousal.get(GirlNameIBS, 0) + 3)
                $ _ibs_call_label_or_fn("PregnancyCheck", GirlNameIBS, "inside", 1, "Вы")
                $ CumInsideYou[GirlNameIBS] = 1
                python:
                    _ibs_end_cock_state()
                $ SomebodyCums = 1
                jump int_becky_sex_after_cum

            "Попрощаться и уйти" if SomebodyCums == 0:
                if CurGiveOrgasms == GiveOrgasms.get(GirlNameIBS, 0):
                    "Вы сообщили Бекки, что вам пора. Она осталась явно неудовлетворенной."
                    if GrupenSex.get("eddie", 0) > 0:
                        "Уже в дверях вы услышали, как вдова тянет сына к себе поближе."
                        $ _ibs_call_label_or_fn("PregnancyCheck", GirlNameIBS, "inside", 1, "eddie")
                    $ _ibs_call_label_or_fn("SlutFriendsIncrease", GirlNameIBS, 3, 1, -1, 0, 0, 0)
                else:
                    "Вы поцеловали удовлетворенную Бекки, поблагодарили ее и собрались домой."
                    $ _ibs_call_label_or_fn("SlutFriendsIncrease", GirlNameIBS, 16, 2, 1, 42, 1, 1)

                $ Arousal["You"] = 0
                $ Arousal[GirlNameIBS] = 0
                python:
                    _ibs_end_cock_state()
                $ BeckyVar["visitedhome"] = max(BeckyVar.get("visitedhome", 0), 2)
                $ _ibs_call_label_or_fn("DressUp", GirlNameIBS)
                $ SomebodyCums = 0
                $ calendar_advance_slots(1)
                python:
                    _returned_to_room = _ibs_return_to_location_after_sex(GirlLocIBS)
                if _returned_to_room:
                    return
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
                python:
                    _returned_to_room = _ibs_return_to_location_after_sex(GirlLocIBS)
                if _returned_to_room:
                    return
                return


label int_becky_sex(girl_name="becky"):
    call IntBeckySex(girl_name)
    return
