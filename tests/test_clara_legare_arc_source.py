from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def label_block(text, name):
    return text.split("label %s:" % name, 1)[1].split("\nlabel ", 1)[0]


def test_clara_path_keeps_the_requested_story_order_in_one_thread():
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    block = runtime.split('LThreadData(1, "clara", "PaintingsPath"', 1)[1].split(
        'LThreadData(1, "clara", "ForestSofa"', 1
    )[0]
    targets = (
        "story_clara_paintings_legare_secret_date_7",
        "story_clara_paintings_secret_date_7",
        "story_clara_paintings_barber_closed_8",
        "story_clara_paintings_luisa_report_9",
        "story_clara_paintings_legare_warning_11",
        "story_clara_paintings_zimmer_wine_10",
        "story_clara_paintings_zimmer_puzzle_11",
        "story_clara_paintings_sergio_followup_12",
        "story_clara_paintings_dance_exposure_15",
        "story_clara_paintings_amanda_punishment_16",
        "story_clara_paintings_winery_rescue_17",
        "story_clara_paintings_confession_14",
        "story_clara_paintings_ointment_15",
    )
    positions = [block.index(target) for target in targets]
    assert positions == sorted(positions)
    assert '"FridayDance",\n            "clara_legare_expose"' in block


def test_both_barber_discoveries_show_clarissa_watching_and_two_closeups():
    text = source("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy")
    for name in (
        "story_clara_paintings_legare_secret_date_7",
        "story_clara_paintings_secret_date_7",
    ):
        block = label_block(text, name)
        assert 'images/clara/secret_date/clarissa_watches_window.png' in block
        assert 'images/clara/secret_date/clarissa_laughing_closeup.png' in block
        assert 'images/clara/secret_date/clarissa_blushing_closeup.png' in block
        assert block.count("event_runtime.active_thread.advance()") == 1


def test_dance_exposure_rescue_and_residency_share_the_clara_thread():
    dance = source("game/NPC/Girls/Amanda/IntAmandaDance.rpy")
    story = source("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy")
    clara = source("game/NPC/Girls/Clara/InitClara.rpy")
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")

    assert 'story_event_available("FridayDance", "clara_legare_expose")' in dance
    assert 'call checkTriggers("FridayDance", "clara_legare_expose", 0)' in dance
    assert 'fight_begin("legare", 1, "FridayDance"' in label_block(
        story, "story_clara_paintings_dance_exposure_15"
    )
    rescue = label_block(story, "story_clara_paintings_winery_rescue_17")
    assert "На этот раз драки не происходит" in rescue
    assert "остаётся членом команды" in rescue
    assert "int(thread_info.num or 0) >= 18" in clara
    revenge = runtime.split('LThreadData(0, "clara", "LegareRevenge"', 1)[1].split(
        'LThreadData(0, "clara", "TavernEducation"', 1
    )[0]
    assert "int(threads['claraPaintingsPath'].num or 0) >= 18" in revenge


def test_v113_maps_old_progress_by_story_meaning():
    migration = source("game/TractirSaveSync.rpy")
    assert "define currentVersion = 114" in migration
    block = migration.split("def updateSave_V113():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]
    for mapping in ("8: 9", "10: 11", "11: 13", "13: 15", "14: 18", "15: 19"):
        assert mapping in block
    assert "paintings.day = old_day" in block
    assert "complete_at_end=True" in block
