from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
TOPICS = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")
INIT = (ROOT / "game/NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
EDDIE_INIT = (ROOT / "game/NPC/Secondary/InitEddie.rpy").read_text(encoding="utf-8-sig")
EDDIE_TALK_INIT = (ROOT / "game/NPC/Secondary/InitEddieTalk.rpy").read_text(encoding="utf-8-sig")
BECKY_TALK = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalk.rpy").read_text(encoding="utf-8-sig")
BECKY_DINNER = (ROOT / "game/NPC/Girls/Becky/IntBeckyGuest.rpy").read_text(encoding="utf-8-sig")
BECKY_GEORGETT = (ROOT / "game/NPC/Girls/Becky/GeorgettBeckyVisit.rpy").read_text(encoding="utf-8-sig")


def test_becky_eddie_topics_are_one_ordered_thread():
    thread = RUNTIME.split('LThreadData(0, "becky", "EddieBackstory"', 1)[1]
    thread = thread.split('LThreadData(0, "becky", "GeorgettHomeVisit"', 1)[0]

    assert thread.count("story_becky_talk_eddie_0") == 1
    assert thread.count("story_becky_talk_eddie_georgett_0") == 1
    assert "EddieFirstTalk" not in RUNTIME
    assert "EddieGeorgettTalk" not in RUNTIME


def test_becky_eddie_labels_advance_same_thread_without_scalar_stage():
    labels = TOPICS.split("label story_becky_talk_eddie_0", 1)[1]
    labels = labels.split("label story_becky_home_invite_talk_0", 1)[0]

    assert labels.count("event_runtime.active_thread.advance()") == 2
    assert "event_runtime.active_thread.complete()" not in labels
    assert "eddietalk" not in labels
    assert '"eddietalk"' not in INIT


def test_invite_reads_completed_eddie_thread_and_old_stage_migrates_once():
    invite = TOPICS.split("label story_becky_home_invite_talk_0", 1)[1]
    invite = invite.split("label story_becky_talk_pregnancy_0", 1)[0]
    migration = MIGRATION.split("def updateSave_V25():", 1)[1]

    assert 'threads.get("beckyEddieBackstory", None)' in invite
    assert "int(_becky_eddie_thread.num or 0) >= 2" in invite
    assert 'becky_var.pop("eddietalk", 0)' in migration
    assert 'thread_rows.get("beckyEddieBackstory", None)' in migration
    assert '"beckyEddieFirstTalk", "beckyEddieGeorgettTalk"' in migration


def test_becky_eddie_reaction_comparison_is_label_local():
    reactions = TOPICS.split("label story_becky_talk_eddie_reaction_0", 1)[1]
    reactions = reactions.split("label story_becky_talk_eddie_after_sex_0", 1)[0]

    assert "change_mind=0" in reactions
    assert "ChangeMind" not in reactions


def test_eddie_story_uses_adult_orphan_manager_relationship():
    displayed_story = "\n".join((EDDIE_INIT, EDDIE_TALK_INIT, BECKY_TALK, BECKY_DINNER, BECKY_GEORGETT))

    assert 'birth_date={"day": 1, "period": 1, "cycle": 1081}' in EDDIE_INIT
    assert "молодой взрослый сирота" in EDDIE_INIT
    assert "приютила его сиротой" in EDDIE_TALK_INIT
    for retired_relation in (
        "сын Ребекки",
        "старший сын вдовы",
        "Беккин сынок",
        "смотрела на братца",
        "присутствием своего сына и дочки",
        "глядя сыну в глаза",
    ):
        assert retired_relation not in displayed_story


def test_eddie_attends_sunday_service_only_during_service_clock_window():
    schedule_path = ROOT / "game/NPC/Schedules/eddie.json"
    payload = json.loads(schedule_path.read_text(encoding="utf-8-sig"))
    rows = [row for row in payload["entries"] if row.get("label") == "sunday_service"]

    assert len(rows) == 1
    assert rows[0]["weekdays"] == [7]
    assert rows[0]["start"] == "08:00"
    assert rows[0]["end"] == "09:29"
    assert rows[0]["location"] == "Church"
    assert rows[0]["condition"] == {"rule": "eddie_in_town"}
