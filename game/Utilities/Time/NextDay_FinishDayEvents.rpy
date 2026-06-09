# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _ndf_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def next_day_finish_day_events():
        global ChurchDonatedToday
        global FridayDancesCount
        global CursedByEllonaDays
        global StolenHorseDays
        global TownStreetEventsToday
        global TownStreetPatrolsToday
        global TownStreetFightToday
        global TownCurfewCaughtToday
        global TownStreetStorySeenKeys
        global TownStreetDailyPlan
        global TownStreetLastEventText
        global TownStreetContext
        global TownStreetFiredLabelsToday
        global TownStreetFiredLocationsToday
        global TownStreetCooldowns

        if "TalkChurchAfterCermonLiza" not in GeorgettVar:
            GeorgettVar["TalkChurchAfterCermonLiza"] = 0
        if "ProstStart" not in LizaVar:
            LizaVar["ProstStart"] = 0
        if "PriestAdvice" not in BeckyVar:
            BeckyVar["PriestAdvice"] = 0
        if "visitedhome" not in BeckyVar:
            BeckyVar["visitedhome"] = 0
        if "EddieTryToFuck" not in BeckyVar:
            BeckyVar["EddieTryToFuck"] = 0
        if "alberfriends" not in AmandaVar:
            AmandaVar["alberfriends"] = 0
        if "lizafriends" not in AmandaVar:
            AmandaVar["lizafriends"] = 0
        if "eddie" not in cametoday_npc:
            cametoday_npc["eddie"] = 0

        week_val = _ndf_int(week, 1)
        dayspassed_val = _ndf_int(dayspassed, 0)
        church_donated_amount = _ndf_int(ChurchDonatedAmount, 0)
        glory_hole_look = _ndf_int(GloryHoleLook, 0)

        if GeorgettVar.get("TalkChurchAfterCermonLiza", 0) and LizaVar.get("ProstStart", 0) == 0:
            LizaVar["ProstStart"] = 1

        if ChurchAfterCermon.get("becky", 0) < 4 and week_val == 7 and BeckyVar.get("PriestAdvice", 0) > 0:
            if BeckyVar.get("PriestAdvice", 0) in (1, 2):
                BeckyVar["PriestAdvice"] = 2
                if renpy.random.randint(1, 70) * 30 <= church_donated_amount:
                    BeckyVar["PriestAdvice"] = 3
            if BeckyVar.get("PriestAdvice", 0) == 3:
                if BeckyVar.get("visitedhome", 0) < 7 and BeckyVar.get("EddieTryToFuck", 0) >= 4:
                    BeckyVar["visitedhome"] = 7

        while TodaySexEvents:
            tmpArray = TodaySexEvents_PopFirst()
            girl = str(tmpArray.get("GirlName", "") or "")
            place = str(tmpArray.get("Place", "") or "")
            event_type = _ndf_int(tmpArray.get("EventType", 0), 0)

            if girl == "georgett" and event_type == 99 and place == "Prostitution":
                PregnancyCheck(girl, "inside", 1, "eddie")
            elif girl == "georgett" and place == "EddieHomeVisit":
                PregnancyCheck(girl, "mouth", 1, "eddie")
            elif girl == "liza" and event_type == 99:
                PregnancyCheck(girl, "mouth", 1, "legare")
            elif girl == "inga" and place == "Lucas":
                inside_or_mouth = "inside" if renpy.random.randint(1, 3) <= 2 else "mouth"
                PregnancyCheck(girl, inside_or_mouth, 1, "Лукас")
            elif place == "Glory":
                glory_hole_inside = "mouth"
                sluttiness_val = _ndf_int(sluttiness.get(girl, 0), 0)
                if sluttiness_val >= 80:
                    if renpy.random.randint(1, 15) == 1:
                        glory_hole_inside = "inside"
                elif sluttiness_val >= 60:
                    if renpy.random.randint(1, 30) == 1:
                        glory_hole_inside = "inside"
                elif sluttiness_val >= 50:
                    if renpy.random.randint(1, 60) == 1:
                        glory_hole_inside = "inside"
                if event_type == 1:
                    PregnancyCheck(girl, glory_hole_inside, 1, "Мастер Драупнир")
                elif event_type == 2:
                    PregnancyCheck(girl, glory_hole_inside, 1, "Эдди")
                elif glory_hole_look == 3:
                    PregnancyCheck(girl, glory_hole_inside, 1, "Мессир Легаре")
                elif event_type == 4:
                    PregnancyCheck(girl, glory_hole_inside, 1, "Отец Герхард")
                else:
                    PregnancyCheck(girl, glory_hole_inside, 1, "", 1, "")
            elif girl == "amanda" and place == "glorytry":
                AmandaVar["glorytried"] = 1
                PregnancyCheck(girl, "mouth", 1, "", 1, "")
            elif girl == "amanda" and place == "legarerun":
                apply_legare_amanda_let_go_code()
            elif girl == "amanda" and place == "lovermeet":
                AmandaLoverSexCalc()
            elif place == "Priest":
                PregnancyCheck(girl, "inside", 1, "Отец Герхард")
                if girl == "becky" and renpy.random.randint(1, 2) == 1:
                    DayLastOrgasmGiven["becky"] = dayspassed_val
            elif girl == "becky":
                if place == "StoreLover":
                    if event_type == 1:
                        PregnancyCheck("becky", "inside", 1, "Легаре")
                    if event_type == 2:
                        PregnancyCheck("becky", "inside", 1, "", 1, "Неизвестный грузчик")
                    DayLastOrgasmGiven["becky"] = dayspassed_val
                elif place == "EddieMom":
                    if _ndf_int(cametoday_npc.get("eddie", 0), 0) == 0:
                        inside_or_mouth = "inside" if renpy.random.randint(1, 2) == 1 else "mouth"
                        PregnancyCheck(girl, inside_or_mouth, 1, "eddie")
                        if renpy.random.randint(1, 5) == 1:
                            DayLastOrgasmGiven["becky"] = dayspassed_val
            else:
                PregnancyCheck(girl, "", 1, "")

        while GirlDance:
            tmpArray = GirlDance_PopFirst()
            event_amanda_legare_create_dance()
            if _ndf_int(tmpArray.get("GoOut", 0), 0) == 1:
                apply_legare_amanda_let_go_code()

        if AmandaVar.get("gloryscold", 0) or AmandaVar.get("glorywalkout", 0) or AmandaVar.get("glorysuck", 0) or AmandaVar.get("glorydeflower", 0):
            AmandaVar["gloryyouknow"] = 1
        if AmandaVar.get("glorysuck", 0):
            AmandaVar["suckyou"] = 1
        if AmandaVar.get("glorydeflower", 0):
            AmandaVar["fuckyou"] = 1
        if AmandaVar.get("glorydeflower", 0) or AmandaVar.get("fuckyou", 0) or AmandaVar.get("sawlegaresex", 0) or AmandaVar.get("sawwithguys", 0) or AmandaVar.get("knowlegaresex", 0) or AmandaVar.get("knownotvirgin", 0):
            AmandaVar["knowsexactive"] = 1
        AmandaVar["knowyouseesex"] = 0
        AmandaVar["kickyoufromroom"] = 0
        AmandaVar["askzalettoday"] = 0
        AmandaVar["leftdances"] = 0
        BeckyVar["leftdances"] = 0
        AmandaVar["alberfriends"] = max(0, min(_ndf_int(AmandaVar.get("alberfriends", 0), 0), 20))
        AmandaVar["lizafriends"] = max(0, min(_ndf_int(AmandaVar.get("lizafriends", 0), 0), 20))

        ChurchDonatedToday = 0
        FridayDancesCount = 0
        if "town_street" in globals():
            town_street.settle_blackworker_candidates()
        TownStreetEventsToday = 0
        TownStreetPatrolsToday = 0
        TownStreetFightToday = 0
        TownCurfewCaughtToday = 0
        TownStreetStorySeenKeys = []
        TownStreetDailyPlan = {}
        TownStreetLastEventText = ""
        TownStreetContext = {}
        TownStreetFiredLabelsToday = []
        TownStreetFiredLocationsToday = []
        TownStreetCooldowns = {}

        DailyEventsList_EndDayUpdate(week_val)

