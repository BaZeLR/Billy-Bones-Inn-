# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default player_company = []

init -5 python:
    import random
    import renpy.exports as renpy_module

    DOG_SPAWN_LOCATIONS = (
        "PortStreets",
        "MarketPlace",
        "ArtisansQuarter",
        "StreetTavern",
    )

    def dog_spawn_location_candidates(time_slot=None):
        candidates = []
        try:
            candidates = list(rooms_in_group(ROOM_GROUP_CITY) or [])
        except Exception:
            candidates = []
        if len(candidates) <= 0:
            candidates = list(DOG_SPAWN_LOCATIONS)

        out = []
        for room_code in candidates:
            room_key = str(room_code or "").strip()
            if not room_key:
                continue
            try:
                if not renpy_module.has_label(room_key):
                    continue
            except Exception:
                pass
            out.append(room_key)

        if len(out) <= 0:
            out = list(DOG_SPAWN_LOCATIONS)
        return sorted(set(out))

    class DogCompanion(object):
        def __init__(self):
            self.met = False
            self.owned = False
            self.in_company = False
            self.name = "Пес"

            self.level = 1
            self.training_progress = 0
            self.play_sessions = 0
            self.bones_given = 0
            self.stray_played = False
            self.last_play_day = -1
            self.last_train_day = -1

            self.loyalty = 0
            self.max_loyalty = 25
            self.health = 50

            self.booth_built = False
            self.can_haul = False

            self.spawn_day = -1
            self.spawn_location = None

        @property
        def max_health(self):
            if int(self.level or 0) >= 2:
                return 65
            return 50

        @property
        def bite_damage(self):
            if int(self.level or 0) >= 2:
                return 25
            return 20

        @property
        def defense(self):
            return 15

        @property
        def skill_name(self):
            if int(self.level or 0) >= 2:
                return "Мертвая хватка"
            return "Укус"

        def sync_health(self):
            self.health = max(0, min(int(self.max_health or 0), int(self.health or 0)))

        def gain_loyalty(self, amount):
            self.loyalty = min(int(self.max_loyalty or 25), max(0, int(self.loyalty or 0) + int(amount or 0)))
            if int(self.loyalty or 0) >= 10:
                self.can_haul = True

        def try_level_up(self):
            while int(self.training_progress or 0) >= 5 and int(self.level or 0) < 2:
                self.training_progress -= 5
                self.level += 1
                self.health = self.max_health

        def prepare_evening_spawn(self, day_number, time_slot):
            day_value = int(day_number or 0)
            slot_value = int(time_slot or 0)

            if self.owned:
                self.spawn_day = day_value
                self.spawn_location = None
                return

            if slot_value != 3:
                if int(self.spawn_day or -1) != day_value:
                    self.spawn_location = None
                return

            if int(self.spawn_day or -1) == day_value:
                return

            self.spawn_day = day_value
            self.spawn_location = random.choice(dog_spawn_location_candidates(slot_value))

        def is_here(self, room_code, day_number, time_slot):
            if self.owned:
                return False
            if int(time_slot or 0) != 3:
                return False
            return int(self.spawn_day or -1) == int(day_number or 0) and str(self.spawn_location or "") == str(room_code or "")

        def adopt(self, dog_name=""):
            if self.owned:
                return False
            if int(self.bones_given or 0) <= 0:
                return False
            if not bool(self.stray_played):
                return False
            if not player_has_dog_collar():
                return False
            if not player_remove_dog_collar():
                return False

            self.met = True
            self.owned = True
            self.in_company = True
            chosen_name = str(dog_name or "").strip()
            self.name = chosen_name if chosen_name in dog_name_options() else dog_random_name()
            self.health = self.max_health
            self.gain_loyalty(3)
            player_state().add_party_member("dog")
            self.spawn_location = None
            try:
                npc_daily_schedule_build_all(True)
                dog_sync_profile()
            except Exception:
                pass
            return True

        def meet_stray(self):
            if self.owned:
                return False
            self.met = True
            return True

        def feed_stray_bone(self):
            if self.owned:
                return False
            if not player_has_bone():
                return False
            if not player_remove_bone():
                return False
            self.met = True
            self.bones_given += 1
            self.gain_loyalty(1)
            return True

        def play_stray(self):
            if self.owned:
                return False
            if int(self.bones_given or 0) <= 0:
                return False
            if int(self.last_play_day or -1) == int(dayspassed or 0):
                return False
            self.met = True
            self.stray_played = True
            self.last_play_day = int(dayspassed or 0)
            self.play_sessions += 1
            self.gain_loyalty(1)
            return True

        def pet_stray(self):
            if self.owned:
                return True
            if int(self.bones_given or 0) <= 0:
                return False
            self.met = True
            self.gain_loyalty(1)
            return True

        def play(self):
            if not self.owned:
                return False
            if int(self.last_play_day or -1) == int(dayspassed or 0):
                return False
            self.last_play_day = int(dayspassed or 0)
            self.play_sessions += 1
            self.training_progress += 1
            self.gain_loyalty(2)
            self.try_level_up()
            return True

        def train(self):
            if not self.owned:
                return False
            if int(self.last_train_day or -1) == int(dayspassed or 0):
                return False
            self.last_train_day = int(dayspassed or 0)
            self.training_progress += 1
            self.gain_loyalty(1)
            self.try_level_up()
            return True

        def feed_bone(self, training=False):
            if not self.owned:
                return False
            if not player_has_bone():
                return False
            if bool(training) and int(self.last_train_day or -1) == int(dayspassed or 0):
                return False
            if not player_remove_bone():
                return False

            self.bones_given += 1
            self.gain_loyalty(1)
            if bool(training):
                self.last_train_day = int(dayspassed or 0)
                self.training_progress += 2
                self.try_level_up()
            return True

        def build_booth(self):
            if self.booth_built:
                return False
            self.booth_built = True
            self.gain_loyalty(5)
            return True

        def prevents_theft(self, theft_kind):
            if not self.owned:
                return False

            theft_key = str(theft_kind or "").strip()
            if theft_key == "horse" and int(self.loyalty or 0) >= 5:
                return True
            if theft_key == "tavern_nonpayment" and dog_can_guard_tavern() and int(self.loyalty or 0) >= 5:
                return True
            if theft_key == "clothes_backyard" and int(self.loyalty or 0) >= 10:
                return True
            if theft_key == "hauling" and int(self.loyalty or 0) >= 10:
                return True
            return False

        def receive_damage(self, amount):
            self.health -= int(amount or 0)
            self.sync_health()

        def heal_full(self):
            self.health = self.max_health

        def is_alive(self):
            return int(self.health or 0) > 0

        @property
        def state_key(self):
            if self.owned:
                return "adopted"
            return "stray"

        @property
        def state_label(self):
            if self.owned:
                return "приученный пес"
            if self.met:
                return "знакомый бродячий пес"
            return "бродячий пес"

    def ensure_dog_runtime():
        global dog
        if isinstance(dog, DogCompanion):
            for attr_name, default_value in (
                ("stray_played", False),
                ("last_play_day", -1),
                ("last_train_day", -1),
            ):
                if not hasattr(dog, attr_name):
                    setattr(dog, attr_name, default_value)
            return dog
        dog = DogCompanion()
        return dog

    def dog_random_name():
        return random.choice(dog_name_options())

    def dog_name_options():
        return ("Sharik", "Tresor", "Bobick", "Muchtar", "Drool")

    def player_has_bone():
        try:
            return _player_item_count_by_id("dog_bone_001") > 0
        except Exception:
            return False

    def player_remove_bone():
        try:
            return bool(_player_remove_item_by_id("dog_bone_001", 1))
        except Exception:
            return False

    def player_has_dog_collar():
        try:
            return _player_item_count_by_id("dog_collar_001") > 0
        except Exception:
            return False

    def player_remove_dog_collar():
        try:
            return bool(_player_remove_item_by_id("dog_collar_001", 1))
        except Exception:
            return False

    def dog_can_adopt_stray():
        d = ensure_dog_runtime()
        return (not bool(d.owned)) and int(d.bones_given or 0) > 0 and bool(d.stray_played) and player_has_dog_collar()

    def dog_stray_bite_player():
        global health
        health = _player_clamp(int(health or 0) - 5, 0, 100)
        d = ensure_dog_runtime()
        d.spawn_location = None
        d.spawn_day = int(dayspassed or 0)
        d.met = False
        return int(health or 0)

    def dog_prepare_current_spawn():
        ensure_dog_runtime().prepare_evening_spawn(int(dayspassed or 0), int(time or 0))
        dog_sync_profile()

    def dog_is_here(room_code=""):
        return ensure_dog_runtime().is_here(str(room_code or ""), int(dayspassed or 0), int(time or 0))

    def dog_can_call_stray_here(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        d = ensure_dog_runtime()
        return (not bool(d.owned)) and d.is_here(room_key, int(dayspassed or 0), int(time or 0))

    def dog_home_roam_active():
        d = ensure_dog_runtime()
        return bool(d.owned) and (not bool(d.in_company)) and bool(d.is_alive())

    def dog_is_available_here(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        d = ensure_dog_runtime()
        if dog_is_here(room_key):
            return True
        if dog_can_call_stray_here(room_key):
            return True
        if dog_home_roam_active() and str(getLocation("dog") or "") == room_key:
            return True
        if d.owned and d.in_company and bool(d.is_alive()):
            return True
        return False

    def dog_can_guard_tavern():
        d = ensure_dog_runtime()
        return bool(d.owned) and (not bool(d.in_company)) and bool(d.is_alive())

    def dog_card_title():
        return str(ensure_dog_runtime().name or "Пес")

    def dog_display_name():
        d = ensure_dog_runtime()
        if d.state_key == "adopted":
            return str(d.name or "Пес")
        return "Бродячий пес"

    def dog_action_data(where_id=""):
        room_code = str(where_id or CurLoc or "").strip()
        return {
            "entity_type": "dog",
            "entity_id": "dog",
            "title": str(dog_display_name() or "Пес"),
            "talk_label": "IntDogTalk",
            "talk_args": (room_code,),
            "examine_id": "dog",
            "examine_label": "",
            "actions": ["look", "talk"],
            "can_examine": True,
            "auto_card": True,
        }

    def dog_sync_profile():
        d = ensure_dog_runtime()
        RealName["dog"] = dog_display_name()
        RealName2["dog"] = dog_display_name()
        RealName3["dog"] = dog_display_name()
        knowsMC["dog"] = bool(d.met or d.owned)
        if d.owned and bool(d.in_company):
            CurrentLoc["dog"] = ""
            return ""
        if dog_home_roam_active():
            return npc_schedule_sync_currentloc("dog")
        if not dog_is_here(str(CurrentLoc.get("dog", "") or "")):
            CurrentLoc["dog"] = ""
        return str(CurrentLoc.get("dog", "") or "")

    def dog_card_portrait_path():
        d = ensure_dog_runtime()
        if not d.owned:
            candidates = ("images/dog/no_colar.png", "images/tavern/myroom/no_colar.png")
        elif d.booth_built:
            candidates = ("images/tavern/myroom/dog_booth.png", "images/player_room/dog_booth.png", "images/dog/dog_booth.png")
        else:
            candidates = ("images/tavern/myroom/dog.png", "images/player_room/dog.png", "images/dog/dog.png")
        for picture_path in candidates:
            if renpy_module.loadable(picture_path):
                return picture_path
        return candidates[0]

    def dog_card_stat_rows():
        d = ensure_dog_runtime()
        return [
            ("Состояние", str(d.state_label)),
            ("Уровень", str(d.level)),
            ("Лояльность", "%s / %s" % (str(d.loyalty), str(d.max_loyalty))),
            ("Здоровье", "%s / %s" % (str(d.health), str(d.max_health))),
            ("Навык", str(d.skill_name)),
            ("Укус", str(d.bite_damage)),
            ("Защита", str(d.defense)),
        ]

    def dog_card_lines():
        d = ensure_dog_runtime()
        lines = []
        if d.state_key == "stray":
            lines.append("Бродячий пес, который пока держится настороженно и не подпускает к себе кого попало.")
            if player_has_bone():
                lines.append("Похоже, его можно попробовать приманить костью.")
            return lines

        lines.append("Кличка: %s." % str(d.name))
        lines.append("Уровень: %s." % str(d.level))
        lines.append("Здоровье: %s / %s." % (str(d.health), str(d.max_health)))
        lines.append("Лояльность: %s / %s." % (str(d.loyalty), str(d.max_loyalty)))
        lines.append("Навык: %s." % str(d.skill_name))
        lines.append("Укус: %s." % str(d.bite_damage))
        lines.append("Защита: %s." % str(d.defense))
        lines.append("Будка построена: %s." % ("да" if d.booth_built else "нет"))
        lines.append("В компании: %s." % ("да" if d.in_company else "нет"))
        if d.can_haul:
            lines.append("Пес уже достаточно к вам привязался и может помогать таскать вещи.")
        return lines

    def dog_talk_picture_path(room_code=""):
        d = ensure_dog_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        if d.state_key == "stray":
            return dog_card_portrait_path()
        if bool(d.booth_built) and (not bool(d.in_company)) and room_key == "Backyard":
            return dog_card_portrait_path()
        if bool(d.in_company) and room_in_group(room_key, ROOM_GROUP_FOREST) and renpy_module.loadable("images/dog/dog.png"):
            return "images/dog/dog.png"
        return dog_card_portrait_path()

    def dog_talk_intro_text(room_code=""):
        d = ensure_dog_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        if d.state_key == "stray":
            if not bool(d.met):
                return "Небольшой, но крепкий бродячий пес держится настороженно и смотрит на вас издалека. Его можно осторожно позвать, но без кости он может не довериться."
            if int(d.bones_given or 0) <= 0:
                return "Пес подошел ближе, смотрит вам в глаза и нервно виляет хвостом. Голыми руками лучше не лезть: возможно, сначала стоит дать ему кость."
            if not bool(d.stray_played):
                return "Пес уже взял вашу кость и держится рядом спокойнее. Теперь можно попробовать поиграть с ним и понять, готов ли он довериться."
            return "Бродячий пес уже узнает вас, помахивает хвостом и ждет, что вы сделаете дальше. Для дома ему нужен ошейник."
        if bool(d.booth_built) and (not bool(d.in_company)) and room_key == "Backyard":
            return "Пес выглядывает из своей будки, шевелит ушами и сразу узнает вас. Увидев хозяина, он оживляется и ждет, что вы ему прикажете."
        if bool(d.in_company) and room_in_group(room_key, ROOM_GROUP_FOREST):
            return "Пес держится рядом с вами, постоянно принюхивается к лесу и готов сорваться вперед по вашему знаку."
        return "Пес сразу оживляется при вашем появлении, настораживает уши и внимательно следит, что вы собираетесь делать."

    def dog_main_ui_action_items(room_code="", include_card=True):
        room_key = str(room_code or CurLoc or "").strip()
        d = ensure_dog_runtime()
        items = []
        if not d.owned and (not bool(d.met)) and not dog_is_here(room_key):
            items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
            return items
        if bool(include_card):
            items.append(MenuItem("Осмотреть", Function(show_dog_card_main_ui_state, room_key)))
        if d.state_key == "stray":
            if not bool(d.met):
                items.append(MenuItem("Позвать пса", Call("IntDogTalkApply", room_key, "call_stray")))
            else:
                items.append(MenuItem("Попробовать погладить", Call("IntDogTalkApply", room_key, "pet_stray")))
                items.append(MenuItem("Попробовать поиграть", Call("IntDogTalkApply", room_key, "play_stray")))
                if player_has_bone():
                    items.append(MenuItem("Дать кость", Call("IntDogTalkApply", room_key, "stray_bone")))
                if dog_can_adopt_stray():
                    items.append(MenuItem("Надеть ошейник и забрать домой", Call("IntDogTalkApply", room_key, "adopt")))
        else:
            if int(d.last_play_day or -1) != int(dayspassed or 0):
                items.append(MenuItem("Поиграть с псом", Call("IntDogTalkApply", room_key, "play")))
            if int(d.last_train_day or -1) != int(dayspassed or 0):
                items.append(MenuItem("Позаниматься дрессировкой", Call("IntDogTalkApply", room_key, "train")))
            if player_has_bone():
                items.append(MenuItem("Угостить пса костью", Call("IntDogTalkApply", room_key, "bone")))
                items.append(MenuItem("Наградить костью за дрессировку", Call("IntDogTalkApply", room_key, "train_bone")))
            if d.in_company:
                items.append(MenuItem("Оставить сторожить дом", Call("IntDogTalkApply", room_key, "stay")))
            else:
                items.append(MenuItem("Взять пса на охоту", Call("IntDogTalkApply", room_key, "hunt")))
                if d.booth_built and room_key.startswith("Backyard"):
                    items.append(MenuItem("Оставить сторожить дом", Call("IntDogTalkApply", room_key, "stay")))
                for household_id in dog_household_walk_candidates(room_key):
                    items.append(MenuItem("Попросить %s погулять с псом" % _action_display_name(household_id), Call("IntDogTalkApply", room_key, "household_walk:" + str(household_id))))
        items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
        return items

    def show_dog_card_main_ui_state(room_code=""):
        global UI_mode, UI_selected_char, current_action_title, current_action_content, current_action_items
        room_key = str(room_code or CurLoc or "").strip()
        UI_mode = "dog"
        UI_selected_char = "dog"
        current_action_title = dog_card_title()
        current_action_content = None
        current_action_items = dog_main_ui_action_items(room_key, include_card=False)
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def dog_action_talk_state(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        picture_path = str(dog_talk_picture_path(room_key) or "").strip()
        if picture_path:
            try:
                ShowImage("", "", picture_path)
            except (AttributeError, NameError, TypeError, ValueError):
                global _layout_last_picture
                _layout_last_picture = picture_path
        renpy_module.call_in_new_context("IntDogTalk", room_key)

    def dog_action_look_state(room_code=""):
        show_dog_card_main_ui_state(room_code)

    def dog_open_action_menu_state(room_code=""):
        global _layout_last_picture, current_action_title, current_action_content, current_action_items
        room_key = str(room_code or CurLoc or "").strip()
        dog_data = dog_action_data(room_key)

        picture_path = str(dog_talk_picture_path(room_key) or "").strip()
        if picture_path:
            try:
                ShowImage("", "", picture_path)
            except (AttributeError, NameError, TypeError, ValueError):
                _layout_last_picture = picture_path

        current_action_title = str(dog_data.get("title", "") or "Пес")
        current_action_content = None
        current_action_items = dog_main_ui_action_items(room_key, include_card=True)

        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def dog_room_action_caption(room_code=""):
        d = ensure_dog_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        if d.owned and bool(d.booth_built) and (not bool(d.in_company)) and room_key == "Backyard":
            return "Позвать пса из будки"
        if (not bool(d.owned)) and dog_can_call_stray_here(room_key):
            return "Подозвать бродячего пса"
        if d.owned and str(getLocation("dog") or "") == room_key:
            return "Пес"
        if d.owned and d.in_company and room_in_group(str(room_code or CurLoc or ""), ROOM_GROUP_FOREST):
            return "Пес"
        return "Подозвать пса"

    def dog_household_walk_candidates(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        d = ensure_dog_runtime()
        if not d.owned or bool(d.in_company):
            return []
        candidates = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if int(Friends.get(npc_id, 0) or 0) < 15:
                continue
            try:
                if str(getLocation(npc_id) or "") != room_key:
                    continue
            except Exception:
                continue
            candidates.append(npc_id)
        return candidates


init 2 python:
    npc_daily_schedule_set(
        "dog",
        default_slots=[
            dict(npc_daily_schedule_slot(4, "Backyard", True, True, "sleep_by_booth"), condition=npc_schedule_rule("dog_home_roam")),
        ],
        random_slots=[
            npc_daily_schedule_random_slot(
                0,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="morning_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 4, True, True, "yard_watch", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernKitchen", 2, True, True, "kitchen_smells", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernStable", 2, True, True, "stable_watch", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernStorage", 1, True, True, "rat_smells", condition=npc_schedule_rule("dog_home_roam")),
                ],
            ),
            npc_daily_schedule_random_slot(
                1,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="noon_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 3, True, True, "yard_roam", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernMain", 2, True, True, "main_hall_watch", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernStable", 2, True, True, "stable_watch", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernMyRoom", 1, True, True, "player_room_door", condition=npc_schedule_rule("dog_home_roam")),
                ],
            ),
            npc_daily_schedule_random_slot(
                2,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="day_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 4, True, True, "yard_guard", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernStable", 3, True, True, "stable_guard", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernStorage", 1, True, True, "storage_guard", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernMain", 1, True, True, "hall_guard", condition=npc_schedule_rule("dog_home_roam")),
                ],
            ),
            npc_daily_schedule_random_slot(
                3,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="evening_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 4, True, True, "evening_yard", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernMain", 2, True, True, "evening_hall", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernStable", 2, True, True, "evening_stable", condition=npc_schedule_rule("dog_home_roam")),
                    npc_daily_schedule_choice("TavernKitchen", 1, True, True, "evening_kitchen", condition=npc_schedule_rule("dog_home_roam")),
                ],
            ),
        ],
    )

    def _dog_after_load_init():
        try:
            dog_sync_profile()
        except Exception:
            pass

    if _dog_after_load_init not in config.after_load_callbacks:
        config.after_load_callbacks.append(_dog_after_load_init)


label ShowDogCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ show_dog_card_main_ui_state()
        return
    show screen dog_card_overlay(return_label)
    return


label HideDogCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
        return
    hide screen dog_card_overlay
    if str(return_label or "") != "":
        call expression return_label
    return


label IntDogTalk(room_code=""):
    $ ensure_dog_runtime()
    $ _dog_room = str(room_code or CurLoc or "").strip()
    $ main_ui_begin_talk_state("Пес рядом", "dog")
    $ current_action_title = "Пес рядом"
    $ current_action_content = None
    $ _dog_picture = dog_talk_picture_path(_dog_room)
    $ scene_image = _dog_picture or None
    if _dog_picture:
        $ _layout_last_picture = _dog_picture
    $ MainTxt = dog_talk_intro_text(_dog_room)
    $ CurLocDesc = MainTxt
    call IntDogTalkRefresh(_dog_room)
    return


label IntDogTalkRefresh(room_code=""):
    $ ensure_dog_runtime()
    $ _dog_room = str(room_code or CurLoc or "").strip()
    $ main_ui_begin_talk_state("Пес рядом", "dog")
    $ current_action_title = "Пес рядом"
    $ current_action_content = None
    $ _dog_picture = dog_talk_picture_path(_dog_room)
    $ scene_image = _dog_picture or None
    if _dog_picture:
        $ _layout_last_picture = _dog_picture
    $ current_action_items = dog_main_ui_action_items(_dog_room, include_card=True)
    return


