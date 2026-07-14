        npc_schedule_sync_currentloc(schedule_name)        bodymodel_sync_character(GirlName, Melissa.data.fullname, "female")            self.current_location = "TavernMain"            self.current_location = "TavernMelissaRoom"            "AskedMCToSolveRoomProblem": 0,            "RoomProblemAskDay": -1,            self.schedule_source = MelissaStaticData.schedule_source            self.schedule_source = MelissaStaticData.schedule_source
            self.current_location = "TavernMain"            "AskedMCToSolveRoomProblem": 0,            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel        npc_schedule_sync_currentloc(schedule_name)        bodymodel_sync_character(GirlName, Melissa.data.fullname, "female")            self.current_location = "TavernMain"            self.current_location = "TavernMelissaRoom"            "AskedMCToSolveRoomProblem": 0,            "RoomProblemAskDay": -1,            self.schedule_source = MelissaStaticData.schedule_source            self.schedule_source = MelissaStaticData.schedule_source
            self.current_location = "TavernMain"            "AskedMCToSolveRoomProblem": 0,            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel        npc_schedule_sync_currentloc(schedule_name)        bodymodel_sync_character(GirlName, Melissa.data.fullname, "female")            self.current_location = "TavernMain"            self.current_location = "TavernMelissaRoom"            "AskedMCToSolveRoomProblem": 0,            "RoomProblemAskDay": -1,            self.schedule_source = MelissaStaticData.schedule_source            self.schedule_source = MelissaStaticData.schedule_source
            self.current_location = "TavernMain"            "AskedMCToSolveRoomProblem": 0,            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -1 python:
    def melissa_schedule_clara_paintings_confession_ready():
            Melissa.install_schedule()

        Melissa.install_schedule()

        Melissa.install_schedule()

        Melissa.install_schedule()

        Melissa.install_schedule()

        Melissa.install_schedule()

    return int(Clara.var.get("peek_done", 0) or 0) == 1 and int(Clara.var.get("confession_done", 0) or 0) == 0

    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        schedule_data = people_schedule_data(schedule_name)
        if schedule_data is not None:
            schedule_data.set_daily_schedule([], [])
            schedule_data.load_interval_schedule(True)
        npc_schedule_set(
            schedule_name,
            [
                NPCHourScheduleEntry(npc_id=schedule_name, location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], start="22:00", end="23:00", awake=True, talkable=True, condition=melissa_schedule_clara_paintings_confession_ready, priority=870, label="clara_paintings_confession", source="rpy_condition"),
            ],
        )

init -1 python:
    def melissa_schedule_clara_paintings_confession_ready():
        return int(Clara.var.get("peek_done", 0) or 0) == 1 and int(Clara.var.get("confession_done", 0) or 0) == 0

    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        schedule_data = people_schedule_data(schedule_name)
        if schedule_data is not None:
            schedule_data.set_daily_schedule([], [])
            schedule_data.load_interval_schedule(True)
        npc_schedule_set(
            schedule_name,
            [
                NPCHourScheduleEntry(npc_id=schedule_name, location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], start="22:00", end="23:00", awake=True, talkable=True, condition=melissa_schedule_clara_paintings_confession_ready, priority=870, label="clara_paintings_confession", source="rpy_condition"),
            ],
        )

init -1 python:
    def melissa_schedule_clara_paintings_confession_ready():
        return int(Clara.var.get("peek_done", 0) or 0) == 1 and int(Clara.var.get("confession_done", 0) or 0) == 0

    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        schedule_data = people_schedule_data(schedule_name)
        if schedule_data is not None:
            schedule_data.set_daily_schedule([], [])
            schedule_data.load_interval_schedule(True)
        npc_schedule_set(
            schedule_name,
            [
                NPCHourScheduleEntry(npc_id=schedule_name, location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], start="22:00", end="23:00", awake=True, talkable=True, condition=melissa_schedule_clara_paintings_confession_ready, priority=870, label="clara_paintings_confession", source="rpy_condition"),
            ],
        )

init -1 python:
    def melissa_schedule_clara_paintings_confession_ready():
        return int(Clara.var.get("peek_done", 0) or 0) == 1 and int(Clara.var.get("confession_done", 0) or 0) == 0

    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        schedule_data = people_schedule_data(schedule_name)
        if schedule_data is not None:
            schedule_data.set_daily_schedule([], [])
            schedule_data.load_interval_schedule(True)
        npc_schedule_set(
            schedule_name,
            [
                NPCHourScheduleEntry(npc_id=schedule_name, location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], start="22:00", end="23:00", awake=True, talkable=True, condition=melissa_schedule_clara_paintings_confession_ready, priority=870, label="clara_paintings_confession", source="rpy_condition"),
            ],
        )

