# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# WineStore.rpy
# Converted from WineStore.txt
# Handles the wine store location and menu logic

default WineStoreSavedText = ""

init python:
    import renpy.exports as renpy

    def wine_store_state():
        return WineStoreRoom.custom_properties

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

    def wine_store_set_notice(text=""):
        WineStoreRoom.custom_properties["notice_text"] = str(text or "")

    def wine_store_take_notice():
        room_state = WineStoreRoom.custom_properties
        text = str(room_state.get("notice_text", "") or "")
        room_state["notice_text"] = ""
        return text

    def wine_store_grocer_name():
        if wine_store_clara_visible():
            return "Кларисса"
        if wine_store_alber_visible():
            return "Альбер"
        return "продавец"

    def wine_store_entry_text():
        notice_text = wine_store_take_notice()
        if notice_text:
            return notice_text
        base_text = WineStoreRoom.descriptions[0].text
        if wine_store_clara_visible():
            base_text += "\n\nСейчас утро, и за прилавком стоит Кларисса, старшая дочь мессира Легаре. Это привлекательная блондинка чуть младше вас."
            if dayspassed > 40 and dayspassed <= 90:
                base_text += "\n\nВы знаете, что Мелисса с ней недавно подружилась."
            elif dayspassed > 90:
                base_text += "\n\nОна с Мелиссой - лучшие подруги."
            base_text += "\n\nВы можете с ней поболтать."
            if not Clara.can_start_social_events():
                base_text += "\n\nПравда, вам кажется, что Кларисса относится к вам пока лишь как к знакомому покупателю."
        elif wine_store_alber_visible():
            if Alber.var_int("FightYouAmanda", 0) == 0:
                base_text += "\n\nЗа прилавком стоит сам хозяин погребка, мессир Альбер Легаре. Это высокий импозантный мужчина тридцати с лишним лет. Вы знаете, что он женат и у него семья. Его старшая дочка, Кларисса, помогает ему в погребке по утрам."
            else:
                fight_text = "вашу ругань" if Alber.var_int("FightYouAmanda", 0) == 2 else "ваш с ним небольшой дружеский спарринг"
                base_text += "\n\nЗа прилавком стоит сам хозяин, месье Легаре. И он очень мрачно смотрит на вас. Похоже, он принял %s близко к сердцу." % fight_text
            base_text += "\n\nВы можете с ним поболтать."
        else:
            base_text += "\n\nСейчас у прилавка никого нет."
        return base_text

    def wine_store_find_visible_object(object_id):
        object_key = str(object_id or "")
        for room_object in WineStoreRoom.visible_objects():
            if str(getattr(room_object, "object_id", "") or "") == object_key:
                return room_object
        return None

    def wine_store_object_text_payload(object_id, action_id):
        room_object = wine_store_find_visible_object(object_id)
        if room_object is None:
            return "", ""
        object_name = str(getattr(room_object, "name", "") or "")
        action_key = str(action_id or "")
        for room_action in room_object.visible_actions():
            if str(getattr(room_action, "action_id", "") or "") == action_key:
                return str(room_action.target or ""), object_name
        return "", object_name

    def wine_store_object_menu_payload(object_id):
        room_object = wine_store_find_visible_object(object_id)
        if room_object is None:
            return None
        menu_items = []
        for room_action in room_object.visible_actions():
            if room_action.hook == "text":
                menu_items.append(MenuItem(room_action.label, Function(wine_store_show_object_text_state, object_id, room_action.action_id)))
            elif room_action.hook == "jump" and str(room_action.target or "") != "":
                menu_items.append(MenuItem(room_action.label, Jump(room_action.target)))
            elif room_action.hook == "call" and str(room_action.target or "") != "":
                action_args = tuple(getattr(room_action, "args", ()) or ())
                menu_items.append(MenuItem(room_action.label, Call(room_action.target, *action_args)))
        return {
            "name": str(getattr(room_object, "name", "") or ""),
            "description": str(getattr(room_object, "description", "") or ""),
            "items": menu_items,
        }

    def wine_store_open_object_menu_state(object_id="", preserve_text=False):
        global MainTxt, CurLocDesc, current_action_title, current_action_content, current_action_items, current_object_id

        payload = wine_store_object_menu_payload(object_id)
        current_object_id = str(object_id or "")
        if payload is None:
            current_action_title = "Действия"
            current_action_content = None
            current_action_items = wine_store_room_action_items()
        else:
            if not bool(preserve_text):
                MainTxt = str(payload.get("description", "") or "")
                CurLocDesc = MainTxt
            current_action_title = str(payload.get("name", "") or "Действия")
            current_action_content = None
            current_action_items = list(payload.get("items", []) or [])
            current_action_items.append(MenuItem("Назад", Jump("WineStore")))
        renpy.restart_interaction()

    def wine_store_show_object_text_state(object_id="", action_id=""):
        global MainTxt, CurLocDesc, current_action_title

        wine_text, wine_name = wine_store_object_text_payload(object_id, action_id)
        if wine_text:
            MainTxt = wine_text
            CurLocDesc = wine_text
            current_action_title = wine_name or "Действия"
        wine_store_open_object_menu_state(object_id, True)

    def wine_store_room_action_items():
        items = []
        for room_object in WineStoreRoom.visible_objects():
            items.append(MenuItem(
                str(getattr(room_object, "name", "") or ""),
                Function(wine_store_open_object_menu_state, str(getattr(room_object, "object_id", "") or "")),
            ))
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
                    ObjectAction(action_id="buy_wine", label="Купить вино", hook="call", target="WineStoreBuyStockMenu"),
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
            "notice_text": "",
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
    $ GrocerName = wine_store_grocer_name()
    $ _wine_room = WineStoreRoom
    $ WineStoreSavedText = ""

    if not _wine_room.is_open(week, time):
        $ MainTxt = _wine_room.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ scene_image = "images/general/closedVenue default.png"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ current_action_items = WineStoreRoom.build_exit_items()
        call screen main_ui
        jump WineStore

    $ MainTxt = wine_store_entry_text()
    $ CurLocDesc = MainTxt

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = WineStoreRoom.build_exit_items()
        call screen main_ui
        jump WineStore

    if wine_store_clara_visible():
        $ _clara_picture = clara_stable_wine_store_talk_picture()
        if str(_clara_picture or "").strip():
            call ShowImage("", "", _clara_picture)
    elif wine_store_alber_visible():
        $ _alber_picture = alber_random_portrait()
        if str(_alber_picture or "").strip():
            vscene _alber_picture

    $ CurLocDesc = MainTxt
    $ WineStoreSavedText = MainTxt
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = wine_store_room_action_items()
    call screen main_ui
    jump WineStore


