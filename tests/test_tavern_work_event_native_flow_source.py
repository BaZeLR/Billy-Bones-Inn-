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


def test_room_entry_and_bar_observation_share_the_work_event_gate():
    room = (ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    bar = (ROOT / "game/Inn/TavernMainBar001.rpy").read_text(encoding="utf-8-sig")
    runtime = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")

    assert 'call RoomEnterEventGate(rooms.current_code, False)' in room
    assert 'action_id="observe_hall"' in bar
    assert 'target="TavernMainBarObserveHall"' in bar
    observe = bar.split("label TavernMainBarObserveHall:", 1)[1].split("label TavernMainBarInviteMenu:", 1)[0]
    assert 'call RoomEnterEventGate("TavernMain", False)' in observe
    assert "tavern_main_routine_visual_data()" in observe
    assert "calendar_v2.advance_minutes(60)" in observe
    assert "event_runtime.tavern_work_events" not in observe
    assert "DisplayTavernEventShort" not in observe
    assert '"TavernMain",\n            "enter",\n            200,\n            True,' in runtime


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
