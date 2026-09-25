from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_nostar_route_has_one_ordered_thread_and_existing_sofa_owner():
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    block = runtime.split('LThreadData(0, "nostar", "RosarioSofa"', 1)[1].split(
        'LThreadData(0, "city", "BlindPirateFall"', 1
    )[0]
    stages = (
        "story_hordus_nostar_sofa_lead_0",
        "story_nostar_rosario_riddle_1",
        "story_nostar_sofa_sale_2",
        "story_nostar_sofa_delivery_3",
    )
    assert all(block.count(stage) == 1 for stage in stages)
    assert [block.index(stage) for stage in stages] == sorted(block.index(stage) for stage in stages)
    assert "#int(threads['claraPaintingsPath'].num or 0) >= 12" in block
    assert "#not Sofa.installed" in block
    assert "#Sofa.installed" in block
    assert source("game/NPC/Secondary/IntNostarTalk.rpy").count("$ Sofa.installed = True") == 1


def test_nobility_route_and_nostar_schedule_are_visible_after_load():
    artisans = source("game/Town/Arts/ArtisansQuarter.rpy")
    quarter = source("game/Town/NobilityQuarters.rpy")
    house = source("game/Town/NostarHouse.rpy")
    person = source("game/NPC/Secondary/InitNostar.rpy")
    migration = source("game/TractirSaveSync.rpy")
    assert 'target="NobilityQuarters"' in artisans
    assert 'target="NostarHouse"' in quarter
    assert 'target="NobilityQuarters"' in house
    assert 'start="09:00"' in house and 'end="20:59"' in house
    assert 'start_hour=9' in person and 'end_hour=21' in person
    assert 'people.register(NostarStaticData, Nostar)' in migration
    assert 'artisans.exits.append(' in migration
    assert 'initThreads()' in migration.split('def updateSave_V103():', 1)[1]


def test_riddle_has_all_clues_and_right_answer_sells_for_1200():
    story = source("game/NPC/Secondary/IntNostarTalk.rpy")
    assert 'define NOSTAR_ROSARIO_ANSWER = "tiefling"' in story
    assert 'define NOSTAR_ROSARIO_PRICE = 1200' in story
    for number in range(1, 15):
        assert f"{number}. " in story
    assert 'player.spend_money(NOSTAR_ROSARIO_PRICE)' in story
    assert '"images/nostar/drawing_room_without_sofa.png"' in story
    for asset in (
        "nobility_quarters.png",
        "drawing_room.png",
        "drawing_room_without_sofa.png",
        "lady_nostar.png",
        "lady_nostar_after_sale.png",
    ):
        assert (ROOT / "game/images/nostar" / asset).is_file()


def test_renovated_yard_scenes_are_event_owned_and_images_exist():
    backyard = source("game/Inn/Backyard.rpy")
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    breakfast = source("game/Inn/TavernKitchenBreakfast.rpy")
    achievements = source("game/Utilities/General/Common/AchievementsEndings.rpy")
    assert 'ObjectAction(action_id="use_toilet"' in backyard
    assert 'label story_backyard_toilet_first_use:' in backyard
    assert '"Backyard", "toilet_first_use"' in backyard
    assert '"BackyardToiletFirstUse"' in runtime
    assert '"ShedRenovationBreakfast"' in runtime
    assert 'label story_shed_renovation_breakfast:' in breakfast
    assert '"shit_with_comfort"' in achievements
    assert 'Saved rooms keep object ids' in source("game/TractirSaveSync.rpy")
    for asset in (
        "backyard_renewal_day.png",
        "backyard_renewal_night.png",
        "backyard_renewal_rain.png",
        "backyard_toilet_renewed_inside.png",
    ):
        assert (ROOT / "game/images/tavern/backyard" / asset).is_file()
