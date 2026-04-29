# Ren'Py Scene Action Panel Template

Use this pattern for text-game events that must keep the existing Tractir UI:

```renpy
label SomeEventLabel:
    $ _items = [
        scene_panel_call_item(
            "Do a mutating action",
            "SomeEventApply",
            args=("value",),
            minutes=15,
        ),
        scene_panel_jump_item("Go to the kitchen", "TavernKitchen", minutes=5),
        scene_panel_add_item("Spend 1 coin and stay in this panel", "money", -1,
            text="Result text after mutation.",
            title="Next actions",
            next_items=[scene_panel_return_item("Return")],
        ),
        scene_panel_return_item("Stay here"),
    ]
    call SceneActionPanel(
        "images/path/to/picture.png",
        "Event text goes here.",
        "Your actions",
        _items,
    )
    return

label SomeEventApply(value=""):
    $ money -= 1
    $ MainTxt = "Result text."
    $ CurLocDesc = MainTxt
    call stat
    $ main_ui_restore_room_scene_state()
    call ReturnToMainUI
    return
```

Rules:
- Use `vscene`/`SceneActionPanel` for the picture and left-panel text.
- Use `MenuItem` actions through `scene_panel_*_item` for the right panel.
- Use `Call`, `Jump`, `Function`, `SetVariable` style actions instead of blocking `menu:` when the right panel must remain intact.
- Use `content_screen` only when a custom right-panel screen is needed; `current_action_panel` renders it with Ren'Py `use expression`.
- Do not create gameplay threads for event flow. Ren'Py UI changes should happen through labels, screen actions, interaction callbacks, and `renpy.restart_interaction()`.
