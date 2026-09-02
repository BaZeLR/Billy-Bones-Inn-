# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitMelissa:
    python:
        Melissa.initialize_new_game_state()
        people.register(MelissaStaticData, Melissa)
    return

init python:
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
                gift_preferences=["lavender_rose_soap_001", "soap_001", "lavender_001", "wild_rose_001", "energy_tea_001", "drink_ale_001", "libido_tincture_001"],
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
                "backyard": {
                    "laundry": [
                        "images/melissa/making laundry.png",
                        "images/melissa/hanging laundry.png",
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
                    "finish": ["images/melissa/thanks.png"],
                },
                "outfit_reward": {
                    "show": ["images/melissa/thanks.png"],
                    "handjob": ["images/melissa/thanks1.png"],
                    "handjob_finish": ["images/melissa/thanks.png"],
                    "oral": ["images/melissa/sexyTimes/blowjob0.png"],
                    "oral_finish": ["images/melissa/sexyTimes/blowjobFinish.jpg"],
                },
            }

    class MelissaInfo(Girl):
        """Melissa runtime: tavern work, bats quest, social state, body state."""
        talk_label = "IntMelissaTalk"
        unknown_name = "Незнакомка"
        def __init__(self):
            super().__init__("melissa")
            self.code_name = "melissa"
            self.data = MelissaStaticData
            self.rel = 5
            self.openness = 0
            self.corruption = 3
            self.known = True
            self.revealing_dress_code = ""
            self.mom_dress_complaint_count = 0
            self.asked_about_clara_day = -1
            self.private_context_day = -1
            self.private_context_origin = ""
            self.storage_thanks_day = -1
            self.temp_room_code = ""
            self.storage_rat_help_day = -1
            self.bat_attic_check_day = -1
            self.drawings_found = False
            self.drawings_booklet_left = False
            self.drawings_booklet_read = False
            self.drawings_returned = False
            self.roof_repair_complete_day = -1
            self.breakfast_tease_day = -1
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
                "jobkitchentomorrow": 0,
                "jobcleaningtomorrow": 1,
                "jobwaitresstomorrow": 1,
                "jobHallAvail": 1,
                "jobWhoreAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
            }
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
        def update(self):
            super(MelissaInfo, self).update()
            self.data = MelissaStaticData
            return self

        def initialize_new_game_state(self):
            self.data = MelissaStaticData
            self.known = True
            return self

        def reset_daily(self, full=False):
            super(MelissaInfo, self).reset_daily(full)
            self.private_context_day = -1
            self.private_context_origin = ""
            return self

        def relationship_stage(self):
            friend_value = people_to_int(self.rel, 0)
            open_value = people_to_int(self.openness, 0)
            corruption_value = people_to_int(self.corruption, 0)
            stage = 0
            if friend_value >= 5 and (open_value >= 2 or corruption_value >= 5):
                stage = 1
            if friend_value >= 10 and (open_value >= 4 or corruption_value >= 8):
                stage = 2
            if friend_value >= 13 and (open_value >= 7 or corruption_value >= 14):
                stage = 3
            if (
                threads["melissaBatProblem"].completed
                and threads["melissaCourtship"].completed
                and friend_value >= 15
                and open_value >= 9
                and corruption_value >= 18
            ):
                stage = 4
            return stage

        def intimacy_story_ready(self):
            booklet_resolved = (
                bool(self.drawings_booklet_left)
                or int(player.item_count("melissa_drawings_booklet_001") or 0) > 0
            )
            return (
                people_to_int(self.storage_rat_help_day, -1) >= 0
                and threads["melissaBatProblem"].completed
                and people_to_int(self.roof_repair_complete_day, -1) >= 0
                and bool(self.drawings_returned)
                and booklet_resolved
            )

        def relationship_allows(self, action_code="talk"):
            action_key = str(action_code or "talk").strip().lower()
            if action_key == "talk":
                return True
            if action_key == "gift":
                return relationship_any_gift_allowed(self.code_name)
            if action_key in ("share", "flirt"):
                allowed, reason = relationship_social_action_allowed(self.code_name, action_key)
                return bool(allowed)
            if action_key == "intimacy":
                return (
                    self.intimacy_story_ready()
                    and threads["melissaCourtship"].completed
                    and self.relationship_stage() >= 3
                    and self.can_have_sex_today()
                )
            if action_key == "sex":
                return (
                    self.intimacy_story_ready()
                    and threads["melissaCourtship"].completed
                    and self.relationship_stage() >= 4
                    and self.can_have_sex_today()
                )
            return False

        def private_context_active(self, room_code=""):
            room_key = str(room_code or rooms.current_code or "").strip()
            return (
                people_to_int(self.private_context_day, -1) == current_game_day()
                and str(self.private_context_origin or "").strip() == room_key
            )

        def room_is_private(self, room_code=""):
            return household_intimacy_room_is_private(self.code_name, room_code)

        def wet_enough_to_find_place(self):
            wet_value = max(
                people_to_int(self.arousal_value(), 0),
                people_to_int(self.stats.get("PussyWetStart", 0), 0),
            )
            return wet_value >= 35 or people_to_int(self.corruption, 0) >= 24

        def private_place_offer(self, room_code=""):
            room_key = str(room_code or rooms.current_code or "").strip()
            if not self.relationship_allows("intimacy"):
                return {"ok": False, "place": "", "text": ""}
            if self.room_is_private(room_key):
                return {"ok": True, "place": room_key, "text": ""}
            if not self.wet_enough_to_find_place():
                return {"ok": False, "place": "", "text": ""}
            if room_key == "WineStore":
                return {
                    "ok": True,
                    "place": "wine_cellar",
                    "text": "Мелисса быстро оглядывается и кивает в сторону дальнего подвальчика за винными стеллажами. Там достаточно темно и тесно, чтобы вас не видели с прилавка.",
                }
            if room_key == "MarketPlace":
                return {
                    "ok": True,
                    "place": "market_shelves",
                    "text": "Мелисса ведет вас к глухому проходу за стеллажами и ящиками, где шум рынка остается совсем рядом, но прямых взглядов уже нет.",
                }
            if room_key in HOUSEHOLD_INTIMACY_SECLUDED_ROOMS:
                return {
                    "ok": True,
                    "place": room_key,
                    "text": "Мелисса сама выбирает место в стороне от тропы, где ветки и тени закрывают вас от случайных глаз.",
                }
            return {"ok": False, "place": "", "text": ""}

        def getLocation(self, wday=None, hour=None):
            scheduled_location = super(MelissaInfo, self).getLocation(wday, hour)
            if scheduled_location == "BarberShop":
                return scheduled_location
            temp_room = str(self.temp_room_code or "").strip()
            if temp_room and self.temp_room_active(temp_room, hour, wday):
                return temp_room
            return scheduled_location

        def bats_repair_complete(self):
            repair_day = people_to_int(self.roof_repair_complete_day, -1)
            return (
                threads["melissaBatProblem"].num >= 7
                and repair_day >= 0
                and current_game_day() >= repair_day
            )

        def temp_room_active(self, room_code="", hour_value=None, weekday_value=None):
            room_key = str(room_code or "").strip()
            temp_room = str(self.temp_room_code or "").strip()
            hour_num = people_to_int(calendar_v2.hour if hour_value is None else hour_value, 0)
            week_num = people_to_int(calendar_v2.week if weekday_value is None else weekday_value, 0)
            if temp_room == "" or temp_room != room_key:
                return False
            if threads["melissaBatProblem"].num >= 10:
                return False
            scheduled_room = str(self.data.getLocation(week_num, hour_num) or "")
            if scheduled_room == "TavernMelissaRoom":
                return True
            return hour_num < 10

        def attic_scandal_ready(self):
            return threads["melissaBatProblem"].num == 5

        def drawings_scene_ready(self):
            return (
                threads["melissaBatProblem"].num == 10
                and not bool(self.drawings_found)
                and str(rooms.current_code or "") == "TavernMelissaRoom"
            )

        def bat_attic_colony_event_ready(self):
            return (
                str(rooms.current_code or "") == "TavernAtic"
                and threads["melissaBatProblem"].num == 3
                and current_game_day() >= people_to_int(self.bat_attic_check_day, -1)
            )

        def bat_attic_window_event_ready(self):
            return str(rooms.current_code or "") == "TavernAtic" and threads["melissaBatProblem"].num in (4, 5)

        def bat_attic_cleanup_event_ready(self):
            return (
                str(rooms.current_code or "") == "TavernAtic"
                and threads["melissaBatProblem"].num >= 6
                and threads["melissaBatProblem"].num < 8
            )

        def bat_completion_talk_event_ready(self):
            return str(rooms.current_code or "") == "TavernMain" and self.bats_completion_ready()

        def bat_attic_event_caption(self):
            stage = threads["melissaBatProblem"].num
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
            if people_to_int(self.roof_repair_complete_day, -1) < 0:
                if people_to_int(player.economy.money, 0) >= 2000:
                    return "Заказать починку крыши за 2000"
                return "Прикинуть, сколько обойдется починка крыши"
            return "Осмотреть починку крыши"

        def bats_completion_ready(self):
            return (
                threads["melissaBatProblem"].num == 11
                and bool(self.drawings_returned)
            )

        def complete_bats_problem(self):
            self.temp_room_code = ""
            return True

define MelissaStaticData = MelissaData()
default Melissa = MelissaInfo()
