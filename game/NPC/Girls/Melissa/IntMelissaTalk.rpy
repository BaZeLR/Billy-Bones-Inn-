# ================================================================================
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
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def melissa_start_total_progress():
        return max(0, _melissa_int(MelissaVar.get("StartTotal", 0), 0))

    def melissa_relationship_stage(girl_name="melissa"):
        key = str(girl_name or "melissa").strip().lower()
        friend_value = _melissa_int(Friends.get(key, 0), 0)
        open_value = _melissa_int(otkroven.get(key, 0), 0)
        corruption_value = _melissa_int(sluttiness.get(key, 0), 0)
        start_progress = melissa_start_total_progress()

        stage = 0
        if friend_value >= 5 and (open_value >= 2 or corruption_value >= 5):
            stage = 1
        if friend_value >= 10 and (open_value >= 4 or corruption_value >= 8):
            stage = 2
        if start_progress >= 3 or (friend_value >= 13 and (open_value >= 7 or corruption_value >= 14)):
            stage = 3
        if (
            _melissa_int(MelissaVar.get("sex_engine_unlocked", 0), 0) == 1
            or (
                melissa_bats_stage() >= 8
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
            _melissa_int(MelissaVar.get("private_context_day", -1), -1) == _melissa_int(dayspassed, 0)
            and str(MelissaVar.get("private_context_origin", "") or "").strip() == room_key
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
            _melissa_int(Arousal.get(key, 0), 0),
            _melissa_int(PussyWetStart.get(key, 0), 0),
            _melissa_int(MelissaVar.get("private_place_heat", 0), 0),
        )
        return wet_value >= 35 or _melissa_int(sluttiness.get(key, 0), 0) >= 24

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

        friend_value = int(Friends.get(key, 0) or 0)
        slut_value = int(sluttiness.get(key, 0) or 0)
        open_value = int(otkroven.get(key, 0) or 0)
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
        if int(MelissaVar.get("StartDay", -1) or -1) != int(dayspassed or 0):
            return 0
        return max(0, min(5, int(MelissaVar.get("StartCount", 0) or 0)))

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
        if melissa_bats_stage() >= 4 and melissa_bats_stage() < 8:
            lines.append("Она все еще заметно лучше держится рядом с вами, когда разговор заходит о ее комнате и чердаке над ней.")
        if int(Friends.get(key, 0) or 0) >= 15:
            lines.append("Доверия между вами уже достаточно, чтобы Мелисса не принимала каждое прикосновение за угрозу.")
        return "\n\n".join(lines)


label IntMelissaTalk(girl_name="melissa"):
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ current_action_title = "Разговор с Мелиссой"
    $ current_action_content = None
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Мелисса вопросительно смотрит на вас, ожидая продолжения разговора."
        $ CurLocDesc = MainTxt
    call IntMelissaTalkRefresh(girl_name)
    return


label IntMelissaTalkRefresh(girl_name="melissa"):
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ current_action_title = "Разговор с Мелиссой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, girl_name, CurLoc)))
    $ current_action_items.extend(social_core_action_items(girl_name, "IntMelissaTalkRefresh"))
    if melissa_storage_thanks_available():
        $ current_action_items.append(MenuItem("Послушать, что Мелисса скажет о кладовой", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "storage_thanks")))
    if clara_paintings_melissa_question_ready() and int(AskedToday.get(girl_name, 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Спросить Мелиссу о найденных рисунках", Call("story_clara_paintings_melissa_0")))
    if melissa_bats_completion_ready():
        $ current_action_items.append(MenuItem(melissa_bat_completion_talk_caption(), Function(main_ui_call_label, "MelissaBatsCompletionScene")))
    elif story_event_available(str(CurLoc or ""), "melissa_talk"):
        $ current_action_items.append(MenuItem(melissa_bat_completion_talk_caption(), Call("checkTriggers", CurLoc, "melissa_talk", 0)))
    if melissa_relationship_allows(girl_name, "intimacy") and melissa_room_is_private(CurLoc):
        $ current_action_items.append(MenuItem("Уединиться с Мелиссой", Function(main_ui_call_label, "IntMelissaSex", girl_name, CurLoc)))
    elif melissa_relationship_allows(girl_name, "intimacy") and bool(melissa_private_place_offer(girl_name, CurLoc).get("ok", False)):
        $ current_action_items.append(MenuItem("Найти укромное место с Мелиссой", Function(main_ui_call_label, "IntMelissaFindPrivatePlace", girl_name, CurLoc)))
    elif melissa_relationship_allows(girl_name, "start") and int(MelissaVar.get("StartDay", -1) or -1) != int(dayspassed or 0):
        $ current_action_items.append(MenuItem("Сблизиться с Мелиссой", Function(main_ui_call_label, "IntMelissaStartMenu", girl_name)))
    if str(CurLoc or "") == "TavernMain" and str(getLocation("clara") or "") == "TavernMain" and int(MelissaVar.get("AskedAboutClaraDay", -1) or -1) != int(dayspassed or 0) and int(AskedToday.get(girl_name, 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Спросить Мелиссу о Клариссе", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "ask_clara")))
    if int(AskedToday.get(girl_name, 0) or 0) == 0 and household_special_talk_available(girl_name):
        $ _melissa_special_entry = household_special_talk_entry(girl_name)
        if _melissa_special_entry is not None:
            $ current_action_items.append(MenuItem(str(_melissa_special_entry.get("label", "Спросить о чем-то важном") or "Спросить о чем-то важном"), Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "insight")))

    if Talked.get(girl_name, 0) < 3 and Friends.get(girl_name, 0) < 5:
        $ current_action_items.append(MenuItem("Попробовать помириться с Мелиссой", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "reconcile")))

    if Friends.get(girl_name, 0) > 8 and CheckDailyEventExists("", "BuyDressTom") == 0 and CheckDailyEventExists(girl_name, "BuyDress") == 0 and Talked.get(girl_name, 0) < 2 and week != 6:
        $ current_action_items.append(MenuItem("Предложить купить Мелиссе обновку", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "buy_dress")))
    if int(AskedToday.get(girl_name, 0) or 0) == 0 and int(Friends.get(girl_name, 0) or 0) >= 15:
        $ current_action_items.append(MenuItem("Спросить, что для нее сейчас важнее всего", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "priorities")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntMelissaTalkApply(girl_name="melissa", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "Вы подошли к Мелиссе и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
        if renpy.random.randint(1, 3) == 1:
            $ MainTxt += "\n\nМелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что очень дорожит вами и все понимает!"
            call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
        else:
            $ MainTxt += "\n\nМелисса холодно выслушала вас, презрительно отвернулась и пошла прочь."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "talk":
        $ _talk_result = player_talk_to(girl_name)
        $ MainTxt = str(_talk_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "flirt":
        $ _flirt_result = player_flirt_with(girl_name)
        $ MainTxt = str(_flirt_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "buy_dress":
        call IntMelissaDressChange(girl_name)
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_clara":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ MelissaVar["AskedAboutClaraDay"] = int(dayspassed or 0)
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Вы осторожно расспрашиваете Мелиссу о Клариссе. Мелисса с улыбкой признается, что Кларисса любит заглядывать к вам не только ради болтовни, а еще потому, что у вас в трактире ей заметно свободнее дышится. «Она хорошая, просто привыкла скрывать это за светскими манерами», - тихо добавляет Мелисса."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "storage_thanks":
        $ MelissaVar["StorageThanksDay"] = int(dayspassed or 0)
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Мелисса сама возвращается к теме кладовой и уже без колкости благодарит вас за помощь. \"Когда знаешь, что с этой дрянью внизу не придется возиться одной, работать куда легче,\" говорит она. Потом, помедлив, добавляет, что если крысы опять полезут к мешкам, она скорее позовет вас сразу, чем будет молча злиться."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "room_problem":
        call IntMelissaRoomProblemAdviceMenu(girl_name)
        return

    if str(choice_code or "") == "attic_findings":
        $ MelissaVar["AtticFindingsDay"] = int(dayspassed or 0)
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ MelissaVar["bat_recipe_clue_seen"] = 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Вы рассказываете Мелиссе, что на чердаке над ее комнатой нашли старое гнездовище: помет, клочья сухого мха и целую дрянную колонию под самой крышей. Мелисса заметно бледнеет, но теперь хотя бы слышит не пустое утешение, а понятный ответ.\n\n\"Значит, я не выдумывала,\" тихо говорит она. Потом, уже чуть спокойнее, добавляет: \"Если их можно выкурить дымом из трав, лаванды и мха, так и сделаем. Только потом щели надо будет заделать по-настоящему, иначе все вернется. Может, в той старой книге с рецептами есть что-то похожее, если ее хорошенько разобрать.\""
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "insight":
        $ _special_entry = household_special_talk_entry(girl_name)
        if _special_entry is None:
            call IntMelissaTalkRefresh(girl_name)
            return
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ household_advance_special_talk(girl_name)
        $ MainTxt = str(_special_entry.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "priorities":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Вы спрашиваете Мелиссу, что для нее сейчас важнее всего. Она на миг задумывается, потом отвечает спокойно и неожиданно открыто.\n\n\"Чтобы в доме было тише и ровнее. Чтобы можно было работать без постоянной ругани и чтобы меня не дергали по пустякам. Но еще мне важно знать, что меня здесь слушают, а не просто считают одной из рабочих рук,\" говорит Мелисса, поднимая на вас внимательный взгляд."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    return


label IntMelissaStartMenu(girl_name="melissa"):
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ current_action_title = "Сближение с Мелиссой"
    $ current_action_content = None
    $ current_action_items = []
    $ MainTxt = melissa_start_intro_text(girl_name)
    $ CurLocDesc = MainTxt
    if melissa_start_scene_remaining() <= 0:
        $ current_action_items.append(MenuItem("На сегодня хватит", Function(main_ui_call_label, "IntMelissaTalkRefresh", girl_name)))
        return
    if melissa_start_action_available(girl_name, "caress"):
        $ current_action_items.append(MenuItem("Осторожно приласкать ее", Call("IntMelissaStartApply", girl_name, "caress")))
    if melissa_start_action_available(girl_name, "kiss"):
        $ current_action_items.append(MenuItem("Поцеловать ее", Call("IntMelissaStartApply", girl_name, "kiss")))
    if melissa_start_action_available(girl_name, "deepkiss"):
        $ current_action_items.append(MenuItem("Поцеловать ее глубже", Call("IntMelissaStartApply", girl_name, "deepkiss")))
    if melissa_start_action_available(girl_name, "fondle"):
        $ current_action_items.append(MenuItem("Позволить рукам стать смелее", Call("IntMelissaStartApply", girl_name, "fondle")))
    if melissa_start_action_available(girl_name, "underclothes"):
        $ current_action_items.append(MenuItem("Пустить руки под одежду", Call("IntMelissaStartApply", girl_name, "underclothes")))
    $ current_action_items.append(MenuItem("Остановиться на сегодня", Function(main_ui_call_label, "IntMelissaTalkRefresh", girl_name)))
    return


label IntMelissaStartApply(girl_name="melissa", start_action=""):
    $ _melissa_start_action = str(start_action or "").strip()
    $ _melissa_scene_count = melissa_start_scene_count() + 1
    $ MelissaVar["StartDay"] = int(dayspassed or 0)
    $ MelissaVar["StartCount"] = _melissa_scene_count
    $ MelissaVar["StartTotal"] = max(int(MelissaVar.get("StartTotal", 0) or 0), 0) + 1
    if _melissa_start_action == "underclothes":
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ sluttiness[girl_name] = min(100, int(sluttiness.get(girl_name, 0) or 0) + 3)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 2)
        $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
        $ MainTxt = "Ваши руки скользят уже смелее, под ткань и вдоль теплой кожи. Мелисса вздрагивает, судорожно выдыхает вам в плечо и все же не останавливает, только шепотом просит не заходить дальше, чем она сейчас готова выдержать."
    elif _melissa_start_action == "deepkiss":
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ sluttiness[girl_name] = min(100, int(sluttiness.get(girl_name, 0) or 0) + 2)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 2)
        $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
        $ MainTxt = "Поцелуй становится заметно глубже и дольше. Мелисса отвечает уже не из одной только осторожности: сперва несмело, потом все горячее, будто сама удивляется тому, как быстро перестает считать секунды."
    elif _melissa_start_action == "kiss":
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ sluttiness[girl_name] = min(100, int(sluttiness.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
        $ MainTxt = "Вы не спешите и сначала просто касаетесь ее руки. Мелисса не отстраняется, а когда вы осторожно целуете ее, отвечает коротко, неловко, но уже без прежней настороженности."
    elif _melissa_start_action == "fondle":
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ sluttiness[girl_name] = min(100, int(sluttiness.get(girl_name, 0) or 0) + 2)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
        $ MainTxt = "Вы держитесь мягко, но позволяете себе чуть больше близости, чем раньше. Мелисса краснеет, шепотом просит не давить на нее и все же остается рядом, явно запоминая это как шаг, который она сама разрешила."
    else:
        $ sluttiness[girl_name] = min(100, int(sluttiness.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
        $ MainTxt = "Вы осторожно прикасаетесь к Мелиссе, будто заранее давая ей возможность остановить вас. Она тихо выдыхает, смотрит в сторону и почти неслышно говорит, что так можно."
    if melissa_start_honey_bonus_active():
        $ sluttiness[girl_name] = min(100, int(sluttiness.get(girl_name, 0) or 0) + 1)
        $ MainTxt = str(MainTxt or "") + "\n\nПохоже, медовые сладости за общим столом все еще делают ее заметно мягче и отзывчивее."
    if _melissa_scene_count < 5:
        $ MainTxt = str(MainTxt or "") + "\n\nНа сегодня между вами остается место еще для нескольких осторожных шагов, если не ломать этот ритм."
    else:
        $ MainTxt = str(MainTxt or "") + "\n\nПосле нескольких таких шагов подряд вы оба все же останавливаетесь на сегодня, чтобы не спугнуть то доверие, которое только-только между вами укрепилось."
    $ CurLocDesc = MainTxt
    if _melissa_scene_count < 5:
        call IntMelissaStartMenu(girl_name)
    else:
        call IntMelissaTalkRefresh(girl_name)
    return


label IntMelissaFindPrivatePlace(girl_name="melissa", source_room=""):
    $ _melissa_private_offer = melissa_private_place_offer(girl_name, source_room)
    if not bool(_melissa_private_offer.get("ok", False)):
        $ MainTxt = "Здесь слишком открыто, а Мелисса сейчас не готова сама искать место, где вас не увидят."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return
    $ MelissaVar["private_context_day"] = int(dayspassed or 0)
    $ MelissaVar["private_context_origin"] = str(source_room or CurLoc or "")
    $ MelissaVar["private_context_place"] = str(_melissa_private_offer.get("place", "") or "")
    $ MainTxt = str(_melissa_private_offer.get("text", "") or "Мелисса сама находит место в стороне, где вы можете остаться без чужих взглядов.")
    $ CurLocDesc = MainTxt
    call IntMelissaSex(girl_name, source_room)
    return


label IntMelissaRoomProblemAdviceMenu(girl_name="melissa"):
    $ MelissaVar["RoomProblemAskDay"] = int(dayspassed or 0)
    $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = []
    $ _stage = melissa_bats_stage()
    $ _holes_seen = 1 if _stage >= 3 else 0
    $ _temp_room = str(MelissaVar.get("temp_room", "") or "").strip()
    if _holes_seen <= 0:
        $ MainTxt = "Ночью, когда в трактире наконец становится тихо, вы спрашиваете Мелиссу о том, что творится у нее под крышей. Она сперва молчит, будто решает, не отмахнуться ли и на этот раз, но потом устало выдыхает и все-таки рассказывает все как есть.\n\nПод потолком снова шуршат летучие мыши, по балкам будто кто-то бегает почти до рассвета, а в щелях и пыли все сильнее чувствуется затхлая сырость. \"Я уже не знаю, что бесит сильнее: шум, вонь или то, что после такой ночи утром стоишь как пьяная,\" признается она.\n\nНа этот раз Мелисса не уходит в сторону и не язвит. Она смотрит прямо на вас, явно ожидая не пустого утешения, а нормального ответа."
        $ MainTxt = str(MainTxt or "") + "\n\nСначала надо осмотреть ее комнату как следует, а уже потом лезть на чердак."
        $ current_action_items.append(MenuItem("Сказать, что вы сами разберетесь с этим", Function(main_ui_call_label, "IntMelissaRoomProblemAdviceApply", girl_name, "solve")))
    else:
        $ MainTxt = "После осмотра комнаты все выглядит куда хуже, чем Мелиссе хотелось бы признавать вслух. Под самым потолком видны щели, доски местами подгнили, а из-за перекосившейся обшивки тянет сыростью прямо сверху.\n\n\"Вот видишь? Я же не выдумывала,\" тихо говорит Мелисса. Теперь вопрос уже не в том, есть ли там дрянь под крышей, а в том, где ей ночевать, пока вы не доберетесь до чердака и не разберетесь с этим как следует."
    if _holes_seen > 0 and _temp_room == "" and _stage < 4:
        $ current_action_items.append(MenuItem("Предложить пока ночевать у вас", Function(main_ui_call_label, "IntMelissaRoomProblemAdviceApply", girl_name, "mc_room")))
        $ current_action_items.append(MenuItem("Предложить перебраться к Аманде", Function(main_ui_call_label, "IntMelissaRoomProblemAdviceApply", girl_name, "amanda_room")))
        $ current_action_items.append(MenuItem("Предложить занять пустую комнату", Function(main_ui_call_label, "IntMelissaRoomProblemAdviceApply", girl_name, "empty_room")))
    elif _holes_seen > 0 and _temp_room != "":
        $ MainTxt = str(MainTxt or "") + "\n\nПока что Мелисса уже устроилась временно в другом месте. Теперь остается утром полезть на чердак и проверить, что творится над ее потолком."
    $ current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "IntMelissaTalkRefresh", girl_name)))
    $ CurLocDesc = MainTxt
    return


label IntMelissaRoomProblemAdviceApply(girl_name="melissa", advice_code=""):
    $ _melissa_advice = str(advice_code or "").strip()
    if _melissa_advice == "mc_room":
        $ MelissaVar["temp_room"] = "TavernMyRoom"
        $ sluttiness[girl_name] = min(100, int(sluttiness.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "На предложение перебраться пока к вам Мелисса сперва вспыхивает до самых ушей, но отказываться не спешит. \"Это... может и лучше, чем слушать эту дрянь под крышей. Только временно, пока ты не разберешься с комнатой. И без глупостей,\" добавляет она уже тише.\n\nВы подтверждаете, что сначала проверите ее комнату, потом чердак, и не оставите это на словах."
    elif _melissa_advice == "amanda_room":
        $ MelissaVar["temp_room"] = "TavernAmandaRoom"
        $ MainTxt = "На предложение уйти к Аманде Мелисса кривится почти сразу. \"Она храпит, как пьяный матрос, и пинается во сне не хуже жеребца,\" бурчит она. Но после короткой паузы все же соглашается, что это лучше, чем снова лежать под шорохом и писком.\n\nВы обещаете, что это только временная мера, пока не выясните, что именно творится под крышей."
    elif _melissa_advice == "empty_room":
        $ MelissaVar["temp_room"] = "TavernEmptyRoom"
        $ MainTxt = "Пустая комната Мелиссе совсем не по душе. \"Там холодно, сыро и так уныло, будто сразу в камеру посадили,\" признается она. Но если других вариантов не останется, она готова переждать там несколько ночей.\n\nВы говорите, что это лишь временно, а сами собираетесь осмотреть ее комнату и разобраться с чердаком."
    else:
        $ MelissaVar["AskedMCToSolveRoomProblem"] = 1
        $ MelissaVar["bats_episode"] = max(int(MelissaVar.get("bats_episode", 0) or 0), 2)
        $ MelissaVar["bat_attic_check_day"] = max(int(MelissaVar.get("bat_attic_check_day", -1) or -1), int(dayspassed or 0) + 1)
        $ MainTxt = "Вы обещаете не замазывать дело словами, а сначала проверить ее комнату, потом утром внимательно осмотреть чердак над ней, а уже после этого думать, чем выкуривать тварей и как по-настоящему заделывать щели. Услышав такой ответ, Мелисса заметно успокаивается.\n\n\"Вот это уже похоже на дело,\" тихо говорит она. \"Ладно. Если ты и правда туда полезешь, я хотя бы буду знать, что мне не чудится.\""
    $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
    if _melissa_advice in ("mc_room", "amanda_room", "empty_room"):
        $ MelissaVar["bats_episode"] = max(int(MelissaVar.get("bats_episode", 0) or 0), 3)
        $ MainTxt = str(MainTxt or "") + "\n\nВы желаете Мелиссе спокойной ночи и решаете, что утром пора наконец проверить чердак над ее комнатой."
    $ CurLocDesc = MainTxt
    call IntMelissaTalkRefresh(girl_name)
    return


label IntMelissaTalkRestore:
    $ main_ui_end_talk_state()
    return
