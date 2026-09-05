from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_marketplace_keeps_authored_hours_and_blind_pirate_scene():
    source = (ROOT / "game/Town/Market/MarketPlace.rpy").read_text(encoding="utf-8-sig")

    assert 'start="06:00"' in source
    assert 'end="18:59"' in source
    assert 'MARKETPLACE_CLOSED_PICTURE = "images/market/LocMarketPlaceClosed.jpg"' in source
    assert "одна совсем молоденькая, другая постарше" in source
    assert "галеры герцогини Кончиты" in source


def test_authored_reconciliation_paths_remain_reachable():
    melissa = (ROOT / "game/NPC/Girls/Melissa/IntMelissaTalk.rpy").read_text(encoding="utf-8-sig")
    sandra = (ROOT / "game/NPC/Girls/Sandra/IntSandraTalk.rpy").read_text(encoding="utf-8-sig")

    assert '"Попробовать помириться с Мелиссой" if int(Melissa.talked_today or 0) < 3 and int(Melissa.rel or 0) < 5:' in melissa
    assert "label IntMelissaTalkApply" not in melissa
    assert "label IntMelissaStartApply" not in melissa
    assert "label IntMelissaRoomProblemAdviceApply" not in melissa
    assert "main_ui_runtime.action_items" not in melissa
    assert "MenuItem(" not in melissa
    assert "menu:" in melissa
    assert "call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)" in melissa
    assert "$ Melissa.mark_talked()" in melissa
    assert "Вы подошли к Мелиссе и извинились" in melissa
    assert "сказала, что ценит вас и все понимает" in melissa
    assert '"Попробовать помириться с Сандрой" if int(Sandra.talked_today or 0) < 3 and int(Sandra.rel or 0) < 5:' in sandra
    assert "call IntSandraReconcile(girl_name)" in sandra
    reconcile = sandra.split('label IntSandraReconcile(girl_name="sandra"):', 1)[1].split("label IntSandraHouseholdInsight", 1)[0]
    assert "Вы подошли к Сандре и извинились" in reconcile
    assert "Сандра благосклонно выслушала вас" in reconcile
    assert "Сандра холодно выслушала вас" in reconcile
    assert "мам" not in reconcile.lower()
    assert "она всегда будет вас любить" in sandra


def test_system_threads_are_not_mistaken_for_npcs():
    source = (ROOT / "game/Utilities/General/Events/conditions.rpy").read_text(encoding="utf-8-sig")
    gate = source.split("def _story_level_enabled", 1)[1].split("def _story_current_location", 1)[0]

    assert "person_info = people.get_info(person_key)" in gate
    assert "if person_info is not None:" in gate
    assert 'person_key not in ("event", "story", "system")' not in gate


def test_runtime_contains_no_fake_compatibility_stub_files():
    assert not (ROOT / "game/StubFunctions.rpy").exists()
    assert not (ROOT / "game/Utilities/General/Common/missing_functions.rpy").exists()

    bar = (ROOT / "game/Inn/TavernMainBar001.rpy").read_text(encoding="utf-8-sig")
    assert "TavernMainBarPlaceholderEvent" not in bar
    assert 'target="TavernMainBarListenEvent"' not in bar
    assert "label TavernMainBarListenEvent:" not in bar


def test_media_python_api_has_no_legacy_uppercase_wrapper():
    media = (ROOT / "game/Utilities/General/Screens/ShowImage.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_lines = [
        line.strip()
        for path in (ROOT / "game").rglob("*.rpy")
        for line in path.read_text(encoding="utf-8-sig").splitlines()
    ]

    assert "def show_image_seq(" in media
    assert "def ShowImage(" not in media
    assert "def ShowImageSeq(" not in media
    for line in game_lines:
        if "ShowImage(" in line or "ShowImageSeq(" in line:
            assert line.startswith("call ") or line.startswith("label ")


def test_pregnancy_python_api_has_no_legacy_uppercase_wrapper():
    pregnancy = (ROOT / "game/NPC/Girls/Common/PregnancyCheck.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_lines = [
        line.strip()
        for path in (ROOT / "game").rglob("*.rpy")
        for line in path.read_text(encoding="utf-8-sig").splitlines()
    ]

    assert "def pregnancy_check(" in pregnancy
    assert "def PregnancyCheck(" not in pregnancy
    for line in game_lines:
        if "PregnancyCheck(" in line:
            assert line.startswith("call ") or line.startswith("label ")
