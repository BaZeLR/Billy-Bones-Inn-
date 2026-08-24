from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "game/Utilities/General/Screens/main_layout.rpy"
CARD_FILES = (
    ROOT / "game/Utilities/General/Screens/PlayerCard.rpy",
    ROOT / "game/NPC/Girls/Common/GirlCard.rpy",
    ROOT / "game/NPC/Secondary/DogCompanion.rpy",
    ROOT / "game/NPC/Secondary/WerecatNPC.rpy",
)


def test_main_ui_cards_restore_their_caller_without_room_reentry():
    layout = LAYOUT.read_text(encoding="utf-8-sig")
    assert "self.card_origin = None" in layout
    assert "def main_ui_begin_card_state():" in layout
    assert "def main_ui_end_card_state():" in layout
    assert 'style "mui_hud_button"' in layout
    assert 'text_style "mui_hud_button_text"' in layout
    assert "main_ui_player_card_back_button" not in layout
    assert "main_ui_girl_card_back_button" not in layout
    assert "main_ui_dog_card_back_button" not in layout
    assert "main_ui_werecat_card_back_button" not in layout

    for path in CARD_FILES:
        source = path.read_text(encoding="utf-8-sig")
        assert "main_ui_begin_card_state()" in source
        assert 'Jump(str(CurLoc or getattr(CurrentRoom' not in source

    player_card = CARD_FILES[0].read_text(encoding="utf-8-sig")
    assert 'Jump(str(CurLoc or ""))' not in player_card
    assert 'MenuItem("Назад", Function(main_ui_end_card_state))' in player_card

    girl_card = CARD_FILES[1].read_text(encoding="utf-8-sig")
    assert 'main_ui_runtime.action_title = "Действия"' in girl_card
    assert "renpy.store" not in girl_card
    assert 'main_ui_runtime.action_items = [MenuItem("Назад", Function(main_ui_end_card_state))]' in girl_card


def test_player_inventory_and_fixed_target_social_panels_stay_inside_main_ui():
    layout = LAYOUT.read_text(encoding="utf-8-sig")
    player_card = CARD_FILES[0].read_text(encoding="utf-8-sig")

    assert 'elif str(main_ui_runtime.mode or "") == "event":' in layout
    assert 'elif main_ui_runtime.action_content:' in layout
    assert 'if str(main_ui_runtime.mode or "scene") == "mc":' in layout
    assert "back_label" not in player_card
    assert "back_args" not in player_card
    assert "call_in_new_context" not in player_card
    assert "call screen main_ui as player_card_fixed_target_interaction" in player_card
    assert "[Function(main_ui_end_card_state), Return()]" in player_card
