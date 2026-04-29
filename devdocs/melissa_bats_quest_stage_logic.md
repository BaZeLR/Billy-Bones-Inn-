# Melissa Bats Quest Stage Logic

This document reflects the current live code path for Melissa's bats quest.

Core rule:
- `MelissaVar["bats_episode"]` is the progression source of truth.

Timing fields:
- `MelissaVar["storage_rat_last_help_day"]`
- `MelissaVar["bat_attic_check_day"]`
- `MelissaVar["drawings_ready_day"]`
- `MelissaVar["roof_repair_order_day"]`
- `MelissaVar["roof_repair_complete_day"]`

Side state:
- `MelissaVar["temp_room"]`

The older boolean fields still exist in save/state, but they are compatibility mirrors. They are not supposed to define the live quest order.

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
| `6` | Fall scandal / aftermath | Melissa catches the player after the fall, moves to Amanda's room, and the drawings side branch can start later. | Use `MelissaBurnAtticColony` once repellent is available. |
| `7` | Colony smoked out / roof repair path | Bats are smoked out, roof repair may be ordered and then completed by day threshold. | Wait for roof completion, then take `MelissaBatsCompletionScene`. |
| `8` | Completed | Melissa gets the explicit completion talk and the room problem is closed. | Final stage. |

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
- roof repair ordered
- `dayspassed >= roof_repair_complete_day`
- completion talk still not taken

Advance by:
- Melissa completion follow-up scene

## Recipe Book Note

The attic recipe book now explicitly hints that:
- there are more recipes in the book
- the hidden note can be noticed only after the bats thread has started
- the player cannot fully read it yet if exploration is still too low

That means the book now supports the intended progression hint:
- there is more in the book than the player can currently decipher
- the hidden bat-repellent path does not appear before Melissa's bat problem is a live story issue

Current gate:
- `MelissaVar["bats_episode"] >= 1`
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
12. Drawings aftermath
13. Smoke out colony
14. Repair roof
15. Melissa completion talk

That is the sequence the live code is now aiming to preserve.
