# Legare household: boarding-school background

Approved scope (2026-09-22): update the household's background, Clarissa's gradual
explanation, and the church illustrations. Other story events remain unchanged.

## Canon and references

- Aloise uses the established Russian name **Элоиза**. She is Legare's wife,
  a professional governess running a boarding/finishing school in their house.
  Adult pupils prepare for marriage, service in noble households, or life as
  a concubine.
- Pauline uses **Полина**. She is an adult boarding pupil from a small remote
  village, not Legare's daughter. No exact age or village name is invented.
- Source appearance: `textLocRef/Church.txt:47` describes Aloise as petite,
  middle-aged and chestnut-haired. It provides no separate Pauline appearance.
  Pauline's new visual design is therefore an illustration choice.
- Clarissa's existing parentage/history is unchanged by this patch. Her
  existing painting, fiance, forest, manners and merchant threads are not reset.
- Old TXT/QSP and extracted dialogue files remain historical references, not
  rewritten source files.

## Playable disclosure

The existing family question in `IntClaraTalk` owns this interaction. Its
existing daily ask/talk counters and +1 friendship/+1 trust reward are unchanged.
Nested native menus provide an explicit return at every depth.

| Detail | Gate |
| --- | --- |
| Aloise's profession and the school | Existing family question: friendship >=6, no question asked today |
| Pauline and everyday schooling | Friendship >=8, trust >=4, paintings stage >=4 |
| Different intended futures for pupils | Friendship >=10, trust >=6, paintings stage >=6 or completed |

Deeper gates read the current values after the existing conversation reward.
No new flag, thread, stored disclosure level or parallel relationship state.
Completed-story saves can ask the same question and read the new background.
Each deeper explanation follows the public introduction rather than replacing it.

`ChurchServiceLegare` keeps its existing story-event interception first, then
owns the repeatable household view, closer governess/pupil view and return.
Church schedules and the two existing fiance illustrations are unchanged.

## New assets

Built-in image generation; original images retained.

- `game/images/Alber/church/household_school.png`: whole household at service.
- `game/images/Alber/church/aloise_pauline_school.png`: closer governess/pupil beat.

New illustrations use adult characters, matching the project's stated age
convention; they do not assign numerical ages.

### Whole-household prompt

```text
Use case: illustration-story. Asset: new 16:9 landscape church attendance illustration for the fantasy historical game Tractir. Generate a NEW image based on the supplied character reference images; do not overwrite or edit the originals.
References: Image1 Alber portrait is the identity reference for Alber Legare (blond swept-back hair, short neat blond beard, light eyes); Image2 Clarissa portrait is her identity reference (long silver-blond hair partly braided, light green-grey eyes); Image3 old church attendance shot is the stone church interior and Alber's black formal coat reference, not the final visual quality.
Primary request: the whole Legare household attending morning service, seven fully clothed adult people beside a pale stone column inside an old church. Main foreground group: Alber Legare in his black doublet/long black formal coat and white cravat; his wife Aloise/Eloise, a petite middle-aged chestnut-haired professional governess with composed authoritative posture and a well-made modest burgundy dress; Clarissa with the exact reference identity, wearing a long modest olive-green dress; Pauline, an adult boarding pupil newly arrived from a remote rural village, with a distinct natural brunette face, neatly braided dark chestnut hair and a simple modest muted blue dress, attentive to her governess. Behind them stand the other three named household members Gerard, Jean-Jacques and Remi, adult young men in modest formal historical clothing, each visually distinct. Remi is the youngest adult, not a child. Exactly seven people, all adults; no other foreground figures.
Style: polished realistic game illustration, natural colors and faces, finely textured cloth and stone, painterly photographic realism matching the portrait reference quality. Composition wide, coherent three-quarter or full length group, all seven faces visible without overlap or duplication; no collage or separate panels. Quiet morning light from high church windows, restrained warmth, candlelight accents. All listening to service, discreet glance between governess and pupil. No sexual action, no nudity, no lettering, no captions, no watermark, no modern objects.
```

### Governess and pupil prompt

```text
Use case: illustration-story / identity-preserve. Reference: household_school.png,
preserving Aloise's and Pauline's faces, hair, clothing and the church setting.
New wide game illustration: a closer waist-up view of middle-aged Aloise in her
burgundy dress and adult pupil Pauline in her blue dress beside the same stone
column. Aloise quietly indicates how to hold a prayer book; Pauline corrects her
posture while listening. Natural colors, polished realistic game illustration,
soft church daylight. Only these two foreground figures, fully clothed, no
lettering, no watermark, no collage. Preserve the source image unchanged.
```
