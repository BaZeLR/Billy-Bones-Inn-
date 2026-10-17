# Presentation-only component for the new dialogue-window expression portraits.
# The Character aliases keep names owned by the existing NPC class instances.
screen npc_sprite_dialogue_line(who, what, text_size=None):
    $ _npc_face_tag = str(renpy.get_say_image_tag() or "")
    $ _npc_face_visible = not renpy.variant("small") and _npc_face_tag.startswith("npcface_") and renpy.get_side_image("side") is not None
    $ _npc_text_width = max(1, int((config.screen_width - 36) * 0.72) - 48 - 236)

    if _npc_face_visible:
        hbox:
            xfill True
            spacing 16
            add SideImage():
                xysize (220, 220)
                fit "contain"
            vbox:
                xsize _npc_text_width
                spacing 8
                if who is not None:
                    text who id "who" style "say_label"
                if text_size is None:
                    text what id "what" style "say_dialogue" xsize _npc_text_width
                else:
                    text what id "what" size text_size xsize _npc_text_width
    else:
        vbox:
            xfill True
            spacing 8
            if who is not None:
                text who id "who" style "say_label"
            if text_size is None:
                text what id "what" style "say_dialogue"
            else:
                text what id "what" size text_size


# Open after starting a game, using the Ren'Py developer console:
# renpy.call_in_new_context("npc_sprite_dialogue_demo")
label npc_sprite_dialogue_demo:
    npc_amanda_voice wink "Так вы слушаете меня — или просто смотрите?"
    npc_amanda_voice annoyed "Я вообще-то задала вопрос."
    npc_clara_voice playful "А может быть, он прекрасно умеет делать и то и другое."
    npc_clara_voice smiling "Хотя проверить всё-таки стоит."
    npc_melissa_voice nervous "Вы обе нарочно его смущаете?"
    npc_melissa_voice laughing "Ладно. Кажется, теперь и меня."
    npc_sandra_voice seductive "Устройтесь поудобнее. Разговор только начинается."
    npc_sandra_voice happy "Вот так гораздо лучше."
    return
