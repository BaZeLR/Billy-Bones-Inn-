from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Inn/TavernKitchenBreakfast.rpy"


def _label_block(source, label_name, next_label):
    return source.split(f"label {label_name}", 1)[1].split(f"label {next_label}", 1)[0]


def test_breakfast_authored_decisions_use_native_label_menus():
    source = SOURCE.read_text(encoding="utf-8-sig")
    slices = (
        ("TavernKitchenBreakfastAmandaAtticMock:", "TavernKitchenBreakfastAmandaAtticExpose:"),
        ("TavernKitchenBreakfastMelissaAmandaGerhard:", "TavernKitchenBreakfastMelissaAmandaGerhardNatural:"),
        ("TavernKitchenBreakfastTease:", "TavernKitchenBreakfastTeasePrivate"),
        ("TavernKitchenBreakfastMorningIssue:", "TavernKitchenBreakfastMarketTalk:"),
        ("TavernKitchenBreakfastPerkMenu:", "TavernKitchenBreakfastLookAtGirl"),
    )

    for label_name, next_label in slices:
        block = _label_block(source, label_name, next_label)
        assert "\n    menu:\n" in block or "\n        menu:\n" in block
        assert "QueuePagedPanelText" not in block
        assert "ReturnToMainUI" not in block
        assert "MenuItem(" not in block


def test_breakfast_hub_has_one_native_choice_authority_without_paging_state():
    source = SOURCE.read_text(encoding="utf-8-sig")
    hub = _label_block(source, "TavernKitchenBreakfastMenu:", "TavernKitchenBreakfastShowText")
    show_text = _label_block(source, "TavernKitchenBreakfastShowText", "TavernKitchenBreakfastHearDialogue:")

    assert "\n    while True:\n" in hub
    assert "\n        menu:\n" in hub
    assert "MenuItem(" not in hub
    assert "ReturnToMainUI" not in hub
    assert "QueuePagedPanelText" not in source
    assert "tavern_breakfast_menu_items" not in source
    assert "build_breakfast_text_pages" not in source
    assert "TavernKitchenBreakfastTextPage" not in source
    assert "return_label" not in show_text
    assert "jump expression" not in show_text
    assert "\n    return\n" in show_text

    player_source = (ROOT / "game/Utilities/General/Player/Player.rpy").read_text(encoding="utf-8-sig")
    sync_source = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for stale_name in ("text_pages", "text_page_index", "text_return_label"):
        assert stale_name not in player_source
        assert stale_name not in sync_source
