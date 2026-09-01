from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraPaintingsThread.rpy"


def test_clara_paintings_story_choices_are_native_label_menus():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert source.count("\n    menu:\n") == 22
    assert source.count('"Продолжить":') == 16
    assert source.count("main_ui_begin_native_scene_state(") == 13
    assert source.count("main_ui_end_native_scene_state()") == 16
    assert source.count("show screen main_ui") == 17
    for index in range(1, 6):
        assert f'vscene "images/clara/panishment/panishment{index}.jpg"' in source
    assert '"Ворваться и поставить Легаре на место":' in source
    assert '"Отступить и поддержать Клариссу позже":' in source
    assert '"Осторожно заглянуть внутрь" if int(player.stats.exploration or 0) >= 200:' in source
    assert '"Промолчать и уйти":' in source
    assert "label story_clara_paintings_first_ask_3:" in source
    assert "label story_clara_paintings_second_ask_4:" in source
    assert "label story_clara_paintings_legare_5:" in source
    assert "Альбер Легаре не ее настоящий отец" in source
    talk = (ROOT / "game" / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy").read_text(encoding="utf-8-sig")
    assert '"Спросить Клариссу о Легаре" if story_event_available' in talk
    assert 'int(threads["claraPaintingsPath"].num or 0) == 5' in talk
