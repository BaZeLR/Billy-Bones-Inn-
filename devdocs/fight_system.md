# Fight System Design

## Goal

This document defines the next combat module for the Inn project without replacing existing story logic.

The design must:
- keep current Ren'Py room and `main_ui` structure intact
- reuse existing runtime variables where possible
- separate combat calculations from scene text and event labels
- allow later extension to hunting, companions, armor, weapons, and loot


## Current Runtime Anchors

The current project already has several pieces that the fight system should build on:

- Player exploration:
  - [Intro.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Intro.rpy)
  - `default exploration = 0`
- Base fight level:
  - [Intro.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Intro.rpy)
  - `default FightLevel = {"you": 1}`
- Existing fight-result helper usage:
  - [FightResult.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FightResult.rpy)
  - [AfterDanceLegare.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/AfterDanceLegare.rpy)
  - [IntAlberTalk.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntAlberTalk.rpy)
- Weapon-capable items:
  - [GameItem.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/GameItem.rpy)
  - [OldAxeItem.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/OldAxeItem.rpy)
- Exploration-gated room content already exists:
  - [TavernMyRoomAtticHatch001.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoomAtticHatch001.rpy)

That means the new combat system should extend the current model, not replace it.


## Split Of Responsibilities

### 1. Exploration

Exploration is the progression stat that unlocks dangerous and hidden content.

It already exists as:
- `exploration`

Exploration will now also drive combat progression.

### 2. Fight Skill

Fight skill is the player combat level.

Use:
- `FightLevel["you"]`

Rule:
- every full `50` exploration points gives `+1` fight level

Formula:
- `FightLevel["you"] = 1 + floor(exploration / 50)`

Examples:
- `0..49 exploration` -> fight level `1`
- `50..99 exploration` -> fight level `2`
- `100..149 exploration` -> fight level `3`

This keeps exploration as the root progression and makes combat growth predictable.

### 3. Player Reputation

Player reputation is separate from tavern reputation.

Player reputation already uses:
- look
- quest progress
- exploration
- number of children

Tavern reputation stays tavern-side:
- `tavernfame`
- visitor/economy performance

Crew interactions can later use both:
- player reputation
- tavern reputation

But combat math should not depend on reputation directly.


## Combat Stats

The player should have these combat stats:

- `health`
- `attack`
- `defence`
- `fight skill`
- equipped weapon modifiers
- equipped armor modifiers
- company/companions
- combat supplies

### Health

Add a dedicated player combat health stat:
- `default health = 100`

Range:
- `0..100`

Rules:
- `100` means full combat health
- `0` means defeated/incapacitated
- health is separate from `energy`

Suggested relation:
- `energy` is daily stamina / life routine
- `health` is direct physical combat condition

### Attack

Attack should be a rolled value built from:
- fight skill
- weapon bonus
- random roll
- optional company bonus

Suggested formula:
- `attack = base_attack + weapon_attack + random_attack + company_attack`

Suggested base:
- `base_attack = 5 + FightLevel["you"] * 5`

Suggested random:
- `random_attack = randint(0, FightLevel["you"] * 3)`

### Defence

Defence should be a rolled value built from:
- fight skill
- armor bonus
- random roll
- optional company bonus

Suggested formula:
- `defence = base_defence + armor_defence + random_defence + company_defence`

Suggested base:
- `base_defence = 5 + FightLevel["you"] * 4`

Suggested random:
- `random_defence = randint(0, FightLevel["you"] * 2)`


## Combat Supplies

Combat and hunting should use a separate player-side dictionary for battle consumables and ammunition, instead of mixing all checks into the main general inventory every turn.

Suggested runtime:
- `default PlayerFightSupply = {}`

Suggested keys for first implementation:
- `arrows`
- `gunpowder`
- `bees_bomb`
- `bandage`
- `energy_tea`
- `healing_potion`

Example:

```python
default PlayerFightSupply = {
    "arrows": 0,
    "gunpowder": 0,
    "bees_bomb": 0,
    "bandage": 0,
    "energy_tea": 0,
    "healing_potion": 0,
}
```

