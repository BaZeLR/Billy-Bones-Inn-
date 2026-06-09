from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"
ACTIONS_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Common" / "Actions.rpy"


def game_sources():
    for path in GAME_ROOT.rglob("*.rpy"):
        yield path, path.read_text(encoding="utf-8-sig")


def test_no_abstract_examine_action_label_or_factory():
    source = ACTIONS_PATH.read_text(encoding="utf-8-sig")

    assert '"examine":' not in source
    assert "def make_examine_action" not in source
    assert "\nlabel Examine" not in source


def test_no_object_action_targets_abstract_examine_label():
    offenders = []
    for path, source in game_sources():
        if 'target="Examine"' in source or "target='Examine'" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []
