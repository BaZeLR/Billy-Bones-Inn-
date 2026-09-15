# ================================================================================
# Clara tavern visit authored event labels.
# Event/thread tuples live in StoryEventRuntime.rpy; this file owns presentation
# and immediate class-state mutations for the Clara/Melissa visit scenes.
# ================================================================================

label story_clara_warns_amanda_about_legare_0:
    $ main_ui_begin_native_scene_state("Предупреждение Клариссы")
    show screen main_ui
    vscene "images/clara/tavern_visit.png"
    $ scene_runtime.text = "Зайдя в общий зал, вы замечаете Клариссу рядом с Амандой. Кларисса говорит тихо и не пытается изображать вашу союзницу.\n\n\"Я не друг вашему хозяину и не собираюсь им становиться,\" предупреждает она, бросив короткий взгляд в вашу сторону. \"Но Альбер опаснее, чем кажется. Он умеет говорить именно то, что девушка хочет услышать, а потом превращает ее доверие в свой товар. Не оставайся с ним наедине и не верь обещаниям только потому, что они красиво звучат.\"\n\nАманда сперва хочет отшутиться, но выражение лица Клариссы заставляет ее замолчать и выслушать предупреждение до конца."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True

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


# The sixth visit closes this ordered social sequence. Clarissa's later lessons
# belong to claraTavernEducation and therefore do not share this cursor.
label story_clara_tavern_visit_close_6:
    $ main_ui_begin_native_scene_state("Кларисса остаётся с вами")
    show screen main_ui
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    vscene "images/clara/tavern_visit.png"
    $ scene_runtime.text = "Кларисса и Мелисса больше не замолкают при вашем появлении. Кларисса прямо говорит, что после всего случившегося считает трактир своим домом, а его обитателей — людьми, за которых готова постоять. Мелисса берёт подругу под руку и с улыбкой замечает, что теперь та может не только прятаться у неё в комнате, но и по-настоящему участвовать в жизни дома."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Принять Клариссу в семью трактира":
            pass
    $ Clara.change_social(friend_delta=1, open_delta=1)
    $ Melissa.change_social(friend_delta=1)
    $ calendar_v2.advance_minutes(45)
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