label IntDogTalkApply(room_code="", choice_code=""):
    $ ensure_dog_runtime()
    if str(choice_code or "") == "call_stray":
        $ dog.meet_stray()
        $ MainTxt = "Вы осторожно зовете пса. Он сперва пятится, потом все же подходит ближе, смотрит вам прямо в глаза и нервно играет хвостом. Теперь можно попробовать его погладить, поиграть с ним или дать кость."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "stray_bone":
        if dog.feed_stray_bone():
            $ MainTxt = "Вы протягиваете псу кость. Он долго принюхивается, хватает угощение и отходит всего на шаг, уже не убегая. Теперь с ним можно попробовать поиграть."
        else:
            $ MainTxt = "У вас нет подходящей кости. Пес видит пустые руки и снова настораживается."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "adopt":
        call IntDogAdoptNameMenu(room_code)
        return

    if str(choice_code or "").startswith("adopt_name:"):
        $ _dog_chosen_name = str(choice_code or "").split(":", 1)[1]
        if dog.adopt(_dog_chosen_name):
            $ MainTxt = "Вы надеваете на пса ошейник. Он не вырывается, только тяжело сопит и смотрит на вас снизу вверх. Теперь это ваш пес. Вы решаете звать его [dog.name]."
        else:
            $ MainTxt = "Пес еще не готов идти с вами. Нужно дать ему кость, поиграть с ним и иметь при себе ошейник."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "pet_stray":
        if dog.owned:
            $ MainTxt = "Пес охотно подставляет голову под вашу ладонь."
        elif dog.pet_stray():
            $ MainTxt = "Вы осторожно гладите пса по голове. Он напрягается, но не кусает, а потом даже коротко тычется мордой в вашу ладонь."
        else:
            $ _dog_bite_health = dog_stray_bite_player()
            $ MainTxt = "Вы тянете руку к настороженному псу, но он дергается вперед и больно прихватывает вас за пальцы. Без доверия так к нему лучше не лезть. Возможно, сначала стоит дать ему кость. Пес отскакивает и скрывается: придется встретить его в другой раз.\n\nЗдоровье: [_dog_bite_health] / 100"
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "play_stray":
        if dog.play_stray():
            $ fun = _player_clamp(fun + 4, 0, 100)
            $ MainTxt = "Вы бросаете псу палку и осторожно играете с ним, не делая резких движений. После кости он уже готов подыграть, а в конце даже сам подбегает ближе.\n\nТеперь, если у вас есть ошейник, можно забрать его домой."
        else:
            $ _dog_bite_health = dog_stray_bite_player()
            $ MainTxt = "Вы пытаетесь играть с псом без угощения, но он принимает движение за угрозу, огрызается и кусает вас. Пес тут же убегает. Возможно, сначала стоит дать ему кость.\n\nЗдоровье: [_dog_bite_health] / 100"
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "play":
        if dog.play():
            $ fun = _player_clamp(fun + 8, 0, 100)
            $ MainTxt = "Вы валяетесь с псом в траве, бросаете ему палку и даете вдоволь набегаться. После такой игры он выглядит заметно веселее и доверчивее.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
        else:
            $ MainTxt = "Сегодня пес уже наигрался. Лучше дать ему отдохнуть до завтра."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "train":
        if dog.train():
            $ MainTxt = "Вы несколько раз подзываете пса, приучаете его держаться рядом и слушать ваш голос. Пес старается изо всех сил и явно схватывает на лету.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
        else:
            $ MainTxt = "Сегодня вы уже занимались дрессировкой. Новые команды лучше закреплять завтра."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "bone":
        if dog.feed_bone(training=False):
            $ MainTxt = "Пес довольно устраивается рядом и с явным удовольствием принимается за кость.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]"
        else:
            $ MainTxt = "У вас нет подходящей кости."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "train_bone":
        if dog.feed_bone(training=True):
            $ MainTxt = "Вы закрепляете удачную дрессировку наградой. Пес мгновенно понимает, за что именно вы его хвалите.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
        else:
            $ MainTxt = "У вас нет подходящей кости."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "").startswith("household_walk:"):
        $ _dog_household = str(choice_code or "").split(":", 1)[1]
        $ _dog_name = _action_display_name(_dog_household)
        $ dog.gain_loyalty(1)
        $ dog.training_progress += 1
        $ dog.try_level_up()
        $ Friends[_dog_household] = min(20, int(Friends.get(_dog_household, 0) or 0) + 1)
        if int(effective_player_exploration() or 0) >= 50:
            $ exploration = max(0, int(exploration or 0) + 1)
            $ MainTxt = "%s с удовольствием забирает пса на прогулку. Судя по шерсти в репьях и сырой земле на лапах, они успели добраться до лесной опушки и там вдоволь набегаться. Пес становится еще послушнее, а %s явно рада, что вы доверили ей такое дело." % (_dog_name, _dog_name)
        else:
            $ MainTxt = "%s охотно берет пса и идет с ним гулять вокруг трактира и двора. Оба возвращаются заметно довольнее, а пес после такой прогулки смотрит на вас и на %s с еще большим доверием." % (_dog_name, _dog_name)
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "hunt":
        $ dog.in_company = True
        $ player_state().add_party_member("dog")
        $ npc_daily_schedule_build_all(True)
        $ dog_sync_profile()
        $ MainTxt = "Теперь пес идет вместе с вами и будет считаться спутником в охотничьих и боевых событиях."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "stay":
        $ dog.in_company = False
        $ player_state().remove_party_member("dog")
        if dog.booth_built:
            $ MainTxt = "Вы оставляете пса сторожить дом и двор. Он послушно устраивается у будки и принимается внимательно следить за всем вокруг."
        else:
            $ MainTxt = "Вы решаете пока оставить пса дома."
        $ npc_daily_schedule_build_all(True)
        $ dog_sync_profile()
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    $ main_ui_end_talk_state()
    return