label NextDay_FinishDayEvents:
    python:
        next_day_finish_day_events()
        _ndf_all_girl_names = list(AllGirlNames)
        _ndf_all_girl_index = 0

    while _ndf_all_girl_index < len(_ndf_all_girl_names):
        call DailySetstatdefault(_ndf_all_girl_names[_ndf_all_girl_index])
        $ _ndf_all_girl_index += 1

    $ Talked["Zimmer"] = 0
    $ people_reset_daily_interactions()

    python:
        if isinstance(Friends, dict):
            for k in list(Friends.keys()):
                try:
                    Friends[k] = max(0, min(20, int(Friends.get(k, 0) or 0)))
                except Exception:
                    Friends[k] = 0
        elif isinstance(Friends, list):
            for i in range(len(Friends)):
                try:
                    Friends[i] = max(0, min(20, int(Friends[i] or 0)))
                except Exception:
                    Friends[i] = 0

        if CursedByEllona > 0:
            CursedByEllonaDays -= 1

        if StolenHorseDays > 0:
            StolenHorseDays -= 1

        cametoday_npc.clear()
        if isinstance(SexTimesToday, dict):
            SexTimesToday.clear()
        if isinstance(MelissaVar, dict):
            MelissaVar["private_context_day"] = -1
            MelissaVar["private_context_origin"] = ""
            MelissaVar["private_context_place"] = ""
            MelissaVar["private_place_heat"] = 0
        Talked.clear()
        ChurchAfterCermon.clear()
        people_sync_all()
    return
