# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _ims_has_dildo():
        for item_id in ("dildo_001", "wooden_dildo_001", "glass_dildo_001"):
            try:
                if int(player.item_count(item_id) or 0) > 0:
                    return True
            except Exception:
                pass
        return False

    def _ims_finish_inside_text(girl_name="melissa", container_id=""):
        container_key = str(container_id or "").strip().lower()
        if container_key == "ass":
            return "Вы удерживаете Мелиссу ближе к себе и кончаете внутрь."
        return "Вы удерживаете Мелиссу ближе к себе и кончаете прямо в нее."

    def _ims_scene_summary(girl_name="melissa"):
        profile = bodymodel_build_profile(girl_name, Melissa.data.fullname, "female")
        lines = []
        if not Melissa.relationship_allows("sex"):
            lines.append("Сейчас это еще не полноценный секс, а осторожное сближение. Мелисса позволяет поцелуи, ласки и все более смелые прикосновения, но пока ее комнатная история с летучими мышами не закрыта и она не вернулась к себе, дальше заходить рано.")
        else:
            lines.append("Мелисса уже готова к полноценной близости, если вы не будете терять ритм и внимание к ее состоянию.")
        lines.append(bodymodel_profile_summary_text(profile))
        return "\n\n".join([row for row in lines if str(row or "").strip() != ""])

    def _ims_clamp_engagement_arousal(girl_name="melissa"):
        if Melissa.relationship_allows("sex"):
            return
        player.intimacy.set_arousal(min(85, player.intimacy.arousal_value()))
        Melissa.set_arousal(min(90, Melissa.arousal_value()))

    def _ims_touch_text(girl_name="melissa", target_id="", action_id="", effect=None):
        girl_key = str(girl_name or "melissa").strip()
        target_key = str(target_id or "").strip()
        action_key = str(action_id or "").strip()
        effect = dict(effect or {})
        if not Melissa.relationship_allows("sex"):
            _ims_clamp_engagement_arousal(girl_key)
        if not bool(effect.get("allowed", False)):
            if target_key == "nipples":
                return "Одежда Мелиссы все еще мешает добраться до ее груди как следует."
            if target_key == "pussy":
                return "Пока на Мелиссе остается слишком много одежды, дальше осторожных ласк вы не продвинетесь."
            if target_key == "ass":
                return "Сквозь оставшуюся одежду до ее попки сейчас не добраться как следует."
            return "Сейчас это не выйдет."
        if target_key == "mouth" and action_key == "kiss":
            return "Вы мягко целуете Мелиссу. Она сперва замирает, потом отвечает куда охотнее, чем в первые ваши осторожные вечера."
        if target_key == "nipples" and action_key == "fondle":
            if Melissa.tits_visible():
                return "Вы ласкаете грудь Мелиссы уже без ткани между руками и телом. Ее соски быстро твердеют, а дыхание заметно сбивается."
            return "Вы начинаете ласкать грудь Мелиссы через одежду. Даже сквозь ткань ее тело отзывается заметной дрожью."
        if target_key == "nipples" and action_key == "lick":
            return "Вы склоняетесь к ее груди и проводите языком по затвердевшим соскам. Мелисса шумно втягивает воздух и прижимается к вам ближе."
        if target_key == "pussy" and action_key == "fondle":
            if Melissa.pussy_visible():
                return "Ваши пальцы скользят по обнажившейся щели Мелиссы, разогревая ее еще сильнее."
            if Melissa.layer_raised("bottom"):
                return "Под задранной юбкой вы начинаете ласкать Мелиссу между ног через тонкую ткань. Она вздрагивает и шире разводит бедра."
            return "Вы осторожно проводите рукой по ее бедрам и промежности через юбку, разжигая Мелиссу даже сквозь одежду."
        if target_key == "pussy" and action_key == "spread":
            return "Вы разводите бедра Мелиссы чуть шире и заставляете ее раскрыться перед вами без слов."
        if target_key == "pussy" and action_key == "insert":
            state_text = str(effect.get("container_state", "") or "")
            if state_text in ("wet", "itchy and wet", "slurping"):
                return "Вы медленно вводите пальцы в уже влажную киску Мелиссы. Она тихо стонет и подается навстречу."
            return "Вы медленно вводите пальцы в Мелиссу, давая ей привыкнуть к глубине и темпу."
        if target_key == "pussy" and action_key == "toy_insert":
            state_text = str(effect.get("container_state", "") or "")
            if state_text in ("wet", "itchy and wet", "slurping"):
                return "С игрушкой выходит легче: Мелисса уже достаточно влажная, чтобы принять ее без лишнего напряжения."
            return "Вы начинаете очень осторожно, пока Мелисса привыкает к форме и давлению игрушки."
        if target_key == "pussy" and action_key == "lick":
            return "Вы опускаетесь ниже и начинаете вылизывать Мелиссу. Ее тело тут же напрягается, а потом дрожь пробегает от живота до колен."
        if target_key == "ass" and action_key == "fondle":
            return "Вы сжимаете и гладите ягодицы Мелиссы, чувствуя, как она вся становится еще чувствительнее к вашим рукам."
        if target_key == "ass" and action_key == "spread":
            return "Вы раздвигаете ягодицы Мелиссы и заставляете ее замереть в особенно уязвимой позе."
        if target_key == "ass" and action_key == "insert":
            return "Смочив пальцы, вы осторожно разрабатываете попку Мелиссы. Она напрягается, но не пытается вас остановить."
        if target_key == "mouth" and action_key == "suck":
            return "Мелисса берет ваш член в рот и постепенно привыкает к ритму, послушно ловя ваши движения губами и языком."
        return "Между вами становится еще меньше расстояния."

    def _ims_finish_scene(girl_name="melissa", start_orgasms=0):
        girl_key = str(girl_name or "melissa").strip()
        if not Melissa.relationship_allows("sex"):
            Melissa.set_cock_position("none")
            Melissa.change_social(friend_delta=1, corruption_delta=1)
            return "Вы останавливаетесь до того, как близость сорвется в настоящий секс. Мелисса еще тяжело дышит, поправляет одежду и смотрит на вас уже мягче: этот вечер остался на грани, но именно поэтому она не чувствует себя загнанной."
        gained_orgasms = max(0, int(Melissa.sex_stat("orgasms_given", 0) or 0) - int(start_orgasms or 0))
        Melissa.set_cock_position("none")
        if gained_orgasms <= 0:
            Melissa.change_social(friend_delta=1)
            return "Вы останавливаетесь прежде, чем довести Мелиссу до разрядки. Она еще тяжело дышит и просит в следующий раз не бросать ее на полпути."
        if gained_orgasms >= 2:
            Melissa.change_social(friend_delta=2, open_delta=2, corruption_delta=3)
            return "Когда вы наконец останавливаетесь, Мелисса выглядит измученной, но довольной. Теперь рядом с вами она держится уже куда менее настороженно."
        Melissa.change_social(friend_delta=2, open_delta=1, corruption_delta=2)
        return "Вы даете Мелиссе перевести дыхание и остановиться вместе с вами. По ее взгляду видно, что этот раз она запомнит как что-то по-настоящему важное."


