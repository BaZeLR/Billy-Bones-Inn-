# Player Development

## Goal

Define the long-term player progression layer that connects:

- chores
- tavern life
- Sandra relationship progression
- Becky-related progression gates
- exploration
- player upkeep
- encounter systems

This document is a design/spec reference for later implementation.


## Core Player Stats

### Fun

Range:

- `0..100`

Purpose:

- represents the player's general drive and willingness to engage with work/life

Rules:

- if `fun < 26`, the player will refuse to do chores

Fun increases from:

- sex encounters
- drinking ale
- tavern reputation growth
- receiving or acquiring a new costume

Fun is affected by:

- tavern reputation
- charisma
- encounter quality


### Exploration

Purpose:

- tracks player development outside the tavern

Effects:

- improves fight skills
- opens additional money-making opportunities outside tavern life
- should influence external encounters and side-content access


### Energy

Purpose:

- limits active player effort

Rules:

- low energy restricts activity
- energy is restored by sleep


### Notoriety

Purpose:

- tracks how much attention the player has attracted through risky or loud behavior

Rules:

- increases from:
  - fights
  - sexual encounters
- resets to `0` after sleep

Effects:

- high notoriety increases probability of being caught by city night patrols


### Charisma

Purpose:

- represents player attractiveness/presence in social and encounter systems

Composition:

- look
- clothing quality/state
- haircut freshness
- hygiene

Effects:

- affects encounter quality and success
- affects tavern-facing and city-facing interactions
- contributes indirectly to fun


## Look / Upkeep Layer

Charisma should be strongly influenced by personal upkeep.

### Costume State

Rules:

- costume decay: `20%` per month

Effects:

- reduced look value
- reduced charisma contribution


### Hair

Rules:

- haircut needed once per month

Effects:

- overdue haircut reduces look


### Hygiene

Rules:

- hygiene maintenance needed every `3` days

Effects:

- poor hygiene reduces look
- poor hygiene reduces charisma


## Chores System

Planned chores:

- `bring_woods`
- `chop_wood`
- `make_fire`
- `clean_ashes`
- `boil_water`
- `clean_upstairs_rooms`

Current weekly rule:

- every chore has a weekly counter with target `3`
- any value below `2` does not count for Sandra's weekly check

### Chore Effects

#### Bring Woods

Requirements:

- player needs an axe
- action sends the player to `Forest` later, once the room is wired

Effects:

- time `+8 hours`
- fun `+25`
- energy `-40`
- exploration `+1`
- tavern cleanliness `-15`
- `lamber +1` in tavern inventory
- `bring_woods +1` in weekly chores

Notes:

- one `lamber` is enough for `4` days of chopping/fire use

#### Chop Wood

Requirements:

- at least one `lamber`

Effects:

- time `+1 hour`
- energy `-10`
- fun `+15`
- fight level `+1`
- hygiene/look `-10`
- exploration `+1`
- consumes `1 lamber`
- adds chopped wood stock

#### Make Fire

Requirements:

- chopped wood available

Effects:

- energy `-5`
- exploration `+1`
- consumes chopped wood
- resets ash state

#### Clean Ashes

Effects:

- fun `-10`
- energy `-5`
- exploration `+1`
- ash state should be cleared

Rule:

- ashes should need cleaning once every `2` days

#### Boil Water

Requirements:

- wood/fire available

Effects:

- time `+1 hour`
- fun `-10`
- energy `-5`
- tavern cleanliness `-4`
- exploration `+1`
- prepares hot water

#### Clean Upstairs Rooms

Notes:

- these are rooms, not game objects

Effects:

- fun `-25`
- energy `-15`
- hygiene/look `-20`
- exploration `+1`

Design intent:

- chores are a weekly player-responsibility layer
- they affect tavern household order
- they affect Sandra relationship progression

Weekly target rule:

- each tracked chore counter should reach at least `2` out of `3` available for the week


## Weekly Sandra Check

Timing:

- every Saturday morning
- occurs together with tavern reports / wake-up flow

Evaluation:

- check each chore counter
- each required chore should be at least `2 / 3`

Success result:

- add `+1` Sandra friendship

Failure result:

- remove `1` Sandra friendship point
- increase tavern staff rebellion by `1`


## Tavern Staff Rebellion

Purpose:

- tracks discontent among tavern workers when the player neglects obligations

Increase:

- failed weekly chores check

Decrease:

- Sandra also checks tavern client-flow increase
- increased client flow reduces rebellion points

Design intent:

- rebellion is a pressure mechanic
- chores are not only relationship content, but tavern-management responsibility


## Sandra Week 5 Event Gate

At game week `5`:

Trigger requirements:

- Sandra friendship reaches at least `10`
- Becky progression is sufficiently advanced

Result:

- Sandra visits the player room
- spicy event starts

Design intent:

- weekly chores and tavern responsibility should feed directly into relationship content


## Becky Dependency

Sandra’s week 5 event is not standalone.

It also depends on:

- Becky progression state

This means Sandra’s route should partially branch through broader tavern/social progress, not only chores.


## Tavern Reputation Interaction

Tavern reputation should be connected to player progression.

Effects:

- higher tavern reputation improves encounter quality
- higher tavern reputation contributes to fun
- higher tavern performance helps reduce rebellion pressure


## Encounter Interaction Model

Player progression should feed back into encounter systems.

### Reputation + Charisma

Should affect:

- encounter availability
- encounter outcomes
- encounter quality

### Encounters

Should affect:

- fun
- notoriety
- possibly energy


## Sleep Reset / Recovery Model

Sleep should be a daily reset point.

On sleep:

- restore energy
- reset notoriety to `0`
- advance upkeep timers as needed


## Suggested Implementation Groups

### Group 1: Player Stats Layer

Add and centralize:

- `fun`
- `exploration`
- `energy`
- `notoriety`
- `charisma`
- `rebellion`


### Group 2: Upkeep Layer

Track:

- costume condition
- haircut freshness
- hygiene freshness


### Group 3: Chore Layer

Track weekly counters:

- bring woods
- chop wood
- make fire
- clean ashes
- boil water
- clean upstairs rooms


## Basic Player Recovery Actions

### Eat

Effects:

- time `+30 minutes`
- energy `+20`
- fun `+5`

### Drink

Effects:

- time `+30 minutes`
- energy `+10`
- fun `+5`


## Room Structure Needed For Chores

Planned connected service spaces:

- `Kitchen`
  - should give access to `Backyard`
- `Backyard`
  - `Shed`
  - `Stables`
  - wooden toilet object/container with:
    - busy/free state
    - locked door while busy
    - own description
  - fireplace
  - huge water barrel
- `Shed`
  - washing sink
  - stored `lamber`
  - stored chopped wood
  - old axe
- `Forest`
  - target room for `bring_woods`
- `Attic`
  - hidden room in player room, unlocked/visible later


## Exploration Gate

Rule:

- if `exploration > 15`, the player can begin to discover hidden rooms and objects

Example:

- `Attic` in the player room


### Group 4: Weekly Evaluation

Saturday report check:

- evaluate chores
- apply Sandra friendship result
- apply rebellion change
- apply client-flow rebellion reduction


### Group 5: Relationship Gate

At week 5:

- evaluate Sandra friendship
- evaluate Becky progression
- trigger player-room event if conditions are met


## Notes

- this is a design document, not implementation
- existing tavern report and chores systems should be reviewed before code integration
- player stat ownership should be defined once, without `globals()` bootstrap or redundant aliases
