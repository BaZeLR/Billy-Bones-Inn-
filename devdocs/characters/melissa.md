# Character Worklist: Мелисса

## Identity
- Canonical id: melissa
- Legacy keys/tokens: melissa, MelissaVar
- Init source: InitMelissa.txt
- Main var store: MelissaVar

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
- Search stage: `story_melissa_bat_problem_5`
- Location/action: `TavernMelissaRoom` / `room_search`
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
