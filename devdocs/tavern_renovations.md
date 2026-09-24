# Tavern renovations (2026-09-23)

## Scope and ownership

Seven improvements share one construction lifecycle. Tavern owns
`renovations: {code: TavernRenovation}`; Player, Draupnir and Melissa no longer
store parallel construction flags, quotes or deadlines. The immutable
`TAVERN_RENOVATIONS` catalog owns prices, materials, durations, requesters and
construction locations. Soap barrels and dog booths are outside this change.

| Project | Request source | Maravedies | Shed logs | Calendar days |
| --- | --- | ---: | ---: | ---: |
| Sign | MC asks Draupnir | 200 | 0 | 1 |
| Existing peephole, now in MC room | MC asks Draupnir after services unlock | 100 | 0 | **1** |
| Glory hole | Georgette explains it; MC asks Draupnir | 700 | 0 | 1 |
| Roof | Melissa bat story, after fumigation | 2000 | 0 | 2 |
| Yard/toilet | Melissa in tavern | 600 | 8 | 3 |
| Laundry/bathroom and utility room | Sandra in tavern | 900 | 12 | 4 |
| Guest room/lounge | Resident Clarissa | 700 | 8 | 3 |

The newer three projects keep their accepted balancing values. Earlier prices
and story prerequisites remain intact. Peephole construction is now explicitly
one day, ready next morning, without resetting the hour or charging again.

## Standard lifecycle

`unrequested -> requested -> accepted -> building -> completed`.
Postponement leaves the carpenter's order available without replaying the NPC
demand. Explicit refusal marks that item
`declined`, never aborting unrelated improvements.

Each saved renovation contains requester, request/start/due/completion days,
paid maravedies and consumed log quantity. Paid/used quantities are transaction
history, not a second wallet or inventory. Whole logs come from the existing
Shed inventory; split or carried firewood cannot replace them.

One existing unordered thread, `tavernRenovations`, contains seven independent
items. Events check the Tavern object's status. Thread `done[index]` records
the inspection/follow-up having been played (or explicit refusal), **not**
physical completion. `num` counts resolved items. Each native event label owns
its text, picture, menu and return; no new dispatch/refresh labels.

- Melissa (`backyard`), Sandra (`shed`) and Clarissa (`guest_room`) own boolean
  entries in `renovation_requests`, initially false. After the demand text is
  displayed the entry becomes true. This is an outstanding request, not a
  second construction/completion flag. It stays true while the work is pending
  or building, and clears on completion or explicit refusal.
- Their request booleans unlock Draupnir's options; no extra promise to the NPC
  is required after hearing the demand. The four older projects retain their
  existing acceptance prerequisites. No resource price or duration changes.
- The shared `DraupnirRenovationOrder` checks this unlock, workshop hours,
  builder availability, money and timber before charging exactly once.
- Draupnir accepts one new construction order at a time. His runtime
  `getLocation` reads the active job and places him at its construction site,
  not the workshop. Conversation is disabled while he is building.
- The existing next-day lifecycle calls `finish_due_renovations`. It changes
  each due job once, grants **+1 motivation (mana)** to every current tavern
  worker and **+2 additional motivation** to its NPC requester. Existing
  motivation limits apply. No corruption change.
- The morning report names completed work; a location-entry inspection event
  follows once and marks the thread item seen. New facilities/actions become
  usable at physical completion, without waiting for inspection.
- The washroom exit and entry guard read that same completion state; no saved
  room-hidden flag mirrors construction progress.
- Roof completion enables Melissa's breakfast invitation; it does **not**
  finish her bats thread or skip the argument, booklet search and thanks.
- Already-completed historical renovations never replay motivation rewards.

The single `tavern_empty_room_peephole` object belongs to `TavernMyRoom`.
The Hall's existing "go and check" shortcut remains direct and returns to Hall;
the bedroom object returns to the bedroom. Both use the same paid unlock and
existing guest observation procedures. There is no second peephole project.

## Flow classification

KEEP: actual room entries, NPC request/quote scenes, carpenter object menu,
shared order event, inspection event, bath/stove object actions.
REMOVE: three separate payment labels, duplicated workshop quote calculations,
Player construction flags, NPC quote/deadline fields and the three parallel
renovation request threads. The Hall's monthly Monday/day-1 reset of paid
peephole/glory-hole state is removed, not translated into a new reset.

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
The existing `backyard_renewal.png` provides the renovated yard view.
The guest lounge's current small-room image set is based on the existing
`images/amanda/gloryfirst/glory room.png`. The sofa stands opposite the stone
stove; a latched door beside it connects to the existing glory-hole cubicle.
The originals, earlier daylight companions and oversized sofa draft remain
on disk; no existing images were overwritten.

