# Main UI Instructions

This document defines the required behavior for the main gameplay UI.

## Source of Truth

- UI layout/spec source of truth: `devdocs/mainUI_screen_template.txt`.
- Runtime implementation files:
  - `game/Inn/my_layouts/main_layout.rpy`
  - `game/Inn/my_layouts/layout_logic.rpy`

## Rendering Contract

- Use a single gameplay UI screen: `screen main_ui`.
- Do not show duplicate gameplay overlays with the same functionality.
- Keep strict split:
  - picture viewport renders location/scene images only;
  - text window renders narration/dialog text only;
  - right column renders controls/status/actions/navigation.

## Navigation/Actions Contract

- Navigation click must update together:
  - current location state;
  - background/picture;
  - room description;
  - available actions/navigation.
- Character names in "In this location" open interaction mode (`UI_mode = "dialog"`), not character card mode.
- Character card mode opens from `C` control button.
- Hide location/character actions when conditions are not met; do not show invalid placeholders.

## Mode Contract

- Supported modes: `scene`, `dialog`, `char`, `tavern`, `mc`.
- `scene`:
  - location image and location text active.
- `dialog`:
  - selected NPC interaction actions in actions/navigation panel.
- `char`:
  - character card/report shown in picture area.
- `tavern`:
  - tavern report shown in picture area.
- `mc`:
  - player report shown in picture area.

## Intro Contract

- Intro is text-only in picture area until pressing "Приступить к управлению трактиром".
- No polling timer loops (`pause(0.1)+jump`) for intro wait flow.
- Start-managing action transitions to normal gameplay state (`TavernMain`) and normal scene rendering.

## State/Runtime Rules

- Use `default`/`store` state, avoid plain implicit globals.
- Avoid `globals()` in UI flow where store helpers are available.
- Do not use Python `renpy.call/renpy.jump` in python blocks.
- Keep flow in script labels (`call`, `jump`, `call expression ... pass (...)`).

## Constraints

- Do not change story text or gameplay mechanics without explicit instruction.
- Preserve current main UI layout unless explicit redesign is requested.
