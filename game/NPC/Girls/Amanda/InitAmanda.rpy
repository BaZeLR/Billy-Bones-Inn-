# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    class AmandaData(PeopleData):
        code_name = "amanda"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Аманда",
                fullname="Аманда",
                genitive="Аманды",
                dative="Аманде",
                portrait="images/amanda/amanda_portrait.jpg",
                default_location="",
                description="Аманда - молодая девушка. У нее очень светлая кожа, белокурые волосы и голубые глаза. Ее груди небольшие, размера А.",
                gift_preferences=["wild_rose_001", "soap_001", "berries_001", "energy_tea_001", "drink_ale_001"],
            )
            self.birth_date = {"day": 10, "period": 9, "cycle": 1082}
            self.card_image = "images/amanda/amanda_card.jpg"
            self.schedule_source = "schedules/amanda.json"
            self.image_manifest = {
                "tavern": {
                    "hall_cleaning": [
                        "images/amanda/tavern/cleaner.webp",
                        "images/amanda/tavern/cleaning1.jpg",
                        "images/amanda/tavern/cleaning2.jpg",
                    ],
                    "waitress": [
                        "images/amanda/tavern/waitress.png",
                        "images/amanda/tavern/waitress1.jpeg",
                        "images/amanda/tavern/waitress2.jpeg",
                        "images/amanda/tavern/waitress3.jpeg",
                        "images/amanda/tavern/waitress4.jpg",
                        "images/amanda/tavern/waitress5.jpg",
                    ],
                },
                "outfit_reward": {
                    "show": ["images/amanda/grope/dressFlirt1.png"],
                    "handjob": ["images/amanda/grope/handjob1.jpg"],
                    "handjob_finish": ["images/amanda/grope/handjob4.jpg"],
                    "oral": ["images/amanda/RandomSex/minet1.jpg"],
                    "oral_finish": ["images/amanda/RandomSex/minet5.jpg"],
                },
            }

    class AmandaInfo(Girl):
        """Amanda runtime: tavern household, Legare path, social state, body state."""
        talk_label = "IntAmandaTalk"
        unknown_name = "Незнакомка"
        uses_own_var_state = True
        STORY_DEFAULTS = {
            "lizafriends": 0,
            "prohibitliza": 0,
            "glorytried": 0,
            "gloryyouknow": 0,
            "gloryscold": 0,
            "glorywalkout": 0,
            "glorysuck": 0,
            "glorysdiscover": 0,
            "glorydeflower": 0,
            "suckyou": 0,
            "fuckyou": 0,
            "knowsexactive": 0,
            "knownotvirgin": 0,
            "beddeflower": 0,
            "sawwithguys": 0,
            "prohibitwithguys": 0,
        }

        def __init__(self):
            super().__init__("amanda")
            self.code_name = "amanda"
            self.data = AmandaStaticData
            self.rel = 5
            self.openness = 3
            self.corruption = 0
            self.known = True
            self.revealing_dress_code = ""
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
            self.mana_reaction_table = {
                "very_low": {"min": 0, "max": 9, "reaction": "withdrawn", "visible_effect": "no_aura", "behavior": "avoid"},
                "low": {"min": 10, "max": 29, "reaction": "neutral_cautious", "visible_effect": "faint_aura", "behavior": "normal"},
                "medium": {"min": 30, "max": 59, "reaction": "warm_interested", "visible_effect": "visible_glow", "behavior": "open"},
                "high": {"min": 60, "max": 84, "reaction": "eager_trusting", "visible_effect": "strong_aura", "behavior": "helpful"},
                "very_high": {"min": 85, "max": 100, "reaction": "devoted_overwhelmed", "visible_effect": "overwhelming_aura", "behavior": "intense"},
                "corrupted": {"min": 0, "max": 100, "reaction": "hostile_unstable", "visible_effect": "dark_corrupted_aura", "behavior": "reject"},
            }
            self.fertility_cycle = {
                "cycle_day": 0,
                "cycle_length": 28,
                "fertile_window_start": 11,
                "fertile_window_end": 16,
                "last_updated_day": None,
            }
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.night_bowl_given = False
            self.night_bowl_request_day = -1
            self.fancy_night_bowl_received = False
            self.backyard_relief_preference = -1
            self.attic_window_breakfast_bj_day = -1
            self.attic_mock_response_day = -1
            self.attic_mock_stopped = False
            self.attic_mock_exposed = False
            self.attic_window_favor_stage = 0
            self.breakfast_tease_day = -1
            self.warned_about_not_working = False
            self.pregnancy_risk_asked_today = False
            self.mom_dress_complaint_count = 0
            self.room_entry_blocked_today = False
            self.room_rejection_count = 0
            self.room_rescue_called = False
            self.legare_affection = 0
            self.dancing_with_legare = False
            self.left_friday_dance = False
            self.legare_forbidden = False
            self.legare_departure_code = 0
            self.escaped_dance_unnoticed = False
            self.performed_oral_with_legare = False
            self.had_sex_with_legare = False
            self.lost_virginity_to_legare = False
            self.player_knows_legare_deflowered = False
            self.player_knows_legare_sex = False
            self.player_saw_legare_sex = False
            self.knows_player_saw_legare_sex = False
            self.knows_player_is_watching_legare_sex = False
            self.drunk = 0
            self.stats = {
                "kids": 0,
                "beauty": 52,
                "sexacts": 0,
                "cuminside": 0,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 10,
                "PussyWetStart": 0,
                "virginity": True,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 20,
                "cleaning": 30,
                "waitress": 15,
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
            self.gift_preferences = list(AmandaStaticData.gift_preferences)
            self.relationship_cap = 100
            self.talk_preferences = {
                "favorite_topics": ["fashion", "dances", "gossip", "money", "stories"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["modestworkdress", "simplebra", "simplepanties", "simpleshoes"],
                "gifted": [],
                "current_dress": "modestworkdress",
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
            self.name = people_normalize_id(self.name)
            self.data = AmandaStaticData
            self.ensure_story_defaults()
            return self

        def initialize_new_game_state(self):
            self.ensure_story_defaults()
            return self

        def mana_profile(self):
            if self.mana_corrupted:
                return self.mana_reaction_table["corrupted"]
            value = max(0, min(100, people_to_int(self.mana, 0)))
            for level in ["very_low", "low", "medium", "high", "very_high"]:
                row = self.mana_reaction_table[level]
                if row["min"] <= value <= row["max"]:
                    return row
            return self.mana_reaction_table["low"]

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
            if context.get("fertile", False):
                score += 1
            self.reaction_state["last_reaction_score"] = score
            return score

        def cycle_state(self):
            return dict(girl_decision_cycle_state(self.code_name) or {})

        def fertility_state(self):
            cycle = self.cycle_state()
            phase = str(cycle.get("phase", "steady") or "steady")
            cycle_day = people_to_int(cycle.get("day", cycle.get("cycle_day", 0)), 0)
            horny = float(cycle.get("horny", 0.0) or 0.0)
            critical = float(cycle.get("critical", 0.0) or 0.0)
            return {
                "phase": phase,
                "cycle_day": cycle_day,
                "fertility": cycle.get("fertility", 0.0),
                "desire": cycle.get("desire", cycle.get("horny", 0.0)),
                "rest": cycle.get("rest", 0.0),
                "safety": cycle.get("safety", 0.0),
                "need_bandage": 1 if critical >= 0.75 else 0,
                "wet_bonus": int(max(0.0, horny) * 8),
                "arousal_bonus": int(max(0.0, horny) * 10),
                "tags": [phase],
            }

        def pregnancy_state(self):
            return {
                "pregnancy": people_to_int(self.stats.get("pregnancy", 0), 0),
                "pregfather": str(self.stats.get("pregfather", "") or ""),
                "cuminside": people_to_int(self.stats.get("cuminside", 0), 0),
                "conception_chance": people_to_int(self.stats.get("ConceptionChance", 0), 0),
                "sexacts": people_to_int(self.stats.get("sexacts", 0), 0),
            }

        def sex_count(self, partner="", cum_target="", sign="", start_day=0):
            partner_value = str(partner or "").strip().lower()
            target_value = str(cum_target or "").strip().lower()
            sign_value = str(sign or "")
            start_day_value = people_to_int(start_day, 0)
            count = 0
            for row in list(getattr(self, "detailed_sex_history", []) or []):
                row_partner = str(row.get("DudeName", "") or "").strip().lower()
                row_target = str(row.get("CumTarget", "") or "").strip().lower()
                row_day = people_to_int(row.get("Day", 0), 0)
                if partner_value and row_partner != partner_value:
                    continue
                if target_value and sign_value == "<>" and row_target == target_value:
                    continue
                if target_value and sign_value != "<>" and row_target != target_value:
                    continue
                if start_day_value > 0 and row_day < start_day_value + 1:
                    continue
                count += 1
            return count

        def pregnancy_check(self, cum_place, repeat_count=1, dad_name="Вы", is_dude_random=0, dad_name_type=""):
            dad = str(dad_name or "").strip()
            dad_type = str(dad_name_type or "").strip()
            is_random = people_to_int(is_dude_random, 0)
            place = str(cum_place or "").strip().lower()
            if dad.lower() == "you" or dad == "вы":
                dad = "Вы"
            if dad == "":
                is_random = 1
            if dad_type == "" and not is_random:
                dad_type = "NPC"
            dad_type_reset = 1 if is_random and dad_type == "" else 0
            dad_name_reset = 1 if dad == "" else 0
            place_reset = 1 if place not in ("inside", "mouth", "tits", "mouthface", "face", "outside") else 0
            fun_awarded = 0
            for _unused_amanda_pregnancy_check in range(max(1, people_to_int(repeat_count, 1))):
                if dad_type_reset:
                    dad_type = [
                        "Неизвестный моряк",
                        "Неизвестный грузчик",
                        "Неизвестный негр",
                        "Неизвестный стражник",
                        "Неизвестный горожанин",
                        "Неизвестный крестьянин",
                        "Неизвестный торговец",
                    ][procedural_randint(1, 7, key="procedural:NPC/Girls/Amanda/InitAmanda.rpy:procedural_randint:475:1") - 1]
                if dad_name_reset:
                    dad = "Случайный негр" if dad_type == "Неизвестный негр" else "Случайный мужчина"
                if place_reset:
                    rand_place = procedural_randint(1, 6, key="procedural:NPC/Girls/Amanda/InitAmanda.rpy:procedural_randint:479:2")
                    if rand_place <= 3:
                        place = "inside"
                    elif rand_place == 4:
                        place = "mouth"
                    elif rand_place == 5:
                        place = "tits"
                    else:
                        place = "mouthface"
                self.add_sex_stat("sexacts", 1)
                cur_conc = people_to_int(self.sex_stat("ConceptionChance", 0), 0)
                if dad == "Вы":
                    cur_conc *= 3
                    self.mark_fucked(1)
                    if fun_awarded == 0:
                        player.condition.change("fun", 30)
                        fun_awarded = 1
                    player.intimacy.record_cum(current_game_day())
                    if place == "inside":
                        self.set_cum_state("cum_inside_you", 1)
                    elif place == "tits":
                        self.set_cum_state("cum_tits_you", 1)
                    elif place in ("face", "mouthface"):
                        self.set_cum_state("cum_face_you", 1)
                    elif place == "mouth":
                        self.set_cum_state("cum_mouth_you", 1)
                else:
                    if place == "inside":
                        self.set_cum_state("cum_inside_others", 1)
                    elif place == "tits":
                        self.set_cum_state("cum_tits_others", 1)
                    elif place in ("face", "mouthface"):
                        self.set_cum_state("cum_face_others", 1)
                    elif place == "mouth":
                        self.set_cum_state("cum_mouth_others", 1)
                    dad_info = people.get_info(dad)
                    if dad_info is not None:
                        dad_state = dad_info.ensure_sex_state()
                        dad_state["came_today"] = people_to_int(dad_state.get("came_today", 0), 0) + 1
                if procedural_randint(1, max(1, self.corruption * 3), key="procedural:NPC/Girls/Amanda/InitAmanda.rpy:procedural_randint:520:3") <= (2 if place == "inside" else 1) and self.corruption <= 70:
                    self.change_social(corruption_delta=1)
                if is_random:
                    cur_conc = int(cur_conc / 10)
                zalet = 0
                if place == "inside":
                    self.add_sex_stat("cuminside", 1)
                    if self.pregnancy_days() == 0:
                        if tavern_kitchen_fertility_bonus_active():
                            cur_conc += max(4, int(people_to_int(self.sex_stat("ConceptionChance", 0), 0) * 0.5))
                        cur_conc = min(cur_conc, 800)
                        if cur_conc > 0 and procedural_randint(1, 1000, key="procedural:NPC/Girls/Amanda/InitAmanda.rpy:procedural_randint:534:4") <= cur_conc:
                            self.set_sex_stat("pregnancy", 1)
                            self.set_sex_stat("pregfather", dad)
                            zalet = 1
                if str(dad).lower() == "eddie" and dad_type == "NPC":
                    dad_record = "Эдди"
                elif str(dad).lower() in ("legare", "месье легаре") and dad_type == "NPC":
                    dad_record = "Мессир Легаре"
                else:
                    dad_record = dad
                if not isinstance(getattr(self, "detailed_sex_history", None), list):
                    self.detailed_sex_history = []
                self.detailed_sex_history.append({
                    "RowId": len(self.detailed_sex_history) + 1,
                    "Day": people_to_int(current_game_day(), 0) + 1,
                    "GirlName": self.code_name,
                    "DudeName": str(dad_record or ""),
                    "DudeNameType": str(dad_type or ""),
                    "IsDudeRandom": is_random,
                    "CumTarget": place,
                    "Zalet": zalet,
                })
            return self.pregnancy_state()

        def birth_ready(self):
            state = self.pregnancy_state()
            return (
                people_to_int(current_game_day(), 0) > 0
                and people_to_int(state.get("pregnancy", 0), 0) >= 240
                and str(state.get("pregfather", "") or "") != ""
            )

        def apply_body_state(self):
            state = self.fertility_state()
            self.stats["PussyWetStart"] = max(people_to_int(self.stats.get("PussyWetStart", 0), 0), people_to_int(state.get("wet_bonus", 0), 0))
            return state

        def body_state_line(self):
            state = self.apply_body_state()
            phase = str(state.get("phase", "steady") or "steady")
            if phase == "horny":
                return "Аманда выглядит оживленнее обычного: в движениях больше тепла, а во взгляде чаще вспыхивает игривый интерес."
            if phase == "critical":
                return "Аманда держится тише обычного и выглядит утомленной."
            return ""

        def legare_intro_ready(self):
            return (
                self.legare_affection <= 0
                and not self.legare_forbidden
                and people_to_int(Alber.rel, 0) >= 0
            )

        def mark_legare_intro_seen(self):
            self.legare_affection = max(1, self.legare_affection)
            return self.var

        def has_given_night_bowl(self):
            return bool(self.night_bowl_given)

        def can_be_asked_for_night_bowl(self):
            return (
                player_has_soap_recipe_book()
                and not self.has_given_night_bowl()
                and player.item_count("night_bowl_001") <= 0
                and int(self.night_bowl_request_day) != int(current_game_day() or 0)
            )

        def can_be_asked_for_night_bowl_favor(self):
            return self.can_be_asked_for_night_bowl() and int(self.rel or 0) >= 7 and int(self.drunk or 0) > 0

        def night_bowl_success_chance(self, from_dance=False):
            friendship_value = int(self.rel or 0)
            chance_value = 20 + max(0, friendship_value - 4) * 8
            if from_dance and int(self.drunk or 0) > 0:
                chance_value += 20
            if friendship_value >= 10:
                chance_value = 100
            return max(5, min(100, int(chance_value or 0)))

        def night_bowl_request_result(self, from_dance=False):
            if not self.can_be_asked_for_night_bowl():
                return {"ok": False, "granted": False, "reason": "unavailable"}
            self.night_bowl_request_day = int(current_game_day() or 0)
            friendship_value = int(self.rel or 0)
            chance_value = self.night_bowl_success_chance(from_dance)
            granted = friendship_value >= 10 or procedural_randint(1, 100, "amanda_night_bowl_%s_%s" % (current_game_day(), int(from_dance))) <= chance_value
            if granted:
                player.add_item("night_bowl_001", 1)
                self.night_bowl_given = True
                return {"ok": True, "granted": True, "chance": chance_value}
            return {"ok": True, "granted": False, "chance": chance_value}

        def can_receive_fancy_night_bowl(self):
            return self.has_given_night_bowl() and not self.fancy_night_bowl_received and player.item_count("fancy_night_bowl_001") > 0

        def prefers_backyard_relief(self):
            return int(self.backyard_relief_preference or 0) == 1

        def pick_backyard_relief_preference(self):
            chance_value = 20 + int(self.rel or 0) * 4 + int(int(self.corruption or 0) / 5)
            if self.has_given_night_bowl():
                chance_value += 10
            chance_value = max(5, min(90, chance_value))
            self.backyard_relief_preference = 1 if procedural_randint(1, 100, "amanda_backyard_relief_%s" % current_game_day()) <= chance_value else 0
            return self.backyard_relief_preference

        def attic_busted(self):
            return threads["melissaBatProblem"].num >= 6

        def dress_change_has_options(self):
            if self.talked_today >= 2:
                return False
            if self.rel > 8 and int(self.sex_stat("orgasms_given", 0) or 0) >= 2:
                return True
            return self.rel > 8 and daily_events.exists("", "BuyDressTom") == 0 and daily_events.exists("amanda", "BuyDress") == 0 and int(calendar_v2.week or 0) != 6

        def legare_claims_first_friday_dance(self):
            return str(people.location("alber") or "") == "FridayDance" and str(people.location("clara") or "") != "FridayDance"

        def dress_change_other_saw_text(self, girl_name="amanda", agreed_to_redress=0):
            if int(agreed_to_redress or 0) != 1 or self.corruption < 50:
                return ""
            randvar = procedural_randint(1, 9, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:18:1")
            if str(people.location("liza") or "") != "TavernMain" and randvar == 4:
                randvar = procedural_randint(5, 7, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:20:2")
            if str(people.location("georgett") or "") != "TavernMain" and randvar == 3:
                randvar = procedural_randint(5, 7, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:22:3")
            if randvar == 1:
                if Sandra.corruption >= 35:
                    text = 'Обернувшись, вы вдруг встретились взглядом с Сандрой, наблюдающей за этой сценкой. Но она всего лишь усмехнулась, покачала головой и пошла по своим делам.'
                else:
                    text = 'Обернувшись, вы вдруг встретились взглядом с Сандрой, наблюдающей за этой сценкой. И увиденное ей явно не понравилось. Она подскочила и сердито заорала: "Значит Аманда становится шлюхой? Раздеваться при всех, ни стыда, ни совести!"\n"Сандра, успокойся," заступились вы за Аманду. У нее там просто что-то кололо, да так больно, что она и не сообразила где она."\nХоть и малоправдоподобная, но все-таки отмазка смутила Сандру и вы смогли заболтать тему.'
            elif randvar == 2:
                if Melissa.corruption >= 35:
                    text = 'Вы окинули взглядом трактир и увидели пораженную Мелиссу, заметившую Амандин стриптиз. Но увиденное ее совсем не шокировало, она понимающе улыбнулась Аманде и пошла дальше по своим делам.'
                else:
                    text = 'Вы окинули взглядом трактир и увидели пораженную Мелиссу, заметившую Амандин стриптиз. И этот стриптиз ее явно шокировал. Она подбежала к вам и воскликнула: "Аманда, ты что, совсем стыд потеряла?"\n"Знаешь что, то что ты старше, не дает тебе права кричать на меня," отвергла критику Аманда, и не слушая возмущенные писки Мелиссы, пошла как ни в чем ни бывало.'
            elif randvar == 3:
                text = 'Вы заметили, что за вами с улыбкой наблюдала Жоржетта и кивнули ей в ответ. А она тогда одобрительно подняла большой палец вверх.'
            elif randvar == 4:
                text = 'Вы заметили, что за подругой наблюдала Лизетта, одобрительно кивая.'
            elif randvar == 5:
                text = 'Из-за ближайшего стола послышался одобрительный свист, посетителям Амандин стриптиз пришелся по душе.'
            elif randvar == 6:
                text = 'Когда Аманда пошла в зал, то сразу пара посетителей, наверное заметивших ее стриптиз, ущипнули девчонку за мягкое место. Она довольно взвизгнула и побежала дальше.'
            elif randvar == 7:
                text = 'Один из посетителей наблюдал за этой сценкой с отвалившей челюстью. Аманда весело подмигнула ему и пошла к стойке.'
            else:
                text = ""
            if randvar <= 2:
                self.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_seen")
            if 5 <= randvar <= 7:
                self.apply_social_chance(0, 0, 0, 60, 1, 1, "dress_change_seen")
                player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 1
            return text


        def is_at(self, location_code):
            return str(people.location(self.code_name) or "") == str(location_code or "")

        def friday_dance_clarissa_absent(self):
            return not Clara.visible_at_friday_dance()

        def friday_dance_base_ready(self):
            return (
                self.is_at("FridayDance")
                and not self.left_friday_dance
                and people_to_int(rooms.get("FridayDance").dance_count, 0) < 5
                and people_to_int(rooms.get("FridayDance").step, 0) == 0
            )

        def friday_dance_legare_row(self):
            row_index = SexEvents.dance_index(self.code_name, "legare", rooms.get("FridayDance").dance_count)
            if row_index <= 0:
                return None
            return SexEvents.girl_dance[row_index - 1]

        def friday_dance_legare_table_ready(self):
            return self.friday_dance_legare_row() is not None

        def friday_dance_mc_table_ready(self):
            return self.friday_dance_legare_row() is None

        def legare_dance_advance_level(self):
            alber_friends = self.legare_affection
            amanda_corruption = people_to_int(self.corruption, 0)
            if alber_friends >= 10 and amanda_corruption >= 18:
                return 5
            if alber_friends >= 9 and amanda_corruption >= 15:
                return 4
            if alber_friends >= 7 and amanda_corruption >= 10:
                return 3
            if alber_friends >= 6 and amanda_corruption >= 6:
                return 2
            if alber_friends >= 5 and amanda_corruption >= 3:
                return 1
            return 0

        def legare_dance_sequence_ready(self, sequence, stage_kind=""):
            seq = people_to_int(sequence, 0)
            advance = self.legare_dance_advance_level()
            if seq <= 0:
                return self.legare_intro_ready()
            if seq == 1:
                return True
            if seq == 2:
                return advance >= 2
            if seq == 3:
                return advance >= 5
            if seq == 4:
                dance_row = self.friday_dance_legare_row()
                return dance_row is not None and people_to_int(dance_row.get("GoOut", 0), 0) == 1 and advance >= 5
            return False

        def dance_event_conditions_met(self, event_obj):
            partner = str(getattr(event_obj, "partner", "") or "")
            if partner == "legare_intro":
                return (
                    self.is_at("FridayDance")
                    and self.friday_dance_clarissa_absent()
                    and not self.left_friday_dance
                    and self.legare_dance_sequence_ready(getattr(event_obj, "sequence", 0), getattr(event_obj, "stage_kind", ""))
                )
            if not self.friday_dance_base_ready():
                return False
            if partner == "legare":
                return (
                    self.friday_dance_clarissa_absent()
                    and self.friday_dance_legare_table_ready()
                    and self.legare_dance_sequence_ready(getattr(event_obj, "sequence", 1), getattr(event_obj, "stage_kind", ""))
                )
            if partner == "mc":
                return self.friday_dance_mc_table_ready()
            return False

        def dynamic_roll(self, low_value=1, high_value=1, key=""):
            return procedural_randint(low_value, high_value, "amanda_dynamic_%s_%s_%s_%s" % (
                str(key or ""),
                people_to_int(current_game_day(), 0),
                people_to_int(calendar_v2.time_slot(), 0),
                self.var_int("dynamic_roll_salt", 0),
            ))

        def happy_confirm_text(self):
            roll_one = self.dynamic_roll(1, 4, "happy_confirm_1_%s" % int(self.warned_about_not_working))
            if roll_one == 1:
                p1 = '"Вот Стефанчик, и ты можешь быть разумным. Если захочешь," '
            elif roll_one == 2:
                p1 = '"Ну вот теперь ты говоришь дело," '
            elif roll_one == 3:
                p1 = '"Это ты мудро сказал, не то что прошлый раз," '
            else:
                p1 = '"Вот теперь сразу видно, то все обдумал и говоришь серьезно, а не истеришь как тогда," '

            roll_two = self.dynamic_roll(1, 3, "happy_confirm_2_%s" % int(self.warned_about_not_working))
            if roll_two == 1:
                p2 = "радостно ответила вам Аманда. "
            elif roll_two == 2:
                p2 = "обрадованно воскликнула Аманда. "
            else:
                p2 = "сказала Аманда, довольная своей маленькой победой. "
            return p1 + p2

        def sex_offer_reaction(self):
            reaction = 0
            rel = people_to_int(self.rel, 0)
            corr = people_to_int(self.corruption, 0)

            if self.var_int("prohibitliza", 0) or (self.legare_forbidden and self.legare_affection >= 5) or self.var_int("gloryscold", 0):
                if self.var_int("suckyou", 0) or self.var_int("fuckyou", 0):
                    if (rel >= 12 and corr >= 40) or corr >= 50:
                        reaction = 4
                        if corr >= 55 and self.dynamic_roll(1, 3, "sex_offer_warned_you") == 1:
                            reaction = 3
                    elif corr <= 25 and rel <= 10:
                        reaction = 2
                    elif corr <= 30 and rel <= 5:
                        reaction = 2
                    else:
                        reaction = 3
                else:
                    if (rel >= 14 and corr >= 45) or corr >= 55:
                        reaction = 4
                        if corr >= 55 and self.dynamic_roll(1, 3, "sex_offer_warned_no_you") == 1:
                            reaction = 3
                    elif corr <= 30 and rel <= 12:
                        reaction = 2
                    elif corr <= 35 and rel <= 8:
                        reaction = 2
                    else:
                        reaction = 3
            else:
                if self.var_int("suckyou", 0) or self.var_int("fuckyou", 0):
                    if rel >= 2 and corr >= 45:
                        reaction = 4
                    elif rel >= 5 and corr >= 35:
                        reaction = 4
                    elif rel >= 10 and corr >= 25:
                        reaction = 4
                    elif rel >= 15 and corr >= 21:
                        reaction = 4
                    elif rel >= 2 and corr >= 35:
                        reaction = 1
                    elif rel >= 5 and corr >= 25:
                        reaction = 1
                    elif rel >= 10 and corr >= 21:
                        reaction = 1
                else:
                    if rel >= 5 and corr >= 45:
                        reaction = 4
                    elif rel >= 10 and corr >= 35:
                        reaction = 4
                    elif rel >= 15 and corr >= 25:
                        reaction = 4
                    elif rel >= 5 and corr >= 35:
                        reaction = 1
                    elif rel >= 10 and corr >= 25:
                        reaction = 1
            return reaction

        def legare_sex_type(self):
            if not self.performed_oral_with_legare:
                sex_type = 0
            elif not self.had_sex_with_legare:
                if self.sex_stat("virginity", True):
                    if self.legare_affection >= 15 and self.corruption >= 35 and people_to_int(self.sex_stat("sexacts", 0), 0) >= 5:
                        sex_type = 2
                    else:
                        sex_type = 1
                else:
                    if self.legare_affection >= 12 and self.corruption >= 32 and people_to_int(self.sex_stat("sexacts", 0), 0) >= 4:
                        sex_type = 3
                    else:
                        sex_type = 1
            elif (self.legare_affection >= 10 and self.corruption >= 30) or (self.legare_affection >= 5 and self.corruption >= 40):
                sex_type = 4
            else:
                sex_type = 1

            if self.pregnancy_days() >= 120 and sex_type == 3:
                sex_type = 4
            return sex_type

        def resolve_legare_let_go(self, use_forced_type=0, forced_type=0):
            if int(use_forced_type or 0) == 1:
                sex_type = int(forced_type or 0)
            else:
                sex_type = self.legare_sex_type()
                if sex_type == 2 and self.dynamic_roll(1, 6, "legare_let_go_type_2") <= 5:
                    sex_type = 1

            if sex_type <= 1:
                self.performed_oral_with_legare = True
                self.legare_affection += 1
                self.apply_social_chance(0, 0, 0, 40, 1, 1, "legare_dance_outcome")
                self.pregnancy_check("mouth", 1, "legare")
            elif sex_type == 2:
                self.had_sex_with_legare = True
                self.lost_virginity_to_legare = True
                self.set_sex_stat("virginity", False)
                self.legare_affection += 2
                self.apply_social_chance(0, 0, 0, 50, 1, 4, "legare_dance_outcome")
                if self.dynamic_roll(1, 3, "legare_let_go_first_sex_finish") <= 2:
                    self.legare_affection += 1
                    self.pregnancy_check("inside", 1, "legare")
                else:
                    self.legare_affection += 2
                    self.pregnancy_check("outside", 1, "legare")
            else:
                self.had_sex_with_legare = True
                self.apply_social_chance(0, 0, 0, 50, 1, 2, "legare_dance_outcome")
                if self.dynamic_roll(1, 3, "legare_let_go_sex_finish") <= 2:
                    self.legare_affection += 1
                    self.pregnancy_check("inside", 1, "legare")
                else:
                    self.legare_affection += 2
                    self.pregnancy_check("outside", 1, "legare")
            return sex_type

        def nesluh_value(self):
            bonus = 0
            if self.var_int("glorydeflower", 0) > 0 or self.var_int("fuckyou", 0) > 0:
                bonus += 6
            if self.var_int("gloryscold", 0) > 0:
                bonus -= 3
            if self.var_int("glorysuck", 0) > 0 or self.var_int("suckyou", 0) > 0:
                bonus += 3
            if self.var_int("glorywalkout", 0) > 0:
                bonus += 2
            if self.legare_affection >= 7:
                bonus += 1
            if self.legare_affection >= 9:
                bonus += 1
            if self.legare_affection >= 12:
                bonus += 2
            if self.corruption >= 23:
                bonus += 1
            if self.corruption >= 30:
                bonus += 2
            if self.corruption >= 40:
                bonus += 4
            if self.corruption >= 50:
                bonus += 3
            if self.performed_oral_with_legare:
                bonus += 2
            if self.had_sex_with_legare:
                bonus += 3
            if self.lost_virginity_to_legare:
                bonus += 3

            bonus = min(14, max(1, bonus))
            nesluh = 1 if self.dynamic_roll(1, 15, "nesluh_%s_%s" % (self.legare_affection, self.corruption)) <= bonus else 0
            if (self.var_int("glorydeflower", 0) or self.var_int("fuckyou", 0)) and nesluh == 1 and self.dynamic_roll(1, 4, "nesluh_deflower") <= 3:
                nesluh = 2
            elif (self.var_int("glorysuck", 0) or self.var_int("suckyou", 0)) and nesluh == 1 and self.dynamic_roll(1, 4, "nesluh_suck") <= 1:
                nesluh = 2
            return nesluh

        def lover_sex_calc(self, guy_name="", forced_type=0):
            guy = str(guy_name or "")
            if not guy:
                guy = RandomNameCode("male")

            sex_type = 0
            if self.corruption >= 57:
                sex_type = 2
            elif self.pregnancy_days() > 120:
                if self.corruption >= 42:
                    sex_type = 2
                elif self.corruption >= 40:
                    sex_type = 1
            elif self.corruption >= 45:
                if self.dynamic_roll(1, 3, "lover_calc_45") == 1:
                    sex_type = 1
                elif self.dynamic_roll(1, 9, "lover_calc_45_alt") <= 4:
                    sex_type = 2
            elif self.corruption >= 40:
                sex_type = 1

            if people_to_int(forced_type, 0) > 0:
                sex_type = people_to_int(forced_type, 0)
            if sex_type == 2 and self.dynamic_roll(1, 2, "lover_calc_variant") == 1:
                sex_type = 3

            if sex_type == 3:
                self.pregnancy_check("outside", 1, guy, 0, "Соседский парень")
                self.change_social(corruption_delta=1)
            elif sex_type == 2:
                self.pregnancy_check("inside", 1, guy, 0, "Соседский парень")
                self.change_social(corruption_delta=1)
            elif sex_type == 1:
                self.pregnancy_check("mouth", 1, guy, 0, "Соседский парень")
                self.change_social(corruption_delta=1)
            return sex_type

        def yell_not_work(self):
            renpy.say(None, "Не стерпев что Аманда отлынивает от работы, вы подскочили к ней, взяли за плечо и начали орать:")
            if self.warned_about_not_working:
                renpy.say(None, "\"Опять ты шляешься по улице вместо того, чтобы работать! А я ведь тебя предупреждал!\"")
                renpy.say(None, "\"Но перерыв...\" попыталась оправдаться Аманда.")
            else:
                renpy.say(None, "\"Ты что это по улице шляешься? У нас, между прочим, посетители есть.\"")
                renpy.say(None, "\"А что такого? У меня перерыв.\" ответила вам она.")
            renpy.say(None, "\"Не выдумывай! Нет у тебя никакого перерыва. А даже если бы и был, то считай что он уже закончился. Марш на работу!\"")

            self.warned_about_not_working = True
            if self.dynamic_roll(1, 3, "yell_not_work") == 1:
                renpy.say(None, "\"Нет так нет,\" недобро ответила вам она. \"Работать я работаю, как умею.\"")
                renpy.say(None, "И, напевая себе под нос: \"Так чего же нам стараться, поработаем с прохладцей,\" она пошла обратно.")
                self.skills["cooking"] = max(10, people_to_int(self.skills.get("cooking", 0), 0) - 3)
                self.skills["cleaning"] = max(10, people_to_int(self.skills.get("cleaning", 0), 0) - 3)
                self.skills["waitress"] = max(10, people_to_int(self.skills.get("waitress", 0), 0) - 3)
            else:
                renpy.say(None, "Расстроившись, но не найдя что вам возразить, Аманда пошлепала обратно в трактир.")

            self.change_social(friend_delta=(1 if self.rel >= 6 else -2))
            return 0

define AmandaStaticData = AmandaData()
default Amanda = AmandaInfo()

label InitAmanda:
    python:
        Amanda.initialize_new_game_state()
        people.register(AmandaStaticData, Amanda)
    return
