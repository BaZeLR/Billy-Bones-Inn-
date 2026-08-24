# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init -5 python:
    import renpy.exports as renpy_module

    class DogData(PeopleData):
        code_name = "dog"
        stray_roam_locations = (
            "PortStreets",
            "MarketPlace",
            "ArtisansQuarter",
            "StreetTavern",
        )

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Пес",
                fullname="Пес",
                genitive="Пса",
                dative="Псу",
                portrait="images/dog/no_colar.png",
                default_location="",
                description="Пес может быть бродячим или вашим спутником, если вы его приручили.",
            )

    class DogCompanion(BaseNPC):
        def __init__(self):
            super().__init__("dog")
            self.met = False
            self.owned = False
            self.pet_name = "Пес"

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

            self.stray_hidden_day = -1

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
        def speed(self):
            return 2

        @property
        def skill_name(self):
            if int(self.level or 0) >= 2:
                return "Мертвая хватка"
            return "Укус"

        def clamp_health(self):
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

        def getLocation(self, wday=None, hour=None):
            if self.owned and "dog" in player.combat.party and self.is_alive():
                return str(rooms.current_code or "")
            return super(DogCompanion, self).getLocation(wday, hour)

        def is_stray_here(self, room_code=""):
            room_key = str(room_code or rooms.current_code or "").strip()
            return (not self.owned) and self.is_alive() and int(self.stray_hidden_day or -1) != current_game_day() and str(self.getLocation() or "") == room_key

        def is_available_here(self, room_code=""):
            room_key = str(room_code or rooms.current_code or "").strip()
            return self.is_alive() and str(self.getLocation() or "") == room_key

        def action_data(self, where_id=""):
            room_code = str(where_id or rooms.current_code or "").strip()
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
            chosen_name = str(dog_name or "").strip()
            self.pet_name = chosen_name if chosen_name in dog_name_options() else dog_random_name()
            self.health = self.max_health
            self.gain_loyalty(3)
            player.add_party_member("dog")
            DogStaticData.invalidate_daily_schedule()
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
            if int(self.last_play_day or -1) == current_game_day():
                return False
            self.met = True
            self.stray_played = True
            self.last_play_day = current_game_day()
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
            if int(self.last_play_day or -1) == current_game_day():
                return False
            self.last_play_day = current_game_day()
            self.play_sessions += 1
            self.training_progress += 1
            self.gain_loyalty(2)
            self.try_level_up()
            return True

        def train(self):
            if not self.owned:
                return False
            if int(self.last_train_day or -1) == current_game_day():
                return False
            self.last_train_day = current_game_day()
            self.training_progress += 1
            self.gain_loyalty(1)
            self.try_level_up()
            return True

        def feed_bone(self, training=False):
            if not self.owned:
                return False
            if not player_has_bone():
                return False
            if bool(training) and int(self.last_train_day or -1) == current_game_day():
                return False
            if not player_remove_bone():
                return False

            self.bones_given += 1
            self.gain_loyalty(1)
            if bool(training):
                self.last_train_day = current_game_day()
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
            self.clamp_health()

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

    def dog_random_name():
        return procedural_choice(dog_name_options(), "dog_name_%s" % current_game_day())

    def dog_name_options():
        return ("Sharik", "Tresor", "Bobick", "Muchtar", "Drool")

    def player_has_bone():
        try:
            return player.item_count("dog_bone_001") > 0
        except Exception:
            return False

    def player_remove_bone():
        try:
            return bool(player.remove_item("dog_bone_001", 1))
        except Exception:
            return False

    def player_has_dog_collar():
        try:
            return player.item_count("dog_collar_001") > 0
        except Exception:
            return False

    def player_remove_dog_collar():
        try:
            return bool(player.remove_item("dog_collar_001", 1))
        except Exception:
            return False

    def dog_can_adopt_stray():
        d = dog
        return (not bool(d.owned)) and int(d.bones_given or 0) > 0 and bool(d.stray_played) and player_has_dog_collar()

    def dog_stray_bite_player():
        player.change_stat("health", -5)
        d = dog
        d.stray_hidden_day = current_game_day()
        d.met = False
        DogStaticData.invalidate_daily_schedule()
        return int(player.condition.health or 0)

    def dog_stray_roam_active():
        d = dog
        return (not bool(d.owned)) and d.is_alive() and int(d.stray_hidden_day or -1) != current_game_day()

    def dog_home_roam_active():
        d = dog
        return bool(d.owned) and "dog" not in player.combat.party and bool(d.is_alive())

    def dog_can_guard_tavern():
        d = dog
        return bool(d.owned) and "dog" not in player.combat.party and bool(d.is_alive())

    def dog_card_title():
        return str(dog.pet_name or "Пес")

    def dog_display_name():
        d = dog
        if d.state_key == "adopted":
            return str(d.pet_name or "Пес")
        return "Бродячий пес"

    def dog_card_portrait_path():
        d = dog
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
        d = dog
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
        d = dog
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
        lines.append("В компании: %s." % ("да" if "dog" in player.combat.party else "нет"))
        if d.can_haul:
            lines.append("Пес уже достаточно к вам привязался и может помогать таскать вещи.")
        return lines

    def dog_talk_picture_path(room_code=""):
        d = dog
        room_key = str(room_code or rooms.current_code or "").strip()
        if d.state_key == "stray":
            return dog_card_portrait_path()
        if bool(d.booth_built) and "dog" not in player.combat.party and room_key == "Backyard":
            return dog_card_portrait_path()
        if "dog" in player.combat.party and room_in_group(room_key, ROOM_GROUP_FOREST) and renpy_module.loadable("images/dog/dog.png"):
            return "images/dog/dog.png"
        return dog_card_portrait_path()

    def dog_talk_intro_text(room_code=""):
        d = dog
        room_key = str(room_code or rooms.current_code or "").strip()
        if d.state_key == "stray":
            if not bool(d.met):
                return "Небольшой, но крепкий бродячий пес держится настороженно и смотрит на вас издалека. Его можно осторожно позвать, но без кости он может не довериться."
            if int(d.bones_given or 0) <= 0:
                return "Пес подошел ближе, смотрит вам в глаза и нервно виляет хвостом. Голыми руками лучше не лезть: возможно, сначала стоит дать ему кость."
            if not bool(d.stray_played):
                return "Пес уже взял вашу кость и держится рядом спокойнее. Теперь можно попробовать поиграть с ним и понять, готов ли он довериться."
            return "Бродячий пес уже узнает вас, помахивает хвостом и ждет, что вы сделаете дальше. Для дома ему нужен ошейник."
        if bool(d.booth_built) and "dog" not in player.combat.party and room_key == "Backyard":
            return "Пес выглядывает из своей будки, шевелит ушами и сразу узнает вас. Увидев хозяина, он оживляется и ждет, что вы ему прикажете."
        if "dog" in player.combat.party and room_in_group(room_key, ROOM_GROUP_FOREST):
            return "Пес держится рядом с вами, постоянно принюхивается к лесу и готов сорваться вперед по вашему знаку."
        return "Пес сразу оживляется при вашем появлении, настораживает уши и внимательно следит, что вы собираетесь делать."

    def dog_room_action_caption(room_code=""):
        d = dog
        room_key = str(room_code or rooms.current_code or "").strip()
        if d.owned and bool(d.booth_built) and "dog" not in player.combat.party and room_key == "Backyard":
            return "Позвать пса из будки"
        if (not bool(d.owned)) and d.is_stray_here(room_key):
            return "Подозвать бродячего пса"
        if d.owned and str(people.location("dog") or "") == room_key:
            return "Пес"
        if d.owned and "dog" in player.combat.party and room_in_group(str(room_code or rooms.current_code or ""), ROOM_GROUP_FOREST):
            return "Пес"
        return "Подозвать пса"

    def dog_household_walk_candidates(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        d = dog
        if not d.owned or "dog" in player.combat.party:
            return []
        candidates = []
        for npc_id in ("sandra", "melissa", "amanda"):
            npc_info = people.get_info(npc_id)
            if int(getattr(npc_info, "rel", 0) or 0) < 15:
                continue
            try:
                if str(people.location(npc_id) or "") != room_key:
                    continue
            except Exception:
                continue
            candidates.append(npc_id)
        return candidates


init 2 python:
    DogStaticData.set_daily_schedule(
        default_intervals=[
            dict(npc_daily_schedule_interval(16, 18, "Backyard", True, True, "sleep_by_booth"), condition=dog_home_roam_active),
        ],
        random_intervals=[
            npc_daily_schedule_random_interval(
                13, 16,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="stray_city_roam",
                choices=[npc_daily_schedule_choice(room_code, 1, True, True, "stray_%s" % room_code.lower(), condition=dog_stray_roam_active) for room_code in DogStaticData.stray_roam_locations],
            ),
            npc_daily_schedule_random_interval(
                6, 8,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="morning_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 4, True, True, "yard_watch", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernKitchen", 2, True, True, "kitchen_smells", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernStable", 2, True, True, "stable_watch", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernStorage", 1, True, True, "rat_smells", condition=dog_home_roam_active),
                ],
            ),
            npc_daily_schedule_random_interval(
                8, 11,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="noon_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 3, True, True, "yard_roam", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernMain", 2, True, True, "main_hall_watch", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernStable", 2, True, True, "stable_watch", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernMyRoom", 1, True, True, "player_room_door", condition=dog_home_roam_active),
                ],
            ),
            npc_daily_schedule_random_interval(
                11, 13,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="day_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 4, True, True, "yard_guard", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernStable", 3, True, True, "stable_guard", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernStorage", 1, True, True, "storage_guard", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernMain", 1, True, True, "hall_guard", condition=dog_home_roam_active),
                ],
            ),
            npc_daily_schedule_random_interval(
                13, 16,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="evening_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 4, True, True, "evening_yard", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernMain", 2, True, True, "evening_hall", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernStable", 2, True, True, "evening_stable", condition=dog_home_roam_active),
                    npc_daily_schedule_choice("TavernKitchen", 1, True, True, "evening_kitchen", condition=dog_home_roam_active),
                ],
            ),
        ],
    )


