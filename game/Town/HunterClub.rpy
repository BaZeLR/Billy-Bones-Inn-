# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy

    HUNTER_CLUB_TRADE_MAX_QTY = 99

    HUNTER_CLUB_CHALLENGES = [
        {
            "id": "wolf_skin",
            "label": "Принести серую волчью шкуру",
            "item_id": "wolf_skin_001",
            "qty": 1,
            "rep": 2,
            "text": "Луиза принимает серую волчью шкуру, щупает мех и одобрительно хмыкает. Для начала вы доказали, что в лесу не только гуляете.",
        },
        {
            "id": "boar_fang",
            "label": "Принести кабаний клык",
            "item_id": "boar_fang_001",
            "qty": 1,
            "rep": 3,
            "text": "Кабаний клык быстро переходит из ваших рук к Луизе. Она показывает его паре охотников у стены, и те смотрят на вас с уважением: вы явно не новичок в лесу.",
        },
        {
            "id": "white_wolf",
            "label": "Принести белую волчью шкуру",
            "item_id": "white_wolf_skin_001",
            "qty": 1,
            "rep": 5,
            "text": "Белая волчья шкура производит в клубе настоящий шум. Луиза больше не шутит: такой трофей здесь уважают.",
        },
        {
            "id": "bear_claw",
            "label": "Принести медвежий коготь",
            "item_id": "bear_claw_001",
            "qty": 1,
            "rep": 6,
            "text": "Медвежий коготь ложится на прилавок тяжело и убедительно. После такого трофея охотники начинают запоминать ваше имя.",
        },
    ]

    HUNTER_CLUB_BUY_STOCK = [
        {"item_id": "drink_ale_001", "price": 2},
        {"item_id": "dog_bone_001", "price": 1},
        {"item_id": "dog_collar_001", "price": 10},
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
        "white_wolf_skin_001",
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
        global HunterClubTradeMode, HunterClubTradeSelection
        HunterClubTradeMode = str(mode or "buy").strip().lower()
        HunterClubTradeSelection = {}
        for entry in list(hunter_club_trade_entries(HunterClubTradeMode) or []):
            HunterClubTradeSelection[str(entry.get("item_id", "") or "")] = 0

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

    def hunter_club_seen_first_visit():
        return int(HunterClubVar.get("first_visit_seen", 0) or 0) > 0

    def hunter_club_reputation():
        return max(0, int(HunterClubVar.get("reputation", 0) or 0))

    def hunter_club_completed_challenges():
        return dict(HunterClubVar.get("completed_challenges", {}) or {})

    def hunter_club_challenge_row(challenge_id=""):
        challenge_key = str(challenge_id or "").strip()
        for row in list(HUNTER_CLUB_CHALLENGES or []):
            if str(row.get("id", "") or "") == challenge_key:
                return dict(row)
        return {}

    def hunter_club_challenge_completed(challenge_id=""):
        return int(hunter_club_completed_challenges().get(str(challenge_id or "").strip(), 0) or 0) > 0

    def hunter_club_challenge_available(row):
        data = dict(row or {})
        if hunter_club_challenge_completed(data.get("id", "")):
            return False
        item_id = str(data.get("item_id", "") or "")
        qty = max(1, int(data.get("qty", 1) or 1))
        return int(_player_item_count_by_id(item_id) or 0) >= qty

    def hunter_club_reputation_title():
        value = hunter_club_reputation()
        if value >= 16:
            return "уважаемый клубный охотник"
        if value >= 9:
            return "заметный добытчик"
        if value >= 4:
            return "подающий надежды следопыт"
        return "новичок клуба"

    def hunter_club_news_text():
        rows = [
            "На доске клуба висят свежие заметки о лесных тропах, зверье и городских слухах.",
            "Ваша репутация в клубе: %s (%s)." % (hunter_club_reputation(), hunter_club_reputation_title()),
        ]
        try:
            if fight_can_hunt_here("Forest"):
                rows.append("Охотники говорят, что в обычном лесу снова видели волчьи следы.")
            if fight_can_hunt_here("ForestDarkWoods"):
                rows.append("У темных троп неспокойно: там попадаются звери покрупнее.")
            if int(effective_player_exploration() or 0) >= 100:
                rows.append("Луиза советует не ходить далеко без бинтов, ловушек и заряженного оружия.")
        except Exception:
            pass
        if int(Mongol.var.get("StocksArrestDay", -1) or -1) >= 0:
            rows.append("У стойки снова обсуждают арест конокрада: городская стража теперь смотрит на рынок строже.")
        return "\n\n".join(rows)

    def hunter_club_challenge_caption(row):
        data = dict(row or {})
        item_id = str(data.get("item_id", "") or "")
        item_obj = get_game_item(item_id)
        item_name = str(getattr(item_obj, "name", item_id) or item_id)
        qty = max(1, int(data.get("qty", 1) or 1))
        rep = max(0, int(data.get("rep", 0) or 0))
        if hunter_club_challenge_completed(data.get("id", "")):
            return "%s (выполнено)" % str(data.get("label", "") or item_name)
        return "%s: %s x%s, репутация +%s" % (str(data.get("label", "") or item_name), item_name, qty, rep)

    def hunter_club_apply_challenge(challenge_id=""):
        global reputation

        row = hunter_club_challenge_row(challenge_id)
        if not row:
            return {"ok": False, "text": "Такого вызова на доске нет."}
        challenge_key = str(row.get("id", "") or "")
        if hunter_club_challenge_completed(challenge_key):
            return {"ok": False, "text": "Этот вызов уже закрыт."}
        item_id = str(row.get("item_id", "") or "")
        qty = max(1, int(row.get("qty", 1) or 1))
        if int(_player_item_count_by_id(item_id) or 0) < qty:
            return {"ok": False, "text": "Для этого вызова у вас пока нет нужного трофея."}
        for _unused in range(qty):
            _player_remove_item_by_id(item_id)
        completed = hunter_club_completed_challenges()
        completed[challenge_key] = 1
        HunterClubVar["completed_challenges"] = completed
        rep_gain = max(0, int(row.get("rep", 0) or 0))
        HunterClubVar["reputation"] = hunter_club_reputation() + rep_gain
        try:
            reputation = min(100, max(int(reputation or 0), int(reputation or 0) + rep_gain))
        except Exception:
            pass
        return {"ok": True, "text": "%s\n\nРепутация в клубе: +%s." % (str(row.get("text", "") or "Луиза принимает трофей."), rep_gain)}

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
            return {"ok": False, "text": "Сначала выберите товар и желаемое количество."}

        if mode_value == "buy":
            if int(money or 0) < total_price:
                return {"ok": False, "text": "У вас не хватает денег на выбранную покупку."}
            money -= total_price
            return {"ok": True, "text": "Толстая Луиза складывает для вас: %s. Всего вы платите %s мараведи." % (", ".join(applied_rows), total_price)}

        money += total_price
        return {"ok": True, "text": " Луиза принимает,с доволной ухмылкой принимает у вас: %s. Всего она платит %s мараведи." % (", ".join(applied_rows), total_price)}

    def hunter_club_main_text():
        return (
            "Вы входите в охотничий клуб на рыночной площади. Внутри пахнет шкурами, сушеными травами, "
            "смолой и дешевым элем. На стенах развешаны старые луки, кабаньи головы, рога, потемневшие "
            "от времени,шкуры различных зверей,и других диковин, а за широким прилавком хозяйничает толстуха Луиза.\n\n"
            "Здесь можно купить охотничьи припасы и сбыть лесную добычу."
        )

    def hunter_club_restore_scene_state():
        global MainTxt, CurLocDesc, HunterClubTradeMode, HunterClubTradeSelection
        room_text = hunter_club_main_text()
        MainTxt = room_text
        CurLocDesc = room_text
        HunterClubTradeMode = ""
        HunterClubTradeSelection = {}
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
        group_name=ROOM_GROUP_CITY,
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
            GameObject(
                object_id="hunter_board",
                name="Доска клуба",
                description="На доске прибиты новости, заметки о звериных следах и небольшие вызовы для тех, кто хочет, совместить приятное с полезным и заработать репутацию в клубе и немного мараведи.",
                actions=[
                    ObjectAction(action_id="club_news", label="Почитать новости", hook="call", target="HunterClubNewsMenu"),
                    ObjectAction(action_id="club_challenges", label="Посмотреть охотничьи вызовы", hook="call", target="HunterClubChallengesMenu"),
                ],
            ),
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 6],
            start="08:00",
            end="18:59",
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
default HunterClubVar = {}


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

    if not HunterClubRoom.is_open():
        $ MainTxt = HunterClubRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        $ _hunter_closed_ui_return = None
        while _hunter_closed_ui_return is None:
            call screen main_ui
            $ _hunter_closed_ui_return = _return
        jump HunterClub

    $ MainTxt = hunter_club_main_text()
    $ CurLocDesc = MainTxt
    if not hunter_club_seen_first_visit():
        call HunterClubFirstVisit
    elif int(Clara.var.get("escape_confessed", 0) or 0) == 1 and int(Mongol.var.get("StocksArrestDay", -1) or -1) < 0:
        call preEvent("claraBookletMarket")
        if thread is not None and int(thread.num or 0) < 4:
            $ thread.advanceTo(4, force_active=True)
        call story_clara_market_booklet_5
    elif story_event_available("HunterClub", "overheard"):
        call checkTriggers("HunterClub", "overheard", 0)
    call HunterClubBuildActions
    $ _hunter_ui_return = None
    while _hunter_ui_return is None:
        call screen main_ui
        $ _hunter_ui_return = _return
    jump HunterClub


