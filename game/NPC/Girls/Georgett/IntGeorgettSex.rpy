# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default GeorgettSexGirlName = "georgett"
default GeorgettSexGirlLoc = "street"
default GeorgettSexReturnRoom = ""
default GeorgettSexPicturePath = ""

init 6 python:
    def georgett_sex_begin_text():
        global MainTxt, CurLocDesc, GeorgettSexPicturePath
        MainTxt = ""
        CurLocDesc = ""
        GeorgettSexPicturePath = ""

    def georgett_sex_add_text(text_value):
        global MainTxt, CurLocDesc
        text_line = str(text_value or "").strip()
        if not text_line:
            return
        try:
            text_line = renpy.substitute(text_line)
        except Exception:
            pass
        current_text = str(MainTxt or "").strip()
        if current_text:
            current_text += "\n\n" + text_line
        else:
            current_text = text_line
        MainTxt = current_text
        CurLocDesc = current_text

    def georgett_sex_set_picture(folder1="", folder2="", image_name=""):
        global GeorgettSexPicturePath, scene_image, _layout_last_picture
        picture_path = build_media_ref(folder1, folder2, image_name)
        if picture_path:
            GeorgettSexPicturePath = picture_path
            scene_image = picture_path
            _layout_last_picture = picture_path

    def georgett_sex_set_portrait():
        Georgett.refresh_sex_visibility()
        if not Georgett.visible_tits() and not Georgett.visible_pussy():
            georgett_sex_set_picture("georgett", "portraits", "portrait" + str(procedural_randint(1, 4, "georgett_sex_portrait")))
        elif not Georgett.visible_tits() and Georgett.visible_pussy():
            georgett_sex_set_picture("georgett", "portraits", "strip01")
        elif Georgett.visible_tits() and not Georgett.visible_pussy():
            georgett_sex_set_picture("georgett", "portraits", "strip10")
        elif Georgett.visible_tits() and Georgett.visible_pussy():
            cur_sperm0 = Georgett.cum_state("cum_face_others") + Georgett.cum_state("cum_face_you")
            cur_sperm1 = Georgett.cum_state("cum_tits_you") + Georgett.cum_state("cum_tits_others")
            cur_sperm2 = Georgett.cum_state("cum_inside_you") + Georgett.cum_state("cum_inside_others")
            if cur_sperm0 == 0 and cur_sperm1 > 0 and cur_sperm2 == 0:
                georgett_sex_set_picture("georgett", "portraits", "stripsperm010")
            elif cur_sperm0 == 0 and cur_sperm1 > 0 and cur_sperm2 > 0:
                georgett_sex_set_picture("georgett", "portraits", "stripsperm011")
            elif cur_sperm0 > 0 and cur_sperm1 > 0 and cur_sperm2 > 0:
                georgett_sex_set_picture("georgett", "portraits", "stripsperm111")
            elif cur_sperm0 == 0 and cur_sperm1 == 0 and cur_sperm2 == 0:
                georgett_sex_set_picture("georgett", "portraits", "strip11")

    def georgett_sex_state_lines():
        runtime = ensure_player_runtime()
        intimacy = runtime.intimacy
        mc_arousal = Georgett.player_arousal()
        mc_came = people_to_int(intimacy.came_today, 0)
        mc_limit = max(1, people_to_int(intimacy.can_cum_daily, 1))
        girl_arousal = Georgett.arousal_value()
        lines = [
            "Стефан: возбуждение %d/100, разрядка %d/%d." % (mc_arousal, mc_came, mc_limit),
            "Жоржетта: возбуждение %d/100." % girl_arousal,
        ]
        if mc_came >= mc_limit:
            lines.append("На сегодня вы уже выжаты.")
        elif mc_arousal >= 100:
            lines.append("Вы на грани и можете кончить.")
        elif mc_arousal >= 20:
            lines.append("Вы достаточно возбуждены для продолжения.")
        return lines

screen georgett_sex_action_panel():
    vbox:
        spacing 8
        for _line in georgett_sex_state_lines():
            text _line size 16 color "#d8c27a"
        null height 4
        viewport:
            ymaximum 520
            mousewheel True
            draggable True
            scrollbars "vertical"
            use choice_panel(current_action_items)

