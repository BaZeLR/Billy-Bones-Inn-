        npc_schedule_sync_currentloc(GirlName)            girl.relationship = girl.rel            self.current_location = "TavernMain"        def story_value(self, key, default=0):
            flags = self.ensure_story_defaults()
            return flags.get(key, default)

        def set_story_value(self, key, value):
            flags = self.ensure_story_defaults()
            flags[key] = value
            return value
            self.schedule_source = SandraStaticData.schedule_source            self.schedule_source = SandraStaticData.schedule_source
            self.current_location = "TavernMain"            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel                self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel        npc_schedule_sync_currentloc(GirlName)            girl.relationship = girl.rel            self.current_location = "TavernMain"        def story_value(self, key, default=0):
            flags = self.ensure_story_defaults()
            return flags.get(key, default)

        def set_story_value(self, key, value):
            flags = self.ensure_story_defaults()
            flags[key] = value
            return value
            self.schedule_source = SandraStaticData.schedule_source            self.schedule_source = SandraStaticData.schedule_source
            self.current_location = "TavernMain"            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel                self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel        npc_schedule_sync_currentloc(GirlName)            girl.relationship = girl.rel            self.current_location = "TavernMain"        def story_value(self, key, default=0):
            flags = self.ensure_story_defaults()
            return flags.get(key, default)

        def set_story_value(self, key, value):
            flags = self.ensure_story_defaults()
            flags[key] = value
            return value
            self.schedule_source = SandraStaticData.schedule_source            self.schedule_source = SandraStaticData.schedule_source
            self.current_location = "TavernMain"            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel                self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def sandra_schedule_match(location="", mode="morning"):
        target = str(location or "").strip()
        mode_key = str(mode or "morning").strip().lower()
        if mode_key == "morning":
            return str(_tavern_household_preopening_location("sandra") or "") == target
        if mode_key == "sunday":
            return str(_tavern_household_sunday_location("sandra") or "") == target
        if mode_key == "friday_evening":
            return str(_tavern_household_friday_evening_location("sandra") or "") == target
        return False

    def sandra_schedule_night_thanks_ready():
        return int(Sandra.night_thanks_ready_flag or 0) > 0 and int(Sandra.night_thanks_last_day or -1) != int(dayspassed or 0)

    def sandra_schedule_morning_hall():
        return sandra_schedule_match("TavernMain", "morning")

    def sandra_schedule_morning_kitchen():
        return sandra_schedule_match("TavernKitchen", "morning")

    def sandra_schedule_morning_storage():
        return sandra_schedule_match("TavernStorage", "morning")

    def sandra_schedule_morning_backyard():
        return sandra_schedule_match("Backyard", "morning")

    def sandra_schedule_morning_room():
        return sandra_schedule_match("TavernSandraRoom", "morning")

    def sandra_schedule_friday_dance():
        return sandra_schedule_match("FridayDance", "friday_evening")

    def sandra_schedule_friday_room():
        return sandra_schedule_match("TavernSandraRoom", "friday_evening")

    def sandra_schedule_sunday_room():
        return sandra_schedule_match("TavernSandraRoom", "sunday")

    def sandra_schedule_sunday_backyard():
        return sandra_schedule_match("Backyard", "sunday")

    def sandra_schedule_sunday_hall():
        return sandra_schedule_match("TavernMain", "sunday")

    def sandra_schedule_sunday_kitchen():
        return sandra_schedule_match("TavernKitchen", "sunday")

init python:
    def sandra_schedule_match(location="", mode="morning"):
        target = str(location or "").strip()
        mode_key = str(mode or "morning").strip().lower()
        if mode_key == "morning":
            return str(_tavern_household_preopening_location("sandra") or "") == target
        if mode_key == "sunday":
            return str(_tavern_household_sunday_location("sandra") or "") == target
        if mode_key == "friday_evening":
            return str(_tavern_household_friday_evening_location("sandra") or "") == target
        return False

    def sandra_schedule_night_thanks_ready():
        return int(Sandra.night_thanks_ready_flag or 0) > 0 and int(Sandra.night_thanks_last_day or -1) != int(dayspassed or 0)

    def sandra_schedule_morning_hall():
        return sandra_schedule_match("TavernMain", "morning")

    def sandra_schedule_morning_kitchen():
        return sandra_schedule_match("TavernKitchen", "morning")

    def sandra_schedule_morning_storage():
        return sandra_schedule_match("TavernStorage", "morning")

    def sandra_schedule_morning_backyard():
        return sandra_schedule_match("Backyard", "morning")

    def sandra_schedule_morning_room():
        return sandra_schedule_match("TavernSandraRoom", "morning")

    def sandra_schedule_friday_dance():
        return sandra_schedule_match("FridayDance", "friday_evening")

    def sandra_schedule_friday_room():
        return sandra_schedule_match("TavernSandraRoom", "friday_evening")

    def sandra_schedule_sunday_room():
        return sandra_schedule_match("TavernSandraRoom", "sunday")

    def sandra_schedule_sunday_backyard():
        return sandra_schedule_match("Backyard", "sunday")

    def sandra_schedule_sunday_hall():
        return sandra_schedule_match("TavernMain", "sunday")

    def sandra_schedule_sunday_kitchen():
        return sandra_schedule_match("TavernKitchen", "sunday")

