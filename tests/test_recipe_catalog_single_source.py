from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_recipe_pages_self_register_in_one_catalog():
    source = (ROOT / "game/Items/Core/CraftingRecipes.rpy").read_text(encoding="utf-8-sig")
    assert "class RecipeCatalog(object):" in source
    assert "recipe_catalog = RecipeCatalog()" in source
    assert "recipe_catalog.register(self)" in source
    assert "recipe_catalog.get(recipe_id)" in source
    assert "recipe_catalog.ids()" in source
    assert "get_recipe_page" not in source
    assert "recipe_names" not in source
    assert "define recipe_pages" not in source
    assert "register_recipe_page" not in source


def test_recipe_pages_own_standard_craft_behavior_without_handler_callbacks():
    core = (ROOT / "game/Items/Core/CraftingRecipes.rpy").read_text(encoding="utf-8-sig")
    recipes = (ROOT / "game/Items/Crafting/SoapCraftAndAtticItems.rpy").read_text(encoding="utf-8-sig")
    assert "def craft(self, resolved_rows=None):" in core
    assert "return dict(page.craft(resolved_rows) or {})" in core
    assert "craft_handler" not in core + recipes
    assert "_recipe_craft_handler" not in recipes
    for token in (
        "craft_minutes=30",
        "craft_text=",
        "craft_failure_text=",
        "class SoapBatchRecipePage(RecipePage):",
        "class LibidoTinctureRecipePage(RecipePage):",
    ):
        assert token in recipes
