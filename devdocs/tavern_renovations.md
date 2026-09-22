# Tavern renovations (new content, 2026-09-22)

These are new game features, not recovered QSP renovations. Existing sign,
client-service peephole, glory-hole, soap-barrel and dog-booth jobs are unchanged.

## Current scope: defined, hidden, not activated

The user requested complete room descriptions, illustrations, objects and
navigation menus, but no NPC request conversations yet. `ShedWashroom` is
defined with the existing `Room.is_hidden=True` mode. Its entrance and direct
entry are blocked while hidden. Existing accessible rooms are not hidden.

Draupnir's four order definitions also have `is_hidden=True`. Both his menu
entry and individual order options are hidden; the transaction rejects a
hidden order. No gameplay action currently activates these additions.
The native test fixture can temporarily enable them in a separate test project.

## Ownership and flow

- `tavern: TavernInfo` owns `renovation_due_days`, one absolute completion date
  per paid project. Do not mirror these dates or completion booleans on Player,
  rooms, Draupnir or quest givers.
- `TAVERN_RENOVATIONS` is the only price/material/duration catalog.
- Future quest givers are catalog metadata only: Sandra for bathroom/laundry,
  Melissa for yard/toilet, Clarissa for guest room/lounge. No request or
  completion story threads or conversations are installed in this update.
- Draupnir's hidden order procedure is prepared to quote and charge. The player
  pays maravedies; the existing
  shed inventory supplies building logs (`lumber_001`). Split firewood is not
  construction timber. No second inventory is created.
- Completion is derived from the saved date and actual calendar day. The
  morning report announces completed work, including during multi-day sleep.
  Story activation and request-thread progression are deferred.
- There is no automatic new relationship reward or schedule change.

## Initial balancing values

These values were proposed for the new content; they are not QSP prices.

| Project | Future quest giver / dependency | Maravedies | Logs | Calendar days |
| --- | --- | ---: | ---: | ---: |
| Yard and toilet | Melissa | 600 | 8 | 3 |
| Shed laundry/bathroom + utility room | Sandra | 900 | 12 | 4 |
| Guest room/lounge | Clarissa | 700 | 8 | 3 |
| Player-room peephole into guest room | Guest renovation finished | 100 | 1 | 1 |

The room opening is distinct from the existing purchased client-service
peephole. Existing story unlocks are not reset or silently replaced.

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
This follows Ren'Py's saved/default-state and native-menu contracts:
[save/rollback](https://www.renpy.org/doc/html/save_load_rollback.html),
[menus](https://www.renpy.org/doc/html/menus.html).

## Verification of the hidden definitions

- 69 focused tests cover the item, renovation owner and navigation projections.
- 12 native Ren'Py 8.5.2 cases cover hidden menu/room defaults, rejected hidden
  orders, prepared transactions, save-state preservation, day/night room
  previews, washing time, both navigation directions and object-menu returns.
- Ren'Py compile and lint pass in a copied project using isolated test saves.
  Tests do not activate renovations or modify the user's saves.
