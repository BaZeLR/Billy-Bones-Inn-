# Four one-time morning visits. ThreadInfo owns progress and the day marker.
# Text below formats the user's supplied scene, without extending its content.

label AmandaMorningWindowArrival(picture, opening):
    $ main_ui_begin_native_scene_state("Аманда у окна")
    show screen main_ui
    vscene "images/tavern/secondfloor/girls_room_day.png"
    $ scene_runtime.text = "Amanda is not at breakfast. You go to check her: you hear weird slurping noises and quiet moaning."
    menu:
        "Войти":
            pass
    $ Amanda.wear_night_clothes(2)
    vscene picture
    $ scene_runtime.text = opening
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "You hear noises at the window."
    menu:
        "Посмотреть в окно":
            pass
    $ scene_runtime.text = tavern_amanda_room_window_scene_text()
    menu:
        "Посмотреть на Аманду":
            pass
    return


label story_amanda_room_morning_window_0:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_004.jpeg", "Amanda is on her bed, covered badly.\n\nAmanda: Oy, mister you should knock.")
    $ scene_runtime.text = "Amanda says she is sorry for not coming for breakfast, while looking at the bulge under your pants."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "You decided to leave."
    menu:
        "Вернуться на кухню":
            pass
    $ household_clear_morning_issue("amanda")
    $ Amanda.wear_day_clothes()
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    jump TavernKitchen


label story_amanda_room_morning_window_1:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_003.jpeg", "Amanda does not even bother to cover herself properly and is sucking her finger.")
    $ scene_runtime.text = "Master, you did not disclose me to Sandra, so can we keep this little secret?\n\nShe winks. Between us???"
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "You decided to leave her again with a huge erection!!!!"
    menu:
        "Вернуться на кухню":
            pass
    $ player.intimacy.add_arousal(10)
    $ Amanda.trust = min(100, int(Amanda.trust or 0) + 1)
    $ Amanda.add_arousal(4)
    $ household_clear_morning_issue("amanda")
    $ Amanda.wear_day_clothes()
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    jump TavernKitchen


label story_amanda_room_morning_window_2:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_002.jpeg", "This time she decided to tease you with a smile and puts on a show of her titties.")
    $ scene_runtime.text = "Melissa said my puppies are too small. Do you like my puppies, Stephan? Do I make you hard???"
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "She laughs. Okay, okay, I know, I know, I am a bad girl and late to breakfast again. But it is so much fun here, isn't it? Did you see how he is pumping his wife!!!! Happy couple. I am almost jealous, and your little bro down there thinks so too."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Amanda laughs, and you leave... again. Damn, Ilmater almighty, she is a little cute devil, the horny one..."
    menu:
        "Вернуться на кухню":
            pass
    $ player.intimacy.add_arousal(10)
    $ Amanda.add_arousal(5)
    $ household_clear_morning_issue("amanda")
    $ Amanda.wear_day_clothes()
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.advance()
    $ threads["amandaMorningWood"].forceEnable()
    $ threads["amandaMorningWood"].setDay()
    $ main_ui_end_native_scene_state()
    jump TavernKitchen


label story_amanda_room_morning_window_3:
    call AmandaMorningWindowArrival("images/amanda/Room/Masturbation/amanda_bedroom_001.jpeg", "This time Amanda is lying on the bed naked, waiting for you.\n\nHello, master, do not be so shy. Let's do it together! Show me your glory!")
    $ scene_runtime.text = "Show or not show?"
    menu:
        "Показать":
            $ scene_runtime.text = "Wow, you are one poor horny bastard! Amanda laughs aloud."
        "Не показывать":
            $ scene_runtime.text = "You are as prude as Melissa. Too bad she likes girls."
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "You say: Do it together? Is this why you are locking the door?\n\nNo, says Amanda, to keep perverts like you outside!!!! She giggles. Girls have many secrets!"
    menu:
        "Продолжить":
            pass
    if Melissa.drawings_found:
        $ scene_runtime.text = "You tell her about the booklet you found at Melissa's. She shuts up.\n\nBut this is our secret too. We will discuss the booklet later, right???"
        menu:
            "Продолжить":
                pass
    if (Amanda.harass_instruction() == "notallow" and Amanda.corruption < 45) or (Amanda.harass_instruction() == "" and Amanda.corruption < 30):
        $ scene_runtime.text = "You tell her: This is hypocrisy. Why not enjoy that and help the tavern as well?\n\nAmanda is pissed off, and you leave. An apology will be needed."
        $ Amanda.change_anger(1, "morning_window_clients_argument")
        menu:
            "Продолжить":
                pass
    vscene "images/amanda/Room/Masturbation/amanda_bedroomAPI.webp"
    $ scene_runtime.text = "You decided to leave her again."
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
    $ scene_runtime.text = "Amanda came in early morning to catch up your erection."
    menu:
        "Продолжить утро":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
