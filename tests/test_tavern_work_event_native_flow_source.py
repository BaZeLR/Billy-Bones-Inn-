from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_tavern_work_trigger_returns_through_existing_ui_context():
    source = (ROOT / "game/Inn/TavernRandomEvents.rpy").read_text(encoding="utf-8-sig")
    block = source.split("label TavernWorkEventTrigger:", 1)[1]

    assert "call DisplayTavernEventShort" in block
    assert "call screen main_ui" not in block
    assert 'rooms.get(\"TavernMain\").state["event_ongoing"]' not in block
    assert "return True" in block


def test_amanda_liza_work_event_uses_the_daily_plan_directly():
    source = (ROOT / "game/Inn/TavernRandomEvents.rpy").read_text(encoding="utf-8-sig")

    assert 'TavernWorkEventDefinition("AmandaLizaTalk", "tavern_story", "EventAmandaLizettTalk"' in source
    assert "story_amanda_liza_talk_work_0" not in source


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


def test_bar_stand_triggers_work_event_and_returns_to_its_object_menu():
    room = (ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    bar = (ROOT / "game/Inn/TavernMainBar001.rpy").read_text(encoding="utf-8-sig")
    listen = bar.split("label TavernMainBarListenEvent:", 1)[1]

    assert 'call checkTriggers("TavernMain", "tavern_work", 0)' not in room
    assert 'if tavern_work_planned_for("", "TavernMain", calendar_v2.time_slot()):' in listen
    assert 'call checkTriggers("TavernMain", "tavern_work", 0)' in listen
    assert 'call TavernMainObjectMenu("bar_001")' in listen
    assert "jump TavernMain" not in listen


def test_tavern_room_establishes_scene_context_before_work_event():
    source = (ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    entry = source.split("label TavernMain:", 1)[1].split("# Determine if tavern is closed", 1)[0]

    assert '$ main_ui_runtime.mode = "scene"' in entry
    assert '$ main_ui_runtime.selected_char = ""' in entry
    assert '$ main_ui_runtime.talk_picture = ""' in entry
    assert '$ main_ui_runtime.action_title = "Действия в трактире"' in entry
    assert "main_ui_runtime.clear_contexts()" in entry


def test_small_fight_owns_text_and_native_choices_until_event_completion():
    source = (ROOT / "game/Utilities/Fight/EventFightSmall.rpy").read_text(encoding="utf-8-sig")
    witnessed = source.split("if eyewitness > 0:", 1)[1].split("else:", 1)[0]
    finish = source.split("label EventFightSmallFinish", 1)[1]

    assert 'main_ui_begin_native_scene_state("Событие в трактире")' in witnessed
    assert "$ scene_runtime.text = CurEventDesc" in witnessed
    assert "menu:" in witnessed
    assert "main_ui_end_native_scene_state()" in witnessed
    assert '"[extra_text]"' not in finish
    assert '"[PhraseEnd1EFS]"' not in finish
    assert '"Вернуться к своим делам":' in finish
