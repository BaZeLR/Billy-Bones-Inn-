init python:
    import renpy

    HUNTER_CLUB_TRADE_MAX_QTY = 99

    HUNTER_CLUB_BUY_STOCK = [
        {"item_id": "drink_ale_001", "price": 2},
        {"item_id": "dog_bone_001", "price": 1},
        {"item_id": "hunting_trap_001", "price": 18},
        {"item_id": "lumber_001", "price": 8},
        {"item_id": "arrows_001", "price": 6},
        {"item_id": "droplets_001", "price": 11},
        {"item_id": "cork_001", "price": 1},
        {"item_id": "flint_001", "price": 4},
        {"item_id": "rope_001", "price": 9},
        {"item_id": "torch_001", "price": 5},
        {"item_id": "gunpowder_001", "price": 16},
        {"item_id": "weapon_oil_001", "price": 7},
        {"item_id": "bandage_001", "price": 4},
        {"item_id": "healing_potion_001", "price": 14},
    ]

    HUNTER_CLUB_SELL_ITEM_IDS = (
        "wolf_skin_001",
        "boar_fang_001",
        "boar_meat_001",
        "bear_claw_001",
        "bear_fur_brown_001",
        "bear_fur_grizzly_001",
        "special_mushroom_001",
        "special_herbs_001",
        "lavender_001",
        "wild_rose_001",
        "moss_001",
        "dried_moss_001",
        "cloth_scrap_001",
        "berries_001",
        "mushroom_001",
        "honey_comb_001",
        "soap_001",
        "ethanol_001",
        "energy_tea_001",
        "torch_001",
        "rope_001",
        "gunpowder_001",
        "bandage_001",
        "healing_potion_001",
        "fire_bomb_001",
        "libido_tincture_001",
    )

    def hunter_club_offer_data(item_id):
        item_key = str(item_id or "").strip()
        for entry in list(HUNTER_CLUB_BUY_STOCK or []):
            if str(entry.get("item_id", "") or "") == item_key:
                return dict(entry)
        return {}

    def hunter_club_buy_entries():
        entries = []
        for entry in list(HUNTER_CLUB_BUY_STOCK or []):
            item_id = str(entry.get("item_id", "") or "")
            item_obj = get_game_item(item_id)
            if item_obj is None:
                continue
            entries.append({
                "item_id": item_id,
                "name": str(getattr(item_obj, "name", item_id) or item_id),
                "price": int(entry.get("price", getattr(item_obj, "price", 0)) or 0),
            })
        return entries

    def hunter_club_sell_entries():
        entries = []
        for item_id in list(HUNTER_CLUB_SELL_ITEM_IDS or []):
            item_obj = get_game_item(item_id)
            item_count = int(_player_item_count_by_id(item_id) or 0)
            if item_obj is None or item_count <= 0:
                continue
            item_price = max(0, int(getattr(item_obj, "price", 0) or 0))
            if item_price <= 0:
                continue
            entries.append({
                "item_id": item_id,
                "name": str(getattr(item_obj, "name", item_id) or item_id),
                "count": item_count,
                "price": item_price,
                "total_price": item_count * item_price,
            })
        return entries

    def hunter_club_buy_max_quantity(item_id):
        offer = hunter_club_offer_data(item_id)
        item_obj = get_game_item(item_id)
        if not offer or item_obj is None:
            return 0
        price_each = max(0, int(offer.get("price", getattr(item_obj, "price", 0)) or 0))
        if price_each <= 0:
            return 0
        return max(0, min(HUNTER_CLUB_TRADE_MAX_QTY, int(money or 0) // price_each))

    def hunter_club_sell_max_quantity(item_id):
        return max(0, min(HUNTER_CLUB_TRADE_MAX_QTY, int(_player_item_count_by_id(item_id) or 0)))

    def hunter_club_trade_entries(trade_mode="buy"):
        mode = str(trade_mode or "buy").strip().lower()
        source_entries = hunter_club_buy_entries() if mode == "buy" else hunter_club_sell_entries()
        rows = []
        for entry in list(source_entries or []):
            item_id = str(entry.get("item_id", "") or "").strip()
            if item_id == "":
                continue
            item_obj = get_game_item(item_id)
            if item_obj is None:
                continue
            rows.append({
                "item_id": item_id,
                "name": str(getattr(item_obj, "name", item_id) or item_id),
                "price": max(0, int(entry.get("price", getattr(item_obj, "price", 0)) or 0)),
                "owned_qty": int(_player_item_count_by_id(item_id) or 0),
                "max_qty": hunter_club_buy_max_quantity(item_id) if mode == "buy" else hunter_club_sell_max_quantity(item_id),
            })
        return rows

    def hunter_club_trade_selected_qty(item_id):
        item_key = str(item_id or "").strip()
        if item_key == "" or not isinstance(HunterClubTradeSelection, dict):
            return 0
        return max(0, int(HunterClubTradeSelection.get(item_key, 0) or 0))

    def hunter_club_trade_set_qty(item_id, qty, trade_mode="buy"):
        item_key = str(item_id or "").strip()
        mode = str(trade_mode or HunterClubTradeMode or "buy").strip().lower()
        if item_key == "":
            return
        max_qty = hunter_club_buy_max_quantity(item_key) if mode == "buy" else hunter_club_sell_max_quantity(item_key)
        HunterClubTradeSelection[item_key] = max(0, min(int(qty or 0), int(max_qty or 0)))
        renpy.restart_interaction()

    def hunter_club_trade_change_qty(item_id, delta, trade_mode="buy"):
        hunter_club_trade_set_qty(item_id, hunter_club_trade_selected_qty(item_id) + int(delta or 0), trade_mode)

    def hunter_club_trade_reset(mode="buy"):
        store = renpy.store
        store.HunterClubTradeMode = str(mode or "buy").strip().lower()
        store.HunterClubTradeSelection = {}
        for entry in list(hunter_club_trade_entries(store.HunterClubTradeMode) or []):
            store.HunterClubTradeSelection[str(entry.get("item_id", "") or "")] = 0

    def hunter_club_trade_total(mode="buy"):
        total = 0
        for entry in list(hunter_club_trade_entries(mode) or []):
            total += int(entry.get("price", 0) or 0) * hunter_club_trade_selected_qty(entry.get("item_id", ""))
        return max(0, int(total or 0))

    def hunter_club_trade_selected_count(mode="buy"):
        total = 0
        for entry in list(hunter_club_trade_entries(mode) or []):
            total += hunter_club_trade_selected_qty(entry.get("item_id", ""))
        return max(0, int(total or 0))

    def hunter_club_trade_summary_text(mode="buy"):
        mode_value = str(mode or HunterClubTradeMode or "buy").strip().lower()
        if len(list(hunter_club_trade_entries(mode_value) or [])) <= 0:
            return "Список пуст." if mode_value == "buy" else "Сейчас вам нечего продавать."
        selected_count = hunter_club_trade_selected_count(mode_value)
        total_price = hunter_club_trade_total(mode_value)
        if mode_value == "buy":
            if selected_count <= 0:
                return "Выберите товары и укажите количество. Луиза сразу назовет общую цену покупки."
            return "К покупке отмечено %s ед. товара. Общая цена: %s мараведи." % (selected_count, total_price)
        if selected_count <= 0:
            return "Отметьте добычу и укажите количество для продажи."
        return "К продаже отмечено %s ед. товара. Луиза заплатит: %s мараведи." % (selected_count, total_price)

    def hunter_club_apply_trade(mode="buy"):
        global money

        mode_value = str(mode or HunterClubTradeMode or "buy").strip().lower()
        applied_rows = []
        total_price = 0

        for entry in list(hunter_club_trade_entries(mode_value) or []):
            item_id = str(entry.get("item_id", "") or "").strip()
            qty = hunter_club_trade_selected_qty(item_id)
            price_each = max(0, int(entry.get("price", 0) or 0))
            if item_id == "" or qty <= 0 or price_each <= 0:
                continue

            max_qty = hunter_club_buy_max_quantity(item_id) if mode_value == "buy" else hunter_club_sell_max_quantity(item_id)
            qty = min(qty, max_qty)
            if qty <= 0:
                continue

            if mode_value == "buy":
                for _unused_trade_unit in range(qty):
                    _player_add_item_by_id(item_id)
            else:
                for _unused_trade_unit in range(qty):
                    _player_remove_item_by_id(item_id)

            total_price += price_each * qty
            applied_rows.append("%s x%s" % (str(entry.get("name", item_id) or item_id), qty))

        if len(applied_rows) <= 0:
            return {"ok": False, "text": "Сначала выберите товар и количество."}

        if mode_value == "buy":
            if int(money or 0) < total_price:
                return {"ok": False, "text": "У вас не хватает денег на выбранную покупку."}
            money -= total_price
            return {"ok": True, "text": "Толстая Луиза складывает для вас: %s. Всего вы платите %s мараведи." % (", ".join(applied_rows), total_price)}

        money += total_price
        return {"ok": True, "text": "Толстая Луиза принимает у вас: %s. Всего она платит %s мараведи." % (", ".join(applied_rows), total_price)}

    def hunter_club_main_text():
        return (
            "Вы входите в охотничий клуб на рыночной площади. Внутри пахнет шкурами, сушеными травами, "
            "смолой и дешевым элем. На стенах развешаны старые луки, кабаньи головы, рога и потемневшие "
            "трофеи, а за широким прилавком хозяйничает толстая Луиза.\n\n"
            "Здесь можно купить охотничьи припасы и сбыть лесную добычу."
        )

    def hunter_club_restore_scene_state():
        store = renpy.store
        room_text = hunter_club_main_text()
        store.MainTxt = room_text
        store.CurLocDesc = room_text
        store.HunterClubTradeMode = ""
        store.HunterClubTradeSelection = {}
        renpy.hide_screen("hunter_club_trade_overlay")
        main_ui_restore_room_scene_state()

    def hunter_club_buy_item(item_id, quantity=1):
        global money

        item_key = str(item_id or "").strip()
        offer = hunter_club_offer_data(item_key)
        item_obj = get_game_item(item_key)
        qty = max(1, int(quantity or 1))

        if not item_key or not offer or item_obj is None:
            return {"ok": False, "text": "Луиза качает головой: такого товара у нее сейчас нет."}

        total_cost = max(0, int(offer.get("price", getattr(item_obj, "price", 0)) or 0)) * qty
        if int(money or 0) < total_cost:
            return {"ok": False, "text": "У вас не хватает денег на эту покупку."}

        for _unused_buy_unit in range(qty):
            _player_add_item_by_id(item_key)
        money -= total_cost

        item_name = str(getattr(item_obj, "name", item_key) or item_key)
        return {
            "ok": True,
            "text": "Толстая Луиза отсчитывает вам {}. Покупка обходится в {} мараведи.".format(item_name, total_cost),
            "item_id": item_key,
            "quantity": qty,
            "total_cost": total_cost,
        }

    def hunter_club_sell_item(item_id, quantity=0):
        global money

        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        available = int(_player_item_count_by_id(item_key) or 0)
        if item_obj is None or available <= 0:
            return {"ok": False, "text": "Продавать сейчас нечего."}

        price_each = max(0, int(getattr(item_obj, "price", 0) or 0))
        if price_each <= 0:
            return {"ok": False, "text": "Луиза не хочет брать это на продажу."}

        qty = available if int(quantity or 0) <= 0 else min(available, max(1, int(quantity or 1)))
        for _unused_sell_unit in range(qty):
            _player_remove_item_by_id(item_key)
        total_price = price_each * qty
        money += total_price

        item_name = str(getattr(item_obj, "name", item_key) or item_key)
        return {
            "ok": True,
            "text": "Толстая Луиза осматривает товар и платит вам {} мараведи за {}.".format(total_price, item_name),
            "item_id": item_key,
            "quantity": qty,
            "total_price": total_price,
        }

    HunterClubRoom = Room(
        code_name="HunterClub",
        display_name="Охотничий клуб",
        bg_picture="images/general/hunter_store.jpg",
        descriptions=[
            RoomDescription(
                text="Охотничий клуб прячется за неприметной дверью на рыночной площади. Здесь держат припасы, меняются байками о звериных тропах и сбывают лесную добычу.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на рынок", target="MarketPlace"),
        ],
        game_items=[
            GameObject(
                object_id="luise_counter",
                name="Толстая Луиза",
                description="Полная, хозяйственная Луиза ведет дела клуба и зорко следит за ценами на добычу и припасы.",
                actions=[
                    ObjectAction(action_id="talk_luise", label="Поговорить с Луизой", hook="call", target="HunterClubLuiseTalk"),
                    ObjectAction(action_id="buy_goods", label="Купить товары", hook="call", target="HunterClubBuyMenu"),
                    ObjectAction(action_id="sell_loot", label="Продать добычу", hook="call", target="HunterClubSellMenu"),
                ],
            ),
            GameObject(
                object_id="hunter_goods",
                name="Охотничьи товары",
                description="На полках лежат веревки, факелы, кремни, стрелы, дробь, порох, масло для оружия и другие полезные вещи для лесной вылазки.",
                actions=[
                    ObjectAction(action_id="inspect_goods", label="Осмотреть товары", hook="text", target="Среди запасов хватает полезного: стрелы, дробь, ловушки, веревки, факелы, порох, оружейное масло, собачьи кости и даже кружки дешевого эля."),
                    ObjectAction(action_id="buy_hunter_goods", label="Купить товары", hook="call", target="HunterClubBuyMenu"),
                ],
            ),
            GameObject(
                object_id="hunter_trophies",
                name="Трофеи на стенах",
                description="Старые головы, клыки, шкуры и когти висят по стенам и служат лучшей рекламой для клуба.",
                actions=[
                    ObjectAction(action_id="inspect_trophies", label="Осмотреть трофеи", hook="text", target="На стенах развешаны старые волчьи шкуры, облезлые кабаньи головы и громадные медвежьи когти. Вид у них внушительный, даже если лучшие времена давно прошли."),
                ],
            ),
        ],
        npcs=[],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 6],
            time_slots=[0, 1, 2, 3],
            closed_text="Охотничий клуб закрыт. По пятницам и воскресеньям здесь не торгуют, а в остальные дни он работает только с утра до вечера.",
        ),
        custom_properties={
            "shop_feature": "hunter_club",
            "object_menu_label": "HunterClubObjectMenu",
            "bg_picture_by_time": {
                3: "images/general/hunter_store_2.png",
            },
        },
    )      


