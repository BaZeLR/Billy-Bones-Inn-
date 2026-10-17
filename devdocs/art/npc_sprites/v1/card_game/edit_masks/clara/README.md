# Clarissa pose-aligned editing masks

Four general fabric-region selections for the `forfeit` and `counterbet`
card sprites: an `upper_fabric` and a `lower_fabric` region for each pose.
These are neutral editing masks, with no anatomical artwork or contours.
The regions follow visible purple fabric and preserve foreground occlusions,
light lace and ribbon trim. A fabric-color gate clips the polygon selections.
They do not locate anatomy hidden by opaque clothing.

Each PNG keeps the original **640 × 800** canvas. Place it at **x=0, y=0**
over the matching original sprite, without scaling, trimming or auto-centering.

| Suffix | Contents | Editor use |
| --- | --- | --- |
| `_black_rgba.png` | Black region on transparent surroundings | Separate overlay layer; Ctrl-click the layer thumbnail in Photopea to load its alpha as a selection |
| `_selection.png` | White selected, black preserved, antialiased edges | Import into a layer mask or an editor's selection-mask input; invert only if that editor uses the opposite convention |

After loading a selection, paint or edit on a separate layer above the source.
Keep the source sprite layer intact. Export the edited layer alone on the
same full canvas if a registered overlay is needed.

`alignment_preview.jpg` tints the actual mask pixels cyan over the source.
`regions.json` stores editable polygon coordinates. `manifest.json` records
each source hash, mask hash, bounds and placement. The masks were constructed
with deterministic polygons, not image generation. Regenerate with:

```sh
python3 tools/build_npc_edit_masks.py
```

These authoring files live outside `game/images/`; they are not registered as
runtime images and do not change any existing sprite or Ren'Py declaration.
