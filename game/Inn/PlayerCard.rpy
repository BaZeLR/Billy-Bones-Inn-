init python:
    import renpy.exports as renpy_module

    def player_card_main_menu_items():
        return [
            MenuItem("Проверить вещи", Function(main_ui_call_label, "PlayerCardInventoryMenu")),
            MenuItem("Назад", Function(main_ui_restore_room_scene_state)),
        ]

    def show_player_card_main_ui_state():
        store = renpy.store
        store.UI_mode = "mc"
        store.UI_selected_char = "you"
        store.current_action_title = "Стефан"
        store.current_action_content = None
        store.current_action_items = player_card_main_menu_items()
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_hygiene_text():
        wash_days = int(dayssincewash or 0)

        if wash_days <= 0:
            return "свежий"
        if wash_days <= 1:
            return "чистый"
        if wash_days <= 2:
            return "терпимый"
        if wash_days <= 4:
            return "грязноват"
        return "грязный"

    def player_card_current_dress_code():
        return str(MyCurDress or "")

    def player_card_display_name():
        return "Стефан Лонгкок"

    def player_card_exploration_title():
        exploration_value = int(effective_player_exploration() or 0)
        if exploration_value >= 150:
            return "матерый охотник и лесной следопыт"
        if exploration_value >= 100:
            return "опытный охотник, привыкший читать следы и лесные тропы"
        if exploration_value >= 75:
            return "уже не просто трактирщик, а уверенный следопыт"
        if exploration_value >= 50:
            return "начинающий охотник, который учится понимать лес"
        if exploration_value >= 25:
            return "любопытный бродяга, все чаще выбирающийся за пределы трактира"
        return "наследник трактира, только начинающий смотреть дальше собственного двора"

    def player_card_equipment_lines():
        lines = []
        if str(EquippedArmor or "") == "old_leather_cuirass_001":
            lines.append("Поверх одежды на вас затянута старая кожаная кираса, придающая вам суровый и дорожный вид.")
        if str(EquippedWeapon or "") == "rusty_hunter_rifle_001":
            if rusty_hunter_rifle_is_oiled() and rusty_hunter_rifle_is_cleaned():
                lines.append("За плечом у вас висит уже приведенная в порядок старая охотничья винтовка, придавая вам почти настоящий охотничий облик.")
            else:
                lines.append("За плечом у вас висит старая охотничья винтовка, и даже в ее потрепанном виде она делает вас больше похожим на лесного добытчика, чем на трактирщика.")
        return lines

    def player_card_portrait_path():
        return "images/rpg_message_bg.png"

    def player_card_stat_rows_left():
        exploration_value = int(effective_player_exploration() or 0)
        exploration_text = str(exploration_value)
        if bool(getattr(dog, "owned", False)):
            exploration_text += " (с псом)"
        return [
            ("Возраст", str(age)),
            ("Деньги", str(money)),
            ("Репутация", str(notoriety)),
            ("Слава трактира", str(tavernfame)),
            ("Внешность", str(look)),
            ("Харизма", str(charisma)),
            ("Исследование", exploration_text),
            ("Гигиена", player_card_hygiene_text()),
        ]

    def player_card_stat_rows_right():
        return [
            ("Энергия", str(energy)),
            ("Веселье", str(fun)),
            ("Секс", str(HadSex.get("You", 0))),
            ("Раз за день", str(cancumdaily)),
            ("Сегодня", str(cametoday)),
        ]

    def player_card_dress_lines():
        current_dress = player_card_current_dress_code()
        if not current_dress:
            return []

        dress_name = str(ShortDressName.get(current_dress, current_dress) or current_dress)
        dress_desc = str(DressDesc.get(current_dress, current_dress) or current_dress)
        full_desc = str(FullDressDesc.get(current_dress, "") or "").strip()

        lines = [
            "Основной наряд: %s." % dress_name,
            "Сейчас на вас: %s." % dress_name.lower(),
            "Кратко: %s." % dress_desc,
        ]
        if full_desc:
            lines.append(full_desc + ".")
        return lines

    def player_card_inventory_lines():
        try:
            sync_soap_batches_with_day()
        except Exception:
            pass
        item_ids = list(_player_inventory_item_ids(False))

        if len(item_ids) <= 0:
            return ["В инвентаре сейчас ничего нет."]

        lines = ["При себе:"]
        for item_id in item_ids:
            game_item = get_game_item(item_id)
            item_name = str(game_item.name).strip() if game_item is not None else str(item_id)
            item_count = int(_player_item_count_by_id(item_id) or 0)
            if item_count > 1:
                lines.append("- %s x%s" % (item_name, item_count))
            else:
                lines.append("- " + item_name)
        return lines

    def player_card_item_display_name(item_id):
        return runtime_item_display_name(item_id)

    def player_card_item_description_text(item_id):
        return runtime_item_description_text(item_id)

    def player_card_inventory_menu_caption(item_id):
        _item_id = str(item_id or "").strip()
        _item_name = player_card_item_display_name(_item_id)
        _item_count = int(_player_item_count_by_id(_item_id) or 0)
        if _item_count > 1:
            return "%s x%s" % (_item_name, _item_count)
        return _item_name

    def player_card_item_status_lines(item_id):
        _item_id = str(item_id or "").strip()
        _item_obj = get_game_item(_item_id)
        if _item_obj is None:
            return []

        _lines = []
        _item_count = int(_player_item_count_by_id(_item_id) or 0)
        if _item_count > 1:
            _lines.append("Сейчас у вас при себе %s единицы этого добра." % _item_count)
        elif _item_count == 1:
            _lines.append("Сейчас у вас при себе только одна такая вещь.")

        if str(_item_id) == str(EquippedWeapon or ""):
            _lines.append("Сейчас это оружие у вас при себе и готово к делу.")
        if str(_item_id) == str(EquippedArmor or ""):
            _lines.append("Эта вещь сейчас на вас.")
        if _item_id == "rusty_hunter_rifle_001":
            _lines.extend(list(rusty_hunter_rifle_status_lines() or []))
        return _lines

    def player_card_get_item_action(item_id, action_id):
        _item_obj = get_game_item(item_id)
        _action_key = str(action_id or "").strip()
        if _item_obj is None or not _action_key:
            return None
        for _action in list(_item_obj.visible_actions() or []):
            if str(getattr(_action, "action_id", "") or "").strip() == _action_key:
                return _action
        return None

    def player_card_item_action_menu_item(item_id, action):
        _item_id = str(item_id or "").strip()
        _action = action
        _hook = str(getattr(_action, "hook", "") or "").strip().lower()
        _caption = str(getattr(_action, "label", "") or "").strip()
        _target = str(getattr(_action, "target", "") or "").strip()
        _args = tuple(getattr(_action, "args", ()) or ())

        if not _caption:
            return None

        if _hook == "text":
            return MenuItem(_caption, Function(main_ui_call_label, "PlayerCardItemTextAction", _item_id, getattr(_action, "action_id", "")))
        if _hook == "call" and _target:
            return MenuItem(_caption, Function(main_ui_call_label, _target, *_args))
        if _hook == "jump" and _target:
            return MenuItem(_caption, Jump(_target))
        return None

    def player_card_extra_item_actions(item_id):
        _item_id = str(item_id or "").strip()
        _items = []
        _item_obj = get_game_item(_item_id)
        _custom_props = dict(getattr(_item_obj, "custom_properties", {}) or {}) if _item_obj is not None else {}
        if int(_custom_props.get("gift_value", 0) or 0) > 0 and player_card_can_offer_direct_social_action(_item_id):
            _items.append(MenuItem("Подарить", Function(main_ui_call_label, "PlayerCardGiftItemMenu", _item_id)))
        if str(_custom_props.get("item_kind", "") or "") in ("drink", "forest_resource", "crafted_good", "ingredient") and player_card_can_offer_direct_social_action(_item_id):
            _items.append(MenuItem("Поделиться", Function(main_ui_call_label, "PlayerCardShareItemMenu", _item_id)))
        if _item_id == "rusty_hunter_rifle_001":
            if rusty_hunter_rifle_can_clean():
                _items.append(MenuItem("Счистить ржавчину", Function(main_ui_call_label, "PlayerCardRifleCleanRust")))
            if rusty_hunter_rifle_can_oil():
                _items.append(MenuItem("Смазать механизм", Function(main_ui_call_label, "PlayerCardRifleOil")))
            if rusty_hunter_rifle_can_load("arrows"):
                _items.append(MenuItem("Зарядить стрелой", Function(main_ui_call_label, "PlayerCardRifleLoadAmmo", "arrows")))
            if rusty_hunter_rifle_can_load("droplets"):
                _items.append(MenuItem("Зарядить дробью", Function(main_ui_call_label, "PlayerCardRifleLoadAmmo", "droplets")))
            if rusty_hunter_rifle_can_unload():
                _items.append(MenuItem("Разрядить оружие", Function(main_ui_call_label, "PlayerCardRifleUnload")))
        return _items

    def player_card_body_lines():
        lines = [
            "Стефан Лонгкок, %s." % player_card_exploration_title(),
        ]
        if bool(getattr(dog, "owned", False)):
            lines.append("Рядом с вами держится верный пес, и вместе с ним вы чувствуете себя в лесу заметно увереннее.")
        lines.extend(player_card_equipment_lines())
        lines.extend(player_card_dress_lines())
        lines.extend(player_card_inventory_lines())
        lines.append("В вашем гардеробе %s костюмов." % str(len(list(MyDresses or []))))
        return [line for line in lines if str(line or "").strip()]


label ShowPlayerCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ show_player_card_main_ui_state()
        return
    show screen player_card_overlay(return_label)
    return


label HidePlayerCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ main_ui_restore_room_scene_state()
        return
    hide screen player_card_overlay
    if str(return_label or "") != "":
        call expression return_label
    return


screen player_card_overlay(return_label=""):
    zorder 120

    $ _title = player_card_display_name()
    $ _portrait = player_card_portrait_path()
    $ _stats_left = player_card_stat_rows_left()
    $ _stats_right = player_card_stat_rows_right()
    $ _lines = player_card_body_lines()
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24
    $ _portrait_w = 180
    $ _portrait_h = 240

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add im.Scale("images/rpg_message_bg.png", _left_w, _left_h)

        vbox:
            xpos 28
            ypos 24
            xmaximum _left_w - 56
            spacing 10

            text _title.upper() size 30 color "#1e130c" xalign 0.5

            hbox:
                spacing 12

                add im.Scale(_portrait, _portrait_w, _portrait_h)

                hbox:
                    xmaximum _left_w - _portrait_w - 120
                    spacing 24

                    vbox:
                        xminimum 220
                        spacing 3
                        for _row in _stats_left:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                    vbox:
                        xminimum 220
                        spacing 3
                        for _row in _stats_right:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

            for _line in _lines:
                text _line size 16 color "#2d1d12"

            textbutton "Назад":
                text_size 22
                if str(return_label or "") == "__return__":
                    action Return()
                elif str(return_label or "") == "__hide__":
                    action Hide("player_card_overlay")
                else:
                    action Call("HidePlayerCard", return_label)


