# Amanda card-game poses

Three additional, individually exported Amanda sprites for a playful private
strip-card scene. Her blonde braided updo, blue eyes, petite adult build and
ivory homewear follow the existing character references.

| State | Acting and wardrobe | Ren'Py image |
| --- | --- | --- |
| `tease` | Seated with crossed legs, cards raised, one chemise shoulder ribbon loosened | `npc_amanda cards tease` |
| `forfeit` | Standing with the removed chemise in one hand, wearing matching ivory camisole and briefs | `npc_amanda cards forfeit` |
| `challenge` | Seated and leaning forward to play a card, in the same camisole and briefs | `npc_amanda cards challenge` |

See [the actual export preview](previews/amanda_cards.jpg) on light and dark
backgrounds. These three poses extend the 160-item library; the base checklist
and its manifest retain their original count. This extension currently covers
Amanda. Each asset is a complete static image with its own facial acting.

## Runtime use

The PNGs are in `game/images/npc_card_game/v1/amanda/`, with a separate manifest
recording dimensions, visible bounds, image names, source hashes and export
hashes. Each file is RGBA, 640×800, with a baseline at y=768. Seated figures have
a smaller visible height than the standing figure. No image processing is
needed in Ren'Py.

`game/Utilities/General/NPC/NPCSpriteCardGame.rpy` registers the three body
images and three media-panel overlays. It uses the base library's existing
`npc_sprite_body` transform and dialogue portraits:

```renpy
show npc_amanda cards tease at npc_sprite_body
npc_amanda_voice playful "Are you watching the cards?"
show npc_amanda cards forfeit at npc_sprite_body
npc_amanda_voice wink "One round. Don't get too confident."
show npc_amanda cards challenge at npc_sprite_body
npc_amanda_voice smiling "Your move."
hide npc_amanda
```

For this project's `main_ui` media panel, set the existing scene overlay in
the scene's owning label:

```renpy
$ previous_card_overlay = scene_runtime.picture_overlay
$ scene_runtime.picture_overlay = "npc_overlay_amanda_cards_tease"
# Continue the existing scene/background and its dialogue here.
$ scene_runtime.picture_overlay = "npc_overlay_amanda_cards_forfeit"
# Later in the same authored scene:
$ scene_runtime.picture_overlay = "npc_overlay_amanda_cards_challenge"
# Restore at scene exit.
$ scene_runtime.picture_overlay = previous_card_overlay
```

The overlay canvas is 1536×1024, placing the sprite at (448, 224). For seated
poses, adjust scene placement to the chosen chair or sofa. The cutouts contain
no furniture or ground shadow. Their card backs are decorative artwork;
specific ranks, hands, rules and round results remain the card game's UI and
story data. This addition supplies assets and declarations, without adding a
card minigame or changing relationship state.

## Authoring records

[generation_prompts.json](generation_prompts.json) retains the exact prompts,
selected source filenames and canonical reference roles. The artwork was
created with the built-in image generation tool. The runtime PNGs are the
selected, alpha-cleaned and normalized exports.

To rebuild from separately retained source images, install Pillow, numpy and
scipy and create a JSON map such as:

```json
{"sprites": [
  {"npc_id": "amanda", "state": "tease", "source": "sources/tease.png", "max_height": 610},
  {"npc_id": "amanda", "state": "forfeit", "source": "sources/forfeit.png", "max_height": 736},
  {"npc_id": "amanda", "state": "challenge", "source": "sources/challenge.png", "max_height": 610}
]}
```

```powershell
py tools/build_npc_card_game_sprites.py --source-map path/to/card_sources.json
```

The builder cleans near-invisible alpha residue, removes isolated background
specks, preserves edge antialiasing and normalizes the individual canvases. It
does not redraw faces, anatomy or clothing, or rebuild the base library.

## Validation

The three exported files passed checks for unique hashes, manifest SHA-256
matches, RGBA mode, 640×800 canvases, transparent borders, zero RGB at zero
alpha, recorded visible bounds, three ordinary image declarations and three
media-panel overlay declarations. The actual exports were visually inspected
on light and dark backgrounds.

Ren'Py 8.5.2 compilation passed with the new declarations. The existing focused
suite passed: 26 tests and 160 base-library image subtests. It was run with:

```powershell
py -m pytest tests/test_npc_sprite_library.py tests/test_main_ui_interaction_ownership.py tests/test_main_ui_saved_menu_context.py -q
```

Full interactive gameplay has not been tested. Automated checks verify files
and image bindings; illustration quality is reviewed visually and is not
certified by those checks. Existing broader lint/test limitations remain
documented in the base library's [validation report](../VALIDATION.md).