label IntGeorgettSexSetup(GirlNameIGSS="georgett", GirlLocIGSS="street"):
    $ Georgett.sex_setup(GirlLocIGSS)
    if Georgett.needs_dress_up():
        call DressUp(GirlNameIGSS)
        $ Georgett.sex_setup(GirlLocIGSS)
    $ Georgett.set_cock_position("none")
    $ Georgett.refresh_sex_visibility()
    return


label IntGeorgettSexRemoveBlouse(GirlNameIGSS="georgett"):
    $ georgett_sex_add_text("Вы сняли с [Georgett.real_name2()] блузку, обнажив ее до пояса.")
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        $ georgett_sex_add_text(_lactate_tits_desc)
    $ Georgett.remove_blouse_for_sex()
    $ georgett_sex_set_portrait()
    return


label IntGeorgettSexUnbuttonBlouse(GirlNameIGSS="georgett"):
    $ georgett_sex_add_text("Вы расстегнули блузку [Georgett.real_name2()], выпустив ее большие груди на волю.")
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        $ georgett_sex_add_text(_lactate_tits_desc)
    $ Georgett.unbutton_blouse_for_sex()
    $ georgett_sex_set_portrait()
    return


label IntGeorgettSexRaiseSkirt(GirlNameIGSS="georgett"):
    $ georgett_sex_add_text("Вы задрали юбочку до пояса, с удовлетворением отметив, что шлюшка под ней ничего не носит.")
    $ Georgett.raise_skirt_for_sex()
    $ georgett_sex_set_portrait()
    return


label GeorgettSexStatus(GirlLocIGSS="street"):
    if Georgett.player_arousal() >= 100:
        if Georgett.cock_in("pussy"):
            $ georgett_sex_add_text("[Georgett.real_name()] чувствует, что вы уже готовы кончить, и нежно шепчет вам, чтобы вы не сдерживались.")
        else:
            $ georgett_sex_add_text("[Georgett.real_name()] чувствует, что вы уже готовы разрядиться, и приглашающе мычит, не прекращая ласку.")

    if Georgett.arousal_value() < 20:
        $ georgett_sex_add_text("Киска [Georgett.real_name2()] суха и зажата. Проникновение не доставит ей удовольствия.")
    if Georgett.arousal_value() >= 20 and Georgett.arousal_value() < 40:
        $ georgett_sex_add_text("[Georgett.real_name()] возбуждена. Её влагалище увлажнилось.")
    if Georgett.arousal_value() >= 40 and Georgett.arousal_value() < 65:
        $ georgett_sex_add_text("[Georgett.real_name()] хорошо возбуждена. Её киска обильно смазана собственным соком.")
    if Georgett.arousal_value() >= 65 and Georgett.arousal_value() < 85:
        $ georgett_sex_add_text("[Georgett.real_name()] близка к оргазму. Её стоны становятся всё чаще.")
    if Georgett.arousal_value() >= 85 and Georgett.arousal_value() < 100:
        $ georgett_sex_add_text("[Georgett.real_name()] на грани оргазма. Каждое движение заставляет ее тело ритмично напрягаться.")

    if Georgett.arousal_value() >= 100:
        $ georgett_sex_add_text("[Georgett.real_name()] забилась в судорогах оргазма, все ее тело выгнулось дугой. Со счастливым вздохом и блаженной улыбкой она кончила.")
        $ _georgett_orgasm_count = Georgett.record_orgasm_given()
        if _georgett_orgasm_count == 2:
            $ georgett_sex_add_text("\"Какой ты заботливый\", сказала [Georgett.real_name()], с трудом отдышавшись после бурного оргазма. \"Не то, что другие, думающие только о своем удовольствии.\"")
            $ Georgett.add_relation(1, 100)
        if Georgett.cock_in("pussy"):
            $ Georgett.set_arousal(20)
        else:
            $ Georgett.set_arousal(0)
        $ Georgett.set_sex_busy(1)
    return


label IntGeorgettSex(GirlNameIGSS="georgett", GirlLocIGSS="street"):
    $ GeorgettSexGirlName = str(GirlNameIGSS or "georgett")
    $ GeorgettSexGirlLoc = str(GirlLocIGSS or "street")
    $ GeorgettSexReturnRoom = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "")
    call IntGeorgettSexSetup(GeorgettSexGirlName, GeorgettSexGirlLoc)
    $ georgett_sex_begin_text()
    $ georgett_sex_set_portrait()
    if str(GeorgettSexPicturePath or "").strip():
        $ scene_image = str(GeorgettSexPicturePath or "")
        $ _layout_last_picture = scene_image
        vscene scene_image
    jump GeorgettSexMenu


