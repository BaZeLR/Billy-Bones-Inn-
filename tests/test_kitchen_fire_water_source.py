from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHORES_PATH = PROJECT_ROOT / "game" / "Inn" / "PlayerChoresSystem.rpy"
CAULDRON_PATH = PROJECT_ROOT / "game" / "Inn" / "TavernKitchenCauldron001.rpy"


def test_kitchen_cauldron_resolves_to_kitchen_hearth_fire():
    source = CHORES_PATH.read_text(encoding="utf-8-sig")
    resolver = source.split("def _pc_fire_object", 1)[1].split("def _pc_water_object", 1)[0]

    assert '"hearth_001"' in resolver
    assert '"cauldron_001"' in resolver
    assert "return TavernKitchenHearthObject" in resolver
    assert "return TavernMainFireplaceObject" in resolver


def test_cauldron_action_uses_contextual_kitchen_arguments():
    source = CAULDRON_PATH.read_text(encoding="utf-8-sig")

    assert 'target="BoilWater"' in source
    assert 'args=("cauldron_001", "TavernKitchen", "", "cauldron_001")' in source
