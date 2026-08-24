# People Data/Info Standard

The authoritative people layer is `game/Utilities/General/NPC/PeopleRuntime.rpy`.

- `peopleData[id]` is static or mostly-static person data: display names, age, portrait, default room, description, gift preferences, and schedule entries.
- `peopleInfo[id]` is save-state runtime info: relation, openness, corruption, known flag, daily talk/flirt/gift/ask counters, current location, and personal topic/gift history.

Do not add scalar or dictionary mirrors for these values. Runtime relationship and
story state belongs to the `PeopleInfo` subclass instance. Static metadata and all
schedule definitions/caches belong to its `PeopleData` owner. `getLocation()` and
`getNPCids()` are projections of that schedule; reads must not write a copied
location into NPC state.

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
2. Define one `PeopleData` subclass/instance for metadata and schedule ownership.
3. Define one `PeopleInfo`, `Girl`, or `BaseNPC` subclass/instance for mutable state.
4. Register those objects in the person's `Init*.rpy` label. `InitGameNPCs` calls
   `initPeople()` once after registrations and then loads interval schedules.

On load, `npc_schedule_after_load()` repairs missing schedule-runtime attributes
from older saves, invalidates only the derived daily plan, and reloads JSON interval
entries. It does not rebuild `peopleInfo`, overwrite story state, or copy schedule
locations into NPC instances.
