from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_amanda_gloryhole_scene_state_is_owned_by_amanda():
    event = (ROOT / "game/NPC/Girls/Amanda/AmandaAtGloryHole.rpy").read_text(
        encoding="utf-8-sig"
    )
    room = (ROOT / "game/Inn/TavernGloryHole.rpy").read_text(encoding="utf-8-sig")

    assert "AmandaGloryCurState" not in event + room
    assert 'Amanda.var_int("glory_cur_state", 0)' in event
    assert 'Amanda.set_var_int("glory_cur_state",' in event
    assert 'Amanda.set_var_int("glory_cur_state",' in room
    assert "default AmandaGloryCurState" not in event
