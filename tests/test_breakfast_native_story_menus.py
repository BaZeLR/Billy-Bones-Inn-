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
    assert '"[scene_runtime.text]"' not in show_text
    assert '"Продолжить":' in show_text
    assert "\n    menu:\n" in show_text
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


def test_finishing_resumed_breakfast_reenters_the_kitchen_room():
    source = SOURCE.read_text(encoding="utf-8-sig")
    menu = _label_block(
        source,
        "TavernKitchenBreakfastMenu:",
        "TavernKitchenBreakfastShowText",
    )
    finish = menu.split('"Закончить завтрак":', 1)[1]

    assert "call TavernKitchenFinishBreakfastEvent" in finish
    assert "jump TavernKitchen" in finish
    assert "return" not in finish


def test_melissa_amanda_breakfast_story_replaces_each_paragraph_in_main_ui():
    source = SOURCE.read_text(encoding="utf-8-sig")
    opening = _label_block(
        source,
        "TavernKitchenBreakfastMelissaAmandaGerhard:",
        "TavernKitchenBreakfastMelissaAmandaGerhardNatural:",
    )
    response = _label_block(
        source,
        "TavernKitchenBreakfastMelissaAmandaGerhardNatural:",
        "TavernKitchenBreakfastAmandaAtticStop:",
    )

    assert "_breakfast_story_lines[_breakfast_story_line_index]" in opening
    assert "_breakfast_response_lines[_breakfast_response_line_index]" in response
    assert "while _breakfast_story_line_index < len(_breakfast_story_lines):" in opening
    assert "while _breakfast_response_line_index < len(_breakfast_response_lines):" in response
    assert '"[scene_runtime.text]"' not in opening
    assert '"[scene_runtime.text]"' not in response
    assert "\\n\\n" not in opening
    assert "\\n\\n" not in response
    assert opening.count('"Продолжить":') == 1
    assert response.count('"Продолжить":') == 1


def test_solved_rat_problem_cannot_emit_breakfast_kitty_dialogue():
    source = SOURCE.read_text(encoding="utf-8-sig")
    dialogue = source.split("def tavern_breakfast_dialogue_lines():", 1)[1].split(
        "def tavern_breakfast_apply_social_bonus():", 1
    )[0]

    assert 'rat_problem = int(werecat_state().get("rats_problem_active", 0) or 0) == 1' in dialogue
    assert 'next_day_runtime.current_day.get("rat_food_loss"' not in dialogue
    kitty_line = 'lines.append("\\\"Крысы?\\\" Аманда пожимает плечом.'
    assert kitty_line in dialogue
    assert dialogue.index("if rat_problem:", dialogue.index('if "amanda" in present_ids:')) < dialogue.index(kitty_line)


def test_breakfast_flirts_cover_household_girls_and_complete_at_chosen_place():
    source = SOURCE.read_text(encoding="utf-8-sig")
    sandra_source = (ROOT / "game/NPC/Girls/Sandra/InitSandra.rpy").read_text(encoding="utf-8-sig")
    migration_source = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    candidate = source.split("def tavern_breakfast_tease_candidate():", 1)[1].split(
        "def tavern_breakfast_tease_ready():", 1
    )[0]
    private_date = _label_block(
        source,
        "TavernKitchenBreakfastTeasePrivate(girl_name=\"\", place_code=\"storage\"):",
        "TavernKitchenBreakfastTalkAbsent:",
    )

    assert 'npc_id not in ("sandra", "amanda", "melissa")' in candidate
    assert "if info is None or not info.date_intimacy_available():" in candidate
    assert 'getattr(info, "breakfast_tease_day", -1)' in candidate
    tease = _label_block(source, "TavernKitchenBreakfastTease:", "TavernKitchenBreakfastTeasePrivate")
    assert "_tease_private_unlocked" not in tease
    assert 'call TavernKitchenBreakfastTeasePrivate(_tease_girl, "storage")' in tease
    assert 'call TavernKitchenBreakfastTeasePrivate(_tease_girl, "shed")' in tease
    assert 'call TavernKitchenBreakfastTeasePrivate(_tease_girl, "player_room")' in tease
    assert 'call TavernKitchenBreakfastOutdoorDate(_tease_girl, "lake")' in tease
    assert 'call TavernKitchenBreakfastOutdoorDate(_tease_girl, "horse")' in tease
    assert "self.breakfast_tease_day = -1" in sandra_source
    assert '"flirt": ["images/sandra/thanks/sandra_thanks.webm"]' in sandra_source
    assert 'return SandraStaticData.image_path("breakfast", "flirt")' in source
    assert 'if not hasattr(Sandra, "breakfast_tease_day"):' in migration_source
    assert "Sandra.breakfast_tease_day = -1" in migration_source
    assert '$ _tease_private_room = "TavernStorage"' in private_date
    assert '$ _tease_private_room = "Shed"' in private_date
    assert '$ _tease_private_room = "TavernMyRoom"' in private_date
    assert "call TavernKitchenFinishBreakfastEvent" in private_date
    assert private_date.count("call HouseholdSexEngine(_tease_private_girl, _tease_private_room)") == 2
    assert "call IntAmandaSex(_tease_private_girl, _tease_private_room)" in private_date
    assert "if _tease_private_elapsed_minutes < 30:" in private_date
    assert "calendar_v2.advance_minutes(30 - _tease_private_elapsed_minutes)" in private_date
    assert '"Продолжить свидание":' in private_date
    assert '"Закончить свидание":' in private_date
    assert 'label TavernKitchenBreakfastOutdoorDate(girl_name="", date_code="lake"):' in private_date
    assert 'player.horse.owns_horse()' in private_date
    assert "daily_events" not in private_date
