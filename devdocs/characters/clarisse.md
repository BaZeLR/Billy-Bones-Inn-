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
| 4 | Hunter Club arrest rumor, at least seven game days after that conversation, or after MC reports Clara before the conversation. This concerns Mongol's arrest, not Clara's separate immediate detention. |
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

## Early accusation and alternative custody route (2026-09-22)

User clarification: naming Clarissa to Zimmer means **immediate arrest**,
not merely recording an allegation. This is independent of the later fiance
case. Ordinary horse/Robin complaints keep their existing conditions and text.
The new choice does not require a stolen horse, an earlier complaint, spare
daily talk allowance, Mongol's arrest, or the cellar/punishment scene.

`claraMongolAccusation` is the single owner of this new case:

| Stage | Event / decision | Consequence |
| --- | --- | --- |
| 0 | Zimmer talk; `claraBookletMarket.done[2]` (actually witnessed the deal), guard office open and Zimmer physically there. | Name Clara: advance to 1 and arrest immediately. Protect: abort this accusation thread and add trust +1 once (cap20), without confessing/advancing her other stories. Postpone: no progression; can reconsider the same day. |
| 1 | Visit Clara at the guardhouse, 21:00–23:59. | Give one existing tavern food unit: advance to2. Leaving spends nothing. No food duplication or separate fed flag. |
| 2 | Clara has been fed and remains detained. | During the existing successful Mongol-release event, an additional explicit choice can free Clara too. Same lockpicks, guard distraction and existing stock costs; her extra food was already consumed at stage1. Declining leaves her in custody. |
| 3 | Return to TavernMain; a dedicated arrival event, not default room description. | Accept Clara as a household worker sharing Melissa's room; schedule cleaning for tomorrow via `Clara.set_job_value("jobcleaningtomorrow", 1)`. Advance completes the case. Postpone retains the arrival event. |

- `Clara.mongol_case_detained()` reads reported `done[0]` and release `done[2]`.
  No `clara_arrested`/`clara_freed` mirror. Normal location and physical-Clara
  event predicates use this result dynamically, even if their thread was
  already activated. No blanket abort/reset of other Clara threads.
- Early reporting skips only pending booklet stage3: `num=4`, `done[3]` stays
  false, day becomes report day. If the denial or later events already played,
  their progress/date is untouched. Mongol's seven-day rumor delay remains.
- The fiance introduction at church now requires recorded Mongol arrest
  (`Mongol.stocks_arrest_day >= 0`) and Clara not in this separate custody.
  The ordinary Legare-family church description also omits detained Clara.
- `Clara.tavern_resident()` replaces the narrower old paintings-resident name;
  it derives residence from the existing paintings milestone or completion of
  this case. Household roster/food count and Clara's schedule use that owner.
  Regular work uses inherited job fields; no hired-service availability flag
  is set. Tomorrow's assignment is available in the existing scheduler.
- A resident's home is Melissa's room, not the wine shop. Hordus's established
  merchant dates remain intact. Friday keeps the same 60/40 dance/home roll;
  the resident home outcome becomes Melissa's room.
- This new user-authored custody route has no equivalent in the available
  Zimmer TXT. Existing portraits are reused; no new detention artwork is claimed.

### Approved continuation still to implement

These are **not completed** by the arrest/shared-escape patch:

1. Melissa requests Clarissa's paid release; the paid branch converges on the
   same release/arrival owner without falsely marking food or Mongol escape as
   played. **Release price awaits user value.** This route is also needed if
   Mongol has already escaped, was convicted, or MC declined the shared escape.
   Until it is implemented, those choices leave Clara detained; do not claim
   this alternative branch is fully playable.
2. Clarissa exposes Legare's fraud during investigation. Legare offers MC the
   wine cellar and flees. **Sale price awaits user value**; no current wine-shop
   property ownership API or implemented sale was found. Keep this consequence
   separate from merely feeding Clara and from the later fiance investigation.
3. Pauline becomes the wine-shop NPC when Clara settles in the tavern through
   either story route. Pauline currently exists only in lore, not as a registered
   NPC. Create her definition/runtime once through PeopleRegistry; subsequent
   shop assignments must preserve her relationships, wardrobe and story stages.
   Her presence/seller menu must follow the shop's actual opening hours. After
   Legare leaves, she runs it without his normal seller/talk presence.
4. Preserve the returner's lack of money and disclosed injury. Integrate the
   previously approved care/ointment continuation without falsely completing
   her fiance, confession or education milestones. The current arrival mentions
   the injury; it does not implement those additional scenes.
5. Shared rescue retains Mongol's existing forest safe-passage/Blackwood opening.
   Finishing the bandit-camp branch and its separately planned loot is not
   implied by this rescue.

The wider approved costume/forest -> fiance case -> protective Legare fight ->
tavern lessons/renovation and Amanda consequence ordering remains a separate
pending delta; this patch does not claim to implement that entire plan.

Verification for this custody slice (Ren'Py 8.5.2): 127 focused Python/source
checks passed; 32 isolated native cases plus the existing church-fiance case
passed. Coverage includes actual report/protect/postpone clicks, one-time food,
both shared-escape decisions, arrival/work enrollment, actual save/load in
detained and resident states, and old-save missing-thread initialization.
Compile/lint exit0; lint's unreachable rows are injected test declarations.
No player save was modified by the checks.

Two pre-existing assertions in `test_clara_fiance_continuation_source.py`
remain outside this slice: literal `currentVersion = 92` (baseline is97), and
ordering a now-absent Mongol sentence in the unchanged ointment label. Neither
production file was rewritten to satisfy those stale expectations. This is
not a claim that the full repository suite or the whole story is complete.
