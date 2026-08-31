# Melissa Bats Quest Stage Logic

This document reflects the current live code path for Melissa's bats quest.

Core rule:
- `melissaBatProblem` thread state is the sole progression source of truth.
- Live gates read `threads["melissaBatProblem"].num` or `completed`; there is no second bats-stage field.

Timing fields:
- `Melissa.storage_rat_help_day`
- `Melissa.bat_attic_check_day`
- `Melissa.roof_repair_complete_day`

Side state:
- `Melissa.temp_room_code`

The old `bats_episode`, `ratKilled`, `AskedMCToSolveRoomProblem`, `bats_completed`, `room_returned`, `sex_engine_unlocked`, and `drawings_ready_day` fields are retired. Save migration promotes the old bat phase into `melissaBatProblem` once and removes the mirrors.

## Real Trigger Sequence

### Shared Trigger
The whole branch starts from the basement rat scene:
- `TavernStorageRatEvent`
- menu:
  - kill the rat
  - leave it

If the player kills the rat:
- Melissa gets the storage-help update
- the werecat branch is also activated
- the rat carcass is cached for bait use later

This is the single shared start point for both threads.

### Next Morning 1: Werecat Breakfast
The next morning after the basement rat kill:
- the breakfast dialogue about the rat problem runs first
- this is the Amanda “good pussy cat” breakfast joke/gesture scene
- this activates the werecat thread as the next real pursuit

### Next Morning 2: Bats Breakfast
The bats breakfast does **not** fire the very next morning.

It waits until:
- `dayspassed >= storage_rat_last_help_day + 2`

Then the bats breakfast can fire:
- Melissa is missing from table
- Amanda comments about “mice with wings”
- Sandra mentions talking to Gerhard

### Next Night: Upstairs Noise Trigger
After the bats breakfast, the next real bats event is not a direct room popup.

It starts from upstairs at night:
- location: `TavernUpstairs`
- time: night slot
- action menu shows the Melissa noise check

That scene is:
- Melissa awake in bed
- she complains about the problem
- she explicitly asks for help

From there:
- you can promise to help
- you can comfort her for an extra friendship point
- you can inspect the ceiling / holes
- you can say good night

This is the real stage-2 room episode.

## Stage Table

| Stage | Meaning | Entry Condition | Next Advancement |
|---|---|---|---|
| `0` | Not started | No bats progression yet. Basement rat may or may not be unresolved. | Kill the rat in `TavernStorageRatChoice`. This does not itself advance bats to breakfast yet, but it sets the shared trigger day. |
| `1` | Bats breakfast happened | `MelissaBatBreakfastScene` fires after the two-day delta from basement rat help. | At night in `TavernUpstairs`, use `Проверить шум в комнате Мелиссы`, then promise help in `MelissaNightNoiseChoice("promise")`. |
| `2` | Melissa asked for help / promise made | Night noise scene accepted, help promised, attic day marker stored. | Inspect Melissa's ceiling in the same night sequence or later room search path. `MelissaNightNoiseInspect` advances to stage `3`. |
| `3` | Room episode complete | Ceiling holes discovered; this includes the room-side discovery and goodnight outcome. Temporary lodging may be chosen. | On or after `bat_attic_check_day`, go to the attic and run `MelissaAtticColonySearch`. |
| `4` | Attic colony found | The colony is confirmed on the attic search. | Use `MelissaAtticWindowPeek`. |
| `5` | Window peek done | The voyeur window step is done. | Use `MelissaAtticFallScene`. |
| `6` | Fall scandal | Melissa catches the player after the fall and moves to Amanda's room. | Smoke out the colony once repellent is available. |
| `7` | Colony smoked out / roof repair | Order the repair for `2000`; `roof_repair_complete_day` is set two days ahead. | After the threshold, speak to Melissa in the Tavern Hall and ask her to attend tomorrow's common breakfast. |
| `8` | Breakfast invitation accepted | The thread's own day marker records the invitation day. | On the following morning, enter the kitchen before breakfast is consumed. |
| `9` | Booklet argument heard | Melissa and Amanda argue about the missing booklet at breakfast. | Enter Amanda's room and catch Melissa searching under the bed. |
| `10` | Lost-booklet aftermath | Melissa has searched Amanda's room and concluded that the booklet may be in her own room. | Search Melissa's room; a successful exploration check reveals the booklet. |
| `11` | Booklet found | The physical booklet is visible in Melissa's room and the Clara paintings continuation can resolve its origin. | After the drawings conversation is resolved, open Melissa's NPC conversation; she thanks the player before the normal choices appear. |
| `12` | Completed | Melissa's thanks closes the room problem and the existing courtship action becomes available from the same conversation. | Final stage. |

