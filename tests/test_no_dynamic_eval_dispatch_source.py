from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_live_game_has_no_qsp_dynamic_eval_compatibility_dispatcher():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "def dyneval(" not in game_sources
    assert "dyneval(" not in game_sources
    assert "DynEvalCompat.rpy" not in [path.name for path in (ROOT / "game").rglob("*.rpy")]


def test_francheska_talk_has_no_python_to_label_dispatcher():
    source = (ROOT / "game/NPC/Secondary/IntFrancheskaTalk.rpy").read_text(encoding="utf-8-sig")

    assert "def _fran_clean(" not in source
    assert "renpy.call(" not in source
