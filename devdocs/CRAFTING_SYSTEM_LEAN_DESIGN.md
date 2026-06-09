# Lean Crafting System Design (Following User's Guidance)

## Core Principles (from this conversation)

1. **Labels are thin UI only**
   - Show picture
   - Show text
   - Present menu
   - Call Python functions for everything else

2. **Heavy logic lives in Python**
   - Ingredient checking
   - Time costs
   - Item creation
   - Quality / aroma / parameter calculation
   - Effects application

3. **Recipes are centralized**
   - One source of truth for all recipes (including soap)
   - Not scattered across Backyard labels, room table, recipe book, etc.

4. **Crafted items are proper objects**
   - They carry their parameters (type, aromas, quality, created_day)
   - They have descriptions
   - They are added via a single `_player_add_item_by_id` or equivalent clean function

5. **No (or very minimal) globals** for crafting state
   - Use the girl objects (`girls_info`) and proper item objects
   - Use the existing calendar/time system for timers and decay

## Current Problems (Confirmed)

- Multiple entry points for the same action (Backyard direct labels + Room Table recipe system)
- Soap has special legacy path (`BackyardCookSoap`) while other crafts try to go through the centralized system
- Room table menu still has old manual patterns ("Посмотреть: ")
- Result text and item creation logic duplicated in many places
- Some use of globals for temporary crafting state

## Recommended Structure

### 1. Centralized Recipe Data (Python)
```python
# game/Items/Core/CraftingRecipes.py (or .rpy init python block)

RECIPES = {
    "luxury_soap": {
        "name": "Роскошное оливковое мыло",
        "ingredients": [...],
        "time_stages": [first_stage_minutes, second_stage_minutes],
        "parameters": ["soap_type", "aromas"],   # player chooses in second stage
        "on_complete": "finish_luxury_soap",     # python function
    },
    ...
}
```

### 2. Thin Label Example (for second stage soap)
```renpy
label SoapSecondStageComplete:
    show screen main_ui
    $ MainTxt = "Вторая стадия варки завершена."

    # Heavy logic + choice happens here or in called python screen/function
    call ChooseSoapTypeAndAromas from _call_aroma_choice

    # Then call pure python to finalize
    $ result = finish_soap_crafting(chosen_type, chosen_aromas)

    $ MainTxt = result.text
    return
```

### 3. Single Item Creation Path
All crafting ends up calling one clean function:
```python
def create_crafted_item(recipe_id, parameters):
    item = RuntimeItem(...)
    item.apply_parameters(parameters)
    _player_add_item_by_id(item.id)
    apply_time_cost(recipe_id)
    return item
```

## Soap Specific (as per latest instructions)

- First stage (ingredients + ash barrel + bowl) → stays in Backyard exactly as it is now.
- Second stage (timer finish) → call the choice menu for type + aromas (implemented in SoapCrafting.rpy).
- Room table version → protected by a simple flag (`soap_process`).
- Effects, decay (1 week), girl requests, 3-day penalty, favor system → implemented as described.

This keeps the "flavor" of backyard soap making while making the choice part clean and player-controlled.

---

Next step: If you want, I can start extracting the common crafting logic into clean Python functions and thin out the room table crafting labels.
