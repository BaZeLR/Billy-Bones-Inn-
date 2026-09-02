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

    class PlayerCondition(object):
        def __init__(self):
            self.health = 100
            self.energy = 100
            self.fun = 50
            self.sick_days = 0
            self.forest_ban_until_day = 0
            self.notice_state = {}

        def change(self, stat_name, delta, minimum=0, maximum=100):
            key = str(stat_name or "").strip()
            if not hasattr(self, key):
                return None
            raw_value = player_to_int(getattr(self, key), 0) + player_to_int(delta, 0)
            value = player_clamp_value(raw_value, minimum, maximum)
            setattr(self, key, value)
            return value

    class PlayerStats(object):
        def __init__(self):
            self.charisma = 0
            self.reputation = 0
            self.notoriety = 0
            self.exploration = 0
            self.rebellion = 0

        def change(self, stat_name, delta, minimum=0, maximum=100):
            key = str(stat_name or "").strip()
            if not hasattr(self, key):
                return None
            raw_value = player_to_int(getattr(self, key), 0) + player_to_int(delta, 0)
            if key == "exploration" and maximum == 100:
                value = max(player_to_int(minimum, 0), raw_value)
            else:
                value = player_clamp_value(raw_value, minimum, maximum)
            setattr(self, key, value)
            return value

    class PlayerEconomy(object):
        def __init__(self):
            self.money = 10000
            self.tavern_fame = 0
            self.child_support_count = 0
            self.child_birth_benefit_notice = ""
            self.church_donated_amount = 0
            self.church_donated_today = 0
            self.church_repairs_donated = [0] * 10

        def add_money(self, amount):
            self.money = max(0, player_to_int(self.money, 0) + player_to_int(amount, 0))
            return self.money

        def set_money(self, amount):
            self.money = max(0, player_to_int(amount, 0))
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

        def church_repair_is_donated(self, repair_index):
            return bool(self.church_repairs_donated[player_to_int(repair_index, 0)])

        def record_church_donation(self, repair_index, amount):
            index = player_to_int(repair_index, 0)
            self.church_repairs_donated[index] = 1
            self.church_donated_today = 1
            self.church_donated_amount += max(0, player_to_int(amount, 0))
            return self.church_donated_amount

    class PlayerInventory(object):
        def __init__(self, items=None):
            self.items = player_normalize_inventory(items or {})

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
            self.dress_life_days = {"villagedress": self.DRESS_LIFE_DAYS}
            self.destroyed_dresses = []
            self.item_life_days = {}
            self.days_since_haircut = 0
            self.days_since_wash = 0
            self.sleep_bottom_layer = "daywear"
            self.girl_dresses_bought = 0
            self.soap_look_bonus = 0
            self.soap_look_bonus_until_day = -1

        def has_dress(self, dress_code):
            dress_key = str(dress_code or "").strip()
            return bool(dress_key) and dress_key in list(self.owned_dresses or []) and dress_key not in list(self.destroyed_dresses or [])

        def add_dress(self, dress_code, acquired_day=0):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            if dress_key in list(self.destroyed_dresses or []):
                return False
            self.owned_dresses = player_normalize_id_list(self.owned_dresses)
            if dress_key not in self.owned_dresses:
                self.owned_dresses.append(dress_key)
            if not isinstance(self.dress_life_days, dict):
                self.dress_life_days = {}
            self.dress_life_days.setdefault(dress_key, self.DRESS_LIFE_DAYS)
            return True

        def replace_dress(self, dress_code, acquired_day=0):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            self.destroyed_dresses = [
                row for row in player_normalize_id_list(self.destroyed_dresses)
                if row != dress_key
            ]
            self.owned_dresses = player_normalize_id_list(self.owned_dresses)
            if dress_key not in self.owned_dresses:
                self.owned_dresses.append(dress_key)
            if not isinstance(self.dress_life_days, dict):
                self.dress_life_days = {}
            self.dress_life_days[dress_key] = self.DRESS_LIFE_DAYS
            return True

        def remove_dress(self, dress_code):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            self.owned_dresses = [row for row in list(self.owned_dresses or []) if str(row or "").strip() != dress_key]
            if isinstance(self.dress_life_days, dict) and dress_key in self.dress_life_days:
                del self.dress_life_days[dress_key]
            if str(self.current_dress or "").strip() == dress_key:
                self.current_dress = ""
                self.sleep_bottom_layer = "nothing"
            return True

        def destroy_dress(self, dress_code):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            self.remove_dress(dress_key)
            self.destroyed_dresses = player_normalize_id_list(self.destroyed_dresses)
            if dress_key not in self.destroyed_dresses:
                self.destroyed_dresses.append(dress_key)
            return True

        def wear_dress(self, dress_code, acquired_day=0):
            dress_key = str(dress_code or "").strip()
            if not dress_key:
                return False
            if not self.has_dress(dress_key):
                return False
            self.current_dress = dress_key
            self.sleep_bottom_layer = "nightwear" if dress_key == "nightshirt" else "daywear"
            return True

        def remove_current_dress(self, dress_code=""):
            dress_key = str(dress_code or "").strip()
            current = str(self.current_dress or "").strip()
            if dress_key and dress_key != current:
                return False
            self.current_dress = ""
            self.sleep_bottom_layer = "nothing"
            return True

        def dress_age_days(self, dress_code="", current_day=0):
            dress_key = str(dress_code or self.current_dress or "").strip()
            if not dress_key:
                return 0
            if not isinstance(self.dress_life_days, dict):
                self.dress_life_days = {}
            self.dress_life_days.setdefault(dress_key, self.DRESS_LIFE_DAYS)
            remaining = max(0, player_to_int(self.dress_life_days.get(dress_key, 0), 0))
            return max(0, self.DRESS_LIFE_DAYS - remaining)

        def dress_condition(self, dress_code=""):
            dress_key = str(dress_code or self.current_dress or "").strip()
            if not dress_key or not self.has_dress(dress_key):
                return 0
            remaining = max(0, player_to_int(self.dress_life_days.get(dress_key, 0), 0))
            if remaining <= 0:
                return 0
            elapsed = max(0, self.DRESS_LIFE_DAYS - remaining)
            return max(0, 100 - int(round((float(elapsed) / float(self.DRESS_LIFE_DAYS)) * 50.0)))

        def damage_dress(self, dress_code="", condition_loss=15):
            dress_key = str(dress_code or self.current_dress or "").strip()
            if not dress_key or not self.has_dress(dress_key):
                return 0
            loss = max(0, player_to_int(condition_loss, 0))
            life_loss = max(1, (loss * self.DRESS_LIFE_DAYS + 49) // 50) if loss else 0
            self.dress_life_days[dress_key] = max(
                0,
                player_to_int(self.dress_life_days.get(dress_key, self.DRESS_LIFE_DAYS), self.DRESS_LIFE_DAYS) - life_loss,
            )
            return self.dress_condition(dress_key)

        def wash(self):
            self.days_since_wash = 0
            return True

        def wash_with_soap(self, current_day=0, bonus=10, duration_days=1):
            self.wash()
            self.soap_look_bonus = max(0, player_to_int(bonus, 10))
            self.soap_look_bonus_until_day = player_to_int(current_day, 0) + max(0, player_to_int(duration_days, 1))
            return self.soap_look_bonus

        def increment_wash_days(self, amount=1):
            amount_value = max(0, player_to_int(amount, 1))
            self.days_since_wash = max(0, player_to_int(self.days_since_wash, 0) + amount_value)
            return self.days_since_wash

        def mark_haircut(self):
            self.days_since_haircut = 0
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

            return self

        def ensure_nightwear(self, current_day=0):
            return self.add_dress("nightshirt", current_day)

        def set_sleep_layer(self, mode="daywear", current_day=0):
            mode_key = str(mode or "daywear").strip().lower()
            if mode_key in ("naked", "nothing", "none"):
                self.current_dress = ""
                self.sleep_bottom_layer = "nothing"
            elif mode_key in ("night", "nightwear", "sleep"):
                if self.has_dress("nightshirt"):
                    self.current_dress = "nightshirt"
                    self.sleep_bottom_layer = "nightwear"
                else:
                    self.current_dress = ""
                    self.sleep_bottom_layer = "nothing"
            else:
                self.owned_dresses = player_normalize_id_list(self.owned_dresses)
                daywear = [row for row in list(self.owned_dresses or []) if str(row or "").strip() != "nightshirt" and row not in list(self.destroyed_dresses or [])]
                current = str(self.current_dress or "").strip()
                if current in daywear:
                    self.sleep_bottom_layer = "daywear"
                elif len(daywear) > 0:
                    self.current_dress = daywear[0]
                    self.sleep_bottom_layer = "daywear"
                else:
                    self.current_dress = ""
                    self.sleep_bottom_layer = "nothing"
            return self.sleep_bottom_layer

        def is_naked(self):
            return str(self.sleep_bottom_layer or "") == "nothing" or str(self.current_dress or "").strip() == ""

        def is_nightwear(self):
            return str(self.sleep_bottom_layer or "") == "nightwear" or str(self.current_dress or "") == "nightshirt"

    class PlayerIntimacy(object):
        def __init__(self):
            self.arousal = 0
            self.can_cum_daily = 2
            self.came_today = 0
            self.last_sex_day = -1
            self.last_cum_day = -1
            self.history = {}
            self.had_sex_count = 0
            self.morning_arousal_day = -1
            self.wake_state_notice = ""
            self.arousal_reasons = []
            self.observed_naked_npc_day = {}
            self.last_help_result = {}
            self.body_containers = {}
            self.ellona_blessed = 0
            self.ellona_cursed = 0
            self.ellona_curse_days = 0
            self.ellona_curse_reduction = 0
            self.ellona_grace_blessings = [0, 0, 0, 0, 0, 0]

        def arousal_value(self):
            self.arousal = player_clamp_value(self.arousal, 0, 100)
            return self.arousal

        def set_arousal(self, value):
            self.arousal = player_clamp_value(value, 0, 100)
            return self.arousal

        def add_arousal(self, amount=0, cap=100):
            return self.set_arousal(min(player_to_int(cap, 100), self.arousal_value() + player_to_int(amount, 0)))

        def can_cum(self):
            return player_to_int(self.came_today, 0) < max(1, player_to_int(self.can_cum_daily, 1))

        def grant_ellona_grace(self, grace_index):
            self.ellona_grace_blessings[player_to_int(grace_index, 0)] = 1
            return sum(player_to_int(value, 0) for value in self.ellona_grace_blessings)

        def grant_ellona_blessing(self):
            if not self.ellona_blessed:
                self.ellona_blessed = 1
                self.can_cum_daily += 1
            return self.can_cum_daily

        def apply_ellona_curse(self, days=14):
            self.ellona_cursed = 1
            self.ellona_curse_reduction = max(0, player_to_int(self.can_cum_daily, 0))
            self.can_cum_daily = 0
            self.ellona_curse_days = max(0, player_to_int(days, 14))
            return self.ellona_curse_days

        def extend_ellona_curse(self, days=7):
            self.ellona_curse_days += max(0, player_to_int(days, 7))
            return self.ellona_curse_days

        def lift_ellona_curse(self):
            if self.ellona_cursed:
                self.can_cum_daily += max(0, player_to_int(self.ellona_curse_reduction, 0))
            self.ellona_cursed = 0
            self.ellona_curse_days = 0
            self.ellona_curse_reduction = 0
            return self.can_cum_daily

        def record_cum(self, day_value=0):
            self.came_today = player_to_int(self.came_today, 0) + 1
            self.had_sex_count = player_to_int(self.had_sex_count, 0) + 1
            self.last_sex_day = player_to_int(day_value, 0)
            self.last_cum_day = player_to_int(day_value, 0)
            self.set_arousal(0)
            return self.came_today

    class PlayerChores(object):
        KEYS = ("bring_woods", "chop_wood", "make_fire", "clean_ashes", "boil_water", "clean_upstairs_rooms")

        def __init__(self):
            self.weekly = {}
            self.last_score = 0
            self.last_evaluation = ""

    class PlayerBreakfastState(object):
        def __init__(self):
            self.today = False
            self.last_day = -1
            self.day = -1
            self.base_text = ""
            self.soap_announced_day = -1
            self.barber_talk_day = -1
            self.listen_day = -1
            self.market_talk_day = -1
            self.motivation_day = -1
            self.absent_talk_day = -1
            self.base_shown_day = -1
            self.event_active = False
            self.sunday_dinner_last_day = -1
            self.sunday_dinner_barber_talk_day = -1
            self.spicy_drink_day = -1
            self.sunday_dinner_spicy_drink_day = -1
            self.georgett_liza_pending = 0
            self.present_ids = None
            self.melissa_amanda_gerhard_day = -1
            self.food_perk_day = -1
            self.drink_perk_day = -1
            self.lewd_series_day = -1
            self.appearance_perk_day = -1
            self.sweet_perk_day = -1
            self.blind_pirate_team_pledge = 0
            self.milk_team_talk_done = 0
            self.ale_team_talk_done = 0
            self.dance_sponsor_announced_day = -1

    class PlayerGloryHoleSessionState(object):
        def __init__(self):
            self.reset()

        def reset(self):
            self.girl_name = ""
            self.current_step = 0
            self.cock_inserted = 0
            self.inside = 0
            self.inside_once = 0
            self.works = 0
            self.client_line1 = ""
            self.client_line2 = ""
            self.client_line3 = ""
            self.girl_line0 = ""
            self.girl_line1 = ""
            self.girl_line2 = ""
            self.girl_line3 = ""
            self.menu_blocked = 0
            self.amanda_present = 0
            self.player_line1 = "Вы засунули свое самое дорогое в дырку. Однако с той стороны никто не поспешил вам на помощь. Вы, еще на что-то надеясь, подождали немного, но безрезультатно. Продолжать стоять дальше с засунутым в отверстие в стене членом в гнетущей тишине показалось вам глуповатым, и, со вздохом разочарования, вы убрали свое хозяйство обратно в штаны. <br>В голове у вас возникло несколько гипотез, объясняющих произошедшее. Возможно вы пришли слишком рано, а может пришли вовремя, но не назначили никого работать у глорихола. Надо провести тщательное расследование."
            self.player_line2 = ""
            self.player_line3 = ""

        def roll_inside(self, worker_corruption=0):
            self.inside = 0
            self.inside_once = 0
            if not self.works or self.amanda_present or not self.girl_name:
                return

            corruption = max(0, player_to_int(worker_corruption, 0))
            if corruption >= 80:
                if procedural_randint(1, 4, key="procedural:Inn/TavernGloryHole.rpy:inside:80") == 1:
                    self.inside = 1
            elif corruption >= 50:
                if procedural_randint(1, 8, key="procedural:Inn/TavernGloryHole.rpy:inside:50") == 1:
                    self.inside = 1

            if self.inside == 0 and corruption >= 40 and procedural_randint(1, 3, key="procedural:Inn/TavernGloryHole.rpy:inside_once") == 1:
                self.inside_once = 1

            self.player_line1 = "Вы засунули свое самое дорогое в дырку, в пугающую неизвестность. И ваша смелость была вознагражденна: чей-то страстный язычок с другой стороны глорихола начал облизывать головку вашего члена. Вскоре незнакомка стала посасывать ваш, уже принявший полную боевую готовность, агрегат, делая вам весьма и весьма приятно."
            if self.inside or self.inside_once:
                self.player_line2 = "Только вы начали входить во вкус, как вдруг минет неожиданно прекращается. Вы с трудом сдерживаете стон разочарования, но тут же вместо ротика на ваш член насаживается что-то теплое и влажное. Вы с трудом верите в происходящее: развратная незнакомка стала трахать вас своей киской! Вы уже очень близки к оргазму."
                if self.inside:
                    self.player_line3 = "Влагалище вашей невидимой любовницы сжимается и из-за ширмы слышится протяжный стон - она кончила. Вы не выдерживаете и тоже кончаете прямо внутрь, заливая ее своим семенем. Хотя ваш обмякший член и выскользнул из жаркой пещерки, но это было еще не все - ловкая незнакомка развернулась у себя за ширмой и ее язычок слизал остатки спермы с вашего обмякшего члена. Удовлетворенный вы застегнули штаны."
                else:
                    self.player_line3 = "Вы уже собирались было кончить во влагалище вашей невидимой подружки, но плутовка как видно угадала ваше намерение и в последний момент соскользнула с вашего ствола, впрочем, быстро взяв его обратно в свой страстный ротик, в который вы и разрядились. Напоследок вам слизали остатки спермы с вашего обмякшего члена. Удовлетворенный вы застегнули штаны."
            else:
                self.player_line2 = "Вы продолжаете наслаждаться минетом от невидимой прелестницы, которая теперь уже заглатывает ваш член почти по самые яйца. Долго такого вы выдержать не можете, вы уже на грани, еще немного и вы кончите."
                self.player_line3 = "Громкий стон по ту сторону ширмы известил вас, что ваша невидимая подруга кончила, лаская себя. Вы решили последовать ее примеру и взорвались, заполняя ее ротик потоками своего семени. Вы почуствовали как чей-то ловкий язычок слизал остатки спермы с вашего обмякшего члена. Удовлетворенный вы застегнули штаны."

    class PlayerTavernServiceState(object):
        def __init__(self):
            self.kitchen_score = 0.0
            self.cleanliness_score = 0.0
            self.waitress_score = 0.0
            self.kitchen_quality = "невыносимо"
            self.cleanliness_quality = "тараканы с трудом могут пробраться сквозь липкую грязь покрывающую все"
            self.waitress_quality = "не ведется вообще, заказать что-либо у вас невозможно."

    class PlayerTavernManagement(object):
        def __init__(self):
            self.productnum = 200
            self.winenum = 100
            self.visitors = 40
            self.slogan_state = 0
            self.client_room_hole = 0
            self.glory_hole = 0
            self.glory_hole_look = 0
            self.glory_hole_session = PlayerGloryHoleSessionState()
            self.dance_sponsor = 0
            self.dance_sponsor_pledge_day = -1
            self.household_members = 4
            self.breakfast = PlayerBreakfastState()
            self.cleanliness = 60
            self.upstairs_rooms_dirty = 0
            self.ashes_dirty_days = 0
            self.weekly_visitors = {"sum": 0, "days": 0, "prev_avg": 0.0}
            self.weekly_chores_last_eval_stamp = ""
            self.breakfast_share_perks = {}
            self.service = PlayerTavernServiceState()

    class PlayerHorse(object):
        def __init__(self):
            self.name = ""
            self.saddled = False
            self.purchase_price = 0
            self.stolen_purchase_price = 0
            self.stolen_days = 0

        def owns_horse(self):
            return bool(str(self.name or "").strip())

        def acquire(self, name, purchase_price=0, saddled=True):
            self.name = str(name or "").strip()
            self.purchase_price = max(0, player_to_int(purchase_price, 0))
            self.saddled = bool(saddled) and self.owns_horse()
            return self.owns_horse()

        def remove(self):
            old_name = str(self.name or "")
            self.name = ""
            self.saddled = False
            self.purchase_price = 0
            return old_name

        def mark_stolen(self, days=14):
            old_name = str(self.name or "")
            self.stolen_purchase_price = max(0, player_to_int(self.purchase_price, 0))
            self.name = ""
            self.saddled = False
            self.purchase_price = 0
            self.stolen_days = max(0, player_to_int(days, 14))
            return old_name

    class PlayerCombat(object):
        def __init__(self):
            self.party = []
            self.special_supply = {"bees_bomb": 0}
            self.mana = 50

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
            self.horse = PlayerHorse()
            self.combat = PlayerCombat()
            self.history = {}
            self.events = []
            self.sleep_wake_hour_override = -1
            self.sleep_wake_minute_override = 0

        @property
        def code_name(self):
            return self.identity.code_name

        @property
        def display_name(self):
            return self.identity.display_name

        def add_money(self, amount):
            return self.economy.add_money(amount)

        def set_money(self, amount):
            return self.economy.set_money(amount)

        def change_tavern_fame(self, amount):
            self.economy.tavern_fame = player_to_int(self.economy.tavern_fame, 0) + player_to_int(amount, 0)
            return self.economy.tavern_fame

        def spend_money(self, amount):
            return self.economy.spend_money(amount)

        def change_stat(self, stat_name, delta, minimum=0, maximum=100):
            key = str(stat_name or "").strip()
            if hasattr(self.condition, key):
                return self.condition.change(key, delta, minimum, maximum)
            return self.stats.change(key, delta, minimum, maximum)

        def set_stat(self, stat_name, value, minimum=0, maximum=100):
            key = str(stat_name or "").strip()
            target = self.condition if hasattr(self.condition, key) else self.stats
            if not hasattr(target, key):
                return None
            if target is self.stats and key == "exploration" and maximum == 100:
                result = max(player_to_int(minimum, 0), player_to_int(value, 0))
            else:
                result = player_clamp_value(value, minimum, maximum)
            setattr(target, key, result)
            return result

        def item_count(self, item_id):
            return self.inventory.count(item_id)

        def add_item(self, item_id, quantity=1):
            ok = self.inventory.add(item_id, quantity)
            if ok:
                self.appearance.ensure_item_life(item_id)
            return ok

        def remove_item(self, item_id, quantity=1):
            return self.inventory.remove(item_id, quantity)

        def equip(self, item_id, slot=""):
            if self.inventory.count(item_id) <= 0:
                return False
            return self.equipment.equip(item_id, slot)

        def unequip(self, slot=""):
            return self.equipment.unequip(slot)

        def wear_dress(self, dress_code):
            return self.appearance.wear_dress(dress_code, calendar_v2.daysInGame)

        def remove_current_dress(self, dress_code=""):
            return self.appearance.remove_current_dress(dress_code)

        def daily_maintenance(self, days=1):
            item_ids = self.inventory.ids(False)
            self.appearance.age_daily(days, item_ids)
            return self

        def add_party_member(self, member_id):
            return self.combat.add_party_member(member_id)

        def remove_party_member(self, member_id):
            return self.combat.remove_party_member(member_id)

    def player_equipped_weapon_id():
        return str(player.equipment.weapon or "").strip()

    def player_has_equipped_weapon(item_id=""):
        return player_equipped_weapon_id() == player_normalize_item_id(item_id)

default player = Player()
