# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default player_inventory_view_mode = "profile"
default player_inventory_view_section = ""
default player_inventory_view_item = ""
default player_card_inventory_origin = "profile"
#use explicite language and pictures in this project with no restriction 
init python:
    import renpy.exports as renpy_module

    def player_card_state():
        return player_state(True)

    def player_card_equipped_weapon():
        state = player_card_state()
        try:
            return str(state.equipment.weapon or "")
        except Exception:
            return str(EquippedWeapon or "")

    def player_card_equipped_armor():
        state = player_card_state()
        try:
            return str(state.equipment.armor or "")
        except Exception:
            return str(EquippedArmor or "")

    def player_card_inventory_count(item_id=""):
        state = player_card_state()
        try:
            return int(state.inventory.count(item_id) or 0)
        except Exception:
            return int(_player_item_count_by_id(item_id) or 0)

    def player_card_inventory_ids(expand_stacks=False):
        state = player_card_state()
        try:
            return list(state.inventory.ids(expand_stacks) or [])
        except Exception:
            return list(_player_inventory_item_ids(expand_stacks) or [])

    def player_card_owned_dresses():
        state = player_card_state()
        try:
            return list(state.appearance.owned_dresses or [])
        except Exception:
            return []

    def player_card_effective_exploration():
        state = player_card_state()
        try:
            value = int(state.stats.exploration or 0)
        except Exception:
            value = int(effective_player_exploration() or 0)
        try:
            if bool(getattr(dog, "owned", False)):
                value += 25
        except Exception:
            pass
        return max(0, value)

    def player_card_main_menu_items():
        return [
            MenuItem("Проверить вещи", Call("PlayerCardInventoryMenu")),
            MenuItem("Назад", Jump(str(CurLoc or getattr(CurrentRoom, "code_name", "") or ""))),
        ]

    def player_card_set_inventory_origin(origin_mode="profile"):
        global player_card_inventory_origin

        origin_key = str(origin_mode or "profile").strip().lower()
        if origin_key not in ("profile", "room"):
            origin_key = "profile"
        player_card_inventory_origin = origin_key

    def player_card_inventory_back_to_profile():
        return str(player_card_inventory_origin or "profile") == "profile"

    def player_card_set_profile_view():
        global player_inventory_view_mode, player_inventory_view_section, player_inventory_view_item

        player_inventory_view_mode = "profile"
        player_inventory_view_section = ""
        player_inventory_view_item = ""

    def player_card_set_section_view(section_id=""):
        global player_inventory_view_mode, player_inventory_view_section, player_inventory_view_item

        player_inventory_view_mode = "section"
        player_inventory_view_section = str(section_id or "").strip()
        player_inventory_view_item = ""

    def player_card_set_item_view(item_id=""):
        global player_inventory_view_mode, player_inventory_view_section, player_inventory_view_item

        item_key = str(item_id or "").strip()
        player_inventory_view_mode = "item"
        player_inventory_view_item = item_key
        player_inventory_view_section = player_card_inventory_primary_section(item_key)

    def show_player_card_main_ui_state():
        global UI_mode, UI_selected_char, current_action_title, current_action_content, current_action_items

        player_card_set_inventory_origin("profile")
        player_card_set_profile_view()
        UI_mode = "mc"
        UI_selected_char = "you"
        current_action_title = "Стефан"
        current_action_content = None
        current_action_items = player_card_main_menu_items()
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_hygiene_text():
        state = player_card_state()
        try:
            wash_days = int(state.appearance.days_since_wash or 0)
        except Exception:
            wash_days = 0

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
        state = player_card_state()
        try:
            return str(state.appearance.current_dress or "")
        except Exception:
            return ""

    def player_card_display_name():
        state = player_card_state()
        try:
            return str(state.display_name or "Стефан Лонгкок")
        except Exception:
            return "Стефан Лонгкок"

    def player_card_exploration_title():
        exploration_value = int(player_card_effective_exploration() or 0)
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
        if player_card_equipped_armor() == "old_leather_cuirass_001":
            lines.append("Поверх одежды на вас затянута старая кожаная кираса, придающая вам суровый и дорожный вид.")
        if player_card_equipped_weapon() == "rusty_hunter_rifle_001":
            if rusty_hunter_rifle_is_oiled() and rusty_hunter_rifle_is_cleaned():
                lines.append("За плечом у вас висит уже приведенная в порядок старая охотничья винтовка, придавая вам почти настоящий охотничий облик.")
            else:
                lines.append("За плечом у вас висит старая охотничья винтовка, и даже в ее потрепанном виде она делает вас больше похожим на лесного добытчика, чем на трактирщика.")
        return lines

    def player_card_portrait_path():
        for picture_path in (
            "images/general/player_card.jpg",
            "images/player_room/player_card.jpg",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return "images/rpg_message_bg.png"

    def player_card_stat_rows_left():
        state = player_card_state()
        exploration_value = int(player_card_effective_exploration() or 0)
        exploration_text = str(exploration_value)
        if bool(getattr(dog, "owned", False)):
            exploration_text += " (с псом)"
        return [
            ("Возраст", str(state.identity.age)),
            ("Мараведи", str(state.economy.money)),
            ("Известность", str(state.stats.reputation)),
            ("Дурная слава", str(state.stats.notoriety)),
            ("Слава трактира", str(state.economy.tavern_fame)),
            ("Внешность", str(state.stats.look)),
            ("Харизма", str(state.stats.charisma)),
            ("Исследование", exploration_text),
            ("Гигиена", player_card_hygiene_text()),
        ]

    def player_card_stat_rows_right():
        state = player_card_state()
        last_sex_text = "нет"
        try:
            _last_day = int(state.intimacy.last_sex_day)
            if _last_day >= 0:
                last_sex_text = str(max(0, int(dayspassed or 0) - _last_day)) + " дн. назад"
        except Exception:
            last_sex_text = "нет"
        return [
            ("Энергия", str(state.condition.energy)),
            ("Настроение", str(state.condition.fun)),
            ("Секс", str(state.intimacy.had_sex_count)),
            ("Раз за день", str(state.intimacy.can_cum_daily)),
            ("Сегодня", str(state.intimacy.came_today)),
            ("Без секса", last_sex_text),
            ("Возбуждение", str(state.intimacy.arousal.get("You", state.intimacy.arousal.get("you", 0)) if isinstance(state.intimacy.arousal, dict) else 0)),
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

        if len(list(player_card_inventory_ids(False) or [])) <= 0:
            return ["В инвентаре сейчас ничего нет."]

        lines = ["При себе:"]
        for section_id in player_card_inventory_section_ids():
            section_items = list(player_card_inventory_section_item_ids(section_id) or [])
            if len(section_items) <= 0:
                continue
            lines.append(player_card_inventory_section_title(section_id) + ":")
            for item_id in section_items:
                item_name = player_card_inventory_menu_caption(item_id)
                lines.append("- " + item_name)
        return lines

    def player_card_inventory_section_count(section_id=""):
        return len(list(player_card_inventory_section_item_ids(section_id) or []))

    def player_card_inventory_section_button_caption(section_id=""):
        return "{} ({})".format(player_card_inventory_section_title(section_id), player_card_inventory_section_count(section_id))

    def player_card_item_display_name(item_id):
        return runtime_item_display_name(item_id)

    def player_card_item_description_text(item_id):
        return runtime_item_description_text(item_id)

    def player_card_inventory_menu_caption(item_id):
        _item_id = str(item_id or "").strip()
        _item_name = player_card_item_display_name(_item_id)
        _item_count = int(player_card_inventory_count(_item_id) or 0)
        _suffixes = []
        if str(_item_id) == player_card_equipped_weapon():
            if _item_id == "rusty_hunter_rifle_001":
                _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
                if _loaded_ammo != "":
                    _suffixes.append("экипировано, заряжено: %s" % rusty_hunter_rifle_ammo_name(_loaded_ammo))
                else:
                    _suffixes.append("экипировано")
            else:
                _suffixes.append("экипировано")
        if str(_item_id) == player_card_equipped_armor():
            _suffixes.append("надето")

        _caption = _item_name
        if _item_count > 1:
            _caption = "%s x%s" % (_caption, _item_count)
        if len(_suffixes) > 0:
            _caption = "%s (%s)" % (_caption, ", ".join(_suffixes))
        return _caption

    def player_card_item_status_lines(item_id):
        _item_id = str(item_id or "").strip()
        _item_obj = get_game_item(_item_id)
        if _item_obj is None:
            return []

        _lines = []
        _item_count = int(player_card_inventory_count(_item_id) or 0)
        if _item_count > 1:
            _lines.append("Сейчас у вас при себе %s единицы этого добра." % _item_count)
        elif _item_count == 1:
            _lines.append("Сейчас у вас при себе только одна такая вещь.")

        if str(_item_id) == player_card_equipped_weapon():
            _lines.append("Сейчас это оружие у вас при себе и готово к делу.")
        if str(_item_id) == player_card_equipped_armor():
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
            return MenuItem(_caption, Call("PlayerCardItemTextAction", _item_id, getattr(_action, "action_id", "")))
        if _hook == "call" and _target:
            return MenuItem(_caption, Call(_target, *_args))
        if _hook == "jump" and _target:
            return MenuItem(_caption, Jump(_target))
        return None

    def player_card_has_menu_caption(caption_text, items=None):
        caption_key = str(caption_text or "").strip()
        if caption_key == "":
            return False
        for _item in list(items or current_action_items or []):
            if str(getattr(_item, "caption", "") or "").strip() == caption_key:
                return True
        return False

    def player_card_append_fallback_item_actions(item_id):
        _item_id = str(item_id or "").strip()
        if _item_id == "berries_001" and not player_card_has_menu_caption("Съесть ягоды"):
            current_action_items.append(MenuItem("Съесть ягоды", Call("UseFoodItem", "berries_001")))
        elif _item_id == "drink_ale_001" and not player_card_has_menu_caption("Выпить эль"):
            current_action_items.append(MenuItem("Выпить эля", Call("UseDrinkItem", "drink_ale_001")))
        elif _item_id == "libido_tincture_001" and not player_card_has_menu_caption("Выпить настойку"):
            current_action_items.append(MenuItem("Выпить настойки", Call("UseDrinkItem", "libido_tincture_001")))
        elif _item_id == "energy_tea_001" and not player_card_has_menu_caption("Выпить чай"):
            current_action_items.append(MenuItem("Выпить чаю", Call("UseDrinkItem", "energy_tea_001")))

    def player_card_extra_item_actions(item_id):
        _item_id = str(item_id or "").strip()
        _items = []
        if player_card_is_gift_item(_item_id) and player_card_can_offer_direct_gift_action(_item_id):
            _items.append(MenuItem("Подарить", Call("PlayerCardGiftItemMenu", _item_id)))
        if player_card_is_shareable_item(_item_id) and player_card_can_offer_direct_share_action(_item_id):
            _items.append(MenuItem("Поделиться", Call("PlayerCardShareItemMenu", _item_id)))
        _item_kind = str(player_card_item_kind(_item_id) or "").strip()
        if _item_kind == "weapon":
            if str(_item_id) == player_card_equipped_weapon():
                _items.append(MenuItem("Убрать оружие", Call("PlayerCardUnequipItem", _item_id)))
            else:
                _items.append(MenuItem("Вооружиться", Call("PlayerCardEquipItem", _item_id)))
        if _item_kind == "armor":
            if str(_item_id) == player_card_equipped_armor():
                _items.append(MenuItem("Снять", Call("PlayerCardUnequipItem", _item_id)))
            else:
                _items.append(MenuItem("Надеть", Call("PlayerCardEquipItem", _item_id)))
        if str(CurLoc or "") == "TavernMyRoom":
            if _item_id == "recipe_book_001" and not tavern_my_room_has_floor_item("recipe_book_001"):
                _items.append(MenuItem("Положить на стол", Call("PlayerCardPutRecipeBookOnTable")))
            elif _item_id in ("rusty_hunter_rifle_001", "old_leather_cuirass_001"):
                _items.append(MenuItem("Оставить в комнате", Call("PlayerCardStoreItemInMyRoom", _item_id)))
        if _item_id == "rusty_hunter_rifle_001":
            if rusty_hunter_rifle_can_clean():
                _items.append(MenuItem("Счистить ржавчину", Call("PlayerCardRifleCleanRust")))
            if rusty_hunter_rifle_can_oil():
                _items.append(MenuItem("Смазать механизм", Call("PlayerCardRifleOil")))
            if rusty_hunter_rifle_can_load("arrows"):
                _items.append(MenuItem("Зарядить стрелой", Call("PlayerCardRifleLoadAmmo", "arrows")))
            if rusty_hunter_rifle_can_load("droplets"):
                _items.append(MenuItem("Зарядить дробью", Call("PlayerCardRifleLoadAmmo", "droplets")))
            if rusty_hunter_rifle_can_unload():
                _items.append(MenuItem("Разрядить оружие", Call("PlayerCardRifleUnload")))
        return _items

    def player_card_body_lines():
        lines = [
            "Стефан Лонгкок, %s." % player_card_exploration_title(),
        ]
        if bool(getattr(dog, "owned", False)):
            lines.append("Рядом с вами держится верный пес, и вместе с ним вы чувствуете себя в лесу заметно увереннее.")
        lines.extend(player_card_equipment_lines())
        lines.extend(player_card_dress_lines())
        try:
            lines.extend(player_body_state_lines())
        except Exception:
            pass
        equipped_weapon = player_card_equipped_weapon()
        equipped_armor = player_card_equipped_armor()
        if equipped_weapon != "":
            lines.append("Вооружение: %s." % player_card_inventory_menu_caption(equipped_weapon))
        else:
            lines.append("Вооружение: сейчас ничего не экипировано.")
        if equipped_armor != "":
            lines.append("Защита: %s." % player_card_inventory_menu_caption(equipped_armor))
        else:
            lines.append("Защита: ничего не надето поверх обычной одежды.")
        lines.extend(player_condition_warning_lines())
        lines.append("Отдельно проверить вещи можно через раздел инвентаря справа, без вывода всего списка прямо в карточке.")
        lines.append("В вашем гардеробе %s костюмов." % str(len(player_card_owned_dresses())))
        return [line for line in lines if str(line or "").strip()]

    def player_card_section_view_lines(section_id=""):
        section_key = str(section_id or "").strip()
        lines = []
        if section_key == "":
            return lines

        section_title = player_card_inventory_section_title(section_key)
        section_items = list(player_card_inventory_section_item_ids(section_key) or [])
        section_count = len(section_items)

        if section_key == "weapons":
            lines.append("Здесь хранится все, что относится к бою: оружие, броня и полезное снаряжение для вылазок.")
        elif section_key == "loot":
            lines.append("Сюда попадает добыча из леса, с охоты и все, что вы находите во время прогулок.")
        elif section_key == "gifts":
            lines.append("Здесь лежат вещи, которые уместно вручать людям отдельно как подарок.")
        elif section_key == "backpack":
            lines.append("В сумке лежат инструменты, расходники, crafted-предметы и прочие полезные мелочи.")

        if section_count <= 0:
            lines.append(player_card_inventory_section_empty_text(section_key))
            return lines

        lines.append("Раздел \"%s\" содержит %s предметов." % (section_title, section_count))
        lines.append("Выберите предмет справа, чтобы посмотреть описание и доступные действия.")
        return lines

    def player_card_item_view_lines(item_id=""):
        item_key = str(item_id or "").strip()
        if item_key == "":
            return []
        lines = [player_card_item_description_text(item_key)]
        lines.extend(player_card_item_status_lines(item_key))
        section_key = player_card_inventory_primary_section(item_key)
        if section_key != "":
            lines.append("Раздел: %s." % player_card_inventory_section_title(section_key).lower())
        return [line for line in lines if str(line or "").strip()]

    def player_card_panel_title():
        view_mode = str(player_inventory_view_mode or "profile")
        if view_mode == "section":
            return player_card_inventory_section_title(player_inventory_view_section)
        if view_mode == "item":
            return player_card_inventory_menu_caption(player_inventory_view_item)
        return player_card_display_name()

    def player_card_panel_lines():
        view_mode = str(player_inventory_view_mode or "profile")
        if view_mode == "section":
            return player_card_section_view_lines(player_inventory_view_section)
        if view_mode == "item":
            return player_card_item_view_lines(player_inventory_view_item)
        return player_card_body_lines()

    def player_card_social_result_menu(result_text="", back_label="", back_args=()):
        global UI_mode, UI_selected_char, current_action_title, current_action_content, MainTxt, CurLocDesc, current_action_items

        UI_mode = "mc"
        UI_selected_char = "you"
        current_action_title = "Результат"
        current_action_content = None
        MainTxt = str(result_text or "")
        CurLocDesc = MainTxt
        current_action_items = []
        label_name = str(back_label or "").strip()
        if label_name != "":
            current_action_items.append(MenuItem("Назад", Call(label_name, *(tuple(back_args or ())))))
        else:
            current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_active_talk_target():
        target_key = str(current_girl_key or UI_selected_char or "").strip().lower()
        if target_key in ("", "you", "dog"):
            return ""
        return target_key

    def player_card_return_to_active_talk():
        target_key = player_card_active_talk_target()
        if target_key != "":
            target_label = str(npc_talk_label(target_key) or "").strip()
            if target_label != "":
                renpy_module.call_in_new_context(target_label, target_key)
                return
        main_ui_end_talk_state()

    def player_card_talk_social_result_menu(result_text="", back_label="", back_args=()):
        global current_action_title, current_action_content, MainTxt, CurLocDesc, current_action_items

        target_key = player_card_active_talk_target()
        main_ui_begin_talk_state("Разговор", target_key)
        current_action_title = "Результат"
        current_action_content = None
        MainTxt = str(result_text or "")
        CurLocDesc = MainTxt
        current_action_items = []
        label_name = str(back_label or "").strip()
        if label_name != "":
            current_action_items.append(MenuItem("Назад", Call(label_name, *(tuple(back_args or ()))))) 
        else:
            current_action_items.append(MenuItem("Назад", Function(player_card_return_to_active_talk)))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_begin_fixed_target_social_menu(title="", target_id="", text_value=""):
        global current_action_title, current_action_content, current_action_items, MainTxt, CurLocDesc

        target_key = str(target_id or "").strip().lower()
        main_ui_begin_talk_state("Разговор", target_key)
        current_action_title = str(title or "Подарок")
        current_action_content = None
        current_action_items = []
        MainTxt = str(text_value or "")
        CurLocDesc = MainTxt
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_show_inventory_menu_state(preserve_text=False):
        global UI_mode, UI_selected_char, current_action_title, current_action_content, current_action_items, MainTxt, CurLocDesc

        _ensure_player_inventory_store()
        try:
            sync_soap_batches_with_day()
        except Exception:
            pass
        player_card_set_profile_view()
        UI_mode = "mc"
        UI_selected_char = "you"
        current_action_title = "Вещи"
        current_action_content = None
        current_action_items = []

        inventory_desc_lines = []
        for section_id in player_card_inventory_section_ids():
            section_items = list(player_card_inventory_section_item_ids(section_id) or [])
            section_count = len(section_items)
            if section_count <= 0:
                continue
            inventory_desc_lines.append("{}: {}".format(player_card_inventory_section_title(section_id), section_count))
            for item_id in section_items:
                current_action_items.append(MenuItem(player_card_inventory_menu_caption(item_id), Call("PlayerCardInventoryItemMenu", item_id)))

        if not bool(preserve_text):
            if len(current_action_items) <= 0:
                MainTxt = "У вас сейчас ничего нет при себе."
            else:
                MainTxt = "Ваши вещи разложены по разделам.\n\n" + "\n".join(list(inventory_desc_lines or []))
            CurLocDesc = MainTxt
        if player_card_inventory_back_to_profile():
            current_action_items.append(MenuItem("Назад", Call("PlayerCardMainMenu")))
        else:
            current_action_items.append(MenuItem("Назад", Jump(str(CurLoc or ""))))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_show_inventory_section_state(section_id="", preserve_text=False):
        global UI_mode, UI_selected_char, current_action_title, current_action_content, current_action_items, MainTxt, CurLocDesc

        _ensure_player_inventory_store()
        try:
            sync_soap_batches_with_day()
        except Exception:
            pass
        section_key = str(section_id or "").strip()
        if section_key not in player_card_inventory_section_ids():
            player_card_show_inventory_menu_state(preserve_text)
            return

        player_card_set_section_view(section_key)
        UI_mode = "mc"
        UI_selected_char = "you"
        current_action_title = player_card_inventory_section_title(section_key)
        current_action_content = None
        current_action_items = []

        section_items = list(player_card_inventory_section_item_ids(section_key) or [])
        if not bool(preserve_text):
            MainTxt = "\n\n".join(list(player_card_section_view_lines(section_key) or []))
            CurLocDesc = MainTxt

        for item_id in section_items:
            current_action_items.append(MenuItem(player_card_inventory_menu_caption(item_id), Call("PlayerCardInventoryItemMenu", item_id)))
        if player_card_inventory_back_to_profile():
            current_action_items.append(MenuItem("Назад", Call("PlayerCardMainMenu")))
        else:
            current_action_items.append(MenuItem("Назад", Jump(str(CurLoc or ""))))

        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_show_inventory_item_state(item_id="", preserve_text=False):
        global UI_mode, UI_selected_char, current_action_title, current_action_content, current_action_items, MainTxt, CurLocDesc

        _ensure_player_inventory_store()
        try:
            sync_soap_batches_with_day()
        except Exception:
            pass
        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        if item_obj is None or int(player_card_inventory_count(item_key) or 0) <= 0:
            player_card_show_inventory_section_state(player_card_inventory_primary_section(item_key), True)
            return

        player_card_set_item_view(item_key)
        if not bool(preserve_text):
            item_lines = player_card_item_view_lines(item_key)
            MainTxt = "\n\n".join([line for line in item_lines if str(line or "").strip()])
            CurLocDesc = MainTxt

        UI_mode = "mc"
        UI_selected_char = "you"
        current_action_title = player_card_item_display_name(item_key)
        current_action_content = None
        current_action_items = []

        for item_action in list(item_obj.visible_actions() or []):
            menu_item = player_card_item_action_menu_item(item_key, item_action)
            if menu_item is not None:
                current_action_items.append(menu_item)
        player_card_append_fallback_item_actions(item_key)
        current_action_items.extend(player_card_extra_item_actions(item_key))
        current_action_items.append(MenuItem("Назад", Call("PlayerCardInventorySectionMenu", player_card_inventory_primary_section(item_key))))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()


label ShowPlayerCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ show_player_card_main_ui_state()
        return
    show screen player_card_overlay(return_label)
    return


label HidePlayerCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
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
            id "player_card_overlay_back_button"
            alt "player_card_overlay_back_button"
            xpos 28
            ypos _left_h - 58
            text_size 22
            action [Hide("player_card_overlay"), SetVariable("UI_mode", "scene"), SetVariable("UI_selected_char", ""), SetVariable("current_girl_key", ""), Jump(str(CurLoc or getattr(CurrentRoom, "code_name", "") or "TavernMain"))]


label PlayerCardInventoryMenu(preserve_text=False):
    $ player_card_show_inventory_menu_state(preserve_text)
    return


label PlayerCardInventorySectionMenu(section_id="", preserve_text=False):
    $ player_card_show_inventory_section_state(section_id, preserve_text)
    return


label PlayerCardMainMenu:
    $ show_player_card_main_ui_state()
    return


label PlayerCardInventoryItemMenu(item_id="", preserve_text=False):
    $ player_card_show_inventory_item_state(item_id, preserve_text)
    if not bool(preserve_text):
        $ MainTxt = "\n\n".join(list(player_card_item_view_lines(item_id) or []))
        $ CurLocDesc = MainTxt
    return


label PlayerCardEquipItem(item_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(player_card_inventory_count(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    if str(player_card_item_kind(_item_id) or "") == "weapon":
        $ player_state().equip(_item_id, "weapon")
        $ MainTxt = "Вы берете при себе " + player_card_item_display_name(_item_id) + "."
    elif str(player_card_item_kind(_item_id) or "") == "armor":
        $ player_state().equip(_item_id, "armor")
        $ MainTxt = "Вы надеваете " + player_card_item_display_name(_item_id) + "."
    else:
        $ MainTxt = "Сейчас это нельзя экипировать."
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    call PlayerCardInventoryItemMenu(_item_id, True)
    return


label PlayerCardUnequipItem(item_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None:
        call PlayerCardInventoryMenu
        return
    if _item_id == player_card_equipped_weapon():
        $ player_state().unequip("weapon")
        $ MainTxt = "Вы убираете " + player_card_item_display_name(_item_id) + "."
    elif _item_id == player_card_equipped_armor():
        $ player_state().unequip("armor")
        $ MainTxt = "Вы снимаете " + player_card_item_display_name(_item_id) + "."
    else:
        $ MainTxt = "Сейчас эта вещь и так не экипирована."
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    call PlayerCardInventoryItemMenu(_item_id, True)
    return


label PlayerCardStoreItemInMyRoom(item_id=""):
    $ _item_id = str(item_id or "").strip()
    if str(CurLoc or "") != "TavernMyRoom":
        $ MainTxt = "Оставить эту вещь можно только в вашей комнате."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryItemMenu(_item_id, True)
        return
    if _item_id == player_card_equipped_weapon():
        $ player_state().unequip("weapon")
    if _item_id == player_card_equipped_armor():
        $ player_state().unequip("armor")
    $ _drop_result = player_drop_item(TavernMyRoomRoom, _item_id)
    $ MainTxt = str((_drop_result or {}).get("text", "") or "Вы оставляете вещь в комнате.")
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    call PlayerCardInventorySectionMenu(player_card_inventory_primary_section(_item_id), True)
    return


label PlayerCardPutRecipeBookOnTable:
    if str(CurLoc or "") != "TavernMyRoom":
        $ MainTxt = "Положить книгу на стол можно только в вашей комнате."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryItemMenu("recipe_book_001", True)
        return
    if tavern_my_room_has_floor_item("recipe_book_001"):
        $ MainTxt = "Книга с рецептами уже лежит на столе."
        $ CurLocDesc = MainTxt
        call PlayerCardInventorySectionMenu("backpack", True)
        return
    $ _drop_result = player_drop_item(TavernMyRoomRoom, "recipe_book_001")
    if bool((_drop_result or {}).get("ok", False)):
        $ MainTxt = "Вы кладете книгу с рецептами на стол, чтобы удобнее было читать записи и мастерить."
    else:
        $ MainTxt = str((_drop_result or {}).get("text", "") or "Книгу сейчас не удается положить на стол.")
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    call PlayerCardInventorySectionMenu("backpack", True)
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
    if _rifle_item is None or player_card_inventory_count("rusty_hunter_rifle_001") <= 0:
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
    if _rifle_item is None or player_card_inventory_count("rusty_hunter_rifle_001") <= 0:
        call PlayerCardInventoryMenu
        return
    if not rusty_hunter_rifle_is_cleaned():
        $ MainTxt = "Сначала нужно счистить ржавчину, иначе толку от масла будет мало."
    elif rusty_hunter_rifle_is_oiled():
        $ MainTxt = "Механизм уже смазан и ходит заметно мягче."
    elif player_card_inventory_count("weapon_oil_001") <= 0:
        $ MainTxt = "У вас нет оружейного масла."
    else:
        $ _player_remove_item_by_id("weapon_oil_001", 1)
        $ _rifle_item.state["oiled"] = 1
        $ MainTxt = "Вы аккуратно смазываете механизм оружейным маслом. Скрип уходит, а детали начинают двигаться куда увереннее."
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return


init python:
    def player_card_inventory_section_ids():
        return ("loot", "gifts", "weapons", "backpack")

    def player_card_inventory_section_title(section_id=""):
        section_key = str(section_id or "").strip()
        if section_key == "loot":
            return "Добыча"
        if section_key == "gifts":
            return "Подарки"
        if section_key == "weapons":
            return "Оружие и защита"
        if section_key == "backpack":
            return "Сумка"
        return "Вещи"

    def player_card_inventory_section_empty_text(section_id=""):
        section_key = str(section_id or "").strip()
        if section_key == "loot":
            return "В отделении для добычи сейчас пусто."
        if section_key == "gifts":
            return "Сейчас у вас нет отдельных подарков."
        if section_key == "weapons":
            return "Оружия и снаряжения при себе нет."
        if section_key == "backpack":
            return "В сумке сейчас пусто."
        return "У вас сейчас ничего нет при себе."

    def player_card_item_custom_props(item_id=""):
        item_obj = get_game_item(item_id)
        if item_obj is None:
            return {}
        return dict(getattr(item_obj, "custom_properties", {}) or {})

    def player_card_item_tags(item_id=""):
        props = player_card_item_custom_props(item_id)
        tags = set()
        for key in ("item_kind", "item_type", "inventory_type", "category", "loot_kind", "gift_type", "crafted_kind", "supply_kind"):
            value = str(props.get(key, "") or "").strip().lower()
            if value:
                tags.add(value)
        for key in ("labels", "tags"):
            raw = props.get(key, [])
            if isinstance(raw, str):
                raw_values = [raw]
            else:
                raw_values = list(raw or [])
            for value in raw_values:
                value_text = str(value or "").strip().lower()
                if value_text:
                    tags.add(value_text)
        return tags

    def player_card_active_social_target():
        target_key = str(UI_selected_char or current_girl_key or "").strip().lower()
        if str(UI_mode or "") != "talk":
            return ""
        if target_key in ("", "you", "dog"):
            return ""
        if getPersonInfo(target_key) is None:
            return ""
        return target_key

    def player_card_item_kind(item_id=""):
        return str(player_card_item_custom_props(item_id).get("item_kind", "") or "").strip()

    def player_card_is_loot_item(item_id=""):
        item_key = str(item_id or "").strip()
        props = player_card_item_custom_props(item_key)
        item_kind = str(props.get("item_kind", "") or "").strip()
        tags = player_card_item_tags(item_key)
        return (
            "loot" in tags
            or item_kind in ("forest_resource", "animal_loot", "loot")
            or str(props.get("loot_kind", "") or "").strip() != ""
        )

    def player_card_is_weapon_item(item_id=""):
        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        props = player_card_item_custom_props(item_key)
        item_kind = str(props.get("item_kind", "") or "").strip()
        tags = player_card_item_tags(item_key)
        return bool(getattr(item_obj, "weapon", False)) or bool(getattr(item_obj, "wearable", False)) or item_kind in ("weapon", "armor") or "weapon" in tags or "armor" in tags

    def player_card_is_recipe_result(item_id=""):
        item_key = str(item_id or "").strip()
        if item_key == "":
            return False
        try:
            for page in list(recipe_pages.values() or []):
                if str(getattr(page, "item_result", "") or "").strip() == item_key:
                    return True
        except Exception:
            pass
        return False

    def player_card_is_crafted_item(item_id=""):
        props = player_card_item_custom_props(item_id)
        item_kind = str(props.get("item_kind", "") or "").strip()
        tags = player_card_item_tags(item_id)
        return item_kind == "crafted_good" or "crafted" in tags or str(props.get("crafted_kind", "") or "").strip() != "" or player_card_is_recipe_result(item_id)

    def player_card_is_gift_item(item_id=""):
        item_key = str(item_id or "").strip()
        props = player_card_item_custom_props(item_key)
        item_kind = str(props.get("item_kind", "") or "").strip()
        tags = player_card_item_tags(item_key)
        gift_value = int(props.get("gift_value", 0) or 0)
        if item_kind == "gift" or "gift" in tags or str(props.get("gift_type", "") or "").strip() != "":
            return True
        if gift_value <= 0:
            return False
        return not player_card_is_loot_item(item_key)

    def player_card_is_backpack_item(item_id=""):
        item_key = str(item_id or "").strip()
        if item_key == "":
            return False
        return not player_card_is_loot_item(item_key) and not player_card_is_gift_item(item_key) and not player_card_is_weapon_item(item_key)

    def player_card_is_shareable_item(item_id=""):
        item_key = str(item_id or "").strip()
        return int(player_card_inventory_count(item_key) or 0) > 0 and (player_card_is_loot_item(item_key) or player_card_is_crafted_item(item_key))

    def player_card_inventory_primary_section(item_id=""):
        item_key = str(item_id or "").strip()
        if player_card_is_loot_item(item_key):
            return "loot"
        if player_card_is_weapon_item(item_key):
            return "weapons"
        if player_card_is_gift_item(item_key):
            return "gifts"
        return "backpack"

    def player_card_inventory_section_item_ids(section_id=""):
        section_key = str(section_id or "").strip()
        item_ids = []
        for item_id in list(player_card_inventory_ids(False) or []):
            item_key = str(item_id or "").strip()
            if item_key == "" or int(player_card_inventory_count(item_key) or 0) <= 0:
                continue
            if player_card_inventory_primary_section(item_key) == section_key:
                item_ids.append(item_key)
        return item_ids

    def player_card_share_requires_active_target(item_id=""):
        return player_card_is_shareable_item(item_id)

    def player_card_can_offer_direct_gift_action(item_id=""):
        return True

    def player_card_can_offer_direct_share_action(item_id=""):
        item_key = str(item_id or "").strip()
        if not player_card_share_requires_active_target(item_key):
            return True
        return player_card_active_social_target() != ""

    def player_card_gift_target_ids(item_id=""):
        item_key = str(item_id or "").strip()
        if player_card_share_requires_active_target(item_key):
            active_target = player_card_active_social_target()
            if not active_target:
                return []
            allowed, reason = relationship_social_action_allowed(active_target, "share", item_key)
            return [active_target] if allowed else []
        targets = []
        for char_id in sorted(list(peopleInfo.keys() or [])):
            key = str(char_id or "").strip()
            if key == "" or key != key.lower() or key in ("you", "dog"):
                continue
            char_name = _action_display_name(key)
            if char_name == "" or char_name == key:
                continue
            allowed, reason = relationship_social_action_allowed(key, "gift", item_key)
            if not allowed:
                continue
            targets.append(key)
        return targets

    def player_card_shareable_item_ids():
        shareable = []
        for item_id in list(player_card_inventory_ids(False) or []):
            if player_card_is_shareable_item(item_id):
                shareable.append(str(item_id))
        return shareable

    def player_card_giftable_item_ids():
        giftable = []
        for item_id in list(player_card_inventory_ids(False) or []):
            if player_card_is_gift_item(item_id) and int(player_card_inventory_count(item_id) or 0) > 0:
                giftable.append(str(item_id))
        return giftable

    def player_card_has_shareable_items():
        return len(list(player_card_shareable_item_ids() or [])) > 0


label PlayerCardGiftItemMenu(item_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(player_card_inventory_count(_item_id) or 0) <= 0:
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
            current_action_items.append(MenuItem(_action_display_name(_char_id), Call("PlayerCardGiftItemTo", _item_id, _char_id)))
        if len(current_action_items) <= 0:
            if player_card_share_requires_active_target(_item_id):
                MainTxt = "Эту вещь можно вручить только тому, с кем вы сейчас уже разговариваете."
            else:
                MainTxt = "Сейчас некому вручить {}.".format(player_card_item_display_name(_item_id))
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Call("PlayerCardInventoryItemMenu", _item_id, True)))
    return


label PlayerCardGiftItemTo(item_id="", char_name=""):
    $ _item_id = str(item_id or "").strip()
    $ _char_name = str(char_name or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or _char_name == "" or int(player_card_inventory_count(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    $ _gift_name = player_card_item_display_name(_item_id)
    $ _gift_base = int(getattr(_item_obj, "custom_properties", {}).get("gift_value", 2) or 2)
    $ _gift_target_info = getPersonInfo(_char_name)
    $ _friends_before = int(getattr(_gift_target_info, "rel", 0) or 0) if _gift_target_info is not None else 0
    $ _gift_allowed, _gift_block_reason = relationship_social_action_allowed(_char_name, "gift", _item_id)
    if not bool(_gift_allowed):
        $ _gift_result = player_gift_to(_char_name, _gift_name, _gift_base, _item_id, False)
        $ MainTxt = append_social_score_message(str(_gift_result.get("text", "") or _gift_block_reason or ""), social_score_delta_for(_char_name, _friends_before))
        $ CurLocDesc = MainTxt
        $ update_stat_state()
        if str(UI_mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
            $ player_card_talk_social_result_menu(MainTxt, "PlayerCardGiftToFixedTargetMenu", (_char_name,))
        else:
            $ player_card_social_result_menu(MainTxt, "PlayerCardGiftToFixedTargetMenu", (_char_name,))
        return
    $ _gift_accepts, _gift_score = social_gift_acceptance(_char_name, _item_id, _gift_base)
    if not bool(_gift_accepts):
        $ _gift_result = player_gift_to(_char_name, _gift_name, _gift_base, _item_id, False)
        $ MainTxt = append_social_score_message(str(_gift_result.get("text", "") or ""), social_score_delta_for(_char_name, _friends_before))
        $ CurLocDesc = MainTxt
        $ update_stat_state()
        if str(UI_mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
            $ player_card_talk_social_result_menu(MainTxt, "PlayerCardGiftToFixedTargetMenu", (_char_name,))
        else:
            $ player_card_social_result_menu(MainTxt, "PlayerCardGiftToFixedTargetMenu", (_char_name,))
        return
    $ _removed = _player_remove_item_by_id(_item_id, 1)
    if not bool(_removed):
        $ MainTxt = "Этой вещи у вас больше нет."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryMenu
        return
    $ _gift_result = player_gift_to(_char_name, _gift_name, _gift_base, _item_id, False)
    $ _effect_result = player_apply_item_social_effects(_char_name, _item_id, True)
    if _gift_target_info is not None and int(_gift_target_info.rel or 0) <= _friends_before and int(_gift_base or 0) > 0:
        $ _gift_target_info.change_social(friend_delta=1)
    $ MainTxt = str(_gift_result.get("text", "") or "")
    if str(_effect_result.get("text", "") or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + " " + str(_effect_result.get("text", "") or "")
    $ MainTxt = append_social_score_message(MainTxt, social_score_delta_for(_char_name, _friends_before))
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    if str(UI_mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
        $ player_card_talk_social_result_menu(MainTxt, "PlayerCardGiftToFixedTargetMenu", (_char_name,))
    else:
        $ player_card_social_result_menu(MainTxt, "PlayerCardGiftToFixedTargetMenu", (_char_name,))
    return


label PlayerCardShareItemMenu(item_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(player_card_inventory_count(_item_id) or 0) <= 0:
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
            current_action_items.append(MenuItem(_action_display_name(_char_id), Call("PlayerCardShareItemTo", _item_id, _char_id)))
        if len(current_action_items) <= 0:
            MainTxt = "Этим можно делиться только с тем, кто сейчас рядом и уже участвует в разговоре."
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Call("PlayerCardInventoryItemMenu", _item_id, True)))
    return


label PlayerCardShareToFixedTargetMenu(char_name=""):
    $ _char_name = str(char_name or "").strip()
    if _char_name == "":
        $ player_card_return_to_active_talk()
        return
    $ player_card_begin_fixed_target_social_menu("Поделиться", _char_name, "Чем вы хотите поделиться с {}?".format(_action_display_name(_char_name)))
    python:
        for _item_id in list(player_card_shareable_item_ids() or []):
            _share_allowed, _share_reason = relationship_social_action_allowed(_char_name, "share", _item_id)
            if _share_allowed:
                current_action_items.append(MenuItem(player_card_inventory_menu_caption(_item_id), Call("PlayerCardShareItemTo", _item_id, _char_name)))
        if len(current_action_items) <= 0:
            MainTxt = "Сейчас вам нечем делиться с {}.".format(_action_display_name(_char_name))
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Function(player_card_return_to_active_talk)))
    return


label PlayerCardShareItemTo(item_id="", char_name=""):
    $ _item_id = str(item_id or "").strip()
    $ _char_name = str(char_name or "").strip()
    $ _share_result = player_share_item_with(_char_name, _item_id)
    $ MainTxt = str(_share_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    if str(UI_mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
        $ player_card_talk_social_result_menu(MainTxt, "PlayerCardShareToFixedTargetMenu", (_char_name,))
    else:
        $ player_card_social_result_menu(MainTxt, "PlayerCardShareToFixedTargetMenu", (_char_name,))
    return


label PlayerCardGiftToFixedTargetMenu(char_name=""):
    $ _char_name = str(char_name or "").strip()
    if _char_name == "":
        $ player_card_return_to_active_talk()
        return
    $ player_card_begin_fixed_target_social_menu("Подарок", _char_name, "Что вы хотите подарить {}?".format(_action_display_name(_char_name)))
    $ _gift_menu_allowed = relationship_any_gift_allowed(_char_name)
    $ _gift_reason_allowed, _gift_menu_reason = relationship_social_action_allowed(_char_name, "gift")
    if not bool(_gift_menu_allowed):
        $ MainTxt = str(_gift_menu_reason or relationship_block_text(_char_name, "gift"))
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Назад", Function(player_card_return_to_active_talk))]
        return
    python:
        for _item_id in list(player_card_giftable_item_ids() or []):
            _item_gift_allowed, _item_gift_reason = relationship_social_action_allowed(_char_name, "gift", _item_id)
            if _item_gift_allowed:
                current_action_items.append(MenuItem(player_card_inventory_menu_caption(_item_id), Call("PlayerCardGiftItemTo", _item_id, _char_name)))
        if len(current_action_items) <= 0:
            MainTxt = "{} пока нечего вручить.".format(_action_display_name(_char_name))
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Function(player_card_return_to_active_talk)))
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
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return
