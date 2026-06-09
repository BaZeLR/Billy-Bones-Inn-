# Crafting System Analysis - Current State (as of user feedback)

## User's Clarifications (Important)
- **All player crafting** happens at the table in the player's room (`TavernMyRoomTableCraftMenu` / `TavernMyRoomTableCraftItem` in `game/Inn/TavernMyRoom.rpy`).
- Crafted items are proper **new inventory objects**.
- **Soap is crafted in the Backyard** (`BackyardCookSoap` in `game/Inn/SoapCraftAndAtticItems.rpy`), **not** in the Barber Shop. Barber Shop only refines/sells luxury soap in some paths.
- The overall system "is good but cumbersome with many redundancies and bad coding."

## Current Architecture Map (from sources)

### 1. Main Intended Path (Modern)
- **Location**: Player's room table (`TavernMyRoomTableCraftMenu`)
- **Data**: `craftable_recipe_pages()` (expected in `game/Items/Core/CraftingRecipes.rpy`)
- **Execution**: `apply_recipe_craft()` + `_player_add_item_by_id()`
- **UI Layer**: Recipe book integration (`TavernMyRoomTableRead`, `RecipeBookCraftItem` in `game/Inn/CraftingRecipes.rpy`)
- **Goal**: Centralized, data-driven, only shows recipes the player can actually craft right now.

### 2. Legacy / Special Paths (Redundancy Source)
- **Soap**: Direct label `BackyardCookSoap(recipe_id)` called from Backyard actions.
  - Still lives in `game/Inn/SoapCraftAndAtticItems.rpy`.
  - Has its own result text handling (`_soap_craft_result`).
- **Other direct crafting?**: Possible remnants in Backyard, Attic search, etc.
- **Recipe Book logic** is split:
  - Current implementation in `game/Inn/CraftingRecipes.rpy`
  - Expected cleaner version in `game/Items/Core/CraftingRecipes.rpy`

### 3. Item System
- Runtime items exist (`runtime_item_description_text`, `runtime_item_display_name`).
- Inventory management via `_player_add_item_by_id` (in Actions.rpy).
- Attic has its own item management layer (`SoapCraftAndAtticItems.rpy` has a lot of attic inventory code).

## Identified Problems & Redundancies

### A. Multiple Crafting Entry Points
1. Room Table recipe system (intended central hub)
2. Direct `BackyardCookSoap` (special cased for soap)
3. Recipe book has its own "Craft" flow (`RecipeBookCraftItem`)
4. Potential attic / other mini-crafting

This means ingredient checking, result text, and item creation logic is duplicated in several places.

### B. Incomplete Migration
- The runtime test `check_recipe_items` is currently failing / warning because:
  - `TavernMyRoomTableCraftMenu` still uses old patterns (`"Посмотреть: "` entries).
  - It does **not** use `craftable_recipe_pages()` yet.
  - This creates the "cumbersome" feeling the user mentioned.

### C. Bad Coding Patterns Visible
- **Monolithic labels**: `TavernMyRoomTableCraftMenu` and `TavernMyRoomTableCraftItem` contain a lot of manual menu building and result handling.
- **Stringly-typed recipe ids** passed around (`"soap_recipe"`, `"luxury_soap_recipe"`).
- **Inconsistent result handling**: Some places use `_craft_result.get("text")`, soap uses its own `_soap_craft_result`.
- **Soap is special-cased** instead of being just another recipe with parameters (aromas).
- **Split recipe data**: Logic and data for recipes is spread across `game/Inn/CraftingRecipes.rpy`, `game/Inn/TavernMyRoom.rpy`, and the missing `game/Items/Core/CraftingRecipes.rpy`.
- **Tight coupling** between UI (menu building) and crafting logic.

### D. Good Parts
- The intent of a centralized `craftable_recipe_pages()` + `apply_recipe_craft` is solid.
- Runtime item system exists and is being used for attic items.
- There is already some separation between "reading recipes" and "crafting".

## Prioritized Recommendations

### High Priority (Quick Wins)
1. **Migrate soap into the main recipe system**
   - Turn soap into normal recipes (with aroma parameters).
   - Remove or deprecate the direct `BackyardCookSoap` path.
   - Use the new player-choice aroma system I created (`SoapCrafting.rpy`) from the room table.

2. **Make `TavernMyRoomTableCraftMenu` actually use the modern functions**
   - Replace manual "Посмотреть / Сделать" logic with `craftable_recipe_pages()`.
   - This will immediately reduce the "cumbersome" feeling.

3. **Centralize result text + item creation**
   - All crafting should go through one `finalize_craft(recipe_id, chosen_params)` function that handles text + `_player_add_item_by_id`.

### Medium Priority
4. Move recipe data + core functions to `game/Items/Core/CraftingRecipes.rpy` (as the tests expect).
5. Make aromas / parameters a first-class part of the recipe system (not special-cased per item type).
6. Improve the `CraftedItem` / runtime item creation so every crafted thing carries its parameters (aromas chosen, quality, etc.).

### Lower Priority / Polish
7. Unify the two CraftingRecipes.rpy files.
8. Add better error handling / requirement checking in one place.
9. Consider a small `Crafting` namespace / module to reduce the monolithic labels.

## Next Concrete Step Suggestion

Would you like me to:
A) Start migrating `BackyardCookSoap` into the room table recipe system using the improved aroma choice code?
B) Refactor `TavernMyRoomTableCraftMenu` to use `craftable_recipe_pages()` (even if the function is stubbed for now)?
C) Create the skeleton for `game/Items/Core/CraftingRecipes.rpy` with the expected functions?

This analysis is based on the LABEL_TEXT_MEDIA_INDEX, runtime tests, and existing references (since several core .rpy files are not present in the current workspace checkout).

Let me know the priority.
