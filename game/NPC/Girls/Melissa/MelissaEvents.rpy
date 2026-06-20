# ================================================================================
# Melissa authored events.
# Event/thread availability is defined in StoryEventRuntime.rpy.
# ================================================================================

label story_melissa_storage_rat_0:
    $ SignalBlockTime = 1
    $ household_mark_runtime_event_seen("melissa_storage_rat")
    vscene "images/melissa/tavern/rat_in_basement_melissa.png"
    $ MainTxt = "В кладовой вас встречает раздраженная Мелисса: у мешков с крупой шуршит крупная крыса, а девушка уже стоит наготове с метлой в руках. \"Опять эта тварь сюда лазит,\" шепчет она. \"Если ее сейчас не прогнать, потом весь угол придется перебирать заново.\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    menu:
        "Прибить крысу":
            $ Melissa.var["ratKilled"] = True
            $ Melissa.var["storage_rat_cleared"] = 1
            $ Melissa.var["storage_rat_last_help_day"] = int(dayspassed or 0)
            $ WerecatVar["rat_carcass_cached"] = 1
            $ WerecatVar["rats_problem_active"] = 1
            $ WerecatVar["rat_food_loss_next_day"] = int(dayspassed or 0) + 7
            $ Melissa.var["work_attitude"] = int(Melissa.var.get("work_attitude", 0) or 0) + 1
            $ Melissa.skills["cleaning"] = min(100, int(Melissa.skills.get("cleaning", 0) or 0) + 1)
            $ Melissa.change_social(friend_delta=1)
            $ thread.advance()
            $ evalTime = None
            $ findAvailableEvents(True)
            $ MainTxt = "Вы быстро расправляетесь с крысой, и Мелисса заметно расслабляется. \"Вот теперь другое дело,\" тихо говорит она, уже без прежнего раздражения. На всякий случай вы решаете не выбрасывать тушку сразу: такая приманка еще может сгодиться, если в лесу и правда водится тот необычный кошачий охотник, о котором судачат по трактирам."
        "Оставить все как есть":
            $ MainTxt = "Вы решаете не возиться с крысой прямо сейчас. Мелисса поджимает губы и берется переставлять мешки подальше от шороха, явно недовольная тем, что проблему придется терпеть еще какое-то время."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    return True


label story_melissa_werecat_intro_0:
    $ SignalBlockTime = 1
    call MelissaRatBreakfastScene
    $ thread.advance()
    $ evalTime = None
    $ findAvailableEvents(True)
    return True


label story_melissa_werecat_rumor_0:
    $ SignalBlockTime = 1
    call WerecatHunterClubTease
    $ thread.advance()
    $ evalTime = None
    $ findAvailableEvents(True)
    return True


label story_melissa_werecat_home_0:
    $ SignalBlockTime = 1
    call WerecatAdoptionBreakfastScene
    $ thread.advance()
    $ evalTime = None
    $ findAvailableEvents(True)
    return True


