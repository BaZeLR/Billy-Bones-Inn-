# Methods Glossary

Last updated: 2026-06-06

This is a living glossary for canonical method and label names in the current project.

Purpose:
- keep naming consistent;
- make redundancy easier to spot;
- clarify which method is the preferred project entry point for a behavior;
- record known mixed or drifting patterns without renaming the project blindly.

Update rule:
- when a new canonical gameplay method/label is added, add it here;
- when an old path is replaced, mark the old one as legacy/drift here instead of silently letting both grow;
- do not treat this file as permission to redesign existing systems.

## Core Naming Rules

- Prefer the existing project owner method instead of creating a second helper with the same meaning.
- Room/UI flow should use room labels and direct room/object/NPC labels. Refresh/apply/renew/rebuild labels are compatibility/bloat, not target architecture.
- Inventory browsing is HUD/category-owned, not player-card-owned.
- Player card is profile/state/equipment summary UI, even if current code still contains mixed inventory paths.
- Gift flows must show giftable items only.
- Share flows must show shareable items only.
- Combat/hunting item use belongs to the combat/weapons section, not generic gift/social menus.

## Room And UI Flow

| Name | Canonical Use | Source |
| --- | --- | --- |
| `register_room_runtime(room_obj)` | Register a room object in the runtime registry. | `game/Inn/RoomTemplate.rpy` |
| `get_registered_room(room_code)` | Resolve the runtime `Room` object from a room code. | `game/Inn/RoomTemplate.rpy` |
| `movement_actions(target_label, movement_minutes=0)` | Builds a returnable time-cost call followed by a room jump, without nesting locations on Ren'Py's return stack. | `game/Utilities/Time/TimeTurnSystem.rpy` |
| `main_ui_restore_room_scene_state()` | Restore room HUD state after temporary menus/scenes. | `game/Inn/my_layouts/main_layout.rpy` |
| `main_ui_open_inventory_section(section_id)` | Canonical HUD entry into categorized inventory browsing. | `game/Inn/my_layouts/main_layout.rpy` |
| `main_ui_begin_talk_state(title, selected_char)` | Enter talk UI mode. | `game/Inn/my_layouts/main_layout.rpy` |
| `main_ui_end_talk_state()` | Exit talk UI mode back to room scene state. | `game/Inn/my_layouts/main_layout.rpy` |
| `main_ui_begin_native_scene_state(title="")` | Enter event/native-scene UI mode. | `game/Inn/my_layouts/main_layout.rpy` |
| `main_ui_end_native_scene_state()` | Exit event/native-scene UI mode back to room scene state. | `game/Inn/my_layouts/main_layout.rpy` |
| `RefreshCurrentActionMenu(where_id="", object_id="", preserve_text=False)` | Compatibility/bloat: room/action refresh dispatcher to remove as slices migrate. | `game/Inn/Actions.rpy` |
| `current_room_object_menu_label()` | Resolve the room’s object-menu label from the current room template. | `game/Inn/Actions.rpy` |

Notes:
- `show_player_card_main_ui_state()` is not the preferred inventory browsing entry.
- Inventory section browsing should come from `main_ui_open_inventory_section(...)`.

## Player Card And Inventory

| Name | Canonical Use | Source |
| --- | --- | --- |
| `show_player_card_main_ui_state()` | Open the player profile/card main menu. | `game/Inn/PlayerCard.rpy` |
| `PlayerCardMainMenu` | Label form of player-card main menu. | `game/Inn/PlayerCard.rpy` |
| `player_card_inventory_section_ids()` | Define inventory section keys. | `game/Inn/PlayerCard.rpy` |
| `player_card_inventory_section_title(section_id)` | Map section key to display title. | `game/Inn/PlayerCard.rpy` |
| `player_card_inventory_primary_section(item_id)` | Map an item to its canonical inventory section. | `game/Inn/PlayerCard.rpy` |
| `player_card_inventory_section_item_ids(section_id)` | Return item ids for one inventory category. | `game/Inn/PlayerCard.rpy` |
| `player_card_is_gift_item(item_id)` | Determine whether an item belongs to gift logic. | `game/Inn/PlayerCard.rpy` |
| `player_card_is_shareable_item(item_id)` | Determine whether an item belongs to share logic. | `game/Inn/PlayerCard.rpy` |
| `player_card_is_weapon_item(item_id)` | Determine whether an item belongs to combat/equipment logic. | `game/Inn/PlayerCard.rpy` |
| `player_card_giftable_item_ids()` | Build the gift-only item list. | `game/Inn/PlayerCard.rpy` |
| `player_card_shareable_item_ids()` | Build the share-only item list. | `game/Inn/PlayerCard.rpy` |
| `PlayerCardGiftItemMenu(item_id)` | Gift-target selection flow for one gift item. | `game/Inn/PlayerCard.rpy` |
| `PlayerCardShareItemMenu(item_id)` | Share-target selection flow for one shareable item. | `game/Inn/PlayerCard.rpy` |

