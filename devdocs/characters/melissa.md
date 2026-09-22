# Character Worklist: Мелисса

> REFERENCE ONLY.
>
> This file preserves source/TXT worklist names. Legacy `*Var` tokens are not
> current runtime owners. Runtime/story state belongs to the character class
> instance and event/thread labels.

## Identity
- Canonical id: melissa
- Legacy keys/tokens: melissa, MelissaVar
- Init source: InitMelissa.txt
- Current runtime owner: Melissa class instance

## Presence/Schedule (TXT-driven notes)
- Основная локация старта: TavernMain.
- Рабочие смены определяются через job* назначения.

## Flags/Variables (Init authority)
- MomDressComplaint

## Primary Scenes/Dialogs/Features (TXT files)
- InitMelissa.txt -> InitMelissa.rpy (rpy_exists)
- IntMelissaTalk.txt -> IntMelissaTalk.rpy (rpy_exists)
- IntMelissaDressChange.txt -> IntMelissaDressChange.rpy (rpy_exists)

## Current Runtime Story Logic

### Household comfort and stock appreciation (2026-09-22)

This is new authored gameplay, not a reconstruction of a missing TXT stage.
`MelissaInfo` owns Melissa's scores; existing owners retain all world state.

- `Melissa.comfort` is derived, not another saved copy of repairs/problems.
  `comfort_components` exposes the breakdown:
  - no rats: +1 from `werecat_state()["rats_problem_active"] == 0`;
  - room repaired: +1 from `Melissa.bats_repair_complete()`;
  - yard and toilet fixed: +1 each from completed `tavern` backyard renovation;
  - laundry/bathroom: +2 from completed `tavern` shed renovation;
  - weekly cleaning adjustment: saved `Melissa.comfort_cleaning_score`.
- The existing weekly chore evaluator adjusts cleaning once per evaluated week:
  at least one `player.chores.weekly["clean_upstairs_rooms"]` gives +1; none gives
  -1. It runs before the existing weekly counters reset and uses their existing
  evaluation stamp. Reopening a menu or loading a save awards nothing.
- `Melissa.household_satisfaction` is separate from friendship, trust and
  corruption. Successful grocery/wine restocking and carried-food deposits add
  +2 per transaction. A multi-unit deposit gives +2, not +2 per unit. The existing
  "deposit all" operation makes one deposit per food type. Empty/cancelled
  actions and passive inventory reads give no points.
- Stock totals stay in `player.tavern_management.productnum` / `winenum` and the
  existing pantry item stock. No stock mirrors are introduced.
- Milestone `melissa_full_storeroom`: after a restock, more than 100 food servings
  and at least 50 barrels of wine together. One barrel is 10 internal wine units,
  so the rule is `productnum > 100 and winenum >= 500`.
- The existing achievement runtime records this milestone. Its one-time reward
  thread is `melissaStoreroomMilestone`, triggered on the next Melissa talk via
  `talk_melissa / storeroom_thanks`. Spending supplies later does not erase the
  earned scene. Completion belongs solely to that thread.
- `MelissaHouseholdPriorities` expands the existing "what matters most" topic;
  its existing daily/relationship conditions and +1 friendship/openness remain.
  The new score mechanics do not add relationship rewards of their own.
- Both new scenes use native paragraph/continuation menus, suppress the room
  description while playing, and return to Melissa's talk menu. Leaving the
  talk restores the original room picture, text and navigation.
- Save migration V94 -> V95 adds only missing scores, initially zero, and
  registers the new thread. Existing inventories/progress are not reset and
  scores are not awarded retroactively.
- Renovations and Draupnir order options remain hidden. No renovation request
  conversations are activated by this change.
- Tavern karma is deferred: the user will identify the existing authoritative
  value. Do not create or derive another karma score.

Verification: `tests/test_melissa_household_runtime.py`, existing story-condition
scope tests, and `tools/external_melissa_household_test.py` (isolated Ren'Py copy,
temporary saves; includes native menus, purchases, event completion and migration).
On 2026-09-22: 144 focused regression checks passed, including 26 new behavioral
cases; 10 native Ren'Py 8.5.2 cases passed. Compile/lint exited 0; lint reports only
the injected test statements as unreachable. A broader check also reproduced two
pre-existing assertions in `test_melissa_object_source.py`: it expects save version
92 (baseline was 94) and an absent `girl in GIRL_DECISION_CORE_IDS` expression.
Neither those tests nor the unrelated decision model were changed by this feature.