label IntMelissaSex(GirlNameIMS="melissa", GirlLocIMS=""):
    $ renpy.dynamic("_ims_effect", "_ims_melissa_picture", "_ims_stage", "_ims_full_engine", "_ims_can_cum", "_ims_inside_container", "_ims_start_orgasms")
    if not (Melissa.relationship_allows("intimacy") and Melissa.room_is_private(GirlLocIMS or rooms.current_code)):
        $ scene_runtime.text = "Для такого между вами уже нужно место без чужих взглядов. Здесь слишком открыто."
        $ scene_runtime.location_text = scene_runtime.text
        return
    python:
        Melissa.ensure_sex_state()
        _ims_start_orgasms = int(Melissa.sex_stat("orgasms_given", 0) or 0)
        Melissa.set_cock_position("none")
    $ main_ui_begin_native_scene_state("Мелисса")
    $ _ims_melissa_picture = MelissaStaticData.image_path("portrait", "default")
    if str(_ims_melissa_picture or "").strip():
        $ scene_runtime.picture = _ims_melissa_picture
        vscene scene_runtime.picture
    $ scene_runtime.text = _ims_scene_summary(GirlNameIMS)
    $ scene_runtime.location_text = scene_runtime.text

    label int_melissa_sex_menu:
        while True:
            $ _ims_stage = Melissa.relationship_stage()
            $ _ims_full_engine = Melissa.relationship_allows("sex")
            $ _ims_can_cum = _ims_full_engine and player.intimacy.arousal_value() >= 100 and player.intimacy.came_today < player.intimacy.can_cum_daily
            menu:
                "Осмотреть Мелиссу":
                    $ scene_runtime.text = _ims_scene_summary(GirlNameIMS)
                    $ scene_runtime.picture = MelissaStaticData.image_path("portrait", "default")

                "Распахнуть блузку" if _ims_stage >= 3 and Melissa.clothing_layer("top") != "" and not Melissa.layer_raised("top"):
                    $ scene_runtime.text = "Вы медленно распахиваете блузку Мелиссы, открывая себе больше простора для рук и губ."
                    $ Melissa.set_layer_raised("top", 1)

                "Снять блузку" if _ims_stage >= 3 and Melissa.clothing_layer("top") != "":
                    $ scene_runtime.text = "Вы стягиваете с Мелиссы блузку, оставляя ее верх куда менее защищенным."
                    $ Melissa.remove_clothing_layer("top")
                    $ Melissa.set_layer_raised("top", 0)

                "Снять лиф" if _ims_stage >= 3 and Melissa.clothing_layer("bra") != "" and (Melissa.clothing_layer("top") == "" or Melissa.layer_raised("top")):
                    $ scene_runtime.text = "Избавившись от лишней застежки, вы освобождаете грудь Мелиссы окончательно."
                    $ Melissa.remove_clothing_layer("bra")

                "Поднять юбку" if _ims_stage >= 3 and Melissa.clothing_layer("bottom") != "" and not Melissa.layer_raised("bottom"):
                    $ scene_runtime.text = "Вы поднимаете юбку Мелиссы, открывая себе путь выше по ее бедрам."
                    $ Melissa.set_layer_raised("bottom", 1)

                "Снять юбку" if _ims_stage >= 3 and Melissa.clothing_layer("bottom") != "":
                    $ scene_runtime.text = "Вы окончательно снимаете юбку Мелиссы, оставляя на ней лишь то, что ближе к телу."
                    $ Melissa.remove_clothing_layer("bottom")
                    $ Melissa.set_layer_raised("bottom", 0)

                "Снять панталончики" if _ims_stage >= 4 and Melissa.clothing_layer("panties") != "" and (Melissa.clothing_layer("bottom") == "" or Melissa.layer_raised("bottom")):
                    $ scene_runtime.text = "Вы стягиваете с Мелиссы панталончики, и теперь между вами и ее телом почти ничего не осталось."
                    $ Melissa.remove_clothing_layer("panties")

                "Поцеловать Мелиссу":
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "mouth", "kiss", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "mouth", "kiss", _ims_effect)
                    $ scene_runtime.picture = MelissaStaticData.image_path("portrait", "default")
                    call IntMelissaSexState(GirlNameIMS)

                "Ласкать грудь" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "nipples"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "nipples", "fondle", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "nipples", "fondle", _ims_effect)
                    $ scene_runtime.picture = MelissaStaticData.image_path("grope", "tit_ok" if _ims_full_engine else "tits_shy")
                    call IntMelissaSexState(GirlNameIMS)

                "Лизнуть соски" if "lick" in bodymodel_actions_for_target(GirlNameIMS, "nipples"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "nipples", "lick", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "nipples", "lick", _ims_effect)
                    $ scene_runtime.picture = MelissaStaticData.image_path("grope", "tit_ok")
                    call IntMelissaSexState(GirlNameIMS)

                "Погладить ее между ног" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "fondle", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "pussy", "fondle", _ims_effect)
                    $ scene_runtime.picture = MelissaStaticData.image_path("grope", "ass_ok")
                    call IntMelissaSexState(GirlNameIMS)

                "Раздвинуть ее бедра" if _ims_full_engine and "spread" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "spread", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "pussy", "spread", _ims_effect)
                    call IntMelissaSexState(GirlNameIMS)

                "Ввести пальцы в киску" if _ims_full_engine and "insert" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "pussy", "insert", _ims_effect)
                    call IntMelissaSexState(GirlNameIMS)

                "Использовать игрушку" if _ims_full_engine and _ims_has_dildo() and "insert" in bodymodel_actions_for_target(GirlNameIMS, "pussy") and Melissa.arousal_value() >= 20:
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", Melissa.data.fullname, "female")
                    $ _ims_effect["action"] = "toy_insert"
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "pussy", "toy_insert", _ims_effect)
                    call IntMelissaSexState(GirlNameIMS)

                "Лизать киску" if _ims_full_engine and "lick" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "lick", "You", Melissa.data.fullname, "female")
                    $ Melissa.record_lick_pussy()
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "pussy", "lick", _ims_effect)
                    call IntMelissaSexState(GirlNameIMS)

                "Погладить ягодицы" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "fondle", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "ass", "fondle", _ims_effect)
                    $ scene_runtime.picture = MelissaStaticData.image_path("grope", "ass_ok")
                    call IntMelissaSexState(GirlNameIMS)

                "Раздвинуть ягодицы" if _ims_full_engine and "spread" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "spread", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "ass", "spread", _ims_effect)
                    call IntMelissaSexState(GirlNameIMS)

                "Ввести палец в попку" if _ims_full_engine and "insert" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "insert", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "ass", "insert", _ims_effect)
                    call IntMelissaSexState(GirlNameIMS)

                "Подставить ей член" if _ims_full_engine and player.intimacy.came_today < player.intimacy.can_cum_daily and not Melissa.sex_busy():
                    $ Melissa.set_cock_position("mouth")
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "mouth", "suck", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = _ims_touch_text(GirlNameIMS, "mouth", "suck", _ims_effect)
                    $ scene_runtime.picture = MelissaStaticData.cycle_image("sexy_times", "blowjob", Melissa.arousal_value())
                    call IntMelissaSexState(GirlNameIMS)

                "Войти в нее" if _ims_full_engine and player.intimacy.came_today < player.intimacy.can_cum_daily and not Melissa.sex_busy() and Melissa.pussy_visible() and player.intimacy.arousal_value() >= 20 and Melissa.arousal_value() >= 20:
                    $ Melissa.set_cock_position("pussy")
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", Melissa.data.fullname, "female")
                    $ scene_runtime.text = "Вы входите в Мелиссу медленно, оставляя ей время принять ваш темп и глубину."
                    call IntMelissaSexState(GirlNameIMS)

                "Войти сзади" if _ims_full_engine and player.intimacy.came_today < player.intimacy.can_cum_daily and not Melissa.sex_busy() and "insert" in bodymodel_actions_for_target(GirlNameIMS, "ass") and player.intimacy.arousal_value() >= 30 and Melissa.arousal_value() >= 40:
                    $ Melissa.set_cock_position("ass")
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "insert", "You", Melissa.data.fullname, "female")
                    if threads["claraTavernVisit"].completed and int(threads["claraForestSofa"].num or 0) >= 1 and not bool(threads["claraForestSofa"].aborted):
                        $ scene_runtime.text = "Вспомнив советы Клариссы, Мелисса сама задает медленный темп и показывает, когда можно продолжить. Вы входите сзади без спешки; она привыкает к новому давлению и не позволяет вам торопиться."
                    else:
                        $ scene_runtime.text = "Вы входите сзади, медленно и без спешки. Мелисса вцепляется в край стола и привыкает к новому давлению."
                    call IntMelissaSexState(GirlNameIMS)

                "Кончить в рот" if _ims_can_cum and Melissa.cock_in("mouth"):
                    $ scene_runtime.text = "Поймав взгляд Мелиссы, вы больше не сдерживаетесь и кончаете ей в рот."
                    $ pregnancy_check(GirlNameIMS, "mouth", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ Melissa.set_cum_state("cum_face_you", 1)
                    $ Melissa.set_sex_busy(True)
                    $ Melissa.set_cock_position("none")
                    $ scene_runtime.picture = MelissaStaticData.image_path("sexy_times", "blowjob_finish")
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call int_melissa_sex_after_cum
                    if _return:
                        return

                "Кончить на лицо" if _ims_can_cum:
                    $ scene_runtime.text = "Вы выходите из близости в последний момент и кончаете Мелиссе на лицо."
                    $ pregnancy_check(GirlNameIMS, "face", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ Melissa.set_cum_state("cum_face_you", 1)
                    $ Melissa.set_sex_busy(True)
                    $ Melissa.set_cock_position("none")
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call int_melissa_sex_after_cum
                    if _return:
                        return

                "Кончить внутрь" if _ims_can_cum and Melissa.cock_position() in ("pussy", "ass"):
                    $ _ims_inside_container = Melissa.cock_position()
                    $ scene_runtime.text = _ims_finish_inside_text(GirlNameIMS, _ims_inside_container)
                    if _ims_inside_container == "pussy":
                        $ pregnancy_check(GirlNameIMS, "inside", 1, "Вы")
                    else:
                        $ pregnancy_check(GirlNameIMS, "outside", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ Melissa.set_cum_state("cum_inside_you", 1)
                    $ Melissa.set_sex_busy(True)
                    $ Melissa.set_cock_position("none")
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call int_melissa_sex_after_cum
                    if _return:
                        return

                "Попросить Мелиссу помочь вам" if (not _ims_full_engine) and player_can_ask_intimacy_help(GirlNameIMS):
                    call PlayerIntimacyHelpAsk(GirlNameIMS, "IntMelissaSexState")

                "Остановиться":
                    call int_melissa_sex_finish
                    return

            $ scene_runtime.location_text = scene_runtime.text
            if str(scene_runtime.picture or "").strip():
                vscene scene_runtime.picture


label IntMelissaSexState(girl_name="melissa"):
    $ renpy.dynamic("_ims_state_lines", "_ims_state_text", "_ims_orgasm_count")
    $ _ims_clamp_engagement_arousal(girl_name)
    $ _ims_state_lines = []
    if player.intimacy.arousal_value() >= 100:
        $ _ims_state_lines.append("Вы уже готовы кончить и можете выбрать, как закончить.")
    if Melissa.arousal_value() >= 100:
        $ _ims_state_lines.append("Мелисса забилась в судорогах оргазма, выгнулась дугой и со счастливым вздохом обмякла в ваших руках.")
        $ _ims_orgasm_count = Melissa.record_orgasm_given()
        if Melissa.cock_in("pussy"):
            $ Melissa.set_arousal(20)
        else:
            $ Melissa.set_arousal(0)
        $ Melissa.set_sex_stat("last_orgasm_day", current_game_day())
    $ _ims_state_text = bodymodel_profile_summary_text(bodymodel_build_profile(girl_name, Melissa.data.fullname, "female"))
    if str(_ims_state_text or "").strip():
        $ _ims_state_lines.append(_ims_state_text)
    if _ims_state_lines:
        $ scene_runtime.text = str(scene_runtime.text or "").strip() + "\n\n" + "\n\n".join(_ims_state_lines)
    $ scene_runtime.location_text = scene_runtime.text
    return


label int_melissa_sex_after_cum:
    menu:
        "Продолжить":
            $ Melissa.set_sex_busy(False)
            return False

        "Закончить":
            $ Melissa.set_sex_busy(False)
            call int_melissa_sex_finish
            return True


label int_melissa_sex_finish:
    $ scene_runtime.text = _ims_finish_scene(GirlNameIMS, _ims_start_orgasms)
    $ scene_runtime.location_text = scene_runtime.text
    $ Melissa.mark_fucked()
    $ player.intimacy.set_arousal(0)
    $ Melissa.set_arousal(0)
    $ Melissa.set_sex_busy(False)
    call DressUp(GirlNameIMS)
    $ main_ui_end_native_scene_state()
    return