label ShowDogCard(return_label=""):
    $ renpy.dynamic("_dog_card_picture")
    $ main_ui_begin_card_state()
    $ _dog_card_picture = dog_card_portrait_path()
    if str(_dog_card_picture or "").strip():
        vscene _dog_card_picture
    $ scene_runtime.text = "\n".join(dog_card_lines())
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ main_ui_end_card_state()
    return


label HideDogCard(return_label=""):
    return


label IntDogTalk(room_code=""):
    $ renpy.dynamic("_dog_household", "_dog_name", "_dog_bite_health", "_dog_room", "_dog_picture", "_dog_chosen_name")
    $ _dog_room = str(room_code or rooms.current_code or "").strip()
    $ main_ui_begin_talk_state("Пес рядом", "dog")
    $ _dog_picture = dog_talk_picture_path(_dog_room)
    if str(_dog_picture or "").strip():
        vscene _dog_picture
    $ scene_runtime.text = dog_talk_intro_text(_dog_room)
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    while True:
        "[scene_runtime.text]"
        menu:
            "Осмотреть":
                call ShowDogCard
                $ scene_runtime.text = dog_talk_intro_text(_dog_room)
                $ scene_runtime.location_text = scene_runtime.text

            "Позвать пса" if dog.state_key == "stray" and not bool(dog.met):
                $ dog.meet_stray()
                $ scene_runtime.text = "Вы осторожно зовете пса. Он сперва пятится, потом все же подходит ближе, смотрит вам прямо в глаза и нервно играет хвостом. Теперь можно попробовать его погладить, поиграть с ним или дать кость."
                $ scene_runtime.location_text = scene_runtime.text

            "Попробовать погладить" if dog.state_key == "stray" and bool(dog.met):
                if dog.owned:
                    $ scene_runtime.text = "Пес охотно подставляет голову под вашу ладонь."
                elif dog.pet_stray():
                    $ scene_runtime.text = "Вы осторожно гладите пса по голове. Он напрягается, но не кусает, а потом даже коротко тычется мордой в вашу ладонь."
                else:
                    $ _dog_bite_health = dog_stray_bite_player()
                    $ scene_runtime.text = "Вы тянете руку к настороженному псу, но он дергается вперед и больно прихватывает вас за пальцы. Без доверия так к нему лучше не лезть. Возможно, сначала стоит дать ему кость. Пес отскакивает и скрывается: придется встретить его в другой раз.\n\nЗдоровье: %d / 100" % int(_dog_bite_health)
                $ scene_runtime.location_text = scene_runtime.text

            "Попробовать поиграть" if dog.state_key == "stray" and bool(dog.met):
                if dog.play_stray():
                    $ player.change_stat("fun", 4)
                    $ scene_runtime.text = "Вы бросаете псу палку и осторожно играете с ним, не делая резких движений. После кости он уже готов подыграть, а в конце даже сам подбегает ближе.\n\nТеперь, если у вас есть ошейник, можно забрать его домой."
                else:
                    $ _dog_bite_health = dog_stray_bite_player()
                    $ scene_runtime.text = "Вы пытаетесь играть с псом без угощения, но он принимает движение за угрозу, огрызается и кусает вас. Пес тут же убегает. Возможно, сначала стоит дать ему кость.\n\nЗдоровье: %d / 100" % int(_dog_bite_health)
                $ scene_runtime.location_text = scene_runtime.text

            "Дать кость" if dog.state_key == "stray" and bool(dog.met) and player_has_bone():
                if dog.feed_stray_bone():
                    $ scene_runtime.text = "Вы протягиваете псу кость. Он долго принюхивается, хватает угощение и отходит всего на шаг, уже не убегая. Теперь с ним можно попробовать поиграть."
                else:
                    $ scene_runtime.text = "У вас нет подходящей кости. Пес видит пустые руки и снова настораживается."
                $ scene_runtime.location_text = scene_runtime.text

            "Надеть ошейник и забрать домой" if dog.state_key == "stray" and dog_can_adopt_stray():
                call IntDogAdoptNameMenu(_dog_room)
                $ _dog_chosen_name = str(_return or "")
                if _dog_chosen_name and dog.adopt(_dog_chosen_name):
                    $ scene_runtime.text = "Вы надеваете на пса ошейник. Он не вырывается, только тяжело сопит и смотрит на вас снизу вверх. Теперь это ваш пес. Вы решаете звать его [dog.pet_name]."
                elif _dog_chosen_name:
                    $ scene_runtime.text = "Пес еще не готов идти с вами. Нужно дать ему кость, поиграть с ним и иметь при себе ошейник."
                $ scene_runtime.location_text = scene_runtime.text

            "Поиграть с псом" if dog.state_key != "stray" and int(dog.last_play_day or -1) != current_game_day():
                if dog.play():
                    $ player.change_stat("fun", 8)
                    $ scene_runtime.text = "Вы валяетесь с псом в траве, бросаете ему палку и даете вдоволь набегаться. После такой игры он выглядит заметно веселее и доверчивее.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
                else:
                    $ scene_runtime.text = "Сегодня пес уже наигрался. Лучше дать ему отдохнуть до завтра."
                $ scene_runtime.location_text = scene_runtime.text

            "Позаниматься дрессировкой" if dog.state_key != "stray" and int(dog.last_train_day or -1) != current_game_day():
                if dog.train():
                    $ scene_runtime.text = "Вы несколько раз подзываете пса, приучаете его держаться рядом и слушать ваш голос. Пес старается изо всех сил и явно схватывает на лету.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
                else:
                    $ scene_runtime.text = "Сегодня вы уже занимались дрессировкой. Новые команды лучше закреплять завтра."
                $ scene_runtime.location_text = scene_runtime.text

            "Угостить пса костью" if dog.state_key != "stray" and player_has_bone():
                if dog.feed_bone(training=False):
                    $ scene_runtime.text = "Пес довольно устраивается рядом и с явным удовольствием принимается за кость.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]"
                else:
                    $ scene_runtime.text = "У вас нет подходящей кости."
                $ scene_runtime.location_text = scene_runtime.text

            "Наградить костью за дрессировку" if dog.state_key != "stray" and player_has_bone():
                if dog.feed_bone(training=True):
                    $ scene_runtime.text = "Вы закрепляете удачную дрессировку наградой. Пес мгновенно понимает, за что именно вы его хвалите.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
                else:
                    $ scene_runtime.text = "У вас нет подходящей кости."
                $ scene_runtime.location_text = scene_runtime.text

            "Взять пса на охоту" if dog.state_key != "stray" and "dog" not in player.combat.party:
                $ player.add_party_member("dog")
                $ DogStaticData.invalidate_daily_schedule()
                $ scene_runtime.text = "Теперь пес идет вместе с вами и будет считаться спутником в охотничьих и боевых событиях."
                $ scene_runtime.location_text = scene_runtime.text

            "Оставить сторожить дом" if dog.state_key != "stray" and ("dog" in player.combat.party or (dog.booth_built and _dog_room.startswith("Backyard"))):
                $ player.remove_party_member("dog")
                if dog.booth_built:
                    $ scene_runtime.text = "Вы оставляете пса сторожить дом и двор. Он послушно устраивается у будки и принимается внимательно следить за всем вокруг."
                else:
                    $ scene_runtime.text = "Вы решаете пока оставить пса дома."
                $ DogStaticData.invalidate_daily_schedule()
                $ scene_runtime.location_text = scene_runtime.text

            "Попросить Сандру погулять с псом" if "sandra" in dog_household_walk_candidates(_dog_room):
                $ _dog_household = "sandra"
                $ _dog_name = _action_display_name(_dog_household)
                $ dog.gain_loyalty(1)
                $ dog.training_progress += 1
                $ dog.try_level_up()
                $ people.get_info(_dog_household).change_social(friend_delta=1)
                $ scene_runtime.text = "%s охотно берет пса и идет с ним гулять. Оба возвращаются заметно довольнее, а пес смотрит на вас и на %s с еще большим доверием." % (_dog_name, _dog_name)
                $ scene_runtime.location_text = scene_runtime.text

            "Попросить Мелиссу погулять с псом" if "melissa" in dog_household_walk_candidates(_dog_room):
                $ _dog_household = "melissa"
                $ _dog_name = _action_display_name(_dog_household)
                $ dog.gain_loyalty(1)
                $ dog.training_progress += 1
                $ dog.try_level_up()
                $ people.get_info(_dog_household).change_social(friend_delta=1)
                $ scene_runtime.text = "%s охотно берет пса и идет с ним гулять. Оба возвращаются заметно довольнее, а пес смотрит на вас и на %s с еще большим доверием." % (_dog_name, _dog_name)
                $ scene_runtime.location_text = scene_runtime.text

            "Попросить Аманду погулять с псом" if "amanda" in dog_household_walk_candidates(_dog_room):
                $ _dog_household = "amanda"
                $ _dog_name = _action_display_name(_dog_household)
                $ dog.gain_loyalty(1)
                $ dog.training_progress += 1
                $ dog.try_level_up()
                $ people.get_info(_dog_household).change_social(friend_delta=1)
                $ scene_runtime.text = "%s охотно берет пса и идет с ним гулять. Оба возвращаются заметно довольнее, а пес смотрит на вас и на %s с еще большим доверием." % (_dog_name, _dog_name)
                $ scene_runtime.location_text = scene_runtime.text

            "Закончить разговор":
                $ main_ui_end_talk_state()
                return