label IntDogAdoptNameMenu(room_code=""):
    $ ensure_dog_runtime()
    $ _dog_room = str(room_code or CurLoc or "").strip()
    $ main_ui_begin_talk_state("Как назвать пса", "dog")
    $ current_action_title = "Как назвать пса"
    $ current_action_content = None
    $ MainTxt = "Пес уже готов идти с вами. Осталось надеть ошейник и выбрать кличку."
    $ CurLocDesc = MainTxt
    $ current_action_items = []
    python:
        for _dog_name_option in dog_name_options():
            current_action_items.append(MenuItem(str(_dog_name_option), Call("IntDogTalkApply", _dog_room, "adopt_name:" + str(_dog_name_option))))
        current_action_items.append(MenuItem("Назад", Call("IntDogTalkRefresh", _dog_room)))
    return


label DogTrainingMenu:
    $ ensure_dog_runtime()
    if not dog.owned:
        "У вас нет собаки."
        return

    menu:
        "Поиграть с псом":
            $ dog.play()
            "Вы проводите некоторое время, играя и дрессируя пса."
            "Лояльность: [dog.loyalty] / [dog.max_loyalty]"
            "Прогресс дрессировки: [dog.training_progress] / 5"

        "Дать кость во время дрессировки" if player_has_bone():
            $ dog.feed_bone(training=True)
            "Вы награждаете пса во время дрессировки."
            "Лояльность: [dog.loyalty] / [dog.max_loyalty]"
            "Прогресс дрессировки: [dog.training_progress] / 5"

        "Дать кость" if player_has_bone():
            $ dog.feed_bone(training=False)
            "Пес довольно грызет кость."
            "Лояльность: [dog.loyalty] / [dog.max_loyalty]"

        "Назад":
            return


