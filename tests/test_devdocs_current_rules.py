from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEVDOCS = PROJECT_ROOT / "devdocs"


def test_reference_devdocs_are_not_deleted_as_cleanup_policy():
    restored_reference_files = [
        "renpy_scene_action_panel_template.md",
        "RPY_AUDIT_2026-03-06.md",
        "SCRIPT_TIME_UI_PATTERN_NOTES.md",
    ]

    assert [name for name in restored_reference_files if not (DEVDOCS / name).exists()] == []


def test_current_knowledge_base_contains_only_current_copyable_rules():
    source = (DEVDOCS / "RENpy_ENGINE_PROJECT_KNOWLEDGE_BASE.md").read_text(encoding="utf-8-sig")

    assert "NPC identity belongs to `PeopleData` subclasses." in source
    assert "NPC runtime state belongs to info-class instances" in source
    assert "Display slots are UI" in source
    assert "display only and should not decide gameplay availability." in source
    assert "call SceneActionPanel" not in source
    assert "$ main_ui_set_action_panel" not in source
    assert "RefreshCurrentActionMenu" not in source
    assert "ApplyActionResultToUI" not in source
    assert "time_slots=[0, 1, 2, 3, 4]" not in source
    assert "Preserve `CharacterActionHub`" not in source
    assert "NPC_META" not in source


def test_project_map_uses_current_workspace_and_owner_model():
    source = (DEVDOCS / "PROJECT_MAP_AND_DEPENDENCIES.md").read_text(encoding="utf-8-sig")

    assert "C:/Users/blank/Documents/RenPy_Projects/Tractir" in source
    assert "Ren'Py_Projects" not in source
    assert "Room files own their local room label" in source
    assert "NPC-specific state belongs on the NPC info object" in source
    assert "`calendar_v2` owns day, week, hour, and minute." in source
    assert "SceneActionPanel" not in source
    assert "RefreshCurrentActionMenu" not in source
    assert "ApplyActionResultToUI" not in source
