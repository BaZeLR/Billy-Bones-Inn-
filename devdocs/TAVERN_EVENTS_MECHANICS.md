# Tavern Events Mechanics (Current RPY Runtime)

This document is the current reference for tavern-event mechanics in the Ren'Py port.
It describes how events are created, dispatched, resolved, and how they modify tavern/crew state.

Scope:
- Queue creation and dispatch.
- Event handlers and side effects.
- Crew-relationship impacts (`Friends`, `sluttiness`, role skills).
- Daily systems that feed tavern event behavior.

Primary sources:
- `game/Inn/CreateTavernEvents.rpy`
- `game/Inn/CreateTavernEventsPeriod.rpy`
- `game/Inn/CreateMandatoryEvents.rpy`
- `game/Inn/DisplayTavernEventShort.rpy`
- `game/Inn/TavernMain.rpy`
- `game/Inn/NextDay.rpy`
- `game/Inn/DisplayTavernEventsSummary.rpy`
- `game/Inn/EventFightSmall.rpy`
- `game/Inn/EventWineForDance.rpy`
- `game/Inn/EventCleaningHarrass*.rpy`
- `game/Inn/EventWaitressHarrass*.rpy`
- `game/Inn/EventAmandaLizettTalk*.rpy`
- `game/Inn/PartEvent*.rpy`
- `game/Inn/NextDay_NewDayEvents.rpy`
- `game/Inn/WhoreNextDayClients.rpy`

## 1. Runtime Lifecycle

1. Day transition builds tavern queue.
- `NextDay` calls `NextDay_NewDayEvents` then `CreateTavernEvents` (`game/Inn/NextDay.rpy:40-42`).

2. Queue is split by period key.
- `EventsCount[period]` stores count.
- `NewEvents["{period}_{index}"]` stores event code.
- See `game/Inn/CreateTavernEvents.rpy:5-6`.

3. Main tavern loop may consume one event for current period.
- In `TavernMain`, if tavern is open and random check passes (or mandatory exists), it calls `DisplayTavernEventShort(time, 1)` (`game/Inn/TavernMain.rpy:76-77`).

4. End-of-day summary drains remaining events with no eyewitness branch.
- `DisplayTavernEventsSummary` loops periods `0..4` and repeatedly calls `display_tavern_event_short(period, 0)` until empty (`game/Inn/DisplayTavernEventsSummary.rpy:18-24`).

## 2. Queue Data Model

- `EventsCount`: dict indexed by time period integer.
- `NewEvents`: dict indexed by composite key `"period_index"`.
- Mandatory queue uses period `10`.

Files:
- `game/Inn/CreateTavernEvents.rpy:4-6`
- `game/Inn/CreateMandatoryEvents.rpy:2-3`

## 3. Event Generation Rules

### 3.1 Normal periods (0..4)
Implemented in `CreateTavernEventsPeriod(TimePeriod)`.

- Per period: exactly 3 rolls (`EventsICounter <= 2`) (`game/Inn/CreateTavernEventsPeriod.rpy:3-5,24`).
- Roll range: `1..20` (`game/Inn/CreateTavernEventsPeriod.rpy:6`).
- If `TimePeriod > 3`, roll is forced to `20` (effectively disables normal random inserts for that period) (`game/Inn/CreateTavernEventsPeriod.rpy:8-9`).

Inserted codes:
- `FightSmall` when `TimePeriod >= 3` and roll `<= 1` (`game/Inn/CreateTavernEventsPeriod.rpy:11-13`).
- `CleaningHarass` when roll `== 3` (`game/Inn/CreateTavernEventsPeriod.rpy:14-16`).
- `WaitressHarass` when roll `== 5/6` or (`TimePeriod >= 3` and roll `== 7/8`) (`game/Inn/CreateTavernEventsPeriod.rpy:17-19`).
- `AmandaLizaTalk` when roll in `9..11`, period is `1` or `2`, `jobWhoreAvail['liza']` true, and `(jobgloryhole['liza'] == 0 or TimePeriod < 2)` (`game/Inn/CreateTavernEventsPeriod.rpy:20-22`).

### 3.2 Mandatory period (10)
Implemented in `CreateMandatoryEvents`.

- Resets `EventsCount[10] = 0`.
- On week 4, pushes `WineForDance`.
- Then calls optional dance sequence label if present.

File:
- `game/Inn/CreateMandatoryEvents.rpy:2-12`

