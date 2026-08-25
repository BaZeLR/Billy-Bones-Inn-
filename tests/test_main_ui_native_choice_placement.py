from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "game" / "screens.rpy"
MAIN_LAYOUT = ROOT / "game" / "Utilities" / "General" / "Screens" / "main_layout.rpy"
EVENTS = ROOT / "game" / "Utilities" / "General" / "Events" / "events.rpy"
OPTIONS = ROOT / "game" / "options.rpy"
SCRIPT = ROOT / "game" / "script.rpy"


def test_native_menu_choice_uses_main_ui_action_region_and_restores_the_hud():
    source = SCREENS.read_text(encoding="utf-8")
    start = source.index("screen choice(items, label=None, menu_name=None):")
    end = source.index("style choice_button_text is button_text", start)
    choice = source[start:end]

    assert 'if str(rooms.current_code or "") != "Intro":' in choice
    assert 'on "show" action Show("main_ui")' in choice
    assert 'if renpy.get_screen("main_ui") is None:' not in choice
    assert 'str(main_ui_runtime.mode or "") in ("talk", "event")' not in choice
    non_intro = choice.split('if str(rooms.current_code or "") != "Intro":', 1)[1].split(
        "    else:", 1
    )[0]
    assert "        null" in non_intro
    assert "frame:" not in non_intro
    assert "textbutton i.caption" not in non_intro
    assert "MAIN_UI_NATIVE_CHOICE" not in choice
    assert "viewport:" not in choice
    assert 'scrollbars "vertical"' not in choice
    assert "mousewheel True" not in choice
    assert "draggable True" not in choice


def test_native_menu_uses_the_named_main_ui_action_region_contract():
    source = MAIN_LAYOUT.read_text(encoding="utf-8")

    assert "MAIN_UI_NATIVE_CHOICE_TOP" not in source
    assert "MAIN_UI_NATIVE_CHOICE_HEIGHT" not in source
    assert "yminimum 300" in source
    assert 'screen current_action_panel(native_choice=None):' in source
    assert 'if native_choice is not None:' in source
    assert 'native_choice.scope.get("items", [])' in source
    assert "use choice_panel(_native_choice_items)" in source
    assert '$ _native_choice_screen = renpy.get_screen("choice")' in source
    assert 'use current_action_panel(_native_choice_screen)' in source
    assert 'if renpy.get_screen("choice") is None:' not in source
    action_region = source.split('$ _native_choice_screen = renpy.get_screen("choice")', 1)[1].split(
        'if str(main_ui_runtime.mode or "") != "event":', 1
    )[0]
    assert "viewport:" not in action_region
    assert "mousewheel True" not in action_region
    assert "draggable True" not in action_region


def test_room_and_object_action_buttons_use_the_same_hud_button_design():
    source = SCREENS.read_text(encoding="utf-8-sig")
    layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    options = OPTIONS.read_text(encoding="utf-8-sig")
    script = SCRIPT.read_text(encoding="utf-8-sig")
    panel = source.split("screen choice_panel(items, label=None):", 1)[1].split(
        "screen choice(items, label=None, menu_name=None):", 1
    )[0]

    assert 'style "mui_action_button"' in panel
    assert 'text_style "mui_action_button_text"' in panel
    assert "style mui_action_button is mui_hud_button:" in layout
    assert "style mui_action_button_text is mui_hud_button_text:" in layout
    hud_style = layout.split("style mui_hud_button is button:", 1)[1].split(
        "style mui_hud_button_text", 1
    )[0]
    assert 'background Solid("#141414")' in hud_style
    assert 'hover_background Solid("#242018")' in hud_style
    assert 'selected_background Solid("#322613")' in hud_style
    assert "gui.button_idle_background = None" in options
    assert "gui.button_hover_background = None" in options
    assert "style.button.background = None" in script
    assert "style.button.hover_background = None" in script


def test_actions_stay_above_the_bottom_character_block_without_scrollbars():
    source = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    main_ui = source.split("screen main_ui():", 1)[1].split("screen main_ui_left_panel", 1)[0]
    action_position = main_ui.index("use current_action_panel")
    spacer_position = main_ui.index("null yfill True", action_position)
    character_position = main_ui.index('text "Персонажи" size 20', spacer_position)

    assert action_position < spacer_position < character_position
    assert "yminimum 180" in main_ui[spacer_position:character_position]
    assert "viewport:" not in main_ui[action_position:character_position]
    assert 'scrollbars "vertical"' not in main_ui[action_position:character_position]


def test_intro_uses_its_authored_full_text_and_single_start_action():
    intro = (ROOT / "game/Inn/Intro.rpy").read_text(encoding="utf-8-sig")
    layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    choice_source = SCREENS.read_text(encoding="utf-8-sig")
    choice = choice_source.split("screen choice(items, label=None, menu_name=None):", 1)[1].split(
        "style choice_button_text is button_text", 1
    )[0]

    assert 'rooms.enter("Intro")' in intro
    assert "scene_runtime.location_text = scene_runtime.text" in intro
    assert '"[scene_runtime.text]"' in intro
    assert '"Приступить к управлению трактиром":' in intro
    assert "jump dev_after_report_checkpoint" in intro
    assert 'if str(rooms.current_code or "") != "Intro":' in choice
    assert 'textbutton "Приступить к управлению трактиром"' not in layout
    assert 'action Jump("TavernMain")' not in layout


def test_story_event_dispatch_keeps_main_ui_visible():
    source = EVENTS.read_text(encoding="utf-8-sig")
    trigger = source.split("label checkTriggers(location, action, numpop=0):", 1)[1].split(
        "label preEvent", 1
    )[0]

    assert 'if str(rooms.current_code or "") != "Intro":' in trigger
    assert "show screen main_ui" in trigger
    assert "jump expression evt.target" in trigger


def test_after_load_clears_every_saved_main_ui_context():
    source = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    clear_contexts = source.split("def clear_contexts(self):", 1)[1].split(
        "def main_ui_context_snapshot", 1
    )[0]

    assert "self.talk_origin = None" in clear_contexts
    assert "self.card_origin = None" in clear_contexts
    assert "self.scene_origin = None" in clear_contexts
    assert 'self.tavern_report_person = ""' in clear_contexts
    assert "self.tavern_report_origin = None" in clear_contexts


def test_tavern_report_uses_main_ui_context_without_detached_overlay_or_room_jump():
    report = (ROOT / "game/Inn/menu_tavernstat.rpy").read_text(encoding="utf-8-sig")
    layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")

    assert "tavern_report_card_overlay" not in report + layout
    assert "screen tavern_report_card_overlay" not in report
    assert "main_ui_runtime.tavern_report_origin" in report
    assert "main_ui_restore_context(origin)" in report
    assert "jump expression _room_label" not in report + layout
    assert 'items.append(MenuItem("Назад", Call("HideTavernReport", return_label)))' in report
    report_panel = layout.split("screen main_ui_tavern_report_panel():", 1)[1]
    assert 'textbutton "Закрыть"' not in report_panel
