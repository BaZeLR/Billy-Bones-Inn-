# NPC card-game poses

Nine additional, individually exported sprites for playful private strip-card
scenes: three poses each for Amanda, Sandra and Melissa. Amanda retains her blonde
braided updo, blue eyes, petite adult build and ivory homewear. Sandra retains
her copper-red hair, green eyes, mature fuller build and burgundy homewear.
Melissa retains her long black hair, olive complexion, established adult
proportions and ivory/olive homewear, with comfortable poses at floor level.

## Amanda

| State | Acting and wardrobe | Ren'Py image |
| --- | --- | --- |
| `tease` | Seated with crossed legs, cards raised, one chemise shoulder ribbon loosened | `npc_amanda cards tease` |
| `forfeit` | Standing with the removed chemise in one hand, wearing matching ivory camisole and briefs | `npc_amanda cards forfeit` |
| `challenge` | Seated and leaning forward to play a card, in the same camisole and briefs | `npc_amanda cards challenge` |

See [Amanda's actual export preview](previews/amanda_cards.jpg).

## Sandra

| State | Acting and wardrobe | Ren'Py image |
| --- | --- | --- |
| `deal` | Standing in a slight forward lean, holding the deck and offering a card, in her burgundy wrap and green sash | `npc_sandra cards deal` |
| `forfeit` | Seated with uncrossed legs, holding her removed wrap, in a burgundy camisole and black briefs | `npc_sandra cards forfeit` |
| `raise` | Standing in three-quarter rear view, looking over her shoulder with cards raised, in the matching camisole and briefs | `npc_sandra cards raise` |

See [Sandra's actual export preview](previews/sandra_cards.jpg).

## Melissa — floor poses

| State | Acting and wardrobe | Ren'Py image |
| --- | --- | --- |
| `floor_deal` | Side-seated with both legs folded to one side, dealing a card in her short ivory babydoll and olive ribbon | `npc_melissa cards floor_deal` |
| `kneel_forfeit` | Kneeling back on folded legs, holding the removed babydoll, in ivory camisole and briefs | `npc_melissa cards kneel_forfeit` |
| `recline_bluff` | Side-reclining with her cheek supported, holding cards, in the existing short-sleeved boudoir chemise | `npc_melissa cards recline_bluff` |

See [Melissa's actual export preview](previews/melissa_cards.jpg). Every pose is
also an individual PNG. Her side-reclining chemise pose is an alternative for
an earlier round; these states are available for scene authors to choose,
rather than an automatic wardrobe progression.

The previews show the runtime PNGs on light and dark backgrounds. These nine poses extend
the 160-item library; the base checklist and its manifest retain their original
count. This extension currently covers Amanda, Sandra and Melissa. Each asset is a
complete static image with its own facial acting.

## Runtime use

The PNGs are in `game/images/npc_card_game/v1/<npc>/`, with a separate manifest
recording dimensions, visible bounds, image names, source hashes and export
hashes. Each file is RGBA, 640×800, with a baseline at y=768. Seated figures have
a smaller visible height than the standing figure. No image processing is
needed in Ren'Py.

`game/Utilities/General/NPC/NPCSpriteCardGame.rpy` registers nine body
images and nine media-panel overlays. It uses the base library's existing
`npc_sprite_body` transform and dialogue portraits:

```renpy
show npc_amanda cards tease at npc_sprite_body
npc_amanda_voice playful "Are you watching the cards?"
show npc_amanda cards forfeit at npc_sprite_body
npc_amanda_voice wink "One round. Don't get too confident."
show npc_amanda cards challenge at npc_sprite_body
npc_amanda_voice smiling "Your move."
hide npc_amanda

show npc_sandra cards deal at npc_sprite_body
npc_sandra_voice playful "Shall I deal another round?"
show npc_sandra cards forfeit at npc_sprite_body
npc_sandra_voice smiling "Enjoy your luck while it lasts."
show npc_sandra cards raise at npc_sprite_body
npc_sandra_voice wink "I raise. Your move."
hide npc_sandra

show npc_melissa cards floor_deal at npc_sprite_body
npc_melissa_voice playful "It's warmer down here. Shall I deal?"
show npc_melissa cards kneel_forfeit at npc_sprite_body
npc_melissa_voice nervous "Just wait until the next hand."
hide npc_melissa
# Alternative relaxed pose for a round in her boudoir chemise:
show npc_melissa cards recline_bluff at npc_sprite_body
npc_melissa_voice smiling "Do you think I'm bluffing?"
hide npc_melissa
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

Sandra's corresponding overlay names are `npc_overlay_sandra_cards_deal`,
`npc_overlay_sandra_cards_forfeit` and `npc_overlay_sandra_cards_raise`.
Melissa's are `npc_overlay_melissa_cards_floor_deal`,
`npc_overlay_melissa_cards_kneel_forfeit` and
`npc_overlay_melissa_cards_recline_bluff`.

### Rug and fireplace placement

Melissa's poses rest on the floor, with no chair-height gap under the pelvis.
They contain no rug, fireplace, floor paint or cast shadow. Place the chosen
sprite over the room and bearskin layers. Each transparent canvas is 640×800,
with the bottom of its visible cutout at y=768; the horizontal reclining art
has more transparent space above it. Align this baseline to the rug and adjust
the scale to match the visible head size of nearby characters and the scene's
perspective.

For an authored scene outside the existing media panel, for example:

```renpy
# With the room and bearskin already shown:
show npc_melissa cards floor_deal:
    anchor (0.5, 1.0)
    pos (720, 790)
```

This places the sprite canvas bottom at y=790 and its visible baseline at
y=758 (790 minus the 32-pixel transparent bottom margin). Move the position to
match the actual rug. Choose one Melissa pose per moment; no rug or room image
is supplied by this sprite extension.

The overlay canvas is 1536×1024, placing the sprite at (448, 224). For seated
poses, adjust scene placement to the chosen chair or sofa. The cutouts contain
no furniture or ground shadow. Their card backs are decorative artwork;
specific ranks, hands, rules and round results remain the card game's UI and
story data. This addition supplies assets and declarations, without adding a
card minigame or changing relationship state.

## Authoring records

[generation_prompts.json](generation_prompts.json) records Amanda's prompts;
[sandra_generation_prompts.json](sandra_generation_prompts.json) records
Sandra's. Both retain selected source filenames and canonical reference roles.
Melissa's prompts and reference poses are in
[melissa_generation_prompts.json](melissa_generation_prompts.json).
The artwork was
created with the built-in image generation tool. The runtime PNGs are the
selected, alpha-cleaned and normalized exports.

To rebuild from separately retained source images, install Pillow, numpy and
scipy and create a JSON map such as:

```json
{"sprites": [
  {"npc_id": "amanda", "state": "tease", "source": "sources/tease.png", "max_height": 610},
  {"npc_id": "amanda", "state": "forfeit", "source": "sources/forfeit.png", "max_height": 736},
  {"npc_id": "amanda", "state": "challenge", "source": "sources/challenge.png", "max_height": 610},
  {"npc_id": "sandra", "state": "deal", "source": "sources/sandra_deal.png", "max_height": 736},
  {"npc_id": "sandra", "state": "forfeit", "source": "sources/sandra_forfeit.png", "max_height": 610},
  {"npc_id": "sandra", "state": "raise", "source": "sources/sandra_raise.png", "max_height": 736},
  {"npc_id": "melissa", "state": "floor_deal", "source": "sources/melissa_floor_deal.png", "max_height": 610},
  {"npc_id": "melissa", "state": "kneel_forfeit", "source": "sources/melissa_kneel_forfeit.png", "max_height": 610},
  {"npc_id": "melissa", "state": "recline_bluff", "source": "sources/melissa_recline_bluff.png", "max_height": 480}
]}
```

```powershell
py tools/build_npc_card_game_sprites.py --source-map path/to/card_sources.json
```

The builder cleans near-invisible alpha residue, removes isolated background
specks, preserves edge antialiasing and normalizes the individual canvases. It
does not redraw faces, anatomy or clothing, or rebuild the base library.

## Validation

The nine exported files passed checks for unique hashes, manifest SHA-256
matches, RGBA mode, 640×800 canvases, transparent borders, zero RGB at zero
alpha, recorded visible bounds, nine ordinary image declarations and nine
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
