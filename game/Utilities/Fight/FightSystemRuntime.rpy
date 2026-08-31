# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -20 python:
    import renpy.exports as renpy_module

    class FightEnemyDefinition(object):
        def __init__(
            self,
            object_id,
            display_name,
            enemy_type="beast",
            health=30,
            attack_min=5,
            attack_max=10,
            defence_min=3,
            defence_max=8,
            moves=None,
            skills=None,
            weapon="",
            tactics="",
            company_min=1,
            company_max=1,
            loot=None,
            money_min=0,
            money_max=0,
            exploration_reward=0,
            energy=0,
        ):
            self.object_id = str(object_id or "")
            self.display_name = str(display_name or self.object_id)
            self.enemy_type = str(enemy_type or "beast")
            self.health = int(health or 0)
            self.energy = int(energy or 0) if int(energy or 0) > 0 else max(20, int(health or 0))
            self.attack_min = int(attack_min or 0)
            self.attack_max = int(attack_max or 0)
            self.defence_min = int(defence_min or 0)
            self.defence_max = int(defence_max or 0)
            self.moves = list(moves or [])
            self.skills = list(skills or [])
            self.weapon = str(weapon or "")
            self.tactics = str(tactics or "")
            self.company_min = max(1, int(company_min or 1))
            self.company_max = max(self.company_min, int(company_max or self.company_min))
            self.loot = dict(loot or {})
            self.money_min = max(0, int(money_min or 0))
            self.money_max = max(self.money_min, int(money_max or self.money_min))
            self.exploration_reward = max(0, int(exploration_reward or 0))

        def as_dict(self):
            return {
                "id": self.object_id,
                "name": self.display_name,
                "enemy_type": self.enemy_type,
                "health": self.health,
                "energy": self.energy,
                "attack_min": self.attack_min,
                "attack_max": self.attack_max,
                "defence_min": self.defence_min,
                "defence_max": self.defence_max,
                "moves": list(self.moves or []),
                "skills": list(self.skills or []),
                "weapon": self.weapon,
                "tactics": self.tactics,
                "company_min": self.company_min,
                "company_max": self.company_max,
                "loot": dict(self.loot or {}),
                "money_min": self.money_min,
                "money_max": self.money_max,
                "exploration_reward": self.exploration_reward,
            }

    class FightEnemyInstance(object):
        def __init__(self, definition, index=1):
            self.object_id = str(definition.object_id or "")
            self.name = str(definition.display_name or self.object_id)
            self.enemy_type = str(definition.enemy_type or "beast")
            self.index = max(1, int(index or 1))
            self.health = max(1, int(definition.health or 1))
            self.health_max = self.health
            self.energy = max(0, int(definition.energy or self.health))
            self.energy_max = self.energy
            self.attack_min = int(definition.attack_min or 0)
            self.attack_max = int(definition.attack_max or 0)
            self.defence_min = int(definition.defence_min or 0)
            self.defence_max = int(definition.defence_max or 0)
            self.moves = list(definition.moves or [])
            self.skills = list(definition.skills or [])
            self.weapon = str(definition.weapon or "")
            self.tactics = str(definition.tactics or "")
            self.loot = dict(definition.loot or {})
            self.money_min = max(0, int(definition.money_min or 0))
            self.money_max = max(self.money_min, int(definition.money_max or self.money_min))
            self.exploration_reward = max(0, int(definition.exploration_reward or 0))
            self.status = {}

    class FightInfo(object):
        def __init__(self):
            self.target_index = 1
            self.victory_loot = {}
            self.retreat_used = 0
            self.enemy_party = []
            self.enemy_id = ""
            self.return_room_code = ""
            self.return_picture = ""
            self.status_state = {}
            self.outcome_kind = ""
            self.last_result = {}

        @property
        def loaded_ammo(self):
            return rusty_hunter_rifle_loaded_ammo() if str(player.equipment.weapon or "") == "rusty_hunter_rifle_001" else ""

        @loaded_ammo.setter
        def loaded_ammo(self, value):
            rifle_item = rusty_hunter_rifle_item()
            if rifle_item is not None:
                rifle_item.state["loaded_ammo"] = str(value or "").strip()

        @property
        def weapon_loaded(self):
            return 1 if self.loaded_ammo else 0

    class HuntInfo(object):
        def __init__(self):
            self.trap_rooms = {}

    FIGHT_SUPPLY_ITEM_MAP = {
        "arrows": "arrows_001",
        "droplets": "droplets_001",
        "gunpowder": "gunpowder_001",
        "fire_bomb": "fire_bomb_001",
        "bandage": "bandage_001",
        "energy_tea": "energy_tea_001",
        "healing_potion": "healing_potion_001",
    }

    FOREST_HUNT_ROOM_TABLE = {
        "Forest": [
            {"enemy_id": "wolf", "count_min": 1, "count_max": 1, "min_exploration": 50, "weight": 55},
            {"enemy_id": "boar", "count_min": 1, "count_max": 1, "min_exploration": 70, "weight": 30},
            {"enemy_id": "white_wolf", "count_min": 1, "count_max": 1, "min_exploration": 100, "weight": 15},
        ],
        "ForestClearing": [
            {"enemy_id": "wolf", "count_min": 1, "count_max": 2, "min_exploration": 50, "weight": 40},
            {"enemy_id": "boar", "count_min": 1, "count_max": 2, "min_exploration": 60, "weight": 45},
            {"enemy_id": "white_wolf", "count_min": 1, "count_max": 1, "min_exploration": 100, "weight": 15},
        ],
        "ForestDarkWoods": [
            {"enemy_id": "wolf", "count_min": 2, "count_max": 5, "min_exploration": 50, "weight": 45},
            {"enemy_id": "boar", "count_min": 1, "count_max": 3, "min_exploration": 60, "weight": 30},
            {"enemy_id": "white_wolf", "count_min": 1, "count_max": 1, "min_exploration": 100, "weight": 10},
            {"enemy_id": "brown_bear", "count_min": 1, "count_max": 1, "min_exploration": 120, "weight": 10},
            {"enemy_id": "giant_grizzly", "count_min": 1, "count_max": 1, "min_exploration": 160, "weight": 5},
        ],
    }

    FIGHT_ENEMY_DEFINITIONS = {
        "wolf": FightEnemyDefinition(
            "wolf", "Волк", "beast", 35, 8, 15, 4, 10,
            moves=["dodge", "bite", "surround", "howl", "dead_lock"],
            skills=["pack_hunt", "fear"],
            tactics="pack",
            company_min=1,
            company_max=5,
            loot={"wolf_skin_001": (1, 1)},
        ),
        "white_wolf": FightEnemyDefinition(
            "white_wolf", "Белый вожак", "beast", 48, 10, 18, 6, 12,
            moves=["dodge", "bite", "howl", "dead_lock"],
            skills=["pack_leader", "fear"],
            tactics="stalk",
            loot={"white_wolf_skin_001": 1},
            exploration_reward=7,
        ),
        "boar": FightEnemyDefinition(
            "boar", "Кабан", "beast", 55, 11, 20, 6, 13,
            moves=["ram", "bite", "attack", "defend"],
            skills=["charge"],
            tactics="charge",
            company_min=1,
            company_max=3,
            loot={"boar_fang_001": (1, 1), "boar_meat_001": (1, 3)},
        ),
        "brown_bear": FightEnemyDefinition(
            "brown_bear", "Бурый медведь", "beast", 90, 16, 28, 10, 18,
            moves=["bite", "claws", "strike", "roar"],
            skills=["maul", "fear"],
            tactics="press",
            loot={"bear_fur_brown_001": (1, 1), "bear_claw_001": (1, 2)},
            exploration_reward=4,
        ),
        "giant_grizzly": FightEnemyDefinition(
            "giant_grizzly", "Гигантский гризли", "beast", 115, 20, 34, 12, 22,
            moves=["bite", "claws", "strike", "roar"],
            skills=["maul", "terror"],
            tactics="break_line",
            loot={"bear_fur_grizzly_001": (1, 1), "bear_claw_001": (1, 2)},
            exploration_reward=6,
        ),
        "street_crook": FightEnemyDefinition(
            "street_crook", "Уличный громила", "human", 42, 8, 16, 5, 11,
            moves=["attack", "strike", "defend"],
            skills=["brawl"],
            weapon="дубинка",
            tactics="pressure",
            company_min=1,
            company_max=3,
            money_min=2,
            money_max=8,
            exploration_reward=3,
        ),
        "street_thief": FightEnemyDefinition(
            "street_thief", "Уличный вор", "human", 32, 7, 14, 7, 13,
            moves=["dodge", "strike", "attack"],
            skills=["knife", "escape"],
            weapon="нож",
            tactics="hit_and_run",
            company_min=1,
            company_max=2,
            loot={"rope_001": 1},
            money_min=4,
            money_max=14,
            exploration_reward=4,
        ),
        "patrol_guard": FightEnemyDefinition(
            "patrol_guard", "Патрульный стражник", "guard", 58, 11, 20, 9, 16,
            moves=["attack", "strike", "defend"],
            skills=["formation", "arrest"],
            weapon="алебарда",
            tactics="formation",
            company_min=2,
            company_max=4,
            money_min=1,
            money_max=5,
            exploration_reward=2,
        ),
        "legare": FightEnemyDefinition(
            "legare", "Месье Легаре", "human", 60, 10, 19, 8, 15,
            moves=["attack", "strike", "dodge", "defend"],
            skills=["brawl", "dirty_fighting"],
            weapon="трость",
            tactics="counter",
            company_min=1,
            company_max=1,
            exploration_reward=4,
        ),
    }
    def fight_player_level():
        return 1 + max(0, int(effective_player_exploration() or 0)) // 50

    def fight_rng_key(purpose="roll"):
        step = max(0, int(fight.status_state.get("rng_step", 0) or 0))
        fight.status_state["rng_step"] = step + 1
        return "fight_%s_%s" % (str(purpose or "roll"), step)

    def hunt_available():
        return int(effective_player_exploration() or 0) >= 50

    def fight_supply_count(supply_key=""):
        key = str(supply_key or "").strip()
        if key == "bees_bomb":
            return max(0, int(player.combat.special_supply.get(key, 0) or 0))
        item_id = str(FIGHT_SUPPLY_ITEM_MAP.get(key, "") or "")
        return max(0, int(player.item_count(item_id) or 0)) if item_id else 0

    def fight_consume_supply(supply_key="", amount=1):
        key = str(supply_key or "").strip()
        count = max(1, int(amount or 1))
        if fight_supply_count(key) < count:
            return False
        if key == "bees_bomb":
            player.combat.special_supply[key] = fight_supply_count(key) - count
            return True
        item_id = str(FIGHT_SUPPLY_ITEM_MAP.get(key, "") or "")
        if not item_id:
            return False
        player.remove_item(item_id, count)
        return True

    def fight_loaded_ammo_name(ammo_code=""):
        ammo_key = str(ammo_code or "").strip()
        if ammo_key == "arrows":
            return "стрела"
        if ammo_key == "droplets":
            return "дробь"
        return "нет"

    def fight_spend_energy(amount):
        return player.change_stat("energy", -max(0, int(amount or 0)))

    def fight_restore_energy(amount):
        return player.change_stat("energy", max(0, int(amount or 0)))

    def fight_player_status_labels():
        labels = []
        if int(fight.status_state.get("locked_turns", 0) or 0) > 0:
            labels.append("захват")
        if int(fight.status_state.get("fear_turns", 0) or 0) > 0:
            labels.append("страх")
        if int(fight.status_state.get("stagger_turns", 0) or 0) > 0:
            labels.append("сбит с ног")
        return labels

    def fight_player_mana_modifier():
        return max(0, int(player.combat.mana or 0) // 10)

    def fight_player_speed_points():
        weapon = get_game_item(str(player.equipment.weapon or ""))
        armor = get_game_item(str(player.equipment.armor or ""))
        weapon_penalty = int(getattr(weapon, "custom_properties", {}).get("speed_penalty", 0) or 0) if weapon else 0
        armor_penalty = int(getattr(armor, "custom_properties", {}).get("speed_penalty", 0) or 0) if armor else 0
        return max(1, 10 + fight_player_level() - weapon_penalty - armor_penalty)

    def fight_enemy_speed_points(enemy=None):
        enemy_obj = enemy or fight_selected_target()
        if enemy_obj is None:
            return 0
        return max(1, 8 + int(enemy_obj.energy or 0) // 20)

    def fight_party_totals(side="player"):
        if str(side or "player") == "enemy":
            rows = fight_active_enemy_rows()
            return {
                "health": sum(int(row.health or 0) for row in rows),
                "energy": sum(int(row.energy or 0) for row in rows),
                "speed": sum(fight_enemy_speed_points(row) for row in rows),
            }
        rows = fight_company_display_rows()
        dog_state = fight_dog_support_state()
        return {
            "health": sum(int(row.get("health", 0) or 0) for row in rows),
            "energy": sum(int(row.get("energy", 0) or 0) for row in rows),
            "speed": fight_player_speed_points() + int(dog_state.get("speed", 0) or 0),
        }

    def fight_decay_player_statuses():
        for status_key in ("locked_turns", "fear_turns", "stagger_turns"):
            fight.status_state[status_key] = max(0, int(fight.status_state.get(status_key, 0) or 0) - 1)

    def fight_apply_player_status(status_key, turns=1):
        turn_count = max(1, int(turns or 1))
        fight.status_state[status_key] = max(turn_count, int(fight.status_state.get(status_key, 0) or 0))

    def fight_weapon_attack_points():
        item_id = str(player.equipment.weapon or "").strip()
        if not item_id:
            return 0
        item_obj = get_game_item(item_id)
        if item_obj is None:
            return 0
        return int(getattr(item_obj, "custom_properties", {}).get("attack_points", 0) or 0)

    def fight_rifle_equipped():
        return str(player.equipment.weapon or "").strip() == "rusty_hunter_rifle_001"

    def fight_armor_defence_points():
        item_id = str(player.equipment.armor or "").strip()
        if not item_id:
            return 0
        item_obj = get_game_item(item_id)
        if item_obj is None:
            return 0
        props = getattr(item_obj, "custom_properties", {}) or {}
        return int(props.get("defence_points", props.get("armor_points", 0)) or 0)

    def fight_item_name(item_id="", fallback=""):
        item_key = str(item_id or "").strip()
        if not item_key:
            return str(fallback or "")
        item_obj = get_game_item(item_key)
        if item_obj is not None:
            return str(getattr(item_obj, "name", "") or getattr(item_obj, "display_name", "") or item_key)
        names = {
            "old_axe_001": "старый топор",
            "rusty_hunter_rifle_001": "ржавое охотничье ружье",
            "old_leather_cuirass_001": "старая кожаная кираса",
        }
        return str(names.get(item_key, fallback or item_key))

    def fight_player_weapon_name():
        weapon_key = str(player.equipment.weapon or "").strip()
        if weapon_key:
            return fight_item_name(weapon_key, weapon_key)
        return "кулаки"

    def fight_player_armor_name():
        armor_key = str(player.equipment.armor or "").strip()
        if armor_key:
            return fight_item_name(armor_key, armor_key)
        return "без брони"

    def fight_attack_action_caption():
        weapon_key = str(player.equipment.weapon or "").strip()
        if weapon_key == "rusty_hunter_rifle_001":
            return "Бить прикладом"
        if weapon_key:
            return "Атаковать: {}".format(fight_player_weapon_name())
        return "Атаковать кулаками"

    def fight_player_attack_preview_text():
        level = fight_player_level()
        dog_state = fight_dog_support_state()
        attack_min = 5 + level * 5 + fight_weapon_attack_points() + int(dog_state.get("attack", 0) or 0)
        attack_max = attack_min + level * 3
        if int(player.condition.energy or 0) < 20:
            attack_min -= 4
            attack_max -= 4
        if int(fight.status_state.get("locked_turns", 0) or 0) > 0:
            attack_min -= 5
            attack_max -= 5
        if int(fight.status_state.get("fear_turns", 0) or 0) > 0:
            attack_min -= 3
            attack_max -= 3
        return "{}-{}".format(max(0, int(attack_min)), max(0, int(attack_max)))

    def fight_player_defence_preview_text():
        level = fight_player_level()
        dog_state = fight_dog_support_state()
        defence_min = 5 + level * 4 + fight_armor_defence_points() + int(dog_state.get("defence", 0) or 0)
        defence_max = defence_min + level * 2
        if int(player.condition.energy or 0) < 15:
            defence_min -= 3
            defence_max -= 3
        if int(fight.status_state.get("stagger_turns", 0) or 0) > 0:
            defence_min -= 5
            defence_max -= 5
        return "{}-{}".format(max(0, int(defence_min)), max(0, int(defence_max)))

    def fight_dog_support_state():
        if not dog.owned or "dog" not in player.combat.party or not dog.is_alive():
            return {"active": False, "attack": 0, "defence": 0, "speed": 0, "moves": []}
        moves = ["bite", "guard", "harry"]
        if int(dog.level or 0) >= 2:
            moves.insert(1, "dead_lock_bite")
        return {
            "active": True,
            "attack": int(dog.bite_damage or 0),
            "defence": int(dog.defense or 0),
            "speed": int(dog.speed or 0),
            "moves": moves,
        }

    def fight_player_attack_roll():
        level = fight_player_level()
        dog_state = fight_dog_support_state()
        base_attack = 5 + level * 5
        random_attack = procedural_randint(0, level * 3, fight_rng_key("player_attack"))
        attack_total = int(base_attack + fight_weapon_attack_points() + random_attack + int(dog_state.get("attack", 0) or 0))
        if int(player.condition.energy or 0) < 20:
            attack_total -= 4
        if int(fight.status_state.get("locked_turns", 0) or 0) > 0:
            attack_total -= 5
        if int(fight.status_state.get("fear_turns", 0) or 0) > 0:
            attack_total -= 3
        return max(0, int(attack_total))

    def fight_player_defence_roll():
        level = fight_player_level()
        dog_state = fight_dog_support_state()
        base_defence = 5 + level * 4
        random_defence = procedural_randint(0, level * 2, fight_rng_key("player_defence"))
        defence_total = int(base_defence + fight_armor_defence_points() + random_defence + int(dog_state.get("defence", 0) or 0))
        if int(player.condition.energy or 0) < 15:
            defence_total -= 3
        if int(fight.status_state.get("stagger_turns", 0) or 0) > 0:
            defence_total -= 5
        return max(0, int(defence_total))

    def fight_enemy_template(enemy_id="wolf"):
        return FIGHT_ENEMY_DEFINITIONS.get(str(enemy_id or "").strip(), FIGHT_ENEMY_DEFINITIONS["wolf"])

    def fight_selected_enemy_image():
        enemy_id = str(fight.enemy_id or "").strip()
        image_map = {
            "street_crook": "images/fight/thug.png",
            "street_thief": "images/fight/thief.png",
            "patrol_guard": "images/fight/patrol_guard.png",
            "wolf": "images/hunt/lonely_wolf_attack.png",
            "white_wolf": "images/hunt/lonely_wolf_attack.png",
            "boar": "images/hunt/boars.png",
            "brown_bear": "images/hunt/bear.png",
            "giant_grizzly": "images/hunt/bear_2.png",
        }
        return image_map.get(enemy_id, "images/fight/default_enemy.png")

    def fight_build_enemy_party(enemy_id="wolf", enemy_count=1):
        definition = FIGHT_ENEMY_DEFINITIONS.get(str(enemy_id or "wolf"), FIGHT_ENEMY_DEFINITIONS["wolf"])
        count = max(1, int(enemy_count or 1))
        return [FightEnemyInstance(definition, idx + 1) for idx in range(count)]

    def fight_active_enemy_rows():
        return [enemy for enemy in list(fight.enemy_party or []) if int(enemy.health or 0) > 0]

    def fight_selected_target():
        rows = fight_active_enemy_rows()
        if len(rows) <= 0:
            return None
        selected_index = max(1, int(fight.target_index or 1))
        for enemy in rows:
            if int(enemy.index or 0) == selected_index:
                return enemy
        fight.target_index = int(rows[0].index or 1)
        return rows[0]

    def fight_cycle_target():
        rows = fight_active_enemy_rows()
        if len(rows) <= 1:
            return None
        indices = [int(row.index or 0) for row in rows]
        current_index = max(1, int(fight.target_index or indices[0]))
        if current_index not in indices:
            fight.target_index = indices[0]
            return fight_selected_target()
        pos = indices.index(current_index)
        next_index = indices[(pos + 1) % len(indices)]
        fight.target_index = next_index
        return fight_selected_target()

    def fight_action_items():
        if len(fight_active_enemy_rows()) <= 0:
            return [MenuItem("Вернуться", Call("FightEnd"))]
        target_row = fight_selected_target()
        target_name = str(target_row.name or "цель") if target_row is not None else "цель"
        items = [
            MenuItem("Цель: {}".format(target_name), Call("FightCycleTarget")) if len(fight_active_enemy_rows()) > 1 else None,
            MenuItem("Уклониться", Call("FightDodge")),
            MenuItem("Блокировать", Call("FightBlock")),
            MenuItem(fight_attack_action_caption(), Call("FightAttack")),
        ]
        items = [row for row in items if row is not None]
        if fight_rifle_equipped() and int(fight.weapon_loaded or 0) == 1 and str(fight.loaded_ammo or "").strip() != "":
            items.append(MenuItem("Выстрелить ({})".format(fight_loaded_ammo_name(fight.loaded_ammo)), Call("FightShoot")))
        elif fight_rifle_equipped():
            if fight_supply_count("arrows") > 0:
                items.append(MenuItem("Перезарядить стрелой", Call("FightReload", "arrows")))
            if fight_supply_count("droplets") > 0:
                items.append(MenuItem("Перезарядить дробью", Call("FightReload", "droplets")))
        if fight_supply_count("bandage") > 0:
            items.append(MenuItem("Использовать бинт", Call("FightUseBandage")))
        if fight_supply_count("energy_tea") > 0:
            items.append(MenuItem("Выпить бодрящий чай", Call("FightDrinkEnergyTea")))
        if fight_supply_count("healing_potion") > 0:
            items.append(MenuItem("Выпить лечебное зелье", Call("FightDrinkHealingPotion")))
        if fight_supply_count("fire_bomb") > 0:
            items.append(MenuItem("Бросить огненную бутылку", Call("FightThrowFireBomb")))
        if fight_supply_count("bees_bomb") > 0:
            items.append(MenuItem("Бросить пчелиный заряд", Call("FightThrowBeesBomb")))
        items.append(MenuItem("Перевести дух", Call("FightCatchBreath")))
        if bool(fight_dog_support_state().get("active", False)):
            items.append(MenuItem("Командовать псом", Call("FightCommandDog")))
        if int(fight.retreat_used or 0) == 0:
            items.append(MenuItem("Скрыться", Call("FightRetreat")))
        else:
            items.append(MenuItem("Попытаться сбежать", Call("FightRetreat")))
        return items

    def fight_random_target():
        return fight_selected_target()

    def fight_apply_damage_to_enemy(amount, target_row=None):
        target = target_row or fight_random_target()
        if target is None:
            return None, 0
        damage = max(0, int(amount or 0))
        target.health = max(0, int(target.health or 0) - damage)
        return target, damage

    def fight_enemy_pick_move(enemy):
        enemy_status = dict(enemy.status or {})
        if int(enemy_status.get("paralyzed", 0) or 0) > 0:
            return "paralyzed"
        move_pool = list(enemy.moves or [])
        if len(move_pool) <= 0:
            return "attack"
        return str(procedural_choice(move_pool, fight_rng_key("enemy_move")) or "attack")

    def fight_hunt_intro_text(enemy_id="", enemy_count=1, room_code=""):
        enemy_template = fight_enemy_template(enemy_id)
        enemy_name = str(enemy_template.display_name or "зверь")
        enemy_count_value = max(1, int(enemy_count or 1))
        room_key = str(room_code or rooms.current_code or "").strip()

        if str(enemy_id or "") == "wolf" and enemy_count_value > 1:
            return "Вы замечаете свежие следы и вскоре понимаете, что это волчья стая. Между стволами уже мелькают серые спины: {} x{}.".format(enemy_name, enemy_count_value)
        if str(enemy_id or "") == "white_wolf":
            return "В чаще почти бесшумно показывается белый вожак. Он держится один и смотрит прямо на вас, будто оценивает противника. Такая встреча больше похожа на настоящий след леса, чем на простую охоту."
        if str(enemy_id or "") == "boar":
            return "В кустах раздается хриплое фырканье. Кабан уже рядом и явно не намерен уступать вам тропу."
        if str(enemy_id or "") in ("brown_bear", "giant_grizzly"):
            return "Воздух наполняется тяжелым звериным запахом. Из темноты выходит {} и поднимается на лапах, готовясь к драке.".format(enemy_name.lower())
        if room_key == "ForestDarkWoods":
            return "В темном лесу вы выходите прямо на добычу. Перед вами: {} x{}.".format(enemy_name, enemy_count_value)
        return "Вы выслеживаете зверя и вскоре натыкаетесь на него. Перед вами: {} x{}.".format(enemy_name, enemy_count_value)

    def fight_enemy_move_resolution(enemy, defence_mode="normal"):
        enemy_name = str(enemy.name or "Зверь")
        move_code = fight_enemy_pick_move(enemy)
        attack_roll = procedural_randint(int(enemy.attack_min or 0), int(enemy.attack_max or 0), fight_rng_key("enemy_attack"))
        extra_attack = 0
        move_text = ""
        move_energy_cost = 5
        if move_code == "paralyzed":
            return {"damage": 0, "text": "{} дергается, но боль и яд не дают ему толком двинуться.".format(enemy_name), "move": move_code}
        if move_code == "dodge":
            enemy.status = dict(enemy.status or {})
            enemy.status["evade_turns"] = 1
            move_text = "{} резко меняет траекторию и выжидает удобный миг.".format(enemy_name)
            attack_roll = max(0, attack_roll - 6)
            move_energy_cost = 4
        elif move_code == "bite":
            extra_attack = 2
            move_text = "{} бросается вперед, стараясь вцепиться клыками.".format(enemy_name)
            move_energy_cost = 7
        elif move_code == "surround":
            pack_bonus = max(1, len(fight_active_enemy_rows()) - 1)
            extra_attack = 2 + pack_bonus
            move_text = "{} вместе с остальными зверями старается зайти с боков и окружить вас.".format(enemy_name)
            move_energy_cost = 6
        elif move_code == "howl":
            move_text = "{} вскидывает голову и воет. От этого по спине пробегает холодок.".format(enemy_name)
            fight_apply_player_status("fear_turns", 1)
            attack_roll = max(0, attack_roll - 4)
            move_energy_cost = 3
        elif move_code == "dead_lock":
            extra_attack = 4
            move_text = "{} пытается вцепиться намертво и повалить вас на месте.".format(enemy_name)
            move_energy_cost = 9
        elif move_code == "ram":
            extra_attack = 6
            move_text = "{} резко опускает голову и идет на таран.".format(enemy_name)
            move_energy_cost = 10
        elif move_code == "defend":
            enemy.status = dict(enemy.status or {})
            enemy.status["guard_turns"] = 1
            move_text = "{} на миг уходит в оборону, прикрываясь массивным корпусом.".format(enemy_name)
            move_energy_cost = 3
            attack_roll = max(0, attack_roll - 7)
        elif move_code == "claws":
            extra_attack = 6
            move_text = "{} взмахивает тяжелой лапой, стараясь полоснуть когтями.".format(enemy_name)
        elif move_code == "strike":
            extra_attack = 8
            move_text = "{} прет напролом, используя всю свою массу.".format(enemy_name)
        elif move_code == "roar":
            move_text = "{} оглашает лес оглушительным рыком. На миг становится по-настоящему не по себе.".format(enemy_name)
            fight_apply_player_status("fear_turns", 2)
            attack_roll = max(0, attack_roll - 5)
            move_energy_cost = 5
        else:
            move_text = "{} идет в простую звериную атаку.".format(enemy_name)

        enemy.energy = max(0, int(enemy.energy or 0) - int(move_energy_cost or 0))
        health_now = max(0, int(enemy.health or 0))
        health_max = max(1, int(enemy.health_max or 1))
        if health_now * 4 <= health_max:
            attack_roll = max(0, attack_roll - 5)
            extra_attack = max(0, extra_attack - 3)
            move_text += " Раны заметно мешают ему бить в полную силу."
        if health_now * 10 <= health_max:
            attack_roll = max(0, attack_roll - 6)
            extra_attack = max(0, extra_attack - 4)
            move_text += " Он едва держится на ногах."
        if int(enemy.energy or 0) <= 0:
            attack_roll = max(0, attack_roll - 8)
            extra_attack = max(0, extra_attack - 4)
            move_text += " Он уже выдыхается."
        attack_total = max(0, int(attack_roll + extra_attack))
        return {"damage": attack_total, "text": move_text, "move": move_code}

    def fight_retreat_success():
        active_rows = list(fight_active_enemy_rows() or [])
        if len(active_rows) <= 0:
            return True
        fight_level = fight_player_level()
        score = int(player.stats.exploration or 0) // 2 + fight_level * 12 + procedural_randint(1, 60, fight_rng_key("retreat"))
        difficulty = 40 + len(active_rows) * 10
        for enemy in active_rows:
            enemy_type = str(enemy.enemy_type or "")
            tactics = str(enemy.tactics or "")
            if enemy_type == "guard":
                difficulty += 18
            if tactics in ("formation", "pack"):
                difficulty += 8
            if "escape" in list(enemy.skills or []):
                difficulty += 5
        return score >= difficulty

    def fight_tick_statuses():
        total_dot = 0
        for enemy in fight_active_enemy_rows():
            status = dict(enemy.status or {})
            if int(status.get("bleed_turns", 0) or 0) > 0:
                bleed_damage = max(1, int(status.get("bleed_damage", 0) or 0))
                enemy.health = max(0, int(enemy.health or 0) - bleed_damage)
                total_dot += bleed_damage
                status["bleed_turns"] = max(0, int(status.get("bleed_turns", 0) or 0) - 1)
            if int(status.get("poison_turns", 0) or 0) > 0:
                poison_damage = max(1, int(status.get("poison_damage", 0) or 0))
                enemy.health = max(0, int(enemy.health or 0) - poison_damage)
                total_dot += poison_damage
                status["poison_turns"] = max(0, int(status.get("poison_turns", 0) or 0) - 1)
            if int(status.get("paralyzed", 0) or 0) > 0:
                status["paralyzed"] = max(0, int(status.get("paralyzed", 0) or 0) - 1)
            if int(status.get("guard_turns", 0) or 0) > 0:
                status["guard_turns"] = max(0, int(status.get("guard_turns", 0) or 0) - 1)
            if int(status.get("evade_turns", 0) or 0) > 0:
                status["evade_turns"] = max(0, int(status.get("evade_turns", 0) or 0) - 1)
            enemy.status = status
        if total_dot > 0:
            return "Раны и яд продолжают делать свое дело."
        return ""

    def fight_dead_enemy_exploration_reward():
        reward = 0
        for enemy in list(fight.enemy_party or []):
            if int(enemy.health or 0) > 0:
                continue
            reward += max(0, int(enemy.exploration_reward or 0))
        return int(reward or 0)

    def fight_collect_victory_loot():
        loot_rows = {}
        money_gain = 0
        for enemy in list(fight.enemy_party or []):
            if int(enemy.health or 0) > 0:
                continue
            for item_id, raw_qty in dict(enemy.loot or {}).items():
                qty = fight_roll_loot_quantity(raw_qty)
                loot_rows[item_id] = int(loot_rows.get(item_id, 0) or 0) + qty
            money_min = max(0, int(enemy.money_min or 0))
            money_max = max(money_min, int(enemy.money_max or money_min))
            if money_max > 0:
                money_gain += procedural_randint(money_min, money_max, fight_rng_key("loot_money"))
        for item_id, qty in dict(loot_rows or {}).items():
            player.add_item(item_id, int(qty or 0))
        if money_gain > 0:
            player.add_money(money_gain)
            loot_rows["money"] = money_gain
        exploration_gain = fight_dead_enemy_exploration_reward()
        if exploration_gain > 0:
            player.change_stat("exploration", exploration_gain)
        fight.victory_loot = dict(loot_rows or {})
        return dict(loot_rows or {})

    def fight_roll_loot_quantity(raw_qty):
        if isinstance(raw_qty, (tuple, list)) and len(raw_qty) >= 2:
            minimum = max(0, int(raw_qty[0] or 0))
            maximum = max(minimum, int(raw_qty[1] or minimum))
            return procedural_randint(minimum, maximum, fight_rng_key("loot_quantity"))
        return max(0, int(raw_qty or 0))

    def fight_loot_text():
        rows = []
        for item_id, qty in dict(fight.victory_loot or {}).items():
            if str(item_id or "") == "money":
                rows.append("{} мараведи".format(int(qty or 0)))
                continue
            item_obj = get_game_item(item_id)
            item_name = str(getattr(item_obj, "name", item_id) or item_id)
            gained_count = max(0, int(qty or 0))
            total_count = max(0, int(player.item_count(item_id) or 0))
            if total_count > gained_count:
                rows.append("{} x{} (всего x{})".format(item_name, gained_count, total_count))
            else:
                rows.append("{} x{}".format(item_name, gained_count))
        return ", ".join(rows)

    def fight_apply_end_consequences(outcome=""):
        result_key = str(outcome or "").strip()
        minutes = 20
        if result_key == "retreat":
            minutes = 10
        elif result_key == "defeat":
            minutes = 60
        calendar_v2.advance_minutes(minutes)
        fight.last_result = {
            "outcome": result_key,
            "enemy_id": str(fight.enemy_id or ""),
            "enemy_count": len(list(fight.enemy_party or [])),
            "loot": dict(fight.victory_loot or {}),
            "minutes": int(minutes or 0),
            "day": int(current_game_day()),
        }
        update_stat_state()
        return minutes

    def fight_hunt_candidates(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        candidates = []
        for row in list(FOREST_HUNT_ROOM_TABLE.get(room_key, []) or []):
            if int(player.stats.exploration or 0) >= int(row.get("min_exploration", 0) or 0):
                candidates.append(dict(row))
        return candidates

    def fight_can_hunt_here(room_code=""):
        return hunt_available() and len(fight_hunt_candidates(room_code)) > 0

    def fight_roll_hunt_enemy(room_code=""):
        candidates = list(fight_hunt_candidates(room_code) or [])
        if len(candidates) <= 0:
            return {"enemy_id": "wolf", "enemy_count": 1}
        total_weight = sum(max(1, int(row.get("weight", 1) or 1)) for row in candidates)
        roll = procedural_randint(1, max(1, total_weight), "hunt_pick_%s" % str(room_code or ""))
        picked = candidates[-1]
        passed = 0
        for row in candidates:
            passed += max(1, int(row.get("weight", 1) or 1))
            if roll <= passed:
                picked = row
                break
        return {
            "enemy_id": str(picked.get("enemy_id", "wolf") or "wolf"),
            "enemy_count": procedural_randint(int(picked.get("count_min", 1) or 1), int(picked.get("count_max", 1) or 1), "hunt_count_%s_%s" % (str(room_code or ""), str(picked.get("enemy_id", "wolf") or "wolf"))),
        }

    def fight_begin(enemy_id="wolf", enemy_count=1, return_room="", picture="", intro_text=""):
        fight.enemy_id = str(enemy_id or "wolf")
        fight.enemy_party = fight_build_enemy_party(enemy_id, enemy_count)
        fight.return_room_code = str(return_room or rooms.current_code or "").strip()
        fight.return_picture = str(picture or scene_runtime.picture or "").strip()
        fight.victory_loot = {}
        fight.outcome_kind = ""
        fight.last_result = {}
        fight.status_state = {}
        fight.target_index = 1
        main_ui_runtime.mode = "fight"
        main_ui_runtime.action_title = "Команды"
        main_ui_runtime.action_content = None
        scene_runtime.picture = str(picture or "images/forest/forest_1.png")
        scene_runtime.text = str(intro_text or fight_preview_text())
        scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items = fight_action_items()

    def fight_finish_to_room(text):
        return_room = str(fight.return_room_code or rooms.current_code or "").strip()
        return_picture = str(fight.return_picture or "")
        main_ui_runtime.mode = "scene"
        fight.enemy_party = []
        fight.enemy_id = ""
        fight.target_index = 1
        fight.outcome_kind = ""
        fight.victory_loot = {}
        fight.status_state = {}
        main_ui_runtime.action_content = None
        main_ui_runtime.action_title = "Действия"
        main_ui_runtime.action_items = []
        if return_room and return_room != str(rooms.current_code or ""):
            rooms.enter(return_room)
        scene_runtime.picture = return_picture
        scene_runtime.text = str(text or "")
        scene_runtime.location_text = scene_runtime.text

    def fight_apply_enemy_phase(defence_mode="normal"):
        active_rows = list(fight_active_enemy_rows() or [])
        if len(active_rows) <= 0:
            return "С вашей добычей покончено."

        phase_lines = []
        if str(defence_mode or "") == "dodge" and procedural_randint(1, 100, fight_rng_key("dodge")) <= 60:
            for enemy in active_rows:
                phase_lines.append(str(fight_enemy_move_resolution(enemy, defence_mode).get("text", "") or ""))
            phase_lines.append("Вам удается сорваться в сторону и избежать худшего.")
            return "\n\n".join([row for row in phase_lines if str(row or "").strip() != ""])

        if str(defence_mode or "") == "dodge":
            defence_points = max(0, int(fight_player_defence_roll() or 0) // 3)
        elif str(defence_mode or "") == "block":
            defence_points = max(0, int(fight_player_defence_roll() or 0) + 8)
        else:
            defence_points = max(0, int(fight_player_defence_roll() or 0))

        player_damage = 0
        dog_damage = 0
        for enemy in active_rows:
            move_row = fight_enemy_move_resolution(enemy, defence_mode)
            phase_lines.append(str(move_row.get("text", "") or ""))
            move_damage = max(0, int(move_row.get("damage", 0) or 0))
            if move_damage <= 0:
                continue
            enemy_defence_slice = max(0, int(defence_points / max(1, len(active_rows))))
            applied_damage = max(0, move_damage - enemy_defence_slice)
            if applied_damage <= 0:
                continue
            if str(enemy.enemy_type or "") == "beast" and bool(fight_dog_support_state().get("active", False)) and procedural_randint(1, 2, fight_rng_key("enemy_target")) == 2:
                dog.receive_damage(applied_damage)
                dog_damage += applied_damage
            else:
                player_damage += applied_damage
                move_code = str(move_row.get("move", "") or "")
                if move_code == "dead_lock":
                    fight_apply_player_status("locked_turns", 1)
                elif move_code in ("ram", "strike"):
                    fight_apply_player_status("stagger_turns", 1)

        player.change_stat("health", -player_damage)
        if player_damage <= 0 and dog_damage <= 0:
            phase_lines.append("Вы выдерживаете натиск и не получаете заметного урона.")
        else:
            if player_damage > 0:
                phase_lines.append("К концу вражеского натиска вы теряете {} здоровья.".format(int(player_damage or 0)))
            if dog_damage > 0:
                phase_lines.append("Пес принимает часть натиска и теряет {} здоровья.".format(int(dog_damage or 0)))
                if not dog.is_alive():
                    phase_lines.append("Пес тяжело ранен и больше не может продолжать бой.")
        return "\n\n".join([row for row in phase_lines if str(row or "").strip() != ""])

    def fight_start_player_action():
        fight_tick_statuses()
        if len(fight_active_enemy_rows()) <= 0:
            fight_collect_victory_loot()
            return {"done": "victory", "text": "Схватка уже окончена."}
        return None

    def fight_enemy_response(result_lines, defence_mode="normal"):
        fight_decay_player_statuses()
        enemy_text = fight_apply_enemy_phase(defence_mode)
        if enemy_text:
            result_lines.append(enemy_text)

    def fight_finish_player_action(result_lines):
        if int(player.condition.health or 0) <= 0:
            player.set_stat("health", 1)
            player.condition.sick_days = max(2, int(player.condition.sick_days or 0))
            player.change_stat("notoriety", -6)
            return {"done": "defeat", "text": "\n\n".join(result_lines + ["Вас жестоко помяли. Вы еле уносите ноги и потом будете болеть несколько дней."])}

        if len(fight_active_enemy_rows()) <= 0:
            exploration_text = fight_dead_enemy_exploration_reward()
            loot_rows = fight_collect_victory_loot()
            loot_text = fight_loot_text()
            victory_line = "Вы побеждаете в схватке."
            if loot_text:
                victory_line += "\n\nВы забираете добычу: {}.".format(loot_text)
            if exploration_text > 0:
                victory_line += "\n\nВы лучше понимаете эти леса: исследование +{}.".format(exploration_text)
            return {"done": "victory", "text": "\n\n".join(result_lines + [victory_line]), "loot": loot_rows}

        return {"done": "continue", "text": "\n\n".join(result_lines)}

    def fight_attack():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        fight_spend_energy(8)
        target = fight_random_target()
        target_status = dict(target.status or {}) if target is not None else {}
        defence = procedural_randint(int(target.defence_min or 0), int(target.defence_max or 0), fight_rng_key("target_defence")) if target else 0
        defence += 5 * int(target_status.get("guard_turns", 0) or 0)
        defence += 4 * int(target_status.get("evade_turns", 0) or 0)
        damage = max(0, int(fight_player_attack_roll() or 0) - defence)
        target, dealt = fight_apply_damage_to_enemy(damage, target)
        result_lines.append("Вы идете в ближний бой и наносите {} урона.".format(int(dealt or 0)))
        fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_change_target():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        target = fight_cycle_target()
        if target is None:
            result_lines.append("Сейчас менять цель не на кого.")
        else:
            result_lines.append("Вы переводите внимание на цель: {}.".format(str(target.name or "враг")))
        return fight_finish_player_action(result_lines)

    def fight_shoot():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        loaded_ammo = str(fight.loaded_ammo or "").strip()
        if not fight_rifle_equipped():
            result_lines.append("У вас не экипировано ружье.")
        elif int(fight.weapon_loaded or 0) != 1 or loaded_ammo == "":
            result_lines.append("Оружие еще не заряжено.")
        else:
            fight_spend_energy(5)
            target = fight_random_target()
            if loaded_ammo == "droplets":
                damage = procedural_randint(15, 30, fight_rng_key("shot_droplets"))
                target, dealt = fight_apply_damage_to_enemy(damage, target)
                result_lines.append("Вы стреляете дробью и наносите {} урона.".format(int(dealt or 0)))
            else:
                damage = procedural_randint(8, 14, fight_rng_key("shot_arrow"))
                target, dealt = fight_apply_damage_to_enemy(damage, target)
                if target is not None:
                    status = dict(target.status or {})
                    status["bleed_turns"] = 5
                    status["bleed_damage"] = max(1, int(target.health_max or 1) // 10)
                    target.status = status
                result_lines.append("Вы выпускаете стрелу и наносите {} урона. Рана начинает кровоточить.".format(int(dealt or 0)))
            fight.loaded_ammo = ""
            fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_reload(ammo_code="arrows"):
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        reload_ammo = "droplets" if str(ammo_code or "").strip() == "droplets" else "arrows"
        if not fight_rifle_equipped():
            result_lines.append("Перезаряжать нечего: ружье не экипировано.")
        elif int(fight.weapon_loaded or 0) == 1 and str(fight.loaded_ammo or "").strip() != "":
            result_lines.append("Оружие уже заряжено.")
        elif fight_supply_count(reload_ammo) <= 0:
            result_lines.append("Нужного боеприпаса при себе не осталось.")
        elif reload_ammo == "droplets" and fight_supply_count("gunpowder") <= 0:
            result_lines.append("Для дробового заряда у вас не осталось пороха.")
        else:
            fight_spend_energy(4)
            fight_consume_supply(reload_ammo)
            if reload_ammo == "droplets":
                fight_consume_supply("gunpowder")
            fight.loaded_ammo = reload_ammo
            result_lines.append("Вы быстро перезаряжаете оружие: {}.".format(fight_loaded_ammo_name(reload_ammo)))
        fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_dodge():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        fight_spend_energy(4)
        result_lines.append("Вы сосредотачиваетесь на уклонении.")
        fight_enemy_response(result_lines, "dodge")
        return fight_finish_player_action(result_lines)

    def fight_block():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        fight_spend_energy(3)
        result_lines.append("Вы занимаете более защищенную стойку.")
        fight_enemy_response(result_lines, "block")
        return fight_finish_player_action(result_lines)

    def fight_use_bandage():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        if fight_supply_count("bandage") <= 0:
            result_lines.append("У вас нет бинта.")
        else:
            fight_spend_energy(2)
            fight_consume_supply("bandage")
            player.change_stat("health", 12)
            result_lines.append("Вы торопливо перевязываете раны и восстанавливаете немного сил.")
            fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_drink_energy_tea():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        if fight_supply_count("energy_tea") <= 0:
            result_lines.append("У вас нет бодрящего чая.")
        else:
            fight_consume_supply("energy_tea")
            fight_restore_energy(15)
            result_lines.append("Вы делаете несколько глотков бодрящего чая.")
            fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_drink_healing_potion():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        if fight_supply_count("healing_potion") <= 0:
            result_lines.append("У вас нет лечебного зелья.")
        else:
            fight_consume_supply("healing_potion")
            player.change_stat("health", 25)
            result_lines.append("Вы выпиваете зелье и чувствуете, как возвращаются силы.")
            fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_throw_bees_bomb():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        if fight_supply_count("bees_bomb") <= 0:
            result_lines.append("У вас нет пчелиного заряда.")
        else:
            fight_spend_energy(4)
            fight_consume_supply("bees_bomb")
            for enemy in fight_active_enemy_rows():
                status = dict(enemy.status or {})
                status["paralyzed"] = 3
                status["poison_turns"] = 5
                status["poison_damage"] = 5
                enemy.status = status
            result_lines.append("Вы бросаете пчелиный заряд. Противники в панике теряют строй.")
        return fight_finish_player_action(result_lines)

    def fight_throw_fire_bomb():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        if fight_supply_count("fire_bomb") <= 0:
            result_lines.append("У вас нет огненной бутылки.")
        else:
            fight_spend_energy(4)
            fight_consume_supply("fire_bomb")
            fire_hits = []
            for enemy in fight_active_enemy_rows():
                damage = procedural_randint(10, 18, fight_rng_key("fire_bomb"))
                target, dealt = fight_apply_damage_to_enemy(damage, enemy)
                if target is not None:
                    fire_hits.append("{}: {}".format(str(target.name or "цель"), int(dealt or 0)))
            if len(fire_hits) > 0:
                result_lines.append("Вы разбиваете огненную бутылку о землю перед противниками. Пламя вспыхивает сразу в нескольких местах: {}.".format(", ".join(fire_hits)))
            else:
                result_lines.append("Вы разбиваете огненную бутылку, но рядом уже не остается ни одной цели.")
            fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_catch_breath():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        fight_restore_energy(6)
        result_lines.append("Вы переводите дух и немного восстанавливаете силы.")
        fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_command_dog():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        result_lines = []
        dog_state = fight_dog_support_state()
        if not bool(dog_state.get("active", False)):
            result_lines.append("Пса рядом нет.")
        else:
            target = fight_random_target()
            target, dealt = fight_apply_damage_to_enemy(int(dog_state.get("attack", 0) or 0), target)
            if int(getattr(dog, "level", 0) or 0) >= 2 and target is not None:
                target_status = dict(target.status or {})
                target_status["paralyzed"] = max(1, int(target_status.get("paralyzed", 0) or 0))
                target.status = target_status
                result_lines.append("Пес вцепляется в противника мертвой хваткой, нанося {} урона и сбивая его с темпа.".format(int(dealt or 0)))
            else:
                result_lines.append("Пес бросается вперед и рвет противника, нанося {} урона.".format(int(dealt or 0)))
            fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def fight_retreat():
        immediate_result = fight_start_player_action()
        if immediate_result is not None:
            return immediate_result
        fight.retreat_used = int(fight.retreat_used or 0) + 1
        if fight_retreat_success():
            player.change_stat("notoriety", -6)
            if int(player.condition.health or 0) <= 20:
                player.condition.sick_days = max(2, int(player.condition.sick_days or 0))
            return {"done": "retreat", "text": "Вы выбираете момент и отступаете из схватки. Такой исход бьет по вашей репутации, но вы уходите на своих ногах."}
        result_lines = ["Вы пытаетесь отступить, но противники не дают вам разорвать дистанцию."]
        fight_enemy_response(result_lines, "normal")
        return fight_finish_player_action(result_lines)

    def forest_trap_can_place(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        active_rooms = hunt.trap_rooms if isinstance(hunt.trap_rooms, dict) else {}
        return bool(fight_can_hunt_here(room_key)) and int(player.item_count("hunting_trap_001") or 0) > 0 and room_key not in active_rooms

    def forest_trap_can_check(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        active_rooms = hunt.trap_rooms if isinstance(hunt.trap_rooms, dict) else {}
        if room_key in active_rooms:
            return int(current_game_day()) > int(dict(active_rooms.get(room_key, {}) or {}).get("day", -1) or -1)
        return False

    def forest_trap_set(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        if not forest_trap_can_place(room_key):
            return {"ok": False, "text": "Сейчас вы не можете поставить здесь ловушку."}
        player.remove_item("hunting_trap_001", 1)
        active_rooms = hunt.trap_rooms if isinstance(hunt.trap_rooms, dict) else {}
        active_rooms[room_key] = {"day": int(current_game_day()), "armed_count": 1}
        hunt.trap_rooms = active_rooms
        return {"ok": True, "text": "Вы тщательно ставите охотничью ловушку и маскируете ее листвой. Проверить ее лучше не раньше завтрашнего дня."}

    def forest_trap_check(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        if not forest_trap_can_check(room_key):
            return {"ok": False, "text": "Ловушку пока рано проверять или здесь ее нет."}
        active_rooms = hunt.trap_rooms if isinstance(hunt.trap_rooms, dict) else {}
        if room_key in active_rooms:
            active_rooms.pop(room_key, None)
        hunt.trap_rooms = active_rooms
        roll = procedural_randint(1, 100, "forest_trap_%s_%s" % (room_key, int(current_game_day())))
        if roll <= 35:
            return {"ok": True, "text": "Вы проверяете ловушку, но она сработала впустую. Добыча ушла.", "loot": {}}
        if roll <= 70:
            player.add_item("wolf_skin_001", 1)
            return {"ok": True, "text": "В ловушке запутался молодой волк. Шкуру с него еще можно снять.", "loot": {"wolf_skin_001": 1}}
        player.add_item("boar_meat_001", 1)
        player.add_item("boar_fang_001", 1)
        return {"ok": True, "text": "Ловушка помогла вам завалить кабана. Вы успеваете взять мясо и клык.", "loot": {"boar_meat_001": 1, "boar_fang_001": 1}}

    def dog_catch_delinquent_apply(event_kind="horse"):
        if not dog.prevents_theft(event_kind):
            return {"ok": False, "text": "Пса рядом нет или он пока не может вам помочь."}
        event_key = str(event_kind or "").strip()
        if event_key == "horse":
            roll = procedural_randint(1, 100, "dog_catch_horse_%s" % int(current_game_day()))
            if roll > 70:
                return {
                    "ok": False,
                    "text": "Пес учуял возню у конюшни и поднял лай, но вор все-таки успел вырваться в темноту и увести коня.",
                    "money_gain": 0,
                }
            paid_price = max(0, int(player.horse.purchase_price or 0))
            ransom = max(0, (paid_price * 2) // 3)
            if ransom > 0:
                player.add_money(ransom)
            for girl_key in ("sandra", "melissa", "amanda"):
                girl_info = people.get_info(girl_key)
                if girl_info is not None:
                    girl_info.change_social(friend_delta=2)
            player.change_stat("notoriety", 3)
            player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 2
            return {
                "ok": True,
                "text": "Ночью Монгол все-таки полез за вашим конем, но пес вовремя поднял лай, бросился на него и повалил прямо у ворот. Прижатый к земле и изрядно перепуганный барышник предпочитает откупиться за свою шкуру и свободу: возвращает вам {} мараведи, то есть две трети цены, что вы когда-то отдали за коня.".format(ransom),
                "money_gain": ransom,
            }
        loot_table = [
            {"item_id": "rope_001", "qty": 1, "money": 8},
            {"item_id": "drink_ale_001", "qty": 1, "money": 10},
            {"item_id": "gunpowder_001", "qty": 1, "money": 12},
            {"item_id": "dog_bone_001", "qty": 2, "money": 6},
        ]
        loot_row = dict(procedural_choice(loot_table, "dog_catch_loot_%s_%s" % (event_key, int(current_game_day()))))
        item_id = str(loot_row.get("item_id", "") or "")
        qty = max(1, int(loot_row.get("qty", 1) or 1))
        money_gain = max(0, int(loot_row.get("money", 0) or 0))
        if item_id:
            player.add_item(item_id, qty)
        player.add_money(money_gain)
        for girl_key in ("sandra", "melissa", "amanda"):
            girl_info = people.get_info(girl_key)
            if girl_info is not None:
                girl_info.change_social(friend_delta=2)
        player.change_stat("notoriety", 3)
        player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 2
        item_name = str(getattr(get_game_item(item_id), "name", item_id) or item_id)
        return {
            "ok": True,
            "text": "Пес бросается на вора, валит его на землю и не дает уйти. При обыске у него находятся {} x{} и еще {} мараведи. В трактире быстро узнают, что пес спас ваше добро.".format(item_name, qty, money_gain),
            "item_id": item_id,
            "qty": qty,
            "money_gain": money_gain,
        }

    def fight_preview_text():
        dog_state = fight_dog_support_state()
        enemy_rows = []
        for enemy in list(fight.enemy_party or []):
            enemy_rows.append("%s: %s/%s HP" % (str(enemy.name or ""), str(enemy.health), str(enemy.health_max)))
        lines = [
            "Подготовка к бою.",
            "Ваш уровень боя: %s." % str(fight_player_level()),
            "Здоровье: %s/100." % str(int(player.condition.health or 0)),
            "Атака: %s." % str(fight_player_attack_preview_text()),
            "Защита: %s." % str(fight_player_defence_preview_text()),
        ]
        if dog_state.get("active", False):
            lines.append("Пес рядом: укус %s, защита %s." % (str(dog_state.get("attack", 0)), str(dog_state.get("defence", 0))))
        if enemy_rows:
            lines.append("Противники:\n" + "\n".join(enemy_rows))
        return "\n\n".join(lines)

    def fight_company_display_rows():
        rows = [{
            "name": "Вы",
            "health": int(player.condition.health or 0),
            "health_max": 100,
            "energy": int(player.condition.energy or 0),
            "energy_max": 100,
            "subtitle": "уровень боя {} | репутация {} | дурная слава {} | исследование {}".format(
                int(fight_player_level()),
                int(player_reputation_breakdown().get("reputation", 0) or 0),
                int(player.stats.notoriety or 0),
                int(player.stats.exploration or 0),
            ),
            "fight_level": int(fight_player_level()),
            "reputation": int(player_reputation_breakdown().get("reputation", 0) or 0),
            "notoriety": int(player.stats.notoriety or 0),
            "exploration": int(player.stats.exploration or 0),
            "tavernfame": int(player.economy.tavern_fame or 0),
            "money": int(player.economy.money or 0),
            "sick_days": int(player.condition.sick_days or 0),
            "fun": int(player.condition.fun or 0),
            "status": fight_player_status_labels(),
            "attack_text": fight_player_attack_preview_text(),
            "defence_text": fight_player_defence_preview_text(),
            "speed": fight_player_speed_points(),
            "weapon": fight_player_weapon_name(),
            "tactics": "адаптивная",
            "skills": ["ближний бой"],
        }]

        dog_state = fight_dog_support_state()
        if bool(dog_state.get("active", False)):
            rows.append({
                "name": str(getattr(dog, "name", "Пес") or "Пес"),
                "health": int(getattr(dog, "health", 0) or 0),
                "health_max": int(getattr(dog, "max_health", 0) or 0),
                "energy": int(getattr(dog, "loyalty", 0) or 0),
                "energy_max": int(getattr(dog, "max_loyalty", 0) or 0),
                "subtitle": str(getattr(dog, "skill_name", "Укус") or "Укус"),
                "status": [],
            })

        for companion_key in list(player.combat.party or []):
            comp_key = str(companion_key or "").strip().lower()
            if not comp_key or comp_key == "dog":
                continue
            rows.append({
                "name": comp_key,
                "health": 0,
                "health_max": 0,
                "energy": 0,
                "energy_max": 0,
                "subtitle": "спутник",
                "status": [],
            })
        return rows

    def fight_enemy_display_rows():
        rows = []
        selected_index = max(1, int(fight.target_index or 1))
        for enemy in list(fight.enemy_party or []):
            status_labels = []
            enemy_status = dict(enemy.status or {})
            if int(enemy_status.get("bleed_turns", 0) or 0) > 0:
                status_labels.append("кровотечение")
            if int(enemy_status.get("poison_turns", 0) or 0) > 0:
                status_labels.append("яд")
            if int(enemy_status.get("paralyzed", 0) or 0) > 0:
                status_labels.append("паралич")
            if int(enemy_status.get("guard_turns", 0) or 0) > 0:
                status_labels.append("оборона")
            if int(enemy_status.get("evade_turns", 0) or 0) > 0:
                status_labels.append("уклонение")
            if int(enemy.index or 0) == selected_index and int(enemy.health or 0) > 0:
                status_labels.insert(0, "цель")
            rows.append({
                "name": str(enemy.name or ""),
                "health": int(enemy.health or 0),
                "health_max": int(enemy.health_max or 0),
                "energy": int(enemy.energy or 0),
                "energy_max": int(enemy.energy_max or 0),
                "subtitle": "оружие: {} | атака {}-{} | защита {}-{} | тактика: {}".format(
                    str(enemy.weapon or "тело"),
                    int(enemy.attack_min or 0),
                    int(enemy.attack_max or 0),
                    int(enemy.defence_min or 0),
                    int(enemy.defence_max or 0),
                    str(enemy.tactics or "простая"),
                ),
                "weapon": str(enemy.weapon or "тело"),
                "attack_text": "{}-{}".format(int(enemy.attack_min or 0), int(enemy.attack_max or 0)),
                "defence_text": "{}-{}".format(int(enemy.defence_min or 0), int(enemy.defence_max or 0)),
                "tactics": str(enemy.tactics or "простая"),
                "speed": fight_enemy_speed_points(enemy),
                "skills": list(enemy.skills or []),
                "status": status_labels,
            })
        return rows

default fight = FightInfo()
default hunt = HuntInfo()


label FightStart(enemy_id="wolf", enemy_count=1):
    $ fight_begin(enemy_id, enemy_count, rooms.current_code, "images/forest/forest_1.png")
    call FightLoop
    return


label FightLoop:
    while str(main_ui_runtime.mode or "") == "fight":
        call screen main_ui
    return


label FightStartHuntCurrentRoom:
    $ renpy.dynamic("_hunt_roll", "_hunt_loaded_ammo", "_hunt_has_ranged_ammo", "_fight_room_code", "_fight_picture", "_fight_enemy_id", "_fight_enemy_count", "_fight_intro_text")
    $ _hunt_loaded_ammo = str(rusty_hunter_rifle_loaded_ammo() or "").strip()
    $ _hunt_has_ranged_ammo = _hunt_loaded_ammo != "" or fight_supply_count("arrows") > 0 or (fight_supply_count("droplets") > 0 and fight_supply_count("gunpowder") > 0)
    if not _hunt_has_ranged_ammo and player.item_count("old_axe_001") > 0 and str(player.equipment.weapon or "") in ("", "rusty_hunter_rifle_001"):
        $ player.equip("old_axe_001", "weapon")
    $ _hunt_roll = fight_roll_hunt_enemy(str(getattr(rooms.current, "code_name", "") or rooms.current_code or ""))
    $ _fight_room_code = str(getattr(rooms.current, "code_name", "") or rooms.current_code or "")
    $ _fight_picture = str(scene_runtime.picture or "")
    $ _fight_enemy_id = str(_hunt_roll.get("enemy_id", "wolf") or "wolf")
    $ _fight_enemy_count = max(1, int(_hunt_roll.get("enemy_count", 1) or 1))
    $ _fight_intro_text = fight_hunt_intro_text(_fight_enemy_id, _fight_enemy_count, _fight_room_code)
    $ fight_begin(_fight_enemy_id, _fight_enemy_count, _fight_room_code, _fight_picture, _fight_intro_text)
    call FightLoop
    $ main_ui_runtime.action_content = None
    if _fight_room_code == "Forest":
        $ main_ui_runtime.action_title = "Действия"
        $ main_ui_runtime.action_items = forest_action_items()
    else:
        $ main_ui_runtime.action_title = str(getattr(rooms.current, "display_name", "") or "Действия")
        $ main_ui_runtime.action_items = forest_subroom_action_items(rooms.current)
    return


label FightAttack:
    call FightApplyActionResult(fight_attack())
    return


label FightCycleTarget:
    call FightApplyActionResult(fight_change_target())
    return


label FightShoot:
    call FightApplyActionResult(fight_shoot())
    return


label FightReload(ammo_code="arrows"):
    call FightApplyActionResult(fight_reload(ammo_code))
    return


label FightDodge:
    call FightApplyActionResult(fight_dodge())
    return


label FightBlock:
    call FightApplyActionResult(fight_block())
    return


label FightUseBandage:
    call FightApplyActionResult(fight_use_bandage())
    return


label FightDrinkEnergyTea:
    call FightApplyActionResult(fight_drink_energy_tea())
    return


label FightDrinkHealingPotion:
    call FightApplyActionResult(fight_drink_healing_potion())
    return


label FightThrowBeesBomb:
    call FightApplyActionResult(fight_throw_bees_bomb())
    return


label FightThrowFireBomb:
    call FightApplyActionResult(fight_throw_fire_bomb())
    return


label FightCatchBreath:
    call FightApplyActionResult(fight_catch_breath())
    return


label FightCommandDog:
    call FightApplyActionResult(fight_command_dog())
    return


label FightRetreat:
    call FightApplyActionResult(fight_retreat())
    return


label FightApplyActionResult(_fight_result):
    $ renpy.dynamic("_fight_minutes", "_fight_done")
    $ scene_runtime.text = str(_fight_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    if str(_fight_result.get("done", "") or "") == "continue":
        $ main_ui_runtime.action_items = fight_action_items()
        return
    if str(_fight_result.get("done", "") or "") == "victory":
        $ _fight_minutes = fight_apply_end_consequences("victory")
        $ scene_runtime.text = scene_runtime.text + "\n\nНа схватку уходит %d минут." % int(_fight_minutes or 0)
        $ scene_runtime.location_text = scene_runtime.text
        $ fight.outcome_kind = "victory"
        $ main_ui_runtime.action_title = "Победа"
        $ main_ui_runtime.action_items = [MenuItem("Забрать добычу и вернуться", Call("FightEnd"))]
        $ renpy.notify("Победа. Добыча: " + (fight_loot_text() or "нет"))
        return
    if str(_fight_result.get("done", "") or "") in ("defeat", "retreat"):
        $ _fight_done = str(_fight_result.get("done", "") or "")
        $ _fight_minutes = fight_apply_end_consequences(_fight_done)
        $ scene_runtime.text = scene_runtime.text + "\n\nНа исход схватки уходит %d минут." % int(_fight_minutes or 0)
        $ scene_runtime.location_text = scene_runtime.text
        $ fight.outcome_kind = _fight_done
        $ main_ui_runtime.action_title = "Поражение" if _fight_done == "defeat" else "Отступление"
        $ main_ui_runtime.action_items = [MenuItem("Вернуться", Call("FightEnd"))]
        $ renpy.notify("Поражение в бою." if _fight_done == "defeat" else "Вы отступили из боя.")
        return
    call FightEnd
    return


label FightEnd:
    $ renpy.dynamic("_fight_text")
    $ _fight_text = str(scene_runtime.text or "")
    $ fight_finish_to_room(_fight_text)
    return
label ForestSetTrap:
    $ renpy.dynamic("_trap_result")
    $ _trap_result = forest_trap_set(str(getattr(rooms.current, "code_name", "") or rooms.current_code or ""))
    $ scene_runtime.text = str(_trap_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    if str(getattr(rooms.current, "code_name", "") or "") == "Forest":
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
        $ main_ui_runtime.action_items = forest_action_items()
    else:
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
        $ main_ui_runtime.action_items = forest_subroom_action_items()
    return
label ForestCheckTrap:
    $ renpy.dynamic("_trap_result")
    $ _trap_result = forest_trap_check(str(getattr(rooms.current, "code_name", "") or rooms.current_code or ""))
    $ scene_runtime.text = str(_trap_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    if str(getattr(rooms.current, "code_name", "") or "") == "Forest":
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
        $ main_ui_runtime.action_items = forest_action_items()
    else:
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
        $ main_ui_runtime.action_items = forest_subroom_action_items()
    return
