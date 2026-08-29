from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game/Utilities/General/Screens/main_layout.rpy"
MIGRATION = ROOT / "game/TractirSaveSync.rpy"


RETIRED_UI_GLOBALS = (
    "current_action_title",
    "current_action_content",
    "current_action_items",
    "current_girl_key",
    "current_talk_picture",
    "current_object_id",
    "UI_mode",
    "UI_selected_char",
    "main_ui_inventory_dropdown_open",
    "main_ui_overlay",
    "player_inventory_view_mode",
    "player_inventory_view_section",
    "player_inventory_view_item",
    "player_card_inventory_origin",
    "story_board_selected_person",
)


def test_main_ui_runtime_is_the_only_live_projection_state_owner():
    runtime = RUNTIME.read_text(encoding="utf-8-sig")
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path != MIGRATION
    )

    for field in (
        "action_title",
        "action_content",
        "action_items",
        "girl_key",
        "talk_picture",
        "object_id",
        "mode",
        "selected_char",
        "inventory_dropdown_open",
        "overlay",
        "inventory_view_mode",
        "inventory_view_section",
        "inventory_view_item",
        "inventory_origin",
        "story_board_person",
    ):
        assert "self.%s =" % field in runtime
        assert "main_ui_runtime.%s" % field in live_sources

    for retired_name in RETIRED_UI_GLOBALS:
        assert re.search(r"\b%s\b" % re.escape(retired_name), live_sources) is None

    assert "global main_ui_runtime." not in live_sources
    assert "SetField(main_ui_runtime" in live_sources


def test_retired_ui_globals_are_consumed_only_by_one_save_migration():
    migration = MIGRATION.read_text(encoding="utf-8-sig")
    migration_block = migration.split("def updateSave_V37():", 1)[1].split(
        "label before_load:", 1
    )[0]

    assert "define currentVersion = 71" in migration
    for retired_name in RETIRED_UI_GLOBALS:
        assert '"%s"' % retired_name in migration_block
    assert "globals().pop(old_name, default_value)" in migration_block


def test_talk_panel_displays_label_owned_scene_picture_changes():
    runtime = RUNTIME.read_text(encoding="utf-8-sig")
    panel = runtime.split('screen main_ui_talk_panel(girl_name="", room_name="", desc=""):', 1)[1].split(
        "screen main_ui_player_card_panel", 1
    )[0]

    assert 'dict(main_ui_runtime.talk_origin or {}).get("picture", "")' in panel
    assert "_scene_picture != _talk_origin_picture" in panel
    assert "_portrait = _scene_picture if" in panel
