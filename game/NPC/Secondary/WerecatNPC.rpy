# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -8 python:
    def werecat_story_defaults():
        return {
            "rats_problem_active": 1,
            "adoption_breakfast_seen": 0,
            "woods_exploration": 0,
            "tracks_seen": 0,
            "tracks_first_text_seen": 0,
            "tracks_room": "",
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

    class WerecatInfo(BaseNPC):
        talk_label = "IntWerecatTalk"
        unknown_name = "Кошкодевочка"

        def __init__(self):
            super().__init__("werecat")
            self.var = werecat_story_defaults()
            self.stats = werecat_pet_defaults()

    def werecat_state():
        return werecat.var

    def werecat_pet_state():
        return werecat.stats

    def werecat_is_living_with_household():
        state = werecat_state()
        adopted_count = int(state.get("adopted_count", 0) or 0)
        if int(state.get("adopted", 0) or 0) == 1:
            adopted_count = max(1, adopted_count)
        return adopted_count >= 1 and int(state.get("sold", 0) or 0) == 0

    WERECAT_MILK_ITEM_IDS = ("milk_pitcher_001",)

    def werecat_is_in_room(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        if room_key == "" or not werecat_is_living_with_household():
            return False
        return str(people.location("werecat") or "") == room_key

    def werecat_ambient_text(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
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
        room_key = str(room_code or rooms.current_code or "").strip()
        if not room_key:
            return ""
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
        room_key = str(room_code or rooms.current_code or "").strip()
        if not werecat_is_in_room(room_key):
            return False
        try:
            d = dog
        except Exception:
            return False
        if not bool(getattr(d, "owned", False)):
            return False
        return room_key in ("Backyard", "TavernMain", "TavernKitchen", "TavernStorage")

    def werecat_has_milk_available(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        for item_id in WERECAT_MILK_ITEM_IDS:
            try:
                if int(player.item_count(item_id) or 0) > 0:
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
        room_key = str(room_code or rooms.current_code or "").strip()
        for item_id in WERECAT_MILK_ITEM_IDS:
            try:
                if int(player.item_count(item_id) or 0) > 0:
                    return bool(player.remove_item(item_id, 1))
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
        return int(current_game_day()) + int(calendar_v2.day or 0) + int(calendar_v2.period or 0) + int(calendar_v2.time_slot() or 0)

    def werecat_talk_intro_text(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
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
        if str(people.location("werecat") or "") == "TavernKitchen":
            lines.append("Сейчас держится поближе к теплу кухни и временами лакает оставленное для нее молоко.")
        elif str(people.location("werecat") or "") == "TavernMain":
            lines.append("Сейчас осваивается в общем зале и любит дремать поближе к камину.")
        elif str(people.location("werecat") or "") == "Backyard":
            lines.append("Сейчас предпочитает двор, где можно и спрятаться, и выбрать удобный угол.")
        elif str(people.location("werecat") or "") == "TavernStorage":
            lines.append("Сейчас держится у припасов и явно прислушивается к подполу.")
        elif str(people.location("werecat") or "") in ("TavernMelissaRoom", "TavernAmandaRoom", "TavernSandraRoom", "TavernMyRoom"):
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
            ("Дом", str(people.location("werecat") or "нет")),
        ]



init 2 python:
    WerecatStaticData.set_daily_schedule(
        default_intervals=[],
        random_intervals=[
            npc_daily_schedule_random_interval(
                6, 8,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="morning_roam",
                choices=[
                    npc_daily_schedule_choice("TavernKitchen", 3, True, True, "warm_hearth", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 3, True, True, "rat_watch", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMain", 1, True, True, "main_hall", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("Backyard", 1, True, True, "yard_roam", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_interval(
                8, 11,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="noon_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 3, True, True, "sun_yard", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernKitchen", 2, True, True, "kitchen_corner", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 2, True, True, "storage_watch", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMelissaRoom", 1, True, True, "melissa_room", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_interval(
                11, 13,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="day_roam",
                choices=[
                    npc_daily_schedule_choice("Backyard", 2, True, True, "yard_hunt", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 3, True, True, "storage_hunt", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMelissaRoom", 1, True, True, "melissa_room", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernAmandaRoom", 1, True, True, "amanda_room", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_interval(
                13, 16,
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                label="evening_roam",
                choices=[
                    npc_daily_schedule_choice("TavernKitchen", 2, True, True, "evening_kitchen", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("Backyard", 2, True, True, "evening_yard", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernStorage", 2, True, True, "evening_storage", condition=werecat_is_living_with_household),
                    npc_daily_schedule_choice("TavernMain", 1, True, True, "evening_hall", condition=werecat_is_living_with_household),
                ],
            ),
            npc_daily_schedule_random_interval(
                16, 18,
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

define WerecatStaticData = PeopleData(
    "werecat",
    cname="Кошка",
    fullname="Луна",
    genitive="Луны",
    dative="Луне",
    portrait="images/general/kitty.png",
    default_location="",
    description="Домовая кошка-оборотень, если она решила остаться при трактире.",
)
default werecat = WerecatInfo()

label InitWerecat:
    $ people.register(WerecatStaticData, werecat)
    return


label IntWerecatTalk(room_code=""):
    $ renpy.dynamic("_werecat_room", "_werecat_picture", "_werecat_pet_state", "_werecat_dog")
    if not werecat_is_living_with_household():
        return
    $ _werecat_room = str(room_code or rooms.current_code or "").strip()
    if not werecat_is_in_room(_werecat_room):
        return
    $ werecat.mark_known()
    $ main_ui_begin_talk_state(str(werecat_display_name() or "Луна"), "werecat")
    $ _werecat_picture = werecat_picture_path()
    if str(_werecat_picture or "").strip():
        vscene _werecat_picture
    $ scene_runtime.text = werecat_talk_intro_text(_werecat_room)
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    while True:
        "[scene_runtime.text]"
        $ _werecat_pet_state = werecat_pet_state()
        menu:
            "Осмотреть":
                call ShowWerecatCard
                $ scene_runtime.text = werecat_talk_intro_text(_werecat_room)
                $ scene_runtime.location_text = scene_runtime.text

            "Погладить кошку" if int(_werecat_pet_state.get("pet_day", -1) or -1) != int(calendar_v2.daysInGame or 0):
                $ _werecat_pet_state["pet_day"] = int(calendar_v2.daysInGame or 0)
                $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 1)
                $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 1)
                $ player.change_stat("fun", 2)
                $ player.change_stat("health", 1)
                $ scene_runtime.text = werecat_reaction_text("pet", _werecat_room)
                $ scene_runtime.location_text = scene_runtime.text
                call stat

            "Дать молока" if int(_werecat_pet_state.get("milk_day", -1) or -1) != int(calendar_v2.daysInGame or 0) and werecat_has_milk_available(_werecat_room):
                if werecat_consume_milk(_werecat_room):
                    $ _werecat_pet_state["milk_day"] = int(calendar_v2.daysInGame or 0)
                    $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 2)
                    $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 2)
                    $ player.change_stat("fun", 2)
                    $ player.change_stat("energy", 3)
                    $ player.change_stat("health", 2)
                    $ scene_runtime.text = werecat_reaction_text("milk", _werecat_room)
                    call stat
                else:
                    $ scene_runtime.text = "Молока под рукой нет."
                $ scene_runtime.location_text = scene_runtime.text

            "Поиграть с кошкой" if int(_werecat_pet_state.get("play_day", -1) or -1) != int(calendar_v2.daysInGame or 0):
                $ _werecat_pet_state["play_day"] = int(calendar_v2.daysInGame or 0)
                $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 1)
                $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 1)
                $ player.change_stat("fun", 5)
                $ player.change_stat("energy", 1)
                $ player.change_stat("health", 1)
                $ scene_runtime.text = werecat_reaction_text("play", _werecat_room)
                $ scene_runtime.location_text = scene_runtime.text
                call stat

            "Понаблюдать за кошкой":
                $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 1)
                $ scene_runtime.text = werecat_ambient_text(_werecat_room)
                $ scene_runtime.location_text = scene_runtime.text

            "Поиграть с кошкой и псом" if werecat_can_play_with_dog(_werecat_room):
                $ _werecat_dog = dog
                if bool(_werecat_dog.owned):
                    $ _werecat_dog.play()
                    $ _werecat_pet_state["trust"] = min(20, int(_werecat_pet_state.get("trust", 0) or 0) + 1)
                    $ _werecat_pet_state["comfort"] = min(20, int(_werecat_pet_state.get("comfort", 0) or 0) + 2)
                    $ player.change_stat("fun", 4)
                    $ player.change_stat("energy", 1)
                    $ player.change_stat("health", 1)
                    $ scene_runtime.text = werecat_reaction_text("dog_play", _werecat_room)
                    call stat
                else:
                    $ scene_runtime.text = "Пса сейчас рядом нет."
                $ scene_runtime.location_text = scene_runtime.text

            "Закончить разговор":
                $ main_ui_end_talk_state()
                return


label ShowWerecatCard(return_label=""):
    $ renpy.dynamic("_werecat_card_picture")
    $ main_ui_begin_card_state()
    $ _werecat_card_picture = werecat_picture_path()
    if str(_werecat_card_picture or "").strip():
        vscene _werecat_card_picture
    $ scene_runtime.text = "\n".join(werecat_card_lines())
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ main_ui_end_card_state()
    return


label HideWerecatCard(return_label=""):
    return
