# Four one-time morning visits. ThreadInfo owns progress and the day marker.
# Text below formats the user's supplied scene, without extending its content.

label AmandaMorningWindowArrival(picture, opening):
    $ main_ui_begin_native_scene_state("Аманда у окна")
    show screen main_ui
    vscene "images/tavern/secondfloor/second_floor.png"
    $ scene_runtime.text = "Аманды нет за завтраком. Вы поднимаетесь наверх проверить, не заболела ли она. В коридоре слышатся странные влажные звуки и приглушённые стоны. Дверь её комнаты чуть приоткрыта."
    menu:
        "Войти":
            pass
    $ Amanda.wear_night_clothes(2)
    vscene picture
    $ scene_runtime.text = opening
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Со стороны окна доносится ещё один звук. Аманда на миг косится туда и снова смотрит на вас."
    menu:
        "Посмотреть в окно":
            pass
    $ scene_runtime.text = tavern_amanda_room_window_scene_text()
    menu:
        "Посмотреть на Аманду":
            pass
    return


label story_amanda_room_morning_window_0:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_004.jpeg", "Аманда лежит на кровати, кое-как прикрывшись одеялом. Увидев вас, она резко прижимает его к груди.\n\n«Ой, мессир! Стучаться надо!»")
    $ scene_runtime.text = "«Ты и сама любишь подглядывать и развлекаться тайком, а других извращенцами зовёшь?» — спрашиваете вы. Аманда краснеет, но не отворачивается: «Потише. Мелисса за стеной услышит»."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "«Прости, что не вышла к завтраку», — говорит Аманда. Но взгляд её уже скользнул ниже вашего пояса."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Вы оставляете её одну и возвращаетесь на кухню."
    menu:
        "Вернуться на кухню":
            pass
    $ household_clear_morning_issue("amanda")
    $ Amanda.change_social(corruption_delta=1)
    $ Amanda.wear_day_clothes()
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    jump TavernKitchen


label story_amanda_room_morning_window_1:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_003.jpeg", "На этот раз Аманда почти не пытается прикрыться. Она медленно облизывает палец и наблюдает за вашей реакцией.")
    $ scene_runtime.text = "«Мессир, вы ведь не рассказали Сандре, чем я тут занимаюсь. Оставим это между нами?» — спрашивает она и подмигивает."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Вы снова уходите. Штаны заметно теснее, чем были по дороге сюда."
    menu:
        "Вернуться на кухню":
            pass
    $ player.intimacy.add_arousal(10)
    $ Amanda.trust = min(100, int(Amanda.trust or 0) + 1)
    $ Amanda.add_arousal(4)
    $ household_clear_morning_issue("amanda")
    $ Amanda.wear_day_clothes()
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    jump TavernKitchen


label story_amanda_room_morning_window_2:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_002.jpeg", "Сегодня Аманда встречает вас улыбкой и нарочно откидывает одеяло с груди.")
    $ scene_runtime.text = "«Мелисса говорит, что мои сиськи слишком маленькие. А тебе нравятся, Стефан? У тебя от них встаёт?»"
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Аманда хохочет. «Ладно, ладно, знаю: я плохая девчонка и опять опоздала к завтраку. Но тут куда веселее! Видел, как сосед свою жену трахает? Счастливая парочка. Я почти завидую. Судя по твоим штанам, ты тоже»."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Она снова смеётся, а вы уходите. Ильматер всемогущий, до чего же она бесстыжая маленькая чертовка."
    menu:
        "Вернуться на кухню":
            pass
    $ player.intimacy.add_arousal(10)
    $ Amanda.add_arousal(5)
    $ household_clear_morning_issue("amanda")
    $ Amanda.wear_day_clothes()
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ threads["amandaMorningWood"].forceEnable()
    $ threads["amandaMorningWood"].setDay()
    $ main_ui_end_native_scene_state()
    jump TavernKitchen


label story_amanda_room_morning_window_3:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_001.jpeg", "На этот раз Аманда лежит на кровати голой и словно ждёт вас.\n\n«Привет, мессир. Не стесняйся. Давай вместе! Покажи, что прячешь в штанах!»")
    $ scene_runtime.text = "Показать ей или отказаться?"
    menu:
        "Показать":
            $ scene_runtime.text = "«Ого, да ты совсем извёлся!» — Аманда громко смеётся."
        "Не показывать":
            $ scene_runtime.text = "«Ты такой же стеснительный, как Мелисса. Только ей нравятся девчонки», — дразнит вас Аманда."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "«Вместе, значит? Поэтому ты заперла дверь?» — спрашиваете вы.\n\n«Нет, чтобы такие извращенцы, как ты, не лезли!» — хихикает Аманда. «У девочек полно секретов»."
    menu:
        "Продолжить":
            pass
    if Melissa.drawings_found:
        $ scene_runtime.text = "Вы напоминаете ей о найденной у Мелиссы книжице. Аманда мигом замолкает.\n\n«Но это ведь тоже наш секрет? Про книжицу поговорим потом, да?»"
        menu:
            "Продолжить":
                pass
    if (Amanda.harass_instruction() == "notallow" and Amanda.corruption < 45) or (Amanda.harass_instruction() == "" and Amanda.corruption < 30):
        $ scene_runtime.text = "«И что за лицемерие? Почему бы тебе не получать удовольствие и заодно не помогать трактиру?» — спрашиваете вы.\n\nАманда сердито отворачивается. Вы уходите, понимая, что без извинения она это не забудет."
        $ Amanda.change_anger(1, "morning_window_clients_argument")
        menu:
            "Продолжить":
                pass
    vscene "images/amanda/Room/Masturbation/amanda_bedroomAPI.webp"
    $ scene_runtime.text = "Вы снова оставляете её одну."
    menu:
        "Вернуться на кухню":
            pass
    $ Amanda.add_arousal(5)
    $ Amanda.change_rebellion(-1 if procedural_random("amanda_morning_window_listen") < 0.5 else 1, "morning_window_listen")
    $ household_clear_morning_issue("amanda")
    $ Amanda.wear_day_clothes()
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    jump TavernKitchen


label story_amanda_morning_wood_0:
    $ main_ui_begin_native_scene_state("Аманда: ранний визит")
    show screen main_ui
    vscene player_room_image_path("wake_up")
    $ scene_runtime.text = "Ранним утром Аманда тихо пробралась к вам в комнату. Она задерживает взгляд на вашем теле, пытаясь понять, проснулись ли вы."
    menu:
        "Продолжить утро":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
