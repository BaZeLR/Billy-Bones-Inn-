# Character Port Plan (TXT Authority)

> REFERENCE ONLY / HISTORICAL PLAN.
>
> This plan may contain old dict/global assumptions. Do not treat it as current
> architecture. Character state now belongs to NPC classes and event/thread
> labels own their own story flow.

Scope: girls + Clarisse/Clara documentation-first pass before UI implementation.

## Locked Rules
1. TXT files are authority for dialogs, scene gates, and variable semantics.
2. Do not change original gameplay text or mechanics.
3. Character interaction UI is additive: clickable character -> dialog window -> conditional action list.

## Concrete TODO (Execution Order)
1. Build per-character TXT coverage docs (done).
2. Build per-character schedule matrix (location x time x condition) (pending).
3. Build per-character action matrix (talk/chat/dress/...) excluding sex engines/special events for first UI pass (pending).
4. Add canonical per-character entry labels (char_<id>_entry) and compatibility aliases (pending).
5. Add character dialog screen with portrait + side action column (pending).
6. Add location-level character visibility resolver and plug it into right status panel (pending).
7. Wire clickable character buttons in location flow (starting: TavernMain, PortStreets, GroceryStore, WineStore, DressShop) (pending).
8. Keep disabled actions hidden until TXT conditions are true (in progress).
9. Run parity test routes and update docs with gaps/bugs (pending).

## Sequential Apply Progress
- `Amanda`: in progress
  - `IntAmandaTalk.rpy`: patched to TXT-parity conditions/branches, restored full deflower branch text, restored missing `SlutFriendsIncrease` calls.
  - Next Amanda targets: `IntAmandaDressChange.rpy`, `IntAmandaSex.rpy`, `AmandaLegareDanceSequence.rpy`.
- `Becky`: in progress
  - `IntBeckyTalk.rpy`: menu flow wired to real talk handlers + Sherwood discussion entry.
  - `RuntimeCompat.rpy`: `_int_becky_talk_*` handlers replaced from stubs with TXT-based stateful logic.
  - `BeckyHome.rpy`: fixed invalid inline call interpolation, stabilized defaults, restored non-crashing mode branches, and unified entry to `IntBeckySex`.
  - `BeckyHomeFront.rpy`: fixed state reset loop on menu return and aligned key menu gates to TXT progression.
  - `BeckyInviteHome.rpy`: fixed legacy `Becky`/`becky` key mismatch and missing default guards for invite conditions.
- `Georgett`: pending
- `Liza`: pending
- `Melissa`: in progress
  - `IntMelissaTalk.rpy`: rebuilt to TXT-faithful action gates (`Talked/Friends`) with proper Ren'Py calls (`GirlsDesc`, `SlutFriendsIncrease`).
  - `IntMelissaTalk.rpy`: integrated conditional dress-buy action visibility using daily-event checks (`BuyDressTom`, `BuyDress`) and week gate (`week != 6`).
  - `IntMelissaDressChange.rpy`: reused as callable sub-flow for scheduled dress-buy setup (`DailyEventsList`).
- `Sandra`: in progress
  - `IntSandraTalk.rpy`: rebuilt to TXT-faithful flow (`Осмотреть`, reconciliation with mother phrasing, conditional dress-buy action).
  - `IntSandraTalk.rpy`: migrated to proper Ren'Py calls (`GirlsDesc`, `SlutFriendsIncrease`) and daily-event/weekday gating for dress-buy visibility.
- `Irma`: in progress
  - `IntIrmaTalk.rpy`: added dedicated Irma interaction flow on Action-based screen buttons (`Осмотреть`, `Спросить, когда будет готово`, dynamic male dress order list).
  - `DressShop.rpy`: wired shop conversation to `IntIrmaTalk`, removed placeholder dress-menu stubs, preserved close/open schedule and return flow.
  - `DressTry.rpy`: restored callable dress-order path with args (`DressTry("You", dress_code)`) and compatibility alias `DressTry`.
- `Inga`: in progress
  - `IntIngaTalk.rpy`: added dedicated Inga interaction entry with TXT-safe action set (`Осмотреть` via `GirlsDesc`) and optional menu mode for character-action UI wiring.
  - `IntBeckyGuest.rpy`: `Осмотреть Ингенборг` now routes through `IntIngaTalk` while preserving original behavior and conditions.
- `Clarisse`: in progress
  - `IntClaraTalk.rpy`: added dedicated Clarisse chat loop from `WineStore.txt` (`smalltalk` + `flirt`) with TXT conditions and stat updates (`Talked['Clara']`, `Friends['Clara']`).
  - `WineStore.rpy`: replaced inline Clarisse chat block with `call IntClaraTalk` and added safe Clara/Talked initialization guards.

## Deliverables in This Pass
- devdocs/CHARACTER_TXT_COVERAGE.md
- devdocs/characters/*.md (one file per character)

## Risks to Address Before UI Wiring
1. Mixed key styles: lowercase IDs (amanda) vs legacy keys (Clara, Alber).
2. Some talk labels are incomplete/placeholder in current .rpy; TXT parity must guide fixes.
3. Location presence can come from both CurrentLoc and direct time/week checks in location TXT.
