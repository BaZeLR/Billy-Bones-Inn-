        "Извиниться перед Мелиссой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntMelissaTalk    if str(choice_code or "") == "talk":
        call TalkSystemSmallTalkMenu(girl_name)
        return

    if str(choice_code or "") == "flirt":
        call TalkSystemFlirtAttempt(girl_name)
        return
        "Извиниться перед Мелиссой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntMelissaTalk    if str(choice_code or "") == "talk":
        call TalkSystemSmallTalkMenu(girl_name)
        return

    if str(choice_code or "") == "flirt":
        call TalkSystemFlirtAttempt(girl_name)
        return
    $ current_action_items = []    $ current_action_items = []    $ current_action_items = []        "Извиниться перед Мелиссой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntMelissaTalk    if str(choice_code or "") == "talk":
        call TalkSystemSmallTalkMenu(girl_name)
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "flirt":
        call TalkSystemFlirtAttempt(girl_name)
        return
        "Извиниться перед Мелиссой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntMelissaTalk    if str(choice_code or "") == "talk":
        call TalkSystemSmallTalkMenu(girl_name)
        return

    if str(choice_code or "") == "flirt":
        call TalkSystemFlirtAttempt(girl_name)
        return
    $ current_action_items = []    $ current_action_items = []    $ current_action_items = []        "Извиниться перед Мелиссой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntMelissaTalk    if str(choice_code or "") == "talk":
        call TalkSystemSmallTalkMenu(girl_name)
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "flirt":
        call TalkSystemFlirtAttempt(girl_name)
        return
        "Извиниться перед Мелиссой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntMelissaTalk    if str(choice_code or "") == "talk":
        call TalkSystemSmallTalkMenu(girl_name)
        return

    if str(choice_code or "") == "flirt":
        call TalkSystemFlirtAttempt(girl_name)
        return
    $ current_action_items = []    $ current_action_items = []    $ current_action_items = []# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    MELISSA_INTIMACY_PRIVATE_ROOMS = {
        "TavernMelissaRoom",
        "TavernMyRoom",
        "TavernAmandaRoom",
        "TavernSandraRoom",
        "TavernEmptyRoom",
        "TavernStorage",
        "Shed",
    }

    MELISSA_INTIMACY_SECLUDED_ROOMS = {
        "Forest",
        "ForestClearing",
        "ForestDarkWoods",
        "ForestWaterfall",
        "ForestLake",
        "ForestSpring",
        "ForestCave",
        "ForestHiddenPath",
        "Backyard",
    }

    def _melissa_int(value, default=0):
        try:
            call IntMelissaTalkRefresh(girl_name)
        return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def melissa_start_total_progress():
        return max(0, _melissa_int(Melissa.var.get("StartTotal", 0), 0))

    def melissa_relationship_stage(girl_name="melissa"):
        friend_value = _melissa_int(Melissa.rel, 0)
        open_value = _melissa_int(Melissa.openness, 0)
        corruption_value = _melissa_int(Melissa.corruption, 0)
        start_progress = melissa_start_total_progress()

        stage = 0
        if friend_value >= 5 and (open_value >= 2 or corruption_value >= 5):
            stage = 1
        if friend_value >= 10 and (open_value >= 4 or corruption_value >= 8):
            stage = 2
        if start_progress >= 3 or (friend_value >= 13 and (open_value >= 7 or corruption_value >= 14)):
            stage = 3
        if (
            _melissa_int(Melissa.var.get("sex_engine_unlocked", 0), 0) == 1
            or (
                Melissa.bats_stage() >= 8
                and start_progress >= 5
                and friend_value >= 15
                and open_value >= 9
                and corruption_value >= 18
            )
        ):
            stage = 4
        return stage

    def melissa_relationship_allows(girl_name="melissa", action_code="talk"):
        action_key = str(action_code or "talk").strip().lower()
        stage = melissa_relationship_stage(girl_name)
        if action_key == "talk":
            return True
        if action_key in ("gift", "share"):
            if action_key == "gift":
                return relationship_any_gift_allowed(girl_name)
            allowed, reason = relationship_social_action_allowed(girl_name, action_key)
            return bool(allowed)
        if action_key == "flirt":
            allowed, reason = relationship_social_action_allowed(girl_name, action_key)
            return bool(allowed)
        if action_key == "start":
            return stage >= 2
        if action_key == "intimacy":
            return stage >= 3
        if action_key == "sex":
            return stage >= 4
        return False

    def melissa_private_context_active(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        return (
            _melissa_int(Melissa.var.get("private_context_day", -1), -1) == _melissa_int(current_game_day(), 0)
            and str(Melissa.var.get("private_context_origin", "") or "").strip() == room_key
        )

    def melissa_room_is_private(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if room_key in MELISSA_INTIMACY_PRIVATE_ROOMS:
            return True
        if room_key in MELISSA_INTIMACY_SECLUDED_ROOMS:
            return True
        return melissa_private_context_active(room_key)

    def melissa_wet_enough_to_find_place(girl_name="melissa"):
        key = str(girl_name or "melissa").strip().lower()
        wet_value = max(
            _melissa_int(Melissa.arousal_value(), 0),
            _melissa_int(Melissa.stats.get("PussyWetStart", 0), 0),
            _melissa_int(Melissa.var.get("private_place_heat", 0), 0),
        )
        return wet_value >= 35 or _melissa_int(Melissa.corruption, 0) >= 24

    def melissa_private_place_offer(girl_name="melissa", room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if not melissa_relationship_allows(girl_name, "intimacy"):
            return {"ok": False, "place": "", "text": ""}
        if melissa_room_is_private(room_key):
            return {"ok": True, "place": room_key, "text": ""}
        if not melissa_wet_enough_to_find_place(girl_name):
            return {"ok": False, "place": "", "text": ""}
        if room_key == "WineStore":
            return {
                "ok": True,
                "place": "wine_cellar",
                "text": "Мелисса быстро оглядывается и кивает в сторону дальнего подвальчика за винными стеллажами. Там достаточно темно и тесно, чтобы вас не видели с прилавка.",
            }
        if room_key == "MarketPlace":
            return {
                "ok": True,
                "place": "market_shelves",
                "text": "Мелисса ведет вас к глухому проходу за стеллажами и ящиками, где шум рынка остается совсем рядом, но прямых взглядов уже нет.",
            }
        if room_key in MELISSA_INTIMACY_SECLUDED_ROOMS:
            return {
                "ok": True,
                "place": room_key,
                "text": "Мелисса сама выбирает место в стороне от тропы, где ветки и тени закрывают вас от случайных глаз.",
            }
        return {"ok": False, "place": "", "text": ""}

    def melissa_start_action_available(girl_name="melissa", action_code=""):
        if not melissa_relationship_allows(girl_name, "start"):
            return False
        key = str(girl_name or "melissa").strip().lower()
        action_key = str(action_code or "").strip().lower()
        current_count = melissa_start_scene_count()
        if current_count >= 5:
            return False

        friend_value = int(Melissa.rel or 0)
        slut_value = int(Melissa.corruption or 0)
        open_value = int(Melissa.openness or 0)
        mood_bonus = 2 if melissa_start_honey_bonus_active() else 0

        if action_key == "caress":
            return True
        if action_key == "kiss":
            return current_count >= 1 or friend_value >= 13 or open_value + mood_bonus >= 8
        if action_key == "deepkiss":
            return current_count >= 1 and (friend_value >= 14 or open_value + mood_bonus >= 10 or slut_value + mood_bonus >= 12)
        if action_key == "fondle":
            return current_count >= 2 and (friend_value >= 15 or slut_value + mood_bonus >= 14)
        if action_key == "underclothes":
            return current_count >= 3 and (friend_value >= 16 or slut_value + mood_bonus >= 18 or open_value + mood_bonus >= 12)
        return False

    def melissa_start_scene_count():
        if int(Melissa.var.get("StartDay", -1) or -1) != int(current_game_day() or 0):
            return 0
        return max(0, min(5, int(Melissa.var.get("StartCount", 0) or 0)))

    def melissa_start_scene_remaining():
        return max(0, 5 - melissa_start_scene_count())

    def melissa_start_honey_bonus_active():
        try:
            return bool(tavern_kitchen_honey_bonus_active())
        except Exception:
            return False

    def melissa_start_intro_text(girl_name="melissa"):
        key = str(girl_name or "melissa").strip().lower()
        current_count = melissa_start_scene_count()
        lines = []
        if current_count <= 0:
            lines.append("Мелисса задерживает на вас взгляд дольше обычного. Между вами уже достаточно доверия, чтобы не сводить разговор только к делам, но торопиться все равно не стоит.")
        else:
            lines.append("Мелисса уже не так шарахается от вашей близости, как раньше. Похоже, сегодня она готова пройти с вами еще несколько осторожных шагов, если вы не будете давить.")
        lines.append("На сегодня у вас осталось %s спокойных, но все более смелых шага." % melissa_start_scene_remaining())
        if melissa_start_honey_bonus_active():
            lines.append("После сладких кухонных угощений Мелисса кажется чуть мягче и отзывчивее обычного.")
        if Melissa.bats_stage() >= 4 and Melissa.bats_stage() < 8:
            lines.append("Она все еще заметно лучше держится рядом с вами, когда разговор заходит о ее комнате и чердаке над ней.")
        if int(Melissa.rel or 0) >= 15:
            lines.append("Доверия между вами уже достаточно, чтобы Мелисса не принимала каждое прикосновение за угрозу.")
        return "\n\n".join(lines)


label IntMelissaTalk(girl_name="melissa"):
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ current_action_title = "Разговор с Мелиссой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items = []
    $ current_action_items = []
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Мелисса вопросительно смотрит на вас, ожидая продолжения разговора."
        $ CurLocDesc = MainTxt
    $ _melissa_special_entry = household_special_talk_entry(girl_name) if int(Melissa.asked_today or 0) == 0 and household_special_talk_available(girl_name) else None
    $ _melissa_bat_caption = Melissa.bat_completion_talk_caption()
    menu:
            "Осмотреть":
                call IntMelissaTalkApply(girl_name, "inspect")
            "Поговорить" if old_point_smalltalk_available(girl_name):
                call OldPointSmallTalkMenu(girl_name)
            "Флиртовать" if old_point_action_unlocked(girl_name, "flirt"):
                call OldPointFlirtAttempt(girl_name)
            "Подарить маленький подарок" if old_point_action_unlocked(girl_name, "gift"):
                call PlayerCardGiftToFixedTargetMenu(girl_name)
            "Коснуться ее смелее" if old_point_action_unlocked(girl_name, "kino"):
                call OldPointKinoAttempt(girl_name)
            "Извиниться перед Мелиссой" if old_point_apology_available(girl_name):
                call OldPointApology(girl_name)
            "Послушать, что Мелисса скажет о кладовой" if melissa_storage_thanks_available():
                $ Melissa.var["StorageThanksDay"] = int(current_game_day() or 0)
                $ Melissa.change_social(friend_delta=1)
                $ MainTxt = "Мелисса сама возвращается к теме кладовой и уже без колкости благодарит вас за помощь. \"Когда знаешь, что с этой дрянью внизу не придется возиться одной, работать куда легче,\" говорит она. Потом, помедлив, добавляет, что если крысы опять полезут к мешкам, она скорее позовет вас сразу, чем будет молча злиться."
                $ CurLocDesc = MainTxt
            "Спросить Мелиссу о найденных рисунках" if story_event_available("talk_melissa", "clara_paintings"):
                call checkTriggers("talk_melissa", "clara_paintings", 0)
            "[_melissa_bat_caption]" if story_event_available(str(CurLoc or ""), "melissa_talk"):
                call checkTriggers(CurLoc, "melissa_talk", 0)

            "Уединиться с Мелиссой" if melissa_relationship_allows(girl_name, "intimacy") and melissa_room_is_private(CurLoc):
                call IntMelissaSex(girl_name, CurLoc)
            "Найти укромное место с Мелиссой" if melissa_relationship_allows(girl_name, "intimacy") and bool(melissa_private_place_offer(girl_name, CurLoc).get("ok", False)):
                call IntMelissaFindPrivatePlace(girl_name, CurLoc)
            "Сблизиться с Мелиссой" if melissa_relationship_allows(girl_name, "start") and int(Melissa.var.get("StartDay", -1) or -1) != int(current_game_day() or 0):
                call IntMelissaStartMenu(girl_name)
            "Спросить Мелиссу о Клариссе" if str(CurLoc or "") == "TavernMain" and str(getLocation("clara") or "") == "TavernMain" and int(Melissa.var.get("AskedAboutClaraDay", -1) or -1) != int(current_game_day() or 0) and int(Melissa.asked_today or 0) == 0:
                $ Melissa.mark_asked()
                $ Melissa.var["AskedAboutClaraDay"] = int(current_game_day() or 0)
                $ Melissa.change_social(friend_delta=1)
                $ MainTxt = "Вы осторожно расспрашиваете Мелиссу о Клариссе. Мелисса с улыбкой признается, что Кларисса любит заглядывать к вам не только ради болтовни, а еще потому, что у вас в трактире ей заметно свободнее дышится. «Она хорошая, просто привыкла скрывать это за светскими манерами», - тихо добавляет Мелисса."
                $ CurLocDesc = MainTxt
            "[_melissa_special_entry.get('label', 'Спросить о чем-то важном')]" if _melissa_special_entry is not None:
                $ Melissa.mark_asked()
                $ Melissa.mark_talked()
                $ Melissa.change_social(friend_delta=1, open_delta=1)
                $ household_advance_special_talk(girl_name)
                $ MainTxt = str(_melissa_special_entry.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "Попробовать помириться с Мелиссой" if int(Melissa.talked_today or 0) < 3 and int(Melissa.rel or 0) < 5:
                $ MainTxt = "Вы подошли к Мелиссе и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
                if procedural_randint(1, 3, key="procedural:NPC/Girls/Melissa/IntMelissaTalk.rpy:reconcile") == 1:
                    $ MainTxt += "\n\nМелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что очень дорожит вами и все понимает!"
                    $ Melissa.change_social(friend_delta=6, open_delta=1, corruption_delta=1)
                else:
                    $ MainTxt += "\n\nМелисса холодно выслушала вас, презрительно отвернулась и пошла прочь."
                $ Melissa.mark_talked()
                $ CurLocDesc = MainTxt
            "Предложить купить Мелиссе обновку" if int(Melissa.rel or 0) > 8 and CheckDailyEventExists("", "BuyDressTom") == 0 and CheckDailyEventExists(girl_name, "BuyDress") == 0 and int(Melissa.talked_today or 0) < 2 and week != 6:
                call IntMelissaDressChange(girl_name)
            "Спросить, что для нее сейчас важнее всего" if int(Melissa.asked_today or 0) == 0 and int(Melissa.rel or 0) >= 15:
                $ Melissa.mark_asked()
                $ Melissa.mark_talked()
                $ Melissa.change_social(friend_delta=1, open_delta=1)
                $ MainTxt = "Вы спрашиваете Мелиссу, что для нее сейчас важнее всего. Она на миг задумывается, потом отвечает спокойно и неожиданно открыто.\n\n\"Чтобы в доме было тише и ровнее. Чтобы можно было работать без постоянной ругани и чтобы меня не дергали по пустякам. Но еще мне важно знать, что меня здесь слушают, а не просто считают одной из рабочих рук,\" говорит Мелисса, поднимая на вас внимательный взгляд."
                $ CurLocDesc = MainTxt
            "Назад":
                $ main_ui_end_talk_state()
                return


label IntMelissaTalkApply(girl_name="melissa", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "Вы подошли к Мелиссе и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
        if procedural_randint(1, 3, key="procedural:NPC/Girls/Melissa/IntMelissaTalk.rpy:procedural_randint:252:1") == 1:
            $ MainTxt += "\n\nМелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что очень дорожит вами и все понимает!"
            $ Melissa.change_social(friend_delta=6, open_delta=1, corruption_delta=1)
        else:
            $ MainTxt += "\n\nМелисса холодно выслушала вас, презрительно отвернулась и пошла прочь."
        $ Melissa.mark_talked()
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "buy_dress":
        call IntMelissaDressChange(girl_name)
        return

    if str(choice_code or "") == "ask_clara":
        $ Melissa.mark_asked()
        $ Melissa.var["AskedAboutClaraDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.change_social(friend_delta=1)
        $ MainTxt = "Вы осторожно расспрашиваете Мелиссу о Клариссе. Мелисса с улыбкой признается, что Кларисса любит заглядывать к вам не только ради болтовни, а еще потому, что у вас в трактире ей заметно свободнее дышится. «Она хорошая, просто привыкла скрывать это за светскими манерами», - тихо добавляет Мелисса."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "storage_thanks":
        $ Melissa.var["StorageThanksDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.change_social(friend_delta=1)
        $ MainTxt = "Мелисса сама возвращается к теме кладовой и уже без колкости благодарит вас за помощь. \"Когда знаешь, что с этой дрянью внизу не придется возиться одной, работать куда легче,\" говорит она. Потом, помедлив, добавляет, что если крысы опять полезут к мешкам, она скорее позовет вас сразу, чем будет молча злиться."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "room_problem":
        call IntMelissaRoomProblemAdviceMenu(girl_name)
        return

    if str(choice_code or "") == "attic_findings":
        $ Melissa.var["AtticFindingsDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.mark_asked()
        $ Melissa.var["bat_recipe_clue_seen"] = 1
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ MainTxt = "Вы рассказываете Мелиссе, что на чердаке над ее комнатой нашли старое гнездовище: помет, клочья сухого мха и целую дрянную колонию под самой крышей. Мелисса заметно бледнеет, но теперь хотя бы слышит не пустое утешение, а понятный ответ.\n\n\"Значит, я не выдумывала,\" тихо говорит она. Потом, уже чуть спокойнее, добавляет: \"Если их можно выкурить дымом из трав, лаванды и мха, так и сделаем. Только потом щели надо будет заделать по-настоящему, иначе все вернется. Может, в той старой книге с рецептами есть что-то похожее, если ее хорошенько разобрать.\""
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "insight":
        $ _special_entry = household_special_talk_entry(girl_name)
        if _special_entry is None:
            call IntMelissaTalk(girl_name)
            return
        $ Melissa.mark_asked()
        $ Melissa.mark_talked()
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ household_advance_special_talk(girl_name)
        $ MainTxt = str(_special_entry.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "priorities":
        $ Melissa.mark_asked()
        $ Melissa.mark_talked()
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ MainTxt = "Вы спрашиваете Мелиссу, что для нее сейчас важнее всего. Она на миг задумывается, потом отвечает спокойно и неожиданно открыто.\n\n\"Чтобы в доме было тише и ровнее. Чтобы можно было работать без постоянной ругани и чтобы меня не дергали по пустякам. Но еще мне важно знать, что меня здесь слушают, а не просто считают одной из рабочих рук,\" говорит Мелисса, поднимая на вас внимательный взгляд."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    return


label IntMelissaTalkApply(girl_name="melissa", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "Вы подошли к Мелиссе и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
        if procedural_randint(1, 3, key="procedural:NPC/Girls/Melissa/IntMelissaTalk.rpy:procedural_randint:252:1") == 1:
            $ MainTxt += "\n\nМелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что очень дорожит вами и все понимает!"
            $ Melissa.change_social(friend_delta=6, open_delta=1, corruption_delta=1)
        else:
            $ MainTxt += "\n\nМелисса холодно выслушала вас, презрительно отвернулась и пошла прочь."
        $ Melissa.mark_talked()
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "buy_dress":
        call IntMelissaDressChange(girl_name)
        return

    if str(choice_code or "") == "ask_clara":
        $ Melissa.mark_asked()
        $ Melissa.var["AskedAboutClaraDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.change_social(friend_delta=1)
        $ MainTxt = "Вы осторожно расспрашиваете Мелиссу о Клариссе. Мелисса с улыбкой признается, что Кларисса любит заглядывать к вам не только ради болтовни, а еще потому, что у вас в трактире ей заметно свободнее дышится. «Она хорошая, просто привыкла скрывать это за светскими манерами», - тихо добавляет Мелисса."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "storage_thanks":
        $ Melissa.var["StorageThanksDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.change_social(friend_delta=1)
        $ MainTxt = "Мелисса сама возвращается к теме кладовой и уже без колкости благодарит вас за помощь. \"Когда знаешь, что с этой дрянью внизу не придется возиться одной, работать куда легче,\" говорит она. Потом, помедлив, добавляет, что если крысы опять полезут к мешкам, она скорее позовет вас сразу, чем будет молча злиться."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "room_problem":
        call IntMelissaRoomProblemAdviceMenu(girl_name)
        return

    if str(choice_code or "") == "attic_findings":
        $ Melissa.var["AtticFindingsDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.mark_asked()
        $ Melissa.var["bat_recipe_clue_seen"] = 1
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ MainTxt = "Вы рассказываете Мелиссе, что на чердаке над ее комнатой нашли старое гнездовище: помет, клочья сухого мха и целую дрянную колонию под самой крышей. Мелисса заметно бледнеет, но теперь хотя бы слышит не пустое утешение, а понятный ответ.\n\n\"Значит, я не выдумывала,\" тихо говорит она. Потом, уже чуть спокойнее, добавляет: \"Если их можно выкурить дымом из трав, лаванды и мха, так и сделаем. Только потом щели надо будет заделать по-настоящему, иначе все вернется. Может, в той старой книге с рецептами есть что-то похожее, если ее хорошенько разобрать.\""
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "insight":
        $ _special_entry = household_special_talk_entry(girl_name)
        if _special_entry is None:
            call IntMelissaTalk(girl_name)
            return
        $ Melissa.mark_asked()
        $ Melissa.mark_talked()
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ household_advance_special_talk(girl_name)
        $ MainTxt = str(_special_entry.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "priorities":
        $ Melissa.mark_asked()
        $ Melissa.mark_talked()
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ MainTxt = "Вы спрашиваете Мелиссу, что для нее сейчас важнее всего. Она на миг задумывается, потом отвечает спокойно и неожиданно открыто.\n\n\"Чтобы в доме было тише и ровнее. Чтобы можно было работать без постоянной ругани и чтобы меня не дергали по пустякам. Но еще мне важно знать, что меня здесь слушают, а не просто считают одной из рабочих рук,\" говорит Мелисса, поднимая на вас внимательный взгляд."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    return


label IntMelissaTalkApply(girl_name="melissa", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "Вы подошли к Мелиссе и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
        if procedural_randint(1, 3, key="procedural:NPC/Girls/Melissa/IntMelissaTalk.rpy:procedural_randint:252:1") == 1:
            $ MainTxt += "\n\nМелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что очень дорожит вами и все понимает!"
            $ Melissa.change_social(friend_delta=6, open_delta=1, corruption_delta=1)
        else:
            $ MainTxt += "\n\nМелисса холодно выслушала вас, презрительно отвернулась и пошла прочь."
        $ Melissa.mark_talked()
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "buy_dress":
        call IntMelissaDressChange(girl_name)
        return

    if str(choice_code or "") == "ask_clara":
        $ Melissa.mark_asked()
        $ Melissa.var["AskedAboutClaraDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.change_social(friend_delta=1)
        $ MainTxt = "Вы осторожно расспрашиваете Мелиссу о Клариссе. Мелисса с улыбкой признается, что Кларисса любит заглядывать к вам не только ради болтовни, а еще потому, что у вас в трактире ей заметно свободнее дышится. «Она хорошая, просто привыкла скрывать это за светскими манерами», - тихо добавляет Мелисса."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "storage_thanks":
        $ Melissa.var["StorageThanksDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.change_social(friend_delta=1)
        $ MainTxt = "Мелисса сама возвращается к теме кладовой и уже без колкости благодарит вас за помощь. \"Когда знаешь, что с этой дрянью внизу не придется возиться одной, работать куда легче,\" говорит она. Потом, помедлив, добавляет, что если крысы опять полезут к мешкам, она скорее позовет вас сразу, чем будет молча злиться."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "room_problem":
        call IntMelissaRoomProblemAdviceMenu(girl_name)
        return

    if str(choice_code or "") == "attic_findings":
        $ Melissa.var["AtticFindingsDay"] = int(calendar_v2.daysInGame or 0)
        $ Melissa.mark_asked()
        $ Melissa.var["bat_recipe_clue_seen"] = 1
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ MainTxt = "Вы рассказываете Мелиссе, что на чердаке над ее комнатой нашли старое гнездовище: помет, клочья сухого мха и целую дрянную колонию под самой крышей. Мелисса заметно бледнеет, но теперь хотя бы слышит не пустое утешение, а понятный ответ.\n\n\"Значит, я не выдумывала,\" тихо говорит она. Потом, уже чуть спокойнее, добавляет: \"Если их можно выкурить дымом из трав, лаванды и мха, так и сделаем. Только потом щели надо будет заделать по-настоящему, иначе все вернется. Может, в той старой книге с рецептами есть что-то похожее, если ее хорошенько разобрать.\""
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "insight":
        $ _special_entry = household_special_talk_entry(girl_name)
        if _special_entry is None:
            call IntMelissaTalk(girl_name)
            return
        $ Melissa.mark_asked()
        $ Melissa.mark_talked()
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ household_advance_special_talk(girl_name)
        $ MainTxt = str(_special_entry.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    if str(choice_code or "") == "priorities":
        $ Melissa.mark_asked()
        $ Melissa.mark_talked()
        $ Melissa.change_social(friend_delta=1, open_delta=1)
        $ MainTxt = "Вы спрашиваете Мелиссу, что для нее сейчас важнее всего. Она на миг задумывается, потом отвечает спокойно и неожиданно открыто.\n\n\"Чтобы в доме было тише и ровнее. Чтобы можно было работать без постоянной ругани и чтобы меня не дергали по пустякам. Но еще мне важно знать, что меня здесь слушают, а не просто считают одной из рабочих рук,\" говорит Мелисса, поднимая на вас внимательный взгляд."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return

    return


label IntMelissaStartMenu(girl_name="melissa"):
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ current_action_title = "Сближение с Мелиссой"
    $ current_action_content = None
    while melissa_start_scene_remaining() > 0:
        $ MainTxt = melissa_start_intro_text(girl_name)
        $ CurLocDesc = MainTxt
        menu:
            "Осторожно приласкать ее" if melissa_start_action_available(girl_name, "caress"):
                $ _melissa_start_action = "caress"
            "Поцеловать ее" if melissa_start_action_available(girl_name, "kiss"):
                $ _melissa_start_action = "kiss"
            "Поцеловать ее глубже" if melissa_start_action_available(girl_name, "deepkiss"):
                $ _melissa_start_action = "deepkiss"
            "Позволить рукам стать смелее" if melissa_start_action_available(girl_name, "fondle"):
                $ _melissa_start_action = "fondle"
            "Пустить руки под одежду" if melissa_start_action_available(girl_name, "underclothes"):
                $ _melissa_start_action = "underclothes"
            "Остановиться на сегодня":
                $ current_action_title = "Разговор с Мелиссой"
                return
        $ _melissa_scene_count = melissa_start_scene_count() + 1
        $ Melissa.var["StartDay"] = int(current_game_day() or 0)
        $ Melissa.var["StartCount"] = _melissa_scene_count
        $ Melissa.var["StartTotal"] = max(int(Melissa.var.get("StartTotal", 0) or 0), 0) + 1
        if _melissa_start_action == "underclothes":
            $ Melissa.change_social(friend_delta=1, open_delta=2, corruption_delta=3)
            $ player.change_stat("fun", 3)
            $ MainTxt = "Ваши руки скользят уже смелее, под ткань и вдоль теплой кожи. Мелисса вздрагивает, судорожно выдыхает вам в плечо и все же не останавливает, только шепотом просит не заходить дальше, чем она сейчас готова выдержать."
        elif _melissa_start_action == "deepkiss":
            $ Melissa.change_social(friend_delta=1, open_delta=2, corruption_delta=2)
            $ player.change_stat("fun", 2)
            $ MainTxt = "Поцелуй становится заметно глубже и дольше. Мелисса отвечает уже не из одной только осторожности: сперва несмело, потом все горячее, будто сама удивляется тому, как быстро перестает считать секунды."
        elif _melissa_start_action == "kiss":
            $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=1)
            $ player.change_stat("fun", 2)
            $ MainTxt = "Вы не спешите и сначала просто касаетесь ее руки. Мелисса не отстраняется, а когда вы осторожно целуете ее, отвечает коротко, неловко, но уже без прежней настороженности."
        elif _melissa_start_action == "fondle":
            $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=2)
            $ player.change_stat("fun", 2)
            $ MainTxt = "Вы держитесь мягко, но позволяете себе чуть больше близости, чем раньше. Мелисса краснеет, шепотом просит не давить на нее и все же остается рядом, явно запоминая это как шаг, который она сама разрешила."
        else:
            $ Melissa.change_social(open_delta=1, corruption_delta=1)
            $ player.change_stat("fun", 1)
            $ MainTxt = "Вы осторожно прикасаетесь к Мелиссе, будто заранее давая ей возможность остановить вас. Она тихо выдыхает, смотрит в сторону и почти неслышно говорит, что так можно."
        if melissa_start_honey_bonus_active():
            $ Melissa.change_social(corruption_delta=1)
            $ MainTxt = str(MainTxt or "") + "\n\nПохоже, медовые сладости за общим столом все еще делают ее заметно мягче и отзывчивее."
        if _melissa_scene_count < 5:
            $ MainTxt = str(MainTxt or "") + "\n\nНа сегодня между вами остается место еще для нескольких осторожных шагов, если не ломать этот ритм."
        else:
            $ MainTxt = str(MainTxt or "") + "\n\nПосле нескольких таких шагов подряд вы оба все же останавливаетесь на сегодня, чтобы не спугнуть то доверие, которое только-только между вами укрепилось."
        $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Мелиссой"
    return


label IntMelissaFindPrivatePlace(girl_name="melissa", source_room=""):
    $ _melissa_private_offer = melissa_private_place_offer(girl_name, source_room)
    if not bool(_melissa_private_offer.get("ok", False)):
        $ MainTxt = "Здесь слишком открыто, а Мелисса сейчас не готова сама искать место, где вас не увидят."
        $ CurLocDesc = MainTxt
        call IntMelissaTalk(girl_name)
        return
    $ Melissa.var["private_context_day"] = int(current_game_day() or 0)
    $ Melissa.var["private_context_origin"] = str(source_room or CurLoc or "")
    $ Melissa.var["private_context_place"] = str(_melissa_private_offer.get("place", "") or "")
    $ MainTxt = str(_melissa_private_offer.get("text", "") or "Мелисса сама находит место в стороне, где вы можете остаться без чужих взглядов.")
    $ CurLocDesc = MainTxt
    call IntMelissaSex(girl_name, source_room)
    return


label IntMelissaRoomProblemAdviceMenu(girl_name="melissa"):
    $ Melissa.var["RoomProblemAskDay"] = int(dayspassed or 0)
    $ Melissa.change_social(friend_delta=1)
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items = []
    $ current_action_items = []
    $ _stage = Melissa.bats_stage()
    $ _holes_seen = 1 if _stage >= 3 else 0
    $ _temp_room = str(Melissa.var.get("temp_room", "") or "").strip()
    if _holes_seen <= 0:
        $ MainTxt = "Ночью, когда в трактире наконец становится тихо, вы спрашиваете Мелиссу о том, что творится у нее под крышей. Она сперва молчит, будто решает, не отмахнуться ли и на этот раз, но потом устало выдыхает и все-таки рассказывает все как есть.\n\nПод потолком снова шуршат летучие мыши, по балкам будто кто-то бегает почти до рассвета, а в щелях и пыли все сильнее чувствуется затхлая сырость. \"Я уже не знаю, что бесит сильнее: шум, вонь или то, что после такой ночи утром стоишь как пьяная,\" признается она.\n\nНа этот раз Мелисса не уходит в сторону и не язвит. Она смотрит прямо на вас, явно ожидая не пустого утешения, а нормального ответа."
        $ MainTxt = str(MainTxt or "") + "\n\nСначала надо осмотреть ее комнату как следует, а уже потом лезть на чердак."
        $ current_action_items.append(MenuItem("Сказать, что вы сами разберетесь с этим", Call("IntMelissaRoomProblemAdviceApply", girl_name, "solve")))
        $ current_action_items.append(MenuItem("Сказать, что вы сами разберетесь с этим", Call("IntMelissaRoomProblemAdviceApply", girl_name, "solve")))
        $ current_action_items.append(MenuItem("Сказать, что вы сами разберетесь с этим", Call("IntMelissaRoomProblemAdviceApply", girl_name, "solve")))
    else:
        $ MainTxt = "После осмотра комнаты все выглядит куда хуже, чем Мелиссе хотелось бы признавать вслух. Под самым потолком видны щели, доски местами подгнили, а из-за перекосившейся обшивки тянет сыростью прямо сверху.\n\n\"Вот видишь? Я же не выдумывала,\" тихо говорит Мелисса. Теперь вопрос уже не в том, есть ли там дрянь под крышей, а в том, где ей ночевать, пока вы не доберетесь до чердака и не разберетесь с этим как следует."
    if _holes_seen > 0 and _temp_room != "":
        $ MainTxt = str(MainTxt or "") + "\n\nПока что Мелисса уже устроилась временно в другом месте. Теперь остается утром полезть на чердак и проверить, что творится над ее потолком."
    $ CurLocDesc = MainTxt
    if _holes_seen <= 0:
        menu:
            "Сказать, что вы сами разберетесь с этим":
                $ _melissa_advice = "solve"
                $ Melissa.var["AskedMCToSolveRoomProblem"] = 1
        $ Melissa.var["AskedMCToSolveRoomProblem"] = 1
        $ Melissa.var["AskedMCToSolveRoomProblem"] = 1
        $ Melissa.var["AskedMCToSolveRoomProblem"] = 1
        $ Melissa.var["AskedMCToSolveRoomProblem"] = 1
        $ Melissa.var["AskedMCToSolveRoomProblem"] = 1
        $ Melissa.var["bats_episode"] = max(int(Melissa.var.get("bats_episode", 0) or 0), 2)
                $ Melissa.var["bat_attic_check_day"] = max(int(Melissa.var.get("bat_attic_check_day", -1) or -1), int(current_game_day() or 0) + 1)
                $ MainTxt = "Вы обещаете не замазывать дело словами, а сначала проверить ее комнату, потом утром внимательно осмотреть чердак над ней, а уже после этого думать, чем выкуривать тварей и как по-настоящему заделывать щели. Услышав такой ответ, Мелисса заметно успокаивается.\n\n\"Вот это уже похоже на дело,\" тихо говорит она. \"Ладно. Если ты и правда туда полезешь, я хотя бы буду знать, что мне не чудится.\""
            "Назад":
                $ current_action_title = "Разговор с Мелиссой"
                return
    elif _temp_room == "" and _stage < 4:
        menu:
            "Предложить пока ночевать у вас":
                $ _melissa_advice = "mc_room"
                $ Melissa.var["temp_room"] = "TavernMyRoom"
                $ Melissa.change_social(corruption_delta=1)
                $ MainTxt = "На предложение перебраться пока к вам Мелисса сперва вспыхивает до самых ушей, но отказываться не спешит. \"Это... может и лучше, чем слушать эту дрянь под крышей. Только временно, пока ты не разберешься с комнатой. И без глупостей,\" добавляет она уже тише.\n\nВы подтверждаете, что сначала проверите ее комнату, потом чердак, и не оставите это на словах."
            "Предложить перебраться к Аманде":
                $ _melissa_advice = "amanda_room"
                $ Melissa.var["temp_room"] = "TavernAmandaRoom"
                $ MainTxt = "На предложение уйти к Аманде Мелисса кривится почти сразу. \"Она храпит, как пьяный матрос, и пинается во сне не хуже жеребца,\" бурчит она. Но после короткой паузы все же соглашается, что это лучше, чем снова лежать под шорохом и писком.\n\nВы обещаете, что это только временная мера, пока не выясните, что именно творится под крышей."
            "Предложить занять пустую комнату":
                $ _melissa_advice = "empty_room"
                $ Melissa.var["temp_room"] = "TavernEmptyRoom"
                $ MainTxt = "Пустая комната Мелиссе совсем не по душе. \"Там холодно, сыро и так уныло, будто сразу в камеру посадили,\" признается она. Но если других вариантов не останется, она готова переждать там несколько ночей.\n\nВы говорите, что это лишь временно, а сами собираетесь осмотреть ее комнату и разобраться с чердаком."
            "Назад":
                $ current_action_title = "Разговор с Мелиссой"
                return
    else:
        menu:
            "Назад":
                $ current_action_title = "Разговор с Мелиссой"
                return
    $ Melissa.change_social(friend_delta=1)
    if _melissa_advice in ("mc_room", "amanda_room", "empty_room"):
        $ Melissa.var["bats_episode"] = max(int(Melissa.var.get("bats_episode", 0) or 0), 3)
        $ MainTxt = str(MainTxt or "") + "\n\nВы желаете Мелиссе спокойной ночи и решаете, что утром пора наконец проверить чердак над ее комнатой."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Мелиссой"
    return

