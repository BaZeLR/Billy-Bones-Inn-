# General Game Description

This document describes the intended high-level game structure.

The game is built from a small set of first-class systems. Each system owns its
own state and rules. Other systems may ask it questions or call its public
methods, but should not keep parallel state for the same thing.

## Core Rule

There must be one source of truth for current game state.

Examples:

- NPC current state belongs to the NPC class instance.
- Player current state belongs to the player model.
- Room open state, description, picture, navigation, and visible objects belong
  to the room model.
- NPC visibility belongs to NPC state and visibility rules.
- Object actions belong to game objects.
- Story flow belongs to event/thread labels and event/thread objects.
- Screens display state and player choices. Screens do not own gameplay state.

Classes and their instances are authoritative. Legacy dicts and scalar variables
are not model owners. They may exist only as temporary compatibility output while
old labels still read them, and must be deleted when the old read path is
converted.

Because class instances are authoritative, a saved game checkpoint must preserve
the current state of those instances. Loading a checkpoint should restore the
same intact gameplay instances for NPCs, player, rooms, events/threads, tavern,
fight, sex, and other systems.

## Main Systems

### Game Loop

The game loop coordinates the current day, time progression, work cycles, event
checks, daily resets, achievements, and ending conditions.

It does not duplicate state from NPCs, rooms, player, tavern, or events. It
advances systems and asks each system to update what it owns.

### Player

The player system owns player identity, stats, money, inventory access, skills,
conditions, reputation, notoriety, and other player-specific state.

Basic player-side actions such as wash, eat, drink, rest, wait, and simple
chores should be direct labels or small Player/domain methods. They mutate the
authoritative owner, apply time cost, show optional picture/text, and return to
the current room/object flow. NPC interaction, purchasing, item use, crafting,
fight, hunt, and sex are separate systems.

### NPCs

NPCs use a class hierarchy:

- `PeopleData`: static person data.
- `PeopleInfo`: common mutable person state.
- `BaseNPC`: shared NPC behavior.
- `Girl`: shared girl behavior.
- Individual NPC classes: unique story state and custom methods.

Each real recurring character NPC class instance is the source of truth for that
NPC. For example, `Amanda`, `Melissa`, `Eddie`, `Francheska`, and other NPC
objects own their current known state, location, relationship state, schedule
behavior, and custom story methods.

`peopleInfo` is a registry that points to existing NPC instances. It must not
rebuild NPCs from legacy dicts as normal runtime behavior. A missing NPC entry is
a registration bug, not permission to invent a generic fallback NPC.

`girls` and `secondary_npcs` are typed lists used for common feature loops. They
are not alternate state stores.

Not every named person in text is a character NPC. Some generated or descriptive
people are story reminders only and may use random names from a generator. They
do not need classes or persistent parameters. Fight-spawned animals, creatures,
patrols, and hunt enemies are combat entities, not character NPCs unless they
also exist as recurring story characters.

### Tavern

The tavern is a first-class management system. It owns tavern state, rooms,
services, reputation, income, expenses, upgrades, customer flow, and tavern-wide
conditions.

The tavern system should coordinate with rooms, NPCs, jobs, economy, and reports
without duplicating their internal state.

### Tavern Team

The tavern team system owns staff assignments and work roles. This includes
waitering, cleaning, cooking, prostitution, security, and other tavern work.

Workers are still NPCs. The tavern team records team-level work assignment and
work-cycle state; individual NPC state remains on the NPC instance.

### Rooms

Rooms are location models. A normal room owns:

- code name and display name
- schedule or always-open status
- current picture or time-dependent picture
- current description
- navigation exits
- visible objects
- explicit custom room actions, only when the room itself is the target
- hosted event availability

Rooms should not own normal gameplay actions. Actions belong to visible objects,
NPCs, or events. A room may have custom room actions only when the room itself is
the acted-on thing, such as search, clean, or explore.

NPCs are not owned by rooms. NPC presence is derived from NPC class instances
through `getLocation()` and NPC visibility methods. The HUD/panel may show NPCs
whose current location is the current room, and selecting one opens that NPC's
interaction menu.

