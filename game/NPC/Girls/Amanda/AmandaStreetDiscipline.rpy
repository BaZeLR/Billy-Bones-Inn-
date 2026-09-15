# ================================================================================
# Amanda street-encounter consequences.
# Thread state owns progression; these labels own presentation and consequences.
# ================================================================================

label story_amanda_street_punishment_breakfast_1:
    $ renpy.dynamic("amanda_scene_breakfast_ids", "amanda_scene_anger_before")
    $ amanda_scene_breakfast_ids = list(tavern_breakfast_present_ids() or [])
    $ amanda_scene_anger_before = int(Amanda.anger_with_player or 0)
    $ main_ui_begin_native_scene_state("Завтрак: разговор об Аманде")
    show screen main_ui
    $ player.tavern_management.breakfast.present_ids = amanda_scene_breakfast_ids
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "Когда все расселись за столом, вы не стали тянуть: рассказали Сандре, как застали Аманду на городской улице с незнакомым парнем, проследили за ними и собственными глазами увидели, чем закончилась их прогулка."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "Аманда сначала попыталась все обратить в шутку, но вы потребовали, чтобы Сандра всерьез наказала ее розгой. Сандра молча вывела племянницу из-за стола; вскоре на кухне были слышны свист прутьев, вскрики и сердитые обещания Аманды еще припомнить вам этот завтрак."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ Amanda.change_anger(12, "street_punishment")
    $ Amanda.change_rebellion(3, "street_punishment")
    vscene AmandaStaticData.image_path("tavern", "angry")
    $ scene_runtime.text = "Вернувшись, Аманда села осторожно и прожгла вас злым взглядом. Сандра объявила, что до особого решения та будет помогать Жоржетте и Лизетте по хозяйству и работать рядом с ними, но клиентов принимать не будет. Вы же прямо запретили Аманде тайные встречи с соседскими парнями и отдельно — любые встречи с Легаре."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ Amanda.set_var_int("prohibitwithguys", 1)
    $ Amanda.legare_forbidden = True
    $ scene_runtime.text = "Позже, когда Сандра ушла к плите, вы отвели Аманду в сторону и осторожно смазали оставшиеся от розги полосы лечебной мазью. Холодный крем быстро унял жжение. Аманда наконец выдохнула: \"Ладно, я уже не сержусь. Глупость сделала — признаю. Но не думай, что теперь все будет только по-твоему. У меня тоже есть свои способы. Еще посмотрим.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить завтрак":
            pass

    $ Amanda.change_anger(amanda_scene_anger_before - int(Amanda.anger_with_player or 0), "street_punishment_reconciled")
    $ calendar_v2.advance_minutes(45)
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = int(current_game_day() or 0)
    $ player.tavern_management.breakfast.day = int(current_game_day() or 0)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    call TavernKitchenFinishBreakfastEvent from _call_amanda_street_punishment_finish
    return True


label story_amanda_street_legare_warning_breakfast_2:
    $ renpy.dynamic("amanda_scene_breakfast_ids", "amanda_scene_warning_decision", "amanda_scene_warning_reaction")
    $ amanda_scene_breakfast_ids = list(tavern_breakfast_present_ids() or [])
    $ amanda_scene_warning_decision = Amanda.decide("street_legare_warning")
    $ amanda_scene_warning_reaction = str(dict(amanda_scene_warning_decision or {}).get("reaction", "neutral") or "neutral")
    $ main_ui_begin_native_scene_state("Завтрак: Легаре и правила дома")
    show screen main_ui
    $ player.tavern_management.breakfast.present_ids = amanda_scene_breakfast_ids
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "На следующем общем завтраке вы вернулись к вчерашнему разговору. Вы рассказали Сандре, что Кларисса связана с Легаре, а сам виноторговец слишком настойчиво кружит возле молодых женщин. Все увиденное заставляет вас подозревать: он хочет развратить девушек, поссорить дом и ослабить трактир ради собственных замыслов."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "Сандра выслушала молча, затем отрезала: \"Коротких нарядов, как у уличных шлюх, в доме больше не будет. А ты, Аманда, к Легаре не подходишь и никаких тайных свиданий не устраиваешь.\" Вы подтвердили запрет: ни Легаре, ни случайных парней."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ Amanda.set_var_int("prohibitwithguys", 1)
    $ Amanda.legare_forbidden = True
    $ Amanda.wardrobe.set_day_dress("modestworkdress", True)
    if amanda_scene_warning_reaction == "bad":
        $ Amanda.set_day_underwear("panties", "", True)
        $ Amanda.change_rebellion(4, "street_legare_warning")
        $ Amanda.change_anger(1, "street_legare_warning")
        vscene AmandaStaticData.image_path("tavern", "angry")
        $ scene_runtime.text = "Аманда вскинула подбородок и подчинилась только наполовину. Скромное рабочее платье она надела, но под ним демонстративно оставила себя без панталон: если ей запретили короткий наряд, свой маленький бунт она устроит иначе."
    else:
        $ Amanda.set_day_underwear("panties", "simplepanties", True)
        $ Amanda.change_rebellion(-2, "street_legare_warning")
        $ Amanda.change_anger(-1, "street_legare_warning")
        vscene AmandaStaticData.portrait
        $ scene_runtime.text = "Аманда долго хмурилась, но в конце концов выбрала не спорить. Она согласилась носить обычное рабочее платье с панталонами, держаться подальше от Легаре и не искать новых приключений на улице."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить завтрак":
            pass

    $ calendar_v2.advance_minutes(45)
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = int(current_game_day() or 0)
    $ player.tavern_management.breakfast.day = int(current_game_day() or 0)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    call TavernKitchenFinishBreakfastEvent from _call_amanda_street_warning_finish
    return True
