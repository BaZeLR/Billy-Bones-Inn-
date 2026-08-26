# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def georgett_sex_begin_text():
        scene_runtime.text = ""
        scene_runtime.location_text = ""

    def georgett_sex_add_text(text_value):
        text_line = str(text_value or "").strip()
        if not text_line:
            return
        try:
            text_line = renpy.substitute(text_line)
        except Exception:
            pass
        current_text = str(scene_runtime.text or "").strip()
        if current_text:
            current_text += "\n\n" + text_line
        else:
            current_text = text_line
        scene_runtime.text = current_text
        scene_runtime.location_text = current_text

    def georgett_sex_set_picture(folder1="", folder2="", image_name=""):
        picture_path = build_media_ref(folder1, folder2, image_name)
        if picture_path:
            scene_runtime.picture = picture_path

    def georgett_sex_set_portrait():
        if not Georgett.tits_visible() and not Georgett.pussy_visible():
            georgett_sex_set_picture("georgett", "portraits", "portrait" + str(procedural_randint(1, 4, "georgett_sex_portrait")))
        elif not Georgett.tits_visible() and Georgett.pussy_visible():
            georgett_sex_set_picture("georgett", "portraits", "strip01")
        elif Georgett.tits_visible() and not Georgett.pussy_visible():
            georgett_sex_set_picture("georgett", "portraits", "strip10")
        elif Georgett.tits_visible() and Georgett.pussy_visible():
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
        runtime = player
        intimacy = runtime.intimacy
        mc_arousal = intimacy.arousal_value()
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

label IntGeorgettSexSetup(GirlNameIGSS="georgett", GirlLocIGSS="street"):
    $ Georgett.sex_setup(GirlLocIGSS)
    if Georgett.needs_dress_up():
        call DressUp(GirlNameIGSS)
        $ Georgett.sex_setup(GirlLocIGSS)
    $ Georgett.set_cock_position("none")
    return


label IntGeorgettSexRemoveBlouse(GirlNameIGSS="georgett", _lactate_tits_desc=""):
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы сняли с [Georgett.real_name2()] блузку, обнажив ее до пояса.")
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        $ georgett_sex_add_text(_lactate_tits_desc)
    $ Georgett.remove_blouse_for_sex()
    $ georgett_sex_set_portrait()
    return


label IntGeorgettSexUnbuttonBlouse(GirlNameIGSS="georgett", _lactate_tits_desc=""):
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы расстегнули блузку [Georgett.real_name2()], выпустив ее большие груди на волю.")
    $ _lactate_tits_desc = LactateTitsDesc(GirlNameIGSS)
    if str(_lactate_tits_desc or "").strip():
        $ georgett_sex_add_text(_lactate_tits_desc)
    $ Georgett.unbutton_blouse_for_sex()
    $ georgett_sex_set_portrait()
    return


label IntGeorgettSexRaiseSkirt(GirlNameIGSS="georgett"):
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы задрали юбочку до пояса, с удовлетворением отметив, что шлюшка под ней ничего не носит.")
    $ Georgett.raise_skirt_for_sex()
    $ georgett_sex_set_portrait()
    return


label GeorgettSexStatus(GirlLocIGSS="street", _georgett_orgasm_count=0):
    if player.intimacy.arousal_value() >= 100:
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
    call IntGeorgettSexSetup(GirlNameIGSS, GirlLocIGSS)
    $ georgett_sex_begin_text()
    $ georgett_sex_set_portrait()
    if str(scene_runtime.picture or "").strip():
        vscene scene_runtime.picture
    call GeorgettSexMenu
    return


