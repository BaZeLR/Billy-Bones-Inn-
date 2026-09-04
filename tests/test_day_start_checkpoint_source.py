from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_day_start_checkpoint_freezes_state_after_report_without_reinitializing():
    next_day = source("game/Utilities/Time/NextDay.rpy")
    body = next_day.split("label NextDay(retlocname, timepassed):", 1)[1].split("default next_day_runtime", 1)[0]

    report = body.index("call screen nextday_report_card_overlay")
    release = body.index("$ calendar_v2.time_advance_blocked = 0")
    clear_stack = body.index("$ renpy.set_return_stack([])")
    inspect_existing = body.index('$ _day_start_existing_name = str((renpy.slot_json("quick-1") or {})')
    new_day = body.index("if _day_start_existing_name != _day_start_save_name:")
    rotate = body.index('$ renpy.loadsave.cycle_saves("quick-", config.quicksave_slots)')
    save = body.index('$ renpy.save("quick-1"')
    room_entry = body.index("jump TavernMyRoom")
    checkpoint_tail = body[report:]

    assert report < release < clear_stack < inspect_existing < new_day < rotate < save < room_entry
    assert '$ _day_start_save_name = "Начало дня — " + calendar_v2.format_date_ru()' in checkpoint_tail
    assert 'if _day_start_existing_name != _day_start_save_name:' in checkpoint_tail
    assert '_nextday_return_label' not in checkpoint_tail
    assert 'extra_info=_day_start_save_name' in checkpoint_tail
    assert "include_screenshot=False" in checkpoint_tail
    assert 'renpy.save("day-1"' not in checkpoint_tail
    assert "InitGameNPCs" not in checkpoint_tail
    assert "NextDay_NewDayEvents" not in checkpoint_tail
    assert "CreateTavernEvents" not in checkpoint_tail


def test_day_start_checkpoint_loads_through_the_real_bedroom_entry():
    next_day = source("game/Utilities/Time/NextDay.rpy")
    bedroom = source("game/Inn/TavernMyRoom.rpy")
    screens = source("game/screens.rpy")

    checkpoint_tail = next_day.split('$ renpy.save("quick-1"', 1)[1].split("default next_day_runtime", 1)[0]
    bedroom_entry = bedroom.split("label TavernMyRoom:", 1)[1].split("label TavernMyRoomObjectMenu", 1)[0]

    assert "jump TavernMyRoom" in checkpoint_tail
    assert '$ rooms.enter("TavernMyRoom")' in bedroom_entry
    assert "tavern_my_room_scene_state()" in bedroom_entry
    assert "tavern_my_room_action_items()" in bedroom_entry
    assert "renpy.save(" not in bedroom_entry
    assert 'textbutton ui_tr("{#quick_page}Q") action FilePage("quick")' in screens


def test_legacy_day_page_does_not_construct_numeric_page_actions():
    screens = source("game/screens.rpy")
    page_buttons = screens.split("## Buttons to access other pages.", 1)[1].split("style page_label", 1)[0]

    assert 'if persistent._file_page == "day":\n                    text "Утро":' in screens
    assert 'if persistent._file_page == "day":' in page_buttons
    assert 'textbutton ui_tr("<") action FilePage("quick")' in page_buttons
    assert 'textbutton ui_tr(">") action FilePage(1)' in page_buttons


def test_checkpoint_repairs_owned_state_before_rebuilding_runtime_views():
    save_sync = source("game/TractirSaveSync.rpy")
    household = source("game/Utilities/General/NPC/HouseholdAI_ren.rpy")
    people_runtime = source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    events = source("game/Utilities/General/Events/events.rpy")
    main_layout = source("game/Utilities/General/Screens/main_layout.rpy")
    after_load = save_sync.split("label after_load:", 1)[1]

    schedule = after_load.index("$ npc_schedule_after_load()")
    story = after_load.index("$ initStoryEventRuntime(True)")
    ui = after_load.index("$ tractir_after_load_restore_ui()")
    rollback = after_load.index("$ renpy.block_rollback()")

    assert schedule < story < ui < rollback
    assert "$ updateSave()" not in after_load
    assert "config.after_load_callbacks.insert(0, updateSave)" in save_sync
    assert "household.repair()" in save_sync
    assert '"barber_appointments",' in household
    assert "def repair(self):" in household
    assert "config.after_load_callbacks.append(npc_schedule_after_load)" not in people_runtime
    assert "config.after_load_callbacks.append(_story_after_load_init)" not in events
    assert "config.after_load_callbacks.append(tractir_after_load_restore_ui)" not in main_layout
