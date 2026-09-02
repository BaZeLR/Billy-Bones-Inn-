from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


SOAP = source("game/Items/Crafting/SoapCraftAndAtticItems.rpy")
BACKYARD = source("game/Inn/Backyard.rpy")
ACTIONS = source("game/Utilities/General/Common/Actions.rpy")
RELATIONSHIPS = source("game/Utilities/General/NPC/RelationshipDynamics.rpy")
SOCIAL = source("game/Utilities/General/NPC/SocialTalkTopics.rpy")
HOUSEHOLD = source("game/Inn/HouseholdRuntimeEvents.rpy")
BREAKFAST = source("game/Inn/TavernKitchenBreakfast.rpy")


SOAP_VARIANTS = {
    "soap_recipe": ("soap_001", ("lavender_001",)),
    "lavender_herbal_soap_recipe": (
        "lavender_herbal_soap_001",
        ("lavender_001", "special_herbs_001"),
    ),
    "lavender_rose_soap_recipe": (
        "lavender_rose_soap_001",
        ("lavender_001", "wild_rose_001"),
    ),
    "rose_honey_soap_recipe": (
        "rose_honey_soap_001",
        ("wild_rose_001", "honey_comb_001"),
    ),
    "luxury_soap_recipe": (
        "luxury_soap_001",
        ("lavender_001", "olive_oil_001"),
    ),
}


def test_each_soap_choice_is_a_real_item_and_exact_recipe_result():
    for recipe_id, (item_id, additives) in SOAP_VARIANTS.items():
        assert f'object_id="{item_id}"' in SOAP
        recipe_block = SOAP.split(f'recipe_id="{recipe_id}"', 1)[1].split("    )", 1)[0]
        assert f'item_result="{item_id}"' in recipe_block
        joined = ", ".join(f'"{item}"' for item in additives)
        assert f"ingredients=soap_recipe_ingredients({joined})" in recipe_block


def test_soap_crafting_uses_declared_ingredients_without_bag_autoselection():
    craft_block = SOAP.split("class SoapBatchRecipePage", 1)[1].split(
        "class LibidoTinctureRecipePage", 1
    )[0]

    assert "recipe_consume_required_ingredients" in craft_block
    assert 'player.item_count("special_herbs_001")' not in craft_block
    assert 'player.item_count("honey_comb_001")' not in craft_block
    assert "soap_selected_flower_item" not in SOAP
    assert '"item_id": self.item_result' in craft_block
    assert "if item_id == \"\":" not in SOAP.split(
        "def crafting_release_ready_soap_batches", 1
    )[1].split("def upstairs_room_search_done", 1)[0]


def test_backyard_has_one_native_choice_menu_for_all_soap_recipes():
    assert 'target="BackyardChooseSoapRecipe"' in BACKYARD
    assert "cook_luxury_soap" not in BACKYARD
    choice_block = SOAP.split("label BackyardChooseSoapRecipe:", 1)[1].split(
        "label ShootingPracticeMenu", 1
    )[0]
    assert "menu:" in choice_block
    assert '"Назад":' in choice_block
    for recipe_id in SOAP_VARIANTS:
        assert f'call BackyardCookSoap("{recipe_id}")' in choice_block


def test_every_finished_soap_is_giftable_through_the_existing_gift_authority():
    for item_id, _ in SOAP_VARIANTS.values():
        item_block = SOAP.split(f'object_id="{item_id}"', 1)[1].split("    )", 1)[0]
        assert '"crafted_kind": "soap"' in item_block
        assert '"gift_value":' in item_block

    assert '"soap": {' in ACTIONS
    assert '"luxury_soap": {' in ACTIONS
    assert 'properties.get("social_effect_family"' in ACTIONS
    assert 'properties.get("crafted_kind"' in RELATIONSHIPS
    assert "relationship_is_care_gift(item_key)" in RELATIONSHIPS
    assert "SOCIAL_EARLY_CARE_GIFT_IDS" not in SOCIAL
    assert "relationship_is_care_gift(item_key)" in SOCIAL


def test_household_preferences_requests_and_breakfast_use_the_same_soap_items():
    preferences = {
        "Amanda": "rose_honey_soap_001",
        "Melissa": "lavender_rose_soap_001",
        "Sandra": "lavender_herbal_soap_001",
    }
    for girl, item_id in preferences.items():
        npc_source = source(f"game/NPC/Girls/{girl}/Init{girl}.rpy")
        assert f'"{item_id}"' in npc_source
        assert f'player.item_count("{item_id}")' in HOUSEHOLD
        assert f'HouseholdSoapRequestGiveNow(_soap_girl, "{item_id}")' in HOUSEHOLD

    assert "player_remove_soap_pieces(3, False)" not in BREAKFAST
    assert "tavern_breakfast_apply_first_soap_samples" not in BREAKFAST
    assert 'player.remove_item("soap_001", 3)' not in BREAKFAST
