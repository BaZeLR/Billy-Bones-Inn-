from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AMANDA_DIR = ROOT / "game/NPC/Girls/Amanda"
EVENT_MODEL = AMANDA_DIR / "AmandaEventModel.rpy"
STREET_EVENT = AMANDA_DIR / "AmandaLegareStreetEvents.rpy"
LOVER_SCENE = AMANDA_DIR / "AmandaLoverSex.rpy"
DISCIPLINE_SCENES = AMANDA_DIR / "AmandaStreetDiscipline.rpy"
AMANDA_INIT = AMANDA_DIR / "InitAmanda.rpy"
AMANDA_TALK = AMANDA_DIR / "IntAmandaTalk.rpy"
STORY_RUNTIME = ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy"
PEOPLE_RUNTIME = ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy"
BREAKFAST = ROOT / "game/Inn/TavernKitchenBreakfast.rpy"
ARREST_CODE = ROOT / "game/Utilities/General/Common/OtherFunctionsCode.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def _label(source, name, next_name=None):
    block = source.split("label %s:" % name, 1)[1]
    if next_name is not None:
        block = block.split("label %s:" % next_name, 1)[0]
    return block


def test_amanda_market_visuals_are_static_data_owned_and_exist():
    source = _source(AMANDA_INIT)
    assert '"market": {' in source
    assert '"talk": ["images/amanda/market/amanda_market_talk.png"]' in source
    assert '"stranger_talk": ["images/amanda/market/amanda_market_stranger.png"]' in source
    assert (ROOT / "game/images/amanda/market/amanda_market_talk.png").is_file()
    assert (ROOT / "game/images/amanda/market/amanda_market_stranger.png").is_file()

    talk = _source(AMANDA_TALK)
    assert 'if str(rooms.current_code or "") == "MarketPlace":' in talk
    assert 'main_ui_runtime.talk_picture = AmandaStaticData.image_path("market", "talk")' in talk


def test_random_lover_event_owns_one_native_scene_and_returns_to_its_origin():
    intro = _label(_source(STREET_EVENT), "story_amanda_street_lover_encounter_0")
    lover = _source(LOVER_SCENE)

    assert 'main_ui_begin_native_scene_state("Аманда на улице")' in intro
    assert 'vscene AmandaStaticData.image_path("market", "stranger_talk")' in intro
    assert intro.count("main_ui_end_native_scene_state()") == 4
    assert "jump AmandaLoverSex" in intro

    assert "main_ui_begin_native_scene_state" not in lover.split("# Supporting functions", 1)[0]
    assert "jump StreetTavern" not in lover
    assert 'main_ui_end_native_scene_state()\n    return True' in lover
    assert 'main_ui_end_native_scene_state()\n                call ArrestCode from _call_amanda_lover_arrest\n                $ main_ui_begin_native_scene_state("Аманда на улице")' in lover
    arrest = _source(ARREST_CODE)
    assert '"Отойти от стражников":\n                        return' in arrest
    assert "jump StreetTavern" not in arrest


def test_first_actual_witness_starts_consequence_and_second_unlocks_service():
    lover = _source(LOVER_SCENE)
    witness_flow = lover.split("    if amanda_lover_build_get_in == 1:\n", 1)[1]
    visible = witness_flow.split("    else:\n", 1)[1].split(
        "    # Pregnancy check based on cum location", 1
    )[0]

    assert 'threads.get("amandaStreetDiscipline", None)' in lover
    assert "amanda_scene_discipline.forceEnable()" in visible
    assert "amanda_scene_discipline.setDay()" in visible
    assert 'Amanda.enable_tavern_service("intimate")' in visible
    assert 'Amanda.assign_tavern_service("intimate", True)' in visible
    assert "sawwithguys" not in visible


def test_repeating_encounter_and_ordered_consequence_have_separate_owners():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(EVENT_MODEL)

    recurring = runtime.split('LThreadData(0, "amanda", "StreetLoverEncounters"', 1)[1].split("),", 1)[0]
    discipline = runtime.split('LThreadData(0, "amanda", "StreetDiscipline"', 1)[1].split("),", 1)[0]
    assert "threaded=False" in recurring
    assert "AmandaStreetPunishmentBreakfast" in discipline
    assert "AmandaStreetLegareWarningBreakfast" in discipline
    assert "threaded=True" in discipline
    assert "SecondEncounter" not in event_model + runtime
    assert "discipline_pending" in event_model
    assert "not discipline_pending" in event_model


def test_breakfast_events_use_thread_state_and_label_local_values_only():
    source = _source(DISCIPLINE_SCENES)
    first = _label(
        source,
        "story_amanda_street_punishment_breakfast_1",
        "story_amanda_street_legare_warning_breakfast_2",
    )
    second = _label(source, "story_amanda_street_legare_warning_breakfast_2")

    assert "default " not in source
    assert "define " not in source
    assert "lambda" not in source
    assert 'renpy.dynamic("_' not in source
    assert first.startswith("\n    $ renpy.dynamic(")
    assert second.startswith("\n    $ renpy.dynamic(")
    for block in (first, second):
        assert "main_ui_begin_native_scene_state" in block
        assert 'menu:\n        "Продолжить":' in block
        assert "event_runtime.active_thread.advance()" in block
        assert "calendar_v2.advance_minutes(45)" in block
        assert "main_ui_end_native_scene_state()" in block
        assert "call TavernKitchenFinishBreakfastEvent from _call_amanda_street_" in block

    assert 'Amanda.set_var_int("prohibitwithguys", 1)' in first
    assert "Amanda.legare_forbidden = True" in first
    assert "special_cream_001" not in first
    assert 'Amanda.decide("street_legare_warning")' in second
    assert 'Amanda.wardrobe.set_day_dress("modestworkdress", True)' in second
    assert 'Amanda.set_day_underwear("panties", "", True)' in second
    assert 'Amanda.set_day_underwear("panties", "simplepanties", True)' in second
    assert "virginity" not in source


def test_intimate_jobs_honor_npc_owned_availability():
    runtime = _source(PEOPLE_RUNTIME)
    available = runtime.split("def tavern_job_available(self, job_key):", 1)[1].split(
        "def tavern_service_available", 1
    )[0]
    assign = runtime.split("def assign_tavern_service(self, target=\"\", tomorrow=True):", 1)[1].split(
        "def apply_tavern_job_plan", 1
    )[0]
    sunday = _source(BREAKFAST).split("def tavern_sunday_dinner_can_offer_service", 1)[1].split(
        "def tavern_sunday_dinner_service_offer_ids", 1
    )[0]

    assert 'self.tavern_service_available("intimate")' in available
    assert 'self.tavern_service_available("gloryhole")' in available
    assert 'self.tavern_service_available("intimate")' in assign
    assert 'self.tavern_service_available("gloryhole")' in assign
    assert 'discipline = threads.get("amandaStreetDiscipline", None)' in sunday
    assert 'not Amanda.tavern_service_available("intimate")' in sunday