label GeorgettSexMenu:
    $ UI_mode = "event"
    $ current_action_title = "Жоржетта"
    $ current_action_content = "georgett_sex_action_panel"
    $ current_action_items = []
    $ _gsgn = str(GeorgettSexGirlName or "georgett")
    $ _gsloc = str(GeorgettSexGirlLoc or "street")
    $ _can_player_cum = Georgett.can_player_cum()

    $ current_action_items.append(MenuItem("Осмотреть", Call("GeorgettSexApply", "look")))
    if Georgett.has_top() and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Снять блузку", Call("GeorgettSexApply", "remove_blouse")))
    if Georgett.has_top() and not Georgett.top_is_raised() and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Растегнуть блузку", Call("GeorgettSexApply", "unbutton_blouse")))
    if Georgett.has_bottom() and not Georgett.bottom_is_raised() and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Задрать юбочку", Call("GeorgettSexApply", "raise_skirt")))
    if (Georgett.cum_state("cum_face_you") or Georgett.cum_state("cum_face_others")) and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Вытереть сперму с лица", Call("GeorgettSexApply", "wipe_face")))
    if (Georgett.cum_state("cum_tits_you") or Georgett.cum_state("cum_tits_others")) and Georgett.visible_tits() and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Вытереть сперму с грудей", Call("GeorgettSexApply", "wipe_tits")))
    if (Georgett.cum_state("cum_inside_you") or Georgett.cum_state("cum_inside_others")) and Georgett.visible_pussy() and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Вытереть сперму с бедер", Call("GeorgettSexApply", "wipe_inside")))
    if not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Целовать", Call("GeorgettSexApply", "kiss")))
        $ current_action_items.append(MenuItem("Лапать", Call("GeorgettSexApply", "grope")))
    if Georgett.visible_pussy() and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Лизать киску", Call("GeorgettSexApply", "lick")))
    if _can_player_cum and not Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Предложить отсосать", Call("GeorgettSexApply", "blowjob")))
    if _can_player_cum and not Georgett.sex_busy() and Georgett.player_arousal() >= 20 and Georgett.visible_tits() and Georgett.pregnancy_days() < 150:
        $ current_action_items.append(MenuItem("Трахать между грудей", Call("GeorgettSexApply", "titfuck")))
    if _can_player_cum and not Georgett.sex_busy() and Georgett.player_arousal() >= 20 and Georgett.arousal_value() >= 20 and Georgett.visible_pussy():
        $ current_action_items.append(MenuItem("Трахать", Call("GeorgettSexApply", "fuck")))
    if Georgett.sex_busy():
        $ current_action_items.append(MenuItem("Продолжить", Call("GeorgettSexApply", "continue")))
    if _can_player_cum and Georgett.player_arousal() >= 100:
        if Georgett.cock_in("mouth") or Georgett.cock_in("tits"):
            $ current_action_items.append(MenuItem("Кончить в ротик", Call("GeorgettSexApply", "cum_mouth")))
        $ current_action_items.append(MenuItem("Кончить на лицо", Call("GeorgettSexApply", "cum_face")))
        if Georgett.visible_tits():
            $ current_action_items.append(MenuItem("Кончить на груди", Call("GeorgettSexApply", "cum_tits")))
        if Georgett.cock_in("pussy"):
            $ current_action_items.append(MenuItem("Кончить внутрь", Call("GeorgettSexApply", "cum_inside")))
    $ current_action_items.append(MenuItem("Закончить", Call("GeorgettSexFinish")))

    call screen main_ui
    return


