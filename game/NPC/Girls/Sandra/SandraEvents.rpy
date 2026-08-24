# ================================================================================
# Sandra authored events.
# Event/thread availability is defined in StoryEventRuntime.rpy.
# SandraInfo owns Sandra's mutable reward state.
# ================================================================================

init python:
    SANDRA_WEEKLY_EVALUATION_STAT_GAINS = (
        {"rel": 1, "openness": 1, "corruption": 1},
        {"rel": 1, "openness": 1, "corruption": 2},
        {"rel": 1, "openness": 2, "corruption": 3},
        {"rel": 2, "openness": 2, "corruption": 4},
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


label SandraWeeklyEvaluationScene(step_index=0, return_label="TavernMain"):
    $ renpy.dynamic("_sandra_step", "_sandra_gains", "_sandra_picture", "_sandra_lines")
    $ _sandra_step = max(0, min(int(step_index or 0), len(SANDRA_WEEKLY_EVALUATION_TEXTS) - 1))
    $ _sandra_gains = dict(SANDRA_WEEKLY_EVALUATION_STAT_GAINS[_sandra_step] or {})
    $ Sandra.rel = max(0, min(20, int(Sandra.rel or 0) + int(_sandra_gains.get("rel", 0) or 0)))
    $ Sandra.openness = max(0, min(20, int(Sandra.openness or 0) + int(_sandra_gains.get("openness", 0) or 0)))
    $ Sandra.corruption = max(0, min(100, int(Sandra.corruption or 0) + int(_sandra_gains.get("corruption", 0) or 0)))
    $ _sandra_picture = SANDRA_WEEKLY_EVALUATION_PICTURES[_sandra_step]
    $ scene_runtime.picture = _sandra_picture
    call ShowImage("", "", _sandra_picture)
    $ _sandra_lines = list(SANDRA_WEEKLY_EVALUATION_TEXTS[_sandra_step] or [])
    "[_sandra_lines[0]]"
    "[_sandra_lines[1]]"
    if int(player.chores.last_score or 0) >= 6 and _sandra_step < 3:
        "\"И да, я заметила, что на этот раз ты вытянул неделю особенно крепко,\" добавляет Сандра уже тише. \"Такое не пропускают мимо глаз.\""
    "[_sandra_lines[2]]"
    "[_sandra_lines[3]]"
    return


label sandraWeeklyEvaluation_0(return_label="TavernMain"):
    call SandraWeeklyEvaluationScene(0, return_label)
    $ threads["sandraWeeklyEvaluation"].day = int(current_game_day() or 0)
    $ threads["sandraWeeklyEvaluation"].advance()
    $ threads["sandraWeeklyEvaluation"].disable()
    return


label sandraWeeklyEvaluation_1(return_label="TavernMain"):
    call SandraWeeklyEvaluationScene(1, return_label)
    $ threads["sandraWeeklyEvaluation"].day = int(current_game_day() or 0)
    $ threads["sandraWeeklyEvaluation"].advance()
    $ threads["sandraWeeklyEvaluation"].disable()
    return


label sandraWeeklyEvaluation_2(return_label="TavernMain"):
    call SandraWeeklyEvaluationScene(2, return_label)
    $ threads["sandraWeeklyEvaluation"].day = int(current_game_day() or 0)
    $ threads["sandraWeeklyEvaluation"].advance()
    $ threads["sandraWeeklyEvaluation"].disable()
    return


label sandraWeeklyEvaluation_3(return_label="TavernMain"):
    call SandraWeeklyEvaluationScene(3, return_label)
    $ threads["sandraWeeklyEvaluation"].day = int(current_game_day() or 0)
    $ threads["sandraWeeklyEvaluation"].advance()
    return


label TavernSandraNightThanksScene:
    $ renpy.dynamic("_sandra_secured_future_now")
    if int(threads["sandraWeeklyEvaluation"].num or 0) != 4 or int(calendar_v2.hour or 0) < 22 or int(calendar_v2.hour or 0) > 23:
        $ main_ui_runtime.action_title = "Комната Сандры"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
        return
    $ Sandra.rel = max(0, min(20, int(Sandra.rel or 0) + 2))
    $ Sandra.openness = max(0, min(20, int(Sandra.openness or 0) + 2))
    $ Sandra.corruption = max(0, min(100, int(Sandra.corruption or 0) + 3))
    $ Sandra.mark_asked()
    $ Sandra.mark_talked()
    $ _sandra_secured_future_now = tractir_apply_sandra_secured_future()
    $ player.change_stat("fun", 8)
    call PregnancyCheck("sandra", "inside", 1, "Вы")
    $ calendar_v2.advance_minutes(60)
    $ scene_runtime.picture = "images/sandra/thanks/player_room_sandra_1.png"
    vscene scene_runtime.picture
    $ scene_runtime.text = "Сандра встречает вас без обычной деловитой брони. Она закрывает дверь, коротко напоминает, что хорошая неделя в трактире заслуживает не только сухой похвалы, и сама делает шаг ближе.\n\nРазговор быстро становится тише и личнее. Сандра не торопится, но и не отступает: этой ночью она действительно благодарит вас как женщина, а не как строгая хозяйка кухни.\n\nКогда все заканчивается, она поправляет платье, смотрит на вас уже спокойнее и предупреждает, что завтра утром снова будет требовать порядка как ни в чем не бывало. Но теперь между вами остается куда более ясное понимание."
    if _sandra_secured_future_now:
        $ scene_runtime.text += "\n\nПосле первого выдержанного месяца Сандра явно понимает, что может закрепиться рядом с вами не только через кухню и счета. Она мягко, но очень уверенно забирает часть вашего внимания на себя, и это уже чувствуется даже телом: на чужие постели сил остается меньше."
    $ scene_runtime.location_text = scene_runtime.text
    $ threads["sandraWeeklyEvaluation"].advance()
    $ main_ui_runtime.action_title = "Комната Сандры"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    return


label SandraSexEngine(girl_name="sandra", source_room="TavernSandraRoom"):
    if not threads["sandraWeeklyEvaluation"].completed:
        $ scene_runtime.text = "Сандра пока не готова к такой близости."
        $ scene_runtime.location_text = scene_runtime.text
        if str(source_room or "") == "TavernSandraRoom":
            $ main_ui_runtime.action_title = "Комната Сандры"
            $ main_ui_runtime.action_content = None
            $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
        return
    $ player.intimacy.set_arousal(player.intimacy.arousal_value())
    $ Sandra.set_arousal(int(Sandra.sex_stat("PussyWetStart", Sandra.arousal_value() or 20) or 20))
    call ShowCurrentSex(girl_name)
    call PregnancyCheck(girl_name, "inside", 1, "Вы")
    $ Sandra.mark_fucked()
    $ calendar_v2.advance_minutes(30)
    $ scene_runtime.text = "Сандра не тратит вечер на лишние слова. Она закрывает дверь, поправляет волосы и смотрит на вас так, будто решение уже давно принято. После близости она снова собирает себя в привычную строгую хозяйку, но в голосе остается теплота, которую теперь уже невозможно спутать с обычной деловитостью."
    $ scene_runtime.location_text = scene_runtime.text
    if str(source_room or "") == "TavernSandraRoom":
        $ main_ui_runtime.action_title = "Комната Сандры"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    return
