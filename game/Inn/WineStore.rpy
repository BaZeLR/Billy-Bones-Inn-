# WineStore.rpy
# Converted from WineStore.txt
# Handles the wine store location and menu logic

init python:
    def wine_store_clara_visible():
        return clara_visible_in_location("WineStore")

    def wine_store_alber_visible():
        return time != 0

    def wine_store_background_picture():
        if int(time or 0) == 0:
            picture = clara_wine_store_talk_picture()
        else:
            picture = alber_random_portrait()
        if str(picture or "").strip():
            return picture
        return "images/clara/wineSellar_clara_talk.png"

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
        npcs=[
            {"npc_id": "clara", "name": "Кларисса", "condition": wine_store_clara_visible, "talk_label": "IntClaraTalk"},
            {"npc_id": "alber", "name": "Альбер", "condition": wine_store_alber_visible, "talk_label": "IntAlberTalk"},
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            time_slots=[0, 1, 2],
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
    if not _wine_room.is_open(week, time):
        $ MainTxt = _wine_room.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        jump WineStoreView
    
    # Assign grocer name
    if time == 0:
        $ GrocerName = 'Кларисса'
    else:
        $ GrocerName = 'Альбер'
    
    $ MainTxt = _wine_room.descriptions[0].text
    $ CurLocDesc = MainTxt

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        jump WineStoreView
    
    # Character interaction
    if time == 0:
        $ MainTxt += "\n\nСейчас утро, и за прилавком стоит Кларисса, старшая дочь мессира Легаре. Это привлекательная блондинка чуть младше вас."
        if dayspassed > 40 and dayspassed <= 90:
            $ MainTxt += "\n\nВы знаете, что ваша ваша сестра Мелисса с ней недавно подружилась."
        elif dayspassed > 90:
            $ MainTxt += "\n\nОна с вашей сестрой Мелиссой - лучшие подруги."
        $ MainTxt += "\n\nВы можете с ней поболтать."
        if not clara_can_start_social_events():
            $ MainTxt += "\n\nПравда, вам кажется, что Кларисса относится к вам пока лишь как к знакомому покупателю."
        # Show Clara's image
        $ _clara_picture = clara_wine_store_talk_picture()
        if str(_clara_picture or "").strip():
            call ShowImage("", "", _clara_picture)
    else:
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

    $ CurLocDesc = MainTxt
    $ WineStoreSavedText = MainTxt
    call WineStoreBuildActions
    jump WineStoreView


label WineStoreView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump WineStoreView


label WineStoreBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _wine_object in WineStoreRoom.visible_objects():
            current_action_items.append(MenuItem(_wine_object.name, Call("WineStoreObjectMenu", _wine_object.object_id)))
        current_action_items.append(MenuItem("Купить вино", Call("WineStoreBuyMenu")))

    if time == 0:
        $ current_action_items.append(MenuItem("Поговорить с Клариссой", Call("IntClaraTalk")))
    else:
        $ current_action_items.append(MenuItem("Поговорить с Альбером", Call("IntAlberTalk")))

    $ current_action_items.append(MenuItem("Вернуться на рынок", Jump("MarketPlace")))
    return


label WineStoreObjectMenu(object_id=""):
    $ _wine_object = None
    python:
        for _room_object in WineStoreRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _wine_object = _room_object
                break

    if _wine_object is None:
        call WineStoreBuildActions
        return

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

    $ current_action_items.append(MenuItem("Назад", Call("WineStoreRestore")))
    return


label WineStoreObjectText(object_id="", action_id=""):
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
            current_action_title = _wine_name or "Действия"
    call WineStoreObjectMenu(object_id)
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
    $ current_action_items.append(MenuItem("Назад", Call("WineStoreRestore")))
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
    call WineStoreBuildActions
    return


label WineStoreRestore:
    $ MainTxt = WineStoreSavedText or WineStoreRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    call WineStoreBuildActions
    return
