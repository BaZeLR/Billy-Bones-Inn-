# Character Worklist: Кларисса (Clara)

> REFERENCE ONLY.
>
> This file preserves source/TXT worklist names. Legacy relationship-map tokens
> are not current runtime owners. Runtime/story state belongs to the character
> class instance and event/thread labels.

## Identity
- Canonical id: clarisse
- Legacy keys/tokens: Clara, Кларисса, clara
- Init source: InitSecondaryNPC.txt
- Current runtime owner: Clarisse/Clara class instance

## Presence/Schedule (TXT-driven notes)
- Утренняя продавщица в WineStore (time == 0).
- Вне утра заменяется на Альбера; прямые ветки Клариссы скрыты.
- Упоминается в церковных/легаре сценах как часть семьи Legare.

## Flags/Variables (Init authority)
- Friends[Clara]
- Talked[Clara]

## Primary Scenes/Dialogs/Features (TXT files)
- WineStore.txt -> WineStore.rpy (rpy_exists)
- Church.txt -> Church.rpy (rpy_exists)
- AfterDanceSexLegare.txt -> AfterDanceSexLegare.rpy (rpy_exists)
- InitSecondaryNPC.txt -> InitSecondaryNPC.rpy (rpy_exists)

## Full TXT Coverage (anti-omission list)
- AfterDanceSexLegare.txt
- Church.txt
- InitSecondaryNPC.txt
- WineStore.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event included.
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.

## Current market / Mongol / forest order (2026-09-22)

This section records the user's current correction, not additional QSP text.
The legacy names and compatibility suggestion above are historical only;
the runtime follows `devdocs/README.md` and does not add aliases or mirrors.

`claraBookletMarket` owns the ordered progression:

| Stage | Event and prerequisites |
| --- | --- |
| 0 | Existing daytime booklet/Hordus encounter; unchanged. |
| 1–2 | Closed-market sighting and witnessed Mongol deal. Monday–Thursday or Saturday, 19:00–22:59, existing daily evening roll, exploration >=100, actual horse-theft attempt recorded, and Melissa's drawings conversation completed (`claraPaintingsPath.done[0]`). Finding the drawings alone is insufficient. |
| 3 | Ask Clara about the night conversation from her Wine Store talk menu while she is there and the shop is open. She denies the theft arrangement. This is NOT the later truthful confession. Finish returns to Clara's talk menu. |
| 4 | Hunter Club arrest rumor, at least seven game days after that conversation. No immediate arrest or rumor before the question. |
| 5–9 | Existing stocks sighting, food, lockpick order, release/conviction and aftermath, in the same order and with their existing requirements. |

- `player.horse.theft_attempted` is the sole durable record of an actual stable
  theft attempt: set when MC scares off the thief, or during overnight
  resolution (dog stops thief / horse stolen). Scheduling or cancelling an
  attempt does not set it. Buying another horse or a cooldown expiring does
  not erase it.
- `claraForestSofa` can begin after the witnessed deal (booklet stage >=3),
  without waiting for arrest/release. Its existing relationship level, daytime
  exploration requirement, ordered scenes, time costs and outcomes remain.
- The costume request remains in the shared forest bath. Gifting transfers
  `thiefdress` to Clara's existing wardrobe; no separate costume-gift flag.

`claraMoonSabbath` is a separate recurring entry event, not another stage of
the theft or forest/sofa quest. Conditions are checked by the event each time:

- Saturday, 19:00–22:59, closed MarketPlace;
- live calendar reports Full Moon (currently period days 17–20);
- exploration >=100, forest request already played (ForestSofa stage >=3),
  forest thread not aborted, Clara owns `thiefdress`;
- follow or stay: staying costs no time; following is a 60-minute round trip
  and 5 energy, showing Clara sketching the sabbath while MC remains hidden;
- paragraph/continuation buttons, no location navigation during the scene;
  return restores market picture/text/menu; other thread stages are untouched;
- the costume uses the existing wardrobe layers; either exit restores the
  previous layers/context without changing Clara's preferred daytime outfit;
- once per eligible day; later eligible full moons may repeat. The current
  moon's name comes directly from Calendar. No new lunar calendar is invented.

No matching sabbath TXT or dedicated illustration was found. The new authored
scene uses existing night-market and hidden-forest-path art. It does not claim
to restore an original illustration or distinct unwritten seasonal scenes.

Save version 97 inserts the denial without replaying completed arrests or
later outcomes. Old stage 3 now waits for the question; old stages 4+ shift by
one. Completed/aborted state, day markers and inventory are preserved. Older
saves recover theft history only from retained theft/cost evidence; expired,
unrecorded thwarted attempts cannot be reconstructed honestly.

Verification (Ren'Py 8.5.2, isolated test saves): 24 native cases in
`tools/external_clara_mongol_test.py` passed, including real menu clicks,
theft resolution, the seven-day boundary, both sabbath exits, temporary
clothing restoration and save-stage migration. Seven native Hordus cases
passed separately, as did the existing Mongol feeding/release and Zimmer
wine-dialogue click tests (33 native cases total). Compile/lint exited 0;
lint's unreachable statements were
in the injected test harness only. Focused Python/source suites: 96 passed.
This verifies the changed paths, not every branch of the entire game.
