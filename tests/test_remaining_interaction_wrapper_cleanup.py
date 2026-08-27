from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_irma_talk_uses_native_menu_without_dispatch_layers():
    source = read("game/NPC/Girls/Irma/IntIrmaTalk.rpy")
    topics = read("game/Utilities/General/NPC/SocialTalkTopics.rpy")
    assert "label IntIrmaTalkMenu:" not in source
    assert "while True:" in source
    assert "jump IntIrmaTalkMenu" not in source
    assert "menu:" in source
    assert "def irma_talk_action_items():" not in source
    assert "IntIrmaTalkApply" not in source
    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert "IntIrmaTalkRefresh" not in source + topics
    assert "if _irma_talk_new:" in source
    assert "jump IntIrmaTalk" not in source
    assert "social_topic_return_label" not in topics
    for choice in ("Осмотреть", "Спросить, когда будет готово", "Спросить про теплые плащи и постели", "Заказать теплый меховой плащ", "Заказать меховую постель"):
        assert '"%s"' % choice in source


def test_melissa_dress_change_has_no_one_screen_refresh_wrapper():
    source = read("game/NPC/Girls/Melissa/IntMelissaDressChange.rpy")
    assert "IntMelissaDressChangeRefresh" not in source
    assert 'label IntMelissaDressChange(GirlNameIMT="melissa"):' in source
    assert "menu:" not in source
    assert "IntMelissaDressChangeApply" not in source
    assert "main_ui_runtime.action_items" not in source
    assert "$ daily_events.add(" in source
    assert "$ Melissa.mark_talked()" in source


def test_georgett_talk_has_native_menu_without_action_builder():
    source = read("game/NPC/Girls/Georgett/IntGeorgettTalk.rpy")
    topics = read("game/Utilities/General/NPC/SocialTalkTopics.rpy")
    assert "label IntGeorgettTalkMenu:" not in source
    assert "while True:" in source
    assert "jump IntGeorgettTalkMenu" not in source
    assert "menu:" in source
    assert "def georgett_talk_action_items(" not in source
    assert "label IntGeorgettTalkApply" not in source
    assert "choice_code" not in source
    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert "IntGeorgettTalkRefresh" not in source + topics
    assert "IntGeorgettTalkRestore" not in source
    assert "if _georgett_talk_new:" in source
    assert "jump IntGeorgettTalk" not in source
    assert "social_topic_return_label" not in topics
    for moved_choice in ("smalltalk", "ask_clients", "ask_sex", "ask_family", "ask_pregnancy", "ask_kids", "ask_gerhard", "tell_liza_gerhard", "invite_tavern", "ask_work", "ask_pirate", "gloryhole_terms", "talk_eddie", "sponsor_eddie_home", "ask_eddie_visit", "hire", "grope", "ask_dad", "dress"):
        assert f'IntGeorgettTalkApply(girl_name, girl_loc, "{moved_choice}")' not in source


def test_dress_buy_suggestion_flow_has_no_refresh_restore_or_boolean_protocol():
    buy = read("game/NPC/Girls/Common/GirlDressBuy.rpy")
    suggest = read("game/NPC/Girls/Common/GirlDressSuggest.rpy")
    source = buy + suggest
    assert "GirlDressBuyRefresh" not in source
    assert "GirlDressSuggestRestore" not in source
    assert "_girl_dress_restore_buy_menu" not in source
    assert "should_restore" not in source
    assert "GirlDressBuyReturnFromSuggestion" not in source
    assert "girl_dress_buy_actions(GirlName)" in buy
    assert "$ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)" in suggest