### Game Objects

Game objects are interactable things inside rooms: doors, beds, bars, shelves,
windows, furniture, work spots, and similar objects.

Object actions belong to game objects and their labels/procedures. A room can
show an object, but the object owns what can be done with it.

### Items And Inventory

Items and inventory own player-held things, resources, use actions, gifts,
crafting materials, equipment, and tradeable goods.

Items should define item behavior. Shops, crafting, NPC gifts, and player use
should call item/inventory APIs instead of duplicating item state.

### Calendar And Time

Calendar/time owns day, week, clock, time advancement, time periods, and daily
or weekly reset triggers.

Other systems may ask current time or subscribe to time changes, but they should
not compute independent time models.

### Event And Thread System

Events and threads own story availability, progress, transitions, outcomes, and
story labels.

Event labels own story flow, text, menus, pictures, state changes, and returns.
Screens may render the menu area, but screens must not decide story progression.

### Fight

Fight owns combat state, enemies, player combat resources, combat actions,
escape, results, loot, and loss handling.

Fight UI should display combat state. Fight rules and state changes belong to
fight system code and fight labels.

### Sex Engine

Sex engine owns sex state, body interaction, act flow, arousal/orgasm state,
finish options, pregnancy-related outcomes, and return flow.

NPC-specific sex behavior can be customized in NPC classes or NPC-specific sex
labels, but common mechanics belong to the sex engine.

### Economy And Shops

Economy/shops own prices, stock, buy/sell flow, wages, fees, tavern income,
expenses, and market-related state.

### Jobs, Chores, And Work

Jobs/chores/work own tasks, work availability, worker assignment effects, work
results, and daily work limits.

Tavern team uses this system for tavern work. Other venues can use it for their
own work flows.

### Social And Relationships

Social/relationship systems own common talk, flirt, gift, relationship changes,
reputation effects, jealousy, favor, hostility, and similar social mechanics.

Individual NPCs may override or customize behavior through class methods.

### Navigation And Travel

Navigation/travel owns movement between physical locations, travel constraints,
return targets, and route-specific travel events.

Rooms expose exits. Navigation decides movement validity and travel flow.

### Reports

Reports show current state across systems. Reports may include:

- player report
- tavern report
- tavern team report
- NPC report
- room/location report
- economy report
- event/thread report
- debug report

Reports are read-only views. They must not become state owners.

### Achievements And Endings

Achievements and endings own long-term unlocks, achievement checks, ending
conditions, ending selection, and final outcome flow.

They observe other systems through public state and methods.

### Assets And Media

Assets/media owns picture path conventions, portraits, room images, event
images, fight images, and UI media assets.

Normal room browsing should use room pictures. Event labels should use event
images with the established scene display method.

### Screens

Screens render UI: HUD, menus, cards, reports, debug panels, and visual layout.

Screens do not own gameplay state, story progression, room behavior, NPC logic,
fight rules, sex rules, or tavern rules.

### Debug And Test Tools

Debug and test tools inspect and exercise the game systems. They may report
state and run controlled test paths. They should not introduce gameplay runtime
architecture.

### Save And Migration

Save/load works with current class instances. At any given moment, gameplay state
must be present on the authoritative instances so Ren'Py can save and load that
checkpoint without reconstructing state from parallel dicts.

Save/migration code may copy old save data into the current class-based model
when needed.

Migration is a boundary operation. After migration, current class instances own
state. Legacy dicts may be written as compatibility output only while old labels
still require them.

## Dependency Direction

Preferred direction:

1. Screens ask systems for state and display it.
2. Rooms expose navigation, visible objects, explicit room actions, and hosted
   events.
3. Objects, NPCs, and events own actions.
4. Systems own rules and state.
5. Game loop advances systems.
6. Reports read systems.

Avoid:

- wrapper layers for one action
- refresh/rebuild labels as architecture
- dispatcher layers where a direct label or method is enough
- recursive menu loops
- duplicated state in dicts and class instances
- room actions that belong to NPCs, objects, or events
- screens mutating gameplay state
