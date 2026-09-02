from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"
ACTIONS_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Common" / "Actions.rpy"


def game_sources():
    for path in GAME_ROOT.rglob("*.rpy"):
        yield path, path.read_text(encoding="utf-8-sig")


def test_no_abstract_examine_action_label_or_factory():
    source = ACTIONS_PATH.read_text(encoding="utf-8-sig")

    assert '"examine":' not in source
    assert "def make_examine_action" not in source
    assert "\nlabel Examine" not in source


def test_no_object_action_targets_abstract_examine_label():
    offenders = []
    for path, source in game_sources():
        if 'target="Examine"' in source or "target='Examine'" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_no_refresh_or_apply_ui_wrappers():
    source = ACTIONS_PATH.read_text(encoding="utf-8-sig")

    assert "renpy.store" not in source
    assert "import renpy.store" not in source
    assert "label RefreshCurrentActionMenu" not in source
    assert "label ApplyActionResultToUI" not in source
    assert "ROOM_ACTION_REFRESH" not in source
    assert "_action_refresh_target_labels" not in source
    assert "call RefreshCurrentActionMenu" not in source
    assert "call ApplyActionResultToUI" not in source


def test_no_generic_scene_action_panel_wrapper():
    offenders = []
    for path, source in game_sources():
        if "SceneActionPanel" in source or "scene_panel_" in source or "main_ui_set_action_panel" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_no_main_ui_label_call_wrapper():
    offenders = []
    for path, source in game_sources():
        if "main_ui_call_label" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_no_active_main_ui_restore_actions():
    offenders = []
    for path, source in game_sources():
        if "Function(main_ui_restore_room_scene_state)" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))
        if "$ main_ui_restore_room_scene_state()" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_no_removed_becky_kitchen_visit_wrapper_name():
    kitchen_source = (GAME_ROOT / "Inn" / "TavernKitchen.rpy").read_text(encoding="utf-8-sig")
    breakfast_source = (GAME_ROOT / "Inn" / "TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")

    assert "becky_kitchen_visit_active" not in kitchen_source
    assert 'people.location("becky")' in kitchen_source
    assert "npc_schedule_becky_sandra_kitchen_visit_active()" not in kitchen_source
    condition_body = breakfast_source.split("def npc_schedule_becky_sandra_kitchen_visit_active():", 1)[1].split("\n    def ", 1)[0]
    assert 'getLocation("sandra")' not in condition_body


def test_hunter_club_open_through_late_day_minutes():
    source = (GAME_ROOT / "Town" / "HunterClub.rpy").read_text(encoding="utf-8-sig")

    assert 'start="08:00"' in source
    assert 'end="18:59"' in source
    assert "time_slots=[0, 1, 2, 3]" not in source


def test_room_schedules_use_clock_not_slots():
    template_source = (GAME_ROOT / "Utilities" / "General" / "Classes" / "RoomTemplate.rpy").read_text(encoding="utf-8-sig")
    offenders = []

    assert "time_slots" not in template_source
    assert "calendar_v2.clock_minutes()" not in template_source
    assert "calendar_v2.hour" in template_source
    assert "calendar_v2.minute" in template_source

    for path, source in game_sources():
        if "RoomSchedule(" in source and "time_slots=" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_only_tavern_main_owns_tavern_open_hours_schedule():
    offenders = []
    for path in (GAME_ROOT / "Inn").rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        if "schedule=RoomSchedule(" in source and path.name != "TavernMain.rpy":
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_sleep_gate_uses_clock_not_display_slot():
    source = ACTIONS_PATH.read_text(encoding="utf-8-sig")
    body = source.split("def _player_can_sleep_now():", 1)[1].split("\n    def ", 1)[0]

    assert "calendar_v2.sync_state()" not in body
    assert "current_hour = int(calendar_v2.hour or 0)" in body
    assert "current_hour >= 20 or current_hour < 6" in body
    assert "time_slot" not in body
    assert "int(time" not in body


def test_room_open_checks_call_schedule_without_time_slot_arguments():
    offenders = []
    for path, source in game_sources():
        if ".is_open(week, time)" in source:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []
