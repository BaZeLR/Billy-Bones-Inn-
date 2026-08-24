from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_tavern_work_trigger_returns_through_existing_ui_context():
    source = (ROOT / "game/Inn/TavernRandomEvents.rpy").read_text(encoding="utf-8-sig")
    block = source.split("label TavernWorkEventTrigger:", 1)[1]

    assert "call DisplayTavernEventShort" in block
    assert "call screen main_ui" not in block
    assert 'rooms.get(\"TavernMain\").state["event_ongoing"]' not in block
    assert "return True" in block


def test_amanda_liza_work_event_does_not_open_an_overlay_room_screen():
    source = (ROOT / "game/NPC/Girls/Amanda/AmandaLizaGloryEvents.rpy").read_text(encoding="utf-8-sig")
    block = source.split("label story_amanda_liza_talk_work_0:", 1)[1]

    assert "call EventAmandaLizettTalk(1)" in block
    assert "call screen main_ui" not in block
    assert 'rooms.get(\"TavernMain\").state["event_ongoing"]' not in block
    assert "return True" in block


def test_tavern_room_does_not_reenter_itself_after_called_work_event():
    source = (ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    gate = source.split('if ShouldDispatchTavernEvent:', 1)[1].split('$ GirlNameTS1 = "georgett"', 1)[0]

    assert 'call checkTriggers("TavernMain", "tavern_work", 0)' in gate
    assert "jump TavernMain" not in gate
