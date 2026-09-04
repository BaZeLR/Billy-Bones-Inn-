from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
RUNTIME = (GAME / "Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
HOME_FRONT = (GAME / "Town/BeckyHomeFront.rpy").read_text(encoding="utf-8-sig")
HOME = (GAME / "Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")
SEX = (GAME / "NPC/Girls/Becky/IntBeckySex.rpy").read_text(encoding="utf-8-sig")
DINNER = (GAME / "NPC/Girls/Becky/IntBeckyGuest.rpy").read_text(encoding="utf-8-sig")
TOPICS = (GAME / "NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")
EDDIE_SCENE = (GAME / "NPC/Girls/Becky/BeckyEddieJoinFirst.rpy").read_text(encoding="utf-8-sig")
CHURCH = (GAME / "NPC/Girls/Becky/IntBeckyAfterCermon.rpy").read_text(encoding="utf-8-sig")


def test_becky_progress_has_one_thread_owner_per_story_sequence():
    for subname in ("Home", "Dinner", "Sex", "EddieSex"):
        assert RUNTIME.count(f'LThreadData(0, "becky", "{subname}"') == 1

    assert 'LThreadData(0, "becky", "GeorgettHomeVisit"' not in RUNTIME
    assert "default becky_home" not in RUNTIME.lower()
    assert "default becky_dinner" not in RUNTIME.lower()
    assert "default becky_sex" not in RUNTIME.lower()
    assert "default becky_eddie_sex" not in RUNTIME.lower()


def test_becky_labels_advance_their_authoritative_story_threads():
    assert 'event_runtime.active_thread.advance()' in HOME_FRONT.split(
        "label story_becky_home_arrival_0:", 1
    )[1].split('label BeckyHomeFront(', 1)[0]
    assert 'threads["beckyHome"].advanceTo(2, force_active=True)' in HOME + SEX
    invite = TOPICS.split("label story_becky_home_invite_talk_0", 1)[1].split(
        "label story_becky_talk_pregnancy_0", 1
    )[0]
    assert 'event_runtime.active_thread.advance()' in invite

    assert 'threads["beckyDinner"].advanceTo(1, force_active=True)' in DINNER
    assert 'threads["beckyDinner"].advanceTo(2, force_active=True)' in DINNER
    assert 'event_runtime.active_thread.advanceTo(4, force_active=True)' in EDDIE_SCENE
    assert 'threads["beckyEddieSex"].advanceTo(5, complete_at_end=True)' in CHURCH


def test_retired_becky_stage_fields_are_load_migration_only():
    live = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in GAME.rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    for retired_stage in (
        "home_visit_stage",
        "home_sex_unlocked",
        "open_oral_stage",
        "eddie_join_stage",
    ):
        assert retired_stage not in live