### Romance / intimacy progression gates
- Flirt is allowed when Melissa's relationship/openness state is high enough and the normal daily/social limits allow it.
- Flirt alone must not unlock make-out, sex-engine access, or deeper sexual actions.
- Deeper intimacy requires Melissa's story safety/trust gates:
  - the rat problem is completed;
  - the bat problem is completed far enough that the room/roof problem is solved;
  - and the player has either taken/kept the found booklet or deliberately left it in place and unlocked the spy branch.
- The booklet/spy branch is a story gate, not a generic social-action shortcut:
  - taking the booklet means the player owns `melissa_drawings_booklet_001` and can read it from inventory;
  - leaving the booklet means `Melissa.var["drawings_spy_option_unlocked"] = 1` and later spy/seduction events may become available;
  - once a sex-engine path is seen/allowed by these events, Melissa's later intimacy actions may use the normal sex engine.
- These gates belong on `MelissaInfo` methods / Melissa thread conditions. Labels should only present the scene, choices, text, pictures, and direct state changes.

### Bat problem / hidden booklet
- Thread: `melissaBatProblem`
- Amanda-room search stage: `story_melissa_bat_problem_5`
- Amanda-room location/action: `TavernAmandaRoom` / `melissa_bats`
- Physical booklet search stage: `story_melissa_bat_problem_booklet_search`
- Physical search location/action: `TavernMelissaRoom` / `room_search`
- Gate: booklet search succeeds only when `effective_player_exploration() > 120`.
- Found object: `melissa_drawings_booklet_001`
- Item source of truth: `MelissaBookletItem` in `game/Items/Resources/MelissaBookletItem.rpy`
- Search result: the event adds `melissa_drawings_booklet_001` to `TavernMelissaRoomRoom.game_items`, advances the thread, and shows a text hyperlink to select the found object.
- Object display: `TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001")` shows the item picture, description, and item-owned action menu.
- Search result flow:
  - `take`: call the existing `Take` procedure, moving the item from room to player inventory; set `Melissa.var["drawings_booklet_taken"] = 1`.
  - `open`: show first booklet page; set `Melissa.var["drawings_booklet_opened"] = 1`; time cost: 5 minutes.
  - `read`: show booklet page sequence; apply player arousal through `player_apply_arousal_trigger("melissa_booklet", 18)`; set `Melissa.var["drawings_booklet_read"] = 1`; time cost: 10 minutes.
  - `leave`: put the booklet back; set `Melissa.var["drawings_booklet_left"] = 1` and `Melissa.var["drawings_spy_option_unlocked"] = 1`.
  - `continue`: close the selected object panel and return to Melissa room actions.
- TODO: `drawings_spy_option_unlocked` should open the later spy/seduction branch from Melissa room logic. That branch must be a proper event/thread stage, not a room-label workaround.

## Full TXT Coverage (anti-omission list)
- $menu_f.txt
- AdjustOtkroven.txt
- AmandaAtHomeCode.txt
- DailySetstatdefault.txt
- DressNoShow.txt
- EllonaBirthPrayMenu.txt
- GirlDressSuggest.txt
- GirlsDesc.txt
- GiveBirth.txt
- GiveBirthFinish.txt
- GiveBirthStep2.txt
- HarassDiscussImage.txt
- HarassShowImage.txt
- InitMelissa.txt
- IntAmandaDressChange.txt
- IntLizaDressChange.txt
- IntMelissaDressChange.txt
- IntMelissaTalk.txt
- Intro.txt
- KidsFunctions.txt
- menu_tavernstat.txt
- MorningSickness.txt
- NextDay_TavernDaily.txt
- NextDay.txt
- RelationshipDesc1.txt
- SetTavernServiceLevels.txt
- TavernMain.txt
- TavernShowImage.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event actions included
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.
- [ ] In active development uses thead/event engine system