default HunterClubTradeMode = ""
default HunterClubTradeSelection = {}


screen hunter_club_trade_overlay():
    zorder 120

    $ _mode = str(HunterClubTradeMode or "buy").strip().lower()
    $ _entries = list(hunter_club_trade_entries(_mode) or [])
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24
    $ _title = "ПОКУПКА В ОХОТНИЧЬЕМ КЛУБЕ" if _mode == "buy" else "ПРОДАЖА В ОХОТНИЧЬЕМ КЛУБЕ"

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        viewport:
            xpos 28
            ypos 24
            xsize _left_w - 56
            ysize _left_h - 48
            draggable True
            mousewheel True

            vbox:
                spacing 14

                text _title size 30 color "#1e130c" xalign 0.5
                text hunter_club_trade_summary_text(_mode) size 18 color "#2d1d12"

                if len(_entries) <= 0:
                    text "Список пуст." size 22 color "#5a3a24"
                else:
                    for _entry in _entries:
                        $ _item_id = str(_entry.get("item_id", "") or "")
                        $ _qty = hunter_club_trade_selected_qty(_item_id)
                        $ _price = int(_entry.get("price", 0) or 0)
                        $ _max_qty = int(_entry.get("max_qty", 0) or 0)
                        $ _owned_qty = int(_entry.get("owned_qty", 0) or 0)
                        $ _line_total = _price * _qty

                        frame:
                            xfill True
                            padding (10, 8)
                            background "#f5ead3"

                            hbox:
                                xfill True
                                spacing 14

                                vbox:
                                    xmaximum int((_left_w - 80) * 0.52)
                                    spacing 4
                                    text str(_entry.get("name", "") or _item_id) size 22 color "#1e130c"
                                    if _mode == "buy":
                                        text "Цена: [str(_price)] мараведи. Можно взять до [str(_max_qty)]." size 17 color "#2d1d12"
                                    else:
                                        text "Цена: [str(_price)] мараведи. У вас: [str(_owned_qty)]." size 17 color "#2d1d12"

                                hbox:
                                    spacing 10
                                    xalign 1.0

                                    textbutton "-":
                                        xminimum 48
                                        text_size 20
                                        sensitive _qty > 0
                                        action Function(hunter_club_trade_change_qty, _item_id, -1, _mode)

                                    text "[_qty]" size 24 color "#1e130c" xalign 0.5 yalign 0.5

                                    textbutton "+":
                                        xminimum 48
                                        text_size 20
                                        sensitive _qty < _max_qty
                                        action Function(hunter_club_trade_change_qty, _item_id, 1, _mode)

                                    vbox:
                                        xminimum 160
                                        spacing 2
                                        text "Сумма" size 16 color "#5a3a24" xalign 0.5
                                        text str(_line_total) + " мараведи" size 20 color "#1e130c" xalign 0.5

