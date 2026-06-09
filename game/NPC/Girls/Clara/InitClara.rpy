# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import random
    import renpy.exports as renpy

    def clara_extra_location_code(day_marker=None, weekday=None):
        day_value = int(dayspassed if day_marker is None else day_marker or 0)
        week_value = int(week if weekday is None else weekday or 0)
        parity = (day_value + week_value) % 2

        if week_value == 5 and time_value == 3:
            return "FridayDance" if parity == 0 else ""

        if clara_melissa_visit_active(day_value, week_value, time_value):
            return "TavernMelissaRoom"

        if clara_market_visit_active(day_value, week_value, time_value):
            return "MarketPlace"

        return ""

    def clara_can_start_social_events():
        try:
            update_stat_state()
        except Exception:
            pass
        return int(charisma or 0) >= 70 and int(Friends.get("clara", 0) or 0) >= 5

    def clara_can_receive_gifts():
        try:
            update_stat_state()
        except Exception:
            pass
        charisma_safe = getattr(renpy.store, 'charisma', 0)
        Friends_safe = getattr(renpy.store, 'Friends', {})
        return int(charisma_safe or 0) >= 70 and int(Friends_safe.get("clara", 0) or 0) >= 7

    def clara_has_caught_cat_gift():
        WerecatVar_safe = getattr(renpy.store, 'WerecatVar', {})
        return werecat_second_gift_available() and int(WerecatVar_safe.get("caught", 0) or 0) == 1

    def clara_wine_store_talk_picture():
        candidates = [
            "images/clara/wineSellar_clara_talk.png",
            "images/clara/wine_sellar_clara_talk_2.png",
            "images/clara/wineSellar_clara_talk_3.png",
            "images/clara/wineSellar_clara_talk_4.png",
            "images/clara/wineSellar_clara_talk_5.png",
            "images/clara/wineSellar_clara_talk_6.png",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def clara_wine_store_flirt_picture():
        candidates = [
            "images/clara/wineSellar_clara_flirt_0.png",
            "images/clara/wineSellar_clara_flirt_1.png",
            "images/clara/wineSellar_clara_flirt_2.png",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def clara_forest_picture(location_code=""):
        location_key = str(location_code or "").strip()
        candidates = []
        if location_key == "ForestClearing":
            candidates = [
                "images/clara/forest_clara.png",
                "images/clara/forest_clara_0.png",
                "images/clara/forest_clara_1.png",
                "images/clara/forest_clara_encounter.png",
                "images/clara/forest_clara_encounter_2.png",
            ]
        elif location_key == "ForestSpring":
            candidates = [
                "images/clara/forestSpring_clara.png",
                "images/clara/forest_spring_clara_1.png",
                "images/clara/forest_spring_clara_2.png",
            ]
        elif location_key == "ForestLake":
            candidates = [
                "images/clara/forestlake_clara.png",
                "images/clara/forestlake_clara_0.png",
                "images/clara/forestLake_clara_2.png",
            ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def alber_random_portrait():
        candidates = [
            "images/Alber/portrait1.png",
            "images/Alber/portrat2.png",
            "images/Alber/portrait3.png",
            "images/Alber/portrait4.png",
            "images/Alber/portrait5.jpg",
            "images/Alber/portrait6.jpg",
            "images/Alber/portrait7.jpg",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def clara_wine_store_shift_active(weekday=None, time_slot=None):
        week_value = int(week if weekday is None else weekday or 0)
        clock_value = int(clock_minutes or 0) % 1440
        if week_value == 7:
            return False
        return 8 * 60 <= clock_value <= 11 * 60 + 59

    def clara_market_visit_active(day_marker=None, weekday=None, time_slot=None):
        day_value = int(dayspassed if day_marker is None else day_marker or 0)
        week_value = int(week if weekday is None else weekday or 0)
        time_value = int(time if time_slot is None else time_slot or 0)
        if time_value == 2:
            if week_value == 7:
                return False
            return clara_market_daytime_roll_active(day_value, week_value)
        return clara_mongol_evening_market_active(day_value, week_value, time_value)

    def clara_mongol_evening_market_active(day_marker=None, weekday=None, time_slot=None):
        day_value = int(dayspassed if day_marker is None else day_marker or 0)
        week_value = int(week if weekday is None else weekday or 0)
        time_value = int(time if time_slot is None else time_slot or 0)
        if week_value in (5, 7) or time_value != 3:
            return False
        return clara_market_evening_roll_active(day_value, week_value)

    def clara_market_daytime_roll_active(day_marker=None, weekday=None):
        day_value = int(dayspassed if day_marker is None else day_marker or 0)
        week_value = int(week if weekday is None else weekday or 0)
        if week_value == 7:
            return False
        if int(ClaraVar.get("market_day_roll_day", -1) or -1) != day_value:
            ClaraVar["market_day_roll_day"] = day_value
            ClaraVar["market_day_roll"] = 1 if renpy.random.randint(1, 2) == 1 else 0
        return int(ClaraVar.get("market_day_roll", 0) or 0) == 1

    def clara_market_evening_roll_active(day_marker=None, weekday=None):
        day_value = int(dayspassed if day_marker is None else day_marker or 0)
        week_value = int(week if weekday is None else weekday or 0)
        if week_value in (5, 7):
            return False
        if int(ClaraVar.get("market_evening_roll_day", -1) or -1) != day_value:
            ClaraVar["market_evening_roll_day"] = day_value
            ClaraVar["market_evening_roll"] = 1 if renpy.random.randint(1, 3) == 1 else 0
        return int(ClaraVar.get("market_evening_roll", 0) or 0) == 1

    def clara_melissa_visit_active(day_marker=None, weekday=None, time_slot=None):
        week_safe = getattr(renpy.store, 'week', 0)
        time_safe = getattr(renpy.store, 'time', 0)
        week_value = int(week_safe if weekday is None else weekday or 0)
        time_value = int(time_safe if time_slot is None else time_slot or 0)
        if Melissa.bats_stage() < 8:
            return False
        if not werecat_is_living_with_household():
            return False
        if time_value == 3:
            if week_value == 5:
                return False
            MongolVar_safe = getattr(renpy.store, 'MongolVar', {})
            RobinVar_safe = getattr(renpy.store, 'RobinVar', {})
            return int(MongolVar_safe.get("StocksReleased", 0) or 0) == 1 or int(RobinVar_safe.get("MongolSafePass", 0) or 0) == 1
        if time_value != 4:
            return False
        return week_value in (1, 2, 3, 4, 5, 6, 7)

    def clara_tavern_visit_active(day_marker=None, weekday=None, time_slot=None):
        dayspassed_safe = getattr(renpy.store, 'dayspassed', 0)
        week_safe = getattr(renpy.store, 'week', 0)
        time_safe = getattr(renpy.store, 'time', 0)
        day_value = int(dayspassed_safe if day_marker is None else day_marker or 0)
        week_value = int(week_safe if weekday is None else weekday or 0)
        time_value = int(time_safe if time_slot is None else time_slot or 0)
        if time_value != 2:
            return False
        if week_value == 7:
            return False
        if ((day_value + week_value) % 4) != 0:
            return False
        try:
            return str(getLocation("melissa") or "") == "TavernMain"
        except Exception:
            return True

    def clara_visible_at_friday_dance():
        try:
            return int(CheckIfDanceExist("amanda", "legare", int(FridayDancesCount or 0)) or 0) <= 0
        except Exception:
            return True

    def clara_can_accept_horse_ride(location_code=""):
        location_key = str(location_code or CurLoc or "").strip()
        if location_key not in ("ForestClearing", "ForestLake"):
            return False
        if str(getLocation("clara") or "") != str(location_key or ""):
            return False
        return bool(str(MyStallion or "").strip()) and int(HorseSaddled or 0) == 1

    def clara_giftable_entries():
        entries = []

        item_ids = ("soap_001", "special_mushroom_001", "lavender_001","luxury_soap_001", "libido_tincture_001")
        for item_id in item_ids:
            if _player_item_count_by_id(item_id) <= 0:
                continue
            item_obj = get_game_item(item_id)
            if item_obj is None:
                continue
            entries.append({
                "source": "item",
                "gift_id": str(item_id),
                "gift_name": str(getattr(item_obj, "name", item_id) or item_id),
            })

        dress_codes = (
            "thiefdress",
            "simplebra",
            "simplepanties",
            "blackstockings",
            "redstockings",
        )
        for dress_code in dress_codes:
            if not player_state().appearance.has_dress(dress_code):
                continue
            if str(player_state().appearance.current_dress or "") == str(dress_code or ""):
                continue
            entries.append({
                "source": "dress",
                "gift_id": "dress_" + str(dress_code),
                "gift_name": str(ShortDressName.get(dress_code, dress_code) or dress_code),
                "dress_code": str(dress_code),
            })

        if clara_has_caught_cat_gift():
            entries.append({
                "source": "werecat",
                "gift_id": "werecat_caught_cat",
                "gift_name": "пойманная лесная кошка",
            })

        return entries

    def clara_has_giftable_entries():
        return len(list(clara_giftable_entries() or [])) > 0

    def clara_remove_gift_entry(entry):
        row = dict(entry or {})
        source = str(row.get("source", "") or "")
        if source == "werecat":
            if not werecat_second_gift_available() or int(WerecatVar.get("caught", 0) or 0) != 1:
                return False
            werecat_apply_clara_gift_bonus()
            return True
        if source == "dress":
            dress_code = str(row.get("dress_code", "") or "")
            if dress_code == "" or not player_state().appearance.has_dress(dress_code):
                return False
            if dress_code == str(player_state().appearance.current_dress or ""):
                return False
            appearance = player_state().appearance
            result = appearance.remove_dress(dress_code)
            appearance.apply_to_store()
            return result

        item_id = str(row.get("gift_id", "") or "")
        if item_id == "":
            return False
        return _player_remove_item_by_id(item_id, 1)

    def clara_social_outcome(interaction_type="talk", gift_item_id=""):
        interaction = str(interaction_type or "talk").strip().lower()
        gift_id = str(gift_item_id or "").strip()
        score = 0
        score += int(charisma or 0) // 15
        score += int(Friends.get("clara", 0) or 0) // 4
        score += int(ClaraVar.get("trust", 0) or 0) // 3
        score += int(sluttiness.get("clara", 0) or 0) // 10

        if str(player_state().appearance.current_dress or "") == "thiefdress":
            score += 1

        if interaction == "flirt":
            score += 2
            score -= int(FlirtedToday.get("clara", 0) or 0) * 3
        elif interaction == "gift":
            score += 1
            score -= int(GiftedToday.get("clara", 0) or 0) * 3
            if gift_id == "werecat_caught_cat":
                score += 4
            elif gift_id in tuple(preferred_gift_item_ids("clara")):
                score += 3
            elif gift_id != "":
                score -= 2
        else:
            score -= int(TalkedToday.get("clara", 0) or 0) * 2

        score += random.randint(-2, 2)

        if score >= 7:
            return "positive"
        if score >= 4:
            return "neutral"
        return "negative"

label InitClara:
    python:
        knowsMC["clara"] = True
        GirlName = "clara"
        RealName[GirlName] = "Кларисса"
        RealName2[GirlName] = "Клариссы"
        RealName3[GirlName] = "Клариссе"
        age_girls[GirlName] = 19
        kids[GirlName] = 0
        beauty[GirlName] = 62
        sluttiness[GirlName] = 10
        sexacts[GirlName] = 0
        cuminside[GirlName] = 0
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ""
        ConceptionChance[GirlName] = 10
        CurrentLoc[GirlName] = "WineStore"
        PussyWetStart[GirlName] = 10
        virginity[GirlName] = True

        girltextdesc[GirlName] = "Кларисса, старшая дочь мессира Легаре, молодая девушка из зажиточного купеческого дома. Это очень приветливая и игривая блондинка чуть младше вас, с большими искрящимися серыми глазами, пухлыми губами и удивительно легкой, грациозной походкой. На ней обычно свободное длинное повседневное платье из легкой ткани, похожее на удобный сарафан; на ярком свету ткань кажется чуть прозрачной. Грудь Клариссы размера B мягко и соблазнительно колышется при каждом движении. От нее пахнет лавандой и дорогими модными духами."
        dressdefault[GirlName] = "greenworkdress"
        bradef[GirlName] = "simplebra"
        pantiesdef[GirlName] = "simplepanties"
        legsdef[GirlName] = ""
        shoesdef[GirlName] = "simpleshoes"

        cooking[GirlName] = 10
        cleaning[GirlName] = 8
        waitress[GirlName] = 45
        otkroven[GirlName] = 0

        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        jobHallAvail[GirlName] = 0
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0
        Friends[GirlName] = 0
        Talked[GirlName] = 0
        ClaraVar["flirt"] = 0
        ClaraVar["knownotvirgin"] = 0
        ClaraVar["trust"] = 0
        ClaraVar["positive"] = 0
        ClaraVar["neutral"] = 0
        ClaraVar["negative"] = 0
        ClaraVar["lastsocial"] = ""
        ClaraVar["booklet_market_seen"] = 0
        ClaraVar["market_intro_seen"] = 0
        ClaraVar["market_evening_intro_seen"] = 0
        ClaraVar["market_day_roll_day"] = -1
        ClaraVar["market_day_roll"] = 0
        ClaraVar["market_evening_roll_day"] = -1
        ClaraVar["market_evening_roll"] = 0
        ClaraVar["mongol_theft_seen"] = 0
        ClaraVar["escape_confessed"] = 0
        ClaraVar["merchant_contact_unlocked"] = 0
        ClaraVar["merchant_contact_month_key"] = -1
        ClaraVar["tavern_melissa_visit_count"] = 0
        ClaraVar["tavern_melissa_visit_day"] = -1
        ClaraVar["tavern_melissa_overheard_2_seen"] = 0
        ClaraVar["tavern_melissa_overheard_3_seen"] = 0
        ClaraVar["old_water_pump_hint_seen"] = 0
        ClaraVar["paintings_melissa_asked"] = 0
        ClaraVar["cellar_seen"] = 0
        ClaraVar["cellar_spanking_discovered"] = 0
        ClaraVar["cellar_confronted"] = 0
        ClaraVar["comfort_pending"] = 0
        ClaraVar["comfort_done"] = 0
        ClaraVar["second_ask_unlocked"] = 0
        ClaraVar["source_known"] = 0
        ClaraVar["sex_engine_unlocked"] = 0
        ClaraVar["necking_unlocked"] = 0
        ClaraVar["petting_unlocked"] = 0
        ClaraVar["fiance_church_seen"] = 0
        ClaraVar["fiance_barber_seen"] = 0
        ClaraVar["fiance_barber_night_roll_day"] = -1
        ClaraVar["fiance_barber_night_roll"] = 0
        ClaraVar["fiance_barber_secret_seen"] = 0
        ClaraVar["commission_started"] = 0
        ClaraVar["commission_followup_done"] = 0
        ClaraVar["commission_followup_day"] = 999999
        ClaraVar["peek_done"] = 0
        ClaraVar["confession_done"] = 0
        ClaraVar["murder_day"] = 999999
        ClaraVar["murder_seen"] = 0
        ClaraVar["murder_solved"] = 0
        ClaraVar["special_cream_recipe_unlocked"] = 0
        ClaraVar["sergio_discount"] = 0
        ClaraVar["anal_unlocked"] = 0
        ClaraVar["virginity_choice_unlocked"] = 0
        GiftPreferences[GirlName] = [
            "dress_thiefdress",
            "soap_001",
            "special_mushroom_001",
            "dress_simplebra",
            "dress_simplepanties",
            "dress_blackstockings",
            "dress_redstockings",
            "libido_tincture_001",
            "werecat_caught_cat",
        ]

        # Uppercase compatibility for legacy references.
        Friends["Clara"] = Friends[GirlName]
        Talked["Clara"] = Talked[GirlName]
        bodymodel_sync_character(GirlName, RealName[GirlName], "female")
        npc_daily_schedule_set(
            GirlName,
            default_slots=[
                npc_daily_schedule_slot(0, "WineStore", True, True, "morning_wine_store"),
                dict(npc_daily_schedule_slot(0, "Church", True, False, "sunday_church"), weekdays=[7]),
                npc_daily_schedule_slot(4, "WineStore", False, False, "sleep_home"),
            ],
            random_slots=[
                npc_daily_schedule_random_slot(
                    1,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="noon",
                    choices=[
                        npc_daily_schedule_choice("WineStore", 5, True, True, "wine_store_with_legare"),
                        npc_daily_schedule_choice("ForestClearing", 1, True, True, "forest_clearing"),
                        npc_daily_schedule_choice("ForestLake", 1, True, True, "forest_lake"),
                        npc_daily_schedule_choice("ForestSpring", 1, True, True, "forest_spring"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    1,
                    weekdays=[7],
                    label="sunday_noon",
                    choices=[
                        npc_daily_schedule_choice("WineStore", 3, True, True, "home_after_church"),
                        npc_daily_schedule_choice("TavernMain", 2, True, True, "sunday_tavern_visit"),
                        npc_daily_schedule_choice("ForestClearing", 1, True, True, "sunday_forest_walk"),
                        npc_daily_schedule_choice("ForestLake", 1, True, True, "sunday_forest_lake"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    2,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="day",
                    choices=[
                        npc_daily_schedule_choice("MarketPlace", 5, True, False, "market_drawings"),
                        npc_daily_schedule_choice("BarberShop", 1, True, True, "monthly_barber", monthly_key="clara_barber", monthly_limit=1),
                        npc_daily_schedule_choice("DressShop", 1, True, True, "tailor_visit", monthly_key="clara_tailor", monthly_limit=2),
                        npc_daily_schedule_choice("TavernMain", 2, True, True, "tavern_visit"),
                        npc_daily_schedule_choice("ForestClearing", 1, True, True, "forest_walk"),
                        npc_daily_schedule_choice("ForestLake", 1, True, True, "forest_lake"),
                        npc_daily_schedule_choice("WineStore", 2, True, True, "wine_store_day"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    2,
                    weekdays=[7],
                    label="sunday_day",
                    choices=[
                        npc_daily_schedule_choice("TavernMain", 3, True, True, "sunday_tavern_visit"),
                        npc_daily_schedule_choice("ForestClearing", 2, True, True, "sunday_forest_walk"),
                        npc_daily_schedule_choice("ForestLake", 1, True, True, "sunday_forest_lake"),
                        npc_daily_schedule_choice("WineStore", 2, True, True, "home_sunday_day"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[1, 2, 3, 4, 6],
                    label="evening",
                    choices=[
                        npc_daily_schedule_choice("MarketPlace", 4, True, False, "evening_market_mongol"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "melissa_room_evening", condition=npc_schedule_rule("clara_melissa_visit", slot=3)),
                        npc_daily_schedule_choice("TavernMain", 1, True, True, "tavern_evening"),
                        npc_daily_schedule_choice("WineStore", 2, True, True, "home_evening"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[5],
                    label="friday_evening",
                    choices=[
                        npc_daily_schedule_choice("FridayDance", 4, True, True, "friday_dance", condition=npc_schedule_rule("clara_visible_friday_dance")),
                        npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "melissa_room_friday"),
                        npc_daily_schedule_choice("WineStore", 1, True, True, "home_friday_evening"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[7],
                    label="sunday_evening",
                    choices=[
                        npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "melissa_room_sunday", condition=npc_schedule_rule("clara_melissa_visit", slot=3)),
                        npc_daily_schedule_choice("TavernMain", 2, True, True, "sunday_tavern_evening"),
                        npc_daily_schedule_choice("WineStore", 3, True, True, "home_sunday_evening"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    4,
                    weekdays=[1, 2, 3, 4, 5, 6, 7],
                    label="late_night",
                    choices=[
                        npc_daily_schedule_choice("WineStore", 8, False, False, "sleep_home"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 1, True, True, "late_melissa_room", condition=npc_schedule_rule("clara_melissa_visit", slot=4)),
                    ],
                ),
            ],
        )
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=clara_visible_at_friday_dance, priority=220, label="friday_dance"),
                NPCScheduleEntry(location="WineStore", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("clara_paintings_evening_watch"), priority=280, label="clara_paintings_evening_watch"),
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[3, 4], awake=True, talkable=True, condition=npc_schedule_rule("clara_paintings_confession"), priority=270, label="clara_paintings_confession"),
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[3, 4], awake=True, talkable=True, condition=clara_melissa_visit_active, priority=210, label="melissa_room_visit"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[2], awake=True, talkable=True, condition=clara_tavern_visit_active, priority=200, label="tavern_visit"),
                NPCScheduleEntry(location="MarketPlace", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[2, 3], awake=True, talkable=False, condition=clara_market_visit_active, priority=190, label="extra_market"),
                NPCScheduleEntry(location="WineStore", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[1, 2], awake=True, talkable=True, condition=clara_wine_store_shift_active, priority=180, label="wine_store"),
                NPCScheduleEntry(location="WineStore", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_daily_schedule_build_all(True)
        npc_schedule_sync_currentloc(GirlName)

    return

# Auto-attach .var for PeopleInfo consistency (requested)
init python:
    if 'peopleInfo' not in dir() or not isinstance(peopleInfo, dict):
        peopleInfo = {}
    # Per user request: class Clara(Girl) defined in game/NPC/Girls/Clara/InitClara.rpy
    if 'clara' not in peopleInfo or not isinstance(peopleInfo.get('clara'), Clara):
        class Clara(Girl):
            """Clara (paintings, lunar fertility)."""
            def __init__(self, name="clara", **kwargs):
                super().__init__(name, **kwargs)
                if 'ClaraVar' in dir() and isinstance(ClaraVar, dict):
                    self.var = ClaraVar
                    self.promote_from_var(ClaraVar)
        peopleInfo['clara'] = Clara(var=ClaraVar if 'ClaraVar' in dir() else {})
    else:
        if 'ClaraVar' in dir() and isinstance(ClaraVar, dict):
            peopleInfo['clara'].var = ClaraVar
    if 'girls' not in dir() or not isinstance(girls, list):
        girls = []
    if peopleInfo.get('clara') not in girls:
        girls.append(peopleInfo['clara'])
