# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -44 python:
    import re
    import renpy

    def _kids_state():
        runtime = player
        if not isinstance(runtime.history, dict):
            runtime.history = {}
        state = runtime.history.setdefault("kids", {})
        state.setdefault("list", [])
        state.setdefault("next_id", 1)
        return state

    def _kids_int(v, d=0):
        try:
            return int(v)
        except Exception:
            try:
                return int(float(v))
            except Exception:
                return d

    def _kids_person_stat(person_name, stat_key, default=0):
        info = people.get_info(person_name)
        if info is None or not hasattr(info, "sex_stat"):
            return default
        return info.sex_stat(stat_key, default)

    def _kids_lactating(person_name):
        lactate_value = _kids_person_stat(person_name, "lactate", None)
        if lactate_value is None:
            lactate_value = _kids_person_stat(person_name, "breastfeed", 0)
        return _kids_int(lactate_value, 0) != 0

    def _kids_list():
        return _kids_state()["list"]

    def kids_count_for_mothers(*mom_names):
        mothers = set(str(name or "") for name in mom_names)
        return sum(1 for row in _kids_list() if str(row.get("MomName", "")) in mothers)

    def _kids_find_row(kid_id):
        kid_id = _kids_int(kid_id, 0)
        for row in _kids_list():
            if _kids_int(row.get("KidId", 0), 0) == kid_id:
                return row
        return None

    def CreateKid(MomName):
        MomName = str(MomName or "")
        current_days = _kids_int(calendar_v2.daysInGame, 0)
        mom_info = people.get_info(MomName)
        if mom_info is None:
            return 0

        if ZaletSuspectLinesCount(MomName) == 0:
            ZaletGetSuspectList(MomName)

        AssumedDad = str(ZaletSuspectGetValue(MomName, 1, "DudeName", "") or "")
        PregnancyID = _kids_int(ZaletGetExactId(MomName), 0)
        DadName = ""
        DaddyType = ""
        for row in sex_history_rows(MomName):
            if _kids_int(row.get("RowId", 0), 0) == PregnancyID:
                DadName = str(row.get("DudeName", "") or "")
                DaddyType = str(row.get("DudeNameType", "") or "")
                break

        KidGender = "Male" if procedural_randint(1, 2, "kid_gender_%s_%s" % (MomName, current_days)) == 2 else "Female"
        if MomName in ["liza", "georgett"]:
            KidName = RandomNameCode(KidGender, "French")
        elif MomName in ["becky", "inga"]:
            KidName = RandomNameCode(KidGender, "German")
        else:
            KidName = RandomNameCode(KidGender)

        if MomName == "liza":
            if re.fullmatch(r".*негр.*", str(DaddyType).lower()):
                KidRace = "N" if procedural_randint(1, 2, "kid_race_liza_black_%s" % current_days) == 1 else "M"
            else:
                KidRace = "M" if procedural_randint(1, 2, "kid_race_liza_%s" % current_days) == 1 else "W"
        else:
            KidRace = "M" if re.fullmatch(r".*негр.*", str(DadName).lower()) else "W"

        r = procedural_randint(1, 4, "kid_eyes_%s_%s" % (MomName, current_days))
        if KidRace == "N":
            r = procedural_randint(3, 4, "kid_eyes_black_%s_%s" % (MomName, current_days))
        if KidRace == "M" and r <= 2:
            r = procedural_randint(1, 4, "kid_eyes_mixed_%s_%s" % (MomName, current_days))
        KidEyes = "B" if r == 1 else ("G" if r in [2, 4] else "D")

        r = procedural_randint(1, 5, "kid_hair_%s_%s" % (MomName, current_days))
        if KidRace == "M" and r != 1:
            r = procedural_randint(1, 5, "kid_hair_mixed_1_%s_%s" % (MomName, current_days))
        if KidRace == "M" and r != 1:
            r = procedural_randint(1, 5, "kid_hair_mixed_2_%s_%s" % (MomName, current_days))
        if MomName in ["becky", "inga"] and r != 4:
            r = procedural_randint(1, 5, "kid_hair_german_1_%s_%s" % (MomName, current_days))
        if MomName in ["becky", "inga"] and r != 4:
            r = procedural_randint(1, 5, "kid_hair_german_2_%s_%s" % (MomName, current_days))
        if KidRace == "N":
            r = 1
        KidHair = "D" if r == 1 else ("P" if r == 2 else ("L" if r == 3 else ("R" if r == 4 else "B")))

        r = procedural_randint(1, 5, "kid_hairstyle_%s_%s" % (MomName, current_days))
        if KidRace == "N":
            r = procedural_randint(3, 4, "kid_hairstyle_black_%s_%s" % (MomName, current_days))
        if KidRace == "M" and r in [3, 5]:
            r = procedural_randint(1, 5, "kid_hairstyle_mixed_1_%s_%s" % (MomName, current_days))
        if KidGender.startswith("M") and r in [1, 5]:
            r = procedural_randint(1, 5, "kid_hairstyle_male_1_%s_%s" % (MomName, current_days))
        if KidRace == "M" and r in [3, 5]:
            r = procedural_randint(1, 5, "kid_hairstyle_mixed_2_%s_%s" % (MomName, current_days))
        if KidGender.startswith("M") and r in [1, 5]:
            r = procedural_randint(1, 5, "kid_hairstyle_male_2_%s_%s" % (MomName, current_days))
        KidHairStyle = "L" if r == 1 else ("K" if r == 2 else ("N" if r == 3 else ("S" if r == 4 else "Z")))

        kids_state = _kids_state()
        kid_id = _kids_int(kids_state["next_id"], 1)
        _kids_list().append({
            "KidId": kid_id,
            "MomName": MomName,
            "DadName": DadName,
            "KidName": KidName,
            "DayBorn": current_days,
            "AssumedDad": AssumedDad,
            "Appearance": KidGender[:1] + KidRace + KidEyes + KidHair + KidHairStyle,
            "DaddySuspects": ZaletSuspectLinesCount(MomName),
            "MyRelation": 0,
        })
        kids_state["next_id"] = kid_id + 1

        mom_info.set_sex_stat("kids", _kids_int(mom_info.sex_stat("kids", 0), 0) + 1)
        ZaletClearSuspectList(MomName)
        mom_info.set_sex_stat("pregnancy", 0)
        mom_info.set_sex_stat("pregfather", "")

        TodaySexEvents_DeleteGirl(MomName)
        if MomName in ["sandra", "melissa", "amanda"]:
            TodaySexEvents_DeleteGirl("sandra")
            TodaySexEvents_DeleteGirl("melissa")
            TodaySexEvents_DeleteGirl("amanda")
        if MomName in ["georgett", "liza"]:
            TodaySexEvents_DeleteGirl("georgett")
            TodaySexEvents_DeleteGirl("liza")
        if MomName in ["becky", "inga"]:
            TodaySexEvents_DeleteGirl("inga")
            TodaySexEvents_DeleteGirl("becky")

        if MomName in ["amanda", "melissa", "sandra"]:
            player.economy.add_child_support(1)
            player.tavern_management.household_members = _kids_int(player.tavern_management.household_members, 0) + 1
            player.economy.child_birth_benefit_notice = "Так как " + people_name(MomName, "nominative", MomName) + " родила без мужа, то именем герцогини Кончитты Дель Семени вашей семье, тоесть вам, было выплаченно единовременно 600 мараведи воспоможения. Также вы будете получать дополнительно по 15 мараведи каждое воскресенье."
        if MomName in ["liza", "georgett"]:
            if str(people.location("georgett") or "") == "TavernMain":
                player.tavern_management.household_members = _kids_int(player.tavern_management.household_members, 0) + 1

        return kid_id

    def GetYoungestKidAge(MomName):
        MomName = str(MomName or "")
        last = 0
        for row in _kids_list():
            if str(row.get("MomName", "")) == MomName:
                last = max(last, _kids_int(row.get("DayBorn", 0), 0))
        res = -1 if last == 0 else (_kids_int(calendar_v2.daysInGame, 0) - last)
        return res

    def GetKidData(KidId):
        KidId = _kids_int(KidId, 0)
        row = _kids_find_row(KidId) or {}
        current_days = _kids_int(calendar_v2.daysInGame, 0)
        kid_desc_code = str(row.get("Appearance", ""))
        return {
            "KidId": KidId,
            "KidDays": current_days - _kids_int(row.get("DayBorn", 0), 0),
            "KidDescCode": kid_desc_code,
            "KidName": str(row.get("KidName", "")),
            "KidMomName": str(row.get("MomName", "")),
            "KidAssumedDad": str(row.get("AssumedDad", "")),
            "KidDaddySuspects": _kids_int(row.get("DaddySuspects", 0), 0),
            "KidGender": kid_desc_code[0:1],
            "KidRace": kid_desc_code[1:2],
            "KidEyes": kid_desc_code[2:3],
            "KidHair": kid_desc_code[3:4],
            "KidHairStyle": kid_desc_code[4:5],
        }

    def ShowKidInteractionMenu(KidId):
        return GetKidData(KidId)["KidName"]

    def ShowKidDesc(KidId):
        kid = GetKidData(KidId)
        KidDays = _kids_int(kid["KidDays"], 0)
        KidGender = str(kid["KidGender"] or "M")
        KidRace = str(kid["KidRace"] or "W")
        KidEyes = str(kid["KidEyes"] or "G")
        KidHair = str(kid["KidHair"] or "B")
        KidHairStyle = str(kid["KidHairStyle"] or "S")

        if KidDays < 180:
            desc = "новорожденн" + ("ый мальчик" if KidGender == "M" else "ая девочка")
        elif KidDays < 400:
            desc = "крохотн" + ("ый мальчик, умеющий пока только ползать," if KidGender == "M" else "ая девочка, умеющая пока только ползать,")
        elif KidDays < 700:
            desc = "малыш" + (", недавно начавший ходить," if KidGender == "M" else "ка, недавно начавшая ходить,")
        else:
            desc = "подвижный и любознательный маленький мальчик" if KidGender == "M" else "шустрая и любопытная маленькая девочка"

        desc += ". " + ("Ему " if KidGender == "M" else "Ей ")
        if KidDays < 30:
            desc += "всего несколько деньков от роду. "
        elif KidDays < 365:
            desc += "идет всего " + str(KidDays // 30) + " месяц. "
        elif KidDays < 730:
            desc += "идет второй годик. "
        else:
            y = KidDays // 365
            desc += "недавно исполнилось " + str(y) + " " + ("года" if y <= 4 else "лет") + ". "

        if KidRace == "N":
            desc += ("Он негритенок" if KidGender == "M" else "Она негритоска") + ", с угольно-черной кожей. "
        elif KidRace == "M":
            desc += ("Он мулат" if KidGender == "M" else "Она мулатка") + ", с молочнокофейной кожей, плод смешения черной и белой рас. "
        elif KidRace == "H":
            desc += ("Его" if KidGender == "M" else "Ее") + " кожа бела, даже слишком бела, а маленькие ушки слегка заостренны, выдавая полуэльфийское происхождение. "
        elif KidRace == "D":
            desc += ("Его" if KidGender == "M" else "Ее") + " кожа имеет цвет кофе с молоком, а ушки слегка заостренны, свидетельствуя об и эльфийской, и черной крови. "
        else:
            desc += ("Он" if KidGender == "M" else "Она") + " обычный ребенок. "

        if KidEyes == "B":
            desc += "Глазенки у " + ("него" if KidGender == "M" else "нее") + " голубые "
        elif KidEyes == "G":
            desc += "У " + ("него" if KidGender == "M" else "нее") + " зеленые глаза "
        elif KidEyes == "D":
            desc += "У " + ("него" if KidGender == "M" else "нее") + " черные глаза "
        else:
            desc += "Глазенки у " + ("него" if KidGender == "M" else "нее") + " серые "
        desc += "a "

        if KidDays < 180:
            desc += "волосья почти полностью отсутствуют."
        else:
            desc += "волосы " + ("темные" if KidHair == "D" else ("платиновые" if KidHair == "P" else ("светлые" if KidHair == "L" else ("рыжие" if KidHair == "R" else "русые"))))
            desc += " и " + ("длиные" if KidHairStyle == "L" else ("кудрявые" if KidHairStyle == "K" else ("кучерявые" if KidHairStyle == "N" else ("короткие" if KidHairStyle == "S" else "в локонах")))) + "."

        return desc

    def ShowFullKidsListByAge(*MomNames):
        dp = _kids_int(calendar_v2.daysInGame, 0)
        age1 = []
        age2 = []
        for mom in MomNames:
            for row in _kids_list():
                if str(row.get("MomName", "")) != str(mom):
                    continue
                kdays = dp - _kids_int(row.get("DayBorn", 0), 0)
                if 180 <= kdays < 400:
                    age1.append(_kids_int(row.get("KidId", 0), 0))
                elif kdays >= 400:
                    age2.append(_kids_int(row.get("KidId", 0), 0))

        lines = []
        if len(age1) == 1:
            lines.append("Вы видите, что здесь ползает и собирает с пола всякую гадость " + ShowKidInteractionMenu(age1[0]) + ".")
        elif len(age1) > 1:
            lines.append("Вы видите, что здесь ползают и собирают с пола всякую гадость " + ", ".join([ShowKidInteractionMenu(x) for x in age1]) + ".")
        if len(age2) == 1:
            lines.append(("Также здесь " if len(age1) > 0 else "Вы видите, что здесь ") + "бегает " + ShowKidInteractionMenu(age2[0]) + ".")
        elif len(age2) > 1:
            lines.append(("Также здесь " if len(age1) > 0 else "Вы видите, что здесь ") + "бегают, играют, и иногда дерутся " + ", ".join([ShowKidInteractionMenu(x) for x in age2]) + ".")
        return "\n".join(lines)

    def DescribeBreastFeeding(MomName, chance=0):
        MomName = str(MomName)
        if _kids_int(chance, 0) == 0:
            chance = 5
        chance = max(1, _kids_int(chance, 5))
        if not _kids_lactating(MomName):
            return ""

        last_kid = 0
        dp = _kids_int(calendar_v2.daysInGame, 0)
        for row in _kids_list():
            if str(row.get("MomName", "")) == MomName and dp - _kids_int(row.get("DayBorn", 0), 0) < 300:
                last_kid = _kids_int(row.get("KidId", 0), 0)
        if last_kid == 0 or procedural_randint(1, chance, "breastfeed_%s_%s" % (MomName, dp)) != 1:
            return ""

        info = people.get_info(MomName)
        KidGender = str(GetKidData(last_kid)["KidGender"] or "M")
        bra = str(info.wardrobe.get("current_underwear", {}).get("bra", "") or "")
        corruption = _kids_int(info.corruption, 0)
        lines = ["Вы заметили что " + people_name(MomName, "nominative", MomName) + " решила дать " + ("своему сыночку" if KidGender == "M" else "своей дочурке") + " сисю."]
        if corruption > 61:
            lines.append("Не смущаясь чужих взоров, она приспустила свое платье " + ("и сняла лифчик" if bra else "под которым ожидаемо ничего не оказалось") + ". Обнажив обе набухшие от молока сиськи, она пристроила ребенка к одной из них. Вторую грудь, с увеличившимся от кормления соском, она прикрыть не удосужилась.")
        elif corruption > 52:
            side = "левой" if procedural_randint(1, 2, "breastfeed_side_%s_%s" % (MomName, dp)) == 1 else "правой"
            lines.append("Не смущаясь тем, что может быть не одна, она приспустила с " + side + " стороны свое платье " + ("а затем приспустила и лифчик" if bra else "под которым ожидаемо ничего не оказалось") + ". Обнажив набухшую от молока грудь, " + people_name(MomName, "nominative", MomName) + " пристроила к ней ребенка.")
        elif corruption > 38:
            lines.append("Смущенно оглянувшись, она отошла в уголочек, стеснительно отвернулась, видимо обнажая грудь, и пристроила к ней ребенка. Лишь после того как он удобно обустроился, она решилась повернуться обратно.")
        else:
            lines.append("Покраснев и смущенно оглянувшись, она отошла в уголочек, стеснительно отвернулась, видимо обнажая грудь, и пристроила к ней ребенка. Достав откуда-то легкую шаль, скромница накрыла и грудь, и ребенка и лишь после этого решилась повернуться обратно.")
        child = ("Маленький " if KidGender == "M" else "Маленькая ") + ShowKidInteractionMenu(last_kid)
        if corruption > 38:
            lines.append(child + " довольно сосет сисю. Иногда " + ("он" if KidGender == "M" else "она") + " выпускает сосок, но заботливая " + people_name(MomName, "nominative", MomName) + " немедленно помогает " + ("ему" if KidGender == "M" else "ей") + ".")
        else:
            lines.append(child + " довольно сосет сисю под шалью. Иногда из-под нее раздается возмущенный писк, но заботливая " + people_name(MomName, "nominative", MomName) + " приходит на помощь, что-то поправляя у себя под накидкой.")
        return "\n".join(lines)

    def LactateTitsDesc(GirlName):
        GirlName = str(GirlName)
        info = people.get_info(GirlName)
        if info.tits_visible() and _kids_lactating(GirlName) and procedural_randint(1, 2, "lactate_desc_%s_%s" % (GirlName, _kids_int(calendar_v2.daysInGame, 0))) == 1:
            return "Из разбухшего соска с большой ареолой вытекла капелька молока."
        return ""

    def LactateTitsFondle(GirlName, PartnerName=""):
        GirlName = str(GirlName)
        info = people.get_info(GirlName)
        if not _kids_lactating(GirlName) or info.arousal_value() <= 35:
            return ""
        if not info.tits_visible():
            if str(info.wardrobe.get("current_underwear", {}).get("bra", "") or "") == "":
                return "От жамкания из доек вскоре потекло молоко, ее блузка быстро намокла и сосочки стали просвечивать через нее."
            return ""
        info.set_arousal(min(65, info.arousal_value() + 8))
        if str(PartnerName or ""):
            return "Вы заметили, что партнер уже не просто ласкает ее груди и соски, а смокчет сосок, подкармливаясь молочком."
        return "Вдруг вы почувствовали, как вам в рот ударила струйка молока. Немного удивившись, вы продолжили ласкать сосок и сжимать груди, высасывая молочко из ее доек."

    def LactateTitsFuck(GirlName, PartnerName=""):
        GirlName = str(GirlName)
        info = people.get_info(GirlName)
        if not _kids_lactating(GirlName) or info.arousal_value() <= 45:
            return ""
        info.set_arousal(min(65, info.arousal_value() + 6))
        if str(PartnerName or ""):
            return "При почти каждом движении члена из ее сосков струйками брызгает молоко, заливая груди и служа дополнительной смазкой."
        player.intimacy.add_arousal(5, 100)
        return "При почти каждом движении вашего члена из ее сосков струйками брызгает молоко. Большая его часть заливает ее титьки и ваш член, служа дополнительной смазкой, а отдельные струйки вам удается поймать ртом."

    def LactatePussyFuck(GirlName, PartnerName=""):
        GirlName = str(GirlName)
        info = people.get_info(GirlName)
        if not _kids_lactating(GirlName) or info.arousal_value() <= 60 or procedural_randint(1, 3, "lactate_pussy_%s_%s" % (GirlName, _kids_int(calendar_v2.daysInGame, 0))) != 1:
            return ""
        if procedural_randint(1, 2, "lactate_pussy_text_%s_%s" % (GirlName, _kids_int(calendar_v2.daysInGame, 0))) == 1:
            return "Вы заметили, что из ее сосков в такт вашим толчкам стало побрызгивать молоко."
        return "Вы заметили, что ее возбужденные соски набухли еще больше и из них начало сочиться молочко."

    def KidsPeekSexCode(MomName):
        MomName = str(MomName)
        dp = _kids_int(calendar_v2.daysInGame, 0)
        info = people.get_info(MomName)
        corruption = _kids_int(info.corruption, 0)
        base_chance = 4 if corruption > 70 else (8 if corruption > 55 else (11 if corruption > 40 else (12 if corruption > 30 else (14 if corruption > 20 else 16))))
        for row in _kids_list():
            if str(row.get("MomName", "")) != MomName:
                continue
            age_days = dp - _kids_int(row.get("DayBorn", 0), 0)
            if age_days <= 365 * 2:
                continue
            age_years = age_days // 365
            peek_chance = 7 * base_chance * (1 if age_years >= 4 else 2)
            if procedural_randint(1, peek_chance, "kids_peek_%s_%s_%s" % (MomName, _kids_int(row.get("KidId", 0), 0), dp)) == 1:
                kid_id = _kids_int(row.get("KidId", 0), 0)
                kid_name = ShowKidInteractionMenu(kid_id)
                g = str(row.get("Appearance", "M"))[0:1]
                text = "Вдруг вы заметили, что из-за приоткрытой двери за вами удивленно следит " + kid_name + ", " + ("сыночек" if g == "M" else "дочка") + " " + people_name(MomName, "genitive", MomName) + ". "
                reaction_max = 3 if age_years >= 4 else (4 if age_years >= 3 else 4)
                reaction_min = 1 if age_years >= 3 else 4
                reaction = procedural_randint(reaction_min, reaction_max, "kids_peek_reaction_%s_%s_%s" % (MomName, kid_id, dp))
                if reaction == 1:
                    text += "Наблюдая за кувырканием мамочки, " + ("он усмехнулся и сделал" if g == "M" else "она рассмеялась и сделала") + " пошлый жест. "
                elif reaction == 2:
                    text += "На " + ("его лице" if g == "M" else "ее личике") + " застыло мечтательное выражение. "
                elif reaction == 3:
                    text += "От увиденного " + ("его" if g == "M" else "ее") + " глазенки расширились, а щеки стали пунцовыми. "
                else:
                    text += ("Он явно удивлен" if g == "M" else "Она явно удивлена") + " происходящим. "
                if g == "M":
                    text += "Неожиданно малой встретился с вами взглядом. Поняв, что его заметили, он сорвался и убежал."
                else:
                    text += "Неожиданно малая встретилась с вами взглядом. Поняв, что ее заметили, она покраснела, сорвалась и убежала."
                row["MyRelation"] = _kids_int(row.get("MyRelation", 0), 0) + 1
                return text
        return ""

