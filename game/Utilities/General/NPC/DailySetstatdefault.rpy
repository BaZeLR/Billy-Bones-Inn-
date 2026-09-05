# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label DailySetstatdefault(girl_name):
    $ renpy.dynamic("_dssd_slut_dress_trigger", "_dssd_know_about_birth", "_dssd_pregnancy_days", "_dssd_info", "_dssd_suspects_count", "_dssd_top_slut", "_dssd_bottom_slut", "_dssd_talked_before", "_dssd_was_drunk", "_dssd_days_age_young_kid", "_dssd_jobs", "_dssd_clients")
    $ _dssd_info = people.get_info(girl_name)
    if _dssd_info is not None:
        $ _dssd_info.set_arousal(_dssd_info.sex_stat("PussyWetStart", 0))
        $ _dssd_info.clear_cum()
        $ _dssd_info.set_sex_stat("breastfeed", 0)
        $ _dssd_info.set_sex_stat("lactate", 0)
    $ _dssd_pregnancy_days = _dssd_info.pregnancy_days() if _dssd_info is not None else 0

    if _dssd_info is not None and not (girl_name == "inga" and Inga.acquaintance_stage == 0):
        if _dssd_pregnancy_days > 0:
            $ _dssd_pregnancy_days += 1
            $ _dssd_info.set_sex_stat("pregnancy", _dssd_pregnancy_days)

    $ _dssd_suspects_count = ZaletSuspectLinesCount(girl_name)
    if _dssd_suspects_count == 0 and _dssd_pregnancy_days >= 50:
        $ ZaletGetSuspectList(girl_name)

    if daily_events.exists(girl_name, "MorningSickness") == 0:
        if ((_dssd_pregnancy_days > 0 and _dssd_pregnancy_days < 80 and procedural_randint(1, 7, "morning_sickness_%s_%s" % (girl_name, int(current_game_day()))) == 1)
                or (_dssd_pregnancy_days == 0 and procedural_randint(1, 60, "false_morning_sickness_%s_%s" % (girl_name, int(current_game_day()))) == 32)):
            $ daily_events.add(girl_name, "TavernKitchen", 1, "<", 1, 8, "MorningSickness", "MorningSickness", "girl")

    if daily_events.exists(girl_name, "GiveBirth") == 0:
        if ((_dssd_pregnancy_days > 240 and procedural_randint(1, 45, "birth_window_%s_%s" % (girl_name, int(current_game_day()))) > max(270 - _dssd_pregnancy_days, 0) + 10 and procedural_randint(1, 3, "birth_confirm_%s_%s" % (girl_name, int(current_game_day()))) == 1)
                or _dssd_pregnancy_days >= 285):
            $ _dssd_know_about_birth = 1
            if (girl_name == "liza" or girl_name == "georgett") and str(people.location(girl_name) or "") != "TavernMain":
                $ _dssd_know_about_birth = 0
            if (girl_name == "becky" or girl_name == "inga") and Becky.rel < 12:
                $ _dssd_know_about_birth = 0

            if _dssd_know_about_birth == 0:
                $ daily_events.add(girl_name, "alllocs", -1, ">", 1, 9999, "GiveBirth", "CreateKid", "girl_location")
            else:
                $ daily_events.add(girl_name, "alllocs", -1, ">", 1, 9999, "GiveBirth", "GiveBirth", "girl")

    call DressUp(girl_name, 1)

    if girl_name == "amanda" or girl_name == "melissa":
        if daily_events.exists(girl_name, "MomDressComplain") == 0:
            $ _dssd_top_slut = _dssd_info.clothing_slut("top")
            $ _dssd_bottom_slut = _dssd_info.clothing_slut("bottom")
            $ _dssd_slut_dress_trigger = 0
            if _dssd_top_slut + _dssd_bottom_slut >= 10:
                $ _dssd_slut_dress_trigger = 1
            if _dssd_top_slut >= 6:
                $ _dssd_slut_dress_trigger = 1
            if _dssd_bottom_slut >= 6:
                $ _dssd_slut_dress_trigger = 1
            if int(Sandra.corruption or 0) <= 25 and _dssd_top_slut + _dssd_bottom_slut >= 8:
                $ _dssd_slut_dress_trigger = 1

            $ _dssd_talked_before = int(Amanda.mom_dress_complaint_count or 0) if girl_name == "amanda" else int(Melissa.mom_dress_complaint_count or 0)
            if _dssd_slut_dress_trigger == 1 and procedural_randint(1, 2 + _dssd_talked_before * 15, "mom_dress_complain_%s_%s" % (girl_name, int(current_game_day()))) == 1:
                $ daily_events.add(girl_name, "TavernMain", 4, "<", 1, 1, "MomDressComplain", "MomDressComplaint", "girl")

    if _dssd_info is not None:
        $ _dssd_was_drunk = int(getattr(_dssd_info, "drunk", 0) or 0)
        $ _dssd_info.reset_daily(False)
        if _dssd_was_drunk > 0:
            $ _dssd_info.change_social(friend_delta=-2, corruption_delta=-4)

    $ _dssd_days_age_young_kid = GetYoungestKidAge(girl_name)
    if _dssd_days_age_young_kid >= 0 and _dssd_days_age_young_kid < 300:
        $ _dssd_info.set_sex_stat("breastfeed", 1)
    if _dssd_info.sex_stat("breastfeed", 0) or _dssd_pregnancy_days > 230:
        $ _dssd_info.set_sex_stat("lactate", 1)

    call CockPosition(girl_name, 0)
    $ _dssd_info.reset_openness_from_relationship()
    call IncreaseSkill(girl_name)

    $ _dssd_jobs = getattr(_dssd_info, "jobs", {}) if _dssd_info is not None else {}
    $ _dssd_clients = int(_dssd_info.sex_stat("clients_day_total", 0) or 0) if _dssd_info is not None else 0
    if tavern_sex_work_day_allowed():
        if int(_dssd_jobs.get("jobwhore", 0) or 0):
            $ TotalWhoreClients[girl_name] = TotalWhoreClients.get(girl_name, 0) + _dssd_clients
        if int(_dssd_jobs.get("jobgloryhole", 0) or 0):
            $ TotalGloryHoleClients[girl_name] = TotalGloryHoleClients.get(girl_name, 0) + _dssd_clients
    return