label GeorgettSexMenu:
    $ main_ui_runtime.mode = "event"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.talk_picture = ""
    $ main_ui_runtime.action_title = "Жоржетта"
    while True:
        $ main_ui_runtime.action_content = "\n".join(georgett_sex_state_lines())
        menu:
            "Осмотреть":
                call GeorgettSexLook
            "Снять блузку" if bool(Georgett.clothing_layer("top")) and not Georgett.sex_busy():
                call IntGeorgettSexRemoveBlouse("georgett")
            "Растегнуть блузку" if bool(Georgett.clothing_layer("top")) and not Georgett.layer_raised("top") and not Georgett.sex_busy():
                call IntGeorgettSexUnbuttonBlouse("georgett")
            "Задрать юбочку" if bool(Georgett.clothing_layer("bottom")) and not Georgett.layer_raised("bottom") and not Georgett.sex_busy():
                call IntGeorgettSexRaiseSkirt("georgett")
            "Вытереть сперму с лица" if (Georgett.cum_state("cum_face_you") or Georgett.cum_state("cum_face_others")) and not Georgett.sex_busy():
                call GeorgettSexWipeFace
            "Вытереть сперму с грудей" if (Georgett.cum_state("cum_tits_you") or Georgett.cum_state("cum_tits_others")) and Georgett.tits_visible() and not Georgett.sex_busy():
                call GeorgettSexWipeTits
            "Вытереть сперму с бедер" if (Georgett.cum_state("cum_inside_you") or Georgett.cum_state("cum_inside_others")) and Georgett.pussy_visible() and not Georgett.sex_busy():
                call GeorgettSexWipeInside
            "Целовать" if not Georgett.sex_busy():
                call GeorgettSexKiss
            "Лапать" if not Georgett.sex_busy():
                call GeorgettSexGrope
            "Лизать киску" if Georgett.pussy_visible() and not Georgett.sex_busy():
                call GeorgettSexLick
            "Предложить отсосать" if player.intimacy.can_cum() and not Georgett.sex_busy():
                call GeorgettSexBlowjob
            "Трахать между грудей" if player.intimacy.can_cum() and not Georgett.sex_busy() and player.intimacy.arousal_value() >= 20 and Georgett.tits_visible() and Georgett.pregnancy_days() < 150:
                call GeorgettSexTitfuck
            "Трахать" if player.intimacy.can_cum() and not Georgett.sex_busy() and player.intimacy.arousal_value() >= 20 and Georgett.arousal_value() >= 20 and Georgett.pussy_visible():
                call GeorgettSexFuck
            "Продолжить" if Georgett.sex_busy():
                $ Georgett.set_sex_busy(0)
            "Кончить в ротик" if player.intimacy.can_cum() and player.intimacy.arousal_value() >= 100 and (Georgett.cock_in("mouth") or Georgett.cock_in("tits")):
                call GeorgettSexCumMouth
            "Кончить на лицо" if player.intimacy.can_cum() and player.intimacy.arousal_value() >= 100:
                call GeorgettSexCumFace
            "Кончить на груди" if player.intimacy.can_cum() and player.intimacy.arousal_value() >= 100 and Georgett.tits_visible():
                call GeorgettSexCumTits
            "Кончить внутрь" if player.intimacy.can_cum() and player.intimacy.arousal_value() >= 100 and Georgett.cock_in("pussy"):
                call GeorgettSexCumInside
            "Закончить":
                call GeorgettSexFinish
                return
        if str(scene_runtime.picture or "").strip():
            vscene scene_runtime.picture
    return