init -1 python:
    def melissa_schedule_clara_paintings_confession_ready():
        return int(Clara.var.get("peek_done", 0) or 0) == 1 and int(Clara.var.get("confession_done", 0) or 0) == 0

    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        schedule_data = people_schedule_data(schedule_name)
        if schedule_data is not None:
            schedule_data.set_daily_schedule([], [])
            schedule_data.load_interval_schedule(True)
        npc_schedule_set(
            schedule_name,
            [
                NPCHourScheduleEntry(npc_id=schedule_name, location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], start="22:00", end="23:00", awake=True, talkable=True, condition=melissa_schedule_clara_paintings_confession_ready, priority=870, label="clara_paintings_confession", source="rpy_condition"),
            ],
        )

init -1 python:
    def melissa_schedule_clara_paintings_confession_ready():
        return int(Clara.var.get("peek_done", 0) or 0) == 1 and int(Clara.var.get("confession_done", 0) or 0) == 0

    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        schedule_data = people_schedule_data(schedule_name)
        if schedule_data is not None:
            schedule_data.set_daily_schedule([], [])
            schedule_data.load_interval_schedule(True)
        npc_schedule_set(
            schedule_name,
            [
                NPCHourScheduleEntry(npc_id=schedule_name, location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], start="22:00", end="23:00", awake=True, talkable=True, condition=melissa_schedule_clara_paintings_confession_ready, priority=870, label="clara_paintings_confession", source="rpy_condition"),
            ],
        )

