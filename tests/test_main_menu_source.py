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
