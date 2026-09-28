from pathlib import Path
from types import SimpleNamespace
import textwrap


ROOT = Path(__file__).resolve().parents[1]


def test_rosario_recipe_registers_distinct_items_and_unlocks_after_sofa_clue():
    source = (ROOT / "game/Items/Crafting/RosarioTinctureItems.rpy").read_text(encoding="utf-8-sig")
    catalog = {}
    items = {}
    book = {"owned": False}
    sofa = SimpleNamespace(installed=False, rosario_recipe_taught=False)
    story = SimpleNamespace(num=6, completed=False)

    class Item:
        def __init__(self, **values):
            self.__dict__.update(values)
            items[self.object_id] = self

    class Recipe:
        def __init__(self, **values):
            self.__dict__.update(values)
            catalog[self.recipe_id] = self

    class Action:
        def __init__(self, **values):
            self.__dict__.update(values)

    namespace = {
        "GameItem": Item,
        "RecipePage": Recipe,
        "ObjectAction": Action,
        "Sofa": sofa,
        "threads": {"claraForestSofa": story},
        "player_has_soap_recipe_book": lambda: book["owned"],
    }
    exec(textwrap.dedent(source.split("init 5 python:", 1)[1]), namespace)

    recipe = catalog["rosario_arousal_tincture_recipe"]
    assert set(items) == {"chinchilla_droppings_001", "rosario_arousal_tincture_001", "silver_coin_001"}
    assert recipe.item_result == "rosario_arousal_tincture_001"
    assert {key: value["quantity"] for key, value in recipe.ingredients.items()} == {
        "chinchilla_droppings_001": 1,
        "honey_comb_001": 1,
        "ethanol_001": 1,
        "special_mushroom_001": 1,
    }
    assert recipe.craft_minutes == 45
    assert not recipe.unlock_condition()

    sofa.installed = True
    sofa.rosario_recipe_taught = True
    book["owned"] = True
    assert not recipe.unlock_condition()
    story.num = 7
    assert recipe.unlock_condition()

    drink = items["rosario_arousal_tincture_001"]
    assert drink.custom_properties["player_libido_days"] == 2
    assert drink.custom_properties["shared_arousal_bonus"] == 15
    assert drink.custom_properties["shared_conception_permille"] == 550
    assert items["silver_coin_001"].custom_properties["material_kind"] == "silver_coin"
    assert "shared_arousal_bonus" in (ROOT / "game/Utilities/General/Common/Actions.rpy").read_text(encoding="utf-8-sig")


def test_sofa_former_owner_story_is_the_recipe_reveal():
    source = (ROOT / "game/Inn/TavernCursedSofa.rpy").read_text(encoding="utf-8-sig")
    assert '"Спросить о прежней хозяйке" if Sofa.installed' in source
    assert "call CursedSofaPreviousOwnerStory" in source
    story = source.split("label CursedSofaPreviousOwnerStory:", 1)[1]
    assert "тифлингша" in story and "дурного корма" in story
    assert "помёта" in story and "редкий гриб" in story
    assert "$ Sofa.rosario_recipe_taught = True" in story


def test_nostar_favor_counts_exploration_pellets_and_silver_once():
    events = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    favor = events.split('LThreadData(0, "nostar", "RosarioFavor"', 1)[1].split('LThreadData(0, "city", "BlindPirateFall"', 1)[0]
    story = (ROOT / "game/NPC/Secondary/IntNostarTalk.rpy").read_text(encoding="utf-8-sig")
    assert "#int(player.stats.exploration or 0) >= 1300" in favor
    for label in ("story_nostar_favor_letter_0", "story_nostar_cage_1", "story_nostar_tiefling_negotiation_2", "story_nostar_favor_reward_3"):
        assert label in favor and "label %s:" % label in story
    cage = story.split("label story_nostar_cage_1:", 1)[1].split("label story_nostar_tiefling_negotiation_2:", 1)[0]
    trade = story.split("label story_nostar_tiefling_negotiation_2:", 1)[1].split("label story_nostar_favor_reward_3:", 1)[0]
    assert 'player.add_item("chinchilla_droppings_001", 10)' in cage
    assert 'player.remove_item("chinchilla_droppings_001", 5)' in trade
    assert 'player.add_item("silver_coin_001", 3)' in trade
    assert "getattr(" not in favor
    room = (ROOT / "game/Town/NostarHouse.rpy").read_text(encoding="utf-8-sig")
    assert "nostar_house_cage_stealth_too_low" in room
    assert "1300 очков" in room