Use:
- ranged fire checks `arrows` and, if needed by the weapon model, `gunpowder`
- bees bomb checks `bees_bomb`
- bandage checks `bandage`
- energy recovery drink checks `energy_tea`
- health potion checks `healing_potion`

Design note:
- these values should still be synchronized with the real item/inventory model when items are bought, crafted, looted, or consumed
- but combat UI should read from this compact combat dictionary, because it is cleaner and easier to validate each turn


## Equipment

### Weapons

Weapons already have a concept in item templates:
- `weapon=True`

The next step is to support combat properties consistently via `custom_properties`, for example:

```python
custom_properties = {
    "attack_points": 10,
    "defence_points": 0,
    "weapon_type": "axe",
}
```

Current example:
- [OldAxeItem.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/OldAxeItem.rpy)

### Armor

Armor should use the same pattern:

```python
custom_properties = {
    "armor_points": 8,
    "defence_points": 8,
    "attack_points": 0,
    "armor_slot": "body",
}
```

Armor should be read from currently worn player dress / equipment data, not from story labels.

Current required armor anchor:
- old leather cuirass / кожаный кирас

First implementation note:
- this cuirass should be the first real armor item used by combat defence math
- it should count as leather armor and provide a meaningful defence bonus


## Company / Companions

The player should have a company list for combat support.

New runtime structure:
- `default company_list = []`

Each companion entry should be data-first, for example:

```python
{
    "id": "npc_id",
    "attack_bonus": 3,
    "defence_bonus": 2,
    "health": 40,
    "can_hunt": True,
}
```

Use:
- companions do not replace the player
- companions add combat support
- some fights or hunts may limit which companions are allowed

This structure must stay modular so future NPC-specific story rules can gate availability.


## Combat Resolution

Combat round design:

1. Build player-side attack/defence
2. Build enemy-side attack/defence
3. Resolve all attacks for the turn
4. Accumulate damage on each side
5. Apply total damage
6. Repeat until one side reaches `health <= 0`

### Turn-Based Player Choices

Each combat turn should present explicit choices, not one automatic exchange.

Required player actions:
- dodge
- block
- close attack
- fire ranged weapon
- reload ranged weapon
- use bees bomb
- use bandage
- drink energy tea
- drink healing potion
- catch breath
- command dog
- retreat from hunt

These actions should be shown only when valid for the current state:
- `fire ranged weapon` only if a loaded ranged weapon is equipped
- `reload ranged weapon` only if the weapon is empty and matching ammo exists
- `use bees bomb` only if the player has the item
- `use bandage` only if the player has the item
- `drink energy tea` only if the player has the item
- `drink healing potion` only if the player has the item
- `command dog` only if the dog is in company and alive
- `retreat` only in hunting / wilderness combat where escape is allowed

### Core Turn Actions

#### Dodge

Purpose:
- avoid part or all of incoming damage this turn

Suggested effect:
- high temporary defence spike
- moderate chance to fully avoid one enemy hit
- weak or zero outgoing attack

#### Block

Purpose:
- reduce incoming damage with a more reliable defensive action

Suggested effect:
- stable defence increase
- no dodge chance bonus
- weak or zero outgoing attack

#### Close Attack

Purpose:
- default melee attack

Suggested effect:
- uses normal attack formula
- benefits from melee weapon
- available every turn unless stunned, pinned, or otherwise blocked

#### Fire Ranged Weapon

Purpose:
- attack from distance before enemies close fully

Suggested effect:
- high attack if loaded
- may get opening bonus against animals
- may lose effectiveness if the enemy is already in close contact

Required ranged special cases:
- gun shot with droplets / дробь:
  - deals `15..30` damage
  - especially effective against packs and bears
- arbalest shot:
  - applies slow bleed
  - within `5` moves the target should lose about half of its full health if the bleed is not cleared

State requirement:
- ranged weapon equipped
- weapon loaded

#### Reload

Purpose:
- prepare ranged weapon for later turns

Suggested effect:
- no meaningful defence or attack this turn
- sets ranged weapon state to loaded

