# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _ibs_update_visibility(girl_name):
        check_visibility(girl_name)

    def _ibs_end_cock_state(girl_name):
        Becky.set_cock_position("none")
        Becky.set_cock_position("none", "eddie")

    def _ibs_set_arousal(who, value):
        value = min(100, max(0, int(value or 0)))
        if str(who or "").lower() == "you":
            player.intimacy.set_arousal(value)
            return
        info = people.get_info(who)
        if info is not None:
            info.set_arousal(value)

    def _ibs_arousal(who):
        if str(who or "").lower() == "you":
            return int(player.intimacy.arousal_value() or 0)
        info = people.get_info(who)
        return int(info.arousal_value() or 0) if info is not None else 0

    def _ibs_inc_arousal(who, amount):
        if str(who or "").lower() == "you":
            _ibs_set_arousal("You", int(player.intimacy.arousal_value() or 0) + int(amount or 0))
            return
        info = people.get_info(who)
        current = int(info.arousal_value() or 0) if info is not None else 0
        _ibs_set_arousal(who, current + int(amount or 0))

    def _ibs_eddie_observe_state(girl_name, obs_type=0):
        if int(Eddie.sex_stat("group_sex", 0) or 0) <= 0:
            return ("", 0)
        if int(obs_type or 0) == 0 and Becky.tits_visible():
            if Becky.corruption < 55:
                return ("Бекки попыталась было прикрыть рукой свои тяжелые обнаженные груди от взгляда Эдди, но быстро одумалась.", 2)
            return ("Заметив, что Эдди любуется ее обнажившимися грудями, вдова повернулась к нему и начала играть с сосками.", 3)
        if int(obs_type or 0) == 1 and Becky.pussy_visible():
            if Becky.corruption < 55:
                return ("Увидев, что Эдди пристально смотрит на ее щель, она плотно сжала ноги, но, вспомнив через несколько секунд, что о целомудрии имело смысл думать малость пораньше, немного расслабилась.", 4)
            return ("Заметив непристойный взгляд Эдди, направленный на ее голую промежность, вдова широко расставила ноги и стала играться с клитором. У него разве что слюна со рта не закапала от такого зрелища.", 7)
        return ("Эдди с горящими глазами наблюдал за тем, как вы раздеваете хозяйку лавки.", 0)


