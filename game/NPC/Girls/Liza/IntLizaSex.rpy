# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label LizaSexStatus(GirlLocILSS="street", _liza_orgasm_count=0, _liza_kids_peek_text="", _liza_status_busy=False):
    $ _liza_status_busy = bool(Liza.sex_busy())
    if _show_current_sex_allows_kids_peek("liza"):
        $ _liza_kids_peek_text = KidsPeekSexCode("liza")
        if str(_liza_kids_peek_text or "").strip():
            $ sex_scene_add_text(_liza_kids_peek_text)

    if not player.intimacy.can_cum():
        $ sex_scene_add_text(PLAYER_DAILY_EXHAUSTION_TEXT)
        $ player.intimacy.set_arousal(0)
    elif player.intimacy.arousal_value() >= 100:
        $ _liza_status_busy = True
        if Liza.cock_in("pussy") and Liza.corruption < 50 and Liza.pregnancy_days() < 120:
            $ sex_scene_add_text("[Liza.data.fullname] почувствовала что вы уже близки к оргазму. Гримаса страха промелькнула на ее смуглой мордашке.")
            $ sex_scene_add_text("«Ой, дядя Стефан, пожалуйста, вытащите. Не кончайте в меня, прошу вас, я боюсь залететь, прошу вас, не в меня!» — забормотала мулаточка.")
        elif Liza.cock_in("pussy"):
            $ sex_scene_add_text("[Liza.data.fullname] чувствует что вы готовы кончить и нежно шепчет вам чтобы вы кончали.")
        else:
            $ sex_scene_add_text("[Liza.data.fullname] чувствует что вы готовы кончить и приглашающе мычит, не прекращая сосать ваш член.")

    if Liza.arousal_value() < 20:
        $ sex_scene_add_text("Киска [Liza.data.genitive] суха и зажата. Проникновение не доставит ей удовольствия.")
    elif Liza.arousal_value() < 40:
        $ sex_scene_add_text("[Liza.data.fullname] возбуждена. Её влагалище увлажнилось.")
    elif Liza.arousal_value() < 65:
        $ sex_scene_add_text("[Liza.data.fullname] хорошо возбуждена. Её киска обильно смазана собственным соком.")
    elif Liza.arousal_value() < 85:
        $ sex_scene_add_text("[Liza.data.fullname] близка к оргазму. Её стоны становятся всё чаще и чаще.")
    elif Liza.arousal_value() < 100:
        $ sex_scene_add_text("[Liza.data.fullname] на грани оргазма. Каждая клеточка её киски ритмично пульсирует, а на теле местами появляются красные пятна.")

    if Liza.arousal_value() >= 100:
        $ _liza_status_busy = True
        $ sex_scene_add_text("[Liza.data.fullname] забилась в судорогах оргазма, все ее тело выгнулось дугой. Со счастливым вздохом и блаженной улыбкой [Liza.data.fullname] кончила.")
        $ sex_scene_add_text("[Liza.data.fullname] только что кончила.")
        $ _liza_orgasm_count = Liza.record_orgasm_given()
        if _liza_orgasm_count == 3:
            $ sex_scene_add_text("«Ой, дяденька Стефан, какой ты добрый и хороший», — заявила дрожащим от пережитого оргазма голоском [Liza.data.fullname]. «Многие дяденьки только о себе и думают, а с тобой всегда так хорошо, всегда мне удается спустить.»")
        if Liza.cock_in("pussy"):
            $ Liza.set_arousal(20)
        else:
            $ Liza.set_arousal(0)

    $ Liza.set_sex_busy(_liza_status_busy)
    return


