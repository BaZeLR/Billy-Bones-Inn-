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
            self.spawn_location = random.choice(DOG_SPAWN_LOCATIONS)

        def is_here(self, room_code, day_number, time_slot):
            if self.owned:
                return False
            if int(time_slot or 0) != 3:
                return False
            return int(self.spawn_day or -1) == int(day_number or 0) and str(self.spawn_location or "") == str(room_code or "")

        def tame(self):
            if self.owned:
                return False
            if not player_has_bone():
                return False
            if not player_remove_bone():
                return False

            self.met = True
            self.owned = True
            self.in_company = True
            self.bones_given += 1
            self.health = self.max_health
            self.gain_loyalty(1)
            if "dog" not in list(player_company or []):
                player_company.append("dog")
            if "dog" not in list(company_list or []):
                company_list.append("dog")
            self.spawn_location = None
            return True

        def play(self):
            if not self.owned:
                return False
            self.play_sessions += 1
            self.training_progress += 1
            self.gain_loyalty(2)
            self.try_level_up()
            return True

        def feed_bone(self, training=False):
            if not self.owned:
                return False
            if not player_has_bone():
                return False
            if not player_remove_bone():
                return False

            self.bones_given += 1
            self.gain_loyalty(1)
            if bool(training):
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

    def ensure_dog_runtime():
        global dog
        if isinstance(dog, DogCompanion):
            return dog
        dog = DogCompanion()
        return dog

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

    def dog_prepare_current_spawn():
        ensure_dog_runtime().prepare_evening_spawn(int(dayspassed or 0), int(time or 0))

    def dog_is_here(room_code=""):
        return ensure_dog_runtime().is_here(str(room_code or ""), int(dayspassed or 0), int(time or 0))

    def dog_is_available_here(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        d = ensure_dog_runtime()
        if dog_is_here(room_key):
            return True
        if d.owned and (not bool(d.in_company)) and bool(d.booth_built) and room_key == "Backyard":
            return True
        if d.owned and (not bool(d.in_company)) and (not bool(d.booth_built)) and room_key in ("Backyard", "TavernMyRoom"):
            return True
        if d.owned and d.in_company and room_key.startswith("Forest"):
            return True
        return False

    def dog_can_guard_tavern():
        d = ensure_dog_runtime()
        return bool(d.owned) and (not bool(d.in_company)) and bool(d.is_alive())

    def dog_card_title():
        return str(ensure_dog_runtime().name or "Пес")

    def dog_display_name():
        d = ensure_dog_runtime()
        if d.owned:
            return str(d.name or "Пес")
        return "Бродячий пес"

    def dog_card_portrait_path():
        d = ensure_dog_runtime()
        if not d.owned:
            return "images/tavern/myroom/no_colar.png"
        if d.booth_built:
            return "images/tavern/myroom/dog_booth.png"
        return "images/tavern/myroom/dog.png"

    def dog_card_stat_rows():
        d = ensure_dog_runtime()
        return [
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
        if not d.owned:
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
        if not d.owned:
            return "images/tavern/myroom/no_colar.png"
        if bool(d.booth_built) and (not bool(d.in_company)) and room_key.startswith("Backyard"):
            return "images/tavern/myroom/dog_booth.png"
        return "images/tavern/myroom/dog.png"

    def dog_talk_intro_text(room_code=""):
        d = ensure_dog_runtime()
        room_key = str(room_code or CurLoc or "").strip()
        if not d.owned:
            return "Небольшой, но крепкий бродячий пес держится настороженно, однако уже не шарахается от людей и явно присматривается к вам."
        if bool(d.booth_built) and (not bool(d.in_company)) and room_key.startswith("Backyard"):
            return "Пес выглядывает из своей будки, шевелит ушами и сразу узнает вас. Увидев хозяина, он оживляется и ждет, что вы ему прикажете."
        if bool(d.in_company) and room_key.startswith("Forest"):
            return "Пес держится рядом с вами, постоянно принюхивается к лесу и готов сорваться вперед по вашему знаку."
        return "Пес сразу оживляется при вашем появлении, настораживает уши и внимательно следит, что вы собираетесь делать."

    def show_dog_card_main_ui_state():
        import renpy as renpy_pkg
        store = renpy_pkg.store
        store.UI_mode = "dog"
        store.UI_selected_char = "dog"
        store.current_action_title = dog_card_title()
        store.current_action_content = None
        store.current_action_items = []
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def dog_room_action_caption(room_code=""):
        d = ensure_dog_runtime()
        room_key = str(room_code or CurLoc or "")
        if d.owned and bool(d.booth_built) and (not bool(d.in_company)) and room_key == "Backyard":
            return "Позвать пса из будки"
        if d.owned and room_key in ("Backyard", "TavernMyRoom"):
            return "Пес"
        if d.owned and d.in_company and str(room_code or CurLoc or "").startswith("Forest"):
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
                if not _tavern_is_in_room(npc_id, room_key):
                    continue
            except Exception:
                continue
            candidates.append(npc_id)
        return candidates


label ShowDogCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ show_dog_card_main_ui_state()
        return
    show screen dog_card_overlay(return_label)
    return


label HideDogCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ main_ui_restore_room_scene_state()
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
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(show_dog_card_main_ui_state)))
    if not dog.owned:
        if player_has_bone():
            $ current_action_items.append(MenuItem("Приучить пса к себе", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "tame")))
    else:
        $ current_action_items.append(MenuItem("Поиграть с псом", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "play")))
        $ current_action_items.append(MenuItem("Позаниматься дрессировкой", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "train")))
        if player_has_bone():
            $ current_action_items.append(MenuItem("Угостить пса костью", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "bone")))
            $ current_action_items.append(MenuItem("Наградить костью за дрессировку", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "train_bone")))
        if dog.in_company:
            $ current_action_items.append(MenuItem("Оставить сторожить дом", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "stay")))
        else:
            $ current_action_items.append(MenuItem("Взять пса на охоту", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "hunt")))
            if dog.booth_built and _dog_room.startswith("Backyard"):
                $ current_action_items.append(MenuItem("Оставить сторожить дом", Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "stay")))
            python:
                for _dog_household in dog_household_walk_candidates(_dog_room):
                    current_action_items.append(MenuItem("Попросить %s погулять с псом" % _action_display_name(_dog_household), Function(main_ui_call_label, "IntDogTalkApply", _dog_room, "household_walk:" + str(_dog_household))))
    $ current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
    return


