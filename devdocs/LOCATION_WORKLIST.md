# Location Worklist

Purpose: single tracking sheet for world/location labels (`CurLoc`-style navigation), excluding utility/function labels.

Related generated references:
- `game/LOCATION_ARGS_MAP.md` (human-readable args mapping for every location)
- `game/location_args_map.json` (programmatic args mapping for tooling)

## Canonical Location Labels

| Status | Label (Code Name) | File | CurLoc Value | Display Name | Description/Conditions | Active/Inactive Rules | Characters Present | Interactable Objects | Navigation Exits | Image Path(s) |
|---|---|---|---|---|---|---|---|---|---|---|
| [ ] | `TavernMain` | `game/Inn/TavernMain.rpy` | `TavernMain` | Main tavern hall | Core tavern hub; closure text depends on day/time. | Closed on Sunday service, Friday dance time, late night; events may override. | `sandra`, `melissa`, `amanda`; `georgett`/`liza` when `CurrentLoc[...] == CurLoc`; Draupnir while construction flags are active. | Family talks; prostitution corner checks; gloryhole status checks; help book access. | `StreetTavern`, `TavernHelp`, `TavernMyRoom`, `TavernAmandaRoom` (conditional), `TavernStable`, `TavernProstClients` (conditional). | `bg TavernMain`; `TavernShowImage` dynamic. |
| [ ] | `TavernMyRoom` | `game/Inn/TavernMyRoom.rpy` | `TavernMyRoom` | My room | Private room with dress chest flow. | Always available from tavern hall. | Player only. | Dress equip/inspect menu from `MyDresses`. | `TavernMain`. | `bg myroom`. |
| [ ] | `TavernAmandaRoom` | `game/Inn/TavernAmandaRoom.rpy` | `TavernAmandaRoom` | Amanda's room | Amanda room; empty by day, sleeping scenes at night. | Night-only character interactions (`time >= 4`). | `amanda` at night; none by day. | Wake/approach Amanda interaction chain; night dress logic. | `TavernMain`. | `bg amanda_room`; multiple `ShowImage` calls. |
| [ ] | `TavernStable` | `game/Inn/TavernStable.rpy` | `TavernStable` | Stable | Tavern stable and horse/travel staging area. | Travel options gated by `BeckyVar`, `MyStallion`, `week`, `time`. | Player; horse if `MyStallion != ""`; thief event presence is implied. | Horse status checks; Sherwood travel trigger options. | `TavernMain`, `SherwoodTravel` (conditional). | `bg stable`; `stablehorse`/`stableempty`. |
| [ ] | `TavernGloryHole` | `game/Inn/TavernGloryHole.rpy` | `TavernGloryHole` | Gloryhole corner | Specialized tavern sub-location with multi-step scene flow. | Works only on configured time windows and assigned worker conditions. | Assigned `jobgloryhole` girl (or none); random clients; `amanda` special scene path. | Watch client; watch girl; insert/cum actions; reaction branches. | `TavernMain`. | `ShowImage/ShowImageSeq` under `gloryhole/*` and girl sets. |
| [ ] | `TavernHelp` | `game/Inn/TavernHelp.rpy` | `TavernHelp` | Help book | Tutorial/help text location. | Always available from tavern hall. | Player only. | Read help text; optional cheat-money action (conditional). | `TavernMain`. | `bg book`. |
| [ ] | `StreetTavern` | `game/Inn/StreetTavern.rpy` | `StreetTavern` | Street by tavern | Exterior street hub around tavern entrance. | Always available as central outdoor node. | Street crowd implied; Draupnir's donkey when `TavernGloryHole == 1`. | Enter tavern; travel to city districts. | `TavernMain`, `MarketPlace`, `PortStreets`, `Church`, `ArtisansQuarter`. | `bg StreetTavern`; `LocStreetTavern*`. |
| [ ] | `MarketPlace` | `game/Inn/MarketPlace.rpy` | `MarketPlace` | Market square | Main market hub with Friday dance trigger and Mongol random scene. | Closed Sunday/late; auto-redirect to Friday dance on Friday evening. | Crowd; Mongol random encounter; nearby guard office access. | Enter grocery/wine/guard; Mongol interaction branch. | `GroceryStore`, `WineStore`, `CityGuard`, `StreetTavern`, `FridayDance` (auto jump condition). | `LocMarketPlace*`; Mongol portraits. |
| [ ] | `GroceryStore` | `game/Inn/GroceryStore.rpy` | `GroceryStore` | Blankenship grocery | Provision shop for tavern supplies. | Closed Sunday/late. | `eddie` in morning; `becky` later day periods. | Buy product sacks; talk interactions with current clerk. | `MarketPlace`. | Character portraits (`eddie`, `becky`) plus text scenes. |
| [ ] | `WineStore` | `game/Inn/WineStore.rpy` | `WineStore` | Legare wine cellar | Wine supplier shop. | Closed Sunday/late. | `clarissa` in morning; `alber` later day periods. | Buy wine barrels; Clarissa talk/flirt; Alber talk. | `MarketPlace`. | `clara`/`alber` portraits and cellar narration. |
| [ ] | `Church` | `game/Inn/Church.rpy` | `Church` | Ilmater church | Sunday service location; later confession/after-sermon flows. | Closed outside Sunday morning/day windows. | Gerhard; congregation; Sandra/Melissa/Amanda; Legare family; Becky family; Georgett/Liza conditional. | Service observation menu; confession entry; after-sermon exploration. | `StreetTavern`, `ChurchIspoved`, `ChurchAfterCermon`. | `LocChurch*`, `gerhard`, family/church portraits. |
| [ ] | `ChurchAfterCermon` | `game/Inn/ChurchAfterCermon.rpy` | `ChurchAfterCermon` | Church after service | Post-service exploration behind confession booths. | Requires `args[0] == 1` or returns to church. | Georgett/Liza/Becky/Gerhard event actors depending conditions. | Keyhole voyeur events (`AfterCermon*`). | `Church`. | Uses called event visuals; no fixed scene bg here. |
| [ ] | `ChurchIspoved` | `game/Inn/ChurchIspoved.rpy` | `ChurchIspoved` | Confession booth | Confession mini-scene with branching topics. | Requires `args[0] == 1` or returns to church. | Gerhard (priest) and player. | Confession topic menu; state flags unlock further topics. | `Church`. | `ShowImage('gerhard', '', 'gerhardispoved')`. |
| [ ] | `EllonaTemple` | `game/Inn/EllonaTemple.rpy` | `EllonaTemple` | Ellona temple | Temple in port district with priestess interactions. | Birth room can be locked depending on `FranBusy[time]`. | `francheska`; laboring woman implied when birth room occupied. | Temple interaction menu via `EllonaTempleMenu`; priestess talk. | `PortStreets`. | `ellona fran_seq*` plus temple narration. |
| [ ] | `PortStreets` | `game/Inn/PortStreets.rpy` | `PortStreets` | Port streets | Alley network toward port and Ellona temple. | Scene branches by `CurrentLoc`, `time`, prostitution flags. | `georgett`, `liza`, rotating clients (conditional). | First-talk/event chains; alley client checks; character talks. | `EllonaTemple`, `StreetTavern`, `StreetClients_*` expression jumps (conditional). | Georgett port images; location text. |
| [ ] | `ArtisansQuarter` | `game/Inn/ArtisansQuarter.rpy` | `ArtisansQuarter` | Artisans quarter | Craft district hub for workshop and dress shop. | Always available from street hub. | Street crowd implied; no fixed named NPC in hub label. | Entry points to Draupnir workshop and Irma shop. | `StolyarWorkshop`, `DressShop`, `StreetTavern`. | `bg ArtisansQuarter`; `LocArtisansQuarter*`. |
| [ ] | `StolyarWorkshop` | `game/Inn/StolyarWorkshop.rpy` | `StolyarWorkshop` | Draupnir workshop | Carpenter workshop with purchase/upgrade options. | Closed Sunday/late or while Draupnir works your active order. | `draupnir` when open and available. | Discuss/commission sign repair, peep hole, gloryhole, and inspection/talk actions. | `ArtisansQuarter`. | `bg StolyarWorkshop`. |
| [ ] | `DressShop` | `game/Inn/DressShop.rpy` | `DressShop` | Irma dress shop | Tailor location for clothing orders. | Closed Sunday/late. | `irma`. | Inspect Irma; inquire order status; dress order list generation. | `ArtisansQuarter`. | Irma portraits and dress-related image calls. |
| [ ] | `SherwoodTravel` | `game/Inn/SherwoodTravel.rpy` | `SherwoodTravel` | Sherwood road | Travel/ambush sequence toward Kunidell. | Entry depends on stable branch; robbery logic controls outcomes. | Robin and robber group. | Continue/retreat negotiation and robbery outcome branches. | `TavernMain` (home path), in-label loops otherwise. | Robin portraits and travel scenes. |
| [ ] | `becky_home_front` | `game/Inn/BeckyHomeFront.rpy` | `becky_home_front` | Becky house front | Exterior of Becky home with optional voyeur scenes. | Encounter branches depend on `ArriveMode`, random roll, and prior checks. | Becky (from dance arrival route), `inga` + `lucas` random encounter. | Peek/share/ignore/watch/approach scene menus; enter house. | `becky_home`, `street_tavern`, self-loop menu jumps. | Becky house and Inga scene images. |
| [ ] | `becky_home` | `game/Inn/BeckyHome.rpy` | `becky_home` | Becky home interior | Dinner/guest/sex branches based on arrival mode and relationship flags. | Heavy branch gating by `arrive_mode`, dress checks, visit progress. | Becky, Eddie, Inga, Lucas (by route/state). | Guest dinner flow; multiple intimacy/event chains. | `street_tavern` (branch exits), caller return paths. | Becky dinner/room image sequences. |
| [ ] | `city_guard` | `game/Inn/CityGuard.rpy` | `city_guard` | City guard office | Complaint/recruit office on market square. | Scheduled location: open only Tue day and Fri morning; otherwise closed message. | Zimmermann when open. | View propaganda posters; talk to Zimmermann. | `market_place`. | `cityguard` and Zimmer images. |

