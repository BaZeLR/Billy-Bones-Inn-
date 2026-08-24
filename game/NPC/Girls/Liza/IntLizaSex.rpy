# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntLizaSex(GirlNameILSS="liza", GirlLocILSS="street"):
    $ GirlNameILSS = "liza"
    $ Liza.sex_setup(GirlLocILSS)
    call ShowLizaPortrait

    label int_liza_sex_menu:
        while True:
            python:
                _liza_name = Liza.data.fullname
                _liza_name2 = Liza.data.genitive
                _liza_busy = Liza.sex_busy()
                _liza_top = Liza.clothing_layer("top")
                _liza_bottom = Liza.clothing_layer("bottom")
                _liza_panties = Liza.clothing_layer("panties")
                _liza_top_raised = Liza.layer_raised("top")
                _liza_bottom_raised = Liza.layer_raised("bottom")
                _liza_tits_visible = Liza.tits_visible()
                _liza_pussy_visible = Liza.pussy_visible()
                _liza_arousal = Liza.arousal_value()
                _you_arousal = Liza.player_arousal()
                _can_player_cum = Liza.can_player_cum()
                _sex_ctx = "sextraktir" if GirlLocILSS == "tavern" else "sexstreet"

            menu:
                "Осмотреть":
                    if renpy.has_label("GirlsDesc"):
                        call GirlsDesc(GirlNameILSS)

                "Снять блузку" if _liza_top != "" and not _liza_busy:
                    "Вы сняли с [_liza_name2] блузку, обнажив ее до пояса."
                    $ Liza.remove_top_for_sex()
                    call ShowLizaPortrait

                "Растегнуть блузку" if _liza_top != "" and not _liza_top_raised and not _liza_busy:
                    "Вы расстегнули блузку [_liza_name2], выпустив на волю ее маленькие крепкие мячики."
                    $ Liza.raise_top_for_sex()
                    call ShowLizaPortrait

                "Задрать юбочку" if _liza_bottom != "" and not _liza_bottom_raised and not _liza_busy:
                    if _liza_panties != "":
                        "Вы задрали красотке юбочку до пояса, обнаружив под ней маленькие кружевные панталончики."
                    else:
                        "Вы прошептали свое нескромное пожелание. [_liza_name] покраснела, но задрала подол платьичка."
                    $ Liza.raise_bottom_for_sex()
                    call ShowLizaPortrait

                "Снять панталончики" if _liza_panties != "" and not _liza_busy:
                    if not _liza_bottom_raised and _liza_bottom != "":
                        "Вы засунули руки под подол платья и стащили с нее панталончики до щиколоток."
                    else:
                        "Вы аккуратно стянули с нее панталончики, открывая киску нескромным взорам."
                    $ Liza.remove_panties_for_sex()
                    call ShowLizaPortrait

                "Вытереть сперму с лица" if (Liza.cum_state("cum_face_you") or Liza.cum_state("cum_face_others") or Liza.cum_state("cum_mouth_you") or Liza.cum_state("cum_mouth_others")) and not _liza_busy:
                    "Вы предложили шлюшке убрать с лица результаты ее предыдущих похождений. [_liza_name] покраснела, достала платочек и вытерла лицо и волосы от спермы."
                    $ Liza.clear_visible_cum("cum_face_you", "cum_face_others", "cum_mouth_you", "cum_mouth_others")
                    call ShowLizaPortrait

                "Вытереть сперму с грудей" if (Liza.cum_state("cum_tits_you") or Liza.cum_state("cum_tits_others")) and _liza_tits_visible and not _liza_busy:
                    "Вы предложили шлюшке убрать с сисечек результаты ее предыдущих похождений. [_liza_name] достала платочек и, кокетливо улыбаясь, вытерла свои маленькие грудки от спермы."
                    $ Liza.clear_visible_cum("cum_tits_you", "cum_tits_others")
                    call ShowLizaPortrait

                "Вытереть сперму с бедер" if (Liza.cum_state("cum_inside_you") or Liza.cum_state("cum_inside_others")) and _liza_pussy_visible and not _liza_busy:
                    "Вы предложили девчушке убрать с влагалища и бедер результаты ее предыдущих похождений. [_liza_name] достала платочек и, виновато посматривая на вас, вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                    $ Liza.clear_visible_cum("cum_inside_you", "cum_inside_others")
                    call ShowLizaPortrait

                "Целовать" if not _liza_busy:
                    "[_liza_name] со всей страстью молодости целует вас в засос, переплетаясь языками."
                    if Liza.cum_state("cum_face_you") > 0 or Liza.cum_state("cum_mouth_you") > 0:
                        "На язык вам попадают капли вашего семени, которым вы обкончали ее раньше."
                    elif Liza.cum_state("cum_face_others") > 0 or Liza.cum_state("cum_mouth_others") > 0:
                        "Вы чувствуете солоноватый привкус чужой спермы. Шустрая девчонка уже успела у кого-то отсосать до вас!"
                    if Liza.arousal_value() < 50:
                        $ Liza.add_arousal(8)
                    if Liza.player_arousal() < 50:
                        $ Liza.add_player_arousal(8)
                    $ Liza.set_cock_position("none")
                    call ShowCurrentSex(GirlNameILSS)

                "Лапать" if not _liza_busy:
                    if not _liza_tits_visible:
                        "Вы начали гладить маленькие сисечки через тонкую ткань блузки."
                        if renpy.has_label("ShowImage"):
                            call ShowImage(GirlNameILSS, _sex_ctx, "grope")
                    else:
                        "Вы припали ртом к обнаженным мячикам, лаская чувствительные соски."
                        if renpy.has_label("ShowImage"):
                            call ShowImage(GirlNameILSS, _sex_ctx, "gropetits")

                    if _liza_pussy_visible:
                        "Вы медленно опустили руку вниз и начали нежно массировать ее вульву."
                        if renpy.has_label("ShowImage"):
                            call ShowImage(GirlNameILSS, _sex_ctx, "gropepussy")
                    else:
                        "Вы ласкаете ее киску через одежду."

                    if Liza.arousal_value() < 60:
                        $ Liza.add_arousal(12)
                    $ Liza.set_cock_position("none")
                    call ShowCurrentSex(GirlNameILSS)

                "Лизать киску" if _liza_pussy_visible and not _liza_busy:
                    "[_liza_name] радостно предоставила вам свое похотливое влагалище. Вы начали старательно ласкать развратницу языком. [_liza_name] прижимает вашу голову к себе обеими руками и сладко попискивает при каждом движении вашего языка."
                    if Liza.cum_state("cum_inside_you") > 0:
                        "Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [_liza_name2]."
                    elif Liza.cum_state("cum_inside_others") > 0:
                        "Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [_liza_name2], кто-то уже успел оттрахать эту девочку до вас."
                    $ _liza_licks = Liza.record_lick_pussy()
                    if _liza_licks == 7:
                        "\"Ой, дяденька, какой ты хороший!\"  говорит [_liza_name]. \"Многие дяденьки сразу начинают меня сношать, а ведь я так люблю когда мне там внизу лижут!\""
                        $ Liza.change_social(friend_delta=1)
                    $ Liza.add_arousal(26)
                    $ Liza.set_cock_position("none")
                    call ShowCurrentSex(GirlNameILSS)
                    if renpy.has_label("ShowImage"):
                        if GirlLocILSS == "tavern":
                            call ShowImage(GirlNameILSS, "sextraktir", "lick")
                        else:
                            call ShowImage(GirlNameILSS, "sexstreet", "lick" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:199:1")))

                "Предложить отсосать" if _can_player_cum and not _liza_busy:
                    if Liza.cock_in("mouth"):
                        "[_liza_name] сидит перед вами на коленках и продолжает "
                    else:
                        "[_liza_name] опустилась перед вами на коленки и стала "
                    if Liza.player_arousal() < 20:
                        "облизывать ваш вялый член."
                    elif Liza.player_arousal() < 40:
                        "облизывать головку вашего напрягшегося члена."
                    elif Liza.corruption < 40:
                        "неумело, но с энтузиазмом сосать ваш член."
                    elif Liza.player_arousal() < 60:
                        "умело сосать ваш член."
                    else:
                        "заглатывать ваш член по самые яйца."
                    if Liza.corruption < 40:
                        $ Liza.add_player_arousal(14)
                    else:
                        $ Liza.add_player_arousal(20)
                    $ Liza.set_cock_position("mouth")
                    call ShowCurrentSex(GirlNameILSS)
                    if renpy.has_label("ShowImage"):
                        if GirlLocILSS == "tavern":
                            call ShowImage(GirlNameILSS, "sextraktir", "minet" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:227:2")))
                        else:
                            call ShowImage(GirlNameILSS, "sexstreet", "minet" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:procedural_randint:229:3")))

                "Трахать" if _can_player_cum and not _liza_busy and _you_arousal >= 20 and _liza_arousal >= 20 and _liza_pussy_visible:
                    if Liza.pregnancy_days() < 130:
                        if not Liza.cock_in("pussy"):
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
                        if not Liza.cock_in("pussy"):
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

                    $ Liza.add_player_arousal(20)
                    $ Liza.add_arousal(26)
                    $ Liza.set_cock_position("pussy")
                    call ShowCurrentSex(GirlNameILSS)

                "Кончить в ротик" if _can_player_cum and _you_arousal >= 100 and (Liza.cock_in("mouth") or Liza.cock_in("tits")):
                    "Вы прижали голову мулатки к себе и разрядились ей в рот, залив горло и подбородок семенем."
                    $ Liza.set_player_arousal(0)
                    call PregnancyCheck(GirlNameILSS, "mouthface", 1, "Вы")
                    $ Liza.set_cock_position("none")
                    $ Liza.set_sex_busy(True)
                    if renpy.has_label("ShowImage"):
                        if GirlLocILSS == "tavern":
                            call ShowImage(GirlNameILSS, "sextraktir", "cummouth")
                        else:
                            call ShowImage(GirlNameILSS, "sexstreet", "cummouth")

                "Кончить на лицо" if _can_player_cum and _you_arousal >= 100:
                    "Вы вытащили член и несколькими струями залили лицо девушки."
                    $ Liza.set_player_arousal(0)
                    call PregnancyCheck(GirlNameILSS, "face", 1, "Вы")
                    $ Liza.set_cock_position("none")
                    $ Liza.set_sex_busy(True)
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameILSS, _sex_ctx, "cumface")

                "Кончить на груди" if _can_player_cum and _you_arousal >= 100 and _liza_tits_visible:
                    "Вы вытащили член и залили спермой ее маленькие грудки."
                    $ Liza.set_player_arousal(0)
                    call PregnancyCheck(GirlNameILSS, "tits", 1, "Вы")
                    $ Liza.set_cock_position("none")
                    $ Liza.set_sex_busy(True)
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameILSS, _sex_ctx, "cumtits")

                "Кончить внутрь" if _can_player_cum and _you_arousal >= 100 and Liza.cock_in("pussy"):
                    if Liza.corruption < 50 and Liza.pregnancy_days() < 120:
                        "Вы проигнорировали просьбу и начали заливать ее киску семенем."
                        "\"Дяденька Стефан, и вы тоже меня не послушали!\" — обреченно проговорила девушка."
                    else:
                        "Вы, насадив худенькую смуглянку на член, начали заливать ее киску горячим семенем."
                    $ Liza.set_player_arousal(0)
                    $ Liza.add_arousal(3)
                    call PregnancyCheck(GirlNameILSS, "inside", 1, "Вы")
                    $ Liza.set_cock_position("none")
                    $ Liza.set_sex_busy(True)
                    if renpy.has_label("ShowImage"):
                        if GirlLocILSS == "tavern":
                            call ShowImage(GirlNameILSS, "sextraktir", "cumpussy")
                        else:
                            call ShowImage(GirlNameILSS, "sexstreet", "cumpussy")

                "Продолжить" if _liza_busy:
                    $ Liza.set_sex_busy(False)

                "Закончить":
                    $ Liza.set_sex_busy(False)
                    $ Liza.set_cock_position("none")
                    return