label GeorgettSexCumMouth(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Ваш дружок напрягся и струя за струей заполнил ротик [Georgett.real_name2()] вашим семенем. [Georgett.real_name()] судорожно заглатывала вашу сперму и потом высунула свой очаровательный язычок дабы продемонстрировать вам что она проглотила все.")
    $ Georgett.player_cum("mouth")
    call GeorgettSexStatus(GirlLocIGSS)
    $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cummouth")
    return


label GeorgettSexCumFace(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы вытащили вашего дружка в последний момент и густые струи вашего семени ударили прямо по пухленьким щечкам и белокурым кудрям [Georgett.real_name2()].")
    $ Georgett.player_cum("face")
    call GeorgettSexStatus(GirlLocIGSS)
    $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cummouth")
    return


label GeorgettSexCumTits(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы вытащили свой член из [Georgett.real_name2()] и немедленно разрядились на ее груди и живот. [Georgett.real_name()] провела пальцем по своим грудям а затем медленно, смотря вам в глаза, облизала измазанный спермой палец и улыбнулась.")
    $ Georgett.player_cum("tits")
    call GeorgettSexStatus(GirlLocIGSS)
    return


label GeorgettSexCumInside(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы зарычали и кончили. Густые струи вашего семени хлынули во влагалище [Georgett.real_name2()]. Блондинка, чувствуя как ее заполняет ваше семя, сладострастно застонала, приговаривая \"Да, милый, прямо в маточку твое семя ударило, сладко-то как. Так и залететь недолго!\"")
    $ georgett_sex_add_text("Ваш обмякший член вывалился из ненасытной щелки и из нее потекла вязкая белая струйка.")
    $ georgett_sex_set_picture(GirlNameIGSS, "sex", "doggyinside")
    $ Georgett.add_arousal(3)
    $ Georgett.player_cum("inside")
    call GeorgettSexStatus(GirlLocIGSS)
    return


label GeorgettSexLook(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text(Georgett.data.description)
    $ georgett_sex_set_portrait()
    return


label GeorgettSexWipeFace(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы предложили шлюшке убрать с лица результаты ее предыдущих похождений. [Georgett.real_name()] достала платочек и вытерла лицо и волосы от спермы.")
    $ Georgett.clear_cum("cum_face_you", "cum_face_others")
    $ georgett_sex_set_portrait()
    return


label GeorgettSexWipeTits(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы предложили шлюшке убрать с сисечек результаты ее предыдущих похождений. [Georgett.real_name()] достала платочек и вытерла свои груди от спермы.")
    $ Georgett.clear_cum("cum_tits_you", "cum_tits_others")
    $ georgett_sex_set_portrait()
    return


label GeorgettSexWipeInside(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("Вы предложили шлюшке убрать с влагалища и бедер результаты ее предыдущих похождений. [Georgett.real_name()] достала платочек и вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете.")
    $ Georgett.clear_cum("cum_inside_you", "cum_inside_others")
    $ georgett_sex_set_portrait()
    return


label GeorgettSexKiss(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    $ georgett_sex_add_text("[Georgett.real_name()] целует вас в засос, переплетаясь языками.")
    if Georgett.cum_state("cum_face_you") > 0:
        $ georgett_sex_add_text("На язык вам попадают капли вашего семени, которым вы обкончали ее раньше.")
    elif Georgett.cum_state("cum_face_others") > 0:
        $ georgett_sex_add_text("Вы чувствуете солоноватый привкус чужой спермы. Шалунья уже успела у кого-то отсосать до вас!")
    if Georgett.arousal_value() < 50:
        $ Georgett.add_arousal(7, 50)
    if player.intimacy.arousal_value() < 50:
        $ player.intimacy.add_arousal(7, 50)
    $ Georgett.set_cock_position("none")
    call GeorgettSexStatus(GirlLocIGSS)
    return


label GeorgettSexGrope(GirlNameIGSS="georgett", GirlLocIGSS="", _grope_text="", _lactate_tits_fondle=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    if not Georgett.tits_visible():
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
    if Georgett.pussy_visible():
        $ georgett_sex_add_text("Вы медленно опустили руку вниз, к ее вульвочке, и начали ее нежно массировать.")
    else:
        $ georgett_sex_add_text("Вы сунули руку под короткую юбочку и стали наминать ее вульву.")
    if Georgett.cum_state("cum_inside_you") > 0:
        $ georgett_sex_add_text("Вы почуствовали свою сперму в пещерке [Georgett.real_name2()].")
    elif Georgett.cum_state("cum_inside_others") > 0:
        $ georgett_sex_add_text("Ваши пальцы заскользили по пещерке [Georgett.real_name2()], похоже кто-то уже кончил в нее.")
    if not Georgett.tits_visible() and not Georgett.pussy_visible():
        $ georgett_sex_set_picture(GirlNameIGSS, "sex", "grope")
    if Georgett.arousal_value() < 60:
        $ Georgett.add_arousal(12, 60)
    $ Georgett.set_cock_position("none")
    call GeorgettSexStatus(GirlLocIGSS)
    return


label GeorgettSexLick(GirlNameIGSS="georgett", GirlLocIGSS="", _georgett_lick_count=0):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    if GirlLocIGSS == "tavern":
        $ georgett_sex_add_text("[Georgett.real_name()] легла на кровать и бесстыдно раздвинула ножки. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком.")
    else:
        $ georgett_sex_add_text("[Georgett.real_name()] стоя облокотилась спиной на стену, развинув бедра. Вы припали к раскрытому как цветок влагалищу и начали старательно ласкать его языком.")
    if Georgett.cum_state("cum_inside_you") > 0:
        $ georgett_sex_add_text("Вы ощущаете привкус собственной спермы, медленно вытекающей из влагалища [Georgett.real_name2()].")
    elif Georgett.cum_state("cum_inside_others") > 0:
        $ georgett_sex_add_text("Вы ощущаете привкус чьей-то спермы, медленно вытекающей из влагалища [Georgett.real_name2()], кто-то уже успел оттрахать эту куколку до вас.")
    $ _georgett_lick_count = Georgett.record_lick_pussy()
    if _georgett_lick_count == 4:
        $ georgett_sex_add_text("\"Ой, какой ты милый!\"  говорит [Georgett.real_name()]. \"Многие мои клиенты особо не утруждаются чтобы сделать девушке приятное, но ты, я вижу, не из таких.\"")
        $ Georgett.add_relation(1, 100)
    $ Georgett.add_arousal(20)
    $ Georgett.set_cock_position("none")
    call GeorgettSexStatus(GirlLocIGSS)
    return


label GeorgettSexBlowjob(GirlNameIGSS="georgett", GirlLocIGSS=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    if Georgett.cock_in("mouth"):
        $ georgett_sex_add_text("[Georgett.real_name()] сидит перед вами на корточках и продолжает ")
        $ georgett_sex_set_picture(GirlNameIGSS, "sex", "minet2")
    else:
        $ georgett_sex_add_text("[Georgett.real_name()] опустилась перед вами на корточки и стала ")
        $ georgett_sex_set_picture(GirlNameIGSS, "sex", "minet1")
    if player.intimacy.arousal_value() < 20:
        $ georgett_sex_add_text("облизывать ваш вялый член.")
    elif player.intimacy.arousal_value() < 40:
        $ georgett_sex_add_text("облизывать головку вашего напрягшегося члена.")
    elif player.intimacy.arousal_value() < 60:
        $ georgett_sex_add_text("умело сосать ваш член.")
    else:
        $ georgett_sex_add_text("заглатывать ваш член по самые яйца.")
    $ player.intimacy.add_arousal(20)
    $ Georgett.set_cock_position("mouth")
    call GeorgettSexStatus(GirlLocIGSS)
    return


label GeorgettSexTitfuck(GirlNameIGSS="georgett", GirlLocIGSS="", _lactate_tits_fuck=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
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
    $ player.intimacy.add_arousal(20)
    $ Georgett.set_cock_position("tits")
    call GeorgettSexStatus(GirlLocIGSS)
    return


label GeorgettSexFuck(GirlNameIGSS="georgett", GirlLocIGSS="", _lactate_pussy_fuck=""):
    $ GirlLocIGSS = str(GirlLocIGSS or Georgett.sex_location())
    $ georgett_sex_begin_text()
    if GirlLocIGSS == "tavern":
        if not Georgett.cock_in("pussy"):
            $ georgett_sex_add_text("Вы легли на кровать и усадили девицу прямо на возбужденный член, засадив по самые яйца.")
            if not Georgett.clothing_layer("top"):
                $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cowgirl3")
            else:
                $ georgett_sex_set_picture(GirlNameIGSS, "sex", "cowgirl1")
        else:
            $ georgett_sex_add_text("Она страстно скачет на вас, пока вы мнете ее ягодицы и сиськи.")
            if not Georgett.clothing_layer("top"):
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
    $ player.intimacy.add_arousal(20)
    $ Georgett.add_arousal(14)
    $ Georgett.set_cock_position("pussy")
    call GeorgettSexStatus(GirlLocIGSS)
    return

label GeorgettSexFinish:
    $ Georgett.set_sex_busy(0)
    call AdvanceTimeOnly(40)
    return
