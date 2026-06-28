# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.exports as renpy_module

    def show_girl_card_main_ui_state(girl_name=""):
        girl_key = str(girl_name or "").strip()
        if not girl_key:
            return
        store = renpy.store
        store.UI_mode = "char"
        store.UI_selected_char = girl_key
        store.current_girl_key = girl_key
        store.current_action_title = girl_card_display_name(girl_key)
        store.current_action_content = None
        store.current_action_items = []
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

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
        try:
            return peopleInfo.get(key, None)
        except Exception:
            return None

    def girl_card_current_dress_code(girl_name):
        key = girl_card_resolved_key(girl_name)
        info = girl_card_info_object(key)
        wardrobe = getattr(info, "wardrobe", {}) if info is not None else {}
        if isinstance(wardrobe, dict):
            dress_code = str(wardrobe.get("current_dress", "") or "").strip()
            if dress_code:
                return dress_code
        return str(_girls_desc_get(dressdefault, key, "") or "").strip()

    def girl_card_current_underwear(girl_name, item_key, legacy_map, legacy_default_map):
        key = girl_card_resolved_key(girl_name)
        info = girl_card_info_object(key)
        wardrobe = getattr(info, "wardrobe", {}) if info is not None else {}
        if isinstance(wardrobe, dict):
            current_underwear = wardrobe.get("current_underwear", {})
            if isinstance(current_underwear, dict):
                value = str(current_underwear.get(item_key, "") or "").strip()
                if value:
                    return value
        value = str(_girls_desc_get(legacy_map, key, "") or "").strip()
        if value:
            return value
        return str(_girls_desc_get(legacy_default_map, key, "") or "").strip()

    def girl_card_current_outfit_line(girl_name):
        key = girl_card_resolved_key(girl_name)
        top = _girls_desc_get(topdress, key, "")
        bottom = _girls_desc_get(bottomdress, key, "")
        bra_value = girl_card_current_underwear(key, "bra", bra, bradef)
        panties_value = girl_card_current_underwear(key, "panties", panties, pantiesdef)
        legs_value = girl_card_current_underwear(key, "legs", legs, legsdef)
        topraised_value = int(_girls_desc_get(topraised, key, 0) or 0)
        bottomraised_value = int(_girls_desc_get(bottomraised, key, 0) or 0)
        dress_code = girl_card_current_dress_code(key)

        if not str(top or "").strip():
            top = _girls_desc_get(DressTopPart, dress_code, "")
        if not str(bottom or "").strip():
            bottom = _girls_desc_get(DressBottomPart, dress_code, "")

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
        lines = []

        try:
            if isinstance(ChurchPurityReport, dict) and int(ChurchPurityLastDay or -1) == int(dayspassed or 0):
                row = dict(ChurchPurityReport.get(key, {}) or {})
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
        except Exception:
            pass

        if int(_girls_desc_get(CumFaceYou, key, 0) or 0) or int(_girls_desc_get(CumFaceOthers, key, 0) or 0):
            lines.append("На лице заметны следы спермы.")

        if int(_girls_desc_get(CumTitsYou, key, 0) or 0) or int(_girls_desc_get(CumTitsOthers, key, 0) or 0):
            lines.append("На груди заметны следы спермы.")

        if int(_girls_desc_get(CumInsideYou, key, 0) or 0) or int(_girls_desc_get(CumInsideOthers, key, 0) or 0):
            lines.append("На бедрах и у лона заметны следы недавнего секса.")

        try:
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
        except Exception:
            pass

        return lines

    def girl_card_resolved_key(girl_name):
        return str(_girls_desc_resolve_key(girl_name) or girl_name or "")

    def girl_card_display_name(girl_name):
        key = girl_card_resolved_key(girl_name)
        return str(_girls_desc_get(RealName, key, key) or key)

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
            return Melissa.image_path("card", "default") or Melissa.image_path("portrait", "default")
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
        info = None
        try:
            info = peopleInfo.get(key, None)
        except Exception:
            info = None
        if info is None:
            info = getPersonInfo(key)
        data = getPersonData(key)
        info_stats = getattr(info, "stats", {}) if info is not None else {}
        info_skills = getattr(info, "skills", {}) if info is not None else {}
        if not isinstance(info_stats, dict):
            info_stats = {}
        if not isinstance(info_skills, dict):
            info_skills = {}
        current_location = ""
        known_value = False
        if info is not None:
            try:
                current_location = str(info.getLocation() or "")
            except Exception:
                current_location = str(getattr(info, "location", "") or "")
            known_value = bool(getattr(info, "known", False))
        if not current_location:
            try:
                current_location = str(getLocation(key) or "")
            except Exception:
                current_location = ""
        age_value = getattr(info, "age", None) if info is not None else None
        if age_value is None or int(age_value or 0) <= 0:
            age_value = getattr(data, "age", 0) if data is not None else _girls_desc_stat_value(key, "age_girls", "age", default=0)
        rows = [
            ("Локация", current_location),
            ("Знакома", "да" if known_value else "нет"),
            ("Возраст", str(age_value)),
            ("Дружба", str(getattr(info, "rel", 0) if info is not None else 0)),
            ("Откровенность", str(getattr(info, "openness", 0) if info is not None else 0)),
            ("Распущенность", str(getattr(info, "corruption", 0) if info is not None else 0)),
            ("Красота", str(info_stats.get("beauty", _girls_desc_stat_value(key, "beauty", default=0)))),
            ("Дети", str(info_stats.get("kids", _girls_desc_stat_value(key, "kids", default=0)))),
            ("Беременность", str(info_stats.get("pregnancy", _girls_desc_stat_value(key, "pregnancy", default=0)))),
            ("Секс", str(info_stats.get("sexacts", _girls_desc_stat_value(key, "sexacts", default=0)))),
            ("Кухня", str(info_skills.get("cooking", _girls_desc_stat_value(key, "cooking", default=0)))),
            ("Уборка", str(info_skills.get("cleaning", _girls_desc_stat_value(key, "cleaning", default=0)))),
            ("Зал", str(info_skills.get("waitress", _girls_desc_stat_value(key, "waitress", default=0)))),
        ]
        try:
            status_line = relationship_card_status_line(key)
            if status_line:
                rows.append(("Отношение", status_line))
        except Exception:
            pass
        return rows

    def girl_card_body_lines(girl_name):
        key = girl_card_resolved_key(girl_name)
        lines = []
        lines.extend([str(line) for line in _girls_desc_build_lines(key) if str(line or "").strip()])
        lines.append(girl_card_current_outfit_line(key))
        lines.extend(girl_card_base_dress_lines(key))
        lines.extend(girl_card_visual_state_lines(key))
        return [str(line) for line in lines if str(line or "").strip()]


