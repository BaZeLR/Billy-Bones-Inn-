from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_obsolete_paged_panel_runtime_is_removed_after_native_menu_port():
    source = (ROOT / "game/Utilities/General/NPC/PartEventYourFirstReaction.rpy").read_text(encoding="utf-8-sig")
    for stale_name in (
        "PagedPanelRuntimeState",
        "default paged_panel",
        "queue_paged_panel_text",
        "advance_paged_panel_text",
        "QueuePagedPanelText",
        "QueueTavernEventPages",
        "build_tavern_event_pages",
    ):
        assert stale_name not in source
    assert "def _normalize_tavern_event_text(text):" in source
    assert "def format_tavern_event_text(text):" in source


def test_paged_panel_save_migration_and_ui_wrapper_are_removed():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    actions = (ROOT / "game/Utilities/General/Common/Actions.rpy").read_text(encoding="utf-8-sig")
    assert "tractir_save_migrate_paged_panel_runtime" not in migration
    assert "panel_paged_" not in migration
    assert "tavern_event_pages" not in migration
    assert "label ReturnToMainUI:" not in actions
