from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game/Utilities/General/Screens/main_layout.rpy"
PLAYER_CARD = ROOT / "game/Utilities/General/Screens/PlayerCard.rpy"
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

    assert "define currentVersion = 76" in migration
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


def test_inventory_items_render_on_left_with_one_quantity_authority_and_fixed_back():
    runtime = RUNTIME.read_text(encoding="utf-8-sig")
    player_card = PLAYER_CARD.read_text(encoding="utf-8-sig")
    inventory_state = player_card.split("def player_card_show_inventory_menu_state", 1)[1].split(
        "def player_card_show_inventory_section_state", 1
    )[0]
    section_state = player_card.split("def player_card_show_inventory_section_state", 1)[1].split(
        "def player_card_show_inventory_item_state", 1
    )[0]
    panel = runtime.split("screen main_ui_player_card_panel():", 1)[1].split(
        "screen main_ui_girl_card_panel", 1
    )[0]

    assert 'main_ui_runtime.inventory_view_mode = "inventory"' in inventory_state
    assert 'MenuItem(player_card_inventory_menu_caption(item_id)' not in inventory_state
    assert 'MenuItem(player_card_inventory_menu_caption(item_id)' not in section_state
    assert 'MenuItem("Назад"' in inventory_state
    assert 'MenuItem("Назад"' in section_state
    assert "_inventory_ids[index:index + 2]" in panel
    assert 'id ("main_ui_inventory_item_%s" % _item_id)' in panel
    assert "player_card_inventory_count(_item_id)" in panel
    assert 'action Call("PlayerCardInventoryItemMenu", _item_id)' in panel
    assert "player.inventory.items" not in panel
