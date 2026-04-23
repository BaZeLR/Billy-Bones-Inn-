init 6 python:
    def tavern_atic_search_available():
        return int(AtticLootFound or 0) == 0

    def tavern_atic_supply_search_available():
        return int(AtticLootFound or 0) == 1 and int(AtticSupplyLootFound or 0) == 0

    def tavern_atic_melissa_investigation_active():
        melissa_sync_room_problem_state()
        return (
            melissa_bats_stage() >= 3
            and melissa_bats_stage() < 6
            and int(dayspassed or 0) >= int(MelissaVar.get("bat_attic_check_day", -1) or -1)
        )

    def tavern_atic_melissa_colony_search_available():
        return (
            tavern_atic_melissa_investigation_active()
            and melissa_bats_stage() == 3
        )

    def tavern_atic_melissa_window_search_available():
        return (
            tavern_atic_melissa_investigation_active()
            and melissa_bats_stage() == 4
        )

    def tavern_atic_visible_items():
        items = []
        seen_item_ids = set()
        for row in list(getattr(TavernAticRoom, "game_items", []) or []):
            item_obj = row
            if isinstance(row, str):
                item_obj = get_game_item(row, TavernAticRoom)
            if item_obj is None:
                continue
            item_id = str(getattr(item_obj, "object_id", "") or "").strip()
            if item_id in seen_item_ids:
                continue
            if hasattr(item_obj, "is_visible") and not item_obj.is_visible():
                continue
            seen_item_ids.add(item_id)
            items.append(item_obj)
        return items

    TavernAticRoom = Room(
        code_name="TavernAtic",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Чердак",
        bg_picture="images/tavern/myroom/playr_room attic.png",
        descriptions=[
            RoomDescription(
                text="Вы выбираетесь на пыльный чердак трактира. Под самой крышей темно, пахнет старым деревом, сухой пылью и забытыми вещами. Между балками навалены какие-то ящики, тряпье и обломки мебели.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Спуститься обратно в комнату", target="TavernMyRoom"),
        ],
        game_items=[],
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
    )


label TavernAtic:
    call EnterLocation("TavernAtic")
    $ CurrentRoom = TavernAticRoom
    $ CurLoc = "TavernAtic"
    $ location = CurLoc
    $ scene_image = attic_room_picture_path() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = TavernAticRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    jump TavernAticView


label TavernAticView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernAticView


label TavernAticBuildActions:
    $ melissa_sync_room_problem_state()
    $ current_action_title = "Чердак"
    $ current_action_content = None
    $ current_action_items = []
    if tavern_atic_search_available():
        $ current_action_items.append(MenuItem("Порыться в старом хламе", Call("TavernAticSearch")))
    elif tavern_atic_supply_search_available():
        $ current_action_items.append(MenuItem("Порыться в старом хламе еще раз", Call("TavernAticSupplySearch")))
    if story_event_available("TavernAtic", "melissa_bats"):
        $ current_action_items.append(MenuItem(melissa_bat_attic_event_caption(), Call("checkTriggers", "TavernAtic", "melissa_bats", 0)))
    python:
        for _atic_item in tavern_atic_visible_items():
            _atic_item_id = str(getattr(_atic_item, "object_id", "") or "")
            _atic_count = _room_item_count_by_id(TavernAticRoom, _atic_item_id)
            _atic_caption = str(_atic_item.name or _atic_item_id)
            if _atic_count > 1:
                _atic_caption = "{} x{}".format(_atic_caption, _atic_count)
            current_action_items.append(MenuItem(_atic_caption, Call("TavernAticObjectMenu", _atic_item_id)))
        for _exit in TavernAticRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
    return


label TavernAticSearch:
    if int(AtticLootFound or 0) == 0:
        $ AtticLootFound = 1
        python:
            for _loot_id in ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001"):
                if not _room_has_item_by_id(TavernAticRoom, _loot_id):
                    _room_add_item_by_id(TavernAticRoom, _loot_id)
        $ MainTxt = "Вы долго роетесь среди ящиков, тряпья и обломков мебели. В дальнем углу под кучей пыли находятся {b}очень старая книга с рецептами{/b}, {b}ржавая охотничья винтовка-арбалет{/b} и {b}старый кожаный кирас{/b}."
    else:
        $ MainTxt = "Вы снова шевелите старый хлам, но больше ничего ценного не обнаруживаете."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return


