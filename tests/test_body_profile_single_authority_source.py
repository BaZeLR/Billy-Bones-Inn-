from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_body_profiles_are_transient_views_over_owner_state():
    body = (ROOT / "game/Utilities/General/Sex/BodyInteractionModel.rpy").read_text(
        encoding="utf-8-sig"
    )
    player = (ROOT / "game/Utilities/General/Player/Player.rpy").read_text(
        encoding="utf-8-sig"
    )
    intimacy = (ROOT / "game/Utilities/General/Sex/PlayerIntimacyState.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "BodyInteractionProfiles" not in game_sources
    assert "def bodymodel_build_profile(" in body
    assert "def bodymodel_owner_containers(" in body
    assert "player.intimacy.body_containers" in body
    assert 'state.setdefault("body_containers", {})' in body
    assert "self.body_containers = {}" in player
    assert "def player_body_profile():" in intimacy
    assert "bodymodel_sync_character" not in game_sources
    assert "bodymodel_sync_profile_arousal" not in game_sources
