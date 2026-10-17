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

## Drawing revision

The latest revision replaces all five Amanda bedroom poses using her existing
standing home sprite as the petite body guide and her A-size description in
`InitAmanda.rpy`. Her seated, kneeling, front-lying, side-lying and over-shoulder
sprites use the smaller chest silhouette and revised body construction.

Sandra's kneeling, front-lying and over-shoulder sprites are replaced to clarify
the folded legs, knees, ankles and feet. The over-shoulder pose now has a
weight-bearing foot planted flat. Face identity, copper hair, green chemise and
burgundy robe are retained.

The selected replacements were inspected at full size before export, followed
by inspection of the final RGBA PNGs on light/dark backgrounds. The
[before/after board](previews/body_corrections.jpg) compares actual exported
files. Automated PNG/hash checks verify file integrity and image bindings;
they do not certify drawn anatomy. This revision changes no Ren'Py source,
image names or canvas dimensions.

## Follow-up: Amanda front-lying torso

The previous front-lying Amanda sprite still had a misplaced rounded contour
on the side of the torso below the near upper arm. That drawing was rejected
and replaced again using her corrected kneeling and existing standing model
references. The new upper torso faces the viewer more clearly, with shallow
chest shaping on the front of the ribs and a flat garment side behind the arm.
Her ivory chemise, character identity and front-lying pose category are kept.
Only this runtime PNG changes in this follow-up; its image name, 640×800 canvas
and Ren'Py bindings remain unchanged.

The [comparison](previews/amanda_torso_correction.jpg) uses the exported PNG
from `4d01fab` and the current export, including light and dark backgrounds.
The focused 26-test run and 160 asset subtests passed after this replacement;
these validate integration and file properties, not the drawing's anatomy.

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
