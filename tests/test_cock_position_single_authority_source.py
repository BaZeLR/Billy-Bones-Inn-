from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_target_npc_owns_the_only_live_cock_position_map():
    people = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    player = _source("game/Utilities/General/Player/Player.rpy")
    procedure = _source("game/Utilities/General/Sex/CockPosition.rpy")

    assert 'self.sex_state["partner_positions"] = {}' in people
    assert 'state["partner_positions"][actor_key] = position_key' in people
    assert 'state["partner_positions"].pop(actor_key, None)' in people
    assert 'self.sex_state.setdefault("cock_position"' not in people
    assert 'state["cock_position"]' not in people
    assert "self.cock_positions" not in player
    assert 'setdefault("cock_positions"' not in procedure
    assert "player.intimacy.set_cock_position" not in procedure


def test_cock_position_is_one_returnable_object_procedure():
    procedure = _source("game/Utilities/General/Sex/CockPosition.rpy")
    becky_home = _source("game/Town/BeckyHome.rpy")

    assert procedure.count("label CockPosition(") == 1
    assert "label cock_position(" not in procedure
    assert "def cock_position_apply(" not in procedure
    assert "def cock_position_target(" not in procedure
    assert "def cock_position_normalize(" not in procedure
    assert 'people.get_info(girl_name).set_cock_position(position_, other_dude_name or "You")' in procedure
    assert "call CockPosition(GirlName, 0)" in becky_home


def test_legacy_position_maps_are_consumed_only_during_load_migration():
    migration = _source("game/TractirSaveSync.rpy")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    for legacy_name in (
        "CockInPussy", "CockInMouth", "CockInTits",
        "YouCockInPussy", "YouCockInMouth", "YouCockInTits",
        "EddieCockInPussy", "EddieCockInMouth", "EddieCockInTits",
    ):
        assert legacy_name not in game_sources
        assert f'"{legacy_name}"' in migration
    assert 'globals().pop(old_name, {})' in migration
    assert 'player.intimacy.__dict__.pop("cock_positions", None)' in migration
    assert 'legacy_position = state.pop("cock_position", None)' in migration
    assert 'state.pop("cock_positions", None)' in migration
    assert 'self.sex_state.pop("cock_position", None)' not in game_sources
    assert 'self.sex_state.pop("cock_positions", None)' not in game_sources
    assert 'actor_key in ("mc", "stefan", "стефан")' not in game_sources
