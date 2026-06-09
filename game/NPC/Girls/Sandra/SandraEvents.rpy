# ================================================================================
# Sandra authored events.
# Event/thread availability is defined in StoryEventRuntime.rpy.
# SandraInfo owns Sandra's mutable reward state.
# ================================================================================

init python:
    SANDRA_WEEKLY_EVALUATION_STAT_GAINS = (
        {"friends": 1, "otkroven": 1, "sluttiness": 1},
        {"friends": 1, "otkroven": 1, "sluttiness": 2},
        {"friends": 1, "otkroven": 2, "sluttiness": 3},
        {"friends": 2, "otkroven": 2, "sluttiness": 4},
    )
    SANDRA_WEEKLY_EVALUATION_PICTURES = (
        "images/sandra/player_room_sandra_0.jpg",
        "images/sandra/thanks/player_room_1.jpg",
        "images/sandra/thanks/player_room_sandra_1.png",
        "images/sandra/thanks/player_room_sandra_1.png",
    )
    SANDRA_WEEKLY_EVALUATION_TEXTS = (
        (
            "Сквозь остатки сна вы слышите осторожный стук в дверь, а затем в комнату заглядывает Сандра.",
            "\"Стефан, на этой неделе ты и правда держал хозяйство в руках,\" говорит она тихо, но уже без привычной колкости. \"Я это вижу. И мне не хочется делать вид, будто ничего не изменилось.\"",
            "\"Если вечером захочешь зайти ко мне не по хозяйству, не стой под дверью как чужой,\" добавляет она, задержав на вас взгляд чуть дольше обычного.",
            "\"Ладно, поднимайся. День уже начинается,\" бросает она напоследок и уходит, оставив после себя непривычно теплое послевкусие.",
        ),
        (
            "На этот раз Сандра входит к вам увереннее, будто уже знает, что вы не проспите ее шаги.",
            "\"Опять вытянул неделю как надо,\" говорит она, подходя ближе к кровати. \"Я заметила не только порядок в трактире. Ты и сам будто держишься собраннее, когда есть ради кого стараться.\"",
            "Она чуть усмехается, замечая ваш взгляд. \"Вечером можешь зайти. Только не вздумай делать вид, будто тебе интересны одни счета и мешки с крупой.\"",
            "\"И не опаздывай, если решишься,\" тихо добавляет Сандра, прежде чем выйти из комнаты.",
        ),
        (
            "Сандра приходит еще до того, как вы толком просыпаетесь, и останавливается уже не в дверях, а у самой кровати.",
            "\"Мне нравится, как ты в последнее время держишь дом,\" говорит она, проводя пальцами по краю покрывала. \"И нравится, как ты смотришь на меня, когда думаешь, что я этого не замечаю.\"",
            "\"Если сегодня ночью придешь, я уже не стану делать вид, что ты пришел только поболтать,\" шепчет она, позволяя фразе повиснуть между вами куда откровеннее прежнего.",
            "\"Поднимайся. Я и так задержалась дольше, чем собиралась,\" говорит Сандра, но в голосе слышится явное довольство.",
        ),
        (
            "Сандра появляется в вашей комнате так, будто давно приняла для себя решение и больше не собирается его прятать.",
            "\"Стефан, ты свой первый месяц выдержал как хозяин,\" говорит она низким, теплым голосом. \"Теперь я уже не хочу ограничиваться одними благодарностями за хозяйство.\"",
            "\"Придешь сегодня ночью тихо, без глупостей и пустого трепа,\" продолжает она, глядя вам прямо в глаза. \"И я отблагодарю тебя уже совсем не словами. Хватит нам обоим ходить вокруг да около.\"",
            "\"Запомни только одно: если зайдешь, назад дороги к прежней Сандре уже не будет,\" говорит она и уходит, оставляя вас с совершенно недвусмысленным обещанием.",
        ),
    )


label SandraWeek5WakeEvent(return_label="TavernMain"):
    $ _sandra_target_label = str(Sandra.weekly_thanks_target_label() or "")
    if _sandra_target_label == "":
        return
    call expression _sandra_target_label pass (return_label,)
    return


