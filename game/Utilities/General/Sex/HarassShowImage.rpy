# ================================================================================
# Tavern harassment event picture selection.
# ================================================================================

label HarassShowImage(GirlNameHSI="", ActionHSI="", ReactionHSI=0, EyewitnessHSI=0, JobTypeHSI="", _hsi_picture="", _hsi_girl="", _hsi_action="", _hsi_reaction=0, _hsi_eyewitness=0, _hsi_info=None):
    $ _hsi_picture = ""
    $ _hsi_girl = str(GirlNameHSI or "")
    $ _hsi_action = str(ActionHSI or "")
    $ _hsi_reaction = int(ReactionHSI or 0)
    $ _hsi_eyewitness = int(EyewitnessHSI or 0)
    $ _hsi_info = people.get_info(_hsi_girl)

    if _hsi_eyewitness > 0:
        if _hsi_girl == "melissa":
            if _hsi_reaction == 0:
                if _hsi_action in ("ass", "dress"):
                    $ _hsi_picture = MelissaStaticData.image_path("grope", "ass_angry")
                else:
                    $ _hsi_picture = MelissaStaticData.image_path("grope", "tit_angry")
            elif _hsi_action in ("ass", "dress"):
                if _hsi_reaction >= 3:
                    $ _hsi_picture = MelissaStaticData.image_path("grope", "ass_ok")
                else:
                    $ _hsi_picture = MelissaStaticData.image_path("grope", "ass_angry")
            else:
                if _hsi_reaction >= 3:
                    $ _hsi_picture = MelissaStaticData.image_path("grope", "tit_ok")
                elif _hsi_reaction == 2:
                    $ _hsi_picture = MelissaStaticData.image_path("grope", "tits_shy")
                else:
                    $ _hsi_picture = MelissaStaticData.image_path("grope", "tit_angry")
        elif _hsi_girl == "amanda":
            if _hsi_reaction == 0:
                $ _hsi_picture = AmandaStaticData.image_path("grope", "intro")
            elif _hsi_action == "ass":
                if _hsi_reaction >= 3:
                    $ _hsi_picture = AmandaStaticData.cycle_image("grope", "ass_ok", procedural_randint(1, 2, "harass_amanda_ass_ok_%s" % int(current_game_day() or 0)) - 1)
                elif _hsi_reaction == 2:
                    $ _hsi_picture = AmandaStaticData.image_path("grope", "ass_shy")
                else:
                    $ _hsi_picture = AmandaStaticData.image_path("grope", "ass_angry")
            elif _hsi_action == "tits":
                if _hsi_reaction >= 3:
                    $ _hsi_picture = AmandaStaticData.cycle_image("grope", "tit_ok", procedural_randint(1, 2, "harass_amanda_tit_ok_%s" % int(current_game_day() or 0)) - 1)
                elif _hsi_reaction == 2:
                    $ _hsi_picture = AmandaStaticData.cycle_image("grope", "tits_shy", procedural_randint(1, 2, "harass_amanda_tit_shy_%s" % int(current_game_day() or 0)) - 1)
                else:
                    $ _hsi_picture = AmandaStaticData.image_path("grope", "tit_angry")
            else:
                if _hsi_info is not None and not _hsi_info.has_panties():
                    if _hsi_reaction >= 2:
                        $ _hsi_picture = AmandaStaticData.cycle_image("grope", "dress_naked", procedural_randint(1, 2, "harass_amanda_dress_naked_%s" % int(current_game_day() or 0)) - 1)
                    else:
                        $ _hsi_picture = AmandaStaticData.image_path("grope", "dress_naked_angry")
                else:
                    $ _hsi_picture = AmandaStaticData.image_path("grope", "dress_panties")
        elif _hsi_girl == "sandra":
            if JobTypeHSI == "waitress":
                $ _hsi_picture = build_media_ref(_hsi_girl, "tavern", "waitress" + str(procedural_randint(1, 4, "harass_sandra_waitress_%s" % int(current_game_day() or 0))))
            else:
                $ _hsi_picture = build_media_ref(_hsi_girl, "tavern", "cleaning1")

    if str(_hsi_picture or "").strip():
        $ scene_runtime.picture = str(_hsi_picture or "")
        vscene scene_runtime.picture
    return
