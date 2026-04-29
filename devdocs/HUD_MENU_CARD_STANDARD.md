# HUD, Menu, Card Standard

FamilyLife reference pattern:

- `status.rpy` keeps player stats, shortcuts, locate, inventory, and thread board access in one persistent HUD.
- Stats are not loose text everywhere; repeated rows use small helper screens like `statusItem`, `statusRel`, and popup screens for explanations.
- Inventory is a modal overlay with a dark click-to-close background, item grid, selected/hover states, and a detail pane.
- Locate and thread board are opened from the HUD and use the same data paths as room/location logic.
- Thread board uses color-coded status boxes, hover detail screens, and a compact top-level person selector.

Tractir application:

- Preserve the existing right panel and left card area.
- Keep HUD commands as right-panel buttons, but route them through reusable `main_ui_hud_button`.
- Keep location/time/player resources as reusable `main_ui_status_item` rows.
- Use stable shortcuts:
  - `L` opens `people_locate_overlay`.
  - `T` opens `story_thread_board`.
  - `I` toggles inventory sections.
  - `P` opens the player card.
- Player card, inventory section views, locate, time, tavern report, and story board must be screens/states called from the HUD, not duplicated as room-specific menus.
- New stats should be added as `main_ui_status_item` or card stat row helpers, not raw one-off text blocks.