## Detailed Advancement Rules

### Stage `0 -> 1`
Requirements:
- basement rat was killed
- `storage_rat_last_help_day >= 0`
- breakfast is being heard
- `dayspassed >= storage_rat_last_help_day + 2`

Advance by:
- `MelissaBatBreakfastScene`

### Stage `1 -> 2`
Requirements:
- current location is `TavernUpstairs`
- night time
- stage is exactly `1`

Advance by:
- select `Проверить шум в комнате Мелиссы`
- in the scene, choose to handle the problem

### Stage `2 -> 3`
Requirements:
- help was promised

Advance by:
- inspect the ceiling / holes in Melissa's room
- this is the room investigation step

### Stage `3 -> 4`
Requirements:
- `dayspassed >= bat_attic_check_day`

Advance by:
- attic colony search

### Stage `4 -> 5`
Advance by:
- attic window peek

### Stage `5 -> 6`
Advance by:
- fall scene

### Stage `6 -> 7`
Advance by:
- smoke out the colony with repellent

### Stage `7 -> 8`
Requirements:
- pay `2000` to order the roof repair
- `dayspassed >= roof_repair_complete_day`

Advance by:
- speak to Melissa from the Tavern Hall NPC list
- choose `Попросить Мелиссу прийти завтра на общий завтрак`

### Stage `8 -> 9`
Requirements:
- at least one day has passed since the invitation
- breakfast has not already been consumed
- enter the kitchen during the morning

Advance by:
- play the paragraph-by-paragraph Melissa/Amanda booklet argument
- finish that breakfast

### Stage `9 -> 10`
Advance by:
- enter Amanda's room and play the three-picture under-bed search scene

Existing saves from the former order may already have `drawings_found`. They still play the required three-picture scene, then advance directly to stage `11` so the same physical booklet is not discovered or created twice.

### Stage `10 -> 11`
Requirements:
- search Melissa's room
- effective exploration is above `120`

Advance by:
- discover the booklet under Melissa's bed

### Stage `11 -> 12`
Requirements:
- resolve the first Clara paintings conversation so `drawings_returned` is true

Advance by:
- open Melissa's NPC conversation in the Tavern Hall
- Melissa's completion thanks plays automatically
- the existing courtship option is then available in the same conversation

## Recipe Book Note

The attic recipe book now explicitly hints that:
- there are more recipes in the book
- the hidden note can be noticed only after the bats thread has started
- the player cannot fully read it yet if exploration is still too low

That means the book now supports the intended progression hint:
- there is more in the book than the player can currently decipher
- the hidden bat-repellent path does not appear before Melissa's bat problem is a live story issue

Current gate:
- `Melissa.bats_stage() >= 1`
- effective exploration is at least `120`
- the note has not already been found

## Smooth Gameplay Goal

For this quest to play smoothly, the intended visible order is:

1. Basement rat scene
2. Next-morning werecat breakfast
3. Later bats breakfast after the day delta
4. Night upstairs noise check
5. Promise help
6. Inspect ceiling / holes
7. Good night
8. Next-morning attic search
9. Bat colony picture
10. Window peek
11. Fall scene
12. Smoke out colony
13. Pay `2000` and wait two days for the roof repair
14. Ask Melissa in the Tavern Hall to attend tomorrow's common breakfast
15. Hear the Melissa/Amanda booklet argument at the next morning's breakfast
16. Catch Melissa searching under Amanda's bed
17. Search Melissa's room and discover the booklet
18. Resolve the drawings continuation
19. Open Melissa's NPC conversation, receive her thanks, and continue into the existing courtship flow

That is the sequence the live code is now aiming to preserve.
