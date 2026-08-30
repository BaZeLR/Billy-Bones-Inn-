from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.runtime_logic_tests import (  # noqa: E402
    RuntimeLogicReport,
    collect_labels,
    event_type_name,
    iter_rpy_files,
    parse_story_threads,
    read_text,
    validate_event_schema,
    validate_thread_blueprints,
)


STORY_PATH = ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
MELISSA_EVENTS_PATH = ROOT / "game" / "NPC" / "Girls" / "Melissa" / "MelissaEvents.rpy"
HOUSEHOLD_EVENTS_PATH = ROOT / "game" / "Inn" / "HouseholdRuntimeEvents.rpy"
MELISSA_WERECAT_PATH = ROOT / "game" / "NPC" / "Secondary" / "MelissaWerecatQuest.rpy"
WERECAT_OWNER_PATH = ROOT / "game" / "NPC" / "Secondary" / "WerecatNPC.rpy"
GAME_ITEMS_PATH = ROOT / "game" / "Items" / "Core" / "GameItems.rpy"
MELISSA_BOOKLET_ITEM_PATH = ROOT / "game" / "Items" / "Resources" / "MelissaBookletItem.rpy"
GAME_DIR = ROOT / "game"

LABEL_RE = re.compile(r"^\s*label\s+([A-Za-z_][A-Za-z0-9_]*)\b", re.MULTILINE)
DIRECT_CALL_RE = re.compile(r"^\s*(?:call(?!\s+screen)|jump)\s+([A-Za-z_][A-Za-z0-9_]*)\b", re.MULTILINE)

MELISSA_TARGET_PREFIXES = (
    "story_melissa_",
    "melissaClaraOverheard_",
    "MelissaDressRequestEvent",
)

MELISSA_ROUTE_TOKENS = {
    ("HunterClub", "overheard"): (
        ("game/Town/HunterClub.rpy", 'rooms.get("HunterClub").build_action_items()'),
        ("game/Town/HunterClub.rpy", 'call checkTriggers("HunterClub", "overheard", 0)'),
    ),
    ("TavernAtic", "melissa_bats"): (
        ("game/Inn/TavernAtic.rpy", 'story_event_available("TavernAtic", "melissa_bats")'),
        ("game/Inn/TavernAtic.rpy", 'Call("checkTriggers", "TavernAtic", "melissa_bats", 0)'),
    ),
    ("TavernAmandaRoom", "melissa_bats"): (
        ("game/Inn/TavernAmandaRoom.rpy", 'story_event_available(rooms.current_code, "melissa_bats")'),
        ("game/Inn/TavernAmandaRoom.rpy", 'call checkTriggers(rooms.current_code, "melissa_bats", 0)'),
    ),
    ("TavernKitchen", "enter"): (
        ("game/Inn/TavernKitchen.rpy", "call RoomEnterEventGate(rooms.current_code, False)"),
        ("game/Utilities/General/Common/RoomEnterPipeline.rpy", 'story_event_available(_room_enter_code, "enter")'),
        ("game/Utilities/General/Common/RoomEnterPipeline.rpy", 'call checkTriggers(_room_enter_code, "enter", 0)'),
    ),
    ("TavernKitchen", "melissa_dress_request"): (
        ("game/Inn/TavernKitchenBreakfast.rpy", 'story_event_available("TavernKitchen", "melissa_dress_request")'),
        ("game/Inn/TavernKitchenBreakfast.rpy", "call MelissaDressRequestEvent"),
    ),
    ("TavernMain", "melissa_talk"): (
        ("game/NPC/Girls/Melissa/IntMelissaTalk.rpy", 'story_event_available(str(rooms.current_code or ""), "melissa_talk")'),
        ("game/NPC/Girls/Melissa/IntMelissaTalk.rpy", 'call checkTriggers(rooms.current_code, "melissa_talk", 0)'),
    ),
    ("TavernMain", "melissa_dress_request"): (
        ("game/Inn/TavernMain.rpy", 'story_event_available("TavernMain", "melissa_dress_request")'),
        ("game/Inn/TavernMain.rpy", "call MelissaDressRequestEvent"),
    ),
    ("TavernMain", "overheard"): (
        ("game/Inn/TavernMain.rpy", 'story_event_available("TavernMain", "overheard")'),
        ("game/Inn/TavernMain.rpy", 'Call("checkTriggers", "TavernMain", "overheard", 0)'),
    ),
    ("talk_melissa", "melissa_intimacy"): (
        ("game/NPC/Girls/Melissa/IntMelissaTalk.rpy", 'story_event_available("talk_melissa", "melissa_intimacy")'),
        ("game/NPC/Girls/Melissa/IntMelissaTalk.rpy", 'call checkTriggers("talk_melissa", "melissa_intimacy", 0)'),
    ),
    ("TavernMelissaRoom", "room_search"): (
        ("game/Inn/TavernMelissaRoom.rpy", 'Call("UpstairsRoomSearch", "TavernMelissaRoom")'),
        ("game/Items/Crafting/SoapCraftAndAtticItems.rpy", 'story_event_available(_up_room_code, "room_search")'),
        ("game/Items/Crafting/SoapCraftAndAtticItems.rpy", 'call checkTriggers(_up_room_code, "room_search", 0)'),
    ),
    ("TavernStorage", "enter"): (
        ("game/Inn/TavernStorage.rpy", "call RoomEnterEventGate(rooms.current_code, False)"),
        ("game/Utilities/General/Common/RoomEnterPipeline.rpy", 'story_event_available(_room_enter_code, "enter")'),
        ("game/Utilities/General/Common/RoomEnterPipeline.rpy", 'call checkTriggers(_room_enter_code, "enter", 0)'),
    ),
    ("TavernUpstairs", "enter"): (
        ("game/Inn/TavernUpstairs.rpy", "call RoomEnterEventGate(rooms.current_code, False)"),
        ("game/Utilities/General/Common/RoomEnterPipeline.rpy", 'story_event_available(_room_enter_code, "enter")'),
        ("game/Utilities/General/Common/RoomEnterPipeline.rpy", 'call checkTriggers(_room_enter_code, "enter", 0)'),
    ),
}


