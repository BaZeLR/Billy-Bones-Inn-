from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_core_runtime_definitions_are_not_silently_overridden():
    cases = (
        ("game/Town/RandomTownEvents.rpy", "def __init__(self):", 1),
        ("game/Town/Market/MarketPlace.rpy", "def marketplace_action_items():", 1),
        ("game/Utilities/General/Classes/GameObjectTemplate.rpy", "def register_room_rule(rule):", 1),
        ("game/Utilities/General/NPC/PeopleRuntime.rpy", "def reset_skill_gains(self):", 1),
        ("game/Utilities/General/NPC/PeopleRuntime.rpy", "def record_skill_gain(self, key, amount=1):", 1),
        ("game/Utilities/General/NPC/PeopleRuntime.rpy", 'def people_name(person="", grammatical_case="nominative", fallback=""):', 1),
        ("game/Utilities/General/Sex/BodyInteractionModel.rpy", 'def bodymodel_owner_containers(char_id=""):', 1),
    )

    for relative, definition, expected_count in cases:
        assert read(relative).count(definition) == expected_count, relative


def test_town_street_constructor_keeps_blackworker_feature_state():
    source = read("game/Town/RandomTownEvents.rpy")
    constructor = source.split("def __init__(self):", 1)[1].split("STREET_NAMES", 1)[0]

    assert "self.blackworkers = []" in constructor
    assert "self.blackworker_candidates = []" in constructor

    migration = read("game/TractirSaveSync.rpy").split("def updateSave_V20():", 1)[1]
    assert 'TownStreet.blackworkers = []' in migration
    assert 'TownStreet.blackworker_candidates = []' in migration


def test_debug_document_output_path_is_not_saved_game_state():
    source = read("game/Utilities/General/Common/DebugTools.rpy")

    assert "DebugBuilderRepairNotesPath" not in source
    assert "_debug_builder_repair_notes_path = debug_builder_write_repair_document()" in source


def test_main_ui_has_no_unused_story_board_state_defaults():
    source = read("game/Utilities/General/Screens/main_layout.rpy")

    assert "story_board_hover_event_thread" not in source
    assert "story_board_hover_event_index" not in source
    assert "story_board_control_thread_name" not in source
