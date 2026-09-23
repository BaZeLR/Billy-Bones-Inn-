# Amanda: upstairs flirt variant

Implemented 2026-09-23 in the existing
`story_amanda_tavern_seduction_0` event label in
`game/NPC/Girls/Amanda/AmandaLegareStreetEvents.rpy`.

## Scope and ownership

- KEEP: `AmandaTavernSeductionEvent` owns availability and cadence; unchanged.
- KEEP: the existing event label owns dialogue, illustrations, native menus,
  the two variants, and return to its caller.
- KEEP: Amanda's existing wardrobe/intimacy methods and the existing common
  begin/finish procedures own clothing, counters, and consequences.
- No new thread, event class, dispatcher, refresh label, or saved state mirror.
- No other event labels in this file changed.

The existing upstairs option still requires friendship >= 12,
corruption >= 35, non-virgin state, `date_intimacy_available()`, and
`player.intimacy.can_cum()`. The existing event's schedule and 0.35 availability
probability are unchanged. After the player chooses upstairs, one
`procedural_random("amanda_tavern_seduction_bedroom") < 0.5` check chooses the
new bedroom variant; otherwise the original window variant plays.
This is a variant split, not a replacement of the event's availability chance.

## Supplied text and existing artwork

The new dialogue preserves the user's supplied wording, spelling, and order.
No new graphic narration or artwork was generated. Assets are under
`game/images/amanda/Room/flirtUpstares/`.

| Beat | Existing image |
| --- | --- |
| Follow upstairs | Retain preceding portrait |
| Greeting / kiss | `close up.jpg` |
| Move toward the bed | `onbed.jpg` |
| Clothing removal | `Boobs.png` |
| Bed close-up | `onbedCloseUp.jpg` |
| Approach | Retain bed close-up |
| Overhead view | `beforeSex.jpg` |

Each of the seven supplied introductory paragraphs has a native `Далее`
button. The supplied final paragraph leads to the existing finish menu.
The common cleanup retains its existing image/text, with only the user's
supplied short ending appended for the bedroom variant and another `Далее`.
The new variant also has an explicit `Завершить` before returning.

The original window illustration was copied byte-for-byte from
`game/NPC/Girls/Amanda/flirts_new room.jpg` into this folder and its two
references updated. The original file and all other pictures were preserved.

Both variants converge on the same counter/consequence calls, once per
encounter. Existing inside/outside choices and pregnancy processing remain
owned by `Amanda.player_cum`, not duplicated in the new branch. The shared
finish procedure restores day clothing and charges its existing 40 minutes.
The existing native scene context restores the caller's picture, text, and
menu; room navigation is not exposed inside the event.

## Verification

2026-09-23, installed Ren'Py **8.5.2.26010301**, copied scripts and temporary
save directory; live playthrough saves were not loaded or modified by testing.

- `python -m pytest tests/test_amanda_upstairs_flirt.py tests/test_amanda_object_source.py::test_amanda_tavern_seduction_upstairs_stays_in_the_event_and_uses_owned_sex_state tests/test_media_alias_free_source.py -q`: **7 passed**.
- `python tools/external_amanda_upstairs_flirt_test.py --keep-temp`:
  compile exit 0, lint exit 0; **8 native cases, 140 assertions passed**.
- Native cases cover both variants x both finishes, plus four blocked
  eligibility conditions. They check paragraph/image order, single visible
  text, explicit continuation, wardrobe transitions, single-count results,
  recorded consequence target, original context restoration, and time cost.
- Lint reports three unreachable-statement notices for the injected test
  suite/testcase declarations only, not production scene code.
- Evidence directory:
  `C:/Users/blank/AppData/Local/Temp/tractir_amanda_flirt_xou7jdog/TractirExternalRenovationsProject/`
  (`amanda-flirt-compile.log`, `amanda-flirt-lint.log`, `amanda-flirt-test.log`).

Native syntax was checked against the official
[menu documentation](https://www.renpy.org/doc/html/menus.html),
[label/call documentation](https://www.renpy.org/doc/html/label.html), and
[automated-test documentation](https://www.renpy.org/doc/html/testcases.html),
then validated with the installed SDK version above.

These checks cover this event change, not the entire game's story flow.