def collect_label_sources():
    sources = {}
    for path in iter_rpy_files(GAME_DIR):
        source = read_text(path)
        rel_path = path.relative_to(ROOT).as_posix()
        for label in LABEL_RE.findall(source):
            sources.setdefault(label, []).append(rel_path)
    return sources


def story_label_bodies(source):
    matches = list(LABEL_RE.finditer(source))
    bodies = {}
    for index, match in enumerate(matches):
        label = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        bodies[label] = source[match.end() : end]
    return bodies


class MelissaThreadEventModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read_text(STORY_PATH)
        cls.melissa_events_source = read_text(MELISSA_EVENTS_PATH)
        cls.household_events_source = read_text(HOUSEHOLD_EVENTS_PATH)
        cls.melissa_werecat_source = read_text(MELISSA_WERECAT_PATH)
        cls.werecat_owner_source = read_text(WERECAT_OWNER_PATH)
        cls.game_items_source = read_text(GAME_ITEMS_PATH)
        cls.melissa_booklet_item_source = read_text(MELISSA_BOOKLET_ITEM_PATH)
        parse_report = RuntimeLogicReport()
        cls.threads = parse_story_threads(cls.source, parse_report)
        cls.melissa_threads = [thread for thread in cls.threads if thread.list_name == "melissaThreadList"]
        cls.melissa_events = [event for thread in cls.melissa_threads for event in thread.events]
        cls.report = RuntimeLogicReport()
        for row in parse_report.failures:
            if "melissa" in row.detail.lower():
                cls.report.add(row.status, row.area, row.detail)
        validate_thread_blueprints(cls.melissa_threads, cls.report)
        validate_event_schema(cls.melissa_events, cls.report)
        cls.labels = collect_labels(GAME_DIR)
        cls.label_sources = collect_label_sources()
        cls.story_bodies = story_label_bodies(cls.source)
        cls.melissa_event_bodies = story_label_bodies(cls.melissa_events_source)
        cls.household_event_bodies = story_label_bodies(cls.household_events_source)

    def test_melissa_thread_list_uses_runtime_thread_model(self):
        failures = [row.detail for row in self.report.failures]
        self.assertFalse(failures, "\n".join(failures))
        self.assertGreaterEqual(len(self.melissa_threads), 3)
        self.assertGreaterEqual(len(self.melissa_events), 10)
        self.assertEqual(
            {thread.name for thread in self.melissa_threads},
            {"melissaBatProblem", "melissaRatProblem", "melissaWerecatProblem", "melissaRevealingDressRequest", "melissaCourtship"},
        )
        for thread in self.melissa_threads:
            self.assertEqual(thread.person, "melissa")
            self.assertTrue(thread.constructor.endswith("ThreadData"))
            self.assertTrue(thread.subname)

    def test_rat_and_werecat_are_separate_threads(self):
        thread_map = {thread.name: thread for thread in self.melissa_threads}
        rat_thread = thread_map["melissaRatProblem"]
        werecat_thread = thread_map["melissaWerecatProblem"]
        bat_thread = thread_map["melissaBatProblem"]

        self.assertEqual([event.target for event in rat_thread.events], ["story_melissa_storage_rat_0"])
        self.assertEqual(
            [event.target for event in werecat_thread.events],
            [
                "story_melissa_werecat_intro_0",
                "story_melissa_werecat_rumor_0",
                "story_melissa_werecat_home_0",
                "story_melissa_werecat_home_1",
            ],
        )
        self.assertIn("melissaRatProblem_0", self.source)
        self.assertNotIn("melissaRatSolution", self.source)
        self.assertIsNone(werecat_thread.cond)
        self.assertEqual(bat_thread.cond, "melissaRatProblem_0")

    def test_rat_problem_is_active_from_new_game_but_werecat_tracking_waits_for_cleanup(self):
        self.assertIn('"rats_problem_active": 1', self.werecat_owner_source)
        self.assertIn('"rat_food_loss_next_day": 7', self.werecat_owner_source)
        self.assertIn('people_to_int(Melissa.storage_rat_help_day, -1) >= 0', self.melissa_werecat_source)
        self.assertNotIn('"rat_breakfast_seen"', self.werecat_owner_source)

    def test_melissa_event_targets_are_existing_runtime_labels(self):
        problems = []
        for event in self.melissa_events:
            event_name = event_type_name(event)
            if not event.target.startswith(MELISSA_TARGET_PREFIXES):
                problems.append(f"{event_name}: target does not use a Melissa event prefix")
            if event.target not in self.labels:
                problems.append(f"{event_name}: missing label {event.target}")
                continue
            sources = self.label_sources.get(event.target, [])
            if event.target.startswith("story_melissa_"):
                if sources != ["game/NPC/Girls/Melissa/MelissaEvents.rpy"]:
                    problems.append(f"{event_name}: target label source must be MelissaEvents.rpy, got {sources}")
                if event.target not in self.melissa_event_bodies:
                    problems.append(f"{event_name}: target label body was not found in MelissaEvents.rpy")
            elif event.target == "MelissaDressRequestEvent":
                if sources != ["game/Inn/HouseholdRuntimeEvents.rpy"]:
                    problems.append(f"{event_name}: target label source must be HouseholdRuntimeEvents.rpy, got {sources}")
                if event.target not in self.household_event_bodies:
                    problems.append(f"{event_name}: target label body was not found in HouseholdRuntimeEvents.rpy")
            else:
                if event.target not in self.story_bodies:
                    problems.append(f"{event_name}: target label body was not found in StoryEventRuntime.rpy")
        self.assertFalse(problems, "\n".join(problems))

    def test_melissa_event_routes_have_clickable_gates(self):
        route_keys = {(event.location, event.action) for event in self.melissa_events}
        problems = []
        for route_key in sorted(route_keys):
            if not route_key[0] or not route_key[1]:
                problems.append(f"{route_key}: empty location/action binding")
                continue
            token_specs = MELISSA_ROUTE_TOKENS.get(route_key)
            if token_specs is None:
                problems.append(f"{route_key}: no Melissa route check registered")
                continue
            for rel_path, token in token_specs:
                source = read_text(ROOT / rel_path)
                if token not in source:
                    problems.append(f"{route_key}: missing route token {token!r} in {rel_path}")
        self.assertFalse(problems, "\n".join(problems))

    def test_melissa_bats_roof_and_booklet_aftermath_follow_smoke(self):
        bat_thread = next(thread for thread in self.melissa_threads if thread.name == "melissaBatProblem")
        ordered_targets = [event.target for event in bat_thread.events]
        self.assertEqual(ordered_targets[4], "story_melissa_bat_problem_3")
        self.assertEqual(ordered_targets[5], "story_melissa_bat_problem_fall")
        self.assertEqual(ordered_targets[6], "story_melissa_bat_problem_4")
        self.assertEqual(ordered_targets[7], "story_melissa_bat_problem_roof")
        self.assertEqual(ordered_targets[8], "story_melissa_bat_problem_5")
        self.assertEqual(ordered_targets[9], "story_melissa_bat_problem_booklet_search")
        self.assertEqual(ordered_targets[10], "story_melissa_bat_problem_6")

    def test_melissa_bat_events_cost_45_minutes(self):
        for target in (
            "story_melissa_bat_problem_0",
            "story_melissa_bat_problem_1",
            "story_melissa_bat_problem_room_inspect",
            "story_melissa_bat_problem_2",
            "story_melissa_bat_problem_3",
            "story_melissa_bat_problem_fall",
            "story_melissa_bat_problem_4",
            "story_melissa_bat_problem_roof",
            "story_melissa_bat_problem_6",
        ):
            body = self.melissa_event_bodies.get(target, "")
            self.assertEqual(body.count("calendar_v2.advance_minutes(45)"), 1, target)
            self.assertGreater(body.find("calendar_v2.advance_minutes(45)"), body.rfind('"[scene_runtime.text]"'), target)
        body = self.melissa_event_bodies.get("story_melissa_bat_problem_booklet_search", "")
        self.assertEqual(body.count("calendar_v2.advance_minutes(45)"), 2, "story_melissa_bat_problem_booklet_search")
        self.assertEqual(body.count('"[scene_runtime.text]"'), 2, "story_melissa_bat_problem_booklet_search")
        self.assertGreater(body.find("calendar_v2.advance_minutes(45)"), body.find('"[scene_runtime.text]"'), "story_melissa_bat_problem_booklet_search")
        self.assertGreater(body.rfind("calendar_v2.advance_minutes(45)"), body.rfind('"[scene_runtime.text]"'), "story_melissa_bat_problem_booklet_search")

    def test_melissa_roof_cost_and_catch_scene_use_authored_sequence(self):
        roof_body = self.melissa_event_bodies.get("story_melissa_bat_problem_roof", "")
        catch_body = self.melissa_event_bodies.get("story_melissa_bat_problem_5", "")
        self.assertIn("player.spend_money(2000)", roof_body)
        self.assertIn("current_game_day() or 0) + 2", roof_body)
        self.assertNotIn("spend_money(1000)", roof_body)
        for image_index in range(3):
            self.assertIn('MelissaStaticData.cycle_image("amanda_room", "under_bed_search", %d)' % image_index, catch_body)
        self.assertIn("main_ui_begin_native_scene_state", catch_body)
        self.assertEqual(catch_body.count("event_runtime.active_thread.advance()"), 2)
        self.assertIn("if bool(Melissa.drawings_found):", catch_body)

    def test_melissa_booklet_search_requires_exploration_and_reveals_room_item(self):
        body = self.melissa_event_bodies.get("story_melissa_bat_problem_booklet_search", "")
        self.assertIn("int(effective_player_exploration() or 0) <= 120", body)
        self.assertNotIn('_room_add_item_by_id(TavernMelissaRoomRoom, "melissa_drawings_booklet_001")', body)
        self.assertIn('"melissa_drawings_booklet_001"', read_text(ROOT / "game/Inn/TavernMelissaRoom.rpy"))
        self.assertIn("condition=melissa_drawings_booklet_visible", self.melissa_booklet_item_source)
        self.assertIn('Melissa.drawings_booklet_left', self.melissa_events_source)
        self.assertNotIn('Melissa.var["drawings_booklet_taken"]', self.melissa_events_source)
        self.assertNotIn('Melissa.var["drawings_spy_option_unlocked"]', self.melissa_events_source)
        self.assertIn("player.item_count('melissa_drawings_booklet_001')", self.source)
        self.assertNotIn("MelissaFoundBookletObjectMenu", self.melissa_events_source)
        self.assertGreater(body.find("Melissa.drawings_found = True"), body.find("effective_player_exploration"))
        self.assertIn("event_runtime.active_thread.advance()", body)

    def test_melissa_booklet_item_is_registered_and_readable(self):
        self.assertIn('object_id="melissa_drawings_booklet_001"', self.melissa_booklet_item_source)
        self.assertIn('target="ReadMelissaBooklet"', self.melissa_booklet_item_source)
        self.assertIn('target="MelissaBookletTake"', self.melissa_booklet_item_source)
        self.assertIn('target="MelissaBookletLeaveThere"', self.melissa_booklet_item_source)
        self.assertIn("readable=True", self.melissa_booklet_item_source)
        self.assertEqual(self.melissa_booklet_item_source.count("condition=melissa_drawings_booklet_visible"), 4)
        self.assertIn('call PlayerCardInventoryItemMenu("melissa_drawings_booklet_001", True)', self.melissa_events_source)

    def test_melissa_target_scene_calls_resolve_to_existing_files(self):
        problems = []
        for event in self.melissa_events:
            body = self.melissa_event_bodies.get(event.target, self.story_bodies.get(event.target, ""))
            for called_label in DIRECT_CALL_RE.findall(body):
                if called_label not in self.labels:
                    problems.append(f"{event.target}: direct call/jump target {called_label} is missing")
                    continue
                if len(self.label_sources.get(called_label, [])) != 1:
                    problems.append(f"{event.target}: direct call/jump target {called_label} is duplicated")
        self.assertFalse(problems, "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
