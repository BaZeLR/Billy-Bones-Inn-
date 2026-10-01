from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_window_clue_precedes_midnight_stove_and_room_visit():
    events = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    thread = events.split('LThreadData(0, "melissa", "MoonStoveRitual"', 1)[1].split(
        'LThreadData(0, "melissa", "MoonNoiseRepeat"', 1
    )[0]

    assert thread.index('"story_melissa_moon_window_clue_0"') < thread.index(
        '"story_melissa_moon_stove_wait_1"'
    ) < thread.index('"story_melissa_moon_room_protection_2"')
    assert '"TavernMyRoom", "window_look"' in thread
    assert '"ShedRuinedChamber", "enter"' in thread
    assert "#17 <= int(calendar_v2.day or 0) <= 18" in thread
    assert "#18 <= int(calendar_v2.day or 0) <= 19" in thread
    assert "player.equipment.hand" in thread
    assert '"TavernMyRoom", "enter"' in thread


def test_glove_is_wearable_and_can_be_cut_from_existing_fur_goods():
    items = source("game/Items/Shops/HunterClubItems.rpy")
    card = source("game/Utilities/General/Screens/PlayerCard.rpy")
    player = source("game/Utilities/General/Player/Player.rpy")

    assert 'object_id="fur_glove_001"' in items
    assert '"wear_slot": "hand"' in items
    assert '"warm_fur_cloak_001", "fur_bedroll_001"' in card
    assert 'label PlayerCardMakeFurGlove' in card
    assert 'self.hand = ""' in player


def test_old_stove_is_reachable_after_shed_renovation():
    shed = source("game/Inn/Shed.rpy")
    chamber = source("game/Inn/ShedRuinedChamber.rpy")
    events = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")

    assert 'return not rooms.get("ShedRuinedChamber").is_hidden' in shed
    assert 'if rooms.get("ShedRuinedChamber").is_hidden:' in chamber
    old_stove = events.split('"story_melissa_moon_old_stove_4"', 1)[1].split(
        'LThreadData(0, "melissa", "MoonStoveRitual"', 1
    )[0]
    assert "tavern.renovation_complete('shed')" not in old_stove


def test_ritual_art_exists_for_window_each_visitor_and_room():
    art = ROOT / "game/images/tavern/backyard/shed/moon_ritual"
    for name in ("window_clue.png", "amanda_stove.png", "melissa_stove.png", "night_visit.png", "fur_glove.png"):
        assert (art / name).is_file()
