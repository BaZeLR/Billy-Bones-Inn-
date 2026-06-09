# Draft only. This file is not loaded by Ren'Py because it lives under devdocs.
# Purpose: reusable girl data/info blueprint for the Amanda V2 model.
#
# Ownership contract:
# - GirlData owns immutable/static identity, base stats, base wardrobe, gift preferences,
#   schedule source metadata, and story-default seeds.
# - GirlInfo owns save/runtime state: age, daily social flags, current mood/reaction,
#   hidden mana reaction model, fertility/pregnancy/birth state, current energy,
#   current wardrobe, current location, birthday knowledge, and story var.
# - `code_name` is the unique logic key used everywhere: "amanda", "melissa", etc.
# - Schedule files use hidden clock-minute intervals. Normal HUD displays fantasy
#   time-slot names only, not real clock text.

init python:
    class GirlDataBlueprint(PeopleData):
        code_name = ""

        def __init__(
            self,
            code_name,
            display_name,
            genitive,
            dative,
            starting_age,
            description,
            default_location,
            base_stats=None,
            base_clothing=None,
            base_jobs=None,
            gift_preferences=None,
            story_defaults=None,
            talk_preferences=None,
            schedule_source=None,
        ):
            self.code_name = str(code_name or "").strip().lower()
            super().__init__(
                self.code_name,
                cname=display_name,
                fullname=display_name,
                genitive=genitive,
                dative=dative,
                default_location=default_location,
                description=description,
                gift_preferences=list(gift_preferences or []),
            )
            self.starting_age = int(starting_age or 0)
            self.birth_record = calendar_make_birth_record(self.starting_age)
            self.base_stats = dict(base_stats or {})
            self.base_clothing = dict(base_clothing or {})
            self.base_jobs = dict(base_jobs or {})
            self.story_defaults = dict(story_defaults or {})
            self.talk_preferences = dict(talk_preferences or {})
            self.schedule_source = schedule_source or ("schedules/%s.json" % self.code_name)
            self.schedule_uses_clock_minutes = True
            self.hud_time_display = "time_slot_only"

        def current_age(self):
            return calendar_age_from_birth_record(self.birth_record)

        def schedule_intervals(self):
            # Individual girls override this only in draft/prototype form.
            # Final runtime should load the JSON schedule by self.schedule_source.
            return []


    class GirlInfoBlueprint(Girl):
        code_name = ""

        def __init__(self, data, var=None):
            super().__init__(data.code_name, var=var)
            self.code_name = data.code_name
            self.name = data.code_name
            self.data = data

            self.age = data.starting_age
            self.relationship = int(data.base_stats.get("Friends", 0) or 0)
            self.openness = int(data.base_stats.get("otkroven", 0) or 0)
            self.corruption = int(data.base_stats.get("sluttiness", 0) or 0)
            self.known = False
            # Energy gates whether she can work, talk, flirt, fight, or recover.
            # Low energy does not decide text directly; it reduces reaction scores.
            self.energy = int(data.base_stats.get("energy", 100) or 100)
            self.energy_max = int(data.base_stats.get("energy_max", 100) or 100)

            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0

            # Rebellion is resistance to player authority or household discipline.
            # It rises from unfair control and lowers obedience/cooperation.
            self.rebellion = 0

            # Anger is direct resentment toward the player.
            # It penalizes talk, flirt, gift, and intimacy reactions.
            self.anger_with_player = 0

            # Fun is short-term appetite for play, teasing, novelty, and relief.
            # It can make light social choices more likely without replacing trust.
            self.fun = 0

            # Trust is belief that the player will not harm, betray, or humiliate her.
            # It offsets fear and makes vulnerable reactions possible.
            self.trust = 0

            # Fear is hidden risk pressure, not visible cowardice.
            # It rises when the player endangers her, the tavern, reputation, or safety.
            self.fear = 0

            # Mana is the hidden personal reaction field.
            # It grows from comfort, care, good food, prosperity, and fulfilled needs.
            # It fades from neglect, sickness, exhaustion, bad conditions, and conflict.
            self.mana = int(data.base_stats.get("mana", 10) or 10)
            self.mana_corrupted = False

            # Mood is the current broad visible posture, derived from recent state.
            # Labels still own exact authored text.
            self.mood = "neutral"

            # Reaction log records hidden calculations for debug boards only.
            # It must not be shown as normal player-facing explanation.
            self.reaction_log = []
            self.mana_reaction_table = {
                "very_low": {
                    "min": 0,
                    "max": 9,
                    "reaction": "dismissive_mocking",
                    "visible_effect": "no_aura",
                    "behavior": "ignore_or_insult",
                },
                "low": {
                    "min": 10,
                    "max": 29,
                    "reaction": "neutral_cautious",
                    "visible_effect": "faint_aura",
                    "behavior": "normal_interactions",
                },
                "medium": {
                    "min": 30,
                    "max": 59,
                    "reaction": "respectful_interested",
                    "visible_effect": "visible_glow",
                    "behavior": "better_prices_more_dialogue",
                },
                "high": {
                    "min": 60,
                    "max": 84,
                    "reaction": "awe_fear_admiration",
                    "visible_effect": "strong_aura",
                    "behavior": "offer_quests_or_fear",
                },
                "very_high": {
                    "min": 85,
                    "max": 100,
                    "reaction": "worship_terror_obsession",
                    "visible_effect": "overwhelming_aura",
                    "behavior": "extreme_reactions",
                },
                "corrupted": {
                    "min": 0,
                    "max": 100,
                    "reaction": "hostility_hatred_madness",
                    "visible_effect": "dark_corrupted_aura",
                    "behavior": "attack_or_run",
                },
            }

            self.fertility_cycle = {
                "cycle_day": 0,
                "cycle_length": 28,
                "fertile_window_start": 11,
                "fertile_window_end": 16,
                "last_updated_day": None,
            }
            self.pregnancy_state = {
                "is_pregnant": False,
                "pregnancy_day": 0,
                "term_days": 280,
                "father_id": "",
                "father_display_name": "",
                "known_to_player": False,
                "suspects": [],
                "last_checked_day": None,
                "birth_pending": False,
                "birth_day": None,
                "children_born": 0,
                "breastfeed": 0,
            }
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
            self.talk_preferences = dict(data.talk_preferences or {})
            self.wardrobe = {
                "owned": [
                    data.base_clothing.get("dressdefault", ""),
                    data.base_clothing.get("bradef", ""),
                    data.base_clothing.get("pantiesdef", ""),
                    data.base_clothing.get("legsdef", ""),
                    data.base_clothing.get("shoesdef", ""),
                ],
                "gifted": [],
                "current_dress": data.base_clothing.get("dressdefault", ""),
                "current_underwear": {
                    "bra": data.base_clothing.get("bradef", ""),
                    "panties": data.base_clothing.get("pantiesdef", ""),
                    "legs": data.base_clothing.get("legsdef", ""),
                    "shoes": data.base_clothing.get("shoesdef", ""),
                },
            }

            self.schedule_id = self.code_name
            self.schedule_source = data.schedule_source
            self.schedule_uses_clock_minutes = True
            self.current_location = data.default_location

            self.bday_asked = False
            self.birthday_known = False
            self.last_birthday_checked_day = None
            self.last_birthday_gift_day = None

            self.var = dict(data.story_defaults or {})
            if isinstance(var, dict):
                self.var.update(var)

        def update(self):
            self.name = self.code_name
            self.sync_from_maps()
            return self

        def check_birthday(self):
            if self.last_birthday_checked_day == dayspassed:
                return False
            self.last_birthday_checked_day = dayspassed
            if calendar_is_birth_record_today(self.data.birth_record):
                self.age += 1
                return True
            return False

        def birthday_gift_bonus_available(self):
            return (
                self.birthday_known
                and calendar_is_birth_record_today(self.data.birth_record)
                and self.last_birthday_gift_day != dayspassed
            )

        def mark_birthday_gift_given(self):
            self.last_birthday_gift_day = dayspassed

        def mana_profile(self):
            # Derive the current mana band from the numeric source of truth.
            if self.mana_corrupted:
                return self.mana_reaction_table["corrupted"]
            value = max(0, min(100, int(self.mana or 0)))
            for level in ["very_low", "low", "medium", "high", "very_high"]:
                row = self.mana_reaction_table[level]
                if row["min"] <= value <= row["max"]:
                    return row
            return self.mana_reaction_table["low"]

        def change_mana(self, amount, reason=""):
            # Mechanical interaction: clamp mana after every gain/loss.
            # Labels decide how the resulting reaction is written.
            before = int(self.mana or 0)
            self.mana = max(0, min(100, before + int(amount or 0)))
            self.reaction_state["last_mana_delta"] = self.mana - before
            self.reaction_state["last_mana_reasons"] = [reason] if reason else []
            return self.mana

        def daily_mana_update(self, context):
            # Mechanical interaction: daily household conditions move mana slowly.
            # Strong event choices should use change_mana directly at the event.
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
            if int(self.energy or 0) < 25:
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

            # Mana fades toward neutral when nothing meaningful happened.
            if delta == 0:
                if int(self.mana or 0) > 30:
                    delta = -1
                    reasons.append("daily_fade_high")
                elif int(self.mana or 0) < 30:
                    delta = 1
                    reasons.append("daily_fade_low")

            before = int(self.mana or 0)
            self.mana = max(0, min(100, before + delta))
            self.reaction_state["last_mana_delta"] = self.mana - before
            self.reaction_state["last_mana_reasons"] = reasons
            return self.mana

        def reaction_score(self, base_score, context):
            # Mechanical interaction: hidden state modifies a reaction key.
            # The event label receives the key and writes the visible behavior.
            score = int(base_score or 0)
            score += int(self.mana or 0) // 20
            score += int(self.relationship or 0) // 25
            score += int(self.trust or 0) // 20
            score -= int(self.anger_with_player or 0) // 20
            score -= int(self.rebellion or 0) // 25
            score -= int(self.fear or 0) // 20

            if int(self.energy or 0) < 25:
                score -= 2
            if context.get("sick", False):
                score -= 3
            if context.get("horny", False):
                score += 2

            self.reaction_state["last_reaction_score"] = score
            return score

        def reset_daily_social(self):
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