label TavernAticSupplySearch:
    if int(AtticSupplyLootFound or 0) == 0:
        $ AtticSupplyLootFound = 1
        $ _player_add_item_by_id("droplets_001", 5)
        $ _player_add_item_by_id("gunpowder_001", 5)
        $ MainTxt = "Вы снова перетряхиваете старый хлам и в дальнем ящике находите завернутые в промасленную тряпку припасы: {b}дробь{/b} и {b}порох{/b}. Этого хватит примерно на пять хороших выстрелов. Вы сразу забираете находку с собой."
    else:
        $ MainTxt = "После второго тщательного обыска чердак больше ничем полезным не радует."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return


label MelissaAtticColonySearch:
    if not tavern_atic_melissa_colony_search_available():
        call TavernAticBuildActions
        return
    $ _attic_picture = melissa_attic_picture_path()
    if str(_attic_picture or "").strip():
        call ShowImage("", "", _attic_picture)
    # Stage 4: attic colony was found.
    $ MelissaVar["bats_episode"] = max(int(MelissaVar.get("bats_episode", 0) or 0), 4)
    $ MainTxt = "Вы медленно обходите чердак вдоль стропил и почти сразу замечаете над той частью дома, где спит Мелисса, старые щели между досками и темные ходы в подгнившей обшивке. Значит, подозрение было верным: снизу она видела не просто трещины в потолке, а настоящий выход под самую крышу.\n\nЕще через пару шагов находится и главная причина ночного шума. Под самой кровлей набилось сухое гнездовое тряпье, комки мха, помет и целая дрянная колония, давно обжившая балки и пустоты под крышей. Теперь ясно, почему внизу по ночам все шуршит и пищит. Одним веником тут не обойтись: сначала эту пакость придется выкурить дымом, а потом уже по-настоящему заделывать щели и приводить крышу в порядок."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return


