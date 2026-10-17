# NPC sprite library v1 validation

Checked on 2026-10-17 against main commit
`fbfd19929890dc42acad864b206a94572fcc8f8f`.

## Delivery status

160 individual RGBA PNGs: all 80 expressions, all 40 gestures and all 40 body
poses. Every entry in the exact reference checklist is delivered.
The completion update adds the five previously unavailable poses:

- Amanda: boudoir kneeling, lying_front.
- Clarissa (`clara`): boudoir lying_side, with the complete supporting arm.
- Sandra: boudoir lying_front, over_shoulder.

The manifest has `complete: true` and an empty `missing` list. All new frames
have individual artwork; there are no duplicate substitutes or placeholders.

## Passed checks

- Ren'Py **8.5.2.26010301**: project `compile` command completed with exit 0.
- Focused pytest run: **26 passed, 160 image subtests passed**. Modules:
  `test_npc_sprite_library.py`, `test_main_ui_interaction_ownership.py`,
  `test_main_ui_saved_menu_context.py`.
- All 160 PNG hashes, dimensions, RGBA mode, transparent borders and image
  paths match the manifest. Atlas boundary residue was removed before export.
- All 80 expression side images and all 40 body overlays are declared.
- Visual inspection of the four labeled catalogs and corrected cutouts.
- Python compilation of the offline builder and asset test module.
- `git diff --check`.

## Existing findings and limits

The earlier broader UI check found two source-expectation failures, both
reproduced using the untouched base before restoring the sprite integration.
The UI source is unchanged by this image-completion update:

- `test_player_inventory_and_fixed_target_social_panels_stay_inside_main_ui`
  expects an older inventory-mode conditional; the base already includes the
  `not dialogue` guard.
- `test_intro_uses_its_authored_full_text_and_single_start_action` expects an
  assignment absent from the base `Intro.rpy`.

The SDK lint command completed, but reports legacy images unavailable in this
sparse checkout. It reported no diagnostics for the new sprite files or
`NPCSprite*` modules. This is not a clean full-project lint result.

No interactive game play-through or save/load test was performed. Scene authors
must place furniture-free seated/reclining poses to match their scene furniture.
The new voice aliases opt into portraits; existing story lines are not rewritten.
