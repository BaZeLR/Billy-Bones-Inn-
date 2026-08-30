# ================================================================================
# Melissa authored events.
# Event/thread availability is defined in StoryEventRuntime.rpy.
# ================================================================================

label story_melissa_storage_rat_0:
    show screen main_ui
    $ household_mark_runtime_event_seen("melissa_storage_rat")
    vscene MelissaStaticData.image_path("tavern", "rat")
    $ scene_runtime.text = "В кладовой вас встречает раздраженная Мелисса: у мешков с крупой шуршит крупная крыса, а девушка уже стоит наготове с метлой в руках. \"Опять эта тварь сюда лазит,\" шепчет она. \"Если ее сейчас не прогнать, потом весь угол придется перебирать заново.\""
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Прибить крысу":
            $ Melissa.storage_rat_help_day = int(current_game_day() or 0)
            $ werecat_state()["rat_carcass_cached"] = 1
            $ werecat_state()["rats_problem_active"] = 1
            $ werecat_state()["rat_food_loss_next_day"] = int(current_game_day() or 0) + 7
            $ Melissa.skills["cleaning"] = min(100, int(Melissa.skills.get("cleaning", 0) or 0) + 1)
            $ Melissa.change_social(friend_delta=1)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
            $ scene_runtime.text = "Вы быстро расправляетесь с крысой, и Мелисса заметно расслабляется. \"Вот теперь другое дело,\" тихо говорит она, уже без прежнего раздражения. На всякий случай вы решаете не выбрасывать тушку сразу: такая приманка еще может сгодиться, если в лесу и правда водится тот необычный кошачий охотник, о котором судачат по трактирам."
        "Оставить все как есть":
            $ scene_runtime.text = "Вы решаете не возиться с крысой прямо сейчас. Мелисса поджимает губы и берется переставлять мешки подальше от шороха, явно недовольная тем, что проблему придется терпеть еще какое-то время."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    return True


label story_melissa_werecat_intro_0:
    $ main_ui_begin_native_scene_state("Завтрак: кошечка")
    show screen main_ui
    $ werecat_state()["rat_breakfast_seen"] = 1
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = current_game_day()
    $ player.tavern_management.breakfast.day = current_game_day()
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    vscene "images/kitchen/need_kitty_1.png"
    $ scene_runtime.text = "Мягкий утренний свет ползет по кухне, в мисках парит каша, воздух пахнет молоком, овсом и горячим хлебом. За общим столом сегодня сидят все трое. Сандра, помешивая кашу с лишней силой, первой возвращается к вчерашнему: \"Крысы в доме совсем распоясались. Уже по три полных тюка припасов за неделю портят. Если так пойдет дальше, к зиме сами у пустых мешков сядем.\" Аманда разваливается на скамье и, как всегда, пытается рассечь тревогу шуткой: \"А знаешь, чего этому дому по-настоящему не хватает? Хорошей сильной киски. Такой, чтоб и мышей ловила, и с вредителями умела разбираться как следует.\" Она лукаво подмигивает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    vscene "images/kitchen/need_kitty_2.png"
    $ scene_runtime.text = "Мелисса сперва краснеет, потом все же хихикает: \"Да... большой, гибкой охотницы. Чтобы маленьких пакостников душила без жалости... и ночами было бы с кем согреться.\" Смех за столом быстро снимает лишнее напряжение. Даже Сандра, отвернувшись к котлу, ворчит уже заметно мягче."
    if relationship_anger("amanda") > 0 and relationship_anger("melissa") > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + " Аманда и Мелисса все равно успевают уколоть друг друга. Сандра сразу обрывает их: \"Когти оставьте для крыс. За столом не шипеть.\""
    elif relationship_anger("amanda") > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + " Аманда шутит привычно, но сегодня в каждой шутке достается именно Мелиссе. Та краснеет, но не опускает глаза."
    elif relationship_anger("melissa") > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + " Мелисса смеется вместе со всеми, но на амандины насмешки отвечает коротко и зло. Еще одно слово, и завтрак снова скатится в спор."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ player.change_stat("fun", 5)
    $ Sandra.change_social(friend_delta=1)
    $ Melissa.change_social(friend_delta=1)
    $ Amanda.change_social(friend_delta=1)
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    call stat
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_werecat_rumor_0:
    $ werecat_state()["hunter_tease_day"] = int(calendar_v2.daysInGame or 0)
    $ scene_runtime.text = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ scene_runtime.location_text = scene_runtime.text
    vscene werecat_info_picture_path()
    "[scene_runtime.text]"
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    return True


