# game/Events/HouseholdMiniEvents.rpy

label HouseholdEvent_Try(location_code="", mode="room"):
    $ renpy.dynamic("_household_event", "_household_label")

    $ _household_event = household_ai_pick_event(location_code, mode)

    if _household_event == "":
        return

    if household_ai_seen(_household_event, location_code):
        return

    $ household_ai_mark_seen(_household_event, location_code)
    $ _household_label = household_ai_event_label(_household_event)

    if _household_label != "":
        call expression _household_label

    return


label HouseholdEvent_KitchenAmandaSandraSpark:
    $ main_ui_begin_native_scene_state("Аманда и Сандра на кухне")
    show screen main_ui
    vscene "images/amanda/kitchen_help.png"

    $ scene_runtime.text = "На кухне и без того жарко, и не только из-за огня в очаге."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    "Сандра стоит у стола и что-то записывает с таким лицом, будто до конца завтрака всем еще прибавится работы."

    "Сандра: Если этот дом собирается выжить, кто-то здесь должен помнить о дисциплине."

    "Аманда отрывается от своего дела и поднимает взгляд."

    "Аманда: Забавно. Дисциплина почему-то всегда значит, что у нас руки заняты, а у тебя рот свободен."

    "Мелисса едва не смеется, но вовремя прячет улыбку за кружкой."

    "Сандра: Следи за языком."

    "Улыбка Аманды становится острее."

    "Аманда: Я и слежу. В этом-то и проблема."

    "На мгновение вся кухня замирает."

    menu:
        "Велеть Аманде вернуться к работе":
            "Аманда слушается, но взгляд у нее остается злым."
            $ household_ai_reduce_drive("amanda", 0.20)
            $ household_ai_raise_friction(0.06)

        "Сказать Сандре, чтобы она перестала ее заводить":
            "Сандра медленно закрывает тетрадь."
            "Сандра: Значит, теперь проблема во мне?"
            $ household_ai_reduce_drive("sandra", 0.15)
            $ household_ai_raise_friction(0.08)

        "Напомнить обеим, что трактир важнее перепалок":
            "Довольной не выглядит ни одна из них, но смысл до обеих доходит."
            $ household_ai_raise_convergence(0.08)
            $ household_ai_reduce_drive("amanda", 0.12)
            $ household_ai_reduce_drive("sandra", 0.12)

    $ main_ui_end_native_scene_state()
    return


