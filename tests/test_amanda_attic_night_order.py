from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THREADS = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
NIGHTS = (ROOT / "game/NPC/Girls/Amanda/AmandaAtticNightVisits.rpy").read_text(encoding="utf-8-sig")
MORNINGS = (ROOT / "game/NPC/Girls/Amanda/AmandaMorningWindowEvents.rpy").read_text(encoding="utf-8-sig")


def test_visit_order_uses_one_amanda_thread_and_existing_booklet_scene():
    assert '"amanda", "AtticNightVisits"' in THREADS
    assert '"story_amanda_attic_night_visit_0"' in THREADS
    assert '"story_amanda_attic_night_visit_1"' in THREADS
    assert '"#int(threads[\'amandaAtticNightVisits\'].num or 0) >= 1"' in THREADS
    assert '"#int(threads[\'amandaMorningWindowEpisode\'].num or 0) >= 1"' in THREADS
    assert '"#int(threads[\'melissaBatProblem\'].num or 0) >= 9"' in THREADS
    assert '"#not bool(player.tavern_management.breakfast.today)"' in THREADS


def test_first_night_uses_numbered_art_and_sets_next_morning_absence_once():
    first = NIGHTS.split("label story_amanda_attic_night_visit_0:", 1)[1].split(
        "label story_amanda_attic_night_visit_1:", 1
    )[0]
    for n in range(9):
        filename = f"amanda_visit_{n}{' ' if n == 3 else ''}.jpg"
        assert filename in first
        assert (ROOT / "game/images/player_room/amandaVisits" / filename).is_file()
    assert '_household_morning_state_key("amanda", current_game_day() + 1)' in first
    assert first.count("event_runtime.active_thread.advance()") == 1


def test_morning_and_second_night_award_only_the_requested_milestones():
    first_morning = MORNINGS.split("label story_amanda_room_morning_window_0:", 1)[1].split(
        "label story_amanda_room_morning_window_1:", 1
    )[0]
    second_night = NIGHTS.split("label story_amanda_attic_night_visit_1:", 1)[1]
    assert first_morning.count("Amanda.change_social(corruption_delta=1)") == 1
    assert second_night.count("Amanda.change_social(friend_delta=1, corruption_delta=1)") == 1
    assert second_night.count("event_runtime.active_thread.advance()") == 1
    for n in range(4):
        filename = f"amanda_visit_provoke_{n}.jpg"
        assert filename in second_night
        assert (ROOT / "game/images/player_room/amandaVisits" / filename).is_file()
