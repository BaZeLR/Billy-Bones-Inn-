# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _time_change_close_action(return_label=""):
        if str(return_label or "") == "__main_ui_overlay__":
            return SetVariable("main_ui_overlay", "")
        return Hide("time_change_card_overlay")

    def _time_return_label():
        if CurrentRoom is not None:
            room_code = str(getattr(CurrentRoom, "code_name", "") or "")
            if room_code:
                return room_code
        return str(CurLoc or "TavernMain")

    TIME_CHANGE_PERIOD_TARGETS = (
        (8, "Дождаться утра"),
        (11, "Дождаться полудня"),
        (16, "Дождаться дня"),
        (18, "Дождаться вечера"),
        (23, "Дождаться ночи"),
    )

    def _time_current_hour():
        calendar_v2.sync_state()
        return int(calendar_v2.hour or 0) % 24

    def _time_overview_lines():
        calendar_v2.sync_state()
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
        if int(BlockTimeAdvance or 0) != 0:
            lines.append("Сейчас пропуск времени недоступен.")
        else:
            lines.append("Выберите, до какого времени ждать, либо пропустите несколько дней.")
        return "\n".join(lines)

    def _time_change_items(return_label=""):
        items = []
        block_advance = int(BlockTimeAdvance or 0)
        current_hour = _time_current_hour()

        if block_advance == 0:
            for target_hour, caption in TIME_CHANGE_PERIOD_TARGETS:
                if current_hour < int(target_hour or 0):
                    items.append(MenuItem(caption, [_time_change_close_action(return_label), Call("ApplyTimePeriodChange", target_hour)]))

        if block_advance == 0:
            items.append(MenuItem("Дождаться следующего утра", [_time_change_close_action(return_label), Call("NextDay", _time_return_label(), 1)]))
            items.append(MenuItem("Пропустить 5 дней", [_time_change_close_action(return_label), Call("NextDay", _time_return_label(), 5)]))
            items.append(MenuItem("Пропустить неделю", [_time_change_close_action(return_label), Call("NextDay", _time_return_label(), 7)]))

        if str(return_label or "") == "__main_ui_overlay__":
            items.append(MenuItem("Назад", SetVariable("main_ui_overlay", "")))
        elif str(return_label or "") == "__hide__":
            items.append(MenuItem("Назад", Hide("time_change_card_overlay")))
        else:
            items.append(MenuItem("Назад", Call("HideTimeChangeMenu", return_label)))
        return items


label ShowTimeChangeMenu(return_label=""):
    $ current_action_title = "Изменить время"
    $ current_action_content = None
    $ current_action_items = []
    show screen time_change_card_overlay(return_label)
    return


label HideTimeChangeMenu(return_label=""):
    hide screen time_change_card_overlay
    if CurrentRoom is not None:
        $ current_action_title = "Действия"
        $ current_action_content = None
        $ current_action_items = build_room_action_items(CurrentRoom)
    if str(return_label or "") != "":
        call expression return_label
    return


label ApplyTimePeriodChange(target_hour=8):
    $ target_hour = int(target_hour or 8) % 24
    $ calendar_v2.sync_state()
    if int(BlockTimeAdvance or 0) == 0 and int(calendar_v2.hour or 0) < target_hour:
        $ calendar_v2.hour = target_hour
        $ calendar_v2.minute = 0
        $ calendar_v2.sync_state()
        call stat
    $ return_loc = _time_return_label()
    if renpy.has_label(return_loc):
        jump expression return_loc
    jump TavernMain


screen time_change_card_overlay(return_label=""):
    zorder 120

    $ _title = "ВРЕМЯ"
    $ _body = _time_change_body_text()
    $ _items = _time_change_items(return_label)
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
