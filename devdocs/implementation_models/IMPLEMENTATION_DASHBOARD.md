# Implementation Dashboard

This dashboard tracks conversion toward the intended model:

- class instances are authoritative
- one source of truth
- explicit class/template ownership
- no accidental bloat
- no parallel state

## Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` done
- `[!]` blocked or risky

## Core Systems

| System | Model Doc | Template | Runtime Owner | Status | Notes |
|---|---|---|---|---|---|
| NPCs | `NPC_MODEL_AND_TEMPLATE.md` | included | NPC class instance | [~] | Classes are authoritative; legacy dict authority must be removed. |
| Rooms | `ROOM_MODEL_AND_TEMPLATE.md` | included | Room object | [~] | Need remove room action bloat, old schedule forms, and room-owned NPC lists. |
| Events/Threads | `EVENT_THREAD_MODEL_AND_TEMPLATE.md` | included | Thread/Event objects + labels | [~] | Need keep labels direct and screens display-only. |
| GameObjects | pending | pending | GameObject instance | [ ] | Needed after room/NPC/event model is stable. |
| Player | `PLAYER_MODEL_AND_TEMPLATE.md` | included | Player class instance | [~] | Basic player actions are direct labels/methods; mixed `Actions.rpy` departments must be split. |
| Calendar/Time | pending | pending | calendar/time model | [ ] | Must enforce one source for time/day/week. |
| Tavern | pending | pending | tavern model | [ ] | Includes tavern economy/state. |
| TavernTeam | pending | pending | team/work model | [ ] | Staff assignments and work roles. |
| Fight | pending | pending | fight state/model | [ ] | Need combat screen/control standard. |
| SexEngine | pending | pending | sex engine state | [ ] | Need finish/return standard. |
| Reports | pending | pending | read-only report views | [ ] | Reports must not mutate state. |
| Screens | pending | pending | UI only | [ ] | Display-only rule must be enforced. |

## NPC Implementation Tasks

| Task | Status | Rule |
|---|---|---|
| Define class ownership rule | [x] | NPC class instance is source of truth. |
| Define NPC template | [x] | Static data + runtime class + registration. |
| Put `unknown_name` on NPC classes | [~] | Class owns unknown display name. |
| Remove dict rebuild authority | [~] | No normal rebuild from legacy dicts. |
| Remove dict-owned unique state | [ ] | Unique state becomes class fields/methods. |
| Remove fallback NPC creation | [ ] | Missing NPC should be registration bug. |
| Verify NPC save/load authority | [ ] | Checkpoint restores NPC instance state, not dict rebuild. |
| Separate descriptive/generated people | [ ] | Dummy story names do not become NPC classes. |
| Separate fight spawns from NPCs | [ ] | Animals/creatures/patrols belong to fight/hunt unless recurring characters. |
| Replace age with birth date | [ ] | Permanent identity uses birth date; age is derived. |
| Move global parameters into classes | [ ] | NPC class fields/methods own NPC parameters. |
| Convert known state to class method | [~] | Use `mark_known()`. |
| Convert visible panel to class display | [~] | Use `npc_display_name()`. |
| Convert HUD NPC presence to class location | [ ] | Use NPC `getLocation()`/visibility, not room NPC lists. |
| Audit NPC talk labels | [ ] | Talk label owns talk flow. |
| Audit social actions | [ ] | Shared social helpers only where real common logic exists. |

## Room Implementation Tasks

| Task | Status | Rule |
|---|---|---|
| Define room ownership rule | [x] | Room owns navigation/visibility/picture/description/schedule. |
| Define room template | [x] | Object model + entry label shape. |
| Remove old time-slot schedule form | [~] | Use explicit clock intervals. |
| Audit rooms for NPC mutations | [ ] | NPC state belongs to NPC. |
| Remove room-owned NPC lists as authority | [ ] | NPC presence comes from NPC class state. |
| Audit rooms for object actions | [ ] | Object actions belong to objects. |
| Audit rooms for event consequences | [ ] | Event labels own story consequences. |
| Remove room refresh/rebuild labels | [ ] | Direct entry/build only. |
| Verify navigation exits | [ ] | Exits are movement only. |
| Verify room pictures | [ ] | Room browsing picture vs event picture. |
| Audit explicit room actions | [ ] | Only clean/search/examine/explore when room itself is target. |