#### Catch Breath

Purpose:
- recover a small amount of energy during combat

Suggested effect:
- regain a small amount of `energy`
- weak defence only
- no attack

Suggested range:
- `+5..10 energy`

### Combat Item Actions

#### Bees Bomb

Purpose:
- disrupt, frighten, or scatter enemies

Suggested effect:
- good against packs
- lowers enemy attack or defence for one turn
- may cause a skip or disorder effect on wolves

Required stronger effect:
- paralyzing effect for `3` rounds
- `25` total health loss during `5` turns

#### Bandage

Purpose:
- patch wounds in combat

Suggested effect:
- restore a modest amount of `health`
- no attack this turn

#### Energy Tea

Purpose:
- restore combat stamina / clarity

Suggested effect:
- restore `energy`
- no direct `health` restoration

#### Healing Potions

Purpose:
- restore `health`

Suggested effect:
- stronger than a bandage
- still costs the whole turn

### Side-Based Turn Logic

Combat should be resolved by sides, not by a single flat attacker.

That means:
- if the enemy is a pack, each pack member attacks in the same turn
- their damage is accumulated into one enemy-turn result
- if the player has company, each companion contributes attack and defence
- companion bonuses are accumulated into the player-side result

So the turn is:
- player side total
- enemy side total
- both sides can accumulate attack and defence from multiple members

### Player Side

The player side consists of:
- the player
- all active companions from `company_list`

Player-side attack for the turn:
- player attack roll
- plus all companion attack contributions

Player-side defence for the turn:
- player defence roll
- plus all companion defence contributions

Suggested formulas:
- `player_side_attack = player_attack + sum(companion_attack_rolls)`
- `player_side_defence = player_defence + sum(companion_defence_rolls)`

### Enemy Side

The enemy side consists of:
- one animal for solo encounters
- multiple animals for pack encounters

Enemy-side attack for the turn:
- each enemy member rolls its own attack
- all attack values are accumulated

Enemy-side defence for the turn:
- each enemy member can contribute defence
- for pack logic this may be:
  - a sum of defence values
  - or a per-target defence resolution
- for the first implementation, summed defence is acceptable and simpler

Suggested formulas:
- `enemy_side_attack = sum(enemy_member_attack_rolls)`
- `enemy_side_defence = sum(enemy_member_defence_rolls)`

### Damage Resolution

Damage should be accumulated per side.

Suggested player-to-enemy damage:
- `damage_to_enemy = max(0, player_side_attack - enemy_side_defence)`

Suggested enemy-to-player damage:
- `damage_to_player = max(0, enemy_side_attack - player_side_defence)`

This means:
- five wolves can all attack in one turn
- the total pressure from the pack is felt in that turn
- companions matter because they add both attack and defence to the player's side

### Pack Behavior

For packs:
- each animal still keeps its own health
- but pack attacks are resolved as accumulated side pressure
- once one member dies, the next turn uses the smaller pack size
- surround/howl bonuses should scale from current living pack count

Suggested pack-health rule:
- each enemy member has separate `health`
- pack total is not one shared HP bar
- attacks can either:
  - focus one target selected by the combat helper
  - or spread damage by later advanced rules

For first implementation:
- enemy side attack accumulates
- enemy side defence accumulates
- player damage is applied to one resolved target animal at a time
- enemy damage is applied to the player health pool

### Companion Behavior

Companions should contribute to the player side every round if active.

Companion rules:
- each active companion adds attack contribution
- each active companion adds defence contribution
- companions do not replace the player turn
- companions can later get their own health, but first implementation may use only support values

If later companion health is enabled:
- dead or disabled companions stop contributing
- wounded companions may contribute reduced values

Suggested damage rules:

- if `side_attack > side_defence`
  - `damage = max(1, side_attack - side_defence)`
- else
  - `damage = 0`

The combat helper layer should be pure Python and return a structured result, for example:

