# Location, NPC Visibility, Talk, And Daily Reset Standard

Use this file only with the current OOP model.

## Location

`CurLoc` is the current player location code. The room label sets the current
room and renders through `main_ui`.

Room entry may check for available events and room/object spawns, but it must
not use refresh/rebuild/apply/renew labels as architecture. Returning or jumping
to the real room label is enough to render the current room state.

## Visible NPCs

NPC visibility comes from NPC class state:

```text
current room code
-> NPC.getLocation()
-> getNPCids(location)
-> right-side visible NPC panel
```

Rooms do not own NPC presence. If an NPC is in a sublocation, scheduled away, or
inside an event, the NPC class/location method must say so.

## Talk

The clicked NPC talk action opens that NPC's real talk label, for example
`IntAmandaTalk` or `IntGeorgettTalk`.

The talk label owns:

- current picture or `vscene`;
- text;
- classic Ren'Py `menu:`;
- branch consequences;
- time cost;
- return to the current room or relevant event flow.

Shared helper methods may calculate a score or preference only when the logic is
truly common. They must not hide the authored menu, state mutation, or return
flow.

## Daily Reset

Daily counters are reset from the new-day cycle by calling owner reset methods.

NPC counters such as talked/flirted/gifted/asked belong to the NPC instance.
Room daily flags belong to the room. Tavern business counters belong to the
tavern system until that system is ported.

Do not reset or mirror daily state through old external dicts when an owning
class exists.
