# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -8 python:
    def werecat_story_defaults():
        return {
            "rats_problem_active": 1,
            "rat_breakfast_seen": 0,
            "adoption_breakfast_seen": 0,
            "woods_exploration": 0,
            "tracks_seen": 0,
            "tracks_first_text_seen": 0,
            "tracks_room": "",
            "trap_active": 0,
            "trap_room": "",
            "trap_day": -1,
            "trap_rooms": {},
            "caught": 0,
            "adopted": 0,
            "adopted_count": 0,
            "sold": 0,
            "gifted_clara": 0,
            "clara_gift_day": -1,
            "name": "",
            "adopted_day": -1,
            "first_month_thanks_day": -1,
            "hunter_tease_day": -1,
            "hunter_tease_offer_day": -1,
            "hunter_tease_offer_ready": 0,
            "rat_carcass_cached": 0,
            "rat_food_loss_next_day": 7,
        }

    def werecat_pet_defaults():
        return {
            "pet_day": -1,
            "milk_day": -1,
            "play_day": -1,
            "trust": 0,
            "comfort": 0,
        }

    def werecat_info():
        if "werecat" not in peopleData:
            peopleData["werecat"] = PeopleData(
                "werecat",
                cname="Кошка",
                fullname="Луна",
                genitive="Луны",
                dative="Луне",
                portrait="images/general/kitty.png",
                default_location="",
                description="Домовая кошка-оборотень, если она решила остаться при трактире.",
            )
        if "werecat" not in peopleInfo:
            peopleInfo["werecat"] = BaseNPC("werecat")
        info = peopleInfo["werecat"]
        info.data = peopleData["werecat"]
        if not isinstance(getattr(info, "var", None), dict):
            info.var = {}
        if not isinstance(getattr(info, "stats", None), dict):
            info.stats = {}
        for key, value in werecat_story_defaults().items():
            if key not in info.var:
                info.var[key] = dict(value) if isinstance(value, dict) else value
        for key, value in werecat_pet_defaults().items():
            if key not in info.stats:
                info.stats[key] = value
        return info

    def werecat_state():
        return werecat_info().var

    def werecat_pet_state():
        return werecat_info().stats

    def werecat_is_living_with_household():
        state = werecat_state()
        adopted_count = int(state.get("adopted_count", 0) or 0)
        if int(state.get("adopted", 0) or 0) == 1:
            adopted_count = max(1, adopted_count)
        return adopted_count >= 1 and int(state.get("sold", 0) or 0) == 0

    WERECAT_ROAM_ROOMS = {
        0: ("TavernKitchen", "TavernMain", "TavernStorage"),
        1: ("Backyard", "TavernKitchen", "TavernStorage"),
        2: ("Backyard", "TavernStorage", "TavernMelissaRoom", "TavernAmandaRoom"),
        3: ("TavernKitchen", "Backyard", "TavernStorage"),
        4: ("TavernMain", "TavernKitchen", "TavernStorage", "TavernMelissaRoom", "TavernAmandaRoom", "TavernSandraRoom", "TavernMyRoom", "Backyard"),
    }
    WERECAT_MILK_ITEM_IDS = ("milk_pitcher_001",)

    werecat_info()

    def werecat_sleep_location():
        return werecat_roam_location() or "Backyard"

    def werecat_roam_location():
        if not werecat_is_living_with_household():
            return ""
        slot_value = int(time or 0)
        rooms = list(WERECAT_ROAM_ROOMS.get(slot_value, WERECAT_ROAM_ROOMS.get(1, ("Backyard",))))
        if not rooms:
            return "Backyard"
        seed_value = int(dayspassed or 0) * 17 + int(day or 0) * 7 + int(month or 0) * 11 + int(week or 0) * 5 + slot_value * 13
        return str(rooms[seed_value % len(rooms)] or "Backyard")

    def werecat_roam_matches(location=""):
        return werecat_is_living_with_household() and str(werecat_roam_location() or "") == str(location or "")

    def werecat_schedule_tavern_kitchen():
        return werecat_roam_matches("TavernKitchen")

    def werecat_schedule_tavern_main():
        return werecat_roam_matches("TavernMain")

    def werecat_schedule_tavern_storage():
        return werecat_roam_matches("TavernStorage")

    def werecat_schedule_backyard():
        return werecat_roam_matches("Backyard")

    def werecat_schedule_melissa_room():
        return werecat_roam_matches("TavernMelissaRoom")

    def werecat_schedule_amanda_room():
        return werecat_roam_matches("TavernAmandaRoom")

    def werecat_schedule_sandra_room():
        return werecat_roam_matches("TavernSandraRoom")

    def werecat_schedule_player_room():
        return werecat_roam_matches("TavernMyRoom")

    WERECAT_ROAM_CONDITIONS = {
        "TavernKitchen": werecat_schedule_tavern_kitchen,
        "TavernMain": werecat_schedule_tavern_main,
        "TavernStorage": werecat_schedule_tavern_storage,
        "Backyard": werecat_schedule_backyard,
        "TavernMelissaRoom": werecat_schedule_melissa_room,
        "TavernAmandaRoom": werecat_schedule_amanda_room,
        "TavernSandraRoom": werecat_schedule_sandra_room,
        "TavernMyRoom": werecat_schedule_player_room,
    }

    def werecat_is_in_room(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if room_key == "" or not werecat_is_living_with_household():
            return False
        return str(getLocation("werecat") or "") == room_key

    def werecat_ambient_text(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        name_value = str(werecat_display_name() or "Кошка")
        seed_value = werecat_scene_seed()
        if room_key == "TavernKitchen":
            options = [
                "%s лакает блюдце молока у очага и временами довольно урчит." % name_value,
                "%s греется у кухонного тепла, лениво прикрыв глаза." % name_value,
                "%s бесшумно ходит между лавками и проверяет запахи у двери в кладовую." % name_value,
            ]
        elif room_key == "TavernMain":
            options = [
                "%s дремлет у камина, но одно ухо все равно поворачивается на каждый новый шаг." % name_value,
                "%s медленно проходит вдоль стены, изучая зал как свою новую территорию." % name_value,
                "%s устраивается возле теплых углей и тихо урчит." % name_value,
            ]
        elif room_key == "TavernStorage":
            options = [
                "%s сидит у мешков с припасами и слушает подпол. Крысам здесь теперь точно неуютно." % name_value,
                "%s исчезает между бочками и возвращается с деловым видом настоящей хозяйки кладовой." % name_value,
                "%s принюхивается к щелям у пола, будто снова почуяла мелкую добычу." % name_value,
            ]
        elif room_key == "Backyard":
            options = [
                "%s ходит по двору мягкими кругами и проверяет все укрытия." % name_value,
                "%s устроилась на солнце и аккуратно вылизывает шерсть." % name_value,
                "%s прислушивается к двору, готовая в любой миг сорваться с места." % name_value,
            ]
        elif room_key in ("TavernMelissaRoom", "TavernAmandaRoom", "TavernSandraRoom", "TavernMyRoom"):
            options = [
                "%s свернулась на свободном месте и делает вид, что крепко спит." % name_value,
                "%s лениво потягивается и умывается, не сводя с вас внимательных глаз." % name_value,
                "%s выбрала тихий угол комнаты и явно считает его подходящим логовом." % name_value,
            ]
        else:
            options = [
                "%s тихо сидит неподалеку, настороженно изучая все вокруг." % name_value,
                "%s мягко ступает по полу и время от времени урчит себе под нос." % name_value,
            ]
        return options[seed_value % len(options)]

    def werecat_visible_text(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if not room_key:
            return ""
        try:
            werecat_sync_profile()
        except Exception:
            pass
        if not werecat_is_in_room(room_key):
            return ""
        return str(werecat_ambient_text(room_key) or "")

    def werecat_append_visible_text(base_text="", room_code=""):
        result = str(base_text or "")
        visible_text = str(werecat_visible_text(room_code) or "").strip()
        if visible_text:
            if result.strip():
                return result + "\n\n" + visible_text
            return visible_text
        return result

    def werecat_can_play_with_dog(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if not werecat_is_in_room(room_key):
            return False
        try:
            d = ensure_dog_runtime()
        except Exception:
            return False
        if not bool(getattr(d, "owned", False)):
            return False
        return room_key in ("Backyard", "TavernMain", "TavernKitchen", "TavernStorage")

    def werecat_has_milk_available(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        for item_id in WERECAT_MILK_ITEM_IDS:
            try:
                if int(_player_item_count_by_id(item_id) or 0) > 0:
                    return True
            except Exception:
                pass
        if room_key in ("TavernKitchen", "TavernStorage", "TavernMain"):
            try:
                return int(tavern_kitchen_food_stock_count("milk_pitcher_001") or 0) > 0
            except Exception:
                return False
        return False

    def werecat_consume_milk(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        for item_id in WERECAT_MILK_ITEM_IDS:
            try:
                if int(_player_item_count_by_id(item_id) or 0) > 0:
                    return bool(_player_remove_item_by_id(item_id, 1))
            except Exception:
                pass
        if room_key in ("TavernKitchen", "TavernStorage", "TavernMain"):
            try:
                return int(tavern_kitchen_consume_stock_units(1, ["milk_pitcher_001"]) or 0) > 0
            except Exception:
                return False
        return False

    def werecat_reaction_text(action_code="", room_code=""):
        action_key = str(action_code or "").strip().lower()
        name_value = str(werecat_display_name() or "Кошка")
        seed_value = werecat_scene_seed() + len(action_key) * 3
        if action_key == "pet":
            options = [
                "%s сперва делает вид, что ей все равно, потом выгибает спину под ладонью и тихо урчит." % name_value,
                "%s боднула вас лбом в ладонь, получила свою порцию ласки и тут же с независимым видом отвернулась." % name_value,
                "%s терпит пару осторожных поглаживаний, потом ловко перехватывает вашу руку лапами, но когти держит убранными." % name_value,
            ]
        elif action_key == "milk":
            options = [
                "%s быстро вылизывает молоко до последней капли, умывается лапой и довольно жмурится." % name_value,
                "%s осторожно нюхает блюдце, потом принимается лакать так сосредоточенно, будто вокруг больше ничего не существует." % name_value,
                "%s пьет молоко маленькими быстрыми глотками, после чего благодарно трется боком о вашу ногу." % name_value,
            ]
        elif action_key == "play":
            options = [
                "%s бросается за веревкой, резко тормозит у ваших сапог и делает вид, что это была серьезная охота." % name_value,
                "%s гоняет по полу щепку, подпрыгивает боком и на миг выглядит совершенно обычной веселой кошкой." % name_value,
                "%s нападает на вашу руку из засады, шлепает лапой по рукаву и тут же отскакивает, ожидая продолжения игры." % name_value,
            ]
        elif action_key == "dog_play":
            options = [
                "%s и пес устраивают короткую возню по трактиру: рывок, прыжок, обиженный фырк, потом оба снова несутся кругами." % name_value,
                "%s делает вид, что пес ей совершенно безразличен, но уже через минуту сама провоцирует его на игру." % name_value,
            ]
        else:
            options = [werecat_ambient_text(room_code)]
        return options[seed_value % len(options)]

    def werecat_sync_profile():
        display_name = str(werecat_display_name() or "Луна")
        # werecat is a creature/animal (pet), not a human girl — skip DateOfBirth entirely
        # (no birth records, pregnancy logic, etc. for non-human entities)
        desc = "Невысокая гибкая кошкодевочка с внимательными золотистыми глазами, мягкими ушами и пушистым хвостом. Двигается бесшумно, настороженно и слишком ловко для обычной домашней любимицы."

        # Use the object model only for werecat (creature/pet). Do NOT write to legacy girltextdesc here —
        # that dict may not exist this early in NextDay init, and werecat is now a BaseNPC object.
        # Set description directly on the instance so .description / self.description works everywhere.
        if "werecat" in peopleInfo:
            info = peopleInfo["werecat"]
            if hasattr(info, "data") and info.data is not None:
                info.data.cname = display_name
                info.data.fullname = display_name
                info.data.genitive = display_name
                info.data.dative = display_name
                info.data.description = desc
            # Direct attribute for code that does werecat.description or info.description
            info.description = desc
        info = peopleInfo.get("werecat", None)
        if info is not None and werecat_is_living_with_household():
            info.mark_known()
        if not werecat_is_living_with_household():
            if info is not None:
                info.location = ""
            return ""
        location_value = str(getLocation("werecat") or "Backyard")
        if info is not None:
            info.location = location_value
        return location_value

    def werecat_picture_path():
        for picture_path in (
            "images/general/kitty.png",
            "images/general/kitty_splash.png",
            "images/general/hunter_store_catInfo.png",
            "images/rpg_message_bg.png",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def werecat_scene_seed():
        return int(dayspassed or 0) + int(day or 0) + int(month or 0) + int(time or 0)

    def werecat_talk_intro_text(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if room_key == "TavernKitchen":
            if werecat_scene_seed() % 2 == 0:
                return "%s устроилась у самого очага и с деловым видом лакает оставленное ей блюдце молока. Кажется, кухню она уже считает своим законным теплым углом." % str(werecat_display_name() or "Кошка")
            return "%s осторожно сидит у очага и следит за кухней так, будто все еще не до конца решила, дом это или просто временная стоянка." % str(werecat_display_name() or "Кошка")
        if room_key == "TavernMain":
            if werecat_scene_seed() % 2 == 0:
                return "%s разлеглась у камина, лениво прищурив глаза на огонь. Со стороны она уже почти выглядит обычной трактирной кошкой, если не считать слишком умного взгляда." % str(werecat_display_name() or "Кошка")
            return "%s держится в стороне от главной залы, но внимательно следит за каждым новым запахом и движением." % str(werecat_display_name() or "Кошка")
        if room_key in ("TavernStorage", "Backyard", "TavernMelissaRoom", "TavernAmandaRoom", "TavernSandraRoom", "TavernMyRoom"):
            return werecat_ambient_text(room_key)
        return "%s устроилась тихо, по-кошачьи свернувшись, но янтарные глаза все равно следят за вами слишком осмысленно." % str(werecat_display_name() or "Кошка")

    def werecat_card_lines():
        lines = [
            "Имя: %s." % str(werecat_display_name() or "Луна"),
            "В трактире она появилась после лесной ловушки и с тех пор постепенно привыкает к дому.",
            "Крыс и прочую мелкую дрянь она чует куда лучше обычной кошки, а людей изучает почти по-человечески внимательно.",
        ]
        if int(werecat_state().get("rats_problem_active", 0) or 0) == 0:
            lines.append("С тех пор в кладовой стало заметно тише: крысы больше не хозяйничают, как раньше.")
        if str(getLocation("werecat") or "") == "TavernKitchen":
            lines.append("Сейчас держится поближе к теплу кухни и временами лакает оставленное для нее молоко.")
        elif str(getLocation("werecat") or "") == "TavernMain":
            lines.append("Сейчас осваивается в общем зале и любит дремать поближе к камину.")
        elif str(getLocation("werecat") or "") == "Backyard":
            lines.append("Сейчас предпочитает двор, где можно и спрятаться, и выбрать удобный угол.")
        elif str(getLocation("werecat") or "") == "TavernStorage":
            lines.append("Сейчас держится у припасов и явно прислушивается к подполу.")
        elif str(getLocation("werecat") or "") in ("TavernMelissaRoom", "TavernAmandaRoom", "TavernSandraRoom", "TavernMyRoom"):
            lines.append("Сейчас выбрала одну из комнат наверху и устроилась там как в тихом логове.")
        return lines

    def werecat_card_title():
        return str(werecat_display_name() or "Луна")

    def werecat_card_stat_rows():
        pet_state = werecat_pet_state()
        trust_value = int(pet_state.get("trust", 0) or 0)
        comfort_value = int(pet_state.get("comfort", 0) or 0)
        if trust_value >= 12:
            trust_text = "домашняя"
        elif trust_value >= 8:
            trust_text = "доверяет"
        elif trust_value >= 4:
            trust_text = "привыкает"
        else:
            trust_text = "насторожена"
        return [
            ("Доверие", str(trust_value)),
            ("Уют", str(comfort_value)),
            ("Состояние", trust_text),
            ("Дом", str(getLocation("werecat") or "нет")),
        ]

    def show_werecat_card_main_ui_state():
        import renpy as renpy_pkg
        store = renpy_pkg.store
        store.UI_mode = "werecat"
        store.UI_selected_char = "werecat"
        store.current_girl_key = "werecat"
        store.current_action_title = werecat_card_title()
        store.current_action_content = None
        store.current_action_items = []
        restart_fn = getattr(renpy, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()


init 2 python:
    npc_daily_schedule_set(
        "werecat",
        default_slots=[],
        random_slots=[
            npc_daily_schedule_random_slot(
                0,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="morning_roam",
                choices=[
                    npc_daily_schedule_choice("TavernKitchen", 3, True, True, "warm_hearth", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 3, True, True, "rat_watch", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMain", 1, True, True, "main_hall", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("Backyard", 1, True, True, "yard_roam", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_slot(
                1,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="noon_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 3, True, True, "sun_yard", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernKitchen", 2, True, True, "kitchen_corner", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 2, True, True, "storage_watch", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMelissaRoom", 1, True, True, "melissa_room", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_slot(
                2,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="day_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 2, True, True, "yard_hunt", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 3, True, True, "storage_hunt", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMelissaRoom", 1, True, True, "melissa_room", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernAmandaRoom", 1, True, True, "amanda_room", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_slot(
                3,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="evening_roam",
                choices=[
                    npc_daily_schedule_choice("TavernKitchen", 2, True, True, "evening_kitchen", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("Backyard", 2, True, True, "evening_yard", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 2, True, True, "evening_storage", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMain", 1, True, True, "evening_hall", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_slot(
                4,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="night_roam",
                choices=[
                    npc_daily_schedule_choice("TavernMyRoom", 2, True, True, "player_room_corner", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "melissa_room_nest", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernAmandaRoom", 1, True, True, "amanda_room_nest", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernSandraRoom", 1, True, True, "sandra_room_nest", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 2, True, True, "night_storage", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("Backyard", 1, True, True, "night_yard", condition=werecat_is_living_with_household),
                ],
            ),
        ],
    )

    _werecat_schedule_entries = []
    for _werecat_slot, _werecat_rooms in WERECAT_ROAM_ROOMS.items():
        for _werecat_room in _werecat_rooms:
            _werecat_schedule_entries.append(NPCScheduleEntry(
                location=_werecat_room,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                time_slots=[_werecat_slot],
                awake=True,
                talkable=True,
                condition=WERECAT_ROAM_CONDITIONS.get(_werecat_room, werecat_is_living_with_household),
                priority=120,
                label="werecat_roam",
            ))
    npc_schedule_set("werecat", _werecat_schedule_entries)

    def _werecat_after_load_init():
        try:
            werecat_sync_profile()
        except Exception:
            pass

    if _werecat_after_load_init not in config.after_load_callbacks:
        config.after_load_callbacks.append(_werecat_after_load_init)


label IntWerecatTalk(room_code=""):
    $ werecat_sync_profile()
    if not werecat_is_living_with_household():
        return
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    if not werecat_is_in_room(_werecat_room):
        $ main_ui_end_talk_state()
        return
    $ werecat.mark_known()
    $ main_ui_begin_talk_state(str(werecat_display_name() or "Луна"), "werecat")
    $ current_action_title = str(werecat_display_name() or "Луна")
    $ current_action_content = None
    $ _werecat_picture = werecat_picture_path()
    if str(_werecat_picture or "").strip():
        $ _layout_last_picture = _werecat_picture
    $ MainTxt = werecat_talk_intro_text(_werecat_room)
    $ CurLocDesc = MainTxt
    call IntWerecatTalkRefresh(_werecat_room)
    return


label IntWerecatTalkRefresh(room_code=""):
    $ werecat_sync_profile()
    if not werecat_is_living_with_household():
        $ main_ui_end_talk_state()
        return
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    if not werecat_is_in_room(_werecat_room):
        $ main_ui_end_talk_state()
        return
    $ main_ui_begin_talk_state(str(werecat_display_name() or "Луна"), "werecat")
    $ current_action_title = str(werecat_display_name() or "Луна")
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Осмотреть", Function(show_werecat_card_main_ui_state)),
    ]
    $ _werecat_pet_state = werecat_pet_state()
    if int(_werecat_pet_state.get("pet_day", -1) or -1) != int(dayspassed or 0):
        $ current_action_items.append(MenuItem("Погладить кошку", Call("IntWerecatTalkApply", _werecat_room, "pet")))
    if int(_werecat_pet_state.get("milk_day", -1) or -1) != int(dayspassed or 0) and werecat_has_milk_available(_werecat_room):
        $ current_action_items.append(MenuItem("Дать молока", Call("IntWerecatTalkApply", _werecat_room, "milk")))
    if int(_werecat_pet_state.get("play_day", -1) or -1) != int(dayspassed or 0):
        $ current_action_items.append(MenuItem("Поиграть с кошкой", Call("IntWerecatTalkApply", _werecat_room, "play")))
    $ current_action_items.append(MenuItem("Понаблюдать за кошкой", Call("IntWerecatTalkApply", _werecat_room, "observe")))
    if werecat_can_play_with_dog(_werecat_room):
        $ current_action_items.append(MenuItem("Поиграть с кошкой и псом", Call("IntWerecatTalkApply", _werecat_room, "dog_play")))
    $ current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
    return


label IntWerecatTalkApply(room_code="", choice_code=""):
    $ _werecat_choice = str(choice_code or "").strip().lower()
    $ _werecat_pet_state = werecat_pet_state()
    if not werecat_is_in_room(room_code):
        $ main_ui_end_talk_state()
        return
    if _werecat_choice == "pet":
        $ _werecat_pet_state["pet_day"] = int(dayspassed or 0)
        $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 1)
        $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 1)
        $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
        $ health = _player_clamp(int(health or 0) + 1, 0, 100)
        $ MainTxt = werecat_reaction_text("pet", room_code)
        $ CurLocDesc = MainTxt
        call stat
        call IntWerecatTalkRefresh(room_code)
        return
    if _werecat_choice == "milk":
        if werecat_consume_milk(room_code):
            $ _werecat_pet_state["milk_day"] = int(dayspassed or 0)
            $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 2)
            $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 2)
            $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
            $ energy = _player_clamp(int(energy or 0) + 3, 0, 100)
            $ health = _player_clamp(int(health or 0) + 2, 0, 100)
            $ MainTxt = werecat_reaction_text("milk", room_code)
            $ CurLocDesc = MainTxt
            call stat
        else:
            $ MainTxt = "Молока под рукой нет."
            $ CurLocDesc = MainTxt
        call IntWerecatTalkRefresh(room_code)
        return
    if _werecat_choice == "play":
        $ _werecat_pet_state["play_day"] = int(dayspassed or 0)
        $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 1)
        $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 1)
        $ fun = _player_clamp(int(fun or 0) + 5, 0, 100)
        $ energy = _player_clamp(int(energy or 0) + 1, 0, 100)
        $ health = _player_clamp(int(health or 0) + 1, 0, 100)
        $ MainTxt = werecat_reaction_text("play", room_code)
        $ CurLocDesc = MainTxt
        call stat
        call IntWerecatTalkRefresh(room_code)
        return
    if _werecat_choice == "observe":
        $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 1)
        $ MainTxt = werecat_ambient_text(room_code)
        $ CurLocDesc = MainTxt
        call IntWerecatTalkRefresh(room_code)
        return
    if _werecat_choice == "dog_play":
        $ _werecat_dog = ensure_dog_runtime()
        if bool(_werecat_dog.owned):
            $ _werecat_dog.play()
            $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 1)
            $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 2)
            $ fun = _player_clamp(int(fun or 0) + 4, 0, 100)
            $ energy = _player_clamp(int(energy or 0) + 1, 0, 100)
            $ health = _player_clamp(int(health or 0) + 1, 0, 100)
            $ MainTxt = werecat_reaction_text("dog_play", room_code)
            $ CurLocDesc = MainTxt
            call stat
        else:
            $ MainTxt = "Пса сейчас рядом нет."
            $ CurLocDesc = MainTxt
        call IntWerecatTalkRefresh(room_code)
        return
    call IntWerecatTalkRefresh(room_code)
    return


label ShowWerecatCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ show_werecat_card_main_ui_state()
        return
    show screen werecat_card_overlay(return_label)
    return


label HideWerecatCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
        return
    hide screen werecat_card_overlay
    if str(return_label or "") != "":
        call expression return_label
    return


screen werecat_card_overlay(return_label=""):
    zorder 120

    $ _title = werecat_card_title()
    $ _portrait = werecat_picture_path()
    $ _stats = werecat_card_stat_rows()
    $ _lines = werecat_card_lines()
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24

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
            ysize _left_h - 96
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                hbox:
                    spacing 12

                    add im.Scale(_portrait, 180, 240)

                    vbox:
                        spacing 3
                        for _row in _stats:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                for _line in _lines:
                    text _line size 16 color "#2d1d12"

        textbutton "Назад":
            id "werecat_card_overlay_back_button"
            alt "werecat_card_overlay_back_button"
            xpos 28
            ypos _left_h - 58
            xminimum 220
            text_size 22
            text_bold True
            text_color "#5c0f1b"
            text_hover_color "#7d1a2c"
            action [Hide("werecat_card_overlay"), SetVariable("UI_mode", "scene"), SetVariable("UI_selected_char", ""), SetVariable("current_girl_key", ""), Jump(str(CurLoc or getattr(CurrentRoom, "code_name", "") or "TavernMain"))]
