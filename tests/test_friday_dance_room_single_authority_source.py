import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
FRIDAY_DANCE = GAME / "Town" / "Market" / "FridayDance.rpy"
SAVE_SYNC = GAME / "TractirSaveSync.rpy"
AMANDA_SCHEDULE = GAME / "NPC" / "Schedules" / "amanda.json"
BECKY_SCHEDULE = GAME / "NPC" / "Schedules" / "becky.json"
AMANDA_DANCE_MODEL = GAME / "NPC" / "Girls" / "Amanda" / "AmandaDanceEventModel.rpy"
BECKY_DANCE_MODEL = GAME / "NPC" / "Girls" / "Becky" / "BeckyDanceEventModel.rpy"
AMANDA_INFO = GAME / "NPC" / "Girls" / "Amanda" / "InitAmanda.rpy"
BECKY_INFO = GAME / "NPC" / "Girls" / "Becky" / "InitBecky.rpy"
ROOM_TEMPLATE = GAME / "Utilities" / "General" / "Classes" / "RoomTemplate.rpy"
PEOPLE_RUNTIME = GAME / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"


def _live_runtime_source():
    return "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in GAME.rglob("*.rpy")
        if path != SAVE_SYNC
    )


def test_friday_dance_room_owns_venue_and_session_state():
    source = FRIDAY_DANCE.read_text(encoding="utf-8-sig")

    assert "class FridayDanceRoom(Room):" in source
    for field, default in (
        ("dance_count", "0"),
        ("becky_home_invited", "False"),
        ("step", "0"),
        ("hands", '""'),
        ("kiss", "0"),
        ("tits", "0"),
        ("max_step", "6"),
    ):
        assert 'self.state.setdefault("%s", %s)' % (field, default) in source
        assert "def %s(self):" % field in source

    assert 'schedule=RoomSchedule(weekdays=[5], start="18:00", end="21:59")' in source
    assert "return self.is_open() and self.dance_count < 5" in source


def test_friday_dance_has_no_parallel_runtime_authority_or_schedule_wrapper():
    runtime = _live_runtime_source()

    for retired_name in (
        "DanceStep",
        "HandsDance",
        "KissDance",
        "TitsDance",
        "DanceMaxIAD",
        "DanceMaxIBD",
        "friday_dance_count",
        "friday_dance_slot_is_active",
        "friday_dance_market_entry_is_active",
    ):
        assert retired_name not in runtime

    assert "def slot_is_active" not in runtime
    assert 'rooms.get("FridayDance").state[' not in runtime


def test_friday_dance_call_sites_use_the_room_instance_directly():
    amanda = (GAME / "NPC" / "Girls" / "Amanda" / "IntAmandaDance.rpy").read_text(encoding="utf-8-sig")
    becky = (GAME / "NPC" / "Girls" / "Becky" / "IntBeckyDance.rpy").read_text(encoding="utf-8-sig")
    market = (GAME / "Town" / "Market" / "MarketPlace.rpy").read_text(encoding="utf-8-sig")

    for source in (amanda, becky):
        assert 'rooms.get("FridayDance").dance_count' in source
        assert 'rooms.get("FridayDance").step' in source
        assert 'rooms.get("FridayDance").max_step' in source

    assert 'rooms.get("FridayDance").market_entry_is_active()' in market


def test_friday_dance_public_menu_loops_without_reentering_the_room_label():
    source = FRIDAY_DANCE.read_text(encoding="utf-8-sig")

    assert source.count('rooms.enter("FridayDance")') == 1
    assert "while True:" in source
    assert "jump FridayDance" not in source
    assert 'call checkTriggers("FridayDance", "enter", 0)' in source
    assert source.index('call checkTriggers("FridayDance", "enter", 0)') < source.index("while True:")
    assert 'story_event_available("FridayDance", "amanda_dance_mc")' in source
    assert 'story_event_available("FridayDance", "becky_dance_mc")' in source
    assert 'rooms.get("FridayDance").step = 0' in source
    assert "python hide:" in source
    for retired_name in ("GirlsCounter", "CurrentActions", "AddDancePhraseTmp"):
        assert retired_name not in source


def test_amanda_mc_dance_owns_its_scene_instead_of_showing_market_description():
    source = (GAME / "NPC" / "Girls" / "Amanda" / "IntAmandaDance.rpy").read_text(encoding="utf-8-sig")
    scene = source.split("label story_amanda_friday_dance_mc_0:", 1)[1].split("label story_amanda_friday_dance_legare_0:", 1)[0]

    assert '$ main_ui_begin_native_scene_state("Танец с Амандой")' in scene
    assert '$ scene_runtime.text = ""' in scene
    assert '$ scene_runtime.location_text = ""' in scene
    assert "$ main_ui_end_native_scene_state()" in scene


