# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label TavernGloryHole:
    call EnterLocation("TavernGloryHole")
    if not can_enter_location("TavernGloryHole"):
        "Отдельная комната пока недоступна. Сначала закажите и оплатите постройку."
        jump TavernMain
    if navigation_only_mode_enabled():
        "Вы находитесь в отдельной комнате трактира, где расположен глорихол."
        "[navigation_only_message()]"
        "[navigation_only_time_note()]"
        menu:
            "Идти обратно в трактир":
                jump TavernMain
        return
    python:
        import random

        if not isinstance(ClientsSaw, dict):
            ClientsSaw = {}
        GirlNameTGH = get_random_girl_by_job("jobgloryhole")

        GloryHoleLook = 0
        GloryHoleCurrentStep = 0
        CockInGloryHole = 0
        GloryHoleInside = 0
        GloryHoleInsideOnce = 0
        GloryHoleWorks = 0

        GloryLine1 = ""
        GloryLine2 = ""
        GloryLine3 = ""
        GloryGirlLine0 = ""
        GloryGirlLine1 = ""
        GloryGirlLine2 = ""
        GloryGirlLine3 = ""

        BlockGloryHoleMenu = 0
        AmandaAtGlory = 0

        _time_now = time
        if _time_now in (2, 3) and GirlNameTGH != "":
            GloryHoleWorks = 1

        if GetSexEventFromTable("amanda", 99, "glorytry") > 0:
            AmandaAtGlory = 1

        GloryHoleYouLine1 = "Вы засунули свое самое дорогое в дырку. Однако с той стороны никто не поспешил вам на помощь. Вы, еще на что-то надеясь, подождали немного, но безрезультатно. Продолжать стоять дальше с засунутым в отверстие в стене членом в гнетущей тишине показалось вам глуповатым, и, со вздохом разочарования, вы убрали свое хозяйство обратно в штаны. <br>В голове у вас возникло несколько гипотез, объясняющих произошедшее. Возможно вы пришли слишком рано, а может пришли вовремя, но не назначили никого работать у глорихола. Надо провести тщательное расследование."
        GloryHoleYouLine2 = ""
        GloryHoleYouLine3 = ""

        def _set_gloryhole_inside():
            global GloryHoleInside, GloryHoleInsideOnce
            global GloryHoleYouLine1, GloryHoleYouLine2, GloryHoleYouLine3

            GloryHoleInside = 0
            GloryHoleInsideOnce = 0

            if GloryHoleWorks and AmandaAtGlory == 0 and GirlNameTGH != "":
                if sluttiness.get(GirlNameTGH, 0) >= 80:
                    if random.randint(1, 4) == 1:
                        GloryHoleInside = 1
                elif sluttiness.get(GirlNameTGH, 0) >= 50:
                    if random.randint(1, 8) == 1:
                        GloryHoleInside = 1

                if GloryHoleInside == 0 and random.randint(1, 3) == 1 and sluttiness.get(GirlNameTGH, 0) >= 40:
                    GloryHoleInsideOnce = 1

                GloryHoleYouLine1 = "Вы засунули свое самое дорогое в дырку, в пугающую неизвестность. И ваша смелость была вознагражденна: чей-то страстный язычок с другой стороны глорихола начал облизывать головку вашего члена. Вскоре незнакомка стала посасывать ваш, уже принявший полную боевую готовность, агрегат, делая вам весьма и весьма приятно."

                if GloryHoleInside or GloryHoleInsideOnce:
                    GloryHoleYouLine2 = "Только вы начали входить во вкус, как вдруг минет неожиданно прекращается. Вы с трудом сдерживаете стон разочарования, но тут же вместо ротика на ваш член насаживается что-то теплое и влажное. Вы с трудом верите в происходящее: развратная незнакомка стала трахать вас своей киской! Вы уже очень близки к оргазму."
                    if GloryHoleInside:
                        GloryHoleYouLine3 = "Влагалище вашей невидимой любовницы сжимается и из-за ширмы слышится протяжный стон - она кончила. Вы не выдерживаете и тоже кончаете прямо внутрь, заливая ее своим семенем. Хотя ваш обмякший член и выскользнул из жаркой пещерки, но это было еще не все - ловкая незнакомка развернулась у себя за ширмой и ее язычок слизал остатки спермы с вашего обмякшего члена. Удовлетворенный вы застегнули штаны."
                    else:
                        GloryHoleYouLine3 = "Вы уже собирались было кончить во влагалище вашей невидимой подружки, но плутовка как видно угадала ваше намерение и в последний момент соскользнула с вашего ствола, впрочем, быстро взяв его обратно в свой страстный ротик, в который вы и разрядились. Напоследок вам слизали остатки спермы с вашего обмякшего члена. Удовлетворенный вы застегнули штаны."
                else:
                    GloryHoleYouLine2 = "Вы продолжаете наслаждаться минетом от невидимой прелестницы, которая теперь уже заглатывает ваш член почти по самые яйца. Долго такого вы выдержать не можете, вы уже на грани, еще немного и вы кончите."
                    GloryHoleYouLine3 = "Громкий стон по ту сторону ширмы известил вас, что ваша невидимая подруга кончила, лаская себя. Вы решили последовать ее примеру и взорвались, заполняя ее ротик потоками своего семени. Вы почуствовали как чей-то ловкий язычок слизал остатки спермы с вашего обмякшего члена. Удовлетворенный вы застегнули штаны."

        if GloryHoleWorks:
            _set_gloryhole_inside()

            _real_name = RealName.get(GirlNameTGH, GirlNameTGH)
            _real_name2 = RealName2.get(GirlNameTGH, _real_name)

            GloryGirlLine0 = _real_name + " сидит за ширмой на скамеечке в ожидании клиентов. Подол юбки задран до пояса, полностью открывая киску. Панталончиков прелестница либо не носит, либо сняла как лишнее препятствие."
            if pregnancy.get(GirlNameTGH, 0) > 120:
                GloryGirlLine0 += " Над задранным подолом из под расстегнутой блузки виднеется беременное пузико " + _real_name2 + "."

            GloryGirlLine1 = _real_name + " обрадованно посмотрела на появившийся в отверстии член, наклонилась к нему, и начала облизывать и обсасывать головку члена, не забывая ласкать себя свободной рукой."

            if GloryHoleInside or GloryHoleInsideOnce:
                GloryGirlLine2 = "Вы не в силах поверить своим глазам: пососав некоторое время член, " + _real_name + " выпускает его изо рта, разворачивается, встает раком и насаживается на член прямо своей похотливой киской. И начинает страстно трахать мужика, лица которого она даже не видела!"
                if pregnancy.get(GirlNameTGH, 0) > 120:
                    GloryGirlLine2 += " Беременность ей в этом ничуть не мешает и не смущает!"
                if GloryHoleInside:
                    GloryGirlLine3 = "Без всяких мыслей о возможных последствиях, " + _real_name + " продолжает трахать член незнакомца, пока тот не разряжается ей прямо внутрь. Вслед за этим кончает и " + _real_name + ". Развернувшись, она тщательно облизывает обмякший член от остатков спермы и возвращается на свою скамеечку, довольно улыбаясь."
                else:
                    GloryGirlLine3 = "Все-таки благоразумие берет верх над страстью: чувствуя, что клиент уже близок к оргазму, " + _real_name + " соскальзывает с его члена, вызывая вздох разочарования с другой стороны ширмы, и берет член обратно в свой ротик, доводя наконец его до разрядки. С трудом проглатив потоки семени, " + _real_name + " слизывает остатки спермы с члена и возвращается на свою скамеечку, довольно улыбаясь."
            else:
                GloryGirlLine2 = "Не в силах оторваться, вы смотрите на то как член входит в ротик " + _real_name2 + ". Она распаляется все больше и больше, и вот уже заглатывает член почти по самые яйца. Одновременно она иступленно ласкает себя, доводя до уже такого близкого оргазма."
                GloryGirlLine3 = "Продолжая сосать член как огромный леденец и натирать в тоже время себе киску " + _real_name + " наконец кончает. Вскоре, прямо ей в ротик кончает и клиент. С трудом " + _real_name + " проглатывает поток семени, потом слизывает остатки с члена и возвращается на свою скамеечку, довольно улыбаясь."

            if pregnancy.get(GirlNameTGH, 0) > 120:
                GloryGirlLine3 += " и поглаживая свой беременный животик."
            else:
                GloryGirlLine3 += "."

            if CheckIfSexEventExist(GirlNameTGH, _time_now) > 0 and random.randint(1, 2) == 1 and AmandaAtGlory == 0:
                GloryHoleLook = GetSexEventFromTable(GirlNameTGH, _time_now)
                ClientsSaw[GirlNameTGH] = ClientsSaw.get(GirlNameTGH, 0) + 1

                if GloryHoleLook == 1:
                    GloryLine1 = "За занавеской вы увидели мастера Драупнира. Видимо низкая цена все-таки привлекла экономного гнома. Расстегнув штаны на помочах, мастер Драупнир извлек свой инструмент. Оный инструмент был как сам гном - очень толстый, но не очень длиный. Встав, в силу невысокого роста, на приступочку, мастер Драупнир направил свой агрегат в дырку."
                    GloryLine2 = "Мастер Драупнир наслаждается происходящим, беря максимум удовольствия за свои деньги. Пока кто-то обрабатывает член через дырку, гном блаженно улыбается."
                    GloryLine3 = "Гном вдруг замер, и судя, по всему кончил. Ну а затем он застегнул штаны и отправился восвояси."
                    PregnancyCheck(GirlNameTGH, "inside" if GloryHoleInside else "mouth", 1, "Мастер Драупнир")
                elif GloryHoleLook == 2:
                    GloryLine1 = "За занавеской вы увидели своего старого знакомца - рыжего Эдди. Немного нервничая, Эдди смело расстегивает штаны и сует свое достоинство прямо в дырку."
                    GloryLine2 = "Эдди кайфует, пока с той стороны ему делают отсос а может и кое-чего покруче."
                    GloryLine3 = "Эдди кончил и, застегнув штаны, отправился восвояси."
                    PregnancyCheck(GirlNameTGH, "inside" if GloryHoleInside else "mouth", 1, "Эдди")
                elif GloryHoleLook == 3:
                    GloryLine1 = "За занавеской вы увидели месье Легаре. Женатый, но похотливый винторговец в который уже раз решил обратиться к продажной любви. Приспустив штаны он сунул свой длинный и тонкий член прямо в дырку."
                    GloryLine2 = "Месье Легаре слегка поставнывает, пока кто-то с той стороны занимается его сокровищем."
                    GloryLine3 = "Месье Легаре извергся и, подтянув штаны, вернулся в главную залу."
                    PregnancyCheck(GirlNameTGH, "inside" if GloryHoleInside else "mouth", 1, "Месье Легаре")
                elif GloryHoleLook == 4:
                    GloryLine1 = "За занавеской вы увидели достойного отца Герхарда. Осенив глорихол знаком Ильматера, он приподнял сутану и, ничтоже сумняшись, сунул своего грешника прямо в дырку."
                    GloryLine2 = "Отец Герхард бормочет толи благословения, толи молитвы, пока с той стороны кто-то, несомненно с благославения Ильматера, пытается уложить его вставшего грешника."
                    GloryLine3 = "Отец Герхард закончил, благословил свою невидимую прихожанку, опустил сутану и отправился дальше нести слово великого Ильматера."
                    PregnancyCheck(GirlNameTGH, "inside" if GloryHoleInside else "mouth", 1, "Отец Герхард")
                elif 5 <= GloryHoleLook <= 7:
                    GloryLine1 = "За занавеской полупьяный морской волк сунул своего волчонка прямо в дырку."
                    GloryLine2 = "Моряк наслаждается процессом, не обращая внимание на окружающее."
                    GloryLine3 = "Морячок кончил, и пошел восвояси, может к себе на корабль, а может гулять дальше."
                    PregnancyCheck(GirlNameTGH, "inside" if GloryHoleInside else "mouth", 1, "", 1, "Неизвестный моряк")
                elif 8 <= GloryHoleLook <= 10:
                    GloryLine1 = "За занавеской городской стражник расстегнул форменные штаны и сунул свой член прямо в дырку."
                    GloryLine2 = "Страж порядка громко стонет от наслаждения."
                    GloryLine3 = "Слуга закона кончил, и пошел обратно на улицы, ловить воров и грабителей."
                    PregnancyCheck(GirlNameTGH, "inside" if GloryHoleInside else "mouth", 1, "", 1, "Неизвестный стражник")
                else:
                    GloryLine1 = "За занавеской совсем молоденький пацан, ужасно краснея и нервничая, извлек свой невеликих размеров член и, закатив глаза в предвкушении, сунул его в дырку."
                    GloryLine2 = "Лицо пацаненка выражает всю гамму чувств - наслаждение, вострог, радость от расставания с девственностью. Надолго его, судя по всему, не хватит."
                    GloryLine3 = "Так и есть: всего через минуту мальчишка кончил и, довольный, убежал, даже забыв застегнуть до конца ширинку."
                    PregnancyCheck(GirlNameTGH, "inside" if GloryHoleInside else "mouth", 1, "", 1, "Неизвестный горожанин")
        else:
            GloryGirlLine0 = "За ширмой оказалось пусто! Может еще рано, а может быть здесь никто не работает."

    label TavernGloryHole_menu:
        "Вы находитесь в дальнем углу вашего трактира, где, за загородкой сделан глорихол. Посетители, чтобы попасть сюда, должны заплатить 6 мараведи, но к вам, согласно договору, это не относится - под внимательными взглядами ваших матери и сестер вы гордо вошли подошли к глорихолу не платя - это ваше право."
        "Что вы собираетесь делать?"

        if renpy.has_label("ShowImage"):
            call ShowImage("gloryhole", "", "glory1")

        menu:
            "Смотреть на клиента" if GloryHoleLook > 0 and GloryHoleCurrentStep <= 3 and BlockGloryHoleMenu == 0:
                if GloryHoleCurrentStep == 0:
                    "Вспомнив про сделанную мастеровитым гномом возможность обзора, вы решили посмотреть на происходящее инкогнито."
                else:
                    "Вы продолжаете обозревать происходящее внимательным взглядом."

                if GloryHoleCurrentStep == 0:
                    "[GloryLine1]"
                elif GloryHoleCurrentStep == 1:
                    "[GloryLine2]"
                else:
                    "[GloryLine3]"

                $ GloryHoleCurrentStep += 1
                if GloryHoleCurrentStep >= 3:
                    $ GloryHoleCurrentStep = 0
                    $ GloryHoleLook = 0

                if renpy.has_label("ShowImage"):
                    call ShowImage("gloryhole", "", "gloryclient")
                jump TavernGloryHole_menu

            "Смотреть на девочку" if CockInGloryHole == 0 and BlockGloryHoleMenu == 0:
                
                if GloryHoleCurrentStep == 0 or GloryHoleLook == 0:
                    "Вы решили аккуратно заглянуть за ширмочку и посмотреть на девочку за работой."
                else:
                    "Вы продолжаете дальше смотреть, как работает очаровательная [RealName.get(GirlNameTGH, GirlNameTGH)]."

                if GloryHoleLook == 0:
                    "[GloryGirlLine0]"
                elif GloryHoleCurrentStep == 0:
                    "[GloryGirlLine1]"
                elif GloryHoleCurrentStep == 1:
                    "[GloryGirlLine2]"
                else:
                    "[GloryGirlLine3]"

                if GloryHoleLook:
                    $ GloryHoleCurrentStep += 1
                    if GloryHoleCurrentStep >= 3:
                        $ GloryHoleCurrentStep = 0
                        $ GloryHoleLook = 0

                if AmandaAtGlory == 1:
                    $ BlockGloryHoleMenu = 1
                    $ AmandaGloryCurState = 1
                    $ AmandaVar["glorysdiscover"] = 1
                    "Ваша реакция?"
                    if renpy.has_label("ShowImage"):
                        call ShowImage("amanda", "gloryfirst", "ambush")

                if GirlNameTGH == "georgett" and GloryHoleWorks:
                    if renpy.has_label("ShowImageSeq"):
                        call ShowImageSeq("georgett", "glory", "glory", 2)
                elif GloryHoleWorks == 0:
                    if renpy.has_label("ShowImage"):
                        call ShowImage("gloryhole", "", "glory1")
                jump TavernGloryHole_menu

            "Вставить член" if CockInGloryHole == 0 and GloryHoleLook == 0 and cametoday < cancumdaily and GloryHoleCurrentStep == 0 and BlockGloryHoleMenu == 0:
                
                python:
                    _set_gloryhole_inside()
                $ CockInGloryHole = 1
                "Вы немного поласкали своего друга, приводя его в боевое состояние, и решительно вставили его в столь привлекательную дырку."
                "[GloryHoleYouLine1]"
                if GloryHoleWorks:
                    $ GloryHoleCurrentStep += 1
                if renpy.has_label("ShowImage"):
                    call ShowImage("gloryhole", "", "gloryyou")
                jump TavernGloryHole_menu

            "Наслаждаться процессом" if CockInGloryHole == 1 and GloryHoleLook == 0 and cametoday < cancumdaily and GloryHoleCurrentStep == 1 and BlockGloryHoleMenu == 0:
                
                "[GloryHoleYouLine2]"
                if GloryHoleWorks:
                    $ GloryHoleCurrentStep += 1
                if renpy.has_label("ShowImage"):
                    call ShowImage("gloryhole", "", "gloryyou")
                jump TavernGloryHole_menu

            "Кончить" if CockInGloryHole == 1 and GloryHoleLook == 0 and cametoday < cancumdaily and GloryHoleCurrentStep == 2 and BlockGloryHoleMenu == 0:
                
                "[GloryHoleYouLine3]"
                if GloryHoleWorks:
                    $ GloryHoleCurrentStep += 1

                if AmandaAtGlory == 1:
                    $ BlockGloryHoleMenu = 1
                    "Ваша реакция?"
                    python:
                        PregnancyCheck("amanda", "mouthface", 1, "Вы")
                    $ AmandaVar["glorysuck"] = 1
                    $ AmandaGloryCurState = 4
                else:
                    python:
                        PregnancyCheck(
                            GirlNameTGH,
                            "inside" if GloryHoleInside else "mouth",
                            1,
                            "Вы",
                        )

                $ CockInGloryHole = 0
                jump TavernGloryHole_menu

            "Что-то не то, проверить кто у глорихола" if AmandaAtGlory == 1 and BlockGloryHoleMenu == 0 and CockInGloryHole == 1:
                
                "[GloryGirlLine1]"
                $ AmandaGloryCurState = 2
                $ BlockGloryHoleMenu = 1
                "Ваша реакция?"
                if renpy.has_label("ShowImage"):
                    call ShowImage("amanda", "gloryfirst", "ambush")
                jump TavernGloryHole_menu

            "Ваша реакция" if BlockGloryHoleMenu == 1:
                if renpy.has_label("AmandaAtGloryHole"):
                    call AmandaAtGloryHole
                else:
                    "Реакция для этой сцены пока недоступна."
                jump TavernGloryHole_menu

            "Идти обратно в трактир":
                jump TavernMain
