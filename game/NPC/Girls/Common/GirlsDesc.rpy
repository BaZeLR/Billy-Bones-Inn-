# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
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

    def _girls_desc_resolve_key(girl_name):
        return people_normalize_id(girl_name)

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

    def _girls_desc_recent_barber_line(girl_key=""):
        key = str(girl_key or "").strip().lower()
        if key not in ("sandra", "melissa", "amanda", "becky", "clara"):
            return ""
        last_day = int(household.barber_visit_last_day.get(key, -99) or -99)
        current_day = int(calendar_v2.daysInGame or 0)
        if last_day < 0 or current_day - last_day > 14:
            return ""
        if key == "sandra":
            return "После визита к Серджио волосы Сандры лежат аккуратнее обычного, и весь ее вид кажется собраннее и чище."
        if key == "melissa":
            return "После визита к Серджио Мелисса выглядит заметно ухоженнее; это делает ее движения спокойнее и увереннее."
        if key == "amanda":
            return "После визита к Серджио Аманда выглядит особенно живо и ухоженно, словно уже заранее примеряет на себя больше внимания от гостей."
        if key == "becky":
            return "Недавний визит к Серджио пошел Бекки на пользу: она выглядит свежее и явно знает об этом."
        return "После визита к Серджио она выглядит аккуратнее и заметно ухоженнее обычного."

    def _girls_desc_build_lines(girl_name):
        g = _girls_desc_resolve_key(girl_name)
        if not g:
            g = str(girl_name or "")
        girl_info = people.get_info(g)

        person_data = people.get_data(g)
        real_name = str(person_data.cname or person_data.fullname or g) if person_data is not None else g
        real_name2 = str(person_data.genitive or real_name) if person_data is not None else real_name
        lines = []

        base_desc = str(person_data.description or "") if person_data is not None else ""
        if base_desc:
            lines.append(base_desc)
        barber_line = _girls_desc_recent_barber_line(g)
        if barber_line:
            lines.append(barber_line)

        top = girl_info.clothing_layer("top") if girl_info is not None else ""
        bra = girl_info.clothing_layer("bra") if girl_info is not None else ""
        bottom = girl_info.clothing_layer("bottom") if girl_info is not None else ""
        panties = girl_info.clothing_layer("panties") if girl_info is not None else ""
        legs = girl_info.current_underwear("legs", "") if girl_info is not None else ""
        shoes = girl_info.current_underwear("shoes", "") if girl_info is not None else ""
        top_raised = bool(girl_info.layer_raised("top")) if girl_info is not None else False
        bottom_raised = bool(girl_info.layer_raised("bottom")) if girl_info is not None else False
        dress_part_desc = DressPartDesc
        dress_part_slut = DressPartSlut

        if girl_info is not None and int(girl_info.sex_stat("lactate", 0) or 0) == 1:
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
                if top_raised:
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
                if top_raised:
                    line += ". Сейчас эта блузка бесстыдно распахнута и груди прикрыты лишь лифчиком. " + lactated_tits_desc
                elif top_slut >= 4:
                    line += ". Глубокий вырез блузки открывал бы прекрасный вид на груди %s, если бы не лиф. %s" % (real_name2, lactated_tits_desc)
                elif top_slut >= 3:
                    line += ". Под тонкой тканью просматриваются очертания лифчика. " + lactated_tits_desc
                else:
                    line += "."

            lines.append(line.strip())
        elif bra:
            bra_desc = _girls_desc_get(FullDressDesc, bra, bra).lower()
            line = "Она одета только в %s." % bra_desc
            if lactated_tits_desc:
                line += " " + lactated_tits_desc
            lines.append(line)

        if bottom and bottom != "nightshirtbottom":
            bottom_desc = _girls_desc_get(dress_part_desc, bottom, bottom)
            prefix = "Также она одета в " if (top or bra) else "Она одета в "
            line = prefix + bottom_desc
            bottom_slut = int(_girls_desc_get(dress_part_slut, bottom, 0) or 0)

            if bottom_raised:
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
            panties_desc = _girls_desc_get(FullDressDesc, panties, panties).lower()
            prefix = "Также она одета в " if (top or bra) else "Она одета в "
            lines.append(prefix + panties_desc + ".")

        if (bottom_raised or not bottom or int(_girls_desc_get(dress_part_slut, bottom, 0) or 0) >= 4) and legs:
            legs_desc = _girls_desc_get(dress_part_desc, legs, legs)
            line = "Ее ножки обтянуты %s" % legs_desc
            if (not bottom_raised) and bottom and int(_girls_desc_get(dress_part_slut, bottom, 0) or 0) >= 5:
                line += ", эротично кончающимися чуть ниже юбочки."
            else:
                line += "."
            lines.append(line)

        if shoes == "simpleshoes":
            lines.append("На ее ногах простые башмаки.")
        elif shoes == "highshoes":
            lines.append("На ее ногах башмачки на очень высоком каблуке.")

        if girl_info is not None and girl_info.tits_visible():
            line = "Ее сиськи бесстыдно обнажены."
            if lactated_tits_desc:
                line += " " + lactated_tits_desc
            lines.append(line)

        if girl_info is not None and girl_info.pussy_visible():
            lines.append("Ее влагалище ничем не прикрыто от нескромных взглядов.")

        cum_face_you = girl_info.cum_state("cum_face_you") if girl_info is not None else 0
        cum_face_others = girl_info.cum_state("cum_face_others") if girl_info is not None else 0
        cum_tits_you = girl_info.cum_state("cum_tits_you") if girl_info is not None else 0
        cum_tits_others = girl_info.cum_state("cum_tits_others") if girl_info is not None else 0
        cum_inside_you = girl_info.cum_state("cum_inside_you") if girl_info is not None else 0
        cum_inside_others = girl_info.cum_state("cum_inside_others") if girl_info is not None else 0
        short_skirt_no_panties = girl_info.short_skirt_no_panties() if girl_info is not None else False

        if cum_face_you > 0:
            lines.append("На личике и волосах %s видны крупные белые капли вашей спермы." % real_name2)
        elif cum_face_others > 0:
            lines.append("На личике и волосах %s видны крупные белые капли чьей-то спермы." % real_name2)

        if cum_tits_you > 0 and girl_info is not None and girl_info.tits_visible():
            lines.append("Груди %s перемазаны в вашем семени." % real_name2)
        elif cum_tits_others > 0 and girl_info is not None and girl_info.tits_visible():
            lines.append("Груди %s перемазаны в чьем-то семени." % real_name2)

        if cum_inside_you > 0 and girl_info is not None and girl_info.pussy_visible():
            lines.append("Из влагалища %s медленно вытекает сперма." % real_name2)
        elif cum_inside_others > 0 and girl_info is not None and girl_info.pussy_visible():
            lines.append("Из влагалища %s медленно вытекает сперма." % real_name2)

        if cum_inside_you > 0 and short_skirt_no_panties:
            lines.append("Вы видите следы вашей спермы на бедрах %s." % real_name2)
        elif cum_inside_others > 0 and short_skirt_no_panties:
            lines.append("Вы видите следы чьей-то спермы на бедрах %s." % real_name2)

        preg = girl_info.pregnancy_days() if girl_info is not None else 0
        top_slut = int(_girls_desc_get(dress_part_slut, top, 0) or 0)

        if (not top or top_raised) and preg >= 120:
            lines.append("%s явно беременна, о чем свидетельствует ее округлившийся животик." % real_name)
        elif top and (not top_raised) and top_slut >= 3 and preg >= 120:
            lines.append("%s явно беременна, из-под легкой блузки виден округлившийся животик." % real_name)
        elif top and (not top_raised) and top_slut < 3 and preg >= 180:
            lines.append("Даже закрытая одежда уже не может скрыть беременность %s." % real_name2)

        if girl_info is not None and int(getattr(girl_info, "drunk", 0) or 0) > 0:
            lines.append("%s слегка выпила, расслабилась и подобрела." % real_name)

        age_val = people_age(g, 0)
        friends_val = int(getattr(girl_info, "rel", 0) or 0) if girl_info is not None else 0
        lines.append("Ей %d лет." % age_val)
        lines.append("Уровень дружбы: %d." % friends_val)

        beauty_val = int(girl_info.sex_stat("beauty", 0) or 0) if girl_info is not None else 0
        lines.append(_girls_desc_beauty_text(beauty_val))

        otkroven = int(getattr(girl_info, "openness", 0) or 0) if girl_info is not None else 0
        sluttiness_val = int(getattr(girl_info, "corruption", 0) or 0) if girl_info is not None else 0
        if otkroven >= 3:
            lines.append("Ее распущенность: %d." % sluttiness_val)

        cooking_val = int(girl_info.skill_value("cooking", 0) or 0) if girl_info is not None else 0
        cleaning_val = int(girl_info.skill_value("cleaning", 0) or 0) if girl_info is not None else 0
        waitress_val = int(girl_info.skill_value("waitress", 0) or 0) if girl_info is not None else 0
        lines.append("Она %s кухарка." % _girls_desc_skill_text(cooking_val))
        lines.append("Она %s уборщица." % _girls_desc_skill_text(cleaning_val))
        lines.append("Она %s официантка." % _girls_desc_skill_text(waitress_val))

        if otkroven >= 7:
            sexacts_val = int(girl_info.sex_stat("sexacts", 0) or 0)
            virginity_val = int(girl_info.sex_stat("virginity", True))
            cuminside_val = int(girl_info.sex_stat("cuminside", 0) or 0)
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
            if bool(config.developer):
                lines.append("Она беременна на %d неделе." % int(preg / 7))
            if preg >= 210:
                lines.append("%s беременна и находится на позднем сроке." % real_name)
            elif preg >= 150:
                lines.append("Средних размеров беременный животик напоминает о бурной личной жизни %s." % real_name)
            else:
                lines.append("Видно, что %s нагуляла себе животик, но он еще не очень заметен." % real_name)

        if otkroven >= 6:
            kids_val = int(girl_info.sex_stat("kids", 0) or 0) if girl_info is not None else 0
            if kids_val == 0:
                lines.append("У нее нет детей.")
            elif kids_val == 1:
                lines.append("У нее один ребенок.")
            else:
                lines.append("У нее %d детей." % kids_val)

        return [line for line in lines if line]

label GirlsDesc(girl_name):
    $ renpy.dynamic("_gd_key", "_gd_id", "_gd_lines", "_gd_line")
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
        call ShowImage("clara", "", "portrait" + str(procedural_randint(1, 7, key="procedural:NPC/Girls/Common/GirlsDesc.rpy:procedural_randint:419:1")))
    elif _gd_id == "fran":
        call ShowImageSeq("ellona", "", "Fran", 4)
    elif _gd_id == "inga":
        call ShowImage("inga", "StreetSex", "minet" + str(procedural_randint(1, 5, key="procedural:NPC/Girls/Common/GirlsDesc.rpy:procedural_randint:423:2")))

    python:
        check_visibility(_gd_key or girl_name)
        _gd_lines = _girls_desc_build_lines(_gd_key or girl_name)

    python:
        for _gd_line in _gd_lines:
            renpy.say(None, str(_gd_line))

    return
