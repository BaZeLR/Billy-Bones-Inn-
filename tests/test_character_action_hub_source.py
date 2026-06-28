from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "game" / "Utilities" / "General" / "NPC" / "CharacterActionHub.rpy"
DOG = ROOT / "game" / "NPC" / "Secondary" / "DogCompanion.rpy"
MAIN_LAYOUT = ROOT / "game" / "Utilities" / "General" / "Screens" / "main_layout.rpy"
ROOM_TEMPLATE = ROOT / "game" / "Utilities" / "General" / "Classes" / "RoomTemplate.rpy"


def _source():
    return HUB.read_text(encoding="utf-8-sig")


def _game_sources():
    for path in (ROOT / "game").rglob("*.rpy"):
        yield path, path.read_text(encoding="utf-8-sig")


def test_action_hub_uses_people_info_var_not_legacy_var_router():
    source = _source()
    state_block = source.split("def npc_unique_state", 1)[1].split("def _npc_explicit_picture", 1)[0]

    assert "getPersonInfo" in state_block
    assert 'getattr(info, "var", None)' in state_block
    for token in ["AmandaVar", "MelissaVar", "SandraVar", "ClaraVar", "BeckyVar", "GeorgettVar", "LizaVar", "IrmaVar"]:
        assert token not in state_block


def test_action_hub_has_one_npc_menu_builder_path():
    source = _source()
    main_layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    dog_source = DOG.read_text(encoding="utf-8-sig")
    room_template = ROOM_TEMPLATE.read_text(encoding="utf-8-sig")
    opener_block = source.split("def open_npc_action_menu_state", 1)[1].split("def npc_action_data", 1)[0]

    assert "normalized = npc_action_data(npc_id, where_id, entity_data)" in opener_block
    assert "def _normalize_entity_action_data" not in source
    assert "def _character_action_text" not in source
    assert "def _character_action_display_name" not in source
    assert "def entity_knows_mc" not in source
    assert "def _entity_unknown_title" not in source
    assert "def entity_presented_name" not in source
    assert "def _entity_action_can_examine" not in source
    assert "def _character_action_entity_talk_args" not in source
    assert "def _character_action_grid_entries" not in source
    assert "def open_entity_action_menu_state" not in source
    assert "def action_menu_handle_talk_state" not in source
    assert "def action_menu_handle_look_state" not in source
    assert "def show_entity_examine_main_ui_state" not in source
    assert "action_menu_entity_" not in source
    assert "action_menu_entity_" not in main_layout
    assert "store.action_menu_entity_type" not in opener_block
    assert "store.action_menu_specs" not in source
    assert "store.action_menu_actions" not in source
    assert "default action_menu_specs" not in source
    assert "default action_menu_actions" not in source
    assert "def action_menu_handle_back_state" not in source
    assert "label ActionMenuHandleBack" not in source
    assert "label OpenEntityActionMenu" not in source
    assert "label OpenNpcActionMenu" not in source
    assert "label NpcActionTalk" not in source
    assert "label NpcActionLook" not in source
    assert "label ActionMenuHandleTalk" not in source
    assert "label ActionMenuHandleLook" not in source
    assert "ActionMenuRunSpec" not in source
    assert "ActionMenuRunSpec" not in main_layout
    assert "screen npc_action_menu" not in main_layout
    assert "main_ui_entity_button_spec" not in main_layout
    assert 'Call("OpenEntityActionMenu"' not in main_layout
    assert 'Call("OpenNpcActionMenu"' not in main_layout
    assert "action_menu_specs" not in main_layout
    assert "action_menu_actions" not in main_layout
    assert "_character_action_grid_entries" not in main_layout
    assert "_room.visible_npcs()" in main_layout
    for checked_source in (source, main_layout, dog_source, room_template):
        assert "globals()" not in checked_source
        assert "renpy.store" not in checked_source
        assert "renpy_pkg.store" not in checked_source
        assert "renpy_module.store" not in checked_source
    visible_npcs_block = room_template.split("def visible_npcs", 1)[1].split("def visible_actions", 1)[0]
    assert "_npc_known_ids()" in visible_npcs_block
    assert "getLocation(npc_key)" in visible_npcs_block
    assert "getNPCids(" not in visible_npcs_block
    assert "npc_action_data_for_room" not in visible_npcs_block
    assert '"talk_label"' not in visible_npcs_block
    assert '"actions"' not in visible_npcs_block
    for path, game_source in _game_sources():
        assert "OpenEntityActionMenu" not in game_source, path
        assert "OpenNpcActionMenu" not in game_source, path
        assert "ActionMenuHandleTalk" not in game_source, path
        assert "ActionMenuHandleLook" not in game_source, path
        assert "_normalize_entity_action_data" not in game_source, path
        assert "entity_presented_name" not in game_source, path


def test_action_hub_uses_direct_menu_actions_not_spec_dispatcher():
    source = _source()
    menu_block = source.split("def open_npc_action_menu_state", 1)[1].split("def npc_action_data", 1)[0]

    assert "menu_specs" not in menu_block
    assert 'Call("ActionMenuRunSpec"' not in menu_block
    assert 'Function(NpcActionTalkState' in menu_block
    assert 'Function(NpcActionLookState' in menu_block
    assert 'Call("SocialTalkTopicMenu"' in menu_block


def test_end_talk_jumps_to_current_room_label():
    main_layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    end_talk_block = main_layout.split("def main_ui_end_talk_state", 1)[1].split("def main_ui_begin_native_scene_state", 1)[0]
    end_scene_block = main_layout.split("def main_ui_end_native_scene_state", 1)[1].split("def tractir_after_load_restore_ui", 1)[0]

    for block in (end_talk_block, end_scene_block):
        assert 'str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()' in block
        assert "renpy_module.jump(room_label)" in block


def test_action_hub_does_not_guess_npc_pictures_from_room_tokens():
    source = _source()

    assert "_character_action_room_picture_tokens" not in source
    assert "_character_action_picture_files" not in source
    assert "media_hints" not in source
    assert "room_hint_map" not in source
    assert "best_score" not in source
    assert "renpy.list_files" not in source


def test_dog_action_data_belongs_to_dog_runtime():
    hub_source = _source()
    dog_source = DOG.read_text(encoding="utf-8-sig")

    assert "def dog_action_data" not in hub_source
    assert "def DogActionTalkState" not in hub_source
    assert "def DogActionLookState" not in hub_source
    assert "def open_dog_action_menu_state" not in hub_source
    assert "dog_main_ui_action_items" not in hub_source
    assert "show_dog_card_main_ui_state" not in hub_source
    assert "dog_card_portrait_path" not in hub_source
    assert "def dog_action_data" in dog_source
    assert "def dog_action_talk_state" in dog_source
    assert "def dog_action_look_state" in dog_source
    assert "def dog_open_action_menu_state" in dog_source
    assert '"talk_label": "IntDogTalk"' in dog_source