label HunterClubFirstVisit:
    $ HunterClubVar["first_visit_seen"] = 1
    $ scene_image ="images/general/hunter_store_2.png"
    $ MainTxt = (
        "Вы внимательно и с живым интересом рассматриваете помещение и товары, Вас с таким же живым интересом рассматривает толстуха за прилавком\n"
        "А ты, вы уважаемый хер... ммм, случайно не родственник покойного Лонгкока?\n"
        "- Да, отвечаете Вы,- покойный был моим дядей, Я Стефан Лонгкок, Мещанин и владелец Дикого Жеребца', отвечаете Вы.\n"
        "Ишь ты!-  мещанин, молод, трактирщик... голуба ты наш!- такие от добры молодцы нам нужны.С задором в голосе говорит толстуха,и, глядя вам прямо в глаза,ухмыляясь,стала наливать эль в две выствавленные кружки\n"
        "- за знакомство!и,залпом выпив свою, продолжила:"
        "-ахх! То-то я смотрю, похож. Вылитый Лонгкок в молодости. Мдэ,\" выдохнула, погрустнев толстуха. \"Покойничек-то лес любил, да и ружьишко у него, помнится, чудное имелось... фамильное... ну, как говорится, земля ему пухом,а тебе не всплыть в канале к верху брюхом... И вообще, синька зло!\" - подытожила она. \"А ты, это... заходи, если что надо, у Луизы,тыча грязным пальцем между жирых сисек, подытоживает, всегда всем рады. Милости просим, да... уж!\n"
    )
    $ CurLocDesc = MainTxt
    return


