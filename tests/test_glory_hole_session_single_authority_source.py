from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_tavern_management_owns_glory_hole_session_and_reroll():
    player_source = read_rel("game/Utilities/General/Player/Player.rpy")
    glory_source = read_rel("game/Inn/TavernGloryHole.rpy")

    assert "class PlayerGloryHoleSessionState(object):" in player_source
    assert "self.glory_hole_session = PlayerGloryHoleSessionState()" in player_source
    assert "def roll_inside(self, worker_corruption=0):" in player_source
    assert glory_source.count("session.roll_inside(") == 2
    assert 'key="procedural:Inn/TavernGloryHole.rpy:inside:80"' in player_source
    assert 'key="procedural:Inn/TavernGloryHole.rpy:inside:50"' in player_source
    assert 'key="procedural:Inn/TavernGloryHole.rpy:inside_once"' in player_source


def test_retired_glory_hole_scratch_names_are_migration_only():
    retired_names = (
        "GirlNameTGH", "GloryHoleCurrentStep", "CockInGloryHole",
        "GloryHoleInside", "GloryHoleInsideOnce", "GloryHoleWorks",
        "GloryLine1", "GloryLine2", "GloryLine3",
        "GloryGirlLine0", "GloryGirlLine1", "GloryGirlLine2", "GloryGirlLine3",
        "BlockGloryHoleMenu", "AmandaAtGlory",
        "GloryHoleYouLine1", "GloryHoleYouLine2", "GloryHoleYouLine3",
    )
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    migration = read_rel("game/TractirSaveSync.rpy")

    for retired_name in retired_names:
        assert re.search(r"\b%s\b" % re.escape(retired_name), live_sources) is None
        assert '"%s"' % retired_name in migration
    assert "def updateSave_V39():" in migration


def test_only_system_instances_are_explicitly_rebound_as_globals():
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    gameplay_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    migration = read_rel("game/TractirSaveSync.rpy")
    global_names = set(re.findall(r"^\s*global\s+([^\n]+)$", live_sources, re.MULTILINE))

    assert global_names == {"people", "saveVersion", "threads"}
    assert "action_menu_specs" not in live_sources
    assert "SignalBlockTime" not in gameplay_sources
    assert 'globals().pop("SignalBlockTime", None)' in migration
