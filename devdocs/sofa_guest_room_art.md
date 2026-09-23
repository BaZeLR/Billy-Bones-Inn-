# Sofa and guest-room artwork (2026-09-23)

Created with built-in image generation. No existing image was overwritten.
No external/local diffusion service or mechanical upscaler was used.

## Current small-room layout

The first sofa illustration used a large hall and did not fit the existing
small guest lounge. The revision uses `images/amanda/gloryfirst/glory room.png`
as the room reference and the first sofa only as the furniture reference.
The sofa now stands in the small guest room opposite the stone stove, with
a closed door beside the stove leading to the existing glory-hole cubicle.
Original images and the earlier three drafts below are retained, not replaced.

The current files are all 1536 x 1024 under `game/images/tavern/guest_room/`:

| Furniture | Day, cold stove | Day, lit stove | Night, cold stove | Night, lit stove |
| --- | --- | --- | --- | --- |
| Sofa installed | `sofa_day_cold.png` | `sofa_day_lit.png` | `sofa_night_cold.png` | `sofa_night_lit.png` |
| No sofa | `lounge_day_cold.png` | `lounge_day_lit.png` | `lounge_night_cold.png` | `lounge_night_lit.png` |

`peephole_frame.png` is an RGBA foreground with a genuinely transparent
opening. The registered `guest_room_peek` image draws that frame over the
same current room background; it does not have another sofa/fire state.
Room selection reads `Sofa.installed`, actual clock hour (day 06:00-17:59),
and `TavernGuestRoomStoveObject`'s existing shared fire timer. Before either
renovation completion or sofa delivery, the original room view is preserved.
Occupied-room events retain their existing scene illustrations.

