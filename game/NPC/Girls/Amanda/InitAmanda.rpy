# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    import random

    def amanda_has_given_night_bowl():
        return Amanda.var_int("gave_night_bowl", 0) == 1

    def amanda_can_be_asked_for_night_bowl():
        return (
            player_has_soap_recipe_book()
            and not amanda_has_given_night_bowl()
            and _player_item_count_by_id("night_bowl_001") <= 0
            and Amanda.var_int("night_bowl_request_day", -1) != int(dayspassed or 0)
        )

    def amanda_can_be_asked_for_night_bowl_favor():
        Drunk_safe = getattr(renpy.store, 'Drunk', {})
        return (
            amanda_can_be_asked_for_night_bowl()
            and int(Amanda.rel or 0) >= 7
            and int(Drunk_safe.get("amanda", 0) or 0) > 0
        )

    def amanda_night_bowl_success_chance(from_dance=False):
        Drunk_safe = getattr(renpy.store, 'Drunk', {})
        friendship_value = int(Amanda.rel or 0)
        chance_value = 20 + max(0, friendship_value - 4) * 8
        if from_dance and int(Drunk_safe.get("amanda", 0) or 0) > 0:
            chance_value += 20
        if friendship_value >= 10:
            chance_value = 100
        return max(5, min(100, int(chance_value or 0)))

    def amanda_night_bowl_request_result(from_dance=False):
        if not amanda_can_be_asked_for_night_bowl():
            return {"ok": False, "granted": False, "reason": "unavailable"}

        Amanda.set_var_int("night_bowl_request_day", dayspassed)
        friendship_value = int(Amanda.rel or 0)
        chance_value = amanda_night_bowl_success_chance(from_dance)
        granted = friendship_value >= 10 or random.randint(1, 100) <= chance_value
        if granted:
            _player_add_item_by_id("night_bowl_001", 1)
            Amanda.set_var_int("gave_night_bowl", 1)
            Amanda.set_var_int("night_bowl_window_seen_day", -1)
            return {"ok": True, "granted": True, "chance": chance_value}
        return {"ok": True, "granted": False, "chance": chance_value}

    def amanda_night_bowl_window_event_ready():
        return (
            amanda_has_given_night_bowl()
            and _player_item_count_by_id("night_bowl_001") > 0
            and (
                Amanda.var_int("got_fancy_night_bowl", 0) == 0
                or Amanda.var_int("prefers_backyard_relief", -1) == 1
            )
            and int(time or 0) >= 4
            and Amanda.var_int("night_bowl_window_seen_day", -1) != int(dayspassed or 0)
        )

    def amanda_can_receive_fancy_night_bowl():
        return (
            amanda_has_given_night_bowl()
            and Amanda.var_int("got_fancy_night_bowl", 0) == 0
            and _player_item_count_by_id("fancy_night_bowl_001") > 0
        )

    def amanda_prefers_backyard_relief():
        return Amanda.var_int("prefers_backyard_relief", -1) == 1

    def amanda_pick_backyard_relief_preference():
        sluttiness_safe = getattr(renpy.store, 'sluttiness', {})
        friendship_value = int(Amanda.rel or 0)
        sluttiness_value = int(sluttiness_safe.get("amanda", 0) or 0)
        chance_value = 20 + friendship_value * 4 + int(sluttiness_value / 5)
        if Amanda.var_int("gave_night_bowl", 0) == 1:
            chance_value += 10
        chance_value = max(5, min(90, chance_value))
        Amanda.set_var_int("prefers_backyard_relief", 1 if random.randint(1, 100) <= chance_value else 0)
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
            self.age = 18
            self.rel = 5
            self.relationship = self.rel
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
            self.schedule_source = AmandaStaticData.schedule_source
            self.schedule_uses_clock_minutes = True
            self.current_location = "TavernMain"
            self.talk_preferences = {
                "favorite_topics": ["fashion", "amanda_boys", "money", "sex_topics", "gossip"],
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
            self.relationship = self.rel
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
            self.reaction_state["last_reaction_day"] = people_to_int(dayspassed, 0)
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
            try:
                state = dict(amanda_ai_cycle_state() or {})
            except Exception:
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
            try:
                body = dict(amanda_ai_body_state_bonus() or {})
            except Exception:
                body = {}
            phase = str(cycle.get("phase", body.get("phase", "steady")) or "steady")
            cycle_day = people_to_int(cycle.get("day", body.get("cycle_day", 0)), 0)
            return {
                "phase": phase,
                "cycle_day": cycle_day,
                "fertility": cycle.get("fertility", 0.0),
                "desire": cycle.get("desire", cycle.get("horny", 0.0)),
                "rest": cycle.get("rest", 0.0),
                "safety": cycle.get("safety", 0.0),
                "need_bandage": people_to_int(body.get("need_bandage", 0), 0),
                "wet_bonus": people_to_int(body.get("wet_bonus", 0), 0),
                "arousal_bonus": people_to_int(body.get("arousal_bonus", 0), 0),
                "tags": list(body.get("tags", []) or []),
            }

        def pregnancy_state(self):
            return {
                "pregnancy": people_to_int(self.stats.get("pregnancy", 0), 0),
                "pregfather": str(self.stats.get("pregfather", "") or ""),
                "cuminside": people_to_int(self.stats.get("cuminside", 0), 0),
                "conception_chance": people_to_int(self.stats.get("ConceptionChance", 0), 0),
                "sexacts": people_to_int(self.stats.get("sexacts", 0), 0),
            }

        def pregnancy_check(self, cum_place, repeat_count=1, dad_name="Вы", is_dude_random=0, dad_name_type=""):
            PregnancyCheck(self.code_name, cum_place, repeat_count, dad_name, is_dude_random, dad_name_type)
            self.stats["pregnancy"] = people_to_int(pregnancy.get(self.code_name, self.stats.get("pregnancy", 0)), 0)
            self.stats["pregfather"] = str(pregfather.get(self.code_name, self.stats.get("pregfather", "")) or "")
            self.stats["cuminside"] = people_to_int(cuminside.get(self.code_name, self.stats.get("cuminside", 0)), 0)
            self.stats["ConceptionChance"] = people_to_int(ConceptionChance.get(self.code_name, self.stats.get("ConceptionChance", 0)), 0)
            self.stats["sexacts"] = people_to_int(sexacts.get(self.code_name, self.stats.get("sexacts", 0)), 0)
            return self.pregnancy_state()

        def birth_ready(self):
            state = self.pregnancy_state()
            return (
                people_to_int(dayspassed, 0) > 0
                and people_to_int(state.get("pregnancy", 0), 0) >= 240
                and str(state.get("pregfather", "") or "") != ""
            )

        def apply_body_state(self):
            try:
                return amanda_ai_apply_visible_body_state()
            except Exception:
                return self.fertility_state()

        def body_state_line(self):
            try:
                return str(amanda_ai_body_state_line() or "")
            except Exception:
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
                and people_to_int(FridayDancesCount, 0) < 5
                and people_to_int(DanceStep, 0) == 0
            )

        def friday_dance_legare_table_ready(self):
            try:
                if self.var_int("legare_dance_pending", 0) == 1:
                    return True
                return people_to_int(CheckIfDanceExist("amanda", "legare", FridayDancesCount), 0) > 0
            except Exception:
                return False

        def friday_dance_mc_table_ready(self):
            try:
                return self.var_int("legare_dance_pending", 0) == 0 and people_to_int(CheckIfDanceExist("amanda", "legare", FridayDancesCount), 0) <= 0
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

define AmandaStaticData = AmandaData()
default Amanda = AmandaInfo()

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
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernMain", mode="morning"), priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernKitchen", mode="morning"), priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernStorage", mode="morning"), priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="Backyard", mode="morning"), priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernAmandaRoom", mode="morning"), priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_hall"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="FridayDance", mode="friday_evening"), priority=250, label="friday_dance"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernAmandaRoom", mode="sunday"), priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="Backyard", mode="sunday"), priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernMain", mode="sunday"), priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernKitchen", mode="sunday"), priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_sync_currentloc(GirlName)

    return
