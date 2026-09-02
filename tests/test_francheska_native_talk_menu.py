from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/NPC/Secondary/IntFrancheskaTalk.rpy"


def test_francheska_talk_uses_native_menu_and_restores_caller_context():
    source = SOURCE.read_text(encoding="utf-8-sig")
    talk = source.split("label FrancheskaTalk:", 1)[1]

    assert "\n    menu:\n" in talk
    assert "while True:" not in talk
    assert talk.count("jump FrancheskaTalk") == 12
    assert "call FrancheskaTalk" not in talk
    assert "label FrancheskaTalkEnd" not in source
    assert "call FrancheskaTalkApply" not in talk
    assert "label FrancheskaTalkApply" not in source
    assert "def _fran_topic_select" not in source
    assert "_fran_topic(" not in talk
    assert "_fran_random_topic" not in talk
    assert "FRANCHESKA_TALK_START[0]" in talk
    assert "FRANCHESKA_TALK_MAIN[10]" in talk
    assert "FRANCHESKA_TALK_SECOND[_fran_topic_index]" in talk
    assert "BuildFrancheskaTalkMenu" not in source
    assert "queue_paged_panel_text" not in source
    assert "ReturnToMainUI" not in source
    assert "MenuItem(" not in talk
    assert "main_ui_end_talk_state()" in source
    assert "jump expression _room_label" not in source


def test_francheska_live_talk_does_not_parse_qsp_or_use_file_fallbacks():
    source = SOURCE.read_text(encoding="utf-8-sig")
    data = (ROOT / "game/NPC/Secondary/FrancheskaTalkData.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "renpy.file" not in source
    assert "open(" not in source
    assert "_fran_read_source_text" not in source
    assert "_FRAN_PHRASE_CACHE" not in source
    assert "define FRANCHESKA_TALK_START" in data
    assert "define FRANCHESKA_TALK_SECOND" in data
    assert "define FRANCHESKA_TALK_MAIN" in data
    assert data.count("define FRANCHESKA_TALK_") == 3