## Event Labels Bound To Locations

These labels are events with their own functionality, but they belong to a parent location flow.

| Status | Event Label | Parent Location | File | Trigger / Schedule | Notes |
|---|---|---|---|---|---|
| [ ] | `friday_dance` | `MarketPlace` | `game/Inn/FridayDance.rpy` | Friday evening (`week == 5`, `time == 3`) | Keep own label and logic; treat as MarketPlace event, not standalone world-map location. |

## Exit Pairs (Current)

Confirmed base navigation pairs to preserve while refactoring:

| Status | A | B |
|---|---|---|
| [ ] | `MarketPlace` | `GroceryStore` |
| [ ] | `MarketPlace` | `WineStore` |
| [ ] | `StreetTavern` | `MarketPlace` |
| [ ] | `StreetTavern` | `PortStreets` |
| [ ] | `StreetTavern` | `Church` |
| [ ] | `StreetTavern` | `ArtisansQuarter` |

## Inner Rooms / SubLocations

Locations may include internal room labels. Example set for tavern:

- `TavernMain` -> `TavernMyRoom`
- `TavernMain` -> `TavernAmandaRoom`
- `TavernMain` -> `TavernStable`
- `TavernMain` -> `TavernHelp`
- `TavernMain` -> `TavernGloryHole` (feature/event sub-location path)

