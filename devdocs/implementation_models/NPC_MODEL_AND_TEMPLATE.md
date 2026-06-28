# NPC Model And Template

This document defines the intended NPC implementation model.

## Purpose

NPCs represent recurring non-player characters whose current state can change
during the game.

NPCs include:

- girls
- secondary NPCs
- workers
- merchants who are real recurring characters
- priests
- guards
- enemies only when they also exist as recurring world characters
- any recurring named or initially unnamed character

Not every named person in text is an NPC class.

Do not create NPC classes for:

- descriptive people used only as story reminders.
- one-off generated names from a name list.
- random townspeople with no persistent state.
- animals, creatures, patrols, hunt targets, or fight spawns that exist only for
  combat.

Those are generated/descriptive entities or fight enemies. They belong to the
story text, generator, or fight/hunt system, not to the NPC registry.

Merchant/vendor semantics:

- a recurring merchant with story state is a secondary NPC.
- a shop function without character state belongs to shop/economy.
- a random seller generated for one scene is not an NPC class.

## Source Of Truth

The NPC class instance is the source of truth.

Examples:

- `Amanda`
- `Melissa`
- `Eddie`
- `Francheska`
- `Robin`
- `Zimmer`

The registry `peopleInfo[id]` points to the NPC instance. It is not a second
state store and not a factory.

Legacy dicts such as `knowsMC`, `CurrentLoc`, `Friends`, `TalkedToday`, and
`AmandaVar` are not authoritative. They may be temporary compatibility output
only while older labels still read them. They must not decide current NPC state
when an NPC instance exists.

NPC parameters should move from global variables and legacy dicts into class
fields and methods. Some state may be exposed through public API methods. Other
state should remain internal to the NPC class.

Save/load rule: the NPC instance must contain the current playable state at any
checkpoint. Loading a save should restore the same NPC instance state, not rebuild
that state from legacy dicts.

## Class Hierarchy

Use this hierarchy:

```text
PeopleData
  static or mostly-static person data

PeopleInfo
  common mutable person state

BaseNPC(PeopleInfo)
  shared NPC behavior

Girl(BaseNPC)
  shared girl behavior

SpecificNpcInfo(BaseNPC or Girl)
  unique NPC behavior and story state
```

## Model Features

Every NPC model should define or inherit:

- `name`: stable code id, lower-case.
- `unknown_name`: name shown before player knows the NPC.
- known state: whether player knows real identity.
- display name method: unknown before known, real name after known.
- location method: where NPC is now.
- visibility method when NPC has special visibility rules.
- relationship state.
- daily interaction counters.
- story flags or unique class-owned state.
- schedule logic or schedule reference.
- social action availability.
- talk label or talk entry method.
- portrait/picture reference where needed.
- birth date, not age, when permanent identity data is needed.
- temporary compatibility write method only where old labels still require
  legacy output.

## Static Data Template

Each recurring NPC should have a static data class when it has names, portrait,
birth date, description, or default location.

```renpy
init python:
    class ExampleData(PeopleData):
        code_name = "example"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Real Name",
                fullname="Full Real Name",
                genitive="Name Genitive",
                dative="Name Dative",
                default_location="RoomCode",
                description="Short NPC description.",
                birth_date=(1480, 4, 12),
                portrait="images/example/portrait.png",
            )

define ExampleStaticData = ExampleData()
```

## Runtime NPC Template

```renpy
init python:
    class ExampleInfo(BaseNPC):
        unknown_name = "Unknown Name"

        def __init__(self, name="example", **kwargs):
            super().__init__(name, **kwargs)
            self.met = 0
            self.lasttalkday = -1
            self.asked_work = 0
            self.location = "RoomCode"

        def getLocation(self, wday=None, hour=None):
            self.location = "RoomCode"
            return self.location

        def visible_now(self):
            return self.getLocation() == str(CurLoc or "")

        def mark_met(self):
            self.met = 1
            self.mark_known()
            return True

default Example = ExampleInfo()
```

