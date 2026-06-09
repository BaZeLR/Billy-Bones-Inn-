# ================================================================================
# Player runtime owner.
#
# Player is the saved MC root. Feature classes own the concrete slices so Player
# does not become one oversized bag of unrelated fields.
# ================================================================================

init -998 python:

    def player_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def player_clamp_value(value, low=0, high=100):
        return max(int(low or 0), min(int(high or 0), player_to_int(value, low)))

    def player_normalize_item_id(item_id=""):
        try:
            return str(get_object_id(item_id) or "").strip()
        except Exception:
            return str(item_id or "").strip()

    def player_normalize_inventory(raw_inventory=None):
        normalized = {}
        if hasattr(raw_inventory, "items"):
            rows = list(raw_inventory.items())
        else:
            rows = [(row, 1) for row in list(raw_inventory or [])]

        for raw_key, raw_count in rows:
            item_key = player_normalize_item_id(raw_key)
            if not item_key:
                continue
            item_count = player_to_int(raw_count, 0)
            if item_count > 0:
                normalized[item_key] = normalized.get(item_key, 0) + item_count
        return normalized

    def player_normalize_id_list(raw_values=None):
        normalized = []
        for raw_value in list(raw_values or []):
            value = str(raw_value or "").strip()
            if value and value not in normalized:
                normalized.append(value)
        return normalized

    class PlayerIdentity(object):
        def __init__(self, code_name="you", display_name="Стефан Лонгкок", age=18):
            self.code_name = str(code_name or "you")
            self.display_name = str(display_name or "Стефан Лонгкок")
            self.age = player_to_int(age, 18)

        def sync_from_store(self):
            self.age = player_to_int(globals().get("age", self.age), 18)
            return self

        def apply_to_store(self):
            globals()["age"] = player_to_int(self.age, 18)
            return self

    class PlayerCondition(object):
        def __init__(self):
            self.health = 100
            self.energy = 100
            self.fun = 50
            self.sick_days = 0
            self.forest_ban_until_day = 0

        def sync_from_store(self):
            g = globals()
            self.health = player_clamp_value(g.get("health", self.health), 0, 100)
            self.energy = player_clamp_value(g.get("energy", self.energy), 0, 100)
            self.fun = player_clamp_value(g.get("fun", self.fun), 0, 100)
            self.sick_days = player_to_int(g.get("SickDays", self.sick_days), 0)
            self.forest_ban_until_day = player_to_int(g.get("PlayerForestBanUntilDay", self.forest_ban_until_day), 0)
            return self

        def apply_to_store(self):
            g = globals()
            g["health"] = player_clamp_value(self.health, 0, 100)
            g["energy"] = player_clamp_value(self.energy, 0, 100)
            g["fun"] = player_clamp_value(self.fun, 0, 100)
            g["SickDays"] = player_to_int(self.sick_days, 0)
            g["PlayerForestBanUntilDay"] = player_to_int(self.forest_ban_until_day, 0)
            return self

        def change(self, stat_name, delta, minimum=0, maximum=100):
            key = str(stat_name or "").strip()
            if not hasattr(self, key):
                return None
            value = player_clamp_value(player_to_int(getattr(self, key), 0) + player_to_int(delta, 0), minimum, maximum)
            setattr(self, key, value)
            return value

    class PlayerStats(object):
        def __init__(self):
            self.charisma = 0
            self.reputation = 0
            self.notoriety = 0
            self.exploration = 0
            self.rebellion = 0
            self.look = 40

        def sync_from_store(self):
            for attr in ("charisma", "reputation", "notoriety", "exploration", "rebellion", "look"):
                setattr(self, attr, player_to_int(globals().get(attr, getattr(self, attr)), getattr(self, attr)))
            return self

        def apply_to_store(self):
            for attr in ("charisma", "reputation", "notoriety", "exploration", "rebellion", "look"):
                globals()[attr] = player_to_int(getattr(self, attr), 0)
            return self

        def change(self, stat_name, delta, minimum=0, maximum=100):
            key = str(stat_name or "").strip()
            if not hasattr(self, key):
                return None
            value = player_clamp_value(player_to_int(getattr(self, key), 0) + player_to_int(delta, 0), minimum, maximum)
            setattr(self, key, value)
            return value

    class PlayerEconomy(object):
        def __init__(self):
            self.money = 10000
            self.tavern_fame = 0
            self.child_support_count = 0

        def sync_from_store(self):
            self.money = player_to_int(globals().get("money", self.money), 10000)
            self.tavern_fame = player_to_int(globals().get("tavernfame", self.tavern_fame), 0)
            self.child_support_count = max(0, player_to_int(globals().get("KidsPosobie", self.child_support_count), 0))
            return self

        def apply_to_store(self):
            globals()["money"] = player_to_int(self.money, 0)
            globals()["tavernfame"] = player_to_int(self.tavern_fame, 0)
            globals()["KidsPosobie"] = max(0, player_to_int(self.child_support_count, 0))
            return self

        def add_money(self, amount):
            self.money = max(0, player_to_int(self.money, 0) + player_to_int(amount, 0))
            return self.money

        def spend_money(self, amount):
            cost = max(0, player_to_int(amount, 0))
            if player_to_int(self.money, 0) < cost:
                return False
            self.money = player_to_int(self.money, 0) - cost
            return True

        def add_child_support(self, count=1):
            self.child_support_count = max(0, player_to_int(self.child_support_count, 0) + player_to_int(count, 1))
            return self.child_support_count

        def weekly_child_support_money(self):
            return 15 * max(0, player_to_int(self.child_support_count, 0))

    class PlayerInventory(object):
        def __init__(self, items=None):
            self.items = player_normalize_inventory(items or {})

        def sync_from_store(self):
            self.items = player_normalize_inventory(globals().get("playerItems", self.items))
            return self

        def apply_to_store(self):
            globals()["playerItems"] = dict(player_normalize_inventory(self.items))
            return self

        def count(self, item_id):
            item_key = player_normalize_item_id(item_id)
            if not item_key:
                return 0
            return max(0, player_to_int(self.items.get(item_key, 0), 0))

        def add(self, item_id, quantity=1):
            item_key = player_normalize_item_id(item_id)
            if not item_key:
                return False
            add_count = max(1, player_to_int(quantity, 1))
            self.items[item_key] = self.count(item_key) + add_count
            return True

        def remove(self, item_id, quantity=1):
            item_key = player_normalize_item_id(item_id)
            if not item_key:
                return False
            remove_count = max(1, player_to_int(quantity, 1))
            current_count = self.count(item_key)
            if current_count < remove_count:
                return False
            if current_count == remove_count:
                self.items.pop(item_key, None)
            else:
                self.items[item_key] = current_count - remove_count
            return True

        def ids(self, expand_stacks=False):
            result = []
            for item_key in sorted(list(self.items.keys())):
                item_count = self.count(item_key)
                if item_count <= 0:
                    continue
                if expand_stacks:
                    for _unused_unit in range(item_count):
                        result.append(item_key)
                else:
                    result.append(item_key)
            return result

    class PlayerEquipment(object):
        def __init__(self):
            self.weapon = ""
            self.armor = ""

        def sync_from_store(self):
            self.weapon = str(globals().get("EquippedWeapon", self.weapon) or "")
            self.armor = str(globals().get("EquippedArmor", self.armor) or "")
            return self

        def apply_to_store(self):
            globals()["EquippedWeapon"] = str(self.weapon or "")
            globals()["EquippedArmor"] = str(self.armor or "")
            return self

        def equip(self, item_id, slot=""):
            item_key = player_normalize_item_id(item_id)
            if not item_key:
                return False
            slot_key = str(slot or "").strip().lower()
            if slot_key not in ("weapon", "armor"):
                try:
                    item_obj = get_game_item(item_key)
                    item_type = str(getattr(item_obj, "item_type", "") or getattr(item_obj, "category", "") or "").lower()
                except Exception:
                    item_type = ""
                slot_key = "armor" if "armor" in item_type else "weapon"
            setattr(self, slot_key, item_key)
            return True

        def unequip(self, slot=""):
            slot_key = str(slot or "").strip().lower()
            if slot_key not in ("weapon", "armor"):
                return False
            setattr(self, slot_key, "")
            return True

    class PlayerAppearance(object):
        WASH_FRESH_DAYS = 3
        HAIRCUT_FRESH_DAYS = 14
        DRESS_LIFE_DAYS = 42
        ITEM_LIFE_DEFAULTS = {
            "soap_001": 3,
            "luxury_soap_001": 7,
        }

        def __init__(self):
            self.current_dress = "villagedress"
            self.owned_dresses = ["villagedress"]
            self.dress_days = {"villagedress": 0}
            self.dress_life_days = {"villagedress": self.DRESS_LIFE_DAYS}
            self.item_life_days = {}
            self.haircut_day = 0
            self.washDays = self.WASH_FRESH_DAYS
            self.hairCutdays = self.HAIRCUT_FRESH_DAYS
            self.days_since_haircut = 0
            self.days_since_wash = 0
            self.costume_condition = 100
            self.sleep_bottom_layer = "daywear"

        def sync_from_store(self):
            g = globals()
            self.days_since_wash = max(0, player_to_int(g.get("dayssincewash", self.days_since_wash), 0))
            self.days_since_haircut = max(0, player_to_int(g.get("dayssincehaircut", self.days_since_haircut), 0))
            self.haircut_day = max(0, player_to_int(g.get("PlayerHaircutDaySt", self.haircut_day), 0))
            self.washDays = max(0, player_to_int(g.get("washDays", self.WASH_FRESH_DAYS - self.days_since_wash), 0))
            self.hairCutdays = max(0, player_to_int(g.get("hairCutdays", self.HAIRCUT_FRESH_DAYS - self.days_since_haircut), 0))
            self.costume_condition = player_clamp_value(g.get("costumecondition", self.costume_condition), 0, 100)
            dress_days = g.get("PlayerDressDaySt", self.dress_days)
            if isinstance(dress_days, dict):
                self.dress_days = dict(dress_days or {})
            dress_life_days = g.get("PlayerDressLifeDays", self.dress_life_days)
            if isinstance(dress_life_days, dict):
                self.dress_life_days = dict(dress_life_days or {})
            item_life_days = g.get("PlayerItemLifeDays", self.item_life_days)
            if isinstance(item_life_days, dict):
                self.item_life_days = dict(item_life_days or {})
            return self

        def apply_to_store(self):
            g = globals()
            g["washDays"] = max(0, player_to_int(self.washDays, 0))
            g["hairCutdays"] = max(0, player_to_int(self.hairCutdays, 0))
            g["dayssincewash"] = max(0, player_to_int(self.days_since_wash, 0))
            g["dayssincehaircut"] = max(0, player_to_int(self.days_since_haircut, 0))
            g["PlayerHaircutDaySt"] = max(0, player_to_int(self.haircut_day, 0))
            g["PlayerDressDaySt"] = dict(self.dress_days or {})
            g["PlayerDressLifeDays"] = dict(self.dress_life_days or {})
            g["PlayerItemLifeDays"] = dict(self.item_life_days or {})
            g["costumecondition"] = player_clamp_value(self.costume_condition, 0, 100)
            return self

        def has_dress(self, dress_code):
            dress_key = str(dress_code or "").strip()
            return bool(dress_key) and dress_key in list(self.owned_dresses or [])

        def add_dress(self, dress_code, acquired_day=0):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            self.owned_dresses = player_normalize_id_list(self.owned_dresses)
            if dress_key not in self.owned_dresses:
                self.owned_dresses.append(dress_key)
            if not isinstance(self.dress_days, dict):
                self.dress_days = {}
            self.dress_days.setdefault(dress_key, player_to_int(acquired_day, 0))
            if not isinstance(self.dress_life_days, dict):
                self.dress_life_days = {}
            self.dress_life_days.setdefault(dress_key, self.DRESS_LIFE_DAYS)
            return True

        def remove_dress(self, dress_code):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            self.owned_dresses = [row for row in list(self.owned_dresses or []) if str(row or "").strip() != dress_key]
            if isinstance(self.dress_days, dict) and dress_key in self.dress_days:
                del self.dress_days[dress_key]
            if isinstance(self.dress_life_days, dict) and dress_key in self.dress_life_days:
                del self.dress_life_days[dress_key]
            if str(self.current_dress or "").strip() == dress_key:
                self.current_dress = ""
            return True

        def wear_dress(self, dress_code, acquired_day=0):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            self.add_dress(dress_key, acquired_day)
            self.current_dress = dress_key
            return True

        def remove_current_dress(self, dress_code=""):
            dress_key = str(dress_code or "").strip()
            current = str(self.current_dress or "").strip()
            if dress_key and dress_key != current:
                return False
            self.current_dress = ""
            return True

        def dress_age_days(self, dress_code="", current_day=0):
            dress_key = str(dress_code or self.current_dress or "").strip()
            if not dress_key:
                return 0
            if not isinstance(self.dress_days, dict):
                self.dress_days = {}
            self.dress_days.setdefault(dress_key, player_to_int(current_day, 0))
            return max(0, player_to_int(current_day, 0) - player_to_int(self.dress_days.get(dress_key, 0), 0))

        def wash(self):
            self.days_since_wash = 0
            self.washDays = self.WASH_FRESH_DAYS
            return True

        def increment_wash_days(self, amount=1):
            amount_value = max(0, player_to_int(amount, 1))
            self.days_since_wash = max(0, player_to_int(self.days_since_wash, 0) + amount_value)
            self.washDays = max(0, player_to_int(self.washDays, self.WASH_FRESH_DAYS) - amount_value)
            return self.days_since_wash

        def mark_haircut(self, current_day=0):
            self.haircut_day = player_to_int(current_day, 0)
            self.days_since_haircut = 0
            self.hairCutdays = self.HAIRCUT_FRESH_DAYS
            return True

        def item_default_life(self, item_id):
            item_key = player_normalize_item_id(item_id)
            if item_key in self.ITEM_LIFE_DEFAULTS:
                return max(0, player_to_int(self.ITEM_LIFE_DEFAULTS.get(item_key, 0), 0))
            if "soap" in item_key:
                return self.ITEM_LIFE_DEFAULTS["soap_001"]
            if "dress" in item_key or "clothes" in item_key or "armor" in item_key:
                return self.DRESS_LIFE_DAYS
            return 0

        def ensure_item_life(self, item_id):
            item_key = player_normalize_item_id(item_id)
            if not item_key:
                return 0
            default_life = self.item_default_life(item_key)
            if default_life <= 0:
                return 0
            if not isinstance(self.item_life_days, dict):
                self.item_life_days = {}
            self.item_life_days.setdefault(item_key, default_life)
            return max(0, player_to_int(self.item_life_days.get(item_key, 0), 0))

        def age_daily(self, days=1, item_ids=None):
            amount = max(0, player_to_int(days, 1))
            if amount <= 0:
                return self
            self.days_since_wash = max(0, player_to_int(self.days_since_wash, 0) + amount)
            self.days_since_haircut = max(0, player_to_int(self.days_since_haircut, 0) + amount)
            self.washDays = max(0, player_to_int(self.washDays, self.WASH_FRESH_DAYS) - amount)
            self.hairCutdays = max(0, player_to_int(self.hairCutdays, self.HAIRCUT_FRESH_DAYS) - amount)

            self.owned_dresses = player_normalize_id_list(self.owned_dresses)
            if not isinstance(self.dress_life_days, dict):
                self.dress_life_days = {}
            for dress_key in list(self.owned_dresses or []):
                self.dress_life_days.setdefault(dress_key, self.DRESS_LIFE_DAYS)
                self.dress_life_days[dress_key] = max(0, player_to_int(self.dress_life_days.get(dress_key, 0), 0) - amount)

            if not isinstance(self.item_life_days, dict):
                self.item_life_days = {}
            for item_key in list(item_ids or []):
                item_id = player_normalize_item_id(item_key)
                if not item_id:
                    continue
                if self.item_default_life(item_id) <= 0:
                    continue
                self.ensure_item_life(item_id)
                self.item_life_days[item_id] = max(0, player_to_int(self.item_life_days.get(item_id, 0), 0) - amount)

            self.costume_condition = max(0, player_to_int(self.costume_condition, 100) - amount)
            return self

        def ensure_nightwear(self, current_day=0):
            return self.add_dress("nightshirt", current_day)

        def set_sleep_layer(self, mode="daywear", current_day=0):
            mode_key = str(mode or "daywear").strip().lower()
            if mode_key in ("naked", "nothing", "none"):
                self.current_dress = ""
                self.sleep_bottom_layer = "nothing"
            elif mode_key in ("night", "nightwear", "sleep"):
                self.ensure_nightwear(current_day)
                self.current_dress = "nightshirt"
                self.sleep_bottom_layer = "nightwear"
            else:
                self.sleep_bottom_layer = "daywear"
                if str(self.current_dress or "").strip() in ("", "nightshirt"):
                    self.wear_dress("villagedress", current_day)
            return self.sleep_bottom_layer

        def is_naked(self):
            return str(self.sleep_bottom_layer or "") == "nothing" or str(self.current_dress or "").strip() == ""

        def is_nightwear(self):
            return str(self.sleep_bottom_layer or "") == "nightwear" or str(self.current_dress or "") == "nightshirt"

    class PlayerIntimacy(object):
        def __init__(self):
            self.arousal = {"you": 0}
            self.can_cum_daily = 2
            self.came_today = 0
            self.last_sex_day = -1
            self.last_cum_day = -1
            self.history = {}
            self.had_sex_count = 0

        def sync_from_store(self):
            g = globals()
            arousal_value = g.get("Arousal", self.arousal)
            self.arousal = dict(arousal_value or {}) if isinstance(arousal_value, dict) else {"you": 0}
            self.can_cum_daily = player_to_int(g.get("cancumdaily", self.can_cum_daily), 2)
            self.came_today = player_to_int(g.get("cametoday", self.came_today), 0)
            self.last_sex_day = player_to_int(g.get("LastDaySex", self.last_sex_day), -1)
            self.last_cum_day = player_to_int(g.get("PlayerLastCumDay", self.last_cum_day), -1)
            had_sex = g.get("HadSex", {})
            if isinstance(had_sex, dict):
                self.had_sex_count = player_to_int(had_sex.get("You", had_sex.get("you", self.had_sex_count)), 0)
            return self

        def apply_to_store(self):
            g = globals()
            g["Arousal"] = dict(self.arousal or {})
            g["cancumdaily"] = player_to_int(self.can_cum_daily, 2)
            g["cametoday"] = player_to_int(self.came_today, 0)
            g["LastDaySex"] = player_to_int(self.last_sex_day, -1)
            g["PlayerLastCumDay"] = player_to_int(self.last_cum_day, -1)
            had_sex = g.get("HadSex", {})
            if not isinstance(had_sex, dict):
                had_sex = {}
            had_sex["You"] = player_to_int(self.had_sex_count, 0)
            g["HadSex"] = had_sex
            return self

    class PlayerChores(object):
        KEYS = ("bring_woods", "chop_wood", "make_fire", "clean_ashes", "boil_water", "clean_upstairs_rooms")

        def __init__(self):
            self.weekly = {}
            self.ui = {}
            self.counters = dict((key, 0) for key in self.KEYS)

        def sync_from_store(self):
            g = globals()
            self.weekly = dict(g.get("PlayerChoresWeek", self.weekly) or {})
            self.ui = dict(g.get("UI_chores", self.ui) or {})
            for key in self.KEYS:
                self.counters[key] = player_to_int(g.get(key, self.counters.get(key, 0)), 0)
            return self

        def apply_to_store(self):
            g = globals()
            g["PlayerChoresWeek"] = dict(self.weekly or {})
            g["UI_chores"] = dict(self.ui or {})
            for key in self.KEYS:
                g[key] = player_to_int(self.counters.get(key, 0), 0)
            return self

    class PlayerTavernManagement(object):
        def __init__(self):
            self.productnum = 0
            self.winenum = 0
            self.cleanliness = 60
            self.upstairs_rooms_dirty = 0
            self.ashes_dirty_days = 0
            self.weekly_visitors = {"sum": 0, "days": 0, "prev_avg": 0.0}

        def sync_from_store(self):
            g = globals()
            self.productnum = player_to_int(g.get("productnum", self.productnum), 0)
            self.winenum = player_to_int(g.get("winenum", self.winenum), 0)
            self.cleanliness = player_to_int(g.get("taverncleanliness", self.cleanliness), 60)
            self.upstairs_rooms_dirty = player_to_int(g.get("upstairsroomsdirty", self.upstairs_rooms_dirty), 0)
            self.ashes_dirty_days = player_to_int(g.get("ashesdirtydays", self.ashes_dirty_days), 0)
            self.weekly_visitors = dict(g.get("WeeklyVisitorsTrack", self.weekly_visitors) or {})
            return self

        def apply_to_store(self):
            g = globals()
            g["productnum"] = player_to_int(self.productnum, 0)
            g["winenum"] = player_to_int(self.winenum, 0)
            g["taverncleanliness"] = player_to_int(self.cleanliness, 60)
            g["upstairsroomsdirty"] = player_to_int(self.upstairs_rooms_dirty, 0)
            g["ashesdirtydays"] = player_to_int(self.ashes_dirty_days, 0)
            g["WeeklyVisitorsTrack"] = dict(self.weekly_visitors or {})
            return self

    class PlayerCombat(object):
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

        def __init__(self):
            self.party = []
            self.fight_level = {"you": 1}
            self.supply = dict(self.FIGHT_SUPPLY_DEFAULTS)

        def sync_from_store(self):
            g = globals()
            party = []
            if isinstance(g.get("player_company", []), list):
                party.extend(list(g.get("player_company", []) or []))
            if isinstance(g.get("company_list", []), list):
                party.extend(list(g.get("company_list", []) or []))
            self.party = player_normalize_id_list(party)

            fight_level = g.get("FightLevel", self.fight_level)
            self.fight_level = dict(fight_level or {}) if isinstance(fight_level, dict) else {"you": 1}
            self.fight_level["you"] = max(1, player_to_int(self.fight_level.get("you", 1), 1))

            supply = g.get("PlayerFightSupply", self.supply)
            self.supply = dict(self.FIGHT_SUPPLY_DEFAULTS)
            if isinstance(supply, dict):
                for key, value in supply.items():
                    self.supply[str(key or "")] = max(0, player_to_int(value, 0))
            return self

        def apply_to_store(self):
            g = globals()
            g["player_company"] = list(self.party or [])
            g["company_list"] = list(self.party or [])
            g["FightLevel"] = dict(self.fight_level or {"you": 1})
            g["FightLevel"]["you"] = max(1, player_to_int(g["FightLevel"].get("you", 1), 1))
            g["PlayerFightSupply"] = dict(self.supply or {})
            for key, value in self.FIGHT_SUPPLY_DEFAULTS.items():
                g["PlayerFightSupply"].setdefault(key, value)
            return self

        def add_party_member(self, member_id):
            member_key = str(member_id or "").strip()
            if not member_key:
                return False
            if member_key not in self.party:
                self.party.append(member_key)
            return True

        def remove_party_member(self, member_id):
            member_key = str(member_id or "").strip()
            if not member_key:
                return False
            self.party = [value for value in list(self.party or []) if str(value or "") != member_key]
            return True

    class Player(object):
        def __init__(self):
            self.identity = PlayerIdentity()
            self.condition = PlayerCondition()
            self.stats = PlayerStats()
            self.skills = {}
            self.economy = PlayerEconomy()
            self.inventory = PlayerInventory()
            self.equipment = PlayerEquipment()
            self.appearance = PlayerAppearance()
            self.intimacy = PlayerIntimacy()
            self.chores = PlayerChores()
            self.tavern_management = PlayerTavernManagement()
            self.combat = PlayerCombat()
            self.history = {}
            self.events = []

        @property
        def code_name(self):
            return self.identity.code_name

        @property
        def display_name(self):
            return self.identity.display_name

        def sync_from_store(self):
            for feature in (self.identity, self.condition, self.stats, self.economy, self.inventory,
                            self.equipment, self.appearance, self.intimacy, self.chores,
                            self.tavern_management, self.combat):
                feature.sync_from_store()
            return self

        def apply_to_store(self):
            for feature in (self.identity, self.condition, self.stats, self.economy, self.inventory,
                            self.equipment, self.appearance, self.intimacy, self.chores,
                            self.tavern_management, self.combat):
                feature.apply_to_store()
            return self

        def add_money(self, amount):
            self.sync_from_store()
            value = self.economy.add_money(amount)
            self.economy.apply_to_store()
            return value

        def spend_money(self, amount):
            self.sync_from_store()
            ok = self.economy.spend_money(amount)
            if ok:
                self.economy.apply_to_store()
            return ok

        def change_stat(self, stat_name, delta, minimum=0, maximum=100):
            self.sync_from_store()
            result = self.condition.change(stat_name, delta, minimum, maximum)
            if result is None:
                result = self.stats.change(stat_name, delta, minimum, maximum)
            self.condition.apply_to_store()
            self.stats.apply_to_store()
            return result

        def item_count(self, item_id):
            self.inventory.sync_from_store()
            return self.inventory.count(item_id)

        def add_item(self, item_id, quantity=1):
            self.inventory.sync_from_store()
            ok = self.inventory.add(item_id, quantity)
            if ok:
                self.inventory.apply_to_store()
                self.appearance.sync_from_store()
                self.appearance.ensure_item_life(item_id)
                self.appearance.apply_to_store()
            return ok

        def remove_item(self, item_id, quantity=1):
            self.inventory.sync_from_store()
            ok = self.inventory.remove(item_id, quantity)
            if ok:
                self.inventory.apply_to_store()
            return ok

        def equip(self, item_id, slot=""):
            self.sync_from_store()
            if self.inventory.count(item_id) <= 0:
                return False
            ok = self.equipment.equip(item_id, slot)
            if ok:
                self.equipment.apply_to_store()
            return ok

        def unequip(self, slot=""):
            self.equipment.sync_from_store()
            ok = self.equipment.unequip(slot)
            if ok:
                self.equipment.apply_to_store()
            return ok

        def wear_dress(self, dress_code):
            self.appearance.sync_from_store()
            ok = self.appearance.wear_dress(dress_code, globals().get("dayspassed", 0))
            if ok:
                self.appearance.apply_to_store()
            return ok

        def remove_current_dress(self, dress_code=""):
            self.appearance.sync_from_store()
            ok = self.appearance.remove_current_dress(dress_code)
            if ok:
                self.appearance.apply_to_store()
            return ok

        def daily_maintenance(self, days=1):
            self.sync_from_store()
            item_ids = self.inventory.ids(False)
            self.appearance.age_daily(days, item_ids)
            self.appearance.apply_to_store()
            return self

        def add_party_member(self, member_id):
            self.combat.sync_from_store()
            ok = self.combat.add_party_member(member_id)
            if ok:
                self.combat.apply_to_store()
            return ok

        def remove_party_member(self, member_id):
            self.combat.sync_from_store()
            ok = self.combat.remove_party_member(member_id)
            if ok:
                self.combat.apply_to_store()
            return ok

    def ensure_player_runtime():
        global player, mc
        if "player" not in globals() or not isinstance(globals().get("player"), Player):
            player = Player()
        if "mc" not in globals() or not isinstance(globals().get("mc"), Player):
            mc = player
        if mc is not player:
            mc = player
        return player

    def sync_player_state_from_store():
        return ensure_player_runtime().sync_from_store()

    def sync_player_state_to_store():
        return ensure_player_runtime().apply_to_store()

    def player_state(sync=True):
        runtime = ensure_player_runtime()
        if bool(sync):
            runtime.sync_from_store()
        return runtime

    def player_after_load_init():
        sync_player_state_from_store()

    if player_after_load_init not in config.after_load_callbacks:
        config.after_load_callbacks.append(player_after_load_init)

default player = Player()
default mc = player