Drift watch:
- `PlayerCardInventoryMenu`, `PlayerCardInventorySectionMenu`, and `PlayerCardInventoryItemMenu` exist now, but inventory ownership is mixed and should not expand further as the canonical model.
- Use them carefully while the project is being normalized; prefer HUD/category entry for new work.

## Inventory Storage And Item Mutation

| Name | Canonical Use | Source |
| --- | --- | --- |
| `_ensure_player_inventory_store()` | Normalize `playerItems` into the runtime inventory dict. | `game/Inn/Actions.rpy` |
| `_player_item_count_by_id(item_id)` | Canonical inventory count lookup. | `game/Inn/Actions.rpy` |
| `_player_inventory_item_ids(expand_stacks=False)` | Canonical inventory item-id iteration. | `game/Inn/Actions.rpy` |
| `_player_add_item_by_id(item_id, quantity=1)` | Add items to player inventory. | `game/Inn/Actions.rpy` |
| `_player_remove_item_by_id(item_id, quantity=1)` | Remove items from player inventory. | `game/Inn/Actions.rpy` |
| `_player_has_item_by_id(item_id)` | Presence check for one item id. | `game/Inn/Actions.rpy` |
| `_room_add_item_by_id(room_obj, item_id)` | Add one item to a room’s object list. | `game/Inn/Actions.rpy` |
| `_room_remove_item_by_id(room_obj, item_id)` | Remove one item from a room’s object list. | `game/Inn/Actions.rpy` |
| `_room_has_item_by_id(room_obj, item_id)` | Room item presence check. | `game/Inn/Actions.rpy` |
| `take(room_obj, item_id)` | Canonical room-to-player pickup logic. | `game/Inn/Actions.rpy` |
| `player_pick_up_item(room_obj, item_id)` | Public pickup wrapper. | `game/Inn/Actions.rpy` |
| `player_drop_item(room_obj, item_id)` | Canonical player-to-room drop logic. | `game/Inn/Actions.rpy` |
| `player_use_item(item_id, action_key="", consume_from_inventory=False)` | Generic item use/action application entry. | `game/Inn/Actions.rpy` |
| `player_apply_item_action(item_id, action_key="", consume_from_inventory=False)` | Alias-level item action application path. | `game/Inn/Actions.rpy` |
| `player_drink_item(item_id)` | Canonical drink item mutation. | `game/Inn/Actions.rpy` |
| `player_eat_item(item_id)` | Canonical food item mutation. | `game/Inn/Actions.rpy` |

Redundancy rule:
- prefer `_player_item_count_by_id(...)` over direct `playerItems[...]` reads in gameplay logic;
- prefer `player_drop_item(...)` over custom room-specific ad hoc drop logic unless the room needs explicit custom behavior.

## Social And Relationship Actions

| Name | Canonical Use | Source |
| --- | --- | --- |
| `apply_social_interaction_base(...)` | Compatibility helper for shared social mutation; do not hide authored talk/gift/flirt consequences behind it in new content. | `game/Inn/Actions.rpy` |
| `player_talk_to(char_name)` | Compatibility helper for generic talk mutation; NPC talk labels should own visible choices and direct consequences. | `game/Inn/Actions.rpy` |
| `player_gift_to(char_name, ..., gift_item_id="")` | Compatibility helper for generic gift mutation; NPC gift labels should own visible choices and direct consequences. | `game/Inn/Actions.rpy` |
| `player_share_item_with(char_name, item_id)` | Compatibility helper for generic share mutation. | `game/Inn/Actions.rpy` |
| `player_flirt_with(char_name)` | Compatibility helper for generic flirt mutation; NPC talk labels should own visible flirt choices and direct consequences. | `game/Inn/Actions.rpy` |
| `_social_item_rule(item_id="", char_name="")` | Social item-effect rule resolver. | `game/Inn/Actions.rpy` |
| `player_apply_item_social_effects(char_name="", item_id="", from_gift=False)` | Apply item-based relationship effects. | `game/Inn/Actions.rpy` |

Rule:
- gift logic should use giftable items;
- share logic should use shareable items;
- do not merge them into one generic “social inventory” bucket.

## NPC Schedule And Location