label SandraWeeklyEvaluationScene(step_index=0, return_label="TavernMain"):
    $ _sandra_step = max(0, min(int(step_index or 0), len(SANDRA_WEEKLY_EVALUATION_TEXTS) - 1))
    $ _sandra_gains = dict(SANDRA_WEEKLY_EVALUATION_STAT_GAINS[_sandra_step] or {})
    $ Sandra.weekly_thanks_wake_seen(_sandra_step, _sandra_gains)
    $ SandraVar = Sandra.var
    $ _sandra_picture = SANDRA_WEEKLY_EVALUATION_PICTURES[_sandra_step]
    $ scene_image = _sandra_picture
    $ _layout_last_picture = _sandra_picture
    call ShowImage("", "", _sandra_picture)
    $ _sandra_lines = list(SANDRA_WEEKLY_EVALUATION_TEXTS[_sandra_step] or [])
    "[_sandra_lines[0]]"
    "[_sandra_lines[1]]"
    if int(Sandra.weekly_chore_score or 0) >= 6 and _sandra_step < 3:
        "\"И да, я заметила, что на этот раз ты вытянул неделю особенно крепко,\" добавляет Сандра уже тише. \"Такое не пропускают мимо глаз.\""
    "[_sandra_lines[2]]"
    "[_sandra_lines[3]]"
    return


label sandraWeeklyEvaluation_0(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeeklyEvaluationScene(0, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return


label sandraWeeklyEvaluation_1(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeeklyEvaluationScene(1, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return


label sandraWeeklyEvaluation_2(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeeklyEvaluationScene(2, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return


label sandraWeeklyEvaluation_3(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeeklyEvaluationScene(3, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return


label TavernSandraNightThanksScene:
    if not Sandra.night_thanks_ready() or int(hour or 0) < 22 or int(hour or 0) > 23:
        call TavernSandraRoomBuildActions
        return
    $ Sandra.night_thanks_seen()
    $ SandraVar = Sandra.var
    $ AskedToday["sandra"] = int(AskedToday.get("sandra", 0) or 0) + 1
    $ Talked["sandra"] = int(Talked.get("sandra", 0) or 0) + 1
    $ _sandra_secured_future_now = tractir_apply_sandra_secured_future()
    $ fun = _player_clamp(int(fun or 0) + 8, 0, 100)
    call PregnancyCheck("sandra", "inside", 1, "Вы")
    $ Sandra.sync_from_sandra_maps()
    $ Sandra.save_story_state()
    $ calendar_v2.advance_minutes(60)
    $ scene_image = "images/sandra/thanks/player_room_sandra_1.png"
    $ _layout_last_picture = scene_image
    call ShowImage("", "", scene_image)
    $ MainTxt = "Сандра встречает вас без обычной деловитой брони. Она закрывает дверь, коротко напоминает, что хорошая неделя в трактире заслуживает не только сухой похвалы, и сама делает шаг ближе.\n\nРазговор быстро становится тише и личнее. Сандра не торопится, но и не отступает: этой ночью она действительно благодарит вас как женщина, а не как строгая хозяйка кухни.\n\nКогда все заканчивается, она поправляет платье, смотрит на вас уже спокойнее и предупреждает, что завтра утром снова будет требовать порядка как ни в чем не бывало. Но теперь между вами остается куда более ясное понимание."
    if _sandra_secured_future_now:
        $ MainTxt += "\n\nПосле первого выдержанного месяца Сандра явно понимает, что может закрепиться рядом с вами не только через кухню и счета. Она мягко, но очень уверенно забирает часть вашего внимания на себя, и это уже чувствуется даже телом: на чужие постели сил остается меньше."
    $ CurLocDesc = MainTxt
    call TavernSandraRoomBuildActions
    return


label SandraSexEngine(girl_name="sandra", source_room="TavernSandraRoom"):
    if not Sandra.sex_available():
        $ MainTxt = "Сандра пока не готова к такой близости."
        $ CurLocDesc = MainTxt
        if str(source_room or "") == "TavernSandraRoom":
            call TavernSandraRoomBuildActions
        return
    $ bodymodel_sync_character(girl_name, RealName.get(girl_name, "Сандра"), "female")
    $ Arousal.setdefault("You", 0)
    $ Arousal.setdefault(girl_name, int(PussyWetStart.get(girl_name, 20) or 20))
    call ShowCurrentSex(girl_name)
    call PregnancyCheck(girl_name, "inside", 1, "Вы")
    $ Sandra.fucked_today = int(Sandra.fucked_today or 0) + 1
    $ FuckedToday[girl_name] = int(FuckedToday.get(girl_name, 0) or 0) + 1
    $ Sandra.sync_from_sandra_maps()
    $ Sandra.save_story_state()
    $ Sandra.sync_sandra_maps()
    $ calendar_v2.advance_minutes(30)
    $ MainTxt = "Сандра не тратит вечер на лишние слова. Она закрывает дверь, поправляет волосы и смотрит на вас так, будто решение уже давно принято. После близости она снова собирает себя в привычную строгую хозяйку, но в голосе остается теплота, которую теперь уже невозможно спутать с обычной деловитостью."
    $ CurLocDesc = MainTxt
    if str(source_room or "") == "TavernSandraRoom":
        call TavernSandraRoomBuildActions
    return
