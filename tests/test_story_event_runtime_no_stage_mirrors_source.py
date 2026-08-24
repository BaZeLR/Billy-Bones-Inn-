from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_story_event_runtime_does_not_copy_thread_or_active_event_state():
    state = _source("game/Utilities/General/Events/EventRuntimeState.rpy")
    events = _source("game/Utilities/General/Events/events.rpy")

    assert "self.active_thread = None" in state
    assert "self.active_event" not in state + events
    assert "self.story_events" not in state + events
    assert "self.random_events" not in state + events
    assert "self.thread_levels" not in state + events


def test_thread_num_remains_the_ordered_story_stage_authority():
    threads = _source("game/Utilities/General/Events/threads.rpy")

    assert "self.num = 0" in threads
    assert "self.num += 1" in threads
    assert "def advance(self):" in threads


def test_paid_scene_procedures_do_not_create_a_parallel_runtime_object():
    source = _source("game/Utilities/General/Classes/ModuleRuntime.rpy")

    assert "label BeginPaidSexModule(" in source
    assert "label FinishPaidSexModule(" in source
    assert "class ModuleRuntimeState" not in source
    assert "default module_runtime" not in source
    assert "self.actor" not in source
    assert "self.actor_location" not in source
    assert "self.picture_path" not in source
    assert 'hasattr(_module_actor_info, "set_arousal")' not in source
    assert '_module_actor_info.set_arousal(_module_actor_info.sex_stat("PussyWetStart", 0))' in source
