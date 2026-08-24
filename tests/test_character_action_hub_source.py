from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "game" / "Utilities" / "General" / "NPC" / "CharacterActionHub.rpy"
PEOPLE_RUNTIME = ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
DOG = ROOT / "game" / "NPC" / "Secondary" / "DogCompanion.rpy"
MAIN_LAYOUT = ROOT / "game" / "Utilities" / "General" / "Screens" / "main_layout.rpy"
TALK_OWNERS = {
    "IntAmandaTalk": ROOT / "game/NPC/Girls/Amanda/InitAmanda.rpy",
    "IntClaraTalk": ROOT / "game/NPC/Girls/Clara/InitClara.rpy",
    "IntMelissaTalk": ROOT / "game/NPC/Girls/Melissa/InitMelissa.rpy",
    "IntSandraTalk": ROOT / "game/NPC/Girls/Sandra/InitSandra.rpy",
}


def _runtime_source():
    return PEOPLE_RUNTIME.read_text(encoding="utf-8-sig")


def _game_sources():
    for path in (ROOT / "game").rglob("*.rpy"):
        yield path, path.read_text(encoding="utf-8-sig")


def test_character_action_hub_and_single_npc_card_wrappers_are_removed():
    assert not HUB.exists()

    game_source = "\n".join(source for _, source in _game_sources())
    assert "def npc_action_data_for_room" not in game_source
    for label in (
        "ShowAmandaCard",
        "ShowMelissaCard",
        "ShowSandraCard",
        "ShowClaraCard",
        "ShowBeckyCard",
        "ShowIrmaCard",
    ):
        assert "label %s:" % label not in game_source


def test_visible_npc_buttons_call_npc_owned_talk_labels_directly():
    main_layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")

    assert "open_npc_action_menu_state" not in main_layout
    assert "$ _talk_label =" in main_layout
    assert "$ _talk_args =" in main_layout
    assert "Call(_talk_label, *_talk_args)" in main_layout
    assert "people.ids_at(current_location)" in main_layout
    assert "people.action_data_for_room(npc_key, current_location)" in main_layout


def test_people_registry_selects_npc_owned_action_data_without_owning_talk_flow():
    runtime = _runtime_source()
    registry = runtime.split("class PeopleRegistry(object):", 1)[1].split(
        "def npc_schedule_clock_minute", 1
    )[0]

    assert "def action_data_for_room(self, person=\"\", room_code=\"\"):" in registry
    assert "info = self.get_info(key)" in registry
    assert "not info.interaction_visible(room_key)" in registry
    assert "return info.action_data(room_key)" in registry
    assert "NPC_META" not in registry
    assert "GroceryStore" not in registry
    assert "PortStreets" not in registry
    assert "call_in_new_context" not in registry
    assert "MenuItem(" not in registry


def test_special_talk_labels_stay_distinct_behind_the_same_visible_button_path():
    main_layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    visible_panel = main_layout.split('text "Персонажи"', 1)[1].split(
        'if str(main_ui_runtime.overlay or "") == "story":', 1
    )[0]

    assert "Call(_talk_label, *_talk_args)" in visible_panel
    for talk_label, owner_path in TALK_OWNERS.items():
        assert 'Call("%s"' % talk_label not in visible_panel
        assert 'talk_label = "%s"' % talk_label in owner_path.read_text(encoding="utf-8-sig")


def test_known_state_is_owned_by_talk_labels_not_the_ui_router():
    talk_entries = {
        "game/NPC/Secondary/IntEddieTalk.rpy": ("label IntEddieTalk:", "Eddie.mark_known()"),
        "game/NPC/Girls/Inga/IntIngaTalk.rpy": ("label IntIngaTalk(show_menu=True):", "Inga.mark_known()"),
        "game/NPC/Secondary/IntAlberTalk.rpy": ("label IntAlberTalk:", "Alber.mark_known()"),
        "game/NPC/Secondary/IntDraupnirTalk.rpy": ("label IntDraupnirTalk:", "Draupnir.mark_known()"),
        "game/NPC/Secondary/IntZimmerTalk.rpy": ("label IntZimmerTalk:", "Zimmer.mark_known()"),
        "game/Town/Arts/BarberShop.rpy": ("label BarberShopTalk:", "Sergio.mark_known()"),
        "game/NPC/Secondary/WerecatNPC.rpy": ("label IntWerecatTalk(room_code=\"\"):", "werecat.mark_known()"),
        "game/NPC/Secondary/IntFrancheskaTalk.rpy": ("label FrancheskaTalk:", "Francheska.mark_known()"),
        "game/Town/Market/MarketPlace.rpy": ("label MarketPlaceApproachMongol(mode_code=\"\"):", "Mongol.mark_known()"),
        "game/NPC/Secondary/IntRobinTalk.rpy": ("label IntRobinTalk:", "Robin.mark_known()"),
    }
    for relative_path, (entry_label, mark_call) in talk_entries.items():
        talk_source = (ROOT / relative_path).read_text(encoding="utf-8-sig")
        talk_block = talk_source.split(entry_label, 1)[1].split("\nlabel ", 1)[0]
        assert mark_call in talk_block, relative_path

    port_source = (ROOT / "game/Town/PortStreets.rpy").read_text(encoding="utf-8-sig")
    first_meet = port_source.split("label PortStreetsMeetGeorgett:", 1)[1].split("\nlabel ", 1)[0]
    assert "Georgett.mark_known()" in first_meet


def test_end_talk_restores_caller_ui_without_reentering_room_label():
    main_layout = MAIN_LAYOUT.read_text(encoding="utf-8-sig")
    end_talk_block = main_layout.split("def main_ui_end_talk_state", 1)[1].split(
        "def main_ui_begin_native_scene_state", 1
    )[0]

    assert "main_ui_runtime.talk_origin" in end_talk_block
    assert "main_ui_restore_context(origin)" in end_talk_block
    assert "renpy_module.jump" not in end_talk_block


def test_npc_selection_does_not_guess_pictures_or_dispatch_social_actions():
    runtime = _runtime_source()
    registry = runtime.split("class PeopleRegistry(object):", 1)[1].split(
        "def npc_schedule_clock_minute", 1
    )[0]

    for token in (
        "_npc_picture_cache",
        "npc_context_picture_path",
        "npc_picture_for_action",
        "show_npc_picture_main_ui_state",
        "media_hints",
        "room_hint_map",
        "npc_social_actions_available_in_room",
        "npc_gift_action_available",
    ):
        assert token not in registry


def test_dog_action_data_belongs_to_dog_runtime():
    runtime = _runtime_source()
    dog_source = DOG.read_text(encoding="utf-8-sig")

    assert "def dog_action_data" not in runtime
    assert "dog_main_ui_action_items" not in runtime
    assert "def action_data(self, where_id=\"\")" in dog_source
    assert "def dog_action_talk_state" not in dog_source
    assert "def dog_action_look_state" not in dog_source
    assert "def dog_open_action_menu_state" not in dog_source
    assert "label IntDogTalkMenu:" not in dog_source
    assert "jump IntDogTalkMenu" not in dog_source
    assert "while True:" in dog_source
    assert '"talk_label": "IntDogTalk"' in dog_source


def test_becky_inspect_calls_the_generic_returnable_card_procedure():
    talk = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalk.rpy").read_text(encoding="utf-8-sig")

    assert "call ShowGirlCard(_becky_name)" in talk
    assert "ShowBeckyCard" not in talk