init python:
    def sandra_schedule_match(location="", mode="morning"):
        target = str(location or "").strip()
        mode_key = str(mode or "morning").strip().lower()
        if mode_key == "morning":
            return str(_tavern_household_preopening_location("sandra") or "") == target
        if mode_key == "sunday":
            return str(_tavern_household_sunday_location("sandra") or "") == target
        if mode_key == "friday_evening":
            return str(_tavern_household_friday_evening_location("sandra") or "") == target
        return False

    def sandra_schedule_night_thanks_ready():
        return int(Sandra.night_thanks_ready_flag or 0) > 0 and int(Sandra.night_thanks_last_day or -1) != int(dayspassed or 0)

    def sandra_schedule_morning_hall():
        return sandra_schedule_match("TavernMain", "morning")

    def sandra_schedule_morning_kitchen():
        return sandra_schedule_match("TavernKitchen", "morning")

    def sandra_schedule_morning_storage():
        return sandra_schedule_match("TavernStorage", "morning")

    def sandra_schedule_morning_backyard():
        return sandra_schedule_match("Backyard", "morning")

    def sandra_schedule_morning_room():
        return sandra_schedule_match("TavernSandraRoom", "morning")

    def sandra_schedule_friday_dance():
        return sandra_schedule_match("FridayDance", "friday_evening")

    def sandra_schedule_friday_room():
        return sandra_schedule_match("TavernSandraRoom", "friday_evening")

    def sandra_schedule_sunday_room():
        return sandra_schedule_match("TavernSandraRoom", "sunday")

    def sandra_schedule_sunday_backyard():
        return sandra_schedule_match("Backyard", "sunday")

    def sandra_schedule_sunday_hall():
        return sandra_schedule_match("TavernMain", "sunday")

    def sandra_schedule_sunday_kitchen():
        return sandra_schedule_match("TavernKitchen", "sunday")

