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
        Georgett.ensure_story_defaults()
        Amanda.ensure_story_defaults()
        week_val = _ndf_int(calendar_v2.week, 1)
        dayspassed_val = int(current_game_day())
        church_donated_amount = _ndf_int(player.economy.church_donated_amount, 0)
        glory_hole_look = _ndf_int(player.tavern_management.glory_hole_look, 0)

        if Georgett.story_value("TalkChurchAfterCermonLiza", 0) and not Liza.prostitution_started:
            Liza.prostitution_started = True

        if week_val == 7 and Becky.priest_advice_stage > 0 and CheckIfSexEventExist("becky", 99, "Priest") > 0:
            if Becky.priest_advice_stage in (1, 2):
                Becky.priest_advice_stage = 2
                if procedural_randint(1, 70, "becky_priest_advice_finish_%s" % dayspassed_val) * 30 <= church_donated_amount:
                    Becky.priest_advice_stage = 3
            if Becky.priest_advice_stage == 3:
                if Becky.home_visit_stage < 7 and Becky.eddie_join_stage >= 4:
                    Becky.home_visit_stage = 7

        while SexEvents.today_events:
            tmpArray = TodaySexEvents_PopFirst()
            girl = str(tmpArray.get("GirlName", "") or "")
            place = str(tmpArray.get("Place", "") or "")
            event_type = _ndf_int(tmpArray.get("EventType", 0), 0)

            if girl == "georgett" and event_type == 99 and place == "Prostitution":
                pregnancy_check(girl, "inside", 1, "eddie")
            elif girl == "georgett" and place == "EddieHomeVisit":
                pregnancy_check(girl, "mouth", 1, "eddie")
            elif girl == "liza" and event_type == 99:
                pregnancy_check(girl, "mouth", 1, "legare")
            elif girl == "inga" and place == "Lucas":
                inside_or_mouth = "inside" if procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:65:1") <= 2 else "mouth"
                pregnancy_check(girl, inside_or_mouth, 1, "Лукас")
            elif place == "Glory":
                glory_hole_inside = "mouth"
                girl_info = people.get_info(girl)
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
                    pregnancy_check(girl, glory_hole_inside, 1, "Мастер Драупнир")
                elif event_type == 2:
                    pregnancy_check(girl, glory_hole_inside, 1, "Эдди")
                elif glory_hole_look == 3:
                    pregnancy_check(girl, glory_hole_inside, 1, "Мессир Легаре")
                elif event_type == 4:
                    pregnancy_check(girl, glory_hole_inside, 1, "Отец Герхард")
                else:
                    pregnancy_check(girl, glory_hole_inside, 1, "", 1, "")
            elif girl == "amanda" and place == "glorytry":
                Amanda.set_var_int("glorytried", 1)
                pregnancy_check(girl, "mouth", 1, "", 1, "")
            elif girl == "amanda" and place == "legarerun":
                Amanda.resolve_legare_let_go()
            elif girl == "amanda" and place == "lovermeet":
                Amanda.lover_sex_calc()
            elif place == "Priest":
                pregnancy_check(girl, "inside", 1, "Отец Герхард")
                if girl == "becky" and procedural_randint(1, 2, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:99:5") == 1:
                    Becky.last_store_orgasm_day = dayspassed_val
            elif girl == "becky":
                if place == "StoreLover":
                    if event_type == 1:
                        pregnancy_check("becky", "inside", 1, "Легаре")
                    if event_type == 2:
                        pregnancy_check("becky", "inside", 1, "", 1, "Неизвестный грузчик")
                    Becky.last_store_orgasm_day = dayspassed_val
                elif place == "EddieMom":
                    eddie = people.get_info("eddie")
                    eddie_came_today = _ndf_int(eddie.ensure_sex_state().get("came_today", 0), 0) if eddie is not None else 0
                    if eddie_came_today == 0:
                        inside_or_mouth = "inside" if procedural_randint(1, 2, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:112:6") == 1 else "mouth"
                        pregnancy_check(girl, inside_or_mouth, 1, "eddie")
                        if procedural_randint(1, 5, key="procedural:Utilities/Time/NextDay_FinishDayEvents.rpy:procedural_randint:114:7") == 1:
                            Becky.last_store_orgasm_day = dayspassed_val
            else:
                pregnancy_check(girl, "", 1, "")

        while SexEvents.girl_dance:
            tmpArray = GirlDance_PopFirst()
            event_amanda_legare_create_dance()
            if _ndf_int(tmpArray.get("GoOut", 0), 0) == 1:
                Amanda.resolve_legare_let_go()

        if Amanda.var_int("gloryscold", 0) or Amanda.var_int("glorywalkout", 0) or Amanda.var_int("glorysuck", 0) or Amanda.var_int("glorydeflower", 0):
            Amanda.set_var_int("gloryyouknow", 1)
        if Amanda.var_int("glorysuck", 0):
            Amanda.set_var_int("suckyou", 1)
        if Amanda.var_int("glorydeflower", 0):
            Amanda.set_var_int("fuckyou", 1)
        if Amanda.var_int("glorydeflower", 0) or Amanda.var_int("fuckyou", 0) or Amanda.player_saw_legare_sex or Amanda.var_int("sawwithguys", 0) or Amanda.player_knows_legare_sex or Amanda.var_int("knownotvirgin", 0):
            Amanda.set_var_int("knowsexactive", 1)
        Amanda.knows_player_is_watching_legare_sex = False
        Amanda.room_entry_blocked_today = False
        Amanda.pregnancy_risk_asked_today = False
        Amanda.left_friday_dance = False
        Becky.left_dances = 0
        Amanda.legare_affection = max(0, min(Amanda.legare_affection, 20))
        Amanda.set_var_int("lizafriends", max(0, min(Amanda.var_int("lizafriends", 0), 20)))

        player.economy.church_donated_today = 0
        rooms.get("FridayDance").dance_count = 0
        TownStreet.settle_blackworker_candidates()
        TownStreet.reset_day()

        daily_events.end_day(week_val)

label NextDay_FinishDayEvents:
    $ renpy.dynamic("_ndf_all_girl_names", "_ndf_all_girl_index")
    python:
        next_day_finish_day_events()
        _ndf_all_girl_names = [info.name for info in people.girl_values()]
        _ndf_all_girl_index = 0

    while _ndf_all_girl_index < len(_ndf_all_girl_names):
        call DailySetstatdefault(_ndf_all_girl_names[_ndf_all_girl_index])
        $ _ndf_all_girl_index += 1

    $ people_reset_daily_interactions()

    python:
        if player.intimacy.ellona_cursed:
            player.intimacy.ellona_curse_days -= 1

        if player.horse.stolen_days > 0:
            player.horse.stolen_days -= 1

    return