label IntBeckySex(GirlNameIBS="becky", GirlLocIBS="home", GirlModeIBS=""):
    $ renpy.dynamic("_becky_rakomstart_pic", "_becky_rakom_pic", "_becky_grope_pic", "_becky_minetalone_pic", "_becky_fuckstart_pic", "_becky_fuck_pic", "_becky_angry_pic", "_becky_happy_pic", "CurGiveOrgasms", "_cametoday", "_cancumdaily")
    python:
        Becky.ensure_sex_state()
        people.get_info("eddie").set_arousal(people.get_info("eddie").arousal_value())
        Eddie.set_sex_stat("group_sex", Eddie.sex_stat("group_sex", 0))
        CurGiveOrgasms = Becky.stats.get("orgasms_given", 0)
        _ibs_update_visibility(GirlNameIBS)
    call ShowBeckyPortrait

    label int_becky_sex_menu:
        while True:
            python:
                _cametoday = int(player.intimacy.came_today or 0)
                _cancumdaily = max(1, int(player.intimacy.can_cum_daily or 1))

            menu:
                "Осмотреть":
                    if renpy.has_label("GirlsDesc"):
                        call GirlsDesc(GirlNameIBS)
                    else:
                        "[people_display_name(GirlNameIBS)] внимательно смотрит на вас."

                "Снять блузку" if Becky.clothing_layer("top") != "" and not Becky.sex_busy():
                    "Хотя блузка [people_name(GirlNameIBS, 'genitive')] и так скрывала не слишком много, вы решили ее полностью снять. Расстегнув последние крючки и застежки, вы окончательно стянули этот явно лишний предмет."
                    $ Becky.remove_clothing_layer("top")
                    $ Becky.set_layer_raised("top", 0)
                    $ _ibs_update_visibility(GirlNameIBS)
                    $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 0)
                    if str(_ibs_observe_text or "").strip():
                        "[_ibs_observe_text]"
                    $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                    call ShowBeckyPortrait

                "Растегнуть блузку" if Becky.clothing_layer("top") != "" and not Becky.layer_raised("top") and not Becky.sex_busy():
                    "Вы начали ласкать груди Бекки сквозь одежду, а потом медленно распахнули блузку спереди, открывая обзор на грудь."
                    $ Becky.set_layer_raised("top", 1)
                    $ _ibs_update_visibility(GirlNameIBS)
                    $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 0)
                    if str(_ibs_observe_text or "").strip():
                        "[_ibs_observe_text]"
                    $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                    call ShowBeckyPortrait

                "Снять лифчик" if Becky.clothing_layer("bra") != "" and (Becky.clothing_layer("top") == "" or Becky.layer_raised("top")) and not Becky.sex_busy():
                    "Выше пояса на вдове теперь остается лишь лифчик. Вы заходите ей за спину и неторопливо расстегиваете его, освобождая тяжелые груди."
                    $ Becky.remove_clothing_layer("bra")
                    $ _ibs_update_visibility(GirlNameIBS)
                    $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 0)
                    if str(_ibs_observe_text or "").strip():
                        "[_ibs_observe_text]"
                    $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                    call ShowBeckyPortrait

                "Задрать юбочку" if Becky.clothing_layer("bottom") != "" and Becky.clothing_slut("bottom") >= 4 and not Becky.layer_raised("bottom") and not Becky.sex_busy():
                    if Becky.clothing_layer("panties") != "":
                        "Вы впились поцелуем в губы [people_name(GirlNameIBS, 'genitive')]. Тем временем ваши шаловливые ручки задрали и без того короткую юбочку до пояса, выставив ее кружевные панталончики на ваше обозрение."
                    else:
                        "Вы прошептали свое нескромное пожелание на ухо разбитной вдовушке. [people_display_name(GirlNameIBS)], даже не покраснев заткнула за пояс и без того короткий подол своего платья. Никакого нижнего белья под ним разумеется не оказалось."
                    $ Becky.set_layer_raised("bottom", 1)
                    $ _ibs_update_visibility(GirlNameIBS)
                    $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 1)
                    if str(_ibs_observe_text or "").strip():
                        "[_ibs_observe_text]"
                    $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                    call ShowBeckyPortrait

                "Поднять подол" if Becky.clothing_layer("bottom") != "" and Becky.clothing_slut("bottom") < 4 and not Becky.layer_raised("bottom") and not Becky.sex_busy():
                    if Becky.clothing_layer("panties") != "":
                        "Вы впились поцелуем в губы [people_name(GirlNameIBS, 'genitive')]. Тем временем ваши шаловливые ручки постепенно подняли длинный подол и завернули его за пояс, выставив ее кружевные панталончики на ваше обозрение."
                    elif Becky.current_underwear("panties", "") == "":
                        "Вы прошептали свое пошлое пожелание на ухо разбитной вдовушке. [people_display_name(GirlNameIBS)], немного покраснев, приподняла и заткнула за пояс длинный подол своего платья. Вы были приятно удивленны, не обнаружив и следов нижнего белья под внешне скромным платьем."
                    else:
                        "Вы впились поцелуем в губы [people_name(GirlNameIBS, 'genitive')]. Тем временем ваши шаловливые ручки постепенно подняли длинный подол и завернули его за пояс, выставив ее мокренькое влагалище на ваше обозрение."
                    $ Becky.set_layer_raised("bottom", 1)
                    $ _ibs_update_visibility(GirlNameIBS)
                    $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 1)
                    if str(_ibs_observe_text or "").strip():
                        "[_ibs_observe_text]"
                    $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                    call ShowBeckyPortrait

                "Снять платье" if Becky.clothing_layer("bottom") != "" and not Becky.sex_busy():
                    "Решив, что одного задранного подола мало, вы развязали завязки и окончательно стянули с Бекки платье."
                    $ Becky.remove_clothing_layer("bottom")
                    $ Becky.set_layer_raised("bottom", 0)
                    $ _ibs_update_visibility(GirlNameIBS)
                    $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 1)
                    if str(_ibs_observe_text or "").strip():
                        "[_ibs_observe_text]"
                    $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                    call ShowBeckyPortrait

                "Снять панталончики" if Becky.clothing_layer("panties") != "" and not Becky.sex_busy():
                    "Вы решаете избавиться от последнего препятствия и аккуратно стягиваете с нее панталончики, окончательно открывая киску нескромным взорам."
                    $ Becky.remove_clothing_layer("panties")
                    $ _ibs_update_visibility(GirlNameIBS)
                    $ _ibs_observe_text, _ibs_eddie_delta = _ibs_eddie_observe_state(GirlNameIBS, 1)
                    if str(_ibs_observe_text or "").strip():
                        "[_ibs_observe_text]"
                    $ _ibs_inc_arousal("eddie", _ibs_eddie_delta)
                    call ShowBeckyPortrait

                "Вытереть сперму с лица" if (Becky.cum_state("cum_face_you") or Becky.cum_state("cum_face_others")) and not Becky.sex_busy():
                    "Вы попросили вдовушку убрать с лица результаты ее предыдущих похождений. [people_display_name(GirlNameIBS)] покраснела, достала платочек и вытерла лицо и волосы от спермы."
                    $ Becky.clear_cum("cum_face_you", "cum_face_others")
                    $ _ibs_update_visibility(GirlNameIBS)
                    call ShowBeckyPortrait

                "Вытереть сперму с грудей" if (Becky.cum_state("cum_tits_you") or Becky.cum_state("cum_tits_others")) and Becky.tits_visible() and not Becky.sex_busy():
                    "Вы попросили вдовушку убрать с сисечек результаты ее предыдущих похождений. [people_display_name(GirlNameIBS)] достала платочек и, чуть стыдливо улыбаясь, вытерла свои дыньки от спермы."
                    $ Becky.clear_cum("cum_tits_you", "cum_tits_others")
                    $ _ibs_update_visibility(GirlNameIBS)
                    call ShowBeckyPortrait

                "Вытереть сперму с бедер" if (Becky.cum_state("cum_inside_you") or Becky.cum_state("cum_inside_others")) and Becky.pussy_visible() and not Becky.sex_busy():
                    "Вы предложили развратной вдовушке убрать с влагалища и бедер результаты ее предыдущих похождений. [people_display_name(GirlNameIBS)] достала платочек и, виновато посматривая на вас, вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                    $ Becky.clear_cum("cum_inside_you", "cum_inside_others")
                    $ _ibs_update_visibility(GirlNameIBS)
                    call ShowBeckyPortrait

                "Целовать" if not Becky.sex_busy():
                    if Becky.cock_in("pussy", "eddie") > 0:
                        "Вы впились в уста Бекки, пока ее сзади сношает Эдди."
                    else:
                        "Бекки страстно целует вас в засос, переплетаясь языками."
                    if Becky.cum_state("cum_face_you") > 0:
                        "На язык вам попадают следы вашего семени."
                    elif Becky.cum_state("cum_face_others") > 0:
                        "Вы чувствуете солоноватый привкус чужой спермы."
                    python:
                        _ibs_inc_arousal(GirlNameIBS, 9)
                        _ibs_inc_arousal("You", 7)
                    call ShowCurrentSex(GirlNameIBS)
                    call ShowImage(GirlNameIBS, "sex", "kiss")

                "Лапать" if not Becky.sex_busy():
                    if Becky.cock_in("mouth", "eddie") == 1:
                        "Полюбовавшись на делающую Эдди минет Бекки, вы решили, пользуясь предоставившейся возможностью, приласкать бедную вдову."
                    if Becky.cock_in("tits", "eddie") == 1:
                        "Полюбовавшись на то как Бекки ласкает член Эдди своими сисями, вы решили в свою очередь немного приласкать бедную вдову."
                    if Becky.cock_in("pussy", "eddie") == 1:
                        "Вы решили заняться массивными дойками Ребекки, пока Эдди сношает ее сзади."

                    if Becky.cock_in("tits", "eddie") == 0:
                        if not Becky.tits_visible():
                            if Becky.clothing_slut("top") == 3 and Becky.clothing_layer("bra") == "":
                                "Вы начали гладить внушительные шары [people_name(GirlNameIBS, 'genitive')] через тонкую ткань ее блузки."
                            elif Becky.clothing_slut("top") >= 4 and Becky.clothing_layer("bra") == "":
                                "Ваши руки забрались под декольте [people_name(GirlNameIBS, 'genitive')] и, не обнаружив там лифчика, начали гладить ее груди и теребить напрягшиеся сосочки."
                            elif Becky.clothing_slut("top") >= 4 and Becky.clothing_layer("bra") != "":
                                "Ваши руки забрались под декольте [people_name(GirlNameIBS, 'genitive')] и начали мять ее груди через лифчик."
                            else:
                                "Вы начали гладить и мять внушительные сиськи [people_name(GirlNameIBS, 'genitive')] через одежду."
                            $ _becky_grope_pic = "grope" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:244:1"))
                            call ShowImage(GirlNameIBS, "sex", _becky_grope_pic)
                        else:
                            if Becky.cum_state("cum_tits_you") > 0:
                                "Вы припали ртом к объемистым грудям [people_name(GirlNameIBS, 'genitive')], лаская языком ее чувствительные соски и слизывая с них свою сперму."
                            elif Becky.cum_state("cum_tits_others") > 0:
                                "Вы припали ртом к объемистым грудям [people_name(GirlNameIBS, 'genitive')], лаская языком ее чувствительные соски и слизывая с них чью-то сперму."
                            else:
                                "Вы припали ртом к объемистым грудям [people_name(GirlNameIBS, 'genitive')], лаская языком ее чувствительные соски."
                            call ShowImage(GirlNameIBS, "sex", "gropetits")

                    if Becky.cock_in("pussy", "eddie") == 0:
                        if Becky.pussy_visible():
                            "Вы медленно опустили руку вниз, к ее истекающей соками похотливой вульвочке, и начали ее нежно массировать."
                            call ShowImage(GirlNameIBS, "sex", "gropenaked")
                        else:
                            if not Becky.layer_raised("bottom") and Becky.clothing_layer("bottom") != "":
                                if Becky.clothing_slut("bottom") >= 4:
                                    if Becky.clothing_layer("panties") != "":
                                        "Вы сунули руку под короткую юбчонку вашей любовницы и начали натирать ее киску сквозь панталончики."
                                    else:
                                        "Вы сунули руку под короткую юбчонку вашей любовницы и стали наминать ее не стесненную бельем киску."
                                else:
                                    if Becky.clothing_layer("panties") != "":
                                        "Вы наклонились и сунули похотливую ручонку под длинную юбку вашей любовницы, медленно, лаская ее ножки, поднялись наверх, к заветному месту и начали натирать ее киску сквозь панталончики."
                                    else:
                                        "Вы наклонились и сунули похотливую ручонку под длинную юбку вашей любовницы, медленно, лаская ее ножки, поднялись наверх, к заветному месту и стали наминать ее не стесненную бельем киску."
                            else:
                                "Вы начали натирать ее похотливую киску сквозь панталончики."
                            call ShowImage(GirlNameIBS, "sex", "grope2")

                        if Becky.clothing_layer("panties") == "":
                            if Becky.cum_state("cum_inside_you") > 0:
                                "Вы почувствовали свою сперму в пещерке [people_name(GirlNameIBS, 'genitive')]."
                            elif Becky.cum_state("cum_inside_others") > 0:
                                "Ваши пальцы заскользили по пещерке [people_name(GirlNameIBS, 'genitive')], похоже кто-то уже кончил в нее."
                    $ _ibs_inc_arousal(GirlNameIBS, 15)
                    call ShowCurrentSex(GirlNameIBS)

                "Лизать киску" if Becky.pussy_visible() and not Becky.sex_busy() and Becky.cock_in("pussy", "eddie") == 0:
                    if Becky.cock_in("mouth", "eddie") == 1:
                        "[people_display_name(GirlNameIBS)], продолжая делать Эдди минет, раздвинула ножки и предоставила вам свою похотливую щель в полное распоряжение. Чем вы и не замедлили воспользоваться, начав старательно ласкать ее своим язычком."
                        $ _ibs_inc_arousal("eddie", 10)
                    elif Becky.cock_in("tits", "eddie") == 1:
                        "[people_display_name(GirlNameIBS)], наклонившись продолжает трахать член Эдди своими дойками, тем самым предоставляя вам свою щелку в полное распоряжение. Чем вы и не замедлили воспользоваться, начав старательно ласкать ее своим языком."
                        $ _ibs_inc_arousal("eddie", 15)
                    else:
                        "[people_display_name(GirlNameIBS)] радостно предоставила вам свое похотливое влагалище. Вы начали старательно ласкать развратную вдовушку своим языком. [people_display_name(GirlNameIBS)] прижимает вашу голову к себе обеими руками и сладко постанывает при каждом движении вашего языка."
                    if Becky.cum_state("cum_inside_you") > 0:
                        "Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [people_name(GirlNameIBS, 'genitive')]."
                    elif Becky.cum_state("cum_inside_others") > 0:
                        "Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [people_name(GirlNameIBS, 'genitive')], кто-то уже успел оттрахать шуструю вдовицу до вас."
                    $ Becky.record_lick_pussy()
                    if Becky.lick_pussy_count() == 4:
                        "\"Стефан, такой молодой, а уже знаешь что нужно даме, негодник!\", смеясь говорит [people_display_name(GirlNameIBS)], трепя вас за шевелюру. \"Продолжай же, продолжай!\""
                        $ Becky.add_relation(1, cap=100)
                    $ _ibs_inc_arousal(GirlNameIBS, 26)
                    call ShowCurrentSex(GirlNameIBS)
                    call ShowImage(GirlNameIBS, "sex", "lick")

                "Предложить отсосать" if _cametoday < _cancumdaily and not Becky.sex_busy() and Becky.cock_in("mouth", "eddie") == 0 and Becky.cock_in("tits", "eddie") == 0:
                    if Becky.cock_in("pussy", "eddie") > 0:
                        if Becky.cock_in("mouth", "You") == 0:
                            "Вы посмотрели немного на то, как задорно вдовушка сношается со своим управляющим, и решили поучаствовать в этом празднике жизни. Бекки не стала огорчать вас отказом и с готовностью приняла вашего дружка в свой ротик."
                        else:
                            "Вы вместе с Эдди продолжаете сношать Бекки в два смычка: он в киску, а вы в ротик."
                        $ _ibs_inc_arousal("eddie", 15)
                        $ _ibs_inc_arousal(GirlNameIBS, 20)
                    else:
                        if Becky.cock_in("mouth", "You"):
                            "[people_display_name(GirlNameIBS)] стоит перед вами на коленях и продолжает."
                        else:
                            "[people_display_name(GirlNameIBS)] опустилась перед вами на коленки и стала."
                    if _ibs_arousal("You") < 20:
                        "Облизывать ваш вялый член."
                        call ShowImage(GirlNameIBS, "sex", "minet1")
                    elif _ibs_arousal("You") < 40:
                        "Облизывать головку вашего напрягшегося члена."
                        call ShowImage(GirlNameIBS, "sex", "minet2")
                    elif Becky.corruption < 40:
                        "Неумело, но с энтузиазмом сосать ваш член."
                        call ShowImage(GirlNameIBS, "sex", "minet3")
                    elif _ibs_arousal("You") < 60:
                        "Умело сосать ваш член."
                        call ShowImage(GirlNameIBS, "sex", "minet3")
                    else:
                        "Заглатывать ваш член по самые яйца."
                        call ShowImage(GirlNameIBS, "sex", "minet4")
                    $ Becky.set_cock_position("mouth")
                    if Becky.cock_in("pussy", "eddie") == 0 and GrupenSex.get("eddie", 0) > 0:
                        $ _becky_minetalone_pic = "minetalone" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:338:2"))
                        call ShowImage(GirlNameIBS, "sex", _becky_minetalone_pic)
                    if Becky.corruption < 40:
                        $ _ibs_inc_arousal("You", 14)
                    else:
                        $ _ibs_inc_arousal("You", 20)
                    if Becky.cock_in("pussy", "eddie") > 0:
                        call ShowImage(GirlNameIBS, "sexeddie", "doubleeddie")
                    call ShowCurrentSex(GirlNameIBS)

                "Трахать между грудей" if _cametoday < _cancumdaily and not Becky.sex_busy() and _ibs_arousal("You") >= 20 and Becky.tits_visible() and Becky.pregnancy_days() < 130 and Becky.cock_in("tits", "eddie") == 0 and Becky.cock_in("mouth", "eddie") == 0:
                    if Becky.cock_in("pussy", "eddie") == 0:
                        if Becky.cock_in("tits", "You"):
                            "Вы лежите на кровати, а вдовица, наклонившись над вами, трахает ваш член своими огромными дойками. Время от времени ей удается поймать головку вашего члена ротиком."
                        else:
                            "Вы легли на кровать, а [people_display_name(GirlNameIBS)] наклонилась над вами, зажав ваш член между своих больших грудей. Затем она руками свела свои дойки вместе и начала слегка покачиваться, трахая вас своими сиськами. Иногда ей даже удается на секунду поймать головку вашего члена ртом."
                    else:
                        if Becky.cock_in("tits", "You"):
                            "Пока Эдди трахает Бекки сзади, она в свою очередь трахает ваш член своими большими сиськами. Толчки Эдди задают темп всей вашей компании. Время от времени ей удается поймать головку вашего члена ротиком."
                        else:
                            "Воспользовавшись тем, что Эдди трахал Бекки сзади, вы ловко подлезли под вдову. [people_display_name(GirlNameIBS)] сразу поняла, чего вы от нее хотите и немного опустилась, запустив ваш член между своих огромных грудей. Вы тоже времени даром не теряли и руками свели ее груди поближе друг к другу. Двигаясь взад и вперед под толчками Эдди она одновременно трахает и ваш член своими сиськами. Иногда ей даже удается на секунду поймать головку ртом."
                        $ _ibs_inc_arousal("eddie", 15)
                        $ _ibs_inc_arousal(GirlNameIBS, 20)
                    $ Becky.set_cock_position("tits")
                    $ _ibs_inc_arousal("You", 15)
                    call ShowCurrentSex(GirlNameIBS)

                "Трахать" if _cametoday < _cancumdaily and not Becky.sex_busy() and _ibs_arousal("You") >= 20 and _ibs_arousal(GirlNameIBS) >= 20 and Becky.pussy_visible() and Becky.cock_in("pussy", "eddie") == 0:
                    if Becky.pregnancy_days() < 130 and GrupenSex.get("eddie", 0) == 0:
                        if Becky.cock_in("pussy", "You") == 0:
                            "Вы страстно впились поцелуем в губы [people_name(GirlNameIBS, 'genitive')]. Не прекращая целовать ее вы с некоторым трудом приподняли ее в воздух и насадили прямо на свой вздыбленный член. [people_display_name(GirlNameIBS)] сладко охнула и, обхватив вас руками и ногами, стала подниматься и опускаться на вашем друге."
                            $ _becky_fuckstart_pic = "fuckstart" + str(procedural_randint(1, 8, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:373:3"))
                            call ShowImage(GirlNameIBS, "sex", _becky_fuckstart_pic)
                        else:
                            "Вы, благодаря своей прекрасной физической форме, трахаете не столь легкую вдову на весу, обняв под ягодицы. После каждого толчка она опускается на ваш член всем своим весом, так что он входит в нее по самые яйца, чуть ли не доставая до матки. [people_display_name(GirlNameIBS)] постанывает от наслаждения каждый раз как вы входите в нее."
                            $ _becky_fuck_pic = "fuck" + str(procedural_randint(1, 9, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:377:4"))
                            call ShowImage(GirlNameIBS, "sex", _becky_fuck_pic)
                    else:
                        if Becky.cock_in("mouth", "eddie") == 1:
                            if Becky.cock_in("pussy", "You") == 0:
                                "Вы посмотрели на то, как Ребекка отсасывает Эдди а потом перевели взгляд на ее истекающую соками дырочку. \"Ну, если это не приглашение, то я заморский гоблин-шахтер,\" подумали вы и резко вошли в любезно подставленную вам щель. Вдова охнула, но быстро приноровилась к вашим возвратно-поступательным движениям, не прекращая делать Эдди минет."
                                $ _becky_rakomstart_pic = "rakomstart" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:383:5"))
                                call ShowImage(GirlNameIBS, "sex", _becky_rakomstart_pic)
                            else:
                                "Вы трахаете Бекки сзади, массируя руками ее ягодицы, а она, в свою очередь, продолжает делать минет Эдди. Должно быть ей трудно заниматься двумя делами сразу но справляется. Умница!"
                            $ _ibs_inc_arousal("eddie", 15)
                            $ _becky_rakom_pic = "rakom" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:388:6"))
                            call ShowImage(GirlNameIBS, "sex", _becky_rakom_pic)
                        elif Becky.cock_in("tits", "eddie") == 1:
                            if Becky.cock_in("pussy", "You") == 0:
                                "Ребекка наклонилась над Эдди и трахает его член своими грудями, выставив свою истекающую соками дырочку на ваше обозрение. \"Ну, если это не приглашение, то я верховный маг высших эльфов,\" подумали вы и резко вошли в любезно подставленную вам щель, начав задавать темп вашей небольшой оргии. Вдове ваша помощь пришлась по нраву, она начала подмахивать вам, одновременно продолжая работать над членом Эдди."
                                $ _becky_rakomstart_pic = "rakomstart" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:393:7"))
                                call ShowImage(GirlNameIBS, "sex", _becky_rakomstart_pic)
                            else:
                                "Вы трахаете Бекки сзади, массируя руками ее ягодицы, а она, в свою очередь, трахает член Эдди своими дыньками. Ваши толчки задают ей темп, упрощая задачу. Как вы любите помогать людям!"
                            $ _ibs_inc_arousal("eddie", 15)
                            $ _becky_rakom_pic = "rakom" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:398:8"))
                            call ShowImage(GirlNameIBS, "sex", _becky_rakom_pic)
                        else:
                            if Becky.cock_in("pussy", "You") == 0:
                                "Вы страстно впились поцелуем в губы [people_name(GirlNameIBS, 'genitive')]. С трудом оторвавшись от ее губ, вы развернули ее раком и вошли в ее разгоряченное лоно одним движением. Вдовушка охнула и, поймав темп ваших толчков, стала вам умело подмахивать."
                                $ _becky_rakomstart_pic = "rakomstart" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:403:9"))
                                call ShowImage(GirlNameIBS, "sex", _becky_rakomstart_pic)
                            else:
                                "Вы трахаете вдову раком на ее кровати. Она умело подмахивает вам, и ваш член входит в нее по самые яйца. Судя по всему [people_name(GirlNameIBS, 'dative')] это приятно не меньше вашего, она постанывает от наслаждения при каждом толчке."
                                $ _becky_rakom_pic = "rakom" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:407:10"))
                                call ShowImage(GirlNameIBS, "sex", _becky_rakom_pic)
                    if Becky.pregnancy_days() > 130:
                        "Вы чувствуете как ребенок в животе у [people_name(GirlNameIBS, 'genitive')] двигается каждый раз когда ваш член входит во влагалище."
                    $ Becky.set_cock_position("pussy")
                    $ _ibs_inc_arousal("You", 20)
                    $ _ibs_inc_arousal(GirlNameIBS, 26)
                    call ShowCurrentSex(GirlNameIBS)

                "Кончить в ротик" if _cametoday < _cancumdaily and _ibs_arousal("You") >= 100 and (Becky.cock_in("mouth", "You") or Becky.cock_in("tits", "You")) and Becky.cock_in("mouth", "eddie") == 0:
                    "Чувствуя приближение концовки вы прижали голову [people_name(GirlNameIBS, 'genitive')] к себе как можно сильней, загоняя свой член ей в горло. Вдова восприняла это как должное, без видимых усилий заглотив ваш член целиком. В следующее мгновение вы разрядились, заливая горло и рот [people_name(GirlNameIBS, 'genitive')] своим семенем. Вдова сглотнула и с улыбкой облизала губы, убрав с них остатки вашей спермы. Вы вытащили свой обмякший член из заполненного спермой ротика."
                    if Becky.cock_in("pussy", "eddie") == 1:
                        "Эдди с восторгом наблюдал за этой сценой, не переставая потрахивать хозяйку."
                        $ _ibs_inc_arousal("eddie", 10)
                    $ _ibs_set_arousal("You", 0)
                    call PregnancyCheck("becky", "mouth", 1, "Вы")
                    $ _ibs_end_cock_state(GirlNameIBS)
                    $ Becky.set_sex_busy(True)
                    call ShowCurrentSex(GirlNameIBS)
                    call ShowImage(GirlNameIBS, "sex", "cummouth")
                    call int_becky_sex_after_cum
                    if _return:
                        return

                "Кончить на лицо" if _cametoday < _cancumdaily and _ibs_arousal("You") >= 100 and Becky.cock_in("mouth", "eddie") == 0 and Becky.cock_in("tits", "eddie") == 0:
                    "Вы вытащили ваш член и в следующее мгновение поток спермы выстрелил в переносицу [people_name(GirlNameIBS, 'genitive')] прямо между глаз. Продолжение струи легло на щеку, третья струя залила подбородок. Ваша подружка стала еще красивее чем была: лицо всё в сперме, струйки спускаются на шею, стекают по подбородку и капают на полные сиськи. Что за прелесть!"
                    $ _ibs_set_arousal("You", 0)
                    call PregnancyCheck("becky", "face", 1, "Вы")
                    $ _ibs_end_cock_state(GirlNameIBS)
                    $ Becky.set_sex_busy(True)
                    call ShowCurrentSex(GirlNameIBS)
                    call int_becky_sex_after_cum
                    if _return:
                        return

                "Кончить на груди" if _cametoday < _cancumdaily and _ibs_arousal("You") >= 100 and Becky.tits_visible() and Becky.cock_in("mouth", "eddie") == 0 and Becky.cock_in("tits", "eddie") == 0:
                    "Вы вытащили свой член из [people_name(GirlNameIBS, 'genitive')] и залили своей спермой ее монументальный бюст."
                    $ _ibs_set_arousal("You", 0)
                    call PregnancyCheck("becky", "tits", 1, "Вы")
                    $ _ibs_end_cock_state(GirlNameIBS)
                    $ Becky.set_sex_busy(True)
                    call ShowCurrentSex(GirlNameIBS)
                    call int_becky_sex_after_cum
                    if _return:
                        return

                "Кончить внутрь" if _cametoday < _cancumdaily and _ibs_arousal("You") >= 100 and Becky.cock_in("pussy", "You"):
                    if Becky.cock_in("mouth", "eddie") == 1:
                        "Приняв ее неразборчивое мычание за приглашение вы загнали свой член по самые яйца в ее похотливое влагалище и разрядились глубоко внутри [people_display_name(GirlNameIBS)]. Бекки, почувствовав что вы кончили в нее промычала что-то неразборчивое, продолжая делать минет Эдди."
                        $ _ibs_inc_arousal("eddie", 10)
                    else:
                        if Becky.pregnancy_days() < 120:
                            "Вы решили пойти на встречу просьбе вдовицы и, загнав свой член по самые яйца в ее похотливое влагалище, разрядились глубоко в [people_display_name(GirlNameIBS)]. Стоило вам вытащить из нее свой обмякший член, как распутница провела пальчиком по своей измазанной семенем киске и, смотря вам в глаза, облизала его и с улыбкой сказала вам:"
                            "\"Стефанчик, какой ты нахальный. Пытаешься бедную одинокую вдову в положение ввести. Наглец!\""
                        else:
                            "Вы решили пойти на встречу просьбе вдовицы и, загнав свой член по самые яйца в ее беременное влагалище, разрядились глубоко в [people_display_name(GirlNameIBS)], как будто пытаясь сделать ее еще более беременной. Стоило вам вытащить из нее свой обмякший член, как распутница погладила по свой округлившийся животик и сказала вам:"
                            "\"Какие же вы, мужчины, нахальные. Воспользовались слабостью бедной вдовы и оставили ее в тягости. Но и этого вам мало, и дальше моей слабостью пользуетесь. Ох, наглец!\""
                    $ _ibs_set_arousal("You", 0)
                    $ _ibs_set_arousal(GirlNameIBS, _ibs_arousal(GirlNameIBS) + 3)
                    call PregnancyCheck("becky", "inside", 1, "Вы")
                    $ _ibs_end_cock_state(GirlNameIBS)
                    $ Becky.set_sex_busy(True)
                    call ShowCurrentSex(GirlNameIBS)
                    call int_becky_sex_after_cum
                    if _return:
                        return

                "Попрощаться и уйти" if not Becky.sex_busy():
                    if CurGiveOrgasms == Becky.stats.get("orgasms_given", 0):
                        "Вы сказали [people_display_name(GirlNameIBS)] что вам нужно идти. Она была поражена:"
                        "\"Стефанчик, но мы же ведь только начали! Что случилось?! Я что, тебе разонравилась?!\""
                        "Но вы были непреклонны и направились к выходу, оставив за спиной неудовлетворенную вдову."
                        if GrupenSex.get("eddie", 0) > 0:
                            "\"Впрочем,\" услышали вы уже в дверях, \"у меня еще управляющий мой рыжий есть,\" и, оглянувшись перед тем как закрыть за собой дверь, вы увидели что Бекки тянет Эдди поближе к себе. \"Ты ведь не оставишь хозяйку мучаться как этот мужлан, нет?\""
                            call PregnancyCheck("becky", "inside", 1, "eddie")
                        $ Becky.apply_social_roll(3, 1, -1, 0, 0, 0)
                        $ _becky_angry_pic = "angry" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:481:11"))
                        call ShowImage(GirlNameIBS, "sex", _becky_angry_pic)
                    else:
                        "Вы поцеловали [people_display_name(GirlNameIBS)], удовлетворенно развалившуюся на кровати, заверили ее что она была бесподобна, но сейчас вам надо возвращаться домой."
                        "\"Стефанчик, жаль, но раз надо то надо. Спасибо тебе, что порадовал меня, не побрезговал мной старой.\""
                        "Вы заверили ее что отнюдь не считаете ее старой, наоборот, она в самом соку, и, получив приглашение заходить еще, отправились к выходу."
                        if GrupenSex.get("eddie", 0) > 0:
                            if int(Eddie.sex_stat("came_today", 0) or 0) < int(Eddie.sex_stat("can_cum_daily", 1) or 1):
                                "Эдди помахал вам вслед рукой, он-то еще уходить явно не собирался."
                            else:
                                "Эдди помахал вам на прощание рукой и тоже стал одеваться."
                        $ Becky.apply_social_roll(16, 2, 1, 42, 1, 1)
                        $ _becky_happy_pic = "happy" + str(procedural_randint(1, 5, key="procedural:NPC/Girls/Becky/IntBeckySex.rpy:procedural_randint:493:12"))
                        call ShowImage(GirlNameIBS, "sex", _becky_happy_pic)

                    $ _ibs_set_arousal("You", 0)
                    $ _ibs_set_arousal(GirlNameIBS, 0)
                    $ _ibs_end_cock_state(GirlNameIBS)
                    if int(threads["beckyHome"].num or 0) < 2:
                        $ threads["beckyHome"].advanceTo(2, force_active=True)
                    call ShowCurrentSex(GirlNameIBS)
                    call DressUp(GirlNameIBS)
                    $ Becky.set_sex_busy(False)
                    $ calendar_v2.advance_minutes(60)
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
                $ Becky.set_sex_busy(False)
                return False

            "Закончить":
                $ Becky.set_sex_busy(False)
                if str(GirlLocIBS or "").strip().lower() == "home":
                    jump BeckyHomeAfterSex
                return True
