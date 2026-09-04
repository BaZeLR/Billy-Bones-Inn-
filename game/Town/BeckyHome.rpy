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

    def becky_home_table_visible():
        return rooms.get("BeckyHomeFront").state["arrival_mode"] == ""

    def becky_home_action_items():
        sections = rooms.get("BeckyHome").build_menu_sections()
        return list(sections.get("movement", [])) + list(sections.get("actions", []))

    BeckyHomeRoomDefinition = Room(
        code_name="BeckyHome",
        group_name=ROOM_GROUP_CITY,
        display_name="Дом Бекки",
        bg_picture="images/becky/Home/withbecky.jpg",
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
        game_items=[
            "becky_home_bed",
            "becky_home_chests",
            "becky_home_dinner_table",
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="17:59"),
        custom_properties={
            "becky_house": True,
            "object_menu_label": "BeckyHomeObjectMenu",
        },
    )

label BeckyHome(arrive_mode=""):
    $ renpy.dynamic("_becky_home_room", "GirlName", "_start_becky_sex", "_becky_admitted")
    $ rooms.get("BeckyHomeFront").state["arrival_mode"] = arrive_mode
    $ _becky_home_room = rooms.get("BeckyHome")
    $ rooms.enter("BeckyHome")
    $ scene_runtime.picture = becky_home_picture(rooms.get("BeckyHomeFront").state["arrival_mode"])
    $ GirlName = 'becky'
    python:
        Becky.stats.setdefault("PussyWetStart", Becky.arousal_value())
    $ _becky_home_room.mark_visited()

    $ _start_becky_sex = False
    if arrive_mode == 'FromDances' and Becky.home_visit_stage < 5:
        "[_becky_home_room.descriptions[1].text] <br>Вы и миссис Блэнкеншип находитесь в ее спальне."
        call ShowImageSeq('becky', 'sex', 'inroom', 3)
        $ _start_becky_sex = True
    elif arrive_mode == 'SvalnyiGreh':
        $ GrupenSex['eddie'] = 1
        call IntEddieBeckySex
        "[_becky_home_room.descriptions[2].text] <br>Вы и миссис Блэнкеншип находитесь в ее спальне.<br>Вместе с вами находится Эдди, ее управляющий лавкой. Им движут к хозяйке отнюдь не деловые чувства."
        $ _start_becky_sex = True
    elif arrive_mode == 'FromDinner':
        "<br><br>[_becky_home_room.descriptions[2].text] "
        if Becky.eddie_join_stage == 1 and Becky.home_visit_stage < 7:
            call BeckyEddieJoinFirst
        else:
            if Becky.home_visit_stage < 7:
                "Дав вам зайти, вдова закрыла дверь на ключ и обернулась к вам, сказав: 'Если детишки мои развлекаются, то почему в конце концов я не могу себе такого позволить? Иди же ко мне!' "
            else:
                "Вдова не позаботилась не то, что запереть дверь на ключ, но и даже полностью закрыть ее, и не теряя времени потащила вас к кровати. "
            "Вы и миссис Блэнкеншип находитесь в ее спальне."
        call ShowImageSeq('becky', 'sex', 'inroom', 3)
        $ _start_becky_sex = True
    else:
        $ _becky_admitted = False
        if arrive_mode == 'FromDances':
            "Ребекка завозилась с ключами, отпирая дверь. Это у нее заняло немного дольше времени, чем должно бы, так как вы все время игриво залазили ей под юбку, отвлекая ее от поисков нужного ключа. Наконец дверь отворилась и Бекки пригласила вас в дом: <br>'Заходи, Стефан, и пожалуй за стол.' "
            $ _becky_admitted = True
        else:
            "[_becky_home_room.descriptions[0].text] "
            if Becky.home_visit_stage < 3:
                if not Becky.uninvited_visit_scolded:
                    "Она не очень-то была рада вашему визиту: 'Стефан, зачем ты пришел?! Мы же договаривались! Надеюсь, тебя никто не видел?' <br> 'Никто,' сказали вы глядя на вдову своими честными глазами. 'Но я просто хотел...' <br> Бекки однако, ваше желание мало интересовало. Она резко прервала вас: 'Не приходи больше, что люди подумают. Все, пока.'<br> И дверь перед вашим носом захлопнулась.  "
                    $ Becky.uninvited_visit_scolded = True
                    $ Becky.apply_social_roll(8, 3, -1, 35, 3, -1)
                else:
                    "Увидев вас она рассердилась не на шутку: 'Стефан, тебе что, все нужно по 20 раз повторять?! Не приходи пока ко мне домой.' <br> 'Но я,' начали оправдываться вы, но поняли, что разговариваете с закрытой дубовой дверью. Изнутри послышался звук запираемого засова. Похоже, сейчас вам здесь не очень-то рады. "
                    $ Becky.apply_social_roll(8, 1, -1, 35, 1, -1)
                menu:
                    "В печали вернуться к трактиру":
                        jump StreetTavern
            elif player.appearance.current_dress != 'citydress':
                "Она тщательно осмотрела вас и строго сказала: 'Стефан, я же тебе говорила, ты должен быть одет скромно но прилично. А ты в чем пришел? Беги переодевайся!'\nС этими словами она захлопнула дверь перед вашим носом. Отчего-то вы почувствовали себя нашкодничавшим школьником."
                menu:
                    "Вернуться к трактиру переодеться":
                        jump StreetTavern
            else:
                "Она тщательно осмотрела вас и сказала: 'Что же ты встал на пороге, проходи скорей!'\nВы не замедлили воспользоваться приглашением и прошли в дом, прямо к накрытому столу. К вашей скромной трапезе из 6 блюд присоединился и Эдди.\nНе успели вы приступить к поглощению пищи, как услышали как хлопнула входная дверь"
                $ _becky_admitted = True
        if _becky_admitted:
            $ Becky.home_visit_count += 1
            if Inga.acquaintance_stage >= 2:
                " и вскоре к вам за столом присоединились Ингенборг, старшая дочка соломенной вдовушки, вместе со своим хахалем Лукасом."
            elif Inga.acquaintance_stage == 1:
                " и на пороге показалась уже виденная вами парочка - Лукас и Ингенборг. Бекки повернулась к вам: 'Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.'\nВы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол. "
                $ Inga.acquaintance_stage = 2
            else:
                " и на пороге показалось двое - высокая рыжеволосая девушка, похожая на хозяйку дома, в сопровождения парня чуть постарше ее. Бекки повернулась к вам: 'Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.'\nВы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол. "
                $ Inga.acquaintance_stage = 2
            call ShowImage('becky', 'dinner', 'DinnerInga')
            if procedural_randint(1, 5, "becky_home_dinner_inga_legacy_%s" % int(current_game_day() or 0)) == 1:
                " Вы присмотрелись к Инге и заметили, что перед ужином времени она не теряла, на ее рыжей шевелюре были видны следы спермы."
            if Inga.pregnancy_days() >= 120:
                " Одного взгляда на круглый живот Инги было достаточно, чтобы понять что она ведет активную половую жизнь."
            call IntBeckyGuest
            " Итак, вы сидите за столом в гостях у вдовы Блэнкеншип и наслаждаетесь аппетитной домашней кухней."
    if _start_becky_sex:
        $ Becky.set_arousal(Becky.sex_stat("PussyWetStart", 0))
        call CockPosition(GirlName, 0)
        call check_visibility(GirlName)
        call IntBeckySex(GirlName)
        return
    $ scene_runtime.text = becky_home_restore_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(rooms.current.display_name or "Дом Бекки")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = becky_home_action_items()
    while True:
        call screen main_ui


