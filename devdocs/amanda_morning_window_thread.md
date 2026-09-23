# Amanda: morning window visits

Implemented 2026-09-23 from the user's four-scene request. This replaces the
old repeatable morning-window outcome, not Amanda's unrelated night, dance,
work, or upstairs-flirt events. No pictures were generated or overwritten.

## Authority and lifecycle

- `amandaMorningWindowEpisode`: existing `LThreadInfo` key retained, now four
  one-time stages. `num`, `done`, `day`, `aborted`, and `completed` remain its
  only progress authority. No parallel NPC stage flags.
- `AmandaMorningWindowEpisodeEvent(stage)`: typed event definition, common
  eligibility with per-stage target/day delta. The existing class name remains
  available for saved objects.
- `AmandaMorningWindowEvents.rpy`: authored labels own text, native menus,
  illustrations, consequences, advancement, and departure to the kitchen.
- `AmandaMorningWindowArrival`: returnable procedure for the repeated
  arrival/window/turn-back sequence. Not a dispatcher or generated menu.
- The obsolete `tavern_amanda_morning_window_outcome` decision function and
  its former repeatable scene were removed. No other room actions were removed.

Prerequisites: attic fall completed (`Amanda.attic_busted()`), actual clock
**06:00–11:59**, Amanda's schedule puts her in her room, she is not sick,
entry has not been blocked for the day, breakfast is not completed, and she
is not on the current active breakfast attendance list.

The event no longer requires a random `sleepy` issue: ordinary scheduled
presence in her room can qualify too. Her schedule itself is unchanged.
Thus a one-day delay is a minimum gap, not a guarantee she is available the
very next day. Stages 2–4 require `current_game_day >= thread.day + 1`.

The normal room-entry gate runs the event. The existing no-knock and breakfast
Wake routes enter that same room when the thread has an available stage;
otherwise their existing generic behavior remains. Events cannot be selected
out of order, repeated after advancement, or played after thread abortion or
completion.

## Stages and pictures

All five scene images already exist in
`game/images/amanda/Room/Masturbation/`. Room catalog references were updated
for the files the user moved there; they were not copied back to the old path.

| Stage | Main picture | Supplied story beat / consequence |
| --- | --- | --- |
| 1 (`num=0`) | `amanda_bedroom_004.jpeg` | Knock remark, window, breakfast apology, leave |
| 2 (`num=1`) | `amanda_bedroom_003.jpeg` | Finger/secret remark, leave |
| 3 (`num=2`) | `amanda_bedroom_002.jpeg` | Teasing conversation, leave; activate morning-visit thread |
| 4 (`num=3`) | `amanda_bedroom_001.jpeg`, then `amanda_bedroomAPI.webp` | Show/refuse menu; conditional booklet and clients remarks; leave |

The user's English text was divided into scene paragraphs and choices with
light spelling cleanup. The existing neighboring-yard text is reused for the
window beat. No new graphic narrative was added. Every new paragraph is held
by a native continuation/choice button, with no room-navigation panel exposed.

`Melissa.drawings_found` gates the booklet exchange. The clients argument
matches the existing refusal thresholds: `notallow` below 45 corruption, or
no instruction below 30. This does not change her work instructions. It adds
one anger point through the existing NPC method, enabling the ordinary apology
option without imposing another friendship loss.

Only the fourth visit adds **one corruption point**, once. Stages 2 and 3 add
10 MC arousal on departure; they do not record a sex act or a finish. All four
visits retain the prior event's 20-minute cost, restore daytime clothing,
resolve the morning absence issue, and return to the kitchen. The no-knock
route retains its existing additional five-minute movement cost.

The new sequence does not set `attic_window_favor_stage` and therefore does
not open the old immediate kitchen-favor outcome. Previously pending favors
from older saves are not erased.

## New morning-visit thread and pending author choices

`amandaMorningWood` is activated and dated on completion of visit 3. Its
single introductory MC-room event uses the existing `morning` hook after the
daily report, **06:00–07:59**, at least one day later, unless Amanda is sick.
It presents only the user's supplied introductory sentence and existing MC
wake-up background, then returns to the morning routine. No further dialogue
or later stages were invented.

Two optional clarification questions were sent during implementation and
have not yet been answered:

1. The fourth scene's 50/50 "listen" point is provisionally mapped to Amanda's
   existing **rebellion** score: -1 or +1, equally likely. Friendship and trust
   are not silently substituted. Confirm or change this mapping with the author.
2. The morning-visit thread currently includes the single introductory sentence
   rather than an expanded MC-room scene. Confirm whether only activation was
   desired, or additional authored material will be supplied.

## Validation

- Focused source suite: **13 passed** (room ownership, event declarations,
  moved assets, unchanged upstairs-flirt checks).
- Installed Ren'Py **8.5.2.26010301**: compile exit 0; lint exit 0 (only
  unreachable test-declaration notices in the injected test file).
- Native UI suite: **17 cases, 297 assertions passed**, plus Python assertions
  for time boundaries, prerequisites, delay, abortion/completion, old one-step
  definition rebinding, and serialization of stage/day/done state.
- Native paths cover direct room entry, no-knock entry, breakfast Wake,
  all Show/refuse x booklet x argument combinations, kitchen restoration,
  exact image order, a single displayed paragraph, no repeated corruption gain,
  and the morning-thread unlock/next-day gate.
- Tests use copied scripts and a temporary save directory, not the live saves.
  Object serialization was tested; a full live-playthrough save/load was not.
- Evidence:
  `C:/Users/blank/AppData/Local/Temp/tractir_amanda_window_2f6kv6l2/TractirExternalRenovationsProject/`
  (`amanda-window-compile.log`, `amanda-window-lint.log`, `amanda-window-test.log`).

The new definitions are rebound by the existing thread initialization and
after-load path. No separate migration or second initialization mechanism was
introduced. Restart the game before loading an existing morning checkpoint
to use the new scripts.