label HunterClub:
    scene black
    call EnterLocation("HunterClub")
    $ CurrentRoom = HunterClubRoom
    $ CurLoc = "HunterClub"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""

    if not HunterClubRoom.is_open(week, time):
        $ MainTxt = HunterClubRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        jump HunterClubView

    $ MainTxt = hunter_club_main_text()
    $ CurLocDesc = MainTxt
    call HunterClubBuildActions
    jump HunterClubView


label HunterClubView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump HunterClubView


label HunterClubBuildActions:
    hide screen hunter_club_trade_overlay
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _club_object in HunterClubRoom.visible_objects():
            current_action_items.append(MenuItem(_club_object.name, Call("HunterClubObjectMenu", _club_object.object_id)))
        for _club_exit in HunterClubRoom.visible_exits():
            current_action_items.append(MenuItem(_club_exit.label, Jump(_club_exit.target)))
    return


label HunterClubObjectMenu(object_id=""):
    hide screen hunter_club_trade_overlay
    $ _club_object = None
    python:
        for _room_object in HunterClubRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _club_object = _room_object
                break

    if _club_object is None:
        call HunterClubBuildActions
        return

    $ MainTxt = _club_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _club_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _club_action in _club_object.visible_actions():
            if _club_action.hook == "text":
                current_action_items.append(MenuItem(_club_action.label, Call("HunterClubObjectText", object_id, _club_action.action_id)))
            elif _club_action.hook == "call" and str(_club_action.target or "") != "":
                _club_args = tuple(getattr(_club_action, "args", ()) or ())
                current_action_items.append(MenuItem(_club_action.label, Call(_club_action.target, *_club_args)))
            elif _club_action.hook == "jump" and str(_club_action.target or "") != "":
                current_action_items.append(MenuItem(_club_action.label, Jump(_club_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("HunterClubRestore")))
    return


label HunterClubObjectText(object_id="", action_id=""):
    python:
        _club_text = ""
        _club_name = ""
        for _room_object in HunterClubRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _club_name = str(getattr(_room_object, "name", "") or "")
            for _club_action in _room_object.visible_actions():
                if getattr(_club_action, "action_id", "") == str(action_id or ""):
                    _club_text = str(_club_action.target or "")
                    break
            break
        if _club_text:
            MainTxt = _club_text
            CurLocDesc = _club_text
            current_action_title = _club_name or "Действия"
    call HunterClubObjectMenu(object_id)
    return


label HunterClubLuiseTalk:
    $ current_action_title = "Толстая Луиза"
    $ current_action_content = None
    $ MainTxt = "Толстая Луиза смеряет вас быстрым опытным взглядом и хмыкает: \"Если принес добычу - платила и буду платить. Если пришел за снарягой - смотри товар, только не торгуйся по пустякам.\""
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Открыть список покупок", Call("HunterClubBuyMenu")),
        MenuItem("Открыть список продажи", Call("HunterClubSellMenu")),
        MenuItem("Назад", Call("HunterClubRestore")),
    ]
    return


