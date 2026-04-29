# Player Condition Social Dynamics

FamilyLife uses a unified player-condition loop: time passes, grooming and clothes age, visible stats are recalculated, and social outcomes react to those stats.

Tractir now follows the same idea for the core women:

- Amanda
- Clarissa
- Melissa
- Sandra

The source stats are still in `game/Inn/stat.rpy`:

- `dayssincewash`
- `dayssincehaircut`
- `PlayerHaircutDaySt`
- `PlayerDressDaySt`
- `costumecondition`
- `look`
- `charisma`

`player_social_condition_modifier()` turns the current player condition into a small score modifier for talk, flirt, gift, and share interactions. Clean clothes, fresh grooming, and strong charisma can help. Dirt, old haircut, worn clothes, or no proper clothing can hurt.

`resolve_player_social_delta()` and social topic scoring now apply this modifier before relationship points are committed.

The player also receives Ren'Py notify feedback:

```renpy
Влияние внешности: -1 (грязь после работы).
```

Talk and flirt topic choices also notify the explicit theme score on the same `-5..+5` scale used by the profile tables:

```renpy
Тема: Об одежде и внешности (+4 -> +3). Отношения: +1.
```

The first value is the chosen theme's profile result. The second value appears when grooming, clothes, mood, or relationship modifiers changed the final applied score.

This is separate from the existing relationship-point notify for non-topic social actions:

```renpy
Очки отношений: +1.
```

Runtime logic tests check that the condition modifier and adjusted social delta work for the four core women.