The composition uses native [Composite and DynamicImage](https://www.renpy.org/doc/html/displayables.html)
with [Transform sizing](https://www.renpy.org/doc/html/transform_properties.html).
These were checked against the installed Ren'Py 8.5.2 runtime, not assumed
from a newer documentation version. The custom `vscene` lint now recognizes
registered image names as well as loadable files, matching its runtime.

## Owners and navigation

- `SofaData` owns the sofa's portrait and guest-room schedule. Hordus's delivery
  text and the room description place it there, no longer in the Hall.
  The existing ritual gathering prerequisite remains unchanged.
- The room definitions own the two-way guest-room/glory-hole exits. The new
  entrance becomes usable when the existing glory-hole project is complete;
  its Hall entrance is retained.
- The peephole remains in `TavernMyRoom`; observing and closing it does not
  relocate the player or add an observation button inside the guest room.
- `TavernGuestRoomStoveObject` owns saved fuel, fire and ash. Its native object
  menu calls the existing `MakeFire` and `Clean` procedures. No second chore
  engine, fuel counter, daily timer or construction state was introduced.
  It is usable after guest-room renovation or an already-permitted sofa delivery.
- Save version 102 adds the stove item and missing connecting exits without
  replacing inventories, purchased furniture, paid renovations or stove state.

Renovation remains **700 maravedies + 8 whole shed logs, 3 calendar days**.
Resident Clarissa's talk option opens her request event; accepting it exposes
Draupnir's `Обустройство трактира -> Ремонт гостевой комнаты` dialogue.
The shared order scene quotes the catalog, checks resources, charges once and
uses Tavern-owned construction state. No new price, timer or request flag.

## Validation

- 199 focused checks passed (room picture selection, renovation runtime,
  guest-room ownership, movement-picture invariants and literal-image lint).
- Ren'Py 8.5.2 compile/lint passed in an isolated project. Lint only reported
  unreachable statements in generated test code.
- 33 native gameplay cases / 207 assertions passed, covering Clarissa's request, Draupnir's order,
  construction completion, all eight room visual states, the empty peephole,
  sofa card/talk/exit, stove firing/ash cleaning/back, and connecting doors
  clicked in both directions. Stove access is also clicked from the room menu.
- A separate native old-save load reached `RENOVATION_FULL_LOAD_PASSED`,
  including preserved guest-stove fuel/fire/ash and sofa location.
  Evidence: `%TEMP%/tractir_renovations_3nzn29pm/TractirExternalRenovationsProject/`
  contains `renovations-{compile,lint,test,load}.log`, eight peephole screenshots
  and `guest-stove-lit.png`. These isolated checks do not touch player saves.
- The broader Clarissa/sofa source suite produced 9 passes and 2 failures.
  Both failures were reproduced against unchanged `HEAD`: they still demand
  retired `player.tavern_management.client_room_hole/glory_hole` fields instead
  of the Tavern renovation owner. Neither progression code nor those older
  assertions was changed for this art task.
- Original room images, story dialogue, prices, prerequisites and player saves
  were not modified. Only room/delivery location text was adjusted for the
  requested sofa placement. No commit or remote push was made for this change.

## Earlier preserved draft: sofa

Output: `game/images/tavern/sofa/cursed_sofa.png`

Reference: none; new illustration.

Prompt:

> Use case: stylized-concept. Asset type: fantasy visual-novel important furniture item illustration. Create one landscape illustration of a mysterious, exceptionally luxurious antique three-seat sofa sold by a wandering merchant from the capital, now at a rustic medieval tavern. Entire sofa clearly visible, centered in three-quarter front view, occupying most of image, generous margin around every carved foot. Fine dark walnut frame, elaborate flowing carved crest and scroll arms, distinctly animal-paw-shaped carved feet, rich deep burgundy velvet upholstery and embroidered antique gold trim, broad comfortable seat with subtle use-worn texture. Implied enchanted personality through intriguing wood carving only; no literal eyes, mouth, human face, ghost or creatures. Quiet stone-and-timber tavern interior softly recedes behind it, warm amber side light, restrained mysterious tone. Painterly high-detail historical fantasy game background art, natural material colors, hand-painted wood grain and cloth texture; not a modern product photo. No people, no nudity, no text, no watermark. Single finished image, not a collage; landscape 3:2.

## Earlier preserved draft: guest_lounge_day

Output: `game/images/tavern/guest_room/lounge_day.png`

Reference: `game/images/amanda/gloryfirst/glory room.png`.

Prompt:

> Use case: lighting-weather. Asset type: alternate daytime background for the SAME fantasy tavern guest-room/lounge. Edit only illumination of the supplied room image from candlelit night to clear warm afternoon daylight entering from an existing off-camera window on the left. Preserve exact camera viewpoint, image framing, all room geometry, fireplace, cauldron, mirror, cabinets, desk, chair, textiles, chest, books and every object position and scale. Daylight should dominate and expose natural stone, dark brown wood and subdued rug colors with soft sun patches and window-cast shadows. Candles can be extinguished and fireplace may retain a small warm glow. Do NOT add windows to visible walls, remove furniture, invent a different room, add people or remodel anything. Maintain the original painterly fantasy visual-novel style and 3:2 landscape composition. No text, no watermark. One full-frame image.

## Earlier preserved draft: guest_bedroom_day

Output: `game/images/tavern/guest_room/bedroom_day.png`

Reference: `game/images/amanda/gloryfirst/glory_room.png`.

Prompt:

> Use case: lighting-weather. Asset type: alternate daytime background for the SAME fantasy tavern guest bedroom. Convert the provided candlelit nighttime room into a naturally lit clear afternoon version. Preserve the exact camera, framing, wooden bed and all four posts, headboard, dark floral patterned bedspread, pillows, side table, mug, candle, window grid, wall stone and timber paneling. The same large window at the left now reveals soft daylight and supplies bright diffuse natural light, gentle sun patches and believable window shadows across the bed. Candle extinguished, warm natural walnut and cream colors, blanket remains the same dark fabric with its same gold floral motif. Preserve all geometry and object positions. No added or removed furniture, no people, no text, no watermark; keep original painterly fantasy visual-novel style. Single landscape 3:2 image.


## Current small-room generation prompts

Mode: built-in image generation and reference editing. All nine results were
visually inspected; the in-game empty peek was also captured and inspected.
No local diffusion service, external CLI or image-editing script was used.

### sofa_day_cold

References: `game/images/amanda/gloryfirst/glory room.png` (room) and
`game/images/tavern/sofa/cursed_sofa.png` (furniture design only).

Output: `game/images/tavern/guest_room/sofa_day_cold.png`

> Use case: compositing. Asset type: consistent small guest-room/lounge game background. Image 1 is the EDIT TARGET, the existing small stone-and-timber lounge. Image 2 is the sofa DESIGN reference only, NOT its large hall background. Refit Image 1 inside the same modest footprint, low timber ceiling, same close stone walls, same plank floor and right-hand stone hearth. Place the antique burgundy velvet sofa from Image 2 at believable compact three-seat scale opposite and FACING the hearth, left/mid foreground, seen in three-quarter side view so cushions, carved walnut scroll arms and animal-paw feet are recognizable. Remove or move the obstructing desk/chair/chest to the edge, keeping a clear narrow walkway. The attractive stone fireplace/stove on the right is COLD AND UNLIT: dark empty firebox, no flame, no glowing embers, simple poker and small ash bucket beside it; remove cooking cauldron. Add one modest closed wooden door with latch on the back wall just left of hearth, entering the adjoining screened cubicle; a little edge of green curtain beyond its jamb, no signage. This is a small private tavern guest lounge, NOT a vast bar or dining hall: no public bar counter, no rows of tables, no grand staircase. Keep original hand-painted realistic fantasy style, wood and stone textures, rug, oval wall mirror and a small side table. Soft natural daylight from existing off-camera left window, candles unlit. Sofa upholstery burgundy with antique gold detail, appropriately scaled within the cramped interior. Preserve a functional and coherent perspective. No people, no nudity, no captions or UI, no watermark. Landscape 1536x1024 composition.

### peephole_frame

No image reference; transparent foreground asset.

Output: `game/images/tavern/guest_room/peephole_frame.png`

> Use case: stylized-concept. Asset type: transparent PNG foreground overlay for a fantasy visual novel. A first-person view through a SMALL SECRET PEEPHOLE cut through a thick old stone-and-timber partition wall, looking from a dark adjacent bedroom. Only render the close rough wooden edges and uneven stone tunnel sides as a very dark softly out-of-focus border around the outer edges of a 1536x1024 landscape canvas. Large rounded rectangular OPENING occupies the central 82 percent of canvas width and 78 percent of height. That entire inner opening must be genuinely fully TRANSPARENT alpha, not a painted scene, not black, not white, not checkerboard. Outside the opening is opaque deep shadow with a little textured wood and masonry, thicker at corners, narrow at center edges. A small pulled-aside wooden sliding cover may be visible at outer right edge. No room, furniture, background or subjects inside the transparent opening. The game will draw the actual room behind this transparent area. No people, no text, no watermark. Single transparent-background PNG overlay, keep exact 3:2 landscape proportion.

### sofa_day_lit

Reference: `game/images/tavern/guest_room/sofa_day_cold.png`.

Output: `game/images/tavern/guest_room/sofa_day_lit.png`

> Use case: lighting-weather. Edit target is the supplied SAME small guest lounge. Keep the entire burgundy velvet sofa EXACTLY as it is: its carved walnut frame, animal-paw feet, size, position and shape. Keep natural daytime illumination from off-camera left, same warm sunlight patches and daylight; candles unlit. The fireplace must now contain a small realistic burning stack of split logs with clear warm orange flames and ember glow illuminating the hearth and nearby floor. No cooking cauldron. Keep EXACT room geometry, camera angle, scale, small footprint, wooden door to adjacent room just left of fireplace, green curtain edge, mirror, shelves, tabletop, chest, rug and all other objects unchanged. Match the original painterly fantasy game art. No new objects or architectural enlargement. No people, no text, no watermark. Single full-frame landscape 1536x1024.

### sofa_night_cold

Reference: `game/images/tavern/guest_room/sofa_day_cold.png`.

Output: `game/images/tavern/guest_room/sofa_night_cold.png`

> Use case: lighting-weather. Edit target is the supplied SAME small guest lounge. Keep the entire burgundy velvet sofa EXACTLY as it is: its carved walnut frame, animal-paw feet, size, position and shape. Change illumination to nighttime: no sunlight patches or daylight, soft cool moonlight from off-camera left, gentle candlelight from existing small candle; readable dim cozy interior. The fireplace remains completely COLD AND UNLIT: empty dark firebox with no logs, flames, glowing embers or orange light. Keep poker and ash bucket. Keep EXACT room geometry, camera angle, scale, small footprint, wooden door to adjacent room just left of fireplace, green curtain edge, mirror, shelves, tabletop, chest, rug and all other objects unchanged. Match the original painterly fantasy game art. No new objects or architectural enlargement. No people, no text, no watermark. Single full-frame landscape 1536x1024.

### sofa_night_lit

Reference: `game/images/tavern/guest_room/sofa_day_cold.png`.

Output: `game/images/tavern/guest_room/sofa_night_lit.png`

> Use case: lighting-weather. Edit target is the supplied SAME small guest lounge. Keep the entire burgundy velvet sofa EXACTLY as it is: its carved walnut frame, animal-paw feet, size, position and shape. Change illumination to nighttime: no sunlight patches or daylight, soft cool moonlight from off-camera left, gentle candlelight from existing small candle; readable dim cozy interior. The fireplace must now contain a small realistic burning stack of split logs with clear warm orange flames and ember glow illuminating the hearth and nearby floor. No cooking cauldron. Keep EXACT room geometry, camera angle, scale, small footprint, wooden door to adjacent room just left of fireplace, green curtain edge, mirror, shelves, tabletop, chest, rug and all other objects unchanged. Match the original painterly fantasy game art. No new objects or architectural enlargement. No people, no text, no watermark. Single full-frame landscape 1536x1024.

### lounge_day_cold

Reference: `game/images/tavern/guest_room/sofa_day_cold.png`.

Output: `game/images/tavern/guest_room/lounge_day_cold.png`

> Use case: precise-object-edit. Edit target is the supplied SAME small guest lounge. REMOVE ONLY the burgundy sofa and its pillows: leave that area empty, reconstructing the same wall paneling, stone wall and wooden floor/rug behind it. Do not replace it with another sofa, chair or furniture. Keep natural daytime illumination from off-camera left, same warm sunlight patches and daylight; candles unlit. The fireplace remains completely COLD AND UNLIT: empty dark firebox with no logs, flames, glowing embers or orange light. Keep poker and ash bucket. Keep EXACT room geometry, camera angle, scale, small footprint, wooden door to adjacent room just left of fireplace, green curtain edge, mirror, shelves, tabletop, chest, rug and all other objects unchanged. Match the original painterly fantasy game art. No new objects or architectural enlargement. No people, no text, no watermark. Single full-frame landscape 1536x1024.

### lounge_day_lit

Reference: `game/images/tavern/guest_room/sofa_day_cold.png`.

Output: `game/images/tavern/guest_room/lounge_day_lit.png`

> Use case: precise-object-edit. Edit target is the supplied SAME small guest lounge. REMOVE ONLY the burgundy sofa and its pillows: leave that area empty, reconstructing the same wall paneling, stone wall and wooden floor/rug behind it. Do not replace it with another sofa, chair or furniture. Keep natural daytime illumination from off-camera left, same warm sunlight patches and daylight; candles unlit. The fireplace must now contain a small realistic burning stack of split logs with clear warm orange flames and ember glow illuminating the hearth and nearby floor. No cooking cauldron. Keep EXACT room geometry, camera angle, scale, small footprint, wooden door to adjacent room just left of fireplace, green curtain edge, mirror, shelves, tabletop, chest, rug and all other objects unchanged. Match the original painterly fantasy game art. No new objects or architectural enlargement. No people, no text, no watermark. Single full-frame landscape 1536x1024.

### lounge_night_cold

Reference: `game/images/tavern/guest_room/sofa_day_cold.png`.

Output: `game/images/tavern/guest_room/lounge_night_cold.png`

> Use case: precise-object-edit. Edit target is the supplied SAME small guest lounge. REMOVE ONLY the burgundy sofa and its pillows: leave that area empty, reconstructing the same wall paneling, stone wall and wooden floor/rug behind it. Do not replace it with another sofa, chair or furniture. Change illumination to nighttime: no sunlight patches or daylight, soft cool moonlight from off-camera left, gentle candlelight from existing small candle; readable dim cozy interior. The fireplace remains completely COLD AND UNLIT: empty dark firebox with no logs, flames, glowing embers or orange light. Keep poker and ash bucket. Keep EXACT room geometry, camera angle, scale, small footprint, wooden door to adjacent room just left of fireplace, green curtain edge, mirror, shelves, tabletop, chest, rug and all other objects unchanged. Match the original painterly fantasy game art. No new objects or architectural enlargement. No people, no text, no watermark. Single full-frame landscape 1536x1024.

### lounge_night_lit

Reference: `game/images/tavern/guest_room/sofa_day_cold.png`.

Output: `game/images/tavern/guest_room/lounge_night_lit.png`

> Use case: precise-object-edit. Edit target is the supplied SAME small guest lounge. REMOVE ONLY the burgundy sofa and its pillows: leave that area empty, reconstructing the same wall paneling, stone wall and wooden floor/rug behind it. Do not replace it with another sofa, chair or furniture. Change illumination to nighttime: no sunlight patches or daylight, soft cool moonlight from off-camera left, gentle candlelight from existing small candle; readable dim cozy interior. The fireplace must now contain a small realistic burning stack of split logs with clear warm orange flames and ember glow illuminating the hearth and nearby floor. No cooking cauldron. Keep EXACT room geometry, camera angle, scale, small footprint, wooden door to adjacent room just left of fireplace, green curtain edge, mirror, shelves, tabletop, chest, rug and all other objects unchanged. Match the original painterly fantasy game art. No new objects or architectural enlargement. No people, no text, no watermark. Single full-frame landscape 1536x1024.