label PlayerCardInventoryMenu:
    $ sync_soap_batches_with_day()
    $ UI_mode = "mc"
    $ UI_selected_char = "you"
    $ current_action_title = "Вещи"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _item_id in list(_player_inventory_item_ids(False) or []):
            if int(_player_item_count_by_id(_item_id) or 0) > 0:
                current_action_items.append(MenuItem(player_card_inventory_menu_caption(_item_id), Function(main_ui_call_label, "PlayerCardInventoryItemMenu", _item_id)))
        if len(current_action_items) <= 0:
            MainTxt = "У вас сейчас ничего нет при себе."
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "PlayerCardMainMenu")))
    return


label PlayerCardMainMenu:
    $ show_player_card_main_ui_state()
    return


label PlayerCardInventoryItemMenu(item_id="", preserve_text=False):
    $ sync_soap_batches_with_day()
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(_player_item_count_by_id(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    if not bool(preserve_text):
        python:
            _item_lines = [player_card_item_description_text(_item_id)]
            _item_lines.extend(player_card_item_status_lines(_item_id))
            MainTxt = "\n\n".join([_line for _line in _item_lines if str(_line or "").strip()])
            CurLocDesc = MainTxt
    $ UI_mode = "mc"
    $ UI_selected_char = "you"
    $ current_action_title = player_card_inventory_menu_caption(_item_id)
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _item_action in list(_item_obj.visible_actions() or []):
            _menu_item = player_card_item_action_menu_item(_item_id, _item_action)
            if _menu_item is not None:
                current_action_items.append(_menu_item)
        current_action_items.extend(player_card_extra_item_actions(_item_id))
        current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "PlayerCardInventoryMenu")))
    return


