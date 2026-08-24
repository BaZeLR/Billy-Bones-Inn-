from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraPaintingsThread.rpy"


def test_clara_paintings_story_choices_are_native_label_menus():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert source.count("\n    menu:\n") == 3
    assert '"Ворваться и поставить Легаре на место":' in source
    assert '"Отступить и поддержать Клариссу позже":' in source
    assert '"Осторожно заглянуть внутрь" if int(player.stats.exploration or 0) >= 200:' in source
    assert '"Промолчать и уйти":' in source