### 3.3 Port fallback injection (non-TXT behavior)
`CreateTavernEvents` adds one fallback event if both current-period and mandatory queues are empty.

Selection:
- `WaitressHarass` if any `jobwaitress` active.
- Else `CleaningHarass` if any `jobcleaning` active.
- Else `FightSmall`.

File:
- `game/Inn/CreateTavernEvents.rpy:14-45`

## 4. Dispatcher Behavior

Dispatcher label: `display_tavern_event_short(time_period, eyewitness)`.

Order:
1. Consume mandatory (`period 10`) first.
2. Else consume current period.
3. Consume from last inserted index (`EventsCount[period] - 1`) and decrement count.

Mapping:
- `WineForDance` -> `event_wine_for_dance`
- `FightSmall` -> `event_fight_small`
- `CleaningHarass` -> `event_cleaning_harrass`
- `WaitressHarass` -> `event_waitress_harrass`
- `AmandaLizaTalk` -> `event_amanda_lizett_talk`

File:
- `game/Inn/DisplayTavernEventShort.rpy:16-37`

## 5. Event Handlers and Side Effects

### 5.1 `FightSmall`
Entry:
- `label event_fight_small(eyewitness=0)`.

Primary side effects:
- Base economic loss via `money -= CurMoneyLoss`.
- Optional guard-call branch also deducts `money -= 4` and `winenum -= 2`.
- No direct `Friends` / `sluttiness` modifications in this event.

Files:
- `game/Inn/EventFightSmall.rpy:8-11,59-61,77-91,98`

### 5.2 `WineForDance`
Entry:
- `label event_wine_for_dance(eyewitness=0)`.

Side effects:
- Accept: `productnum -= 4`, `winenum -= 5`, `money -= 20`, `DanceSponsor = 1`.
- Decline or no stock: `DanceSponsor = 0`.

Files:
- `game/Inn/EventWineForDance.rpy:40-52`

### 5.3 `CleaningHarass` and `WaitressHarass`
Entries:
- `event_cleaning_harrass`
- `event_waitress_harrass`

Selection:
- Picks girl via `get_random_girl_by_job("jobcleaning")` or `get_random_girl_by_job("jobwaitress")`.

Files:
- `game/Inn/EventCleaningHarrass.rpy:9-12`
- `game/Inn/EventWaitressHarrass.rpy:11-13`

They both execute shared reaction chain:
1. `PartEventYourFirstReaction`
2. `PartEventGirlHarrassmentReaction`
3. `PartEventCustomerHarrassmentReaction`
4. `PartEventAfterHarrassment` (only when `eyewitness > 0`)

Files:
- `game/Inn/EventCleaningHarrass.rpy:24-27`
- `game/Inn/EventWaitressHarrass.rpy:26-29`
- `game/Inn/EventCleaningHarrassPart2.rpy:16,91-95`
- `game/Inn/EventWaitressHarrassPart2.rpy:12,72-75`

### 5.4 `AmandaLizaTalk`
Entries:
- `event_amanda_lizett_talk`
- `event_amanda_lizett_talk2`

State touched:
- `AmandaVar['prohibitliza']` transitions.
- `NotToSpeak`, `YourReaction1`, `YourReaction2` local state.
- `SlutFriendsIncrease("amanda", ...)` called in punishment and trust branches.

Files:
- `game/Inn/EventAmandaLizettTalk.rpy:14-67,84-98`
- `game/Inn/EventAmandaLizettTalk2.rpy:16-27,37-49`
- `game/Inn/SlutFriendsIncrease.rpy:2-23`

## 6. Crew Relationship and Skill Impact Matrix

### 6.1 Direct relationship effects (`Friends`)
- Harassment chain can increase/decrease `Friends[girl]` depending on player reaction and instruction mode.
- `PartEventGirlHarrassmentReaction` includes random ±1 paths.
- `PartEventAfterHarrassment` includes additional random negative reactions.
- Amanda-Liza talk can change Amanda relationship via `SlutFriendsIncrease`.

Files:
- `game/Inn/PartEventGirlHarrassmentReaction.rpy:29-37,42-44`
- `game/Inn/PartEventAfterHarrassment.rpy:19-22,30-33,40-42`
- `game/Inn/EventAmandaLizettTalk.rpy:87`
- `game/Inn/EventAmandaLizettTalk2.rpy:39,48`

### 6.2 Sexual openness effects (`sluttiness`)
- Harassment customer reaction can increment/decrement `sluttiness[girl]`.
- `SlutFriendsIncrease` may alter Amanda sluttiness in event branches.