label GeorgettSexApply(action_id=""):
    $ GirlNameIGSS = str(GeorgettSexGirlName or "georgett")
    $ GirlLocIGSS = str(GeorgettSexGirlLoc or "street")
    $ _georgett_sex_action = str(action_id or "")
    $ georgett_sex_begin_text()

    if _georgett_sex_action == "cum_mouth":
        $ georgett_sex_add_text("Ваш дружок напрягся и струя за струей заполнил ротик [Georgett.real_name2()] вашим семенем. [Georgett.real_name()] судорожно заглатывала вашу сперму и потом высунула свой очаровательный язычок дабы продемонстрировать вам что она проглотила все.")
        $ Georgett.player_cum("mouth")
        call GeorgettSexStatus(GirlLocIGSS)
        $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cummouth")

    elif _georgett_sex_action == "cum_face":
        $ georgett_sex_add_text("Вы вытащили вашего дружка в последний момент и густые струи вашего семени ударили прямо по пухленьким щечкам и белокурым кудрям [Georgett.real_name2()].")
        $ Georgett.player_cum("face")
        call GeorgettSexStatus(GirlLocIGSS)
        $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cummouth")

    elif _georgett_sex_action == "cum_tits":
        $ georgett_sex_add_text("Вы вытащили свой член из [Georgett.real_name2()] и немедленно разрядились на ее груди и живот. [Georgett.real_name()] провела пальцем по своим грудям а затем медленно, смотря вам в глаза, облизала измазанный спермой палец и улыбнулась.")
        $ Georgett.player_cum("tits")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "cum_inside":
        $ georgett_sex_add_text("Вы зарычали и кончили. Густые струи вашего семени хлынули во влагалище [Georgett.real_name2()]. Блондинка, чувствуя как ее заполняет ваше семя, сладострастно застонала, приговаривая \"Да, милый, прямо в маточку твое семя ударило, сладко-то как. Так и залететь недолго!\"")
        $ georgett_sex_add_text("Ваш обмякший член вывалился из ненасытной щелки и из нее потекла вязкая белая струйка.")
        $ georgett_sex_set_picture(GirlNameIGSS, "sex", "doggyinside")
        $ Georgett.add_arousal(3)
        $ Georgett.player_cum("inside")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "look":
        $ georgett_sex_add_text(Georgett.info_card_text() if hasattr(Georgett, "info_card_text") else Georgett.description)
        $ georgett_sex_set_portrait()

    elif _georgett_sex_action == "remove_blouse":
        call IntGeorgettSexRemoveBlouse(GirlNameIGSS)

    elif _georgett_sex_action == "unbutton_blouse":
        call IntGeorgettSexUnbuttonBlouse(GirlNameIGSS)

    elif _georgett_sex_action == "raise_skirt":
        call IntGeorgettSexRaiseSkirt(GirlNameIGSS)

    elif _georgett_sex_action == "wipe_face":
        $ georgett_sex_add_text("Вы предложили шлюшке убрать с лица результаты ее предыдущих похождений. [Georgett.real_name()] достала платочек и вытерла лицо и волосы от спермы.")
        $ Georgett.clear_cum("cum_face_you", "cum_face_others")
        $ georgett_sex_set_portrait()

    elif _georgett_sex_action == "wipe_tits":
        $ georgett_sex_add_text("Вы предложили шлюшке убрать с сисечек результаты ее предыдущих похождений. [Georgett.real_name()] достала платочек и вытерла свои груди от спермы.")
        $ Georgett.clear_cum("cum_tits_you", "cum_tits_others")
        $ georgett_sex_set_portrait()

    elif _georgett_sex_action == "wipe_inside":
        $ georgett_sex_add_text("Вы предложили шлюшке убрать с влагалища и бедер результаты ее предыдущих похождений. [Georgett.real_name()] достала платочек и вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете.")
        $ Georgett.clear_cum("cum_inside_you", "cum_inside_others")
        $ georgett_sex_set_portrait()

    elif _georgett_sex_action == "kiss":
        $ georgett_sex_add_text("[Georgett.real_name()] целует вас в засос, переплетаясь языками.")
        if Georgett.cum_state("cum_face_you") > 0:
            $ georgett_sex_add_text("На язык вам попадают капли вашего семени, которым вы обкончали ее раньше.")
        elif Georgett.cum_state("cum_face_others") > 0:
            $ georgett_sex_add_text("Вы чувствуете солоноватый привкус чужой спермы. Шалунья уже успела у кого-то отсосать до вас!")
        if Georgett.arousal_value() < 50:
            $ Georgett.add_arousal(7, 50)
        if Georgett.player_arousal() < 50:
            $ Georgett.add_player_arousal(7, 50)
        $ Georgett.set_cock_position("none")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "grope":
        if not Georgett.visible_tits():
            $ georgett_sex_add_text("Вы начали мять сиськи через тонкую ткань ее блузки.")
        else:
            $ _grope_text = "Вы припали ртом к обнаженным грудям %s, лаская ртом ее чувствительные соски" % Georgett.real_name2()
            if Georgett.cum_state("cum_tits_you") > 0:
                $ _grope_text += " и слизывая с них свою сперму."
            elif Georgett.cum_state("cum_tits_others") > 0:
                $ _grope_text += " и слизывая с них чью-то сперму."
            else:
                $ _grope_text += "."
            $ georgett_sex_add_text(_grope_text)
        $ _lactate_tits_fondle = LactateTitsFondle(GirlNameIGSS)
        if str(_lactate_tits_fondle or "").strip():
            $ georgett_sex_add_text(_lactate_tits_fondle)
        if Georgett.visible_pussy():
            $ georgett_sex_add_text("Вы медленно опустили руку вниз, к ее вульвочке, и начали ее нежно массировать.")
        else:
            $ georgett_sex_add_text("Вы сунули руку под короткую юбочку и стали наминать ее вульву.")
        if Georgett.cum_state("cum_inside_you") > 0:
            $ georgett_sex_add_text("Вы почуствовали свою сперму в пещерке [Georgett.real_name2()].")
        elif Georgett.cum_state("cum_inside_others") > 0:
            $ georgett_sex_add_text("Ваши пальцы заскользили по пещерке [Georgett.real_name2()], похоже кто-то уже кончил в нее.")
        if not Georgett.visible_tits() and not Georgett.visible_pussy():
            $ georgett_sex_set_picture(GirlNameIGSS, "sex", "grope")
        if Georgett.arousal_value() < 60:
            $ Georgett.add_arousal(12, 60)
        $ Georgett.set_cock_position("none")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "lick":
        if GirlLocIGSS == "tavern":
            $ georgett_sex_add_text("[Georgett.real_name()] легла на кровать и бесстыдно раздвинула ножки. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком.")
        else:
            $ georgett_sex_add_text("[Georgett.real_name()] стоя облокотилась спиной на стену, развинув бедра. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком.")
        if Georgett.cum_state("cum_inside_you") > 0:
            $ georgett_sex_add_text("Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [Georgett.real_name2()].")
        elif Georgett.cum_state("cum_inside_others") > 0:
            $ georgett_sex_add_text("Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [Georgett.real_name2()], кто-то уже успел оттрахать эту куколку до вас.")
        $ _georgett_lick_count = Georgett.add_lick_pussy()
        if _georgett_lick_count == 4:
            $ georgett_sex_add_text("\"Ой, какой ты милый!\"  говорит [Georgett.real_name()]. \"Многие мои клиенты особо не утруждаются чтобы сделать девушке приятное, но ты, я вижу, не из таких.\"")
            $ Georgett.add_relation(1, 100)
        $ Georgett.add_arousal(20)
        $ Georgett.set_cock_position("none")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "blowjob":
        if Georgett.cock_in("mouth"):
            $ georgett_sex_add_text("[Georgett.real_name()] сидит перед вами на корточках и продолжает ")
            $ georgett_sex_set_picture(GirlNameIGSS, "sex", "minet2")
        else:
            $ georgett_sex_add_text("[Georgett.real_name()] опустилась перед вами на корточки и стала ")
            $ georgett_sex_set_picture(GirlNameIGSS, "sex", "minet1")
        if Georgett.player_arousal() < 20:
            $ georgett_sex_add_text("облизывать ваш вялый член.")
        elif Georgett.player_arousal() < 40:
            $ georgett_sex_add_text("облизывать головку вашего напрягшегося члена.")
        elif Georgett.player_arousal() < 60:
            $ georgett_sex_add_text("умело сосать ваш член.")
        else:
            $ georgett_sex_add_text("заглатывать ваш член по самые яйца.")
        $ Georgett.add_player_arousal(20)
        $ Georgett.set_cock_position("mouth")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "titfuck":
        if GirlLocIGSS == "tavern":
            if Georgett.cock_in("tits"):
                $ georgett_sex_add_text("[Georgett.real_name()] лежит изогнувшись на кровати, выставив вперед оба своих выдающихся достоинства, чтобы вы могли их трахнуть. Вы сношаете ее между упругих грудок. В конце каждого вашего движения [Georgett.real_name()] ловко ловит головку вашего члена своим страстным ротиком.")
            else:
                $ georgett_sex_add_text("[Georgett.real_name()] легла спиной на кровать, частично свесившись, и изогнулась, выставив вперед оба своих выдающихся достоинства. Ваш член скользнул в ложбинку между ее холмов, и [Georgett.real_name()] прижала свои сисечки руками одна к другой.")
                $ georgett_sex_add_text("Вы начали трахать ее между упругих грудок. В конце каждого вашего движения [Georgett.real_name()] ловко ловит головку вашего члена своим страстным ротиком.")
        else:
            if Georgett.cock_in("tits"):
                $ georgett_sex_add_text("[Georgett.real_name()] сидит перед вами на корточках, выставив вперед оба своих выдающихся достоинства. Вы трахаете ее между упругих грудок. В конце каждого вашего движения [Georgett.real_name()] ловко ловит головку вашего члена своим страстным ротиком.")
            else:
                $ georgett_sex_add_text("[Georgett.real_name()] опустилась перед вами на корточки и изогнулась, выставив вперед оба своих выдающихся достоинства. Ваш член скользнул в ложбинку между ее холмов, и [Georgett.real_name()] прижала свои сисечки руками одна к другой.")
                $ georgett_sex_add_text("Вы начали трахать ее между упругих грудок. В конце каждого вашего движения [Georgett.real_name()] ловко ловит головку вашего члена своим страстным ротиком.")
        $ _lactate_tits_fuck = LactateTitsFuck(GirlNameIGSS)
        if str(_lactate_tits_fuck or "").strip():
            $ georgett_sex_add_text(_lactate_tits_fuck)
        $ Georgett.add_player_arousal(20)
        $ Georgett.set_cock_position("tits")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "fuck":
        if GirlLocIGSS == "tavern":
            if not Georgett.cock_in("pussy"):
                $ georgett_sex_add_text("Вы легли на кровать и усадили девицу прямо на возбужденный член, засадив по самые яйца.")
                if not Georgett.has_top():
                    $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cowgirl3")
                else:
                    $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cowgirl1")
            else:
                $ georgett_sex_add_text("Она страстно скачет на вас, пока вы мнете ее ягодицы и сиськи.")
                if not Georgett.has_top():
                    $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cowgirl4")
                else:
                    $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cowgirl2")
        else:
            if not Georgett.cock_in("pussy"):
                $ georgett_sex_add_text("Она уперлась ладонями в стену и выставила киску. Вы немедленно засадили ей по самые яйца.")
                $ georgett_sex_set_picture(GirlNameIGSS, "sex", "doggy1")
            else:
                $ georgett_sex_add_text("Вы продолжаете страстно трахать девушку, нежно мять ее ягодицы и сиськи.")
                $ georgett_sex_set_picture(GirlNameIGSS, "sex", "doggy" + str(procedural_randint(2, 3, "georgett_sex_doggy")))
        if Georgett.pregnancy_days() >= 150:
            $ georgett_sex_add_text("Вы чувствуете, как ребенок в ее животе шевелится при каждом толчке.")
        $ _lactate_pussy_fuck = LactatePussyFuck(GirlNameIGSS)
        if str(_lactate_pussy_fuck or "").strip():
            $ georgett_sex_add_text(_lactate_pussy_fuck)
        $ Georgett.add_player_arousal(20)
        $ Georgett.add_arousal(14)
        $ Georgett.set_cock_position("pussy")
        call GeorgettSexStatus(GirlLocIGSS)

    elif _georgett_sex_action == "continue":
        $ Georgett.set_sex_busy(0)

    if str(GeorgettSexPicturePath or "").strip():
        $ scene_image = str(GeorgettSexPicturePath or "")
        $ _layout_last_picture = scene_image
        vscene scene_image
    jump GeorgettSexMenu


label GeorgettSexFinish:
    $ Georgett.set_sex_busy(0)
    if str(active_module_kind or "") == "sex" and str(active_module_actor or "") == "georgett":
        return
    call AdvanceTimeOnly(40)
    $ _georgett_return_room = str(GeorgettSexReturnRoom or CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
    if _georgett_return_room:
        jump expression _georgett_return_room
    return
