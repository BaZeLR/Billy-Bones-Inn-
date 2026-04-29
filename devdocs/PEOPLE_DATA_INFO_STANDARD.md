# People Data/Info Standard

This project now has a FamilyLife-style people layer in `game/Inn/PeopleRuntime.rpy`.

The layer does not replace the existing Tractir maps. It exposes the same state through OOP objects:

- `peopleData[id]` is static or mostly-static person data: display names, age, portrait, default room, description, gift preferences, and schedule entries.
- `peopleInfo[id]` is save-state runtime info: relation, openness, corruption, known flag, daily talk/flirt/gift/ask counters, current location, and personal topic/gift history.

Existing maps remain authoritative for old code:

- `Friends`
- `otkroven`
- `sluttiness`
- `knowsMC`
- `TalkedToday`, `FlirtedToday`, `GiftedToday`, `AskedToday`
- `CurrentLoc`
- `NPCSchedules`

Use these helpers in new event/thread code:

```renpy
$ amanda = getPersonInfo("amanda")
if amanda.isInLocation("TavernAmandaRoom") and amanda.corruption >= 20:
    "Amanda is in her room and the condition is visible."
```

```renpy
$ melissa_data = getPersonData("melissa")
$ portrait = melissa_data.selectIcon()
$ room = melissa_data.getLocation()
```

When adding a new person:

1. Add names to `NamesSet.rpy` or another init source.
2. Set existing maps in that person's `Init*.rpy`: `CurrentLoc`, `Friends`, `sluttiness`, `otkroven`, `knowsMC`, `age_girls`, `girltextdesc`.
3. Add schedule entries with `npc_schedule_set`.
4. `call InitPeople` rebuilds `peopleData`/`peopleInfo` after all current init labels.

For loaded saves, `people_after_load_update()` rebuilds the layer without removing existing event or UI state.
