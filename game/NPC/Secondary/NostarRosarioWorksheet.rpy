define NOSTAR_ROSARIO_SCRIPT_FONT = "fonts/Amatic_SC,Lobster,Roboto_Slab/Lobster/Lobster-Regular.ttf"
define NOSTAR_ROSARIO_MARKER_FONT = "fonts/Amatic_SC,Lobster,Roboto_Slab/Amatic_SC/AmaticSC-Bold.ttf"
define NOSTAR_ROSARIO_BODY_FONT = "fonts/Amatic_SC,Lobster,Roboto_Slab/Roboto_Slab/static/RobotoSlab-Regular.ttf"

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

    add Transform("images/nostar/nobility_quarters.png", fit="cover")
    add Solid("#1d100bd0")
    add Transform("images/rpg_message_bg.png", fit="cover", alpha=0.92)

    hbox:
        xpos _margin
        ypos _margin
        spacing _gap

        frame:
            xsize _left_width
            ysize _panel_height
            padding (24, 20)
            background "#f3e3c7ed"

            vbox:
                xfill True
                spacing 12

                text "Загадка Розарио" font NOSTAR_ROSARIO_SCRIPT_FONT size 45 color "#6b2e25" xalign 0.5
                text "Пять домов слева направо. Каждая строка — одна тайна улицы." font NOSTAR_ROSARIO_BODY_FONT size 19 color "#624a36" xalign 0.5

                frame:
                    xfill True
                    ysize 3
                    background "#ad8652"

                null height 1

                hbox:
                    spacing 4
                    frame:
                        xsize _heading_width
                        ysize 55
                        background "#79543c"
                        text "ПРИМЕТА" font NOSTAR_ROSARIO_MARKER_FONT size 31 color "#f8e9ce" xalign 0.5 yalign 0.5
                    for house in range(5):
                        frame:
                            xsize _cell_width
                            ysize 55
                            background "#79543c"
                            text "ДОМ [house + 1]" font NOSTAR_ROSARIO_MARKER_FONT size 33 color "#f8e9ce" xalign 0.5 yalign 0.5

                for field, title, choices in NOSTAR_ROSARIO_FIELDS:
                    hbox:
                        spacing 4
                        frame:
                            xsize _heading_width
                            ysize 62
                            background "#ddbd8d"
                            text title font NOSTAR_ROSARIO_MARKER_FONT size 29 color "#583322" xalign 0.5 yalign 0.5
                        for house in range(5):
                            $ _cell = Nostar.rosario_cell(field, house)
                            $ _caption = next((label for code, label in choices if code == _cell), "+ выбрать")
                            textbutton _caption:
                                id ("nostar_rosario_cell_%s_%d" % (field, house))
                                xsize _cell_width
                                ysize 62
                                background ("#fff2d6a8" if picked_field != field or picked_house != house else "#d7a16c")
                                hover_background "#e9cb9e"
                                text_font NOSTAR_ROSARIO_BODY_FONT
                                text_size 18
                                text_color "#4b3122"
                                text_hover_color "#6b2e25"
                                text_xalign 0.5
                                text_yalign 0.5
                                action [SetScreenVariable("picked_field", field), SetScreenVariable("picked_house", house)]

                text "На пергаменте [Nostar.rosario_count()] из 25 примет. Каждая принадлежит лишь одному дому." font NOSTAR_ROSARIO_BODY_FONT size 17 color "#70533c" xalign 0.5

                frame:
                    xfill True
                    ysize 177
                    padding (12, 10)
                    background "#e1c596dc"

                    vbox:
                        spacing 7
                        if _picked_row is not None and picked_house >= 0:
                            text "Дом [picked_house + 1] — [_picked_row[1]]" font NOSTAR_ROSARIO_SCRIPT_FONT size 26 color "#743b29"
                            grid 3 2:
                                spacing 6
                                for code, caption in list(_picked_row[2]) + [("", "Очистить клетку")]:
                                    textbutton caption:
                                        id ("nostar_rosario_choice_%s" % (code or "clear"))
                                        xsize _option_width
                                        ysize 52
                                        background "#f9ebcce0"
                                        hover_background "#fff5db"
                                        text_font NOSTAR_ROSARIO_BODY_FONT
                                        text_size 18
                                        text_color "#4b3122"
                                        text_hover_color "#7b3627"
                                        text_xalign 0.5
                                        text_yalign 0.5
                                        action [Function(Nostar.set_rosario_cell, picked_field, picked_house, code), SetScreenVariable("picked_field", ""), SetScreenVariable("picked_house", -1)]
                        else:
                            text "Коснитесь пустой клетки и впишите примету. Чернила ещё можно стереть." font NOSTAR_ROSARIO_SCRIPT_FONT size 25 color "#70442e"

                null height 5
                frame:
                    xfill True
                    ysize 2
                    background "#ad8652"
                hbox:
                    spacing 18
                    textbutton "Назвать похитительницу Розарио":
                        id "nostar_rosario_submit"
                        xsize int(_inner_width * 0.60)
                        ysize 54
                        background "#763e30"
                        hover_background "#9a5642"
                        insensitive_background "#a69783"
                        text_font NOSTAR_ROSARIO_SCRIPT_FONT
                        text_size 26
                        text_color "#f6e9d2"
                        text_insensitive_color "#dfd2bf"
                        text_xalign 0.5
                        sensitive Nostar.rosario_filled()
                        action Return("submit")
                    textbutton "Вернуться позже":
                        id "nostar_rosario_later"
                        xsize int(_inner_width * 0.36)
                        ysize 54
                        background "#b38f5e"
                        hover_background "#c6a16c"
                        text_font NOSTAR_ROSARIO_SCRIPT_FONT
                        text_size 25
                        text_color "#2f1d12"
                        text_xalign 0.5
                        action Return("later")

        frame:
            xsize _right_width
            ysize _panel_height
            padding (22, 20)
            background "#f3e3c7f4"

            vbox:
                xfill True
                spacing 14
                text "Приметы улицы" font NOSTAR_ROSARIO_SCRIPT_FONT size 39 color "#6b2e25" xalign 0.5
                text "Леди Ностар велела читать их по порядку, от первого дома к пятому." font NOSTAR_ROSARIO_BODY_FONT size 18 color "#624a36"

                frame:
                    xfill True
                    ysize 3
                    background "#ad8652"

                hbox:
                    spacing 8
                    for page, caption in ((0, "Лист I"), (1, "Лист II"), (2, "Лист III")):
                        textbutton caption:
                            id ("nostar_rosario_clues_%d" % page)
                            xsize int((_right_width - 60) / 3)
                            ysize 48
                            background ("#874b37" if clue_page == page else "#c5a270")
                            hover_background "#9a5e43"
                            text_font NOSTAR_ROSARIO_SCRIPT_FONT
                            text_size 24
                            text_color ("#fff1d8" if clue_page == page else "#3e291d")
                            text_xalign 0.5
                            action SetScreenVariable("clue_page", page)

                frame:
                    xfill True
                    yfill True
                    padding (16, 15)
                    background "#fbf0d7bf"

                    viewport:
                        xfill True
                        yfill True
                        draggable True
                        mousewheel True
                        scrollbars "vertical"
                        vscrollbar_base_bar "#d2b88d"
                        vscrollbar_thumb "#8f5e40"
                        vscrollbar_xsize 10
                        vscrollbar_unscrollable "hide"

                        text NOSTAR_ROSARIO_CLUE_PAGES[clue_page] font NOSTAR_ROSARIO_BODY_FONT size 19 color "#423020" line_spacing 7