label IntLizaSex(GirlNameILSS="liza", GirlLocILSS="street", SceneTextILSS=""):
    $ renpy.dynamic("_liza_licks", "_liza_name", "_liza_name2", "_liza_busy", "_liza_top", "_liza_bottom", "_liza_panties", "_liza_top_raised", "_liza_bottom_raised", "_liza_tits_visible", "_liza_pussy_visible", "_liza_arousal", "_you_arousal", "_can_player_cum", "_sex_ctx", "_liza_action_text", "_liza_lactate_text")
    $ GirlNameILSS = "liza"
    $ Liza.sex_setup(GirlLocILSS)
    $ main_ui_runtime.mode = "event"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.talk_picture = ""
    $ main_ui_runtime.action_title = "Лизетта"
    $ sex_scene_begin_text()
    if str(SceneTextILSS or "").strip():
        $ sex_scene_add_text(SceneTextILSS)
    call ShowLizaPortrait
    if str(scene_runtime.picture or "").strip():
        vscene scene_runtime.picture

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
                _you_arousal = player.intimacy.arousal_value()
                _can_player_cum = player.intimacy.can_cum()
                _sex_ctx = "sextraktir" if GirlLocILSS == "tavern" else "sexstreet"

            menu:
                "Осмотреть":
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text(Liza.data.description)
                    call ShowLizaPortrait

                "Снять блузку" if _liza_top != "" and not _liza_busy:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Вы сняли с [Liza.data.genitive] блузку, обнажив ее до пояса.")
                    $ Liza.remove_top_for_sex()
                    $ _liza_lactate_text = LactateTitsDesc(GirlNameILSS)
                    if str(_liza_lactate_text or "").strip():
                        $ sex_scene_add_text(_liza_lactate_text)
                    call ShowLizaPortrait

                "Растегнуть блузку" if _liza_top != "" and not _liza_top_raised and not _liza_busy:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Вы расстегнули блузку [Liza.data.genitive], выпустив на волю ее маленькие крепкие мячики.")
                    $ Liza.raise_top_for_sex()
                    $ _liza_lactate_text = LactateTitsDesc(GirlNameILSS)
                    if str(_liza_lactate_text or "").strip():
                        $ sex_scene_add_text(_liza_lactate_text)
                    call ShowLizaPortrait

                "Задрать юбочку" if _liza_bottom != "" and not _liza_bottom_raised and not _liza_busy:
                    $ sex_scene_begin_text()
                    if _liza_panties != "":
                        $ sex_scene_add_text("Вы задрали красотке юбочку до пояса, обнаружив под ней маленькие кружевные панталончики.")
                    else:
                        $ sex_scene_add_text("Вы прошептали свое нескромное пожелание на ушко девчушке. [Liza.data.fullname] покраснела, но задрала подол платьичка, под которым никаких панталончиков не обнаружилось.")
                    $ Liza.raise_bottom_for_sex()
                    call ShowLizaPortrait

                "Снять панталончики" if _liza_panties != "" and not _liza_busy:
                    $ sex_scene_begin_text()
                    if not _liza_bottom_raised and _liza_bottom != "":
                        $ sex_scene_add_text("Вы засунули свои шаловливые ручки под подол платья девушки и одним движением стащили с нее панталончики до щиколоток. [Liza.data.fullname] переступает через них, окончательно избавляясь от этого препятствия.")
                    else:
                        $ sex_scene_add_text("Вы решаетесь избавиться от последнего препятствия, отделяющего вас от пещерки вашей подружки. Вы аккуратно стягиваете с нее панталончики, открывая ее киску нескромным взорам. [Liza.data.fullname] переступает через них, окончательно избавляясь от этой досадной помехи.")
                    $ Liza.remove_panties_for_sex()
                    call ShowLizaPortrait

                "Вытереть сперму с лица" if (Liza.cum_state("cum_face_you") or Liza.cum_state("cum_face_others") or Liza.cum_state("cum_mouth_you") or Liza.cum_state("cum_mouth_others")) and not _liza_busy:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Вы предложили шлюшке убрать с лица результаты ее предыдущих похождений. [Liza.data.fullname] покраснела, достала платочек и вытерла лицо и волосы от спермы.")
                    $ Liza.clear_visible_cum("cum_face_you", "cum_face_others", "cum_mouth_you", "cum_mouth_others")
                    call ShowLizaPortrait

                "Вытереть сперму с грудей" if (Liza.cum_state("cum_tits_you") or Liza.cum_state("cum_tits_others")) and _liza_tits_visible and not _liza_busy:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Вы предложили шлюшке убрать с сисечек результаты ее предыдущих похождений. [Liza.data.fullname] достала платочек и, кокетливо улыбаясь, вытерла свои маленькие грудки от спермы.")
                    $ Liza.clear_visible_cum("cum_tits_you", "cum_tits_others")
                    call ShowLizaPortrait

                "Вытереть сперму с бедер" if (Liza.cum_state("cum_inside_you") or Liza.cum_state("cum_inside_others")) and _liza_pussy_visible and not _liza_busy:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Вы предложили девчушке убрать с влагалища и бедер результаты ее предыдущих похождений. [Liza.data.fullname] достала платочек и, виновато посматривая на вас, вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете.")
                    $ Liza.clear_visible_cum("cum_inside_you", "cum_inside_others")
                    call ShowLizaPortrait

                "Целовать" if not _liza_busy:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("[Liza.data.fullname] со всей страстью молодости целует вас в засос, переплетаясь языками.")
                    if Liza.cum_state("cum_face_you") > 0 or Liza.cum_state("cum_mouth_you") > 0:
                        $ sex_scene_add_text("На язык вам попадают капли вашего семени, которым вы обкончали ее раньше.")
                    elif Liza.cum_state("cum_face_others") > 0 or Liza.cum_state("cum_mouth_others") > 0:
                        $ sex_scene_add_text("Вы чувствуете солоноватый привкус чужой спермы. Шустрая девчонка уже успела у кого-то отсосать до вас!")
                    if Liza.arousal_value() < 50:
                        $ Liza.add_arousal(8)
                    if player.intimacy.arousal_value() < 50:
                        $ player.intimacy.add_arousal(8)
                    $ Liza.set_cock_position("none")
                    call LizaSexStatus(GirlLocILSS)
                    call ShowLizaPortrait

                "Лапать" if not _liza_busy:
                    $ sex_scene_begin_text()
                    if not _liza_tits_visible:
                        $ sex_scene_add_text("Вы начали гладить маленькие сисечки [Liza.data.genitive] через тонкую ткань ее блузки.")
                        $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "grope")
                    else:
                        $ _liza_action_text = "Вы припали ртом к обнаженным мячикам [Liza.data.genitive], лаская ртом ее чувствительные соски"
                        if Liza.cum_state("cum_tits_you") > 0:
                            $ _liza_action_text += " и слизывая с них свою сперму."
                        elif Liza.cum_state("cum_tits_others") > 0:
                            $ _liza_action_text += " и слизывая с них чью-то сперму."
                        else:
                            $ _liza_action_text += "."
                        $ sex_scene_add_text(_liza_action_text)
                        $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "gropetits")
                    $ _liza_lactate_text = LactateTitsFondle(GirlNameILSS)
                    if str(_liza_lactate_text or "").strip():
                        $ sex_scene_add_text(_liza_lactate_text)
                    if _liza_pussy_visible:
                        $ sex_scene_add_text("Вы медленно опустили руку вниз, к ее истекающей молодыми соками вульвочке, и начали ее нежно массировать.")
                        $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "gropepussy")
                    elif not _liza_bottom_raised and _liza_bottom != "":
                        if _liza_panties != "":
                            $ sex_scene_add_text("Вы сунули руку под платьичко вашей любовницы и начали натирать ее киску сквозь панталончики.")
                        else:
                            $ sex_scene_add_text("Вы сунули руку под короткое платьичко вашей любовницы и стали наминать ее юную вульвочку.")
                    else:
                        $ sex_scene_add_text("Вы начали натирать ее похотливую киску сквозь панталончики.")
                    if _liza_panties == "":
                        if Liza.cum_state("cum_inside_you") > 0:
                            $ sex_scene_add_text("Вы почувствовали свою сперму в пещерке [Liza.data.genitive].")
                        elif Liza.cum_state("cum_inside_others") > 0:
                            $ sex_scene_add_text("Ваши пальцы заскользили по пещерке [Liza.data.genitive], похоже кто-то уже кончил в нее.")
                    if Liza.arousal_value() < 60:
                        $ Liza.add_arousal(12)
                    $ Liza.set_cock_position("none")
                    call LizaSexStatus(GirlLocILSS)

                "Лизать киску" if _liza_pussy_visible and not _liza_busy:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("[Liza.data.fullname] радостно предоставила вам свое похотливое влагалище. Вы начали старательно ласкать развратницу языком. [Liza.data.fullname] прижимает вашу голову к себе обеими руками и сладко попискивает при каждом движении вашего языка.")
                    if Liza.cum_state("cum_inside_you") > 0:
                        $ sex_scene_add_text("Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [Liza.data.genitive].")
                    elif Liza.cum_state("cum_inside_others") > 0:
                        $ sex_scene_add_text("Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [Liza.data.genitive], кто-то уже успел оттрахать эту девочку до вас.")
                    $ _liza_licks = Liza.record_lick_pussy()
                    if _liza_licks == 7:
                        $ sex_scene_add_text("«Ой, дяденька, какой ты хороший!» — говорит [Liza.data.fullname]. «Многие дяденьки сразу начинают меня сношать, а ведь я так люблю когда мне там внизу лижут!»")
                    $ Liza.add_arousal(26)
                    $ Liza.set_cock_position("none")
                    call LizaSexStatus(GirlLocILSS)
                    if GirlLocILSS == "tavern":
                        $ sex_scene_set_picture(GirlNameILSS, "sextraktir", "lick")
                    else:
                        $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "lick" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:lick")))

                "Предложить отсосать" if _can_player_cum and Liza.can_have_sex_today() and not _liza_busy:
                    $ sex_scene_begin_text()
                    if Liza.cock_in("mouth"):
                        $ _liza_action_text = "[Liza.data.fullname] сидит перед вами на коленках и продолжает "
                    else:
                        $ _liza_action_text = "[Liza.data.fullname] опустилась перед вами на коленки и стала "
                    if player.intimacy.arousal_value() < 20:
                        $ _liza_action_text += "облизывать ваш вялый член."
                    elif player.intimacy.arousal_value() < 40:
                        $ _liza_action_text += "облизывать головку вашего напрягшегося члена."
                    elif Liza.corruption < 40:
                        $ _liza_action_text += "неумело, но с энтузиазмом сосать ваш член."
                    elif player.intimacy.arousal_value() < 60:
                        $ _liza_action_text += "умело сосать ваш член."
                    else:
                        $ _liza_action_text += "заглатывать ваш член по самые яйца."
                    $ sex_scene_add_text(_liza_action_text)
                    if Liza.corruption < 40:
                        $ player.intimacy.add_arousal(14)
                    else:
                        $ player.intimacy.add_arousal(20)
                    $ Liza.set_cock_position("mouth")
                    call LizaSexStatus(GirlLocILSS)
                    if GirlLocILSS == "tavern":
                        $ sex_scene_set_picture(GirlNameILSS, "sextraktir", "minet" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:minet_tavern")))
                    else:
                        $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "minet" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:minet_street")))

                "Трахать" if _can_player_cum and Liza.can_have_sex_today() and not _liza_busy and _you_arousal >= 20 and _liza_arousal >= 20 and _liza_pussy_visible:
                    $ sex_scene_begin_text()
                    if Liza.pregnancy_days() < 130:
                        if not Liza.cock_in("pussy"):
                            $ sex_scene_add_text("Вы страстно впились поцелуем в губы [Liza.data.genitive]. Не прекращая целовать ее, вы приподняли ее легкое тело в воздух и насадили прямо на свой вздыбленный член. Мулаточка охнула и, обхватив вас руками и ногами, стала подниматься и опускаться на вашем друге.")
                            if GirlLocILSS == "tavern":
                                $ sex_scene_set_picture(GirlNameILSS, "sextraktir", "fuckstart" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:fuckstart_tavern")))
                            else:
                                $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "fuck" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:fuckstart_street")))
                        else:
                            $ sex_scene_add_text("Вы трахаете молоденькую мулатку на весу, обняв под ягодицы. После каждого толчка она опускается на ваш член всем своим весом, так что он входит в нее по самые яйца, чуть ли не доставая до матки девушки. [Liza.data.fullname] постанывает от наслаждения каждый раз как вы входите в нее.")
                            if GirlLocILSS == "tavern":
                                $ sex_scene_set_picture(GirlNameILSS, "sextraktir", "fuck" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:fuck_tavern")))
                            else:
                                $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "fuck" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:fuck_street")))
                    else:
                        if not Liza.cock_in("pussy"):
                            $ sex_scene_add_text("Вы не можете взять юную мулатку как обычно стоя, так как этому помешал бы выросший из-за ее проказ животик. Впрочем, это вас не останавливает: [Liza.data.fullname] встает раком, а вы, пристроившись сзади, начинаете сношать ее беременную киску.")
                            if GirlLocILSS == "tavern":
                                $ sex_scene_set_picture(GirlNameILSS, "sextraktir", "fuckstart" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:pregnant_start_tavern")))
                            else:
                                $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "rakomstart" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:pregnant_start_street")))
                        else:
                            $ sex_scene_add_text("Вы страстно трахаете смуглянку, постепенно наращивая темп. Вы чувствуете как ребенок в животе у [Liza.data.genitive] двигается каждый раз когда ваш член входит во влагалище его или ее развратной мамочки. Мулаточка постанывает все громче.")
                            if GirlLocILSS == "tavern":
                                $ sex_scene_set_picture(GirlNameILSS, "sextraktir", "fuck" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:pregnant_fuck_tavern")))
                            else:
                                $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "rakom" + str(procedural_randint(1, 6, key="procedural:NPC/Girls/Liza/IntLizaSex.rpy:pregnant_fuck_street")))
                    $ _liza_lactate_text = LactatePussyFuck(GirlNameILSS)
                    if str(_liza_lactate_text or "").strip():
                        $ sex_scene_add_text(_liza_lactate_text)
                    $ player.intimacy.add_arousal(20)
                    $ Liza.add_arousal(26)
                    $ Liza.set_cock_position("pussy")
                    call LizaSexStatus(GirlLocILSS)

                "Кончить в ротик" if _can_player_cum and Liza.can_have_sex_today() and _you_arousal >= 100 and (Liza.cock_in("mouth") or Liza.cock_in("tits")):
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Чувствуя приближение концовки, вы прижали голову мулатки к себе как можно сильней, загоняя свой член ей в горло. Глаза мулатки округлились от неожиданности, и в следующее мгновение вы разрядились, заливая горло и рот [Liza.data.genitive] своим семенем. Его было слишком много, девушка поперхнулась, и вязкая белая жидкость потекла по подбородку. Вы вытащили свой обмякший член из заполненного спермой ротика.")
                    $ sex_scene_add_text("[Liza.data.fullname] слизала сколько смогла вашего семени со своих губ и подбородка, однако его еще много осталось на личике и щечках юной развратницы.")
                    $ Liza.player_cum("mouth")
                    call LizaSexStatus(GirlLocILSS)
                    $ sex_scene_set_picture(GirlNameILSS, _sex_ctx, "cummouth")

                "Кончить на лицо" if _can_player_cum and Liza.can_have_sex_today() and _you_arousal >= 100:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Вы вытащили ваш член, и в следующее мгновение поток спермы выстрелил в переносицу [Liza.data.genitive] прямо между глаз. Продолжение струи легло на щеку, третья струя залила подбородок. Ваша подружка стала еще красивее чем была: лицо всё в сперме, струйки спускаются на шею, стекают по подбородку и капают на маленькие грудки. Что за прелесть!")
                    $ Liza.player_cum("face")
                    call LizaSexStatus(GirlLocILSS)
                    $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "cumface")

                "Кончить на груди" if _can_player_cum and Liza.can_have_sex_today() and _you_arousal >= 100 and _liza_tits_visible:
                    $ sex_scene_begin_text()
                    $ sex_scene_add_text("Вы вытащили свой член из [Liza.data.genitive] и залили своей спермой ее маленькие грудки.")
                    $ Liza.player_cum("tits")
                    call LizaSexStatus(GirlLocILSS)
                    $ sex_scene_set_picture(GirlNameILSS, "sexstreet", "cumtits")

                "Кончить внутрь" if _can_player_cum and Liza.can_have_sex_today() and _you_arousal >= 100 and Liza.cock_in("pussy"):
                    $ sex_scene_begin_text()
                    if Liza.corruption < 50 and Liza.pregnancy_days() < 120:
                        $ sex_scene_add_text("Вы проигнорировали просьбу и, насадив худенькую смуглянку на ваш вздыбленный член, начали заливать ее киску потоками горячего семени. Почувствовав что вы спустили прямо в нее, [Liza.data.fullname] обреченно проговорила:")
                        $ sex_scene_add_text("«Дяденька Стефан, и вы тоже меня не послушали! Что же вы все такие! Ведь от этого ребеночек может быть, а мне же еще рано, я ведь сама еще маленькая!» Тем временем ваш обмякший член выскользнул из девичьей щелки, и по бедрам мулатки потекло вязкое белое семя.")
                    else:
                        $ sex_scene_add_text("Вы, насадив худенькую смуглянку на ваш вздыбленный член, начали заливать ее киску потоками своего горячего семени. Почувствовав, что вы спускаете в нее, [Liza.data.fullname] еще крепче обхватила вас и прижала к себе.")
                        $ sex_scene_add_text("Кончив, вы поцеловали девушку еще раз и ослабили объятия. Ваш обмякший член выскользнул из девичьей щелки, и по бедрам мулатки потекло вязкое белое семя.")
                    $ Liza.add_arousal(3)
                    $ Liza.player_cum("inside")
                    call LizaSexStatus(GirlLocILSS)
                    $ sex_scene_set_picture(GirlNameILSS, _sex_ctx, "cumpussy")

                "Продолжить" if _liza_busy:
                    $ Liza.set_sex_busy(False)

                "Закончить":
                    $ Liza.set_sex_busy(False)
                    $ Liza.set_cock_position("none")
                    return

            if str(scene_runtime.picture or "").strip():
                vscene scene_runtime.picture
    return
