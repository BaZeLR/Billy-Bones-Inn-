# Tractir Devdocs Index

This file is the documentation entry point.

The current architecture is class-owned and label-driven:

- Rooms own room identity, description, media, navigation, room objects, room state, and room-only actions.
- Game objects and game items own their own descriptions, pictures, menus, and action labels.
- NPC class instances own NPC state, schedules, location, relationship, daily interaction counters, and talk/event state.
- Events and threads own availability and progression. Event labels own authored text, `vscene` media, menus, consequences, time cost, and return flow.
- Screens display UI only. They do not own gameplay flow or story consequences.

Do not use old globals, `*Var` dicts, `Friends[...]`, `Talked[...]`, `CurrentLoc[...]`, refresh/rebuild/apply/renew labels, dispatcher layers, handler methods, recursive menu loops, or compatibility fallback systems as implementation models.

## Active Architecture Docs

Use these as implementation authority:

- `project_index.md`
- `implementation_models/IMPLEMENTATION_DASHBOARD.md`
- `implementation_models/ROOM_MODEL_AND_TEMPLATE.md`
- `implementation_models/NPC_MODEL_AND_TEMPLATE.md`
- `implementation_models/EVENT_THREAD_MODEL_AND_TEMPLATE.md`
- `implementation_models/PLAYER_MODEL_AND_TEMPLATE.md`
- `EventThreadInstruction/README.md`
- `EventThreadInstruction/STORY_LABEL_EVENT_FLOW_STANDARD.md`
- `EventThreadInstruction/ENGINE_STYLE_EVENT_THREAD_STANDARD.md`
- `EventThreadInstruction/FAMILY_LIFE_HUD_MENU_PATTERN.md`
- `ACTION_BINDING_MODEL.md`
- `ACTION_ITEM_STANDARD.md`
- `PEOPLE_DATA_INFO_STANDARD.md`
- `HUD_MENU_CARD_STANDARD.md`
- `PROJECT_MAP_AND_DEPENDENCIES.md`
- `RENpy_ENGINE_PROJECT_KNOWLEDGE_BASE.md`

## Reference Only

Historical audits, old port plans, TXT/QSP extraction notes, and `characters/full_logic/*` files are not architecture. Use them only to recover story content, original text, or a past bug note. When they mention old names like `AmandaVar`, `MelissaVar`, `GeorgettVar`, `Friends[...]`, or time slots, port that meaning into the current owner class/event/item/room model.

## Cleanup Rule

If a doc contradicts this index, update it, delete it, or mark it reference-only. Do not add a second parallel standard.
