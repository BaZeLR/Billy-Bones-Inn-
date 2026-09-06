from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BECKY_DANCE = ROOT / "game" / "NPC" / "Girls" / "Becky" / "IntBeckyDance.rpy"
BECKY_INVITE = ROOT / "game" / "NPC" / "Girls" / "Becky" / "BeckyInviteHome.rpy"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def test_becky_movie_belongs_only_to_the_home_invitation_boundary():
    dance = _source(BECKY_DANCE)
    invite = _source(BECKY_INVITE)

    assert "dance_finish.webm" not in dance
    assert invite.count('vscene "images/becky/dance/dance_finish.webm"') == 1
    assert 'renpy.music.set_volume(0.0, delay=0.0, channel="movie")' in invite
    assert '"Закрыть видео":' in invite

    movie_index = invite.index('vscene "images/becky/dance/dance_finish.webm"')
    close_index = invite.index('"Закрыть видео":')
    invitation_index = invite.index('"Стефан, а может ко мне в гости зайдешь')
    assert movie_index < close_index < invitation_index


def test_becky_invitation_restores_the_last_dance_picture_after_movie():
    invite = _source(BECKY_INVITE)

    assert '$ _becky_dance_picture_before_invite = scene_runtime.picture' in invite
    assert "vscene _becky_dance_picture_before_invite" in invite
