# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# WineStore.rpy
# Converted from WineStore.txt
# Handles the wine store location and menu logic

default WineStoreSavedText = ""

init python:
    def wine_store_clara_visible():
        return str(getLocation("clara") or "") == "WineStore" and bool(npc_can_talk_now("clara"))

    def wine_store_alber_visible():
        return str(getLocation("alber") or "") == "WineStore" and bool(npc_can_talk_now("alber"))

    def wine_store_open_now():
        current_week = int(week or 0)
        current_minutes = int(clock_minutes or 0) % 1440
        if current_week == 7:
            return False
        if current_week == 5:
            return 8 * 60 <= current_minutes <= 15 * 60
        return 8 * 60 <= current_minutes <= 17 * 60

    def clara_stable_wine_store_talk_picture():
        candidates = [
            "images/clara/wineSellar_clara_talk.png",
            "images/clara/wine_sellar_clara_talk_2.png",
            "images/clara/wineSellar_clara_talk_3.png",
            "images/clara/wineSellar_clara_talk_4.png",
            "images/clara/wineSellar_clara_talk_5.png",
            "images/clara/wineSellar_clara_talk_6.png",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return loadable[0] if len(loadable) > 0 else ""

    def wine_store_background_picture():
        if wine_store_clara_visible():
            picture = clara_stable_wine_store_talk_picture()
        elif wine_store_alber_visible():
            picture = alber_random_portrait()
        else:
            picture = clara_stable_wine_store_talk_picture()
        if str(picture or "").strip():
            return picture
        return "images/clara/wineSellar_clara_talk.png"

    def wine_store_room_action_items():
        items = []
        items.extend(WineStoreRoom.build_object_items())
        if story_event_available("WineStore", "clara_paintings"):
            items.append(MenuItem("Поговорить с Клариссой о рисунках", Call("checkTriggers", "WineStore", "clara_paintings", 0)))
        items.extend(WineStoreRoom.build_exit_items())
        return items

    WineStoreRoom = Room(
        code_name="WineStore",
        display_name="Винный погребок",
        bg_picture="images/clara/wineSellar_clara_talk.png",
        descriptions=[
            RoomDescription(
                text="Вы в винном погребке мессира Легаре. По всему погребку стоят бочки с разными винами. У задней стены расположен вход в подвал, еще больше забитый стеллажами с бутылками и огромными бочками с вином, стоящими одна на другой.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на рынок", target="MarketPlace"),
        ],
        game_items=[
            GameObject(
                object_id="wine_stock",
                name="Бочки с вином",
                description="Ряды бочек и бутылок, из которых пополняются запасы вашего трактира.",
                actions=[
                    ObjectAction(action_id="buy_wine", label="Купить вино", hook="call", target="WineStoreBuyMenu"),
                    ObjectAction(action_id="examine_wine", label="Осмотреть товар", hook="text", target="Повсюду бочки, бутылки и винный дух. Сразу видно, что здесь торгуют всерьез."),
                ],
            ),
            GameObject(
                object_id="cellar",
                name="Подвал",
                description="Дальше вглубь уходит еще более тесный и заставленный подвал.",
                actions=[
                    ObjectAction(action_id="examine_cellar", label="Осмотреть подвал", hook="text", target="Подвал забит винными запасами еще плотнее, чем сама лавка."),
                ],
            ),
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            start="08:00",
            end="17:00",
            condition=wine_store_open_now,
            closed_text="В это время погребок закрыт.",
        ),
        custom_properties={
            "shop_feature": "wine",
            "object_menu_label": "WineStoreObjectMenu",
        },
    )

label WineStore:
    scene black
    call EnterLocation("WineStore")
    $ CurrentRoom = WineStoreRoom
    $ CurLoc = "WineStore"
    $ location = CurLoc
    $ scene_image = wine_store_background_picture()
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ Friends.setdefault("clara", 0)
    $ Talked.setdefault("clara", 0)
    $ AlberVar.setdefault("FightYouAmanda", 0)
    $ _wine_room = WineStoreRoom
    $ WineStoreSavedText = ""

    # Check if the store is closed
    if not _wine_room.is_open():
        $ MainTxt = _wine_room.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ current_action_items = WineStoreRoom.build_exit_items()
        $ _wine_ui_return = None
        while _wine_ui_return is None:
            call screen main_ui
            $ _wine_ui_return = _return
        jump WineStore
    
    $ _wine_clara_visible = wine_store_clara_visible()
    $ _wine_alber_visible = wine_store_alber_visible()

    # Assign grocer name from the NPC schedule, not the display-only time slot.
    if _wine_clara_visible:
        $ GrocerName = 'Кларисса'
    elif _wine_alber_visible:
        $ GrocerName = 'Альбер'
    else:
        $ GrocerName = 'продавец'
    
    $ MainTxt = _wine_room.descriptions[0].text
    $ CurLocDesc = MainTxt

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = WineStoreRoom.build_exit_items()
        $ _wine_ui_return = None
        while _wine_ui_return is None:
            call screen main_ui
            $ _wine_ui_return = _return
        jump WineStore
    
    # Character interaction
    if _wine_clara_visible:
        $ MainTxt += "\n\nСейчас утро, и за прилавком стоит Кларисса, старшая дочь мессира Легаре. Это привлекательная блондинка чуть младше вас."
        if dayspassed > 40 and dayspassed <= 90:
            $ MainTxt += "\n\nВы знаете, что Мелисса с ней недавно подружилась."
        elif dayspassed > 90:
            $ MainTxt += "\n\nОна с Мелиссой - лучшие подруги."
        $ MainTxt += "\n\nВы можете с ней поболтать."
        if not Clara.can_start_social_events():
            $ MainTxt += "\n\nПравда, вам кажется, что Кларисса относится к вам пока лишь как к знакомому покупателю."
        # Show Clara's image
        $ _clara_picture = clara_stable_wine_store_talk_picture()
        if str(_clara_picture or "").strip():
            call ShowImage("", "", _clara_picture)
    elif _wine_alber_visible:
        # Alber is present
        if AlberVar['FightYouAmanda'] == 0:
            $ MainTxt += "\n\nЗа прилавком стоит сам хозяин погребка, мессир Альбер Легаре. Это высокий импозантный мужчина тридцати с лишним лет. Вы знаете, что он женат и у него семья. Его старшая дочка, Кларисса, помогает ему в погребке по утрам."
        else:
            $ fight_text = 'вашу ругань' if AlberVar['FightYouAmanda'] == 2 else 'ваш с ним небольшой дружеский спарринг'
            $ MainTxt += "\n\nЗа прилавком стоит сам хозяин, месье Легаре. И он очень мрачно смотрит на вас. Похоже, он принял [fight_text] близко к сердцу."
        $ MainTxt += "\n\nВы можете с ним поболтать."
        # Show Alber's image
        $ _alber_picture = alber_random_portrait()
        if str(_alber_picture or "").strip():
            call ShowImage("", "", _alber_picture)
    else:
        $ MainTxt += "\n\nСейчас у прилавка никого нет."

    $ CurLocDesc = MainTxt
    $ WineStoreSavedText = MainTxt
    call WineStoreRoomActions
    $ _wine_ui_return = None
    while _wine_ui_return is None:
        call screen main_ui
        $ _wine_ui_return = _return
    jump WineStore


label WineStoreRoomActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = wine_store_room_action_items()
    $ action_menu_specs = []
    return


label WineStoreObjectMenu(object_id="", preserve_text=False):
    $ _wine_object = None
    python:
        for _room_object in WineStoreRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _wine_object = _room_object
                break

    if _wine_object is None:
        call WineStoreRoomActions
        return

    if not preserve_text:
        $ MainTxt = _wine_object.description
        $ CurLocDesc = MainTxt
    $ current_action_title = _wine_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _wine_action in _wine_object.visible_actions():
            if _wine_action.hook == "text":
                current_action_items.append(MenuItem(_wine_action.label, Call("WineStoreObjectText", object_id, _wine_action.action_id)))
            elif _wine_action.hook == "jump" and str(_wine_action.target or "") != "":
                current_action_items.append(MenuItem(_wine_action.label, Jump(_wine_action.target)))
            elif _wine_action.hook == "call" and str(_wine_action.target or "") != "":
                _wine_args = tuple(getattr(_wine_action, "args", ()) or ())
                current_action_items.append(MenuItem(_wine_action.label, Call(_wine_action.target, *_wine_args)))

    $ current_action_items.append(MenuItem("Назад", Call("WineStoreRoomActions")))
    return


label WineStoreObjectText(object_id="", action_id=""):
    $ _wine_title = "Действия"
    python:
        _wine_text = ""
        _wine_name = ""
        for _room_object in WineStoreRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _wine_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _wine_text = str(_room_action.target or "")
                    break
            break
        if _wine_text:
            MainTxt = _wine_text
            CurLocDesc = _wine_text
            _wine_title = _wine_name or "Действия"
    call WineStoreObjectMenu(object_id, True)
    $ current_action_title = _wine_title
    return


label WineStoreBuyMenu:
    $ current_action_title = "Покупка вина"
    $ current_action_content = None
    $ MainTxt = "В этом погребке вы можете купить вино для вашего трактира, по 14 мараведи за бочонок."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Ничего не покупать", Call("WineStoreBuyApply", 0, 0, 0))]
    if money >= 14:
        $ current_action_items.append(MenuItem("Купить один бочонок", Call("WineStoreBuyApply", 14, 10, 1)))
    if money >= 14 * 5:
        $ current_action_items.append(MenuItem("Купить пять бочонков", Call("WineStoreBuyApply", 14 * 5, 50, 5)))
    if money >= 14 * 20:
        $ current_action_items.append(MenuItem("Купить двадцать бочонков", Call("WineStoreBuyApply", 14 * 20, 200, 20)))
    if money >= 14 * 50:
        $ current_action_items.append(MenuItem("Купить пятьдесят бочонков", Call("WineStoreBuyApply", 14 * 50, 500, 50)))
    if money >= 14 * 200:
        $ current_action_items.append(MenuItem("Купить двести бочонков", Call("WineStoreBuyApply", 14 * 200, 2000, 200)))
    $ current_action_items.append(MenuItem("Назад", Call("WineStoreRoomActions")))
    return


label WineStoreBuyApply(cost=0, add_amount=0, barrel_count=0):
    if int(barrel_count or 0) == 0:
        $ MainTxt = "Вы решили пока ничего не покупать."
        call stat
    else:
        $ winenum += int(add_amount or 0)
        $ money -= int(cost or 0)
        if int(barrel_count or 0) == 1:
            $ MainTxt = "Вы купили бочонок вина. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        elif int(barrel_count or 0) == 5:
            $ MainTxt = "Вы купили пять бочонков вина. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        elif int(barrel_count or 0) == 20:
            $ MainTxt = "Вы купили двадцать бочонков вина. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        elif int(barrel_count or 0) == 50:
            $ MainTxt = "Вы купили пятьдесят бочонков вина. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        else:
            $ MainTxt = "Вы купили двести бочонков вина. [GrocerName] говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно."
        call stat
    $ CurLocDesc = MainTxt
    $ WineStoreSavedText = MainTxt
    call WineStoreRoomActions
    return

