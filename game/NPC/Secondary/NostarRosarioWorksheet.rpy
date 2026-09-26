screen nostar_rosario_worksheet():
    modal True
    zorder 200
    key "game_menu" action ShowMenu("save")

    default clue_page = 0
    default picked_field = ""
    default picked_house = -1

    $ _width = int(config.screen_width)
    $ _height = int(config.screen_height)
    $ _margin = int(_width * 0.03)
    $ _gap = int(_width * 0.015)
    $ _left_width = int(_width * 0.60)
    $ _right_width = _width - 2 * _margin - _gap - _left_width
    $ _panel_height = _height - 2 * _margin
    $ _inner_width = _left_width - 48
    $ _heading_width = 160
    $ _cell_width = int((_inner_width - _heading_width - 20) / 5)
    $ _option_width = int((_inner_width - 20) / 3)
    $ _picked_row = next((row for row in NOSTAR_ROSARIO_FIELDS if row[0] == picked_field), None)

    add Solid("#100b08")
    add Transform("images/rpg_message_bg.png", fit="cover")

    hbox:
        xpos _margin
        ypos _margin
        spacing _gap

        frame:
            xsize _left_width
            ysize _panel_height
            padding (24, 20)
            background "#f1dfb9f2"

            vbox:
                xfill True
                spacing 12

                text "ЗАПИСИ О РОЗАРИО" size 33 bold True color "#452719" xalign 0.5
                text "Пять домов слева направо. Нажмите на клетку и впишите одну из примет." size 19 color "#654730" xalign 0.5

                null height 4

                hbox:
                    spacing 4
                    frame:
                        xsize _heading_width
                        ysize 48
                        background "#593b29"
                        text "Примета" size 20 bold True color "#f6e6c8" xalign 0.5 yalign 0.5
                    for house in range(5):
                        frame:
                            xsize _cell_width
                            ysize 48
                            background "#593b29"
                            text "Дом [house + 1]" size 21 bold True color "#f6e6c8" xalign 0.5 yalign 0.5

                for field, title, choices in NOSTAR_ROSARIO_FIELDS:
                    hbox:
                        spacing 4
                        frame:
                            xsize _heading_width
                            ysize 62
                            background "#b99768"
                            text title size 20 bold True color "#342216" xalign 0.5 yalign 0.5
                        for house in range(5):
                            $ _cell = Nostar.rosario_cell(field, house)
                            $ _caption = next((label for code, label in choices if code == _cell), "+ выбрать")
                            textbutton _caption:
                                id ("nostar_rosario_cell_%s_%d" % (field, house))
                                xsize _cell_width
                                ysize 62
                                background ("#f9edcf" if picked_field != field or picked_house != house else "#d7a96a")
                                hover_background "#ffe6ae"
                                text_size 18
                                text_color "#3d2a1b"
                                text_hover_color "#24160e"
                                text_xalign 0.5
                                text_yalign 0.5
                                action [SetScreenVariable("picked_field", field), SetScreenVariable("picked_house", house)]

                text "Заполнено [Nostar.rosario_count()] из 25 клеток. Каждая примета может принадлежать только одному дому." size 18 color "#5d3c25"

                frame:
                    xfill True
                    ysize 177
                    padding (12, 10)
                    background "#d8b98be8"

                    vbox:
                        spacing 7
                        if _picked_row is not None and picked_house >= 0:
                            text "Дом [picked_house + 1] — [_picked_row[1]]" size 20 bold True color "#442817"
                            grid 3 2:
                                spacing 6
                                for code, caption in list(_picked_row[2]) + [("", "Очистить клетку")]:
                                    textbutton caption:
                                        id ("nostar_rosario_choice_%s" % (code or "clear"))
                                        xsize _option_width
                                        ysize 52
                                        background "#f7e9c8"
                                        hover_background "#fff4d8"
                                        text_size 18
                                        text_color "#382516"
                                        text_hover_color "#1e130c"
                                        text_xalign 0.5
                                        text_yalign 0.5
                                        action [Function(Nostar.set_rosario_cell, picked_field, picked_house, code), SetScreenVariable("picked_field", ""), SetScreenVariable("picked_house", -1)]
                        else:
                            text "Выберите клетку в таблице. Варианты появятся здесь; ошибочную запись можно заменить или стереть." size 21 color "#4b301d"

                null height 5
                hbox:
                    spacing 18
                    textbutton "Назвать хозяйку Розарио":
                        id "nostar_rosario_submit"
                        xsize int(_inner_width * 0.60)
                        ysize 54
                        background "#754426"
                        hover_background "#965a30"
                        insensitive_background "#9b8d78"
                        text_size 22
                        text_color "#f6e9d2"
                        text_insensitive_color "#dfd2bf"
                        text_xalign 0.5
                        sensitive Nostar.rosario_filled()
                        action Return("submit")
                    textbutton "Вернуться позже":
                        id "nostar_rosario_later"
                        xsize int(_inner_width * 0.36)
                        ysize 54
                        background "#a88961"
                        hover_background "#c2a374"
                        text_size 21
                        text_color "#2f1d12"
                        text_xalign 0.5
                        action Return("later")

        frame:
            xsize _right_width
            ysize _panel_height
            padding (22, 20)
            background "#2c1d16ee"

            vbox:
                xfill True
                spacing 14
                text "ПРИМЕТЫ УЛИЦЫ" size 29 bold True color "#efdbaf" xalign 0.5
                text "Сверяйте записи с таблицей. Дома стоят по порядку, от первого до пятого." size 19 color "#d5c29f"

                hbox:
                    spacing 8
                    for page, caption in ((0, "1–5"), (1, "6–10"), (2, "11–14")):
                        textbutton caption:
                            id ("nostar_rosario_clues_%d" % page)
                            xsize int((_right_width - 60) / 3)
                            ysize 48
                            background ("#ad8250" if clue_page == page else "#65452f")
                            hover_background "#ba915c"
                            text_size 20
                            text_color "#fff1d8"
                            text_xalign 0.5
                            action SetScreenVariable("clue_page", page)

                frame:
                    xfill True
                    yfill True
                    padding (16, 15)
                    background "#ead6ad"

                    viewport:
                        xfill True
                        yfill True
                        draggable True
                        mousewheel True

                        text NOSTAR_ROSARIO_CLUE_PAGES[clue_page] size 21 color "#352318" line_spacing 5
