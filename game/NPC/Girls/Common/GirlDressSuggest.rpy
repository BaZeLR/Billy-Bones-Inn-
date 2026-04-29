# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.store as store

    def _gds_get_dict(name):
        value = getattr(store, name, None)
        if not isinstance(value, dict):
            value = {}
            setattr(store, name, value)
        return value

    def _gds_get_list(name):
        value = getattr(store, name, None)
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            value = list(value)
            setattr(store, name, value)
            return value
        if isinstance(value, dict):
            ordered = []
            for _gds_key, v in sorted(value.items(), key=lambda kv: str(kv[0])):
                s = str(v or "").strip()
                if s:
                    ordered.append(s)
            setattr(store, name, ordered)
            return ordered
        value = []
        setattr(store, name, value)
        return value

    def _gds_name(dict_name, girl_key):
        table = _gds_get_dict(dict_name)
        key = str(girl_key or "")
        return str(table.get(key, key))

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
        _gds_get_dict("Friends").setdefault(g, 0)
        _gds_get_dict("sluttiness").setdefault(g, 0)
        _gds_get_dict("HadSex").setdefault(g, 0)
        _gds_get_dict("pregnancy").setdefault(g, 0)

    def _gds_showoff_level(girl_name):
        g = str(girl_name or "")
        sluttiness = _gds_get_dict("sluttiness")
        had_sex = _gds_get_dict("HadSex")
        friends = _gds_get_dict("Friends")

        girl_slut = int(sluttiness.get(g, 0) or 0)
        girl_had = int(had_sex.get(g, 0) or 0)
        girl_friend = int(friends.get(g, 0) or 0)

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
        key = str(girl_name or "") + "Dresses"
        return _gds_get_list(key)

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
        cost_map = _gds_get_dict("DressCost")
        return int(cost_map.get(str(dress_code or ""), 0) or 0)

    def _gds_dress_top_bottom_slut(dress_code):
        top_map = _gds_get_dict("DressTopPart")
        bottom_map = _gds_get_dict("DressBottomPart")
        part_slut = _gds_get_dict("DressPartSlut")
        d = str(dress_code or "")
        top_name = str(top_map.get(d, "") or "")
        bottom_name = str(bottom_map.get(d, "") or "")
        top_slut = int(part_slut.get(top_name, 0) or 0)
        bottom_slut = int(part_slut.get(bottom_name, 0) or 0)
        return top_slut, bottom_slut

    def _gds_apply_purchase(girl_name, dress_code, set_legsdef=False, set_legs=False, set_produced=False):
        g = str(girl_name or "")
        d = str(dress_code or "")
        if g == "" or d == "":
            return 0

        cost = _gds_dress_cost(d)
        money_val = int(getattr(store, "money", 0) or 0) - cost
        setattr(store, "money", money_val)

        _gds_add_dress_for_girl(g, d)

        if set_legsdef:
            legsdef = _gds_get_dict("legsdef")
            legsdef[g] = d
        if set_legs:
            legs = _gds_get_dict("legs")
            legs[g] = d

        bought = int(getattr(store, "GirlDressesBought", 0) or 0)
        setattr(store, "GirlDressesBought", bought + 1)

        if set_produced:
            setattr(store, "DressProduced", d)
            try:
                household_mark_revealing_dress_order(g, d)
            except Exception:
                pass

        return cost

    def _gds_player_hadsex():
        had = _gds_get_dict("HadSex")
        return int(had.get("you", had.get("You", 0)) or 0)

    def _gds_player_cum_today():
        value = getattr(store, "cametoday", 0)
        if isinstance(value, dict):
            return int(value.get("You", value.get("you", 0)) or 0)
        return int(value or 0)

    def _gds_player_cum_cap():
        value = getattr(store, "cancumdaily", 0)
        if isinstance(value, dict):
            return int(value.get("You", value.get("you", 0)) or 0)
        return int(value or 0)

    def _gds_relative_callout_name(girl_name):
        girl = str(girl_name or "").strip().lower()
        if girl == "sandra":
            return "Сандра"
        if girl == "amanda":
            return "Аманда"
        if girl == "melissa":
            return "Мелисса"
        return str(_gds_name("RealName", girl_name))


