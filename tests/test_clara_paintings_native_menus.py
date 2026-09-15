from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraPaintingsThread.rpy"


def test_clara_paintings_story_choices_are_native_label_menus():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert source.count("\n    menu:\n") == 33
    assert source.count('"Продолжить":') == 19
    assert source.count("main_ui_begin_native_scene_state(") == 17
    assert source.count("main_ui_end_native_scene_state()") == 25
    assert source.count("show screen main_ui") == 19
    for index in range(1, 6):
        assert f'vscene "images/clara/panishment/panishment{index}.jpg"' in source
    assert '"Ворваться и поставить Легаре на место":' in source
    assert '"Отступить и поддержать Клариссу позже":' in source
    assert '"Осторожно заглянуть внутрь":' in source
    assert "if int(player.stats.exploration or 0) < 200:" in source
    assert '"Не вмешиваться и уйти":' in source
    assert "label story_clara_paintings_first_ask_3:" in source
    assert "label story_clara_paintings_second_ask_4:" in source
    assert "label story_clara_paintings_legare_5:" in source
    assert 'vscene "images/Alber/church/cermon_fiance_clara.png"' in source
    assert 'vscene "images/Alber/church/cermon_fiance1_clara.png"' in source
    church = source.split("label story_clara_paintings_church_6:", 1)[1].split("\nlabel ", 1)[0]
    assert church.index('cermon_fiance_clara.png') < church.index('cermon_fiance1_clara.png')
    assert '"\u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u043a \u043f\u0440\u0438\u0445\u043e\u0436\u0430\u043d\u0430\u043c":' in church
    assert "Альбер Легаре не ее настоящий отец" in source
    talk = (ROOT / "game" / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy").read_text(encoding="utf-8-sig")
    assert '"Спросить Клариссу о Легаре" if story_event_available' in talk
    assert 'int(threads["claraPaintingsPath"].num or 0) == 5' in talk
