# ================================================================================
# Clara tavern visit authored event labels.
# Event/thread tuples live in StoryEventRuntime.rpy; this file owns presentation
# and immediate class-state mutations for the Clara/Melissa visit scenes.
# ================================================================================

label story_clara_tavern_visit_bar_0:
    $ main_ui_begin_native_scene_state("Кларисса и Мелисса у стойки")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ scene_runtime.text = "Проходя мимо, вы слышите, как Мелисса, едва сдерживая смех, говорит Клариссе: \"Девчонка утром рано встала, песду о лавку почесала и села у окошка сечь, как бобик Жучку станет ебсть\".\n\nКларисса тут же подхватывает, уже совсем не скрывая довольной ухмылки: \"А бобик жарил Жучку раком, чего стесняться им, собакам!\" После этого обе разом заливаются таким дружным хохотом, будто давно уже спелись на этой пошлой волне."
    $ Melissa.change_social(corruption_delta=3)
    $ Clara.change_social(open_delta=1)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/tavern_visit.png"
    menu:
        "Продолжить":
            pass
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_tavern_visit_bar_1:
    $ main_ui_begin_native_scene_state("Кларисса и Мелисса у стойки")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ scene_runtime.text = "Вы делаете вид, что заняты у барной стойки, но слух сам цепляет веселый шепот за спиной. Мелисса, уже откровенно дурачась, декламирует: \"Если б я была царица, говорит одна девица, я б пизду покрыла лаком и давала только раком\".\n\n\"Ой-ёй,\" тут же тянет Клара с ехидной ухмылкой, \"царь наш был мужичок скромный, у него был хуй огромный...\" Мелисса шутливо хлопает подружку по плечу и отвечает: \"Да говорю же, вот такой\", после чего раздвигает ладони сантиметров на двадцать.\n\nОбе многозначительно косятся на вас, а потом прыскают от смеха, пока вы изо всех сил делаете вид, будто целиком поглощены стойкой и делами трактира."
    $ Melissa.change_social(corruption_delta=4)
    $ Clara.change_social(open_delta=2)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/tavern_visit_size.png"
    menu:
        "Продолжить":
            pass
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_tavern_visit_bar_2:
    $ main_ui_begin_native_scene_state("Кларисса и Мелисса у стойки")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ scene_runtime.text = "Возле барной стойки вы вдруг слышите странные звуки и приглушенный смех из тихого угла. За шорохом одежды различаются тихие стоны и звуки поцелуев.\n\nКраем глаза вы замечаете Клариссу и Мелиссу. Обе слишком поспешно отстраняются друг от друга; щеки у них пылают, а на губах остаются одинаково загадочные улыбки. Похоже, за эти разговоры девушки успели стать очень близкими подругами."
    $ Melissa.change_social(open_delta=1)
    $ Clara.change_social(open_delta=1)
    $ Melissa.trust = min(20, int(Melissa.trust or 0) + 1)
    $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa_talk.png"
    menu:
        "Продолжить":
            pass
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_melissa_room_visit_0:
    $ main_ui_begin_native_scene_state("Кларисса в комнате Мелиссы")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ scene_runtime.text = "Вы заглядываете в комнату Мелиссы и тут же понимаете, что пришли не вовремя: Кларисса с Мелиссой уже устроили на кровати полушутливую драку подушками, а по полу летят перья и обрывки смеха. Обе резко замирают, увидев вас в дверях, и Мелисса первой просит вас не торчать у порога."
    $ Melissa.fun = min(100, int(Melissa.fun or 0) + 3)
    $ Clara.fun = min(100, int(Clara.fun or 0) + 3)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa Pillow fight.png"
    menu:
        "Вернуться в коридор":
            pass
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_melissa_room_visit_1:
    $ main_ui_begin_native_scene_state("Кларисса в комнате Мелиссы")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ scene_runtime.text = "Сегодня девушки сидят совсем близко друг к другу на кровати и, склонившись над коленями, возятся с листками и угольком. Кларисса что-то быстро дорисовывает, а Мелисса смеется шепотом и тут же прикрывает рисунки ладонью, заметив вас."
    $ Melissa.change_social(open_delta=1)
    $ Clara.change_social(open_delta=1)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa_doodleTimes.png"
    menu:
        "Оставить девушек одних":
            pass
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_melissa_room_visit_2:
    $ main_ui_begin_native_scene_state("Кларисса в комнате Мелиссы")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ scene_runtime.text = "Кларисса с Мелиссой так увлечены своими непристойными каракулями и перешептыванием, что сперва даже не сразу замечают вас. Когда же замечают, обе смотрят одинаково красноречиво: вам здесь сейчас делать нечего."
    $ Melissa.change_social(open_delta=1)
    $ Clara.change_social(open_delta=1)
    $ Melissa.change_social(corruption_delta=2)
    $ Clara.change_social(corruption_delta=2)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa_doodles.png"
    menu:
        "Оставить девушек одних":
            pass
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


# Event: after receiving protection, Clarissa keeps her promise to the household.
# Consequence: tavern service improves, new clientele arrives, and Clarissa
# prepares Melissa for anal intimacy without replacing Melissa's sex engine.
label story_clara_tavern_protection_lessons_6:
    $ main_ui_begin_native_scene_state("Уроки Клариссы")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_tavern_visit")

    vscene "images/clara/tavern_visit.png"
    $ scene_runtime.text = "Кларисса собирает Сандру, Аманду и Мелиссу у стойки и без прежних насмешек объясняет, чему ее годами учил Альбер: как встретить богатого гостя, рассадить компанию, принять заказ без суеты и не позволить дворянину принять вежливость за слабость. Сандра быстро превращает светские советы в рабочие правила, Аманда упражняется в поклонах, а Мелисса учится держаться увереннее."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Продолжить урок":
            pass

    vscene "images/clara/melissa_doodleTimes.png"
    $ scene_runtime.text = "После общего занятия Кларисса остается с Мелиссой. Они снова раскладывают уголь и бумагу, но теперь непристойные рисунки служат не обману Легаре, а честному разговору о желаниях и границах. Кларисса спокойно объясняет подруге, как подготовиться к близости сзади, не спешить и вовремя остановить партнера. Мелисса смущается, однако внимательно запоминает советы."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Поблагодарить Клариссу за помощь":
            pass

    $ Sandra.skills["waitress"] = min(100, int(Sandra.skills.get("waitress", 0) or 0) + 5)
    $ Amanda.skills["waitress"] = min(100, int(Amanda.skills.get("waitress", 0) or 0) + 5)
    $ Melissa.skills["waitress"] = min(100, int(Melissa.skills.get("waitress", 0) or 0) + 5)
    $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=2)
    $ Clara.change_social(friend_delta=2, open_delta=1)
    $ player.tavern_management.visitors = max(0, int(player.tavern_management.visitors or 0) + 5)
    $ player.change_tavern_fame(3)
    $ scene_runtime.text = "Новые манеры быстро становятся частью работы. По городу расходится слух, что в \"Диком Жеребце\" теперь умеют принять не только грузчиков и матросов: в трактир начинают заглядывать состоятельные купцы и дворяне, а обычное число посетителей растет."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Вернуться к делам трактира":
            pass

    $ calendar_v2.advance_minutes(60)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
