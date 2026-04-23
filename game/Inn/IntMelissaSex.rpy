init python:
    def melissa_sex_available(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip().lower()
        return (
            melissa_bats_stage() >= 8
            and int(Friends.get(girl_key, 0) or 0) >= 12
            and int(otkroven.get(girl_key, 0) or 0) >= 4
        )

    def _ims_set_arousal(who, value):
        value = min(100, max(0, int(value or 0)))
        if str(who or "").lower() == "you":
            Arousal["You"] = value
            Arousal["you"] = value
            return
        Arousal[str(who or "").strip()] = value

    def _ims_prepare_scene_state(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip()
        topdress.setdefault(girl_key, "")
        bottomdress.setdefault(girl_key, "")
        bra.setdefault(girl_key, "")
        panties.setdefault(girl_key, "")
        topraised.setdefault(girl_key, 0)
        bottomraised.setdefault(girl_key, 0)
        TitsVisible.setdefault(girl_key, 0)
        PussyVisible.setdefault(girl_key, 0)
        CockInMouth.setdefault(girl_key, 0)
        CockInPussy.setdefault(girl_key, 0)
        CockInTits.setdefault(girl_key, 0)
        CumFaceYou.setdefault(girl_key, 0)
        CumFaceOthers.setdefault(girl_key, 0)
        CumTitsYou.setdefault(girl_key, 0)
        CumTitsOthers.setdefault(girl_key, 0)
        CumInsideYou.setdefault(girl_key, 0)
        CumInsideOthers.setdefault(girl_key, 0)
        Arousal.setdefault("You", 0)
        Arousal.setdefault("you", Arousal.get("You", 0))
        Arousal.setdefault(girl_key, int(PussyWetStart.get(girl_key, 0) or 0))
        GiveOrgasms.setdefault(girl_key, 0)
        LickPussy.setdefault(girl_key, 0)
        check_visibility(girl_key)
        return bodymodel_sync_character(girl_key, RealName.get(girl_key, girl_key), "female")

    def _ims_clear_contact_states(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip()
        CockInMouth[girl_key] = 0
        CockInPussy[girl_key] = 0
        CockInTits[girl_key] = 0

    def _ims_scene_summary(girl_name="melissa"):
        profile = _ims_prepare_scene_state(girl_name)
        return bodymodel_profile_summary_text(profile)

    def _ims_touch_text(girl_name="melissa", target_id="", action_id="", effect=None):
        girl_key = str(girl_name or "melissa").strip()
        target_key = str(target_id or "").strip()
        action_key = str(action_id or "").strip()
        effect = dict(effect or {})
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
            if int(TitsVisible.get(girl_key, 0) or 0) > 0:
                return "Вы ласкаете грудь Мелиссы уже без ткани между руками и телом. Ее соски быстро твердеют, а дыхание заметно сбивается."
            return "Вы начинаете ласкать грудь Мелиссы через одежду. Даже сквозь ткань ее тело отзывается заметной дрожью."
        if target_key == "nipples" and action_key == "lick":
            return "Вы склоняетесь к ее груди и проводите языком по затвердевшим соскам. Мелисса шумно втягивает воздух и прижимается к вам ближе."
        if target_key == "pussy" and action_key == "fondle":
            if int(PussyVisible.get(girl_key, 0) or 0) > 0:
                return "Ваши пальцы скользят по обнажившейся щели Мелиссы, разогревая ее еще сильнее."
            if int(bottomraised.get(girl_key, 0) or 0) > 0:
                return "Под задранной юбкой вы начинаете ласкать Мелиссу между ног через тонкую ткань. Она вздрагивает и шире разводит бедра."
            return "Вы осторожно проводите рукой по ее бедрам и промежности через юбку, разжигая Мелиссу даже сквозь одежду."
        if target_key == "pussy" and action_key == "spread":
            return "Вы разводите бедра Мелиссы чуть шире и заставляете ее раскрыться перед вами без слов."
        if target_key == "pussy" and action_key == "insert":
            state_text = str(effect.get("container_state", "") or "")
            if state_text in ("wet", "itchy and wet", "slurping"):
                return "Вы медленно вводите пальцы в уже влажную киску Мелиссы. Она тихо стонет и подается навстречу."
            return "Вы медленно вводите пальцы в Мелиссу, давая ей привыкнуть к глубине и темпу."
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
        gained_orgasms = max(0, int(GiveOrgasms.get(girl_key, 0) or 0) - int(start_orgasms or 0))
        _ims_clear_contact_states(girl_key)
        if gained_orgasms <= 0:
            Friends[girl_key] = min(20, int(Friends.get(girl_key, 0) or 0) + 1)
            return "Вы останавливаетесь прежде, чем довести Мелиссу до разрядки. Она еще тяжело дышит и просит в следующий раз не бросать ее на полпути."
        if gained_orgasms >= 2:
            Friends[girl_key] = min(20, int(Friends.get(girl_key, 0) or 0) + 2)
            sluttiness[girl_key] = min(100, int(sluttiness.get(girl_key, 0) or 0) + 3)
            otkroven[girl_key] = min(20, int(otkroven.get(girl_key, 0) or 0) + 2)
            return "Когда вы наконец останавливаетесь, Мелисса выглядит измученной, но довольной. Теперь рядом с вами она держится уже куда менее настороженно."
        Friends[girl_key] = min(20, int(Friends.get(girl_key, 0) or 0) + 2)
        sluttiness[girl_key] = min(100, int(sluttiness.get(girl_key, 0) or 0) + 2)
        otkroven[girl_key] = min(20, int(otkroven.get(girl_key, 0) or 0) + 1)
        return "Вы даете Мелиссе перевести дыхание и остановиться вместе с вами. По ее взгляду видно, что этот раз она запомнит как что-то по-настоящему важное."


label IntMelissaSex(GirlNameIMS="melissa", GirlLocIMS=""):
    hide screen main_ui
    if not melissa_sex_available(GirlNameIMS):
        return
    python:
        _ims_prepare_scene_state(GirlNameIMS)
        _ims_start_orgasms = int(GiveOrgasms.get(GirlNameIMS, 0) or 0)
        _ims_clear_contact_states(GirlNameIMS)
    if renpy.loadable("images/melissa/tavern/melissa_portrait.png"):
        call ShowImage("melissa", "", "portrait")

    label int_melissa_sex_menu:
        $ _ims_prepare_scene_state(GirlNameIMS)
        $ _ims_can_cum = int(Arousal.get("You", 0) or 0) >= 100 and int(cametoday or 0) < int(cancumdaily or 1)
        menu:
            "Осмотреть Мелиссу":
                $ MainTxt = _ims_scene_summary(GirlNameIMS)
                "[MainTxt]"
                jump int_melissa_sex_menu

            "Распахнуть блузку" if topdress.get(GirlNameIMS, "") != "" and int(topraised.get(GirlNameIMS, 0) or 0) == 0:
                "Вы медленно распахиваете блузку Мелиссы, открывая себе больше простора для рук и губ."
                $ topraised[GirlNameIMS] = 1
                $ _ims_prepare_scene_state(GirlNameIMS)
                jump int_melissa_sex_menu

            "Снять блузку" if topdress.get(GirlNameIMS, "") != "":
                "Вы стягиваете с Мелиссы блузку, оставляя ее верх куда менее защищенным."
                $ topdress[GirlNameIMS] = ""
                $ topraised[GirlNameIMS] = 0
                $ _ims_prepare_scene_state(GirlNameIMS)
                jump int_melissa_sex_menu

            "Снять лиф" if bra.get(GirlNameIMS, "") != "" and (topdress.get(GirlNameIMS, "") == "" or int(topraised.get(GirlNameIMS, 0) or 0) == 1):
                "Избавившись от лишней застежки, вы освобождаете грудь Мелиссы окончательно."
                $ bra[GirlNameIMS] = ""
                $ _ims_prepare_scene_state(GirlNameIMS)
                jump int_melissa_sex_menu

            "Поднять юбку" if bottomdress.get(GirlNameIMS, "") != "" and int(bottomraised.get(GirlNameIMS, 0) or 0) == 0:
                "Вы поднимаете юбку Мелиссы, открывая себе путь выше по ее бедрам."
                $ bottomraised[GirlNameIMS] = 1
                $ _ims_prepare_scene_state(GirlNameIMS)
                jump int_melissa_sex_menu

            "Снять юбку" if bottomdress.get(GirlNameIMS, "") != "":
                "Вы окончательно снимаете юбку Мелиссы, оставляя на ней лишь то, что ближе к телу."
                $ bottomdress[GirlNameIMS] = ""
                $ bottomraised[GirlNameIMS] = 0
                $ _ims_prepare_scene_state(GirlNameIMS)
                jump int_melissa_sex_menu

            "Снять панталончики" if panties.get(GirlNameIMS, "") != "" and (bottomdress.get(GirlNameIMS, "") == "" or int(bottomraised.get(GirlNameIMS, 0) or 0) == 1):
                "Вы стягиваете с Мелиссы панталончики, и теперь между вами и ее телом почти ничего не осталось."
                $ panties[GirlNameIMS] = ""
                $ _ims_prepare_scene_state(GirlNameIMS)
                jump int_melissa_sex_menu

            "Поцеловать Мелиссу":
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "mouth", "kiss", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "mouth", "kiss", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Ласкать грудь" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "nipples"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "nipples", "fondle", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "nipples", "fondle", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Лизнуть соски" if "lick" in bodymodel_actions_for_target(GirlNameIMS, "nipples"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "nipples", "lick", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "nipples", "lick", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Погладить ее между ног" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "fondle", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "fondle", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Раздвинуть ее бедра" if "spread" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "spread", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "spread", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Ввести пальцы в киску" if "insert" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "insert", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Лизать киску" if "lick" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "lick", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ LickPussy[GirlNameIMS] = int(LickPussy.get(GirlNameIMS, 0) or 0) + 1
                $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "lick", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Погладить ягодицы" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "fondle", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "ass", "fondle", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Раздвинуть ягодицы" if "spread" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "spread", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "ass", "spread", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Ввести палец в попку" if "insert" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "insert", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "ass", "insert", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Подставить ей член" if int(cametoday or 0) < int(cancumdaily or 1) and int(SomebodyCums or 0) == 0:
                $ _ims_clear_contact_states(GirlNameIMS)
                $ CockInMouth[GirlNameIMS] = 1
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "mouth", "suck", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                $ MainTxt = _ims_touch_text(GirlNameIMS, "mouth", "suck", _ims_effect)
                "[MainTxt]"
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Войти в нее" if int(cametoday or 0) < int(cancumdaily or 1) and int(SomebodyCums or 0) == 0 and int(PussyVisible.get(GirlNameIMS, 0) or 0) == 1 and int(Arousal.get("You", 0) or 0) >= 20 and int(Arousal.get(GirlNameIMS, 0) or 0) >= 20:
                $ _ims_clear_contact_states(GirlNameIMS)
                $ CockInPussy[GirlNameIMS] = 1
                $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", RealName.get(GirlNameIMS, GirlNameIMS), "female")
                "Вы входите в Мелиссу медленно, оставляя ей время принять ваш темп и глубину."
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_menu

            "Кончить в рот" if _ims_can_cum and int(CockInMouth.get(GirlNameIMS, 0) or 0) == 1:
                "Поймав взгляд Мелиссы, вы больше не сдерживаетесь и кончаете ей в рот."
                $ PregnancyCheck(GirlNameIMS, "mouth", 1, "Вы")
                $ cametoday = int(cametoday or 0) + 1
                $ _ims_set_arousal("You", 0)
                $ CumFaceYou[GirlNameIMS] = 1
                $ SomebodyCums = 1
                $ _ims_clear_contact_states(GirlNameIMS)
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_after_cum

            "Кончить на лицо" if _ims_can_cum:
                "Вы выходите из близости в последний момент и кончаете Мелиссе на лицо."
                $ PregnancyCheck(GirlNameIMS, "face", 1, "Вы")
                $ cametoday = int(cametoday or 0) + 1
                $ _ims_set_arousal("You", 0)
                $ CumFaceYou[GirlNameIMS] = 1
                $ SomebodyCums = 1
                $ _ims_clear_contact_states(GirlNameIMS)
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_after_cum

            "Кончить внутрь" if _ims_can_cum and int(CockInPussy.get(GirlNameIMS, 0) or 0) == 1:
                "Вы удерживаете Мелиссу ближе к себе и кончаете прямо в нее."
                $ PregnancyCheck(GirlNameIMS, "inside", 1, "Вы")
                $ cametoday = int(cametoday or 0) + 1
                $ _ims_set_arousal("You", 0)
                $ CumInsideYou[GirlNameIMS] = 1
                $ SomebodyCums = 1
                $ _ims_clear_contact_states(GirlNameIMS)
                call ShowCurrentSex(GirlNameIMS)
                jump int_melissa_sex_after_cum

            "Остановиться":
                jump int_melissa_sex_finish


label int_melissa_sex_after_cum:
    menu:
        "Продолжить":
            $ SomebodyCums = 0
            jump int_melissa_sex_menu

        "Закончить":
            $ SomebodyCums = 0
            jump int_melissa_sex_finish


label int_melissa_sex_finish:
    $ MainTxt = _ims_finish_scene(GirlNameIMS, _ims_start_orgasms)
    "[MainTxt]"
    $ _ims_set_arousal("You", 0)
    $ _ims_set_arousal(GirlNameIMS, 0)
    $ SomebodyCums = 0
    call DressUp(GirlNameIMS)
    $ _ims_prepare_scene_state(GirlNameIMS)
    return
