# ================================================================================
# Shared current sex-state narration. State belongs to Player.intimacy and the
# participating PeopleInfo/Girl object.
# ================================================================================

init python:
    def _show_current_sex_allows_kids_peek(girl_name):
        girl = getPersonInfo(girl_name)
        if girl is None:
            return False
        location_code = str(getattr(girl, "location", "") or "")
        if hasattr(girl, "getLocation"):
            location_code = str(girl.getLocation() or location_code)
        if str(girl_name or "").strip().lower() == "georgett" and location_code not in ("TavernMain", "TavernKitchen", "TavernStorage", "TavernMyRoom"):
            return False
        if str(girl_name or "").strip().lower() == "amanda" and location_code == "street":
            return False
        return True

    def sex_current_name(girl, form="name"):
        if girl is None:
            return ""
        data = getattr(girl, "data", None)
        if form == "genitive" and data is not None:
            return str(getattr(data, "genitive", "") or getattr(data, "fullname", "") or getattr(girl, "name", ""))
        if hasattr(girl, "display_name"):
            return str(girl.display_name() or getattr(girl, "name", ""))
        return str(people_display_name(getattr(girl, "name", "")) or getattr(girl, "name", ""))


label ShowCurrentSex(GirlNameSCS=""):
    if not GirlNameSCS:
        return

    $ _scs_girl = getPersonInfo(GirlNameSCS)
    if _scs_girl is None:
        return

    call ShowCurrentCockState("You")

    $ _scs_intimacy = player_state(False).intimacy
    $ _scs_real_name = sex_current_name(_scs_girl)
    $ _scs_real_name2 = sex_current_name(_scs_girl, "genitive")
    $ _scs_key = str(getattr(_scs_girl, "name", GirlNameSCS) or GirlNameSCS).strip().lower()
    $ _scs_arousal_you = int(_scs_intimacy.arousal_value("You") or 0)
    $ _scs_arousal_girl = int(_scs_girl.arousal_value() or 0)
    $ _scs_corruption = int(getattr(_scs_girl, "corruption", 0) or 0)
    $ _scs_pregnancy = int(_scs_girl.pregnancy_days() or 0)
    $ _scs_cuminside = int(_scs_girl.sex_stat("cuminside", 0) or 0)
    $ _scs_you_pussy = bool(_scs_girl.cock_in("pussy", "You"))
    $ _scs_you_mouth = bool(_scs_girl.cock_in("mouth", "You"))
    $ _scs_eddie = getPersonInfo("eddie")
    $ _scs_eddie_arousal = int(_scs_eddie.arousal_value() or 0) if _scs_eddie is not None else 0
    $ _scs_eddie_pussy = bool(_scs_girl.cock_in("pussy", "eddie"))
    $ _scs_eddie_mouth = bool(_scs_girl.cock_in("mouth", "eddie"))

    if _show_current_sex_allows_kids_peek(_scs_key):
        $ KidsPeekSexCode(_scs_key)

    if _scs_arousal_you >= 100:
        if _scs_you_pussy:
            if _scs_key == "liza" and _scs_corruption < 50 and _scs_pregnancy < 120:
                "[_scs_real_name] почувствовала что вы уже близки к оргазму. Гримаса страха промелькнула на ее смуглой мордашке."
                "\"Ой, дядя Стефан, пожалуйста, вытащите. Не кончайте в меня, прошу вас, я боюсь залететь, прошу вас, не в меня!\" - забормотала мулаточка."
            elif _scs_key == "becky" and _scs_eddie_mouth:
                "[_scs_real_name] почувствовала что вы уже близки к оргазму и что-то замычала, но что именно было не понять, член Эдди во рту мешал ей выражаться ясно и понятно."
            elif _scs_key == "becky":
                "[_scs_real_name] почувствовала что вы уже близки к оргазму  и ободряюще сказала вам:"
                "\"Стефанчик, если хочешь, то можешь кончить внутрь, это ничего.\""
            elif _scs_key == "amanda" and _scs_corruption < 60 and _scs_pregnancy < 120:
                "\"Стефан, ты что, кончаешь?!\" как будто почуствовала [_scs_real_name]. \"Только не в меня, я не хочу так залететь! Вытащи, хорошо?\""
                if _scs_cuminside >= 4:
                    "\"Только обязательно вытащи, а то мне уже несколько раз везло, а может ведь и не повезти!\" добавила она."
            elif _scs_key == "amanda" and _scs_corruption >= 60 and _scs_pregnancy < 120:
                "\"Стефан, если ты кончаешь, то можешь в середину!\" похотливо сказала [_scs_real_name]. \"Рано или поздно кто-то мне пузо обязательно заделает, почему бы и не ты?\""
            else:
                "[_scs_real_name] чувствует что вы готовы кончить и нежно шепчет вам чтобы вы кончали."
        else:
            "[_scs_real_name] чувствует что вы готовы кончить и приглашающе мычит, не прекращая сосать ваш член."

    if _scs_eddie is not None and (_scs_eddie_pussy or _scs_eddie_mouth):
        call ShowCurrentCockState("eddie", "Эдди", "Эдди")
        if _scs_eddie_arousal >= 100:
            if _scs_eddie_pussy:
                if _scs_you_mouth:
                    if _scs_corruption < 65:
                        "[_scs_real_name] почувствовала что Эдди готов вот-вот кончить и что-то с ужасом в голосе промычала, однако вы так и не вынули своего члена у нее изо рта и поэтому бедная вдова не смогла ясно выразить свою мысль."
                    else:
                        "[_scs_real_name] почувствовала что Эдди готов вот-вот кончить и что-то промычала, но что именно было не понять, ваш член во рту мешал ей выражаться ясно и понятно."
                else:
                    if _scs_pregnancy >= 120:
                        "Ребекка, почусвтвовав что Эдди уже близок к разрядке, просто сказала: \"Может кончать куда вздумается, более беременной чем сейчас ты меня все равно не сделаешь.\""
                    elif _scs_corruption < 65:
                        "Ребекка, почусвтвовав что Эдди уже близок к разрядке, быстро забормотала: \"Эдди, миленький, только не в меня, ты слышишь?\""
                    else:
                        "Ребекка, почусвтвовав что Эдди уже близок к разрядке, страстно закричала: \"Да, кончи в меня, я хочу почувствовать как ты кончаешь!\""
            elif _scs_eddie_mouth:
                "[_scs_real_name] чувствует что Эдди уже готов разрядиться и приглашающе мычит, продолжая сосать его член."

    if _scs_arousal_girl < 20:
        "Киска [_scs_real_name2] суха и зажата. Проникновение не доставит ей удовольствия."
    if _scs_arousal_girl >= 20 and _scs_arousal_girl < 40:
        "[_scs_real_name] возбуждена. Её влагалище увлажнилось."
    if _scs_arousal_girl >= 40 and _scs_arousal_girl < 65:
        "[_scs_real_name] хорошо возбуждена. Её киска обильна смазана собственным \"соком\""
    if _scs_arousal_girl >= 65 and _scs_arousal_girl < 85:
        "[_scs_real_name] близка к оргазму. Её стоны становятся всё чаще и чаще."
    if _scs_arousal_girl >= 85 and _scs_arousal_girl < 100:
        "[_scs_real_name] на грани оргазма. Каждая клеточка её киски ритмично пульсирует, а на теле местами появляются красные пятна."

    if _scs_arousal_girl >= 100:
        "[_scs_real_name] забилась в судорогах оргазма, все ее тело выгнулось дугой. Со счастливым вздохом и блаженной улыбкой [_scs_real_name] кончила."
        "[_scs_real_name] только что кончила."
        $ _scs_orgasm_count = _scs_girl.record_orgasm_given()

        if _scs_key == "georgett" and _scs_orgasm_count == 2:
            "\"Какой ты заботливый\", сказала [_scs_real_name], с трудом отдышавшись после бурного оргазма. \"Не то, что другие, думающие только о своем удовольствии.\""
            $ _scs_girl.change_social(friend_delta=1)

        if _scs_key == "liza" and _scs_orgasm_count == 3:
            "\"Ой, дяденька Стефан, какой ты добрый и хороший\", заявила дрожащим от пережитого оргазма голоском [_scs_real_name]. \"Многие дяденьки только о себе и думают, а с тобой всегда так хорошо, всегда мне удается спустить.\""
            $ _scs_girl.change_social(friend_delta=1)

        if _scs_key == "becky" and _scs_orgasm_count == 5:
            "\"Ну ты даешь, Стефанчик, не зря я дала себя уболтать\", томно заявила вам [_scs_real_name]. \"С тобой я все кончаю и кончаю, знаешь ты как к женщине подойти.\""
            $ _scs_girl.change_social(friend_delta=1)

        if _scs_key == "amanda" and _scs_orgasm_count == 4:
            "\"Ох, Стефанчик, как же хорошо с тобой!\", довольно сказала вам [_scs_real_name]. \"Ты такой ласковый, правильно я тебе дала!\""
            $ _scs_girl.change_social(friend_delta=1)

        if _scs_you_pussy or _scs_eddie_pussy:
            $ _scs_girl.set_arousal(20)
        else:
            $ _scs_girl.set_arousal(0)
        $ _scs_girl.set_sex_stat("last_orgasm_day", dayspassed)

    $ _scs_any_cums = int(_scs_intimacy.arousal_value("You") >= 100 or _scs_girl.arousal_value() >= 100 or _scs_eddie_arousal >= 100)
    $ _scs_girl.set_sex_busy(_scs_any_cums)
    return
