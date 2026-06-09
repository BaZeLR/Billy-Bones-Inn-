# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitSandra:
    python:
        knowsMC["sandra"] = True
        # Initialize Sandra's attributes
        GirlName = 'sandra'

        RealName[GirlName] = 'Сандра'
        RealName2[GirlName] = 'Сандры'
        RealName3[GirlName] = 'Сандре'
        age_girls[GirlName] = 34
        kids[GirlName] = 3
        beauty[GirlName] = 65
        sluttiness[GirlName] = 20
        sexacts[GirlName] = 4352
        cuminside[GirlName] = 2593
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 5
        CurrentLoc[GirlName] = 'TavernMain'
        PussyWetStart[GirlName] = 20
        virginity[GirlName] = False

        # Description and default dress
        girltextdesc[GirlName] = 'Сандра - женщина в самом соку. У нее темные волосы, зеленые глаза и грудь размера DD.'
        dressdefault[GirlName] = 'workdresszhilet'

        # Default clothing
        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = ''
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 90
        cleaning[GirlName] = 70
        waitress[GirlName] = 20

        # Job-related data
        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 1
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        Friends[GirlName] = 5
        jobHallAvail[GirlName] = 1
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        # Custom variables
        for key, value in sandra_story_defaults().items():
            SandraVar.setdefault(key, value)
        GiftPreferences[GirlName] = ["soap_001", "wild_rose_001", "lavender_001", "berries_001", "mushroom_001", "honey_comb_001", "energy_tea_001", "drink_ale_001"]
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[6, 7], awake=True, talkable=True, condition=npc_schedule_rule("sandra_night_thanks_ready"), priority=380, label="night_thanks"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernMain", mode="morning"), priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernKitchen", mode="morning"), priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernStorage", mode="morning"), priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="Backyard", mode="morning"), priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernSandraRoom", mode="morning"), priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_kitchen"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="FridayDance", mode="friday_evening"), priority=250, label="friday_dance"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernSandraRoom", mode="friday_evening"), priority=240, label="friday_room"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernSandraRoom", mode="sunday"), priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="Backyard", mode="sunday"), priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernMain", mode="sunday"), priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernKitchen", mode="sunday"), priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_sync_currentloc(GirlName)
        peopleData["sandra"] = SandraStaticData
        Sandra.var = SandraVar
        Sandra.ensure_story_defaults()
        Sandra.sync_from_maps()
        Sandra.sync_from_sandra_maps()
        Sandra.update()
        peopleInfo["sandra"] = Sandra
        if Sandra not in girls:
            girls.append(Sandra)

    return