label MelissaAtticWindowPeek:
    if not tavern_atic_melissa_window_search_available():
        call TavernAticBuildActions
        return
    # Stage 5: attic window peek happened and the scandal can trigger.
    $ MelissaVar["bats_episode"] = max(int(MelissaVar.get("bats_episode", 0) or 0), 5)
    $ MainTxt = "Раздвинув старое тряпье и осторожно пригнувшись, вы находите маленькое слуховое окно над стороной дома, где расположена комната Аманды. Сквозь мутное стекло и щели в раме открывается слишком уж ясный вид на соседний двор.\n\n" + attic_neighbor_sex_scene_text() + " Вы невольно задерживаетесь у окна дольше, чем следовало бы."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Чердак"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Податься ближе", Call("MelissaAtticFallScene")), MenuItem("Отступить от окна", Call("TavernAticBuildActions"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label MelissaBurnAtticColony:
    if int(_player_item_count_by_id("bat_repellent_001") or 0) <= 0 or melissa_bats_stage() < 4:
        call TavernAticBuildActions
        return
    $ _player_remove_item_by_id("bat_repellent_001", 1)
    # Stage 7: colony was smoked out; roof repair / final cleanup still pending.
    $ MelissaVar["bats_episode"] = max(int(MelissaVar.get("bats_episode", 0) or 0), 7)
    $ MelissaVar["bat_recipe_unlocked"] = 1
    $ MainTxt = "Вы раскладываете дымную смесь между балок, даете ей как следует разгореться и быстро отступаете. Чердак наполняется густым едким дымом из мха, лаванды и трав. Из-под крыши с писком и хлопаньем вырываются летучие мыши, а мышиная дрянь начинает в панике разбегаться по щелям.\n\nГнездовище вы наконец выкурили, но на одном дыме дело не закончится: пока крышу не заделают как следует, щели останутся и вся пакость со временем полезет обратно."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return


label MelissaOrderRoofRepair:
    if melissa_bats_stage() < 7 or int(MelissaVar.get("roof_repair_order_day", -1) or -1) >= 0:
        call TavernAticBuildActions
        return
    if int(money or 0) < 1000:
        $ MainTxt = "На починку крыши сейчас не хватает денег."
        $ CurLocDesc = MainTxt
        call TavernAticBuildActions
        return
    $ money = int(money or 0) - 1000
    $ MelissaVar["roof_repair_order_day"] = int(dayspassed or 0)
    $ MelissaVar["roof_repair_complete_day"] = int(dayspassed or 0) + 2
    $ MainTxt = "Вы договариваетесь о починке старой крыши и отдаете за работу тысячу монет. Теперь остается только дождаться, пока мастера перетянут гнилые доски, забьют щели и приведут верх трактира в порядок. Обещают управиться за пару дней."
    $ CurLocDesc = MainTxt
    $ story_thread_advance_current()
    call stat
    call TavernAticBuildActions
    return


label MelissaCheckRoofRepair:
    $ melissa_sync_room_problem_state()
    if melissa_bats_stage() >= 8 or melissa_bats_repair_complete():
        $ MainTxt = "Теперь все видно сразу: крыша над комнатой Мелиссы наконец подлатана, щели закрыты, а прежнее гнездовище выжжено и вычищено. Похоже, на этот раз проблема действительно решена."
        $ CurLocDesc = MainTxt
        call TavernAticBuildActions
        return
    if int(MelissaVar.get("roof_repair_complete_day", -1) or -1) > int(dayspassed or 0):
        $ _days_left = int(MelissaVar.get("roof_repair_complete_day", -1) or -1) - int(dayspassed or 0)
        $ MainTxt = "Работа над крышей еще не закончена. Придется подождать еще примерно {} дн.".format(_days_left)
        $ CurLocDesc = MainTxt
        call TavernAticBuildActions
        return
    $ melissa_sync_room_problem_state()
    $ MainTxt = "Крыша уже должна быть готова. Судя по виду балок и свежим заплатам, мастера и правда сделали свое дело. Теперь под потолком тихо, и дряни сверху больше взяться неоткуда."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return


label TavernAticObjectMenu(object_id="", refresh_only=False):
    $ _atic_item = get_game_item(object_id, TavernAticRoom)
    if _atic_item is None or not _room_has_item_by_id(TavernAticRoom, object_id):
        call TavernAticBuildActions
        return
    $ scene_image = attic_item_picture_path(object_id) or attic_room_picture_path() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = str(_atic_item.description or "")
    if _room_item_count_by_id(TavernAticRoom, object_id) > 1:
        $ MainTxt = MainTxt + "\n\nЗдесь лежит несколько одинаковых предметов: {}.".format(_room_item_count_by_id(TavernAticRoom, object_id))
    $ CurLocDesc = MainTxt
    $ current_action_title = str(_atic_item.name or "Чердак")
    $ current_action_content = None
    $ current_action_items = []
    python:
        _atic_has_take_action = False
        for _atic_action in _atic_item.visible_actions():
            _atic_args = tuple(getattr(_atic_action, "args", ()) or ())
            if str(getattr(_atic_action, "target", "") or "") == "Take":
                _atic_has_take_action = True
            if _atic_action.hook == "text":
                current_action_items.append(MenuItem(_atic_action.label, Call("TavernAticObjectText", object_id, _atic_action.action_id)))
            elif _atic_action.hook == "call" and str(_atic_action.target or "") != "":
                current_action_items.append(MenuItem(_atic_action.label, Call(_atic_action.target, *_atic_args)))
            elif _atic_action.hook == "jump" and str(_atic_action.target or "") != "":
                current_action_items.append(MenuItem(_atic_action.label, Jump(_atic_action.target)))
        if bool(getattr(_atic_item, "carriable", False)) and not _atic_has_take_action:
            current_action_items.append(MenuItem("Взять", Call("Take", object_id, "TavernAtic", "", object_id)))
    $ current_action_items.append(MenuItem("Назад", Call("TavernAticRestore")))
    return


label TavernAticObjectText(object_id="", action_id=""):
    python:
        _atic_text = ""
        _atic_item = get_game_item(object_id, TavernAticRoom)
        if _atic_item is not None:
            for _atic_action in _atic_item.visible_actions():
                if getattr(_atic_action, "action_id", "") == str(action_id or ""):
                    _atic_text = str(_atic_action.target or "")
                    break
        if _atic_text:
            MainTxt = _atic_text
            CurLocDesc = _atic_text
    call TavernAticObjectMenu(object_id)
    return


label TavernAticRestore:
    $ scene_image = attic_room_picture_path() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = TavernAticRoom.descriptions[0].text
    if int(AtticLootFound or 0) == 1:
        $ MainTxt = MainTxt + "\n\nВы уже перерыли здесь хлам и теперь знаете, где лежат найденные вещи."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return
