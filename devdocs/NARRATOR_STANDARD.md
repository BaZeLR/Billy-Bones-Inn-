# Narrator Standard

Tractir now has a FamilyLife-style narrator in `game/Inn/NarratorRuntime.rpy`.

Use it in story labels when the text is scene description, MC observation, or connective narration:

```renpy
n "The morning rain softened the noise from the street, but the tavern still felt awake."
```

For Python-built events, use the same narrator through:

```renpy
$ tractir_narrate("The hallway is quiet enough that every floorboard sounds guilty.")
```

The narrator uses `images/general/narrator.png` as a side image. Existing unnamed narration is not overwritten, so old labels stay visually stable until they are intentionally rewritten to use `n`.

The external pure-Python logic test script also verifies that the narrator character, helper function, and side image are present.
