# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import random
    import renpy.exports as renpy

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
        clock_safe = getattr(renpy.store, 'clock_minutes', 480)
        day_value = int(dayspassed_safe if day_marker is None else day_marker or 0)
        week_value = int(week_safe if weekday is None else weekday or 0)
        clock_value = int(clock_safe or 0) % 1440
        if clock_value < 720 or clock_value > 1079:
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

    def clara_story_defaults():
        return {
            "flirt": 0,
            "knownotvirgin": 0,
            "trust": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "lastsocial": "",
            "booklet_market_seen": 0,
            "drawings_secret_known": 0,
            "market_intro_seen": 0,
            "market_evening_intro_seen": 0,
            "market_follow_failed_day": -1,
            "market_follow_failed_hour": -1,
            "market_day_roll_day": -1,
            "market_day_roll": 0,
            "market_evening_roll_day": -1,
            "market_evening_roll": 0,
            "mongol_theft_seen": 0,
            "escape_confessed": 0,
            "merchant_contact_unlocked": 0,
            "merchant_contact_month_key": -1,
            "tavern_visit_bar_0_seen": 0,
            "tavern_visit_bar_1_seen": 0,
            "tavern_visit_bar_2_seen": 0,
            "melissa_room_visit_0_seen": 0,
            "melissa_room_visit_1_seen": 0,
            "melissa_room_visit_2_seen": 0,
            "melissa_room_visit_count": 0,
            "old_water_pump_hint_seen": 0,
            "paintings_melissa_asked": 0,
            "cellar_seen": 0,
            "cellar_spanking_discovered": 0,
            "cellar_confronted": 0,
            "comfort_pending": 0,
            "comfort_done": 0,
            "second_ask_unlocked": 0,
            "source_known": 0,
            "sex_engine_unlocked": 0,
            "necking_unlocked": 0,
            "petting_unlocked": 0,
            "fiance_church_seen": 0,
            "fiance_seen_day": -1,
            "fiance_barber_seen": 0,
            "fiance_barber_night_roll_day": -1,
            "fiance_barber_night_roll": 0,
            "fiance_barber_secret_seen": 0,
            "commission_started": 0,
            "commission_followup_done": 0,
            "commission_followup_day": 999999,
            "peek_done": 0,
            "confession_done": 0,
            "drawings_betrayal_confessed": 0,
            "murder_day": 999999,
            "murder_seen": 0,
            "murder_solved": 0,
            "special_cream_recipe_unlocked": 0,
            "sergio_discount": 0,
            "anal_unlocked": 0,
            "virginity_choice_unlocked": 0,
            "werecat_gifted": 0,
            "werecat_gift_day": -1,
        }

    class ClaraData(PeopleData):
        code_name = "clara"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Кларисса",
                fullname="Кларисса",
                genitive="Клариссы",
                dative="Клариссе",
                description="Кларисса, старшая дочь мессира Легаре, молодая девушка из зажиточного купеческого дома. Это очень приветливая и игривая блондинка чуть младше вас, с большими искрящимися серыми глазами, пухлыми губами и удивительно легкой, грациозной походкой. На ней обычно свободное длинное повседневное платье из легкой ткани, похожее на удобный сарафан; на ярком свету ткань кажется чуть прозрачной. Грудь Клариссы размера B мягко и соблазнительно колышется при каждом движении. От нее пахнет лавандой и дорогими модными духами.",
            )
            self.birth_date = {"day":20, "period":11, "cycle": 1081}
            self.card_image = "images/clara/portrait1.jpg"
            self.schedule_source = "schedules/clara.json"

    class ClaraInfo(Girl):
        """Clara runtime: wine store, market booklet, paintings thread, social state."""
        def __init__(self):
            super().__init__("clara")
            self.code_name = "clara"
            self.data = ClaraStaticData
            self.age = 19
            self.rel = 0
            self.relationship = self.rel
            self.openness = 0
            self.corruption = 10
            self.known = True
            self.energy = 100
            self.energy_max = 100
            self.rebellion = 0
            self.anger_with_player = 0
            self.fun = 0
            self.trust = 0
            self.fear = 0
            self.mana = 25
            self.mana_corrupted = False
            self.mood = "neutral"
            self.reaction_log = []
            self.reaction_state = {
                "last_reaction": "",
                "last_reaction_day": None,
                "last_reaction_context": "",
                "last_reaction_score": 0,
                "last_mana_delta": 0,
                "last_mana_reasons": [],
                "pending_decision": "",
            }
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.stats = {
                "kids": 0,
                "beauty": 62,
                "sexacts": 0,
                "cuminside": 0,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 10,
                "PussyWetStart": 10,
                "virginity": True,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 10,
                "cleaning": 8,
                "waitress": 45,
            }
            self.jobs = {
                "jobkitchen": 0,
                "jobcleaning": 0,
                "jobwaitress": 0,
                "jobHallAvail": 0,
                "jobWhoreAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
            }
            self.gift_preferences = [
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
            self.schedule_source = ClaraStaticData.schedule_source
            self.schedule_uses_clock_minutes = True
            self.current_location = "WineStore"
            self.talk_preferences = {
                "favorite_topics": ["fashion", "stories", "secrets", "art", "family_life"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["greenworkdress", "simplebra", "simplepanties", "simpleshoes"],
                "gifted": [],
                "current_dress": "greenworkdress",
                "current_underwear": {
                    "bra": "simplebra",
                    "panties": "simplepanties",
                    "legs": "",
                    "shoes": "simpleshoes",
                },
            }
            self.var = {}
            self.ensure_story_defaults()

        def update(self):
            super(ClaraInfo, self).update()
            self.data = ClaraStaticData
            self.relationship = self.rel
            self.sync_from_clara_maps()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in clara_story_defaults().items():
                self.var.setdefault(key, value)
            self.trust = people_to_int(self.var.get("trust", self.trust), self.trust)
            return self.var

        def can_start_social_events(self):
            try:
                update_stat_state()
            except Exception:
                pass
            name = self.code_name
            return int(charisma or 0) >= 70 and int(Friends.get(name, 0) or 0) >= 5

        def can_receive_gifts(self):
            try:
                update_stat_state()
            except Exception:
                pass
            name = self.code_name
            return int(charisma or 0) >= 70 and int(Friends.get(name, 0) or 0) >= 7

        def has_caught_cat_gift(self):
            return werecat_second_gift_available() and int(WerecatVar.get("caught", 0) or 0) == 1

        def can_accept_horse_ride(self, location_code=""):
            location_key = str(location_code or CurLoc or "").strip()
            if location_key not in ("ForestClearing", "ForestLake"):
                return False
            if str(getLocation(self.code_name) or "") != str(location_key or ""):
                return False
            return bool(str(MyStallion or "").strip()) and int(HorseSaddled or 0) == 1

        def giftable_entries(self):
            entries = []

            item_ids = ("soap_001", "special_mushroom_001", "lavender_001", "luxury_soap_001", "libido_tincture_001")
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

            if self.has_caught_cat_gift():
                entries.append({
                    "source": "werecat",
                    "gift_id": "werecat_caught_cat",
                    "gift_name": "пойманная лесная кошка",
                })

            return entries

        def has_giftable_entries(self):
            return len(list(self.giftable_entries() or [])) > 0

        def remove_gift_entry(self, entry):
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

        def social_outcome(self, interaction_type="talk", gift_item_id=""):
            name = self.code_name
            interaction = str(interaction_type or "talk").strip().lower()
            gift_id = str(gift_item_id or "").strip()
            score = 0
            score += int(charisma or 0) // 15
            score += int(Friends.get(name, 0) or 0) // 4
            score += int(self.var.get("trust", 0) or 0) // 3
            score += int(sluttiness.get(name, 0) or 0) // 10

            if str(player_state().appearance.current_dress or "") == "thiefdress":
                score += 1

            if interaction == "flirt":
                score += 2
                score -= int(FlirtedToday.get(name, 0) or 0) * 3
            elif interaction == "gift":
                score += 1
                score -= int(GiftedToday.get(name, 0) or 0) * 3
                if gift_id == "werecat_caught_cat":
                    score += 4
                elif gift_id in tuple(preferred_gift_item_ids(name)):
                    score += 3
                elif gift_id != "":
                    score -= 2
            else:
                score -= int(TalkedToday.get(name, 0) or 0) * 2

            roll_key = "%s_social_%s_%s_%s_%s" % (name, interaction, gift_id, int(dayspassed or 0), int(Talked.get(name, 0) or 0))
            score += procedural_randint(-2, 2, roll_key)

            if score >= 7:
                return "positive"
            if score >= 4:
                return "neutral"
            return "negative"

        def apply_result_counters(self, result_code):
            result_key = str(result_code or "neutral").strip().lower()
            self.var["lastsocial"] = result_key
            self.var[result_key] = int(self.var.get(result_key, 0) or 0) + 1
            return result_key

        def apply_social_result(self, interaction_type="talk", gift_item_id=""):
            name = self.code_name
            interaction = str(interaction_type or "talk").strip().lower()
            gift_id = str(gift_item_id or "").strip()
            result_key = self.social_outcome(interaction, gift_id)

            if interaction == "talk":
                Talked[name] = int(Talked.get(name, 0) or 0) + 1
                TalkedToday[name] = int(TalkedToday.get(name, 0) or 0) + 1
            elif interaction == "flirt":
                Talked[name] = int(Talked.get(name, 0) or 0) + 1
                FlirtedToday[name] = int(FlirtedToday.get(name, 0) or 0) + 1
                self.var["flirt"] = int(self.var.get("flirt", 0) or 0) + 1
            elif interaction == "gift":
                Talked[name] = int(Talked.get(name, 0) or 0) + 1
                GiftedToday[name] = int(GiftedToday.get(name, 0) or 0) + 1

            if result_key == "positive":
                Friends[name] = min(20, int(Friends.get(name, 0) or 0) + (2 if interaction == "gift" else 1))
                self.var["trust"] = min(20, int(self.var.get("trust", 0) or 0) + 1)
                if interaction == "flirt":
                    sluttiness[name] = min(100, int(sluttiness.get(name, 0) or 0) + 1)
            elif result_key == "negative":
                Friends[name] = max(0, int(Friends.get(name, 0) or 0) - (1 if interaction == "flirt" else 0))
                self.var["trust"] = max(0, int(self.var.get("trust", 0) or 0) - 1)

            self.rel = int(Friends.get(name, self.rel) or 0)
            self.relationship = self.rel
            self.trust = int(self.var.get("trust", self.trust) or 0)
            self.talked_today = int(TalkedToday.get(name, 0) or 0)
            self.flirted_today = int(FlirtedToday.get(name, 0) or 0)
            self.gifted_today = int(GiftedToday.get(name, 0) or 0)
            self.corruption = int(sluttiness.get(name, self.corruption) or 0)
            Friends["Clara"] = Friends[name]
            Talked["Clara"] = Talked[name]
            self.apply_result_counters(result_key)
            return result_key

        def sync_from_clara_maps(self):
            self.rel = people_to_int(Friends.get("clara", self.rel), self.rel)
            self.relationship = self.rel
            self.openness = people_to_int(otkroven.get("clara", self.openness), self.openness)
            self.corruption = people_to_int(sluttiness.get("clara", self.corruption), self.corruption)
            self.drunk = people_to_int(Drunk.get("clara", self.drunk), self.drunk)
            self.talked_today = people_to_int(TalkedToday.get("clara", self.talked_today), self.talked_today)
            self.flirted_today = people_to_int(FlirtedToday.get("clara", self.flirted_today), self.flirted_today)
            self.gifted_today = people_to_int(GiftedToday.get("clara", self.gifted_today), self.gifted_today)
            self.asked_today = people_to_int(AskedToday.get("clara", self.asked_today), self.asked_today)
            self.fucked_today = people_to_int(FuckedToday.get("clara", self.fucked_today), self.fucked_today)
            for table, stat_key in [
                (kids, "kids"),
                (beauty, "beauty"),
                (sexacts, "sexacts"),
                (cuminside, "cuminside"),
                (pregnancy, "pregnancy"),
                (pregfather, "pregfather"),
                (ConceptionChance, "ConceptionChance"),
                (PussyWetStart, "PussyWetStart"),
                (virginity, "virginity"),
                (Breastfeed, "breastfeed"),
            ]:
                if "clara" in table:
                    self.stats[stat_key] = table.get("clara")
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                if "clara" in table:
                    self.jobs[job_key] = table.get("clara")
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                if "clara" in table:
                    self.skills[skill_key] = table.get("clara")
            self.ensure_story_defaults()
            return self

        def sync_clara_maps(self):
            name = self.code_name
            knowsMC[name] = bool(self.known)
            RealName[name] = self.data.fullname
            RealName2[name] = self.data.genitive
            RealName3[name] = self.data.dative
            age_girls[name] = people_to_int(self.age, 19)
            DateOfBirth[name] = dict(self.data.birth_date)
            girltextdesc[name] = self.data.description
            Friends[name] = people_to_int(self.rel, 0)
            otkroven[name] = people_to_int(self.openness, 0)
            sluttiness[name] = people_to_int(self.corruption, 0)
            Drunk[name] = people_to_int(self.drunk, 0)
            Talked[name] = people_to_int(Talked.get(name, 0), 0)
            TalkedToday[name] = people_to_int(self.talked_today, 0)
            FlirtedToday[name] = people_to_int(self.flirted_today, 0)
            GiftedToday[name] = people_to_int(self.gifted_today, 0)
            AskedToday[name] = people_to_int(self.asked_today, 0)
            FuckedToday[name] = people_to_int(self.fucked_today, 0)
            CurrentLoc[name] = str(self.current_location or "WineStore")
            GiftPreferences[name] = list(self.gift_preferences)
            dressdefault[name] = self.wardrobe["current_dress"]
            bradef[name] = self.wardrobe["current_underwear"]["bra"]
            pantiesdef[name] = self.wardrobe["current_underwear"]["panties"]
            legsdef[name] = self.wardrobe["current_underwear"]["legs"]
            shoesdef[name] = self.wardrobe["current_underwear"]["shoes"]
            for table, stat_key in [
                (kids, "kids"),
                (beauty, "beauty"),
                (sexacts, "sexacts"),
                (cuminside, "cuminside"),
                (pregnancy, "pregnancy"),
                (pregfather, "pregfather"),
                (ConceptionChance, "ConceptionChance"),
                (PussyWetStart, "PussyWetStart"),
                (virginity, "virginity"),
                (Breastfeed, "breastfeed"),
            ]:
                table[name] = self.stats.get(stat_key)
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                table[name] = self.skills.get(skill_key, 0)

            # Uppercase legacy references still read these keys in old content.
            Friends["Clara"] = Friends[name]
            Talked["Clara"] = Talked[name]
            self.ensure_story_defaults()
            return self

        def initialize_new_game_state(self):
            self.var = ClaraVar
            self.ensure_story_defaults()
            self.prepare_daily_event_rolls()
            self.sync_clara_maps()
            return self

        def prepare_daily_event_rolls(self):
            day_value = int(dayspassed or 0)
            week_value = int(week or 0)
            if int(self.var.get("market_day_roll_day", -1) or -1) != day_value:
                self.var["market_day_roll_day"] = day_value
                if week_value == 7:
                    self.var["market_day_roll"] = 0
                else:
                    self.var["market_day_roll"] = 1 if procedural_randint(1, 2, "clara_market_day_%s_%s" % (day_value, week_value)) == 1 else 0
            if int(self.var.get("market_evening_roll_day", -1) or -1) != day_value:
                self.var["market_evening_roll_day"] = day_value
                if week_value in (5, 7):
                    self.var["market_evening_roll"] = 0
                else:
                    self.var["market_evening_roll"] = 1 if procedural_randint(1, 3, "clara_market_evening_%s_%s" % (day_value, week_value)) == 1 else 0
            return self.var

        def reset_daily(self, full=False):
            super(ClaraInfo, self).reset_daily(full)
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.sync_clara_maps()
            return self

        def install_schedule(self):
            name = self.code_name
            npc_interval_schedule_load_file(name)
            npc_schedule_sync_currentloc(name)
            return self

define ClaraStaticData = ClaraData()
default Clara = ClaraInfo()

label InitClara:
    python:
        GirlName = Clara.code_name
        peopleData[GirlName] = ClaraStaticData
        Clara.var = ClaraVar
        Clara.initialize_new_game_state()
        peopleInfo[GirlName] = Clara
        if Clara not in girls:
            girls.append(Clara)
        bodymodel_sync_character(GirlName, RealName[GirlName], "female")
        Clara.install_schedule()

    return
