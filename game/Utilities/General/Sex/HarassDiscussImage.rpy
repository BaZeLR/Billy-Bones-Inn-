# ================================================================================
# Harassment discussion picture selection.
# ================================================================================

label HarassDiscussImage(girl="", value=0):
    $ _hdi_girl = str(girl or "")
    $ _hdi_value = int(value or 0)
    $ _hdi_picture = ""
    if _hdi_girl == "melissa":
        if _hdi_value == 0:
            $ _hdi_picture = build_media_ref(_hdi_girl, "grope", "scoldangry")
        elif _hdi_value == 1:
            $ _hdi_picture = build_media_ref(_hdi_girl, "grope", "scoldneutral")
        else:
            $ _hdi_picture = build_media_ref(_hdi_girl, "grope", "scoldok")
    elif _hdi_girl == "amanda":
        $ _hdi_picture = build_media_ref(_hdi_girl, "grope", "scold")

    if str(_hdi_picture or "").strip():
        $ scene_image = str(_hdi_picture or "")
        $ _layout_last_picture = scene_image
        vscene scene_image
    return
