# Logical Runtime Test Standard

Tractir now has a FamilyLife-style logic test harness in `tools/runtime_logic_tests.py`.

It is pure Python and stays outside the Ren'Py `game/` tree. Run it from the project root:

```powershell
python tools/runtime_logic_tests.py
```

The same checks are wired into `pytest`, matching the template convention:

```powershell
python -m pytest
```

The test script checks source structure without adding labels, screens, or developer UI to the shipped game:

- story thread and event construction from `StoryEventRuntime.rpy`
- thread blueprint metadata: level, person, subname, generated name, constructor type
- event tuple field shape: target, day, hour, delay, probability, requirements, conditions, item, location, action, priority
- event target labels and location/action bindings
- competing location/action/priority slots
- recipe outputs and ingredient item ids against the registered `GameItem` ids
- crafting menu structure: unavailable recipes stay out of the create-item menu
- Amanda, Clarissa, Melissa, and Sandra talk/flirt score tables
- projection, player-condition, narrator, and thread-board hooks
- narrator side-image asset

This is different from Ren'Py lint. Lint only proves the script compiles. These checks prove that the sandbox logic can actually evaluate the current event graph without broken labels, invalid thread state, missing schedule hooks, or action gates that crash at runtime.

## Expected Use

When adding or rewriting a story thread:

1. Add the thread through the existing event/thread classes.
2. Keep every event target as a real Ren'Py label.
3. Keep location/action names explicit so the UI can find the event.
4. Run Ren'Py lint.
5. Run `python tools/runtime_logic_tests.py` or `python -m pytest`.
6. Fix any failure before adding more events on top.

Warnings are not always fatal. They mark ambiguity that can create repeated or hidden content, especially competing events with the same location, action, and priority.

## Why This Matters

The project already has OOP blueprints for events, threads, people, schedules, relationships, and action builders. The test harness is built around those blueprints. It is meant to stop accidental breakage while keeping the content readable and editable as labels, vscenes, menus, and thread definitions.
