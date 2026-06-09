# Draft only. This file is not loaded by Ren'Py because it lives under devdocs.
# Purpose: reusable secondary NPC data/info blueprint.
#
# Ownership contract:
# - SecondaryNPCData owns static identity, role, description, base location,
#   schedule source metadata, talk/action preferences, and story-default seeds.
# - SecondaryNPCInfo owns save/runtime state: current location, known state,
#   relationship/reputation toward player, mood/reaction, hidden mana reaction
#   response, daily interaction flags, and story var.
# - `code_name` is the unique logic key used everywhere: "eddie", "alber", etc.
# - Schedule files use hidden clock-minute intervals. Normal HUD displays fantasy
#   time-slot names only, not real clock text.

init python:
    class SecondaryNPCDataBlueprint(PeopleData):
        code_name = ""

        def __init__(
            self,
            code_name,
            display_name,
            genitive,
            dative,
            description,
            default_location,
            role="town_npc",
            base_stats=None,
            action_preferences=None,
            story_defaults=None,
            schedule_source=None,
            portrait="",
        ):
            self.code_name = str(code_name or "").strip().lower()
            super().__init__(
                self.code_name,
                cname=display_name,
                fullname=display_name,
                genitive=genitive,
                dative=dative,
                portrait=portrait,
                default_location=default_location,
                description=description,
            )
            self.role = str(role or "town_npc")
            self.base_stats = dict(base_stats or {})
            self.action_preferences = dict(action_preferences or {})
            self.story_defaults = dict(story_defaults or {})
            self.schedule_source = schedule_source or ("schedules/%s.json" % self.code_name)
            self.schedule_uses_clock_minutes = True
            self.hud_time_display = "time_slot_only"

        def schedule_intervals(self):
            # Individual secondaries should use JSON schedules.
            # Override only for draft/prototype examples.
            return []


    class SecondaryNPCInfoBlueprint(BaseNPC):
        code_name = ""

        def __init__(self, data, var=None):
            super().__init__(data.code_name, var=var)
            self.code_name = data.code_name
            self.name = data.code_name
            self.data = data

            self.known = False
            self.relationship = int(data.base_stats.get("relationship", 0) or 0)
            self.reputation = int(data.base_stats.get("reputation", 0) or 0)
            self.fear = int(data.base_stats.get("fear", 0) or 0)
            self.respect = int(data.base_stats.get("respect", 0) or 0)
            self.hostility = int(data.base_stats.get("hostility", 0) or 0)
            self.mood = "neutral"

            self.talked_today = 0
            self.asked_today = 0
            self.helped_today = 0
            self.bribed_today = 0
            self.fought_today = 0

            self.mana_reaction = {
                "level": "low",
                "value": 10,
                "corrupted": False,
                "visible_effect": "faint_aura",
                "reaction": "neutral_cautious",
            }
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

            self.schedule_id = self.code_name
            self.schedule_source = data.schedule_source
            self.schedule_uses_clock_minutes = True
            self.current_location = data.default_location

            self.action_preferences = dict(data.action_preferences or {})
            self.var = dict(data.story_defaults or {})
            if isinstance(var, dict):
                self.var.update(var)

        def update(self):
            self.name = self.code_name
            self.sync_from_maps()
            return self

        def mana_profile(self):
            if self.mana_reaction.get("corrupted", False):
                return self.mana_reaction_table["corrupted"]
            value = max(0, min(100, int(self.mana_reaction.get("value", 0) or 0)))
            for level in ["very_low", "low", "medium", "high", "very_high"]:
                row = self.mana_reaction_table[level]
                if row["min"] <= value <= row["max"]:
                    self.mana_reaction["level"] = level
                    self.mana_reaction["reaction"] = row["reaction"]
                    self.mana_reaction["visible_effect"] = row["visible_effect"]
                    return row
            return self.mana_reaction_table["low"]

        def reset_daily_social(self):
            self.talked_today = 0
            self.asked_today = 0
            self.helped_today = 0
            self.bribed_today = 0
            self.fought_today = 0
