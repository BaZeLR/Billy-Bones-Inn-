from pathlib import Path
from types import SimpleNamespace
import textwrap


ROOT = Path(__file__).resolve().parents[1]


def test_three_silver_coins_cast_three_tips_once_through_recipe_book():
    core = (ROOT / "game/Items/Core/CraftingRecipes.rpy").read_text(encoding="utf-8-sig")
    source = (ROOT / "game/Items/Crafting/SilverArrowTips.rpy").read_text(encoding="utf-8-sig")
    items = {}
    book = {"owned": False}
    clock = SimpleNamespace(minutes=0)
    favor = SimpleNamespace(num=2, completed=False)

    class Item:
        def __init__(self, **values):
            self.__dict__.update(values)
            items[self.object_id] = self

    class Player:
        inventory = {"silver_coin_001": 3, "chopped_wood_001": 1}

        def item_count(self, item_id):
            return self.inventory.get(item_id, 0)

        def remove_item(self, item_id, quantity):
            if self.item_count(item_id) < quantity:
                return False
            self.inventory[item_id] -= quantity
            return True

        def add_item(self, item_id, quantity):
            self.inventory[item_id] = self.item_count(item_id) + quantity

    player = Player()
    clock.advance_minutes = lambda amount: setattr(clock, "minutes", clock.minutes + amount)
    namespace = {
        "GameItem": Item,
        "player": player,
        "calendar_v2": clock,
        "threads": {"nostarRosarioFavor": favor},
        "player_has_soap_recipe_book": lambda: book["owned"],
        "get_game_item": lambda item_id: items.get(item_id, SimpleNamespace(name=item_id)),
        "get_object_id": lambda item_id: str(item_id or ""),
        "update_stat_state": lambda: None,
    }
    exec(textwrap.dedent(core.split("init 4 python:", 1)[1].split("\ndefault recipe_book", 1)[0]), namespace)
    exec(textwrap.dedent(source.split("init 5 python:", 1)[1]), namespace)

    recipe = namespace["recipe_catalog"].get("silver_arrow_tips_recipe")
    assert recipe.image == "images/recipe_book/silver_arrow_tips_recipe.png"
    assert (ROOT / "game" / recipe.image).is_file()
    assert recipe.item_result == "silver_arrow_tip_001"
    assert recipe.result_quantity == 3
    assert recipe.craft_minutes == 90
    assert not namespace["recipe_page_is_unlocked"](recipe.recipe_id)

    book["owned"] = True
    favor.num = 3
    assert namespace["recipe_page_is_unlocked"](recipe.recipe_id)
    result = namespace["apply_recipe_craft"](recipe.recipe_id)
    assert result["ok"] and result["quantity"] == 3
    assert player.inventory == {
        "silver_coin_001": 0,
        "chopped_wood_001": 0,
        "silver_arrow_tip_001": 3,
    }
    assert clock.minutes == 90
    assert not namespace["apply_recipe_craft"](recipe.recipe_id)["ok"]
    assert clock.minutes == 90
