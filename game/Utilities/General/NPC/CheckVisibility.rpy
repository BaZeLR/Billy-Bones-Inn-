# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# CheckVisibility.rpy
# Converted from legacy script. Checks visibility of tits, pussy, and short skirt with no panties for a girl.
# All logic and assignments preserved and mapped to Ren'Py idioms.

init python:
    def check_visibility(girl_name):
        global TitsVisible, PussyVisible, ShortSkirtNoPanties
        if not isinstance(globals().get("TitsVisible", None), dict):
            TitsVisible = {}
        if not isinstance(globals().get("PussyVisible", None), dict):
            PussyVisible = {}
        if not isinstance(globals().get("ShortSkirtNoPanties", None), dict):
            ShortSkirtNoPanties = {}
        dress_part_slut = globals().get("DressPartSlut", {}) or {}
        TitsVisible[girl_name] = 0
        PussyVisible[girl_name] = 0
        ShortSkirtNoPanties[girl_name] = 0
        if bra.get(girl_name, '') == '' and (topdress.get(girl_name, '') == '' or topraised.get(girl_name, 0)):
            TitsVisible[girl_name] = 1
        if panties.get(girl_name, '') == '' and (bottomdress.get(girl_name, '') == '' or bottomraised.get(girl_name, 0)):
            PussyVisible[girl_name] = 1
        if panties.get(girl_name, '') == '' and int(bottomraised.get(girl_name, 0) or 0) == 0 and dress_part_slut.get(bottomdress.get(girl_name, ''), 0) >= 4:
            ShortSkirtNoPanties[girl_name] = 1

# Usage: check_visibility('liza')
# This will update the TitsVisible, PussyVisible, and ShortSkirtNoPanties dicts for the given girl.


label check_visibility(girl_name=""):
    $ check_visibility(girl_name)
    return


label CheckVisibility(girl_name=""):
    $ check_visibility(girl_name)
    return