label story_melissa_werecat_home_1:
    $ SignalBlockTime = 1
    call WerecatMonthThanksScene
    $ thread.advance()
    $ evalTime = None
    $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_0:
    $ SignalBlockTime = 1
    $ TavernBreakfastPresentIds = ["sandra", "amanda"]
    vscene tavern_kitchen_breakfast_picture()
    "Утренний стол уже накрыт, но одного места не хватает. Аманда первой замечает пустую скамью Мелиссы и с ленивой усмешкой тянет: \"Вот увидите, сейчас она явится с таким лицом, будто всю ночь воевала с нечистой силой.\""
    vscene "images/melissa/bats/yawns.png"
    "В этот момент в кухню, зевая и еле переставляя ноги, входит Мелисса. Вид у нее злой и невыспавшийся."
    $ TavernBreakfastPresentIds = ["sandra", "melissa", "amanda"]
    vscene "images/melissa/kitchen.jpg"
    "Мелисса садится за стол и, даже взяв кружку, продолжает коситься так, будто над ее головой все еще что-то шуршит."
    "Сандра уже спокойнее говорит: \"У нас уже была крысиная проблема, из-за которой портились припасы, а теперь еще и летучие мыши? После крыс в кладовой я не хочу ждать, пока новая дрянь опять испортит дом.\""
    if relationship_anger("amanda") > 0 and relationship_anger("melissa") > 0:
        "Аманда не удерживается: \"Может, это все за тобой ходит? Крысы, летучие мыши... Ведьма у нас завелась, вот и зверье сбежалось.\""
        "Мелисса ставит кружку на стол. \"Если я ведьма, Аманда, начну с тебя. Заколдую, чтобы ты одно утро помолчала.\""
    elif relationship_anger("amanda") > 0:
        "Аманда цепляет ее резче обычного: \"Крысы, летучие мыши... Может, они все к тебе, Мелисса? Ведьма при хозяйстве, да?\""
        "Мелисса зло щурится: \"Если я ведьма, то первым делом заколдую кое-кому язык, чтобы он хоть за завтраком помолчал.\""
    elif relationship_anger("melissa") > 0:
        "Аманда тут же оживляется, складывает пальцы в дразнящий знак и тянет с ухмылкой: \"Мелисса, а что если ты настоящая ведьма? Крысы в подвале, мыши с крыльями под крышей... Может, это все твои любимцы сбежались?\""
        "Мелисса отвечает ровно: \"Продолжай. Если я ведьма, мне как раз нужен кто-то болтливый для первого проклятия.\""
    else:
        "Аманда тут же оживляется, складывает пальцы в дразнящий знак и тянет с ухмылкой: \"Мелисса, а что если ты настоящая ведьма? Крысы в подвале, мыши с крыльями под крышей... Может, это все твои любимцы сбежались?\""
        "Мелисса зло щурится: \"Если я ведьма, то первым делом заколдую кое-кому язык, чтобы он хоть за завтраком помолчал.\""
    $ MainTxt = "Разговор за столом быстро становится серьезнее. У вас в голове остается одна ясная мысль: с комнатой Мелиссы придется разбираться всерьез."
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    "[MainTxt]"
    $ calendar_v2.advance_minutes(45)
    $ Melissa.var["bats_episode"] = max(int(Melissa.var.get("bats_episode", 0) or 0), 1)
    $ BreakfastToday = True
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ TavernBreakfastDay = int(dayspassed or 0)
    $ TavernBreakfastEventActive = True
    $ Melissa.current_location = "TavernKitchen"
    $ thread.advance()
    $ evalTime = None
    $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_1:
    $ SignalBlockTime = 1
    $ _melissa_bat_problem_1_choice = ""
    vscene tavern_melissa_room_picture()
    $ MainTxt = "Проходя по коридору наверху, вы слышите из комнаты Мелиссы тревожный шум: скрип кровати, злой шепот и какое-то нервное шевеление под самым потолком. Заглянув внутрь, вы видите, что Мелисса не спит и сидит на кровати, зло глядя вверх.\n\n\"О, хорошо, что ты здесь,\" шепчет она почти сразу. \"Опять эта дрянь над головой возится. То шорох, то писк, то будто кто-то бегает по балкам. Я уже не знаю, что хуже: сам шум или то, что после такой ночи утром стоишь как пьяная. Если можешь, помоги мне с этим по-человечески.\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    menu:
        "Сказать, что вы разберетесь с этим":
            $ _melissa_bat_problem_1_choice = "promise"
            $ MainTxt = "Вы обещаете, что не ограничитесь одними словами. Сначала вы прямо сейчас осматриваете потолок и щели в комнате, а утром подниметесь на чердак над ней.\n\nПод самым верхом действительно видны мелкие дыры в дереве, а оттуда тянет затхлым чердаком. Теперь все ясно: надо лезть наверх и смотреть, что там развелось."
        "Успокоить Мелиссу":
            $ _melissa_bat_problem_1_choice = "comfort"
            $ MainTxt = "Вы говорите Мелиссе чуть тише и спокойнее, чем обычно, что не отмахнетесь от ее жалоб. От этого она не перестает злиться на потолок, но по голосу слышно, что ей уже легче от одного того, что кто-то наконец воспринимает проблему всерьез."
        "Оставить ее на сегодня в покое":
            $ _melissa_bat_problem_1_choice = "leave"
            $ MainTxt = "Вы решаете пока не затягивать ночной разговор. Мелисса недовольно выдыхает, плотнее кутается в одеяло и снова косится на потолок."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ calendar_v2.advance_minutes(45)
    if _melissa_bat_problem_1_choice == "promise":
        $ Melissa.var["AskedMCToSolveRoomProblem"] = 1
        $ Melissa.var["bats_episode"] = 3
        $ Melissa.var["bat_attic_check_day"] = max(int(Melissa.var.get("bat_attic_check_day", -1) or -1), int(dayspassed or 0))
        $ thread.advance()
        $ evalTime = None
        $ findAvailableEvents(True)
    elif _melissa_bat_problem_1_choice == "comfort":
        $ Melissa.add_trust(1)
    return True


