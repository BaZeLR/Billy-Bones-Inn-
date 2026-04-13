init python:
    # Ensure the default padding is safe
    style.default.padding = (0, 0, 0, 0)

    # Window styles
    style.intro_window = Style(style.default)
    style.intro_window.background = "#000000"
    style.intro_window.xfill = True
    style.intro_window.yfill = True
    style.intro_window.padding = (20, 20, 20, 20)

    # VBox style
    style.intro_vbox = Style(style.vbox)
    style.intro_vbox.spacing = 20
    style.intro_vbox.xalign = 0.5
    style.intro_vbox.yalign = 0.5

    # Text style
    style.intro_text = Style(style.text)
    style.intro_text.size = 24
    style.intro_text.color = "#ffffff"
    style.intro_text.xalign = 0.5
    style.intro_text.text_align = 0.5
