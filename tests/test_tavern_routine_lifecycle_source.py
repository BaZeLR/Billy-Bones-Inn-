from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_tavern_routine_visuals_come_from_present_assigned_jobs():
    source = _source("game/Inn/TavernMain.rpy")

    assert "def tavern_main_routine_visual_data():" in source
    assert 'girls_by_job(job_key, "TavernMain")' in source
    assert 'person_data.image_sequence("tavern", image_key)' in source
    assert '(("jobcleaning", "hall_cleaning"), ("jobwaitress", "waitress"))' in source
    assert '"preopening" if preopening else "open"' in source
    assert 'return str(tavern_main_routine_visual_data().get("picture", "") or default_picture)' in source
    assert "$ scene_runtime.picture = tavern_main_picture()" in source
    assert not (ROOT / "game/Inn/TavernShowImage.rpy").exists()


def test_household_npc_data_owns_job_picture_catalogs_through_people_data_api():
    people = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    melissa = _source("game/NPC/Girls/Melissa/InitMelissa.rpy")
    amanda = _source("game/NPC/Girls/Amanda/InitAmanda.rpy")
    sandra = _source("game/NPC/Girls/Sandra/InitSandra.rpy")

    assert people.count("def image_sequence(self") == 1
    for source in (melissa, amanda, sandra):
        assert "self.image_manifest = {" in source
        assert '"hall_cleaning"' in source
        assert '"waitress"' in source


def test_melissa_morning_backyard_routine_uses_her_laundry_catalog():
    melissa = _source("game/NPC/Girls/Melissa/InitMelissa.rpy")
    backyard = _source("game/Inn/Backyard.rpy")

    assert '"images/melissa/making laundry.png"' in melissa
    assert '"images/melissa/hanging laundry.png"' in melissa
    assert 'MelissaStaticData.image_sequence("backyard", "laundry")' in backyard
    assert 'procedural_choice(melissa_backyard, "backyard_melissa_morning_routine")' in backyard


def test_melissa_fall_is_a_consumable_native_tavern_work_event():
    event = _source("game/NPC/Girls/Melissa/MelissaEvents.rpy")
    block = event.split("label event_melissa_waitress_fall", 1)[1]

    assert 'main_ui_begin_native_scene_state("Событие: неуклюжая официантка")' in block
    assert 'MelissaStaticData.cycle_image("tavern", "clumsy_waitress", 0)' in block
    assert 'MelissaStaticData.cycle_image("tavern", "clumsy_waitress", 1)' in block
    assert 'MelissaStaticData.cycle_image("tavern", "clumsy_waitress", 2)' in block
    assert '"Помочь Мелиссе подняться":' in block
    assert '"Не обращать внимания":' in block
    assert '"Отчитать за неуклюжесть и потерю":' in block
    assert "Melissa.change_social(friend_delta=relationship_delta)" in block
    assert "player.tavern_management.winenum = max(0" in block
    assert '"Вернуться к работе":' in block
    assert "main_ui_end_native_scene_state()" in block
    assert "return result" in block