label IntDogAdoptNameMenu(room_code=""):
    show screen main_ui
    "Пес уже готов идти с вами. Осталось надеть ошейник и выбрать кличку."
    menu:
        "Sharik":
            return "Sharik"
        "Tresor":
            return "Tresor"
        "Bobick":
            return "Bobick"
        "Muchtar":
            return "Muchtar"
        "Drool":
            return "Drool"
        "Назад":
            return ""


label DogTrainingMenu:
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

label DogBackyardBuildBooth:
    if dog.booth_built:
        $ scene_runtime.text = "Во дворе уже стоит собачья будка."
        $ scene_runtime.location_text = scene_runtime.text
        if str(rooms.current_code or "") == "Backyard":
            $ main_ui_runtime.action_items = backyard_action_items()
        return
    if int(player.economy.money or 0) < 100:
        $ scene_runtime.text = "У вас не хватает денег на собачью будку."
        $ scene_runtime.location_text = scene_runtime.text
        if str(rooms.current_code or "") == "Backyard":
            $ main_ui_runtime.action_items = backyard_action_items()
        return
    $ dog.build_booth()
    $ DogStaticData.invalidate_daily_schedule()
    $ Draupnir.dog_booth_quote_received = False
    $ scene_runtime.text = "Вы платите мастеру Драупниру 100 мараведи, и вскоре во дворе появляется крепкая собачья будка."
    $ scene_runtime.location_text = scene_runtime.text
    if str(rooms.current_code or "") == "Backyard":
        $ main_ui_runtime.action_items = backyard_action_items()
    return


label HorseTheftEvent:
    $ renpy.dynamic("_dog_theft_result")
    if dog.prevents_theft("horse"):
        $ _dog_theft_result = dog_catch_delinquent_apply("horse")
        "[_dog_theft_result['text']]"
        return

    "Вор уводит лошадь."
    return


define DogStaticData = DogData()
default dog = DogCompanion()

label InitDog:
    $ people.register(DogStaticData, dog)
    return
