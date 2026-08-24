from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Events" / "threads.rpy"
EVENTS_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Events" / "events.rpy"
CONDITIONS_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Events" / "conditions.rpy"
CONTENT_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"


def function_body(source, function_name):
    marker = f"    def {function_name}"
    start = source.index(marker)
    next_def = source.find("\n    def ", start + len(marker))
    if next_def == -1:
        return source[start:]
    return source[start:next_def]


def test_find_blocked_threads_is_bounded_not_open_while_loop():
    source = RUNTIME_PATH.read_text(encoding="utf-8-sig")
    body = function_body(source, "findBlockedThreads")

    assert "while True" not in body
    assert "max_passes = max(1, len(dict(threads_in or {})) + 1)" in body
    assert "for _pass_index in range(max_passes):" in body
    assert "next_signature == pending_signature" in body


def test_find_blocked_threads_clears_unresolved_pending_state():
    source = RUNTIME_PATH.read_text(encoding="utf-8-sig")
    body = function_body(source, "findBlockedThreads")

    assert 'getattr(thread_info, "blocked", None) is None' in body
    assert "thread_info.blocked = False" in body
    assert "False if row is None else row" in body


def test_story_event_runtime_monolith_keeps_only_content_definitions():
    source = CONTENT_PATH.read_text(encoding="utf-8-sig")

    assert "class StoryCondition" not in source
    assert "class Event(object)" not in source
    assert "class ThreadData(object)" not in source
    assert "def findAvailableEvents" not in source
    assert "def findBlockedThreads" not in source
    assert "label checkTriggers" not in source
    assert "label preEvent" not in source
    assert "define amandaThreadList" in source
    assert "label melissaClaraOverheard_0:" not in source
    assert "label story_clara_tavern_visit_bar_0:" not in source
    assert "label story_clara_melissa_room_visit_0:" not in source


def test_story_runtime_uses_familylife_style_split_files():
    conditions = CONDITIONS_PATH.read_text(encoding="utf-8-sig")
    threads = RUNTIME_PATH.read_text(encoding="utf-8-sig")
    events = EVENTS_PATH.read_text(encoding="utf-8-sig")

    assert "class StoryCondition(object)" in conditions
    assert "def makeConditions" in conditions
    assert "class ThreadData(object)" in threads
    assert "class ThreadInfo(object)" in threads
    assert "class Event(object)" in events
    assert "def findAvailableEvents" in events
    assert "label before_main_menu:" in events
    assert "$ initStoryEventRuntime(True)" in events
    assert "label checkTriggers(location, action, numpop=0):" in events
    assert "label preEvent(thread_name=None):" in events


def test_linear_thread_complete_advances_the_authoritative_stage_cursor():
    source = RUNTIME_PATH.read_text(encoding="utf-8-sig")
    linear_thread = source.split("class LThreadInfo(ThreadInfo):", 1)[1].split("class RThreadInfo(ThreadInfo):", 1)[0]
    complete = function_body(linear_thread, "complete")

    assert "self.done[self.num] = True" in complete
    assert "self.num += 1" in complete
    assert "if self.num >= self.data.length:" in complete
    assert "self.completed = True" in complete


def test_check_triggers_uses_cached_events_and_marks_event_once_per_day():
    source = EVENTS_PATH.read_text(encoding="utf-8-sig")
    body = source.split("label checkTriggers(location, action, numpop=0):", 1)[1].split("\n\nlabel ", 1)[0]

    assert "$ findAvailableEvents(False)" in body
    assert "$ findAvailableEvents(True)" not in body
    assert "$ story_event_mark_fired_today(evt)" in body
    assert body.index("$ story_event_mark_fired_today(evt)") < body.index("jump expression evt.target")


def test_story_events_are_blocked_after_firing_today():
    source = EVENTS_PATH.read_text(encoding="utf-8-sig")
    body = function_body(source, "canTrigger")

    assert "story_event_fired_today(self)" in body
    assert 'getattr(self, "repeatable", False)' in body
    assert "return False" in body
    assert "def story_event_reset_fired_today_if_needed" in source
    assert "event_runtime.fired_keys_today = []" in source
    assert "event_runtime.fired_day or -1" not in source
    assert "fired_day_value if fired_day_value is not None else -1" in source
