# Tavern + Shops Test Plan

## Scope
- Tavern daily event queue and dispatch.
- Location picture update after navigation jump.
- Dialog actions in:
  - Grocery (`Eddie`/`Becky`)
  - Wine shop (`Clara`/`Alber`)
  - Tailor (`Irma`)
  - Carpenter (`Draupnir`)
- Time-turn rule: **4 actions per time slot**.

## In-Game Entry
1. Start game.
2. Press `TR` (top row) to open `DebugTestRoom`.

## Event Queue Checks
1. In `DebugTestRoom` choose:
   - `Показать очередь событий (все слоты дня)`
2. Expected:
   - message shows slot `10` and slots `0..4`
   - each slot prints event list or `<empty>`
   - same list is logged to Ren'Py log (`DBG day queue slot ...`)

3. Then choose:
   - `Показать и запустить 1 таверн-событие`
4. Expected:
   - before/after counters change (`cur` or `mandatory` decrements)
   - event text is shown when mapped event handler returns text

## Shop Dialog + Picture Checks
1. In `DebugTestRoom` choose:
   - `Проверка shop flow (dialog + images)`
2. Expected:
   - `PASS` lines for NPC presence + talk-row + talk label:
     - Grocery morning: `IntEddieTalk`
     - Grocery day: `IntBeckyTalk`
     - Wine morning: `IntClaraTalk`
     - Wine day: `IntAlberTalk`
     - Tailor: `IntIrmaTalk`
     - Carpenter: `IntDraupnirTalk`
   - image presence checks for all 4 locations

3. Manual room checks:
   - `Тест: продуктовая лавка (утро)`
   - `Тест: винный погребок (утро)`
   - `Тест: лавка Ирмы`
   - `Тест: мастерская Драупнира`
4. Expected:
   - location image in left picture area updates per room
   - right panel `In this location` has correct NPC
   - clicking NPC opens dialog actions (`Поговорить`)

## Time-Turn Check (4 actions)
1. Stay outside `Intro`.
2. Perform 4 counted actions (talk/interaction/travel).
3. Expected:
   - slot advances after the 4th action
   - day rollover still works at last slot

## Fixed Issues In This Pass
- Carpenter NPC now wired into UI dialog flow.
- Added `IntDraupnirTalk` label and reused in carpenter menu.
- MarketPlace text tag typo fixed (`{/i}>` -> `{/i}`).
- Added debug labels for full-day event queue and shop flow checks.
- Time-turn rule updated to 4 actions per slot.

## Known Risks / Follow-up
- Python helper `DisplayTavernEventShort(...)` returns code/short value; full story text comes from script label `display_tavern_event_short`.
- If specific image files are missing in `images/...`, picture checks for that location will fail even when logic is correct.
