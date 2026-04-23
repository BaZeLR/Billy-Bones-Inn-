# Variables Glossary

Last updated: 2026-04-21

This is a living glossary for canonical runtime variable names in the current project.

Purpose:
- keep naming and ownership consistent;
- make duplicate state easier to detect;
- document which variable is the project truth and which variables are only UI/runtime mirrors.

Update rule:
- when a new persistent gameplay variable is added, add it here;
- when a variable is only a UI helper or transition value, mark it clearly as such;
- do not create second truth layers when a variable already exists.

## Core Naming Rules

- Persistent game truth belongs in existing defaulted/project-owned variables.
- UI helper variables must not become new game-truth layers.
- Use one variable for one meaning.
- If a variable is only a view helper, document it as a helper and avoid spreading it into gameplay logic.

## Player Location, Room, And UI State

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `CurLoc` | Player’s current room code. | many room labels, main UI | Canonical player location code. |
| `CurrentRoom` | Runtime `Room` object for the current room. | `game/Inn/my_layouts/main_layout.rpy` | Object-level room truth for menus and room methods. |
| `current_room_code` | UI/runtime copy of current room code. | `game/Inn/my_layouts/main_layout.rpy` | Helper only; do not replace `CurLoc`. |
| `scene_image` | Current room or event image path shown in UI. | `game/Inn/my_layouts/main_layout.rpy` | Display helper, not world truth. |
| `UI_mode` | Active HUD mode such as `scene`, `talk`, or `event`. | `game/Inn/my_layouts/main_layout.rpy` | UI state only. |
| `UI_selected_char` | Current selected character in talk/social UI. | `game/Inn/my_layouts/main_layout.rpy` | UI helper only. |
| `current_action_title` | Current right-panel action title. | `game/Inn/my_layouts/main_layout.rpy` | UI helper only. |
| `current_action_content` | Current right-panel content payload. | `game/Inn/my_layouts/main_layout.rpy` | UI helper only. |
| `current_action_items` | Current right-panel menu items. | `game/Inn/my_layouts/main_layout.rpy` | UI helper only. |
| `current_girl_key` | Currently selected NPC key for UI flow. | `game/Inn/my_layouts/main_layout.rpy` | UI helper only. |
| `current_object_id` | Current selected room object id. | `game/Inn/my_layouts/main_layout.rpy` | UI helper only. |
| `main_ui_inventory_dropdown_open` | Whether the HUD inventory dropdown is open. | `game/Inn/my_layouts/main_layout.rpy` | HUD helper only. |
| `action_override_text` | Temporary room/object text override after a local action. | `game/Inn/Actions.rpy` | Temporary helper; do not reuse as narrative truth. |

Rule:
- `CurLoc` and `CurrentRoom` are the core room truth pair;
- `current_*` variables are UI transport/view state, not gameplay ownership.

## Player Inventory And Equipment

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `playerItems` | Player inventory store. | `game/Inn/Intro.rpy`, normalized in `Actions.rpy` | Canonical player inventory truth. |
| `EquippedWeapon` | Current equipped weapon item id. | used in `PlayerCard.rpy`, combat, item runtime | Equipment truth. |
| `EquippedArmor` | Current equipped armor item id. | used in `PlayerCard.rpy`, room text | Equipment truth. |
| `player_inventory_view_mode` | Current player-card inventory subview mode. | `game/Inn/PlayerCard.rpy` | View helper only. |
| `player_inventory_view_section` | Current player-card inventory section view. | `game/Inn/PlayerCard.rpy` | View helper only. |
| `player_inventory_view_item` | Current player-card inventory item view. | `game/Inn/PlayerCard.rpy` | View helper only. |
| `player_card_inventory_origin` | Where the current inventory view was opened from. | `game/Inn/PlayerCard.rpy` | Transitional helper; do not grow this pattern further. |

Rule:
- `playerItems` is the inventory truth;
- inventory categorization is derived from item metadata, not stored as a second inventory variable.

## Inventory Categories

| Category Key | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `loot` | gathered resources / loot items | `game/Inn/PlayerCard.rpy` | category key |
| `gifts` | gift-oriented items | `game/Inn/PlayerCard.rpy` | gifting should display these only |
| `weapons` | combat / hunting / wearable protection items | `game/Inn/PlayerCard.rpy` | use for fight/hunt equipment browsing |
| `backpack` | general carried items / tools / misc | `game/Inn/PlayerCard.rpy` | catch-all carried section |

Rule:
- gift flows should use `player_card_giftable_item_ids()`;
- share flows should use `player_card_shareable_item_ids()`;
- do not flatten all item types into one generic player-card list.

## Time And Calendar

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `dayspassed` | absolute day counter used by the runtime. | `game/Inn/StoryEventRuntime.rpy` | canonical day-count truth |
| `week` | current weekday/week slot used by schedules and events. | used across schedule/event code | calendar truth |
| `time` | broad time-of-day slot. | used across rooms/events | coarse time bucket |
| `hour` | current clock hour. | used across room/event checks | fine time truth |
| `minute` | current clock minute. | used across calendar functions | fine time truth |
| `evalTime` | event-runtime cached evaluation time. | `game/Inn/StoryEventRuntime.rpy` | event-system helper |

Rule:
- if event gating depends on exact hour/minute, use the actual time variables;
- if UI or schedule only needs a slot, `time` may be enough.

