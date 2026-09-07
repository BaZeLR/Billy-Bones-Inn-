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
        {"item_id": "shovel_001", "price": 24},
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
            item_count = int(player.item_count(item_id) or 0)
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
        return max(0, min(HUNTER_CLUB_TRADE_MAX_QTY, int(player.economy.money or 0) // price_each))

    def hunter_club_sell_max_quantity(item_id):
        return max(0, min(HUNTER_CLUB_TRADE_MAX_QTY, int(player.item_count(item_id) or 0)))

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
                "owned_qty": int(player.item_count(item_id) or 0),
                "max_qty": hunter_club_buy_max_quantity(item_id) if mode == "buy" else hunter_club_sell_max_quantity(item_id),
            })
        return rows

    def hunter_club_trade_selected_qty(item_id):
        item_key = str(item_id or "").strip()
        selection = rooms.get("HunterClub").state.get("trade_selection", {})
        if item_key == "" or not hasattr(selection, "get"):
            return 0
        return max(0, int(selection.get(item_key, 0) or 0))

    def hunter_club_trade_set_qty(item_id, qty, trade_mode="buy"):
        item_key = str(item_id or "").strip()
        mode = str(trade_mode or rooms.get("HunterClub").state.get("trade_mode", "") or "buy").strip().lower()
        if item_key == "":
            return
        max_qty = hunter_club_buy_max_quantity(item_key) if mode == "buy" else hunter_club_sell_max_quantity(item_key)
        rooms.get("HunterClub").state["trade_selection"][item_key] = max(0, min(int(qty or 0), int(max_qty or 0)))
        renpy.restart_interaction()

    def hunter_club_trade_change_qty(item_id, delta, trade_mode="buy"):
        hunter_club_trade_set_qty(item_id, hunter_club_trade_selected_qty(item_id) + int(delta or 0), trade_mode)

    def hunter_club_trade_reset(mode="buy"):
        rooms.get("HunterClub").state["trade_mode"] = str(mode or "buy").strip().lower()
        rooms.get("HunterClub").state["trade_selection"] = {}
        for entry in list(hunter_club_trade_entries(rooms.get("HunterClub").state["trade_mode"]) or []):
            rooms.get("HunterClub").state["trade_selection"][str(entry.get("item_id", "") or "")] = 0

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
        mode_value = str(mode or rooms.get("HunterClub").state.get("trade_mode", "") or "buy").strip().lower()
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
        return int(rooms.get("HunterClub").state.get("first_visit_seen", 0) or 0) > 0

    def hunter_club_reputation():
        return max(0, int(rooms.get("HunterClub").state.get("reputation", 0) or 0))

    def hunter_club_completed_challenges():
        return dict(rooms.get("HunterClub").state.get("completed_challenges", {}) or {})

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
        return int(player.item_count(item_id) or 0) >= qty

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
        if int(threads["claraBookletMarket"].num or 0) >= 4:
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

    def hunter_club_challenge_items():
        items = []
        for challenge in list(HUNTER_CLUB_CHALLENGES or []):
            challenge_id = str(challenge.get("id", "") or "")
            caption = hunter_club_challenge_caption(challenge)
            if hunter_club_challenge_available(challenge):
                items.append(MenuItem(caption, Call("HunterClubChallengeApply", challenge_id)))
            elif not hunter_club_challenge_completed(challenge_id):
                items.append(MenuItem(caption, Call("HunterClubChallengeMissing", challenge_id)))
        if len(items) <= 0:
            items.append(MenuItem("Все доступные вызовы уже закрыты", Call("HunterClubNewsMenu")))
        items.append(MenuItem("Назад", [
            SetField(scene_runtime, "picture", rooms.get("HunterClub").bg_picture or None),
            SetField(scene_runtime, "text", hunter_club_main_text()),
            SetField(scene_runtime, "location_text", hunter_club_main_text()),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", rooms.get("HunterClub").build_action_items() + rooms.get("HunterClub").build_exit_items()),
            Function(main_ui_restart_interaction),
        ]))
        return items

    def hunter_club_apply_challenge(challenge_id=""):
        row = hunter_club_challenge_row(challenge_id)
        if not row:
            return {"ok": False, "text": "Такого вызова на доске нет."}
        challenge_key = str(row.get("id", "") or "")
        if hunter_club_challenge_completed(challenge_key):
            return {"ok": False, "text": "Этот вызов уже закрыт."}
        item_id = str(row.get("item_id", "") or "")
        qty = max(1, int(row.get("qty", 1) or 1))
        if int(player.item_count(item_id) or 0) < qty:
            return {"ok": False, "text": "Для этого вызова у вас пока нет нужного трофея."}
        player.remove_item(item_id, qty)
        completed = hunter_club_completed_challenges()
        completed[challenge_key] = 1
        rooms.get("HunterClub").state["completed_challenges"] = completed
        rep_gain = max(0, int(row.get("rep", 0) or 0))
        rooms.get("HunterClub").state["reputation"] = hunter_club_reputation() + rep_gain
        player.change_stat("reputation", rep_gain)
        return {"ok": True, "text": "%s\n\nРепутация в клубе: +%s." % (str(row.get("text", "") or "Луиза принимает трофей."), rep_gain)}

    def hunter_club_apply_trade(mode="buy"):

        mode_value = str(mode or rooms.get("HunterClub").state.get("trade_mode", "") or "buy").strip().lower()
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

            total_price += price_each * qty
            applied_rows.append({
                "item_id": item_id,
                "quantity": qty,
                "name": str(entry.get("name", item_id) or item_id),
            })

        if len(applied_rows) <= 0:
            return {"ok": False, "text": "Сначала выберите товар и желаемое количество."}

        if mode_value == "buy":
            if int(player.economy.money or 0) < total_price:
                return {"ok": False, "text": "У вас не хватает денег на выбранную покупку."}
            for applied in applied_rows:
                player.add_item(applied["item_id"], applied["quantity"])
            player.spend_money(total_price)
            applied_text = ", ".join(["%s x%s" % (row["name"], row["quantity"]) for row in applied_rows])
            return {"ok": True, "text": "Толстая Луиза складывает для вас: %s. Всего вы платите %s мараведи." % (applied_text, total_price)}

        for applied in applied_rows:
            player.remove_item(applied["item_id"], applied["quantity"])
        player.add_money(total_price)
        applied_text = ", ".join(["%s x%s" % (row["name"], row["quantity"]) for row in applied_rows])
        return {"ok": True, "text": " Луиза принимает,с доволной ухмылкой принимает у вас: %s. Всего она платит %s мараведи." % (applied_text, total_price)}

    def hunter_club_main_text():
        return (
            "Вы входите в охотничий клуб на рыночной площади. Внутри пахнет шкурами, сушеными травами, "
            "смолой и дешевым элем. На стенах развешаны старые луки, кабаньи головы, рога, потемневшие "
            "от времени,шкуры различных зверей,и других диковин, а за широким прилавком хозяйничает толстуха Луиза.\n\n"
            "Здесь можно купить охотничьи припасы и сбыть лесную добычу."
        )

    HunterClubRoomDefinition = Room(
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
            RoomExit(label="Вернуться на рынок", target="MarketPlace", minutes_to_pass=10),
        ],
        game_items=[],
        action_menus=[
            RoomAction(action_id="buy_goods", label="Купить товары", hook="call", target="HunterClubBuyMenu"),
            RoomAction(action_id="sell_loot", label="Продать добычу", hook="call", target="HunterClubSellMenu"),
            RoomAction(action_id="club_news", label="Почитать новости клуба", hook="call", target="HunterClubNewsMenu"),
            RoomAction(action_id="club_challenges", label="Посмотреть охотничьи вызовы", hook="call", target="HunterClubChallengesMenu"),
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 6],
            start="08:00",
            end="18:59",
            closed_text="Охотничий клуб закрыт. По пятницам и воскресеньям здесь не торгуют, а в остальные дни он работает только с утра до вечера.",
        ),
        state={
            "first_visit_seen": 0,
            "reputation": 0,
            "completed_challenges": {},
            "trade_mode": "",
            "trade_selection": {},
        },
        custom_properties={
            "shop_feature": "hunter_club",
            "bg_picture_by_time": {
                3: "images/general/hunter_store_2.png",
            },
        },
    )      

