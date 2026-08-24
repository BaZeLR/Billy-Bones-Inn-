from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/NPC/Girls/Becky/BeckyLoversInStore.rpy"


def test_becky_store_lover_event_keeps_original_gates_and_consequences():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert 'CheckIfSexEventExist("becky", 99, "StoreLover") > 0' in source
    assert 'GetSexEventFromTable("becky", 99, "StoreLover")' in source
    assert "Becky.store_lover_modest_reaction()" in source
    for event_type in (1, 2, 3):
        assert f"becky_store_sex_type == {event_type}" in source
    assert 'call PregnancyCheck("becky", "inside", 1, "Легаре")' in source
    assert 'call PregnancyCheck("becky", "inside", 1, gruzchik_name, 1, "Неизвестный грузчик")' in source
    assert "Becky.mark_store_orgasm_today()" in source


def test_becky_store_lover_scene_scratch_is_local_to_the_authored_label():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert 'renpy.dynamic("becky_store_sex_type", "choose_option", "gruzchik_name", "gruzchik_girl")' in source
    for legacy_name in (
        "BeckyStoreSexType",
        "ChooseOption",
        "GruzchikName",
        "GruzchikGirl",
    ):
        assert legacy_name not in source
    assert "default " not in source
    assert "define " not in source
