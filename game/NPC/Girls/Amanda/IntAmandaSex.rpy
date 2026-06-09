# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _ias_set_arousal(who, value):
        value = min(100, max(0, int(value or 0)))
        if str(who or "").lower() == "you":
            Arousal["You"] = value
            Arousal["you"] = value
            return
        Arousal[who] = value

    def _ias_inc_arousal(who, amount):
        if str(who or "").lower() == "you":
            _ias_set_arousal("You", int(Arousal.get("You", 0) or 0) + int(amount or 0))
            return
        Arousal[who] = min(100, max(0, int(Arousal.get(who, 0) or 0) + int(amount or 0)))

    def _ias_get_sex_num(*args):
        try:
            return int(GetSexNum(*args) or 0)
        except Exception:
            return 0

label IntAmandaSex(GirlNameASDS="amanda", GirlLocASDS="home", GirlModeASDS=""):
    hide screen main_ui
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
        CurGiveOrgasms = GiveOrgasms.get(GirlNameASDS, 0)
        LickPussy.setdefault(GirlNameASDS, 0)
        Friends.setdefault(GirlNameASDS, 0)
        EddieCockInPussy.setdefault(GirlNameASDS, 0)
        SomebodyCums = int(SomebodyCums or 0)
        check_visibility(GirlNameASDS)
    call ShowAmandaPortrait

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
                if DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) >= 4 or topraised.get(GirlNameASDS, 0):
                    "Хотя Амандина блузка и так не скрывала почти ничего, вы решили ее полностью снять. Расстегнув последние крючки и застежки, вы стянули этот явно лишний предмет."
                    if bra.get(GirlNameASDS, "") == "":
                        "Так вы обнажили ее до пояса."
                    else:
                        "И теперь на ней оставался лишь лиф."
                else:
                    "На ваш нескромный взгляд, тело [RealName2.get(GirlNameASDS, GirlNameASDS)] было слишком закутано. Решив помочь Аманде почувствовать себя открытой и свободной, вы с энтузиазмом взялись за дело, смело вступив в битву с многочисленными крючками и застежками, скрепляющими верхнюю часть платья вместе."
                    if bra.get(GirlNameASDS, "") == "":
                        "Победа над ними принесла вам приятное открытие: ваша маленькая проказница не надела лиф! Ее маленькие острые грудки доступны вашим нескромным взорам и не только им."
                    else:
                        "И вот наконец победа близка: от вожделенных сисечек вас отделяет только лиф!"
                if DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) < 4 and topraised.get(GirlNameASDS, 0) == 0 and pregnancy.get(GirlNameASDS, 0) >= 120:
                    "Также, после избавления от блузки, стал хорошо заметен округлившийся животик [RealName2.get(GirlNameASDS, GirlNameASDS)]."
                $ topdress[GirlNameASDS] = ""
                $ topraised[GirlNameASDS] = 0
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Растегнуть блузку" if topdress.get(GirlNameASDS, "") != "" and topraised.get(GirlNameASDS, 0) == 0 and SomebodyCums == 0 and GirlModeASDS != "minet":
                if bra.get(GirlNameASDS, "") == "":
                    if DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) >= 4:
                        "Вы начали поглаживать и сжимать грудки [RealName2.get(GirlNameASDS, GirlNameASDS)] сквозь одежду, вызвав несколько сдержанных стонов у девушки. Дабы облегчить себе доступ к ним, вы начали расстегивать ее блузку и вскоре преуспели в этом, тем более что под ней не оказалось лифа. Теперь сисечки [RealName2.get(GirlNameASDS, GirlNameASDS)] с задорно торчащими сосками на свободе, блузка расстегнута до пупа."
                    else:
                        "Ваша скромница оделась уж как-то слишком консервативно. Непорядок. Вы начали расстегивать явно стесняющую ее блузку и не прогадали: под скромной с виду одеждой не оказалось лифчика и ее маленькие сисечки оказались полностью в вашем распоряжении."
                else:
                    if DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) >= 4:
                        "Вы начали поглаживать и сжимать грудки [RealName2.get(GirlNameASDS, GirlNameASDS)] сквозь одежду, вызвав несколько сдержанных стонов у девушки. Дабы облегчить себе доступ к ним, вы начали расстегивать ее блузку и вскоре преуспели в этом, хотя между вами и ее грудями все еще остается лифчик."
                    else:
                        "Ваша скромница оделась уж как-то слишком консервативно. Непорядок. Вы начали расстегивать явно стесняющую ее блузку, не встречая никаких возражений со стороны [RealName2.get(GirlNameASDS, GirlNameASDS)]. Как и следовало ожидать, под ней оказался лиф, последнее препятствие, лежащее между вами и ее грудями."
                if DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) < 4 and pregnancy.get(GirlNameASDS, 0) >= 120:
                    "Распахнутая блузка также теперь не мешает вам лицезреть округлившийся животик [RealName2.get(GirlNameASDS, GirlNameASDS)]."
                $ topraised[GirlNameASDS] = 1
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Снять лифчик" if bra.get(GirlNameASDS, "") != "" and (topdress.get(GirlNameASDS, "") == "" or topraised.get(GirlNameASDS, 0)) and SomebodyCums == 0 and GirlModeASDS != "minet":
                if topdress.get(GirlNameASDS, "") == "":
                    "Выше пояса на [RealName3.get(GirlNameASDS, GirlNameASDS)] теперь остается лишь лифчик. Поцеловав и обняв Аманду, вы запустили руки ей за спину и начали его на ощупь расстегивать."
                else:
                    "Хоть блузка и распахнута настежь, но между вами и сиськами еще остается лифчик. Засунув руки под ткань блузки, вы начинаете расстегивать его на ощупь."
                if (HadSex.get("You", 0) >= 8 and topdress.get(GirlNameASDS, "") == "") or HadSex.get("You", 0) >= 16:
                    "С легкостью справившись с застежками и завязками, вы отбрасываете лиф прочь, обнажив маленькие упругие груди."
                else:
                    "Вы провозились с бесчисленными застежками и завязками довольно долго, не смотря на подаваемые без конца советы Аманды. И вот наконец лифчик снят, сиськи [RealName2.get(GirlNameASDS, GirlNameASDS)] на вашем обозрении."
                $ bra[GirlNameASDS] = ""
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Поднять подол" if bottomdress.get(GirlNameASDS, "") != "" and bottomraised.get(GirlNameASDS, 0) == 0 and SomebodyCums == 0 and GirlModeASDS != "minet":
                if DressPartSlut.get(bottomdress.get(GirlNameASDS, ""), 0) >= 4:
                    if panties.get(GirlNameASDS, "") != "":
                        "Вы впились жарким поцелуем в губы [RealName2.get(GirlNameASDS, GirlNameASDS)]. Ну а затем задрали и без того короткую юбочку Аманды до пояса, выставив ее панталончики на ваше обозрение."
                    elif pantiesdef.get(GirlNameASDS, "") == "":
                        "\"А что, [RealName.get(GirlNameASDS, GirlNameASDS)],\" — спросили вы, — \"юбчишку ты носишь коротенькую, небось под ней и нижнего белья-то нет?\""
                        "\"Угадал,\" — игриво ответила вам [RealName.get(GirlNameASDS, GirlNameASDS)] и заткнула за пояс подол своей юбки, показывая, что под ним и правда ничего не было."
                    else:
                        "Вы впились жарким поцелуем в губы [RealName2.get(GirlNameASDS, GirlNameASDS)]. Ну а затем задрали и без того короткую юбочку Аманды до пояса, выставив ее голенькую щелку на свое обозрение."
                else:
                    if panties.get(GirlNameASDS, "") != "":
                        "Вы впились жарким поцелуем в губы [RealName2.get(GirlNameASDS, GirlNameASDS)]. Ну а затем оборочка за оборочкой подняли длинный подол ее платья и завернули его за пояс, выставляя Амандины панталончики на ваше обозрение."
                    elif pantiesdef.get(GirlNameASDS, "") == "":
                        "\"А что, [RealName.get(GirlNameASDS, GirlNameASDS)],\" — скептически спросили вы, — \"юбка у тебя почти до пят, раз ты такая скромница, то небось под ней у тебя еще несколько юбок и уж затем панталончики?\""
                        "\"А вот и не угадал,\" — ответила вам Аманда слегка покраснев. \"Под ней у меня вообще ничего нет. Смотри!\" И она сноровисто приподняла и заткнула за пояс длинный подол своего платья. Вы были приятно удивлены, не обнаружив под ним и следов нижнего белья."
                    else:
                        "Вы впились жарким поцелуем в губы [RealName2.get(GirlNameASDS, GirlNameASDS)]. Ну а затем оборочка за оборочкой подняли длинный подол ее платья и завернули его за пояс, выставив голенькую щелку Аманды на свое обозрение."
                $ bottomraised[GirlNameASDS] = 1
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Снять платье" if bottomdress.get(GirlNameASDS, "") != "" and SomebodyCums == 0 and GirlModeASDS != "minet":
                if bottomraised.get(GirlNameASDS, 0):
                    "Решив, что задранного подола вам мало, вы развязали на [RealName3.get(GirlNameASDS, GirlNameASDS)] поясок и несколько завязочек и наконец окончательно стянули с нее платье."
                else:
                    if panties.get(GirlNameASDS, "") != "":
                        "Вы поцеловали [RealName2.get(GirlNameASDS, GirlNameASDS)] в губы, а затем развязали поясок, и юбка упала к ногам Аманды, выставив ее кружевные панталончики на ваше обозрение."
                    elif pantiesdef.get(GirlNameASDS, "") == "":
                        "\"[RealName.get(GirlNameASDS, GirlNameASDS)], мне кажется что ты будешь куда лучше выглядеть в одних панталонах,\" — нагло заявили вы. — \"А ты как считаешь? Давай заценим!\""
                        "\"Не знаю,\" — ответила вам Аманда слегка покраснев. \"Я ведь под платьем совсем голенькая. Смотри!\" И она сноровисто распустила завязки на платье, которое незамедлительно упало к ее ногам. Вы были приятно удивлены, воочию убедившись в том, что она сказала чистую правду."
                    else:
                        "Вы поцеловали [RealName2.get(GirlNameASDS, GirlNameASDS)] в губы, а затем развязали поясок, и юбка упала к ее ногам, выставив ее голенькую щелку на ваше обозрение."
                $ bottomdress[GirlNameASDS] = ""
                $ bottomraised[GirlNameASDS] = 0
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Снять панталончики" if panties.get(GirlNameASDS, "") != "" and SomebodyCums == 0 and GirlModeASDS != "minet":
                if bottomraised.get(GirlNameASDS, 0) == 0 and bottomdress.get(GirlNameASDS, "") != "" and DressPartSlut.get(bottomdress.get(GirlNameASDS, ""), 0) >= 4:
                    "Вы засунули свои шаловливые ручки под короткую юбчонку Аманды и стащили с нее панталончики."
                elif bottomraised.get(GirlNameASDS, 0) == 0 and bottomdress.get(GirlNameASDS, "") != "":
                    "Вы присели перед Амандой на колени, залезли под длинный подол ее платья и медленно повели свои руки вверх. [RealName.get(GirlNameASDS, GirlNameASDS)] захихикала, видно ей было немного щекотно. Наконец вы нащупали панталоны и спустили их вниз. [RealName.get(GirlNameASDS, GirlNameASDS)] переступила через них, но длинный подол опять скрыл ее прелести."
                else:
                    "Вы решаете избавиться от последнего препятствия, отделяющего вас от ее пещерки. Не теряя времени, вы аккуратно стягиваете с нее панталончики. Досадная помеха убрана, киска [RealName2.get(GirlNameASDS, GirlNameASDS)] беззащитна перед вами."
                $ panties[GirlNameASDS] = ""
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Вытереть сперму с лица" if (CumFaceYou.get(GirlNameASDS, 0) or CumFaceOthers.get(GirlNameASDS, 0)) and SomebodyCums == 0:
                "Вы попросили Аманду убрать с лица свидетельства ее половой жизни. [RealName.get(GirlNameASDS, GirlNameASDS)] покраснела, достала платочек и вытерла лицо и волосы от спермы."
                $ CumFaceYou[GirlNameASDS] = 0
                $ CumFaceOthers[GirlNameASDS] = 0
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Вытереть сперму с грудей" if (CumTitsYou.get(GirlNameASDS, 0) or CumTitsOthers.get(GirlNameASDS, 0)) and TitsVisible.get(GirlNameASDS, 0) and SomebodyCums == 0:
                "Вы попросили Аманду убрать свидетельства ее половой жизни с сисек. [RealName.get(GirlNameASDS, GirlNameASDS)] достала платочек и, улыбаясь чуть стыдливо, вытерла сперму со своих маленьких грудок."
                $ CumTitsYou[GirlNameASDS] = 0
                $ CumTitsOthers[GirlNameASDS] = 0
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Вытереть сперму с бедер" if (CumInsideYou.get(GirlNameASDS, 0) or CumInsideOthers.get(GirlNameASDS, 0)) and PussyVisible.get(GirlNameASDS, 0) and SomebodyCums == 0:
                "\"[RealName.get(GirlNameASDS, GirlNameASDS)]\", сказали вы, \"прибери пожалуйста свою делянку. Чтобы не так очевидно было то, что ее недавно засеяли.\" Та рассмеялась, достала платочек и, чуть виновато посматривая на вас, вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                $ CumInsideYou[GirlNameASDS] = 0
                $ CumInsideOthers[GirlNameASDS] = 0
                $ check_visibility(GirlNameASDS)
                call ShowAmandaPortrait
                jump int_amanda_sex_menu

            "Целовать" if SomebodyCums == 0:
                "[RealName.get(GirlNameASDS, GirlNameASDS)] прижимается к вам всем телом и со всей страстью молодости целует вас отнюдь не семейным поцелуем."
                if CumFaceYou.get(GirlNameASDS, 0) > 0:
                    "На язык вам попадают капли вашего семени, которым вы обкончали девушку раньше."
                elif CumFaceOthers.get(GirlNameASDS, 0) > 0:
                    "Вы чувствуете солоноватый привкус чужой спермы. Похоже, Аманда уже успела сегодня у кого-то отсосать!"
                $ _ias_inc_arousal(GirlNameASDS, 14)
                if int(Arousal.get("You", 0) or 0) < 50:
                    $ _ias_inc_arousal("You", 9)
                call ShowCurrentSex(GirlNameASDS)
                if GirlLocASDS != "street":
                    if TitsVisible.get(GirlNameASDS, 0) and PussyVisible.get(GirlNameASDS, 0):
                        call ShowImage(GirlNameASDS, "sexroom", "kissnaked")
                    else:
                        call ShowImage(GirlNameASDS, "sexroom", "kiss")
                jump int_amanda_sex_menu

            "Лапать" if SomebodyCums == 0:
                if TitsVisible.get(GirlNameASDS, 0) == 0:
                    if DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) == 3 and bra.get(GirlNameASDS, "") == "":
                        "Вы начали поглаживать маленькую грудь [RealName2.get(GirlNameASDS, GirlNameASDS)] через тонкую ткань ее блузки."
                    elif DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) >= 4 and bra.get(GirlNameASDS, "") == "":
                        "Ваши руки забрались под декольте Аманды и, не обнаружив там лифчика, начали гладить ее небольшие груди и теребить напрягшиеся сосочки."
                    elif DressPartSlut.get(topdress.get(GirlNameASDS, ""), 0) >= 4 and bra.get(GirlNameASDS, "") != "":
                        "Ваши руки забрались под декольте [RealName2.get(GirlNameASDS, GirlNameASDS)] и начали мять ее сисечки через лифчик."
                    else:
                        "Скромное одеяние девушки не отвратило вас от пошлых мыслей, вы начали гладить и мять маленькие сисечки [RealName2.get(GirlNameASDS, GirlNameASDS)] и через него."
                else:
                    if CumTitsYou.get(GirlNameASDS, 0) > 0:
                        "Вы припали к маленьким грудям [RealName2.get(GirlNameASDS, GirlNameASDS)], благо они помещались у вас во рту почти целиком. На языке вы почувствовали солоноватый привкус своей спермы."
                    elif CumTitsOthers.get(GirlNameASDS, 0) > 0:
                        "Вы припали к маленьким грудям [RealName2.get(GirlNameASDS, GirlNameASDS)], благо они помещались у вас во рту почти целиком. На языке вы почувствовали солоноватый привкус чьей-то спермы."
                    else:
                        "Вы припали к маленьким грудям [RealName2.get(GirlNameASDS, GirlNameASDS)], благо они помещались у вас во рту почти целиком."

                if PussyVisible.get(GirlNameASDS, 0) == 1:
                    "Вы медленно опустили руку вниз, к вульве Аманды. Она вздрогнула от вашего прикосновения. На этом вы не остановились, запустив пару пальцев внутрь текущей девушки."
                else:
                    if bottomraised.get(GirlNameASDS, 0) == 0 and bottomdress.get(GirlNameASDS, "") != "":
                        if DressPartSlut.get(bottomdress.get(GirlNameASDS, ""), 0) >= 4:
                            if panties.get(GirlNameASDS, "") != "":
                                "Вы сунули руку под короткую юбчонку Аманды и начали натирать ее киску сквозь панталончики."
                            else:
                                "Вы сунули руку под короткую юбчонку Аманды и пролезли ловким пальчиком в ее не стесненную нижним бельем киску."
                        else:
                            if panties.get(GirlNameASDS, "") != "":
                                "Вы наклонились дабы залезть шаловливыми ручонками под длинную юбку Аманды. На этом вы не остановились, а стали потихоньку двигаться наверх, к заветному месту и начали натирать ее киску сквозь панталончики."
                            else:
                                "Вы наклонились дабы залезть шаловливыми ручонками под длинную юбку Аманды. На этом вы не остановились, а стали потихоньку двигаться наверх, к заветному месту и пролезли ловким пальчиком в ее не стесненную нижним бельем киску."
                    else:
                        "Вы начали натирать киску Аманды сквозь панталончики."
                if panties.get(GirlNameASDS, "") == "":
                    if CumInsideYou.get(GirlNameASDS, 0) > 0:
                        "Вдруг вы почувствовали свою сперму в пещерке [RealName2.get(GirlNameASDS, GirlNameASDS)]."
                    elif CumInsideOthers.get(GirlNameASDS, 0) > 0:
                        "Ваши пальцы легко заскользили по пещерке [RealName2.get(GirlNameASDS, GirlNameASDS)]: похоже кто-то уже кончил в нее."
                $ _ias_inc_arousal(GirlNameASDS, 12)
                call ShowCurrentSex(GirlNameASDS)
                if GirlLocASDS != "street":
                    if TitsVisible.get(GirlNameASDS, 0) and PussyVisible.get(GirlNameASDS, 0):
                        call ShowImage(GirlNameASDS, "sexroom", "grope2")
                    elif PussyVisible.get(GirlNameASDS, 0):
                        call ShowImage(GirlNameASDS, "sexroom", "grope1")
                jump int_amanda_sex_menu

            "Лизать киску" if PussyVisible.get(GirlNameASDS, 0) and SomebodyCums == 0 and GirlModeASDS != "minet":
                "Вы пролезли между раздвинутых ножек [RealName2.get(GirlNameASDS, GirlNameASDS)] и начали делать Аманде куни. Это пришлось ей по душе и по кое-чему еще. [RealName.get(GirlNameASDS, GirlNameASDS)] откинулась назад и сладко стонет от ваших ласк."
                if CumInsideYou.get(GirlNameASDS, 0) > 0:
                    "Ну а вы ощущаете привкус собственной спермы, медленно вытекающей из ее влагалища."
                elif CumInsideOthers.get(GirlNameASDS, 0) > 0:
                    "Ну а вы ощущаете привкус чьей-то спермы, медленно вытекающей из ее влагалища. Похоже, Аманда уже успела сегодня кому-то дать."
                $ LickPussy[GirlNameASDS] += 1
                if LickPussy.get(GirlNameASDS, 0) == 6:
                    "\"Стефанчик, приятно-то как!\", смеясь говорит [RealName.get(GirlNameASDS, GirlNameASDS)], \"где это с кем это ты так научился? Впрочем не важно, эх, приятно-то как!\""
                    $ Friends[GirlNameASDS] = Friends.get(GirlNameASDS, 0) + 1
                $ _ias_inc_arousal(GirlNameASDS, 25)
                call ShowCurrentSex(GirlNameASDS)
                if GirlLocASDS != "street":
                    call ShowImage(GirlNameASDS, "sexroom", "cuni")
                jump int_amanda_sex_menu

            "Минет" if _cametoday < _cancumdaily and SomebodyCums == 0:
                if GirlLocASDS == "street":
                    if CockInMouth.get(GirlNameASDS, 0):
                        "[RealName.get(GirlNameASDS, GirlNameASDS)], не забывая посматривать по сторонам, продолжает."
                    else:
                        "Вы расстегнули штаны. [RealName.get(GirlNameASDS, GirlNameASDS)] метнула взгляд к выходу из переулка, убедилась что никого нет, опустилась перед вами на коленки и стала."
                else:
                    if CockInMouth.get(GirlNameASDS, 0):
                        "Вы расселись на кровати и ловите кайф, в то время как [RealName.get(GirlNameASDS, GirlNameASDS)] стоит перед вами на коленях и продолжает."
                    else:
                        "Вы уселись поудобней на кровати и расстегнули штаны. Умненькая [RealName.get(GirlNameASDS, GirlNameASDS)] сразу поняла что от нее требуется. Сестричка слезла с кровати, опустилась на колени и стала."
                if Arousal.get("You", 0) < 20:
                    "Облизывать ваш вялый член."
                elif Arousal.get("You", 0) < 40:
                    "Облизывать головку вашего напрягшегося члена."
                elif sluttiness.get(GirlNameASDS, 0) < 40:
                    "Неумело, но с энтузиазмом сосать ваш член."
                elif Arousal.get("You", 0) < 60:
                    "Умело сосать ваш член."
                else:
                    "Заглатывать ваш член по самые яйца."
                $ CockInMouth[GirlNameASDS] = 1
                $ CockInPussy[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                if sluttiness.get(GirlNameASDS, 0) < 40:
                    $ _ias_inc_arousal("You", 18)
                else:
                    $ _ias_inc_arousal("You", 22)
                $ AmandaVar["suckyou"] = 1
                call ShowCurrentSex(GirlNameASDS)
                if GirlLocASDS == "street":
                    if Arousal.get("You", 0) < 20:
                        call ShowImage(GirlNameASDS, "sexafterdance", "minet1")
                    elif Arousal.get("You", 0) < 40:
                        call ShowImage(GirlNameASDS, "sexafterdance", "minet2")
                    elif sluttiness.get(GirlNameASDS, 0) < 40:
                        call ShowImage(GirlNameASDS, "sexafterdance", "minet3")
                    elif Arousal.get("You", 0) < 60:
                        call ShowImage(GirlNameASDS, "sexafterdance", "minet4")
                    else:
                        call ShowImage(GirlNameASDS, "sexafterdance", "minet5")
                else:
                    call ShowImageSeq(GirlNameASDS, "sexroom", "minet", 12)
                jump int_amanda_sex_menu

            "Трахать" if _cametoday < _cancumdaily and SomebodyCums == 0 and Arousal.get("You", 0) >= 20 and Arousal.get(GirlNameASDS, 0) >= 20 and PussyVisible.get(GirlNameASDS, 0) and EddieCockInPussy.get(GirlNameASDS, 0) == 0 and GirlModeASDS != "minet":
                $ _was_fucking_amanda = int(CockInPussy.get(GirlNameASDS, 0) or 0)
                if GirlLocASDS == "street":
                    if pregnancy.get(GirlNameASDS, 0) < 130:
                        if _was_fucking_amanda == 0:
                            "Вы посмотрели Аманде прямо в глаза и, убедившись что она вас поняла, перевели взгляд на своего стоящего колом дружка. Как загипнотизированная [RealName.get(GirlNameASDS, GirlNameASDS)] последовала своим взглядом за вашим. Решив что медлить дальше не имеет смысла, вы притянули девушку к себе, крепко ее поцеловав, а затем подхватили ее и насадили прямо на свой член. [RealName.get(GirlNameASDS, GirlNameASDS)] слегка охнула, обхватила вас за шею и сжала ногами."
                        else:
                            "Вы стоите в переулке и сношаете на весу свою блудливую любовницу. Слава Ильматеру, она стройная и легкая, тростиночка ваша. И вы, и она, время от времени оглядываетесь по сторонам, но, к вашему счастью, никто сюда не идет. Впрочем, даже если кто вас и засечет, уличным трахом в Коитополисе никого не удивить. Ваша поза позволяет загонять вам свой член в тесное влагалище Аманды по самые яйца, почти доставая до матки."
                    else:
                        if _was_fucking_amanda == 0:
                            "На ваше счастье в подворотне нашлась какая-то тележка, типа той на которой в ваш трактир привозили заказы. Быстро сориентировавшись в обстановке вы уложили свою залетную красотку на эту телегу пузом вверх и, закинув ее ножки себе на плечи, начали сношать девицу. Впрочем [RealName.get(GirlNameASDS, GirlNameASDS)] быстро устала держать ноги на весу и вам пришлось поменять позу, дав Аманде встать и прислониться к пресловутой тележке."
                        else:
                            "Маленький переулок стал весьма шумным местом - ваша беременная подруга стоит облокотившись на какую-то телегу, а вы трахаете ее сзади. [RealName.get(GirlNameASDS, GirlNameASDS)] уже не сдерживает стоны, но вроде пока к вам никто еще не заглянул."
                            if pregnancy.get(GirlNameASDS, 0) > 120:
                                "Вы чувствуете как ребенок в животике у маленькой [RealName2.get(GirlNameASDS, GirlNameASDS)] двигается каждый раз когда ваш член входит в нее."
                else:
                    if _was_fucking_amanda == 0:
                        "Бесстыжая [RealName.get(GirlNameASDS, GirlNameASDS)] откинулась на кровати, задрав ножки и открыв свою киску вашим нескромным взглядам. Решив не пренебрегать таким приглашением вы нацелили свой член на вход в ее пещерку. Найдя заветную дырочку вы легко проскользнули в мокренькую Аманду."
                    else:
                        "Вы имеете свою не слишком целомудренную любовницу на ее собственной кровати. Ее ножки красиво обрамляют ваши плечи, а удобная поза позволяет вам загонять свой член в нее по самые яйца."
                        if pregnancy.get(GirlNameASDS, 0) > 120:
                            "Руками вы то теребите [RealName3.get(GirlNameASDS, GirlNameASDS)] клитор, то поглаживаете пузатый живот который та себе нагуляла."
                        else:
                            "Руками вы то теребите [RealName3.get(GirlNameASDS, GirlNameASDS)] клитор, то ласкаете ее груди."
                $ CockInPussy[GirlNameASDS] = 1
                $ CockInMouth[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                $ _ias_inc_arousal("You", 25)
                $ _ias_inc_arousal(GirlNameASDS, 20)
                $ AmandaVar["fuckyou"] = 1
                if AmandaVar.get("knownotvirgin", 0) == 0 and virginity.get(GirlNameASDS, 1) == 0:
                    "Кстати, вы легко и без препятствий вошли в Аманду. Похоже, она уже не девочка. Может стоит потом ее об этом расспросить."
                    $ AmandaVar["knownotvirgin"] = 1
                if virginity.get(GirlNameASDS, 1):
                    $ virginity[GirlNameASDS] = 0
                    $ AmandaVar["knownotvirgin"] = 1
                call ShowCurrentSex(GirlNameASDS)
                if GirlLocASDS == "street":
                    if pregnancy.get(GirlNameASDS, 0) < 130:
                        $ _amanda_street_fuck_pic = "fuck" + str(renpy.random.randint(1, 4))
                        call ShowImage(GirlNameASDS, "sexafterdance", _amanda_street_fuck_pic)
                    else:
                        if _was_fucking_amanda == 0:
                            call ShowImage(GirlNameASDS, "sexafterdance", "fuckarba1")
                        else:
                            call ShowImage(GirlNameASDS, "sexafterdance", "fuckarba2")
                else:
                    if _was_fucking_amanda == 1:
                        $ _amanda_room_fuck_pic = "fuck" + str(renpy.random.randint(1, 6))
                        call ShowImage(GirlNameASDS, "sexroom", _amanda_room_fuck_pic)
                    else:
                        call ShowImage(GirlNameASDS, "sexroom", "fuckstart")
                jump int_amanda_sex_menu

            "Кончить в ротик" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and (CockInMouth.get(GirlNameASDS, 0) or CockInTits.get(GirlNameASDS, 0)):
                "Вы кончили, заливая горло и рот [RealName2.get(GirlNameASDS, GirlNameASDS)] своей спермой. Девушка не сделала ни малейшей попытки отстраниться и начала жадно глотать ваше семя. Его было много, она не успела сглотнуть все, и вязкая белая жидкость потекла из уголков ее очаровательного ротика. [RealName.get(GirlNameASDS, GirlNameASDS)] выпустила ваш обмякший член из сладкого плена, облизала губы и, с томной улыбкой сказала: надеюсь тебе понравилось. Вы поспешили заверить девушку что вам очень и очень понравилось."
                $ _ias_set_arousal("You", 0)
                $ _aah_pregnancy_check(GirlNameASDS, "mouth", 1, "Вы")
                $ CockInMouth[GirlNameASDS] = 0
                $ CockInPussy[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumFaceYou[GirlNameASDS] = 1
                call ShowCurrentSex(GirlNameASDS)
                if GirlLocASDS == "street":
                    call ShowImage(GirlNameASDS, "sexafterdance", "cumface")
                else:
                    call ShowImageSeq(GirlNameASDS, "sexroom", "come", 2)
                jump int_amanda_sex_after_cum

            "Кончить на лицо" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100:
                "Перед самым оргазмом"
                if CockInMouth.get(GirlNameASDS, 0):
                    "вы вытащили член изо рта Аманды и кончили ей на мордашку."
                elif CockInPussy.get(GirlNameASDS, 0):
                    "колоссальным усилием воли вы вынули член из киски Аманды и направили его на ее смазливую мордашку."
                else:
                    "вы направили свой член на ее смазливую мордашку."
                "Густая белая струя брызнула прямо [RealName3.get(GirlNameASDS, GirlNameASDS)] в лицо. Крупные белые капли потекли по ее щечкам и подбородку, одна струйка попала ей в левый глаз, отчего она зажмурилась, а пара капель осталась в ее белокурых локонах. Очень романтично!"
                $ _ias_set_arousal("You", 0)
                $ _aah_pregnancy_check(GirlNameASDS, "face", 1, "Вы")
                $ CockInMouth[GirlNameASDS] = 0
                $ CockInPussy[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumFaceYou[GirlNameASDS] = 1
                call ShowCurrentSex(GirlNameASDS)
                if GirlLocASDS == "street":
                    call ShowImage(GirlNameASDS, "sexafterdance", "cumface")
                else:
                    call ShowImage(GirlNameASDS, "sexroom", "comeface")
                jump int_amanda_sex_after_cum

            "Кончить на груди" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and TitsVisible.get(GirlNameASDS, 0) and GirlModeASDS != "minet":
                "Почувствовав наступление оргазма"
                if CockInMouth.get(GirlNameASDS, 0):
                    "вы вытащили член изо рта Аманды и нацелили его на маленькие сисечки."
                elif CockInPussy.get(GirlNameASDS, 0):
                    "колоссальным усилием воли вы вынули член из киски Аманды и направили его на маленькие сисечки."
                else:
                    "вы решили обкончать ее маленькие сисечки."
                "Сказано - сделано! Двумя точными струями вы заляпали оба шарика своим семенем."
                $ _ias_set_arousal("You", 0)
                $ _aah_pregnancy_check(GirlNameASDS, "tits", 1, "Вы")
                $ CockInMouth[GirlNameASDS] = 0
                $ CockInPussy[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumTitsYou[GirlNameASDS] = 1
                call ShowCurrentSex(GirlNameASDS)
                jump int_amanda_sex_after_cum

            "Кончить в Аманду" if _cametoday < _cancumdaily and Arousal.get("You", 0) >= 100 and CockInPussy.get(GirlNameASDS, 0) and GirlModeASDS != "minet":
                $ tmpCumInside = _ias_get_sex_num("amanda", "you", "inside")
                if pregnancy.get(GirlNameASDS, 0) < 120 and sluttiness.get(GirlNameASDS, 0) < 60:
                    "Вы не особо-то прислушались к просьбе Аманды и даже не попытались вовремя вытащить. Почувствовав что ее заполняет ваше семя, Аманда попробовала оттолкнуть вас, но все было без толку: пока вы не заполнили ее киску своей спермой - члена вы не вытащили. [RealName.get(GirlNameASDS, GirlNameASDS)] с ужасом посмотрела на белую струйку, вытекающую из нее."
                    if tmpCumInside == 0 and int(cuminside.get("amanda", 0) or 0) >= 2:
                        "\"Эх, и ты тоже такой же как все, кончаешь внутрь, а о последствиях и не думаешь,\" несколько туманно заметила Аманда."
                    elif tmpCumInside > 4:
                        "\"Да сколько раз тебе говорить, чтобы в меня не кончал!\" сердито воскликнула [RealName.get(GirlNameASDS, GirlNameASDS)]. \"Вот доиграемся до детей и что тогда? Только тебе это все как об стенку горох! Мог бы хоть разок не о себе, а обо мне подумать!\""
                    else:
                        "\"Стефан, ты чего, оглох? Я тебе сказала вытащить. А теперь что делать? А если я залечу? Чтобы это в последний раз было!\" строго отчитала вас девушка."
                    if GirlLocASDS != "street":
                        call ShowImage(GirlNameASDS, "sexroom", "cumpussyangry")
                elif pregnancy.get(GirlNameASDS, 0) >= 120:
                    "Рассудив про себя что более беременной чем она есть уже не станет, вы спустили прямо в нее. Судя по всему [RealName.get(GirlNameASDS, GirlNameASDS)] разделяла ваше мнение, так как почувствовав в себе ваше горячее семя она лишь улыбнулась и сказала: \"Смотри не утопи моего маленького!\""
                    if GirlLocASDS != "street":
                        $ _amanda_cumpussy_pic = "cumpussy" + str(renpy.random.randint(1, 2))
                        call ShowImage(GirlNameASDS, "sexroom", _amanda_cumpussy_pic)
                else:
                    "Решив не утруждать себя вы не стали вытаскивать а кончили прямо в тесную киску [RealName2.get(GirlNameASDS, GirlNameASDS)]."
                    "\"Ох ты,\" игриво заметила Аманда. \"Ты и в самом деле пытаешься меня обрюхатить! Посмотри, сколько ты накончал!\""
                    "С этими словами Аманда раздвинула ножки, предоставив вам на обозрение свою полную вашей спермы киску."
                    if GirlLocASDS != "street":
                        $ _amanda_cumpussy_pic = "cumpussy" + str(renpy.random.randint(1, 2))
                        call ShowImage(GirlNameASDS, "sexroom", _amanda_cumpussy_pic)
                $ _ias_set_arousal("You", 0)
                $ _ias_set_arousal(GirlNameASDS, int(Arousal.get(GirlNameASDS, 0) or 0) + 3)
                $ _aah_pregnancy_check(GirlNameASDS, "inside", 1, "Вы")
                $ CockInMouth[GirlNameASDS] = 0
                $ CockInPussy[GirlNameASDS] = 0
                $ CockInTits[GirlNameASDS] = 0
                $ SomebodyCums = 1
                $ CumInsideYou[GirlNameASDS] = 1
                call ShowCurrentSex(GirlNameASDS)
                jump int_amanda_sex_after_cum

            "Попрощаться и уйти" if SomebodyCums == 0 and GirlLocASDS == "home" and GirlModeASDS != "minet":
                if CurGiveOrgasms == GiveOrgasms.get(GirlNameASDS, 0):
                    "\"Ну все, пока!\" бодро сказали вы направляясь к выходу. \"Надеюсь тебе понравилось!\""
                    "\"Да ты издеваешься что ли?\" возмутилась та. \"Я же еще не кончила!\""
                    "\"Ну, если тебе это так важно, то можешь ручкой там или пальчиком. Ну, да не мне тебя учить. А лично я уже все что хотел получил. До встречи завтра!\" и с этими словами вы закрыли за собой дверь. С той стороны."
                    $ _aah_slut_friends_increase(GirlNameASDS, 3, 1, -1, 25, 1, -2)
                    call ShowImage(GirlNameASDS, "sexroom", "angry")
                elif GiveOrgasms.get(GirlNameASDS, 0) >= CurGiveOrgasms + 3:
                    "Увидев что [RealName.get(GirlNameASDS, GirlNameASDS)], измотанная серией оргазмов, усталая лежит на кровати вы решили что хорошенького понемножку и, чмокнув ее, пошли к выходу."
                    "\"Ну пока, я пошел, а то завтра тебе надо работать, да и мне надо выспаться,\" заметили вы по пути."
                    "\"Братик, это было просто нечто, дай мне отдохнуть, а завтра приходи еще!\" слабым голосом ответила вам она, слегка привстав на кровати."
                    "И вы вышли в коридор."
                    $ _aah_slut_friends_increase(GirlNameASDS, 20, 1, 1, 50, 1, 2)
                    $ _amanda_naked_pic = "naked" + str(renpy.random.randint(1, 3))
                    call ShowImage(GirlNameASDS, "sexroom", _amanda_naked_pic)
                else:
                    "[RealName.get(GirlNameASDS, GirlNameASDS)], после пережитого оргазма, тяжело дыша лежала на кровати."
                    "\"Ну пока, я пошел, а то завтра тебе надо работать, да и мне надо выспаться,\" заметили вы идя к дверям."
                    "\"Да, конечно,\" ответила вам довольная [RealName.get(GirlNameASDS, GirlNameASDS)], привстав на кровати, \"все было здорово, но теперь надо и поспать.\""
                    "И вы вышли в коридор."
                    $ _aah_slut_friends_increase(GirlNameASDS, 16, 2, 1, 42, 1, 1)
                    $ _amanda_naked_pic = "naked" + str(renpy.random.randint(1, 3))
                    call ShowImage(GirlNameASDS, "sexroom", _amanda_naked_pic)
                $ _ias_set_arousal("You", 0)
                $ _ias_set_arousal(GirlNameASDS, 0)
                $ AmandaVar["kickyoufromroom"] = 1
                $ SomebodyCums = 0
                call ShowCurrentSex(GirlNameASDS)
                call DressUp(GirlNameASDS)
                jump TavernMain

            "Привести себя в порядок и вернуться" if SomebodyCums == 0 and GirlLocASDS == "street" and GirlModeASDS != "minet":
                if CurGiveOrgasms == GiveOrgasms.get(GirlNameASDS, 0):
                    "\"Ну вот и все, идем обратно к трактиру!\" весело заявили вы, застегивая штаны."
                    "\"Как обратно? Ты разве не дашь мне кончить?\" поразилась Аманда."
                    "\"Почему не дам? Хочешь ручкой себя доведи, хочешь пальчиком, я тебе не запрещаю!\" искрометно пошутили вы, продолжая одеваться."
                    "\"Ах ты козел!\" только и смогла ответить вам Аманда, впрочем вы уже оделись и весело пошли широкой походкой к трактиру, оставив хамящую девушку в подворотне."
                    $ _aah_slut_friends_increase(GirlNameASDS, 3, 1, -2, 25, 1, -2)
                elif GiveOrgasms.get(GirlNameASDS, 0) >= CurGiveOrgasms + 3:
                    "[RealName.get(GirlNameASDS, GirlNameASDS)] от пережитых оргазмов едва стоит на ногах. Решив что хорошего должно быть в меру, вы начали одеваться сами, одновременно помогая Аманде привести себя в порядок. Одевшись, вы пошли обратно к трактиру."
                    "\"Это было просто нечто, ты самый лучший!\" сказала вам по дороге удовлетворенная Аманда. \"Ну все, пока, я в свою комнату пойду отлежаться,\" и девица упорхнула."
                    $ _aah_slut_friends_increase(GirlNameASDS, 20, 1, 1, 50, 1, 2)
                else:
                    "Что ж, [RealName.get(GirlNameASDS, GirlNameASDS)] кончила, пора и домой. Вы начали одеваться сами, одновременно помогая Аманде привести себя в порядок. Ну а затем вы пошли обратно к трактиру."
                    "У входа в него Аманда сказала вам: \"Ну все, пока, я наверное уже баиньки пойду,\" и с этими словами упорхнула."
                    $ _aah_slut_friends_increase(GirlNameASDS, 16, 2, 1, 42, 1, 1)
                $ _ias_set_arousal("You", 0)
                $ _ias_set_arousal(GirlNameASDS, 0)
                $ AmandaVar["kickyoufromroom"] = 1
                call ShowCurrentSex(GirlNameASDS)
                call DressUp(GirlNameASDS)
                $ calendar_v2.advance_minutes(60)
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