## Navigation Label Mismatches / Missing Targets

These are location-related labels referenced by jumps/calls but currently mismatched or missing. Keep as migration tasks.

| Status | Reference | Current State | Expected Action |
|---|---|---|---|
| [ ] | `jump CityGuard` | location label is `city_guard` | add alias or rename caller/callee consistently |
| [ ] | `jump FridayDance` | location label is `friday_dance` | add alias or rename caller/callee consistently |
| [ ] | `jump street_tavern` | location label is `StreetTavern` | add alias or rename caller/callee consistently |
| [ ] | `jump market_place` | location label is `MarketPlace` | add alias or rename caller/callee consistently |
| [ ] | `jump city_guard_menu` | no label found | add target label or adjust flow |
| [ ] | `jump TavernProstClients` | no label found | add target label or replace with current prostitution location flow |

## Definition Checklist Per Location

For each location above, fill these fields in code/data:

1. `name` (player-facing display name)
2. `code_name` (label / CurLoc value)
3. `description` with conditional branches
4. `active` / `inactive` logic and access conditions
5. `presence` rules (`CurrentLoc`, time/day conditions, etc.)
6. `interactable_objects` (menus, props, and inspect/action points)
7. `navigation` edges (where player can go next)
8. `image_path` and fallback behavior if missing
## Ren'Py Port Plan: TXT→RPY Mapping, World Navigation, and Time-Linked Turns