## Event/Thread Implementation Tasks

| Task | Status | Rule |
|---|---|---|
| Define event/thread ownership rule | [x] | Availability in event/thread, flow in label. |
| Define event template | [x] | Fixed tuple + direct label. |
| Define thread initialization procedure | [x] | Use `threadList`, `threadData`, `threads`, `initStoryEventRuntime()`. |
| Define trigger/check controls | [x] | Use `story_event_available()` for display and `checkTriggers()` for execution. |
| Define highlight/status projections | [x] | Highlight maps are derived from thread/event state only. |
| Audit tuple field order | [ ] | Exact order only. |
| Audit location/action keys | [ ] | Must match trigger call. |
| Audit condition authority | [ ] | Conditions call class/system methods, not legacy dicts. |
| Remove redundant condition wrappers | [ ] | Event tuple fields and `Event.canTrigger()` own availability checks. |
| Remove wrapper/handler labels | [ ] | Direct label owns story flow. |
| Audit event images | [ ] | Use `vscene` in event labels. |
| Audit event consequences | [ ] | Mutate correct owner directly. |
| Audit thread advance/complete | [ ] | Only at real outcome. |
| Verify thread save/load authority | [ ] | Checkpoint restores `ThreadInfo` state directly. |
| Verify screens display only | [ ] | No story authority in screens. |

## Player And Basic Action Implementation Tasks

| Task | Status | Rule |
|---|---|---|
| Define Player ownership rule | [x] | Player class instance owns player state. |
| Define basic action template | [x] | Direct label/method mutates state and returns directly. |
| Audit `Actions.rpy` mixed departments | [ ] | Separate basic player actions from NPC/shop/item/craft/fight/sex flow. |
| Keep primitive actions primitive | [ ] | Direct mutation in label when no calculation is needed. |
| Use Python only for real calculation | [ ] | Method belongs to the owner of the logic. |
| Add player action restrictions | [ ] | Energy, late time, fun, health, resource, and daily limits. |
| Move player globals into Player class | [ ] | Legacy globals are compatibility output only. |
| Move chore state to correct owners | [ ] | Player/Tavern/Room/Object own their parts. |
| Remove refresh/apply action wrappers | [ ] | No dispatcher around a direct action result. |
| Split NPC social actions out | [ ] | NPC/social system owns relationship flow. |
| Split purchasing/shop actions out | [ ] | Economy/shop system owns buy/sell flow. |
| Split inventory item actions out | [ ] | Item/inventory system owns item behavior. |
| Split crafting actions out | [ ] | Crafting/object system owns creation flow. |
| Split fight/hunt actions out | [ ] | Fight/hunt system owns combat flow. |
| Split sex actions out | [ ] | SexEngine owns sex state and acts. |
| Verify Player save/load authority | [ ] | Checkpoint restores Player instance state directly. |

## Forbidden Pattern Checks

Run these checks during implementation:

```powershell
rg -n "globals\(\)" game
rg -n "time_slots=\[" game
rg -n "RoomSchedule\(.*time_slots" game
rg -n "Refresh|Rebuild|Apply|Dispatcher|Handler" game
rg -n "CurrentLoc\[|knowsMC\[|Friends\[" game
```

Each match must be classified:

- KEEP: real class/object/system owner or temporary compatibility output.
- REMOVE/BYPASS: duplicate authority, bloat, workaround, stale bridge.

## Next Documents To Create

- `GAME_OBJECT_MODEL_AND_TEMPLATE.md`
- `CALENDAR_TIME_MODEL_AND_TEMPLATE.md`
- `TAVERN_MODEL_AND_TEMPLATE.md`
- `TAVERN_TEAM_MODEL_AND_TEMPLATE.md`
- `FIGHT_MODEL_AND_TEMPLATE.md`
- `SEX_ENGINE_MODEL_AND_TEMPLATE.md`
- `REPORTS_MODEL_AND_TEMPLATE.md`
- `SCREENS_MODEL_AND_TEMPLATE.md`
