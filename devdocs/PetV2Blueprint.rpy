# Draft only. This file is not loaded by Ren'Py because it lives under devdocs.
# Purpose: reusable pet NPC blueprint for dog, werecat, and future animal companions.
#
# Existing model references:
# - Dog: game/NPC/Secondary/DogCompanion.rpy. Dog has no TXT source.
# - Dog items: game/Items/Shops/HunterClubItems.rpy.
# - Dog combat support: game/Utilities/Fight/FightSystemRuntime.rpy.
# - Werecat: game/NPC/Secondary/WerecatNPC.rpy and game/NPC/Secondary/MelissaWerecatQuest.rpy.
#
# Ownership contract:
# - PetData owns static identity, species/type, description, base location,
#   portrait/media, schedule source metadata, action preferences, and story-default seeds.
# - PetInfo owns save/runtime state: current location, trust/bond, mood, hunger,
#   health, obedience, daily interaction flags, hidden mana reaction response,
#   and story var.
# - `code_name` is the unique logic key used everywhere: "dog", "werecat", etc.
# - Schedule files use hidden clock-minute intervals. Normal HUD displays fantasy
#   time-slot names only, not real clock text.

init python:
    class PetDataBlueprint(PeopleData):
        code_name = ""

        def __init__(
            self,
            code_name,
            display_name,
            species,
            description,
            default_location,
            portrait="",
            base_stats=None,
            action_preferences=None,
            story_defaults=None,
            schedule_source=None,
        ):
            self.code_name = str(code_name or "").strip().lower()
            self.species = str(species or "pet")
            super().__init__(
                self.code_name,
                cname=display_name,
                fullname=display_name,
                genitive=display_name,
                dative=display_name,
                portrait=portrait,
                default_location=default_location,
                description=description,
            )
            self.base_stats = dict(base_stats or {})
            self.action_preferences = dict(action_preferences or {})
            self.story_defaults = dict(story_defaults or {})
            self.schedule_source = schedule_source or ("schedules/%s.json" % self.code_name)
            self.schedule_uses_clock_minutes = True
            self.hud_time_display = "time_slot_only"

        def schedule_intervals(self):
            # Individual pets should use JSON schedules.
            # Override only for draft/prototype examples.
            return []


    class PetInfoBlueprint(BaseNPC):
        code_name = ""

        def __init__(self, data, var=None):
            super().__init__(data.code_name, var=var)
            self.code_name = data.code_name
            self.name = data.code_name
            self.data = data
            self.species = data.species

            self.known = False
            self.trust = int(data.base_stats.get("trust", 0) or 0)
            self.bond = int(data.base_stats.get("bond", 0) or 0)
            self.obedience = int(data.base_stats.get("obedience", 0) or 0)
            self.health = int(data.base_stats.get("health", 100) or 100)
            self.health_max = int(data.base_stats.get("health_max", 100) or 100)
            self.hunger = int(data.base_stats.get("hunger", 0) or 0)
            self.energy = int(data.base_stats.get("energy", 100) or 100)
            self.energy_max = int(data.base_stats.get("energy_max", 100) or 100)
            self.mood = "neutral"

            self.fed_today = 0
            self.petted_today = 0
            self.played_today = 0
            self.trained_today = 0
            self.sent_on_task_today = 0

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
                    "reaction": "dismissive_or_aggressive",
                    "visible_effect": "no_aura",
                    "behavior": "avoid_or_growl",
                },
                "low": {
                    "min": 10,
                    "max": 29,
                    "reaction": "neutral_cautious",
                    "visible_effect": "faint_aura",
                    "behavior": "ordinary_pet_behavior",
                },
                "medium": {
                    "min": 30,
                    "max": 59,
                    "reaction": "friendly_interested",
                    "visible_effect": "visible_glow",
                    "behavior": "approaches_and_obeys_more",
                },
                "high": {
                    "min": 60,
                    "max": 84,
                    "reaction": "devoted_or_afraid",
                    "visible_effect": "strong_aura",
                    "behavior": "protects_or_submits",
                },
                "very_high": {
                    "min": 85,
                    "max": 100,
                    "reaction": "bonded_or_terrified",
                    "visible_effect": "overwhelming_aura",
                    "behavior": "extreme_loyalty_or_panic",
                },
                "corrupted": {
                    "min": 0,
                    "max": 100,
                    "reaction": "hostile_or_maddened",
                    "visible_effect": "dark_corrupted_aura",
                    "behavior": "attack_flee_or_hunt",
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

        def reset_daily_pet_flags(self):
            self.fed_today = 0
            self.petted_today = 0
            self.played_today = 0
            self.trained_today = 0
            self.sent_on_task_today = 0


    class DogPetData(PetDataBlueprint):
        code_name = "dog"

        def __init__(self):
            super().__init__(
                code_name=self.code_name,
                display_name="Пес",
                species="dog",
                description="Охотничий пес: сперва бродячий, потом домашний спутник, сторож и помощник в охоте.",
                default_location="",
                portrait="images/dog/dog.png",
                base_stats={
                    "level": 1,
                    "training_progress": 0,
                    "loyalty": 0,
                    "max_loyalty": 25,
                    "health": 50,
                    "health_max": 50,
                    "bite_damage": 20,
                    "defense": 15,
                },
                action_preferences={
                    "stray_actions": ["call_stray", "pet_stray", "play_stray", "stray_bone", "adopt"],
                    "owned_actions": ["play", "train", "bone", "train_bone", "hunt", "stay", "household_walk"],
                    "required_items": {
                        "bone": "dog_bone_001",
                        "collar": "dog_collar_001",
                    },
                    "name_options": ["Sharik", "Tresor", "Bobick", "Muchtar", "Drool"],
                },
                story_defaults={
                    "mode": "stray",
                    "met": False,
                    "owned": False,
                    "in_company": False,
                    "booth_built": False,
                    "can_haul": False,
                    "spawn_day": None,
                    "spawn_location": "",
                    "last_play_day": None,
                    "last_train_day": None,
                    "bones_given": 0,
                    "stray_played": False,
                    "play_sessions": 0,
                },
                schedule_source="schedules/dog.json",
            )
            self.spawn_locations = ["PortStreets", "MarketPlace", "ArtisansQuarter", "StreetTavern"]
            self.home_roam_locations = ["Backyard", "TavernKitchen", "TavernStable", "TavernStorage", "TavernMain", "TavernMyRoom"]
            self.picture_paths = {
                "stray": ["images/dog/no_colar.png", "images/tavern/myroom/no_colar.png"],
                "owned": ["images/tavern/myroom/dog.png", "images/player_room/dog.png", "images/dog/dog.png"],
                "booth": ["images/tavern/myroom/dog_booth.png", "images/player_room/dog_booth.png", "images/dog/dog_booth.png"],
            }


    class DogPetInfo(PetInfoBlueprint):
        code_name = "dog"

        def __init__(self, data, var=None):
            super().__init__(data, var=var)
            self.mode = "stray"
            self.met = False
            self.owned = False
            self.in_company = False
            self.nickname = "Пес"

            self.level = int(data.base_stats.get("level", 1) or 1)
            self.training_progress = int(data.base_stats.get("training_progress", 0) or 0)
            self.loyalty = int(data.base_stats.get("loyalty", 0) or 0)
            self.max_loyalty = int(data.base_stats.get("max_loyalty", 25) or 25)
            self.health = int(data.base_stats.get("health", 50) or 50)
            self.health_max = int(data.base_stats.get("health_max", 50) or 50)
            self.bite_damage = int(data.base_stats.get("bite_damage", 20) or 20)
            self.defense = int(data.base_stats.get("defense", 15) or 15)

            self.bones_given = 0
            self.stray_played = False
            self.play_sessions = 0
            self.last_play_day = None
            self.last_train_day = None
            self.booth_built = False
            self.can_haul = False
            self.spawn_day = None
            self.spawn_location = ""
            self.household_walks = []
            self.party_roles = {
                "hunting": False,
                "fight_support": False,
                "guard_home": False,
                "haul": False,
            }


    class WerecatPetData(PetDataBlueprint):
        code_name = "werecat"

        def __init__(self):
            super().__init__(
                code_name=self.code_name,
                display_name="Луна",
                species="werecat",
                description="Лесная кошкодевочка: сперва дикая добыча лесной охоты, затем возможная домашняя охотница на крыс.",
                default_location="",
                portrait="images/hunt/kitty_1.png",
                base_stats={
                    "trust": 0,
                    "comfort": 0,
                    "health": 100,
                    "health_max": 100,
                    "energy": 100,
                    "energy_max": 100,
                },
                action_preferences={
                    "wild_actions": ["search_tracks", "set_trap", "check_trap", "adopt", "sell", "release", "gift_clara"],
                    "adopted_actions": ["pet", "milk", "play", "observe", "dog_play"],
                    "required_items": {
                        "trap": "hunting_trap_001",
                        "milk": "milk_pitcher_001",
                    },
                },
                story_defaults={
                    "mode": "wild",
                    "rats_problem_active": 0,
                    "rat_breakfast_seen": 0,
                    "adoption_breakfast_seen": 0,
                    "woods_exploration": 0,
                    "tracks_seen": 0,
                    "tracks_first_text_seen": 0,
                    "tracks_room": "",
                    "trap_active": 0,
                    "trap_room": "",
                    "trap_day": None,
                    "trap_rooms": {},
                    "caught": 0,
                    "adopted": 0,
                    "adopted_count": 0,
                    "sold": 0,
                    "gifted_clara": 0,
                    "clara_gift_day": None,
                    "name": "",
                    "adopted_day": None,
                    "first_month_thanks_day": None,
                    "hunter_tease_day": None,
                    "hunter_tease_offer_day": None,
                    "hunter_tease_offer_ready": 0,
                    "rat_carcass_cached": 0,
                    "rat_food_loss_next_day": None,
                },
                schedule_source="schedules/werecat.json",
            )
            self.roam_locations_by_period = {
                "early": ["TavernKitchen", "TavernMain", "TavernStorage"],
                "morning": ["Backyard", "TavernKitchen", "TavernStorage"],
                "day": ["Backyard", "TavernStorage", "TavernMelissaRoom", "TavernAmandaRoom"],
                "evening": ["TavernKitchen", "Backyard", "TavernStorage"],
                "night": ["TavernMain", "TavernKitchen", "TavernStorage", "TavernMelissaRoom", "TavernAmandaRoom", "TavernSandraRoom", "TavernMyRoom", "Backyard"],
            }
            self.picture_paths = {
                "info": ["images/hunt/kitty_1.png", "images/hunt/kitty free.png", "images/hunt/hunt.png", "images/general/hunter_store_catInfo.png"],
                "caught": ["images/hunt/kitty_trapped.png", "images/hunt/kitty_1.png", "images/hunt/kitty free.png", "images/hunt/hunt.png"],
                "home": ["images/general/kitty.png", "images/general/kitty_splash.png", "images/general/hunter_store_catInfo.png"],
            }


    class WerecatPetInfo(PetInfoBlueprint):
        code_name = "werecat"

        def __init__(self, data, var=None):
            super().__init__(data, var=var)
            self.mode = "wild"
            self.caught = False
            self.adopted = False
            self.sold = False
            self.gifted_clara = False
            self.nickname = ""
            self.adopted_count = 0
            self.adopted_day = None

            self.trust = int(data.base_stats.get("trust", 0) or 0)
            self.comfort = int(data.base_stats.get("comfort", 0) or 0)
            self.pet_day = None
            self.milk_day = None
            self.play_day = None
            self.rat_hunting = {
                "rats_problem_active": False,
                "rat_food_loss_next_day": None,
                "rat_carcass_cached": False,
            }
            self.tracking = {
                "woods_exploration": 0,
                "tracks_seen": False,
                "tracks_first_text_seen": False,
                "tracks_room": "",
            }
            self.traps = {
                "active": False,
                "rooms": {},
            }
