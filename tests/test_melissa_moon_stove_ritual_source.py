from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_three_nights_use_window_shed_and_explicit_stove_action():
    events = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    thread = events.split('LThreadData(0, "melissa", "MoonStoveRitual"', 1)[1].split(
        'LThreadData(0, "melissa", "MoonNoiseRepeat"', 1
    )[0]

    assert thread.index('"story_melissa_moon_window_clue_0"') < thread.index(
        '"story_melissa_moon_stove_wait_1"'
    )
    assert thread.index('"story_melissa_moon_shed_check_1"') < thread.index('"story_melissa_moon_second_window_2"') < thread.index('"story_melissa_moon_shed_conversation_3"') < thread.index('"story_melissa_moon_stove_wait_1"')
    assert '"story_melissa_moon_room_protection_2"' not in thread
    assert '"TavernMyRoom", "window_look"' in thread
    assert '"ShedRuinedChamber", "stove_hide_wait"' in thread
    assert "#17 <= int(calendar_v2.day or 0) <= 18" in thread
    assert "#18 <= int(calendar_v2.day or 0) <= 19" in thread
    assert "#19 <= int(calendar_v2.day or 0) <= 20" in thread
    assert "player.equipment.hand" not in thread
    assert "player.item_count('fur_glove_001')" not in thread
    assert '"TavernMyRoom", "bedtime"' in thread
    conditions = source("game/Utilities/General/Events/conditions.rpy")
    assert '"moon_stove_npc_available": moon_stove_npc_available' in conditions
    assert '"relationship_anger": relationship_anger' in conditions


def test_glove_is_wearable_and_can_be_cut_from_existing_fur_goods():
    items = source("game/Items/Shops/HunterClubItems.rpy")
    card = source("game/Utilities/General/Screens/PlayerCard.rpy")
    player = source("game/Utilities/General/Player/Player.rpy")

    assert 'object_id="fur_glove_001"' in items
    assert 'define 4 FurGloveItem = GameItem(' in items
    assert items.count('object_id="fur_glove_001"') == 1
    assert '"wear_slot": "hand"' in items
    assert 'picture="images/tavern/backyard/shed/ghostEvent/fur_glove.png"' in items
    assert '"warm_fur_cloak_001", "fur_bedroll_001"' in card
    assert 'label PlayerCardMakeFurGlove' in card
    assert 'self.hand = ""' in player


def test_old_stove_is_reachable_after_shed_renovation():
    shed = source("game/Inn/Shed.rpy")
    chamber = source("game/Inn/ShedRuinedChamber.rpy")
    events = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")

    assert 'return not rooms.get("ShedRuinedChamber").is_hidden' in shed
    assert 'if rooms.get("ShedRuinedChamber").is_hidden:' in chamber
    assert '"story_melissa_moon_old_stove_4"' not in events
    assert 'call checkTriggers("ShedRuinedChamber", "stove_hide_wait", 0)' in source("game/Inn/TavernRenovations.rpy")


def test_ritual_art_exists_for_window_conversation_each_visitor_and_room():
    art = ROOT / "game/images/tavern/backyard/shed/ghostEvent"
    for name in ("window_clue.png", "stove_conversation.png", "night_visit.png", "fur_glove.png"):
        assert (art / name).is_file()
    for name in ("amanda_enters_shed.png", "amanda_stove.png", "amanda_stove_over_melissa_shoulder.png", "amanda_surprised_closeup.png", "amanda_laughing_stove_closeup.png"):
        assert (art / "amanda" / name).is_file()
    for name in ("melissa_stove.png", "melissa_stove_over_amanda_shoulder.png", "melissa_surprised_closeup.png", "melissa_laughing_stove_closeup.png"):
        assert (art / "melissa" / name).is_file()

    scene = source("game/NPC/Girls/Melissa/MelissaMoonNoise.rpy").split(
        "label story_melissa_moon_window_clue_0:", 1
    )[1].split("label story_melissa_moon_shed_check_1:", 1)[0]
    assert 'vscene "images/player_room/windowAmand.png"' in scene
    assert 'ghostEvent/window_clue.png' not in scene
    assert 'amanda/amanda_enters_shed.png' in scene

    stove_scene = source("game/NPC/Girls/Melissa/MelissaMoonNoise.rpy").split(
        "label story_melissa_moon_stove_wait_1:", 1
    )[1].split("label story_melissa_moon_stove_not_needed:", 1)[0]
    assert stove_scene.index('vscene "images/tavern/backyard/shed/ghostEvent/stove_conversation.png"') < stove_scene.index(
        'vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_stove.png"'
    ) < stove_scene.index('vscene "images/tavern/backyard/shed/ghostEvent/melissa/melissa_stove.png"')



def test_branch_media_and_user_text():
    scenes = source("game/NPC/Girls/Melissa/MelissaMoonNoise.rpy")
    second = scenes.split("label story_melissa_moon_shed_conversation_3:", 1)[1].split("label story_melissa_moon_stove_wait_1:", 1)[0]
    assert second.count("vscene ") == 1
    assert "TrialF" not in second
    assert second.index("Сквозняк протискивается") < second.index("Это ты?")
    stove = scenes.split("label story_melissa_moon_stove_wait_1:", 1)[1].split("label story_melissa_moon_stove_not_needed:", 1)[0]
    no_glove = stove.split("    else:\n", 1)[1].split("    python:\n", 1)[0]
    for forbidden in ("TrialF", "fur_touch", "amanda_stove.png", "melissa_stove.png"):
        assert forbidden not in no_glove
    assert "1440 - calendar_v2.clock_minutes()" in stove
    assert "NextDay" not in stove
    assert "ritual_result is None" in stove
    for supplied in ("Вас просто распирает от любопытсва", "чудом не были замечены", "Че совсем дура,вааще...блин!", "всех своих друзей извращенцев", "королева сранделей"):
        assert supplied in scenes
    assert "amanda_stove_front.png" not in scenes
