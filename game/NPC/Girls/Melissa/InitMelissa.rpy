# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -1 python:
    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        npc_daily_schedule_set(
            schedule_name,
            default_slots=[
                dict(npc_daily_schedule_slot(0, "Church", True, False, "sunday_church"), weekdays=[7]),
                dict(npc_daily_schedule_slot(1, "Church", True, False, "sunday_church"), weekdays=[7]),
                npc_daily_schedule_slot(4, "TavernMelissaRoom", False, False, "sleep"),
            ],
            random_slots=[
                npc_daily_schedule_random_slot(
                    0,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="morning",
                    priority=500,
                    choices=[
                        npc_daily_schedule_choice("TavernKitchen", 4, True, True, "breakfast_and_kitchen"),
                        npc_daily_schedule_choice("TavernStorage", 4, True, True, "basement_cleaning"),
                        npc_daily_schedule_choice("TavernMain", 3, True, True, "hall_cleaning"),
                        npc_daily_schedule_choice("Backyard", 2, True, True, "yard_laundry"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 1, True, True, "late_start_room"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    1,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="noon_work",
                    priority=420,
                    choices=[
                        npc_daily_schedule_choice("TavernMain", 6, True, True, "working_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "kitchen_help"),
                        npc_daily_schedule_choice("TavernStorage", 1, True, True, "storage_sorting"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "yard_chore"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    2,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="day_work",
                    priority=420,
                    choices=[
                        npc_daily_schedule_choice("TavernMain", 7, True, True, "working_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "kitchen_help"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "yard_chore"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[1, 2, 3, 4, 6],
                    label="evening",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("TavernMain", 3, True, True, "evening_hall"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "evening_room"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "evening_yard"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[5],
                    label="friday_evening",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("FridayDance", 4, True, True, "friday_dance"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "friday_room"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    2,
                    weekdays=[7],
                    label="sunday_day",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("TavernMelissaRoom", 3, True, True, "sunday_room"),
                        npc_daily_schedule_choice("Backyard", 2, True, True, "sunday_backyard"),
                        npc_daily_schedule_choice("TavernMain", 2, True, True, "sunday_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "sunday_kitchen"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[7],
                    label="sunday_evening",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("TavernMelissaRoom", 3, True, True, "sunday_room"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "sunday_backyard"),
                        npc_daily_schedule_choice("TavernMain", 2, True, True, "sunday_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "sunday_kitchen"),
                    ],
                ),
            ],
        )
        npc_schedule_set(
            schedule_name,
            [
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[3, 4], awake=True, talkable=True, condition=npc_schedule_rule("clara_paintings_confession"), priority=470, label="clara_paintings_confession"),
            ],
        )
        npc_daily_schedule_build_all(True)
        npc_schedule_sync_currentloc(schedule_name)

    def melissa_after_load_schedule():
        try:
            if "melissa" in list(RealName.keys()):
                peopleData["melissa"] = MelissaStaticData
                Melissa.var = MelissaVar
                Melissa.sync_from_melissa_maps()
                Melissa.ensure_story_defaults()
                peopleInfo["melissa"] = Melissa
                if Melissa not in girls:
                    girls.append(Melissa)
                melissa_install_schedule("melissa")
        except Exception:
            pass

    config.after_load_callbacks.append(melissa_after_load_schedule)

label InitMelissa:
    python:
        GirlName = Melissa.code_name
        peopleData[GirlName] = MelissaStaticData
        Melissa.var = MelissaVar
        Melissa.initialize_new_game_state()
        peopleInfo[GirlName] = Melissa
        if Melissa not in girls:
            girls.append(Melissa)
        bodymodel_sync_character(GirlName, RealName[GirlName], "female")
        Melissa.install_schedule()

    return

init python:
    def melissa_story_defaults():
        return {
            "MomDressComplaint": 0,
            "AskedAboutClaraDay": -1,
            "StartDay": -1,
            "StartCount": 0,
            "StartTotal": 0,
            "private_context_day": -1,
            "private_context_origin": "",
            "private_context_place": "",
            "private_place_heat": 0,
            "RoomProblemAskDay": -1,
            "StorageThanksDay": -1,
            "AtticFindingsDay": -1,
            "bats_episode": 0,
            "temp_room": "",
            "ratKilled": False,
            "storage_rat_cleared": 0,
            "storage_rat_last_help_day": -1,
            "room_pests_last_help_day": -1,
            "AskedMCToSolveRoomProblem": 0,
            "bat_attic_check_day": -1,
            "drawings_ready_day": -1,
            "drawings_found": 0,
            "drawings_booklet_taken": 0,
            "drawings_booklet_left": 0,
            "drawings_booklet_opened": 0,
            "drawings_booklet_read": 0,
            "drawings_spy_option_unlocked": 0,
            "drawings_returned": 0,
            "bat_recipe_clue_seen": 0,
            "bat_recipe_unlocked": 0,
            "bats_completed": 0,
            "bats_completion_day": -1,
            "room_returned": 0,
            "sex_engine_unlocked": 0,
            "roof_repair_order_day": -1,
            "roof_repair_complete_day": -1,
            "breakfast_tease_day": -1,
        }

    class MelissaData(PeopleData):
        code_name = "melissa"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Мелисса",
                fullname="Мелисса",
                genitive="Мелиссы",
                dative="Мелиссе",
                description="Мелисса - молодая девушка. В ее сложении немного проступают восточные черты. Она немного отличается от остальных работниц трактира. У нее оливкового цвета кожа, черные глаза, волосы цвета вороньего крыла и полные, похожие на мячи груди размера С.",
            )
            self.birth_date = {"day": 25, "period": 6, "cycle": 1082}
            self.card_image = "images/melissa/melissa_card.jpg"
            self.schedule_source = "schedules/melissa.json"

    class MelissaInfo(Girl):
        """Melissa runtime: tavern work, bats quest, social state, body state."""
        def __init__(self):
            super().__init__("melissa")
            self.code_name = "melissa"
            self.data = MelissaStaticData
            self.age = 18
            self.rel = 5
            self.relationship = self.rel
            self.openness = 0
            self.corruption = 3
            self.known = True
            self.energy = 100
            self.energy_max = 100
            self.rebellion = 0
            self.anger_with_player = 0
            self.fun = 0
            self.trust = 0
            self.fear = 0
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
                "beauty": 55,
                "sexacts": 0,
                "cuminside": 0,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 15,
                "PussyWetStart": 10,
                "virginity": True,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 30,
                "cleaning": 40,
                "waitress": 30,
            }
            self.jobs = {
                "jobkitchen": 0,
                "jobcleaning": 1,
                "jobwaitress": 1,
                "jobHallAvail": 1,
                "jobWhoreAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
            }
            self.gift_preferences = ["soap_001", "lavender_001", "wild_rose_001", "energy_tea_001", "drink_ale_001", "libido_tincture_001"]
            self.schedule_source = MelissaStaticData.schedule_source
            self.schedule_uses_clock_minutes = True
            self.current_location = "TavernMain"
            self.talk_preferences = {
                "favorite_topics": ["job_routine", "family_life", "melissa_safety", "melissa_quiet", "stories"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["workdress", "simplebra", "simplepanties", "simpleshoes"],
                "gifted": [],
                "current_dress": "workdress",
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
            super(MelissaInfo, self).update()
            self.data = MelissaStaticData
            self.relationship = self.rel
            self.sync_from_melissa_maps()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in melissa_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def sync_from_melissa_maps(self):
            self.rel = people_to_int(Friends.get("melissa", self.rel), self.rel)
            self.relationship = self.rel
            self.openness = people_to_int(otkroven.get("melissa", self.openness), self.openness)
            self.corruption = people_to_int(sluttiness.get("melissa", self.corruption), self.corruption)
            self.drunk = people_to_int(Drunk.get("melissa", self.drunk), self.drunk)
            self.talked_today = people_to_int(TalkedToday.get("melissa", self.talked_today), self.talked_today)
            self.flirted_today = people_to_int(FlirtedToday.get("melissa", self.flirted_today), self.flirted_today)
            self.gifted_today = people_to_int(GiftedToday.get("melissa", self.gifted_today), self.gifted_today)
            self.asked_today = people_to_int(AskedToday.get("melissa", self.asked_today), self.asked_today)
            self.fucked_today = people_to_int(FuckedToday.get("melissa", self.fucked_today), self.fucked_today)
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
                if "melissa" in table:
                    self.stats[stat_key] = table.get("melissa")
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                if "melissa" in table:
                    self.jobs[job_key] = table.get("melissa")
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                if "melissa" in table:
                    self.skills[skill_key] = table.get("melissa")
            self.ensure_story_defaults()
            return self

        def sync_melissa_maps(self):
            name = self.code_name
            RealName[name] = self.data.fullname
            RealName2[name] = self.data.genitive
            RealName3[name] = self.data.dative
            age_girls[name] = people_to_int(self.age, 18)
            DateOfBirth[name] = dict(self.data.birth_date)
            girltextdesc[name] = self.data.description
            knowsMC[name] = bool(self.known)
            Friends[name] = people_to_int(self.rel, 0)
            otkroven[name] = people_to_int(self.openness, 0)
            sluttiness[name] = people_to_int(self.corruption, 0)
            Drunk[name] = people_to_int(self.drunk, 0)
            TalkedToday[name] = people_to_int(self.talked_today, 0)
            FlirtedToday[name] = people_to_int(self.flirted_today, 0)
            GiftedToday[name] = people_to_int(self.gifted_today, 0)
            AskedToday[name] = people_to_int(self.asked_today, 0)
            FuckedToday[name] = people_to_int(self.fucked_today, 0)
            CurrentLoc[name] = str(self.current_location or "TavernMain")
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
            self.ensure_story_defaults()
            return self

        def initialize_new_game_state(self):
            self.var = MelissaVar
            self.ensure_story_defaults()
            self.sync_melissa_maps()
            return self

        def reset_daily(self, full=False):
            super(MelissaInfo, self).reset_daily(full)
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.sync_melissa_maps()
            return self

        def install_schedule(self):
            melissa_install_schedule(self.code_name)
            return self

        def bats_stage(self):
            return max(0, people_to_int(self.var.get("bats_episode", 0), 0))

        def bats_repair_complete(self):
            repair_day = people_to_int(self.var.get("roof_repair_complete_day", -1), -1)
            return (
                self.bats_stage() >= 7
                and repair_day >= 0
                and people_to_int(dayspassed, 0) >= repair_day
            )

        def sync_room_problem_state(self):
            stage = self.bats_stage()
            if stage >= 8:
                self.var["temp_room"] = ""
                self.var["roof_repair_complete_day"] = -1
                self.var["roof_repair_order_day"] = -1
            self.var["bats_episode"] = stage
            self.sync_melissa_maps()
            return stage >= 8 or self.bats_repair_complete()

        def temp_room_active(self, room_code="", time_value=None):
            self.sync_room_problem_state()
            room_key = str(room_code or "").strip()
            temp_room = str(self.var.get("temp_room", "") or "").strip()
            slot = people_to_int(time if time_value is None else time_value, 0)
            hour_num = people_to_int(hour, 0)
            if temp_room == "" or temp_room != room_key:
                return False
            if self.bats_stage() >= 8:
                return False
            scheduled_room = ""
            try:
                scheduled_room = str(npc_schedule_location(self.code_name, people_to_int(week, 0), slot) or "")
            except Exception:
                scheduled_room = ""
            if scheduled_room == "TavernMelissaRoom":
                return True
            return hour_num < 10

        def attic_scandal_ready(self):
            self.sync_room_problem_state()
            return self.bats_stage() == 5

        def drawings_scene_ready(self):
            return (
                self.bats_stage() >= 6
                and self.bats_stage() < 8
                and str(self.var.get("temp_room", "") or "") == "TavernAmandaRoom"
                and people_to_int(self.var.get("drawings_found", 0), 0) == 0
                and people_to_int(dayspassed, 0) >= people_to_int(self.var.get("drawings_ready_day", -1), -1)
                and str(CurLoc or "") == "TavernMelissaRoom"
            )

        def drawings_return_ready(self):
            return (
                people_to_int(self.var.get("drawings_found", 0), 0) == 1
                and people_to_int(self.var.get("drawings_returned", 0), 0) == 0
            )

        def bat_attic_colony_event_ready(self):
            return (
                str(CurLoc or "") == "TavernAtic"
                and self.bats_stage() == 3
                and people_to_int(dayspassed, 0) >= people_to_int(self.var.get("bat_attic_check_day", -1), -1)
            )

        def bat_attic_window_event_ready(self):
            return str(CurLoc or "") == "TavernAtic" and self.bats_stage() in (4, 5)

        def bat_attic_cleanup_event_ready(self):
            return (
                str(CurLoc or "") == "TavernAtic"
                and self.bats_stage() >= 6
                and self.bats_stage() < 8
            )

        def bat_completion_talk_event_ready(self):
            return str(CurLoc or "") == "TavernMain" and self.bats_completion_ready()

        def bat_attic_event_caption(self):
            stage = self.bats_stage()
            if stage == 3:
                return "Осмотреть балки и щели под крышей"
            if stage == 4:
                return "Осмотреть маленькое слуховое окно над комнатой Аманды"
            if stage == 5:
                return "Вернуться к слуховому окну над комнатой Аманды"
            if stage < 7:
                if int(_player_item_count_by_id("bat_repellent_001") or 0) > 0:
                    return "Выжечь гнездо дымной смесью"
                return "Осмотреть, как выкурить гнездо"
            if people_to_int(self.var.get("roof_repair_order_day", -1), -1) < 0:
                if people_to_int(money, 0) >= 1000:
                    return "Заказать починку крыши за 1000"
                return "Прикинуть, сколько обойдется починка крыши"
            return "Осмотреть починку крыши"

        def bat_drawings_event_caption(self):
            return "Присмотреться, чем шуршит Мелисса у кровати"

        def bat_completion_talk_caption(self):
            return "Сказать Мелиссе, что с ее комнатой наконец покончено"

        def bat_repellent_recipe_unlocked(self):
            return (
                people_to_int(self.var.get("bat_recipe_unlocked", 0), 0) == 1
                or recipe_book_hidden_recipes_revealed()
            )

        def bats_completion_ready(self):
            self.sync_room_problem_state()
            return (
                self.bats_stage() == 7
                and self.bats_repair_complete()
                and people_to_int(self.var.get("drawings_returned", 0), 0) == 1
            )

        def complete_bats_problem(self):
            self.var["bats_episode"] = 8
            self.var["bats_completed"] = 1
            self.var["bats_completion_day"] = people_to_int(dayspassed, 0)
            self.var["temp_room"] = ""
            self.var["room_returned"] = 1
            self.var["sex_engine_unlocked"] = 1
            self.var["roof_repair_complete_day"] = -1
            self.var["roof_repair_order_day"] = -1
            self.var["AskedMCToSolveRoomProblem"] = 0
            self.current_location = "TavernMelissaRoom"
            self.sync_melissa_maps()
            return True

        def add_trust(self, amount, cap=20):
            self.rel = min(people_to_int(cap, 20), max(0, people_to_int(self.rel, 0) + people_to_int(amount, 0)))
            self.relationship = self.rel
            self.sync_melissa_maps()
            return self.rel

        def add_openness(self, amount, cap=20):
            self.openness = min(people_to_int(cap, 20), max(0, people_to_int(self.openness, 0) + people_to_int(amount, 0)))
            self.sync_melissa_maps()
            return self.openness

define MelissaStaticData = MelissaData()
default Melissa = MelissaInfo()