label HunterClubBuyMenu:
    $ hunter_club_trade_reset("buy")
    show screen hunter_club_trade_overlay
    $ current_action_title = "Покупка"
    $ current_action_content = None
    $ MainTxt = "Толстая Луиза показывает вам охотничьи припасы, лесной инструмент и прочие полезные вещи. Выберите товар и сразу укажите количество."
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Подтвердить покупку", Call("HunterClubApplyTrade", "buy")),
        MenuItem("Сбросить выбор", Call("HunterClubResetTrade", "buy")),
        MenuItem("Назад", Call("HunterClubRestore")),
    ]
    return


label HunterClubBuyApply(item_id=""):
    $ _buy_result = hunter_club_buy_item(item_id, 1)
    $ MainTxt = str(_buy_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    call stat
    call HunterClubBuildActions
    return


label HunterClubSellMenu:
    $ hunter_club_trade_reset("sell")
    show screen hunter_club_trade_overlay
    $ current_action_title = "Продажа"
    $ current_action_content = None
    $ MainTxt = "Толстая Луиза готова принять шкуры, когти, мясо, травы и прочую лесную добычу. Отметьте нужное и укажите количество."
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Подтвердить продажу", Call("HunterClubApplyTrade", "sell")),
        MenuItem("Сбросить выбор", Call("HunterClubResetTrade", "sell")),
        MenuItem("Назад", Call("HunterClubRestore")),
    ]
    return


label HunterClubSellApply(item_id=""):
    $ _sell_result = hunter_club_sell_item(item_id, 0)
    $ MainTxt = str(_sell_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    call stat
    call HunterClubBuildActions
    return


label HunterClubRestore:
    $ hunter_club_restore_scene_state()
    call HunterClubBuildActions
    return


label HunterClubResetTrade(mode="buy"):
    $ hunter_club_trade_reset(mode)
    if str(mode or "buy") == "sell":
        call HunterClubSellMenu
        return
    call HunterClubBuyMenu
    return


label HunterClubApplyTrade(mode="buy"):
    $ _trade_mode = str(mode or HunterClubTradeMode or "buy")
    $ _trade_result = hunter_club_apply_trade(_trade_mode)
    $ MainTxt = str(_trade_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    call stat
    if bool(_trade_result.get("ok", False)):
        $ hunter_club_trade_reset(_trade_mode)
    if _trade_mode == "sell":
        call HunterClubSellMenu
        return
    call HunterClubBuyMenu
    return
