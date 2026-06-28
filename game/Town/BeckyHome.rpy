# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Becky Home Location (Converted from legacy script)
# Handles arrival modes, scene setup, and branching for Becky home events.
# Arguments: arrive_mode (str)

default BeckyHomeActive = 0

init python:
    def becky_home_picture(arrive_mode=""):
        mode_key = str(arrive_mode or ArriveMode or "").strip()
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
        mode_key = str(ArriveMode or "").strip()
        if mode_key == "FromDances":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне."
        if mode_key == "FromDinner":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне."
        if mode_key == "SvalnyiGreh":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне.\nВместе с вами находится Эдди, ее управляющий лавкой. Им движут к хозяйке отнюдь не деловые чувства."
        return "Итак, вы сидите за столом в гостях у вдовы Блэнкеншип и наслаждаетесь аппетитной домашней кухней."

    def becky_home_after_sex_text():
        mode_key = str(ArriveMode or "").strip()
        if mode_key == "FromDances":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне."
        if mode_key == "FromDinner":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне."
        if mode_key == "SvalnyiGreh":
            return "Вы и миссис Блэнкеншип находитесь в ее спальне.\nВместе с вами находится Эдди, ее управляющий лавкой. Им движут к хозяйке отнюдь не деловые чувства."
        return "Итак, вы сидите за столом в гостях у вдовы Блэнкеншип и наслаждаетесь аппетитной домашней кухней."

    def becky_home_desc_default():
        return ArriveMode == ""

    def becky_home_desc_dances():
        return ArriveMode == "FromDances"

    def becky_home_desc_special():
        return ArriveMode in ("SvalnyiGreh", "FromDinner")

    def becky_home_table_visible():
        return ArriveMode == ""

    BeckyHomeRoom = Room(
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
            GameObject(
                object_id="bed",
                name="Большая кровать",
                description="Широкая кровать, занимающая центр комнаты Бекки.",
                actions=[
                    ObjectAction(action_id="examine_bed", label="Осмотреть кровать", hook="text", target="Большая кровать, занимающая центр спальни Бекки."),
                ],
            ),
            GameObject(
                object_id="chests",
                name="Сундуки вдоль стен",
                description="Вдоль стен стоят массивные сундуки, скамья и пара стульев.",
                actions=[
                    ObjectAction(action_id="examine_chests", label="Осмотреть сундуки", hook="text", target="Массивные сундуки и мебель делают обстановку спальни простой, но добротной."),
                ],
            ),
            GameObject(
                object_id="dinner_table",
                name="Накрытый стол",
                description="Если Бекки принимает вас как гостя, стол у нее накрыт на совесть.",
                actions=[
                    ObjectAction(action_id="examine_table", label="Осмотреть стол", hook="text", target="Для обычного домашнего ужина здесь все устроено удивительно щедро.", condition=becky_home_table_visible),
                ],
            ),
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="17:59"),
        custom_properties={
            "becky_house": True,
            "object_menu_label": "BeckyHomeObjectMenu",
        },
    )

