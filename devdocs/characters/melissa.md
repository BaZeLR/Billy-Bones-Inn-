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

### Corrected lunar / early-intimacy specification (2026-10-03)

**User-approved specification; not a claim that all corrections are implemented.**
This section supersedes the earlier proposed +2/+3 corruption awards, the
no-glove-only Melissa visit restriction, and the early cream-request route.
The scene composition is in [the noise/stove plan](moon_noise_stove_ghost_event_plan.md).
This documentation update changes no gameplay code, saves or authored dialogue.

#### Story ownership and order

Melissa owns the noise continuation. Amanda participates; she does not own or
advance a duplicate version of Melissa's story. Existing thread cursors remain
authoritative; this narrative order is not a request for another master thread.

| Story step | Existing owner | Required outcome |
| --- | --- | --- |
| 1. Bat problem resolved | `melissaBatProblem`; `tavern.renovations` owns the roof | Roof repaired. The original quest opening is eligible on lunar days 14–23. |
| 2. Melissa's thanks | Final authored stage of `melissaBatProblem` | Play thanks before the post-repair continuation; do not replay it monthly. |
| 3. Returning complaints and Sandra's story | `melissaMoonNoise` | Noise returns in a later lunar month on days 14–23. Live virgin listeners hear it; MC does not. Amanda keeps her enjoyment private and does not complain publicly at breakfast. Preserve the attic recheck and Sandra's account. |
| 4. Amanda alone at the stove | `melissaMoonStoveRitual`, stages 0–1 | Ordinary backyard-window action, then unnoticed inspection; Amanda flees from the sound. Glove crafting becomes available after the clue. |
| 5. Both women at the shed | `melissaMoonStoveRitual`, stages 2–3 | On a later night, see both through the window and follow to overhear their conversation. No ambush on this night. |
| 6. Stove ambush | `melissaMoonStoveRitual`, stage 4 | On a later night, hide and wait. Glove branch: Amanda's individual touch and Melissa's individual climax. This outcome must lead into Melissa's night visits, not exclude them. No glove remains a valid alternative outcome. |

After Sandra's story, `melissaMoonNoiseRepeat` supplies one private corridor
reminder per lunar month on days 14–23: Melissa and Amanda approach MC worried,
messy-haired and wearing dishevelled nightshirts. Its ending finishes only the
reminder. It queues no extra breakfast, resets no investigation or stove stage,
and does not resolve the curse. The one-time stove encounter is not replayed.

The three-night stove windows are 14–21 for the first clue/check, 15–22 for
the second clue/conversation, and 16–23 for waiting. Retain at least one absolute
day after the actual first check and another after the actual conversation.
Missed encounters stay pending; completed scenes and save history stay earned.

#### Corruption chart: one point per completed step

Melissa's current new-game corruption is 3. The approved reward is **+1**, not
+2 or +3, for each completed early-intimacy progression step below. This is a
reward chart, not a list of automatic unlock thresholds or a guarantee that
every step has already been coded in this order.

| Completed Melissa milestone | Corruption award | Progression rule |
| --- | ---: | --- |
| Her individual glove encounter | +1 | Resolve once; the completed outcome leads into her night visits. |
| Accepted protection visit / first sleepover | +1 | Seeking protection starts the gradual visit progression, not advanced actions. |
| First playful morning tickling | +1 | A later sleepy-morning opportunity; illness is not an intimacy shortcut. |
| She asks to look at MC | +1 | Separate accepted step. |
| Further tickling and mutual teasing | +1 | Separate later encounter, not the first morning repeated for rewards. |
| She asks to touch MC | +1 | Separate accepted step. |
| First completed handjob milestone | +1 | Only the completed interaction earns this point. |
| She requests touching and receives oral stimulation | +1 | Her own requested/accepted progression step. |
| Reciprocal oral milestone | +1 | A possible returning favour, not an automatic obligation. |
| Accepted new-clothing progression milestone | +1 | Apply through the existing outfit interaction, not a menu read or duplicate reward. |
| Each completed Clarissa night visit involving Melissa | +1 additional | Each real completed visit supplies its own point, subject to the same early cap. |

