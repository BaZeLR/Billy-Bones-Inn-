# Francheska talk logic ported from textLocRef/FrancheskaTalk.txt.
# Static dialogue text lives in FrancheskaTalkData.rpy; this label owns choices and consequences.

label FrancheskaTalk:
    $ renpy.dynamic("_fran_text", "_fran_topic_index", "_fran_talking")
    $ Francheska.mark_known()
    $ main_ui_begin_talk_state("Что обсудить с Франческой?", "fran")
    $ _fran_talking = True

    while _fran_talking:
        menu:
            "Порасспрашивать об этом месте" if not Francheska.met and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran2.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[0] + "\n\n" + FRANCHESKA_TALK_MAIN[0]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.met = True
                $ Francheska.mark_talked(1)

            "Порасспрашивать Франческу о богине Эллоне" if Francheska.met and not Francheska.asked_about_ellona and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/stories.png"
                $ _fran_text = FRANCHESKA_TALK_START[1] + "\n\n" + FRANCHESKA_TALK_MAIN[1]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_ellona = True
                $ Francheska.mark_talked(1)

            "Порасспрашивать Франческу о грациях" if Francheska.asked_about_ellona and Francheska.graces_stage == 0 and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/stories.png"
                $ _fran_text = FRANCHESKA_TALK_START[2] + "\n\n" + FRANCHESKA_TALK_MAIN[2]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.graces_stage = 1
                $ Francheska.mark_talked(1)

            "Узнать больше о грациях" if Francheska.graces_stage == 1 and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/agla1.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[10] + "\n\n" + FRANCHESKA_TALK_MAIN[10]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.graces_stage = 2
                $ Francheska.mark_talked(1)

            "Порасспрашивать Франческу о герцогине" if Francheska.met and not Francheska.asked_about_duchess and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran4.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[3] + "\n\n" + FRANCHESKA_TALK_MAIN[3]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_duchess = True
                $ Francheska.mark_talked(1)

            "Спросить Франческу о герцоге" if Francheska.asked_about_duchess and not Francheska.asked_about_duke and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran4.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[4] + "\n\n" + FRANCHESKA_TALK_MAIN[4]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_duke = True
                $ Francheska.mark_talked(1)

            "Узнать больше о предателе" if Francheska.asked_about_duke and not Francheska.asked_about_stark and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran4.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[5] + "\n\n" + FRANCHESKA_TALK_MAIN[5]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_stark = True
                $ Francheska.mark_talked(1)

            "Порасспрашивать Франческу о герцогстве" if Francheska.asked_about_duchess and not Francheska.asked_about_duchy and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran4.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[6] + "\n\n" + FRANCHESKA_TALK_MAIN[6]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_duchy = True
                $ Francheska.mark_talked(1)

            "Узнать больше о короле" if Francheska.asked_about_duchy and not Francheska.asked_about_king and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran4.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[7] + "\n\n" + FRANCHESKA_TALK_MAIN[7]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_king = True
                $ Francheska.mark_talked(1)

            "Узнать больше об отношениях с королевством" if Francheska.asked_about_king and not Francheska.asked_about_kingdom_relations and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran4.jpg"
                $ _fran_text = FRANCHESKA_TALK_START[8] + "\n\n" + FRANCHESKA_TALK_MAIN[8]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_kingdom_relations = True
                $ Francheska.mark_talked(1)

            "Расспросить про нелюдей" if Francheska.asked_about_duchy and not Francheska.asked_about_aliens and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/aliens.png"
                $ _fran_text = FRANCHESKA_TALK_START[9] + "\n\n" + FRANCHESKA_TALK_MAIN[9]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.asked_about_aliens = True
                $ Francheska.mark_talked(1)

            "Поболтать с Франческой" if Francheska.asked_about_kingdom_relations and Francheska.asked_about_aliens and Francheska.asked_about_stark and Francheska.graces_stage == 2 and int(Francheska.talked_today or 0) < 3:
                vscene "images/ellona/Fran4.jpg"
                $ _fran_topic_index = procedural_randint(0, 10, key="procedural:NPC/Secondary/IntFrancheskaTalk.rpy:random_topic")
                $ _fran_text = FRANCHESKA_TALK_SECOND[_fran_topic_index] + "\n\n" + FRANCHESKA_TALK_MAIN[_fran_topic_index]
                $ scene_runtime.text = _fran_text
                "[_fran_text]"
                $ Francheska.mark_talked(1)

            "Закончить разговор":
                $ _fran_talking = False

    $ main_ui_end_talk_state()
    return
