"""Regression contracts for the authored Legare household disclosure."""

import re
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
CLARA = (ROOT / "game/NPC/Girls/Clara/IntClaraTalk.rpy").read_text(encoding="utf-8")
ALBER = (ROOT / "game/NPC/Secondary/InitAlber.rpy").read_text(encoding="utf-8")
CHURCH = (ROOT / "game/Town/Church/Church.rpy").read_text(encoding="utf-8")
FAMILY = CLARA.split('            "Спросить Клариссу о семье"', 1)[1].split(
    '            "Спросить Клариссу о ней самой"', 1
)[0]
SERVICE = CHURCH.split("label ChurchServiceLegare:", 1)[1].split(
    "label ChurchServiceBlanken:", 1
)[0]


def choice_gate(caption):
    match = re.search(r'^\s*"' + re.escape(caption) + r'" if (.*):$', CLARA, re.M)
    assert match, caption
    return match.group(1)


@pytest.mark.parametrize("rel,asked,available", [(5, 0, False), (6, 0, True), (20, 1, False)])
def test_public_question_keeps_existing_friendship_and_daily_gate(rel, asked, available):
    state = {"Clara": SimpleNamespace(rel=rel, asked_today=asked)}
    assert eval(choice_gate("Спросить Клариссу о семье"), {}, state) is available


@pytest.mark.parametrize(
    "rel,trust,paintings,completed,deeper,deepest",
    [
        (7, 4, 4, False, False, False),
        (8, 3, 4, False, False, False),
        (8, 4, 3, False, False, False),
        (8, 4, 4, False, True, False),
        (9, 6, 6, False, True, False),
        (10, 5, 6, False, True, False),
        (10, 6, 5, False, True, False),
        (10, 6, 6, False, True, True),
        (10, 6, 4, True, True, True),
        (20, 20, 10, True, True, True),
    ],
)
def test_each_disclosure_gate_reads_existing_current_state(
    rel, trust, paintings, completed, deeper, deepest
):
    state = {
        "Clara": SimpleNamespace(rel=rel, trust=trust),
        "threads": {"claraPaintingsPath": SimpleNamespace(num=paintings, completed=completed)},
    }
    assert eval(choice_gate("Узнать о пансионе подробнее"), {}, state) is deeper
    assert eval(choice_gate("Спросить о будущем воспитанниц"), {}, state) is deepest


def test_daily_reward_occurs_once_before_disclosure_gates_without_new_story_state():
    reward = (
        "$ Clara.mark_asked()",
        "$ Clara.mark_talked()",
        "$ Clara.trust = min(20, int(Clara.trust or 0) + 1)",
        "$ Clara.change_social(friend_delta=1)",
    )
    for statement in reward:
        assert FAMILY.count(statement) == 1
        assert FAMILY.index(statement) < FAMILY.index('"Узнать о пансионе подробнее"')
    assert re.findall(r"\$ Clara\.(\w+)\s*=", FAMILY) == ["trust"]
    assert not re.search(r'threads\[.*?\]\.(?:\w+\s*=(?!=)|(?:advance\w*|complete|abort)\s*\()', FAMILY)


def test_native_disclosure_is_sequential_and_has_back_at_every_depth():
    assert FAMILY.count("menu:") == 3
    assert FAMILY.count('"Вернуться к разговору":') == 3
    assert FAMILY.count("main_ui_begin_native_scene_state(") == 1
    assert FAMILY.count("main_ui_end_native_scene_state()") == 1
    assert 'vscene "images/clara/portrait.png"' in FAMILY
    assert FAMILY.index("профессиональная гувернантка") < FAMILY.index("взрослая пансионерка")
    assert FAMILY.index("взрослая пансионерка") < FAMILY.index("наложницей")
    assert "профессиональная гувернантка" in ALBER
    assert "не дочь Легаре" in FAMILY
    assert not re.search(r"\b(?:label|jump|call screen|while)\b", FAMILY)


def test_church_story_interception_stays_before_repeatable_household_scene():
    assert SERVICE.index('if story_event_available("Church", "clara_paintings"):') < SERVICE.index(
        'main_ui_begin_native_scene_state("Дом Легаре")'
    )
    assert 'call checkTriggers("Church", "clara_paintings", 0)\n        return' in SERVICE
    assert "профессиональная гувернантка" in SERVICE
    assert "взрослая воспитанница" in SERVICE
    assert "а не дочь Легаре" in SERVICE
    assert '"Рассмотреть Элоизу и Полину":' in SERVICE
    assert '"Вернуться к прихожанам":' in SERVICE
    assert '"Назад":' in SERVICE
    assert SERVICE.count("main_ui_end_native_scene_state()") == 1
    assert "ShowImageSeq" not in SERVICE


@pytest.mark.parametrize("filename", ["household_school.png", "aloise_pauline_school.png"])
def test_church_illustration_paths_are_real_assets(filename):
    relative = "images/Alber/church/" + filename
    assert 'vscene "' + relative + '"' in SERVICE
    assert (ROOT / "game" / relative).is_file()


def test_existing_fiance_illustrations_remain_in_their_story_owner():
    story = (ROOT / "game/NPC/Girls/Clara/ClaraPaintingsThread.rpy").read_text(encoding="utf-8")
    church_story = story.split("label story_clara_paintings_church_6:", 1)[1].split("\nlabel ", 1)[0]
    for filename in ("cermon_fiance_clara.png", "cermon_fiance1_clara.png"):
        assert 'vscene "images/Alber/church/' + filename + '"' in church_story
    assert "$ event_runtime.active_thread.advance()" in church_story