label IntDogTalkApply(room_code="", choice_code=""):
    $ ensure_dog_runtime()
    if str(choice_code or "") == "tame":
        if dog.tame():
            $ MainTxt = "Вы осторожно подманиваете пса костью и не делаете резких движений. Он долго принюхивается, берет угощение и, поколебавшись, все-таки остается рядом. Похоже, теперь пес признал в вас хозяина."
        else:
            $ MainTxt = "Без угощения пес пока не решается довериться вам."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "play":
        if dog.play():
            $ fun = _player_clamp(fun + 8, 0, 100)
            $ MainTxt = "Вы валяетесь с псом в траве, бросаете ему палку и даете вдоволь набегаться. После такой игры он выглядит заметно веселее и доверчивее.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
        else:
            $ MainTxt = "Сейчас играть не с кем."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "train":
        if dog.play():
            $ MainTxt = "Вы несколько раз подзываете пса, приучаете его держаться рядом и слушать ваш голос. Пес старается изо всех сил и явно схватывает на лету.\n\nЛояльность: [dog.loyalty] / [dog.max_loyalty]\nПрогресс дрессировки: [dog.training_progress] / 5"
        else:
            $ MainTxt = "Сейчас дрессировать некого."
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
        if "dog" not in list(player_company or []):
            $ player_company.append("dog")
        if "dog" not in list(company_list or []):
            $ company_list.append("dog")
        $ MainTxt = "Теперь пес идет вместе с вами и будет считаться спутником в охотничьих и боевых событиях."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    if str(choice_code or "") == "stay":
        $ dog.in_company = False
        if "dog" in list(player_company or []):
            python:
                try:
                    player_company.remove("dog")
                except ValueError:
                    pass
        if "dog" in list(company_list or []):
            python:
                try:
                    company_list.remove("dog")
                except ValueError:
                    pass
        if dog.booth_built:
            $ MainTxt = "Вы оставляете пса сторожить дом и двор. Он послушно устраивается у будки и принимается внимательно следить за всем вокруг."
        else:
            $ MainTxt = "Вы решаете пока оставить пса дома."
        $ CurLocDesc = MainTxt
        call IntDogTalkRefresh(room_code)
        return

    $ main_ui_end_talk_state()
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
