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
    $ main_ui_begin_native_scene_state("Мелисса на кухне")
    show screen main_ui
    vscene MelissaStaticData.image_path("kitchen", "work")

    $ scene_runtime.text = "Мелисса оглядывает кухню так, будто считает каждую недостающую монету и каждую грязную тарелку."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    "Мелисса: Нельзя бесконечно делать вид, будто все в порядке."

    "Она кивает в сторону полок."

    "Мелисса: Еда, чистая ткань, починка. Если с этим провалиться, все начинают не работать, а драться за поблажки."

    "Сандра: Хоть кто-то здесь умеет считать."

    "Мелисса тонко улыбается."

    "Мелисса: Считать я умею. И еще умею помнить, кому помогают первым."

    menu:
        "Пообещать разобраться с припасами":
            "Мелисса немного расслабляется."
            $ household_ai_raise_convergence(0.06)
            $ household_ai_reduce_drive("melissa", 0.15)

        "Сказать, чтобы справлялась с тем, что есть":
            "Мелисса ничего не отвечает, но лицо у нее становится холоднее."
            $ household_ai_raise_friction(0.08)

        "Спросить, что ей нужнее всего":
            "Мелисса: Сначала безопасность. Потом удобство. После этого со всеми становится куда проще иметь дело."
            $ household_ai_raise_convergence(0.04)

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
