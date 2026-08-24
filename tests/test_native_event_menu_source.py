from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_tavern_fight_event_owns_native_choices_and_returns_to_caller():
    source = _source("game/Utilities/Fight/EventFightSmall.rpy")
    assert "menu:" in source
    assert "main_ui_runtime.action_items" not in source
    assert "EventFightSmallApply" not in source
    assert "jump TavernMain" not in source
    assert "label EventFightSmallFinish(" in source


def test_ellona_inspection_uses_native_menus_without_apply_dispatchers():
    source = _source("game/Town/Temple/EllonaTempleMenu.rpy")
    assert source.count("menu:") == 2
    assert "main_ui_runtime.action_items" not in source
    assert "MenuApply" not in source
    assert "while True:" not in source
    assert "jump PortStreets" not in source
    assert "label EllonaTemplePasiphaeaPortrait:" in source
    assert "label EllonaTempleThaliaPortrait:" in source


def test_ellona_rooms_do_not_recursively_reenter_after_main_ui():
    source = _source("game/Town/Temple/EllonaTemple.rpy")

    assert "_ellona_temple_ui_return" not in source
    assert "_ellona_birth_ui_return" not in source
    assert source.count("while True:\n        call screen main_ui") == 2
    assert source.count("call screen main_ui") == 2
    assert "jump EllonaBirthRoom" not in source


def test_social_topics_use_native_menu_inside_main_ui_without_action_dispatcher():
    source = _source("game/Utilities/General/NPC/SocialTalkTopics.rpy")
    menu_source = source.split("label SocialTalkTopicMenu", 1)[1]
    assert "menu:" in menu_source
    assert '$ _social_parent_mode = str(main_ui_runtime.mode or "scene")' in menu_source
    assert 'if _social_parent_mode != "talk":' in menu_source
    assert "main_ui_begin_talk_state" in menu_source
    assert "main_ui_end_talk_state" in menu_source
    assert "renpy.display_menu" not in menu_source
    assert "main_ui_runtime.action_items" not in menu_source
    assert "SocialTalkTopicApply" not in source
    assert "def social_core_action_items" not in source
    assert '_social_topic_id=""' in source.split("label SocialTalkTopicMenu", 1)[1].split(":", 1)[0]


def test_live_game_has_no_detached_display_menu_or_global_result_scratch():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    assert "renpy.display_menu" not in runtime
    assert "call screen choice" not in runtime
    assert "default Result =" not in runtime


def test_native_choice_replaces_underlying_main_ui_action_panel():
    source = _source("game/Utilities/General/Screens/main_layout.rpy")
    panel = source.split("screen current_action_panel():", 1)[1].split("screen main_ui_status_item", 1)[0]
    assert 'if renpy.get_screen("choice") is not None:' in panel
    assert panel.index('if renpy.get_screen("choice") is not None:') < panel.index("elif main_ui_runtime.action_items:")


def test_unused_legacy_dress_catalog_is_removed():
    assert not (ROOT / "game/Utilities/General/Clothes/CreateDressListMenu.rpy").exists()
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    for legacy_label in (
        "CreateDressListMenu",
        "MaleDressShop",
        "male_dress_shop",
        "FemaleDressShop",
        "female_dress_shop",
    ):
        assert legacy_label not in runtime


def test_called_dress_purchase_helpers_return_to_their_scene_owner():
    source = _source("game/NPC/Girls/Common/GirlSuggestDressFunc.rpy")
    pay_source = source.split('label GirlDressBuyPay(', 1)[1].split('label GirlDressBuyPregRemark', 1)[0]
    assert "jump ArtisansQuarter" not in pay_source
    assert "return" in pay_source
    assert "RandVar" not in source
    assert "rand_var=0" in source


def test_amanda_liza_reaction_menu_owns_consequences_and_returns_to_caller():
    source = _source("game/NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy")

    assert "menu:" in source
    assert "EventAmandaLizettTalk2Apply" not in source
    assert "jump TavernMain" not in source
    assert 'Amanda.set_var_int("prohibitliza", 2)' in source
    assert 'Amanda.set_var_int("prohibitliza", 1)' in source
    assert 'Amanda.set_var_int("prohibitliza", 0)' in source
    assert "YourReaction2" not in source


def test_small_fight_menu_uses_label_local_event_scratch():
    source = _source("game/Utilities/Fight/EventFightSmall.rpy")

    assert 'label EventFightSmall(eyewitness=0, CurMoneyLoss=0, FightRand=0, PhraseEnd1EFS="", CurEventDesc=""' in source
    assert "$ YourReaction1 =" not in source


def test_legacy_card_overlay_screens_are_removed_from_live_runtime():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    for screen_name in (
        "player_card_overlay",
        "girl_card_overlay",
        "dog_card_overlay",
        "werecat_card_overlay",
    ):
        assert screen_name not in runtime


def test_clara_tavern_visit_events_do_not_author_room_action_state():
    source = _source("game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy")
    assert "main_ui_runtime.action_items" not in source
    assert "main_ui_runtime.action_content" not in source
    assert "main_ui_runtime.action_title" not in source


def test_story_labels_with_native_menus_keep_choices_inside_main_ui():
    violations = []
    label_pattern = re.compile(
        r"(?ms)^label\s+(story_[A-Za-z0-9_]+)(?:\([^\r\n]*\))?:[ \t]*\r?\n(.*?)(?=^label\s+|\Z)"
    )
    for path in (ROOT / "game").rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        for match in label_pattern.finditer(source):
            body = match.group(2)
            if re.search(r"(?m)^\s+menu\s*:", body) and not re.search(
                r"(?m)^\s+show screen main_ui\s*$", body
            ):
                violations.append(f"{path.relative_to(ROOT)}:{match.group(1)}")

    assert violations == []