`tavern_empty_room_picture` selects `images/tavern/guest_room/`
`{sofa|lounge}_{day|night}_{lit|cold}.png` from actual sofa ownership, hour
(06:00-17:59 daylight) and the guest stove's shared fire timer. Entry,
inspection and the empty-room peephole use that same state. The peephole
adds a transparent foreground frame from the player-room side; occupied
events retain their scene pictures. Before renovation or sofa installation,
the previous room backgrounds remain available.

`SofaData` places the sofa in `TavernEmptyRoom`, with `sofa_day_cold.png` as
its card portrait; conversation uses current room lighting. Purchase price
and prerequisites are unchanged. The original gathering prerequisite still
uses the Hall as the meeting point before inviting the participants upstairs.
The sofa description and delivery text no longer place it in the Hall.

The two room definitions own their connecting exits. The new entrance is
available after glory-hole construction; the existing Hall entrance stays.
`TavernGuestRoomStoveObject` owns its independent saved fuel/fire/ash state
and native object menu, using the shared `MakeFire` and `Clean` procedures.
It does not share the Hall or kitchen fire state. See
[assets, exact prompts and verification](sofa_guest_room_art.md).

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

Version 100 moved the existing observation object. Version 101 transfers old
Player flags, Draupnir quotes, Melissa's roof deadline and Tavern's old date map
into renovation objects, then removes those retired fields and threads.
Version 102 adds the guest stove object to old room inventories and the new
connecting exits only when absent, preserving existing room items and fire state.
Version 103 seeds missing member-request booleans from the prior saved lifecycle
once (`requested`, `accepted` or `building` means pending). Already-present
booleans are not overwritten. There is no ongoing reverse synchronization.
Existing inventories, resources, room identities, story progress and paid dates
are not rebuilt. Previously paid overlapping jobs keep their deadlines; only
new orders obey the single-builder limit. An old sign/glory-hole job lacking a
timestamp retains the original next-day completion promise.

Saved RoomAction callbacks retain their callable names; their payment targets
are migrated to the shared order event. The saved runtime uses `default tavern`,
not mutable state in a `define`. This follows Ren'Py's
[save/rollback contract](https://www.renpy.org/doc/html/save_load_rollback.html).
Use the established morning-after-report checkpoint when changing script flow;
this is not a guarantee that arbitrary old mid-scene return addresses survive.

## Verification

- NPC request-flag follow-up (version 103): 167 focused tests passed; the
  combined resident/renovation native suite passed 40 cases / 276 assertions
  plus the separate full old-save load check. Details and the unchanged stale
  version-number assertion are recorded in [resident verification](clara_resident_routine.md#results-2026-09-23).
- Focused runtime checks: all seven exact costs/durations, no double charges,
  one builder, exact-once team/requester rewards, preservation of paid state
  and resources, rejection/refusal, and residual-authority scan.
- Native Ren'Py 8.5.2 tests click request/order/inspection menus, test next-day
  completion and Draupnir's actual location, preserve roof-story continuation,
  bath navigation and both existing Hall/bedroom observation routes.
- Melissa's kitchen event suite remains a separate regression check.
- Original renovation baseline checks: 103 focused Python tests; 22 native renovation cases with
  165 assertions; 22 native Melissa kitchen cases with 125 assertions.
  A separate native save/load run uses an actual Ren'Py statement checkpoint
  and verifies version-100 state conversion, resources and motivation via
  seven post-load assertions. It exits after the verification marker, rather
  than depending on the test runner resuming across a loaded call stack.
  Ren'Py 8.5.2 compile/lint pass (only generated test-code reachability notes).
- Guest-room follow-up: 199 focused Python checks, 33 native cases / 207
  assertions, and a separate successful full save/load check covering the
  stove registry identity, saved fire/fuel/ash, sofa placement and old room
  item migration. Ren'Py 8.5.2 compile/lint passed; the only lint notes are
  unreachable generated test statements. See the asset document for logs.
- Source-based tests that demand saveVersion 92 or an obsolete unrelated
  girl-decision expression already fail on the pre-change baseline; they
  are not treated as gameplay failures or repaired in this change.
