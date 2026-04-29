# Thread Board Standard

FamilyLife uses `board.rpy` to make story structure visible:

- rows are threads;
- cells are events inside a thread;
- colors show completed, available, waiting, blocked, aborted, or future events;
- hover panels show conditions, location, time, item, and stat requirements;
- thread labels expose control actions such as highlight, abort, reactivate, and force-enable.

Tractir now has the same concept in `game/Inn/StoryThreadBoard.rpy`.

## Access

Open the board from the right panel with the `Сюжеты` button.

The board is an overlay. It does not replace `main_ui`, room labels, or the action panel.

## Runtime Source

The board reads existing runtime objects:

- `threads`
- `threadData`
- `threadListsByGirl`
- `ThreadInfo.done`
- `ThreadInfo.blocks`
- `ThreadInfo.num`
- `ThreadInfo.completed`
- `ThreadInfo.aborted`
- `ThreadInfo.highlight`
- `Event.conds`
- `ThreadData.conds`

No duplicate story state is created.

## Colors

- green: done/completed
- white: currently available
- yellow: active but waiting for location/time/item/condition
- grey: future
- purple: blocked
- red: aborted

## Controls

Click a thread title to open its control panel:

- toggle highlight
- force enabled
- abort thread
- reactivate thread
- reset thread progress

Hover a thread title to see thread conditions.

Hover an event cell to see event target, location, action key, day/time checks, item requirement, stat requirements, and condition checks.

## Rule

When adding new event content, put real conditions in the thread/event definitions. The board can only be useful when the event rows hold the actual location, action, timing, item, and condition data.

Use flags and counters as chapter labels for the board:

- stage counters show ordered story progress;
- `*_seen` flags show one-time scenes;
- `*_count` values show repeatable scenes;
- `*_last_day` values prevent same-day repeats;
- lock/abort flags should be visible in readiness conditions, not hidden in room code.

This keeps the board useful for writing and debugging instead of becoming only a list of labels.
