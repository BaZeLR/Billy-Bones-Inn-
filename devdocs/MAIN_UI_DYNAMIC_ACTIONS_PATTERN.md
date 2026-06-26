# Main UI Dynamic Actions Pattern

This is the project rule for rendering room, object, NPC, and shop actions in
the main UI.

It is not the rule for authored story/event scenes. Story/event scenes must
follow `devdocs/EventThreadInstruction/README.md`: event tuples own
availability; event labels own `vscene`, text, classic Ren'Py `menu:`, direct
consequences, time cost, and thread progression; the right-side HUD remains
persistent.

## Goal

Keep the right-side action area simple and direct:

- one embedded action panel inside `screen main_ui`
- one current title
- one current content screen
- no `globals()`
- no `renpy.store`
- no Python-side `renpy.call()` / `renpy.jump()`
- no UI shim layers that rebuild menus through helper chains

## Core State

Use defaulted Ren'Py variables:

```renpy
default current_action_title = "Actions"
default current_action_content = None

default current_girl_key = ""
default current_object_id = ""
default CurrentRoom = None
```

## Main UI Area

The right panel contains one fixed action area:

```renpy
frame:
    has vbox

    text "[current_action_title]"

    use dynamic_actions_panel
```

## Dynamic Panel

The panel swaps content by current state:

```renpy
screen dynamic_actions_panel():
    if UI_actions:
        use qsp_menu_actions
    elif current_action_content == "room_navigation":
        use room_navigation_actions
    elif current_action_content == "girl_interaction":
        use girl_interaction(current_girl_key)
    elif current_action_content == "object_interaction":
        use object_interaction(current_object_id)
    else:
        text "Select something to interact with."
```

## Room Entry Rule

Each room source file sets its own room object directly before entering:

```renpy
$ CurrentRoom = TavernMainRoom
$ CurLoc = CurrentRoom.code_name
$ location = CurLoc
$ current_action_title = "Actions"
$ current_action_content = "room_navigation"
$ current_girl_key = ""
$ current_object_id = ""
```

No central room registry is needed.

## Character Buttons

Buttons in `main_ui` or any label can open character interaction directly:

```renpy
textbutton "Sandra":
    action [
        SetVariable("current_action_title", "Sandra"),
        SetVariable("current_action_content", "girl_interaction"),
        SetVariable("current_girl_key", "sandra"),
    ]
```

## Object Buttons

Room objects open their own interaction screen:

```renpy
textbutton "[room_object.name]":
    action [
        SetVariable("current_action_title", room_object.name),
        SetVariable("current_action_content", "object_interaction"),
        SetVariable("current_object_id", room_object.object_id),
    ]
```

## Navigation

Room exits jump directly to the real room label:

```renpy
textbutton "[room_exit.label]":
    action Jump(room_exit.target)
```

No alias map, no fallback resolver.

## Event Use

Authored events do not build choices through the dynamic action panel. They use
the event/thread runtime for availability and a normal Ren'Py label for flow:

```renpy
label story_example_event:
    vscene "images/example/event.jpg"
    "Event text."

    menu:
        "Act":
            $ SomeNpc.var["example_seen"] = 1
            $ thread.advance()
            jump expression CurLoc

        "Leave":
            jump expression CurLoc
```

The screen layer may style the Ren'Py menu in the right-side action area, but
the choices and consequences stay in the event label.

## Execution Rule

For action buttons, use plain Ren'Py actions:

- `Jump(...)` for navigation
- `Call(...)` for subroutines that return
- `SetVariable(...)` to swap current action panel content

This is the preferred project style going forward.
