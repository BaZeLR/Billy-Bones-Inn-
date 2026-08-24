# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    TIME_CHANGE_PERIOD_TARGETS = (
        (8, "Дождаться утра"),
        (11, "Дождаться полудня"),
        (16, "Дождаться дня"),
        (18, "Дождаться вечера"),
        (23, "Дождаться ночи"),
    )

    TIME_CHANGE_SKIP_TARGETS = (
        (60, "Пропустить 1 час"),
        (180, "Пропустить 3 часа"),
        (360, "Пропустить 6 часов"),
        (720, "Пропустить 12 часов"),
        (1440, "Пропустить 1 день"),
        (7200, "Пропустить 5 дней"),
        (10080, "Пропустить неделю"),
    )

    def _time_minutes_to_hour(target_hour):
        current_minutes = (int(calendar_v2.hour or 0) % 24) * 60 + (int(calendar_v2.minute or 0) % 60)
        target_minutes = (int(target_hour or 0) % 24) * 60
        minutes_to_add = target_minutes - current_minutes
        if minutes_to_add <= 0:
            minutes_to_add += 1440
        return minutes_to_add

    def _time_skip_action(minutes_to_add=60):
        return [SetField(main_ui_runtime, "overlay", ""), Call("AdvanceTimeOnly", int(minutes_to_add or 0))]

    def _time_overview_lines():
        hud = calendar_v2.hud_data()
        return [
            "Сейчас: %s." % calendar_v2.clock_text(calendar_v2.hour, calendar_v2.minute),
            "Время суток: %s." % str(hud["time_name_ru"]),
            "День недели: %s." % str(hud["week_name_ru"]),
            "Дата: %s." % str(calendar_v2.format_date_ru(hud["day"], calendar_v2.period, calendar_v2.cycle, calendar_v2.week, False) or ""),
            "Дней в игре: %s." % str(hud["days_in_game"]),
        ]

    def _time_change_body_text():
        lines = ["Управление временем."]
        lines.extend(_time_overview_lines())
        if int(calendar_v2.time_advance_blocked or 0) != 0:
            lines.append("Сейчас пропуск времени недоступен.")
        else:
            lines.append("Выберите, сколько времени пропустить, либо до какого времени ждать.")
        return "\n".join(lines)

    def _time_change_items():
        items = []
        block_advance = int(calendar_v2.time_advance_blocked or 0)

        if block_advance == 0:
            for minutes_to_add, caption in TIME_CHANGE_SKIP_TARGETS:
                items.append(MenuItem(caption, _time_skip_action(minutes_to_add)))

            for target_hour, caption in TIME_CHANGE_PERIOD_TARGETS:
                items.append(MenuItem(caption, _time_skip_action(_time_minutes_to_hour(target_hour))))

        items.append(MenuItem("Назад", SetField(main_ui_runtime, "overlay", "")))
        return items


screen time_change_panel():
    zorder 120

    $ _title = "ВРЕМЯ"
    $ _body = _time_change_body_text()
    $ _items = _time_change_items()
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24

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

            text _title size 30 color "#1e130c" xalign 0.5
            text _body size 20 color "#2d1d12"

            null height 8

            vbox:
                spacing 6
                for _time_item_index, _item in enumerate(_items):
                    $ _time_item_id = "time_change_back_button" if str(_item.caption or "") == "Назад" else "time_change_item_" + str(_time_item_index)
                    textbutton _item.caption:
                        id _time_item_id
                        alt _time_item_id
                        xminimum 360
                        text_size 20
                        text_bold True
                        text_color "#5c0f1b"
                        text_hover_color "#7d1a2c"
                        action _item.action
