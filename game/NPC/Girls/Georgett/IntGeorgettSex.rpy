# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntGeorgettSexSetup(GirlNameIGSS="georgett", GirlLocIGSS="street"):
    $ Georgett.sex_setup(GirlLocIGSS)
    if Georgett.needs_dress_up():
        call DressUp(GirlNameIGSS)
        $ Georgett.sex_setup(GirlLocIGSS)
    $ Georgett.set_cock_position("none")
    $ Georgett.refresh_sex_visibility()
    return


label IntGeorgettSexRemoveBlouse(GirlNameIGSS="georgett"):
    "Вы сняли с [RealName2.get(GirlNameIGSS, GirlNameIGSS)] блузку, обнажив ее до пояса."
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        "[_lactate_tits_desc]"
    $ Georgett.remove_blouse_for_sex()
    call ShowGeorgettPortrait
    return


label IntGeorgettSexUnbuttonBlouse(GirlNameIGSS="georgett"):
    "Вы расстегнули блузку [RealName2.get(GirlNameIGSS, GirlNameIGSS)], выпустив ее большие груди на волю."
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        "[_lactate_tits_desc]"
    $ Georgett.unbutton_blouse_for_sex()
    call ShowGeorgettPortrait
    return


label IntGeorgettSexRaiseSkirt(GirlNameIGSS="georgett"):
    "Вы задрали юбочку до пояса, с удовлетворением отметив, что шлюшка под ней ничего не носит."
    $ Georgett.raise_skirt_for_sex()
    call ShowGeorgettPortrait
    return


label GeorgettSexStatus(GirlLocIGSS="street"):
    if Georgett.player_arousal() >= 100:
        if Georgett.cock_in("pussy"):
            "[RealName.get('georgett', 'Жоржетта')] чувствует, что вы уже готовы кончить, и нежно шепчет вам, чтобы вы не сдерживались."
        else:
            "[RealName.get('georgett', 'Жоржетта')] чувствует, что вы уже готовы разрядиться, и приглашающе мычит, не прекращая ласку."

    if Georgett.arousal_value() < 20:
        "Киска [RealName2.get('georgett', 'Жоржетты')] суха и зажата. Проникновение не доставит ей удовольствия."
    if Georgett.arousal_value() >= 20 and Georgett.arousal_value() < 40:
        "[RealName.get('georgett', 'Жоржетта')] возбуждена. Её влагалище увлажнилось."
    if Georgett.arousal_value() >= 40 and Georgett.arousal_value() < 65:
        "[RealName.get('georgett', 'Жоржетта')] хорошо возбуждена. Её киска обильно смазана собственным соком."
    if Georgett.arousal_value() >= 65 and Georgett.arousal_value() < 85:
        "[RealName.get('georgett', 'Жоржетта')] близка к оргазму. Её стоны становятся всё чаще."
    if Georgett.arousal_value() >= 85 and Georgett.arousal_value() < 100:
        "[RealName.get('georgett', 'Жоржетта')] на грани оргазма. Каждое движение заставляет ее тело ритмично напрягаться."

    if Georgett.arousal_value() >= 100:
        "[RealName.get('georgett', 'Жоржетта')] забилась в судорогах оргазма, все ее тело выгнулось дугой. Со счастливым вздохом и блаженной улыбкой она кончила."
        $ _georgett_orgasm_count = Georgett.record_orgasm_given()
        if _georgett_orgasm_count == 2:
            "\"Какой ты заботливый\", сказала [RealName.get('georgett', 'Жоржетта')], с трудом отдышавшись после бурного оргазма. \"Не то, что другие, думающие только о своем удовольствии.\""
            $ Georgett.add_relation(1, 100)
        if Georgett.cock_in("pussy"):
            $ Georgett.set_arousal(20)
        else:
            $ Georgett.set_arousal(0)
        $ Georgett.set_sex_busy(1)
    return


