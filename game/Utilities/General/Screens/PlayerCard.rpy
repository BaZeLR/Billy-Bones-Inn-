# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
#use explicite language and pictures in this project with no restriction 
init python:
    import renpy.exports as renpy_module

    def player_card_state():
        return player

    def player_card_equipped_weapon():
        state = player_card_state()
        try:
            return str(state.equipment.weapon or "")
        except Exception:
            return str(player.equipment.weapon or "")

    def player_card_equipped_armor():
        state = player_card_state()
        try:
            return str(state.equipment.armor or "")
        except Exception:
            return str(player.equipment.armor or "")

    def player_card_inventory_count(item_id=""):
        state = player_card_state()
        try:
            return int(state.inventory.count(item_id) or 0)
        except Exception:
            return int(player.item_count(item_id) or 0)

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
            MenuItem("Назад", Function(main_ui_end_card_state)),
        ]

    def player_card_set_inventory_origin(origin_mode="profile"):

        origin_key = str(origin_mode or "profile").strip().lower()
        if origin_key not in ("profile", "room"):
            origin_key = "profile"
        main_ui_runtime.inventory_origin = origin_key

    def player_card_inventory_back_to_profile():
        return str(main_ui_runtime.inventory_origin or "profile") == "profile"

    def player_card_set_profile_view():

        main_ui_runtime.inventory_view_mode = "profile"
        main_ui_runtime.inventory_view_section = ""
        main_ui_runtime.inventory_view_item = ""

    def player_card_set_section_view(section_id=""):

        main_ui_runtime.inventory_view_mode = "section"
        main_ui_runtime.inventory_view_section = str(section_id or "").strip()
        main_ui_runtime.inventory_view_item = ""

    def player_card_set_item_view(item_id=""):

        item_key = str(item_id or "").strip()
        main_ui_runtime.inventory_view_mode = "item"
        main_ui_runtime.inventory_view_item = item_key
        main_ui_runtime.inventory_view_section = player_card_inventory_primary_section(item_key)

    def show_player_card_main_ui_state():

        main_ui_begin_card_state()
        player_card_set_inventory_origin("profile")
        player_card_set_profile_view()
        main_ui_runtime.mode = "mc"
        main_ui_runtime.selected_char = "you"
        main_ui_runtime.action_title = "Действия"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = player_card_main_menu_items()
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
            ("Известность", str(player_reputation_breakdown().get("reputation", 0))),
            ("Дурная слава", str(state.stats.notoriety)),
            ("Слава трактира", str(state.economy.tavern_fame)),
            ("Внешность", str(player_look_breakdown().get("look", 0))),
            ("Харизма", str(player_charisma_breakdown().get("charisma", 0))),
            ("Исследование", exploration_text),
            ("Гигиена", player_card_hygiene_text()),
        ]

    def player_card_stat_rows_right():
        state = player_card_state()
        last_sex_text = "нет"
        try:
            _last_day = int(state.intimacy.last_sex_day)
            if _last_day >= 0:
                last_sex_text = str(max(0, int(current_game_day() or 0) - _last_day)) + " дн. назад"
        except Exception:
            last_sex_text = "нет"
        return [
            ("Энергия", str(state.condition.energy)),
            ("Настроение", str(state.condition.fun)),
            ("Секс", str(state.intimacy.had_sex_count)),
            ("Раз за день", str(state.intimacy.can_cum_daily)),
            ("Сегодня", str(state.intimacy.came_today)),
            ("Без секса", last_sex_text),
            ("Возбуждение", str(state.intimacy.arousal_value())),
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
        if str(rooms.current_code or "") == "TavernMyRoom":
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
        view_mode = str(main_ui_runtime.inventory_view_mode or "profile")
        if view_mode == "section":
            return player_card_inventory_section_title(main_ui_runtime.inventory_view_section)
        if view_mode == "item":
            return player_card_inventory_menu_caption(main_ui_runtime.inventory_view_item)
        return player_card_display_name()

    def player_card_panel_lines():
        view_mode = str(main_ui_runtime.inventory_view_mode or "profile")
        if view_mode == "section":
            return player_card_section_view_lines(main_ui_runtime.inventory_view_section)
        if view_mode == "item":
            return player_card_item_view_lines(main_ui_runtime.inventory_view_item)
        return player_card_body_lines()

    def player_card_social_result_menu(result_text="", back_action=None):

        main_ui_runtime.mode = "mc"
        main_ui_runtime.selected_char = "you"
        main_ui_runtime.action_title = "Результат"
        main_ui_runtime.action_content = None
        scene_runtime.text = str(result_text or "")
        scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items = []
        main_ui_runtime.action_items.append(MenuItem("Назад", back_action if back_action is not None else Function(main_ui_end_card_state)))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_active_talk_target():
        target_key = str(main_ui_runtime.girl_key or main_ui_runtime.selected_char or "").strip().lower()
        if target_key in ("", "you", "dog"):
            return ""
        return target_key

    def player_card_talk_social_result_menu(result_text=""):

        target_key = player_card_active_talk_target()
        main_ui_begin_talk_state("Разговор", target_key)
        main_ui_runtime.action_title = "Результат"
        main_ui_runtime.action_content = None
        scene_runtime.text = str(result_text or "")
        scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items = []
        main_ui_runtime.action_items.append(MenuItem("Назад", [Function(main_ui_end_card_state), Return()]))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_begin_fixed_target_social_menu(title="", target_id="", text_value=""):

        target_key = str(target_id or "").strip().lower()
        main_ui_begin_talk_state("Разговор", target_key)
        main_ui_runtime.action_title = str(title or "Подарок")
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []
        scene_runtime.text = str(text_value or "")
        scene_runtime.location_text = scene_runtime.text
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_show_inventory_menu_state(preserve_text=False):

        player_card_set_profile_view()
        main_ui_runtime.mode = "mc"
        main_ui_runtime.selected_char = "you"
        main_ui_runtime.action_title = "Вещи"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []

        inventory_desc_lines = []
        for section_id in player_card_inventory_section_ids():
            section_items = list(player_card_inventory_section_item_ids(section_id) or [])
            section_count = len(section_items)
            if section_count <= 0:
                continue
            inventory_desc_lines.append("{}: {}".format(player_card_inventory_section_title(section_id), section_count))
            for item_id in section_items:
                main_ui_runtime.action_items.append(MenuItem(player_card_inventory_menu_caption(item_id), Call("PlayerCardInventoryItemMenu", item_id)))

        if not bool(preserve_text):
            if len(main_ui_runtime.action_items) <= 0:
                scene_runtime.text = "У вас сейчас ничего нет при себе."
            else:
                scene_runtime.text = "Ваши вещи разложены по разделам.\n\n" + "\n".join(list(inventory_desc_lines or []))
            scene_runtime.location_text = scene_runtime.text
        if player_card_inventory_back_to_profile():
            main_ui_runtime.action_items.append(MenuItem("Назад", Call("PlayerCardMainMenu")))
        else:
            main_ui_runtime.action_items.append(MenuItem("Назад", Function(main_ui_end_card_state)))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_show_inventory_section_state(section_id="", preserve_text=False):

        section_key = str(section_id or "").strip()
        if section_key not in player_card_inventory_section_ids():
            player_card_show_inventory_menu_state(preserve_text)
            return

        player_card_set_section_view(section_key)
        main_ui_runtime.mode = "mc"
        main_ui_runtime.selected_char = "you"
        main_ui_runtime.action_title = player_card_inventory_section_title(section_key)
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []

        section_items = list(player_card_inventory_section_item_ids(section_key) or [])
        if not bool(preserve_text):
            scene_runtime.text = "\n\n".join(list(player_card_section_view_lines(section_key) or []))
            scene_runtime.location_text = scene_runtime.text

        for item_id in section_items:
            main_ui_runtime.action_items.append(MenuItem(player_card_inventory_menu_caption(item_id), Call("PlayerCardInventoryItemMenu", item_id)))
        if player_card_inventory_back_to_profile():
            main_ui_runtime.action_items.append(MenuItem("Назад", Call("PlayerCardMainMenu")))
        else:
            main_ui_runtime.action_items.append(MenuItem("Назад", Function(main_ui_end_card_state)))

        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def player_card_show_inventory_item_state(item_id="", preserve_text=False):

        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        if item_obj is None or int(player_card_inventory_count(item_key) or 0) <= 0:
            player_card_show_inventory_section_state(player_card_inventory_primary_section(item_key), True)
            return

        player_card_set_item_view(item_key)
        if not bool(preserve_text):
            item_lines = player_card_item_view_lines(item_key)
            scene_runtime.text = "\n\n".join([line for line in item_lines if str(line or "").strip()])
            scene_runtime.location_text = scene_runtime.text

        main_ui_runtime.mode = "mc"
        main_ui_runtime.selected_char = "you"
        main_ui_runtime.action_title = player_card_item_display_name(item_key)
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []

        for item_action in list(item_obj.visible_actions() or []):
            menu_item = player_card_item_action_menu_item(item_key, item_action)
            if menu_item is not None:
                main_ui_runtime.action_items.append(menu_item)
        main_ui_runtime.action_items.extend(player_card_extra_item_actions(item_key))
        main_ui_runtime.action_items.append(MenuItem("Назад", Call("PlayerCardInventorySectionMenu", player_card_inventory_primary_section(item_key))))
        restart_fn = getattr(renpy_module, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()


label ShowPlayerCard(return_label=""):
    $ show_player_card_main_ui_state()
    return


label HidePlayerCard(return_label=""):
    $ main_ui_end_card_state()
    return

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
        $ scene_runtime.text = "\n\n".join(list(player_card_item_view_lines(item_id) or []))
        $ scene_runtime.location_text = scene_runtime.text
    return


label PlayerCardEquipItem(item_id=""):
    $ renpy.dynamic("_item_id", "_item_obj")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(player_card_inventory_count(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    if str(player_card_item_kind(_item_id) or "") == "weapon":
        $ player.equip(_item_id, "weapon")
        $ scene_runtime.text = "Вы берете при себе " + player_card_item_display_name(_item_id) + "."
    elif str(player_card_item_kind(_item_id) or "") == "armor":
        $ player.equip(_item_id, "armor")
        $ scene_runtime.text = "Вы надеваете " + player_card_item_display_name(_item_id) + "."
    else:
        $ scene_runtime.text = "Сейчас это нельзя экипировать."
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    call PlayerCardInventoryItemMenu(_item_id, True)
    return


label PlayerCardUnequipItem(item_id=""):
    $ renpy.dynamic("_item_id", "_item_obj")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None:
        call PlayerCardInventoryMenu
        return
    if _item_id == player_card_equipped_weapon():
        $ player.unequip("weapon")
        $ scene_runtime.text = "Вы убираете " + player_card_item_display_name(_item_id) + "."
    elif _item_id == player_card_equipped_armor():
        $ player.unequip("armor")
        $ scene_runtime.text = "Вы снимаете " + player_card_item_display_name(_item_id) + "."
    else:
        $ scene_runtime.text = "Сейчас эта вещь и так не экипирована."
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    call PlayerCardInventoryItemMenu(_item_id, True)
    return


label PlayerCardStoreItemInMyRoom(item_id=""):
    $ renpy.dynamic("_item_id", "_drop_result")
    $ _item_id = str(item_id or "").strip()
    if str(rooms.current_code or "") != "TavernMyRoom":
        $ scene_runtime.text = "Оставить эту вещь можно только в вашей комнате."
        $ scene_runtime.location_text = scene_runtime.text
        call PlayerCardInventoryItemMenu(_item_id, True)
        return
    if _item_id == player_card_equipped_weapon():
        $ player.unequip("weapon")
    if _item_id == player_card_equipped_armor():
        $ player.unequip("armor")
    $ _drop_result = player_drop_item(rooms.get("TavernMyRoom"), _item_id)
    $ scene_runtime.text = str((_drop_result or {}).get("text", "") or "Вы оставляете вещь в комнате.")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    call PlayerCardInventorySectionMenu(player_card_inventory_primary_section(_item_id), True)
    return


label PlayerCardPutRecipeBookOnTable:
    $ renpy.dynamic("_drop_result")
    if str(rooms.current_code or "") != "TavernMyRoom":
        $ scene_runtime.text = "Положить книгу на стол можно только в вашей комнате."
        $ scene_runtime.location_text = scene_runtime.text
        call PlayerCardInventoryItemMenu("recipe_book_001", True)
        return
    if tavern_my_room_has_floor_item("recipe_book_001"):
        $ scene_runtime.text = "Книга с рецептами уже лежит на столе."
        $ scene_runtime.location_text = scene_runtime.text
        call PlayerCardInventorySectionMenu("backpack", True)
        return
    $ _drop_result = player_drop_item(rooms.get("TavernMyRoom"), "recipe_book_001")
    if bool((_drop_result or {}).get("ok", False)):
        $ scene_runtime.text = "Вы кладете книгу с рецептами на стол, чтобы удобнее было читать записи и мастерить."
    else:
        $ scene_runtime.text = str((_drop_result or {}).get("text", "") or "Книгу сейчас не удается положить на стол.")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    call PlayerCardInventorySectionMenu("backpack", True)
    return


label PlayerCardItemTextAction(item_id="", action_id=""):
    $ renpy.dynamic("_item_id", "_item_action")
    $ _item_id = str(item_id or "").strip()
    $ _item_action = player_card_get_item_action(_item_id, action_id)
    if _item_action is not None:
        $ scene_runtime.text = str(getattr(_item_action, "target", "") or "")
        $ scene_runtime.location_text = scene_runtime.text
    call PlayerCardInventoryItemMenu(_item_id, True)
    return


label PlayerCardRifleCleanRust:
    $ renpy.dynamic("_rifle_item")
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or player_card_inventory_count("rusty_hunter_rifle_001") <= 0:
        call PlayerCardInventoryMenu
        return
    if rusty_hunter_rifle_is_cleaned():
        $ scene_runtime.text = "Вы уже счистили основную ржавчину с механизма."
    else:
        $ _rifle_item.state["rust_cleaned"] = 1
        $ scene_runtime.text = "Вы долго скоблите металл, снимаете рыжий налет и понемногу приводите механизм в порядок. Оружие уже не выглядит совсем уж мертвым."
    $ scene_runtime.location_text = scene_runtime.text
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return


label PlayerCardRifleOil:
    $ renpy.dynamic("_rifle_item")
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or player_card_inventory_count("rusty_hunter_rifle_001") <= 0:
        call PlayerCardInventoryMenu
        return
    if not rusty_hunter_rifle_is_cleaned():
        $ scene_runtime.text = "Сначала нужно счистить ржавчину, иначе толку от масла будет мало."
    elif rusty_hunter_rifle_is_oiled():
        $ scene_runtime.text = "Механизм уже смазан и ходит заметно мягче."
    elif player_card_inventory_count("weapon_oil_001") <= 0:
        $ scene_runtime.text = "У вас нет оружейного масла."
    else:
        $ player.remove_item("weapon_oil_001", 1)
        $ _rifle_item.state["oiled"] = 1
        $ scene_runtime.text = "Вы аккуратно смазываете механизм оружейным маслом. Скрип уходит, а детали начинают двигаться куда увереннее."
    $ scene_runtime.location_text = scene_runtime.text
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
        target_key = str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower()
        if str(main_ui_runtime.mode or "") != "talk":
            return ""
        if target_key in ("", "you", "dog"):
            return ""
        if people.get_info(target_key) is None:
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
        for char_id in people.ids():
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
    $ renpy.dynamic("_item_id", "_item_obj", "_char_id")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(player_card_inventory_count(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    $ scene_runtime.text = "Кому вы хотите вручить {}?".format(player_card_item_display_name(_item_id))
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.mode = "mc"
    $ main_ui_runtime.selected_char = "you"
    $ main_ui_runtime.action_title = "Подарок"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _char_id in player_card_gift_target_ids(_item_id):
            main_ui_runtime.action_items.append(MenuItem(_action_display_name(_char_id), Call("PlayerCardGiftItemTo", _item_id, _char_id)))
        if len(main_ui_runtime.action_items) <= 0:
            if player_card_share_requires_active_target(_item_id):
                scene_runtime.text = "Эту вещь можно вручить только тому, с кем вы сейчас уже разговариваете."
            else:
                scene_runtime.text = "Сейчас некому вручить {}.".format(player_card_item_display_name(_item_id))
            scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items.append(MenuItem("Назад", Call("PlayerCardInventoryItemMenu", _item_id, True)))
    return


label PlayerCardGiftItemTo(item_id="", char_name=""):
    $ renpy.dynamic("_gift_result", "_item_id", "_char_name", "_item_obj", "_gift_name", "_gift_base", "_gift_target_info", "_friends_before", "_removed", "_effect_result")
    $ _item_id = str(item_id or "").strip()
    $ _char_name = str(char_name or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or _char_name == "" or int(player_card_inventory_count(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    $ _gift_name = player_card_item_display_name(_item_id)
    $ _gift_base = int(getattr(_item_obj, "custom_properties", {}).get("gift_value", 2) or 2)
    $ _gift_target_info = people.get_info(_char_name)
    $ _friends_before = int(getattr(_gift_target_info, "rel", 0) or 0) if _gift_target_info is not None else 0
    $ _gift_allowed, _gift_block_reason = relationship_social_action_allowed(_char_name, "gift", _item_id)
    if not bool(_gift_allowed):
        $ _gift_result = player_gift_to(_char_name, _gift_name, _gift_base, _item_id, False)
        $ scene_runtime.text = append_social_score_message(str(_gift_result.get("text", "") or _gift_block_reason or ""), social_score_delta_for(_char_name, _friends_before))
        $ scene_runtime.location_text = scene_runtime.text
        $ update_stat_state()
        if str(main_ui_runtime.mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
            $ player_card_talk_social_result_menu(scene_runtime.text)
        else:
            $ player_card_social_result_menu(scene_runtime.text, Call("PlayerCardGiftToFixedTargetMenu", _char_name))
        return
    $ _gift_accepts, _gift_score = social_gift_acceptance(_char_name, _item_id, _gift_base)
    if not bool(_gift_accepts):
        $ _gift_result = player_gift_to(_char_name, _gift_name, _gift_base, _item_id, False)
        $ scene_runtime.text = append_social_score_message(str(_gift_result.get("text", "") or ""), social_score_delta_for(_char_name, _friends_before))
        $ scene_runtime.location_text = scene_runtime.text
        $ update_stat_state()
        if str(main_ui_runtime.mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
            $ player_card_talk_social_result_menu(scene_runtime.text)
        else:
            $ player_card_social_result_menu(scene_runtime.text, Call("PlayerCardGiftToFixedTargetMenu", _char_name))
        return
    $ _removed = player.remove_item(_item_id, 1)
    if not bool(_removed):
        $ scene_runtime.text = "Этой вещи у вас больше нет."
        $ scene_runtime.location_text = scene_runtime.text
        call PlayerCardInventoryMenu
        return
    $ _gift_result = player_gift_to(_char_name, _gift_name, _gift_base, _item_id, False)
    $ _effect_result = player_apply_item_social_effects(_char_name, _item_id, True)
    if _gift_target_info is not None and int(_gift_target_info.rel or 0) <= _friends_before and int(_gift_base or 0) > 0:
        $ _gift_target_info.change_social(friend_delta=1)
    $ scene_runtime.text = str(_gift_result.get("text", "") or "")
    if str(_effect_result.get("text", "") or "").strip() != "":
        $ scene_runtime.text = str(scene_runtime.text or "") + " " + str(_effect_result.get("text", "") or "")
    $ scene_runtime.text = append_social_score_message(scene_runtime.text, social_score_delta_for(_char_name, _friends_before))
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    if str(main_ui_runtime.mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
        $ player_card_talk_social_result_menu(scene_runtime.text)
    else:
        $ player_card_social_result_menu(scene_runtime.text, Call("PlayerCardGiftToFixedTargetMenu", _char_name))
    return


label PlayerCardShareItemMenu(item_id=""):
    $ renpy.dynamic("_item_id", "_item_obj", "_char_id")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or int(player_card_inventory_count(_item_id) or 0) <= 0:
        call PlayerCardInventoryMenu
        return
    $ scene_runtime.text = "С кем вы хотите разделить {}?".format(player_card_item_display_name(_item_id))
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.mode = "mc"
    $ main_ui_runtime.selected_char = "you"
    $ main_ui_runtime.action_title = "Поделиться"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _char_id in player_card_gift_target_ids(_item_id):
            main_ui_runtime.action_items.append(MenuItem(_action_display_name(_char_id), Call("PlayerCardShareItemTo", _item_id, _char_id)))
        if len(main_ui_runtime.action_items) <= 0:
            scene_runtime.text = "Этим можно делиться только с тем, кто сейчас рядом и уже участвует в разговоре."
            scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items.append(MenuItem("Назад", Call("PlayerCardInventoryItemMenu", _item_id, True)))
    return


label PlayerCardShareToFixedTargetMenu(char_name=""):
    $ renpy.dynamic("_char_name", "_fixed_from_native_talk", "_fixed_back_action", "_item_id", "_share_allowed", "_share_reason")
    $ _char_name = str(char_name or "").strip()
    if _char_name == "":
        return
    $ _fixed_from_native_talk = str(main_ui_runtime.mode or "") == "talk"
    $ main_ui_begin_card_state()
    $ player_card_begin_fixed_target_social_menu("Поделиться", _char_name, "Чем вы хотите поделиться с {}?".format(_action_display_name(_char_name)))
    $ _fixed_back_action = [Function(main_ui_end_card_state), Return()] if _fixed_from_native_talk else Function(main_ui_end_card_state)
    python:
        for _item_id in list(player_card_shareable_item_ids() or []):
            _share_allowed, _share_reason = relationship_social_action_allowed(_char_name, "share", _item_id)
            if _share_allowed:
                main_ui_runtime.action_items.append(MenuItem(player_card_inventory_menu_caption(_item_id), Call("PlayerCardShareItemTo", _item_id, _char_name)))
        if len(main_ui_runtime.action_items) <= 0:
            scene_runtime.text = "Сейчас вам нечем делиться с {}.".format(_action_display_name(_char_name))
            scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items.append(MenuItem("Назад", _fixed_back_action))
    if _fixed_from_native_talk:
        call screen main_ui as player_card_fixed_target_interaction
        $ main_ui_end_card_state()
    return


label PlayerCardShareItemTo(item_id="", char_name=""):
    $ renpy.dynamic("_item_id", "_char_name", "_share_result")
    $ _item_id = str(item_id or "").strip()
    $ _char_name = str(char_name or "").strip()
    $ _share_result = player_share_item_with(_char_name, _item_id)
    $ scene_runtime.text = str(_share_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    if str(main_ui_runtime.mode or "") == "talk" and str(player_card_active_talk_target() or "") == str(_char_name or "").strip().lower():
        $ player_card_talk_social_result_menu(scene_runtime.text)
    else:
        $ player_card_social_result_menu(scene_runtime.text, Call("PlayerCardShareToFixedTargetMenu", _char_name))
    return


label PlayerCardGiftToFixedTargetMenu(char_name=""):
    $ renpy.dynamic("_char_name", "_fixed_from_native_talk", "_fixed_back_action", "_gift_menu_allowed", "_item_id", "_item_gift_allowed", "_item_gift_reason")
    $ _char_name = str(char_name or "").strip()
    if _char_name == "":
        return
    $ _fixed_from_native_talk = str(main_ui_runtime.mode or "") == "talk"
    $ main_ui_begin_card_state()
    $ player_card_begin_fixed_target_social_menu("Подарок", _char_name, "Что вы хотите подарить {}?".format(_action_display_name(_char_name)))
    $ _fixed_back_action = [Function(main_ui_end_card_state), Return()] if _fixed_from_native_talk else Function(main_ui_end_card_state)
    $ _gift_menu_allowed = relationship_any_gift_allowed(_char_name)
    $ _gift_reason_allowed, _gift_menu_reason = relationship_social_action_allowed(_char_name, "gift")
    if not bool(_gift_menu_allowed):
        $ scene_runtime.text = str(_gift_menu_reason or relationship_block_text(_char_name, "gift"))
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = [MenuItem("Назад", _fixed_back_action)]
        if _fixed_from_native_talk:
            call screen main_ui as player_card_fixed_target_interaction
            $ main_ui_end_card_state()
        return
    python:
        for _item_id in list(player_card_giftable_item_ids() or []):
            _item_gift_allowed, _item_gift_reason = relationship_social_action_allowed(_char_name, "gift", _item_id)
            if _item_gift_allowed:
                main_ui_runtime.action_items.append(MenuItem(player_card_inventory_menu_caption(_item_id), Call("PlayerCardGiftItemTo", _item_id, _char_name)))
        if len(main_ui_runtime.action_items) <= 0:
            scene_runtime.text = "{} пока нечего вручить.".format(_action_display_name(_char_name))
            scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items.append(MenuItem("Назад", _fixed_back_action))
    if _fixed_from_native_talk:
        call screen main_ui as player_card_fixed_target_interaction
        $ main_ui_end_card_state()
    return


label PlayerCardRifleLoadAmmo(ammo_code="arrows"):
    $ renpy.dynamic("_ammo_code")
    $ _ammo_code = str(ammo_code or "").strip()
    if not rusty_hunter_rifle_can_load(_ammo_code):
        $ scene_runtime.text = "Сейчас оружие нельзя так зарядить."
        $ scene_runtime.location_text = scene_runtime.text
        call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
        return
    if _ammo_code == "arrows":
        $ player.remove_item("arrows_001", 1)
    elif _ammo_code == "droplets":
        $ player.remove_item("droplets_001", 1)
        $ player.remove_item("gunpowder_001", 1)
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = _ammo_code
    $ scene_runtime.text = "Вы заряжаете оружие {} и осторожно ставите механизм наготове.".format(rusty_hunter_rifle_ammo_name(_ammo_code))
    $ scene_runtime.location_text = scene_runtime.text
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return


label PlayerCardRifleUnload:
    $ renpy.dynamic("_loaded_ammo")
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ scene_runtime.text = "Оружие и так уже разряжено."
        $ scene_runtime.location_text = scene_runtime.text
        call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
        return
    if _loaded_ammo == "arrows":
        $ player.add_item("arrows_001", 1)
    elif _loaded_ammo == "droplets":
        $ player.add_item("droplets_001", 1)
        $ player.add_item("gunpowder_001", 1)
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ scene_runtime.text = "Вы осторожно разряжаете оружие и убираете заряд."
    $ scene_runtime.location_text = scene_runtime.text
    call PlayerCardInventoryItemMenu("rusty_hunter_rifle_001", True)
    return