label story_melissa_bat_problem_2:
    $ SignalBlockTime = 1
    vscene "images/player_room/player_room_attic_1.png"
    $ MainTxt = "Вы медленно обходите чердак вдоль стропил и почти сразу замечаете над той частью дома, где спит Мелисса, старые щели между досками и темные ходы в подгнившей обшивке.\n\nЕще через пару шагов находится и главная причина ночного шума. Под самой кровлей набилось сухое гнездовое тряпье, комки мха, помет и целая дрянная колония, давно обжившая балки и пустоты под крышей. Одним веником тут не обойтись: сначала эту пакость придется выкурить дымом, а потом уже по-настоящему заделывать щели."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ calendar_v2.advance_minutes(45)
    $ Melissa.var["bats_episode"] = max(int(Melissa.var.get("bats_episode", 0) or 0), 4)
    $ thread.advance()
    $ evalTime = None
    $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_3:
    $ SignalBlockTime = 1
    $ _melissa_bat_problem_3_choice = ""
    vscene "images/player_room/player_room_attic.png"
    $ MainTxt = "Раздвинув старое тряпье и осторожно пригнувшись, вы находите маленькое слуховое окно над стороной дома, где расположена комната Аманды. Сквозь мутное стекло и щели в раме открывается слишком уж ясный вид на соседний двор.\n\n" + attic_neighbor_sex_scene_text() + " Вы невольно задерживаетесь у окна дольше, чем следовало бы."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    menu:
        "Податься ближе":
            $ _melissa_bat_problem_3_choice = "fall"
            vscene "images/player_room/batsProblem/fell_from_attic.png"
            "Вы тянетесь вперед еще на полшага, но старое дерево под ногами не выдерживает. Доска жалобно трещит, потом ломается, и в следующий миг вас с грохотом несет вниз вместе с пылью, щепками и куском прогнившего настила."
            "Несколько тяжелых мгновений вы лежите среди пыли и щепок, пытаясь понять, куда именно вас выбросило. С потолка свисают обломки, над головой зияет пролом, а вокруг слишком хорошо знакомые вещи из вашей комнаты."
            vscene "images/player_room/batsProblem/melissa in room.png"
            "Дверь распахивается как раз тогда, когда вы пытаетесь подняться. На пороге появляется Мелисса: растрепанная, злая, с одеялом и узлом вещей в руках. Она явно собиралась переждать ночь подальше от своей комнаты, но вместо этого застает вас посреди вашей собственной спальни, под грудой чердачного мусора."
            vscene "images/player_room/batsProblem/melissa in the room.png"
            "Мелисса смотрит на пролом, потом на вас, потом снова вверх. На ее лице за одно мгновение сменяются испуг, понимание и обида."
            vscene "images/player_room/batsProblem/melissa_talk.png"
            "\"Ты... ты извращенец!\" — срывается у нее голос. — \"Подглядывал оттуда? А потом еще и свалился сюда через потолок?! Всё. Хватит. Сегодня же переберусь к Аманде. Там, по крайней мере, потолок на голову не падает!\""
            $ MainTxt = "Вы провалились с чердака в свою комнату как раз в тот момент, когда Мелисса пришла сюда с вещами. Объясняться сейчас бесполезно: история вышла слишком громкой и слишком стыдной."
        "Отступить от окна":
            $ _melissa_bat_problem_3_choice = "retreat"
            $ MainTxt = "Вы отступаете от окна, пока старые доски под ногами еще держат. Гнездовище найдено, но с чердаком придется разбираться осторожнее."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ calendar_v2.advance_minutes(45)
    if _melissa_bat_problem_3_choice == "fall":
        $ Melissa.var["bats_episode"] = max(int(Melissa.var.get("bats_episode", 0) or 0), 6)
        $ Melissa.var["drawings_ready_day"] = int(dayspassed or 0) + 2
        $ Melissa.var["temp_room"] = "TavernAmandaRoom"
        $ AmandaVar["attic_window_busted"] = 1
        $ Melissa.add_trust(-7)
        $ Amanda.change_social(friend_delta=-5)
        $ notoriety = min(100, int(notoriety or 0) + 10)
        $ tavernfame = max(-20, int(tavernfame or 0) - 2)
        $ thread.advance()
        $ evalTime = None
        $ findAvailableEvents(True)
    else:
        $ Melissa.var["bats_episode"] = max(int(Melissa.var.get("bats_episode", 0) or 0), 5)
    return True