label story_melissa_werecat_home_0:
    $ werecat_state()["adoption_breakfast_seen"] = 1
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = current_game_day()
    $ player.tavern_management.breakfast.day = current_game_day()
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "За завтраком сегодня разговор быстро сворачивает к новой обитательнице трактира. У самого очага, настороженно щурясь, устроилась ваша необычная лесная кошка, и даже с такого расстояния видно, что она следит за каждым шорохом куда внимательнее обычного зверя.\n\nСандра первой признает очевидное: \"В кладовой ночью впервые было тихо. Если эта хвостатая и правда останется у нас, припасы хоть поживут спокойно.\" Аманда тут же расплывается в ухмылке: \"Говорила же, дому нужна хорошая киска. А эта еще и красавица, не только охотница.\" Мелисса тихо фыркает, но спорить не спешит: \"Главное, чтобы она крыс душила так же ловко, как на всех смотрит.\"\n\nПохоже, в трактире уже начинают принимать вашу странную добычу как свою. История на этом не кончается, но теперь у нее наконец есть продолжение дома, а не только в лесу."
    if relationship_anger("amanda") > 0 and relationship_anger("melissa") > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nАманда и Мелисса опять начинают цеплять друг друга, но кошка вдруг шипит от очага, и обе замолкают. Сандра только хмыкает: \"Вот. Даже зверю надоело.\""
    elif relationship_anger("amanda") > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nАманда цепляет Мелиссу за каждую реплику о кошке. Мелисса держится, но губы у нее сжаты."
    elif relationship_anger("melissa") > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nМелисса сегодня не дает Аманде разгуляться. На каждую шутку отвечает сухо, и Сандра быстро переводит разговор обратно к кладовой."
    $ scene_runtime.location_text = scene_runtime.text
    $ player.change_stat("fun", 3)
    $ Sandra.change_social(friend_delta=1)
    $ Melissa.change_social(friend_delta=1)
    $ Amanda.change_social(friend_delta=1)
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    return True


