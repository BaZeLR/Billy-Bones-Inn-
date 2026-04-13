init python:
    def _girls_desc_map(name, default=None):
        value = getattr(renpy.store, str(name or ""), default)
        if value is None:
            return default
        return value

    def _girls_desc_get(mapping, key, default=None):
        if mapping is None:
            return default

        try:
            if hasattr(mapping, "get"):
                value = mapping.get(key, default)
                if value is not default:
                    return value
        except Exception:
            pass

        try:
            return mapping[key]
        except Exception:
            pass

        # Legacy data is often mixed-case ("Clara" vs "clara"), so allow
        # case-insensitive lookups for dict-backed game state.
        if isinstance(mapping, dict):
            key_l = str(key).lower()
            for mk, mv in mapping.items():
                if str(mk).lower() == key_l:
                    return mv

        return default

    def _girls_desc_alias_name(girl_name):
        raw = str(girl_name or "").strip()
        if not raw:
            return ""
        aliases = {
            "georgette": "georgett",
            "lizette": "liza",
            "lizzette": "liza",
            "francesca": "fran",
            "franchesca": "fran",
            "francheska": "fran",
            "clarisse": "Clara",
            "clara": "Clara",
        }
        return aliases.get(raw.lower(), raw)

    def _girls_desc_resolve_key(girl_name):
        base = _girls_desc_alias_name(girl_name)
        if not base:
            return ""

        variants = []
        for v in (base, str(base).lower(), str(base).capitalize(), str(base).upper()):
            if v not in variants:
                variants.append(v)

        probe_maps = (
            _girls_desc_map("girltextdesc", {}),
            _girls_desc_map("RealName", {}),
            _girls_desc_map("RealName2", {}),
            _girls_desc_map("age", {}),
            _girls_desc_map("beauty", {}),
            _girls_desc_map("friends", {}),
            _girls_desc_map("Friends", {}),
            _girls_desc_map("pregnancy", {}),
            _girls_desc_map("topdress", {}),
            _girls_desc_map("bottomdress", {}),
        )

        for mapping in probe_maps:
            if not isinstance(mapping, dict):
                continue
            for cand in variants:
                if cand in mapping:
                    return cand
            lower_index = {}
            for mk in mapping.keys():
                lower_index[str(mk).lower()] = mk
            for cand in variants:
                found = lower_index.get(str(cand).lower(), None)
                if found is not None:
                    return found

        return base

    def _girls_desc_skill_text(value):
        try:
            value = int(value)
        except Exception:
            value = 0

        if value < 10:
            return "совсем неумелая"
        if value < 20:
            return "неумелая"
        if value < 30:
            return "начинающая"
        if value < 40:
            return "посредственная"
        if value < 50:
            return "средняя"
        if value < 60:
            return "умелая"
        if value < 70:
            return "опытная"
        if value < 80:
            return "очень опытная"
        if value < 90:
            return "профессиональная"
        return "просто потрясающая"

    def _girls_desc_beauty_text(value):
        try:
            value = int(value)
        except Exception:
            value = 0

        if value < 10:
            return "Она страшнее самого черта."
        if value < 20:
            return "Она, мягко выражаясь, страшновата."
        if value < 30:
            return "Она дурнушка."
        if value < 40:
            return "Красавицей ее не назовешь, но и особо страшной тоже."
        if value < 50:
            return "Она ничего, в ней есть что-то интересное."
        if value < 60:
            return "Она красива."
        if value < 70:
            return "Она привлекает взоры мужчин."
        if value < 80:
            return "Она просто прекрасна."
        return "Она красавица из красавиц."

    def _girls_desc_stat_value(key, *map_names, **kwargs):
        default = kwargs.get("default", 0)
        for map_name in map_names:
            mapping = _girls_desc_map(map_name, {})
            value = _girls_desc_get(mapping, key, None)
            if value is not None:
                return value
        return default

    def _girls_desc_build_lines(girl_name):
        g = _girls_desc_resolve_key(girl_name)
        if not g:
            g = str(girl_name or "")

        def gm(name):
            return _girls_desc_map(name, {})

        real_name = _girls_desc_get(gm("RealName"), g, g)
        real_name2 = _girls_desc_get(gm("RealName2"), g, real_name)
        lines = []

        base_desc = _girls_desc_get(gm("girltextdesc"), g, "")
        if base_desc:
            lines.append(base_desc)

        top = _girls_desc_get(gm("topdress"), g, "")
        bra = _girls_desc_get(gm("bra"), g, "")
        bottom = _girls_desc_get(gm("bottomdress"), g, "")
        panties = _girls_desc_get(gm("panties"), g, "")
        legs = _girls_desc_get(gm("legs"), g, "")
        shoes = _girls_desc_get(gm("shoes"), g, "")
        topraised = bool(_girls_desc_get(gm("topraised"), g, 0))
        bottomraised = bool(_girls_desc_get(gm("bottomraised"), g, 0))
        dress_part_desc = gm("DressPartDesc")
        dress_part_slut = gm("DressPartSlut")

        if int(_girls_desc_get(gm("Lactate"), g, 0) or 0) == 1:
            lactated_tits_desc = (
                "Видно что груди %s набухли, а соски увеличились. "
                "Ткань напротив них слегка промокла." % real_name2
            )
        else:
            lactated_tits_desc = ""

        if top:
            top_desc = _girls_desc_get(dress_part_desc, top, top)
            line = "Она одета в %s" % top_desc
            top_slut = int(_girls_desc_get(dress_part_slut, top, 0) or 0)

            if not bra:
                if topraised:
                    line += ". Сейчас эта блузка бесстыдно распахнута и не стесненные лифом груди вырвались на свободу."
                elif top_slut >= 6:
                    line += ". Под ней нет лифчика и соски проглядывают через тонкую ткань. " + lactated_tits_desc
                elif top_slut >= 4:
                    line += ". Под ней нет лифчика, из глубокого выреза видны ареолы. " + lactated_tits_desc
                elif top_slut >= 3:
                    line += ". Под ней нет лифчика, так как из-под ткани выступают бугорки сосочков."
                else:
                    line += "."
            else:
                if topraised:
                    line += ". Сейчас эта блузка бесстыдно распахнута и груди прикрыты лишь лифчиком. " + lactated_tits_desc
                elif top_slut >= 4:
                    line += ". Глубокий вырез блузки открывал бы прекрасный вид на груди %s, если бы не лиф. %s" % (real_name2, lactated_tits_desc)
                elif top_slut >= 3:
                    line += ". Под тонкой тканью просматриваются очертания лифчика. " + lactated_tits_desc
                else:
                    line += "."

            lines.append(line.strip())
        elif bra:
            bra_desc = _girls_desc_get(gm("FullDressDesc"), bra, bra).lower()
            line = "Она одета только в %s." % bra_desc
            if lactated_tits_desc:
                line += " " + lactated_tits_desc
            lines.append(line)

        if bottom and bottom != "nightshirtbottom":
            bottom_desc = _girls_desc_get(dress_part_desc, bottom, bottom)
            prefix = "Также она одета в " if (top or bra) else "Она одета в "
            line = prefix + bottom_desc
            bottom_slut = int(_girls_desc_get(dress_part_slut, bottom, 0) or 0)

            if bottomraised:
                if bottom_slut >= 4:
                    line += ", которая бесстыдно задрана до пояса."
                else:
                    line += ", длинный подол которой поднят и завернут до самого пояса."
                if not panties:
                    line += " Ну а так как панталончиков у %s нет, то ее влагалище открыто всем взорам." % real_name2
                else:
                    line += " %s осталась в одних панталончиках." % real_name
            else:
                if not panties and bottom_slut >= 6:
                    line += ". Когда %s наклоняется, видно что на ней нет трусиков." % real_name
                elif not panties and bottom_slut >= 4:
                    line += ". Когда %s наклоняется, порой кажется что под юбкой ничего нет." % real_name
                elif panties and bottom_slut >= 6:
                    line += ". Когда %s наклоняется, то видны ее панталончики." % real_name
                elif panties and bottom_slut >= 4:
                    line += ". Когда %s наклоняется, порой удается увидеть краешек ее панталончиков." % real_name
                else:
                    line += "."

            lines.append(line)
        elif panties and bottom != "nightshirtbottom":
            panties_desc = _girls_desc_get(gm("FullDressDesc"), panties, panties).lower()
            prefix = "Также она одета в " if (top or bra) else "Она одета в "
            lines.append(prefix + panties_desc + ".")

        if (bottomraised or not bottom or int(_girls_desc_get(dress_part_slut, bottom, 0) or 0) >= 4) and legs:
            legs_desc = _girls_desc_get(dress_part_desc, legs, legs)
            line = "Ее ножки обтянуты %s" % legs_desc
            if (not bottomraised) and bottom and int(_girls_desc_get(dress_part_slut, bottom, 0) or 0) >= 5:
                line += ", эротично кончающимися чуть ниже юбочки."
            else:
                line += "."
            lines.append(line)

        if shoes == "simpleshoes":
            lines.append("На ее ногах простые башмаки.")
        elif shoes == "highshoes":
            lines.append("На ее ногах башмачки на очень высоком каблуке.")

        if int(_girls_desc_get(gm("TitsVisible"), g, 0) or 0):
            line = "Ее сиськи бесстыдно обнажены."
            if lactated_tits_desc:
                line += " " + lactated_tits_desc
            lines.append(line)

        if int(_girls_desc_get(gm("PussyVisible"), g, 0) or 0):
            lines.append("Ее влагалище ничем не прикрыто от нескромных взглядов.")

        cum_face_you = int(_girls_desc_get(gm("CumFaceYou"), g, 0) or 0)
        cum_face_others = int(_girls_desc_get(gm("CumFaceOthers"), g, 0) or 0)
        cum_tits_you = int(_girls_desc_get(gm("CumTitsYou"), g, 0) or 0)
        cum_tits_others = int(_girls_desc_get(gm("CumTitsOthers"), g, 0) or 0)
        cum_inside_you = int(_girls_desc_get(gm("CumInsideYou"), g, 0) or 0)
        cum_inside_others = int(_girls_desc_get(gm("CumInsideOthers"), g, 0) or 0)
        short_skirt_no_panties = int(_girls_desc_get(gm("ShortSkirtNoPanties"), g, 0) or 0)

        if cum_face_you > 0:
            lines.append("На личике и волосах %s видны крупные белые капли вашей спермы." % real_name2)
        elif cum_face_others > 0:
            lines.append("На личике и волосах %s видны крупные белые капли чьей-то спермы." % real_name2)

        if cum_tits_you > 0 and int(_girls_desc_get(gm("TitsVisible"), g, 0) or 0):
            lines.append("Груди %s перемазаны в вашем семени." % real_name2)
        elif cum_tits_others > 0 and int(_girls_desc_get(gm("TitsVisible"), g, 0) or 0):
            lines.append("Груди %s перемазаны в чьем-то семени." % real_name2)

        if cum_inside_you > 0 and int(_girls_desc_get(gm("PussyVisible"), g, 0) or 0):
            lines.append("Из влагалища %s медленно вытекает сперма." % real_name2)
        elif cum_inside_others > 0 and int(_girls_desc_get(gm("PussyVisible"), g, 0) or 0):
            lines.append("Из влагалища %s медленно вытекает сперма." % real_name2)

        if cum_inside_you > 0 and short_skirt_no_panties:
            lines.append("Вы видите следы вашей спермы на бедрах %s." % real_name2)
        elif cum_inside_others > 0 and short_skirt_no_panties:
            lines.append("Вы видите следы чьей-то спермы на бедрах %s." % real_name2)

        preg = int(_girls_desc_get(gm("pregnancy"), g, 0) or 0)
        top_slut = int(_girls_desc_get(dress_part_slut, top, 0) or 0)

        if (not top or topraised) and preg >= 120:
            lines.append("%s явно беременна, о чем свидетельствует ее округлившийся животик." % real_name)
        elif top and (not topraised) and top_slut >= 3 and preg >= 120:
            lines.append("%s явно беременна, из-под легкой блузки виден округлившийся животик." % real_name)
        elif top and (not topraised) and top_slut < 3 and preg >= 180:
            lines.append("Даже закрытая одежда уже не может скрыть беременность %s." % real_name2)

        if int(_girls_desc_get(gm("Drunk"), g, 0) or 0) > 0:
            lines.append("%s слегка выпила, расслабилась и подобрела." % real_name)

        age_val = int(_girls_desc_stat_value(g, "age_girls", "age", default=0) or 0)
        friends_val = int(_girls_desc_stat_value(g, "Friends", "friends", default=0) or 0)
        lines.append("Ей %d лет." % age_val)
        lines.append("Уровень дружбы: %d." % friends_val)

        beauty_val = int(_girls_desc_get(gm("beauty"), g, 0) or 0)
        lines.append(_girls_desc_beauty_text(beauty_val))

        otkroven = int(_girls_desc_get(gm("otkroven"), g, 0) or 0)
        sluttiness_val = int(_girls_desc_get(gm("sluttiness"), g, 0) or 0)
        if otkroven >= 3:
            lines.append("Ее распущенность: %d." % sluttiness_val)

        cooking_val = int(_girls_desc_get(gm("cooking"), g, 0) or 0)
        cleaning_val = int(_girls_desc_get(gm("cleaning"), g, 0) or 0)
        waitress_val = int(_girls_desc_get(gm("waitress"), g, 0) or 0)
        lines.append("Она %s кухарка." % _girls_desc_skill_text(cooking_val))
        lines.append("Она %s уборщица." % _girls_desc_skill_text(cleaning_val))
        lines.append("Она %s официантка." % _girls_desc_skill_text(waitress_val))

        if otkroven >= 7:
            sexacts_val = int(_girls_desc_get(gm("sexacts"), g, 0) or 0)
            virginity_val = int(_girls_desc_get(gm("virginity"), g, 0) or 0)
            cuminside_val = int(_girls_desc_get(gm("cuminside"), g, 0) or 0)
            if sexacts_val == 0:
                lines.append("Она девственница.")
            elif virginity_val == 1:
                lines.append("Она не настолько невинна, как хочет казаться, но еще девственница.")
                lines.append("У нее было %d половых актов." % sexacts_val)
                lines.append("Ей кончали в киску %d раз." % cuminside_val)
            else:
                lines.append("У нее было %d половых актов." % sexacts_val)
                lines.append("Ей кончали в киску %d раз." % cuminside_val)

        if preg < 120:
            lines.append("На вид она не беременна.")
        else:
            if bool(getattr(renpy.store, "DebugFlag", False)):
                lines.append("Она беременна на %d неделе." % int(preg / 7))
            if preg >= 210:
                lines.append("%s беременна и находится на позднем сроке." % real_name)
            elif preg >= 150:
                lines.append("Средних размеров беременный животик напоминает о бурной личной жизни %s." % real_name)
            else:
                lines.append("Видно, что %s нагуляла себе животик, но он еще не очень заметен." % real_name)

        if otkroven >= 6:
            kids_val = int(_girls_desc_get(gm("kids"), g, 0) or 0)
            if kids_val == 0:
                lines.append("У нее нет детей.")
            elif kids_val == 1:
                lines.append("У нее один ребенок.")
            else:
                lines.append("У нее %d детей." % kids_val)

        return [line for line in lines if line]

