# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    class BeckyData(PeopleData):
        code_name = "becky"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Бекки",
                fullname="Ребекка Блэнкеншип",
                genitive="Бекки",
                dative="Бекки",
                default_location="",
                description="Вдова Блэнкеншип, для друзей Бекки, высокая рыжеволосая женщина с полной грудью, чуть младше сорока лет.",
                gift_preferences=["soap_001", "wild_rose_001", "pig_lard_001", "libido_tincture_001", "drink_ale_001"],
            )
            # Original Becky init only defines age 36. This keeps that age at game start until a canonical birthday is written.
            self.birth_date = {"day": 1, "period": 1, "cycle": 1064}
            self.card_image = "images/becky/becky_card.jpg"
            self.schedule_source = "schedules/becky.json"

    class BeckyInfo(Girl):
        """Becky runtime: grocery work, home visits, Eddie, church, Sherwood trade, pregnancy."""
        talk_label = "IntBeckyTalk"
        unknown_name = "Незнакомка"

        def __init__(self):
            super().__init__("becky")
            self.code_name = "becky"
            self.data = BeckyStaticData
            self.rel = 0
            self.openness = 0
            self.corruption = 25
            self.known = True
            self.left_dances = 0
            self.home_visit_stage = 0
            self.inga_sex_greeting_seen = False
            self.uninvited_visit_scolded = False
            self.home_front_checked_today = False
            self.home_sex_unlocked = False
            self.eddie_georgett_stage = 0
            self.eddie_home_visit_state = 0
            self.open_oral_stage = 0
            self.home_visit_count = 0
            self.talked_about_eddie = False
            self.georgett_mentioned = False
            self.eddie_intervention_reaction = 0
            self.priest_advice_stage = 0
            self.gerhard_talk_stage = 0
            self.asked_about_eddie_sex_stage = 0
            self.eddie_join_stage = 0
            self.eddie_join_failures = 0
            self.eddie_robbed_day = 0
            self.knows_blackwood = False
            self.sherwood_suspicion = 0
            self.trade_offer_stage = 0
            self.sherwood_warning_stage = 0
            self.asked_about_elf_trade = False
            self.fingal_connection_clarified = False
            self.admitted_sherwood_stage = 0
            self.robin_robbery_stage = 0
            self.robbery_consolation_count = 0
            self.sandra_kitchen_visit_period = 0
            self.last_store_orgasm_day = -1
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
                "kids": 5,
                "beauty": 45,
                "sexacts": 5352,
                "cuminside": 3593,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 5,
                "PussyWetStart": 25,
                "virginity": False,
                "breastfeed": 0,
                "orgasms_given": 0,
            }
            self.skills = {
                "cooking": 70,
                "cleaning": 50,
                "waitress": 40,
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
            self.gift_preferences = list(BeckyStaticData.gift_preferences)
            self.talk_preferences = {
                "favorite_topics": ["family", "husband", "eddie", "inga", "sherwood"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["openworkdress", "simplebra", "simplepanties", "blackstockings", "simpleshoes"],
                "gifted": [],
                "current_dress": "openworkdress",
                "current_underwear": {
                    "bra": "simplebra",
                    "panties": "simplepanties",
                    "legs": "blackstockings",
                    "shoes": "simpleshoes",
                },
            }
        def update(self):
            super(BeckyInfo, self).update()
            self.data = BeckyStaticData
            return self

        def interaction_visible(self, room_code=""):
            room_key = str(room_code or "").strip()
            if room_key == "BeckyHome":
                return True
            if room_key == "BeckyHomeFront":
                return rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances"
            return super(BeckyInfo, self).interaction_visible(room_key)

        def action_data(self, where_id=""):
            data = super(BeckyInfo, self).action_data(where_id)
            if str(where_id or "").strip() == "GroceryStore":
                if not self.known:
                    data["title"] = "Торговец"
                data["picture_path"] = grocery_store_grocer_picture(self.name)
                data["talk_picture"] = data["picture_path"]
            return data

        def initialize_new_game_state(self):
            return self

        def reset_daily(self, full=False):
            super(BeckyInfo, self).reset_daily(full)
            self.home_front_checked_today = False
            return self

        def add_corruption(self, amount=1, floor=0, cap=100):
            self.corruption = max(people_to_int(floor, 0), min(people_to_int(cap, 100), people_to_int(self.corruption, 0) + people_to_int(amount, 0)))
            return self.corruption

        def apply_social_gate(self, rel_gate=0, open_delta=0, rel_delta=0, corruption_gate=0, corruption_delta=0, fallback_rel_delta=0):
            if people_to_int(self.rel, 0) >= people_to_int(rel_gate, 0):
                self.add_relation(rel_delta)
            elif fallback_rel_delta:
                self.add_relation(fallback_rel_delta)
            if people_to_int(self.corruption, 0) >= people_to_int(corruption_gate, 0):
                self.add_corruption(corruption_delta)
            self.openness = max(0, min(20, people_to_int(self.openness, 0) + people_to_int(open_delta, 0)))
            return self

        def apply_social_roll(self, limit_friend, friend_chance, inc_decr_friends, limit_corruption, corruption_chance, inc_decr_corruption):
            friend_delta = people_to_int(inc_decr_friends, 0)
            corruption_delta = people_to_int(inc_decr_corruption, 0)
            positive_friend_chance = social_friend_roll_chance(friend_chance, self.code_name, True)
            negative_friend_chance = social_friend_roll_chance(friend_chance, self.code_name, False)
            corruption_roll_chance = max(1, people_to_int(corruption_chance, 1))
            roll_index = 0
            while friend_delta < 0:
                roll_index += 1
                if people_to_int(self.rel, 0) > people_to_int(limit_friend, 0) and procedural_randint(1, negative_friend_chance, "becky_social_friend_down_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_relation(-1, cap=100)
                friend_delta += 1
            while friend_delta > 0:
                roll_index += 1
                if people_to_int(self.rel, 0) < people_to_int(limit_friend, 0) and procedural_randint(1, positive_friend_chance, "becky_social_friend_up_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_relation(1, cap=100)
                friend_delta -= 1
            while corruption_delta < 0:
                roll_index += 1
                if people_to_int(self.corruption, 0) > people_to_int(limit_corruption, 0) and procedural_randint(1, corruption_roll_chance, "becky_social_corruption_down_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_corruption(-1)
                corruption_delta += 1
            while corruption_delta > 0:
                roll_index += 1
                if people_to_int(self.corruption, 0) < people_to_int(limit_corruption, 0) and procedural_randint(1, corruption_roll_chance, "becky_social_corruption_up_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_corruption(1)
                corruption_delta -= 1
            return self

        def dress_change_flags(self, girl_name="becky"):
            girl_key = str(girl_name or self.code_name)
            can_offer_bra_off = self.stats.get("orgasms_given", 0) >= 2 and self.rel > 8 and self.has_bra() and self.talk_count() < 2
            can_offer_panties_off = self.stats.get("orgasms_given", 0) >= 2 and self.rel > 8 and self.has_panties() and self.talk_count() < 2
            can_shame = self.stats.get("orgasms_given", 0) >= 2 and self.rel > 8 and self.talk_count() < 2
            can_buy = (
                self.rel > 8
                and daily_events.exists("", "BuyDressTom", "") == 0
                and daily_events.exists(girl_key, "BuyDress", "") == 0
                and self.talk_count() < 2
                and int(calendar_v2.week or 0) != 6
            )
            return {
                "can_offer_bra_off": bool(can_offer_bra_off),
                "can_offer_panties_off": bool(can_offer_panties_off),
                "can_shame": bool(can_shame),
                "can_buy": bool(can_buy),
            }

        def dress_change_has_options(self, girl_name="becky"):
            return any(bool(value) for value in self.dress_change_flags(girl_name).values())

        def dress_change_other_saw_text(self, girl_name="becky", agreed_to_redress=0):
            if int(agreed_to_redress or 0) != 1 or self.corruption < 45:
                return ""
            randvar = procedural_randint(1, 6, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:71:1")
            if randvar == 1:
                text = "Какой-то мужик, зашедший за чем-то в лавку, наблюдал за этой сценкой с отвалившей челюстью. Бекки подмигнула ему и стала перекладывать овощи на прилавке как ни в чем не бывало."
            elif randvar == 2:
                text = "Глаза у какой-то девицы, заглянувшей в лавку за покупками, расширились от такого зрелища, но под конец она с одобрением кивнула вдове."
            elif randvar == 3:
                text = 'Какая-то мать семейства, заглянувшая в лавку миссис Блэнкеншип за зеленью, назидательно сказала своим двум дочкам, указывая на Бекки: "Вот видите как нужно парней привлекать, а вы все \'это платье слишком смелое\' и прочую чушь, так у меня в девках и проходите, коли за ум не возьметесь."'
            else:
                text = ""
            if randvar <= 3:
                self.apply_social_roll(0, 0, 0, 60, 2, 1)
            return text

        def can_trigger_after_sermon_event(self):
            return people_to_int(self.priest_advice_stage, 0) > 0

        def is_visibly_pregnant(self):
            return self.pregnancy_days() >= 120

        def can_drink_wine(self):
            return self.pregnancy_days() <= 30

        def store_lover_modest_reaction(self):
            return (people_to_int(self.corruption, 0) <= 45 or people_to_int(self.rel, 0) < 10) and people_to_int(self.corruption, 0) <= 55

        def mark_store_orgasm_today(self):
            self.last_store_orgasm_day = people_to_int(current_game_day(), 0)
            return self.last_store_orgasm_day

        def has_bra(self):
            return str(self.wardrobe.get("current_underwear", {}).get("bra", "") or "") != ""

        def set_default_bra(self, item_id):
            self.wardrobe.setdefault("current_underwear", {})["bra"] = str(item_id or "")
            return self

        def set_default_panties(self, item_id):
            self.wardrobe.setdefault("current_underwear", {})["panties"] = str(item_id or "")
            return self

        def friday_dance_base_ready(self):
            if not rooms.get("FridayDance").is_open():
                return False
            location_now = str(people.location("becky") or "")
            return (
                location_now in ("FridayDance", "MarketPlace")
                and people_to_int(self.left_dances, 0) == 0
                and people_to_int(rooms.get("FridayDance").dance_count, 0) < 5
                and people_to_int(rooms.get("FridayDance").step, 0) == 0
            )

        def dance_event_conditions_met(self, event_obj):
            partner = str(getattr(event_obj, "partner", "") or "")
            if partner == "mc":
                return self.friday_dance_base_ready()
            return False

define BeckyStaticData = BeckyData()
default Becky = BeckyInfo()

label InitBecky:
    python:
        Becky.initialize_new_game_state()
        people.register(BeckyStaticData, Becky)
    return