label story_melissa_werecat_home_1:
    $ werecat_state()["first_month_thanks_day"] = current_game_day()
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = current_game_day()
    $ player.tavern_management.breakfast.day = current_game_day()
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "За общим столом сегодня куда спокойнее обычного. В кладовой уже давно не слышно прежней возни, а у самого очага, свернувшись теплым клубком, дремлет ваша необычная кошка.\n\nСандра первой нарушает молчание: \"Эта малышка и правда спасла нам припасы. Если бы не она, мы бы еще долго слушали шорох в мешках и считали, сколько еды уходит в никуда.\" Потом она смотрит уже прямо на вас и говорит мягче: \"Хорошее дело вы все-таки сделали. Такой зверь дому в радость.\"\n\nОстальные тоже заметно теплеют. Даже обычная утренняя суета сегодня кажется куда уютнее."
    if threads["melissaBatProblem"].num >= 6:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nПосле короткой паузы Сандра добавляет уже совсем иначе: \"А ту глупую историю с чердаком пора бы и отпустить. Дом у нас старый, люди живые, а дурных случаев без того хватает. Главное, что теперь ты не отмахнулся от настоящей беды и довел дело до ума.\" Похоже, за столом наконец начинают считать тот позорный случай скорее нелепостью, чем клеймом."
    $ scene_runtime.location_text = scene_runtime.text
    $ Sandra.change_social(friend_delta=1)
    $ Melissa.change_social(friend_delta=1)
    $ Amanda.change_social(friend_delta=1)
    $ player.change_stat("fun", 3)
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_0:
    $ main_ui_begin_native_scene_state("Завтрак: летучие мыши")
    show screen main_ui
    $ player.tavern_management.breakfast.present_ids = ["sandra", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "Утренний стол уже накрыт, но одного места не хватает. Аманда первой замечает пустую скамью Мелиссы и с ленивой усмешкой тянет: \"Вот увидите, сейчас она явится с таким лицом, будто всю ночь воевала с нечистой силой.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    vscene MelissaStaticData.image_path("bats", "yawns")
    $ scene_runtime.text = "В этот момент в кухню, зевая и еле переставляя ноги, входит Мелисса. Вид у нее злой и невыспавшийся."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    vscene MelissaStaticData.image_path("kitchen", "work")
    $ scene_runtime.text = "Мелисса садится за стол и, даже взяв кружку, продолжает коситься так, будто над ее головой все еще что-то шуршит."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Сандра уже спокойнее говорит: \"У нас уже была крысиная проблема, из-за которой портились припасы, а теперь еще и летучие мыши? После крыс в кладовой я не хочу ждать, пока новая дрянь опять испортит дом.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    if relationship_anger("amanda") > 0 and relationship_anger("melissa") > 0:
        $ scene_runtime.text = "Аманда не удерживается: \"Может, это все за тобой ходит? Крысы, летучие мыши... Ведьма у нас завелась, вот и зверье сбежалось.\""
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
        $ scene_runtime.text = "Мелисса ставит кружку на стол. \"Если я ведьма, Аманда, начну с тебя. Заколдую, чтобы ты одно утро помолчала.\""
    elif relationship_anger("amanda") > 0:
        $ scene_runtime.text = "Аманда цепляет ее резче обычного: \"Крысы, летучие мыши... Может, они все к тебе, Мелисса? Ведьма при хозяйстве, да?\""
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
        $ scene_runtime.text = "Мелисса зло щурится: \"Если я ведьма, то первым делом заколдую кое-кому язык, чтобы он хоть за завтраком помолчал.\""
    elif relationship_anger("melissa") > 0:
        $ scene_runtime.text = "Аманда тут же оживляется, складывает пальцы в дразнящий знак и тянет с ухмылкой: \"Мелисса, а что если ты настоящая ведьма? Крысы в подвале, мыши с крыльями под крышей... Может, это все твои любимцы сбежались?\""
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
        $ scene_runtime.text = "Мелисса отвечает ровно: \"Продолжай. Если я ведьма, мне как раз нужен кто-то болтливый для первого проклятия.\""
    else:
        $ scene_runtime.text = "Аманда тут же оживляется, складывает пальцы в дразнящий знак и тянет с ухмылкой: \"Мелисса, а что если ты настоящая ведьма? Крысы в подвале, мыши с крыльями под крышей... Может, это все твои любимцы сбежались?\""
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
        $ scene_runtime.text = "Мелисса зло щурится: \"Если я ведьма, то первым делом заколдую кое-кому язык, чтобы он хоть за завтраком помолчал.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Разговор за столом быстро становится серьезнее. У вас в голове остается одна ясная мысль: с комнатой Мелиссы придется разбираться всерьез."
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
    call TavernKitchenFinishBreakfastEvent
    return True


label story_melissa_bat_problem_1:
    $ renpy.dynamic("_melissa_bat_problem_1_choice")
    show screen main_ui
    $ _melissa_bat_problem_1_choice = ""
    vscene tavern_melissa_room_picture()
    $ scene_runtime.text = "Проходя по коридору наверху, вы слышите из комнаты Мелиссы тревожный шум: скрип кровати, злой шепот и какое-то нервное шевеление под самым потолком. Заглянув внутрь, вы видите, что Мелисса не спит и сидит на кровати, зло глядя вверх.\n\n\"О, хорошо, что ты здесь,\" шепчет она почти сразу. \"Опять эта дрянь над головой возится. То шорох, то писк, то будто кто-то бегает по балкам. Я уже не знаю, что хуже: сам шум или то, что после такой ночи утром стоишь как пьяная. Если можешь, помоги мне с этим по-человечески.\""
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Сказать, что вы разберетесь с этим":
            $ _melissa_bat_problem_1_choice = "promise"
            $ scene_runtime.text = "Вы обещаете, что не ограничитесь одними словами. Сначала вы внимательно осмотрите потолок и щели в ее комнате, а утром подниметесь на чердак над ней.\n\n\"Вот это уже похоже на дело,\" тихо отвечает Мелисса. \"Ладно. Если ты и правда туда полезешь, я хотя бы буду знать, что мне не чудится.\""
        "Успокоить Мелиссу":
            $ _melissa_bat_problem_1_choice = "comfort"
            $ scene_runtime.text = "Вы говорите Мелиссе чуть тише и спокойнее, чем обычно, что не отмахнетесь от ее жалоб. От этого она не перестает злиться на потолок, но по голосу слышно, что ей уже легче от одного того, что кто-то наконец воспринимает проблему всерьез."
        "Оставить ее на сегодня в покое":
            $ _melissa_bat_problem_1_choice = "leave"
            $ scene_runtime.text = "Вы решаете пока не затягивать ночной разговор. Мелисса недовольно выдыхает, плотнее кутается в одеяло и снова косится на потолок."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(45)
    if _melissa_bat_problem_1_choice == "promise":
        $ Melissa.bat_attic_check_day = max(people_to_int(Melissa.bat_attic_check_day, -1), int(current_game_day() or 0))
        $ event_runtime.active_thread.advance()
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
    elif _melissa_bat_problem_1_choice == "comfort":
        $ Melissa.change_social(friend_delta=1)
    return True


label story_melissa_bat_problem_room_inspect:
    vscene tavern_melissa_room_picture()
    $ scene_runtime.text = "Вы внимательно осматриваете потолок и верхние балки в комнате Мелиссы. Под самым потолком обнаруживаются мелкие щели и темные норки в старом дереве, а сверху тянет пылью и затхлым чердаком. Теперь ясно: шум идет не из самой комнаты — дрянь пробирается сюда через старую крышу. Утром придется подняться наверх и проверить все над ее потолком."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(45)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_2:
    vscene "images/player_room/player_room_attic_1.png"
    $ scene_runtime.text = "Вы медленно обходите чердак вдоль стропил и почти сразу замечаете над той частью дома, где спит Мелисса, старые щели между досками и темные ходы в подгнившей обшивке.\n\nЕще через пару шагов находится и главная причина ночного шума. Под самой кровлей набилось сухое гнездовое тряпье, комки мха, помет и целая дрянная колония, давно обжившая балки и пустоты под крышей. Одним веником тут не обойтись: сначала эту пакость придется выкурить дымом, а потом уже по-настоящему заделывать щели."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(45)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_3:
    $ renpy.dynamic("_melissa_bat_problem_3_choice")
    show screen main_ui
    $ _melissa_bat_problem_3_choice = ""
    vscene "images/player_room/player_room_attic.png"
    $ scene_runtime.text = "Раздвинув старое тряпье и осторожно пригнувшись, вы находите маленькое слуховое окно над стороной дома, где расположена комната Аманды. Сквозь мутное стекло и щели в раме открывается слишком уж ясный вид на соседний двор.\n\n" + attic_neighbor_sex_scene_text() + " Вы невольно задерживаетесь у окна дольше, чем следовало бы."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Податься ближе":
            $ _melissa_bat_problem_3_choice = "fall"
        "Отступить от окна":
            $ _melissa_bat_problem_3_choice = "retreat"
            $ scene_runtime.text = "Вы отступаете от окна, пока старые доски под ногами еще держат. Гнездовище найдено, но с чердаком придется разбираться осторожнее."
    $ event_runtime.active_thread.advance()
    if _melissa_bat_problem_3_choice == "fall":
        call story_melissa_bat_problem_fall
    else:
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        $ calendar_v2.advance_minutes(45)
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_fall:
    vscene "images/player_room/batsProblem/fell_from_attic.png"
    "Вы тянетесь вперед еще на полшага, но старое дерево под ногами не выдерживает. Доска жалобно трещит, потом ломается, и в следующий миг вас с грохотом несет вниз вместе с пылью, щепками и куском прогнившего настила."
    "Несколько тяжелых мгновений вы лежите среди пыли и щепок, пытаясь понять, куда именно вас выбросило. С потолка свисают обломки, над головой зияет пролом, а вокруг слишком хорошо знакомые вещи из вашей комнаты."
    vscene "images/player_room/batsProblem/melissa in room.png"
    "Дверь распахивается как раз тогда, когда вы пытаетесь подняться. На пороге появляется Мелисса: растрепанная, злая, с одеялом и узлом вещей в руках. Она явно собиралась переждать ночь подальше от своей комнаты, но вместо этого застает вас посреди вашей собственной спальни, под грудой чердачного мусора."
    vscene "images/player_room/batsProblem/melissa in the room.png"
    "Мелисса смотрит на пролом, потом на вас, потом снова вверх. На ее лице за одно мгновение сменяются испуг, понимание и обида."
    vscene "images/player_room/batsProblem/melissa_talk.png"
    "\"Ты... ты извращенец!\" — срывается у нее голос. — \"Подглядывал оттуда? А потом еще и свалился сюда через потолок?! Всё. Хватит. Сегодня же переберусь к Аманде. Там, по крайней мере, потолок на голову не падает!\""
    $ scene_runtime.text = "Вы провалились с чердака в свою комнату как раз в тот момент, когда Мелисса пришла сюда с вещами. Объясняться сейчас бесполезно: история вышла слишком громкой и слишком стыдной."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(45)
    $ Melissa.drawings_ready_day = int(current_game_day() or 0) + 2
    $ Melissa.temp_room_code = "TavernAmandaRoom"
    $ Melissa.change_social(friend_delta=-7)
    $ Amanda.change_social(friend_delta=-5)
    $ player.change_stat("notoriety", 10)
    $ player.economy.tavern_fame = max(-20, int(player.economy.tavern_fame or 0) - 2)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_5:
    if int(effective_player_exploration() or 0) <= 120:
        $ scene_runtime.text = "Пока Мелисса вынужденно ночует у Аманды, ее собственная комната остается непривычно тихой. Вы осматриваете ее внимательнее обычного: ларь, табурет, складки одеяла, щель между стеной и кроватью. Однако за сорок пять минут поисков ничего важного в глаза так и не бросается."
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        $ calendar_v2.advance_minutes(45)
    else:
        vscene MelissaStaticData.image_path("bedroom_search", "booklet")
        "Пока Мелисса вынужденно ночует у Аманды, ее собственная комната остается непривычно тихой. Вы осматриваете ее внимательнее обычного: ларь, табурет, складки одеяла, щель между стеной и кроватью."
        "Под кроватью Мелиссы, задвинутый почти к самой стене, обнаруживается потертый рисованный буклет. Обложка ничего не объясняет, зато место, где его прятали, говорит само за себя."
        $ Melissa.drawings_found = True
        $ scene_runtime.text = "Под кроватью Мелиссы вы нашли потертый рисованный буклет. Теперь его можно рассмотреть как найденный предмет."
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        $ calendar_v2.advance_minutes(45)
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
        $ main_ui_runtime.action_title = "Комната Мелиссы"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    return True


label MelissaBookletOpenPreview:
    vscene MelissaStaticData.image_path("bedroom_search", "lewd_pages")
    $ scene_runtime.text = "Вы раскрываете буклет на первых страницах. Манера уверенная, линии смелые, а сюжеты вовсе не девичьи."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(5)
    if int(player.item_count("melissa_drawings_booklet_001") or 0) > 0:
        call PlayerCardInventoryItemMenu("melissa_drawings_booklet_001", True)
    else:
        call TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001", True)
    return


label ReadMelissaBooklet:
    vscene MelissaStaticData.image_path("bedroom_search", "booklet")
    "Вы достаете спрятанную пачку рисунков и осторожно разворачиваете потертые листы."
    vscene MelissaStaticData.image_path("bedroom_search", "lewd_pages")
    "Первые страницы выглядят почти как упражнение в линии и тени, но позы и детали быстро выдают совсем другой интерес автора."
    vscene MelissaStaticData.cycle_image("bedroom_search", "lewd_pages", 1)
    "На следующих листах осторожность исчезает: тела нарисованы смело, без стыда, будто тот, кто держал перо, слишком хорошо представлял себе каждое движение."
    vscene MelissaStaticData.cycle_image("bedroom_search", "lewd_pages", 2)
    $ player_apply_arousal_trigger("melissa_booklet", 18)
    "К концу просмотра мысли становятся тяжелее и жарче. Это уже не просто любопытство: картинки цепляют тело быстрее, чем вы успеваете отвести взгляд."
    $ calendar_v2.advance_minutes(10)
    $ Melissa.drawings_booklet_read = True
    if int(player.item_count("melissa_drawings_booklet_001") or 0) > 0:
        call PlayerCardInventoryItemMenu("melissa_drawings_booklet_001", True)
    else:
        call TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001", True)
    return


label MelissaBookletTake:
    call Take("melissa_drawings_booklet_001", "TavernMelissaRoom", "", "melissa_drawings_booklet_001")
    if int(player.item_count("melissa_drawings_booklet_001") or 0) > 0:
        $ Melissa.drawings_booklet_left = False
    $ main_ui_runtime.object_id = ""
    $ main_ui_runtime.action_title = "Комната Мелиссы"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    return


label MelissaBookletLeaveThere:
    vscene MelissaStaticData.image_path("bedroom_search", "booklet")
    $ scene_runtime.text = "Вы аккуратно возвращаете буклет туда, где нашли. Теперь вы знаете, что искать и где смотреть, не выдавая того, что уже обнаружили тайник."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ Melissa.drawings_booklet_left = True
    call TavernMelissaRoomObjectMenu("melissa_drawings_booklet_001", True)
    return


label MelissaBookletContinueSearch:
    $ main_ui_runtime.object_id = ""
    $ scene_runtime.text = "Вы оставляете буклет пока лежать под кроватью и продолжаете осматривать комнату."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Комната Мелиссы"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    return


label story_melissa_bat_problem_4:
    vscene "images/player_room/player_room_attic_1.png"
    if int(player.item_count("bat_repellent_001") or 0) > 0:
        $ scene_runtime.text = "Вы раскладываете дымную смесь между балок, даете ей как следует разгореться и быстро отступаете. Чердак наполняется густым едким дымом из мха, лаванды и трав. Из-под крыши с писком и хлопаньем вырываются летучие мыши.\n\nГнездовище вы наконец выкурили, но на одном дыме дело не закончится: пока крышу не заделают как следует, щели останутся и вся пакость со временем полезет обратно."
    else:
        $ scene_runtime.text = "Теперь уже ясно, что под крышей свилось настоящее гнездовище. Просто так его не вымести: сначала нужна едкая дымная смесь, чтобы выгнать всю эту дрянь из-под кровли."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(45)
    if int(player.item_count("bat_repellent_001") or 0) > 0:
        $ player.remove_item("bat_repellent_001", 1)
        $ event_runtime.active_thread.advance()
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
    return True


label story_melissa_bat_problem_roof:
    vscene "images/player_room/player_room_attic_1.png"
    if int(player.economy.money or 0) >= 1000:
        $ scene_runtime.text = "Вы договариваетесь о починке старой крыши и отдаете за работу тысячу монет. Теперь остается только дождаться, пока мастера перетянут гнилые доски, забьют щели и приведут верх трактира в порядок. Обещают управиться за пару дней."
    else:
        $ scene_runtime.text = "Летучих мышей вы уже выкурили, но без починки крыши дело не закончить. Денег на мастеров пока не хватает."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(45)
    if int(player.economy.money or 0) >= 1000:
        $ player.spend_money(1000)
        $ Melissa.roof_repair_complete_day = int(current_game_day() or 0) + 2
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
        call stat
    return True


label story_melissa_bat_problem_6:
    vscene MelissaStaticData.image_path("portrait", "thanks")
    $ scene_runtime.text = "Вы говорите Мелиссе, что на этот раз все действительно закончено: чердачное гнездовище выжжено, щели под крышей забиты, а над ее комнатой теперь наконец тихо. Она сперва смотрит на вас с привычной настороженностью, будто все еще ждет подвоха, но потом сама коротко выдыхает и впервые за все это время заметно расслабляется.\n\n\"Значит, можно снова спать у себя и не ждать, что ночью над головой начнут бегать, пищать и сыпать трухой...\" Она качает головой, будто сама до конца не верит в удачу, а потом уже тише добавляет: \"Спасибо. Не за слова — за то, что ты и правда довел дело до конца.\"\n\nПохоже, история с летучими мышами и чердаком для Мелиссы наконец действительно закрыта."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(45)
    $ event_runtime.active_thread.advance()
    $ Melissa.complete_bats_problem()
    $ Melissa.change_social(friend_delta=3, open_delta=2)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    return True


label story_melissa_courtship_touch_0:
    $ main_ui_begin_native_scene_state("Сближение с Мелиссой")
    show screen main_ui
    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "После всего, что случилось с ее комнатой и чердаком, Мелисса уже не избегает вашего общества, но по-прежнему внимательно следит, не попытаетесь ли вы торопить ее."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Осторожно коснуться Мелиссы":
            $ Melissa.change_social(open_delta=1, corruption_delta=1)
            $ player.change_stat("fun", 1)
            $ Melissa.mark_fucked()
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
            $ scene_runtime.text = "Вы осторожно прикасаетесь к Мелиссе, будто заранее давая ей возможность остановить вас. Она тихо выдыхает, смотрит в сторону и почти неслышно говорит, что так можно."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
        "Не торопить события":
            $ scene_runtime.text = "Вы не давите на Мелиссу и оставляете решение о следующем шаге на другой день."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_courtship_kiss_1:
    $ main_ui_begin_native_scene_state("Сближение с Мелиссой")
    show screen main_ui
    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Мелисса вспоминает ваше прежнее осторожное прикосновение и сегодня остается рядом чуть дольше, чем нужно для обычного разговора."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Осторожно поцеловать Мелиссу":
            $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=1)
            $ player.change_stat("fun", 2)
            $ Melissa.mark_fucked()
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
            $ scene_runtime.text = "Вы не спешите и сначала просто касаетесь ее руки. Мелисса не отстраняется, а когда вы осторожно целуете ее, отвечает коротко, неловко, но уже без прежней настороженности."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
        "Не торопить события":
            $ scene_runtime.text = "Вы замечаете ее волнение и оставляете поцелуй на другой день. Мелисса благодарно улыбается."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_courtship_deep_kiss_2:
    $ main_ui_begin_native_scene_state("Сближение с Мелиссой")
    show screen main_ui
    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Теперь Мелисса уже понимает, чего вы хотите, и не отступает, когда вы подходите ближе. Но она все еще ждет, что вы позволите ей самой выбрать темп."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить поцелуй":
            $ Melissa.change_social(friend_delta=1, open_delta=2, corruption_delta=2)
            $ player.change_stat("fun", 2)
            $ Melissa.mark_fucked()
            $ calendar_v2.advance_minutes(20)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
            $ scene_runtime.text = "Поцелуй становится заметно глубже и дольше. Мелисса отвечает уже не из одной только осторожности: сперва несмело, потом все горячее, будто сама удивляется тому, как быстро перестает считать секунды."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
        "Остановиться на разговоре":
            $ scene_runtime.text = "Вы сохраняете теплую близость, но не превращаете ее в новый шаг раньше времени."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_courtship_fondle_3:
    $ main_ui_begin_native_scene_state("Сближение с Мелиссой")
    show screen main_ui
    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Мелисса отвечает на поцелуй увереннее прежнего и не спешит разрывать объятие, хотя напряжение в ее плечах выдает, насколько важна для нее возможность остановить вас."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Позволить себе более смелые ласки":
            $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=2)
            $ player.change_stat("fun", 2)
            $ Melissa.mark_fucked()
            $ calendar_v2.advance_minutes(20)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
            $ scene_runtime.text = "Вы держитесь мягко, но позволяете себе чуть больше близости, чем раньше. Мелисса краснеет, шепотом просит не давить на нее и все же остается рядом, явно запоминая это как шаг, который она сама разрешила."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
        "Остановиться на поцелуях":
            $ scene_runtime.text = "Вы не переходите установленную Мелиссой границу. Она расслабляется и остается рядом еще немного."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_courtship_underclothes_4:
    $ main_ui_begin_native_scene_state("Сближение с Мелиссой")
    show screen main_ui
    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Сегодня Мелисса сама сокращает расстояние между вами. В ее движениях еще остается робость, но прежней попытки спрятаться за ней уже нет."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Коснуться ее под одеждой":
            $ Melissa.change_social(friend_delta=1, open_delta=2, corruption_delta=3)
            $ player.change_stat("fun", 3)
            $ Melissa.mark_fucked()
            $ calendar_v2.advance_minutes(20)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
            $ scene_runtime.text = "Ваши руки скользят уже смелее, под ткань и вдоль теплой кожи. Мелисса вздрагивает, судорожно выдыхает вам в плечо и все же не останавливает, только шепотом просит не заходить дальше, чем она сейчас готова выдержать."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
        "Не заходить дальше":
            $ scene_runtime.text = "Вы оставляете последний шаг на другой день. Мелисса не скрывает облегчения от того, что ее границу снова услышали."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
    $ main_ui_end_native_scene_state()
    return True


