from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_forest_return_and_help_page_are_room_owned():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    assert 'rooms.get(\"Forest\").state.get("return_target"' in runtime
    assert 'SetDict(rooms.get(\"Forest\").state, "return_target"' in runtime
    assert 'rooms.get(\"TavernHelp\").state["page"]' in runtime
    assert '$ _book = TavernHelpBookItem' in runtime
    assert '_book.state.get("stash_taken"' in runtime
    for legacy_name in ("ForestReturnTarget", "TavernHelpPage", "CheatMoneyGrab", "RobbersHeadNameTmp"):
        assert legacy_name not in runtime


def test_navigation_help_has_no_legacy_save_authority():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in ("ForestReturnTarget", "TavernHelpPage", "CheatMoneyGrab", "RobbersHeadNameTmp"):
        assert legacy_name not in migration


def test_disabled_navigation_only_parallel_flow_is_removed():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    for legacy_name in (
        "navigation_only_mode_enabled",
        "navigation_only_message",
        "navigation_only_time_note",
        "NAVIGATION_ONLY_MODE",
    ):
        assert legacy_name not in runtime


def test_tavern_help_uses_native_reading_menu_without_apply_loop():
    source = (ROOT / "game/Inn/TavernHelp.rpy").read_text(encoding="utf-8-sig")
    read_flow = source.split("label TavernHelpReadPage:", 1)[1]
    assert "menu:" in read_flow
    assert "while True:" not in read_flow
    assert "TavernHelpApply" not in source
    assert "label TavernHelpShowPage:" not in source
    assert "label TavernHelpTakeStash:" not in source
    assert "call screen main_ui" not in source
    assert "main_ui_runtime.action_items.append" not in source
    assert '$ _book = TavernHelpBookItem' in read_flow
    assert '_book.state.get("stash_taken"' in read_flow


def test_tavern_help_book_has_one_registered_state_owner():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    assert runtime.count('object_id="book_001"') == 1
    assert "TavernMainBookObject" not in runtime
    assert not (ROOT / "game/Inn/TavernMainBook001.rpy").exists()


def test_current_room_code_has_no_location_global_mirror():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    assert "$ location = CurLoc" not in runtime
    assert "CurLoc or location" not in runtime
    assert "default current_room_code" not in runtime
    assert "global current_room_code" not in runtime