def test_called_object_menus_restore_hud_without_reentering_rooms():
    cases = (
        ("game/Forest/Forest.rpy", "ForestObjectMenu", "Forest"),
        ("game/Inn/Backyard.rpy", "BackyardObjectMenu", "Backyard"),
        ("game/Inn/TavernAmandaRoom.rpy", "tavern_amanda_room_object_menu", "TavernAmandaRoom"),
        ("game/Inn/TavernAtic.rpy", "TavernAticObjectMenu", "TavernAtic"),
        ("game/Inn/TavernEmptyRoom.rpy", "TavernEmptyRoomObjectMenu", "TavernEmptyRoom"),
        ("game/Inn/TavernMain.rpy", "TavernMainObjectMenu", "TavernMain"),
        ("game/Inn/TavernMelissaRoom.rpy", "TavernMelissaRoomObjectMenu", "TavernMelissaRoom"),
        ("game/Inn/TavernMyRoom.rpy", "TavernMyRoomObjectMenu", "TavernMyRoom"),
        ("game/Inn/TavernSandraRoom.rpy", "TavernSandraRoomObjectMenu", "TavernSandraRoom"),
        ("game/Inn/TavernStable.rpy", "tavern_stable_object_menu", "TavernStable"),
        ("game/Town/Arts/ArtisansQuarter.rpy", "ArtisansQuarterObjectMenu", "ArtisansQuarter"),
        ("game/Town/BeckyHome.rpy", "BeckyHomeObjectMenu", "BeckyHome"),
    )

    for relative, label_name, room_label in cases:
        source = read(relative)
        block = source.split(f"label {label_name}", 1)[1].split("\nlabel ", 1)[0]
        assert f"jump {room_label}" not in block
        assert f'Jump("{room_label}")' not in block
        assert "main_ui_runtime.action_items" in block


def test_in_room_submenus_restore_actions_without_room_jumps():
    cases = (
        ("game/Forest/Forest.rpy", "ForestSubroomSpawnedItemMenu", "Forest"),
        ("game/Inn/TavernKitchen.rpy", "TavernKitchenDepositMenu", "TavernKitchen"),
        ("game/Inn/TavernKitchenHearth001.rpy", "TavernKitchenHearthMenu", "TavernKitchen"),
        ("game/Inn/TavernKitchenCauldron001.rpy", "TavernKitchenCauldronMenu", "TavernKitchen"),
        ("game/Inn/TavernEmptyRoom.rpy", "TavernEmptyRoomPeekEmpty", "TavernEmptyRoom"),
    )
    for relative, label_name, room_label in cases:
        source = read(relative)
        block = source.split(f"label {label_name}", 1)[1].split("\nlabel ", 1)[0]
        assert f'Jump("{room_label}")' not in block
        assert "main_ui_restart_interaction" in block


def test_recipe_book_closes_to_its_object_without_return_state_mirrors():
    source = read("game/Items/Core/CraftingRecipes.rpy")

    assert "return_room_code" not in source
    assert "return_object_id" not in source
    assert "return_picture" not in source
    assert "recipe_book_restore_picture" not in source
    assert "jump expression where_id" not in source
    close_block = source.split("label RecipeBookClose", 1)[1]
    assert 'call TavernAticObjectMenu(object_id or "recipe_book_001")' in close_block
    assert "jump expression" not in close_block


def test_gameplay_ui_actions_do_not_start_detached_renpy_contexts():
    sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "call_in_new_context" not in sources


def test_item_consumption_uses_direct_action_labels_without_apply_dispatcher():
    source = read("game/Utilities/General/Common/Actions.rpy")

    assert "ApplyItemAction" not in source
    assert "player_apply_item_action" not in source
    assert '"drink": {"hook": "call", "target": "Drink"' in source
    assert '"eat": {"hook": "call", "target": "EatItem"' in source
    assert 'label Drink(what_id="", where_id="", fallback_text="", object_id=""):' in source
    assert 'label EatItem(what_id="", where_id="", fallback_text="", object_id=""):' in source