label event_melissa_waitress_fall(eyewitness=0, result="", tavern_loss=0, relationship_delta=0, outcome_text=""):
    $ tavern_loss = min(1, max(0, int(player.tavern_management.winenum or 0)))
    $ player.tavern_management.winenum = max(0, int(player.tavern_management.winenum or 0) - tavern_loss)
    $ result = "Во время работы в зале Мелисса зацепилась ногой за край доски, растянулась на полу и расплескала кружку выпивки."
    if tavern_loss > 0:
        $ result += " Потеряно %s бочонка вина." % DispFrac(tavern_loss)

    if eyewitness > 0:
        $ main_ui_begin_native_scene_state("Событие: неуклюжая официантка")
        show screen main_ui
        vscene MelissaStaticData.cycle_image("tavern", "clumsy_waitress", 0)
        $ scene_runtime.text = "Мелисса торопится между столами с полной кружкой, цепляется ногой за неровную половицу и с шумом падает. Выпивка растекается по полу, а посетители поворачиваются посмотреть на переполох."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Подойти к Мелиссе":
                pass

        vscene MelissaStaticData.cycle_image("tavern", "clumsy_waitress", 1)
        $ scene_runtime.text = "Мелисса сидит на полу возле опрокинутой кружки. Она явно ушиблась и теперь со стыдом ждет, как вы отреагируете на ее падение и потерянную выпивку."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Помочь Мелиссе подняться":
                $ relationship_delta = procedural_randint(1, 2, "melissa_waitress_fall_help_%s" % current_game_day())
                $ Melissa.change_social(friend_delta=relationship_delta)
                vscene MelissaStaticData.cycle_image("tavern", "clumsy_waitress", 2)
                $ outcome_text = "Вы протягиваете Мелиссе руку и помогаете подняться, не позволяя насмешкам посетителей разгореться. Она благодарно улыбается и, немного смущаясь, возвращается к работе."
            "Не обращать внимания":
                $ relationship_delta = procedural_randint(-1, 0, "melissa_waitress_fall_ignore_%s" % current_game_day())
                $ Melissa.change_social(friend_delta=relationship_delta)
                if relationship_delta < 0:
                    $ outcome_text = "Вы оставляете Мелиссу разбираться самой. Она молча поднимается и убирает разлитое, но ваш демонстративный холод явно ее задел."
                else:
                    $ outcome_text = "Вы не вмешиваетесь. Мелисса быстро приходит в себя, убирает разлитое и возвращается к столам, стараясь больше не привлекать внимания."
            "Отчитать за неуклюжесть и потерю":
                $ relationship_delta = -procedural_randint(1, 2, "melissa_waitress_fall_scold_%s" % current_game_day())
                $ Melissa.change_social(friend_delta=relationship_delta)
                $ outcome_text = "Вы резко отчитываете Мелиссу за неуклюжесть и испорченную выпивку. Она краснеет, торопливо убирает за собой и возвращается к работе, избегая смотреть в вашу сторону."

        $ scene_runtime.text = outcome_text
        $ scene_runtime.location_text = outcome_text
        menu:
            "Вернуться к работе":
                pass
        $ main_ui_end_native_scene_state()

    return result
