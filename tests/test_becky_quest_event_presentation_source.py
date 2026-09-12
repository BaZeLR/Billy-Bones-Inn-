from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEST = (ROOT / "game/NPC/Girls/Becky/BeckyQuestInit.rpy").read_text(encoding="utf-8-sig")
REFERENCE = (ROOT / "textLocRef/BeckyQuestInit.txt").read_text(encoding="utf-8-sig")


def test_becky_quest_offer_owns_its_event_picture_text_and_native_menus():
    label = QUEST.split("label BeckyQuestInit():", 1)[1]

    assert '$ main_ui_begin_native_scene_state("Предложение Бекки")' in label
    assert "show screen main_ui" in label
    assert 'vscene grocery_store_grocer_picture("becky")' in label
    assert "call GirlsDesc" not in label
    assert "$ scene_runtime.text =" in label
    assert "$ scene_runtime.location_text = scene_runtime.text" in label
    assert label.count("menu:") == 3


def test_becky_quest_offer_preserves_reference_choices_and_market_exits():
    for caption in (
        "А кто ж не хочет?",
        "Пойти подумать над предложением",
        "Неа. Меня ни работа, ни деньги не интересуют",
        "Вернуться на рыночную площадь",
    ):
        assert caption in REFERENCE
        assert caption in QUEST

    assert QUEST.count("$ main_ui_end_native_scene_state()") == 2
    assert QUEST.count("jump MarketPlace") == 2
    assert "$ event_runtime.active_thread.advanceTo(2, force_active=True)" in QUEST
    assert "$ event_runtime.active_thread.advance()" in QUEST
    assert "$ Becky.sherwood_warning_stage = 1" in QUEST
    assert "$ Becky.sherwood_suspicion += 1" in QUEST