label BeckyHomeAfterSex:
    $ Becky.home_visit_stage = max(Becky.home_visit_stage, 2)
    $ scene_runtime.text = becky_home_restore_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(rooms.get("BeckyHome").display_name or "Дом Бекки")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = becky_home_action_items()
    while True:
        call screen main_ui


label BeckyHomeObjectMenu(object_id=""):
    $ renpy.dynamic("_becky_home_object", "_room_object", "_becky_action", "_becky_args")
    if str(object_id or "") != "":
        $ main_ui_runtime.object_id = object_id
    $ object_id = main_ui_runtime.object_id
    $ _becky_home_object = None
    python:
        for _room_object in rooms.get("BeckyHome").visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _becky_home_object = _room_object
                break

    if _becky_home_object is None:
        $ scene_runtime.text = becky_home_restore_text()
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = str(rooms.get("BeckyHome").display_name or "Дом Бекки")
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = becky_home_action_items()
        return

    $ main_ui_runtime.action_title = str(_becky_home_object.name or "Дом Бекки")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ scene_runtime.text = str(_becky_home_object.description or "")
    $ scene_runtime.location_text = scene_runtime.text
    python:
        for _becky_action in _becky_home_object.visible_actions():
            _becky_args = tuple(getattr(_becky_action, "args", ()) or ())
            if _becky_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_becky_action.label, Call("BeckyHomeObjectText", object_id, _becky_action.action_id)))
            elif _becky_action.hook == "call" and str(_becky_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_becky_action.label, Call(_becky_action.target, *_becky_args)))
            elif _becky_action.hook == "jump" and str(_becky_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_becky_action.label, Jump(_becky_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "picture", becky_home_picture(rooms.get("BeckyHomeFront").state["arrival_mode"])),
            SetField(scene_runtime, "text", becky_home_restore_text()),
            SetField(scene_runtime, "location_text", becky_home_restore_text()),
            SetField(main_ui_runtime, "action_title", str(rooms.get("BeckyHome").display_name or "Дом Бекки")),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", becky_home_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label BeckyHomeObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_becky_name", "_becky_text", "_room_action", "_room_object")
    python:
        _becky_text = ""
        _becky_name = ""
        for _room_object in rooms.get("BeckyHome").visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _becky_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _becky_text = str(_room_action.target or "")
                    break
            break
        if _becky_text:
            scene_runtime.text = _becky_text
            scene_runtime.location_text = _becky_text
            main_ui_runtime.action_title = _becky_name or "Дом Бекки"
    call BeckyHomeObjectMenu(object_id)
    return

