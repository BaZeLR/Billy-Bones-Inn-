from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_item_registry_maps_ids_directly_to_item_objects():
    items = (ROOT / "game/Items/Core/GameItems.rpy").read_text(encoding="utf-8-sig")
    lookup = (ROOT / "game/Utilities/General/Classes/GameObjectTemplate.rpy").read_text(encoding="utf-8-sig")
    dress = (ROOT / "game/Utilities/General/Clothes/DressUp.rpy").read_text(encoding="utf-8-sig")
    game_item = (ROOT / "game/Items/Core/GameItem.rpy").read_text(encoding="utf-8-sig")
    assert "game_item_registry[self.object_id] = self" in game_item
    assert "define item_catalog" not in items
    assert "define game_items" not in items
    assert "_game_item_catalog_entry" not in items
    assert "_all_game_item_objects" not in items
    assert "MALE_DRESS_ITEM_IDS" in items
    assert "FEMALE_DRESS_ITEM_IDS" in items
    assert "dict(game_item_registry or {}).get(item_id" in lookup
    assert "item_catalog" not in dress


def test_inventory_consumption_actions_come_only_from_item_objects():
    player_card = (ROOT / "game/Utilities/General/Screens/PlayerCard.rpy").read_text(encoding="utf-8-sig")
    berries = (ROOT / "game/Items/Resources/BerriesItem.rpy").read_text(encoding="utf-8-sig")
    hunter_items = (ROOT / "game/Items/Shops/HunterClubItems.rpy").read_text(encoding="utf-8-sig")
    crafting_items = (ROOT / "game/Items/Crafting/SoapCraftAndAtticItems.rpy").read_text(encoding="utf-8-sig")

    assert "player_card_append_fallback_item_actions" not in player_card
    assert 'object_id="berries_001"' in berries and 'target="UseFoodItem"' in berries
    assert 'object_id="drink_ale_001"' in hunter_items and 'target="UseDrinkItem"' in hunter_items
    for item_id in ("energy_tea_001", "libido_tincture_001"):
        item_block = crafting_items.split('object_id="%s"' % item_id, 1)[1].split("GameItem(", 1)[0]
        assert 'target="UseDrinkItem"' in item_block
