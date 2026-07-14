# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def melissa_sex_available(girl_name="melissa"):
        return melissa_relationship_allows(girl_name, "sex")

    def melissa_intimacy_available(girl_name="melissa", room_code=""):
        return melissa_relationship_allows(girl_name, "intimacy") and melissa_room_is_private(room_code or CurLoc)

    def melissa_intimacy_is_engagement(girl_name="melissa"):
        return not melissa_sex_available(girl_name)

    def _ims_player_cum_count():
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        if isinstance(player.intimacy.came_today, dict):
            return int(player.intimacy.came_today.get("You", player.intimacy.came_today.get("you", 0)) or 0)
        return int(player.intimacy.came_today or 0)

    def _ims_player_cum_limit():
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        if isinstance(player.intimacy.can_cum_daily, dict):
            return int(player.intimacy.can_cum_daily.get("You", player.intimacy.can_cum_daily.get("you", 1)) or 1)
        return int(player.intimacy.can_cum_daily or 1)

    def _ims_has_dildo():
        for item_id in ("dildo_001", "wooden_dildo_001", "glass_dildo_001"):
            try:
                if int(player.item_count(item_id) or 0) > 0:
                    return True
            except Exception:
                pass
        return False

    def _ims_count_sex_time(girl_name="melissa"):
        Melissa.var["sex_times_today"] = max(0, int(Melissa.var.get("sex_times_today", 0) or 0)) + 1

    def _ims_set_arousal(who, value):
        value = min(100, max(0, int(value or 0)))
        if str(who or "").lower() == "you":
            player.intimacy.set_arousal(value, "You")
            return
        info = getPersonInfo(who)
        if info is not None and hasattr(info, "set_arousal"):
            info.set_arousal(value)

    def _ims_arousal(who):
        if str(who or "").lower() == "you":
            return int(player.intimacy.arousal_value("You") or 0)
        info = getPersonInfo(who)
        return int(info.arousal_value() or 0) if info is not None and hasattr(info, "arousal_value") else 0

    def _ims_prepare_scene_state(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip()
        topdress.setdefault(girl_key, "")
        bottomdress.setdefault(girl_key, "")
        bra.setdefault(girl_key, "")
        panties.setdefault(girl_key, "")
        topraised.setdefault(girl_key, 0)
        bottomraised.setdefault(girl_key, 0)
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
        CockInAss.setdefault(girl_key, 0)
        CockInTits.setdefault(girl_key, 0)
        SexInsertedContainer.setdefault(girl_key, "")
        CumFaceYou.setdefault(girl_key, 0)
        CumFaceOthers.setdefault(girl_key, 0)
        CumTitsYou.setdefault(girl_key, 0)
        CumTitsOthers.setdefault(girl_key, 0)
        CumInsideYou.setdefault(girl_key, 0)
        CumInsideOthers.setdefault(girl_key, 0)
        _ims_set_arousal(girl_key, int(Melissa.stats.get("PussyWetStart", 0) or 0))
        GiveOrgasms.setdefault(girl_key, 0)
        LickPussy.setdefault(girl_key, 0)
        check_visibility(girl_key)
        return bodymodel_sync_character(girl_key, Melissa.data.fullname, "female")

    def _ims_clear_contact_states(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip()
        CockInMouth[girl_key] = 0
        CockInPussy[girl_key] = 0
        CockInAss[girl_key] = 0
        CockInTits[girl_key] = 0
        SexInsertedContainer[girl_key] = ""

    def _ims_set_inserted_container(girl_name="melissa", container_id=""):
        girl_key = str(girl_name or "melissa").strip()
        container_key = str(container_id or "").strip().lower()
        _ims_clear_contact_states(girl_key)
        if container_key == "mouth":
            CockInMouth[girl_key] = 1
        elif container_key == "pussy":
            CockInPussy[girl_key] = 1
        elif container_key == "ass":
            CockInAss[girl_key] = 1
        elif container_key == "tits":
            CockInTits[girl_key] = 1
        else:
            container_key = ""
        SexInsertedContainer[girl_key] = container_key
        return container_key

    def _ims_current_inserted_container(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip()
        if int(CockInPussy.get(girl_key, 0) or 0) == 1:
            return "pussy"
        if int(CockInAss.get(girl_key, 0) or 0) == 1:
            return "ass"
        if int(CockInMouth.get(girl_key, 0) or 0) == 1:
            return "mouth"
        return str(SexInsertedContainer.get(girl_key, "") or "")

    def _ims_finish_inside_text(girl_name="melissa", container_id=""):
        container_key = str(container_id or "").strip().lower()
        if container_key == "ass":
            return "Вы удерживаете Мелиссу ближе к себе и кончаете внутрь."
        return "Вы удерживаете Мелиссу ближе к себе и кончаете прямо в нее."

    def _ims_scene_summary(girl_name="melissa"):
        profile = _ims_prepare_scene_state(girl_name)
        lines = []
        if melissa_intimacy_is_engagement(girl_name):
            lines.append("Сейчас это еще не полноценный секс, а осторожное сближение. Мелисса позволяет поцелуи, ласки и все более смелые прикосновения, но пока ее комнатная история с летучими мышами не закрыта и она не вернулась к себе, дальше заходить рано.")
        else:
            lines.append("Мелисса уже готова к полноценной близости, если вы не будете терять ритм и внимание к ее состоянию.")
        lines.append(bodymodel_profile_summary_text(profile))
        return "\n\n".join([row for row in lines if str(row or "").strip() != ""])

    def _ims_engagement_state_text(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip()
        _ims_clamp_engagement_arousal(girl_key)
        state = bodymodel_profile_summary_text(_ims_prepare_scene_state(girl_key))
        return "Вы оба уже заметно разгорячены, но это все еще стадия сближения: поцелуи, руки под тканью, тяжелое дыхание и остановки до той черты, после которой начнется настоящий секс.\n\n" + state

    def _ims_clamp_engagement_arousal(girl_name="melissa"):
        girl_key = str(girl_name or "melissa").strip()
        if melissa_sex_available(girl_key):
            return
        _ims_set_arousal("You", min(85, _ims_arousal("You")))
        _ims_set_arousal(girl_key, min(90, _ims_arousal(girl_key)))

    def _ims_touch_text(girl_name="melissa", target_id="", action_id="", effect=None):
        girl_key = str(girl_name or "melissa").strip()
        target_key = str(target_id or "").strip()
        action_key = str(action_id or "").strip()
        effect = dict(effect or {})
        if melissa_intimacy_is_engagement(girl_key):
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
        if melissa_intimacy_is_engagement(girl_key):
            _ims_clear_contact_states(girl_key)
            Melissa.change_social(friend_delta=1, corruption_delta=1)
            return "Вы останавливаетесь до того, как близость сорвется в настоящий секс. Мелисса еще тяжело дышит, поправляет одежду и смотрит на вас уже мягче: этот вечер остался на грани, но именно поэтому она не чувствует себя загнанной."
        gained_orgasms = max(0, int(GiveOrgasms.get(girl_key, 0) or 0) - int(start_orgasms or 0))
        _ims_clear_contact_states(girl_key)
        if gained_orgasms <= 0:
            Melissa.change_social(friend_delta=1)
            return "Вы останавливаетесь прежде, чем довести Мелиссу до разрядки. Она еще тяжело дышит и просит в следующий раз не бросать ее на полпути."
        if gained_orgasms >= 2:
            Melissa.change_social(friend_delta=2, open_delta=2, corruption_delta=3)
            return "Когда вы наконец останавливаетесь, Мелисса выглядит измученной, но довольной. Теперь рядом с вами она держится уже куда менее настороженно."
        Melissa.change_social(friend_delta=2, open_delta=1, corruption_delta=2)
        return "Вы даете Мелиссе перевести дыхание и остановиться вместе с вами. По ее взгляду видно, что этот раз она запомнит как что-то по-настоящему важное."


label IntMelissaSex(GirlNameIMS="melissa", GirlLocIMS=""):
    if not melissa_intimacy_available(GirlNameIMS, GirlLocIMS):
        $ MainTxt = "Для такого между вами уже нужно место без чужих взглядов. Здесь слишком открыто."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(GirlNameIMS)
        return
    python:
        _ims_prepare_scene_state(GirlNameIMS)
        _ims_start_orgasms = int(GiveOrgasms.get(GirlNameIMS, 0) or 0)
        _ims_clear_contact_states(GirlNameIMS)
        _ims_scene_counted = False
    $ _ims_melissa_picture = Melissa.image_path("portrait", "default")
    if str(_ims_melissa_picture or "").strip():
        call ShowImage("", "", _ims_melissa_picture)

    label int_melissa_sex_menu:
        while True:
            $ _ims_prepare_scene_state(GirlNameIMS)
            $ _ims_stage = melissa_relationship_stage(GirlNameIMS)
            $ _ims_full_engine = melissa_sex_available(GirlNameIMS)
            $ _ims_can_cum = _ims_full_engine and _ims_arousal("You") >= 100 and _ims_player_cum_count() < _ims_player_cum_limit()
            menu:
                "Осмотреть Мелиссу":
                    $ MainTxt = _ims_scene_summary(GirlNameIMS)
                    "[MainTxt]"

                "Распахнуть блузку" if _ims_stage >= 3 and topdress.get(GirlNameIMS, "") != "" and int(topraised.get(GirlNameIMS, 0) or 0) == 0:
                    "Вы медленно распахиваете блузку Мелиссы, открывая себе больше простора для рук и губ."
                    $ topraised[GirlNameIMS] = 1
                    $ _ims_prepare_scene_state(GirlNameIMS)

                "Снять блузку" if _ims_stage >= 3 and topdress.get(GirlNameIMS, "") != "":
                    "Вы стягиваете с Мелиссы блузку, оставляя ее верх куда менее защищенным."
                    $ Melissa.remove_clothing_layer("top")
                    $ Melissa.set_layer_raised("top", 0)
                    $ _ims_prepare_scene_state(GirlNameIMS)

                "Снять лиф" if _ims_stage >= 3 and bra.get(GirlNameIMS, "") != "" and (topdress.get(GirlNameIMS, "") == "" or int(topraised.get(GirlNameIMS, 0) or 0) == 1):
                    "Избавившись от лишней застежки, вы освобождаете грудь Мелиссы окончательно."
                    $ bra[GirlNameIMS] = ""
                    $ _ims_prepare_scene_state(GirlNameIMS)

                "Поднять юбку" if _ims_stage >= 3 and bottomdress.get(GirlNameIMS, "") != "" and int(bottomraised.get(GirlNameIMS, 0) or 0) == 0:
                    "Вы поднимаете юбку Мелиссы, открывая себе путь выше по ее бедрам."
                    $ bottomraised[GirlNameIMS] = 1
                    $ _ims_prepare_scene_state(GirlNameIMS)

                "Снять юбку" if _ims_stage >= 3 and bottomdress.get(GirlNameIMS, "") != "":
                    "Вы окончательно снимаете юбку Мелиссы, оставляя на ней лишь то, что ближе к телу."
                    $ Melissa.remove_clothing_layer("bottom")
                    $ Melissa.set_layer_raised("bottom", 0)
                    $ _ims_prepare_scene_state(GirlNameIMS)

                "Снять панталончики" if _ims_stage >= 4 and panties.get(GirlNameIMS, "") != "" and (bottomdress.get(GirlNameIMS, "") == "" or int(bottomraised.get(GirlNameIMS, 0) or 0) == 1):
                    "Вы стягиваете с Мелиссы панталончики, и теперь между вами и ее телом почти ничего не осталось."
                    $ panties[GirlNameIMS] = ""
                    $ _ims_prepare_scene_state(GirlNameIMS)

                "Поцеловать Мелиссу":
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "mouth", "kiss", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "mouth", "kiss", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Ласкать грудь" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "nipples"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "nipples", "fondle", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "nipples", "fondle", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Лизнуть соски" if "lick" in bodymodel_actions_for_target(GirlNameIMS, "nipples"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "nipples", "lick", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "nipples", "lick", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Погладить ее между ног" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "fondle", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "fondle", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Раздвинуть ее бедра" if _ims_full_engine and "spread" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "spread", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "spread", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Ввести пальцы в киску" if _ims_full_engine and "insert" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "insert", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Использовать игрушку" if _ims_full_engine and _ims_has_dildo() and "insert" in bodymodel_actions_for_target(GirlNameIMS, "pussy") and _ims_arousal(GirlNameIMS) >= 20:
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", Melissa.data.fullname, "female")
                    $ _ims_effect["action"] = "toy_insert"
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "toy_insert", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Лизать киску" if _ims_full_engine and "lick" in bodymodel_actions_for_target(GirlNameIMS, "pussy"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "lick", "You", Melissa.data.fullname, "female")
                    $ LickPussy[GirlNameIMS] = int(LickPussy.get(GirlNameIMS, 0) or 0) + 1
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "pussy", "lick", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Погладить ягодицы" if "fondle" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "fondle", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "ass", "fondle", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Раздвинуть ягодицы" if _ims_full_engine and "spread" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "spread", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "ass", "spread", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Ввести палец в попку" if _ims_full_engine and "insert" in bodymodel_actions_for_target(GirlNameIMS, "ass"):
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "insert", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "ass", "insert", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Подставить ей член" if _ims_full_engine and _ims_player_cum_count() < _ims_player_cum_limit() and int(SomebodyCums or 0) == 0:
                    $ _ims_set_inserted_container(GirlNameIMS, "mouth")
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "mouth", "suck", "You", Melissa.data.fullname, "female")
                    $ MainTxt = _ims_touch_text(GirlNameIMS, "mouth", "suck", _ims_effect)
                    "[MainTxt]"
                    call IntMelissaSexState(GirlNameIMS)

                "Войти в нее" if _ims_full_engine and _ims_player_cum_count() < _ims_player_cum_limit() and int(SomebodyCums or 0) == 0 and int(PussyVisible.get(GirlNameIMS, 0) or 0) == 1 and _ims_arousal("You") >= 20 and _ims_arousal(GirlNameIMS) >= 20:
                    $ _ims_set_inserted_container(GirlNameIMS, "pussy")
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "pussy", "insert", "You", Melissa.data.fullname, "female")
                    "Вы входите в Мелиссу медленно, оставляя ей время принять ваш темп и глубину."
                    call IntMelissaSexState(GirlNameIMS)

                "Войти сзади" if _ims_full_engine and _ims_player_cum_count() < _ims_player_cum_limit() and int(SomebodyCums or 0) == 0 and "insert" in bodymodel_actions_for_target(GirlNameIMS, "ass") and _ims_arousal("You") >= 30 and _ims_arousal(GirlNameIMS) >= 40:
                    $ _ims_set_inserted_container(GirlNameIMS, "ass")
                    $ _ims_effect = bodymodel_apply_action(GirlNameIMS, "ass", "insert", "You", Melissa.data.fullname, "female")
                    "Вы входите сзади, медленно и без спешки. Мелисса вцепляется в край стола и привыкает к новому давлению."
                    call IntMelissaSexState(GirlNameIMS)

                "Кончить в рот" if _ims_can_cum and int(CockInMouth.get(GirlNameIMS, 0) or 0) == 1:
                    "Поймав взгляд Мелиссы, вы больше не сдерживаетесь и кончаете ей в рот."
                    $ pregnancy_check(GirlNameIMS, "mouth", 1, "Вы")
                    $ _ims_set_arousal("You", 0)
                    $ CumFaceYou[GirlNameIMS] = 1
                    $ SomebodyCums = 1
                    $ _ims_clear_contact_states(GirlNameIMS)
                    call ShowCurrentSex(GirlNameIMS)
                    call int_melissa_sex_after_cum
                    if _return:
                        return

                "Кончить на лицо" if _ims_can_cum:
                    "Вы выходите из близости в последний момент и кончаете Мелиссе на лицо."
                    $ pregnancy_check(GirlNameIMS, "face", 1, "Вы")
                    $ _ims_set_arousal("You", 0)
                    $ CumFaceYou[GirlNameIMS] = 1
                    $ SomebodyCums = 1
                    $ _ims_clear_contact_states(GirlNameIMS)
                    call ShowCurrentSex(GirlNameIMS)
                    call int_melissa_sex_after_cum
                    if _return:
                        return

                "Кончить внутрь" if _ims_can_cum and _ims_current_inserted_container(GirlNameIMS) in ("pussy", "ass"):
                    $ _ims_inside_container = _ims_current_inserted_container(GirlNameIMS)
                    $ MainTxt = _ims_finish_inside_text(GirlNameIMS, _ims_inside_container)
                    "[MainTxt]"
                    if _ims_inside_container == "pussy":
                        $ pregnancy_check(GirlNameIMS, "inside", 1, "Вы")
                    else:
                        $ pregnancy_check(GirlNameIMS, "outside", 1, "Вы")
                    $ _ims_set_arousal("You", 0)
                    $ CumInsideYou[GirlNameIMS] = 1
                    $ SomebodyCums = 1
                    $ _ims_clear_contact_states(GirlNameIMS)
                    call ShowCurrentSex(GirlNameIMS)
                    call int_melissa_sex_after_cum
                    if _return:
                        return

                "Попросить Мелиссу помочь вам" if (not _ims_full_engine) and player_can_ask_intimacy_help(GirlNameIMS):
                    call PlayerIntimacyHelpAsk(GirlNameIMS, "IntMelissaSexState")

                "Остановиться":
                    call int_melissa_sex_finish
                    return


label IntMelissaSexState(girl_name="melissa"):
    if melissa_sex_available(girl_name):
        call ShowCurrentSex(girl_name)
        return
    $ MainTxt = _ims_engagement_state_text(girl_name)
    "[MainTxt]"
    return


label int_melissa_sex_after_cum:
    menu:
        "Продолжить":
            $ SomebodyCums = 0
            return False

        "Закончить":
            $ SomebodyCums = 0
            call int_melissa_sex_finish
            return True


label int_melissa_sex_finish:
    $ MainTxt = _ims_finish_scene(GirlNameIMS, _ims_start_orgasms)
    "[MainTxt]"
    if not _ims_scene_counted:
        $ _ims_count_sex_time(GirlNameIMS)
        $ _ims_scene_counted = True
    $ _ims_set_arousal("You", 0)
    $ _ims_set_arousal(GirlNameIMS, 0)
    $ SomebodyCums = 0
    call DressUp(GirlNameIMS)
    $ _ims_prepare_scene_state(GirlNameIMS)
    return