label BeckyHome(arrive_mode=""):
    if int(BeckyHomeActive or 0) == 1 and str(CurLoc or "") == "BeckyHome" and str(arrive_mode or "") == "":
        call BeckyHomeRestore
        call screen main_ui
        jump BeckyHome
    $ BeckyHomeActive = 1
    $ ArriveMode = arrive_mode
    $ _becky_home_room = BeckyHomeRoom
    $ CurrentRoom = _becky_home_room
    $ CurLoc = "BeckyHome"
    $ location = CurLoc
    $ scene_image = becky_home_picture(ArriveMode)
    if str(scene_image or "").strip():
        $ _layout_last_picture = scene_image
    if navigation_only_mode_enabled():
        "Вы находитесь у вдовы Блэнкеншип дома."
        "[navigation_only_message()]"
        "[navigation_only_time_note()]"
        menu:
            "Вернуться к трактиру":
                jump StreetTavern
        return
    $ GirlName = 'becky'
    python:
        Becky.ensure_story_defaults()
        Inga.ensure_story_defaults()
        pregnancy.setdefault("inga", 0)
        PussyWetStart.setdefault(GirlName, Becky.arousal_value())
    $ _becky_home_room.mark_visited()

    $ _start_becky_sex = False
    if arrive_mode == 'FromDances' and Becky.story_value('visitedhome', 0) < 5:
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
        if Becky.story_value('EddieTryToFuck', 0) == 1 and Becky.story_value('visitedhome', 0) < 7:
            call BeckyEddieJoinFirst
        else:
            if Becky.story_value('visitedhome', 0) < 7:
                "Дав вам зайти, вдова закрыла дверь на ключ и обернулась к вам, сказав: 'Если детишки мои развлекаются, то почему в конце концов я не могу себе такого позволить? Иди же ко мне!' "
            else:
                "Вдова не позаботилась не то, что запереть дверь на ключ, но и даже полностью закрыть ее, и не теряя времени потащила вас к кровати. "
            "Вы и миссис Блэнкеншип находитесь в ее спальне."
        call ShowImageSeq('becky', 'sex', 'inroom', 3)
        $ _start_becky_sex = True
    else:
        $ BeckyAdmit = 0
        if arrive_mode == 'FromDances':
            "Ребекка завозилась с ключами, отпирая дверь. Это у нее заняло немного дольше времени, чем должно бы, так как вы все время игриво залазили ей под юбку, отвлекая ее от поисков нужного ключа. Наконец дверь отворилась и Бекки пригласила вас в дом: <br>'Заходи, Стефан, и пожалуй за стол.' "
            $ BeckyAdmit = 1
        else:
            "[_becky_home_room.descriptions[0].text] "
            if Becky.story_value('visitedhome', 0) < 3:
                if Becky.story_value('VisitScolded', 0) == 0:
                    "Она не очень-то была рада вашему визиту: 'Стефан, зачем ты пришел?! Мы же договаривались! Надеюсь, тебя никто не видел?' <br> 'Никто,' сказали вы глядя на вдову своими честными глазами. 'Но я просто хотел...' <br> Бекки однако, ваше желание мало интересовало. Она резко прервала вас: 'Не приходи больше, что люди подумают. Все, пока.'<br> И дверь перед вашим носом захлопнулась.  "
                    $ Becky.set_story_value('VisitScolded', 1)
                    $ Becky.apply_social_roll(8, 3, -1, 35, 3, -1)
                else:
                    "Увидев вас она рассердилась не на шутку: 'Стефан, тебе что, все нужно по 20 раз повторять?! Не приходи пока ко мне домой.' <br> 'Но я,' начали оправдываться вы, но поняли, что разговариваете с закрытой дубовой дверью. Изнутри послышался звук запираемого засова. Похоже, сейчас вам здесь не очень-то рады. "
                    $ Becky.apply_social_roll(8, 1, -1, 35, 1, -1)
                menu:
                    "В печали вернуться к трактиру":
                        jump StreetTavern
            elif player_state().appearance.current_dress != 'citydress':
                "Она тщательно осмотрела вас и строго сказала: 'Стефан, я же тебе говорила, ты должен быть одет скромно но прилично. А ты в чем пришел? Беги переодевайся!'\nС этими словами она захлопнула дверь перед вашим носом. Отчего-то вы почувствовали себя нашкодничавшим школьником."
                menu:
                    "Вернуться к трактиру переодеться":
                        jump StreetTavern
            else:
                "Она тщательно осмотрела вас и сказала: 'Что же ты встал на пороге, проходи скорей!'\nВы не замедлили воспользоваться приглашением и прошли в дом, прямо к накрытому столу. К вашей скромной трапезе из 6 блюд присоединился и Эдди.\nНе успели вы приступить к поглощению пищи, как услышали как хлопнула входная дверь"
                $ BeckyAdmit = 1
        if BeckyAdmit == 1:
            $ Becky.add_story_value('TimesVisited', 1)
            if Inga.var_int("Knowher", 0) >= 2:
                " и вскоре к вам за столом присоединились Ингенборг, старшая дочка соломенной вдовушки, вместе со своим хахалем Лукасом."
            elif Inga.var_int("Knowher", 0) == 1:
                " и на пороге показалась уже виденная вами парочка - Лукас и Ингенборг. Бекки повернулась к вам: 'Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.'\nВы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол. "
                $ Inga.set_var_int("Knowher", 2)
            else:
                " и на пороге показалось двое - высокая рыжеволосая девушка, похожая на хозяйку дома, в сопровождения парня чуть постарше ее. Бекки повернулась к вам: 'Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.'\nВы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол. "
                $ Inga.set_var_int("Knowher", 2)
            call ShowImage('becky', 'dinner', 'DinnerInga')
            if procedural_randint(1, 5, "becky_home_dinner_inga_legacy_%s" % int(dayspassed or 0)) == 1:
                " Вы присмотрелись к Инге и заметили, что перед ужином времени она не теряла, на ее рыжей шевелюре были видны следы спермы."
            if pregnancy.get('inga', 0) >= 120:
                " Одного взгляда на круглый живот Инги было достаточно, чтобы понять что она ведет активную половую жизнь."
            call IntBeckyGuest
            " Итак, вы сидите за столом в гостях у вдовы Блэнкеншип и наслаждаетесь аппетитной домашней кухней."
    if _start_becky_sex:
        $ Becky.set_arousal(PussyWetStart[GirlName])
        call cock_position(GirlName, 0)
        call check_visibility(GirlName)
        call IntBeckySex(GirlName)
        return
    call BeckyHomeRestore
    call screen main_ui
    jump BeckyHome