screen dog_card_overlay(return_label=""):
    zorder 120

    $ _title = dog_card_title()
    $ _portrait = dog_card_portrait_path()
    $ _lines = dog_card_lines()
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24
    $ _portrait_w = 180
    $ _portrait_h = 240

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add im.Scale("images/rpg_message_bg.png", _left_w, _left_h)

        viewport:
            xpos 28
            ypos 24
            xsize _left_w - 56
            ysize _left_h - 48
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                hbox:
                    spacing 12
                    add im.Scale(_portrait, _portrait_w, _portrait_h)
                    vbox:
                        spacing 3
                        text "Уровень: [dog.level]" size 18 color "#1e130c"
                        text "Лояльность: [dog.loyalty] / [dog.max_loyalty]" size 18 color "#1e130c"
                        text "Здоровье: [dog.health] / [dog.max_health]" size 18 color "#1e130c"
                        text "Навык: [dog.skill_name]" size 18 color "#1e130c"

                for _line in _lines:
                    text _line size 16 color "#2d1d12"

                textbutton "Назад":
                    text_size 22
                    if str(return_label or "") == "__return__":
                        action Return()
                    else:
                        action Call("HideDogCard", return_label)


label DogBackyardBuildBooth:
    $ ensure_dog_runtime()
    if dog.booth_built:
        $ MainTxt = "Во дворе уже стоит собачья будка."
        $ CurLocDesc = MainTxt
        if str(CurLoc or "") == "Backyard":
            call BackyardBuildActions
        else:
            call StolyarWorkshopBuildActions
        return
    if int(money or 0) < 100:
        $ MainTxt = "У вас не хватает денег на собачью будку."
        $ CurLocDesc = MainTxt
        if str(CurLoc or "") == "Backyard":
            call BackyardBuildActions
        else:
            call StolyarWorkshopBuildActions
        return
    $ dog.build_booth()
    $ npc_daily_schedule_build_all(True)
    $ dog_sync_profile()
    $ DraupnirVar["DogBoothAsked"] = 0
    $ MainTxt = "Вы платите мастеру Драупниру 100 мараведи, и вскоре во дворе появляется крепкая собачья будка."
    $ CurLocDesc = MainTxt
    if str(CurLoc or "") == "Backyard":
        call BackyardBuildActions
    else:
        call StolyarWorkshopBuildActions
    return


label HorseTheftEvent:
    $ ensure_dog_runtime()
    if dog.prevents_theft("horse"):
        $ _dog_theft_result = dog_catch_delinquent_apply("horse")
        "[_dog_theft_result['text']]"
        return

    "Вор уводит лошадь."
    return


default dog = DogCompanion()
