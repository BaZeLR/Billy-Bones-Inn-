label IntAmandaSex(GirlNameASDS="amanda", GirlLocASDS="home", GirlModeASDS=""):
    python:
        topdress.setdefault(GirlNameASDS, "")
        bottomdress.setdefault(GirlNameASDS, "")
        bra.setdefault(GirlNameASDS, "")
        panties.setdefault(GirlNameASDS, "")
        topraised.setdefault(GirlNameASDS, 0)
        bottomraised.setdefault(GirlNameASDS, 0)
        TitsVisible.setdefault(GirlNameASDS, 0)
        PussyVisible.setdefault(GirlNameASDS, 0)
        CockInMouth.setdefault(GirlNameASDS, 0)
        CockInPussy.setdefault(GirlNameASDS, 0)
        CockInTits.setdefault(GirlNameASDS, 0)
        CumFaceYou.setdefault(GirlNameASDS, 0)
        CumFaceOthers.setdefault(GirlNameASDS, 0)
        CumTitsYou.setdefault(GirlNameASDS, 0)
        CumTitsOthers.setdefault(GirlNameASDS, 0)
        CumInsideYou.setdefault(GirlNameASDS, 0)
        CumInsideOthers.setdefault(GirlNameASDS, 0)
        Arousal.setdefault("You", 0)
        Arousal.setdefault(GirlNameASDS, 0)
        GiveOrgasms.setdefault(GirlNameASDS, 0)
        LickPussy.setdefault(GirlNameASDS, 0)
        Friends.setdefault(GirlNameASDS, 0)
        EddieCockInPussy.setdefault(GirlNameASDS, 0)
        SomebodyCums = int(SomebodyCums or 0)
        check_visibility(GirlNameASDS)

    label int_amanda_sex_menu:
        python:
            if isinstance(cametoday, (int, float)):
                _cametoday = cametoday
            elif isinstance(cametoday, dict):
                _cametoday = cametoday.get("You", 0)
            else:
                _cametoday = 0

            if isinstance(cancumdaily, (int, float)):
                _cancumdaily = cancumdaily
            else:
                _cancumdaily = 1

        menu:
            "Осмотреть":
                if renpy.has_label("GirlsDesc"):
                    call GirlsDesc(GirlNameASDS)
                else:
                    "[RealName.get(GirlNameASDS, GirlNameASDS)] внимательно смотрит на вас."
                jump int_amanda_sex_menu

            "Снять блузку" if topdress.get(GirlNameASDS, "") != "" and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы сняли с [RealName2.get(GirlNameASDS, GirlNameASDS)] верхнюю одежду."
                $ topdress[GirlNameASDS] = ""
                $ topraised[GirlNameASDS] = 0
                $ check_visibility(GirlNameASDS)
                jump int_amanda_sex_menu

            "Растегнуть блузку" if topdress.get(GirlNameASDS, "") != "" and topraised.get(GirlNameASDS, 0) == 0 and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы распахнули блузку сестры."
                $ topraised[GirlNameASDS] = 1
                jump int_amanda_sex_menu

            "Снять лифчик" if bra.get(GirlNameASDS, "") != "" and (topdress.get(GirlNameASDS, "") == "" or topraised.get(GirlNameASDS, 0)) and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы расстегнули и сняли лифчик."
                $ bra[GirlNameASDS] = ""
                $ check_visibility(GirlNameASDS)
                jump int_amanda_sex_menu

            "Поднять подол" if bottomdress.get(GirlNameASDS, "") != "" and bottomraised.get(GirlNameASDS, 0) == 0 and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы задрали подол, открывая обзор снизу."
                $ bottomraised[GirlNameASDS] = 1
                $ check_visibility(GirlNameASDS)
                jump int_amanda_sex_menu

            "Снять платье" if bottomdress.get(GirlNameASDS, "") != "" and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы сняли с сестры нижнюю часть одежды."
                $ bottomdress[GirlNameASDS] = ""
                $ bottomraised[GirlNameASDS] = 0
                $ check_visibility(GirlNameASDS)
                jump int_amanda_sex_menu

            "Снять панталончики" if panties.get(GirlNameASDS, "") != "" and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы аккуратно стянули панталончики."
                $ panties[GirlNameASDS] = ""
                $ check_visibility(GirlNameASDS)
                jump int_amanda_sex_menu

            "Вытереть сперму с лица" if (CumFaceYou.get(GirlNameASDS, 0) or CumFaceOthers.get(GirlNameASDS, 0)) and SomebodyCums == 0:
                "Сестра вытерла лицо и волосы от спермы."
                $ CumFaceYou[GirlNameASDS] = 0
                $ CumFaceOthers[GirlNameASDS] = 0
                jump int_amanda_sex_menu

            "Вытереть сперму с грудей" if (CumTitsYou.get(GirlNameASDS, 0) or CumTitsOthers.get(GirlNameASDS, 0)) and TitsVisible.get(GirlNameASDS, 0) and SomebodyCums == 0:
                "Сестра вытерла грудь от спермы."
                $ CumTitsYou[GirlNameASDS] = 0
                $ CumTitsOthers[GirlNameASDS] = 0
                jump int_amanda_sex_menu

            "Вытереть сперму с бедер" if (CumInsideYou.get(GirlNameASDS, 0) or CumInsideOthers.get(GirlNameASDS, 0)) and PussyVisible.get(GirlNameASDS, 0) and SomebodyCums == 0:
                "Сестра вытерла бедра и лобок."
                $ CumInsideYou[GirlNameASDS] = 0
                $ CumInsideOthers[GirlNameASDS] = 0
                jump int_amanda_sex_menu

            "Целовать" if SomebodyCums == 0:
                "[RealName.get(GirlNameASDS, GirlNameASDS)] страстно целует вас."
                $ Arousal[GirlNameASDS] = min(100, Arousal.get(GirlNameASDS, 0) + 14)
                $ Arousal["You"] = min(100, Arousal.get("You", 0) + 9)
                jump int_amanda_sex_menu

            "Лапать" if SomebodyCums == 0:
                "Вы ласкаете грудь и бедра сестры, распаляя ее еще сильнее."
                $ Arousal[GirlNameASDS] = min(100, Arousal.get(GirlNameASDS, 0) + 12)
                $ Arousal["You"] = min(100, Arousal.get("You", 0) + 8)
                jump int_amanda_sex_menu

            "Лизать киску" if PussyVisible.get(GirlNameASDS, 0) and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы опустились между ее ног и начали делать куни."
                $ LickPussy[GirlNameASDS] += 1
                $ Arousal[GirlNameASDS] = min(100, Arousal.get(GirlNameASDS, 0) + 25)
                if LickPussy.get(GirlNameASDS, 0) >= 6:
                    $ Friends[GirlNameASDS] = Friends.get(GirlNameASDS, 0) + 1
                jump int_amanda_sex_menu

            "Минет" if _cametoday < _cancumdaily and SomebodyCums == 0:
                "[RealName.get(GirlNameASDS, GirlNameASDS)] встала на колени и взяла ваш член в рот."
                $ CockInMouth[GirlNameASDS] = 1
                $ CockInPussy[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                $ Arousal["You"] = min(100, Arousal.get("You", 0) + 22)
                $ AmandaVar["suckyou"] = 1
                jump int_amanda_sex_menu

            "Трахать" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and Arousal.get(GirlNameASDS, 0) >= 20 and PussyVisible.get(GirlNameASDS, 0) and EddieCockInPussy.get(GirlNameASDS, 0) == 0 and GirlModeASDS != "minet":
                "Вы вошли в сестру и начали двигаться в такт ее стонам."
                $ CockInPussy[GirlNameASDS] = 1
                $ CockInMouth[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                $ Arousal["You"] = min(100, Arousal.get("You", 0) + 25)
                $ Arousal[GirlNameASDS] = min(100, Arousal.get(GirlNameASDS, 0) + 20)
                $ AmandaVar["fuckyou"] = 1
                $ AmandaVar["knownotvirgin"] = 1
                if virginity.get(GirlNameASDS, 1):
                    $ virginity[GirlNameASDS] = 0
                jump int_amanda_sex_menu

            "Кончить в ротик" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and (CockInMouth.get(GirlNameASDS, 0) or CockInTits.get(GirlNameASDS, 0)):
                "Вы кончили в рот сестры, и она жадно проглотила сперму."
                $ Arousal["You"] = 0
                python:
                    _aah_pregnancy_check(GirlNameASDS, "mouth", 1, "Вы")
                    CockInMouth[GirlNameASDS] = 0
                    CockInPussy[GirlNameASDS] = 0
                    CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumFaceYou[GirlNameASDS] = 1
                jump int_amanda_sex_after_cum

            "Кончить на лицо" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100:
                "В последний момент вы направили струю ей на лицо."
                $ Arousal["You"] = 0
                python:
                    _aah_pregnancy_check(GirlNameASDS, "face", 1, "Вы")
                    CockInMouth[GirlNameASDS] = 0
                    CockInPussy[GirlNameASDS] = 0
                    CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumFaceYou[GirlNameASDS] = 1
                jump int_amanda_sex_after_cum

            "Кончить на груди" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and TitsVisible.get(GirlNameASDS, 0) and GirlModeASDS != "minet":
                "Вы залили ее грудь своей спермой."
                $ Arousal["You"] = 0
                python:
                    _aah_pregnancy_check(GirlNameASDS, "tits", 1, "Вы")
                    CockInMouth[GirlNameASDS] = 0
                    CockInPussy[GirlNameASDS] = 0
                    CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumTitsYou[GirlNameASDS] = 1
                jump int_amanda_sex_after_cum

            "Кончить в сестру" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and CockInPussy.get(GirlNameASDS, 0) and GirlModeASDS != "minet":
                "Вы не стали вытаскивать и кончили прямо в нее."
                $ Arousal["You"] = 0
                $ Arousal[GirlNameASDS] = min(100, Arousal.get(GirlNameASDS, 0) + 3)
                python:
                    _aah_pregnancy_check(GirlNameASDS, "inside", 1, "Вы")
                    CockInMouth[GirlNameASDS] = 0
                    CockInPussy[GirlNameASDS] = 0
                    CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumInsideYou[GirlNameASDS] = 1
                jump int_amanda_sex_after_cum

            "Попрощаться и уйти" if SomebodyCums == 0 and GirlLocASDS == "home" and GirlModeASDS != "minet":
                "Вы попрощались с Амандой и вернулись в общий зал."
                $ Arousal["You"] = 0
                $ Arousal[GirlNameASDS] = 0
                $ AmandaVar["kickyoufromroom"] = 1
                $ SomebodyCums = 0
                jump TavernMain

            "Привести себя в порядок и вернуться" if SomebodyCums == 0 and GirlLocASDS == "street" and GirlModeASDS != "minet":
                "Вы с Амандой привели себя в порядок и вернулись к трактиру."
                $ Arousal["You"] = 0
                $ Arousal[GirlNameASDS] = 0
                $ AmandaVar["kickyoufromroom"] = 1
                $ calendar_advance_slots(1)
                $ SomebodyCums = 0
                jump TavernMain

            "Закончить":
                return

    label int_amanda_sex_after_cum:
        menu:
            "Продолжить":
                $ SomebodyCums = 0
                jump int_amanda_sex_menu

            "Закончить":
                $ SomebodyCums = 0
                return