init 4 python:
    import copy

    # Shared descriptive state for adult NPCs. Permanent identity is data;
    # mutable grooming/skin state is owned by BodyInteractionProfiles.
    NPC_APPEARANCE_PROFILES = {
        "amanda": {
            "signature": "teasing_awakening", "sensual": 1, "daring": 1, "grooming": 2,
            "skin": (18, 7, 9, 76, 45), "hair_density": ("light", "average", "average", 3), "pubic_barber": "careful_trim",
            "hair": "Светлые волосы Аманды мягко обрамляют лицо; в ее домашней небрежности всегда остается что-то задорное.",
            "barber": "После Серджио светлые волосы Аманды лежат особенно легко и аккуратно, открывая тонкую шею и делая ее живость почти вызывающей.",
            "body": (
                "Аманда тонкая в талии, с легкими бедрами и небольшой молодой грудью; ее фигура скорее дразнит намеком, чем пышностью.",
                "Когда Аманда замечает взгляд, тонкая талия, легкая линия бедер и небольшая упругая грудь вдруг становятся частью вполне сознательной игры."
            ),
            "neck": "У нее тонкая светлая шея и аккуратные плечи, на которых особенно заметна гладкость ухоженной кожи.",
            "hips": "Стройные ноги и легкие бедра Аманды заканчиваются тонкими лодыжками; в движении ее фигура кажется быстрой и гибкой.",
            "breasts": "Ее небольшая грудь выглядит легкой и упругой, естественно двигаясь вместе с телом.",
            "intimate": "У Аманды компактная вульва: полные внешние губы почти скрывают мягкие внутренние складки; небольшой капюшон плотно прикрывает клитор, оставляя заметной лишь его тонкую форму.",
        },
        "melissa": {
            "signature": "curious_soft", "sensual": 1, "daring": 0, "grooming": 2,
            "skin": (25, 9, 12, 70, 50), "hair_density": ("average", "average", "average", 3), "pubic_barber": "neat_trim",
            "hair": "Черные, почти вороньи волосы Мелиссы резко оттеняют оливковую кожу; чистыми и расчесанными они кажутся особенно густыми.",
            "barber": "После рук Серджио тяжелые черные волосы Мелиссы лежат ровнее и блестят глубже; она еще немного смущается собственной ухоженности.",
            "body": (
                "У Мелиссы мягкая фигура с полной грудью, узкой талией и округлыми бедрами; в ней больше естественной теплоты, чем нарочитого кокетства.",
                "Оливковая кожа, полная мягкая грудь и округлые бедра придают Мелиссе теплую чувственность, которая становится заметнее по мере того, как уходит ее смущение."
            ),
            "neck": "Черные волосы особенно красиво обрамляют теплую оливковую кожу на шее, ключицах и мягких плечах.",
            "hips": "Бедра Мелиссы полные и мягкие, ноги крепкие и женственные, с плавной линией от талии к коленям.",
            "breasts": "Полная грудь Мелиссы имеет естественный вес и мягкость, заметно отзываясь на каждый шаг.",
            "intimate": "У Мелиссы более узкая вульва со стройными внешними губами; между ними заметны мягкие, слегка несимметричные внутренние складки, а клитор частично прикрыт небольшим капюшоном.",
        },
        "sandra": {
            "signature": "mature_authority", "sensual": 1, "daring": 0, "grooming": 2,
            "skin": (28, 4, 14, 65, 42), "hair_density": ("average", "average", "dense", 3), "pubic_barber": "neat_trim",
            "hair": "Темные волосы Сандры обычно собраны практично; именно поэтому хорошая укладка сразу делает ее лицо и шею неожиданно женственными.",
            "barber": "После Серджио темные волосы Сандры лежат безупречно, открывая шею и скулы; привычная хозяйская строгость от этого становится лишь привлекательнее.",
            "body": (
                "Сандра — зрелая, пышная женщина с тяжелой большой грудью, крепкой талией и широкими женственными бедрами.",
                "Когда Сандра позволяет себе выглядеть не только хозяйкой, большая мягкая грудь, сильная талия и зрелая округлость бедер приобретают властную чувственность."
            ),
            "neck": "У Сандры сильные плечи и зрелая шея с мягкими линиями, особенно выигрышными, когда волосы аккуратно убраны.",
            "hips": "Ее бедра широкие, полные и сильные; ноги выдают женщину, привыкшую много часов проводить на ногах.",
            "breasts": "Очень большая грудь Сандры тяжелая и мягкая, с естественной зрелой посадкой.",
            "intimate": "У Сандры полная зрелая вульва с мягкими внешними губами и заметными внутренними складками; широкий капюшон частично прикрывает довольно выраженный клитор.",
        },
        "becky": {
            "signature": "warm_libertine", "sensual": 2, "daring": 2, "grooming": 3,
            "skin": (20, 3, 8, 74, 52), "hair_density": ("light", "average", "average", 2), "pubic_barber": "short_trim",
            "hair": "Рыжие волосы и теплая кожа Бекки создают живой здоровый контраст; она носит себя с непринужденностью женщины, вполне довольной своим телом.",
            "barber": "Свежая укладка делает рыжие волосы Бекки ярче, а лицо моложе; она замечает эффект сразу и носит его с естественным удовольствием.",
            "body": (
                "Бекки высокая и пышная, с полной грудью, мягкой талией и щедрыми округлыми бедрами; ее тело выглядит зрелым, здоровым и очень живым.",
                "Бекки чувственна без всякой позы: тяжелая грудь, мягкий живот, широкие бедра и длинные ноги двигаются свободно, а ее телесная уверенность делает близость почти осязаемой."
            ),
            "neck": "У Бекки открытая шея, мягкие плечи и светлая кожа с теплым живым оттенком.",
            "hips": "Полные бедра и длинные ноги Бекки сохраняют крепкую, здоровую форму, несмотря на зрелую мягкость ее тела.",
            "breasts": "Большая грудь Бекки мягкая и тяжелая, с естественной зрелой полнотой.",
            "intimate": "У Бекки широкая, мягко округлая вульва: полные внешние губы закрывают большую часть внутренних складок; клитор невелик и в основном укрыт мягким капюшоном.",
        },
        "georgett": {
            "signature": "professional_sensual", "sensual": 3, "daring": 3, "grooming": 4,
            "skin": (30, 4, 10, 72, 55), "hair_density": ("average", "light", "average", 3), "pubic_barber": "close_shave",
            "hair": "Светлые волосы Жоржетты всегда выглядят частью ее ремесла — уложенными так, чтобы лицо, шея и декольте сразу ловили взгляд.",
            "barber": "После профессионального ухода светлые волосы Жоржетты становятся мягче и ровнее; она оценивает результат почти деловито, уже понимая, как лучше его показать.",
            "body": (
                "Жоржетта невысока и немного пухла: крупная грудь, мягкий живот и полные бедра придают ей откровенно телесную привлекательность.",
                "Жоржетта двигается так, будто демонстрация тела — привычный язык: тяжелая грудь, мягкий живот и полные бедра подаются с уверенной профессиональной чувственностью."
            ),
            "neck": "Шея Жоржетты мягкая и светлая, плечи округлые и привычно открытые для чужого взгляда.",
            "hips": "Талия у нее мягкая, зато бедра полные, округлые и тяжелые.",
            "breasts": "Большая налитая грудь Жоржетты тяжелая, мягкая и заметно колышется при движении.",
            "intimate": "У Жоржетты полная вульва с хорошо заметными, мягко рифлеными внутренними губами; клитор выражен сильнее среднего и лишь частично прикрыт широким капюшоном.",
        },
        "clara": {
            "signature": "refined_playful", "sensual": 2, "daring": 1, "grooming": 4,
            "skin": (14, 2, 5, 85, 62), "hair_density": ("light", "light", "light", 2), "pubic_barber": "precise_trim",
            "hair": "Светлые волосы Клариссы выглядят дорого ухоженными даже в простой прическе; рядом почти всегда держится знакомый запах лаванды.",
            "barber": "После Серджио волосы Клариссы лежат с почти безупречной легкостью; хорошая стрижка лишь усиливает впечатление дорогого ухода.",
            "body": (
                "Кларисса стройна и грациозна: мягкая грудь, тонкая талия и легкие бедра подчинены той же плавности, что и ее походка.",
                "Даже откровенный взгляд Кларисса превращает в игру хорошего вкуса: тонкая талия, мягкая грудь и гладкая линия бедер открываются ровно настолько, насколько она решила позволить."
            ),
            "neck": "Длинная шея и тонкие плечи Клариссы выглядят особенно изящно на фоне светлых волос.",
            "hips": "Тонкая талия, легкие бедра и длинные стройные ноги образуют почти танцевальную линию.",
            "breasts": "Ее грудь среднего малого размера мягкая, аккуратная и естественно покачивается при движении.",
            "intimate": "У Клариссы стройная вульва с тонкими внешними губами и более заметными длинными внутренними складками; небольшой клитор частично прикрыт узким аккуратным капюшоном.",
        },
        "irma": {
            "signature": "fashion_precision", "sensual": 2, "daring": 2, "grooming": 5,
            "skin": (10, 2, 4, 86, 58), "hair_density": ("light", "light", "light", 2), "pubic_barber": "precise_trim",
            "hair": "Ирма относится к волосам почти как к ткани хорошего платья: ни одна выбившаяся прядь не кажется случайной, а форма прически согласована с одеждой.",
            "barber": "Свежую работу цирюльника Ирма тут же превращает в часть общего образа, подбирая к новой линии волос одежду, украшения и выражение лица.",
            "body": (
                "Ирма высокая, очень стройная и почти фарфорово-бледная; небольшая грудь, узкая талия и длинные ноги образуют резкий модный силуэт.",
                "Ирма умеет сделать даже худобу чувственной: длинная шея, узкая талия, небольшая грудь и бесконечные ноги подчеркнуты с точностью профессионального портного."
            ),
            "neck": "Длинная тонкая шея Ирмы и острые плечи усиливают ее почти эльфийскую хрупкость.",
            "hips": "Ноги Ирмы длинные, тонкие и прямые, словно специально созданные для чулок и высоких каблуков.",
            "breasts": "Небольшая грудь Ирмы аккуратная и легкая, хорошо подходящая ее очень стройному телосложению.",
            "intimate": "У Ирмы узкая аккуратная вульва со стройными внешними губами и небольшой естественной асимметрией внутренних складок; клитор невелик и почти полностью прикрыт тонким капюшоном.",
        },
        "inga": {
            "signature": "energetic_bold", "sensual": 2, "daring": 2, "grooming": 2,
            "skin": (34, 18, 18, 68, 48), "hair_density": ("average", "average", "average", 3), "pubic_barber": "short_trim",
            "hair": "Рыжие волосы Инги яркие и живые, как у Бекки, но носит она их менее чинно: пряди чаще выбиваются, будто не успевая за ее движениями.",
            "barber": "После хорошей стрижки рыжие волосы Инги впервые лежат почти образцово; она явно сомневается, долго ли выдержит такую аккуратность, но эффект ей нравится.",
            "body": (
                "Инга высокая и крепко сложенная; большая молодая грудь, длинные ноги и округлые бедра делают сходство с Бекки очевидным, хотя в ней больше резкой энергии.",
                "Инга пользуется своей привлекательностью импульсивно: полная грудь, четкая талия, округлые бедра и длинные ноги оказываются подчеркнуты скорее дерзким движением, чем рассчитанной позой."
            ),
            "neck": "У Инги высокая шея и открытые крепкие плечи, часто усыпанные легкими рыжеватыми веснушками.",
            "hips": "Ноги Инги длинные и крепкие, бедра упругие и округлые.",
            "breasts": "Большая молодая грудь Инги полная и более упругая, чем у ее матери.",
            "intimate": "У Инги округлая вульва с полными внешними губами и умеренно заметными мягкими внутренними складками; клитор среднего размера частично прикрыт мягким капюшоном.",
        },
    }

    NPC_BODY_PRODUCT_PROFILES = {
        "soap_001": (32, 4, -12, -3, -1, 2, 1, "простого чистого мыла", 1, 4),
        "luxury_soap_001": (46, 14, -16, -6, -2, 10, -3, "мягкого мыла и оливкового масла", 3, 12),
    }

    def _npc_desc_clamp(value):
        try:
            return max(0, min(100, int(value)))
        except Exception:
            return 0

    def _npc_desc_key(girl_name=""):
        return str(_girls_desc_resolve_key(girl_name) or girl_name or "").strip().lower()

    def _npc_desc_clock_minute():
        try:
            calendar_v2.sync_state()
            return int(getattr(renpy.store, "dayspassed", 0) or 0) * 1440 + (int(calendar_v2.hour or 0) % 24) * 60 + (int(calendar_v2.minute or 0) % 60)
        except Exception:
            return int(getattr(renpy.store, "dayspassed", 0) or 0) * 1440

    def _girls_desc_age_value(girl_name=""):
        key = _npc_desc_key(girl_name)
        for map_name in ("age_girls", "age"):
            value = _girls_desc_get(_girls_desc_map(map_name, {}), key, None)
            try:
                if value is not None and int(value) > 0:
                    return int(value)
            except Exception:
                pass
        birth = _girls_desc_get(_girls_desc_map("DateOfBirth", {}), key, {}) or {}
        try:
            return max(0, int(getattr(renpy.store, "year", 1100) or 1100) - int(birth.get("cycle", 1100) or 1100))
        except Exception:
            return 0

    def npc_appearance_profile(girl_name=""):
        key = _npc_desc_key(girl_name)
        profile = NPC_APPEARANCE_PROFILES.get(key)
        if not isinstance(profile, dict):
            return {}
        person = getPersonInfo(key)
        data_obj = getattr(person, "data", None) if person is not None else None
        if data_obj is not None and not isinstance(getattr(data_obj, "appearance_profile", None), dict):
            data_obj.appearance_profile = copy.deepcopy(profile)
        return getattr(data_obj, "appearance_profile", profile) if data_obj is not None else copy.deepcopy(profile)

    def _npc_desc_default_state(profile):
        oil, acne, blackheads, softness, sheen = profile.get("skin", (25, 5, 8, 65, 40))
        leg_density, pit_density, pubic_density, _growth = profile.get("hair_density", ("average", "average", "average", 3))
        def zone(density):
            return {"state": "natural", "density": density, "last_groom_minute": -1}
        return {
            "cleanliness": 62,
            "skin": {"oiliness": oil, "acne": acne, "blackheads": blackheads, "softness": softness, "sheen": sheen, "irritation": 0},
            "head_hair": {"condition": 65, "style": "normal", "last_barber_minute": -1},
            "body_hair": {"legs": zone(leg_density), "underarms": zone(pit_density), "pubic": zone(pubic_density)},
            "grooming": {"quality": max(0, min(5, int(profile.get("grooming", 2) or 2))), "last_service": "", "last_service_minute": -1, "last_wash_minute": -1, "last_product": "", "legacy_barber_day": -1},
            "scent": {"type": "", "strength": 0, "expires_minute": -1},
        }

    def _npc_desc_apply_barber(profile, state, minute_value):
        state["cleanliness"] = max(_npc_desc_clamp(state.get("cleanliness", 0)), 92)
        skin = state.setdefault("skin", {})
        skin["oiliness"] = _npc_desc_clamp(int(skin.get("oiliness", 0) or 0) - 7)
        skin["blackheads"] = _npc_desc_clamp(int(skin.get("blackheads", 0) or 0) - 3)
        skin["softness"] = _npc_desc_clamp(int(skin.get("softness", 0) or 0) + 10)
        skin["sheen"] = _npc_desc_clamp(int(skin.get("sheen", 0) or 0) + 10)
        skin["irritation"] = _npc_desc_clamp(int(skin.get("irritation", 0) or 0) + 4)
        state["head_hair"] = {"condition": 96, "style": "barber", "last_barber_minute": minute_value}
        state["grooming"].update({"quality": 5, "last_service": "barber_full", "last_service_minute": minute_value})
        for zone_name in ("legs", "underarms"):
            state["body_hair"][zone_name].update({"state": "fresh_shaved", "last_groom_minute": minute_value})
        state["body_hair"]["pubic"].update({"state": profile.get("pubic_barber", "neat_trim"), "last_groom_minute": minute_value})
        return state

    def npc_appearance_state(girl_name=""):
        key = _npc_desc_key(girl_name)
        profile = npc_appearance_profile(key)
        if not profile:
            return {}
        person = getPersonInfo(key)
        display_name = str(getattr(getattr(person, "data", None), "fullname", "") or key) if person is not None else key
        body_profile = bodymodel_sync_character(key, display_name, "female")
        state = body_profile.get("appearance") if isinstance(body_profile, dict) else None
        if not isinstance(state, dict):
            state = _npc_desc_default_state(profile)
            body_profile["appearance"] = state
        raw_day = _girls_desc_get(_girls_desc_map("BarberVisitLastDay", {}), key, None)
        try:
            barber_day = int(raw_day) if raw_day is not None else -1
        except Exception:
            barber_day = -1
        imported = state.get("grooming", {}).get("legacy_barber_day", -1)
        try:
            imported = int(imported)
        except Exception:
            imported = -1
        if barber_day >= 0 and barber_day > imported:
            _npc_desc_apply_barber(profile, state, barber_day * 1440 + 720)
            state["grooming"]["legacy_barber_day"] = barber_day
        BodyInteractionProfiles[key] = body_profile
        return state

    def npc_apply_grooming(girl_name="", service="barber_full"):
        profile = npc_appearance_profile(girl_name)
        state = npc_appearance_state(girl_name)
        if not profile or not state:
            return False
        service = str(service or "").strip().lower()
        if service in ("barber", "barber_full", "full_grooming"):
            _npc_desc_apply_barber(profile, state, _npc_desc_clock_minute())
            state["grooming"]["legacy_barber_day"] = int(getattr(renpy.store, "dayspassed", 0) or 0)
            return True
        if service in ("wash", "bath"):
            state["cleanliness"] = max(_npc_desc_clamp(state.get("cleanliness", 0)), 88)
            state["grooming"]["last_wash_minute"] = _npc_desc_clock_minute()
            return True
        return False

    def npc_set_body_hair_state(girl_name="", zone="legs", hair_state="natural"):
        state = npc_appearance_state(girl_name)
        zone = str(zone or "").strip().lower()
        if not state or zone not in ("legs", "underarms", "pubic"):
            return False
        state["body_hair"][zone].update({"state": str(hair_state or "natural").strip().lower(), "last_groom_minute": _npc_desc_clock_minute()})
        return True

    def npc_apply_body_product(girl_name="", item_id="soap_001"):
        state = npc_appearance_state(girl_name)
        effect = NPC_BODY_PRODUCT_PROFILES.get(str(item_id or "").strip())
        if not state or not effect:
            return False
        cleaning, softness, oil, blackheads, acne, sheen, irritation, scent_name, scent_strength, scent_hours = effect
        state["cleanliness"] = _npc_desc_clamp(int(state.get("cleanliness", 0) or 0) + cleaning)
        skin = state["skin"]
        for name, delta in (("softness", softness), ("oiliness", oil), ("blackheads", blackheads), ("acne", acne), ("sheen", sheen), ("irritation", irritation)):
            skin[name] = _npc_desc_clamp(int(skin.get(name, 0) or 0) + delta)
        now = _npc_desc_clock_minute()
        state["grooming"].update({"last_wash_minute": now, "last_product": str(item_id or ""), "quality": max(int(state["grooming"].get("quality", 0) or 0), 4 if "luxury" in str(item_id) else 3)})
        state["scent"] = {"type": scent_name, "strength": scent_strength, "expires_minute": now + scent_hours * 60}
        return True

    def _npc_desc_intensity(girl_name, profile, state, context):
        if "intensity" in context:
            try:
                return max(0, min(4, int(context["intensity"])))
            except Exception:
                pass
        person = getPersonInfo(_npc_desc_key(girl_name))
        rel = int(getattr(person, "rel", 0) or 0) if person is not None else 0
        openness = int(getattr(person, "openness", 0) or 0) if person is not None else 0
        corruption = int(getattr(person, "corruption", 0) or 0) if person is not None else 0
        flirted = int(getattr(person, "flirted_today", 0) or 0) if person is not None else 0
        score = int(profile.get("sensual", 0) or 0) + int(profile.get("daring", 0) or 0)
        score += (1 if rel >= 5 else 0) + (1 if rel >= 10 else 0) + (1 if openness >= 3 else 0) + (1 if openness >= 6 else 0)
        score += (1 if corruption >= 45 else 0) + (1 if flirted else 0) + (1 if int(state["grooming"].get("quality", 0) or 0) >= 4 else 0)
        return 0 if score <= 1 else 1 if score <= 3 else 2 if score <= 5 else 3 if score <= 7 else 4

    def _npc_desc_skin_line(state, intensity):
        skin = state["skin"]
        clean = _npc_desc_clamp(state.get("cleanliness", 0))
        oil, acne, blackheads = (_npc_desc_clamp(skin.get(k, 0)) for k in ("oiliness", "acne", "blackheads"))
        softness, sheen, irritation = (_npc_desc_clamp(skin.get(k, 0)) for k in ("softness", "sheen", "irritation"))
        if clean < 35:
            return "Кожа выглядит несвежей, с жирным налетом и следами долгого дня."
        if acne >= 35:
            return "Кожа чистая, но проблемная: заметны воспаленные прыщики, неровная текстура и темные закупоренные поры."
        if oil >= 65 and blackheads >= 25:
            return "Несмотря на чистоту, кожа быстро покрывается жирным блеском; вокруг носа и на подбородке заметны темные точки забитых пор."
        if blackheads >= 28:
            return "Кожа в целом чистая, хотя вблизи заметны темные точки пор и несколько неровностей."
        if acne >= 16:
            return "На чистой коже остается несколько прыщиков и мелких неровностей, особенно заметных вблизи."
        if irritation >= 20:
            return "После недавнего бритья местами заметна легкая краснота и чувствительная шероховатость."
        if clean >= 85 and softness >= 82 and sheen >= 55:
            return "Кожа выглядит почти шелковой: чистая, очень мягкая, с тонким живым блеском." if intensity >= 2 else "Кожа очень чистая и гладкая, с мягким здоровым блеском."
        if clean >= 75 and softness >= 68:
            return "Кожа выглядит свежей, чистой и мягкой; вместо жирного блеска на ней остается лишь здоровое ровное сияние."
        return "Кожа выглядит чистой, с естественной текстурой и легким живым блеском."

    def _npc_desc_hair_stage(profile, zone_state):
        stage = str(zone_state.get("state", "natural") or "natural")
        if stage != "fresh_shaved":
            return stage
        raw_last = zone_state.get("last_groom_minute", -1)
        try:
            last = int(raw_last)
        except Exception:
            last = -1
        if last < 0:
            return stage
        hours = max(0, int((_npc_desc_clock_minute() - last) / 60))
        growth = int(profile.get("hair_density", ("", "", "", 3))[3] or 3)
        if hours < 18 + (3 - growth) * 4:
            return "silky_shaved"
        if hours < 42 + (3 - growth) * 8:
            return "micro_stubble"
        if hours < 84 + (3 - growth) * 12:
            return "stubble"
        if hours < 144 + (3 - growth) * 18:
            return "soft_regrowth"
        return "natural"

    def _npc_desc_body_hair_line(profile, state, zone, intensity):
        data = state["body_hair"][zone]
        stage = _npc_desc_hair_stage(profile, data)
        prefix = {"legs": "На открытых ногах", "underarms": "В подмышках", "pubic": "На лобке"}[zone]
        if stage in ("fresh_shaved", "silky_shaved"):
            return "%s кожа выбрита совсем гладко; она выглядит мягкой и шелковистой." % prefix if intensity >= 2 else "%s кожа тщательно выбрита, без заметной щетины." % prefix
        if stage == "micro_stubble":
            return "%s уже проступают крошечные темные точки нового роста — почти невидимые, но нарушающие вчерашнюю гладкость." % prefix
        if stage == "stubble":
            return "%s появилась короткая мелкая щетинка: на ощупь кожа была бы уже слегка колючей." % prefix
        if stage == "soft_regrowth":
            return "%s короткая щетина успела смягчиться и превратиться в тонкий мягкий пушок." % prefix
        if stage in ("precise_trim", "careful_trim", "neat_trim", "short_trim"):
            return "%s волосы аккуратно и коротко подстрижены, оставляя вид явно ухоженным." % prefix
        density = {"light": "редкий тонкий пушок", "average": "естественный заметный покров", "dense": "густой естественный покров"}.get(str(data.get("density", "average")), "естественный волосяной покров")
        return "%s остается %s." % (prefix, density)

    def _npc_desc_visible_zones(girl_name, context):
        key = _girls_desc_resolve_key(girl_name) or girl_name
        visible = set(context.get("visible_zones", []) or [])
        if int(_girls_desc_get(_girls_desc_map("TitsVisible", {}), key, 0) or 0):
            visible.update(("breasts", "upper"))
        if int(_girls_desc_get(_girls_desc_map("PussyVisible", {}), key, 0) or 0):
            visible.update(("pubic", "vulva", "thighs"))
        bottom = _girls_desc_get(_girls_desc_map("bottomdress", {}), key, "")
        if bool(_girls_desc_get(_girls_desc_map("bottomraised", {}), key, 0)) or not bottom or int(_girls_desc_get(_girls_desc_map("DressPartSlut", {}), bottom, 0) or 0) >= 4:
            visible.update(("legs", "thighs"))
        top = _girls_desc_get(_girls_desc_map("topdress", {}), key, "")
        if bool(_girls_desc_get(_girls_desc_map("topraised", {}), key, 0)) or not top or int(_girls_desc_get(_girls_desc_map("DressPartSlut", {}), top, 0) or 0) >= 3:
            visible.add("neck")
        if context.get("underarms_visible"):
            visible.add("underarms")
        return visible

    def npc_appearance_description_lines(girl_name="", context=None):
        key = _npc_desc_key(girl_name)
        profile, state = npc_appearance_profile(key), npc_appearance_state(key)
        if not profile or not state:
            return []
        context = dict(context or {})
        intensity = _npc_desc_intensity(key, profile, state, context)
        visible = _npc_desc_visible_zones(key, context)
        lines = [profile["barber"] if state["head_hair"].get("style") == "barber" else profile["hair"], _npc_desc_skin_line(state, intensity)]
        lines.append(profile["body"][1 if intensity >= 2 else 0])
        if "neck" in visible and intensity >= 1:
            lines.append(profile["neck"])
        if "thighs" in visible and intensity >= 2:
            lines.append(profile["hips"])
        if "breasts" in visible and intensity >= 2:
            lines.append(profile["breasts"])
        scent = state.get("scent", {})
        raw_expiry = scent.get("expires_minute", -1)
        try:
            expiry = int(raw_expiry)
        except Exception:
            expiry = -1
        if scent.get("type") and int(scent.get("strength", 0) or 0) > 0 and (expiry < 0 or _npc_desc_clock_minute() <= expiry):
            lines.append("Вблизи от нее держится запах %s." % scent["type"])
        if "legs" in visible and intensity >= 1:
            lines.append(_npc_desc_body_hair_line(profile, state, "legs", intensity))
        if "underarms" in visible and intensity >= 1:
            lines.append(_npc_desc_body_hair_line(profile, state, "underarms", intensity))
        if ("pubic" in visible or "vulva" in visible) and _girls_desc_age_value(key) >= 18:
            lines.append(_npc_desc_body_hair_line(profile, state, "pubic", intensity))
            if "vulva" in visible and intensity >= 2:
                lines.append(profile["intimate"])
        result = []
        for line in lines:
            line = str(line or "").strip()
            if line and line not in result:
                result.append(line)
        try:
            budget = max(1, int(context.get("detail_budget", 7) or 7))
        except Exception:
            budget = 7
        return result[:budget]


init 5 python:
    # Extend the existing GirlsDesc builder; do not add another description UI.
    _girls_desc_build_lines_core = _girls_desc_build_lines

    def _girls_desc_build_lines(girl_name):
        lines = list(_girls_desc_build_lines_core(girl_name) or [])
        appearance = npc_appearance_description_lines(girl_name, {"scene": "profile", "detail_budget": 7})
        if not appearance:
            return lines
        insert_at = 1 if lines else 0
        return lines[:insert_at] + appearance + lines[insert_at:]
