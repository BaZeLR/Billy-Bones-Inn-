from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_media_runtime_has_no_explicit_legacy_alias_table():
    media = _source("game/Utilities/General/Screens/ShowImage.rpy")

    assert "LEGACY_MEDIA_ALIASES" not in media
    assert "def _media_alias_candidate(" not in media
    assert "LEGACY_MEDIA_ALIASES.get(" not in media


def test_amanda_and_becky_dance_calls_name_real_assets():
    amanda_dance = _source("game/NPC/Girls/Amanda/IntAmandaDance.rpy")
    amanda_after = _source("game/NPC/Girls/Amanda/AmandaSexDanceStreet.rpy")
    amanda_events = _source("game/NPC/Girls/Amanda/AmandaLegareStreetEvents.rpy")
    becky_dance = _source("game/NPC/Girls/Becky/IntBeckyDance.rpy")
    combined = "\n".join((amanda_dance, amanda_after, amanda_events, becky_dance))

    for retired_name in (
        "YouInvite1", "YouInvite2", "YouClose", "YouDanceWorry",
        "YouDanceAngry", "YouDance", "YouKiss", "alberdanceStep",
    ):
        assert retired_name not in combined
    assert '"waiting_0.png"' in becky_dance
    assert '"you_invite_1.png"' in combined
    assert '"you_invites.png"' in combined
    assert '"you_kiss.png"' in combined
    assert '"legare_step_"' in amanda_dance
    assert '"amanda_portrait.jpg"' in amanda_events
