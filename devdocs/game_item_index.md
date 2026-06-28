# Game Item Index

Source of truth:

- `GameItem` class: `game/Items/Core/GameItem.rpy`
- Registered item list: `game/Items/Core/GameItems.rpy`
- Runtime item lookup: `get_game_item(...)` in `game/Utilities/General/Classes/GameObjectTemplate.rpy`

Every real item should have:

1. A `GameItem(...)` definition.
2. A stable `object_id`.
3. A non-empty `name`.
4. A non-empty `description`.
5. An explicit `picture` value when it has item art, or an intentional empty picture.
6. An `actions=[...]` list when the item has direct item actions.
7. Each `ObjectAction` must lead to a real direct label or text action.
8. The item object must be listed in `_all_game_item_objects()` unless it is deliberately not part of gameplay.

Do not add wrapper dispatchers to make item menus work. Fix the item definition, room item list, or direct action label.

## Registered Item Domains

| Domain | Definition file |
| --- | --- |
| Clothes | `game/Items/Clothes/*.rpy` |
| Attic / soap / crafted goods / weapon / armor | `game/Items/Crafting/SoapCraftAndAtticItems.rpy` |
| Resources | `game/Items/Resources/*.rpy` |
| Grocery | `game/Items/Shops/GroceryStoreItems.rpy` |
| Hunter club goods and loot | `game/Items/Shops/HunterClubItems.rpy` |

## Registry Audit

Fixed:

- `WhiteWolfSkinItem` was defined in `game/Items/Shops/HunterClubItems.rpy` but missing from `_all_game_item_objects()`. It is now registered.

## Item Definitions By File

### `game/Items/Resources`

| Item object | File |
| --- | --- |
| `OldAxeItem` | `game/Items/Resources/OldAxeItem.rpy` |
| `LumberItem` | `game/Items/Resources/LumberItem.rpy` |
| `ChoppedWoodItem` | `game/Items/Resources/ChoppedWoodItem.rpy` |
| `MushroomItem` | `game/Items/Resources/MushroomItem.rpy` |
| `BerriesItem` | `game/Items/Resources/BerriesItem.rpy` |
| `HoneyCombItem` | `game/Items/Resources/HoneyCombItem.rpy` |
| `FoodBaleItem` | `game/Items/Resources/FoodBaleItem.rpy` |
| `WineBarrelItem` | `game/Items/Resources/WineBarrelItem.rpy` |
| `TavernHelpBookItem` | `game/Items/Resources/TavernHelpBookItem.rpy` |
| `MelissaBookletItem` | `game/Items/Resources/MelissaBookletItem.rpy` |

### `game/Items/Crafting/SoapCraftAndAtticItems.rpy`

| Item object |
| --- |
| `RecipeBookItem` |
| `NightBowlItem` |
| `FancyNightBowlItem` |
| `BucketItem` |
| `EmptyBottleItem` |
| `CorkItem` |
| `PigLardItem` |
| `DriedMossItem` |
| `ClothScrapItem` |
| `SoapItem` |
| `OliveOilItem` |
| `LuxurySoapItem` |
| `EthanolItem` |
| `EnergyTeaItem` |
| `LibidoTinctureItem` |
| `SpecialCreamItem` |
| `FireBombItem` |
| `BatRepellentItem` |
| `AshBarrelItem` |
| `RustyHunterRifleItem` |
| `OldLeatherCuirassItem` |

### `game/Items/Shops`

| Item object | File |
| --- | --- |
| `MilkPitcherItem` | `game/Items/Shops/GroceryStoreItems.rpy` |
| `AleItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `DogBoneItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `DogCollarItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `HuntingTrapItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `ArrowsItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `FlintItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `RopeItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `TorchItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `GunpowderItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `ShotDropletsItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `WeaponOilItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `BandageItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `HealingPotionItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `WolfSkinItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `WhiteWolfSkinItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `BoarFangItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `BoarMeatItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `BearClawItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `BrownBearFurItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `GrizzlyBearFurItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `WarmFurCloakItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `FurBedrollItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `SpecialMushroomItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `SpecialHerbsItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `LavenderItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `WildRoseItem` | `game/Items/Shops/HunterClubItems.rpy` |
| `MossItem` | `game/Items/Shops/HunterClubItems.rpy` |

### `game/Items/Clothes`

| Item object |
| --- |
| `PeasantCostumeItem` |
| `BourgeoisCostumeItem` |
| `SailorCostumeItem` |
| `BanditCostumeItem` |
| `NobleCostumeItem` |
| `ModestWorkDressItem` |
| `ModestNiceDressItem` |
| `WorkDressItem` |
| `WorkDressZhiletItem` |
| `GreenWorkDressItem` |
| `OpenWorkDressItem` |
| `MiniDressItem` |
| `SlutDressItem` |
| `SimpleBraItem` |
| `SimplePantiesItem` |
| `WhiteStockingsItem` |
| `BlackStockingsItem` |
| `RedStockingsItem` |
| `NightshirtItem` |

## Known Follow-Up

Some items currently rely on default empty `picture` or have no direct action list because they are consumed by shop/inventory flow. That should be made explicit item by item: either `picture=""` with no item art, or a real picture path; either `actions=[]` because it has no direct item action, or direct `ObjectAction(...)` entries with labels.
