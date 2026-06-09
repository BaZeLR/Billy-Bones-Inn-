# Crafting System Improvement Suggestions (Tractir)

## Current State Observations (from existing code)

- There is a legacy crafting path (BackyardCookSoap, direct labels).
- There is a newer data-driven system:
  - `game/Items/Core/CraftingRecipes.rpy`
  - `craftable_recipe_pages()`
  - `RecipeBookCraftMenu`
  - `apply_recipe_craft`
- Soap has special handling (regular vs luxury olive oil).
- Aromas were previously random → now player-controlled (see `game/Items/Crafting/SoapCrafting.rpy`).
- Girls can request specific scented soap (HouseholdRuntimeEvents).
- BarberShop can refine and sell luxury soap.
- Attic has soap usage.

## Concrete Improvement Suggestions

### 1. Unified Recipe + Instance System (High Priority)
- Make every crafted item a proper runtime object (like the attic items system).
- Store chosen parameters (aromas, quality, ingredients used) on the item instance.
- Example: `luxury_soap_001.aromas = ["lavender", "rose"]`

### 2. Player Choice Over Randomness (Already started with soap)
- Extend the pattern used in the new SoapCrafting.rpy to other crafts:
  - Candle scents
  - Food seasoning/spices
  - Perfumes / tinctures
  - Dye colors for cloth
- Always give the player meaningful choices instead of random results.

### 3. Quality / Mastery System
- Track player's crafting skill per category (Soapmaking, Cooking, Alchemy, Smithing...).
- Higher skill = better base quality + more options (more aromas, better yield, special variants).
- Failure / partial success states (currently many crafts feel binary).

### 4. Ingredient Substitution & Experimentation
- Allow limited substitution (e.g. use lard instead of tallow for soap, with different results).
- "Experimental" crafting mode that can discover new recipes or variants.

### 5. Better UI / Recipe Book Integration
- Make the recipe book the central place for crafting.
- Show "Aroma selection" as part of the recipe execution when the recipe supports it.
- Preview what the final item will be called ("Лавандово-розовое оливковое мыло").

### 6. Economic & Social Loops (Already partially there)
- Good soap is requested by girls → gift / sell / reputation.
- Luxury soap can be sold to BarberShop or Clara's secret merchant.
- Improve feedback when gifting crafted items (currently somewhat generic).

### 7. Modularity & Extensibility
- Define aromas, scents, dyes, etc. in data tables instead of hard-coded in labels.
- Allow easy addition of new aromas without touching crafting logic.
- Same for recipe categories.

### 8. Hidden / Advanced Features (for later)
- Certain aromas can have mild gameplay effects (relaxation, attraction, masking smells for stealth, etc.).
- Link crafted soap quality to daily hygiene / appearance bonuses.

## Recommended Next Steps

1. Finish migrating soap crafting fully to the new player-choice system (replace calls to old random version).
2. Create a small `CraftingUtils.rpy` with helpers:
   - `player_choose_aromas(available_list, max_choices=3)`
   - `finalize_crafted_item(recipe_id, chosen_params)`
3. Add a proper `CraftedItem` class or use the existing runtime item system consistently.
4. Update recipe book pages to support "parameterized recipes" (recipes that ask for choices).

This direction makes crafting feel more player-driven and rewarding instead of "press button, get random thing".

---
*Document created after user request for general crafting improvements (2026).*
