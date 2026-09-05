from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_main_menu_uses_full_screen_tavern_team_portrait_with_readable_text():
    screens = (PROJECT_ROOT / "game/screens.rpy").read_text(encoding="utf-8-sig")
    main_menu = screens.split("screen main_menu():", 1)[1].split("style main_menu_vbox is vbox", 1)[0]

    assert 'add "images/tavern/mainhall/tavern_crew.jpg":' in main_menu
    assert "xysize (config.screen_width, config.screen_height)" in main_menu
    assert 'fit "cover"' in main_menu
    assert 'style "main_menu_title"' in main_menu
    assert 'outlines [(2, "#000d", 0, 0)]' in screens


def test_main_menu_centers_text_only_actions_directly_below_large_title():
    screens = (PROJECT_ROOT / "game/screens.rpy").read_text(encoding="utf-8-sig")
    main_menu = screens.split("screen main_menu():", 1)[1].split("style main_menu_vbox is vbox", 1)[0]
    title = main_menu.split('text "Billy Bones Inn":', 1)[1].split("vbox:", 1)[0]
    actions = main_menu.split("vbox:", 1)[1]
    title_style = screens.split("style main_menu_title:", 1)[1].split("style main_menu_version:", 1)[0]
    button_style = screens.split("style main_menu_button:", 1)[1].split("style main_menu_button_text:", 1)[0]

    assert "xalign 0.5" in title
    assert "yalign 0.62" in title
    assert "text_align 0.5" in title
    assert "size 96" in title_style
    assert "xalign 0.5" in actions
    assert "ypos 0.70" in actions
    assert "yanchor 0.0" in actions
    assert "background None" in button_style
    assert "hover_background None" in button_style
    assert "selected_background None" in button_style
    assert "insensitive_background None" in button_style
    assert "Solid(" not in main_menu