label HouseholdEvent_KitchenMelissaPracticalComplaint:
    $ renpy.dynamic("_melissa_food", "_melissa_wine", "_melissa_forest_food", "_melissa_supplied", "_melissa_needs", "_melissa_need", "_melissa_comfort", "_melissa_reply", "_melissa_bonus")
    $ main_ui_begin_native_scene_state("Мелисса на кухне")
    show screen main_ui
    vscene MelissaStaticData.image_path("kitchen", "work")
    python:
        _melissa_food = int(player.tavern_management.productnum)
        _melissa_wine = int(player.tavern_management.winenum)
        _melissa_forest_food = any(tavern_kitchen_food_stock_count(item_id) > 0 for item_id in ("berries_001", "mushroom_001", "honey_comb_001", "boar_meat_001")) or tavern_kitchen_bear_bonus_active()
        _melissa_supplied = _melissa_food + tavern_kitchen_food_stock_count() >= 100
    "Мелисса пересчитывает припасы на кухне, сверяет мешки и полки, затем заглядывает в записи о вине."
    menu:
        "Выслушать Мелиссу":
            pass
    if not _melissa_supplied:
        "«Провизии осталось мало. Нельзя бесконечно делать вид, будто все в порядке», — Мелисса кивает в сторону полок. «Нужно пополнить запас, а не ждать, пока кончится последний мешок»."
    else:
        "«С провизией сейчас порядок, запас есть», — Мелисса удовлетворенно кивает, закончив подсчет. «Можно готовить спокойно, а не придумывать, чем заменить половину продуктов»."
    menu:
        "Продолжить":
            pass
    if _melissa_forest_food:
        "«И лесная добыча пригодилась. Ягоды, грибы, мед или мясо — это уже не одна и та же похлебка каждый день. Хорошо, что ты относишь добытое на кухню»."
        menu:
            "Продолжить":
                pass
    if _melissa_food > 100 and _melissa_wine >= 500 and "melissa_full_storeroom" not in tractir_progress.activated_achievements and "melissa_full_storeroom" not in tractir_progress.achieved:
        "«Больше ста порций провизии и не меньше пятидесяти бочонков вина!» Мелисса еще раз сверяет записи. «Вот теперь действительно полная кладовая»."
        menu:
            "Продолжить":
                pass
        if household_morning_issue_type("melissa") in ("sick", "sleepy") or Melissa.energy < 35:
            "Мелисса устало улыбается. «Спасибо. Сегодня сил совсем мало, но хоть о пустых полках не надо беспокоиться». Она ненадолго присаживается, прижимая к себе тетрадь."
        elif Melissa.rel >= 11 and Melissa.corruption >= 20 and Melissa.arousal_value() >= 35:
            vscene MelissaStaticData.image_path("portrait", "happy")
            "Мелисса оглядывается на дверь, берет вас за ворот и притягивает ближе. «За такие запасы полагается особая благодарность». Она целует вас, задержавшись рядом дольше обычного, и лукаво шепчет: «Не все же мне только бочки считать… Но на кухне нас сейчас поймают»."
        elif Melissa.rel >= 11 and Melissa.corruption >= 20:
            vscene MelissaStaticData.image_path("portrait", "happy")
            "Мелисса неторопливо поправляет вам воротник, с улыбкой проведя пальцами по вашей груди поверх рубашки. «У хорошего хозяина и благодарность должна быть приятной. Остальную пока запишем в долг», — добавляет она с озорным видом."
        elif Melissa.rel >= 8:
            vscene MelissaStaticData.image_path("portrait", "happy")
            "Мелисса краснеет, но все-таки приподнимается на носки и быстро целует вас в щеку. «Это за то, что заботишься о нас. Только не зазнавайся», — просит она, пряча улыбку."
        else:
            "Мелисса сдержанно благодарит вас. «Запасы хорошие. Когда хозяин помнит о доме, это заметно». В ее голосе становится теплее, но фамильярничать она пока не собирается."
        menu:
            "Продолжить":
                pass
        $ tractir_activate_achievement("melissa_full_storeroom")
        call TractirShowPendingAchievements
        vscene MelissaStaticData.image_path("kitchen", "work")
    "«Считать я умею. И еще умею помнить, кому помогают первым», — замечает Мелисса, откладывая записи."
    menu:
        "Пообещать разобраться с припасами":
            $ _melissa_reply = "provide"
            if _melissa_supplied:
                "«Тогда продолжай так же. Видно, что за хозяйством следят», — Мелисса немного расслабляется."
            else:
                "«Хорошо. Я жду продукты, а не только обещание», — отвечает Мелисса, показывая вам почти опустевшие полки."
            $ household_ai_raise_convergence(0.06)
            $ household_ai_reduce_drive("melissa", 0.15)
        "Сказать, чтобы справлялась с тем, что есть":
            $ _melissa_reply = "make_do"
            "Мелисса ничего не отвечает, но лицо у нее становится холоднее."
            $ Melissa.comfort_interaction_score -= 1
            $ Melissa.trust = max(0, Melissa.trust - 1)
            $ household_ai_raise_friction(0.08)
        "Спросить, что ей нужнее всего":
            $ _melissa_reply = "needs"
            "Мелисса: Сначала безопасность. Потом удобство. После этого со всеми становится куда проще иметь дело."
            menu:
                "Выслушать, что осталось сделать":
                    pass
            python:
                _melissa_needs = []
                _melissa_comfort = Melissa.comfort_components
                if not _melissa_supplied:
                    _melissa_needs.append("Сначала пополни провизию: в кладовой уже мало продуктов.")
                if not _melissa_comfort["rats"]:
                    _melissa_needs.append("Избавь нас от крыс в кладовой. Они портят припасы, а мне приходится с ними возиться.")
                if not _melissa_comfort["room"]:
                    _melissa_needs.append("Доведи до конца ремонт моей комнаты и крыши. Я хочу спать спокойно, без шума и щелей над кроватью.")
                if not _melissa_comfort["yard"]:
                    _melissa_needs.append("Приведи в порядок двор: ходить по грязи и разбитым дорожкам надоело.")
                if not _melissa_comfort["toilet"]:
                    _melissa_needs.append("И нужник нужно починить. Это не прихоть, а самое необходимое удобство.")
                if int(player.chores.weekly.get("clean_upstairs_rooms", 0)) <= 0:
                    _melissa_needs.append("На этой неделе наверху еще не убирались. Нужна чистая комната, а не новый слой пыли.")
                if not _melissa_comfort["bathroom_laundry"]:
                    _melissa_needs.append("Прачечная с теплой купальней тоже очень нужна: стирать и мыться хочется по-человечески.")
            if _melissa_needs:
                while _melissa_needs:
                    $ _melissa_need = _melissa_needs.pop(0)
                    "Мелисса: [_melissa_need]"
                    menu:
                        "Продолжить":
                            pass
            else:
                "«Из того, о чем я просила, все сделано. Теперь просто поддерживай порядок», — Мелисса довольно улыбается."
            $ household_ai_raise_convergence(0.04)
    if _melissa_reply != "make_do" and _melissa_supplied:
        $ _melissa_bonus = 1 + int(_melissa_forest_food)
        $ Melissa.comfort_interaction_score += _melissa_bonus
        $ Melissa.trust = min(20, Melissa.trust + _melissa_bonus)
    menu:
        "Закончить разговор":
            pass
    $ main_ui_end_native_scene_state()
    return


