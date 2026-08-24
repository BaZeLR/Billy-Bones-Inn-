# ================================================================================
# Clara tavern visit authored event labels.
# Event/thread tuples live in StoryEventRuntime.rpy; this file owns presentation
# and immediate class-state mutations for the Clara/Melissa visit scenes.
# ================================================================================

label story_clara_tavern_visit_bar_0:
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ scene_runtime.text = "Проходя мимо, вы слышите, как Мелисса, едва сдерживая смех, говорит Клариссе: \"Девчонка утром рано встала, песду о лавку почесала и села у окошка сечь, как бобик Жучку станет ебсть\".\n\nКларисса тут же подхватывает, уже совсем не скрывая довольной ухмылки: \"А бобик жарил Жучку раком, чего стесняться им, собакам!\" После этого обе разом заливаются таким дружным хохотом, будто давно уже спелись на этой пошлой волне."
    $ Melissa.change_social(corruption_delta=3)
    $ Clara.change_social(open_delta=1)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/tavern_visit.png"
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    return True


label story_clara_tavern_visit_bar_1:
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ scene_runtime.text = "Вы делаете вид, что заняты у барной стойки, но слух сам цепляет веселый шепот за спиной. Мелисса, уже откровенно дурачась, декламирует: \"Если б я была царица, говорит одна девица, я б пизду покрыла лаком и давала только раком\".\n\n\"Ой-ёй,\" тут же тянет Клара с ехидной ухмылкой, \"царь наш был мужичок скромный, у него был хуй огромный...\" Мелисса шутливо хлопает подружку по плечу и отвечает: \"Да говорю же, вот такой\", после чего раздвигает ладони сантиметров на двадцать.\n\nОбе многозначительно косятся на вас, а потом прыскают от смеха, пока вы изо всех сил делаете вид, будто целиком поглощены стойкой и делами трактира."
    $ Melissa.change_social(corruption_delta=4)
    $ Clara.change_social(open_delta=2)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/tavern_visit_size.png"
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    return True


label story_clara_tavern_visit_bar_2:
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ scene_runtime.text = "У стойки снова слышится знакомый девичий смех. Вы оборачиваетесь как раз в тот миг, когда Кларисса и Мелисса слишком поспешно отстраняются друг от друга. У Мелиссы горят щеки, Кларисса поправляет платье с нарочитой деловитостью, а на их лицах написано ровно то, что они обе не хотят произносить вслух.\n\nМелисса первая находит выход: громко спрашивает, не закончились ли у вас чистые кружки. Кларисса тут же подхватывает этот нелепый повод, и обе принимаются обсуждать посуду с такой старательной серьезностью, что становится только смешнее."
    $ Melissa.change_social(open_delta=1)
    $ Clara.change_social(open_delta=1)
    $ Melissa.trust = min(20, int(Melissa.trust or 0) + 1)
    $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa_talk.png"
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    return True


label story_clara_melissa_room_visit_0:
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ scene_runtime.text = "Вы заглядываете в комнату Мелиссы и тут же понимаете, что пришли не вовремя: Кларисса с Мелиссой уже устроили на кровати полушутливую драку подушками, а по полу летят перья и обрывки смеха. Обе резко замирают, увидев вас в дверях, и Мелисса первой просит вас не торчать у порога."
    $ Melissa.fun = min(100, int(Melissa.fun or 0) + 3)
    $ Clara.fun = min(100, int(Clara.fun or 0) + 3)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa Pillow fight.png"
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    return True


label story_clara_melissa_room_visit_1:
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ scene_runtime.text = "Сегодня девушки сидят совсем близко друг к другу на кровати и, склонившись над коленями, возятся с листками и угольком. Кларисса что-то быстро дорисовывает, а Мелисса смеется шепотом и тут же прикрывает рисунки ладонью, заметив вас."
    $ Melissa.change_social(open_delta=1)
    $ Clara.change_social(open_delta=1)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa_doodleTimes.png"
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    return True


label story_clara_melissa_room_visit_2:
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ scene_runtime.text = "Кларисса с Мелиссой так увлечены своими непристойными каракулями и перешептыванием, что сперва даже не сразу замечают вас. Когда же замечают, обе смотрят одинаково красноречиво: вам здесь сейчас делать нечего."
    $ Melissa.change_social(open_delta=1)
    $ Clara.change_social(open_delta=1)
    $ Melissa.change_social(corruption_delta=2)
    $ Clara.change_social(corruption_delta=2)
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/clara/melissa_doodles.png"
    $ calendar_v2.advance_minutes(45)
    if event_runtime.active_thread is not None:
        $ event_runtime.active_thread.advance()
    return True