screen hunter_club_trade_overlay():
    zorder 120

    $ _mode = str(rooms.get("HunterClub").state.get("trade_mode", "") or "buy").strip().lower()
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
    hide screen hunter_club_trade_overlay
    $ rooms.enter("HunterClub")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    if scene_runtime.picture:
        vscene scene_runtime.picture
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""

    if not rooms.get("HunterClub").is_open():
        $ scene_runtime.text = rooms.get("HunterClub").schedule.closed_text
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = rooms.get("HunterClub").build_exit_items()
        while True:
            call screen main_ui

    $ scene_runtime.text = hunter_club_main_text()
    $ scene_runtime.location_text = scene_runtime.text
    if not hunter_club_seen_first_visit():
        call HunterClubFirstVisit
    elif story_event_available("HunterClub", "overheard"):
        call checkTriggers("HunterClub", "overheard", 0)

    $ main_ui_runtime.action_items = rooms.get("HunterClub").build_action_items() + rooms.get("HunterClub").build_exit_items()
    while True:
        call screen main_ui


label HunterClubFirstVisit:
    $ rooms.get("HunterClub").state["first_visit_seen"] = 1
    $ scene_runtime.picture = "images/general/hunter_store_2.png"
    vscene scene_runtime.picture
    $ scene_runtime.text = (
        "Вы внимательно и с живым интересом рассматриваете помещение и товары, Вас с таким же живым интересом рассматривает толстуха за прилавком\n"
        "А ты, вы уважаемый хер... ммм, случайно не родственник покойного Лонгкока?\n"
        "- Да, отвечаете Вы,- покойный был моим дядей, Я Стефан Лонгкок, Мещанин и владелец Дикого Жеребца', отвечаете Вы.\n"
        "Ишь ты!-  мещанин, молод, трактирщик... голуба ты наш!- такие от добры молодцы нам нужны.С задором в голосе говорит толстуха,и, глядя вам прямо в глаза,ухмыляясь,стала наливать эль в две выствавленные кружки\n"
        "- за знакомство!и,залпом выпив свою, продолжила:"
        "-ахх! То-то я смотрю, похож. Вылитый Лонгкок в молодости. Мдэ,\" выдохнула, погрустнев толстуха. \"Покойничек-то лес любил, да и ружьишко у него, помнится, чудное имелось... фамильное... ну, как говорится, земля ему пухом,а тебе не всплыть в канале к верху брюхом... И вообще, синька зло!\" - подытожила она. \"А ты, это... заходи, если что надо, у Луизы,тыча грязным пальцем между жирых сисек, подытоживает, всегда всем рады. Милости просим, да... уж!\n"
    )
    $ scene_runtime.location_text = scene_runtime.text
    return


