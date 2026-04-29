# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowCurrentCockState(DudeName="You", DudeNameFull="", DudeNameFull2=""):
    python:
        Arousal.setdefault(DudeName, 0)
        if not isinstance(cametoday_npc, dict):
            cametoday_npc = {}

        if not DudeNameFull:
            DudeNameFull = DudeName
        if not DudeNameFull2:
            DudeNameFull2 = DudeNameFull

        is_you = str(DudeName).lower() == "you"
        cur_arousal = int(Arousal.get(DudeName, 0) or 0)

        if is_you:
            if isinstance(cametoday, dict):
                cur_came = int(cametoday.get("You", cametoday.get("you", 0)) or 0)
            else:
                cur_came = int(cametoday or 0)

            if isinstance(cancumdaily, dict):
                cur_limit = int(cancumdaily.get("You", cancumdaily.get("you", 1)) or 1)
            else:
                cur_limit = int(cancumdaily or 1)
        else:
            cur_came = int(cametoday_npc.get(DudeName, 0) or 0)

            if isinstance(cancumdaily, dict):
                cur_limit = int(cancumdaily.get(DudeName, 1) or 1)
            else:
                cur_limit = int(cancumdaily or 1)

    if str(DudeName).lower() == "you":
        if cur_came >= cur_limit:
            "То что упало - подняться не может. По крайней мере сегодня. Вот завтра силы к вам, быть может, вернутся."
            $ Arousal[DudeName] = 0
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
    else:
        if cur_came >= cur_limit:
            "[DudeNameFull] совсем выдохся, бедолага. Сомнительно, чтобы его боец еще раз смог подняться для новой схватки. По крайней мере сегодня."
            $ Arousal[DudeName] = 0
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
