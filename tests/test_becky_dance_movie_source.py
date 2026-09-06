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


def test_becky_dance_pictures_follow_the_authored_action_progression():
    dance = _source(BECKY_DANCE)

    assert "becky_dance_continue_" not in dance
    assert '_dance_pic' not in dance

    invite_action = dance.split('"Пригласить потанцевать"', 1)[1].split('"Продолжить танцевать"', 1)[0]
    assert invite_action.count('"images/becky/dance/you_dance_2.png"') == 2
    assert '"images/becky/dance/waiting_0.png"' in invite_action
    assert '"images/becky/dance/butt_angy.png"' not in invite_action

    continue_action = dance.split('"Продолжить танцевать"', 1)[1].split('"Положить руки на талию"', 1)[0]
    for picture in (
        "french_kiss_2.png",
        "you_dance_7.png",
        "you dance_6.png",
        "you_dance_5.png",
        "you_dance_4.png",
        "you dance_3.png",
    ):
        assert '"images/becky/dance/{}"'.format(picture) in continue_action

    waist_action = dance.split('"Положить руки на талию"', 1)[1].split('"Положить руки на попу"', 1)[0]
    assert '"images/becky/dance/you_dance_3.png"' in waist_action
    assert '"images/becky/dance/you_dance_4.png"' in waist_action

    butt_action = dance.split('"Положить руки на попу"', 1)[1].split('"Сжать попу вдовы"', 1)[0]
    assert butt_action.count('"images/becky/dance/you_dance_5.png"') == 2

    squeeze_action = dance.split('"Сжать попу вдовы"', 1)[1].split('"Поцеловать Бекки"', 1)[0]
    assert squeeze_action.count('"images/becky/dance/you dance_6.png"') == 2

    kiss_action = dance.split('"Поцеловать Бекки"', 1)[1].split('"Принять предложение вдовы"', 1)[0]
    assert '"images/becky/dance/you_dance_7.png"' in kiss_action
    assert kiss_action.index('"images/becky/dance/french_kiss_1.png"') < kiss_action.index('"images/becky/dance/french_kiss_2.png"')
