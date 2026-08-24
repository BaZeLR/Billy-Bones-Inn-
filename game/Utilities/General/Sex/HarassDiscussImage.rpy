# ================================================================================
# Harassment discussion picture selection.
# ================================================================================

label HarassDiscussImage(girl="", value=0, _hdi_girl="", _hdi_value=0, _hdi_picture=""):
    $ _hdi_girl = str(girl or "")
    $ _hdi_value = int(value or 0)
    $ _hdi_picture = ""
    if _hdi_girl == "melissa":
        if _hdi_value == 0:
            $ _hdi_picture = MelissaStaticData.image_path("grope", "scold_angry")
        elif _hdi_value == 1:
            $ _hdi_picture = MelissaStaticData.image_path("grope", "scold_neutral")
        else:
            $ _hdi_picture = MelissaStaticData.image_path("grope", "scold_agree")
    elif _hdi_girl == "amanda":
        $ _hdi_picture = build_media_ref(_hdi_girl, "grope", "scold")

    if str(_hdi_picture or "").strip():
        $ scene_runtime.picture = str(_hdi_picture or "")
        vscene scene_runtime.picture
    return
