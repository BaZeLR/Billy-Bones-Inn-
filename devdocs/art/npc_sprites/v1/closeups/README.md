# Dialogue close-ups

Clarissa's two additional close-ups preserve her established grey eyes,
silver hair and lavender/ivory homewear. `attentive` has alert eyes and gently
parted lips; `amused` has a closed-lip smile and one eye closed in a wink.
Each expression is exported as a 640 × 800 portrait and a 320 × 320 dialogue
crop. Both use the same original canvas and shared crop coordinates.

The existing `npc_clara_voice` alias and `npcface_clara` side-image tag are
reused. No new character wrapper or screen is needed:

```renpy
npc_clara_voice closeup_attentive "You have my attention."
npc_clara_voice closeup_amused "I think you're bluffing."

show npc_clara closeup attentive at npc_sprite_body
npc_clara_voice closeup_attentive "What did you have in mind?"
show npc_clara closeup amused at npc_sprite_body
npc_clara_voice closeup_amused "Your move."
hide npc_clara
```

For the media panel, use `npc_overlay_clara_closeup_attentive` or
`npc_overlay_clara_closeup_amused` with the existing
`scene_runtime.picture_overlay` field. Restore the previous overlay when
the owning scene exits.

The accompanying body pose is `npc_clara cards floor_lean`: seated with one
palm supporting her, one knee raised, the other leg folded and cards held
near her shoulder. It wears the lavender slip and is registered in the
separate card-game module. Its skeleton guide was approximate; the selected
result is a floor-seated lean, rather than a literal copy of the guide.

`generation_prompts.json` retains the three exact built-in generation
prompts, input references and selected source names. The close-up manifest
records source/export hashes and crop coordinates. See
`previews/clara_closeups.jpg` and
`../card_game/previews/clara_cards_floor_lean.jpg` for the actual exports.

## Rebuild

```json
{
  "portraits": [
    {
      "npc_id": "clara", "state": "attentive", "source": "attentive_source.png",
      "portrait_source_box": [0, 0, 1122, 1402],
      "dialogue_source_box": [180, 0, 1060, 880]
    },
    {
      "npc_id": "clara", "state": "amused", "source": "amused_source.png",
      "portrait_source_box": [0, 0, 1122, 1402],
      "dialogue_source_box": [180, 0, 1060, 880]
    }
  ]
}
```

Run `python3 tools/build_npc_closeups.py --source-map closeup_sources.json`.
Pillow, numpy and scipy are offline build dependencies; the game uses only
the exported PNGs and native Ren'Py declarations.
