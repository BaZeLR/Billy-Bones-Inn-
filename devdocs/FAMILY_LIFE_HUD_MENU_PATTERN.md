# Family Life HUD Placement Finding

Reference project:
`C:\Users\blank\Documents\RenPy_Projects\FamilyLife-0.1.1-base+Event0\game`

## Finding

Family Life keeps its HUD visible as a right-side screen while event choices are displayed in the normal interaction area. The important rule is that event choices stay attached to the active event scene.

Example:

```renpy
show screen status
menu:
    "Choice":
        ...
```

Observed in:

- `script.rpy`, `label start`: shows `status`, then immediately uses a normal Ren'Py `menu:`.
- `sexAngel.rpy`, `label nannyFollow_0`: authored event text and normal Ren'Py `menu:`; event logic advances the thread in the label.
- `sexNikki.rpy`, labels such as `nikkiSex_0` and `nikkiSex_1`: `vscene`, authored text, then classic `menu:` choices inside the event label.
- `status.rpy`, `screen status`: HUD is a right-side screen, not a menu controller.

Family Life does not build event choices through a separate refresh/apply/renew
screen path. The event label writes the choices where the event happens.

## Tractir Rule

Tractir's `main_ui` right side has three sections:

1. top stats/time/chores,
2. middle navigation/action buttons,
3. bottom visible NPCs.

For events that use `main_ui`, event choices must appear in section 2, the middle action panel. The top stats/chores and bottom visible NPC section must remain visible and unchanged.

This is mandatory for story and sex events. The visual target is the attached
event screenshot: event picture and text remain visible, and the available event
choices appear inside the right-side action area during the event.

Classic event-label menu authorship is the preferred source model:

```renpy
label some_event:
    vscene "images/event/picture.jpg"
    "Event text."

    menu:
        "Choice A":
            $ SomeVar["choice"] = "a"
            jump some_event_a

        "Leave":
            jump expression CurLoc
```

Tractir may render this through `main_ui`, but the choices must still be owned
by the event label and displayed in the event layout.

## Multi-Picture Proceed Beats

Family Life sex events often show several pictures in one label:

```renpy
vscene "images/event/1.jpg"
"Text."
vscene "images/event/2.jpg"
"More text."
menu:
    "Continue":
        pass
vscene "images/event/3.jpg"
"Next text."
```

The `Continue` menu is an authored pause, not a paging subsystem. Tractir should
match this behavior. When the proceed button appears in the right action area,
it must advance to the next authored event beat while preserving the current
event picture/text layout.

## Tractir Rendering Compatibility Pattern

Classic event-label `menu:` is the preferred source model. When the current
Tractir `main_ui` screen is used to render the same event choices, the event
label may prepare:

- `MainTxt` / `CurLocDesc` for event text,
- image state through existing image helpers,
- `current_action_title`,
- `current_action_items` for the middle action panel.

Then `call screen main_ui` displays the full standard layout. No overlay screen should move the choices away from section 2.

This is a rendering compatibility path, not permission to move choice ownership
out of the event label.

## Current Tractir Comparison

Desired/currently acceptable:

- Classic `menu:` inside event labels, as in `game/NPC/Girls/Becky/BeckyEvents.rpy`.
- Event-label-owned `current_action_items` when it renders choices in the
  current `main_ui` event panel and does not create a separate dispatcher.

Problematic/currently not desired:

- `QueuePagedPanelText` or other queued panels when they replace the authored
  event menu flow.
- `AdvancePagedPanelText` or generic proceed buttons when they replace a simple
  authored `menu: "Продолжить": pass` beat.
- `SceneActionPanel` or overlay screens when they detach choices from the
  normal event picture/text/main UI layout.
- `main_ui_set_action_panel` used as a distant generic event dispatcher instead
  of direct event-label choices.
- Any refresh/apply/renew path that rebuilds event choices outside the event
  label.
