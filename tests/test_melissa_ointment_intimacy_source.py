from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STORY_RUNTIME = ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
MELISSA_EVENTS = ROOT / "game" / "NPC" / "Girls" / "Melissa" / "MelissaOintmentIntimacy.rpy"
MELISSA_SEX = ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaSex.rpy"
MELISSA_INIT = ROOT / "game" / "NPC" / "Girls" / "Melissa" / "InitMelissa.rpy"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def test_ointment_story_is_one_melissa_owned_linear_thread():
    runtime = read(STORY_RUNTIME)
    block = runtime.split('LThreadData(0, "melissa", "OintmentIntimacy"', 1)[1].split(
        'LThreadData(0, "melissa", "AnalSolution"', 1
    )[0]

    assert "#threads['melissaCourtship'].completed" in block
    assert "#int(threads['amandaStreetDiscipline'].num or 0) >= 1" in block
    assert "#not bool(threads['amandaStreetDiscipline'].aborted)" in block
    assert '"story_melissa_ointment_talk_0"' in block
    assert '"story_melissa_ointment_request_1"' in block
    assert '"story_melissa_ointment_try_2"' in block
    assert 'TAVERN_AMANDA_LIZA_TALK_ROOMS, "enter", 14' in block
    assert block.count('"TavernMyRoom", "bedtime", 0') == 2
    assert block.count('None, (20, 22), 1,') == 2
    assert "#not Amanda.tavern_service_busy_now()" in block
    assert "#not Melissa.tavern_service_busy_now()" in block
    assert block.count("#people.is_awake('melissa')") == 3
    for person in ("amanda", "melissa", "liza"):
        assert "#str(people.location('%s') or '') == str(rooms.current_code or '')" % person in block
    assert block.count("#room_in_group(str(people.location('melissa') or ''), ROOM_GROUP_TAVERN)") == 2
    assert block.count("#not Melissa.sex_busy()") == 2
    assert '"special_cream_001"' in block
    assert "ointment_seen" not in block
    assert "ointment_requested" not in block
    assert "anal_unlocked" not in block


def test_ointment_labels_own_their_native_scene_flow_and_inventory_cost():
    labels = read(MELISSA_EVENTS)

    for label_name in (
        "story_melissa_ointment_talk_0",
        "story_melissa_ointment_request_1",
        "story_melissa_ointment_try_2",
    ):
        block = labels.split("label %s:" % label_name, 1)[1].split("\n\nlabel ", 1)[0]
        assert "main_ui_begin_native_scene_state(" in block
        assert "show screen main_ui" in block
        assert "menu:" in block
        assert "main_ui_end_native_scene_state()" in block
        assert "while True" not in block

    treatment = labels.split("label story_melissa_ointment_try_2:", 1)[1].split("\n\nlabel ", 1)[0]
    assert treatment.count('player.remove_item("special_cream_001", 1)') == 1
    assert treatment.count("event_runtime.active_thread.advance()") == 1
    assert 'Melissa.set_sex_stat("beauty"' in treatment
    assert "Melissa.add_arousal(8)" in treatment
    assert "анальный секс" not in treatment
    items = read(ROOT / "game/Items/Crafting/SoapCraftAndAtticItems.rpy")
    gifts = read(ROOT / "game/Utilities/General/Common/Actions.rpy")
    assert "делает ее шелковистой" in items
    assert '"special_cream_001": {' in gifts
    assert '"beauty_bonus": 2' in gifts.split('"special_cream_001": {', 1)[1].split("},", 1)[0]
    clara = read(ROOT / "game/NPC/Girls/Clara/ClaraPaintingsThread.rpy")
    assert 'Clara.set_sex_stat("beauty"' in clara
    assert "Clara.add_arousal(8)" in clara


def test_melissa_anal_action_waits_for_the_shared_moon_event():
    engine = read(MELISSA_SEX)
    melissa = read(MELISSA_INIT)
    melissa_class = melissa.split("class MelissaInfo(Girl):", 1)[1].split(
        "define MelissaStaticData", 1
    )[0]
    action = engine.split('"Войти сзади" if ', 1)[1].split(":\n", 1)[0]

    assert '_hse_info.intimacy_action_allowed("anal")' in action
    assert 'def intimacy_action_allowed(self, action_code=""):' in melissa_class
    assert 'return bool(threads["melissaAnalSolution"].completed)' in melissa_class
    assert 'if action_key == "vaginal":' in melissa_class
    assert 'return not bool(self.sex_stat("virginity", True))' in melissa_class
    assert 'threads["melissaOintmentIntimacy"]' not in engine
    assert "def household_sex_anal_unlocked" not in engine
    assert "melissa_anal_unlocked" not in engine + melissa
    assert "ointment_seen" not in engine + melissa


def test_applying_ointment_has_one_completion_path_and_one_item_cost():
    labels = read(MELISSA_EVENTS)
    treatment = labels.split("label story_melissa_ointment_try_2:", 1)[1]

    assert treatment.count('player.remove_item("special_cream_001", 1)') == 1
    assert treatment.count("event_runtime.active_thread.advance()") == 1
    assert '"Не торопить Мелиссу":' not in treatment
    assert treatment.index('"Отложить просьбу":') > treatment.index(
        '"Помочь Мелиссе нанести крем":'
    )


def test_clarissa_melissa_talk_is_an_entry_event_and_shared_visit_is_lunar():
    runtime = read(STORY_RUNTIME)
    block = runtime.split('LThreadData(0, "melissa", "AnalSolution"', 1)[1].split(
        'LThreadData(0, "melissa", "UpstairsBedroomRelief"', 1
    )[0]
    room = read(ROOT / "game/Inn/TavernMelissaRoom.rpy")
    scenes = read(ROOT / "game/NPC/Girls/Melissa/MelissaAnalSolution.rpy")

    assert '"TavernMelissaRoom", "enter", 2' in block
    assert '"TavernMyRoom", "bedtime", 0' in block
    assert "#calendar_v2.moon_phase_name_en() == 'Full Moon'" in block
    assert "#bool(Melissa.sex_stat('virginity', True))" in block
    assert "#bool(Clara.sex_stat('virginity', True))" in block
    assert '"solution_talk"' not in room
    assert '"solution"' not in room
    assert 'Clara.record_sex_history("You", "TavernMyRoom", "outside")' in scenes
    assert 'Melissa.record_sex_history("You", "TavernMyRoom", "outside")' in scenes
    assert 'set_sex_stat("virginity", False)' not in scenes


def test_morning_wake_refreshes_room_actions_after_restoring_scene_context():
    wake = read(ROOT / "game/NPC/Girls/Melissa/MelissaMorningWake.rpy")
    for step in range(6):
        block = wake.split("label story_melissa_morning_wake_%d:" % step, 1)[1].split(
            "\n\nlabel ", 1
        )[0]
        assert block.index("main_ui_end_native_scene_state()") < block.index(
            "main_ui_runtime.action_items = tavern_melissa_room_action_items()"
        )