label HunterClubLuiseTalk:
    $ main_ui_runtime.action_title = "Толстуха Луиза"
    $ main_ui_runtime.action_content = None
    $ scene_runtime.text = " Луиза смеряет вас быстрым опытным взглядом и хмыкает: \"Если принес добычу - платила и буду платить. Если пришел за снарягой - смотри товар, только не торгуйся по пустякам.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = [
        MenuItem("Закупиться для охоты", Call("HunterClubBuyMenu")),
        MenuItem("Подать добычу", Call("HunterClubSellMenu")),
        MenuItem("Спросить, где купить лошадь", Call("HunterClubAskHorse")),
        MenuItem("Назад", [
            SetField(scene_runtime, "picture", rooms.get("HunterClub").bg_picture or None),
            SetField(scene_runtime, "text", hunter_club_main_text()),
            SetField(scene_runtime, "location_text", hunter_club_main_text()),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", rooms.get("HunterClub").build_action_items() + rooms.get("HunterClub").build_exit_items()),
            Function(main_ui_restart_interaction),
        ]),
    ]
    return


label HunterClubAskHorse:
    if player.horse.owns_horse():
        $ scene_runtime.text = "Луиза кивает: \"Конь у тебя уже есть. Береги его и не оставляй конюшню без присмотра.\""
    elif int(Luisa.horse_referral_stage or 0) > 0:
        $ scene_runtime.text = "Луиза напоминает: \"Я же сказала: у городской стражи есть свои конюшни. Поговори с десятником Циммерманом.\""
    elif hunter_club_reputation() > 5:
        $ Luisa.horse_referral_stage = 1
        $ scene_runtime.text = "Луиза одобрительно хмыкает: \"Раз уж охотники тебя знают, подскажу. У городской стражи есть свои конюшни. Поговори с десятником Циммерманом — за вино и монету он может подобрать тебе коня.\""
    else:
        $ scene_runtime.text = "Луиза качает головой: \"Сначала заработай имя среди охотников. Когда твоя репутация в клубе будет выше пяти, тогда и поговорим о надежном коне.\""
    $ scene_runtime.location_text = scene_runtime.text
    return