## Temporary Legacy Bridge

Only add this while old labels still read `ExampleVar`. This is compatibility
output, not the model.

```renpy
default ExampleVar = {}

init python:
    class ExampleInfo(BaseNPC):
        # normal class fields stay authoritative

        def write_legacy_mirror(self):
            ExampleVar["met"] = self.met
            ExampleVar["lasttalkday"] = self.lasttalkday
            ExampleVar["asked_work"] = self.asked_work
            return True
```

## Registration Template

Registration must point the registry to the existing NPC instance.

Do not rebuild the NPC from legacy dicts.

```renpy
label register_example_secondary:
    python:
        peopleData["example"] = ExampleStaticData
        Example.update()
        peopleInfo["example"] = Example
        if Example not in secondary_npcs:
            secondary_npcs.append(Example)
    return
```

For a girl:

```renpy
label register_example_girl:
    python:
        peopleData["example"] = ExampleStaticData
        Example.update()
        peopleInfo["example"] = Example
        if Example not in girls:
            girls.append(Example)
    return
```

## Talk Template

Talk labels own dialogue flow and dialogue choices.

```renpy
label IntExampleTalk:
    $ Example.mark_met()

    "Dialogue text."

    menu:
        "Ask about work":
            $ Example.asked_work = 1
            jump IntExampleTalk

        "Leave":
            jump expression CurLoc
```

Use `call` only for returnable procedures. Use `jump` for story continuation or
return to a room.

## Utilities

Allowed utility functions:

- `getPersonInfo(id)`: returns registered NPC instance.
- `getPersonData(id)`: returns static data.
- `npc_display_name(id)`: returns unknown or real display name.
- `mark_known()` on the NPC instance.
- shared social helper labels when they are real returnable procedures.
- explicit public API methods on NPC classes for state that other systems are
  allowed to read or change.

Utilities must not:

- create generic fallback NPCs as normal runtime.
- rebuild NPCs from legacy dicts.
- treat legacy dicts as source of truth.
- own NPC story consequences.
- duplicate NPC-specific methods in a central dispatcher.
- expose every internal NPC field as global API.

## Controls

Controls are player-facing actions tied to the NPC.

Examples:

- look
- talk
- flirt
- gift
- ask a special question
- start a story event

The visible NPC panel is built by asking NPC class instances for current
location and visibility. A room does not own the NPC list. The panel may call a
small UI helper, but the NPC or its talk/event label owns behavior.

## Forbidden Patterns

Do not implement NPC behavior through:

- legacy dicts as source of truth.
- `globals()` lookup.
- generic fallback `BaseNPC(id)` creation.
- central dispatcher that owns NPC outcomes.
- room labels mutating NPC state except for direct room-entry setup that belongs
  to room navigation.
- screens mutating NPC story state.
- duplicate unknown-name maps when class already owns `unknown_name`.

## Implementation Checklist

For each NPC:

- [ ] Static data class exists where needed.
- [ ] Runtime class exists and inherits correct base.
- [ ] Instance is created once.
- [ ] Instance is explicitly registered.
- [ ] `unknown_name` is on class if NPC can be unknown.
- [ ] Static identity uses birth date, not mutable age.
- [ ] Known state is changed through `mark_known()` or NPC method.
- [ ] Location logic lives on NPC or schedule system.
- [ ] HUD presence comes from NPC location/visibility, not room NPC lists.
- [ ] Unique story state lives on NPC object/class instance.
- [ ] Legacy dict writes are compatibility output only.
- [ ] Save/load restores NPC class instance state without dict rebuild authority.
- [ ] Global parameter variables are moved into class fields/methods.
- [ ] Only needed state is exposed through NPC API methods.
- [ ] Visible NPC panel uses `npc_display_name()`.
- [ ] Talk label calls NPC methods, not room-owned mutations.
