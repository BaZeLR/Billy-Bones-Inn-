# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def show_girl_card_main_ui_state(girl_name=""):
        girl_key = str(girl_name or "").strip()
        if not girl_key:
            return
        main_ui_begin_card_state()
        main_ui_runtime.mode = "char"
        main_ui_runtime.selected_char = girl_key
        main_ui_runtime.girl_key = girl_key
        main_ui_runtime.action_title = "Действия"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = [MenuItem("Назад", Function(main_ui_end_card_state))]
        main_ui_restart_interaction()

    def girl_card_base_dress_lines(girl_name):
        key = girl_card_resolved_key(girl_name)
        dress_code = girl_card_current_dress_code(key)
        if not dress_code:
            return []

        short_name = str(_girls_desc_get(ShortDressName, dress_code, dress_code) or dress_code)
        full_desc = str(_girls_desc_get(FullDressDesc, dress_code, "") or "").strip()

        lines = ["Основной наряд: %s." % short_name]
        if full_desc:
            lines.append(full_desc + ".")
        return lines

    def girl_card_info_object(girl_name):
        key = girl_card_resolved_key(girl_name)
        return people.get_info(key)

    def girl_card_current_dress_code(girl_name):
        key = girl_card_resolved_key(girl_name)
        info = girl_card_info_object(key)
        return str(info.current_dress() if info is not None else "").strip()

    def girl_card_current_underwear(girl_name, item_key):
        key = girl_card_resolved_key(girl_name)
        info = girl_card_info_object(key)
        if info is None:
            return ""
        if item_key in ("bra", "panties"):
            return str(info.clothing_layer(item_key) or "").strip()
        return str(info.current_underwear(item_key, "") or "").strip()

    def girl_card_current_outfit_line(girl_name):
        key = girl_card_resolved_key(girl_name)
        info = girl_card_info_object(key)
        top = info.clothing_layer("top") if info is not None else ""
        bottom = info.clothing_layer("bottom") if info is not None else ""
        bra_value = girl_card_current_underwear(key, "bra")
        panties_value = girl_card_current_underwear(key, "panties")
        legs_value = girl_card_current_underwear(key, "legs")
        topraised_value = info.layer_raised("top") if info is not None else 0
        bottomraised_value = info.layer_raised("bottom") if info is not None else 0

        parts = []
        if top and not topraised_value:
            parts.append(str(_girls_desc_get(DressPartDesc, top, top) or top))
        elif top and topraised_value:
            parts.append("блузка расстегнута или поднята")
        if bottom and str(bottom) != "nightshirtbottom":
            if bottomraised_value:
                parts.append("юбка задрана")
            else:
                parts.append(str(_girls_desc_get(DressPartDesc, bottom, bottom) or bottom))
        if bra_value and not top:
            parts.append(str(_girls_desc_get(FullDressDesc, bra_value, bra_value) or bra_value).lower())
        if panties_value and (not bottom or str(bottom) == "nightshirtbottom"):
            parts.append(str(_girls_desc_get(FullDressDesc, panties_value, panties_value) or panties_value).lower())
        if legs_value:
            parts.append(str(_girls_desc_get(DressPartDesc, legs_value, legs_value) or legs_value))

        if not parts:
            return "Сейчас на ней нет заметной одежды."

        return "Сейчас на ней: %s." % "; ".join([p for p in parts if str(p or "").strip()])

    def girl_card_visual_state_lines(girl_name):
        key = girl_card_resolved_key(girl_name)
        info = girl_card_info_object(key)
        lines = []

        church_state = rooms.get("Church").state
        if int(church_state.get("purity_last_day", -1) or -1) == int(current_game_day() or 0):
            row = dict(church_state.get("purity_report", {}).get(key, {}) or {})
            before_value = int(row.get("before", 0) or 0)
            after_value = int(row.get("after", 0) or 0)
            reduction = max(0, before_value - after_value)
            if reduction > 0:
                if reduction >= 18 or after_value <= before_value // 2:
                    lines.append("Последняя воскресная служба заметно укрепила ее сдержанность.")
                elif reduction >= 8:
                    lines.append("После последней воскресной службы она держится строже обычного.")
                else:
                    lines.append("Последняя воскресная служба слегка остудила ее порывистость.")

        if info is not None and (info.cum_state("cum_face_you") or info.cum_state("cum_face_others")):
            lines.append("На лице заметны следы спермы.")

        if info is not None and (info.cum_state("cum_tits_you") or info.cum_state("cum_tits_others")):
            lines.append("На груди заметны следы спермы.")

        if info is not None and (info.cum_state("cum_inside_you") or info.cum_state("cum_inside_others")):
            lines.append("На бедрах и у лона заметны следы недавнего секса.")

        if key == "amanda":
            cycle = Amanda.fertility_state()
        else:
            cycle = girl_decision_cycle_state(key)
        phase = str(cycle.get("phase", "") or "")
        desire_value = float(cycle.get("desire", cycle.get("horny", 0.0)) or 0.0)
        tags = [str(row or "") for row in list(cycle.get("tags", []) or [])]
        if key == "amanda" and (phase == "restless" or desire_value >= 0.6 or "horny" in tags):
            lines.append("Аманда чуть возбуждена: улыбается чаще обычного и держится немного вызывающе.")
        elif phase == "critical":
            lines.append("Цикл: тело уязвимее обычного, настроение сдержаннее.")
        elif phase == "fertile":
            lines.append("Цикл: плодородные дни, тело реагирует живее.")
        elif phase == "restless":
            lines.append("Цикл: беспокойная фаза, возбуждение приходит легче.")
        elif phase == "steady":
            lines.append("Цикл: ровное состояние.")

        return lines

    def girl_card_resolved_key(girl_name):
        return str(_girls_desc_resolve_key(girl_name) or girl_name or "")

    def girl_card_display_name(girl_name):
        key = girl_card_resolved_key(girl_name)
        return people_name(key, "nominative", key)

    def girl_card_portrait_path(girl_name):
        key = girl_card_resolved_key(girl_name)
        key_l = str(key or "").lower()

        card_candidates = [
            "images/%s/%s_card.jpg" % (key_l, key_l),
            "images/%s/%s_card.png" % (key_l, key_l),
            "images/%s/card.jpg" % key_l,
            "images/%s/card.png" % key_l,
        ]
        for card_path in card_candidates:
            if renpy.loadable(card_path):
                return card_path

        if key_l == "sandra":
            return "images/sandra/sandra_card.jpg" if renpy.loadable("images/sandra/sandra_card.jpg") else "images/sandra/sandra_0.png"
        if key_l == "melissa":
            return MelissaStaticData.image_path("card", "default") or MelissaStaticData.image_path("portrait", "default")
        if key_l == "amanda":
            return "images/amanda/amanda_card.jpg" if renpy.loadable("images/amanda/amanda_card.jpg") else "images/amanda/amanda_portrait.jpg"
        if key_l == "becky":
            return "images/becky/portraits/portrait_1.png"
        if key_l == "georgett":
            return "images/georgett/portraits/portrait.jpg"
        if key_l == "liza":
            return "images/liza/portraits/naked.jpg"
        if key_l == "irma":
            return irma_card_portrait_path()
        if key_l == "clara":
            return "images/clara/portrait1.jpg"
        if key_l == "werecat":
            return werecat_picture_path()
        if key_l == "inga":
            return "images/inga/StreetSex/minet1.jpg"
        if key_l == "fran":
            return "images/ellona/Fran1.jpg"

        return "images/rpg_message_bg.png"

    def girl_card_stat_rows(girl_name):
        key = girl_card_resolved_key(girl_name)
        info = people.get_info(key)
        info_stats = info.stats if info is not None else {}
        info_skills = info.skills if info is not None else {}
        current_location = str(info.getLocation() or "") if info is not None else ""
        known_value = bool(info.known) if info is not None else False
        age_value = people_age(key, 0)
        rows = [
            ("Локация", current_location),
            ("Знакома", "да" if known_value else "нет"),
            ("Возраст", str(age_value)),
            ("Дружба", str(info.rel if info is not None else 0)),
            ("Откровенность", str(info.openness if info is not None else 0)),
            ("Распущенность", str(info.corruption if info is not None else 0)),
            ("Красота", str(info_stats.get("beauty", 0))),
            ("Дети", str(info_stats.get("kids", 0))),
            ("Беременность", str(info_stats.get("pregnancy", 0))),
            ("Секс", str(info_stats.get("sexacts", 0))),
            ("Кухня", str(info_skills.get("cooking", 0))),
            ("Уборка", str(info_skills.get("cleaning", 0))),
            ("Зал", str(info_skills.get("waitress", 0))),
        ]
        status_line = relationship_card_status_line(key)
        if status_line:
            rows.append(("Отношение", status_line))
        if info is not None and int(info.job_value("jobHallAvail", 0) or 0) != 0:
            rows.append(("Работа сегодня", _tavern_worker_current_jobs(key)))
            rows.append(("Работа завтра", _tavern_worker_tomorrow_jobs(key)))
        return rows

    def girl_card_body_lines(girl_name):
        key = girl_card_resolved_key(girl_name)
        lines = []
        lines.extend([str(line) for line in _girls_desc_build_lines(key) if str(line or "").strip()])
        lines.append(girl_card_current_outfit_line(key))
        lines.extend(girl_card_base_dress_lines(key))
        lines.extend(girl_card_visual_state_lines(key))
        return [str(line) for line in lines if str(line or "").strip()]


label ShowGirlCard(girl_name=""):
    if str(girl_name or "") == "":
        return
    $ show_girl_card_main_ui_state(girl_name)
    $ main_ui_runtime.action_items = []
    menu:
        "Назад":
            $ main_ui_end_card_state()
            return


label HideGirlCard:
    $ main_ui_end_card_state()
    return
