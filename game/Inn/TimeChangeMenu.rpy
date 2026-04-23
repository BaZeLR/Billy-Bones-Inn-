init python:
    def _time_return_label():
        if CurrentRoom is not None:
            room_code = str(getattr(CurrentRoom, "code_name", "") or "")
            if room_code:
                return room_code
        return str(CurLoc or "TavernMain")

    def _time_label(value):
        labels = {
            0: "утро",
            1: "полдень",
            2: "день",
            3: "вечер",
            4: "ночь",
        }
        return labels.get(int(value or 0), str(value))

    def _time_overview_lines():
        ensure_calendar_state()
        return [
            "Сейчас: %02d:%02d." % (int(hour or 0), int(minute or 0)),
            "Время суток: %s." % str(calendar_time_slot_name_ru or _time_label(time)),
            "День недели: %s." % str(week_name or ""),
            "Дата: %s." % str(calendar_format_date_ru(day, month, year, week, False) or ""),
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
        current_time = int(time or 0)

        if block_advance == 0 and current_time == 0:
            items.append(MenuItem("Дождаться полудня", [Hide("time_change_card_overlay"), Call("ApplyTimeSlotChange", 1)]))
        if block_advance == 0 and current_time < 2:
            items.append(MenuItem("Дождаться дня", [Hide("time_change_card_overlay"), Call("ApplyTimeSlotChange", 2)]))
        if block_advance == 0 and current_time < 3:
            items.append(MenuItem("Дождаться вечера", [Hide("time_change_card_overlay"), Call("ApplyTimeSlotChange", 3)]))
        if block_advance == 0 and current_time < 4:
            items.append(MenuItem("Дождаться ночи", [Hide("time_change_card_overlay"), Call("ApplyTimeSlotChange", 4)]))

        if block_advance == 0:
            items.append(MenuItem("Дождаться следующего утра", [Hide("time_change_card_overlay"), Call("NextDay", _time_return_label(), 1)]))
            items.append(MenuItem("Пропустить 5 дней", [Hide("time_change_card_overlay"), Call("NextDay", _time_return_label(), 5)]))
            items.append(MenuItem("Пропустить неделю", [Hide("time_change_card_overlay"), Call("NextDay", _time_return_label(), 7)]))

        if str(return_label or "") == "__hide__":
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


label ApplyTimeSlotChange(target_time=0):
    $ target_time = int(target_time or 0)
    if int(BlockTimeAdvance or 0) == 0 and int(time or 0) < target_time:
        $ calendar_set_time_slot(target_time)
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
                for _item in _items:
                    textbutton _item.caption:
                        xminimum 360
                        text_size 20
                        text_bold True
                        text_color "#5c0f1b"
                        text_hover_color "#7d1a2c"
                        action _item.action
