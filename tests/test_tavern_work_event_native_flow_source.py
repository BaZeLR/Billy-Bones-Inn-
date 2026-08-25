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


def test_amanda_liza_event_owns_event_title_text_and_native_choices():
    event = (ROOT / "game/NPC/Girls/Amanda/EventAmandaLizettTalk.rpy").read_text(encoding="utf-8-sig")
    followup = (ROOT / "game/NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy").read_text(encoding="utf-8-sig")
    eyewitness = event.rsplit("if eyewitness > 0:", 1)[1].split('\n    $ result = ""', 1)[0]

    assert 'main_ui_begin_native_scene_state("Событие: Аманда и Лизетта")' in eyewitness
    assert "$ scene_runtime.text = result" in eyewitness
    assert "$ scene_runtime.location_text = result" in eyewitness
    assert '"[result]"' not in eyewitness
    assert "menu:" in eyewitness
    assert "main_ui_end_native_scene_state()" in eyewitness
    assert "$ scene_runtime.text = result" in followup
    assert '"[result]"' not in followup


def test_tavern_room_does_not_reenter_itself_after_called_work_event():
    source = (ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    gate = source.split('if ShouldDispatchTavernEvent:', 1)[1].split('$ GirlNameTS1 = "georgett"', 1)[0]

    assert 'call checkTriggers("TavernMain", "tavern_work", 0)' in gate
    assert "if _return:" not in gate
    assert "return" not in gate
    assert "jump TavernMain" not in gate


def test_tavern_room_establishes_scene_context_before_work_event():
    source = (ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    entry = source.split("label TavernMain:", 1)[1].split("# Determine if tavern is closed", 1)[0]

    assert '$ main_ui_runtime.mode = "scene"' in entry
    assert '$ main_ui_runtime.selected_char = ""' in entry
    assert '$ main_ui_runtime.talk_picture = ""' in entry
    assert '$ main_ui_runtime.action_title = "Действия в трактире"' in entry
    assert "main_ui_runtime.clear_contexts()" in entry
