from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDDIE_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntEddieTalk.rpy"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_eddie_dialogs_are_explicit_sublabels_not_dispatcher():
    source = _source(EDDIE_TALK)
    init_source = _source(ROOT / "game" / "NPC" / "Secondary" / "InitEddieTalk.rpy")

    assert "label IntEddieTalkMenu:" not in source
    assert "jump IntEddieTalkMenu" not in source
    assert "jump IntEddieTalk" not in source
    assert "while True:" in source
    assert "menu:" in source
    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert "label IntEddieTalkApply" not in source
    assert 'str(choice_code or "")' not in source
    assert "Eddie.ensure_story_defaults()" not in source
    assert "_eddie_var" not in source
    assert "peopleInfo[_eddie_name].update()" not in source
    assert "EddieVar" not in source
    assert "renpy.random" not in source
    assert "eddie_talk_init_state" not in source + init_source
    assert "label InitEddieTalk:" not in init_source
    assert "if _eddie_talk_new:" in source

    for label in [
        "label IntEddieTalkSmalltalk:",
        "label IntEddieTalkPersonal:",
        "label IntEddieTalkWhores:",
        "label IntEddieTalkGirls:",
        "label IntEddieTalkMomHelper:",
        "label IntEddieTalkBruise:",
        "label IntEddieTalkWhoHit:",
        "label IntEddieTalkDestination:",
        "label IntEddieTalkComplain:",
    ]:
        assert label in source


def test_eddie_dialog_menu_has_all_reference_choices():
    source = _source(EDDIE_TALK)

    for choice in [
        "Поболтать с Эдди о разной фигне.",
        "Поболтать с Эдди о личных вещах.",
        "Рассказать Эдди о том, что у вас теперь работают девочки.",
        "Поинтересоваться у Эдди как ему ваши девочки.",
        "Предложить помочь подкатится к хозяйке лавки.",
        "Спросить о синяке.",
        "А все таки расскажи, кто это тебе так вмазал?",
        "А куда это ты ездил?",
        "Страже жаловался?",
    ]:
        assert choice in source


def test_eddie_dialog_uses_vscene_and_room_restore_end():
    source = _source(EDDIE_TALK)

    assert 'vscene grocery_store_grocer_picture("eddie")' in source
    assert 'vscene "images/eddie/portraits/fingal.png"' not in source
    assert 'vscene "images/eddie/portraits/portrait_0.png"' not in source
    assert 'vscene "images/eddie/portraits/surprised.png"' in source
    assert '"Закончить разговор":' in source
    assert "$ main_ui_end_talk_state()" in source
    assert 'Jump("GroceryStore")' not in source


def test_shop_click_regression_uses_current_oop_and_object_menu_apis():
    source = _source(ROOT / "tools" / "external_click_play_test.py")

    assert 'Talked["eddie"]' not in source
    assert 'TalkedToday["eddie"]' not in source
    assert 'Friends["eddie"]' not in source
    assert 'Function(grocery_store_open_object_menu_state' not in source
    assert 'Function(wine_store_open_object_menu_state' not in source
    assert '$ Eddie.talked_today = 0' in source
