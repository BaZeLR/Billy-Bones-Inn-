# Draft only. This file is not loaded by Ren'Py because it lives under devdocs.
# Purpose: enemy / hunt animal blueprint for combat-spawn definitions.
#
# Existing model references:
# - Combat class and live enemy definitions:
#   game/Utilities/Fight/FightSystemRuntime.rpy
# - Town random combat triggers:
#   game/Town/RandomTownEvents.rpy
# - Hunt design notes:
#   devdocs/fight_system.md
#
# Ownership contract:
# - EnemyData owns immutable combat definition: id, display name, type,
#   health, attack/defence ranges, moves, skills, weapon, tactics, loot,
#   money, image paths, description, and spawn rules.
# - EnemyInstance owns per-fight mutable state: health, status effects,
#   selected move, and combat log state.
# - Events/rooms only choose an enemy id and call the combat system.

init python:
    class EnemyDataBlueprint(object):
        def __init__(
            self,
            object_id,
            display_name,
            enemy_type="beast",
            description="",
            health=30,
            attack_min=5,
            attack_max=10,
            defence_min=3,
            defence_max=8,
            moves=None,
            skills=None,
            weapon=None,
            weapon_features=None,
            tactics="",
            company_min=1,
            company_max=1,
            loot=None,
            money_min=0,
            money_max=0,
            exploration_reward=0,
            picture_paths=None,
            spawn_rules=None,
        ):
            self.object_id = str(object_id or "")
            self.display_name = str(display_name or self.object_id)
            self.enemy_type = str(enemy_type or "beast")
            self.description = str(description or "")
            self.health = int(health or 0)
            self.attack_min = int(attack_min or 0)
            self.attack_max = int(attack_max or 0)
            self.defence_min = int(defence_min or 0)
            self.defence_max = int(defence_max or 0)
            self.moves = list(moves or [])
            self.skills = list(skills or [])
            self.weapon = str(weapon or "")
            self.weapon_features = dict(weapon_features or {})
            self.tactics = str(tactics or "")
            self.company_min = max(1, int(company_min or 1))
            self.company_max = max(self.company_min, int(company_max or self.company_min))
            self.loot = dict(loot or {})
            self.money_min = max(0, int(money_min or 0))
            self.money_max = max(self.money_min, int(money_max or self.money_min))
            self.exploration_reward = max(0, int(exploration_reward or 0))
            self.picture_paths = list(picture_paths or [])
            self.spawn_rules = list(spawn_rules or [])

        def to_fight_definition_kwargs(self):
            return {
                "object_id": self.object_id,
                "display_name": self.display_name,
                "enemy_type": self.enemy_type,
                "health": self.health,
                "attack_min": self.attack_min,
                "attack_max": self.attack_max,
                "defence_min": self.defence_min,
                "defence_max": self.defence_max,
                "moves": list(self.moves),
                "skills": list(self.skills),
                "weapon": self.weapon,
                "tactics": self.tactics,
                "company_min": self.company_min,
                "company_max": self.company_max,
                "loot": dict(self.loot),
                "money_min": self.money_min,
                "money_max": self.money_max,
                "exploration_reward": self.exploration_reward,
            }


    class EnemyInstanceBlueprint(object):
        def __init__(self, data, index=1):
            self.data = data
            self.object_id = data.object_id
            self.display_name = data.display_name
            self.index = int(index or 1)
            self.health = data.health
            self.health_max = data.health
            self.status = {}
            self.selected_move = ""


    ENEMY_HUNT_V2_DEFINITIONS = {
        "wolf": EnemyDataBlueprint(
            "wolf",
            "Волк",
            enemy_type="beast",
            description="Обычный лесной волк. Опасен в стае, давит числом и страхом.",
            health=35,
            attack_min=8,
            attack_max=15,
            defence_min=4,
            defence_max=10,
            moves=["dodge", "bite", "surround", "howl", "dead_lock"],
            skills=["pack_hunt", "fear"],
            tactics="pack",
            company_min=1,
            company_max=5,
            loot={"wolf_skin_001": 1},
            picture_paths=["images/hunt/lonely_wolf_attack.png", "images/hunt/hunt.png"],
            spawn_rules=[
                {"room": "Forest", "count_min": 1, "count_max": 1, "min_exploration": 50, "weight": 55},
                {"room": "ForestClearing", "count_min": 1, "count_max": 2, "min_exploration": 50, "weight": 40},
                {"room": "ForestDarkWoods", "count_min": 2, "count_max": 5, "min_exploration": 50, "weight": 45},
            ],
        ),
        "white_wolf": EnemyDataBlueprint(
            "white_wolf",
            "Белый вожак",
            enemy_type="beast",
            description="Редкий белый волк-вожак. Всегда один, сильнее обычного волка и опасен страхом.",
            health=48,
            attack_min=10,
            attack_max=18,
            defence_min=6,
            defence_max=12,
            moves=["dodge", "bite", "howl", "dead_lock"],
            skills=["pack_leader", "fear"],
            tactics="stalk",
            loot={"white_wolf_skin_001": 1},
            exploration_reward=7,
            picture_paths=["images/hunt/lonely_wolf_attack.png", "images/hunt/hunt.png"],
            spawn_rules=[
                {"room": "Forest", "count_min": 1, "count_max": 1, "min_exploration": 100, "weight": 15},
                {"room": "ForestClearing", "count_min": 1, "count_max": 1, "min_exploration": 100, "weight": 15},
                {"room": "ForestDarkWoods", "count_min": 1, "count_max": 1, "min_exploration": 100, "weight": 10},
            ],
        ),
        "boar": EnemyDataBlueprint(
            "boar",
            "Кабан",
            enemy_type="beast",
            description="Лесной кабан. Идет напролом, бьет рывком и защищается толстой шкурой.",
            health=55,
            attack_min=11,
            attack_max=20,
            defence_min=6,
            defence_max=13,
            moves=["ram", "bite", "attack", "defend"],
            skills=["charge"],
            tactics="charge",
            company_min=1,
            company_max=3,
            loot={"boar_fang_001": 1, "boar_meat_001": 1},
            picture_paths=["images/hunt/boars.png", "images/hunt/hunt.png"],
            spawn_rules=[
                {"room": "Forest", "count_min": 1, "count_max": 1, "min_exploration": 70, "weight": 30},
                {"room": "ForestClearing", "count_min": 1, "count_max": 2, "min_exploration": 60, "weight": 45},
                {"room": "ForestDarkWoods", "count_min": 1, "count_max": 3, "min_exploration": 60, "weight": 30},
            ],
        ),
        "brown_bear": EnemyDataBlueprint(
            "brown_bear",
            "Бурый медведь",
            enemy_type="beast",
            description="Тяжелый лесной хищник. Медленный, но опасный: давит силой, когтями и страхом.",
            health=90,
            attack_min=16,
            attack_max=28,
            defence_min=10,
            defence_max=18,
            moves=["bite", "claws", "strike", "roar"],
            skills=["maul", "fear"],
            tactics="press",
            loot={"bear_fur_brown_001": 1, "bear_claw_001": 1},
            exploration_reward=4,
            picture_paths=["images/hunt/bear.png", "images/hunt/bear_2.png", "images/hunt/hunt.png"],
            spawn_rules=[
                {"room": "ForestDarkWoods", "count_min": 1, "count_max": 1, "min_exploration": 120, "weight": 10},
            ],
        ),
        "giant_grizzly": EnemyDataBlueprint(
            "giant_grizzly",
            "Гигантский гризли",
            enemy_type="beast",
            description="Редкий огромный медведь. Почти босс охоты, ломает строй и пугает даже опытного охотника.",
            health=115,
            attack_min=20,
            attack_max=34,
            defence_min=12,
            defence_max=22,
            moves=["bite", "claws", "strike", "roar"],
            skills=["maul", "terror"],
            tactics="break_line",
            loot={"bear_fur_grizzly_001": 1, "bear_claw_001": 1},
            exploration_reward=6,
            picture_paths=["images/hunt/bear_2.png", "images/hunt/bear.png", "images/hunt/hunt.png"],
            spawn_rules=[
                {"room": "ForestDarkWoods", "count_min": 1, "count_max": 1, "min_exploration": 160, "weight": 5},
            ],
        ),
        "street_crook": EnemyDataBlueprint(
            "street_crook",
            "Уличный громила",
            enemy_type="human",
            description="Городской громила из случайных уличных событий. Давит дубинкой и числом.",
            health=42,
            attack_min=8,
            attack_max=16,
            defence_min=5,
            defence_max=11,
            moves=["attack", "strike", "defend"],
            skills=["brawl"],
            weapon="дубинка",
            weapon_features={"weapon_type": "club", "range": "melee", "lethal": False},
            tactics="pressure",
            company_min=1,
            company_max=3,
            money_min=2,
            money_max=8,
            exploration_reward=3,
            picture_paths=["images/general/cityguard.jpg"],
            spawn_rules=[
                {"event": "TownStreetThugsEvent", "probability": 10, "locations": "town", "cooldown": "once_per_day_fight"},
            ],
        ),
        "street_thief": EnemyDataBlueprint(
            "street_thief",
            "Уличный вор",
            enemy_type="human",
            description="Быстрый вор с ножом. Слабее громилы, но лучше уворачивается и пытается уйти.",
            health=32,
            attack_min=7,
            attack_max=14,
            defence_min=7,
            defence_max=13,
            moves=["dodge", "strike", "attack"],
            skills=["knife", "escape"],
            weapon="нож",
            weapon_features={"weapon_type": "knife", "range": "melee", "lethal": True},
            tactics="hit_and_run",
            company_min=1,
            company_max=2,
            loot={"rope_001": 1},
            money_min=4,
            money_max=14,
            exploration_reward=4,
            picture_paths=["images/general/cityguard.jpg"],
            spawn_rules=[
                {"event": "future_thief_event", "probability": 10, "locations": "town", "status": "not_currently_wired"},
            ],
        ),
        "patrol_guard": EnemyDataBlueprint(
            "patrol_guard",
            "Патрульный стражник",
            enemy_type="guard",
            description="Группа ночного патруля. Спавнится только в комендантские часы, дерется строем.",
            health=58,
            attack_min=11,
            attack_max=20,
            defence_min=9,
            defence_max=16,
            moves=["attack", "strike", "defend"],
            skills=["formation", "arrest"],
            weapon="алебарда",
            weapon_features={"weapon_type": "halberd", "range": "reach", "formation_bonus": True},
            tactics="formation",
            company_min=2,
            company_max=4,
            money_min=1,
            money_max=5,
            exploration_reward=2,
            picture_paths=["images/general/cityguard.jpg"],
            spawn_rules=[
                {"event": "TownStreetPatrolEvent", "base_probability": 25, "notoriety_bonus": "notoriety // 2", "time": "curfew_only_21_30_to_05_30", "locations": "town"},
            ],
        ),
        "forest_bandit": EnemyDataBlueprint(
            "forest_bandit",
            "Лесной разбойник",
            enemy_type="human",
            description="Draft: вооруженный лесной разбойник для будущих Blackwood / forest road fights. В runtime пока не подключен.",
            health=50,
            attack_min=10,
            attack_max=18,
            defence_min=7,
            defence_max=14,
            moves=["attack", "strike", "dodge", "defend"],
            skills=["ambush", "knife", "bow"],
            weapon="нож / короткий лук",
            weapon_features={"weapon_type": "mixed", "range": "melee_or_ranged", "ambush_bonus": True},
            tactics="ambush",
            company_min=1,
            company_max=4,
            loot={"rope_001": 1, "arrows_001": 1},
            money_min=5,
            money_max=20,
            exploration_reward=5,
            picture_paths=["images/forest/forest_1.png", "images/forest/forest_2.png"],
            spawn_rules=[
                {"event": "future_bandit_fight", "locations": ["ForestDarkWoods", "Blackwood"], "status": "not_currently_wired"},
            ],
        ),
    }

    ENEMY_HUNT_V2_GROUPS = {
        "hunt_animals": ["wolf", "white_wolf", "boar", "brown_bear", "giant_grizzly"],
        "town_fightable": ["street_crook", "street_thief", "patrol_guard"],
        "draft_bandits": ["forest_bandit"],
    }
