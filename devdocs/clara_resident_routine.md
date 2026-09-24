# Clarissa: resident routine and table conversation

## Scope

Clarissa's existing `tavern_resident()` predicate remains authoritative. This
change does not rewrite her earlier story, merchant inventory, dialogue or
education thread.

| Situation | Owner / behavior |
| --- | --- |
| Regular assigned duties | Existing Girl job scheduler; obsolete visitor overrides no longer apply to a resident |
| Hordus's two monthly visits | Existing merchant calendar; Clarissa joins only when not on an assigned shift |
| Breakfast | Resident Clarissa joins the existing attendance snapshot; no attendance when detained |
| Sunday dinner | Kitchen, 12:30–13:30; existing Sunday lake-walk selection includes her when its relationship/awake conditions pass |
| Drawing at MC's window | Resident, completed peephole, 09:00–11:59 in MC room; jobs retain priority |

Friday dances and planned education outings remain unchanged. This is not a
blanket prohibition on leaving the tavern. No new sickness/pregnancy system or
forest travel procedure is introduced.

## Events and return flow

`claraResidentLife` is an ambient RThread (not a linear quest). Its entry and
breakfast events use the existing once-per-day event firing guard, not a new
NPC counter. They do not advance/complete a one-shot quest. Explicit drawing
conversation is repeatable without a stat reward.

- `story_clara_drawing_work`: MC-room entry shows the existing room picture.
  Asking about the sketches explains their intended sale to Hordus. Attempting
  a kiss gets her busy response and returns to the caller. Flirting through her
  talk menu while she draws uses this same event, then returns to the talk menu.
  Ordinary conversation in MC's room does not apply a work-interruption penalty.
- `story_clara_breakfast_banter`: a separate native event during active breakfast,
  only while Clarissa is an attendee. Eleven equally weighted anecdotes include
  the original masked noble, servant's table manners, and aristocratic hypocrisy,
  plus the user's wedding-night rustic, fat abbot at the city gate, adulterous
  friar's sermon, and wool-net/brothel retort. The four supplied jokes are retold
  in Russian with Clarissa's comic delivery; no existing joke is removed. Four
  further entries retell the supplied Miller's Tale, Summoner's Tale, friars-in-hell
  prologue, and an original non-graphic joke about a married scribe's private
  "rehearsals". These are comic adaptations, not verbatim Chaucer translations.
  She also
  suggests a Sunday lake outing. Supporting her mood gives each present NPC +1
  motivation via the existing `change_mana` method; simply continuing gives no
  bonus. No corruption or clothing change. Another higher-priority breakfast
  story can take precedence, so this is not guaranteed at every breakfast.

The event labels own their choices, pictures and text. The existing UI context
restore returns to the room/talk/breakfast without retaining event imagery or
duplicating the static room paragraph. Room navigation remains room-owned.

The lake proposal is dialogue plus participation in the existing Sunday-walk
mechanic, not a new group-trip system. A distinct post-renovation drawing scene
has not been specified or added. New explicit touching/erotic stories were not
implemented; pre-existing authored content is unchanged.

## Kitchen and Sunday meal art

New natural-style assets under `game/images/kitchen/renewed/` retain the existing
kitchen layout and character identities. The room background is
`kitchen_room_day.png`; ordinary breakfast uses `breakfast_core.png`; Sunday
dinner uses `sunday_core.png` or `sunday_clarissa.png` when both Clarissa and
Melissa are present. On alternate Sundays, Clarissa temporarily chooses her
loose home chemise if she is in her ordinary green dress. In that case the
whole-table image is `sunday_clarissa_homewear.png`, and her wardrobe returns
to the day outfit after dinner or before the lake walk. Gifted/current outfits
are not overwritten by this choice. The images are selected from her actual
current wardrobe state, not a second clothing flag.

During Sunday dinner the existing event menu has a once-per-meal option to
hear Clarissa's anecdote. It shows the matching close-up,
`clarissa_story_cozy.png` or `clarissa_story_homewear.png`, with Melissa beside
her; after the continuation, the full Sunday image and menu return. The
existing meal schedule and completion state own the scene. All old images
remain in place.

The meal images were generated with the built-in image tool. Prompt set:
natural, portrait-matched game rendering in the existing kitchen; an empty
daylight room; the usual four-person breakfast and Sunday dinner; five-person
Sunday variants with Clarissa beside Melissa in green daywear and loose ivory
homewear; and two matching close-ups of their story. The current NPC cards and
portrait supplied facial references. The room's hearth, window, doorway and
shelves were kept in consistent positions across the set.

Ren'Py 8.5.2 compile and lint passed in an isolated project. The native Sunday
story test passed in both wardrobe states (2 cases, 14 assertions), including
the return to the dinner menu and restoration of Clarissa's day clothes.

## Verification commands

- `python -m pytest tests/test_tavern_renovations_runtime.py tests/test_clara_residency_runtime.py tests/test_hordus_schedule_runtime.py -q`
- `python tools/external_clara_resident_test.py --keep-temp --compile-lint`

The native runner copies scripts into a temporary project and reuses the
renovation suite, including its actual old-save load check. Added cases click
all drawing choices, the busy-flirt return, breakfast encouragement/decline,
and check attendance, Sunday eligibility, daily limits and single text rendering.
The player's running game and saves are not modified by this runner.

### Results, 2026-09-23

- Focused owner/schedule tests: **167 passed**, 3 skipped. The skipped rejection
  combinations are the three newly permitted `requested` member projects;
  dedicated positive cases verify their request-to-order path.
- Native Ren'Py **8.5.2.26010301**: **40 cases / 276 assertions passed**.
  The disabled-by-default old-save case ran separately and reached
  `RENOVATION_FULL_LOAD_PASSED`, including restored pending request booleans.
- Compile/lint passed; lint only reported unreachable generated test statements.
- Expanded regression selection: 307 passed, 3 skipped, 1 pre-existing failing
  source assertion in `test_hordus_sofa_save_migration.py` demanding version 93.
  HEAD was already version 102; this change upgrades to 103. That unrelated
  hard-coded assertion was left untouched, not reported as a passing test.
- Native logs retained under
  `C:/Users/blank/AppData/Local/Temp/tractir_renovations_olek1dff/TractirExternalRenovationsProject/`
  (`renovations-compile.log`, `renovations-lint.log`, `renovations-test.log`,
  `renovations-load.log`).

### Breakfast anecdote expansion, 2026-09-23

Only the authored anecdote branches, their random-selection upper bound, this
document and the breakfast test parameters changed. Triggers, continuation
buttons, daily firing guard and motivation reward are unchanged.

All eleven anecdotes were exercised with both reward choices using real
calendar seeds: **22 native cases / 220 assertions passed**. Focused log:
`C:/Users/blank/AppData/Local/Temp/tractir_breakfast_anecdotes_rnb30huj/TractirExternalRenovationsProject/log.txt`.
Compile/lint passed in the `tractir_renovations_v6bdykdv` isolated project.
Its broader run was **not clean**: 49 passed, 11 menu-click timeouts in unchanged
renovation/guest-room cases, one separate save/load case skipped. No failed
assertions; all breakfast variants passed in that run as well. Those intermittent
non-breakfast failures were not repaired as part of this content-only request.