label InitMelissa:
    python:
        GirlName = Melissa.code_name
        peopleData[GirlName] = MelissaStaticData
        Melissa.initialize_new_game_state()
        peopleInfo[GirlName] = Melissa
        if Melissa not in girls:
            girls.append(Melissa)
        Melissa.install_schedule()
        Melissa.install_schedule()
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
            "ratKilled": False,
            "ratKilled": False,
            "ratKilled": False,
            "ratKilled": False,
            "ratKilled": False,
            "storage_rat_cleared": 0,
            "storage_rat_last_help_day": -1,
            "room_pests_last_help_day": -1,
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
            "bats_completed": 0,
            "bats_completed": 0,
            "bats_completed": 0,
            "bats_completed": 0,
            "bats_completed": 0,
            "bats_completion_day": -1,
            "room_returned": 0,
            "sex_engine_unlocked": 0,
            "room_returned": 0,
            "sex_engine_unlocked": 0,
            "room_returned": 0,
            "sex_engine_unlocked": 0,
            "room_returned": 0,
            "sex_engine_unlocked": 0,
            "room_returned": 0,
            "sex_engine_unlocked": 0,
            "room_returned": 0,
            "sex_engine_unlocked": 0,
            "roof_repair_order_day": -1,
            "roof_repair_complete_day": -1,
            "breakfast_tease_day": -1,
            "sex_times_today": 0,
            "harass_instruction": "",
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
                portrait="images/melissa/melissa_portrait_0.jpg",
                description="Мелисса - молодая девушка. В ее сложении немного проступают восточные черты. Она немного отличается от остальных работниц трактира. У нее оливкового цвета кожа, черные глаза, волосы цвета вороньего крыла и полные, похожие на мячи груди размера С.",
            )
            self.birth_date = {"day": 25, "period": 6, "cycle": 1082}
            self.card_image = "images/melissa/melissa_card.jpg"
            self.schedule_source = "schedules/melissa.json"
            self.image_manifest = {
                "card": {
                    "default": ["images/melissa/melissa_card.jpg"],
                },
                "portrait": {
                    "default": [
                        "images/melissa/melissa_portrait_0.jpg",
                        "images/melissa/melissa_portrait_1.jpg",
                        "images/melissa/tavern/portrait.png",
                    ],
                    "happy": ["images/melissa/happy.png"],
                    "angry": ["images/melissa/angy.png"],
                    "thanks": ["images/melissa/thanks.png", "images/melissa/thanks1.png"],
                    "bats_problem": ["images/melissa/bats_problem.png"],
                },
                "kitchen": {
                    "work": [
                        "images/melissa/tavern/kitchen_0.png",
                        "images/melissa/tavern/kitchen_1.png",
                        "images/melissa/kitchen.jpg",
                        "images/melissa/kitchen2.jpg",
                        "images/melissa/kitchen3.jpg",
                    ],
                    "breakfast": [
                        "images/breakfast/melissa_breakfast/melissa breakfast.jpg",
                        "images/breakfast/melissa_breakfast/melissa breakfast_2.jpg",
                        "images/breakfast/melissa_breakfast/melissa_breakfast.jpg",
                        "images/breakfast/melissa_breakfast/melissa_breakfast_1.jpg",
                        "images/melissa/tavern/kitchen_0.png",
                        "images/melissa/tavern/kitchen_1.png",
                        "images/melissa/tavern/portrait.png",
                    ],
                },
                "tavern": {
                    "hall_cleaning": [
                        "images/melissa/tavern/clean_0.png",
                        "images/melissa/tavern/clean_1.png",
                        "images/melissa/tavern/cleans_0.png",
                    ],
                    "waitress": [
                        "images/melissa/tavern/waitress_0.png",
                        "images/melissa/tavern/waitress_1.png",
                        "images/melissa/tavern/waitress_2.png",
                        "images/melissa/tavern/waitress_4.png",
                    ],
                    "backyard": [
                        "images/melissa/tavern/backyard_0.png",
                        "images/melissa/tavern/backyard_1.png",
                    ],
                    "basement": ["images/melissa/tavern/basement.png"],
                    "rat": ["images/melissa/tavern/rat_in_basement_melissa.png"],
                    "sleep": [
                        "images/melissa/tavern/melissa_sleeps_0.jpg",
                        "images/melissa/tavern/melissa_sleeps_1.png",
                        "images/melissa/tavern/melissa_sleeps_2.png",
                        "images/melissa/tavern/melissa_sleeps_3.png",
                        "images/melissa/tavern/melissa_sleeps_4.png",
                        "images/melissa/tavern/melissa_sleeps.png",
                    ],
                    "clumsy_waitress": [
                        "images/melissa/tavern/clumsywaitress/waitressFall1.jpg",
                        "images/melissa/tavern/clumsywaitress/waitresFall2.png",
                        "images/melissa/tavern/clumsywaitress/waitresshelp.png",
                    ],
                    "room": ["images/melissa/tavern/portrait.png"],
                    "angry": ["images/melissa/tavern/angry.jpg"],
                },
                "bats": {
                    "points_to_ceiling": ["images/melissa/bats/points_to_ceiling.jpg"],
                    "sleepless": ["images/melissa/bats/sleepless.png"],
                    "yawns": ["images/melissa/bats/yawns.png"],
                },
                "amanda_room": {
                    "under_bed_search": [
                        "images/melissa/amandaRoom/underBedsearch_0.png",
                        "images/melissa/amandaRoom/underBedsearch_1.png",
                        "images/melissa/amandaRoom/underBedsearch_2.png",
                    ],
                },
                "bedroom_search": {
                    "booklet": ["images/melissa/bedRoomSearch/underBedBooklet.png"],
                    "lewd_pages": [
                        "images/melissa/bedRoomSearch/lewd_pages0.jpg",
                        "images/melissa/bedRoomSearch/lewd_pages1.jpg",
                        "images/melissa/bedRoomSearch/lewd2_pages.jpg",
                    ],
                },
                "church": {
                    "sisters": ["images/melissa/church/sisters.png"],
                },
                "grope": {
                    "ass_angry": ["images/melissa/Grope/assAngry.png"],
                    "ass_ok": ["images/melissa/Grope/assOk.png"],
                    "georgette": ["images/melissa/Grope/Georgette.jpg"],
                    "scold_agree": ["images/melissa/Grope/scoldAgree.png"],
                    "scold_angry": ["images/melissa/Grope/scoldAngry.png"],
                    "scold_disagree": ["images/melissa/Grope/scoldDisagree.png"],
                    "scold_like": ["images/melissa/Grope/scoldLike.png"],
                    "scold_neutral": [
                        "images/melissa/Grope/scoldNeutral1.png",
                        "images/melissa/Grope/scoldNeutral2.png",
                    ],
                    "throw_delinquent": ["images/melissa/Grope/throwdeliquient.png"],
                    "tit_angry": ["images/melissa/Grope/titAngry.png"],
                    "tit_ok": [
                        "images/melissa/Grope/titok1.png",
                        "images/melissa/Grope/titsok2.png",
                    ],
                    "tits_shy": ["images/melissa/Grope/titsShy.png"],
                    "waitress_rebel": [
                        "images/melissa/Grope/waiteringrebel1.png",
                        "images/melissa/Grope/waiteresRebel2.png",
                        "images/melissa/Grope/waiteressrebel3.png",
                        "images/melissa/Grope/waitressrebel4.png",
                    ],
                },
                "sexy_times": {
                    "blowjob": [
                        "images/melissa/sexyTimes/blowjob0.png",
                        "images/melissa/sexyTimes/blowjob1.jpg",
                        "images/melissa/sexyTimes/blowjob3.png",
                        "images/melissa/sexyTimes/blowjob5.png",
                    ],
                    "blowjob_finish": ["images/melissa/sexyTimes/blowjobFinish.jpg"],
                },
            }

        def image_sequence(self, context="", key="default"):
            context_key = str(context or "").strip()
            image_key = str(key or "default").strip()
            context_row = self.image_manifest.get(context_key, {})
            if isinstance(context_row, list):
                candidates = context_row
            else:
                candidates = context_row.get(image_key, [])
            if isinstance(candidates, str):
                candidates = [candidates]
            return [str(path) for path in list(candidates or []) if str(path or "").strip() and renpy.loadable(str(path))]

        def image_path(self, context="", key="default"):
            candidates = self.image_sequence(context, key)
            if len(candidates) > 0:
                return candidates[0]
            return ""

    class MelissaInfo(Girl):
        """Melissa runtime: tavern work, bats quest, social state, body state."""
        unknown_name = "Незнакомка"

        def __init__(self):
            super().__init__("melissa")
            self.code_name = "melissa"
            self.uses_own_var_state = True
            self.data = MelissaStaticData
            self.rel = 5
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
            self.relationship_cap = 100
            self.talk_preferences = {
                "favorite_topics": ["job_routine", "family_life", "forest", "stories", "food"],
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
            self.name = self.code_name
            self.data = MelissaStaticData
            self.ensure_story_defaults()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in melissa_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def initialize_new_game_state(self):
            self.data = MelissaStaticData
            self.known = True
            self.ensure_story_defaults()
            return self

        def image_sequence(self, context="", key="default"):
            return self.data.image_sequence(context, key)

        def image_path(self, context="", key="default"):
            return self.data.image_path(context, key)

        def cycle_image(self, context="", key="default", salt=0):
            candidates = self.image_sequence(context, key)
            if len(candidates) <= 0:
                return ""
            return candidates[people_to_int(salt, 0) % len(candidates)]

        def reset_daily(self, full=False):
            super(MelissaInfo, self).reset_daily(full)
            self.ensure_story_defaults()
            self.var["private_context_day"] = -1
            self.var["private_context_origin"] = ""
            self.var["private_context_place"] = ""
            self.var["private_place_heat"] = 0
            self.var["sex_times_today"] = 0
            return self

        def install_schedule(self):
            melissa_install_schedule(self.code_name)
            return self

        def install_schedule(self):
            melissa_install_schedule(self.code_name)
            return self

        def install_schedule(self):
            melissa_install_schedule(self.code_name)
            return self

        def install_schedule(self):
            melissa_install_schedule(self.code_name)
            return self

        def getLocation(self, wday=None, hour=None):
            location_value = super(MelissaInfo, self).getLocation(wday, hour)
            temp_room = str(self.var.get("temp_room", "") or "").strip()
            if str(self.location or "").strip() in (temp_room, "TavernMelissaRoom", "TavernAmandaRoom"):
                self.location = ""
            if temp_room and self.temp_room_active(temp_room, hour, wday):
                self.location = temp_room
                return temp_room
            return location_value

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
            return stage >= 8 or self.bats_repair_complete()

        def temp_room_active(self, room_code="", hour_value=None, weekday_value=None):
            self.sync_room_problem_state()
            room_key = str(room_code or "").strip()
            temp_room = str(self.var.get("temp_room", "") or "").strip()
            hour_num = people_to_int(calendar_v2.hour if hour_value is None else hour_value, 0)
            week_num = people_to_int(week if weekday_value is None else weekday_value, 0)
            if temp_room == "" or temp_room != room_key:
                return False
            if self.bats_stage() >= 8:
                return False
            scheduled_room = ""
            try:
                scheduled_room = str(npc_schedule_location(self.code_name, week_num, hour_num) or "")
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
                if int(player.item_count("bat_repellent_001") or 0) > 0:
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
            self.current_location = "TavernMelissaRoom"
            self.var["AskedMCToSolveRoomProblem"] = 0
            self.current_location = "TavernMelissaRoom"
            return True

        def add_trust(self, amount, cap=20):
            self.rel = min(people_to_int(cap, 20), max(0, people_to_int(self.rel, 0) + people_to_int(amount, 0)))
            return self.rel

        def add_openness(self, amount, cap=20):
            self.openness = min(people_to_int(cap, 20), max(0, people_to_int(self.openness, 0) + people_to_int(amount, 0)))
            return self.openness

define MelissaStaticData = MelissaData()
default Melissa = MelissaInfo()