```python
{
    "winner": "player",
    "rounds": [...],
    "player_side_attack_last": 24,
    "player_side_defence_last": 18,
    "enemy_side_attack_last": 21,
    "enemy_side_defence_last": 13,
    "player_health_end": 74,
    "enemy_health_end": 0,
    "loot": {"wolf_pelt": 1},
}
```

Scene labels can then render text and pictures on top of that result.

### Dog Companion Actions

The dog is not just a passive stat bonus. If present in company, the dog should have its own selectable move each turn or a command slot resolved in the same turn.

Required dog moves:
- bite
- dead-lock bite
- guard
- harry / distract

Suggested dog behavior:
- `bite`
  - normal dog attack
  - adds direct attack contribution
- `dead-lock bite`
  - level-2 move
  - stronger bite
  - may reduce enemy defence or movement for the turn
- `guard`
  - adds defence to the player side
  - best when facing pack pressure
- `harry / distract`
  - small attack
  - increases player dodge chance or lowers one enemy action quality

Dog participation rules:
- only available if dog is in company
- dog must be alive
- if dog health reaches `0`, dog actions disappear until recovery
- dog hunt mode should automatically include the dog in hunting fights

### Status Effects

Combat needs explicit status effects for both player and enemies.

Required first statuses:
- bleed
- paralysis
- damage over time

Suggested runtime shape:

```python
{
    "bleed": {"turns": 5, "half_health_target": True},
    "paralysis": {"turns": 3},
    "poison": {"turns": 5, "damage_total": 25},
}
```

Required uses:
- arbalest shot applies `bleed`
- bees bomb applies `paralysis` and `25` total health loss over `5` turns

Rules:
- status ticks should be deterministic and visible in the combat log
- paralysis blocks or heavily reduces enemy actions while active


## Combat Level Unlocks

### Level 1

Exploration:
- `0..49`

Available:
- human fights
- tavern event fights
- scripted duel/fistfight scenes

Not yet available:
- hunting system

### Level 2

Exploration:
- `>= 50`

Fight level:
- `>= 2`

Unlock:
- hunting animals

This matches the requested threshold:
- once the player has more than `50` exploration points, hunting becomes available


## Hunting Module

Hunting is a combat-enabled exploration feature.

It should not be embedded directly into room narration. It should be its own module.

### Entry Rule

Player may hunt only if:
- `exploration >= 50`

### Hunt Flow

1. Enter hunting location
2. Roll an animal encounter
3. Start combat
4. Resolve combat
5. Grant loot on success
6. Apply damage/state loss on failure

### Hunt Retreat / Withdrawal

The player must be able to retreat from hunting.

Retreat rules:
- retreat is a normal turn action in hunt encounters
- retreat should show proper explanatory text
- retreat is not guaranteed to succeed against every enemy every turn

Suggested retreat outcomes:
- success:
  - player escapes combat
  - hunt ends with no loot
  - player loses `6` player-reputation points
- failure:
  - enemy gets a parting attack
  - next turn continues

Retreat should be described as:
- losing face
- coming back empty-handed
- failing to finish what the player started

### Low-Health Escape Sickness

If the player escapes from a hunt with very low health, there should be a recovery consequence.

Rule:
- if retreat succeeds while player `health` is below the configured low-health threshold, the player becomes sick for `2` days

Suggested threshold:
- `health <= 20`

Suggested runtime:
- `default SickDays = 0`

Effect:
- for the next `2` in-game days, the player is sick
- this should be applied through the normal day-advance helper, not through ad hoc scene flags

### Sickness And Renewal Systems

Because sickness advances time pressure, it must interact with renewal systems already planned for the player:
- clothes deterioration
- soap decay
- hair growth

That means sickness days should still count toward:
- dress age
- haircut age
- soap expiration

So if the player spends `2` days sick:
- dress renewal gets `+2` days older
- haircut gets `+2` days older
- soap gets `+2` days closer to expiration

### Animal Definitions

Huntable animals required for the first implementation:
- wolf
- wolf pack
- lone white wolf
- boar
- brown bear
- giant grizzly

Animal spawn probability must depend on:
- exploration points
- current forest zone
- rarity tier

#### Wolves