def test_amanda_alber_dances_own_their_scenes_and_images():
    dance_source = (GAME / "NPC" / "Girls" / "Amanda" / "IntAmandaDance.rpy").read_text(encoding="utf-8-sig")
    sequence_source = (GAME / "NPC" / "Girls" / "Amanda" / "AmandaLegareDanceSequence.rpy").read_text(encoding="utf-8-sig")
    repeatable_scene = dance_source.split("label story_amanda_friday_dance_legare_0:", 1)[1].split("label IntAmandaDance", 1)[0]

    for scene in [repeatable_scene] + [
        sequence_source.split("label story_amanda_legare_dance_{}:".format(stage), 1)[1].split(
            "label story_amanda_legare_dance_{}:".format(stage + 1) if stage < 4 else "label AmandaLegareDanceSequence",
            1,
        )[0]
        for stage in range(5)
    ]:
        assert "main_ui_begin_native_scene_state(" in scene
        assert '$ scene_runtime.text = ""' in scene
        assert '$ scene_runtime.location_text = ""' in scene
        assert "$ main_ui_end_native_scene_state()" in scene

    assert 'call ShowImage("amanda", "dance", "legare_step_0")' in repeatable_scene
    assert sequence_source.count('call ShowImage("amanda", "dance", "legare_step_0")') == 3


def test_friday_dance_featured_partners_follow_the_venue_schedule():
    amanda_rows = json.loads(AMANDA_SCHEDULE.read_text(encoding="utf-8-sig"))["entries"]
    becky_rows = json.loads(BECKY_SCHEDULE.read_text(encoding="utf-8-sig"))["entries"]
    amanda_dance = next(row for row in amanda_rows if row.get("label") == "friday_dance")
    becky_dance = next(row for row in becky_rows if row.get("label") == "friday_dance")

    for row in (amanda_dance, becky_dance):
        assert row["location"] == "FridayDance"
        assert row["follows_room_schedule"] is True
        assert "weekdays" not in row
        assert "start" not in row
        assert "end" not in row
        assert "location_probabilities" not in row


def test_npc_room_schedule_relationship_uses_the_room_api_directly():
    room_source = ROOM_TEMPLATE.read_text(encoding="utf-8-sig")
    people_source = PEOPLE_RUNTIME.read_text(encoding="utf-8-sig")

    assert "def is_open(self, week_value=None, time_value=None):" in room_source
    assert "return self.schedule.is_open(week_value, time_value)" in room_source
    assert "self.follows_room_schedule = bool(follows_room_schedule)" in people_source
    assert "room_obj.is_open(weekday_value, time_value)" in people_source
    assert 'data.get("follows_room_schedule", False)' in people_source


def test_friday_dance_venue_schedule_is_the_only_event_time_authority():
    amanda_model = AMANDA_DANCE_MODEL.read_text(encoding="utf-8-sig")
    becky_model = BECKY_DANCE_MODEL.read_text(encoding="utf-8-sig")

    for model in (amanda_model, becky_model):
        event_tuple = model.split("super(", 1)[1].split("self.event_name", 1)[0]
        assert "                    None,\n                    None," in event_tuple
        assert "(18, 21)" not in model
        assert "def canTrigger(" not in model

    assert "def becky_dance_event(" not in becky_model


def test_friday_dance_partner_objects_own_only_personal_eligibility():
    amanda = AMANDA_INFO.read_text(encoding="utf-8-sig")
    becky = BECKY_INFO.read_text(encoding="utf-8-sig")
    amanda_ready = amanda.split("def friday_dance_base_ready(self):", 1)[1].split("def friday_dance_legare_row", 1)[0]
    becky_ready = becky.split("def friday_dance_base_ready(self):", 1)[1].split("def dance_event_conditions_met", 1)[0]

    for ready in (amanda_ready, becky_ready):
        assert 'rooms.get("FridayDance").is_open()' not in ready
    assert 'self.is_at("FridayDance")' in amanda_ready
    assert 'location_now == "FridayDance"' in becky_ready
    assert '"MarketPlace"' not in becky_ready


def test_old_friday_dance_globals_are_consumed_only_by_save_migration():
    source = SAVE_SYNC.read_text(encoding="utf-8-sig")

    assert "def updateSave_V43():" in source
    assert 'roomDefinitions.get("FridayDance", None)' in source
    for legacy_name in (
        "DanceStep",
        "HandsDance",
        "KissDance",
        "TitsDance",
        "DanceMaxIAD",
        "DanceMaxIBD",
    ):
        assert legacy_name in source


def test_amanda_legare_dance_builder_uses_label_local_scratch():
    dance = (GAME / "NPC" / "Girls" / "Amanda" / "AmandaLegareDanceSequence.rpy").read_text(encoding="utf-8-sig")
    migration = SAVE_SYNC.read_text(encoding="utf-8-sig")

    assert "label AmandaLegareDanceSequence(dance_created=0, force_legare_first_dance=False, go_phrase=\"\", dance_index=0, created_index=0):" in dance
    for retired_name in ("DanceCreated", "ForceLegareFirstDance", "GoPhrase"):
        assert retired_name not in dance
        assert '"%s"' % retired_name in migration
    assert "def updateSave_V44():" in migration
