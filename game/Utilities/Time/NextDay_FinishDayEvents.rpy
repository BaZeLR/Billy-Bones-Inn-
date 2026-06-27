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

        Georgett.ensure_story_defaults()
        Liza.ensure_story_defaults()
        Becky.ensure_story_defaults()
        Amanda.ensure_story_defaults()
        week_val = _ndf_int(week, 1)
        dayspassed_val = _ndf_int(dayspassed, 0)
        church_donated_amount = _ndf_int(ChurchDonatedAmount, 0)
        glory_hole_look = _ndf_int(GloryHoleLook, 0)

        if Georgett.story_value("TalkChurchAfterCermonLiza", 0) and Liza.story_value("ProstStart", 0) == 0:
            Liza.set_story_value("ProstStart", 1)

        if Becky.after_sermon_stage() < 4 and week_val == 7 and Becky.var.get("PriestAdvice", 0) > 0:
            if Becky.var.get("PriestAdvice", 0) in (1, 2):
                Becky.var["PriestAdvice"] = 2
                if procedural_randint(1, 70, "becky_priest_advice_finish_%s" % dayspassed_val) * 30 <= church_donated_amount:
                    Becky.var["PriestAdvice"] = 3
            if Becky.var.get("PriestAdvice", 0) == 3:
                if Becky.var.get("visitedhome", 0) < 7 and Becky.var.get("EddieTryToFuck", 0) >= 4:
                    Becky.var["visitedhome"] = 7

        while SexEvents.today_events:
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
                inside_or_mouth = "inside" if procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:65:1") <= 2 else "mouth"
                PregnancyCheck(girl, inside_or_mouth, 1, "Лукас")
            elif place == "Glory":
                glory_hole_inside = "mouth"
                girl_info = getPersonInfo(girl)
                corruption_val = _ndf_int(getattr(girl_info, "corruption", 0), 0) if girl_info is not None else 0
                if corruption_val >= 80:
                    if procedural_randint(1, 15, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:72:2") == 1:
                        glory_hole_inside = "inside"
                elif corruption_val >= 60:
                    if procedural_randint(1, 30, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:75:3") == 1:
                        glory_hole_inside = "inside"
                elif corruption_val >= 50:
                    if procedural_randint(1, 60, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:78:4") == 1:
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
                Amanda.set_var_int("glorytried", 1)
                PregnancyCheck(girl, "mouth", 1, "", 1, "")
            elif girl == "amanda" and place == "legarerun":
                apply_legare_amanda_let_go_code()
            elif girl == "amanda" and place == "lovermeet":
                Amanda.lover_sex_calc()
            elif place == "Priest":
                PregnancyCheck(girl, "inside", 1, "Отец Герхард")
                if girl == "becky" and procedural_randint(1, 2, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:99:5") == 1:
                    Becky.set_story_value("last_store_orgasm_day", dayspassed_val)
            elif girl == "becky":
                if place == "StoreLover":
                    if event_type == 1:
                        PregnancyCheck("becky", "inside", 1, "Легаре")
                    if event_type == 2:
                        PregnancyCheck("becky", "inside", 1, "", 1, "Неизвестный грузчик")
                    Becky.set_story_value("last_store_orgasm_day", dayspassed_val)
                elif place == "EddieMom":
                    eddie = getPersonInfo("eddie")
                    eddie_came_today = _ndf_int(eddie.ensure_sex_state().get("came_today", 0), 0) if eddie is not None else 0
                    if eddie_came_today == 0:
                        inside_or_mouth = "inside" if procedural_randint(1, 2, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:112:6") == 1 else "mouth"
                        PregnancyCheck(girl, inside_or_mouth, 1, "eddie")
                        if procedural_randint(1, 5, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:114:7") == 1:
                            Becky.set_story_value("last_store_orgasm_day", dayspassed_val)
            else:
                PregnancyCheck(girl, "", 1, "")

        while SexEvents.girl_dance:
            tmpArray = GirlDance_PopFirst()
            event_amanda_legare_create_dance()
            if _ndf_int(tmpArray.get("GoOut", 0), 0) == 1:
                apply_legare_amanda_let_go_code()

        if Amanda.var_int("gloryscold", 0) or Amanda.var_int("glorywalkout", 0) or Amanda.var_int("glorysuck", 0) or Amanda.var_int("glorydeflower", 0):
            Amanda.set_var_int("gloryyouknow", 1)
        if Amanda.var_int("glorysuck", 0):
            Amanda.set_var_int("suckyou", 1)
        if Amanda.var_int("glorydeflower", 0):
            Amanda.set_var_int("fuckyou", 1)
        if Amanda.var_int("glorydeflower", 0) or Amanda.var_int("fuckyou", 0) or Amanda.var_int("sawlegaresex", 0) or Amanda.var_int("sawwithguys", 0) or Amanda.var_int("knowlegaresex", 0) or Amanda.var_int("knownotvirgin", 0):
            Amanda.set_var_int("knowsexactive", 1)
        Amanda.set_var_int("knowyouseesex", 0)
        Amanda.set_var_int("kickyoufromroom", 0)
        Amanda.set_var_int("askzalettoday", 0)
        Amanda.set_var_int("leftdances", 0)
        Becky.set_story_value("leftdances", 0)
        Amanda.set_var_int("alberfriends", max(0, min(Amanda.var_int("alberfriends", 0), 20)))
        Amanda.set_var_int("lizafriends", max(0, min(Amanda.var_int("lizafriends", 0), 20)))

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

    $ Talked["zimmer"] = 0
    $ people_reset_daily_interactions()

    python:
        if CursedByEllona > 0:
            CursedByEllonaDays -= 1

        if StolenHorseDays > 0:
            StolenHorseDays -= 1

        Talked.clear()
        ChurchAfterCermon.clear()
        people_sync_all()
    return