label ShowGirlCard(girl_name="", return_label=""):
    if str(girl_name or "") == "":
        return
    if str(return_label or "") == "__main_ui__":
        $ show_girl_card_main_ui_state(girl_name)
        return
    show screen girl_card_overlay(girl_name, return_label)
    return


label HideGirlCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
        return
    hide screen girl_card_overlay
    if str(return_label or "") != "":
        call expression return_label
    return


screen girl_card_overlay(girl_name="", return_label=""):
    zorder 120

    $ _girl_key = girl_card_resolved_key(girl_name)
    $ _title = girl_card_display_name(_girl_key)
    $ _portrait = girl_card_portrait_path(_girl_key)
    $ _stats = girl_card_stat_rows(_girl_key)
    $ _lines = girl_card_body_lines(_girl_key)
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24
    $ _portrait_w = 180
    $ _portrait_h = 240

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add im.Scale("images/rpg_message_bg.png", _left_w, _left_h)

        viewport:
            xpos 28
            ypos 24
            xsize _left_w - 56
            ysize _left_h - 96
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                hbox:
                    spacing 12

                    add im.Scale(_portrait, _portrait_w, _portrait_h)

                    vbox:
                        xmaximum _left_w - _portrait_w - 120
                        spacing 3
                        for _row in _stats:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                for _line in _lines:
                    text _line size 16 color "#2d1d12"

        textbutton "Назад":
            id "girl_card_overlay_back_button"
            alt "girl_card_overlay_back_button"
            xpos 28
            ypos _left_h - 58
            text_size 22
            action [Hide("girl_card_overlay"), SetVariable("UI_mode", "scene"), SetVariable("UI_selected_char", ""), SetVariable("current_girl_key", ""), Jump(str(CurLoc or getattr(CurrentRoom, "code_name", "") or "TavernMain"))]
