init python:
    SANDRA_WEEKLY_WAKE_THREAD_NAME = "sandraWeeklyEvaluation"
    SANDRA_WEEKLY_WAKE_STAT_GAINS = (
        {"friends": 1, "otkroven": 1, "sluttiness": 1},
        {"friends": 1, "otkroven": 1, "sluttiness": 2},
        {"friends": 1, "otkroven": 2, "sluttiness": 3},
        {"friends": 2, "otkroven": 2, "sluttiness": 4},
    )
    SANDRA_WEEKLY_WAKE_TEXTS = (
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

    def sandra_weekly_wake_thread():
        try:
            return threads.get(SANDRA_WEEKLY_WAKE_THREAD_NAME)
        except Exception:
            return None

    def sandra_weekly_wake_step():
        thread = sandra_weekly_wake_thread()
        if thread is None:
            return 0
        try:
            return max(0, min(int(thread.num or 0), len(SANDRA_WEEKLY_WAKE_TEXTS) - 1))
        except Exception:
            return 0

    def sandra_weekly_wake_target_label():
        thread = sandra_weekly_wake_thread()
        if thread is None:
            return "sandraWeeklyEvaluation_0"
        try:
            if getattr(thread, "completed", False) or getattr(thread, "aborted", False):
                return ""
            return str(thread.currentTarget() or "")
        except Exception:
            return "sandraWeeklyEvaluation_0"

    def sandra_week5_scene_picture_path(step_index=0):
        step = max(0, int(step_index or 0))
        picture_sets = (
            [
                "images/sandra/player_room_sandra_0.jpg",
                "images/sandra/talk_0.png",
            ],
            [
                "images/sandra/thanks/player_room_1.jpg",
                "images/sandra/thanks/player_room_sandra_1.png",
                "images/sandra/player_room_sandra_0.jpg",
            ],
            [
                "images/sandra/thanks/player_room_sandra_1.png",
                "images/sandra/thanks/player_room_1.jpg",
                "images/sandra/player_room_sandra_0.jpg",
            ],
            [
                "images/player_room/sandra_thanks.mp4",
                "images/sandra/thanks/player_room_sandra_1.png",
                "images/sandra/thanks/player_room_1.jpg",
            ],
        )
        candidates = picture_sets[min(step, len(picture_sets) - 1)]
        for picture_path in candidates:
            try:
                if renpy.loadable(picture_path):
                    return picture_path
            except Exception:
                pass
        return ""

    def sandra_week5_talk_picture_path():
        for picture_path in (
            "images/sandra/talk_0.png",
            "images/sandra/player_room_sandra_0.jpg",
        ):
            try:
                if renpy.loadable(picture_path):
                    return picture_path
            except Exception:
                pass
        return ""

    def sandra_week5_apply_step_gains(step_index=0):
        step = max(0, min(int(step_index or 0), len(SANDRA_WEEKLY_WAKE_STAT_GAINS) - 1))
        gains = dict(SANDRA_WEEKLY_WAKE_STAT_GAINS[step] or {})
        Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + int(gains.get("friends", 0) or 0))
        otkroven["sandra"] = min(20, int(otkroven.get("sandra", 0) or 0) + int(gains.get("otkroven", 0) or 0))
        sluttiness["sandra"] = min(100, int(sluttiness.get("sandra", 0) or 0) + int(gains.get("sluttiness", 0) or 0))


label SandraWeek5WakeEvent(return_label="TavernMain"):
    $ _sandra_target_label = str(sandra_weekly_wake_target_label() or "")
    if _sandra_target_label == "":
        return
    call expression _sandra_target_label pass (return_label,)
    return


label SandraWeek5WakeEventScene(step_index=0, return_label="TavernMain"):
    $ _sandra_step = max(0, int(step_index or 0))
    $ SandraVar["Week5WakePending"] = 0
    $ SandraVar["RoomUnlocked"] = 1
    $ _sandra_weekly_score = int((SandraVar or {}).get("WeeklyChoreCheckScore", 0) or 0)
    $ _sandra_scene_picture = str(sandra_week5_scene_picture_path(_sandra_step) or "")
    if _sandra_scene_picture != "":
        $ scene_image = _sandra_scene_picture
        $ _layout_last_picture = _sandra_scene_picture
        call ShowImage("", "", _sandra_scene_picture)

    if _sandra_step == 0:
        $ SandraVar["MCVisitFirstReady"] = 1
        $ SandraVar["MCVisitFirstDone"] = 1
    $ SandraVar["MCVisitFirstPending"] = 0
    $ sandra_week5_apply_step_gains(_sandra_step)
    $ _sandra_scene_lines = list(SANDRA_WEEKLY_WAKE_TEXTS[_sandra_step] or [])
    "[_sandra_scene_lines[0]]"
    $ _sandra_talk_picture = str(sandra_week5_talk_picture_path() or "")
    if _sandra_talk_picture != "" and _sandra_talk_picture != _sandra_scene_picture:
        $ scene_image = _sandra_talk_picture
        $ _layout_last_picture = _sandra_talk_picture
        call ShowImage("", "", _sandra_talk_picture)
    "[_sandra_scene_lines[1]]"
    if _sandra_weekly_score >= 6 and _sandra_step < 3:
        "\"И да, я заметила, что на этот раз ты вытянул неделю особенно крепко,\" добавляет Сандра уже тише. \"Такое не пропускают мимо глаз.\""
    "[_sandra_scene_lines[2]]"
    "[_sandra_scene_lines[3]]"
    return


label sandraWeeklyEvaluation_0(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeek5WakeEventScene(0, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return


label sandraWeeklyEvaluation_1(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeek5WakeEventScene(1, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return


label sandraWeeklyEvaluation_2(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeek5WakeEventScene(2, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return


label sandraWeeklyEvaluation_3(return_label="TavernMain"):
    $ thread = threads["sandraWeeklyEvaluation"]
    call SandraWeek5WakeEventScene(3, return_label)
    $ thread.day = int(dayspassed or 0)
    $ thread.advance()
    return