label BeckyHomeBuildActions:
    $ CurrentRoom = BeckyHomeRoom
    $ current_action_title = str(CurrentRoom.display_name or "Дом Бекки")
    $ current_action_content = None
    $ _becky_home_menu = CurrentRoom.build_menu_sections()
    $ current_action_items = list(_becky_home_menu.get("movement", [])) + list(_becky_home_menu.get("actions", []))
    return


label BeckyHomeRestore:
    $ CurrentRoom = BeckyHomeRoom
    $ CurLoc = "BeckyHome"
    $ location = CurLoc
    $ scene_image = becky_home_picture(ArriveMode)
    if str(scene_image or "").strip():
        $ _layout_last_picture = scene_image
    $ MainTxt = becky_home_restore_text()
    $ CurLocDesc = MainTxt
    call BeckyHomeBuildActions
    return


label BeckyHomeAfterSex:
    $ Becky.set_story_value_min("visitedhome", 2)
    $ MainTxt = becky_home_after_sex_text()
    $ CurLocDesc = MainTxt
    call BeckyHomeBuildActions
    call screen main_ui
    jump BeckyHome


label BeckyHomeObjectMenu(object_id=""):
    if str(object_id or "") != "":
        $ current_object_id = object_id
    $ object_id = current_object_id
    $ _becky_home_object = None
    python:
        for _room_object in BeckyHomeRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _becky_home_object = _room_object
                break

    if _becky_home_object is None:
        call BeckyHomeRestore
        return

    $ current_action_title = str(_becky_home_object.name or "Дом Бекки")
    $ current_action_content = None
    $ current_action_items = []
    $ MainTxt = str(_becky_home_object.description or "")
    $ CurLocDesc = MainTxt
    python:
        for _becky_action in _becky_home_object.visible_actions():
            _becky_args = tuple(getattr(_becky_action, "args", ()) or ())
            if _becky_action.hook == "text":
                current_action_items.append(MenuItem(_becky_action.label, Call("BeckyHomeObjectText", object_id, _becky_action.action_id)))
            elif _becky_action.hook == "call" and str(_becky_action.target or "") != "":
                current_action_items.append(MenuItem(_becky_action.label, Call(_becky_action.target, *_becky_args)))
            elif _becky_action.hook == "jump" and str(_becky_action.target or "") != "":
                current_action_items.append(MenuItem(_becky_action.label, Jump(_becky_action.target)))
        current_action_items.append(MenuItem("Назад", Jump("BeckyHome")))
    return


label BeckyHomeObjectText(object_id="", action_id=""):
    python:
        _becky_text = ""
        _becky_name = ""
        for _room_object in BeckyHomeRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _becky_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _becky_text = str(_room_action.target or "")
                    break
            break
        if _becky_text:
            MainTxt = _becky_text
            CurLocDesc = _becky_text
            current_action_title = _becky_name or "Дом Бекки"
    call BeckyHomeObjectMenu(object_id)
    return

