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


def test_breakfast_entry_shows_one_paragraph_per_continue_beat():
    source = SOURCE.read_text(encoding="utf-8-sig")
    entry = _label_block(source, "TavernKitchenBreakfast:", "TavernKitchenBreakfastMenu:")

    assert 'scene_runtime.text = "\\n\\n".join' not in entry
    assert 'scene_runtime.text = _breakfast_lines[_breakfast_line_index]' in entry
    assert 'while _breakfast_line_index < len(_breakfast_lines):' in entry
    assert entry.count('"\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c":') == 1
    assert '_breakfast_lines.append(str(_eat_result.get("text", "") or "").strip())' in entry
    assert '_breakfast_lines.append("\u0421\u043e\u0432\u043c\u0435\u0441\u0442\u043d\u044b\u0439 \u0437\u0430\u0432\u0442\u0440\u0430\u043a' in entry
    assert 'player.tavern_management.breakfast.base_text = str(scene_runtime.text or "")' in entry
