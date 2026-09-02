# ================================================================================
# Shared household intimacy procedure. Relationship/story state remains on the
# participating NPC object; this label owns only the authored scene flow.
# ================================================================================
init python:
    HOUSEHOLD_INTIMACY_PRIVATE_ROOMS = frozenset((
        "TavernMelissaRoom",
        "TavernMyRoom",
        "TavernAmandaRoom",
        "TavernSandraRoom",
        "TavernEmptyRoom",
        "TavernStorage",
        "Shed",
    ))
    HOUSEHOLD_INTIMACY_SECLUDED_ROOMS = frozenset((
        "Forest",
        "ForestClearing",
        "ForestDarkWoods",
        "ForestWaterfall",
        "ForestLake",
        "ForestSpring",
        "ForestCave",
        "ForestHiddenPath",
        "Backyard",
    ))

    def household_intimacy_room_is_private(girl_name="", room_code=""):
        girl = str(girl_name or "").strip().lower()
        room_key = str(room_code or rooms.current_code or "").strip()
        if room_key in HOUSEHOLD_INTIMACY_PRIVATE_ROOMS or room_key in HOUSEHOLD_INTIMACY_SECLUDED_ROOMS:
            return True
        if girl == "melissa":
            return Melissa.private_context_active(room_key)
        return False

    def household_sex_available(girl_name="", action_code="intimacy"):
        girl = str(girl_name or "").strip().lower()
        info = people.get_info(girl)
        if info is None:
            return False
        if girl == "melissa":
            return bool(info.relationship_allows(action_code))
        if girl == "sandra":
            unlocked = (
                threads["sandraWeeklyEvaluation"].completed
                or int(threads["sandraWeeklyEvaluation"].num or 0) == 4
            )
            return unlocked and info.can_have_sex_today()
        return False

    def household_sex_relationship_stage(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "melissa":
            return Melissa.relationship_stage()
        if girl == "sandra" and household_sex_available(girl, "intimacy"):
            return 4
        return 0

    def household_sex_has_dildo():
        for item_id in ("dildo_001", "wooden_dildo_001", "glass_dildo_001"):
            if int(player.item_count(item_id) or 0) > 0:
                return True
        return False

    def household_sex_finish_inside_text(girl_name="", container_id=""):
        if str(container_id or "").strip().lower() == "ass":
            return "Вы удерживаете ее ближе к себе и кончаете ей в попку."
        return "Вы удерживаете ее ближе к себе и кончаете ей в киску."

    def household_sex_scene_summary(girl_name="", full_engine=False):
        girl = str(girl_name or "").strip().lower()
        info = people.get_info(girl)
        data = people.get_data(girl)
        if info is None or data is None:
            return ""
        lines = []
        if girl == "melissa" and not bool(full_engine):
            lines.append("Сейчас это еще не полноценный секс, а осторожное сближение. Мелисса позволяет поцелуи, ласки и все более смелые прикосновения, но пока ее комнатная история и ухаживания не завершены, дальше заходить рано.")
        elif girl == "melissa":
            lines.append("Мелисса уже готова к полноценной близости, если вы не будете терять ритм и внимание к ее состоянию.")
        else:
            lines.append("Сандра не прячет желания и прямо дает понять, что в этой комнате вы оба можете говорить о своих намерениях открыто.")
        lines.append(bodymodel_profile_summary_text(bodymodel_build_profile(girl, data.fullname, "female")))
        return "\n\n".join([row for row in lines if str(row or "").strip()])

    def household_sex_clamp_engagement_arousal(girl_name="", full_engine=False):
        if bool(full_engine):
            return
        info = people.get_info(girl_name)
        if info is None:
            return
        player.intimacy.set_arousal(min(85, player.intimacy.arousal_value()))
        info.set_arousal(min(90, info.arousal_value()))

    def household_sex_touch_text(girl_name="", target_id="", action_id="", effect=None, full_engine=False):
        girl = str(girl_name or "").strip().lower()
        info = people.get_info(girl)
        display_name = people_display_name(girl)
        target_key = str(target_id or "").strip()
        action_key = str(action_id or "").strip()
        effect = dict(effect or {})
        household_sex_clamp_engagement_arousal(girl, full_engine)
        if not bool(effect.get("allowed", False)):
            if target_key == "nipples":
                return "Одежда {} все еще мешает добраться до ее груди как следует.".format(people_name(girl, "genitive"))
            if target_key == "pussy":
                return "Пока на {} остается слишком много одежды, дальше осторожных ласк вы не продвинетесь.".format(people_name(girl, "dative"))
            if target_key == "ass":
                return "Сквозь оставшуюся одежду до ее ягодиц сейчас не добраться как следует."
            return "Сейчас это не выйдет."
        if target_key == "mouth" and action_key == "kiss":
            return "Вы мягко целуете {}. Она сперва замирает, а затем сама отвечает на поцелуй.".format(display_name)
        if target_key == "nipples" and action_key == "fondle":
            if info.tits_visible():
                return "Вы ласкаете грудь {} уже без ткани между руками и телом. Ее соски быстро твердеют, а дыхание заметно сбивается.".format(people_name(girl, "genitive"))
            return "Вы начинаете ласкать грудь {} через одежду. Даже сквозь ткань ее тело отзывается заметной дрожью.".format(people_name(girl, "genitive"))
        if target_key == "nipples" and action_key == "lick":
            return "Вы склоняетесь к ее груди и проводите языком по затвердевшим соскам. {} шумно втягивает воздух и прижимается к вам ближе.".format(display_name)
        if target_key == "pussy" and action_key == "fondle":
            if info.pussy_visible():
                return "Ваши пальцы скользят по обнажившейся щели, разогревая {} еще сильнее.".format(display_name)
            if info.layer_raised("bottom"):
                return "Под задранной юбкой вы начинаете ласкать {} между ног через тонкую ткань. Она вздрагивает и шире разводит бедра.".format(display_name)
            return "Вы осторожно проводите рукой по ее бедрам и промежности через юбку, разжигая желание даже сквозь одежду."
        if target_key == "pussy" and action_key == "spread":
            return "Вы разводите ее бедра чуть шире, и она раскрывается перед вами без слов."
        if target_key == "pussy" and action_key == "insert":
            if str(effect.get("container_state", "") or "") in ("wet", "itchy and wet", "slurping"):
                return "Вы медленно вводите пальцы в уже влажную киску. {} тихо стонет и подается навстречу.".format(display_name)
            return "Вы медленно вводите пальцы, давая ей привыкнуть к глубине и темпу."
        if target_key == "pussy" and action_key == "toy_insert":
            if str(effect.get("container_state", "") or "") in ("wet", "itchy and wet", "slurping"):
                return "С игрушкой выходит легче: она уже достаточно влажная, чтобы принять ее без лишнего напряжения."
            return "Вы начинаете очень осторожно, пока она привыкает к форме и давлению игрушки."
        if target_key == "pussy" and action_key == "lick":
            return "Вы опускаетесь ниже и начинаете вылизывать ее. Дрожь пробегает от живота до колен."
        if target_key == "ass" and action_key == "fondle":
            return "Вы сжимаете и гладите ее ягодицы, чувствуя, как она становится еще чувствительнее к вашим рукам."
        if target_key == "ass" and action_key == "spread":
            return "Вы раздвигаете ее ягодицы и заставляете замереть в особенно уязвимой позе."
        if target_key == "ass" and action_key == "insert":
            return "Смочив пальцы, вы осторожно разрабатываете ее попку. Она напрягается, но не пытается вас остановить."
        if target_key == "mouth" and action_key == "suck":
            return "{} берет ваш член в рот и постепенно привыкает к ритму, послушно ловя ваши движения губами и языком.".format(display_name)
        return "Между вами становится еще меньше расстояния."

    def household_sex_finish_scene(girl_name="", full_engine=False, start_orgasms=0):
        info = people.get_info(girl_name)
        display_name = people_display_name(girl_name)
        if info is None:
            return ""
        info.set_cock_position("none")
        if not bool(full_engine):
            info.change_social(friend_delta=1, corruption_delta=1)
            return "Вы останавливаетесь до того, как близость сорвется в настоящий секс. {} еще тяжело дышит, поправляет одежду и смотрит на вас уже мягче.".format(display_name)
        gained_orgasms = max(0, int(info.sex_stat("orgasms_given", 0) or 0) - int(start_orgasms or 0))
        if gained_orgasms <= 0:
            info.change_social(friend_delta=1)
            return "Вы останавливаетесь прежде, чем довести ее до разрядки. {} еще тяжело дышит и просит в следующий раз не бросать ее на полпути.".format(display_name)
        if gained_orgasms >= 2:
            info.change_social(friend_delta=2, open_delta=2, corruption_delta=3)
            return "Когда вы наконец останавливаетесь, {} выглядит измученной, но довольной и держится рядом с вами куда менее настороженно.".format(display_name)
        info.change_social(friend_delta=2, open_delta=1, corruption_delta=2)
        return "Вы даете ей перевести дыхание. По взгляду {} видно, что этот раз она запомнит как что-то по-настоящему важное.".format(people_name(girl_name, "genitive"))


label HouseholdSexEngine(girl_name="melissa", source_room="", initial_action="sex"):
    $ renpy.dynamic("_hse_girl", "_hse_info", "_hse_data", "_hse_display", "_hse_effect", "_hse_picture", "_hse_stage", "_hse_full_engine", "_hse_can_cum", "_hse_inside_container", "_hse_initial_action", "_hse_start_orgasms", "_hse_start_player_cums")
    $ _hse_girl = str(girl_name or "").strip().lower()
    $ _hse_initial_action = str(initial_action or "sex").strip().lower()
    $ _hse_info = people.get_info(_hse_girl)
    $ _hse_data = people.get_data(_hse_girl)
    if _hse_girl not in ("melissa", "sandra") or _hse_info is None or _hse_data is None:
        return
    if not household_sex_available(_hse_girl, "intimacy"):
        $ scene_runtime.text = "Для такой близости ваши отношения должны зайти дальше."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if not household_intimacy_room_is_private(_hse_girl, source_room or rooms.current_code):
        $ scene_runtime.text = "Для такого между вами нужно место без чужих взглядов. Здесь слишком открыто."
        $ scene_runtime.location_text = scene_runtime.text
        return
    python:
        _hse_display = people_display_name(_hse_girl)
        _hse_info.ensure_sex_state()
        _hse_start_orgasms = int(_hse_info.sex_stat("orgasms_given", 0) or 0)
        _hse_start_player_cums = int(player.intimacy.came_today or 0)
        _hse_full_engine = household_sex_available(_hse_girl, "sex")
        _hse_info.set_cock_position("none")
    $ main_ui_begin_native_scene_state(_hse_display)
    $ _hse_picture = _hse_data.image_path("portrait", "default")
    if str(_hse_picture or "").strip():
        $ scene_runtime.picture = _hse_picture
        vscene scene_runtime.picture
    $ scene_runtime.text = household_sex_scene_summary(_hse_girl, _hse_full_engine)
    $ scene_runtime.location_text = scene_runtime.text
    if _hse_initial_action == "handjob":
        $ _hse_info.set_cock_position("none")
        $ player.intimacy.add_arousal(30, 100)
        $ _hse_info.add_arousal(5)
        $ scene_runtime.text = "Вы просите ее помочь вам рукой. Она соглашается, устраивается ближе, обхватывает ваш член ладонью и начинает двигать ею в ровном, уверенном ритме."
        $ scene_runtime.picture = _hse_data.image_path("outfit_reward", "handjob")
        call HouseholdSexState(_hse_girl, _hse_full_engine)
    elif _hse_initial_action == "blowjob":
        $ _hse_info.set_cock_position("mouth")
        $ _hse_effect = bodymodel_apply_action(_hse_girl, "mouth", "suck", "You", _hse_data.fullname, "female")
        $ scene_runtime.text = household_sex_touch_text(_hse_girl, "mouth", "suck", _hse_effect, _hse_full_engine)
        $ scene_runtime.picture = _hse_data.cycle_image("sexy_times", "blowjob", _hse_info.arousal_value())
        call HouseholdSexState(_hse_girl, _hse_full_engine)

    label household_sex_menu:
        while True:
            $ _hse_stage = household_sex_relationship_stage(_hse_girl)
            $ _hse_can_cum = _hse_full_engine and _hse_info.can_have_sex_today() and player.intimacy.arousal_value() >= 100 and player.intimacy.can_cum()
            menu:
                "Осмотреть её":
                    $ scene_runtime.text = household_sex_scene_summary(_hse_girl, _hse_full_engine)
                    $ scene_runtime.picture = _hse_data.image_path("portrait", "default")

                "Распахнуть блузку" if _hse_stage >= 3 and _hse_info.clothing_layer("top") != "" and not _hse_info.layer_raised("top"):
                    $ scene_runtime.text = "Вы медленно распахиваете ее блузку, открывая себе больше простора для рук и губ."
                    $ _hse_info.set_layer_raised("top", 1)

                "Снять блузку" if _hse_stage >= 3 and _hse_info.clothing_layer("top") != "":
                    $ scene_runtime.text = "Вы стягиваете с нее блузку, оставляя верх куда менее защищенным."
                    $ _hse_info.remove_clothing_layer("top")
                    $ _hse_info.set_layer_raised("top", 0)

                "Снять лиф" if _hse_stage >= 3 and _hse_info.clothing_layer("bra") != "" and (_hse_info.clothing_layer("top") == "" or _hse_info.layer_raised("top")):
                    $ scene_runtime.text = "Избавившись от лишней застежки, вы окончательно освобождаете ее грудь."
                    $ _hse_info.remove_clothing_layer("bra")

                "Поднять юбку" if _hse_stage >= 3 and _hse_info.clothing_layer("bottom") != "" and not _hse_info.layer_raised("bottom"):
                    $ scene_runtime.text = "Вы поднимаете ее юбку, открывая себе путь выше по бедрам."
                    $ _hse_info.set_layer_raised("bottom", 1)

                "Снять юбку" if _hse_stage >= 3 and _hse_info.clothing_layer("bottom") != "":
                    $ scene_runtime.text = "Вы окончательно снимаете ее юбку, оставляя лишь то, что ближе к телу."
                    $ _hse_info.remove_clothing_layer("bottom")
                    $ _hse_info.set_layer_raised("bottom", 0)

                "Снять панталончики" if _hse_stage >= 4 and _hse_info.clothing_layer("panties") != "" and (_hse_info.clothing_layer("bottom") == "" or _hse_info.layer_raised("bottom")):
                    $ scene_runtime.text = "Вы стягиваете с нее панталончики, и теперь между вами почти ничего не осталось."
                    $ _hse_info.remove_clothing_layer("panties")

                "Поцеловать [_hse_display]":
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "mouth", "kiss", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "mouth", "kiss", _hse_effect, _hse_full_engine)
                    $ scene_runtime.picture = _hse_data.image_path("portrait", "default")
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Ласкать грудь" if "fondle" in bodymodel_actions_for_target(_hse_girl, "nipples"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "nipples", "fondle", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "nipples", "fondle", _hse_effect, _hse_full_engine)
                    $ scene_runtime.picture = _hse_data.image_path("grope", "tit_ok" if _hse_full_engine else "tits_shy")
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Лизнуть соски" if "lick" in bodymodel_actions_for_target(_hse_girl, "nipples"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "nipples", "lick", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "nipples", "lick", _hse_effect, _hse_full_engine)
                    $ scene_runtime.picture = _hse_data.image_path("grope", "tit_ok")
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Погладить ее между ног" if "fondle" in bodymodel_actions_for_target(_hse_girl, "pussy"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "pussy", "fondle", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "pussy", "fondle", _hse_effect, _hse_full_engine)
                    $ scene_runtime.picture = _hse_data.image_path("grope", "ass_ok")
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Раздвинуть ее бедра" if _hse_full_engine and "spread" in bodymodel_actions_for_target(_hse_girl, "pussy"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "pussy", "spread", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "pussy", "spread", _hse_effect, _hse_full_engine)
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Ввести пальцы в киску" if _hse_full_engine and "insert" in bodymodel_actions_for_target(_hse_girl, "pussy"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "pussy", "insert", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "pussy", "insert", _hse_effect, _hse_full_engine)
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Использовать игрушку" if _hse_full_engine and household_sex_has_dildo() and "insert" in bodymodel_actions_for_target(_hse_girl, "pussy") and _hse_info.arousal_value() >= 20:
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "pussy", "insert", "You", _hse_data.fullname, "female")
                    $ _hse_effect["action"] = "toy_insert"
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "pussy", "toy_insert", _hse_effect, _hse_full_engine)
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Лизать киску" if _hse_full_engine and "lick" in bodymodel_actions_for_target(_hse_girl, "pussy"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "pussy", "lick", "You", _hse_data.fullname, "female")
                    $ _hse_info.record_lick_pussy()
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "pussy", "lick", _hse_effect, _hse_full_engine)
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Погладить ягодицы" if "fondle" in bodymodel_actions_for_target(_hse_girl, "ass"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "ass", "fondle", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "ass", "fondle", _hse_effect, _hse_full_engine)
                    $ scene_runtime.picture = _hse_data.image_path("grope", "ass_ok")
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Раздвинуть ягодицы" if _hse_full_engine and "spread" in bodymodel_actions_for_target(_hse_girl, "ass"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "ass", "spread", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "ass", "spread", _hse_effect, _hse_full_engine)
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Ввести палец в попку" if _hse_full_engine and "insert" in bodymodel_actions_for_target(_hse_girl, "ass"):
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "ass", "insert", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "ass", "insert", _hse_effect, _hse_full_engine)
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Попросить помочь рукой" if _hse_full_engine and player.intimacy.can_cum() and not _hse_info.sex_busy():
                    $ _hse_info.set_cock_position("none")
                    $ player.intimacy.add_arousal(30, 100)
                    $ _hse_info.add_arousal(5)
                    $ scene_runtime.text = "Вы просите ее помочь вам рукой. Она устраивается ближе, обхватывает ваш член ладонью и начинает двигать ею в ровном, уверенном ритме."
                    $ scene_runtime.picture = _hse_data.image_path("outfit_reward", "handjob")
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Попросить сделать минет" if _hse_full_engine and player.intimacy.can_cum() and not _hse_info.sex_busy():
                    $ _hse_info.set_cock_position("mouth")
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "mouth", "suck", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = household_sex_touch_text(_hse_girl, "mouth", "suck", _hse_effect, _hse_full_engine)
                    $ scene_runtime.picture = _hse_data.cycle_image("sexy_times", "blowjob", _hse_info.arousal_value())
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Войти в нее" if _hse_full_engine and player.intimacy.can_cum() and not _hse_info.sex_busy() and _hse_info.pussy_visible() and player.intimacy.arousal_value() >= 20 and _hse_info.arousal_value() >= 20:
                    $ _hse_info.set_cock_position("pussy")
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "pussy", "insert", "You", _hse_data.fullname, "female")
                    $ scene_runtime.text = "Вы входите в нее медленно, оставляя время принять ваш темп и глубину."
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Войти сзади" if _hse_full_engine and player.intimacy.can_cum() and not _hse_info.sex_busy() and "insert" in bodymodel_actions_for_target(_hse_girl, "ass") and player.intimacy.arousal_value() >= 30 and _hse_info.arousal_value() >= 40:
                    $ _hse_info.set_cock_position("ass")
                    $ _hse_effect = bodymodel_apply_action(_hse_girl, "ass", "insert", "You", _hse_data.fullname, "female")
                    if _hse_girl == "melissa" and threads["claraTavernVisit"].completed and int(threads["claraForestSofa"].num or 0) >= 6 and not bool(threads["claraForestSofa"].aborted):
                        $ scene_runtime.text = "Вспомнив советы Клариссы, Мелисса сама задает медленный темп и показывает, когда можно продолжить. Вы входите сзади без спешки; она привыкает к новому давлению и не позволяет вам торопиться."
                    else:
                        $ scene_runtime.text = "Вы входите сзади медленно и без спешки. Она сама показывает, когда можно продолжить, и не позволяет вам торопиться."
                    call HouseholdSexState(_hse_girl, _hse_full_engine)

                "Кончить в рот" if _hse_can_cum and _hse_info.cock_in("mouth"):
                    $ scene_runtime.text = "Поймав ее взгляд, вы больше не сдерживаетесь и кончаете ей в рот."
                    $ pregnancy_check(_hse_girl, "mouth", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ _hse_info.set_cum_state("cum_mouth_you", 1)
                    $ _hse_info.set_sex_busy(True)
                    $ _hse_info.set_cock_position("none")
                    $ scene_runtime.picture = _hse_data.image_path("sexy_times", "blowjob_finish")
                    call HouseholdSexAfterCum
                    if _return:
                        return

                "Кончить на грудь" if _hse_can_cum:
                    $ scene_runtime.text = "Вы выходите в последний момент и кончаете ей на грудь."
                    $ pregnancy_check(_hse_girl, "tits", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ _hse_info.set_cum_state("cum_tits_you", 1)
                    $ _hse_info.set_sex_busy(True)
                    $ _hse_info.set_cock_position("none")
                    $ scene_runtime.picture = _hse_data.image_path("sexy_times", "finish")
                    call HouseholdSexAfterCum
                    if _return:
                        return

                "Кончить на лицо" if _hse_can_cum:
                    $ scene_runtime.text = "Вы выходите в последний момент и кончаете ей на лицо."
                    $ pregnancy_check(_hse_girl, "face", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ _hse_info.set_cum_state("cum_face_you", 1)
                    $ _hse_info.set_sex_busy(True)
                    $ _hse_info.set_cock_position("none")
                    $ scene_runtime.picture = _hse_data.image_path("sexy_times", "finish")
                    call HouseholdSexAfterCum
                    if _return:
                        return

                "Кончить в киску" if _hse_can_cum and _hse_info.cock_in("pussy"):
                    $ _hse_inside_container = "pussy"
                    $ scene_runtime.text = household_sex_finish_inside_text(_hse_girl, _hse_inside_container)
                    $ pregnancy_check(_hse_girl, "inside", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ _hse_info.set_cum_state("cum_inside_you", 1)
                    $ _hse_info.set_sex_busy(True)
                    $ _hse_info.set_cock_position("none")
                    $ scene_runtime.picture = _hse_data.image_path("sexy_times", "finish")
                    call HouseholdSexAfterCum
                    if _return:
                        return

                "Кончить в попку" if _hse_can_cum and _hse_info.cock_in("ass"):
                    $ _hse_inside_container = "ass"
                    $ scene_runtime.text = household_sex_finish_inside_text(_hse_girl, _hse_inside_container)
                    $ pregnancy_check(_hse_girl, "ass", 1, "Вы")
                    $ player.intimacy.set_arousal(0)
                    $ _hse_info.set_sex_busy(True)
                    $ _hse_info.set_cock_position("none")
                    $ scene_runtime.picture = _hse_data.image_path("sexy_times", "finish")
                    call HouseholdSexAfterCum
                    if _return:
                        return

                "Попросить ее помочь вам" if (not _hse_full_engine) and player_can_ask_intimacy_help(_hse_girl):
                    call PlayerIntimacyHelpAsk(_hse_girl, "HouseholdSexState")

                "Остановиться":
                    call HouseholdSexFinish
                    return

            $ scene_runtime.location_text = scene_runtime.text
            if str(scene_runtime.picture or "").strip():
                vscene scene_runtime.picture


label HouseholdSexState(girl_name="melissa", full_engine=False):
    $ renpy.dynamic("_hse_state_info", "_hse_state_data", "_hse_state_lines", "_hse_state_text")
    $ _hse_state_info = people.get_info(girl_name)
    $ _hse_state_data = people.get_data(girl_name)
    if _hse_state_info is None or _hse_state_data is None:
        return
    $ household_sex_clamp_engagement_arousal(girl_name, full_engine)
    $ _hse_state_lines = []
    if player.intimacy.arousal_value() >= 100:
        $ _hse_state_lines.append("Вы уже готовы кончить и можете выбрать, как закончить.")
    if _hse_state_info.arousal_value() >= 100:
        $ _hse_state_lines.append("{} забилась в судорогах оргазма, выгнулась дугой и со счастливым вздохом обмякла в ваших руках.".format(people_display_name(girl_name)))
        $ _hse_state_info.record_orgasm_given()
        if _hse_state_info.cock_in("pussy"):
            $ _hse_state_info.set_arousal(20)
        else:
            $ _hse_state_info.set_arousal(0)
    $ _hse_state_text = bodymodel_profile_summary_text(bodymodel_build_profile(girl_name, _hse_state_data.fullname, "female"))
    if str(_hse_state_text or "").strip():
        $ _hse_state_lines.append(_hse_state_text)
    if _hse_state_lines:
        $ scene_runtime.text = str(scene_runtime.text or "").strip() + "\n\n" + "\n\n".join(_hse_state_lines)
    $ scene_runtime.location_text = scene_runtime.text
    return


label HouseholdSexAfterCum:
    $ scene_runtime.location_text = scene_runtime.text
    if str(scene_runtime.picture or "").strip():
        vscene scene_runtime.picture
    menu:
        "Продолжить":
            $ _hse_info.set_sex_busy(False)
            return False

        "Закончить":
            $ _hse_info.set_sex_busy(False)
            call HouseholdSexFinish
            return True


label HouseholdSexFinish:
    $ scene_runtime.text = household_sex_finish_scene(_hse_girl, _hse_full_engine, _hse_start_orgasms)
    $ scene_runtime.location_text = scene_runtime.text
    if int(player.intimacy.came_today or 0) == _hse_start_player_cums:
        $ _hse_info.mark_fucked()
    $ player.intimacy.set_arousal(0)
    $ _hse_info.set_arousal(0)
    $ _hse_info.set_sex_busy(False)
    $ calendar_v2.advance_minutes(30)
    $ _hse_picture = _hse_data.image_path("sexy_times", "finish")
    if str(_hse_picture or "").strip():
        $ scene_runtime.picture = _hse_picture
        vscene scene_runtime.picture
    call DressUp(_hse_girl)
    menu:
        "Закончить близость":
            pass
    $ main_ui_end_native_scene_state()
    return
