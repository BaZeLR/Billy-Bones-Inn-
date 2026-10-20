# Optional developer-only asset browser. It owns no story or NPC state.
# Open from the Ren'Py console with: renpy.call_in_new_context("npc_sprite_library_preview")
label npc_sprite_library_preview:
    call screen npc_sprite_library_browser
    if _return == "dialogue_demo":
        call npc_sprite_dialogue_demo
        jump npc_sprite_library_preview
    return

screen npc_sprite_library_browser():
    modal True
    zorder 300
    default npc_id = "amanda"
    default group = "expressions"
    default background_color = "#252a30"

    add Solid(background_color)
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1800
        ysize 1000
        background None
        vbox:
            spacing 14
            text "NPC sprite library — static PNGs" size 36 color "#ffffff"
            hbox:
                spacing 22
                for code, caption in (("amanda", "Amanda"), ("clara", "Clarissa"), ("melissa", "Melissa"), ("sandra", "Sandra")):
                    textbutton caption action SetScreenVariable("npc_id", code) selected (npc_id == code)
                null width 45
                textbutton "Close" action Return()
            hbox:
                spacing 22
                for category in ("expressions", "home", "boudoir", "gestures"):
                    textbutton category.capitalize() action SetScreenVariable("group", category) selected (group == category)
                textbutton "Dialogue demo" action Return("dialogue_demo")
                textbutton "Dark background" action SetScreenVariable("background_color", "#252a30")
                textbutton "Light background" action SetScreenVariable("background_color", "#e2d9ca")

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                ymaximum 800
                vpgrid:
                    cols 4
                    spacing 18
                    for state, path in NPC_SPRITE_PREVIEW[npc_id][group]:
                        vbox:
                            xsize 410
                            spacing 6
                            add Transform(path, xysize=(400, 300 if group == "expressions" else 650), fit="contain")
                            text state size 24 color ("#ffffff" if background_color == "#252a30" else "#20252b") xalign 0.5
