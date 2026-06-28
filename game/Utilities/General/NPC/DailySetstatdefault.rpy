# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label DailySetstatdefault(girl_name):
    $ _dssd_info = getPersonInfo(girl_name)
    if _dssd_info is not None and hasattr(_dssd_info, "set_arousal"):
        $ _dssd_info.set_arousal(PussyWetStart.get(girl_name, 0))
    $ CumInsideYou[girl_name] = 0
    $ CumInsideOthers[girl_name] = 0
    $ CumFaceYou[girl_name] = 0
    $ CumTitsYou[girl_name] = 0
    $ CumFaceOthers[girl_name] = 0
    $ CumTitsOthers[girl_name] = 0
    $ Breastfeed[girl_name] = 0
    $ Lactate[girl_name] = 0

    if not (girl_name == "inga" and IngaVar.get("Knowher", 0) == 0):
        if pregnancy.get(girl_name, 0) > 0:
            $ pregnancy[girl_name] = pregnancy.get(girl_name, 0) + 1

    $ _dssd_suspects_count = ZaletSuspectLinesCount(girl_name)
    if _dssd_suspects_count == 0 and pregnancy.get(girl_name, 0) >= 50:
        $ ZaletGetSuspectList(girl_name)

    if CheckDailyEventExists(girl_name, "MorningSickness") == 0:
        if ((pregnancy.get(girl_name, 0) > 0 and pregnancy.get(girl_name, 0) < 80 and procedural_randint(1, 7, "morning_sickness_%s_%s" % (girl_name, int(dayspassed or 0))) == 1)
                or (pregnancy.get(girl_name, 0) == 0 and procedural_randint(1, 60, "false_morning_sickness_%s_%s" % (girl_name, int(dayspassed or 0))) == 32)):
            $ DailyEventsList_Add(girl_name, "TavernKitchen", 1, "<", 1, 8, "MorningSickness", "MorningSickness")

    if CheckDailyEventExists(girl_name, "GiveBirth") == 0:
        if ((pregnancy.get(girl_name, 0) > 240 and procedural_randint(1, 45, "birth_window_%s_%s" % (girl_name, int(dayspassed or 0))) > max(270 - pregnancy.get(girl_name, 0), 0) + 10 and procedural_randint(1, 3, "birth_confirm_%s_%s" % (girl_name, int(dayspassed or 0))) == 1)
                or pregnancy.get(girl_name, 0) >= 285):
            $ _dssd_know_about_birth = 1
            if (girl_name == "liza" or girl_name == "georgett") and str(getLocation(girl_name) or "") != "TavernMain":
                $ _dssd_know_about_birth = 0
            if (girl_name == "becky" or girl_name == "inga") and Becky.rel < 12:
                $ _dssd_know_about_birth = 0

            if _dssd_know_about_birth == 0:
                $ DailyEventsList_Add(girl_name, "alllocs", -1, ">", 1, 9999, "GiveBirth", "CreateKid")
            else:
                $ DailyEventsList_Add(girl_name, "alllocs", -1, ">", 1, 9999, "GiveBirth", "GiveBirth")

    call DressUp(girl_name, 1)

    if girl_name == "amanda" or girl_name == "melissa":
        if CheckDailyEventExists(girl_name, "MomDressComplain") == 0:
            $ _dssd_top_slut = DressPartSlut.get(topdress.get(girl_name, ""), 0)
            $ _dssd_bottom_slut = DressPartSlut.get(bottomdress.get(girl_name, ""), 0)
            $ _dssd_slut_dress_trigger = 0
            if _dssd_top_slut + _dssd_bottom_slut >= 10:
                $ _dssd_slut_dress_trigger = 1
            if _dssd_top_slut >= 6:
                $ _dssd_slut_dress_trigger = 1
            if _dssd_bottom_slut >= 6:
                $ _dssd_slut_dress_trigger = 1
            if int(Sandra.corruption or 0) <= 25 and _dssd_top_slut + _dssd_bottom_slut >= 8:
                $ _dssd_slut_dress_trigger = 1

            $ _dssd_talked_before = Amanda.var_int("MomDressComplaint", 0) if girl_name == "amanda" else Melissa.var.get("MomDressComplaint", 0)
            if _dssd_slut_dress_trigger == 1 and procedural_randint(1, 2 + _dssd_talked_before * 15, "mom_dress_complain_%s_%s" % (girl_name, int(dayspassed or 0))) == 1:
                $ DailyEventsList_Add(girl_name, "TavernMain", 4, "<", 1, 1, "MomDressComplain", "MomDressComplaint")

    if _dssd_info is not None and hasattr(_dssd_info, "reset_daily"):
        $ _dssd_was_drunk = int(getattr(_dssd_info, "drunk", 0) or 0)
        $ _dssd_info.reset_daily(False)
        if _dssd_was_drunk > 0:
            $ _dssd_info.change_social(friend_delta=-2, corruption_delta=-4)

    $ _dssd_days_age_young_kid = GetYoungestKidAge(girl_name)
    if _dssd_days_age_young_kid >= 0 and _dssd_days_age_young_kid < 300:
        $ Breastfeed[girl_name] = 1
    if Breastfeed.get(girl_name, 0) or pregnancy.get(girl_name, 0) > 230:
        $ Lactate[girl_name] = 1

    call CockPosition(girl_name, 0)
    $ adjust_otkroven(girl_name)
    call IncreaseSkill(girl_name)

    $ _dssd_jobs = getattr(_dssd_info, "jobs", {}) if _dssd_info is not None else {}
    $ _dssd_clients = int(_dssd_info.sex_stat("clients_day_total", 0) or 0) if _dssd_info is not None and hasattr(_dssd_info, "sex_stat") else 0
    if int(_dssd_jobs.get("jobwhore", 0) or 0):
        $ TotalWhoreClients[girl_name] = TotalWhoreClients.get(girl_name, 0) + _dssd_clients
    if int(_dssd_jobs.get("jobgloryhole", 0) or 0):
        $ TotalGloryHoleClients[girl_name] = TotalGloryHoleClients.get(girl_name, 0) + _dssd_clients
    return