| Name | Canonical Use | Source |
| --- | --- | --- |
| `npc_schedule_set(npc_id, entries)` | Set one NPC’s schedule entries. | `game/Inn/NPCScheduleModel.rpy` |
| `npc_schedule_add(npc_id, entry)` | Append one schedule entry. | `game/Inn/NPCScheduleModel.rpy` |
| `npc_schedule_sorted_entries(npc_id)` | Return ordered schedule entries. | `game/Inn/NPCScheduleModel.rpy` |
| `npc_schedule_resolve(npc_id, weekday_value=None, time_value=None)` | Resolve the active schedule entry. | `game/Inn/NPCScheduleModel.rpy` |
| `npc_schedule_location(npc_id, weekday_value=None, time_value=None)` | Resolve the active scheduled location. | `game/Inn/NPCScheduleModel.rpy` |
| `npc_schedule_state(npc_id, weekday_value=None, time_value=None)` | Resolve the full current schedule state. | `game/Inn/NPCScheduleModel.rpy` |
| `npc_schedule_sync_currentloc(npc_id, weekday_value=None, time_value=None)` | Sync schedule truth into `CurrentLoc[npc_id]`. | `game/Inn/NPCScheduleModel.rpy` |
| `npc_schedule_sync_all(weekday_value=None, time_value=None)` | Sync all scheduled NPCs. | `game/Inn/NPCScheduleModel.rpy` |
| `getLocation(person, weekday_value=None, time_value=None)` | Project-facing NPC location accessor. | `game/Inn/NPCScheduleModel.rpy` |
| `getNPCids(location, weekday_value=None, time_value=None)` | NPC ids currently in one location. | `game/Inn/NPCScheduleModel.rpy` |
| `getNPCnames(location, weekday_value=None, time_value=None)` | NPC names currently in one location. | `game/Inn/NPCScheduleModel.rpy` |

Truth rule:
- `npc_schedule_location(...)` is the resolver;
- `CurrentLoc[npc_id]` is the synced mirror used by the wider game;
- avoid ad hoc room-specific location calculations if schedule truth already exists.

## Story Event And Thread Runtime

| Name | Canonical Use | Source |
| --- | --- | --- |
| `initStoryEventRuntime(force=False)` | Initialize event/thread runtime. | `game/Inn/StoryEventRuntime.rpy` |
| `loadThreadData(thread_list)` | Load raw thread definitions. | `game/Inn/StoryEventRuntime.rpy` |
| `createThread(data)` | Build one thread runtime object from thread data. | `game/Inn/StoryEventRuntime.rpy` |
| `createThreads()` | Build the global `threads` store. | `game/Inn/StoryEventRuntime.rpy` |
| `findAvailableEvents(forced=False)` | Recompute currently available events. | `game/Inn/StoryEventRuntime.rpy` |
| `story_event_available(location_name="", action_name="")` | Public availability check for story-triggered room actions. | `game/Inn/StoryEventRuntime.rpy` |
| `checkTriggers(location, action, numpop=0)` | Trigger dispatcher for available story events. | `game/Inn/StoryEventRuntime.rpy` |
| `preEvent(thread_name=None)` | Pre-event hook before jumping into the event label. | `game/Inn/StoryEventRuntime.rpy` |
| `story_thread_advance_current()` | Canonical “advance current thread” helper for event labels. | `game/Inn/StoryEventRuntime.rpy` |
| `CheckDailyEvent(...)` | Daily-event dispatcher; keep distinct from thread/story runtime. | `game/Inn/CheckDailyEvent.rpy` |
| `DailyEventsList_Add(...)` | Add a daily event entry. | `game/Inn/CheckDailyEvent.rpy` |
| `DailyEventsList_PopMatch(...)` | Resolve/remove a matching daily event entry. | `game/Inn/CheckDailyEvent.rpy` |

Rule:
- use story thread/event runtime for story-owned thread events;
- use daily-event runtime for daily/room routine prompts;
- do not mix them casually just because both can fire on room entry.

## Room-Specific Pattern Example

| Name | Canonical Use | Source |
| --- | --- | --- |
| `tavern_my_room_apply_scene_state()` | Example of room-owned picture/text rebuild method. | `game/Inn/TavernMyRoom.rpy` |
| `TavernMyRoomBuildActions` | Example of room-owned action rebuild label. | `game/Inn/TavernMyRoom.rpy` |
| `TavernMyRoomObjectMenu(object_id="", refresh_only=False)` | Example of room object-menu label. | `game/Inn/TavernMyRoom.rpy` |

Pattern:
- room owns room scene state;
- room rebuild label owns action list rebuilding;
- object menu label owns one room object’s local interaction menu.

## Known Naming Drift To Watch

- `PlayerCard*Inventory*` names still imply inventory ownership by the player card.
- Inventory browsing should settle under HUD/category language, not expand under player-card language.
- `getLocation(...)` and `npc_schedule_location(...)` overlap semantically; keep one clear precedence in code comments and call sites.
- `CheckDailyEvent(...)` and `checkTriggers(...)` are different systems and should not be treated as interchangeable.
