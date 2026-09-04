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


def test_recipe_book_list_uses_catalog_buttons_and_keeps_back_in_actions():
    core = (ROOT / "game/Items/Core/CraftingRecipes.rpy").read_text(encoding="utf-8-sig")
    room = (ROOT / "game/Inn/TavernMyRoom.rpy").read_text(encoding="utf-8-sig")

    screen_block = core.split("screen recipe_book_page_list", 1)[1].split("\n\nlabel RecipeBookList", 1)[0]
    list_block = core.split("label RecipeBookList", 1)[1].split("\n\nlabel ReadRecipeBook", 1)[0]
    read_block = core.split("label ReadRecipeBook", 1)[1].split("\n\nlabel RecipeBookFindTinyNote", 1)[0]

    assert "visible_recipe_pages()" in screen_block
    assert "recipe_catalog.get(_recipe_id)" in screen_block
    assert "_recipe_columns" in screen_block
    assert "viewport" not in screen_block
    assert "vscrollbar" not in screen_block
    assert 'id "recipe_book_list_button_" + _recipe_id' in screen_block
    assert 'Call("ReadRecipeBook"' in screen_block
    assert 'main_ui_runtime.action_items = [MenuItem("Назад"' in list_block
    assert 'show screen recipe_book_page_list' in list_block
    assert 'hide screen recipe_book_page_list' in read_block

    assert "label TavernMyRoomTableRead" not in room
    assert 'Call("RecipeBookList", "TavernMyRoom", "recipe_book_001")' in room
