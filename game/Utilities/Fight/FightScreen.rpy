screen fight_enemy_info_window(rows):
    frame:
        xalign 1.0
        yalign 0.0
        xmaximum 390
        ymaximum 310
        padding (12, 10)
        background "#080808e8"

        vbox:
            xfill True
            spacing 7
            text "Противники" size 18 color "#f0d08a" xalign 0.5

            viewport:
                xfill True
                ymaximum 250
                draggable True
                mousewheel True

                vbox:
                    xfill True
                    spacing 8
                    for _row in list(rows or []):
                        $ _name = str(_row.get("name", "") or "Противник")
                        $ _health = int(_row.get("health", 0) or 0)
                        $ _health_max = max(1, int(_row.get("health_max", 0) or 0))
                        $ _energy = int(_row.get("energy", 0) or 0)
                        $ _energy_max = max(1, int(_row.get("energy_max", 0) or 0))
                        $ _weapon = str(_row.get("weapon", "") or "тело")
                        $ _attack = str(_row.get("attack_text", "") or "")
                        $ _defence = str(_row.get("defence_text", "") or "")
                        $ _tactics = str(_row.get("tactics", "") or "")
                        $ _skills = ", ".join([str(item) for item in list(_row.get("skills", []) or [])])
                        $ _status = ", ".join([str(item) for item in list(_row.get("status", []) or []) if str(item or "").strip()])
                        frame:
                            xfill True
                            padding (8, 6)
                            background "#151515ee"

                            vbox:
                                spacing 2
                                text _name size 17 color "#f0e6d2"
                                text "Здоровье: [_health]/[_health_max]   Силы: [_energy]/[_energy_max]" size 14
                                text "Оружие: [_weapon]" size 14 color "#d8c27a"
                                text "Атака: [_attack]   Защита: [_defence]" size 14
                                text "Скорость: [_row.get('speed', 0)]" size 13
                                if _tactics:
                                    text "Тактика: [_tactics]" size 13 color "#a39a8b"
                                if _skills:
                                    text "Навыки: [_skills]" size 13 color "#a39a8b"
                                if _status:
                                    text "Состояние: [_status]" size 13 color "#d8c27a"


screen fight_player_info_window(rows, ammo_text=""):
    frame:
        xalign 0.0
        yalign 0.0
        xmaximum 315
        padding (12, 10)
        background "#080808e8"

        vbox:
            xfill True
            spacing 6
            text "Вы" size 18 color "#f0d08a" xalign 0.5
            $ _row = list(rows or [{}])[0]
            $ _health = int(_row.get("health", 0) or 0)
            $ _health_max = max(1, int(_row.get("health_max", 0) or 0))
            $ _energy = int(_row.get("energy", 0) or 0)
            $ _energy_max = max(1, int(_row.get("energy_max", 0) or 0))
            $ _subtitle = str(_row.get("subtitle", "") or "")
            $ _status = ", ".join([str(item) for item in list(_row.get("status", []) or []) if str(item or "").strip()])
            $ _fight_level = int(_row.get("fight_level", fight_player_level()) or 1)
            $ _reputation = int(_row.get("reputation", player_reputation_breakdown().get("reputation", 0)) or 0)
            $ _notoriety = int(_row.get("notoriety", player.stats.notoriety) or 0)
            $ _exploration = int(_row.get("exploration", player.stats.exploration) or 0)
            $ _tavernfame = int(_row.get("tavernfame", player.economy.tavern_fame) or 0)
            $ _money = int(_row.get("money", player.economy.money) or 0)
            $ _sick_days = int(_row.get("sick_days", player.condition.sick_days) or 0)
            $ _fun = int(_row.get("fun", player.condition.fun) or 0)
            text "Здоровье: [_health]/[_health_max]   Силы: [_energy]/[_energy_max]" size 14
            text "Оружие: [fight_player_weapon_name()]" size 14 color "#d8c27a"
            text "Броня: [fight_player_armor_name()]" size 14 color "#d8c27a"
            text "Атака: [fight_player_attack_preview_text()]   Защита: [fight_player_defence_preview_text()]" size 14
            text "Скорость: [_row.get('speed', 0)]" size 13
            text "Бой: [_fight_level]   Веселье: [_fun]   Болезнь: [_sick_days]" size 13
            text "Репутация: [_reputation]   Дурная слава: [_notoriety]" size 13
            text "Исследование: [_exploration]   Слава трактира: [_tavernfame]" size 13
            text "Деньги: [_money]" size 13
            if ammo_text:
                text ammo_text size 13 color "#d8c27a"
            if _subtitle:
                text _subtitle size 13 color "#a39a8b"
            if _status:
                text "Состояние: [_status]" size 13 color "#d8c27a"


screen main_ui_fight_panel():
    $ _company_rows = list(fight_company_display_rows() or [])
    $ _player_row = _company_rows[0] if len(_company_rows) > 0 else {"name": "Вы", "health": player.condition.health, "health_max": 100, "energy": player.condition.energy, "energy_max": 100}
    $ _enemy_rows = list(fight_enemy_display_rows() or [])
    $ _target_rows = [row for row in _enemy_rows if "цель" in list(row.get("status", []) or [])]
    $ _enemy_row = _target_rows[0] if len(_target_rows) > 0 else (_enemy_rows[0] if len(_enemy_rows) > 0 else {"name": "Противник", "health": 0, "health_max": 1, "energy": 0, "energy_max": 1})
    $ _loaded = str(fight.loaded_ammo or "").strip()
    $ _loaded_text = "Заряжено: " + fight_loaded_ammo_name(_loaded) if int(fight.weapon_loaded or 0) == 1 and _loaded else "Оружие не заряжено"
    $ _ammo_text = _loaded_text + "\nСтрелы: " + str(fight_supply_count("arrows")) + " / дробь: " + str(fight_supply_count("droplets"))
    $ _fight_picture = str(fight_selected_enemy_image() or scene_runtime.picture or "")
    $ _fight_text = str(scene_runtime.text or fight_preview_text() or "")
    $ _top_h = int((config.screen_height - int(getattr(gui, "textbox_height", 278)) - 24) * 0.55)
    $ _text_h = int((config.screen_height - int(getattr(gui, "textbox_height", 278)) - 24) * 0.30)

    fixed:
        xfill True
        yfill True

        vbox:
            xfill True
            yfill True
            spacing 8

            fixed:
                xfill True
                ysize _top_h

                use BGIMAGE(_fight_picture)
                use fight_player_info_window(_company_rows if _company_rows else [_player_row], _ammo_text)
                use fight_enemy_info_window(_enemy_rows if _enemy_rows else [_enemy_row])

            if _fight_text:
                frame:
                    xfill True
                    ysize _text_h
                    padding (12, 10)
                    background "#000000ff"

                    viewport:
                        xfill True
                        yfill True
                        draggable True
                        mousewheel True
                        text _fight_text size 18
            else:
                null height _text_h