label InitSandra:
    python:
        GirlName = Sandra.code_name
        Sandra.initialize_new_game_state()
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[6, 7], awake=True, talkable=True, condition=sandra_schedule_night_thanks_ready, priority=380, label="night_thanks"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_kitchen"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_room, priority=240, label="friday_room"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[6, 7], awake=True, talkable=True, condition=sandra_schedule_night_thanks_ready, priority=380, label="night_thanks"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_kitchen"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_room, priority=240, label="friday_room"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[6, 7], awake=True, talkable=True, condition=sandra_schedule_night_thanks_ready, priority=380, label="night_thanks"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_kitchen"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_room, priority=240, label="friday_room"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[6, 7], awake=True, talkable=True, condition=sandra_schedule_night_thanks_ready, priority=380, label="night_thanks"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=sandra_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_kitchen"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=sandra_schedule_friday_room, priority=240, label="friday_room"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=sandra_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        peopleData["sandra"] = SandraStaticData
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
            "harass_instruction": "",
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
        unknown_name = "Незнакомка"

        def __init__(self):
            super().__init__("sandra")
            self.code_name = "sandra"
            self.uses_own_var_state = True
            self.data = SandraStaticData
            self.rel = 5
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
            self.relationship_cap = 100
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
            self.name = self.code_name
            self.data = SandraStaticData
            self.ensure_story_defaults()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            self.save_story_state()
            return self.var.var.var.var.var.var.var.var.var.var.var.var.var.var.var.var.var.var

        def initialize_new_game_state(self):
            self.data = SandraStaticData
            self.known = True
            self.ensure_story_defaults()
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

        def story_value(self, key, default=0):
            flags = self.ensure_story_defaults()
            return flags.get(key, default)

        def set_story_value(self, key, value):
            flags = self.ensure_story_defaults()
            flags[key] = value
            return value

        def kitchen_can_discuss_household_food(self):
            self.update()
            return (
                str(getLocation(self.code_name) or "") == "TavernKitchen"
                and tavern_kitchen_food_stock_count() > 0
                and people_to_int(self.rel, 0) >= 5
                and people_to_int(self.asked_today, 0) == 0
            )

        def _add_household_relation(self, girl, amount=1):
            if girl is None:
                return
            try:
                girl.update()
            except Exception:
                pass
            girl.rel = max(0, min(20, people_to_int(getattr(girl, "rel", 0), 0) + people_to_int(amount, 0)))
            girl.fun = max(0, min(100, people_to_int(getattr(girl, "fun", 0), 0) + 1))

        def apply_kitchen_regular_breakfast_request(self, used_item_id=""):
            self.update()
            self.asked_today = people_to_int(self.asked_today, 0) + 1
            self.talked_today = people_to_int(self.talked_today, 0) + 1
            self.rel = min(20, people_to_int(self.rel, 0) + 1)
            self.fun = min(100, people_to_int(self.fun, 0) + 2)
            self.ensure_story_defaults()["kitchen_regular_breakfast_requests"] = people_to_int(self.var.get("kitchen_regular_breakfast_requests", 0), 0) + 1
            self._add_household_relation(Melissa, 1)
            self._add_household_relation(Amanda, 1)
            player.change_stat("fun", 2)
            return self.kitchen_regular_breakfast_text(used_item_id)

        def apply_kitchen_client_manners_request(self, used_item_id=""):
            self.update()
            self.asked_today = people_to_int(self.asked_today, 0) + 1
            self.talked_today = people_to_int(self.talked_today, 0) + 1
            self.rel = min(20, people_to_int(self.rel, 0) + 1)
            self.ensure_story_defaults()["kitchen_client_manners_requests"] = people_to_int(self.var.get("kitchen_client_manners_requests", 0), 0) + 1
            player.sync_from_store()
            player.economy.tavern_fame = people_to_int(player.economy.tavern_fame, 0) + 1
            player.economy.apply_to_store()
            return self.kitchen_client_manners_text(used_item_id)

        def apply_kitchen_tea_with_becky(self):
            self.update()
            player.remove_item("energy_tea_001", 1)
            self.rel = min(20, people_to_int(self.rel, 0) + 1)
            self.fun = min(100, people_to_int(self.fun, 0) + 1)
            self._add_household_relation(Becky, 1)
            player.change_stat("fun", 1)
            return "Вы завариваете бодрящий чай и угощаете им Сандру с Бекки. Разговор за столом быстро теплеет: Сандра благодарит вас за внимание к хозяйству, а Бекки охотно подхватывает кухонные сплетни и делится парой полезных замечаний о трактирных делах."

        def kitchen_regular_breakfast_text(self, used_item_id=""):
            text = "Вы просите Сандру почаще собирать домочадцев за общий утренний стол и не давать всем разбредаться без толку. Сандра выслушивает вас без лишних слов, потом переводит взгляд на оставленные припасы и кивает.\n\n\"Ладно. Если уж на кухне есть из чего готовить, я поговорю с девочками. Общий завтрак дому не повредит, а там и работа ровнее пойдет,\" решает она."
            if str(used_item_id or "").strip():
                text += "\nДля ближайшего такого стола Сандра сразу откладывает %s." % tavern_kitchen_food_item_name(used_item_id)
            return text

        def kitchen_client_manners_text(self, used_item_id=""):
            text = "Вы просите Сандру поговорить с домочадцами и держаться с гостями немного мягче обычного. Сандра щурится, явно взвешивая сказанное, а потом нехотя соглашается.\n\n\"Если уж хочешь, чтобы в трактире было больше довольных рож, я скажу девочкам не срываться на людях почем зря. Но и ты смотри, чтобы работа не шла через пень-колоду,\" бурчит она."
            if str(used_item_id or "").strip():
                text += "\nЗаодно Сандра решает пустить %s на что-нибудь поприятнее для посетителей." % tavern_kitchen_food_item_name(used_item_id)
            return text

        def first_month_passed(self):
            try:
                return int(current_game_day() or 0) >= 30
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
            return self

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
            self.rel = max(0, min(20, people_to_int(self.rel, 0) + people_to_int(gains.get("rel", 0), 0)))
            self.openness = max(0, min(20, people_to_int(self.openness, 0) + people_to_int(gains.get("openness", 0), 0)))
            self.corruption = max(0, min(100, people_to_int(self.corruption, 0) + people_to_int(gains.get("corruption", 0), 0)))
            return self

        def night_thanks_seen(self):
            self.ensure_story_defaults()
            self.night_thanks_ready_flag = 0
            try:
                self.night_thanks_last_day = int(current_game_day() or 0)
            except Exception:
                self.night_thanks_last_day = 0
            self.mc_visit_first_done = 1
            self.final_reward_flag = 1
            self.room_unlocked_flag = 1
            self.sandraSex = True
            self.rel = max(0, min(20, people_to_int(self.rel, 0) + 2))
            self.openness = max(0, min(20, people_to_int(self.openness, 0) + 2))
            self.corruption = max(0, min(100, people_to_int(self.corruption, 0) + 3))
            return self

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