label HouseholdEvent_BreakfastSquirrelMockery:
    $ main_ui_begin_native_scene_state("Разговор за завтраком")
    show screen main_ui
    vscene BREAKFAST_GIRLS_TEASE_PICTURE

    $ scene_runtime.text = "Завтрак начинается с мелких звуков, коротких взглядов и такой тишины, которую никак не назовешь мирной."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    "Аманда: Ну что, кто сегодня притворяется невинной?"

    "Мелисса: Смотря кто старается сильнее всех."

    "Аманда смеется."

    "Сандра переводит взгляд с одной девушки на другую."

    "Сандра: Ешьте. Работайте. Потом разговаривайте."

    "Аманда: Вот. Домашняя проповедь началась."

    "Мелисса постукивает ложкой по миске."

    "Мелисса: Осторожнее. Когда трактир беднеет, проповеди становятся длиннее."

    menu:
        "Дать им еще немного поддеть друг друга":
            "За столом становится шумнее, но никто не уходит."
            $ household_ai_raise_friction(0.06)

        "Оборвать разговор":
            "Наступившая тишина выходит хуже шума."
            $ household_ai_raise_friction(0.04)
            $ household_ai_reduce_drive("sandra", 0.10)

        "Перевести разговор в рабочие планы":
            "Они ворчат, но разговор становится полезнее."
            $ household_ai_raise_convergence(0.08)

    $ main_ui_end_native_scene_state()
    return


label HouseholdEvent_AmandaPrivatePressure:
    $ main_ui_begin_native_scene_state("Разговор с Амандой")
    show screen main_ui
    vscene "images/amanda/amanda_portrait.jpg"

    $ scene_runtime.text = "Аманда находит повод оказаться рядом, когда поблизости больше никого нет."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    "Прямо она не просит. Это было бы слишком просто."

    "Аманда: Ты всегда замечаешь, чего не хватает трактиру."

    "Она делает шаг ближе."

    "Аманда: А замечаешь, чего не хватает мне?"

    menu:
        "Спросить, чего она хочет":
            "Аманда: Смотря что ты можешь себе позволить. Внимание дешевое. Красивые вещи — нет."
            $ household_ai_reduce_drive("amanda", 0.16)

        "Сказать, что она выпрашивает поблажки":
            "Аманда улыбается, но не слишком доброжелательно."
            "Аманда: Тогда, может, научись лучше наживку подбирать."
            $ household_ai_raise_friction(0.05)

        "Сказать, что поговорите потом":
            "Она принимает это плохо, но все-таки принимает."
            $ household_ai_raise_friction(0.04)

    $ main_ui_end_native_scene_state()
    return


label HouseholdEvent_SandraPrivateCheck:
    $ main_ui_begin_native_scene_state("Разговор с Сандрой")
    show screen main_ui
    vscene "images/sandra/portrait2.jpg"

    $ scene_runtime.text = "Сандра появляется в самый неподходящий момент и с лицом человека, который прекрасно это понимает."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    "Сандра: Я хотела посмотреть, ты управляешь домом или дом уже управляет тобой."

    "Она оглядывается, ни в чем не обвиняя вас прямо, и от этого становится только хуже."

    menu:
        "Спросить, чего она на самом деле хочет":
            "Сандра: Порядка. Безопасности. И чтобы девчонки не рвали друг друга на части из-за объедков."
            $ household_ai_reduce_drive("sandra", 0.15)
            $ household_ai_raise_convergence(0.05)

        "Напомнить ей, что управляете здесь вы":
            "Сандра: Тогда управляй."
            $ household_ai_raise_friction(0.06)

        "Попросить ее помочь с девчонками":
            "Сандра долго смотрит на вас."
            "Сандра: Тогда перестань награждать беспорядок."
            $ household_ai_raise_convergence(0.06)

    $ main_ui_end_native_scene_state()
    return


label HouseholdEvent_ThreeWomenConverge:
    $ main_ui_begin_native_scene_state("Трактирная команда")
    show screen main_ui
    vscene "images/tavern/mainhall/tavern_crew.jpg"

    $ scene_runtime.text = "На этот раз никто не начинает утро со ссоры."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    "У Сандры есть записи, у Мелиссы — цифры, у Аманды — возражения, но все трое смотрят на одну и ту же проблему."

    "Сандра: Если дом устоит, все будут сыты."

    "Мелисса: Если все сыты, все ведут себя лучше."

    "Аманда: Только не надо делать вид, будто это так благородно. Свою долю я все равно хочу."

    "Сандра почти улыбается."

    "Сандра: Хорошо. Если хочешь долю, значит, собираешься остаться."

    menu:
        "Сказать, что так дом и выживает":
            "На редкое мгновение все трое, кажется, принимают это."
            $ household_ai_raise_convergence(0.12)

        "Пообещать награды, когда трактир поднимется":
            "Аманде нравится слово «награды». Мелиссе нравится слово «когда». Сандре нравится слово «поднимется»."
            $ household_ai_raise_convergence(0.10)

    $ main_ui_end_native_scene_state()
    return
