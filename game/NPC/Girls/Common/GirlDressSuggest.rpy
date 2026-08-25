# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:

    def _gds_relative_type(girl_name):
        girl = str(girl_name or "").strip().lower()
        if girl == "sandra":
            return 1
        if girl in ("melissa", "amanda"):
            return 2
        return 0

    def _gds_ensure_stats(girl_name):
        g = str(girl_name or "").strip()
        if not g:
            return
        info = people.get_info(g)
        if info is not None:
            info.ensure_sex_state()

    def _gds_showoff_level(girl_name):
        g = str(girl_name or "")
        girl_info = people.get_info(g)
        girl_slut = int(getattr(girl_info, "corruption", 0) or 0) if girl_info is not None else 0
        girl_had = int(girl_info.sex_stat("sexacts", 0) or 0) if girl_info is not None else 0
        girl_friend = int(getattr(girl_info, "rel", 0) or 0) if girl_info is not None else 0

        level = 0
        if (girl_slut > 25 and girl_had > 1 and girl_friend > 10) or (girl_slut > 33 and girl_had > 0 and girl_friend > 5):
            level = 1
        if (girl_slut > 35 and girl_had > 3 and girl_friend > 10) or (girl_slut > 47 and girl_had > 0 and girl_friend > 5):
            level = 2
        if (girl_slut > 55 and girl_had > 0) or girl_slut > 65:
            level = 3
        if g == "georgett":
            level = 3
        return level

    def _gds_get_dress_list_for_girl(girl_name):
        info = people.get_info(girl_name)
        if info is None:
            return []
        if not isinstance(getattr(info, "wardrobe", None), dict):
            info.wardrobe = {}
        owned = info.wardrobe.setdefault("owned", [])
        if not isinstance(owned, list):
            owned = list(owned or [])
            info.wardrobe["owned"] = owned
        return owned

    def _gds_has_dress_for_girl(girl_name, dress_code):
        dress = str(dress_code or "")
        if dress == "":
            return True
        return dress in _gds_get_dress_list_for_girl(girl_name)

    def _gds_add_dress_for_girl(girl_name, dress_code):
        dress = str(dress_code or "")
        if dress == "":
            return
        wardrobe = _gds_get_dress_list_for_girl(girl_name)
        if dress not in wardrobe:
            wardrobe.append(dress)

    def _gds_dress_cost(dress_code):
        item_obj = get_game_item("dress_" + str(dress_code or ""))
        return int(getattr(item_obj, "price", 0) or 0)

    def _gds_dress_name(dress_code):
        code = str(dress_code or "")
        item_obj = get_game_item("dress_" + code)
        return str(getattr(item_obj, "name", "") or code)

    def _gds_dress_top_bottom_slut(dress_code):
        d = str(dress_code or "")
        top_name = str(DressTopPart.get(d, "") or "")
        bottom_name = str(DressBottomPart.get(d, "") or "")
        top_slut = int(DressPartSlut.get(top_name, 0) or 0)
        bottom_slut = int(DressPartSlut.get(bottom_name, 0) or 0)
        return top_slut, bottom_slut

    def _gds_apply_purchase(girl_name, dress_code, set_legsdef=False, set_legs=False, set_produced=False):
        g = str(girl_name or "")
        d = str(dress_code or "")
        if g == "" or d == "":
            return 0

        cost = _gds_dress_cost(d)
        player.spend_money(cost)

        _gds_add_dress_for_girl(g, d)

        if set_legsdef or set_legs:
            girl = people.get_info(g)
            if girl is not None:
                girl.set_current_underwear("legs", d)

        player.appearance.girl_dresses_bought = int(player.appearance.girl_dresses_bought or 0) + 1

        if set_produced:
            dress_shop.produced = d
            try:
                household_mark_revealing_dress_order(g, d)
            except Exception:
                pass

        return cost

    def _gds_player_cum_today():
        return int(player.intimacy.came_today or 0)

    def _gds_player_cum_cap():
        return max(1, int(player.intimacy.can_cum_daily or 1))

    def _gds_relative_callout_name(girl_name):
        girl = str(girl_name or "").strip().lower()
        if girl == "sandra":
            return "Сандра"
        if girl == "amanda":
            return "Аманда"
        if girl == "melissa":
            return "Мелисса"
        return str(people_display_name(girl_name))