label GirlDressSuggest(GirlName="", DressToBuy=""):
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        return

    $ _girl_dress_restore_buy_menu = (str(CurLoc or "") == "GirlDressBuy")
    hide screen main_ui
    $ _gds_ensure_stats(GirlName)
    $ _gds_ensure_stats("irma")

    $ DressBuyIsRelative = _gds_relative_type(GirlName)
    $ ShowOffLevel = _gds_showoff_level(GirlName)

    if renpy.has_label("CleanScreenOverflow"):
        call CleanScreenOverflow

    $ _rn = _gds_name("RealName", GirlName)
    $ _short_name = str(_gds_get_dict("ShortDressName").get(DressToBuy, DressToBuy)).lower()

    '"[_rn]", предложили вы, а давай я куплю тебе [_short_name]?'

    python:
        _gds_dress_id = str(DressToBuy or "").lower()
        _is_bra = "bra" in _gds_dress_id
        _is_panties = "panties" in _gds_dress_id
        _is_stockings = "stockings" in _gds_dress_id
        _slut = int(_gds_get_dict("sluttiness").get(GirlName, 0) or 0)

    if _is_bra:
        if GirlName == "georgett":
            '"Лифчик?" удивилась шлюха. "А зачем он мне? Вот, посомтри на мои титьки, какие они сочные, мужики так и налетают" и с этими словами она приподняла и чуть сжала предметы обсуждения, да так, что левый сосок даже выскочил из плена декольте. "Ну и зачем их лифом скрывать? Не дури."'
        elif GirlName == "liza":
            '"Лифчик?" удивилась мулатка. "Мама мне говорила, что нельзя лиф носить, титьки из-за этого плохо будут расти. Так что не, дяденька Стефан, такой подарок мне не нужон!"'
        else:
            '"Лифчик?" удивилась [_rn]. "Не, спасибо конечно, но он мне не нужен!"'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if _is_panties:
        if GirlName == "georgett":
            '"Панталоны?" удивилась шлюха. "Да я их и не носила никогда! Юбочки вполне достаточно! Только время тратить, снимать-одевать, снимать-одевать, снимать-одевать и так по десять раз на дню. Не, не надо мне такого счастья."'
        else:
            '"Панталончики?" удивилась [_rn]. "Не, спасибо конечно, но они мне не нужны!"'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if _is_stockings:
        if _slut < 15:
            '"Ой, чулочки! Ну не знаю, нужны ли они мне?" скромно заметила [_rn]. "Наверное нет, я же никому свои ножки показывать не собираюсь. Давай лучше еще что-то посмотрим."'
            call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
            return

        if ShowOffLevel > 1:
            $ _legs_now = str(_gds_get_dict("legsdef").get(GirlName, "") or "")
            $ _panties_now = str(_gds_get_dict("panties").get(GirlName, "") or "")

            if _legs_now != "":
                '"О, еще чулочки," обрадованно сказала [_rn]. Лукаво посмотрев на вас, она присела на лавочку, сбросила обувку, и начала стягивать с себя [str(_gds_get_dict("ShortDressName").get(_legs_now, _legs_now)).lower()] дабы примерить обновку.'
            else:
                '"О, чулочки," обрадованно сказала [_rn]. Лукаво посмотрев на вас, она присела на лавочку, сбросила обувку, и начала натягивать подарок на свои стройные ножки.'

            if _panties_now != "":
                'Задравшийся при этом подол платья ее ничуть не обеспокоил. Впрочем, под ним обнаружились [str(_gds_get_dict("ShortDressName").get(_panties_now, _panties_now)).lower()], скрывшие все самое интересное от вашего любопытного взора.'
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
            call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
            return

        '"Ой, какие хорошенькие чулочки," восхитилась [_rn]. "Они мне?! Спасибочки!" С этими словами она взяла ваш подарочек, явно намереваясь одеть его позже.'
        '"А примерить? Вдруг не подойдут?" попробовали вы подначить одариваемую, однако та лишь отмахнулась: "Конечно же подойдут, я и так вижу. Дома примерю!"'
        "Делать нечего, хоть вы и надеялись на большее, но посмотреть на примерку чулочков вам не удалось. Слегка огорченный, вы направили свои стопы к Ирме и выложили перед ней от щедрот своих [_gds_dress_cost(DressToBuy)] мараведи."
        call SlutFriendsIncrease(GirlName, 20, 1, 1, 0, 0, 0)
        $ _gds_apply_purchase(GirlName, DressToBuy, set_legsdef=True, set_legs=False, set_produced=False)
        call stat
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    $ _top_slut, _bottom_slut = _gds_dress_top_bottom_slut(DressToBuy)

    if _slut < 40 and _top_slut >= 5:
        '"Не, ну ты чего?" удивилась вашему выбору [_rn]. "Тут же сиськи практически наружу. Да если и не поворачиваться - все равно все будет видно. Я такое не то, что одевать, в комнате своей не хочу хранить."'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if _slut < 20 and _top_slut >= 3:
        '"Стефан, ты видел эту блузку? В ней же все открыто. Она на грани приличия, вернее уже за гранью," попеняла вам [_rn]. "А я девушка приличная и мне нужны приличные платья."'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if _slut < 10 and _top_slut >= 2:
        '"Стефан, это платье конечно милое, но какое-то черезчур смелое. Не думаю, что я смогу такое, с вырезом, носить," засмущалась [_rn]. "Давай пока посмотрим другие платья, поскромнее."'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if _slut < 55 and _bottom_slut >= 5:
        '"Ну ты и выбрал! Наверное членом думал," прокоментировала ваш выбор [_rn]. "С такой юбочкой наклонишься и все видно. Сам такое носи."'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if _slut < 35 and _bottom_slut >= 3:
        '"Долго думал? Я такую юбочку не то что на люди, в комнате своей не одену," не одобрила ваш выбор [_rn]. "Если хочешь мне подарок сделать, то давай что-то другое купим."'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if _slut < 20 and _bottom_slut >= 2:
        '"Ну все таки такое платье слишком смелое," зарделась [_rn]. "Давай посмотрим другие, такие чтоб подол до пола был."'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    if ((_slut >= 35 and _top_slut < 2) or (_slut >= 55 and _top_slut < 3) or (_slut >= 70 and _top_slut < 6) or (_slut >= 45 and _bottom_slut < 2) or (_slut >= 60 and _bottom_slut < 3) or (_slut >= 75 and _bottom_slut < 6)):
        '"Стефан, я по твоему кто? Грымза какая или серая мышка? Зачем ты мне суешь это платье, которое слишком скромно и для сорокалетней девственницы? Давай другие посмотрим, понаряднее и попривлекательней."'
        call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
        return

    '"Ой какое миленькое платье!" обрадовалась [_rn]. "Ты хочешь мне такое заказать?"'
    '"Ну да, если оно тебе нравится, то давай я закажу," ответили вы демонстрируя присущую вам щедрость и широту души.'
    '"Ой, здорово. Тогда пусть Ирмочка с меня мерку сейчас и снимет, чтобы уже сегодня могла начать кроить и шить!"'

    call GirlSuggestDressFunc(GirlName, DressToBuy, ShowOffLevel, DressBuyIsRelative)
    call GirlDressSuggestRestore(GirlName, _girl_dress_restore_buy_menu)
    return


label GirlDressSuggestRestore(GirlName="", should_restore=False):
    if should_restore:
        call GirlDressBuyRefresh(GirlName)
        show screen main_ui
    return


label girl_dress_suggest(girl_name="", dress_to_buy=""):
    call GirlDressSuggest(girl_name, dress_to_buy)
    return