init python:
    def sandra_story_defaults():
        return {
            "knowmolodost": 0,
            "WeeklyChoreCheckScore": 0,
            "WeeklyChoreCheckCounter": 0,
            "Week5WakePending": 0,
            "WeeklyChoreCheckEval": "",
            "RoomUnlocked": 0,
            "MCVisitFirstReady": 0,
            "MCVisitFirstPending": 0,
            "MCVisitFirstDone": 0,
            "FinalRewardDone": 0,
            "NightThanksReady": 0,
            "NightThanksLastDay": -1,
            "SandraSex": 0,
            "revealing_dress_ordered": 0,
            "revealing_dress_code": "",
            "revealing_dress_initiative_seen": 0,
            "MaidRevengeEnding": 0,
        }

    class SandraData(PeopleData):
        code_name = "sandra"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Сандра",
                fullname="Сандра",
                genitive="Сандры",
                dative="Сандре",
                description="Сандра - женщина в самом соку. У нее темные волосы, зеленые глаза и грудь размера DD.",
            )
            self.birth_date = {"day": 1, "period": 1, "cycle": 1066}
            self.card_image = "images/sandra/sandra_card.jpg"
            self.schedule_source = "schedules/sandra.json"

    class SandraInfo(Girl):
        """Sandra runtime: household authority, chore rewards, room access."""
        def __init__(self):
            super().__init__("sandra")
            self.code_name = "sandra"
            self.data = SandraStaticData
            self.age = 34
            self.rel = 5
            self.relationship = self.rel
            self.openness = 0
            self.corruption = 20
            self.known = True

            # Energy gates work, social response, and recovery.
            self.energy = 100
            self.energy_max = 100

            # Rebellion is resistance to player authority or household discipline.
            self.rebellion = 0

            # Anger is direct resentment toward the player.
            self.anger_with_player = 0

            # Fun is short-term appetite for relief, warmth, and playful response.
            self.fun = 0

            # Trust offsets fear and makes softer reactions possible.
            self.trust = 0

            # Fear is hidden risk pressure from MC behavior and tavern instability.
            self.fear = 0

            # Mana is the hidden personal reaction field.
            self.mana = 10
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
                "last_energy_state": "normal",
                "last_sick_state": "",
                "last_food_quality": "",
                "last_beauty_state": "normal",
                "pending_decision": "",
            }
            self.weekly_chore_score = 0
            self.weekly_chore_counter = 0
            self.weekly_chore_eval = ""
            self.weekly_wake_pending = 0
            self.weekly_wake_num = 0
            self.room_unlocked_flag = 0
            self.mc_visit_first_ready = 0
            self.mc_visit_first_pending = 0
            self.mc_visit_first_done = 0
            self.final_reward_flag = 0
            self.night_thanks_ready_flag = 0
            self.night_thanks_last_day = -1
            self.sandraSex = False
            self.mana_reaction_table = {
                "very_low": {"min": 0, "max": 9, "reaction": "dismissive_mocking", "visible_effect": "no_aura", "behavior": "ignore_or_insult"},
                "low": {"min": 10, "max": 29, "reaction": "neutral_cautious", "visible_effect": "faint_aura", "behavior": "normal_interactions"},
                "medium": {"min": 30, "max": 59, "reaction": "respectful_interested", "visible_effect": "visible_glow", "behavior": "better_prices_more_dialogue"},
                "high": {"min": 60, "max": 84, "reaction": "awe_fear_admiration", "visible_effect": "strong_aura", "behavior": "offer_quests_or_fear"},
                "very_high": {"min": 85, "max": 100, "reaction": "worship_terror_obsession", "visible_effect": "overwhelming_aura", "behavior": "extreme_reactions"},
                "corrupted": {"min": 0, "max": 100, "reaction": "hostility_hatred_madness", "visible_effect": "dark_corrupted_aura", "behavior": "attack_or_run"},
            }

            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0

            self.stats = {
                "kids": 3,
                "beauty": 65,
                "sexacts": 4352,
                "cuminside": 2593,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 5,
                "PussyWetStart": 20,
                "virginity": False,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 90,
                "cleaning": 70,
                "waitress": 20,
            }
            self.jobs = {
                "jobkitchen": 1,
                "jobcleaning": 0,
                "jobwaitress": 0,
                "jobHallAvail": 1,
                "jobWhoreAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
            }
            self.gift_preferences = ["soap_001", "wild_rose_001", "lavender_001", "berries_001", "mushroom_001", "honey_comb_001", "energy_tea_001", "drink_ale_001"]
            self.schedule_source = SandraStaticData.schedule_source
            self.schedule_uses_clock_minutes = True
            self.current_location = "TavernMain"
            self.talk_preferences = {
                "favorite_topics": ["job_routine", "food", "money", "family_life", "fashion"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["workdresszhilet", "simplebra", "simplepanties", "simpleshoes"],
                "gifted": [],
                "current_dress": "workdresszhilet",
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
            super(SandraInfo, self).update()
            self.data = SandraStaticData
            self.relationship = self.rel
            self.sync_from_sandra_maps()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in sandra_story_defaults().items():
                self.var.setdefault(key, value)
            self.weekly_chore_score = people_to_int(self.var.get("WeeklyChoreCheckScore", self.weekly_chore_score), self.weekly_chore_score)
            self.weekly_chore_counter = people_to_int(self.var.get("WeeklyChoreCheckCounter", self.weekly_chore_counter), self.weekly_chore_counter)
            self.weekly_chore_eval = str(self.var.get("WeeklyChoreCheckEval", self.weekly_chore_eval) or "")
            self.weekly_wake_pending = people_to_int(self.var.get("Week5WakePending", self.weekly_wake_pending), self.weekly_wake_pending)
            self.room_unlocked_flag = people_to_int(self.var.get("RoomUnlocked", self.room_unlocked_flag), self.room_unlocked_flag)
            self.mc_visit_first_ready = people_to_int(self.var.get("MCVisitFirstReady", self.mc_visit_first_ready), self.mc_visit_first_ready)
            self.mc_visit_first_pending = people_to_int(self.var.get("MCVisitFirstPending", self.mc_visit_first_pending), self.mc_visit_first_pending)
            self.mc_visit_first_done = people_to_int(self.var.get("MCVisitFirstDone", self.mc_visit_first_done), self.mc_visit_first_done)
            self.final_reward_flag = people_to_int(self.var.get("FinalRewardDone", self.final_reward_flag), self.final_reward_flag)
            self.night_thanks_ready_flag = people_to_int(self.var.get("NightThanksReady", self.night_thanks_ready_flag), self.night_thanks_ready_flag)
            self.night_thanks_last_day = people_to_int(self.var.get("NightThanksLastDay", self.night_thanks_last_day), self.night_thanks_last_day)
            self.sandraSex = bool(people_to_int(self.var.get("SandraSex", 1 if self.sandraSex else 0), 0))
            return self.var

        def save_story_state(self):
            if not isinstance(self.var, dict):
                self.var = {}
            self.var["WeeklyChoreCheckScore"] = max(0, people_to_int(self.weekly_chore_score, 0))
            self.var["WeeklyChoreCheckCounter"] = max(0, people_to_int(self.weekly_chore_counter, 0))
            self.var["WeeklyChoreCheckEval"] = str(self.weekly_chore_eval or "")
            self.var["Week5WakePending"] = max(0, people_to_int(self.weekly_wake_pending, 0))
            self.var["RoomUnlocked"] = max(0, people_to_int(self.room_unlocked_flag, 0))
            self.var["MCVisitFirstReady"] = max(0, people_to_int(self.mc_visit_first_ready, 0))
            self.var["MCVisitFirstPending"] = max(0, people_to_int(self.mc_visit_first_pending, 0))
            self.var["MCVisitFirstDone"] = max(0, people_to_int(self.mc_visit_first_done, 0))
            self.var["FinalRewardDone"] = max(0, people_to_int(self.final_reward_flag, 0))
            self.var["NightThanksReady"] = max(0, people_to_int(self.night_thanks_ready_flag, 0))
            self.var["NightThanksLastDay"] = people_to_int(self.night_thanks_last_day, -1)
            self.var["SandraSex"] = 1 if self.sandraSex else 0
            return self.var

        def sync_from_sandra_maps(self):
            self.rel = people_to_int(people_get_map("Friends").get("sandra", self.rel), self.rel)
            self.relationship = self.rel
            self.openness = people_to_int(people_get_map("otkroven").get("sandra", self.openness), self.openness)
            self.corruption = people_to_int(people_get_map("sluttiness").get("sandra", self.corruption), self.corruption)
            self.drunk = people_to_int(people_get_map("Drunk").get("sandra", self.drunk), self.drunk)
            self.talked_today = people_to_int(people_get_map("TalkedToday").get("sandra", self.talked_today), self.talked_today)
            self.flirted_today = people_to_int(people_get_map("FlirtedToday").get("sandra", self.flirted_today), self.flirted_today)
            self.gifted_today = people_to_int(people_get_map("GiftedToday").get("sandra", self.gifted_today), self.gifted_today)
            self.asked_today = people_to_int(people_get_map("AskedToday").get("sandra", self.asked_today), self.asked_today)
            self.fucked_today = people_to_int(people_get_map("FuckedToday").get("sandra", self.fucked_today), self.fucked_today)
            for map_name, stat_key in [
                ("kids", "kids"),
                ("beauty", "beauty"),
                ("sexacts", "sexacts"),
                ("cuminside", "cuminside"),
                ("pregnancy", "pregnancy"),
                ("pregfather", "pregfather"),
                ("ConceptionChance", "ConceptionChance"),
                ("PussyWetStart", "PussyWetStart"),
                ("virginity", "virginity"),
                ("Breastfeed", "breastfeed"),
            ]:
                table = people_get_map(map_name)
                if "sandra" in table:
                    self.stats[stat_key] = table.get("sandra")
            for map_name, job_key in [
                ("jobkitchen", "jobkitchen"),
                ("jobcleaning", "jobcleaning"),
                ("jobwaitress", "jobwaitress"),
                ("jobHallAvail", "jobHallAvail"),
                ("jobWhoreAvail", "jobWhoreAvail"),
                ("jobwhore", "jobwhore"),
                ("jobgloryhole", "jobgloryhole"),
            ]:
                table = people_get_map(map_name)
                if "sandra" in table:
                    self.jobs[job_key] = table.get("sandra")
            for map_name, skill_key in [("cooking", "cooking"), ("cleaning", "cleaning"), ("waitress", "waitress")]:
                table = people_get_map(map_name)
                if "sandra" in table:
                    self.skills[skill_key] = table.get("sandra")
            self.ensure_story_defaults()
            return self

        def sync_sandra_maps(self):
            people_get_map("Friends")["sandra"] = people_to_int(self.rel, 0)
            people_get_map("otkroven")["sandra"] = people_to_int(self.openness, 0)
            people_get_map("sluttiness")["sandra"] = people_to_int(self.corruption, 0)
            people_get_map("Drunk")["sandra"] = people_to_int(self.drunk, 0)
            people_get_map("TalkedToday")["sandra"] = people_to_int(self.talked_today, 0)
            people_get_map("FlirtedToday")["sandra"] = people_to_int(self.flirted_today, 0)
            people_get_map("GiftedToday")["sandra"] = people_to_int(self.gifted_today, 0)
            people_get_map("AskedToday")["sandra"] = people_to_int(self.asked_today, 0)
            people_get_map("FuckedToday")["sandra"] = people_to_int(self.fucked_today, 0)
            for map_name, stat_key in [
                ("kids", "kids"),
                ("beauty", "beauty"),
                ("sexacts", "sexacts"),
                ("cuminside", "cuminside"),
                ("pregnancy", "pregnancy"),
                ("pregfather", "pregfather"),
                ("ConceptionChance", "ConceptionChance"),
                ("PussyWetStart", "PussyWetStart"),
                ("virginity", "virginity"),
                ("Breastfeed", "breastfeed"),
            ]:
                people_get_map(map_name)["sandra"] = self.stats.get(stat_key)
            for map_name, job_key in [
                ("jobkitchen", "jobkitchen"),
                ("jobcleaning", "jobcleaning"),
                ("jobwaitress", "jobwaitress"),
                ("jobHallAvail", "jobHallAvail"),
                ("jobWhoreAvail", "jobWhoreAvail"),
                ("jobwhore", "jobwhore"),
                ("jobgloryhole", "jobgloryhole"),
            ]:
                people_get_map(map_name)["sandra"] = self.jobs.get(job_key, 0)
            for map_name, skill_key in [("cooking", "cooking"), ("cleaning", "cleaning"), ("waitress", "waitress")]:
                people_get_map(map_name)["sandra"] = self.skills.get(skill_key, 0)
            return self

        def reset_daily(self, full=False):
            super(SandraInfo, self).reset_daily(full)
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.sync_sandra_maps()
            return self

        def story_value(self, key, default=0):
            flags = self.ensure_story_defaults()
            return flags.get(key, default)

        def set_story_value(self, key, value):
            flags = self.ensure_story_defaults()
            flags[key] = value
            return value

        def first_month_passed(self):
            try:
                return int(dayspassed or 0) >= 30
            except Exception:
                return False

        def final_reward_done(self):
            try:
                self.ensure_story_defaults()
                return int(self.final_reward_flag or 0) > 0
            except Exception:
                return False

        def room_unlocked(self):
            try:
                self.ensure_story_defaults()
                return int(self.room_unlocked_flag or 0) > 0
            except Exception:
                return False

        def night_thanks_ready(self):
            try:
                self.ensure_story_defaults()
                return int(self.night_thanks_ready_flag or 0) > 0
            except Exception:
                return False

        def mana_profile(self):
            if self.mana_corrupted:
                return self.mana_reaction_table["corrupted"]
            value = max(0, min(100, people_to_int(self.mana, 0)))
            for level in ["very_low", "low", "medium", "high", "very_high"]:
                row = self.mana_reaction_table[level]
                if row["min"] <= value <= row["max"]:
                    return row
            return self.mana_reaction_table["low"]

        def change_mana(self, amount, reason=""):
            before = people_to_int(self.mana, 0)
            self.mana = max(0, min(100, before + people_to_int(amount, 0)))
            self.reaction_state["last_mana_delta"] = self.mana - before
            self.reaction_state["last_mana_reasons"] = [reason] if reason else []
            return self.mana

        def change_fear(self, amount, reason=""):
            before = people_to_int(self.fear, 0)
            self.fear = max(0, min(100, before + people_to_int(amount, 0)))
            return self.fear

        def daily_mana_update(self, context=None):
            context = dict(context or {})
            delta = 0
            reasons = []
            if context.get("comfortable_sleep", False):
                delta += 2
                reasons.append("comfortable_sleep")
            if context.get("good_food_quality", False):
                delta += 2
                reasons.append("good_food_quality")
            if context.get("clean_tavern", False):
                delta += 1
                reasons.append("clean_tavern")
            if context.get("wood_stock_ok", False):
                delta += 1
                reasons.append("wood_stock_ok")
            if context.get("food_stock_ok", False):
                delta += 1
                reasons.append("food_stock_ok")
            if context.get("sick", False):
                delta -= 3
                reasons.append("sick")
            if people_to_int(self.energy, 0) < 25:
                delta -= 2
                reasons.append("low_energy")
            if context.get("bad_food_quality", False):
                delta -= 2
                reasons.append("bad_food_quality")
            if context.get("dirty_tavern", False):
                delta -= 2
                reasons.append("dirty_tavern")
            if context.get("wood_stock_low", False):
                delta -= 2
                reasons.append("wood_stock_low")
            if context.get("food_stock_low", False):
                delta -= 2
                reasons.append("food_stock_low")
            if delta == 0:
                if people_to_int(self.mana, 0) > 30:
                    delta = -1
                    reasons.append("daily_fade_high")
                elif people_to_int(self.mana, 0) < 30:
                    delta = 1
                    reasons.append("daily_fade_low")
            before = people_to_int(self.mana, 0)
            self.mana = max(0, min(100, before + delta))
            self.reaction_state["last_mana_delta"] = self.mana - before
            self.reaction_state["last_mana_reasons"] = reasons
            return self.mana

        def reaction_score(self, base_score=0, context=None):
            context = dict(context or {})
            score = people_to_int(base_score, 0)
            score += people_to_int(self.mana, 0) // 20
            score += people_to_int(self.rel, 0) // 25
            score += people_to_int(self.trust, 0) // 20
            score -= people_to_int(self.anger_with_player, 0) // 20
            score -= people_to_int(self.rebellion, 0) // 25
            score -= people_to_int(self.fear, 0) // 20
            if people_to_int(self.energy, 0) < 25:
                score -= 2
            if context.get("sick", False):
                score -= 3
            if context.get("horny", False):
                score += 2
            self.reaction_state["last_reaction_score"] = score
            return score

        def weekly_report_finished(self, score=0, evaluation="", counter=None, wake_pending=None, visit_first_ready=None, visit_first_pending=None, friend_value=None):
            self.ensure_story_defaults()
            result = str(evaluation or "").strip().lower()
            self.weekly_chore_score = max(0, people_to_int(score, 0))
            self.weekly_chore_eval = result
            if counter is not None:
                self.weekly_chore_counter = max(0, people_to_int(counter, 0))
            if wake_pending is not None:
                self.weekly_wake_pending = max(0, people_to_int(wake_pending, 0))
            if visit_first_ready is not None:
                self.mc_visit_first_ready = max(0, people_to_int(visit_first_ready, 0))
            if visit_first_pending is not None:
                self.mc_visit_first_pending = max(0, people_to_int(visit_first_pending, 0))
            if friend_value is not None:
                self.rel = max(0, min(20, people_to_int(friend_value, self.rel)))
                self.relationship = self.rel
            if self.weekly_wake_pending:
                self.weekly_wake_num = max(0, min(people_to_int(self.weekly_chore_counter, 0) - 1, 3))
            if result == "good":
                self.change_mana(3, "weekly_check_good")
                self.change_fear(-5, "weekly_check_good")
                self.trust = max(0, min(100, people_to_int(self.trust, 0) + 3))
            elif result == "bad":
                self.change_mana(-3, "weekly_check_bad")
                self.change_fear(5, "weekly_check_bad")
                if people_to_int(self.anger_with_player, 0) > 40:
                    self.rebellion = max(0, min(100, people_to_int(self.rebellion, 0) + 2))
            self.save_story_state()
            self.sync_sandra_maps()
            return self.var

        def weekly_thanks_wake_seen(self, step_index=0, gains=None):
            self.ensure_story_defaults()
            step = max(0, people_to_int(step_index, 0))
            gains = dict(gains or {})
            self.weekly_wake_pending = 0
            self.room_unlocked_flag = 1
            self.night_thanks_ready_flag = 1 if step >= 3 else 0
            if step == 0:
                self.mc_visit_first_ready = 1
                self.mc_visit_first_done = 1
            self.mc_visit_first_pending = 0
            self.rel = max(0, min(20, people_to_int(self.rel, 0) + people_to_int(gains.get("friends", 0), 0)))
            self.relationship = self.rel
            self.openness = max(0, min(20, people_to_int(self.openness, 0) + people_to_int(gains.get("otkroven", 0), 0)))
            self.corruption = max(0, min(100, people_to_int(self.corruption, 0) + people_to_int(gains.get("sluttiness", 0), 0)))
            self.save_story_state()
            self.sync_sandra_maps()
            return self.var

        def night_thanks_seen(self):
            self.ensure_story_defaults()
            self.night_thanks_ready_flag = 0
            try:
                self.night_thanks_last_day = int(dayspassed or 0)
            except Exception:
                self.night_thanks_last_day = 0
            self.mc_visit_first_done = 1
            self.final_reward_flag = 1
            self.room_unlocked_flag = 1
            self.sandraSex = True
            self.rel = max(0, min(20, people_to_int(self.rel, 0) + 2))
            self.relationship = self.rel
            self.openness = max(0, min(20, people_to_int(self.openness, 0) + 2))
            self.corruption = max(0, min(100, people_to_int(self.corruption, 0) + 3))
            self.save_story_state()
            self.sync_sandra_maps()
            return self.var

        def weekly_thanks_event_ready(self):
            self.ensure_story_defaults()
            return bool(self.weekly_wake_pending)

        def weekly_thanks_target_label(self):
            if not self.weekly_thanks_event_ready():
                return ""
            return "sandraWeeklyEvaluation_%d" % max(0, min(people_to_int(self.weekly_wake_num, 0), 3))

        def sex_available(self):
            self.ensure_story_defaults()
            return bool(self.sandraSex or self.final_reward_flag)

        def social_action_allowed(self, action="", item_id=""):
            action_key = str(action or "").strip().lower()
            if action_key in ("talk", "flirt", "gift", "share"):
                if not self.first_month_passed() or not self.final_reward_done():
                    return False
            return super(SandraInfo, self).social_action_allowed(action_key, item_id)

define SandraStaticData = SandraData()
default Sandra = SandraInfo()
