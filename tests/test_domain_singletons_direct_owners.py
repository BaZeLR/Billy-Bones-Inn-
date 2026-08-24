from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_recipe_crafting_and_household_use_direct_initialized_owners():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    assert "default recipe_book = RecipeBookSession()" in runtime
    assert "default crafting = CraftingInfo()" in runtime
    assert "default household = HouseholdInfo()" in runtime
    assert "recipe_book_session()" not in runtime
    assert "crafting_info()" not in runtime
    assert "household_info()" not in runtime
    assert "default RecipeBook" not in runtime
    assert "default Crafting" not in runtime
    assert "default Household" not in runtime


def test_legacy_singletons_cannot_overwrite_canonical_owners_after_load():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in ("RecipeBook", "Crafting", "Household"):
        assert '"%s"' % legacy_name not in migration
    assert "tractir_save_migrate_domain_singletons" not in migration