label GirlDressSuggest(GirlName="", DressToBuy=""):
    $ renpy.dynamic("DressBuyIsRelative", "ShowOffLevel", "_rn", "_short_name", "_gds_dress_id", "_is_bra", "_is_panties", "_is_stockings", "_girl_info", "_slut", "_legs_now", "_panties_now")
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        return

    hide screen dress_shop_catalog_page
    $ _gds_ensure_stats(GirlName)
    $ _gds_ensure_stats("irma")

    $ DressBuyIsRelative = _gds_relative_type(GirlName)
    $ ShowOffLevel = _gds_showoff_level(GirlName)


    $ _rn = people_display_name(GirlName)
    $ _short_name = _gds_dress_name(DressToBuy).lower()

    '"[_rn]", предложили вы, а давай я куплю тебе [_short_name]?'

    python:
        _gds_dress_id = str(DressToBuy or "").lower()
        _is_bra = "bra" in _gds_dress_id
        _is_panties = "panties" in _gds_dress_id
        _is_stockings = "stockings" in _gds_dress_id
        _girl_info = people.get_info(GirlName)
        _slut = int(_girl_info.corruption or 0) if _girl_info is not None else 0

    if _is_bra:
        if GirlName == "georgett":
            '"Лифчик?" удивилась шлюха. "А зачем он мне? Вот, посомтри на мои титьки, какие они сочные, мужики так и налетают" и с этими словами она приподняла и чуть сжала предметы обсуждения, да так, что левый сосок даже выскочил из плена декольте. "Ну и зачем их лифом скрывать? Не дури."'
        elif GirlName == "liza":
            '"Лифчик?" удивилась мулатка. "Мама мне говорила, что нельзя лиф носить, титьки из-за этого плохо будут расти. Так что не, дяденька Стефан, такой подарок мне не нужон!"'
        else:
            '"Лифчик?" удивилась [_rn]. "Не, спасибо конечно, но он мне не нужен!"'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if _is_panties:
        if GirlName == "georgett":
            '"Панталоны?" удивилась шлюха. "Да я их и не носила никогда! Юбочки вполне достаточно! Только время тратить, снимать-одевать, снимать-одевать, снимать-одевать и так по десять раз на дню. Не, не надо мне такого счастья."'
        else:
            '"Панталончики?" удивилась [_rn]. "Не, спасибо конечно, но они мне не нужны!"'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if _is_stockings:
        if _slut < 15:
            '"Ой, чулочки! Ну не знаю, нужны ли они мне?" скромно заметила [_rn]. "Наверное нет, я же никому свои ножки показывать не собираюсь. Давай лучше еще что-то посмотрим."'
            $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
            show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
            return

        if ShowOffLevel > 1:
            $ _legs_now = str(people.get_info(GirlName).current_underwear("legs", "") or "")
            $ _panties_now = str(people.get_info(GirlName).clothing_layer("panties") or "")

            if _legs_now != "":
                '"О, еще чулочки," обрадованно сказала [_rn]. Лукаво посмотрев на вас, она присела на лавочку, сбросила обувку, и начала стягивать с себя [_gds_dress_name(_legs_now).lower()] дабы примерить обновку.'
            else:
                '"О, чулочки," обрадованно сказала [_rn]. Лукаво посмотрев на вас, она присела на лавочку, сбросила обувку, и начала натягивать подарок на свои стройные ножки.'

            if _panties_now != "":
                'Задравшийся при этом подол платья ее ничуть не обеспокоил. Впрочем, под ним обнаружились [_gds_dress_name(_panties_now).lower()], скрывшие все самое интересное от вашего любопытного взора.'
            else:
                'Подол ее платья задрался и вы увидели что под ним ничего не было. Шалунья сначала убедилась в том, что вам удалось полюбоваться ее щелкой.'

            'Портниха, с улыбкой наблюдавшая за этой сценой, заметила: "Похоже ваша дама из тех, кто ценит подарки и умеет их примерять. Молодец!"'
            if DressBuyIsRelative == 1:
                '"Я ему не дама, а Сандра!" вырвалось у Сандры. Потом она поняла, что сказала лишнее и щеки ее стали пунцовыми.'
            elif DressBuyIsRelative == 2:
                '"Он мой покровитель, а не кавалер!" воскликнула [_rn]. "Ах, вот как," протянула Ирма, улыбнувшись. "Вижу, что очень, очень ценящая заботу девушка. Всем бы таких благодетелей, не правда ли, Стефан?"'
            else:
                'Та зарделась от комплимента.'

            'Вы смогли лишь согласно кивнуть Ирме и под ее пристальным взглядом отсчитали ей [_gds_dress_cost(DressToBuy)] мараведи.'
            call SlutFriendsIncrease("irma", 5, 1, 1, 0, 0, 0)
            call SlutFriendsIncrease(GirlName, 20, 1, 1, 50, 1, 2)
            $ _gds_apply_purchase(GirlName, DressToBuy, set_legsdef=True, set_legs=True, set_produced=False)
            call stat
            $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
            show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
            return

        '"Ой, какие хорошенькие чулочки," восхитилась [_rn]. "Они мне?! Спасибочки!" С этими словами она взяла ваш подарочек, явно намереваясь одеть его позже.'
        '"А примерить? Вдруг не подойдут?" попробовали вы подначить одариваемую, однако та лишь отмахнулась: "Конечно же подойдут, я и так вижу. Дома примерю!"'
        "Делать нечего, хоть вы и надеялись на большее, но посмотреть на примерку чулочков вам не удалось. Слегка огорченный, вы направили свои стопы к Ирме и выложили перед ней от щедрот своих [_gds_dress_cost(DressToBuy)] мараведи."
        call SlutFriendsIncrease(GirlName, 20, 1, 1, 0, 0, 0)
        $ _gds_apply_purchase(GirlName, DressToBuy, set_legsdef=True, set_legs=False, set_produced=False)
        call stat
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    $ _top_slut, _bottom_slut = _gds_dress_top_bottom_slut(DressToBuy)

    if _slut < 40 and _top_slut >= 5:
        '"Не, ну ты чего?" удивилась вашему выбору [_rn]. "Тут же сиськи практически наружу. Да если и не поворачиваться - все равно все будет видно. Я такое не то, что одевать, в комнате своей не хочу хранить."'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if _slut < 20 and _top_slut >= 3:
        '"Стефан, ты видел эту блузку? В ней же все открыто. Она на грани приличия, вернее уже за гранью," попеняла вам [_rn]. "А я девушка приличная и мне нужны приличные платья."'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if _slut < 10 and _top_slut >= 2:
        '"Стефан, это платье конечно милое, но какое-то черезчур смелое. Не думаю, что я смогу такое, с вырезом, носить," засмущалась [_rn]. "Давай пока посмотрим другие платья, поскромнее."'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if _slut < 55 and _bottom_slut >= 5:
        '"Ну ты и выбрал! Наверное членом думал," прокоментировала ваш выбор [_rn]. "С такой юбочкой наклонишься и все видно. Сам такое носи."'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if _slut < 35 and _bottom_slut >= 3:
        '"Долго думал? Я такую юбочку не то что на люди, в комнате своей не одену," не одобрила ваш выбор [_rn]. "Если хочешь мне подарок сделать, то давай что-то другое купим."'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if _slut < 20 and _bottom_slut >= 2:
        '"Ну все таки такое платье слишком смелое," зарделась [_rn]. "Давай посмотрим другие, такие чтоб подол до пола был."'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    if ((_slut >= 35 and _top_slut < 2) or (_slut >= 55 and _top_slut < 3) or (_slut >= 70 and _top_slut < 6) or (_slut >= 45 and _bottom_slut < 2) or (_slut >= 60 and _bottom_slut < 3) or (_slut >= 75 and _bottom_slut < 6)):
        '"Стефан, я по твоему кто? Грымза какая или серая мышка? Зачем ты мне суешь это платье, которое слишком скромно и для сорокалетней девственницы? Давай другие посмотрим, понаряднее и попривлекательней."'
        $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
        show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
        return

    '"Ой какое миленькое платье!" обрадовалась [_rn]. "Ты хочешь мне такое заказать?"'
    '"Ну да, если оно тебе нравится, то давай я закажу," ответили вы демонстрируя присущую вам щедрость и широту души.'
    '"Ой, здорово. Тогда пусть Ирмочка с меня мерку сейчас и снимет, чтобы уже сегодня могла начать кроить и шить!"'

    call GirlSuggestDressFunc(GirlName, DressToBuy, ShowOffLevel, DressBuyIsRelative)
    if str(dress_shop.produced or "") == str(DressToBuy or ""):
        jump ArtisansQuarter
    $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
    show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
    return
