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
        "images/sandra/portrait2.jpg",
        "images/sandra/portrait3.jpg",
        "images/sandra/portrait4.jpg",
        "images/sandra/portrait4.jpg",
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
    $ _sandra_lines = list(SANDRA_WEEKLY_EVALUATION_TEXTS[_sandra_step] or [])
    $ main_ui_begin_native_scene_state("Визит Сандры")
    show screen main_ui
    vscene _sandra_picture
    $ scene_runtime.text = _sandra_lines[0]
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = _sandra_lines[1]
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    if int(player.chores.last_score or 0) >= 6 and _sandra_step < 3:
        $ scene_runtime.text = "\"И да, я заметила, что на этот раз ты вытянул неделю особенно крепко,\" добавляет Сандра уже тише. \"Такое не пропускают мимо глаз.\""
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
    $ scene_runtime.text = _sandra_lines[2]
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = _sandra_lines[3]
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ main_ui_end_native_scene_state()
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
    call SandraSexEngine("sandra", "TavernSandraRoom")
    $ calendar_v2.advance_minutes(30)
    if _sandra_secured_future_now:
        $ main_ui_begin_native_scene_state("Сандра")
        $ scene_runtime.picture = SandraStaticData.image_path("outfit_reward", "handjob_finish")
        if str(scene_runtime.picture or "").strip():
            vscene scene_runtime.picture
        $ scene_runtime.text = "После первого выдержанного месяца Сандра явно понимает, что может закрепиться рядом с вами не только через кухню и счета. Она мягко, но очень уверенно забирает часть вашего внимания на себя, и это уже чувствуется даже телом: на чужие постели сил остается меньше."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Закончить вечер":
                pass
        $ main_ui_end_native_scene_state()
    $ threads["sandraWeeklyEvaluation"].advance()
    $ main_ui_runtime.action_title = "Комната Сандры"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    return


