        npc_schedule_sync_currentloc(GirlName)            self.current_location = "TavernMain"        def var_int(self, key, default=0):
            return people_to_int(self.ensure_story_defaults().get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()[str(key or "")] = people_to_int(value, 0)
            return self.var[str(key or "")]
            self.fertility_cycle = {
                "cycle_day": 0,
                "cycle_length": 28,
                "fertile_window_start": 11,
                "fertile_window_end": 16,
                "last_updated_day": None,
            }        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()[key] = value
            return value
            self.schedule_source = AmandaStaticData.schedule_source            self.schedule_source = AmandaStaticData.schedule_source
            self.current_location = "TavernMain"            self.relationship = self.rel            self.relationship = self.rel        npc_schedule_sync_currentloc(GirlName)            self.current_location = "TavernMain"        def var_int(self, key, default=0):
                npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_hall"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=amanda_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )

    return people_to_int(self.ensure_story_defaults().get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()[str(key or "")] = people_to_int(value, 0)
            return self.var[str(key or "")]
            self.fertility_cycle = {
                "cycle_day": 0,
                "cycle_length": 28,
                "fertile_window_start": 11,
                "fertile_window_end": 16,
                "last_updated_day": None,
            }        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()[key] = value
            return value
            self.schedule_source = AmandaStaticData.schedule_source            self.schedule_source = AmandaStaticData.schedule_source
            self.current_location = "TavernMain"            self.relationship = self.rel            self.relationship = self.rel        npc_schedule_sync_currentloc(GirlName)            self.current_location = "TavernMain"        def var_int(self, key, default=0):
                npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_hall"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=amanda_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )

    return people_to_int(self.ensure_story_defaults().get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()[str(key or "")] = people_to_int(value, 0)
            return self.var[str(key or "")]
            self.fertility_cycle = {
                "cycle_day": 0,
                "cycle_length": 28,
                "fertile_window_start": 11,
                "fertile_window_end": 16,
                "last_updated_day": None,
            }        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()[key] = value
            return value
            self.schedule_source = AmandaStaticData.schedule_source            self.schedule_source = AmandaStaticData.schedule_source
            self.current_location = "TavernMain"            self.relationship = self.rel            self.relationship = self.rel# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def amanda_has_given_night_bowl():
            npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_hall"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=amanda_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )

    return Amanda.var_int("gave_night_bowl", 0) == 1

    def amanda_can_be_asked_for_night_bowl():
        return (
            player_has_soap_recipe_book()
            and not amanda_has_given_night_bowl()
            and player.item_count("night_bowl_001") <= 0
            and Amanda.var_int("night_bowl_request_day", -1) != int(current_game_day() or 0)
        )

    def amanda_can_be_asked_for_night_bowl_favor():
        return (
            amanda_can_be_asked_for_night_bowl()
            and int(Amanda.rel or 0) >= 7
            and int(Amanda.drunk or 0) > 0
        )

    def amanda_night_bowl_success_chance(from_dance=False):
        friendship_value = int(Amanda.rel or 0)
        chance_value = 20 + max(0, friendship_value - 4) * 8
        if from_dance and int(Amanda.drunk or 0) > 0:
            chance_value += 20
        if friendship_value >= 10:
            chance_value = 100
        return max(5, min(100, int(chance_value or 0)))

    def amanda_night_bowl_request_result(from_dance=False):
        if not amanda_can_be_asked_for_night_bowl():
            return {"ok": False, "granted": False, "reason": "unavailable"}

        Amanda.set_var_int("night_bowl_request_day", current_game_day())
        friendship_value = int(Amanda.rel or 0)
        chance_value = amanda_night_bowl_success_chance(from_dance)
        granted = friendship_value >= 10 or procedural_randint(1, 100, "amanda_night_bowl_%s_%s" % (current_game_day(), int(from_dance))) <= chance_value
        if granted:
            player.add_item("night_bowl_001", 1)
            Amanda.set_var_int("gave_night_bowl", 1)
            Amanda.set_var_int("night_bowl_window_seen_day", -1)
            return {"ok": True, "granted": True, "chance": chance_value}
        return {"ok": True, "granted": False, "chance": chance_value}

    def amanda_night_bowl_window_event_ready():
        return (
            amanda_has_given_night_bowl()
            and player.item_count("night_bowl_001") > 0
            and (
                Amanda.var_int("got_fancy_night_bowl", 0) == 0
                or Amanda.var_int("prefers_backyard_relief", -1) == 1
            )
            and int(time or 0) >= 4
            and Amanda.var_int("night_bowl_window_seen_day", -1) != int(current_game_day() or 0)
        )

    def amanda_can_receive_fancy_night_bowl():
        return (
            amanda_has_given_night_bowl()
            and Amanda.var_int("got_fancy_night_bowl", 0) == 0
            and player.item_count("fancy_night_bowl_001") > 0
        )

    def amanda_prefers_backyard_relief():
        return Amanda.var_int("prefers_backyard_relief", -1) == 1

    def amanda_pick_backyard_relief_preference():
        friendship_value = int(Amanda.rel or 0)
        sluttiness_value = int(Amanda.corruption or 0)
        chance_value = 20 + friendship_value * 4 + int(sluttiness_value / 5)
        if Amanda.var_int("gave_night_bowl", 0) == 1:
            chance_value += 10
        chance_value = max(5, min(90, chance_value))
        Amanda.set_var_int("prefers_backyard_relief", 1 if procedural_randint(1, 100, "amanda_backyard_relief_%s" % current_game_day()) <= chance_value else 0)
        return Amanda.var_int("prefers_backyard_relief", 0)

init python:
    def amanda_story_defaults():
        return {
            "lizafriends": 0,
            "prohibitliza": 0,
            "alberfriends": 0,
            "albernowdances": 0,
            "legare_dance_pending": 0,
            "alberdanceadvance": 0,
            "legare_dance_thread_stage": 0,
            "legare_dance_private_seen": 0,
            "leftdances": 0,
            "alberprohibit": 0,
            "LegareGo": 0,
            "EscapeUnnoticed": 0,
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
            "knowlegaresex": 0,
            "sawlegaresex": 0,
            "sucklegare": 0,
            "fucklegare": 0,
            "deflowerlegare": 0,
            "knowdeflowerlegare": 0,
            "beddeflower": 0,
            "kickyoufromroom": 0,
            "kickyoufromroomcount": 0,
            "kickedwithmomhelp": 0,
            "knowyousawlegaresex": 0,
            "knowyouseesex": 0,
            "warnnotwork": 0,
            "sawwithguys": 0,
            "prohibitwithguys": 0,
            "askzalettoday": 0,
            "MomDressComplaint": 0,
            "gave_night_bowl": 0,
            "night_bowl_request_day": -1,
            "night_bowl_window_seen_day": -1,
            "got_fancy_night_bowl": 0,
            "prefers_backyard_relief": -1,
            "attic_window_busted": 0,
            "attic_window_breakfast_bj_day": -1,
            "attic_window_morning_day": -1,
            "attic_mock_response_day": -1,
            "attic_mock_stopped": 0,
            "attic_mock_exposed": 0,
            "breakfast_tease_day": -1,
            "revealing_dress_request_seen": 0,
            "revealing_dress_ordered": 0,
            "revealing_dress_code": "",
            "dress_request_satisfied": 0,
            "attention_hint_day": -1,
            "beauty_help_terms_accepted": 0,
            "night_tease_seen": 0,
            "night_tease_scene_active": 0,
            "mc_dance_after_seen": 0,
            "mc_dance_makeout_seen": 0,
            "mc_dance_sex_seen": 0,
            "mc_dance_private_walks": 0,
            "mc_dance_last_day": -1,
            "tavern_seduction_seen_day": -1,
            "legare_tavern_visit_seen_day": -1,
            "street_legare_sighting_seen_day": -1,
            "street_lover_encounter_seen_day": -1,
            "liza_talk_seen_day": -1,
            "liza_glory_hint_seen_day": -1,
            "glory_liza_invite_seen": 0,
            "glory_liza_invite_day": -1,
            "liza_glory_invite_event_seen_day": -1,
            "glory_last_event_day": -1,
            "glory_tavern_aftermath_seen_day": -1,
            "night_after_glory_seen_day": -1,
            "body_state_stamp": "",
            "cycle_phase": "steady",
            "cycle_day": 0,
            "needs_bandage": 0,
            "need_blocked": 0,
        }

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
                default_location="TavernMain",
                description="Аманда - молодая девушка. У нее очень светлая кожа, белокурые волосы и голубые глаза. Ее груди небольшие, размера А.",
                gift_preferences=["wild_rose_001", "soap_001", "berries_001", "energy_tea_001", "drink_ale_001"],
            )
            self.birth_date = {"day": 10, "period": 9, "cycle": 1082}
            self.card_image = "images/amanda/amanda_card.jpg"
            self.schedule_source = "schedules/amanda.json"

    class AmandaInfo(Girl):
        """Amanda runtime: tavern household, Legare path, social state, body state."""
        unknown_name = "Незнакомка"
        uses_own_var_state = True

        def __init__(self):
            super().__init__("amanda")
            self.code_name = "amanda"
            self.data = AmandaStaticData
            self.rel = 5
            self.openness = 3
            self.corruption = 0
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

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in amanda_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def initialize_new_game_state(self):
            self.ensure_story_defaults()
            self.publish_wardrobe_state()
            return self

        def reset_daily(self, full=False):
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            return self

        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()[key] = value
            return value

        def decision_profile(self):
            return build_girl_decision_profile(self.code_name)

        def decide(self, action_name="", profile=None, roll=None):
            result = girl_decide(self.code_name, action_name, profile, roll)
            self.record_reaction(action_name, str(dict(result or {}).get("reaction", "neutral") or "neutral"), None, result)
            return result

        def decision_good_probability(self, action_name="", profile=None):
            return girl_decision_good_probability(self.code_name, action_name, profile)

        def mana_bad_probability(self):
            return max(0.0, min(1.0, 1.0 - (float(people_to_int(self.mana, 0)) / 100.0)))

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

        def reward_need_fulfilled(self, amount=1, reason="need_fulfilled"):
            return self.change_mana(abs(people_to_int(amount, 1)), reason)

        def punish_need_unfulfilled(self, amount=1, reason="need_unfulfilled"):
            return self.change_mana(-abs(people_to_int(amount, 1)), reason)

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

        def record_reaction(self, action_name="", reaction="", score=None, context=None):
            reaction_key = str(reaction or "neutral")
            score_value = people_to_int(score, girl_decision_reaction_score(reaction_key))
            self.reaction_state["last_reaction"] = reaction_key
            self.reaction_state["last_reaction_day"] = people_to_int(current_game_day(), 0)
            self.reaction_state["last_reaction_context"] = str(action_name or "")
            self.reaction_state["last_reaction_score"] = score_value
            self.reaction_state["pending_decision"] = ""
            self.reaction_log.append({
                "day": self.reaction_state["last_reaction_day"],
                "action": str(action_name or ""),
                "reaction": reaction_key,
                "score": score_value,
            })
            if len(self.reaction_log) > 20:
                self.reaction_log = self.reaction_log[-20:]
            return score_value

        def last_decision_reaction(self, action_name=""):
            action_key = str(action_name or "").strip().lower()
            if action_key:
                return dict(GirlDecisionLast.get("%s:%s" % (self.code_name, action_key), {}) or {})
            if self.reaction_log:
                return dict(self.reaction_log[-1])
            return {}

        def apply_decision_reaction(self, decision=None, mana_reason="decision"):
            row = dict(decision or self.last_decision_reaction() or {})
            reaction = str(row.get("reaction", "neutral") or "neutral")
            action_name = str(row.get("action", "") or "")
            score = self.record_reaction(action_name, reaction, girl_decision_reaction_score(reaction), row)
            if score > 0:
                self.change_mana(1, mana_reason)
            elif score < 0:
                self.change_mana(-1, mana_reason)
            return score

        def cycle_state(self):
            state = dict(girl_decision_cycle_state(self.code_name) or {})
            phase = str(state.get("phase", "steady") or "steady")
            cycle_day = people_to_int(state.get("day", state.get("cycle_day", 0)), 0)
            self.fertility_cycle["cycle_day"] = cycle_day
            self.fertility_cycle["last_updated_day"] = people_to_int(dayspassed, 0)
            self.var["cycle_phase"] = phase
            self.var["cycle_day"] = cycle_day
            return state

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
                    dad_info = getPersonInfo(dad)
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
                        try:
                            if callable(tavern_kitchen_fertility_bonus_active) and tavern_kitchen_fertility_bonus_active():
                                cur_conc += max(4, int(people_to_int(self.sex_stat("ConceptionChance", 0), 0) * 0.5))
                        except Exception:
                            pass
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

        def morning_issue(self, time_value=None, hour_value=None):
            try:
                return str(household_morning_issue_type(self.code_name, time_value, hour_value) or "")
            except Exception:
                return ""

        def morning_sickness_active(self, location_name="TavernKitchen", time_value=None):
            try:
                return morning_sickness_daily_event_ready(self.code_name, location_name, time if time_value is None else time_value)
            except Exception:
                return False

        def legare_intro_ready(self):
            return (
                self.var_int("alberfriends", 0) <= 0
                and self.var_int("alberprohibit", 0) <= 0
                and people_to_int(Alber.rel, 0) >= 0
            )

        def mark_legare_intro_seen(self):
            self.set_var_int("alberfriends", max(1, self.var_int("alberfriends", 0)))
            return self.var

        def var_int(self, key, default=0):
            return people_to_int(self.ensure_story_defaults().get(str(key or ""), default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()[str(key or "")] = people_to_int(value, 0)
            return self.var[str(key or "")]

        def add_var_int(self, key, amount=1):
            return self.set_var_int(key, self.var_int(key, 0) + people_to_int(amount, 0))


        def is_at(self, location_code):
            try:
                return str(getLocation(self.code_name) or "") == str(location_code or "")
            except Exception:
                return False

        def friday_dance_clarissa_absent(self):
            try:
                return not bool(clara_visible_at_friday_dance())
            except Exception:
                return True

        def friday_dance_base_ready(self):
            try:
                if not friday_dance_slot_is_active():
                    return False
            except Exception:
                return False
            return (
                self.is_at("FridayDance")
                and self.var_int("leftdances", 0) == 0
                and people_to_int(friday_dance_count(), 0) < 5
                and people_to_int(DanceStep, 0) == 0
            )

        def friday_dance_legare_table_ready(self):
            try:
                if self.var_int("legare_dance_pending", 0) == 1:
                    return True
                return people_to_int(CheckIfDanceExist("amanda", "legare", friday_dance_count()), 0) > 0
            except Exception:
                return False

        def friday_dance_mc_table_ready(self):
            try:
                return self.var_int("legare_dance_pending", 0) == 0 and people_to_int(CheckIfDanceExist("amanda", "legare", friday_dance_count()), 0) <= 0
            except Exception:
                return True

        def legare_dance_advance_level(self):
            alber_friends = self.var_int("alberfriends", 0)
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
                return self.var_int("LegareGo", 0) == 1 and advance >= 5
            return False

        def dance_event_conditions_met(self, event_obj):
            partner = str(getattr(event_obj, "partner", "") or "")
            if partner == "legare_intro":
                return (
                    self.is_at("FridayDance")
                    and self.friday_dance_clarissa_absent()
                    and self.var_int("leftdances", 0) == 0
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
                people_to_int(time, 0),
                self.var_int("dynamic_roll_salt", 0),
            ))

        def happy_confirm_text(self):
            roll_one = self.dynamic_roll(1, 4, "happy_confirm_1_%s" % self.var_int("warnnotwork", 0))
            if roll_one == 1:
                p1 = '"Вот Стефанчик, и ты можешь быть разумным. Если захочешь," '
            elif roll_one == 2:
                p1 = '"Ну вот теперь ты говоришь дело," '
            elif roll_one == 3:
                p1 = '"Это ты мудро сказал, не то что прошлый раз," '
            else:
                p1 = '"Вот теперь сразу видно, то все обдумал и говоришь серьезно, а не истеришь как тогда," '

            roll_two = self.dynamic_roll(1, 3, "happy_confirm_2_%s" % self.var_int("warnnotwork", 0))
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

            if self.var_int("prohibitliza", 0) or (self.var_int("alberprohibit", 0) and self.var_int("alberfriends", 0) >= 5) or self.var_int("gloryscold", 0):
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
            if self.var_int("sucklegare", 0) == 0:
                sex_type = 0
            elif self.var_int("fucklegare", 0) == 0:
                if self.sex_stat("virginity", True):
                    if self.var_int("alberfriends", 0) >= 15 and self.corruption >= 35 and people_to_int(self.sex_stat("sexacts", 0), 0) >= 5:
                        sex_type = 2
                    else:
                        sex_type = 1
                else:
                    if self.var_int("alberfriends", 0) >= 12 and self.corruption >= 32 and people_to_int(self.sex_stat("sexacts", 0), 0) >= 4:
                        sex_type = 3
                    else:
                        sex_type = 1
            elif (self.var_int("alberfriends", 0) >= 10 and self.corruption >= 30) or (self.var_int("alberfriends", 0) >= 5 and self.corruption >= 40):
                sex_type = 4
            else:
                sex_type = 1

            if self.pregnancy_days() >= 120 and sex_type == 3:
                sex_type = 4
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
            if self.var_int("alberfriends", 0) >= 7:
                bonus += 1
            if self.var_int("alberfriends", 0) >= 9:
                bonus += 1
            if self.var_int("alberfriends", 0) >= 12:
                bonus += 2
            if self.corruption >= 23:
                bonus += 1
            if self.corruption >= 30:
                bonus += 2
            if self.corruption >= 40:
                bonus += 4
            if self.corruption >= 50:
                bonus += 3
            if self.var_int("sucklegare", 0) > 0:
                bonus += 2
            if self.var_int("fucklegare", 0) > 0:
                bonus += 3
            if self.var_int("deflowerlegare", 0) > 0:
                bonus += 3

            bonus = min(14, max(1, bonus))
            nesluh = 1 if self.dynamic_roll(1, 15, "nesluh_%s_%s" % (self.var_int("alberfriends", 0), self.corruption)) <= bonus else 0
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
            if self.var_int("warnnotwork", 0):
                renpy.say(None, "\"Опять ты шляешься по улице вместо того, чтобы работать! А я ведь тебя предупреждал!\"")
                renpy.say(None, "\"Но перерыв...\" попыталась оправдаться Аманда.")
            else:
                renpy.say(None, "\"Ты что это по улице шляешься? У нас, между прочим, посетители есть.\"")
                renpy.say(None, "\"А что такого? У меня перерыв.\" ответила вам она.")
            renpy.say(None, "\"Не выдумывай! Нет у тебя никакого перерыва. А даже если бы и был, то считай что он уже закончился. Марш на работу!\"")

            self.set_var_int("warnnotwork", 1)
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

init python:
    def amanda_schedule_match(location="", mode="morning"):
        target = str(location or "").strip()
        mode_key = str(mode or "morning").strip().lower()
        if mode_key == "morning":
            return str(_tavern_household_preopening_location("amanda") or "") == target
        if mode_key == "sunday":
            return str(_tavern_household_sunday_location("amanda") or "") == target
        if mode_key == "friday_evening":
            return str(_tavern_household_friday_evening_location("amanda") or "") == target
        return False

    def amanda_schedule_morning_hall():
        return amanda_schedule_match("TavernMain", "morning")

    def amanda_schedule_morning_kitchen():
        return amanda_schedule_match("TavernKitchen", "morning")

    def amanda_schedule_morning_storage():
        return amanda_schedule_match("TavernStorage", "morning")

    def amanda_schedule_morning_backyard():
        return amanda_schedule_match("Backyard", "morning")

    def amanda_schedule_morning_room():
        return amanda_schedule_match("TavernAmandaRoom", "morning")

    def amanda_schedule_friday_dance():
        return amanda_schedule_match("FridayDance", "friday_evening")

    def amanda_schedule_sunday_room():
        return amanda_schedule_match("TavernAmandaRoom", "sunday")

    def amanda_schedule_sunday_backyard():
        return amanda_schedule_match("Backyard", "sunday")

    def amanda_schedule_sunday_hall():
        return amanda_schedule_match("TavernMain", "sunday")

    def amanda_schedule_sunday_kitchen():
        return amanda_schedule_match("TavernKitchen", "sunday")

init python:
    def amanda_schedule_match(location="", mode="morning"):
        target = str(location or "").strip()
        mode_key = str(mode or "morning").strip().lower()
        if mode_key == "morning":
            return str(_tavern_household_preopening_location("amanda") or "") == target
        if mode_key == "sunday":
            return str(_tavern_household_sunday_location("amanda") or "") == target
        if mode_key == "friday_evening":
            return str(_tavern_household_friday_evening_location("amanda") or "") == target
        return False

    def amanda_schedule_morning_hall():
        return amanda_schedule_match("TavernMain", "morning")

    def amanda_schedule_morning_kitchen():
        return amanda_schedule_match("TavernKitchen", "morning")

    def amanda_schedule_morning_storage():
        return amanda_schedule_match("TavernStorage", "morning")

    def amanda_schedule_morning_backyard():
        return amanda_schedule_match("Backyard", "morning")

    def amanda_schedule_morning_room():
        return amanda_schedule_match("TavernAmandaRoom", "morning")

    def amanda_schedule_friday_dance():
        return amanda_schedule_match("FridayDance", "friday_evening")

    def amanda_schedule_sunday_room():
        return amanda_schedule_match("TavernAmandaRoom", "sunday")

    def amanda_schedule_sunday_backyard():
        return amanda_schedule_match("Backyard", "sunday")

    def amanda_schedule_sunday_hall():
        return amanda_schedule_match("TavernMain", "sunday")

    def amanda_schedule_sunday_kitchen():
        return amanda_schedule_match("TavernKitchen", "sunday")

init python:
    def amanda_schedule_match(location="", mode="morning"):
        target = str(location or "").strip()
        mode_key = str(mode or "morning").strip().lower()
        if mode_key == "morning":
            return str(_tavern_household_preopening_location("amanda") or "") == target
        if mode_key == "sunday":
            return str(_tavern_household_sunday_location("amanda") or "") == target
        if mode_key == "friday_evening":
            return str(_tavern_household_friday_evening_location("amanda") or "") == target
        return False

    def amanda_schedule_morning_hall():
        return amanda_schedule_match("TavernMain", "morning")

    def amanda_schedule_morning_kitchen():
        return amanda_schedule_match("TavernKitchen", "morning")

    def amanda_schedule_morning_storage():
        return amanda_schedule_match("TavernStorage", "morning")

    def amanda_schedule_morning_backyard():
        return amanda_schedule_match("Backyard", "morning")

    def amanda_schedule_morning_room():
        return amanda_schedule_match("TavernAmandaRoom", "morning")

    def amanda_schedule_friday_dance():
        return amanda_schedule_match("FridayDance", "friday_evening")

    def amanda_schedule_sunday_room():
        return amanda_schedule_match("TavernAmandaRoom", "sunday")

    def amanda_schedule_sunday_backyard():
        return amanda_schedule_match("Backyard", "sunday")

    def amanda_schedule_sunday_hall():
        return amanda_schedule_match("TavernMain", "sunday")

    def amanda_schedule_sunday_kitchen():
        return amanda_schedule_match("TavernKitchen", "sunday")

label InitAmanda:
    python:
        GirlName = Amanda.code_name
        peopleData[GirlName] = AmandaStaticData
        Amanda.initialize_new_game_state()
        peopleInfo[GirlName] = Amanda
        if Amanda not in girls:
            girls.append(Amanda)
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_hall, priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_kitchen, priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_storage, priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_backyard, priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=amanda_schedule_morning_room, priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_hall"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=amanda_schedule_friday_dance, priority=250, label="friday_dance"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_room, priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_backyard, priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_hall, priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=amanda_schedule_sunday_kitchen, priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
    return
