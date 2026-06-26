# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowCurrentCockState(DudeName="You", DudeNameFull="", DudeNameFull2=""):
    python:
        if not DudeNameFull:
            DudeNameFull = DudeName
        if not DudeNameFull2:
            DudeNameFull2 = DudeNameFull

        is_you = str(DudeName).lower() == "you"
        if is_you:
            _cock_intimacy = player_state(False).intimacy
            cur_arousal = _cock_intimacy.arousal_value("You")
            cur_came = int(_cock_intimacy.came_today or 0)
            cur_limit = max(1, int(_cock_intimacy.can_cum_daily or 1))
        else:
            _cock_actor = getPersonInfo(DudeName)
            if _cock_actor is not None:
                _cock_state = _cock_actor.ensure_sex_state()
                cur_arousal = int(_cock_actor.arousal_value() or 0)
                cur_came = int(_cock_state.get("came_today", 0) or 0)
                cur_limit = max(1, int(_cock_state.get("can_cum_daily", 1) or 1))
            else:
                cur_arousal = 0
                cur_came = 0
                cur_limit = 1

    if str(DudeName).lower() == "you":
        if cur_came >= cur_limit:
            "То что упало - подняться не может. По крайней мере сегодня. Вот завтра силы к вам, быть может, вернутся."
            $ player_state(False).intimacy.set_arousal(0, "You")
            $ player_state(False).intimacy.apply_to_store()
        else:
            if cur_arousal < 20:
                "Вы спокойны. Ваш член какой-то вялый."
            elif cur_arousal < 40:
                "Вы возбуждены. У вас хороший стояк."
            elif cur_arousal < 65:
                "Вы сильно возбуждены. У вас мощный стояк."
            elif cur_arousal < 85:
                "Вы очень близки к оргазму. Ваш член так и норовит выдать струю спермы."
            elif cur_arousal < 100:
                "Вы на грани оргазма. Вы еле-еле сдерживаете рвущийся на ружу поток семени."
            else:
                "Вы кончаете!"
                $ player_record_orgasm("arousal")
    else:
        if cur_came >= cur_limit:
            "[DudeNameFull] совсем выдохся, бедолага. Сомнительно, чтобы его боец еще раз смог подняться для новой схватки. По крайней мере сегодня."
            $ _cock_actor = getPersonInfo(DudeName)
            if _cock_actor is not None:
                $ _cock_actor.set_arousal(0)
        else:
            if cur_arousal < 20:
                "Член [DudeNameFull2] какой-то вялый."
            elif cur_arousal < 40:
                "У [DudeNameFull2] хороший стояк, он возбужден."
            elif cur_arousal < 65:
                "[DudeNameFull] сильно возбужден. У него стоит колом."
            elif cur_arousal < 85:
                "[DudeNameFull] очень близок к оргазму. Его член так и норовит выдать струю спермы."
            elif cur_arousal < 100:
                "[DudeNameFull] на грани оргазма. Он едва сдерживает рвущийся на ружу поток семени."
            else:
                "[DudeNameFull] кончает!"
    return


label show_current_cock_state(dude_name="You", dude_name_full="", dude_name_full2=""):
    call ShowCurrentCockState(dude_name, dude_name_full, dude_name_full2)
    return
