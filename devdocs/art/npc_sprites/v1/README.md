# NPC sprite library v1

Amanda, Clarissa (`clara`), Melissa and Sandra have separate static PNG libraries.
The requested checklist is **20 expressions, 10 body poses and 10 dialogue
gestures per character**. This delivery contains **155 of the 160 requested
PNGs**. All expressions and dialogue gestures are complete. Five body poses
could not be produced after repeated image-generator rejections; they are
explicitly listed in `manifest.json.missing` and have no placeholder images.

| Character | Expressions | Body poses | Gestures | Missing body poses |
| --- | ---: | ---: | ---: | --- |
| Amanda | 20 | 8 | 10 | kneeling, lying_front |
| Clarissa (`clara`) | 20 | 9 | 10 | lying_side (edge repair was blocked) |
| Melissa | 20 | 10 | 10 | None |
| Sandra | 20 | 8 | 10 | lying_front, over_shoulder |

The body categories follow the reference names, with character-specific
posture, gestures and acting. Missing poses are not filled with duplicates.

## Files

`game/images/npc_sprites/v1/<npc>/` contains individual RGBA PNGs:

- `expressions/`: twenty 320×320 dialogue-window portraits.
- `home/`: five 640×800 full-body poses in light, short private homewear.
- `boudoir/`: available 640×800 full-body bedroom poses; see the gaps above.
- `gestures/`: ten 384×512 conversation gesture cutouts.

`manifest.json` records every file, image name, canvas, source crop and SHA-256.
PNG dimensions are export canvases; the source artwork's native detail varies.
These are complete static images. Facial portraits are not interchangeable
face layers for the body poses. Clothing/hair are not separate rig layers.

## Exact reference checklist

Expressions: neutral, happy, smiling, wink, laughing, playful, seductive,
lip_bite, licking_lips, surprised, angry, annoyed, sad, crying, terrified,
disgusted, talking, arguing, drunk, nervous.

Home body poses: standing_neutral, hand_on_hip, arms_crossed, leaning_forward,
sitting_chair.

Boudoir body poses: sitting_legs_crossed, kneeling, lying_front, lying_side,
over_shoulder.

Gestures: invite, tease, think, shy, point, stop, explain, dismiss, welcome,
goodbye.

## Dialogue-window expressions

`NPCSpriteLibrary.rpy` registers ordinary Ren'Py `image side` declarations and
four Character aliases. Names and name colors use the existing NPC data.
The existing story text and NPC state remain owned by their current labels and
classes. Authors opt into the new portraits when writing a line:

```renpy
npc_amanda_voice wink "Вы всё ещё смотрите?"
npc_amanda_voice annoyed "Я вообще-то задала вопрос."
npc_clara_voice playful "Может быть, ему просто нравится наша компания."
npc_melissa_voice nervous "Вы обе нарочно его смущаете?"
npc_sandra_voice smiling "Устройтесь поудобнее."
```

The face changes with the expression attribute. It appears beside the text in
the normal dialogue window, room-event text panel and NPC talk panel. The
portrait does not overlap the text or duplicate the legacy lower-left image.
Existing dialogue lines are not automatically rewritten to the new aliases.

After starting a game, preview all four speakers from the developer console:

```python
renpy.call_in_new_context("npc_sprite_dialogue_demo")
```

## Body and gesture sprites

Ordinary Ren'Py scene authoring:

```renpy
show npc_amanda home hand_on_hip at npc_sprite_body
npc_amanda_voice playful "Здесь гораздо уютнее."
show npc_amanda gestures invite at npc_sprite_body
npc_amanda_voice smiling "Подойдите поближе."
hide npc_amanda
```

The project's active `main_ui` draws its media in a screen. For that flow use
the registered overlay images with the already existing `picture_overlay`
field, so sprites appear inside the media panel:

```renpy
# Inside the scene's owning label; use the existing background for this room.
$ scene_runtime.picture_overlay = "npc_overlay_clara_home_sitting_chair"
vscene "images/tavern/guest_room/lounge_day_lit.png"
npc_clara_voice playful "Я рассчитывала на более интересную беседу."
# Clear at scene exit, or restore the scene owner's previous overlay value.
$ scene_runtime.picture_overlay = ""
```

The overlay canvas matches `BGIMAGE` (1536×1024). Seated/reclining art is
furniture-free, so scene authors choose placement to match the specific bed,
chair or sofa. All body PNGs share a 640×800 canvas and a consistent baseline.
No new action dispatcher, event engine, schedule state or NPC state is added.

Open the light/dark asset browser after starting a game:

```python
renpy.call_in_new_context("npc_sprite_library_preview")
```

## Identity sources

The canonical Git references are Amanda's `amanda_card.jpg`, Melissa's
`melissa_card.jpg`, Sandra's newer copper-haired `sandra_card.jpg`, and
Clarissa's `portrait1.jpg` plus `ClaraData.description` in `InitClara.rpy`.
Amanda retains her petite A-size build, Clarissa her slim B-size build and
grey eyes, Melissa her established olive complexion and natural C-size build,
and Sandra her mature fuller build. No new body measurements are introduced.
The supplied dark-haired example is a category/layout reference only.

## Offline preparation and validation

The game loads the delivered PNGs directly and needs no image-processing
dependencies. The optional builder consumes the original authoring atlases:

```powershell
py -m pip install Pillow numpy scipy
py tools/build_npc_sprite_library.py --source-map path/to/source_map.json
py -m unittest discover -s tests -p test_npc_sprite_library.py -v
```

Source maps contain `amanda`, `clara`, `melissa`, `sandra` keys, each mapping
`expressions`, `home`, `boudoir`, `gestures` to source atlas paths. Source art
is separate from the runtime PNG delivery. The builder extracts silhouettes,
removes near-invisible alpha residue, preserves antialiased edges, normalizes
canvases and regenerates plain image declarations. No generative anatomy or
facial edits are performed during extraction.

The delivery checks account for every reference category and the five declared
gaps, unique file hashes, RGBA transparency, clean canvas borders, declared paths,
all 80 side-image bindings and all 35 available media-panel overlays. Ren'Py
8.5.2 compilation passed. The focused checks passed (26 tests and 155 image
subtests). Full in-game click-through remains unverified; see
[validation results](VALIDATION.md), including the existing test/lint findings.

Ren'Py references: [Side images](https://www.renpy.org/doc/html/side_image.html)
and [image declarations](https://www.renpy.org/doc/html/displaying_images.html).