label SandraSexEngine(girl_name="sandra", source_room="TavernSandraRoom"):
    $ renpy.dynamic("_sandra_sex_active", "_sandra_sex_first_thanks", "_sandra_sex_finished", "_sandra_sex_picture", "_sandra_sex_unlocked")
    $ _sandra_sex_unlocked = threads["sandraWeeklyEvaluation"].completed or int(threads["sandraWeeklyEvaluation"].num or 0) == 4
    if not _sandra_sex_unlocked:
        $ scene_runtime.text = "Сандра пока не готова к такой близости."
        $ scene_runtime.location_text = scene_runtime.text
        if str(source_room or "") == "TavernSandraRoom":
            $ main_ui_runtime.action_title = "Комната Сандры"
            $ main_ui_runtime.action_content = None
            $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
        return
    if int(Sandra.fucked_today or 0) >= 2:
        $ main_ui_begin_native_scene_state("Сандра")
        $ scene_runtime.text = "Сандра останавливает вас коротким взглядом. \"На сегодня хватит. Даже свободная жизнь не отменяет ни усталости, ни завтрашней работы.\""
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Назад":
                pass
        $ main_ui_end_native_scene_state()
        return
    $ _sandra_sex_first_thanks = not threads["sandraWeeklyEvaluation"].completed and int(threads["sandraWeeklyEvaluation"].num or 0) == 4
    $ _sandra_sex_finished = False
    $ _sandra_sex_active = True
    $ main_ui_begin_native_scene_state("Сандра")
    $ _sandra_sex_picture = SandraStaticData.image_path("outfit_reward", "handjob")
    if str(_sandra_sex_picture or "").strip():
        $ scene_runtime.picture = _sandra_sex_picture
        vscene scene_runtime.picture
    if _sandra_sex_first_thanks:
        $ scene_runtime.text = "Сандра встречает вас без обычной деловитой брони. Она закрывает дверь, коротко напоминает, что хорошая неделя в трактире заслуживает не только сухой похвалы, и сама делает шаг ближе. \"Сегодня без проповедей. Я сама решила, чего хочу.\""
    else:
        $ scene_runtime.text = "Сандра закрывает дверь и говорит уже без прежней неловкости: \"Если мы оба этого хотим, незачем делать вид, будто свободная постельная жизнь — преступление. Только завтра работу не проспи.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ player.intimacy.set_arousal(player.intimacy.arousal_value())
    $ Sandra.set_arousal(int(Sandra.sex_stat("PussyWetStart", Sandra.arousal_value() or 20) or 20))
    $ Sandra.set_cock_position("pussy")
    while _sandra_sex_active:
        menu:
            "Прижать Сандру к себе" if player.intimacy.arousal_value() < 100:
                $ player.intimacy.add_arousal(35)
                $ Sandra.add_arousal(35)
                $ scene_runtime.text = "Вы притягиваете Сандру ближе. Она не прячет ни желание, ни голос и сама задает более быстрый ритм, открыто говоря, что именно ей нравится."

            "Позволить Сандре вести" if player.intimacy.arousal_value() < 100:
                $ player.intimacy.add_arousal(45)
                $ Sandra.add_arousal(30)
                $ scene_runtime.text = "Сандра заставляет вас лечь удобнее и садится сверху. \"Вот так. Свободная жизнь тем и хороша, что женщина тоже может прямо сказать, чего хочет,\" бросает она, не замедляясь."

            "Кончить внутрь" if player.intimacy.can_cum() and player.intimacy.arousal_value() >= 100:
                $ scene_runtime.text = "В последний момент Сандра лишь крепче прижимается к вам, позволяя кончить глубоко внутри нее. Теперь именно этот выбор может привести к беременности."
                $ pregnancy_check(girl_name, "inside", 1, "Вы")
                $ _sandra_sex_finished = True
                $ _sandra_sex_active = False

            "Кончить на грудь" if player.intimacy.can_cum() and player.intimacy.arousal_value() >= 100:
                $ scene_runtime.text = "Вы выходите из Сандры в последний момент и кончаете ей на грудь. Она смотрит на следы спермы без стыда и только сухо замечает, что простыни хотя бы останутся чистыми."
                $ pregnancy_check(girl_name, "tits", 1, "Вы")
                $ _sandra_sex_finished = True
                $ _sandra_sex_active = False

            "Кончить на лицо" if player.intimacy.can_cum() and player.intimacy.arousal_value() >= 100:
                $ scene_runtime.text = "Вы выходите из Сандры и кончаете ей на лицо. Она спокойно проводит пальцами по щеке и напоминает, что утром снова будет хозяйкой кухни, сколько бы свободы ни позволила себе ночью."
                $ pregnancy_check(girl_name, "face", 1, "Вы")
                $ _sandra_sex_finished = True
                $ _sandra_sex_active = False

            "Остановиться":
                $ scene_runtime.text = "Вы останавливаетесь. Сандра принимает решение без обиды: свобода для нее означает и право начать, и право закончить без лишних оправданий."
                $ _sandra_sex_active = False

        if Sandra.arousal_value() >= 100:
            $ Sandra.record_orgasm_given()
            $ Sandra.set_arousal(20)
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nСандра срывается на хриплый стон, на миг теряет свой обычный контроль, а затем требует не останавливаться."
        $ scene_runtime.location_text = scene_runtime.text
    $ Sandra.set_cock_position("none")
    $ _sandra_sex_picture = SandraStaticData.image_path("outfit_reward", "handjob_finish")
    if str(_sandra_sex_picture or "").strip():
        $ scene_runtime.picture = _sandra_sex_picture
        vscene scene_runtime.picture
    $ calendar_v2.advance_minutes(30)
    if _sandra_sex_finished:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nПосле близости Сандра снова собирает себя в привычную строгую хозяйку, но теперь уже не притворяется, будто желание и свободная половая жизнь делают женщину хуже."
    else:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nСандра поправляет одежду и спокойно дает понять, что ваше решение ничего между вами не испортило."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить":
            pass
    $ main_ui_end_native_scene_state()
    if str(source_room or "") == "TavernSandraRoom":
        $ main_ui_runtime.action_title = "Комната Сандры"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    return