label HunterClubNewsMenu:
    $ main_ui_runtime.action_title = "Новости клуба"
    $ main_ui_runtime.action_content = None
    $ scene_runtime.text = hunter_club_news_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = [
        MenuItem("Посмотреть охотничьи вызовы", Call("HunterClubChallengesMenu")),
        MenuItem("Назад", [
            SetField(scene_runtime, "picture", rooms.get("HunterClub").bg_picture or None),
            SetField(scene_runtime, "text", hunter_club_main_text()),
            SetField(scene_runtime, "location_text", hunter_club_main_text()),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", rooms.get("HunterClub").build_action_items() + rooms.get("HunterClub").build_exit_items()),
            Function(main_ui_restart_interaction),
        ]),
    ]
    return


label HunterClubChallengesMenu(result_text=""):
    $ main_ui_runtime.action_title = "Охотничьи вызовы"
    $ main_ui_runtime.action_content = None
    $ scene_runtime.text = str(result_text or "").strip()
    if scene_runtime.text == "":
        $ scene_runtime.text = "Луиза кивает на доску: \"Кто приносит трофеи, того тут запоминают. Деньги деньгами, а имя среди охотников тоже чего-то стоит.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = hunter_club_challenge_items()
    return


label HunterClubChallengeMissing(challenge_id=""):
    $ renpy.dynamic("_challenge")
    $ _challenge = hunter_club_challenge_row(challenge_id)
    $ scene_runtime.text = "Для этого вызова у вас пока нет нужного трофея."
    if _challenge:
        $ scene_runtime.text = "Луиза смотрит на доску и качает головой: \"Сначала принеси то, что там написано. Тут словам не верят, тут трофеи кладут на стол.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = hunter_club_challenge_items()
    return


label HunterClubChallengeApply(challenge_id=""):
    $ renpy.dynamic("_challenge_result")
    $ _challenge_result = hunter_club_apply_challenge(challenge_id)
    $ scene_runtime.text = str(_challenge_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = hunter_club_challenge_items()
    return


label HunterClubBuyMenu:
    $ hunter_club_trade_reset("buy")
    show screen hunter_club_trade_overlay
    $ main_ui_runtime.action_title = "Покупка"
    $ main_ui_runtime.action_content = None
    $ scene_runtime.text = "Толстая Луиза показывает вам охотничьи припасы, лесной инструмент и прочие полезные вещи. Выберите товар и сразу укажите количество."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = [
        MenuItem("Подтвердить покупку", Call("HunterClubApplyTrade", "buy")),
        MenuItem("Сбросить выбор", Function(hunter_club_trade_reset, "buy")),
        MenuItem("Назад", [
            Hide("hunter_club_trade_overlay"),
            SetField(scene_runtime, "picture", rooms.get("HunterClub").bg_picture or None),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", rooms.get("HunterClub").build_action_items() + rooms.get("HunterClub").build_exit_items()),
            SetField(scene_runtime, "text", hunter_club_main_text()),
            SetField(scene_runtime, "location_text", hunter_club_main_text()),
            Function(main_ui_restart_interaction),
        ]),
    ]
    return


label HunterClubSellMenu:
    $ hunter_club_trade_reset("sell")
    show screen hunter_club_trade_overlay
    $ main_ui_runtime.action_title = "Продажа"
    $ main_ui_runtime.action_content = None
    $ scene_runtime.text = "Толстуха Луиза готова принять шкуры, когти, мясо, травы и прочую лесную добычу. Отметьте нужное и укажите количество."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = [
        MenuItem("Подтвердить продажу", Call("HunterClubApplyTrade", "sell")),
        MenuItem("Сбросить выбор", Function(hunter_club_trade_reset, "sell")),
        MenuItem("Назад", [
            Hide("hunter_club_trade_overlay"),
            SetField(scene_runtime, "picture", rooms.get("HunterClub").bg_picture or None),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", rooms.get("HunterClub").build_action_items() + rooms.get("HunterClub").build_exit_items()),
            SetField(scene_runtime, "text", hunter_club_main_text()),
            SetField(scene_runtime, "location_text", hunter_club_main_text()),
            Function(main_ui_restart_interaction),
        ]),
    ]
    return


label HunterClubApplyTrade(mode="buy"):
    $ renpy.dynamic("_trade_mode", "_trade_result")
    $ _trade_mode = str(mode or rooms.get("HunterClub").state.get("trade_mode", "") or "buy")
    $ _trade_result = hunter_club_apply_trade(_trade_mode)
    $ scene_runtime.text = str(_trade_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    if bool(_trade_result.get("ok", False)):
        $ hunter_club_trade_reset(_trade_mode)
    return