Wolves are common forest hunters and should have the best spawn probability.

Wolf variants:
- common wolf
- wolf pack
- lone white wolf

Wolf combat skills:
- dodge
- bite
- surround
- howl
- dead lock

Wolf rules:
- max pack size: `5`
- larger packs should appear deeper in the forest
- the white wolf is always alone
- the white wolf is rarer and stronger than a normal wolf

Suggested role:
- agile enemy
- moderate attack
- moderate defence
- medium-low health
- gains power from pack actions instead of raw health

#### Boars

Boars are tougher and more direct than wolves.

Boar combat skills:
- ram
- bite
- attack
- defend

Boar rules:
- max pack size: `3`
- stronger opening burst than wolves
- less dodge, more raw impact

Suggested role:
- high first-hit damage
- medium defence
- medium-high health

#### Bears

Bears are always lone high-danger encounters.

Bear variants:
- brown bear
- giant grizzly

Bear combat skills:
- bite
- claws
- strike
- roar

Bear rules:
- always solo
- low spawn probability
- high attack
- high defence
- high health
- giant grizzly is the rarest and hardest variant

Suggested role:
- heavy boss-style forest enemy
- brown bear is standard high danger
- giant grizzly is late-tier rare danger

### Animal Action Notes

Animal skills should be reusable data-driven actions, not hardcoded per scene.

Suggested action behavior:
- `dodge`: short defence spike or hit-cancel chance
- `bite`: basic damaging action
- `surround`: pack-size bonus to attack and pressure
- `howl`: morale / attack buff for wolves
- `dead_lock`: pinning effect or defence penalty on the player
- `ram`: strong opening boar strike
- `defend`: boar defence raise
- `claws`: heavy bear attack
- `strike`: strongest bear single hit
- `roar`: fear / pressure effect before later attacks

Animals should be data-driven, for example:

```python
{
    "id": "wolf",
    "name": "Волк",
    "health": 35,
    "attack_min": 8,
    "attack_max": 15,
    "defence_min": 4,
    "defence_max": 10,
    "loot": {
        "wolf_pelt_001": 1,
        "raw_meat_001": 2,
    },
}
```

### Per-Turn Enemy Actions

Each enemy turn should choose or roll one concrete action from its move list, not only a flat attack number.

Examples:
- wolf:
  - dodge
  - bite
  - surround
  - howl
  - dead lock
- boar:
  - ram
  - bite
  - attack
  - defend
- bear:
  - bite
  - claws
  - strike
  - roar

The action result should then feed the side-based attack/defence totals for that turn.

### Loot

Animal loot should use the same item/inventory model as the rest of the game.

Required loot:

#### Wolf Loot

- wolf skin / fur

Suggested item ids:
- `wolf_skin_001`

Price:
- wolf skin: `25`

#### Boar Loot

- boar fangs
- boar meat

Suggested item ids:
- `boar_fang_001`
- `boar_meat_001`

Prices:
- fang necklace value: `50`
- boar meat: `45`

#### Bear Loot

- bear fur
- bear claws

Suggested item ids:
- `bear_fur_brown_001`
- `bear_fur_grizzly_001`
- `bear_claw_001`

Prices:
- brown bear fur: `80`
- grizzly fur: `90`
- claw necklace value: `50`

Use:
- sold
- gifted
- optionally crafted later into trophy jewelry

Loot must be defined in data, not hardcoded into narration.


## Forest Resource Expansion

The fight/hunt module should align with the current forest-zone structure.

Current forest zone anchors:
- [Forest.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Forest.rpy)
- [ForestDarkWoods.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ForestDarkWoods.rpy)
- [ForestCave.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ForestCave.rpy)
- [ForestClearing.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ForestClearing.rpy)
- [ForestHiddenPath.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ForestHiddenPath.rpy)
- [ForestSpring.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ForestSpring.rpy)
- [ForestLake.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ForestLake.rpy)
- [ForestWaterfall.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ForestWaterfall.rpy)

Current common forest resources already present:
- `lumber_001`
- `mushroom_001`
- `berries_001`
- `honey_comb_001`

