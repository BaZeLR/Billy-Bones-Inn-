# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Becky Home Location (Converted from legacy script)
# Handles arrival modes, scene setup, and branching for Becky home events.
# Arguments: arrive_mode (str)

init python:
    def becky_home_picture(arrive_mode=""):
        mode_key = str(arrive_mode or rooms.get("BeckyHomeFront").state["arrival_mode"] or "").strip()
        if mode_key in ("FromDances", "FromDinner", "SvalnyiGreh"):
            candidates = [
                "images/becky/sex/inroom1.jpg",
                "images/becky/sex/inroom2.jpg",
                "images/becky/sex/inroom3.jpg",
                "images/becky/Home/withbecky.jpg",
            ]
        else:
            candidates = [
                "images/becky/Home/withbecky.jpg",
                "images/becky/Home/house1.jpg",
                "images/becky/Home/house2.jpg",
            ]
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return candidates[0]

    def becky_home_restore_text():
        mode_key = str(rooms.get("BeckyHomeFront").state["arrival_mode"] or "").strip()
        if mode_key == "FromDances":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне."
        if mode_key == "FromDinner":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне."
        if mode_key == "SvalnyiGreh":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне.\nВместе с вами находится Эдди, ее управляющий лавкой. Им движут к хозяйке отнюдь не деловые чувства."
        return "Итак, вы сидите за столом в гостях у вдовы Блэнкеншип и наслаждаетесь аппетитной домашней кухней."

    def becky_home_desc_default():
        return rooms.get("BeckyHomeFront").state["arrival_mode"] == ""

    def becky_home_desc_dances():
        return rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances"

    def becky_home_desc_special():
        return rooms.get("BeckyHomeFront").state["arrival_mode"] in ("SvalnyiGreh", "FromDinner")

    BeckyHomeRoomDefinition = Room(
        code_name="BeckyHome",
        group_name=ROOM_GROUP_CITY,
        display_name="Дом Бекки",
        bg_picture="images/becky/Home/interior.png",
        descriptions=[
            RoomDescription(
                text="Вы постучали в дверь и через несколько секунд она распахнулась. За ней стояла Ребекка Блэнкеншип.",
                condition=becky_home_desc_default,
                priority=200,
            ),
            RoomDescription(
                text="Заведя вас к себе в дом, Бекки тихо и осторожно повела вас по коридору к себе в спальню. Вдоль стен стояло несколько массивных сундуков, скамья, пара стульев. А весь центр комнаты занимала большая кровать.",
                condition=becky_home_desc_dances,
                priority=210,
            ),
            RoomDescription(
                text="Весь центр комнаты занимает большая кровать, а вдоль стен стоит несколько массивных сундуков, скамья, пара стульев.",
                condition=becky_home_desc_special,
                priority=205,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[],
        custom_properties={
            "becky_house": True,
        },
    )

label BeckyHome(arrive_mode=""):
    $ renpy.dynamic("_becky_home_room", "_becky_home_text", "GirlName", "_start_becky_sex", "_becky_admitted")
    if arrive_mode not in ("FromDances", "FromDinner", "SvalnyiGreh") and not Becky.is_home_for_evening_visit():
        vscene "images/becky/Home/house2.jpg"
        $ scene_runtime.text = "Вы постучали, но Бекки не ответила. Стоит вернуться вечером, когда она будет дома и еще не ляжет спать."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Вернуться на рынок":
                $ apply_movement_time(10, "MarketPlace")
                jump MarketPlace
    $ rooms.get("BeckyHomeFront").state["arrival_mode"] = arrive_mode
    $ _becky_home_room = rooms.get("BeckyHome")
    $ rooms.enter("BeckyHome")
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.talk_picture = ""
    $ main_ui_runtime.clear_contexts()
    $ main_ui_runtime.action_title = _becky_home_room.display_name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ Eddie.set_sex_stat("group_sex", 1 if arrive_mode == "SvalnyiGreh" else 0)
    $ scene_runtime.picture = becky_home_picture(rooms.get("BeckyHomeFront").state["arrival_mode"])
    vscene scene_runtime.picture
    $ _becky_home_text = _becky_home_room.visible_descriptions()[0].text
    $ scene_runtime.text = _becky_home_text
    $ scene_runtime.location_text = _becky_home_text
    $ GirlName = 'becky'
    python:
        Becky.stats.setdefault("PussyWetStart", Becky.arousal_value())
    $ _becky_home_room.mark_visited()

    $ _start_becky_sex = False
    if arrive_mode == 'FromDances' and int(threads["beckyDinner"].num or 0) < 2:
        "[_becky_home_room.descriptions[1].text]\nВы и миссис Блэнкеншип находитесь в ее спальне."
        call ShowImageSeq('becky', 'sex', 'inroom', 3)
        $ _start_becky_sex = True
    elif arrive_mode == 'SvalnyiGreh':
        call IntEddieBeckySex
        "[_becky_home_room.descriptions[2].text]\nВы и миссис Блэнкеншип находитесь в ее спальне.\nВместе с вами находится Эдди, ее управляющий лавкой. Им движут к хозяйке отнюдь не деловые чувства."
        $ _start_becky_sex = True
    elif arrive_mode == 'FromDinner':
        "[_becky_home_room.descriptions[2].text]"
        if story_event_available("BeckyHome", "enter"):
            call checkTriggers("BeckyHome", "enter", 0)
        else:
            if not threads["beckyEddieSex"].completed:
                "Дав вам зайти, вдова закрыла дверь на ключ и обернулась к вам, сказав: 'Если детишки мои развлекаются, то почему в конце концов я не могу себе такого позволить? Иди же ко мне!' "
            else:
                "Вдова не позаботилась не то, что запереть дверь на ключ, но и даже полностью закрыть ее, и не теряя времени потащила вас к кровати. "
            "Вы и миссис Блэнкеншип находитесь в ее спальне."
        call ShowImageSeq('becky', 'sex', 'inroom', 3)
        $ _start_becky_sex = True
    else:
        $ _becky_admitted = False
        if arrive_mode == 'FromDances':
            $ scene_runtime.text = "Ребекка завозилась с ключами, отпирая дверь. Это у нее заняло немного дольше времени, чем должно бы, так как вы все время игриво залазили ей под юбку, отвлекая ее от поисков нужного ключа. Наконец дверь отворилась и Бекки пригласила вас в дом:\n'Заходи, Стефан, и пожалуй за стол.' "
            $ scene_runtime.location_text = scene_runtime.text
            $ _becky_admitted = True
            menu:
                "Продолжить":
                    pass
        else:
            menu:
                "Продолжить":
                    pass
            if int(threads["beckyHome"].num or 0) < 3:
                if not Becky.uninvited_visit_scolded:
                    $ scene_runtime.text = "Она не очень-то была рада вашему визиту: 'Стефан, зачем ты пришел?! Мы же договаривались! Надеюсь, тебя никто не видел?'\n'Никто,' сказали вы глядя на вдову своими честными глазами. 'Но я просто хотел...'\nБекки однако, ваше желание мало интересовало. Она резко прервала вас: 'Не приходи больше, что люди подумают. Все, пока.'\nИ дверь перед вашим носом захлопнулась.  "
                    $ scene_runtime.location_text = scene_runtime.text
                    $ Becky.uninvited_visit_scolded = True
                    $ Becky.apply_social_roll(8, 3, -1, 35, 3, -1)
                else:
                    $ scene_runtime.text = "Увидев вас она рассердилась не на шутку: 'Стефан, тебе что, все нужно по 20 раз повторять?! Не приходи пока ко мне домой.'\n'Но я,' начали оправдываться вы, но поняли, что разговариваете с закрытой дубовой дверью. Изнутри послышался звук запираемого засова. Похоже, сейчас вам здесь не очень-то рады. "
                    $ scene_runtime.location_text = scene_runtime.text
                    $ Becky.apply_social_roll(8, 1, -1, 35, 1, -1)
                menu:
                    "В печали вернуться к трактиру":
                        jump StreetTavern
            elif player.appearance.current_dress != 'citydress':
                $ scene_runtime.text = "Она тщательно осмотрела вас и строго сказала: 'Стефан, я же тебе говорила, ты должен быть одет скромно но прилично. А ты в чем пришел? Беги переодевайся!'\nС этими словами она захлопнула дверь перед вашим носом. Отчего-то вы почувствовали себя нашкодничавшим школьником."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Вернуться к трактиру переодеться":
                        jump StreetTavern
            else:
                $ scene_runtime.text = "Она тщательно осмотрела вас и сказала: 'Что же ты встал на пороге, проходи скорей!'\nВы не замедлили воспользоваться приглашением и прошли в дом, прямо к накрытому столу. К вашей скромной трапезе из 6 блюд присоединился и Эдди.\nНе успели вы приступить к поглощению пищи, как услышали как хлопнула входная дверь"
                $ scene_runtime.location_text = scene_runtime.text
                $ _becky_admitted = True
                menu:
                    "Продолжить":
                        pass
        if _becky_admitted:
            $ Becky.home_visit_count += 1
            if Inga.acquaintance_stage >= 2:
                $ scene_runtime.text = " и вскоре к вам за столом присоединились Ингенборг, старшая дочка соломенной вдовушки, вместе со своим хахалем Лукасом."
                $ scene_runtime.location_text = scene_runtime.text
            elif Inga.acquaintance_stage == 1:
                $ scene_runtime.text = " и на пороге показалась уже виденная вами парочка - Лукас и Ингенборг. Бекки повернулась к вам: 'Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.'\nВы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол. "
                $ scene_runtime.location_text = scene_runtime.text
                $ Inga.acquaintance_stage = 2
            else:
                $ scene_runtime.text = " и на пороге показалось двое - высокая рыжеволосая девушка, похожая на хозяйку дома, в сопровождения парня чуть постарше ее. Бекки повернулась к вам: 'Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.'\nВы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол. "
                $ scene_runtime.location_text = scene_runtime.text
                $ Inga.acquaintance_stage = 2
            call ShowImage('becky', 'dinner', 'DinnerInga')
            menu:
                "Продолжить":
                    pass
            if procedural_randint(1, 5, "becky_home_dinner_inga_legacy_%s" % int(current_game_day() or 0)) == 1:
                $ scene_runtime.text = " Вы присмотрелись к Инге и заметили, что перед ужином времени она не теряла, на ее рыжей шевелюре были видны следы спермы."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Продолжить":
                        pass
            if Inga.pregnancy_days() >= 120:
                $ scene_runtime.text = " Одного взгляда на круглый живот Инги было достаточно, чтобы понять что она ведет активную половую жизнь."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Продолжить":
                        pass
            call IntBeckyGuest
            $ scene_runtime.text = " Итак, вы сидите за столом в гостях у вдовы Блэнкеншип и наслаждаетесь аппетитной домашней кухней."
            $ scene_runtime.location_text = scene_runtime.text
    if _start_becky_sex:
        $ Becky.set_arousal(Becky.sex_stat("PussyWetStart", 0))
        call CockPosition(GirlName, 0)
        call check_visibility(GirlName)
        call IntBeckySex(GirlName)
        jump BeckyHomeAfterSex
    $ scene_runtime.picture = _becky_home_room.bg_picture
    $ scene_runtime.text = becky_home_restore_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(rooms.current.display_name or "Дом Бекки")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = _becky_home_room.build_exit_items()
    while True:
        call screen main_ui


label BeckyHomeAfterSex:
    if int(threads["beckyHome"].num or 0) < 2:
        $ threads["beckyHome"].advanceTo(2, force_active=True)
    $ scene_runtime.picture = rooms.get("BeckyHome").bg_picture
    $ scene_runtime.text = becky_home_restore_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(rooms.get("BeckyHome").display_name or "Дом Бекки")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = rooms.get("BeckyHome").build_exit_items()
    while True:
        call screen main_ui

