from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_returnable_labels_keep_result_text_in_label_parameters():
    label_sources = {
        "EventAmandaLizettTalk": read_rel("game/NPC/Girls/Amanda/EventAmandaLizettTalk.rpy"),
        "EventAmandaLizettTalk2": read_rel("game/NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy"),
        "DisplayTavernEventsSummary": read_rel("game/Utilities/General/Common/DisplayTavernEventsSummary.rpy"),
        "PartEventAfterHarrassment": read_rel("game/Utilities/General/NPC/PartEventAfterHarrassment.rpy"),
        "PartEventCustomerHarrassmentReaction": read_rel("game/Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy"),
        "EventWineForDance": read_rel("game/Inn/EventWineForDance.rpy"),
        "event_cleaning_harrass": read_rel("game/NPC/Girls/Common/EventCleaningHarrass.rpy"),
        "event_waitress_harrass": read_rel("game/NPC/Girls/Common/EventWaitressHarrass.rpy"),
        "ShowGirlSexHistory": read_rel("game/NPC/Girls/Common/ShowGirlSexHistory.rpy"),
        "PartEventGirlHarrassmentReaction": read_rel("game/NPC/Girls/Common/PartEventGirlHarrassmentReaction.rpy"),
    }

    for label_name, source in label_sources.items():
        assert re.search(r"label %s\([^\n]*\bresult=" % label_name, source)
        assert "return result" in source or label_name in ("ShowGirlSexHistory", "PartEventAfterHarrassment", "PartEventGirlHarrassmentReaction")


def test_kid_creation_has_one_python_api_without_unused_label_wrappers():
    source = read_rel("game/Utilities/General/Sex/KidsFunctions.rpy")

    assert "def CreateKid(MomName):" in source
    assert "label CreateKid" not in source
    assert "label KidsFunctions" not in source


def test_retired_shared_result_store_is_migration_only():
    gameplay = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    migration = read_rel("game/TractirSaveSync.rpy")

    assert re.search(r"\bResult\b", gameplay) is None
    assert 'globals().pop("Result", None)' in migration
    assert "def updateSave_V42():" in migration


def test_tavern_summary_uses_label_local_accumulators():
    source = read_rel("game/Utilities/General/Common/DisplayTavernEventsSummary.rpy")
    header = source.split("label DisplayTavernEventsSummary", 1)[1].split(":", 1)[0]

    assert 'today_events_summary=""' in header
    assert "TodayEventsSummary" not in source
    assert "TimePeriodEvents" not in source
