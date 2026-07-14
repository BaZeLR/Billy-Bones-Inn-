# Event/Thread Instruction Index

Use this folder as the first guide for writing or reviewing event/thread code.

Start from `devdocs/README.md` for the full documentation map.

This folder is the current blueprint. Do not use older early-stage devdocs to
justify alternate UI/event approaches, compatibility adapters, fallback layers,
or TXT-parity wrappers.

## Read Order

1. `STORY_LABEL_EVENT_FLOW_STANDARD.md`
   - Event tuples own availability.
   - Story labels own actual scene text, `vscene` media, menus, branch consequences, time cost, return flow, and thread progression.

2. `ENGINE_STYLE_EVENT_THREAD_STANDARD.md`
   - Thread rows use the existing `LThreadData`, `RThreadData`, and `UThreadData` classes.
   - Target labels advance, complete, or abort the active thread directly.

3. `FAMILY_LIFE_HUD_MENU_PATTERN.md`
   - Family Life reference pattern for keeping HUD visible while event choices remain attached to the active scene.
   - Tractir event choices must appear in the active event/action area, not in detached overlays or refresh/apply paths.

4. `../implementation_models/EVENT_THREAD_MODEL_AND_TEMPLATE.md`
   - Current implementation model and tuple/template expectations.

## Non-Negotiable Rules

- Keep the right-side HUD persistent.
- Use the Family Life pattern: event labels own `vscene`, text, classic Ren'Py
  `menu:`, consequences, time cost, and direct thread progression.
- Screens display HUD/menu placement/cards/debug views only; screens do not own
  event logic.
- Do not duplicate event conditions inside labels when the event tuple owns them.
- Do not use refresh, rebuild, apply, renew, dispatcher, or wrapper labels for authored event choices.
- Do not hide player choices behind Python handler methods.
- Use `vscene` for authored event media.
- Use branch sublabels only when they are real authored branches with text, media, consequences, or time cost.
- Update thread state only at the real outcome point: `thread.advance()`, `thread.complete()`, or `thread.abort()`.