Roof repair, thanks, complaints, reminders and observation alone are not new
sexual-corruption rewards. Successful personal progression also improves
openness and friendship as requested, but their per-step amounts have not been
approved here; do not invent another numerical reward chart. Friendship with
MC must reflect an interaction she credits to MC, not an anonymous encounter
she attributes to Ollie. Clarissa-only interactions do not automatically award
friendship with MC.

**Early-phase corruption ceiling: 20.** All Melissa corruption gains during
these stages, including Clarissa's additional visit points, stop at that ceiling.
Friendship, trust, comfort and openness remain separate values. Do not change
the shared Girl ceiling to 20, cap other characters, lower an already-earned
score in an older save, or maintain a second Melissa corruption counter.
Re-entering a menu, loading a save, refusing, or presenting an already-completed
event earns nothing; a genuinely separate eligible visit is not a UI replay.

#### Later cream / anal gate

Melissa asks about the cream **only after Clarissa's cure and the start of the
anal progression**. Merely reaching 20 corruption, buying an outfit or waiting
28 days after bat completion does not unlock that request. Cure and the anal
introduction must be verified on their existing story owners, not invented
parallel flags. Do not make Clarissa's cure depend on Melissa's later request.

The player must obtain a real plug as part of the later preparation. The current
item is `blackwood_smooth_plug_001`, obtainable from Robin's abandoned-camp chest
in `story_robin_blackwood_camp_loot_0`; player inventory owns possession. Cream
and plug possession do not themselves mean treatment or a later encounter has
occurred. Progression beyond the early ceiling belongs to that later phase;
its further reward schedule is not specified by this early chart.

#### Protection, comfort and public versus team behaviour

Melissa prioritizes feeling protected and comfortable. Reliable care, fulfilled
promises and the existing derived `Melissa.comfort` should support willingness
to cooperate, tease and flirt. Corruption is sexual familiarity, not obedience,
trust or safety; high corruption must not bypass her story gates, refusal or
current condition. Keep one owner for each value and derive world-state needs
from existing repair, provision and household owners.

| Context | Behaviour / clothing rule |
| --- | --- |
| Private with MC | Use her relationship with MC, comfort, protection, current condition and completed personal stages. Private teasing is not permission for a public scene. |
| Trusted tavern team | Evaluate the actual participants and staff-only context. Comfort with MC does not imply identical willingness with every team member. |
| Public / customers / strangers | Separate context conditions govern public clothing, flirting and interaction. A customer-facing tavern hall is public even though it is inside the tavern building. |

Use the same canonical Melissa stats with different context conditions; do not
create public/private corruption copies. Buying clothing, accepting it, wearing
it privately, and agreeing to wear it publicly are distinct decisions. A dress
purchase does not automatically unlock customer behaviour or public exposure.
The **general dress-buying/reward table remains a separate requested audit**;
this Melissa-specific +1 milestone does not establish reward rates for every
garment or other NPC. Preserve existing clothing text pending that audit.

#### Current-code discrepancies to address separately

The preceding rules are the corrected target specification. The last code
audit found these remaining differences, not fixes delivered by this update:

- `melissaMoonProtection` is still restricted to `no_glove`; the glove outcome
  does not yet supply the requested introduction, and courtship can begin
  without completing the stove encounter.
- The stove outcome currently awards openness but no corruption; morning
  stages mostly award openness/friendship, with corruption only at the handjob
  stage. Later courtship awards include +2/+3 and need alignment to +1.
- Melissa's early ceiling of 20 is not enforced by the shared `change_social`.
  Clarissa's existing social/room visits also have differing corruption awards,
  rather than the specified +1 per completed night visit.
- The 28-day cream entry can precede Clarissa's cure; the plug is obtainable but
  is not yet required by Melissa's progression.

Implementation requires a separate code request; preserve completed history and
existing authored content when correcting those owners.

### Household comfort and stock appreciation (2026-09-22)

