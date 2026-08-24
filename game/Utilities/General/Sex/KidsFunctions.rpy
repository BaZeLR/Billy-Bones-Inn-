        if key == "dayspassed":
            return dayspassed            _kids_set("EventsCount", {})
            _kids_set("NewEvents", {})        if key == "RealName":
            return dict((girl, people_display_name(girl)) for girl in list(AllGirlNames or []))
        if key == "RealName2":
            names = {}
            for girl in list(AllGirlNames or []):
                info = getPersonInfo(girl)
                data = getattr(info, "data", None) if info is not None else None
                names[girl] = str(getattr(data, "genitive", "") or people_display_name(girl))
            return names        if key == "dayspassed":
            return dayspassed            _kids_set("EventsCount", {})
            _kids_set("NewEvents", {})        if key == "RealName":
            return dict((girl, people_display_name(girl)) for girl in list(AllGirlNames or []))
        if key == "RealName2":
            names = {}
            for girl in list(AllGirlNames or []):
                info = getPersonInfo(girl)
                data = getattr(info, "data", None) if info is not None else None
                names[girl] = str(getattr(data, "genitive", "") or people_display_name(girl))
            return names        if key == "dayspassed":
            return dayspassed            _kids_set("EventsCount", {})
            _kids_set("NewEvents", {})        if key == "RealName":
            return dict((girl, people_display_name(girl)) for girl in list(AllGirlNames or []))
        if key == "RealName2":
            names = {}
            for girl in list(AllGirlNames or []):
                info = getPersonInfo(girl)
                data = getattr(info, "data", None) if info is not None else None
                names[girl] = str(getattr(data, "genitive", "") or people_display_name(girl))
            return names# ================================================================================
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
        state.setdefault("scratch", {})
        return state

    def _kids_get(name, default=None):
        key = str(name or "")
        state = _kids_state()
        if key == "KidsList":
            return state["list"]
        if key == "KidsListNextId":
            return state["next_id"]
        if key == "pregnancy":
            result = {}
            for girl in list(AllGirlNames or []):
                info = getPersonInfo(girl)
                if info is not None:
                    result[girl] = info.pregnancy_days()
            return result
        return state["scratch"].get(key, default)

    def _kids_set(name, value):
        key = str(name or "")
        state = _kids_state()
        if key == "KidsList":
            state["list"] = value if isinstance(value, list) else []
        elif key == "KidsListNextId":
            state["next_id"] = _kids_int(value, 1)
        else:
            state["scratch"][key] = value
        return value

    def _kids_int(v, d=0):
        try:
            return int(v)
        except Exception:
            try:
                return int(float(v))
            except Exception:
                return d

    def _k_int(v, d=0):
        return _kids_int(v, d)

    def _kids_person_stat(person_name, stat_key, default=0):
        info = getPersonInfo(person_name)
        if info is None or not hasattr(info, "sex_stat"):
            return default
        return info.sex_stat(stat_key, default)

    def _kids_lactating(person_name):
        lactate_value = _kids_person_stat(person_name, "lactate", None)
        if lactate_value is None:
            lactate_value = _kids_person_stat(person_name, "breastfeed", 0)
        return _k_int(lactate_value, 0) != 0

    def _kids_list():
        kids_list = _kids_get("KidsList", None)
        if kids_list is None:
            kids_list = []
            _kids_set("KidsList", kids_list)
        return kids_list

    def _kids_row_ids():
        return [row.get("KidId", 0) for row in _kids_list()]

    def _kids_find_row(kid_id):
        kid_id = _kids_int(kid_id, 0)
        for row in _kids_list():
            if _kids_int(row.get("KidId", 0), 0) == kid_id:
                return row
        return None

    def _k_rows(table_name):
        if table_name == "KidsList":
            return _kids_row_ids()
        return []

    def _k_cols(table_name):
        if table_name == "KidsList":
            return ["KidId", "MomName", "DadName", "KidName", "DayBorn", "AssumedDad", "Appearance", "DaddySuspects", "MyRelation"]
        return []

    def _k_col(table_name, wanted):
        for c in _k_cols(table_name):
            if str(c).lower() == str(wanted).lower():
                return c
        return wanted

    def _k_get(table_name, row_id, col, default=""):
        if table_name != "KidsList":
            return default
        row = _kids_find_row(row_id)
        if row is None:
            return default
        return row.get(_k_col(table_name, col), default)

    def _k_set(table_name, row_id, col, value):
        if table_name != "KidsList":
            return
        row = _kids_find_row(row_id)
        if row is None:
            return
        row[_k_col(table_name, col)] = value

    def _k_add_row(table_name, row):
        if table_name != "KidsList":
            return 0

        next_id = _kids_int(_kids_get("KidsListNextId", 1), 1)
        row_copy = dict(row)
        row_copy["KidId"] = next_id
        _kids_list().append(row_copy)
        _kids_set("KidsListNextId", next_id + 1)
        return next_id

    def _kids_result(value):
        _kids_set("Result", value)
        return value

    def CreateKid(MomName):
        MomName = str(MomName or "")
        current_days = _kids_int(_kids_get("dayspassed", 0), 0)
        Pregnancy = _kids_get("pregnancy", {})

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
        try:
            if MomName in ["liza", "georgett"]:
                KidName = RandomNameCode(KidGender, "French")
            elif MomName in ["becky", "inga"]:
                KidName = RandomNameCode(KidGender, "German")
            else:
                KidName = RandomNameCode(KidGender)
        except Exception:
            KidName = "Ребенок"

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

        kid_id = _k_add_row("KidsList", {
            "MomName": MomName,
            "DadName": DadName,
            "KidName": KidName,
            "DayBorn": current_days,
            "AssumedDad": AssumedDad,
            "Appearance": KidGender[:1] + KidRace + KidEyes + KidHair + KidHairStyle,
            "DaddySuspects": _kids_int(_kids_get("PregTotalSuspects", {}).get(MomName, 0), 0),
            "MyRelation": 0,
        })

        kids = _kids_get("kids", {})
        kids[MomName] = _kids_int(kids.get(MomName, 0), 0) + 1
        ZaletClearSuspectList(MomName)
        Pregnancy[MomName] = 0
        _kids_get("pregfather", {})[MomName] = ""

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
            player.economy.sync_from_store()
            player.economy.sync_from_store()
            player.economy.sync_from_store()
            player.economy.add_child_support(1)
            player.economy.apply_to_store()
            player.economy.apply_to_store()
            player.economy.apply_to_store()
            _kids_set("player.tavern_management.household_members", _kids_int(_kids_get("player.tavern_management.household_members", 0), 0) + 1)
            _kids_set("KidBirthPosobie", "Так как " + str(_kids_get("RealName", {}).get(MomName, MomName)) + " родила без мужа, то именем герцогини Кончитты Дель Семени вашей семье, тоесть вам, было выплаченно единовременно 600 мараведи воспоможения. Также вы будете получать дополнительно по 15 мараведи каждое воскресенье.")
        if MomName in ["liza", "georgett"]:
            current_loc = _kids_get("CurrentLoc", {})
            if str(current_loc.get("georgett", "")) == "TavernMain":
                _kids_set("player.tavern_management.household_members", _kids_int(_kids_get("player.tavern_management.household_members", 0), 0) + 1)
            _kids_set("ProstitutesKids", _kids_int(_kids_get("ProstitutesKids", 0), 0) + 1)

        return _kids_result(kid_id)

    def GetYoungestKidAge(MomName):
        MomName = str(MomName or "")
        last = 0
        for row in _kids_list():
            if str(row.get("MomName", "")) == MomName:
                last = max(last, _kids_int(row.get("DayBorn", 0), 0))
        res = -1 if last == 0 else (_kids_int(_kids_get("dayspassed", 0), 0) - last)
        return _kids_result(res)

    def GetKidData(KidId):
        KidId = _kids_int(KidId, 0)
        row = _kids_find_row(KidId) or {}
        current_days = _kids_int(_kids_get("dayspassed", 0), 0)
        kid_desc_code = str(row.get("Appearance", ""))

        _kids_set("KidDays", current_days - _kids_int(row.get("DayBorn", 0), 0))
        _kids_set("KidDescCode", kid_desc_code)
        _kids_set("KidName", str(row.get("KidName", "")))
        _kids_set("KidMomName", str(row.get("MomName", "")))
        _kids_set("KidAssumedDad", str(row.get("AssumedDad", "")))
        _kids_set("KidDaddySuspects", _kids_int(row.get("DaddySuspects", 0), 0))
        _kids_set("KidGender", kid_desc_code[0:1])
        _kids_set("KidRace", kid_desc_code[1:2])
        _kids_set("KidEyes", kid_desc_code[2:3])
        _kids_set("KidHair", kid_desc_code[3:4])
        _kids_set("KidHairStyle", kid_desc_code[4:5])
        return _kids_result(0)

    def ShowKidInteractionMenu(KidId):
        GetKidData(KidId)
        return _kids_result(_kids_get("KidName", ""))

    def ShowKidDesc(KidId):
        GetKidData(KidId)
        KidDays = _kids_int(_kids_get("KidDays", 0), 0)
        KidGender = str(_kids_get("KidGender", "M"))
        KidRace = str(_kids_get("KidRace", "W"))
        KidEyes = str(_kids_get("KidEyes", "G"))
        KidHair = str(_kids_get("KidHair", "B"))
        KidHairStyle = str(_kids_get("KidHairStyle", "S"))

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

        return _kids_result(desc)

    def ShowFullKidsListByAge(*MomNames):
        dp = _kids_int(_kids_get("dayspassed", 0), 0)
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

        if len(age1) == 1:
            renpy.say(None, "Вы видите, что здесь ползает и собирает с пола всякую гадость " + ShowKidInteractionMenu(age1[0]) + ".")
        elif len(age1) > 1:
            renpy.say(None, "Вы видите, что здесь ползают и собирают с пола всякую гадость " + ", ".join([ShowKidInteractionMenu(x) for x in age1]) + ".")
        if len(age2) == 1:
            renpy.say(None, ("Также здесь " if len(age1) > 0 else "Вы видите, что здесь ") + "бегает " + ShowKidInteractionMenu(age2[0]) + ".")
        elif len(age2) > 1:
            renpy.say(None, ("Также здесь " if len(age1) > 0 else "Вы видите, что здесь ") + "бегают, играют, и иногда дерутся " + ", ".join([ShowKidInteractionMenu(x) for x in age2]) + ".")
        return 0

    def DescribeBreastFeeding(MomName, chance=0):
        MomName = str(MomName)
        if _k_int(chance, 0) == 0:
            chance = 5
        chance = max(1, _k_int(chance, 5))
        if not _kids_lactating(MomName):
            return 0

        last_kid = 0
        dp = _k_int(_kids_get("dayspassed", 0), 0)
        for row in _kids_list():
            if str(row.get("MomName", "")) == MomName and dp - _k_int(row.get("DayBorn", 0), 0) < 300:
                last_kid = _kids_int(row.get("KidId", 0), 0)
        if last_kid == 0 or procedural_randint(1, chance, "breastfeed_%s_%s" % (MomName, dp)) != 1:
            return 0

        GetKidData(last_kid)
        KidGender = str(_kids_get("KidGender", "M"))
        renpy.say(None, "Вы заметили что " + str(_kids_get("RealName", {}).get(MomName, MomName)) + " решила дать " + ("своему сыночку" if KidGender == "M" else "своей дочурке") + " сисю.")
        renpy.say(None, ("Маленький " if KidGender == "M" else "Маленькая ") + ShowKidInteractionMenu(last_kid) + " довольно сосет сисю.")
        return 0

    def LactateTitsDesc(GirlName):
        GirlName = str(GirlName)
        info = getPersonInfo(GirlName)
        state = info.ensure_sex_state() if info is not None else {}
        underwear = getattr(info, "wardrobe", {}).get("current_underwear", {}) if info is not None else {}
        top_visible = _k_int(state.get("top_raised", 0), 0) == 1 or _k_int(state.get("top_removed", 0), 0) == 1
        if top_visible and str(underwear.get("bra", "") or "") == "":
            if _kids_lactating(GirlName) and procedural_randint(1, 2, "lactate_desc_%s_%s" % (GirlName, _k_int(_kids_get("dayspassed", 0), 0))) == 1:
                renpy.say(None, "Из разбухшего соска с большой ареолой вытекла капелька молока.")
        return 0

    def LactateTitsFondle(GirlName, PartnerName=""):
        GirlName = str(GirlName)
        info = getPersonInfo(GirlName)
        if info is not None and _kids_lactating(GirlName) and info.arousal_value() > 35:
            info.set_arousal(min(65, info.arousal_value() + 8))
        return 0

    def LactateTitsFuck(GirlName, PartnerName=""):
        GirlName = str(GirlName)
        info = getPersonInfo(GirlName)
        if info is not None and _kids_lactating(GirlName) and info.arousal_value() > 45:
            info.set_arousal(min(65, info.arousal_value() + 6))
            if str(PartnerName) == "":
                player.intimacy.add_arousal(5, 100, "You")
        return 0

    def LactatePussyFuck(GirlName, PartnerName=""):
        GirlName = str(GirlName)
        info = getPersonInfo(GirlName)
        if info is not None and _kids_lactating(GirlName) and info.arousal_value() > 60 and procedural_randint(1, 3, "lactate_pussy_%s_%s" % (GirlName, _k_int(_kids_get("dayspassed", 0), 0))) == 1:
            renpy.say(None, "Вы заметили, что из сосков стало побрызгивать молоко.")
        return 0

    def KidsPeekSexCode(MomName):
        MomName = str(MomName)
        dp = _k_int(_kids_get("dayspassed", 0), 0)
        for row in _kids_list():
            if str(row.get("MomName", "")) != MomName:
                continue
            if dp - _k_int(row.get("DayBorn", 0), 0) <= 365 * 2:
                continue
            if procedural_randint(1, 100, "kids_peek_%s_%s_%s" % (MomName, _kids_int(row.get("KidId", 0), 0), dp)) == 1:
                kid_id = _kids_int(row.get("KidId", 0), 0)
                name = ShowKidInteractionMenu(kid_id)
                kid_name = str(row.get("KidName", name))
                g = str(row.get("Appearance", "M"))[0:1]
                renpy.say(None, "Вдруг вы заметили что из-за приоткрытой двери за вами удивленно следит " + name + ", " + kid_name + ", " + ("сыночек" if g == "M" else "дочка") + " " + str(_kids_get("RealName2", {}).get(MomName, MomName)) + ".")
                row["MyRelation"] = _k_int(row.get("MyRelation", 0), 0) + 1
                break
        return 0

label KidsFunctions:
    $ _kids_functions_initialized = True
    return

label CreateKid(MomName="", CurLocArg=""):
    $ Result = CreateKid(MomName)
    return Result
