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


# One-time household conversation after Sandra accepts the player as landlord.
# The label owns every story beat, consequence, and completion point directly.
label story_sandra_kitchen_household_respect_0:
    $ renpy.dynamic("_sandra_kitchen_respect_picture")
    $ main_ui_begin_native_scene_state("Разговор на кухне")
    show screen main_ui
    $ _sandra_kitchen_respect_picture = SandraStaticData.image_path("kitchen", "work")
    if str(_sandra_kitchen_respect_picture or "").strip():
        vscene _sandra_kitchen_respect_picture
    $ scene_runtime.text = "Едва вы входите на кухню, Аманда и Мелисса наперебой жалуются Сандре на посетителей. Одни распускают руки, другие щиплют за ягодицы и делают вид, будто монета за кружку дает им право трогать служанок."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Сандра выслушивает их и отвечает строго: \"Внимание посетителей — часть работы в людном трактире, но терпеть всякую наглость вы не обязаны. Если кто-то переходит черту, говорите хозяину сразу, а не копите обиду и не устраивайте драку посреди зала.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Потом Сандра поворачивается уже к девушкам: \"И еще запомните: Стефан здесь хозяин и наш домовладелец. Его надо уважать, ценить то, что он держит этот дом, и самим давать ему достаточно тепла, чтобы он не искал ее у случайных женщин на стороне. Дом держится не только на работе, но и на внимании друг к другу.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Вы отвечаете, что подумаете, как защитить девушек от наглых рук и при этом не превратить каждый вечер в драку с посетителями. Если после происшествия кто-то из них будет по-настоящему несчастна, решение о клиенте останется за вами."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить разговор":
            pass
    $ Sandra.change_social(friend_delta=1, open_delta=1)
    $ Melissa.change_mana(1, "kitchen_landlord_respect")
    $ Amanda.change_mana(1, "kitchen_landlord_respect")
    $ calendar_v2.advance_minutes(5)
    $ event_runtime.active_thread.complete()
    $ main_ui_end_native_scene_state()
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
    call HouseholdSexEngine("sandra", "TavernSandraRoom")
    if _sandra_secured_future_now:
        $ main_ui_begin_native_scene_state("Сандра")
        $ scene_runtime.picture = SandraStaticData.image_path("outfit_reward", "handjob_finish")
        if str(scene_runtime.picture or "").strip():
            vscene scene_runtime.picture
        $ scene_runtime.text = "После первого выдержанного месяца Сандра явно понимает, что может закрепиться рядом с вами не только через кухню и счета. Она мягко, но очень уверенно дает понять, что теперь видит свое будущее рядом с вами."
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
