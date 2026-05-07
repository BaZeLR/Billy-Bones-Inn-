# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _show_current_sex_allows_kids_peek(girl_name):
        georgett_loc = str(getattr(renpy.store, "GirlLocIGSS", "") or "")
        amanda_loc = str(getattr(renpy.store, "GirlLocASDS", "") or "")
        return (not (girl_name == "georgett" and georgett_loc != "tavern")) and (not (girl_name == "amanda" and amanda_loc == "street"))

label ShowCurrentSex(GirlNameSCS=""):
    if not GirlNameSCS:
        return

    call ShowCurrentCockState("You")

    python:
        Arousal.setdefault("You", 0)
        CockInPussy.setdefault(GirlNameSCS, 0)
        CockInMouth.setdefault(GirlNameSCS, 0)
        EddieCockInPussy.setdefault(GirlNameSCS, 0)
        EddieCockInMouth.setdefault(GirlNameSCS, 0)
        sluttiness.setdefault(GirlNameSCS, 0)
        pregnancy.setdefault(GirlNameSCS, 0)
        RealName.setdefault(GirlNameSCS, GirlNameSCS)
        RealName2.setdefault(GirlNameSCS, GirlNameSCS)
        GrupenSex.setdefault("eddie", 0)
        GiveOrgasms.setdefault(GirlNameSCS, 0)
        Friends.setdefault(GirlNameSCS, 0)
        DayLastOrgasmGiven.setdefault(GirlNameSCS, 0)
        cuminside.setdefault(GirlNameSCS, 0)

    if _show_current_sex_allows_kids_peek(GirlNameSCS):
        $ KidsPeekSexCode(GirlNameSCS)

    if Arousal.get("You", 0) >= 100:
        if CockInPussy.get(GirlNameSCS, 0) == 1:
            if GirlNameSCS == "liza" and sluttiness.get(GirlNameSCS, 0) < 50 and pregnancy.get(GirlNameSCS, 0) < 120:
                "[RealName.get(GirlNameSCS, GirlNameSCS)] почувствовала что вы уже близки к оргазму. Гримаса страха промелькнула на ее смуглой мордашке."
                "\"Ой, дядя Стефан, пожалуйста, вытащите. Не кончайте в меня, прошу вас, я боюсь залететь, прошу вас, не в меня!\" - забормотала мулаточка."
            elif GirlNameSCS == "becky" and EddieCockInMouth.get(GirlNameSCS, 0) == 1:
                "[RealName.get(GirlNameSCS, GirlNameSCS)] почувствовала что вы уже близки к оргазму и что-то замычала, но что именно было не понять, член Эдди во рту мешал ей выражаться ясно и понятно."
            elif GirlNameSCS == "becky":
                "[RealName.get(GirlNameSCS, GirlNameSCS)] почувствовала что вы уже близки к оргазму  и ободряюще сказала вам:"
                "\"Стефанчик, если хочешь, то можешь кончить внутрь, это ничего.\""
            elif GirlNameSCS == "amanda" and sluttiness.get(GirlNameSCS, 0) < 60 and pregnancy.get(GirlNameSCS, 0) < 120:
                "\"Стефан, ты что, кончаешь?!\" как будто почуствовала [RealName.get(GirlNameSCS, GirlNameSCS)]. \"Только не в меня, я не хочу так залететь! Вытащи, хорошо?\""
                if cuminside.get("amanda", 0) >= 4:
                    "\"Только обязательно вытащи, а то мне уже несколько раз везло, а может ведь и не повезти!\" добавила она."
            elif GirlNameSCS == "amanda" and sluttiness.get(GirlNameSCS, 0) >= 60 and pregnancy.get(GirlNameSCS, 0) < 120:
                "\"Стефан, если ты кончаешь, то можешь в середину!\" похотливо сказала [RealName.get(GirlNameSCS, GirlNameSCS)]. \"Рано или поздно кто-то мне пузо обязательно заделает, почему бы и не ты?\""
            else:
                "[RealName.get(GirlNameSCS, GirlNameSCS)] чувствует что вы готовы кончить и нежно шепчет вам чтобы вы кончали."
        else:
            "[RealName.get(GirlNameSCS, GirlNameSCS)] чувствует что вы готовы кончить и приглашающе мычит, не прекращая сосать ваш член."

    if GrupenSex.get("eddie", 0) > 0:
        call ShowCurrentCockState("eddie", "Эдди", "Эдди")
        if Arousal.get("eddie", 0) >= 100:
            if EddieCockInPussy.get(GirlNameSCS, 0) == 1:
                if CockInMouth.get(GirlNameSCS, 0) == 1:
                    if sluttiness.get(GirlNameSCS, 0) < 65:
                        "[RealName.get(GirlNameSCS, GirlNameSCS)] почувствовала что Эдди готов вот-вот кончить и что-то с ужасом в голосе промычала, однако вы так и не вынули своего члена у нее изо рта и поэтому бедная вдова не смогла ясно выразить свою мысль."
                    else:
                        "[RealName.get(GirlNameSCS, GirlNameSCS)] почувствовала что Эдди готов вот-вот кончить и что-то промычала, но что именно было не понять, ваш член во рту мешал ей выражаться ясно и понятно."
                else:
                    if pregnancy.get(GirlNameSCS, 0) >= 120:
                        "Ребекка, почусвтвовав что Эдди уже близок к разрядке, просто сказала: \"Может кончать куда вздумается, более беременной чем сейчас ты меня все равно не сделаешь.\""
                    elif sluttiness.get(GirlNameSCS, 0) < 65:
                        "Ребекка, почусвтвовав что Эдди уже близок к разрядке, быстро забормотала: \"Эдди, миленький, только не в меня, ты слышишь?\""
                    else:
                        "Ребекка, почусвтвовав что Эдди уже близок к разрядке, страстно закричала: \"Да, кончи в меня, я хочу почувствовать как ты кончаешь!\""
            elif EddieCockInMouth.get(GirlNameSCS, 0) == 1:
                "[RealName.get(GirlNameSCS, GirlNameSCS)] чувствует что Эдди уже готов разрядиться и приглашающе мычит, продолжая сосать его член."

    if Arousal.get(GirlNameSCS, 0) < 20:
        "Киска [RealName2.get(GirlNameSCS, GirlNameSCS)] суха и зажата. Проникновение не доставит ей удовольствия."
    if Arousal.get(GirlNameSCS, 0) >= 20 and Arousal.get(GirlNameSCS, 0) < 40:
        "[RealName.get(GirlNameSCS, GirlNameSCS)] возбуждена. Её влагалище увлажнилось."
    if Arousal.get(GirlNameSCS, 0) >= 40 and Arousal.get(GirlNameSCS, 0) < 65:
        "[RealName.get(GirlNameSCS, GirlNameSCS)] хорошо возбуждена. Её киска обильна смазана собственным \"соком\""
    if Arousal.get(GirlNameSCS, 0) >= 65 and Arousal.get(GirlNameSCS, 0) < 85:
        "[RealName.get(GirlNameSCS, GirlNameSCS)] близка к оргазму. Её стоны становятся всё чаще и чаще."
    if Arousal.get(GirlNameSCS, 0) >= 85 and Arousal.get(GirlNameSCS, 0) < 100:
        "[RealName.get(GirlNameSCS, GirlNameSCS)] на грани оргазма. Каждая клеточка её киски ритмично пульсирует, а на теле местами появляются красные пятна."

    if Arousal.get(GirlNameSCS, 0) >= 100:
        "[RealName.get(GirlNameSCS, GirlNameSCS)] забилась в судорогах оргазма, все ее тело выгнулось дугой. Со счастливым вздохом и блаженной улыбкой [RealName.get(GirlNameSCS, GirlNameSCS)] кончила."
        "[RealName.get(GirlNameSCS, GirlNameSCS)] только что кончила."
        $ GiveOrgasms[GirlNameSCS] = GiveOrgasms.get(GirlNameSCS, 0) + 1

        if GirlNameSCS == "georgett":
            if GiveOrgasms.get(GirlNameSCS, 0) == 2:
                "\"Какой ты заботливый\", сказала [RealName.get(GirlNameSCS, GirlNameSCS)], с трудом отдышавшись после бурного оргазма. \"Не то, что другие, думающие только о своем удовольствии.\""
                $ Friends[GirlNameSCS] = Friends.get(GirlNameSCS, 0) + 1

        if GirlNameSCS == "liza":
            if GiveOrgasms.get(GirlNameSCS, 0) == 3:
                "\"Ой, дяденька Стефан, какой ты добрый и хороший\", заявила дрожащим от пережитого оргазма голоском [RealName.get(GirlNameSCS, GirlNameSCS)]. \"Многие дяденьки только о себе и думают, а с тобой всегда так хорошо, всегда мне удается спустить.\""
                $ Friends[GirlNameSCS] = Friends.get(GirlNameSCS, 0) + 1

        if GirlNameSCS == "becky":
            if GiveOrgasms.get(GirlNameSCS, 0) == 5:
                "\"Ну ты даешь, Стефанчик, не зря я дала себя уболтать\", томно заявила вам [RealName.get(GirlNameSCS, GirlNameSCS)]. \"С тобой я все кончаю и кончаю, знаешь ты как к женщине подойти.\""
                $ Friends[GirlNameSCS] = Friends.get(GirlNameSCS, 0) + 1

        if GirlNameSCS == "amanda":
            if GiveOrgasms.get(GirlNameSCS, 0) == 4:
                "\"Ох, Стефанчик, как же хорошо с тобой!\", довольно сказала вам [RealName.get(GirlNameSCS, GirlNameSCS)]. \"Ты такой ласковый, правильно я тебе дала!\""
                $ Friends[GirlNameSCS] = Friends.get(GirlNameSCS, 0) + 1

        if CockInPussy.get(GirlNameSCS, 0) or EddieCockInPussy.get(GirlNameSCS, 0):
            $ Arousal[GirlNameSCS] = 20
        else:
            $ Arousal[GirlNameSCS] = 0
        $ DayLastOrgasmGiven[GirlNameSCS] = dayspassed

    python:
        SomebodyCums = 0
        if isinstance(Arousal, dict):
            for _arousal_value in Arousal.values():
                if isinstance(_arousal_value, (int, float)) and _arousal_value >= 100:
                    SomebodyCums = 1
                    break
        elif isinstance(Arousal, (list, tuple)):
            for _arousal_value in Arousal:
                if isinstance(_arousal_value, (int, float)) and _arousal_value >= 100:
                    SomebodyCums = 1
                    break

    return