label WineStoreBuyStockMenu:
    $ current_action_title = "Покупка вина"
    $ current_action_content = None
    $ MainTxt = "В этом погребке вы можете купить вино для вашего трактира, по 14 мараведи за бочонок."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Ничего не покупать", Call("WineStoreBuyStockApply", 0, 0, 0))]
    if money >= 14:
        $ current_action_items.append(MenuItem("Купить один бочонок", Call("WineStoreBuyStockApply", 14, 10, 1)))
    if money >= 14 * 5:
        $ current_action_items.append(MenuItem("Купить пять бочонков", Call("WineStoreBuyStockApply", 14 * 5, 50, 5)))
    if money >= 14 * 20:
        $ current_action_items.append(MenuItem("Купить двадцать бочонков", Call("WineStoreBuyStockApply", 14 * 20, 200, 20)))
    if money >= 14 * 50:
        $ current_action_items.append(MenuItem("Купить пятьдесят бочонков", Call("WineStoreBuyStockApply", 14 * 50, 500, 50)))
    if money >= 14 * 200:
        $ current_action_items.append(MenuItem("Купить двести бочонков", Call("WineStoreBuyStockApply", 14 * 200, 2000, 200)))
    $ current_action_items.append(MenuItem("Назад", Jump("WineStore")))
    call ReturnToMainUI
    return


label WineStoreBuyStockApply(cost=0, add_amount=0, barrel_count=0):
    if int(barrel_count or 0) == 0:
        $ MainTxt = "Вы решили пока ничего не покупать."
    else:
        $ winenum += int(add_amount or 0)
        $ money -= int(cost or 0)
        if int(barrel_count or 0) == 1:
            $ MainTxt = "Вы купили бочонок вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_grocer_name()
        elif int(barrel_count or 0) == 5:
            $ MainTxt = "Вы купили пять бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_grocer_name()
        elif int(barrel_count or 0) == 20:
            $ MainTxt = "Вы купили двадцать бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_grocer_name()
        elif int(barrel_count or 0) == 50:
            $ MainTxt = "Вы купили пятьдесят бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_grocer_name()
        else:
            $ MainTxt = "Вы купили двести бочонков вина. %s говорит вам, что ваш заказ будет доставлен в \"Дикий жеребец\" немедленно." % wine_store_grocer_name()
        call stat
    $ CurLocDesc = MainTxt
    $ WineStoreSavedText = MainTxt
    $ wine_store_set_notice(MainTxt)
    jump WineStore