label HunterClubBuildActions:
    hide screen hunter_club_trade_overlay
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ findAvailableEvents(True)

    python:
        current_action_items.append(MenuItem("Купить товары", Call("HunterClubBuyMenu")))
        current_action_items.append(MenuItem("Продать добычу", Call("HunterClubSellMenu")))
        current_action_items.append(MenuItem("Поговорить с Луизой", Call("HunterClubLuiseTalk")))
        for _club_object in HunterClubRoom.visible_objects():
            current_action_items.append(MenuItem(_club_object.name, Call("HunterClubObjectMenu", _club_object.object_id)))
        if story_event_available("HunterClub", "overheard"):
            current_action_items.append(MenuItem("Подслушать охотников у стены", Call("checkTriggers", "HunterClub", "overheard", 0)))
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

    $ current_action_items.append(MenuItem("Назад", Jump("HunterClub")))
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
    $ current_action_title = "Толстуха Луиза"
    $ current_action_content = None
    $ MainTxt = " Луиза смеряет вас быстрым опытным взглядом и хмыкает: \"Если принес добычу - платила и буду платить. Если пришел за снарягой - смотри товар, только не торгуйся по пустякам.\""
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Закупиться для охоты", Call("HunterClubBuyMenu")),
        MenuItem("Подать добычу", Call("HunterClubSellMenu")),
        MenuItem("Назад", Jump("HunterClub")),
    ]
    return


label HunterClubNewsMenu:
    $ current_action_title = "Новости клуба"
    $ current_action_content = None
    $ MainTxt = hunter_club_news_text()
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Посмотреть охотничьи вызовы", Call("HunterClubChallengesMenu")),
        MenuItem("Назад", Jump("HunterClub")),
    ]
    return


label HunterClubChallengesMenu(result_text=""):
    $ current_action_title = "Охотничьи вызовы"
    $ current_action_content = None
    $ MainTxt = str(result_text or "").strip()
    if MainTxt == "":
        $ MainTxt = "Луиза кивает на доску: \"Кто приносит трофеи, того тут запоминают. Деньги деньгами, а имя среди охотников тоже чего-то стоит.\""
    $ CurLocDesc = MainTxt
    $ current_action_items = []
    python:
        for _challenge in list(HUNTER_CLUB_CHALLENGES or []):
            _caption = hunter_club_challenge_caption(_challenge)
            _challenge_id = str(_challenge.get("id", "") or "")
            if hunter_club_challenge_available(_challenge):
                current_action_items.append(MenuItem(_caption, Call("HunterClubChallengeApply", _challenge_id)))
            elif not hunter_club_challenge_completed(_challenge_id):
                current_action_items.append(MenuItem(_caption, Call("HunterClubChallengeMissing", _challenge_id)))
        if len(current_action_items) <= 0:
            current_action_items.append(MenuItem("Все доступные вызовы уже закрыты", Call("HunterClubNewsMenu")))
        current_action_items.append(MenuItem("Назад", Jump("HunterClub")))
    return


label HunterClubChallengeMissing(challenge_id=""):
    $ _challenge = hunter_club_challenge_row(challenge_id)
    $ MainTxt = "Для этого вызова у вас пока нет нужного трофея."
    if _challenge:
        $ MainTxt = "Луиза смотрит на доску и качает головой: \"Сначала принеси то, что там написано. Тут словам не верят, тут трофеи кладут на стол.\""
    $ CurLocDesc = MainTxt
    call HunterClubChallengesMenu(MainTxt)
    return


label HunterClubChallengeApply(challenge_id=""):
    $ _challenge_result = hunter_club_apply_challenge(challenge_id)
    $ MainTxt = str(_challenge_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    call stat
    call HunterClubChallengesMenu(MainTxt)
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
    $ MainTxt = "Толстуха Луиза готова принять шкуры, когти, мясо, травы и прочую лесную добычу. Отметьте нужное и укажите количество."
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
