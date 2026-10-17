# Stick-pose reference library

Sixteen hand-authored 2D joint guides, with four suggested poses per NPC.
Every pose is separate and editable. These are construction references for
new artwork, rather than finished character sprites or rigged 3D models.

## Files

- `png/`: sixteen transparent 640 × 800 skeleton images.
- `svg/`: matching editable vector skeletons on the same canvas.
- `poses.json`: named joint coordinates, head-facing direction, view and pose notes.
- `pose_library_preview.jpg`: a contact sheet of all sixteen guides.
- `manifest.json`: exact filenames and hashes.

Solid dark bones identify the near limbs. Dashed blue-gray bones identify the
far limbs. Orange marks the hip bar and the head-facing direction. The foot
chains explicitly include ankle, heel and toe points. Near/far describe the
intended depth order, not the character's anatomical left/right.

## Use

Pick one PNG as a pose reference while supplying the NPC's established face,
body and clothing references separately. The skeleton specifies joint layout;
it does not encode the NPC's body measurements, garment silhouette or hands.
Each pose has a suggested NPC assignment; any guide may be reused for another
character when the scene requires it.

Open an SVG in a vector editor, or change coordinates in `poses.json` and run:

```sh
python3 tools/render_stick_pose_library.py
```

For the standalone ZIP, run `python3 render_stick_pose_library.py --library .`.
Rendering requires Pillow. SVGs and PNGs can be opened without Python.

This is a custom guide format, not an OpenPose JSON export or motion-capture
dataset. The poses are manual 2D constructions, with no claim of anatomical
or biomechanical validation. Foreshortening and contact surfaces still need
checking in the final character drawing. Runtime sprites remain separate in
`game/images/npc_sprites/` and `game/images/npc_card_game/`.