User correction: these mechanics belong to the EXISTING
`HouseholdEvent_KitchenMelissaPracticalComplaint` kitchen counting event, not a
new talk topic or another reward thread. This is new authored gameplay, not a
reconstruction of a missing TXT stage.
`MelissaInfo` owns Melissa's scores; existing owners retain all world state.

- `Melissa.comfort` is derived, not another saved copy of repairs/problems.
  `comfort_components` exposes the breakdown:
  - no rats: +1 from `werecat_state()["rats_problem_active"] == 0`;
  - room repaired: +1 from `Melissa.bats_repair_complete()`;
  - yard and toilet fixed: +1 each from completed `tavern` backyard renovation;
  - laundry/bathroom: +2 from completed `tavern` shed renovation;
  - weekly cleaning adjustment: saved `Melissa.comfort_cleaning_score`;
  - kitchen interaction adjustment: saved `Melissa.comfort_interaction_score`.
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
- The existing kitchen event keeps its three choices: promise to provide,
  make do with existing supplies, ask what is needed. It counts live stock and
  describes a shortage below 100 total food units (bulk plus deposited pantry
  food), or adequate provision at/above that reserve.
- Confirmed choice effects: make-do costs 1 comfort and 1 trust. For the other
  choices, adequate supplies give +1 comfort/+1 trust; deposited berries,
  mushrooms, honey or boar, or the active bear-meat supply effect give another
  +1/+1. Carried but undeposited food does not count. Trust retains its 0..20
  range. An empty promise with low stock gives no comfort/trust reward.
- "What do you need?" describes only unfinished needs, one paragraph per
  continuation: low provision, rats, room/roof, yard, toilet, this week's room
  cleaning, bath/laundry. Completed repairs disappear from her request.
- The existing room-entry selector permits the counting event with Melissa and
  Sandra present even when scarcity pressure is low. Existing day/slot/room
  deduplication remains; a previously played Amanda/Sandra argument no longer
  masks this event. No new recurring-event queue or scene dispatcher is added.
- Milestone `melissa_full_storeroom`: during this kitchen count, more than 100 food servings
  and at least 50 barrels of wine together. One barrel is 10 internal wine units,
  so the rule is `productnum > 100 and winenum >= 500`.
- The reward is inline in the counting event, before its three choices. The
  existing achievement runtime records completion once; purchases and ordinary
  talk cannot activate it. Sick/sleepy/energy below 35: tired thanks; friendship
  below 8: reserved thanks; friendship at least 8: shy affection; friendship at
  least 11 and corruption at least 20: playful teasing, becoming bolder at
  arousal 35 or higher. No sex-engine/story access gates are bypassed.
- The misplaced `MelissaHousehold.rpy` labels and `melissaStoreroomMilestone`
  thread are removed. The ordinary Melissa talk topic returns to its prior text.
- Native paragraph/continuation menus suppress the room description throughout
  the kitchen event. "Finish conversation" restores the room picture, text and
  navigation, not the ordinary talk menu.
- V94 -> V95 added the original scores. V95 -> V96 adds the interaction adjustment
  and removes the misplaced thread. Already played rewards remain earned; an
  unplayed purchase-queued reward must now be earned in the real kitchen count.
  Inventories, existing scores and other story progress are preserved.
- Renovations and Draupnir order options remain hidden. No renovation request
  conversations are activated by this change.
- Tavern karma is deferred: the user will identify the existing authoritative
  value. Do not create or derive another karma score.

Verification: `tests/test_melissa_household_runtime.py`, existing story-condition
scope tests, and `tools/external_melissa_household_test.py` (isolated Ren'Py copy,
temporary saves; includes native menus, purchases, event completion and migration).
The earlier separate-talk implementation passed tests for the wrong interaction
and was rejected by the user. Verification now targets the actual kitchen event
and the three specified choices, including differing supply/body states.
Corrected version: 149 focused regression checks (31 household behavior cases)
and 21 native Ren'Py 8.5.2 cases passed; compile/lint exited 0. Lint only flags
the injected test statements as unreachable. The actual kitchen menu screenshot
was inspected: Melissa picture, one event paragraph and the three expected
choices; no static room description or room navigation leaks into the event.
A broader check previously also reproduced two
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
