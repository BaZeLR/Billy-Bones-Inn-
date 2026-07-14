# Tractir Project Index

Use this index before broad searches. The active checkout is:

`C:\Users\blank\Documents\RenPy_Projects\Tractir`

Do not use the stale apostrophe path:

`C:\Users\blank\Documents\Ren'Py_Projects\Tractir`

## Ren'Py SDK

Compile/lint helper:

`tools/renpy_compile.ps1`

Fixed SDK path:

`C:\Users\blank\renpy\renpy-8.5.2-sdk\renpy.exe`

Commands:

```powershell
powershell -ExecutionPolicy Bypass -File tools\renpy_compile.ps1 compile
powershell -ExecutionPolicy Bypass -File tools\renpy_compile.ps1 lint
```

## Core Runtime

Documentation entry point:

`devdocs/README.md`

Use `devdocs/README.md` before older audit/status/plan files. Historical docs
may preserve old QSP names, but they are not implementation authority.

| Area | File |
| --- | --- |
| Calendar source of truth | `game/script.rpy` |
| Room template | `game/Utilities/General/Classes/RoomTemplate.rpy` |
| Room object / object action classes | `game/Utilities/General/Classes/GameObjectTemplate.rpy` |
| Game item class | `game/Items/Core/GameItem.rpy` |
| Game item registry | `game/Items/Core/GameItems.rpy` |
| Event/thread data | `game/Utilities/General/Classes/StoryEventRuntime.rpy` |
| Event classes/runtime | `game/Utilities/General/Events/events.rpy` |
| Thread classes/runtime | `game/Utilities/General/Events/threads.rpy` |
| Main UI layout | `game/Utilities/General/Screens/main_layout.rpy` |
| Room action UI builder | `game/Utilities/General/Screens/build_room_action_items.rpy` |

## Game Item Definition Files

| Domain | File |
| --- | --- |
| Core item class | `game/Items/Core/GameItem.rpy` |
| Registry / item catalog build | `game/Items/Core/GameItems.rpy` |
| Crafting recipes | `game/Items/Core/CraftingRecipes.rpy` |
| Soap, attic, weapons, armor, utility items | `game/Items/Crafting/SoapCraftAndAtticItems.rpy` |
| Soap crafting flow | `game/Items/Crafting/SoapCrafting.rpy` |
| Resources: axe, lumber, wood, food, books, wine | `game/Items/Resources/*.rpy` |
| Hunter club supplies and loot | `game/Items/Shops/HunterClubItems.rpy` |
| Grocery item definitions | `game/Items/Shops/GroceryStoreItems.rpy` |
| Clothing item definitions | `game/Items/Clothes/*.rpy` |

## Room/Object Menu Entry Points

| Room | File | Object menu label |
| --- | --- | --- |
| Player room | `game/Inn/TavernMyRoom.rpy` | `TavernMyRoomObjectMenu` |
| Attic | `game/Inn/TavernAtic.rpy` | `TavernAticObjectMenu` |
| Shed | `game/Inn/Shed.rpy` | item actions via `OldAxeItem`, `LumberItem`, etc. |
| Backyard | `game/Inn/Backyard.rpy` | `BackyardObjectMenu` |
| Kitchen hearth | `game/Inn/TavernKitchenHearth001.rpy` | `TavernKitchenHearthMenu` |
| Kitchen cauldron | `game/Inn/TavernKitchenCauldron001.rpy` | `TavernKitchenCauldronMenu` |
| Grocery store | `game/Town/GroceryStore.rpy` | `GroceryStoreObjectMenu` |
| Wine store | `game/Town/WineStore.rpy` | `WineStoreObjectMenu` |
| Hunter club | `game/Town/HunterClub.rpy` | `HunterClubObjectMenu` |
| Port streets | `game/Town/PortStreets.rpy` | `PortStreetsBottleMenu` |
| Market | `game/Town/Market/MarketPlace.rpy` | `MarketPlaceObjectMenu` |

## NPC Class Entry Points

| NPC | Init / class file |
| --- | --- |
| Amanda | `game/NPC/Girls/Amanda/InitAmanda.rpy` |
| Melissa | `game/NPC/Girls/Melissa/InitMelissa.rpy` |
| Sandra | `game/NPC/Girls/Sandra/InitSandra.rpy` |
| Clara | `game/NPC/Girls/Clara/InitClara.rpy` |
| Becky | `game/NPC/Girls/Becky/InitBecky.rpy` |
| Georgette | `game/NPC/Girls/Georgett/InitGeorgett.rpy` |
| Liza / Lizette | `game/NPC/Girls/Liza/InitLiza.rpy` |
| Eddie | `game/NPC/Secondary/InitEddie.rpy` |
| Alber / Legare | `game/NPC/Secondary/InitAlber.rpy` |
| Zimmer | `game/NPC/Secondary/InitZimmer.rpy` |
| Mongol | `game/NPC/Secondary/InitMongol.rpy` |
| Draupnir | `game/NPC/Secondary/InitDraupnir.rpy` |
| Robin | `game/NPC/Secondary/InitRobin.rpy` |
| Francheska | `game/NPC/Secondary/InitFrancheska.rpy` |

## Current Item Model Rule

`GameItem` definitions own item identity, description, picture reference, and item action metadata.

Room labels may show items and call their action labels, but room labels should not own item behavior.

Actual effects belong to direct labels or the owning class/state object.
