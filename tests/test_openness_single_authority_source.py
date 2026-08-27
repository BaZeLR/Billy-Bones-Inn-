from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_social_actions_do_not_reverse_sync_authored_openness_from_relationship():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    actions = (ROOT / "game/Utilities/General/Common/Actions.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "adjust_otkroven" not in game_sources
    assert "_action_sync_openness" not in game_sources
    assert "sync_openness" not in actions
    assert "info.change_social(friend_delta=" in actions


def test_old_point_actions_use_the_authoritative_social_signature():
    source = (ROOT / "game/NPC/Girls/Common/OldPointTalkSystem.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert 'apply_social_interaction_base(key, "flirt", gain, 4, 30, 1, 1, 0, 0)' in source
    assert 'apply_social_interaction_base(key, "kino", gain, 5, 30, 1, 0, 0, 0)' in source
    assert 'apply_social_interaction_base(key, "flirt", gain, 4, 30, 1, 1, 0, 0, True)' not in source
    assert 'apply_social_interaction_base(key, "kino", gain, 5, 30, 1, 0, 0, 0, True)' not in source
