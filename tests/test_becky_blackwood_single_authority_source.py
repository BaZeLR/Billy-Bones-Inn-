from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_becky_blackwood_knowledge_has_one_live_property():
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert "KnowSherwood" not in live_sources
    assert "KnowBlackwood" not in live_sources
    assert "Becky.knows_blackwood" in live_sources
    assert 'becky_var.pop("KnowSherwood", 0)' in migration
    assert 'becky_var.pop("KnowBlackwood"' in migration
    assert 'becky_var["KnowBlackwood"]' not in migration


def test_becky_has_no_unused_legacy_import_marker():
    source = (ROOT / "game/NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")

    assert "legacy_story_imported" not in source