label PlayerCardItemTextAction(item_id="", action_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _item_action = player_card_get_item_action(_item_id, action_id)
    if _item_action is not None:
        $ MainTxt = str(getattr(_item_action, "target", "") or "")
        $ CurLocDesc = MainTxt
    call PlayerCardInventoryItemMenu(_item_id, True)
    return


label PlayerCardRifleCleanRust:
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or _player_item_count_by_id("rusty_hunter_rifle_001") <= 0:
        call PlayerCardInventoryMenu
        return
    if rusty_hunter_rifle_is_cleaned():
        $ MainTxt = "Вы уже счистили основную ржавчину с механизма."
    else:
        $ _rifle_item.state["rust_cleaned"] = 1
        $ MainTxt = "Вы долго скоблите металл, снимаете рыжий налет и понемногу приводите механизм в порядок. Оружие уже не выглядит совсем уж мертвым."
    $ CurLocDesc = MainTxt
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return


label PlayerCardRifleOil:
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or _player_item_count_by_id("rusty_hunter_rifle_001") <= 0:
        call PlayerCardInventoryMenu
        return
    if not rusty_hunter_rifle_is_cleaned():
        $ MainTxt = "Сначала нужно счистить ржавчину, иначе толку от масла будет мало."
    elif rusty_hunter_rifle_is_oiled():
        $ MainTxt = "Механизм уже смазан и ходит заметно мягче."
    elif _player_item_count_by_id("weapon_oil_001") <= 0:
        $ MainTxt = "У вас нет оружейного масла."
    else:
        $ _player_remove_item_by_id("weapon_oil_001", 1)
        $ _rifle_item.state["oiled"] = 1
        $ MainTxt = "Вы аккуратно смазываете механизм оружейным маслом. Скрип уходит, а детали начинают двигаться куда увереннее."
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return


init python:
    def player_card_active_social_target():
        target_key = str(UI_selected_char or current_girl_key or "").strip().lower()
        if str(UI_mode or "") != "talk":
            return ""
        if target_key in ("", "you", "dog"):
            return ""
        if not isinstance(Friends, dict) or target_key not in Friends:
            return ""
        return target_key

    def player_card_item_kind(item_id=""):
        item_obj = get_game_item(item_id)
        if item_obj is None:
            return ""
        return str(getattr(item_obj, "custom_properties", {}).get("item_kind", "") or "").strip()

    def player_card_requires_active_social_target(item_id=""):
        return player_card_item_kind(item_id) in ("drink", "forest_resource", "crafted_good", "ingredient")

    def player_card_can_offer_direct_social_action(item_id=""):
        item_key = str(item_id or "").strip()
        if not player_card_requires_active_social_target(item_key):
            return True
        return player_card_active_social_target() != ""

    def player_card_gift_target_ids(item_id=""):
        item_key = str(item_id or "").strip()
        if player_card_requires_active_social_target(item_key):
            active_target = player_card_active_social_target()
            return [active_target] if active_target else []
        targets = []
        if not isinstance(Friends, dict):
            return targets
        for char_id in sorted(list(Friends.keys())):
            key = str(char_id or "").strip()
            if key == "" or key != key.lower() or key in ("you", "dog"):
                continue
            char_name = _action_display_name(key)
            if char_name == "" or char_name == key:
                continue
            targets.append(key)
        return targets

    def player_card_shareable_item_ids():
        shareable = []
        for item_id in list(_player_inventory_item_ids(False) or []):
            item_obj = get_game_item(item_id)
            if item_obj is None:
                continue
            custom_props = dict(getattr(item_obj, "custom_properties", {}) or {})
            item_kind = str(custom_props.get("item_kind", "") or "").strip()
            loot_kind = str(custom_props.get("loot_kind", "") or "").strip()
            if (
                item_kind in ("drink", "forest_resource", "crafted_good", "ingredient")
                or (item_kind == "animal_loot" and loot_kind == "meat")
            ) and int(_player_item_count_by_id(item_id) or 0) > 0:
                shareable.append(str(item_id))
        return shareable

    def player_card_has_shareable_items():
        return len(list(player_card_shareable_item_ids() or [])) > 0


label PlayerCardGiftItemMenu(item_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(_player_item_count_by_id(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    $ MainTxt = "Кому вы хотите вручить {}?".format(player_card_item_display_name(_item_id))
    $ CurLocDesc = MainTxt
    $ UI_mode = "mc"
    $ UI_selected_char = "you"
    $ current_action_title = "Подарок"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _char_id in player_card_gift_target_ids(_item_id):
            current_action_items.append(MenuItem(_action_display_name(_char_id), Function(main_ui_call_label, "PlayerCardGiftItemTo", _item_id, _char_id)))
        if len(current_action_items) <= 0:
            if player_card_requires_active_social_target(_item_id):
                MainTxt = "Эту вещь можно вручить только тому, с кем вы сейчас уже разговариваете."
            else:
                MainTxt = "Сейчас некому вручить {}.".format(player_card_item_display_name(_item_id))
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "PlayerCardInventoryItemMenu", _item_id, True)))
    return


label PlayerCardGiftItemTo(item_id="", char_name=""):
    $ _item_id = str(item_id or "").strip()
    $ _char_name = str(char_name or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or _char_name == "" or int(_player_item_count_by_id(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    $ _gift_name = player_card_item_display_name(_item_id)
    $ _gift_base = int(getattr(_item_obj, "custom_properties", {}).get("gift_value", 2) or 2)
    $ _removed = _player_remove_item_by_id(_item_id, 1)
    if not bool(_removed):
        $ MainTxt = "Этой вещи у вас больше нет."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryMenu
        return
    $ _gift_result = player_gift_to(_char_name, _gift_name, _gift_base, _item_id)
    $ _effect_result = player_apply_item_social_effects(_char_name, _item_id, True)
    $ MainTxt = str(_gift_result.get("text", "") or "")
    if str(_effect_result.get("text", "") or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + " " + str(_effect_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryMenu
    return


label PlayerCardShareItemMenu(item_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(_player_item_count_by_id(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    $ MainTxt = "С кем вы хотите разделить {}?".format(player_card_item_display_name(_item_id))
    $ CurLocDesc = MainTxt
    $ UI_mode = "mc"
    $ UI_selected_char = "you"
    $ current_action_title = "Поделиться"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _char_id in player_card_gift_target_ids(_item_id):
            current_action_items.append(MenuItem(_action_display_name(_char_id), Function(main_ui_call_label, "PlayerCardShareItemTo", _item_id, _char_id)))
        if len(current_action_items) <= 0:
            MainTxt = "Этим можно делиться только с тем, кто сейчас рядом и уже участвует в разговоре."
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "PlayerCardInventoryItemMenu", _item_id, True)))
    return


label PlayerCardShareToFixedTargetMenu(char_name=""):
    $ _char_name = str(char_name or "").strip()
    if _char_name == "":
        call PlayerCardInventoryMenu
        return
    $ MainTxt = "Чем вы хотите поделиться с {}?".format(_action_display_name(_char_name))
    $ CurLocDesc = MainTxt
    $ UI_mode = "mc"
    $ UI_selected_char = "you"
    $ current_action_title = "Поделиться"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _item_id in list(player_card_shareable_item_ids() or []):
            current_action_items.append(MenuItem(player_card_inventory_menu_caption(_item_id), Function(main_ui_call_label, "PlayerCardShareItemTo", _item_id, _char_name)))
        if len(current_action_items) <= 0:
            MainTxt = "Сейчас вам нечем делиться с {}.".format(_action_display_name(_char_name))
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
    return


label PlayerCardShareItemTo(item_id="", char_name=""):
    $ _item_id = str(item_id or "").strip()
    $ _char_name = str(char_name or "").strip()
    $ _share_result = player_share_item_with(_char_name, _item_id)
    $ MainTxt = str(_share_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryMenu
    return


label PlayerCardGiftToFixedTargetMenu(char_name=""):
    $ _char_name = str(char_name or "").strip()
    if _char_name == "":
        call PlayerCardInventoryMenu
        return
    $ MainTxt = "Что вы хотите подарить {}?".format(_action_display_name(_char_name))
    $ CurLocDesc = MainTxt
    $ UI_mode = "mc"
    $ UI_selected_char = "you"
    $ current_action_title = "Подарок"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _item_id in list(_player_inventory_item_ids(False) or []):
            _item_obj = get_game_item(_item_id)
            _gift_value = int(getattr(_item_obj, "custom_properties", {}).get("gift_value", 0) or 0) if _item_obj is not None else 0
            if _gift_value > 0 and int(_player_item_count_by_id(_item_id) or 0) > 0:
                current_action_items.append(MenuItem(player_card_inventory_menu_caption(_item_id), Function(main_ui_call_label, "PlayerCardGiftItemTo", _item_id, _char_name)))
        if len(current_action_items) <= 0:
            MainTxt = "{} пока нечего вручить.".format(_action_display_name(_char_name))
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
    return


label PlayerCardRifleLoadAmmo(ammo_code="arrows"):
    $ _ammo_code = str(ammo_code or "").strip()
    if not rusty_hunter_rifle_can_load(_ammo_code):
        $ MainTxt = "Сейчас оружие нельзя так зарядить."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
        return
    if _ammo_code == "arrows":
        $ _player_remove_item_by_id("arrows_001", 1)
    elif _ammo_code == "droplets":
        $ _player_remove_item_by_id("droplets_001", 1)
        $ _player_remove_item_by_id("gunpowder_001", 1)
    $ RustyHunterRifleLoadedAmmo = _ammo_code
    $ MainTxt = "Вы заряжаете оружие {} и осторожно ставите механизм наготове.".format(rusty_hunter_rifle_ammo_name(_ammo_code))
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return


label PlayerCardRifleUnload:
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ MainTxt = "Оружие и так уже разряжено."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
        return
    if _loaded_ammo == "arrows":
        $ _player_add_item_by_id("arrows_001", 1)
    elif _loaded_ammo == "droplets":
        $ _player_add_item_by_id("droplets_001", 1)
        $ _player_add_item_by_id("gunpowder_001", 1)
    $ RustyHunterRifleLoadedAmmo = ""
    $ MainTxt = "Вы осторожно разряжаете оружие и убираете заряд."
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return
