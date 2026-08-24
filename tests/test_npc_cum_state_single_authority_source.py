import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SAVE_SYNC = GAME / "TractirSaveSync.rpy"


def test_npc_cum_state_is_owned_by_npc_objects():
    runtime = (GAME / "Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    becky = (GAME / "NPC/Girls/Becky/IntBeckySex.rpy").read_text(
        encoding="utf-8-sig"
    )
    eddie = (GAME / "NPC/Secondary/IntEddieBeckySex.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "def cum_state(self, key):" in runtime
    assert "def set_cum_state(self, key, value=1):" in runtime
    assert "def clear_cum(self, *keys):" in runtime
    assert 'Becky.cum_state("cum_face_you")' in becky
    assert 'Becky.clear_cum("cum_face_you", "cum_face_others")' in becky
    assert 'Becky.clear_cum("cum_inside_you", "cum_inside_others")' in eddie


def test_legacy_npc_cum_and_lick_maps_are_absent_from_live_code():
    sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in GAME.rglob("*.rpy")
        if path != SAVE_SYNC
    )
    migration = SAVE_SYNC.read_text(encoding="utf-8-sig")

    for name in (
        "CumFaceYou",
        "CumFaceOthers",
        "CumTitsYou",
        "CumTitsOthers",
        "CumInsideYou",
        "CumInsideOthers",
        "LickPussy",
    ):
        assert not re.search(r"\b%s\b" % name, sources), name
        assert '"%s"' % name in migration

    assert "def updateSave_V45():" in migration
    assert 'state["lick_pussy"] = max(' in migration
