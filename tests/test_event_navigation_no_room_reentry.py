from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_melissa_booklet_returns_to_its_object_without_location_jump_protocol():
    event = read("game/NPC/Girls/Melissa/MelissaEvents.rpy")
    item = read("game/Items/Resources/MelissaBookletItem.rpy")
    block = event.split("label ReadMelissaBooklet:", 1)[1].split("\nlabel ", 1)[0]

    assert "return_to_location" not in event
    assert "jump expression CurLoc" not in block
    assert 'call TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001", True)' in block
    assert 'target="ReadMelissaBooklet"' in item
    assert "args=(False,)" not in item


def test_unused_button_to_current_location_dispatcher_is_removed():
    source = read("game/Utilities/General/Common/OtherFunctionsCode.rpy")

    assert "ButtonToCurloc" not in source
    assert "jump expression CurLoc" not in source


def test_clara_paintings_event_returns_to_trigger_caller_without_room_reentry():
    source = read("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy")
    block = source.split("label story_clara_paintings_evening_peek_8:", 1)[1].split("\nlabel ", 1)[0]

    assert "jump TavernMelissaRoom" not in block
    assert block.rstrip().endswith("return True")


def test_same_location_events_return_to_their_callers_without_room_reentry():
    cases = (
        ("game/Town/Market/MarketPlace.rpy", "story_city_blind_pirate_fall_0", "jump MarketPlace", "return True"),
        ("game/NPC/Girls/Melissa/MelissaEvents.rpy", "story_melissa_werecat_rumor_0", "jump HunterClub", "return True"),
        ("game/Town/Church/Church.rpy", "becky_church_talk", "jump Church", "return"),
    )
    for relative_path, label_name, forbidden, ending in cases:
        source = read(relative_path)
        block = source.split(f"label {label_name}", 1)[1].split("\nlabel ", 1)[0]
        assert forbidden not in block
        assert block.rstrip().endswith(ending)


def test_room_entry_uses_iterative_main_ui_owner_without_recursive_reentry():
    source = read("game/Town/PortStreets.rpy")
    block = source.split("label PortStreets:", 1)[1].split("\nlabel ", 1)[0]

    assert "call screen main_ui\n    jump PortStreets" not in block
    assert "while True:\n        call screen main_ui" in block


def test_mongol_no_money_discount_exits_talk_without_reentering_marketplace():
    source = read("game/NPC/Secondary/IntMongolTalk.rpy")
    branch = source.split("if player.economy.money < Mongol.horse_price - 200:", 1)[1].split("else:", 1)[0]

    assert "jump MarketPlace" not in branch
    assert "main_ui_end_talk_state()" in branch
    assert branch.rstrip().endswith("return")
