# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default FightLoadedAmmo = ""
default FightTargetIndex = 1
default FightVictoryLoot = {}
default FightLevel = {"you": 1}
default company_list = []
default PlayerFightSupply = {"arrows": 0, "droplets": 0, "gunpowder": 0, "bees_bomb": 0, "fire_bomb": 0, "bandage": 0, "energy_tea": 0, "healing_potion": 0}
default FightWeaponLoaded = 0
default FightRetreatUsed = 0
default FightEnemyState = {}
default HuntUnlocked = False
default HuntLastResult = {}
default FightSideLog = []
default FightEnemyParty = []
default FightEnemyId = ""
default FightReturnRoomCode = ""
default FightReturnPicture = ""
default FightStatusState = {}
default FightOutcomeText = ""
default FightOutcomeKind = ""
default ForestTrapState = {"active": 0, "room": "", "day": -1, "armed_count": 0}
default ForestTrapRooms = {}

init -20 python:
    import random
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

        def get(self, key, default=None):
            return self.as_dict().get(key, default)

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

    class FightRuntimeView(object):
        @property
        def enemy_id(self):
            return str(FightEnemyId or "")

        @property
        def enemy_party(self):
            return FightEnemyParty

        @property
        def level(self):
            return FightLevel

        @level.setter
        def level(self, value):
            FightLevel.clear()
            FightLevel.update(dict(value or {}))

        @property
        def weapon_loaded(self):
            return int(FightWeaponLoaded or 0)

        @property
        def loaded_ammo(self):
            return str(FightLoadedAmmo or "")

        @property
        def supply(self):
            return PlayerFightSupply

        @property
        def outcome_popup(self):
            return {"kind": str(FightOutcomeKind or ""), "text": str(FightOutcomeText or "")}

        @property
        def return_picture(self):
            return str(FightReturnPicture or "")

    def fight_info():
        return FightRuntimeView()

    FIGHT_SUPPLY_DEFAULTS = {
        "arrows": 0,
        "droplets": 0,
        "gunpowder": 0,
        "bees_bomb": 0,
        "fire_bomb": 0,
        "bandage": 0,
        "energy_tea": 0,
        "healing_potion": 0,
    }

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
            loot={"wolf_skin_001": 1},
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
            loot={"boar_fang_001": 1, "boar_meat_001": 1},
        ),
        "brown_bear": FightEnemyDefinition(
            "brown_bear", "Бурый медведь", "beast", 90, 16, 28, 10, 18,
            moves=["bite", "claws", "strike", "roar"],
            skills=["maul", "fear"],
            tactics="press",
            loot={"bear_fur_brown_001": 1, "bear_claw_001": 1},
            exploration_reward=4,
        ),
        "giant_grizzly": FightEnemyDefinition(
            "giant_grizzly", "Гигантский гризли", "beast", 115, 20, 34, 12, 22,
            moves=["bite", "claws", "strike", "roar"],
            skills=["maul", "terror"],
            tactics="break_line",
            loot={"bear_fur_grizzly_001": 1, "bear_claw_001": 1},
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
    }
    ANIMAL_FIGHT_TABLE = FIGHT_ENEMY_DEFINITIONS

    def fight_supply_default_state():
        return dict(FIGHT_SUPPLY_DEFAULTS)

    def fight_ensure_runtime():
        global FightLevel, company_list, PlayerFightSupply, FightEnemyState, HuntLastResult
        global FightSideLog, FightEnemyParty, FightStatusState, health, ForestTrapState, ForestTrapRooms
        if not isinstance(FightLevel, dict):
            FightLevel = {"you": 1}
        if not isinstance(company_list, list):
            company_list = []
        if not isinstance(PlayerFightSupply, dict):
            PlayerFightSupply = fight_supply_default_state()
        for _key, _value in FIGHT_SUPPLY_DEFAULTS.items():
            PlayerFightSupply.setdefault(_key, _value)
        if not isinstance(FightEnemyState, dict):
            FightEnemyState = {}
        if not isinstance(HuntLastResult, dict):
            HuntLastResult = {}
        if not isinstance(FightSideLog, list):
            FightSideLog = []
        if not isinstance(FightEnemyParty, list):
            FightEnemyParty = []
        if not isinstance(FightStatusState, dict):
            FightStatusState = {}
        health = _player_clamp_stat(health, 0, 100)
        if not isinstance(ForestTrapState, dict):
            ForestTrapState = {"active": 0, "room": "", "day": -1, "armed_count": 0}
        if not isinstance(ForestTrapRooms, dict):
            ForestTrapRooms = {}

    def fight_sync_loaded_weapon_state_from_inventory():
        global FightLoadedAmmo, FightWeaponLoaded
        fight_ensure_runtime()
        loaded_ammo = ""
        if str(EquippedWeapon or "").strip() == "rusty_hunter_rifle_001":
            loaded_ammo = str(RustyHunterRifleLoadedAmmo or "").strip()
        FightLoadedAmmo = loaded_ammo
        FightWeaponLoaded = 1 if loaded_ammo else 0
        return loaded_ammo

    def fight_store_loaded_weapon_state():
        global RustyHunterRifleLoadedAmmo
        if str(EquippedWeapon or "").strip() == "rusty_hunter_rifle_001":
            RustyHunterRifleLoadedAmmo = str(FightLoadedAmmo or "").strip()

    def fight_loaded_ammo_name(ammo_code=""):
        ammo_key = str(ammo_code or "").strip()
        if ammo_key == "arrows":
            return "стрела"
        if ammo_key == "droplets":
            return "дробь"
        return "нет"

    def fight_sync_level_from_exploration():
        global HuntUnlocked
        fight_ensure_runtime()
        level = 1 + max(0, int(effective_player_exploration() or 0)) // 50
        FightLevel["you"] = max(1, int(level))
        HuntUnlocked = int(effective_player_exploration() or 0) >= 50
        return FightLevel["you"]

    def fight_sync_supply_from_inventory():
        global PlayerFightSupply
        fight_ensure_runtime()
        synced = fight_supply_default_state()
        for supply_key, item_id in FIGHT_SUPPLY_ITEM_MAP.items():
            try:
                synced[supply_key] = int(_player_item_count_by_id(item_id) or 0)
            except Exception:
                synced[supply_key] = 0
        for supply_key in ("bees_bomb",):
            synced[supply_key] = int(PlayerFightSupply.get(supply_key, 0) or 0)
        PlayerFightSupply = synced
        return dict(PlayerFightSupply)

    def fight_spend_energy(amount):
        global energy
        energy = max(0, int(energy or 0) - max(0, int(amount or 0)))
        return int(energy or 0)

    def fight_restore_energy(amount):
        global energy
        energy = min(100, int(energy or 0) + max(0, int(amount or 0)))
        return int(energy or 0)

    def fight_player_status_labels():
        fight_ensure_runtime()
        labels = []
        if int(FightStatusState.get("locked_turns", 0) or 0) > 0:
            labels.append("захват")
        if int(FightStatusState.get("fear_turns", 0) or 0) > 0:
            labels.append("страх")
        if int(FightStatusState.get("stagger_turns", 0) or 0) > 0:
            labels.append("сбит с ног")
        return labels

    def fight_decay_player_statuses():
        fight_ensure_runtime()
        for status_key in ("locked_turns", "fear_turns", "stagger_turns"):
            FightStatusState[status_key] = max(0, int(FightStatusState.get(status_key, 0) or 0) - 1)

    def fight_apply_player_status(status_key, turns=1):
        fight_ensure_runtime()
        turn_count = max(1, int(turns or 1))
        FightStatusState[status_key] = max(turn_count, int(FightStatusState.get(status_key, 0) or 0))

    def fight_weapon_attack_points():
        item_id = str(EquippedWeapon or "").strip()
        if not item_id:
            return 0
        item_obj = get_game_item(item_id)
        if item_obj is None:
            return 0
        return int(getattr(item_obj, "custom_properties", {}).get("attack_points", 0) or 0)

    def fight_rifle_equipped():
        return str(EquippedWeapon or "").strip() == "rusty_hunter_rifle_001"

    def fight_armor_defence_points():
        item_id = str(EquippedArmor or "").strip()
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
        weapon_key = str(EquippedWeapon or "").strip()
        if weapon_key:
            return fight_item_name(weapon_key, weapon_key)
        return "кулаки"

    def fight_player_armor_name():
        armor_key = str(EquippedArmor or "").strip()
        if armor_key:
            return fight_item_name(armor_key, armor_key)
        return "без брони"

    def fight_attack_action_caption():
        weapon_key = str(EquippedWeapon or "").strip()
        if weapon_key == "rusty_hunter_rifle_001":
            return "Бить прикладом"
        if weapon_key:
            return "Атаковать: {}".format(fight_player_weapon_name())
        return "Атаковать кулаками"

    def fight_player_attack_preview_text():
        fight_ensure_runtime()
        level = int(fight_sync_level_from_exploration() or 1)
        dog_state = fight_dog_support_state()
        attack_min = 5 + level * 5 + fight_weapon_attack_points() + int(dog_state.get("attack", 0) or 0)
        attack_max = attack_min + level * 3
        if int(energy or 0) < 20:
            attack_min -= 4
            attack_max -= 4
        if int(FightStatusState.get("locked_turns", 0) or 0) > 0:
            attack_min -= 5
            attack_max -= 5
        if int(FightStatusState.get("fear_turns", 0) or 0) > 0:
            attack_min -= 3
            attack_max -= 3
        return "{}-{}".format(max(0, int(attack_min)), max(0, int(attack_max)))

    def fight_player_defence_preview_text():
        fight_ensure_runtime()
        level = int(fight_sync_level_from_exploration() or 1)
        dog_state = fight_dog_support_state()
        defence_min = 5 + level * 4 + fight_armor_defence_points() + int(dog_state.get("defence", 0) or 0)
        defence_max = defence_min + level * 2
        if int(energy or 0) < 15:
            defence_min -= 3
            defence_max -= 3
        if int(FightStatusState.get("stagger_turns", 0) or 0) > 0:
            defence_min -= 5
            defence_max -= 5
        return "{}-{}".format(max(0, int(defence_min)), max(0, int(defence_max)))

    def fight_dog_support_state():
        ensure_dog_runtime()
        try:
            if not dog.owned or not dog.in_company or not dog.is_alive():
                return {"active": False, "attack": 0, "defence": 0, "moves": []}
            moves = ["bite", "guard", "harry"]
            if int(dog.level or 0) >= 2:
                moves.insert(1, "dead_lock_bite")
            return {
                "active": True,
                "attack": int(dog.bite_damage or 0),
                "defence": int(dog.defense or 0),
                "moves": moves,
            }
        except Exception:
            return {"active": False, "attack": 0, "defence": 0, "moves": []}

    def fight_player_attack_roll():
        fight_ensure_runtime()
        level = fight_sync_level_from_exploration()
        dog_state = fight_dog_support_state()
        base_attack = 5 + level * 5
        random_attack = random.randint(0, level * 3)
        attack_total = int(base_attack + fight_weapon_attack_points() + random_attack + int(dog_state.get("attack", 0) or 0))
        if int(energy or 0) < 20:
            attack_total -= 4
        if int(FightStatusState.get("locked_turns", 0) or 0) > 0:
            attack_total -= 5
        if int(FightStatusState.get("fear_turns", 0) or 0) > 0:
            attack_total -= 3
        return max(0, int(attack_total))

    def fight_player_defence_roll():
        fight_ensure_runtime()
        level = fight_sync_level_from_exploration()
        dog_state = fight_dog_support_state()
        base_defence = 5 + level * 4
        random_defence = random.randint(0, level * 2)
        defence_total = int(base_defence + fight_armor_defence_points() + random_defence + int(dog_state.get("defence", 0) or 0))
        if int(energy or 0) < 15:
            defence_total -= 3
        if int(FightStatusState.get("stagger_turns", 0) or 0) > 0:
            defence_total -= 5
        return max(0, int(defence_total))

    def fight_enemy_template(enemy_id="wolf"):
        definition = ANIMAL_FIGHT_TABLE.get(str(enemy_id or "").strip(), ANIMAL_FIGHT_TABLE["wolf"])
        if hasattr(definition, "as_dict"):
            return definition.as_dict()
        return dict(definition or ANIMAL_FIGHT_TABLE["wolf"].as_dict())

    def fight_selected_enemy_image():
        enemy_id = str(FightEnemyId or "").strip()
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
        template = fight_enemy_template(enemy_id)
        count = max(1, int(enemy_count or 1))
        party = []
        for idx in range(count):
            party.append({
                "id": template["id"],
                "name": template["name"],
                "index": idx + 1,
                "health": int(template["health"]),
                "health_max": int(template["health"]),
                "energy": int(template.get("energy", 0) or max(20, int(template["health"]))),
                "energy_max": int(template.get("energy", 0) or max(20, int(template["health"]))),
                "attack_min": int(template["attack_min"]),
                "attack_max": int(template["attack_max"]),
                "defence_min": int(template["defence_min"]),
                "defence_max": int(template["defence_max"]),
                "moves": list(template.get("moves", []) or []),
                "skills": list(template.get("skills", []) or []),
                "weapon": str(template.get("weapon", "") or ""),
                "tactics": str(template.get("tactics", "") or ""),
                "enemy_type": str(template.get("enemy_type", "") or ""),
                "loot": dict(template.get("loot", {}) or {}),
                "money_min": int(template.get("money_min", 0) or 0),
                "money_max": int(template.get("money_max", 0) or 0),
                "exploration_reward": int(template.get("exploration_reward", 0) or 0),
                "status": {},
            })
        return party

    def fight_active_enemy_rows():
        return [row for row in list(FightEnemyParty or []) if int(row.get("health", 0) or 0) > 0]

    def fight_selected_target():
        global FightTargetIndex
        rows = fight_active_enemy_rows()
        if len(rows) <= 0:
            return None
        selected_index = max(1, int(FightTargetIndex or 1))
        for row in rows:
            if int(row.get("index", 0) or 0) == selected_index:
                return row
        FightTargetIndex = int(rows[0].get("index", 1) or 1)
        return rows[0]

    def fight_cycle_target():
        global FightTargetIndex
        rows = fight_active_enemy_rows()
        if len(rows) <= 1:
            return None
        indices = [int(row.get("index", 0) or 0) for row in rows]
        current_index = max(1, int(FightTargetIndex or indices[0]))
        if current_index not in indices:
            FightTargetIndex = indices[0]
            return fight_selected_target()
        pos = indices.index(current_index)
        next_index = indices[(pos + 1) % len(indices)]
        FightTargetIndex = next_index
        return fight_selected_target()

    def fight_append_log(line):
        text = str(line or "").strip()
        if not text:
            return
        FightSideLog.append(text)
        if len(FightSideLog) > 8:
            del FightSideLog[:-8]

    def fight_refresh_ui_actions():
        global current_action_items
        if len(fight_active_enemy_rows()) <= 0:
            current_action_items = [MenuItem("Вернуться", Call("FightReturnToScene"))]
            return
        target_row = fight_selected_target()
        target_name = str(target_row.get("name", "цель") or "цель") if target_row is not None else "цель"
        items = [
            MenuItem("Цель: {}".format(target_name), Call("FightDoAction", "cycle_target")) if len(fight_active_enemy_rows()) > 1 else None,
            MenuItem("Уклониться", Call("FightDoAction", "dodge")),
            MenuItem("Блокировать", Call("FightDoAction", "block")),
            MenuItem(fight_attack_action_caption(), Call("FightDoAction", "attack")),
        ]
        items = [row for row in items if row is not None]
        if fight_rifle_equipped() and int(FightWeaponLoaded or 0) == 1 and str(FightLoadedAmmo or "").strip() != "":
            items.append(MenuItem("Выстрелить ({})".format(fight_loaded_ammo_name(FightLoadedAmmo)), Call("FightDoAction", "shoot")))
        elif fight_rifle_equipped():
            if int(PlayerFightSupply.get("arrows", 0) or 0) > 0:
                items.append(MenuItem("Перезарядить стрелой", Call("FightDoAction", "reload_arrows")))
            if int(PlayerFightSupply.get("droplets", 0) or 0) > 0:
                items.append(MenuItem("Перезарядить дробью", Call("FightDoAction", "reload_droplets")))
        if int(PlayerFightSupply.get("bandage", 0) or 0) > 0:
            items.append(MenuItem("Использовать бинт", Call("FightDoAction", "bandage")))
        if int(PlayerFightSupply.get("energy_tea", 0) or 0) > 0:
            items.append(MenuItem("Выпить бодрящий чай", Call("FightDoAction", "tea")))
        if int(PlayerFightSupply.get("healing_potion", 0) or 0) > 0:
            items.append(MenuItem("Выпить лечебное зелье", Call("FightDoAction", "potion")))
        if int(PlayerFightSupply.get("fire_bomb", 0) or 0) > 0:
            items.append(MenuItem("Бросить огненную бутылку", Call("FightDoAction", "fire_bomb")))
        if int(PlayerFightSupply.get("bees_bomb", 0) or 0) > 0:
            items.append(MenuItem("Бросить пчелиный заряд", Call("FightDoAction", "bees_bomb")))
        items.append(MenuItem("Перевести дух", Call("FightDoAction", "breath")))
        if bool(fight_dog_support_state().get("active", False)):
            items.append(MenuItem("Командовать псом", Call("FightDoAction", "dog")))
        items.append(MenuItem("Отступить", Call("FightDoAction", "retreat")))
        current_action_items = items

    def fight_random_target():
        return fight_selected_target()

    def fight_apply_damage_to_enemy(amount, target_row=None):
        target = target_row or fight_random_target()
        if target is None:
            return None, 0
        damage = max(0, int(amount or 0))
        target["health"] = max(0, int(target.get("health", 0) or 0) - damage)
        return target, damage

    def fight_enemy_pick_move(enemy):
        enemy_status = dict(enemy.get("status", {}) or {})
        if int(enemy_status.get("paralyzed", 0) or 0) > 0:
            return "paralyzed"
        move_pool = list(enemy.get("moves", []) or [])
        if len(move_pool) <= 0:
            return "attack"
        return str(random.choice(move_pool) or "attack")

    def fight_hunt_intro_text(enemy_id="", enemy_count=1, room_code=""):
        enemy_template = fight_enemy_template(enemy_id)
        enemy_name = str(enemy_template.get("name", "зверь") or "зверь")
        enemy_count_value = max(1, int(enemy_count or 1))
        room_key = str(room_code or CurLoc or "").strip()

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
        enemy_name = str(enemy.get("name", "Зверь") or "Зверь")
        move_code = fight_enemy_pick_move(enemy)
        attack_roll = random.randint(int(enemy.get("attack_min", 0) or 0), int(enemy.get("attack_max", 0) or 0))
        extra_attack = 0
        move_text = ""
        move_energy_cost = 5
        if move_code == "paralyzed":
            return {"damage": 0, "text": "{} дергается, но боль и яд не дают ему толком двинуться.".format(enemy_name), "move": move_code}
        if move_code == "dodge":
            enemy["status"] = dict(enemy.get("status", {}) or {})
            enemy["status"]["evade_turns"] = 1
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
            enemy["status"] = dict(enemy.get("status", {}) or {})
            enemy["status"]["guard_turns"] = 1
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

        enemy["energy"] = max(0, int(enemy.get("energy", 0) or 0) - int(move_energy_cost or 0))
        health_now = max(0, int(enemy.get("health", 0) or 0))
        health_max = max(1, int(enemy.get("health_max", 1) or 1))
        if health_now * 4 <= health_max:
            attack_roll = max(0, attack_roll - 5)
            extra_attack = max(0, extra_attack - 3)
            move_text += " Раны заметно мешают ему бить в полную силу."
        if health_now * 10 <= health_max:
            attack_roll = max(0, attack_roll - 6)
            extra_attack = max(0, extra_attack - 4)
            move_text += " Он едва держится на ногах."
        if int(enemy.get("energy", 0) or 0) <= 0:
            attack_roll = max(0, attack_roll - 8)
            extra_attack = max(0, extra_attack - 4)
            move_text += " Он уже выдыхается."
        attack_total = max(0, int(attack_roll + extra_attack))
        return {"damage": attack_total, "text": move_text, "move": move_code}

    def fight_retreat_success():
        active_rows = list(fight_active_enemy_rows() or [])
        if len(active_rows) <= 0:
            return True
        fight_level = int(fight_sync_level_from_exploration() or 1)
        score = int(exploration or 0) // 2 + fight_level * 12 + random.randint(1, 60)
        difficulty = 40 + len(active_rows) * 10
        for enemy in active_rows:
            enemy_type = str(enemy.get("enemy_type", "") or "")
            tactics = str(enemy.get("tactics", "") or "")
            if enemy_type == "guard":
                difficulty += 18
            if tactics in ("formation", "pack"):
                difficulty += 8
            if "escape" in list(enemy.get("skills", []) or []):
                difficulty += 5
        return score >= difficulty

    def fight_tick_statuses():
        total_dot = 0
        for enemy in fight_active_enemy_rows():
            status = dict(enemy.get("status", {}) or {})
            if int(status.get("bleed_turns", 0) or 0) > 0:
                bleed_damage = max(1, int(status.get("bleed_damage", 0) or 0))
                enemy["health"] = max(0, int(enemy.get("health", 0) or 0) - bleed_damage)
                total_dot += bleed_damage
                status["bleed_turns"] = max(0, int(status.get("bleed_turns", 0) or 0) - 1)
            if int(status.get("poison_turns", 0) or 0) > 0:
                poison_damage = max(1, int(status.get("poison_damage", 0) or 0))
                enemy["health"] = max(0, int(enemy.get("health", 0) or 0) - poison_damage)
                total_dot += poison_damage
                status["poison_turns"] = max(0, int(status.get("poison_turns", 0) or 0) - 1)
            if int(status.get("paralyzed", 0) or 0) > 0:
                status["paralyzed"] = max(0, int(status.get("paralyzed", 0) or 0) - 1)
            if int(status.get("guard_turns", 0) or 0) > 0:
                status["guard_turns"] = max(0, int(status.get("guard_turns", 0) or 0) - 1)
            if int(status.get("evade_turns", 0) or 0) > 0:
                status["evade_turns"] = max(0, int(status.get("evade_turns", 0) or 0) - 1)
            enemy["status"] = status
        if total_dot > 0:
            fight_append_log("Раны и яд продолжают делать свое дело.")

    def fight_dead_enemy_exploration_reward():
        reward = 0
        for enemy in list(FightEnemyParty or []):
            if int(enemy.get("health", 0) or 0) > 0:
                continue
            reward += max(0, int(enemy.get("exploration_reward", 0) or 0))
        return int(reward or 0)

    def fight_collect_victory_loot():
        global money, exploration, FightVictoryLoot
        loot_rows = {}
        money_gain = 0
        for enemy in list(FightEnemyParty or []):
            if int(enemy.get("health", 0) or 0) > 0:
                continue
            for item_id, qty in dict(enemy.get("loot", {}) or {}).items():
                loot_rows[item_id] = int(loot_rows.get(item_id, 0) or 0) + int(qty or 0)
            money_min = max(0, int(enemy.get("money_min", 0) or 0))
            money_max = max(money_min, int(enemy.get("money_max", money_min) or money_min))
            if money_max > 0:
                money_gain += random.randint(money_min, money_max)
        for item_id, qty in dict(loot_rows or {}).items():
            _player_add_item_by_id(item_id, int(qty or 0))
        if money_gain > 0:
            money = max(0, int(money or 0) + money_gain)
            loot_rows["money"] = money_gain
        exploration_gain = fight_dead_enemy_exploration_reward()
        if exploration_gain > 0:
            exploration = max(0, int(exploration or 0) + exploration_gain)
        FightVictoryLoot = dict(loot_rows or {})
        return dict(loot_rows or {})

    def fight_loot_text():
        rows = []
        for item_id, qty in dict(FightVictoryLoot or {}).items():
            if str(item_id or "") == "money":
                rows.append("{} мараведи".format(int(qty or 0)))
                continue
            item_obj = get_game_item(item_id)
            item_name = str(getattr(item_obj, "name", item_id) or item_id)
            rows.append("{} x{}".format(item_name, int(qty or 0)))
        return ", ".join(rows)

    def fight_apply_end_consequences(outcome=""):
        global HuntLastResult
        result_key = str(outcome or "").strip()
        minutes = 20
        if result_key == "retreat":
            minutes = 10
        elif result_key == "defeat":
            minutes = 60
        try:
            calendar_v2.advance_minutes(minutes)
        except Exception:
            pass
        HuntLastResult = {
            "outcome": result_key,
            "enemy_id": str(FightEnemyId or ""),
            "enemy_count": len(list(FightEnemyParty or [])),
            "loot": dict(FightVictoryLoot or {}),
            "minutes": int(minutes or 0),
            "day": int(dayspassed or 0),
        }
        update_stat_state()
        return minutes

    def fight_hunt_candidates(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        candidates = []
        for row in list(FOREST_HUNT_ROOM_TABLE.get(room_key, []) or []):
            if int(exploration or 0) >= int(row.get("min_exploration", 0) or 0):
                candidates.append(dict(row))
        return candidates

    def fight_can_hunt_here(room_code=""):
        return bool(HuntUnlocked) and len(fight_hunt_candidates(room_code)) > 0

    def fight_roll_hunt_enemy(room_code=""):
        candidates = list(fight_hunt_candidates(room_code) or [])
        if len(candidates) <= 0:
            return {"enemy_id": "wolf", "enemy_count": 1}
        total_weight = sum(max(1, int(row.get("weight", 1) or 1)) for row in candidates)
        roll = random.randint(1, max(1, total_weight))
        picked = candidates[-1]
        passed = 0
        for row in candidates:
            passed += max(1, int(row.get("weight", 1) or 1))
            if roll <= passed:
                picked = row
                break
        return {
            "enemy_id": str(picked.get("enemy_id", "wolf") or "wolf"),
            "enemy_count": random.randint(int(picked.get("count_min", 1) or 1), int(picked.get("count_max", 1) or 1)),
        }

    def fight_begin(enemy_id="wolf", enemy_count=1, return_room="", picture="", intro_text=""):
        global FightEnemyId, FightEnemyParty, FightEnemyState, FightReturnRoomCode, FightReturnPicture
        global FightVictoryLoot, FightOutcomeText, FightOutcomeKind, FightStatusState, FightSideLog, FightTargetIndex
        global UI_mode, current_action_title, current_action_content, scene_image, _layout_last_picture, MainTxt, CurLocDesc
        fight_ensure_runtime()
        fight_sync_level_from_exploration()
        fight_sync_supply_from_inventory()
        FightEnemyId = str(enemy_id or "wolf")
        FightEnemyParty = fight_build_enemy_party(enemy_id, enemy_count)
        FightEnemyState = {
            "enemy_id": str(enemy_id or "wolf"),
            "enemy_count": max(1, int(enemy_count or 1)),
            "active": 1,
        }
        FightReturnRoomCode = str(return_room or CurLoc or "").strip()
        FightReturnPicture = str(picture or _layout_last_picture or scene_image or "").strip()
        FightVictoryLoot = {}
        FightOutcomeText = ""
        FightOutcomeKind = ""
        FightStatusState = {}
        FightSideLog = []
        FightTargetIndex = 1
        UI_mode = "fight"
        current_action_title = "Бой"
        current_action_content = "fight_action_panel"
        scene_image = str(picture or "images/forest/forest_1.png")
        _layout_last_picture = scene_image
        MainTxt = str(intro_text or fight_preview_text())
        CurLocDesc = MainTxt
        fight_sync_loaded_weapon_state_from_inventory()
        fight_refresh_ui_actions()

    def fight_finish_to_room(text):
        global UI_mode, FightEnemyState, FightEnemyParty, FightEnemyId, FightSideLog, FightLoadedAmmo, FightWeaponLoaded
        global FightTargetIndex, FightOutcomeText, FightOutcomeKind, current_action_content, current_action_title
        global CurLoc, location, MainTxt, CurLocDesc
        return_room = str(FightReturnRoomCode or CurLoc or "").strip()
        UI_mode = "scene"
        FightEnemyState = {}
        FightEnemyParty = []
        FightEnemyId = ""
        FightSideLog = []
        FightLoadedAmmo = ""
        FightWeaponLoaded = 0
        FightTargetIndex = 1
        FightOutcomeText = ""
        FightOutcomeKind = ""
        current_action_content = None
        current_action_title = "Действия"
        if return_room:
            CurLoc = return_room
            location = return_room
        MainTxt = str(text or "")
        CurLocDesc = MainTxt

    def fight_apply_enemy_phase(defence_mode="normal"):
        global health
        active_rows = list(fight_active_enemy_rows() or [])
        if len(active_rows) <= 0:
            return "С вашей добычей покончено."

        phase_lines = []
        if str(defence_mode or "") == "dodge" and random.randint(1, 100) <= 60:
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

        total_damage = 0
        for enemy in active_rows:
            move_row = fight_enemy_move_resolution(enemy, defence_mode)
            phase_lines.append(str(move_row.get("text", "") or ""))
            move_damage = max(0, int(move_row.get("damage", 0) or 0))
            if move_damage <= 0:
                continue
            enemy_defence_slice = max(0, int(defence_points / max(1, len(active_rows))))
            applied_damage = max(0, move_damage - enemy_defence_slice)
            total_damage += applied_damage
            if applied_damage > 0:
                move_code = str(move_row.get("move", "") or "")
                if move_code == "dead_lock":
                    fight_apply_player_status("locked_turns", 1)
                elif move_code in ("ram", "strike"):
                    fight_apply_player_status("stagger_turns", 1)

        health = max(0, int(health or 0) - total_damage)
        if total_damage <= 0:
            phase_lines.append("Вы выдерживаете натиск и не получаете заметного урона.")
        else:
            phase_lines.append("К концу вражеского натиска вы теряете {} здоровья.".format(int(total_damage or 0)))
        return "\n\n".join([row for row in phase_lines if str(row or "").strip() != ""])

    def fight_apply_player_action(action_code=""):
        global FightWeaponLoaded, FightLoadedAmmo, health, notoriety, SickDays
        fight_ensure_runtime()
        action = str(action_code or "").strip().lower()
        result_lines = []
        fight_tick_statuses()

        if len(fight_active_enemy_rows()) <= 0:
            fight_collect_victory_loot()
            return {"done": "victory", "text": "Схватка уже окончена."}

        if action == "attack":
            fight_spend_energy(8)
            target = fight_random_target()
            target_status = dict(target.get("status", {}) or {}) if target is not None else {}
            defence = random.randint(int(target.get("defence_min", 0) or 0), int(target.get("defence_max", 0) or 0)) if target else 0
            defence += 5 * int(target_status.get("guard_turns", 0) or 0)
            defence += 4 * int(target_status.get("evade_turns", 0) or 0)
            damage = max(0, int(fight_player_attack_roll() or 0) - defence)
            target, dealt = fight_apply_damage_to_enemy(damage, target)
            result_lines.append("Вы идете в ближний бой и наносите {} урона.".format(int(dealt or 0)))
            fight_decay_player_statuses()
            enemy_text = fight_apply_enemy_phase("normal")
            if enemy_text:
                result_lines.append(enemy_text)
        elif action == "cycle_target":
            target = fight_cycle_target()
            if target is None:
                result_lines.append("Сейчас менять цель не на кого.")
            else:
                result_lines.append("Вы переводите внимание на цель: {}.".format(str(target.get("name", "") or "враг")))
        elif action == "shoot":
            loaded_ammo = str(FightLoadedAmmo or "").strip()
            if not fight_rifle_equipped():
                result_lines.append("У вас не экипировано ружье.")
            elif int(FightWeaponLoaded or 0) != 1 or loaded_ammo == "":
                result_lines.append("Оружие еще не заряжено.")
            else:
                fight_spend_energy(5)
                target = fight_random_target()
                if loaded_ammo == "droplets":
                    damage = random.randint(15, 30)
                    target, dealt = fight_apply_damage_to_enemy(damage, target)
                    result_lines.append("Вы стреляете дробью и наносите {} урона.".format(int(dealt or 0)))
                else:
                    damage = random.randint(8, 14)
                    target, dealt = fight_apply_damage_to_enemy(damage, target)
                    if target is not None:
                        status = dict(target.get("status", {}) or {})
                        status["bleed_turns"] = 5
                        status["bleed_damage"] = max(1, int(target.get("health_max", 1) or 1) // 10)
                        target["status"] = status
                    result_lines.append("Вы выпускаете стрелу и наносите {} урона. Рана начинает кровоточить.".format(int(dealt or 0)))
                FightWeaponLoaded = 0
                FightLoadedAmmo = ""
                fight_store_loaded_weapon_state()
                fight_decay_player_statuses()
                enemy_text = fight_apply_enemy_phase("normal")
                if enemy_text:
                    result_lines.append(enemy_text)
        elif action == "reload_arrows" or action == "reload_droplets":
            reload_ammo = "arrows" if action == "reload_arrows" else "droplets"
            if not fight_rifle_equipped():
                result_lines.append("Перезаряжать нечего: ружье не экипировано.")
            elif int(FightWeaponLoaded or 0) == 1 and str(FightLoadedAmmo or "").strip() != "":
                result_lines.append("Оружие уже заряжено.")
            elif int(PlayerFightSupply.get(reload_ammo, 0) or 0) <= 0:
                result_lines.append("Нужного боеприпаса при себе не осталось.")
            elif reload_ammo == "droplets" and int(PlayerFightSupply.get("gunpowder", 0) or 0) <= 0:
                result_lines.append("Для дробового заряда у вас не осталось пороха.")
            else:
                fight_spend_energy(4)
                PlayerFightSupply[reload_ammo] = max(0, int(PlayerFightSupply.get(reload_ammo, 0) or 0) - 1)
                if reload_ammo == "arrows":
                    _player_remove_item_by_id("arrows_001", 1)
                else:
                    _player_remove_item_by_id("droplets_001", 1)
                    PlayerFightSupply["gunpowder"] = max(0, int(PlayerFightSupply.get("gunpowder", 0) or 0) - 1)
                    _player_remove_item_by_id("gunpowder_001", 1)
                FightWeaponLoaded = 1
                FightLoadedAmmo = reload_ammo
                fight_store_loaded_weapon_state()
                result_lines.append("Вы быстро перезаряжаете оружие: {}.".format(fight_loaded_ammo_name(reload_ammo)))
            fight_decay_player_statuses()
            enemy_text = fight_apply_enemy_phase("normal")
            if enemy_text:
                result_lines.append(enemy_text)
        elif action == "dodge":
            fight_spend_energy(4)
            result_lines.append("Вы сосредотачиваетесь на уклонении.")
            fight_decay_player_statuses()
            enemy_text = fight_apply_enemy_phase("dodge")
            if enemy_text:
                result_lines.append(enemy_text)
        elif action == "block":
            fight_spend_energy(3)
            result_lines.append("Вы занимаете более защищенную стойку.")
            fight_decay_player_statuses()
            enemy_text = fight_apply_enemy_phase("block")
            if enemy_text:
                result_lines.append(enemy_text)
        elif action == "bandage":
            if int(PlayerFightSupply.get("bandage", 0) or 0) <= 0:
                result_lines.append("У вас нет бинта.")
            else:
                fight_spend_energy(2)
                _player_remove_item_by_id("bandage_001", 1)
                PlayerFightSupply["bandage"] = max(0, int(PlayerFightSupply.get("bandage", 0) or 0) - 1)
                health = min(100, int(health or 0) + 12)
                result_lines.append("Вы торопливо перевязываете раны и восстанавливаете немного сил.")
                fight_decay_player_statuses()
                enemy_text = fight_apply_enemy_phase("normal")
                if enemy_text:
                    result_lines.append(enemy_text)
        elif action == "tea":
            if int(PlayerFightSupply.get("energy_tea", 0) or 0) <= 0:
                result_lines.append("У вас нет бодрящего чая.")
            else:
                _player_remove_item_by_id("energy_tea_001", 1)
                PlayerFightSupply["energy_tea"] = max(0, int(PlayerFightSupply.get("energy_tea", 0) or 0) - 1)
                fight_restore_energy(15)
                result_lines.append("Вы делаете несколько глотков бодрящего чая.")
                fight_decay_player_statuses()
                enemy_text = fight_apply_enemy_phase("normal")
                if enemy_text:
                    result_lines.append(enemy_text)
        elif action == "potion":
            if int(PlayerFightSupply.get("healing_potion", 0) or 0) <= 0:
                result_lines.append("У вас нет лечебного зелья.")
            else:
                _player_remove_item_by_id("healing_potion_001", 1)
                PlayerFightSupply["healing_potion"] = max(0, int(PlayerFightSupply.get("healing_potion", 0) or 0) - 1)
                health = min(100, int(health or 0) + 25)
                result_lines.append("Вы выпиваете зелье и чувствуете, как возвращаются силы.")
                fight_decay_player_statuses()
                enemy_text = fight_apply_enemy_phase("normal")
                if enemy_text:
                    result_lines.append(enemy_text)
        elif action == "bees_bomb":
            if int(PlayerFightSupply.get("bees_bomb", 0) or 0) <= 0:
                result_lines.append("У вас нет пчелиного заряда.")
            else:
                fight_spend_energy(4)
                PlayerFightSupply["bees_bomb"] = max(0, int(PlayerFightSupply.get("bees_bomb", 0) or 0) - 1)
                for enemy in fight_active_enemy_rows():
                    status = dict(enemy.get("status", {}) or {})
                    status["paralyzed"] = 3
                    status["poison_turns"] = 5
                    status["poison_damage"] = 5
                    enemy["status"] = status
                result_lines.append("Вы бросаете пчелиный заряд. Противники в панике теряют строй.")
        elif action == "fire_bomb":
            if int(PlayerFightSupply.get("fire_bomb", 0) or 0) <= 0:
                result_lines.append("У вас нет огненной бутылки.")
            else:
                fight_spend_energy(4)
                _player_remove_item_by_id("fire_bomb_001", 1)
                PlayerFightSupply["fire_bomb"] = max(0, int(PlayerFightSupply.get("fire_bomb", 0) or 0) - 1)
                _fire_hits = []
                for enemy in fight_active_enemy_rows():
                    damage = random.randint(10, 18)
                    target, dealt = fight_apply_damage_to_enemy(damage, enemy)
                    if target is not None:
                        _fire_hits.append("{}: {}".format(str(target.get("name", "цель") or "цель"), int(dealt or 0)))
                if len(_fire_hits) > 0:
                    result_lines.append("Вы разбиваете огненную бутылку о землю перед противниками. Пламя вспыхивает сразу в нескольких местах: {}.".format(", ".join(_fire_hits)))
                else:
                    result_lines.append("Вы разбиваете огненную бутылку, но рядом уже не остается ни одной цели.")
                fight_decay_player_statuses()
                enemy_text = fight_apply_enemy_phase("normal")
                if enemy_text:
                    result_lines.append(enemy_text)
        elif action == "breath":
            fight_restore_energy(6)
            result_lines.append("Вы переводите дух и немного восстанавливаете силы.")
            fight_decay_player_statuses()
            enemy_text = fight_apply_enemy_phase("normal")
            if enemy_text:
                result_lines.append(enemy_text)
        elif action == "dog":
            dog_state = fight_dog_support_state()
            if not bool(dog_state.get("active", False)):
                result_lines.append("Пса рядом нет.")
            else:
                target = fight_random_target()
                target, dealt = fight_apply_damage_to_enemy(int(dog_state.get("attack", 0) or 0), target)
                if int(getattr(dog, "level", 0) or 0) >= 2 and target is not None:
                    target_status = dict(target.get("status", {}) or {})
                    target_status["paralyzed"] = max(1, int(target_status.get("paralyzed", 0) or 0))
                    target["status"] = target_status
                    result_lines.append("Пес вцепляется в противника мертвой хваткой, нанося {} урона и сбивая его с темпа.".format(int(dealt or 0)))
                else:
                    result_lines.append("Пес бросается вперед и рвет противника, нанося {} урона.".format(int(dealt or 0)))
                fight_decay_player_statuses()
                enemy_text = fight_apply_enemy_phase("normal")
                if enemy_text:
                    result_lines.append(enemy_text)
        elif action == "retreat":
            if fight_retreat_success():
                notoriety = max(0, int(notoriety or 0) - 6)
                if int(health or 0) <= 20:
                    SickDays = max(2, int(SickDays or 0))
                return {"done": "retreat", "text": "Вы выбираете момент и отступаете из схватки. Такой исход бьет по вашей репутации, но вы уходите на своих ногах."}
            result_lines.append("Вы пытаетесь отступить, но противники не дают вам разорвать дистанцию.")
            fight_decay_player_statuses()
            enemy_text = fight_apply_enemy_phase("normal")
            if enemy_text:
                result_lines.append(enemy_text)
        else:
            result_lines.append("Вы медлите, и момент оказывается упущен.")
            enemy_text = fight_apply_enemy_phase("normal")
            if enemy_text:
                result_lines.append(enemy_text)

        if int(health or 0) <= 0:
            health = 1
            SickDays = max(2, int(SickDays or 0))
            notoriety = max(0, int(notoriety or 0) - 6)
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

    def forest_trap_can_place(room_code=""):
        global ForestTrapRooms
        fight_ensure_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        active_rooms = ForestTrapRooms if isinstance(ForestTrapRooms, dict) else {}
        legacy_room = str(ForestTrapState.get("room", "") or "")
        if legacy_room and int(ForestTrapState.get("active", 0) or 0) == 1 and legacy_room not in active_rooms:
            active_rooms[legacy_room] = {"day": int(ForestTrapState.get("day", -1) or -1), "armed_count": max(1, int(ForestTrapState.get("armed_count", 1) or 1))}
            ForestTrapRooms = active_rooms
        return bool(fight_can_hunt_here(room_key)) and int(_player_item_count_by_id("hunting_trap_001") or 0) > 0 and room_key not in active_rooms

    def forest_trap_can_check(room_code=""):
        fight_ensure_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        active_rooms = ForestTrapRooms if isinstance(ForestTrapRooms, dict) else {}
        if room_key in active_rooms:
            return int(dayspassed or 0) > int(dict(active_rooms.get(room_key, {}) or {}).get("day", -1) or -1)
        return int(ForestTrapState.get("active", 0) or 0) == 1 and str(ForestTrapState.get("room", "") or "") == room_key and int(dayspassed or 0) > int(ForestTrapState.get("day", -1) or -1)

    def forest_trap_set(room_code=""):
        global ForestTrapRooms, ForestTrapState
        fight_ensure_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        if not forest_trap_can_place(room_key):
            return {"ok": False, "text": "Сейчас вы не можете поставить здесь ловушку."}
        _player_remove_item_by_id("hunting_trap_001", 1)
        active_rooms = ForestTrapRooms if isinstance(ForestTrapRooms, dict) else {}
        active_rooms[room_key] = {"day": int(dayspassed or 0), "armed_count": 1}
        ForestTrapRooms = active_rooms
        ForestTrapState = {"active": 1, "room": room_key, "day": int(dayspassed or 0), "armed_count": len(active_rooms)}
        return {"ok": True, "text": "Вы тщательно ставите охотничью ловушку и маскируете ее листвой. Проверить ее лучше не раньше завтрашнего дня."}

    def forest_trap_check(room_code=""):
        global ForestTrapRooms, ForestTrapState
        fight_ensure_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        if not forest_trap_can_check(room_key):
            return {"ok": False, "text": "Ловушку пока рано проверять или здесь ее нет."}
        active_rooms = ForestTrapRooms if isinstance(ForestTrapRooms, dict) else {}
        if room_key in active_rooms:
            active_rooms.pop(room_key, None)
        ForestTrapRooms = active_rooms
        if active_rooms:
            next_room = sorted(active_rooms.keys())[0]
            next_row = dict(active_rooms.get(next_room, {}) or {})
            ForestTrapState = {"active": 1, "room": next_room, "day": int(next_row.get("day", -1) or -1), "armed_count": len(active_rooms)}
        else:
            ForestTrapState = {"active": 0, "room": "", "day": -1, "armed_count": 0}
        roll = random.randint(1, 100)
        if roll <= 35:
            return {"ok": True, "text": "Вы проверяете ловушку, но она сработала впустую. Добыча ушла.", "loot": {}}
        if roll <= 70:
            _player_add_item_by_id("wolf_skin_001", 1)
            return {"ok": True, "text": "В ловушке запутался молодой волк. Шкуру с него еще можно снять.", "loot": {"wolf_skin_001": 1}}
        _player_add_item_by_id("boar_meat_001", 1)
        _player_add_item_by_id("boar_fang_001", 1)
        return {"ok": True, "text": "Ловушка помогла вам завалить кабана. Вы успеваете взять мясо и клык.", "loot": {"boar_meat_001": 1, "boar_fang_001": 1}}

    def dog_catch_delinquent_apply(event_kind="horse"):
        global money, notoriety, tavernfame
        ensure_dog_runtime()
        if not dog.prevents_theft(event_kind):
            return {"ok": False, "text": "Пса рядом нет или он пока не может вам помочь."}
        event_key = str(event_kind or "").strip()
        if event_key == "horse":
            roll = random.randint(1, 100)
            if roll > 70:
                return {
                    "ok": False,
                    "text": "Пес учуял возню у конюшни и поднял лай, но вор все-таки успел вырваться в темноту и увести коня.",
                    "money_gain": 0,
                }
            paid_price = max(0, int(HorsePurchasePrice or 0))
            ransom = max(0, (paid_price * 2) // 3)
            if ransom > 0:
                money += ransom
            for girl_key in ("sandra", "melissa", "amanda"):
                Friends[girl_key] = int(Friends.get(girl_key, 0) or 0) + 2
            notoriety = min(100, int(notoriety or 0) + 3)
            tavernfame = int(tavernfame or 0) + 2
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
        loot_row = dict(random.choice(loot_table))
        item_id = str(loot_row.get("item_id", "") or "")
        qty = max(1, int(loot_row.get("qty", 1) or 1))
        money_gain = max(0, int(loot_row.get("money", 0) or 0))
        if item_id:
            _player_add_item_by_id(item_id, qty)
        money = int(money or 0) + money_gain
        for girl_key in ("sandra", "melissa", "amanda"):
            Friends[girl_key] = int(Friends.get(girl_key, 0) or 0) + 2
        notoriety = min(100, int(notoriety or 0) + 3)
        tavernfame = int(tavernfame or 0) + 2
        item_name = str(getattr(get_game_item(item_id), "name", item_id) or item_id)
        return {
            "ok": True,
            "text": "Пес бросается на вора, валит его на землю и не дает уйти. При обыске у него находятся {} x{} и еще {} мараведи. В трактире быстро узнают, что пес спас ваше добро.".format(item_name, qty, money_gain),
            "item_id": item_id,
            "qty": qty,
            "money_gain": money_gain,
        }

    def fight_preview_action_items():
        fight_ensure_runtime()
        items = [
            MenuItem("Уклониться", NullAction()),
            MenuItem("Блокировать", NullAction()),
            MenuItem("Атаковать вблизи", NullAction()),
        ]
        if len(fight_active_enemy_rows()) > 1:
            target_row = fight_selected_target()
            target_name = str(target_row.get("name", "цель") or "цель") if target_row is not None else "цель"
            items.insert(0, MenuItem("Цель: {}".format(target_name), NullAction()))
        if int(FightWeaponLoaded or 0) == 1 and str(FightLoadedAmmo or "").strip() != "":
            items.append(MenuItem("Выстрелить ({})".format(fight_loaded_ammo_name(FightLoadedAmmo)), NullAction()))
        else:
            if int(PlayerFightSupply.get("arrows", 0) or 0) > 0:
                items.append(MenuItem("Перезарядить стрелой", NullAction()))
            if int(PlayerFightSupply.get("droplets", 0) or 0) > 0:
                items.append(MenuItem("Перезарядить дробью", NullAction()))
        if int(PlayerFightSupply.get("bees_bomb", 0) or 0) > 0:
            items.append(MenuItem("Бросить пчелиный заряд", NullAction()))
        if int(PlayerFightSupply.get("fire_bomb", 0) or 0) > 0:
            items.append(MenuItem("Бросить огненную бутылку", NullAction()))
        if int(PlayerFightSupply.get("bandage", 0) or 0) > 0:
            items.append(MenuItem("Использовать бинт", NullAction()))
        if int(PlayerFightSupply.get("energy_tea", 0) or 0) > 0:
            items.append(MenuItem("Выпить бодрящий чай", NullAction()))
        if int(PlayerFightSupply.get("healing_potion", 0) or 0) > 0:
            items.append(MenuItem("Выпить лечебное зелье", NullAction()))
        items.append(MenuItem("Перевести дух", NullAction()))
        if bool(fight_dog_support_state().get("active", False)):
            items.append(MenuItem("Командовать псом", NullAction()))
        items.append(MenuItem("Отступить", NullAction()))
        return items

    def fight_preview_text():
        fight_ensure_runtime()
        player_attack = fight_player_attack_roll()
        player_defence = fight_player_defence_roll()
        dog_state = fight_dog_support_state()
        enemy_rows = []
        for enemy in list(FightEnemyParty or []):
            enemy_rows.append("%s: %s/%s HP" % (str(enemy.get("name", "") or ""), str(enemy.get("health", 0)), str(enemy.get("health_max", 0))))
        lines = [
            "Подготовка к бою.",
            "Ваш уровень боя: %s." % str(FightLevel.get("you", 1)),
            "Здоровье: %s/100." % str(int(health or 0)),
            "Атака: %s." % str(player_attack),
            "Защита: %s." % str(player_defence),
        ]
        if dog_state.get("active", False):
            lines.append("Пес рядом: укус %s, защита %s." % (str(dog_state.get("attack", 0)), str(dog_state.get("defence", 0))))
        if enemy_rows:
            lines.append("Противники:\n" + "\n".join(enemy_rows))
        return "\n\n".join(lines)

    def fight_company_display_rows():
        fight_ensure_runtime()
        rows = [{
            "name": "Вы",
            "health": int(health or 0),
            "health_max": 100,
            "energy": int(energy or 0),
            "energy_max": 100,
            "subtitle": "уровень боя {} | репутация {} | дурная слава {} | исследование {}".format(
                int(FightLevel.get("you", 1) or 1),
                int(reputation or 0),
                int(notoriety or 0),
                int(exploration or 0),
            ),
            "fight_level": int(FightLevel.get("you", 1) or 1),
            "reputation": int(reputation or 0),
            "notoriety": int(notoriety or 0),
            "exploration": int(exploration or 0),
            "tavernfame": int(tavernfame or 0),
            "money": int(money or 0),
            "sick_days": int(SickDays or 0),
            "fun": int(fun or 0),
            "status": fight_player_status_labels(),
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

        for companion_key in list(company_list or []):
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
        selected_index = max(1, int(FightTargetIndex or 1))
        for enemy in list(FightEnemyParty or []):
            status_labels = []
            enemy_status = dict(enemy.get("status", {}) or {})
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
            if int(enemy.get("index", 0) or 0) == selected_index and int(enemy.get("health", 0) or 0) > 0:
                status_labels.insert(0, "цель")
            rows.append({
                "name": str(enemy.get("name", "") or ""),
                "health": int(enemy.get("health", 0) or 0),
                "health_max": int(enemy.get("health_max", 0) or 0),
                "energy": int(enemy.get("energy", 0) or 0),
                "energy_max": int(enemy.get("energy_max", 0) or 0),
                "subtitle": "оружие: {} | атака {}-{} | защита {}-{} | тактика: {}".format(
                    str(enemy.get("weapon", "") or "тело"),
                    int(enemy.get("attack_min", 0) or 0),
                    int(enemy.get("attack_max", 0) or 0),
                    int(enemy.get("defence_min", 0) or 0),
                    int(enemy.get("defence_max", 0) or 0),
                    str(enemy.get("tactics", "") or "простая"),
                ),
                "weapon": str(enemy.get("weapon", "") or "тело"),
                "attack_text": "{}-{}".format(int(enemy.get("attack_min", 0) or 0), int(enemy.get("attack_max", 0) or 0)),
                "defence_text": "{}-{}".format(int(enemy.get("defence_min", 0) or 0), int(enemy.get("defence_max", 0) or 0)),
                "tactics": str(enemy.get("tactics", "") or "простая"),
                "status": status_labels,
            })
        return rows

    def show_fight_preview_main_ui(enemy_id="wolf", enemy_count=1, picture="images/forest/forest_1.png"):
        global FightEnemyId, FightEnemyParty, FightEnemyState, FightSideLog, FightTargetIndex
        global UI_mode, current_action_title, current_action_content, current_action_items
        global MainTxt, CurLocDesc, scene_image, _layout_last_picture
        fight_ensure_runtime()
        fight_sync_level_from_exploration()
        fight_sync_supply_from_inventory()
        FightEnemyId = str(enemy_id or "wolf")
        FightEnemyParty = fight_build_enemy_party(enemy_id, enemy_count)
        FightEnemyState = {
            "enemy_id": str(enemy_id or "wolf"),
            "enemy_count": max(1, int(enemy_count or 1)),
        }
        FightSideLog = ["Бой пока открыт как тестовый экран подготовки."]
        FightTargetIndex = 1
        UI_mode = "fight"
        current_action_title = "Бой"
        current_action_content = None
        fight_sync_loaded_weapon_state_from_inventory()
        current_action_items = fight_preview_action_items()
        MainTxt = fight_preview_text()
        CurLocDesc = MainTxt
        scene_image = str(picture or "images/forest/forest_1.png")
        _layout_last_picture = scene_image
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()


label FightPreviewStart(enemy_id="wolf", enemy_count=1):
    $ show_fight_preview_main_ui(enemy_id, enemy_count)
    return


label FightLoop:
    while str(UI_mode or "") == "fight":
        call screen main_ui
    return


label FightStartHuntCurrentRoom:
    $ _hunt_roll = fight_roll_hunt_enemy(str(getattr(CurrentRoom, "code_name", "") or CurLoc or ""))
    $ _fight_room_code = str(getattr(CurrentRoom, "code_name", "") or CurLoc or "")
    $ _fight_picture = str(_layout_last_picture or scene_image or "")
    $ _fight_enemy_id = str(_hunt_roll.get("enemy_id", "wolf") or "wolf")
    $ _fight_enemy_count = max(1, int(_hunt_roll.get("enemy_count", 1) or 1))
    $ _fight_intro_text = fight_hunt_intro_text(_fight_enemy_id, _fight_enemy_count, _fight_room_code)
    $ fight_begin(_fight_enemy_id, _fight_enemy_count, _fight_room_code, _fight_picture, _fight_intro_text)
    call FightLoop
    return


label FightDoAction(action_code=""):
    $ _fight_result = fight_apply_player_action(action_code)
    $ MainTxt = str(_fight_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    if str(_fight_result.get("done", "") or "") == "continue":
        python:
            for _fight_line in str(MainTxt or "").split("\n\n"):
                fight_append_log(_fight_line)
        $ fight_refresh_ui_actions()
        return
    if str(_fight_result.get("done", "") or "") == "victory":
        python:
            for _fight_line in str(MainTxt or "").split("\n\n"):
                fight_append_log(_fight_line)
        $ _fight_minutes = fight_apply_end_consequences("victory")
        $ MainTxt = MainTxt + "\n\nНа схватку уходит %d минут." % int(_fight_minutes or 0)
        $ CurLocDesc = MainTxt
        $ FightOutcomeKind = "victory"
        $ FightOutcomeText = MainTxt
        $ current_action_title = "Победа"
        $ current_action_items = [MenuItem("Забрать добычу и вернуться", Call("FightReturnToScene"))]
        $ renpy.notify("Победа. Добыча: " + (fight_loot_text() or "нет"))
        return
    if str(_fight_result.get("done", "") or "") in ("defeat", "retreat"):
        $ _fight_done = str(_fight_result.get("done", "") or "")
        $ _fight_minutes = fight_apply_end_consequences(_fight_done)
        $ MainTxt = MainTxt + "\n\nНа исход схватки уходит %d минут." % int(_fight_minutes or 0)
        $ CurLocDesc = MainTxt
        $ FightOutcomeKind = _fight_done
        $ FightOutcomeText = MainTxt
        $ current_action_title = "Поражение" if _fight_done == "defeat" else "Отступление"
        $ current_action_items = [MenuItem("Вернуться", Call("FightReturnToScene"))]
        $ renpy.notify("Поражение в бою." if _fight_done == "defeat" else "Вы отступили из боя.")
        return
    call FightReturnToScene
    return


label FightReturnToScene:
    $ _fight_text = str(MainTxt or "")
    $ _fight_return_room = str(FightReturnRoomCode or CurLoc or "")
    $ _fight_return_picture = str(FightReturnPicture or "")
    $ fight_finish_to_room(_fight_text)
    $ scene_image = _fight_return_picture
    $ _layout_last_picture = _fight_return_picture
    jump expression _fight_return_room


label ForestSetTrap:
    $ _trap_result = forest_trap_set(str(getattr(CurrentRoom, "code_name", "") or CurLoc or ""))
    $ MainTxt = str(_trap_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    if str(getattr(CurrentRoom, "code_name", "") or "") == "Forest":
        $ ForestSavedText = MainTxt
        call ForestBuildActions
    else:
        $ ForestSubroomSavedText = MainTxt
        call ForestSubroomBuildActions
    return


label ForestCheckTrap:
    $ _trap_result = forest_trap_check(str(getattr(CurrentRoom, "code_name", "") or CurLoc or ""))
    $ MainTxt = str(_trap_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    if str(getattr(CurrentRoom, "code_name", "") or "") == "Forest":
        $ ForestSavedText = MainTxt
        call ForestBuildActions
    else:
        $ ForestSubroomSavedText = MainTxt
        call ForestSubroomBuildActions
    return