## Story Event And Thread Runtime

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `active_event` | Current event object being run. | `game/Inn/StoryEventRuntime.rpy` | story-event runtime truth |
| `story_events` | Global story-event definitions/runtime list. | `game/Inn/StoryEventRuntime.rpy` | story runtime |
| `random_events` | Random event list. | `game/Inn/StoryEventRuntime.rpy` | event runtime |
| `tavern_work_events` | Tavern work event list. | `game/Inn/StoryEventRuntime.rpy` | event runtime |
| `availEvents` | Location/action-indexed available event map. | `game/Inn/StoryEventRuntime.rpy` | computed availability cache |
| `threads` | Global thread runtime store. | `game/Inn/StoryEventRuntime.rpy` | canonical thread store |
| `thread` | Current active thread in scene/event context. | `game/Inn/StoryEventRuntime.rpy` | contextual pointer |
| `story_thread_levels` | Thread level gating state. | `game/Inn/StoryEventRuntime.rpy` | thread gating |
| `eventLocations` | Known story-event locations set. | `game/Inn/StoryEventRuntime.rpy` | runtime helper |
| `eventPeople` | Known story-event people set. | `game/Inn/StoryEventRuntime.rpy` | runtime helper |
| `eventTalk` | Story-event talk flags/set. | `game/Inn/StoryEventRuntime.rpy` | runtime helper |
| `eventOptions` | Story-event options set. | `game/Inn/StoryEventRuntime.rpy` | runtime helper |
| `eventItems` | Story-event item set. | `game/Inn/StoryEventRuntime.rpy` | runtime helper |

Rule:
- `threads` and `active_event` are runtime truth;
- per-scene `thread` is just the current thread pointer used by scene labels.

## Daily Event Runtime

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `DailyEventsList` style structures | daily event queue/store | `game/Inn/CheckDailyEvent.rpy` | separate system from story threads |

Rule:
- daily-event variables belong to daily events only;
- do not use them as shadow storage for story threads.

## NPC Identity, Presence, And Relationship

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `RealName[npc_id]` | Known/display name of an NPC. | project data tables | canonical known-name lookup |
| `knowsMC[npc_id]` | Whether the player knows the NPC. | project data tables | knowledge truth |
| `Friends[npc_id]` | Core relationship/friendship value. | project data tables | relationship truth |
| `CurrentLoc[npc_id]` | Current synced NPC location. | project data tables, schedule sync | mirror of scheduler truth |
| `AmandaVar` / `MelissaVar` / `SandraVar` / etc. | Per-NPC custom state tables. | project data tables | canonical custom NPC state |
| `GiftedToday[npc_id]` | Gift usage/cooldown state for one day. | project data tables | social state |
| `TalkedToday[npc_id]` | Talk usage/cooldown state for one day. | project data tables | social state |
| `FlirtedToday[npc_id]` | Flirt usage/cooldown state for one day. | project data tables | social state |

Rule:
- use existing per-NPC tables directly;
- do not duplicate them inside menu state or temporary scene containers.

## NPC Age And Birthday Data

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `age` | Player age scalar. | `game/Inn/Intro.rpy` | player-only age |
| `age_girls[npc_id]` | Canonical NPC age value. | `game/Inn/Intro.rpy`, NPC init files | preferred NPC age storage |
| `DateOfBirth[npc_id]` | Canonical NPC birthday/birth record. | `game/Inn/Intro.rpy`, NPC init files | use for birthday/day-match logic |
| `Age[...]` | Legacy non-canonical NPC age dict. | `game/Inn/BeckyHomeFront.rpy` | naming drift; do not extend |

Rule:
- `age` is the player age scalar.
- NPC ages should use `age_girls[npc_id]`.
- NPC birthday/date logic should use `DateOfBirth[npc_id]`.
- `Age` with a capital letter is legacy drift and should not be used as a canonical pattern.

## NPC Scheduling

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `NPCSchedules` | Master NPC schedule store. | `game/Inn/NPCScheduleModel.rpy` | canonical schedule truth |

Rule:
- `NPCSchedules` is the schedule source;
- `CurrentLoc[npc_id]` should be treated as a synced projection of schedule truth plus explicit overrides.

## Room Runtime

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `roomFirstVisit[room_code]` | Whether the player has visited a room before. | `game/Inn/RoomTemplate.rpy` | room progression truth |

## Player Core Stats And Development

| Variable | Meaning | Source | Notes |
| --- | --- | --- | --- |
| `energy` | Player stamina/energy. | project data | player truth |
| `fun` | Player enjoyment/mood. | project data | player truth |
| `look` | Player appearance score. | project data | player truth |
| `charisma` | Player charisma score. | project data | player truth |
| `exploration` | Player exploration progression. | project data | player truth |
| `notoriety` | Player reputation/notoriety. | project data | player truth |
| `money` | Player money. | project data | player truth |
| `MyDresses` | Owned dresses/costumes. | project data | player wardrobe truth |
| `MyCurDress` | Currently worn dress code. | project data | player wardrobe truth |

## Redundancy Watchlist

- `CurLoc` vs `current_room_code`
  - `CurLoc` is gameplay truth.
  - `current_room_code` is a UI/runtime helper.
- `age` vs `age_girls` vs `Age`
  - `age` is player age.
  - `age_girls[npc_id]` is the intended NPC age store.
  - `Age[...]` is legacy duplicate/drift and should be removed or migrated.
- `NPCSchedules` vs `CurrentLoc`
  - `NPCSchedules` is schedule truth.
  - `CurrentLoc[npc_id]` is the synced active location mirror.
- player card inventory view variables
  - helper state only; do not build new gameplay logic on top of them.
- `current_action_*` variables
  - right-panel UI state only; do not treat them as persistent gameplay ownership.
