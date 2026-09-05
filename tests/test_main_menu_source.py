from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_main_menu_uses_full_screen_tavern_team_portrait_with_contrast_overlay():
    screens = (PROJECT_ROOT / "game/screens.rpy").read_text(encoding="utf-8-sig")
    main_menu = screens.split("screen main_menu():", 1)[1].split("style main_menu_frame is empty", 1)[0]

    assert 'add "images/tavern/mainhall/tavern_crew.jpg":' in main_menu
    assert "xysize (config.screen_width, config.screen_height)" in main_menu
    assert 'fit "cover"' in main_menu
    assert 'background Solid("#080604b8")' in main_menu
    assert 'style "main_menu_title"' in main_menu
    assert 'outlines [(2, "#000d", 0, 0)]' in screens


def test_main_menu_centers_large_title_and_places_backed_buttons_lower_right():
    screens = (PROJECT_ROOT / "game/screens.rpy").read_text(encoding="utf-8-sig")
    main_menu = screens.split("screen main_menu():", 1)[1].split("style main_menu_frame is empty", 1)[0]
    title = main_menu.split('text "Billy Bones Inn":', 1)[1].split("frame:", 1)[0]
    frame = main_menu.split("frame:", 1)[1]
    title_style = screens.split("style main_menu_title:", 1)[1].split("style main_menu_version:", 1)[0]
    button_style = screens.split("style main_menu_button:", 1)[1].split("style main_menu_button_text:", 1)[0]

    assert "xalign 0.5" in title
    assert "yalign 0.62" in title
    assert "text_align 0.5" in title
    assert "size 96" in title_style
    assert "xalign 1.0" in frame
    assert "yalign 1.0" in frame
    assert "xoffset -24" in frame
    assert "yoffset -24" in frame
    assert 'background Solid("#17100bd9")' in button_style
    assert 'hover_background Solid("#8a5a24e6")' in button_style