### Summary
1. Existing starter document is here: [LOCATION_WORKLIST.md](C:/Users/blank/Documents/RenPy_Projects/Tractir/devdocs/LOCATION_WORKLIST.md).  
2. Startup flow is confirmed: [script.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/script.rpy#L510) → [Intro.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Intro.rpy#L1) → [Intro.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Intro.rpy#L206) / [Intro.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Intro.rpy#L207) → [Intro.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Intro.rpy#L210).  
3. Source inventory found: `224` TXT `Location:` entries, with `56` missing same-name `.rpy` files and `53` existing `.rpy` files missing same-name label (many are utility/table/menu items, not world rooms).  
4. World-location starter scope is `23` rooms/locations with active navigation graph.

### Starter Room Inventory (world map scope)
1. `TavernMain`
2. `TavernMyRoom`
3. `TavernAmandaRoom`
4. `TavernStable`
5. `TavernGloryHole`
6. `TavernHelp`
7. `StreetTavern`
8. `MarketPlace`
9. `GroceryStore`
10. `WineStore`
11. `Church`
12. `ChurchAfterCermon`
13. `ChurchIspoved`
14. `EllonaTemple`
15. `PortStreets`
16. `ArtisansQuarter`
17. `StolyarWorkshop`
18. `DressShop`
19. `SherwoodTravel`
20. `BeckyHomeFront`
21. `BeckyHome`
22. `CityGuard` / `city_guard`
23. `FridayDance` / `friday_dance`

### Navigation Components To Implement (no mechanics changes)
1. Single canonical room graph source: extend/use [RoomClassSystem.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/RoomClassSystem.rpy#L454) as authoritative runtime navigation registry.
2. Keep alias compatibility layer in [RuntimeCompat.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/RuntimeCompat.rpy#L82) to preserve legacy links (`street_tavern`, `market_place`, `CityGuard`, `FridayDance`, etc.).
3. Ensure every world label sets location state via [loc.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/loc.rpy#L6) so HUD/navigation and event logic always see correct `CurLoc`.
4. Use extracted TXT descriptions as source text for room descriptions (no text rewriting), with existing parser behavior from [RoomClassSystem.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/RoomClassSystem.rpy#L76).
5. Keep current HUD-driven navigation in [status.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/status.rpy#L253) and time menu in [onobjsel.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/onobjsel.rpy#L129), but bind all targets to canonical graph nodes.

### Turn→Time Advancement Policy (parity with source mechanics)
1. Default movement edge time cost: `0` (travel between locations does not auto-advance time unless source TXT explicitly does).
2. Explicit time advancement stays in:
   - [onobjsel.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/onobjsel.rpy#L129) (`qsp_time_change_menu`)
   - [AdvanceTime.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/AdvanceTime.rpy#L4)
   - [NextDay.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/NextDay.rpy)
   - event-specific scripted branches (example: Sherwood/FridayDance branches).
3. Fix incorrect time-call wiring where TXT requires `gs 'AdvanceTime'` semantics.

### Concrete TODO List (implementation order)
1. **Create authoritative mapping document**
   - Add `devdocs/TXT_TO_RPY_MAP.md` with:
   - Full TXT location inventory (`224`) and port status.
   - World-room table (`23`) with: txt source, rpy label(s), aliases, exits, description source, time behavior.
   - Missing/incomplete map list (`missing rpy`, `missing label`, `runtime blockers`).
2. **Fix startup/runtime blockers first**
   - Implement missing `WhoreNextDayClients` label/function path referenced at [NextDay_NewDayEvents.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/NextDay_NewDayEvents.rpy#L230).
   - Verify no startup traceback on new game.
3. **Normalize world location entry**
   - Add `qsp_enter_location(...)` call at top of world labels that currently miss it (`TavernGloryHole`, `GroceryStore`, `WineStore`, `Church`, `ChurchAfterCermon`, `ChurchIspoved`, `EllonaTemple`, `PortStreets`, `ArtisansQuarter`, `StolyarWorkshop`, `DressShop`, `SherwoodTravel`, `BeckyHomeFront`, `BeckyHome`, `city_guard`, `friday_dance`).
4. **Repair location-link semantics mismatches**
   - Church arg flow: [Church.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Church.rpy#L81), [Church.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Church.rpy#L93) must pass expected argument for [ChurchIspoved.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ChurchIspoved.rpy#L2) and [ChurchAfterCermon.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ChurchAfterCermon.rpy#L3).
   - Fix invalid `$ AdvanceTime('Church')` call at [ChurchIspoved.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ChurchIspoved.rpy#L38) to proper label call flow.
5. **Canonical navigation graph alignment**
   - Reconcile room graph exits in [RoomClassSystem.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/RoomClassSystem.rpy#L454) with actual TXT `act ... gt ...` edges from world TXT files.
   - Keep all alias links operational through [RuntimeCompat.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/RuntimeCompat.rpy).
6. **Screen and menu integration pass**
   - Validate status navigation buttons and dynamic action menus resolve to existing labels.
   - Ensure click-to-continue and action menus preserve source branch logic and texts.
7. **Parity validation pass**
   - Run scripted smoke route over all `23` world nodes and all direct exits.
   - Confirm `CurLoc`, `PrevLoc`, HUD location, and `BlockTimeAdvance` are correct after each move.
   - Confirm tavern events queue/dispatcher still works from day transition.

### Important Interface/API Changes
1. `Room`/`RoomExit` graph in [RoomClassSystem.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/RoomClassSystem.rpy) becomes explicit authoritative navigation interface.
2. Add/standardize a per-exit `time_cost` metadata field (default `0`) for future-proof parity checks.
3. Standardize world label entry contract: every world label must call `qsp_enter_location(<canonical_room_id>)`.
4. Preserve alias API in [RuntimeCompat.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/RuntimeCompat.rpy) to avoid breaking legacy jumps/calls.

### Confirmed Potential Ren’Py Bugs (to fix early)
1. Missing label crash: `WhoreNextDayClients` at [NextDay_NewDayEvents.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/NextDay_NewDayEvents.rpy#L230).
2. Church route argument mismatch: [Church.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Church.rpy#L81), [Church.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Church.rpy#L93), [ChurchIspoved.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ChurchIspoved.rpy#L4), [ChurchAfterCermon.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ChurchAfterCermon.rpy#L5).
3. Invalid `AdvanceTime` invocation style at [ChurchIspoved.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ChurchIspoved.rpy#L38) vs label in [AdvanceTime.rpy](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/AdvanceTime.rpy#L4).
4. Location sync gaps: many world labels do not call [qsp_enter_location](C:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/loc.rpy#L6), causing HUD/event desync risk.

### Test Cases and Acceptance Criteria
1. New game start reaches tavern with no traceback.
2. Every world location can be entered and exited via valid links; no `LabelNotFound`.
3. HUD `Location` and `CurLoc` always match actual location after each move.
4. Time behavior matches source:
   - movement default no time cost,
   - explicit time menu advances correctly,
   - day rollover via `NextDay` works,
   - special scripted branches preserve intended time changes.
5. Tavern event queue lifecycle still works across day transitions.
6. No text changes in migrated content; no mechanic changes beyond bug-fix parity restoration.

### Assumptions and Defaults
1. Preserve original gameplay mechanics exactly; fix only conversion bugs and broken links.
2. “Turn linked to time” means explicit time-aware action policy per edge/action, not forced auto time increment on every movement click.
3. World navigation scope for starter phase is the `23` locations listed above; utility/event/internal labels are mapped in the full TXT→RPY matrix document but not treated as top-level map nodes.
4. Existing docs remain and are extended, not replaced.