Add rare special gatherables:
- rare special mushroom
- rare special herbs
- lavender
- wild roses
- moss

Suggested item ids:
- `special_mushroom_001`
- `special_herbs_001`
- `lavender_001`
- `wild_rose_001`
- `moss_001`

Suggested zone placement:
- cave: moss, special mushroom
- deep forest / dark woods: wolves, bears, rare herbs
- clearings: lavender, wild roses
- hidden paths: herbs and rare gatherables


## Hunting Spawn Logic

Exploration should affect both unlocking and danger scaling.

### Exploration 50..99

Common:
- lone wolf
- small wolf pack
- lone boar

Rare:
- white wolf

Very rare:
- brown bear

### Exploration 100..149

Common:
- wolf pack
- boar pair
- white wolf

Rare:
- large wolf pack
- brown bear

Very rare:
- giant grizzly

### Exploration 150+

Common:
- large wolf pack
- boar group
- brown bear

Rare:
- white wolf
- giant grizzly

Zone weighting:
- safer forest zones should favor lone or lighter enemies
- deep forest should favor packs and bears
- cave-adjacent or darkest zones can have the rarest danger rolls


## Recommended Runtime Data

Add these defaults later during implementation:

```python
default health = 100
default company_list = []
default FightWeaponLoaded = 0
default FightRetreatUsed = 0
default SickDays = 0
default enemy_health = 0
default FightEnemyState = {}
default HuntUnlocked = False
default HuntLastResult = {}
```

Optional helper tables:

```python
default AnimalTable = []
default CombatLootTable = {}
default ForestHuntEncounterTable = {}
default ForestResourceSpawnTable = {}
```


## UI / Screen Integration

The combat module should follow the current screen policy:

- keep `main_ui` as the persistent owner
- use a dedicated `UI_mode`, for example:
  - `"fight"`
  - `"hunt"`
- do not create nested legacy menu overlays

Recommended:
- left panel: fight text + image
- right panel: combat choices
- action choices:
  - dodge
  - block
  - close attack
  - fire
  - reload
  - use item
  - retreat
  - command companion
  - command dog

This keeps combat consistent with the existing room/event/talk screen system.


## Images

Fight and hunting visuals should use the shared media path resolver, not hardcoded `.jpg` assumptions.

Current image path system:
- [ShowImage.rpy](c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ShowImage.rpy)

Use standard folder-based structure, for example:

- `images/animals/wolf_attack_1.png`
- `images/animals/boar_idle_1.png`
- `images/general/forest_hunt_day.png`

Room or fight backgrounds may later vary by time of day via the current shared background resolver.


## Test Requirements

When implemented, add regression coverage for:

1. `FightLevel["you"]` derives correctly from exploration
2. health clamps to `0..100`
3. weapon bonus affects attack
4. armor bonus affects defence
5. company bonus affects combat only when companion is present
6. hunting locked below `50` exploration
7. wolf/boar/bear encounter generation respects exploration tiers
8. deep forest increases hard-animal probability
9. loot tables return wolf, boar, and bear rewards correctly
10. rare forest resources appear only in the intended zones
7. hunting unlocked at `>= 50` exploration
8. successful hunt grants defined loot
9. failed hunt applies health loss without corrupting room UI


## Implementation Order

Recommended order:

1. Add pure Python combat stat helpers
2. Derive `FightLevel["you"]` from exploration
3. Add player `health`
4. Add weapon/armor combat readers
5. Add company list structure
6. Add generic fight result object
7. Add hunting unlock and animal table
8. Add `main_ui` fight mode
9. Add regression tests


## Summary

Final intended model:

- exploration drives fight growth
- every `50` exploration gives `+1` fight level
- player combat uses `health`, `attack`, `defence`
- attack/defence depend on fight skill, random roll, armor, weapon, companions
- player reputation and tavern reputation stay separate
- tavern crew interaction can use both reputations
- hunting unlocks at exploration level two (`> 50`)
- animals have defined loot tables
- combat remains modular and screen-driven, not embedded into ad hoc scene logic

