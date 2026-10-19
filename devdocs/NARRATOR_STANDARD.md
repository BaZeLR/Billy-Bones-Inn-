# Narrator Standard

The flea narrator is defined in `game/Utilities/General/Common/NarratorRuntime.rpy`.

Use it in story labels when the text is scene description, MC observation, or connective narration:

```renpy
n "The morning rain softened the noise from the street, but the tavern still felt awake."
```

For Python-built events, use the same narrator through:

```renpy
$ tractir_narrate("The hallway is quiet enough that every floorboard sounds guilty.")
```

The default side image, `images/general/narrator.png`, is the neutral flea portrait.
The eight expression sprites in `images/narrator/side/` are transparent 400×400 PNGs,
using the same portrait size and the existing `zoom=0.72` presentation.

## Expressions

Use native Ren'Py image attributes to select an expression:

```renpy
n neutral "Начнём нашу историю."
n mischievous "У этой истории есть любопытная подробность."
n surprised "Вот это поворот!"
n defiant "Попробуй меня переубедить."
n thoughtful "Здесь стоит присмотреться к деталям."
n delighted "Отличные новости!"
n suspicious "Что-то здесь не сходится."
n whispering "Только между нами..."
n neutral "Продолжим."
```

An expression stays selected until another is requested. Use `n neutral` to
return to the neutral portrait. Python-driven narration uses the same native
attributes and the existing helper:

```renpy
$ renpy.set_tag_attributes("tractir_narrator thoughtful")
$ tractir_narrate("Здесь стоит присмотреться к деталям.")
$ renpy.set_tag_attributes("tractir_narrator neutral")
```

`call narrator_test` previews all eight expressions and returns with neutral selected.
Existing unnamed narration keeps its existing presentation until intentionally
rewritten to use `n`.

## Full illustration

`images/narrator/flea_table.png` is the supplied candlelit table illustration,
copied without redrawing or changing its pixels. It is registered as
`flea_narrator_table` and fits inside the current screen while preserving its
aspect ratio:

```renpy
scene flea_narrator_table
n neutral "Откроем книгу и начнём рассказ."
```

The illustration is shown only when an authored scene requests it. Narrator
dialogue selects a side portrait through the existing `SideImage()` display.

## Art source

The user supplied the flea expression sheet and table illustration on
20 October 2026. The portraits preserve the golden-brown chitin, glossy black
eyes, buckled black hat, red feather, ivory ruff, and burgundy-and-gold cloak.
The built-in image-generation tool extracted the expression atlas; its prompt
and the export details are recorded in
[art/narrator/ASSET_PROMPT.txt](art/narrator/ASSET_PROMPT.txt).

The external pure-Python logic test script also verifies that the narrator character, helper function, and side image are present.
