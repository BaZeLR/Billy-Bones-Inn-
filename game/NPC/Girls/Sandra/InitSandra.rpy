# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitSandra:
    python:
        Sandra.initialize_new_game_state()
        people.register(SandraStaticData, Sandra)

    return

init python:
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
            self.image_manifest = {
                "kitchen": {
                    "work": [
                        "images/sandra/tavern/kitchen_sandra_0.jpg",
                        "images/sandra/tavern/kitchen_sandra_1.jpg",
                        "images/sandra/tavern/kitchen_sandra_2.jpg",
                        "images/sandra/tavern/kitchen_sandra_3.jpg",
                        "images/sandra/tavern/kitchen_sandra_4.jpg",
                    ],
                },
                "tavern": {
                    "hall_cleaning": ["images/sandra/tavern/cleaning1.jpg"],
                    "waitress": [
                        "images/sandra/tavern/waitress1.jpg",
                        "images/sandra/tavern/waitress2.jpg",
                        "images/sandra/tavern/waitress3.jpg",
                        "images/sandra/tavern/waitress4.jpg",
                    ],
                },
                "outfit_reward": {
                    "show": ["images/sandra/portrait4.jpg"],
                    "handjob": ["images/sandra/thanks/player_room_1.jpg"],
                    "handjob_finish": ["images/sandra/thanks/player_room_sandra_1.png"],
                    "oral": ["images/sandra/portrait3.jpg"],
                    "oral_finish": ["images/sandra/portrait4.jpg"],
                },
            }

    class SandraInfo(Girl):
        """Sandra runtime: household authority, chore rewards, room access."""
        talk_label = "IntSandraTalk"
        unknown_name = "Незнакомка"

        def __init__(self):
            super().__init__("sandra")
            self.code_name = "sandra"
            self.data = SandraStaticData
            self.rel = 5
            self.openness = 0
            self.corruption = 20
            self.known = True
            self.knows_molodost = False
            self.revealing_dress_code = ""

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
                "jobkitchentomorrow": 1,
                "jobcleaningtomorrow": 0,
                "jobwaitresstomorrow": 0,
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
        def update(self):
            super(SandraInfo, self).update()
            self.data = SandraStaticData
            return self

        def initialize_new_game_state(self):
            self.data = SandraStaticData
            self.known = True
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

define SandraStaticData = SandraData()
default Sandra = SandraInfo()