label story_melissa_bat_problem_5:
    $ SignalBlockTime = 1
    if int(effective_player_exploration() or 0) <= 120:
        $ MainTxt = "Пока Мелисса вынужденно ночует у Аманды, ее собственная комната остается непривычно тихой. Вы осматриваете ее внимательнее обычного: ларь, табурет, складки одеяла, щель между стеной и кроватью. Однако за сорок пять минут поисков ничего важного в глаза так и не бросается."
        $ CurLocDesc = MainTxt
        "[MainTxt]"
        $ calendar_v2.advance_minutes(45)
    else:
        vscene "images/melissa/bedRoomSearch/underBedBooklet.png"
        "Пока Мелисса вынужденно ночует у Аманды, ее собственная комната остается непривычно тихой. Вы осматриваете ее внимательнее обычного: ларь, табурет, складки одеяла, щель между стеной и кроватью."
        "Под кроватью Мелиссы, задвинутый почти к самой стене, обнаруживается потертый рисованный буклет. Обложка ничего не объясняет, зато место, где его прятали, говорит само за себя."
        $ Melissa.var["drawings_found"] = 1
        $ MainTxt = "Под кроватью Мелиссы вы нашли {a=melissa_room_object:melissa_drawings_booklet_001}{color=#245b2b}потертый рисованный буклет{/color}{/a}. Теперь его можно рассмотреть как найденный предмет."
        $ CurLocDesc = MainTxt
        "[MainTxt]"
        $ calendar_v2.advance_minutes(45)
        $ thread.advance()
        $ evalTime = None
        $ findAvailableEvents(True)
        call TavernMelissaRoomBuildActions
    return True


label MelissaBookletOpenPreview:
    vscene "images/melissa/bedRoomSearch/lewd_pages0.jpg"
    $ MainTxt = "Вы раскрываете буклет на первых страницах. Манера уверенная, линии смелые, а сюжеты вовсе не девичьи."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ calendar_v2.advance_minutes(5)
    $ Melissa.var["drawings_booklet_opened"] = 1
    call TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001", True)
    return


label ReadMelissaBooklet(return_to_location=True):
    vscene "images/melissa/bedRoomSearch/underBedBooklet.png"
    "Вы достаете спрятанную пачку рисунков и осторожно разворачиваете потертые листы."
    vscene "images/melissa/bedRoomSearch/lewd_pages0.jpg"
    "Первые страницы выглядят почти как упражнение в линии и тени, но позы и детали быстро выдают совсем другой интерес автора."
    vscene "images/melissa/bedRoomSearch/lewd_pages1.jpg"
    "На следующих листах осторожность исчезает: тела нарисованы смело, без стыда, будто тот, кто держал перо, слишком хорошо представлял себе каждое движение."
    vscene "images/melissa/bedRoomSearch/lewd2_pages.jpg"
    $ player_apply_arousal_trigger("melissa_booklet", 18)
    "К концу просмотра мысли становятся тяжелее и жарче. Это уже не просто любопытство: картинки цепляют тело быстрее, чем вы успеваете отвести взгляд."
    $ calendar_v2.advance_minutes(10)
    $ Melissa.var["drawings_booklet_opened"] = 1
    $ Melissa.var["drawings_booklet_read"] = 1
    if bool(return_to_location):
        menu:
            "Закрыть буклет":
                jump expression CurLoc
    call TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001", True)
    return


label MelissaBookletTake:
    call Take("melissa_drawings_booklet_001", "TavernMelissaRoom", "", "melissa_drawings_booklet_001")
    if int(_player_item_count_by_id("melissa_drawings_booklet_001") or 0) > 0:
        $ Melissa.var["drawings_booklet_taken"] = 1
        $ Melissa.var["drawings_booklet_left"] = 0
    $ current_object_id = ""
    call TavernMelissaRoomBuildActions
    return


label MelissaBookletLeaveThere:
    vscene "images/melissa/bedRoomSearch/underBedBooklet.png"
    $ MainTxt = "Вы аккуратно возвращаете буклет туда, где нашли. Теперь вы знаете, что искать и где смотреть, не выдавая того, что уже обнаружили тайник."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ Melissa.var["drawings_booklet_left"] = 1
    $ Melissa.var["drawings_spy_option_unlocked"] = 1
    call TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001", True)
    return