def test_old_point_system_no_longer_duplicates_authoritative_smalltalk():
    old_point = read("game/NPC/Girls/Common/OldPointTalkSystem.rpy")
    amanda = read("game/NPC/Girls/Amanda/IntAmandaTalk.rpy")

    assert "old_point_smalltalk" not in old_point
    assert "OldPointSmallTalkMenu" not in old_point
    assert 'call SocialTalkTopicMenu(girl_name, "talk")' in amanda


def test_tavern_report_actions_call_job_owners_without_dispatch_labels():
    source = read("game/Inn/menu_tavernstat.rpy")
    layout = read("game/Utilities/General/Screens/main_layout.rpy")

    assert "TavernReportApplyAction" not in source + layout
    assert "TavernReportApplyOverviewAction" not in source + layout
    assert "Function(toggle_hall_job_with_limit" in source
    assert "Function(assign_special_job" in source
    report_panel = layout.split("screen main_ui_tavern_report_panel():", 1)[1]
    assert 'text "Завтрашняя смена"' in report_panel
    assert 'Function(toggle_hall_job_with_limit, "jobkitchentomorrow", _worker)' in report_panel
    assert 'Function(toggle_hall_job_with_limit, "jobcleaningtomorrow", _worker)' in report_panel
    assert 'Function(toggle_hall_job_with_limit, "jobwaitresstomorrow", _worker)' in report_panel
    assert 'toggle_hall_job_with_limit, "jobkitchentomorrow", _worker, 2' not in report_panel


def test_inga_talk_and_dress_topics_have_no_one_call_alias_labels():
    inga = read("game/NPC/Girls/Inga/IntIngaTalk.rpy")
    liza = read("game/NPC/Girls/Liza/IntLizaTalk.rpy")
    georgett = read("game/NPC/Girls/Georgett/IntGeorgettTalk.rpy")

    assert "menu:" in inga
    assert "main_ui_runtime.action_items" not in inga
    assert "label int_inga_talk" not in inga
    assert "label IntLizaTalkDress" not in liza
    assert "call IntLizaDressChange(girl_name_ilt)" in liza
    assert "GirlNameILT" not in liza
    assert "GirlLocILT" not in liza
    assert "jump IntLizaTalk" not in liza
    assert "while True:" in liza
    assert "label IntGeorgettDress(" not in georgett
    assert "call IntGeorgettDressChange(girl_name)" in georgett


def test_amanda_dress_change_uses_semantic_event_procedures_without_dispatch_or_loop():
    source = read("game/NPC/Girls/Amanda/IntAmandaDressChange.rpy")

    assert "IntAmandaDressChangeApply" not in source
    assert "choice_code" not in source
    assert "while True:" not in source
    for label_name in (
        "IntAmandaDressChangeOfferBra",
        "IntAmandaDressChangeOfferPanties",
        "IntAmandaDressChangeShameBra",
        "IntAmandaDressChangeShamePanties",
        "IntAmandaDressChangeBuyDress",
    ):
        assert f"label {label_name}" in source
        assert f"call {label_name}(GirlNameIAT)" in source


def test_core_sex_action_menus_iterate_without_recursive_self_jumps():
    cases = (
        ("game/NPC/Girls/Amanda/IntAmandaSex.rpy", "int_amanda_sex_menu"),
        ("game/NPC/Girls/Becky/IntBeckySex.rpy", "int_becky_sex_menu"),
        ("game/NPC/Girls/Liza/IntLizaSex.rpy", "int_liza_sex_menu"),
        ("game/NPC/Girls/Melissa/IntMelissaSex.rpy", "int_melissa_sex_menu"),
        ("game/NPC/Secondary/IntEddieBeckySex.rpy", "int_eddie_becky_sex_menu"),
        ("game/NPC/Girls/Georgett/IntGeorgettSex.rpy", "GeorgettSexMenu"),
    )

    for relative, label_name in cases:
        source = read(relative)
        block = source.split(f"label {label_name}:", 1)[1].split("\n    label ", 1)[0]
        assert "while True:" in block, relative
        assert f"jump {label_name}" not in source, relative