label GirlsDesc(girl_name):
    scene black
    $ _gd_key = _girls_desc_resolve_key(girl_name)
    $ _gd_id = str(_gd_key or girl_name or "").lower()

    if _gd_id == "sandra":
        call ShowImageSeq("sandra", "", "portrait", 4)
    elif _gd_id == "melissa":
        call ShowImage("melissa", "", "portrait")
    elif _gd_id == "becky":
        call ShowBeckyPortrait
    elif _gd_id == "georgett":
        call ShowGeorgettPortrait
    elif _gd_id == "liza":
        call ShowLizaPortrait
    elif _gd_id == "amanda":
        call ShowAmandaPortrait
    elif _gd_id == "irma":
        call ShowImage("", "", irma_card_portrait_path())
    elif _gd_id == "clara":
        call ShowImage("clara", "", "portrait" + str(renpy.random.randint(1, 7)))
    elif _gd_id == "fran":
        call ShowImageSeq("ellona", "", "Fran", 4)
    elif _gd_id == "inga":
        call ShowImage("inga", "StreetSex", "minet" + str(renpy.random.randint(1, 5)))

    python:
        check_visibility(_gd_key or girl_name)
        _gd_lines = _girls_desc_build_lines(_gd_key or girl_name)

    python:
        for _gd_line in _gd_lines:
            renpy.say(None, str(_gd_line))

    return