label MelissaBookletContinueSearch:
    $ current_object_id = ""
    $ MainTxt = "Вы оставляете буклет пока лежать под кроватью и продолжаете осматривать комнату."
    $ CurLocDesc = MainTxt
    call TavernMelissaRoomBuildActions
    return


label story_melissa_bat_problem_4:
    $ SignalBlockTime = 1
    $ _melissa_bat_problem_4_result = ""
    vscene "images/player_room/player_room_attic_1.png"
    if int(Melissa.var.get("bats_episode", 0) or 0) < 7:
        if int(_player_item_count_by_id("bat_repellent_001") or 0) > 0:
            $ _melissa_bat_problem_4_result = "smoke"
            $ MainTxt = "Вы раскладываете дымную смесь между балок, даете ей как следует разгореться и быстро отступаете. Чердак наполняется густым едким дымом из мха, лаванды и трав. Из-под крыши с писком и хлопаньем вырываются летучие мыши.\n\nГнездовище вы наконец выкурили, но на одном дыме дело не закончится: пока крышу не заделают как следует, щели останутся и вся пакость со временем полезет обратно."
        else:
            $ MainTxt = "Теперь уже ясно, что под крышей свилось настоящее гнездовище. Просто так его не вымести: сначала нужна едкая дымная смесь, чтобы выгнать всю эту дрянь из-под кровли."
    elif int(Melissa.var.get("roof_repair_order_day", -1) or -1) < 0:
        if int(money or 0) >= 1000:
            $ _melissa_bat_problem_4_result = "order_roof"
            $ MainTxt = "Вы договариваетесь о починке старой крыши и отдаете за работу тысячу монет. Теперь остается только дождаться, пока мастера перетянут гнилые доски, забьют щели и приведут верх трактира в порядок. Обещают управиться за пару дней."
        else:
            $ MainTxt = "Летучих мышей вы уже выкурили, но без починки крыши дело не закончить. Денег на мастеров пока не хватает."
    elif int(Melissa.var.get("roof_repair_complete_day", -1) or -1) < 0 or int(dayspassed or 0) < int(Melissa.var.get("roof_repair_complete_day", -1) or -1):
        $ _days_left = max(0, int(Melissa.var.get("roof_repair_complete_day", -1) or -1) - int(dayspassed or 0))
        $ MainTxt = "Крыша еще в работе. По свежим доскам и забитым щелям видно, что мастера уже начали, но до полного порядка придется подождать еще {} дн.".format(_days_left)
    else:
        $ MainTxt = "Теперь на чердаке сразу видно, что работа завершена: щели закрыты, прогнившие доски заменены, а от старого гнездовища не осталось ничего, кроме сухой пыли."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ calendar_v2.advance_minutes(45)
    if _melissa_bat_problem_4_result == "smoke":
        $ _player_remove_item_by_id("bat_repellent_001", 1)
        $ Melissa.var["bats_episode"] = max(int(Melissa.var.get("bats_episode", 0) or 0), 7)
        $ Melissa.var["bat_recipe_unlocked"] = 1
    elif _melissa_bat_problem_4_result == "order_roof":
        $ money = int(money or 0) - 1000
        $ Melissa.var["roof_repair_order_day"] = int(dayspassed or 0)
        $ Melissa.var["roof_repair_complete_day"] = int(dayspassed or 0) + 2
        $ thread.advance()
        $ evalTime = None
        $ findAvailableEvents(True)
        call stat
    return True


label story_melissa_bat_problem_6:
    $ SignalBlockTime = 1
    vscene "images/melissa/thanks.png"
    $ MainTxt = "Вы говорите Мелиссе, что на этот раз все действительно закончено: чердачное гнездовище выжжено, щели под крышей забиты, а над ее комнатой теперь наконец тихо. Она сперва смотрит на вас с привычной настороженностью, будто все еще ждет подвоха, но потом сама коротко выдыхает и впервые за все это время заметно расслабляется.\n\n\"Значит, можно снова спать у себя и не ждать, что ночью над головой начнут бегать, пищать и сыпать трухой...\" Она качает головой, будто сама до конца не верит в удачу, а потом уже тише добавляет: \"Спасибо. Не за слова — за то, что ты и правда довел дело до конца.\"\n\nПохоже, история с летучими мышами и чердаком для Мелиссы наконец действительно закрыта."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ calendar_v2.advance_minutes(45)
    $ thread.complete()
    $ Melissa.complete_bats_problem()
    $ Melissa.add_trust(3)
    $ Melissa.add_openness(2)
    $ evalTime = None
    $ findAvailableEvents(True)
    return True