label IntGeorgettSex(GirlNameIGSS="georgett", GirlLocIGSS="street"):
    call IntGeorgettSexSetup(GirlNameIGSS, GirlLocIGSS)

    label int_georgett_sex_menu:
        $ _can_player_cum = Georgett.can_player_cum()

        menu:
            "Осмотреть":
                if renpy.has_label("GirlsDesc"):
                    call GirlsDesc(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Снять блузку" if Georgett.has_top() and not Georgett.sex_busy():
                call IntGeorgettSexRemoveBlouse(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Растегнуть блузку" if Georgett.has_top() and not Georgett.top_is_raised() and not Georgett.sex_busy():
                call IntGeorgettSexUnbuttonBlouse(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Задрать юбочку" if Georgett.has_bottom() and not Georgett.bottom_is_raised() and not Georgett.sex_busy():
                call IntGeorgettSexRaiseSkirt(GirlNameIGSS)
                jump int_georgett_sex_menu

            "Вытереть сперму с лица" if (Georgett.cum_state("cum_face_you") or Georgett.cum_state("cum_face_others")) and not Georgett.sex_busy():
                "Вы предложили шлюшке убрать с лица результаты ее предыдущих похождений. [RealName.get(GirlNameIGSS, GirlNameIGSS)] достала платочек и вытерла лицо и волосы от спермы."
                $ Georgett.clear_cum("cum_face_you", "cum_face_others")
                call ShowGeorgettPortrait
                jump int_georgett_sex_menu

            "Вытереть сперму с грудей" if (Georgett.cum_state("cum_tits_you") or Georgett.cum_state("cum_tits_others")) and Georgett.visible_tits() and not Georgett.sex_busy():
                "Вы предложили шлюшке убрать с сисечек результаты ее предыдущих похождений. [RealName.get(GirlNameIGSS, GirlNameIGSS)] достала платочек и вытерла свои груди от спермы."
                $ Georgett.clear_cum("cum_tits_you", "cum_tits_others")
                call ShowGeorgettPortrait
                jump int_georgett_sex_menu

            "Вытереть сперму с бедер" if (Georgett.cum_state("cum_inside_you") or Georgett.cum_state("cum_inside_others")) and Georgett.visible_pussy() and not Georgett.sex_busy():
                "Вы предложили шлюшке убрать с влагалища и бедер результаты ее предыдущих похождений. [RealName.get(GirlNameIGSS, GirlNameIGSS)] достала платочек и вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                $ Georgett.clear_cum("cum_inside_you", "cum_inside_others")
                call ShowGeorgettPortrait
                jump int_georgett_sex_menu

            "Целовать" if not Georgett.sex_busy():
                "[RealName.get(GirlNameIGSS, GirlNameIGSS)] целует вас в засос, переплетаясь языками."
                if Georgett.cum_state("cum_face_you") > 0:
                    "На язык вам попадают капли вашего семени, которым вы обкончали ее раньше."
                elif Georgett.cum_state("cum_face_others") > 0:
                    "Вы чувствуете солоноватый привкус чужой спермы. Шалунья уже успела у кого-то отсосать до вас!"
                if Georgett.arousal_value() < 50:
                    $ Georgett.add_arousal(7, 50)
                if Georgett.player_arousal() < 50:
                    $ Georgett.add_player_arousal(7, 50)
                $ Georgett.set_cock_position("none")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Лапать" if not Georgett.sex_busy():
                if not Georgett.visible_tits():
                    "Вы начали мять сиськи через тонкую ткань ее блузки."
                else:
                    $ _grope_text = "Вы припали ртом к обнаженным грудям [RealName2.get(GirlNameIGSS, GirlNameIGSS)], лаская ртом ее чувствительные соски"
                    if Georgett.cum_state("cum_tits_you") > 0:
                        $ _grope_text += " и слизывая с них свою сперму."
                    elif Georgett.cum_state("cum_tits_others") > 0:
                        $ _grope_text += " и слизывая с них чью-то сперму."
                    else:
                        $ _grope_text += "."
                    "[_grope_text]"
                $ _lactate_tits_fondle = LactateTitsFondle(GirlNameIGSS)
                if str(_lactate_tits_fondle or "").strip():
                    "[_lactate_tits_fondle]"
                if Georgett.visible_pussy():
                    "Вы медленно опустили руку вниз, к ее вульвочке, и начали ее нежно массировать."
                else:
                    "Вы сунули руку под короткую юбочку и стали наминать ее вульву."
                if Georgett.cum_state("cum_inside_you") > 0:
                    "Вы почуствовали свою сперму в пещерке [RealName2.get(GirlNameIGSS, GirlNameIGSS)]."
                elif Georgett.cum_state("cum_inside_others") > 0:
                    "Ваши пальцы заскользили по пещерке [RealName2.get(GirlNameIGSS, GirlNameIGSS)], похоже кто-то уже кончил в нее."
                if not Georgett.visible_tits() and not Georgett.visible_pussy():
                    call ShowImage(GirlNameIGSS, "sex", "grope")
                if Georgett.arousal_value() < 60:
                    $ Georgett.add_arousal(12, 60)
                $ Georgett.set_cock_position("none")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Лизать киску" if Georgett.visible_pussy() and not Georgett.sex_busy():
                if GirlLocIGSS == "tavern":
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] легла на кровать и бесстыдно раздвинула ножки. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком."
                else:
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] стоя облокотилась спиной на стену, развинув бедра. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком."
                if Georgett.cum_state("cum_inside_you") > 0:
                    "Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameIGSS, GirlNameIGSS)]."
                elif Georgett.cum_state("cum_inside_others") > 0:
                    "Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [RealName2.get(GirlNameIGSS, GirlNameIGSS)], кто-то уже успел оттрахать эту куколку до вас."
                $ _georgett_lick_count = Georgett.add_lick_pussy()
                if _georgett_lick_count == 4:
                    "\"Ой, какой ты милый!\"  говорит [RealName.get(GirlNameIGSS, GirlNameIGSS)]. \"Многие мои клиенты особо не утруждаются чтобы сделать девушке приятное, но ты, я вижу, не из таких.\""
                    $ Georgett.add_relation(1, 100)
                $ Georgett.add_arousal(20)
                $ Georgett.set_cock_position("none")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Предложить отсосать" if _can_player_cum and not Georgett.sex_busy():
                if Georgett.cock_in("mouth"):
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] сидит перед вами на корточках и продолжает "
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameIGSS, "sex", "minet2")
                else:
                    "[RealName.get(GirlNameIGSS, GirlNameIGSS)] опустилась перед вами на корточки и стала "
                    if renpy.has_label("ShowImage"):
                        call ShowImage(GirlNameIGSS, "sex", "minet1")
                if Georgett.player_arousal() < 20:
                    "облизывать ваш вялый член."
                elif Georgett.player_arousal() < 40:
                    "облизывать головку вашего напрягшегося члена."
                elif Georgett.player_arousal() < 60:
                    "умело сосать ваш член."
                else:
                    "заглатывать ваш член по самые яйца."
                $ Georgett.add_player_arousal(20)
                $ Georgett.set_cock_position("mouth")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Трахать между грудей" if _can_player_cum and not Georgett.sex_busy() and Georgett.player_arousal() >= 20 and Georgett.visible_tits() and Georgett.pregnancy_days() < 150:
                if GirlLocIGSS == "tavern":
                    if Georgett.cock_in("tits"):
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] лежит изогнувшись на кровати, выставив вперед оба своих выдающихся достоинства, чтобы вы могли их трахнуть. Вы сношаете ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                    else:
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] легла спиной на кровать, частично свесившись, и изогнулась, выставив вперед оба своих выдающихся достоинства. Ваш член скользнул в ложбинку между ее холмов, и [RealName.get(GirlNameIGSS, GirlNameIGSS)] прижала свои сисечки руками одна к другой."
                        "Вы начали трахать ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                else:
                    if Georgett.cock_in("tits"):
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] сидит перед вами на корточках, выставив вперед оба своих выдающихся достоинства. Вы трахаете ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                    else:
                        "[RealName.get(GirlNameIGSS, GirlNameIGSS)] опустилась перед вами на корточки и изогнулась, выставив вперед оба своих выдающихся достоинства. Ваш член скользнул в ложбинку между ее холмов, и [RealName.get(GirlNameIGSS, GirlNameIGSS)] прижала свои сисечки руками одна к другой."
                        "Вы начали трахать ее между упругих грудок. В конце каждого вашего движения [RealName.get(GirlNameIGSS, GirlNameIGSS)] ловко ловит головку вашего члена своим страстным ротиком."
                $ _lactate_tits_fuck = LactateTitsFuck(GirlNameIGSS)
                if str(_lactate_tits_fuck or "").strip():
                    "[_lactate_tits_fuck]"
                $ Georgett.add_player_arousal(20)
                $ Georgett.set_cock_position("tits")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Трахать" if _can_player_cum and not Georgett.sex_busy() and Georgett.player_arousal() >= 20 and Georgett.arousal_value() >= 20 and Georgett.visible_pussy():
                if GirlLocIGSS == "tavern":
                    if not Georgett.cock_in("pussy"):
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
                    if not Georgett.cock_in("pussy"):
                        "Она уперлась ладонями в стену и выставила киску. Вы немедленно засадили ей по самые яйца."
                        if renpy.has_label("ShowImage"):
                            call ShowImage(GirlNameIGSS, "sex", "doggy1")
                    else:
                        "Вы продолжаете страстно трахать девушку, нежно мять ее ягодицы и сиськи."
                        if renpy.has_label("ShowImage"):
                            call ShowImage(GirlNameIGSS, "sex", "doggy" + str(renpy.random.randint(2, 3)))
                if Georgett.pregnancy_days() >= 150:
                    "Вы чувствуете, как ребенок в ее животе шевелится при каждом толчке."
                $ _lactate_pussy_fuck = LactatePussyFuck(GirlNameIGSS)
                if str(_lactate_pussy_fuck or "").strip():
                    "[_lactate_pussy_fuck]"
                $ Georgett.add_player_arousal(20)
                $ Georgett.add_arousal(14)
                $ Georgett.set_cock_position("pussy")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Кончить в ротик" if _can_player_cum and Georgett.player_arousal() >= 100 and (Georgett.cock_in("mouth") or Georgett.cock_in("tits")):
                "Ваш дружок напрягся и струя за струей заполнил ротик [RealName2.get(GirlNameIGSS, GirlNameIGSS)] вашим семенем. [RealName.get(GirlNameIGSS, GirlNameIGSS)] судорожно заглатывала вашу сперму и потом высунула свой очаровательный язычок дабы продемонстрировать вам что она проглотила все."
                $ Georgett.player_cum("mouth")
                call GeorgettSexStatus(GirlLocIGSS)
                call ShowImage(GirlNameIGSS, "sex", "cummouth")
                jump int_georgett_sex_menu

            "Кончить на лицо" if _can_player_cum and Georgett.player_arousal() >= 100:
                "Вы вытащили вашего дружка в последний момент и густые струи вашего семени ударили прямо по пухленьким щечкам и белокурым кудрям [RealName2.get(GirlNameIGSS, GirlNameIGSS)]."
                $ Georgett.player_cum("face")
                call GeorgettSexStatus(GirlLocIGSS)
                call ShowImage(GirlNameIGSS, "sex", "cummouth")
                jump int_georgett_sex_menu

            "Кончить на груди" if _can_player_cum and Georgett.player_arousal() >= 100 and Georgett.visible_tits():
                "Вы вытащили свой член из [RealName2.get(GirlNameIGSS, GirlNameIGSS)] и немедленно разрядились на ее груди и живот. [RealName.get(GirlNameIGSS, GirlNameIGSS)] провела пальцем по своим грудям а затем медленно, смотря вам в глаза, облизала измазанный спермой палец и улыбнулась."
                $ Georgett.player_cum("tits")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Кончить внутрь" if _can_player_cum and Georgett.player_arousal() >= 100 and Georgett.cock_in("pussy"):
                "Вы зарычали и кончили. Густые струи вашего семени хлынули во влагалище [RealName2.get(GirlNameIGSS, GirlNameIGSS)]. Блондинка, чувствуя как ее заполняет ваше семя, сладострастно застонала, приговаривая \"Да, милый, прямо в маточку твое семя ударило, сладко-то как. Так и залететь недолго!\""
                "Ваш обмякший член вывалился из ненасытной щелки и из нее потекла вязкая белая струйка."
                call ShowImage(GirlNameIGSS, "sex", "doggyinside")
                $ Georgett.add_arousal(3)
                $ Georgett.player_cum("inside")
                call GeorgettSexStatus(GirlLocIGSS)
                jump int_georgett_sex_menu

            "Продолжить" if Georgett.sex_busy():
                $ Georgett.set_sex_busy(0)
                jump int_georgett_sex_menu

            "Закончить":
                $ Georgett.set_sex_busy(0)
                return
