# ================================================================================
# Clara tavern visit authored event labels.
# Event/thread tuples live in StoryEventRuntime.rpy; this file owns presentation
# and immediate class-state mutations for the Clara/Melissa visit scenes.
# ================================================================================

label story_clara_tavern_visit_bar_0:
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ Clara.var["tavern_visit_bar_0_seen"] = 1
    $ MainTxt = "Проходя мимо, вы слышите, как Мелисса, едва сдерживая смех, говорит Клариссе: \"Девчонка утром рано встала, песду о лавку почесала и села у окошка сечь, как бобик Жучку станет ебсть\".\n\nКларисса тут же подхватывает, уже совсем не скрывая довольной ухмылки: \"А бобик жарил Жучку раком, чего стесняться им, собакам!\" После этого обе разом заливаются таким дружным хохотом, будто давно уже спелись на этой пошлой волне."
    $ Melissa.corruption = min(100, int(Melissa.corruption or 0) + 3)
    $ Clara.openness = min(20, int(Clara.openness or 0) + 1)
    $ Melissa.sync_melissa_maps()
    $ Clara.sync_clara_maps()
    $ CurLocDesc = MainTxt
    call ShowImage("", "", "images/clara/tavern_visit.png")
    $ calendar_v2.advance_minutes(45)
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ current_action_items = []
    if thread is not None:
        $ thread.advance()
    return True


label story_clara_tavern_visit_bar_1:
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ Clara.var["tavern_visit_bar_1_seen"] = 1
    $ MainTxt = "Вы делаете вид, что заняты у барной стойки, но слух сам цепляет веселый шепот за спиной. Мелисса, уже откровенно дурачась, декламирует: \"Если б я была царица, говорит одна девица, я б пизду покрыла лаком и давала только раком\".\n\n\"Ой-ёй,\" тут же тянет Клара с ехидной ухмылкой, \"царь наш был мужичок скромный, у него был хуй огромный...\" Мелисса шутливо хлопает подружку по плечу и отвечает: \"Да говорю же, вот такой\", после чего раздвигает ладони сантиметров на двадцать.\n\nОбе многозначительно косятся на вас, а потом прыскают от смеха, пока вы изо всех сил делаете вид, будто целиком поглощены стойкой и делами трактира."
    $ Melissa.corruption = min(100, int(Melissa.corruption or 0) + 4)
    $ Clara.openness = min(20, int(Clara.openness or 0) + 2)
    $ Melissa.sync_melissa_maps()
    $ Clara.sync_clara_maps()
    $ CurLocDesc = MainTxt
    call ShowImage("", "", "images/clara/tavern_visit_size.png")
    $ calendar_v2.advance_minutes(45)
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ current_action_items = []
    if thread is not None:
        $ thread.advance()
    return True


label story_clara_tavern_visit_bar_2:
    $ household_mark_runtime_event_seen("clara_tavern_visit")
    $ Clara.var["tavern_visit_bar_2_seen"] = 1
    $ MainTxt = "У стойки снова слышится знакомый девичий смех. Вы оборачиваетесь как раз в тот миг, когда Кларисса и Мелисса слишком поспешно отстраняются друг от друга. У Мелиссы горят щеки, Кларисса поправляет платье с нарочитой деловитостью, а на их лицах написано ровно то, что они обе не хотят произносить вслух.\n\nМелисса первая находит выход: громко спрашивает, не закончились ли у вас чистые кружки. Кларисса тут же подхватывает этот нелепый повод, и обе принимаются обсуждать посуду с такой старательной серьезностью, что становится только смешнее."
    $ Melissa.openness = min(20, int(Melissa.openness or 0) + 1)
    $ Clara.openness = min(20, int(Clara.openness or 0) + 1)
    $ Melissa.trust = min(20, int(Melissa.trust or 0) + 1)
    $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
    $ Melissa.sync_melissa_maps()
    $ Clara.sync_clara_maps()
    $ CurLocDesc = MainTxt
    call ShowImage("", "", "images/clara/melissa_talk.png")
    $ calendar_v2.advance_minutes(45)
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ current_action_items = []
    if thread is not None:
        $ thread.advance()
    return True


label story_clara_melissa_room_visit_0:
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ Clara.var["melissa_room_visit_0_seen"] = 1
    $ Clara.var["melissa_room_visit_count"] = int(Clara.var.get("melissa_room_visit_count", 0) or 0) + 1
    $ MainTxt = "Вы заглядываете в комнату Мелиссы и тут же понимаете, что пришли не вовремя: Кларисса с Мелиссой уже устроили на кровати полушутливую драку подушками, а по полу летят перья и обрывки смеха. Обе резко замирают, увидев вас в дверях, и Мелисса первой просит вас не торчать у порога."
    $ Melissa.fun = min(100, int(Melissa.fun or 0) + 3)
    $ Clara.fun = min(100, int(Clara.fun or 0) + 3)
    $ Melissa.sync_melissa_maps()
    $ Clara.sync_clara_maps()
    $ CurLocDesc = MainTxt
    call ShowImage("", "", "images/clara/melissa Pillow fight.png")
    $ calendar_v2.advance_minutes(45)
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = []
    if thread is not None:
        $ thread.advance()
    return True


label story_clara_melissa_room_visit_1:
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ Clara.var["melissa_room_visit_1_seen"] = 1
    $ Clara.var["melissa_room_visit_count"] = int(Clara.var.get("melissa_room_visit_count", 0) or 0) + 1
    $ MainTxt = "Сегодня девушки сидят совсем близко друг к другу на кровати и, склонившись над коленями, возятся с листками и угольком. Кларисса что-то быстро дорисовывает, а Мелисса смеется шепотом и тут же прикрывает рисунки ладонью, заметив вас."
    $ Melissa.openness = min(20, int(Melissa.openness or 0) + 1)
    $ Clara.openness = min(20, int(Clara.openness or 0) + 1)
    $ Melissa.sync_melissa_maps()
    $ Clara.sync_clara_maps()
    $ CurLocDesc = MainTxt
    call ShowImage("", "", "images/clara/melissa_doodleTimes.png")
    $ calendar_v2.advance_minutes(45)
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = []
    if thread is not None:
        $ thread.advance()
    return True


label story_clara_melissa_room_visit_2:
    $ household_mark_runtime_event_seen("clara_melissa_room_visit")
    $ Clara.var["melissa_room_visit_2_seen"] = 1
    $ Clara.var["melissa_room_visit_count"] = int(Clara.var.get("melissa_room_visit_count", 0) or 0) + 1
    $ MainTxt = "Кларисса с Мелиссой так увлечены своими непристойными каракулями и перешептыванием, что сперва даже не сразу замечают вас. Когда же замечают, обе смотрят одинаково красноречиво: вам здесь сейчас делать нечего."
    $ Melissa.openness = min(20, int(Melissa.openness or 0) + 1)
    $ Clara.openness = min(20, int(Clara.openness or 0) + 1)
    $ Melissa.corruption = min(100, int(Melissa.corruption or 0) + 2)
    $ Clara.corruption = min(100, int(Clara.corruption or 0) + 2)
    $ Melissa.sync_melissa_maps()
    $ Clara.sync_clara_maps()
    $ CurLocDesc = MainTxt
    call ShowImage("", "", "images/clara/melissa_doodles.png")
    $ calendar_v2.advance_minutes(45)
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = []
    if thread is not None:
        $ thread.advance()
    return True