Files:
- `game/Inn/PartEventCustomerHarrassmentReaction.rpy:29-31,42-45,55-57`
- `game/Inn/SlutFriendsIncrease.rpy:13-20`

### 6.3 Tavern reputation and role skill effects
- `PartEventCustomerHarrassmentReaction` can change `tavernfame`.
- Same handler can change `waitress[girl]` by ±1 in some outcomes.

File:
- `game/Inn/PartEventCustomerHarrassmentReaction.rpy:17-28,35-38,48-51`

## 7. Daily Systems That Feed Tavern Events

1. `NextDay_NewDayEvents` builds next-day sex/event tables and schedule flags.
- Writes `TodaySexEvents` and `DailyEventsList` rows.
- Rebuilds `FranBusy[0..4]` each day.
- Calls `WhoreNextDayClients` for georgett/liza.

Files:
- `game/Inn/NextDay_NewDayEvents.rpy:138-243`
- `game/Inn/WhoreNextDayClients.rpy:58-103`

2. `NextDay_TavernDaily` computes daily tavern economics/happiness and applies tomorrow jobs.
- Calls `SetTavernServiceLevels`.
- Uses role presence checks (`GetRandomGirlByJob('jobwhore'/'jobgloryhole')`) to modify happiness chance.
- Calls `ChangeTommorowWhoreJob` and `ChangeTommorowHallJob`.

Files:
- `game/Inn/NextDay_TavernDaily.rpy:6,48-51,88-92`

## 8. Signatures (for scripting/debug)

- `CreateTavernEvents`
- `CreateTavernEventsPeriod(TimePeriod)`
- `CreateMandatoryEvents`
- `display_tavern_event_short(time_period, eyewitness)`
- `event_fight_small(eyewitness=0)`
- `event_wine_for_dance(eyewitness=0)`
- `event_cleaning_harrass(eyewitness=0)`
- `event_cleaning_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1)`
- `event_waitress_harrass(eyewitness=0)`
- `event_waitress_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1)`
- `event_amanda_lizett_talk(eyewitness=0)`
- `event_amanda_lizett_talk2(eyewitness=0)`
- `PartEventYourFirstReaction(GirlNamePEYFR, SecondPartFuncName)`
- `PartEventGirlHarrassmentReaction(GirlNamePEGHR, JobTypePEGHR)`
- `PartEventCustomerHarrassmentReaction(GirlNamePECHR)`
- `PartEventAfterHarrassment(GirlNamePEAH, GirlSlapped, YourReaction1)`

Source index:
- `game/Inn/*.rpy` (see `rg` signatures list)

## 9. Known Risks / Mismatches to Track

1. Possible typo in Amanda-Legare chance logic:
- Uses `sluttiness.get('alberfriends', 0)` where code pattern suggests `AmandaVar['alberfriends']` or Amanda sluttiness threshold logic.
- File: `game/Inn/NextDay_NewDayEvents.rpy:203-205`.

2. `CreateTavernEvents` forces one fallback event if queue is empty for current period and mandatory.
- This can increase event frequency compared to strict random generation.
- File: `game/Inn/CreateTavernEvents.rpy:14-45`.

3. `NextDay_TavernDaily.rpy` contains helper stubs at file end (`GetRandomGirlByJob` returns empty string, others `pass`).
- If these are the active bindings at runtime, whore/glory happiness effects and some job transitions can be neutralized or redirected unexpectedly.
- File: `game/Inn/NextDay_TavernDaily.rpy:95-111`.

4. Multiple definitions for `get_random_girl_by_job` / `GetRandomGirlByJob` exist.
- Keep one canonical implementation path to prevent load-order behavior drift.
- Files: `game/Inn/GetRandomGirlByJob.rpy`, `game/Inn/ChangeTommorowWhoreJob.rpy`, `game/Inn/NextDay_NewDayEvents.rpy`.

## 10. Minimal Verification Checklist

- Start new day and confirm `EventsCount`/`NewEvents` populated after `CreateTavernEvents`.
- Enter `TavernMain` and confirm at most one short event is consumed per entry.
- Confirm period `10` events are consumed before period `time` events.
- Run one `CleaningHarass`/`WaitressHarass` branch and verify diffs in:
  - `Friends[girl]`
  - `sluttiness[girl]`
  - `tavernfame`
  - `waitress[girl]`
- Confirm `DisplayTavernEventsSummary` drains remaining queues with `eyewitness=0`.
