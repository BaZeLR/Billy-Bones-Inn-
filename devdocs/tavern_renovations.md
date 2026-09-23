# Tavern renovations (new content, 2026-09-22)

These are new game features, not recovered QSP renovations. Existing sign,
glory-hole, soap-barrel and dog-booth jobs are unchanged. The existing paid
guest-room observation window is relocated to MC's room, without a second fee.

## Current scope: quest-driven construction (2026-09-23)

The earlier hidden preparation is now connected to native NPC request events.
Sandra offers the bathroom/laundry, Melissa the yard/toilet, and resident
Clarissa the guest room/lounge. Their existing talk menus expose the request;
Melissa's kitchen needs conversation can also lead into the same request after
the kitchen event ends. No parallel kitchen quest or extra progression flag.

Each uses the existing three-step `LThreadData`/`LThreadInfo` lifecycle:

| Stage | State / action |
| --- | --- |
| 0 | Request available with the giver present in the tavern; Clarissa must reside there. |
| 1 | Accept calls `enable()` and `advance()`; only that order appears at Draupnir. |
| 2 | Successful payment advances once; construction is ongoing until its saved due day. |
| 3 | On entry to the renovated location, inspection calls `complete()`. |

Postponement does not advance and permits a later request. Explicit refusal
calls `abort()` and prevents the order. Insufficient resources and closing a
quote leave stage 1 intact, including retrying the quote on the same day.
`ShedWashroom` stays hidden until the completion event opens its door.

## Ownership and flow

- `tavern: TavernInfo` owns `renovation_due_days`, one absolute completion date
  per paid project. Do not mirror these dates or completion booleans on Player,
  rooms, Draupnir or quest givers.
- `TAVERN_RENOVATIONS` is the only price/material/duration catalog.
- Quest state lives only in `sandraTavernRenovation`,
  `melissaTavernRenovation`, and `claraTavernRenovation`. These appear under
  their NPCs in the existing story board. Catalog visibility reads their state;
  no mutable `is_hidden` flag remains on the constant catalog.
- Draupnir's order event quotes and charges. The player
  pays maravedies; the existing
  shed inventory supplies building logs (`lumber_001`). Split firewood is not
  construction timber. No second inventory is created.
- Completion is derived from the saved date and actual calendar day. The
  morning report announces completed work, including during multi-day sleep.
  The completion event, not the report or room-entry procedure, completes the quest.
- There is no automatic new relationship reward or schedule change.

## Initial balancing values

These values were proposed for the new content; they are not QSP prices.

| Project | Quest giver | Maravedies | Logs | Calendar days |
| --- | --- | ---: | ---: | ---: |
| Yard and toilet | Melissa | 600 | 8 | 3 |
| Shed laundry/bathroom + utility room | Sandra | 900 | 12 | 4 |
| Guest room/lounge | Clarissa | 700 | 8 | 3 |

The single `tavern_empty_room_peephole` object now belongs to `TavernMyRoom`,
not `TavernEmptyRoom`. It retains the existing `client_room_hole` paid-unlock
state and guest observation routines. The hall's existing "go and check" shortcut
still opens the observation event directly and returns to the hall afterward;
its narration uses the window in MC's room. No extra object-menu click is needed.
The redundant `player_peephole` order, object and procedure were removed.

## Physical rooms and art

Before renovation, the old shed contains a chamber with a large cold,
half-ruined oven. Its cavity is large enough for an adult to hide in.

After renovation there are **two enclosed rooms**, not one open combined room:

- `Shed`: masonry stove with a copper hot-water tank; separate whole-log and
  split-firewood storage. Existing inventory and wood chores stay here.
- `ShedWashroom`: separate laundry/bathing room reached through a door;
  wash trough, bathing tub, linens and a privacy curtain. Bathing uses the
  existing player appearance/washing method and takes 15 minutes.

New day/night image pairs are under `game/images/tavern/backyard/shed/`:

- `ruined_stove_chamber.png`, `ruined_stove_chamber_night.png`
- `renovated.png`, `renovated_night.png` (utility room)
- `washroom.png`, `washroom_night.png` (separate wet room)

Original images are retained. The combined first preview is not used in-game.
The existing `backyard_renewal.png` and `images/amanda/Room/emptyroom.jpg`
provide the renovated yard and furnished guest-room views.

### Image prompt set (built-in image generation)

Reference for the old chamber: existing `shed.png`. Wide painted historical
game interior in the same rough-stone/aged-timber style, a cramped back chamber
with a large half-ruined cold oven and a dark empty arched cavity large enough
for a crouching adult. Loose bricks, dust and a bucket. No people, text,
watermarks or modern appliances. Its night variant changes lighting only:
cool moonlight, cold unlit oven, identical geometry and objects.

Utility-room revision: preserve the approved masonry stove, copper water tank
and tap, small firebox, textures and beams. Replace the bathing area with a
full-height partition and closed door to the separate washroom, plus full-log
storage. Keep split wood in separate racks; no bath or laundry in this room.
One coherent wide interior, not split panels. Night variant: same layout,
moonlight outside and amber light from the existing firebox.

Washroom: new viewpoint inside the separate enclosed wet room, matching the
timber/stone style. Wooden bath, separate washing trough, washboard, linen,
privacy curtain, buckets and a floor drain. Closed door to the utility room;
no stove, boiler or firewood here. Night variant preserves all objects and
geometry with moonlight and soft off-frame candlelight. All images landscape
16:9, no people, captions, watermarks or modern appliances.

## Save handling

Version 94 adds only missing permanent object IDs and the new room exit to old
saves. The new `default tavern` supplies the new owner's initial state.
Never replace an existing room or repopulate consumable inventory. Existing
logs, fuel, items, relationships, quests and construction purchases remain.
Version 100 moves the old window ID and removes its duplicate without replacing
either room. Already paid renovations resume at their inspection stage, not at
a new request/payment. Existing advanced or aborted threads are not reset.
This follows Ren'Py's saved/default-state and native-menu contracts:
[save/rollback](https://www.renpy.org/doc/html/save_load_rollback.html),
[menus](https://www.renpy.org/doc/html/menus.html).

## Verification

- Focused runtime tests cover exact costs, construction dates, rejected and
  duplicate payments, accepted/aborted states, and preserved inventory.
- Native Ren'Py 8.5.2 tests click all three NPC request menus and Draupnir's
  orders through completion, refusal/postponement and same-day payment retry.
  They check the moved window, both existing client scenes, migration
  idempotence, room opening, bathing and return contexts: 14 cases / 79 assertions.
  Both the unchanged Hall shortcut and the bedroom object are exercised.
- Melissa's kitchen suite passes 22 cases / 124 assertions, including the
  handoff from her finished needs conversation into the renovation request.
  Its click helper waits for the next menu's items, not the outgoing screen.
- The focused Python suite passes 110 tests. A broader source check has three
  pre-existing failures expecting save version 92 (HEAD before this work was
  already 98); this is not a claim that the whole project's suite is green.
- Ren'Py compile and lint pass in a copied project using isolated test saves.
  Tests do not modify the user's saves.
