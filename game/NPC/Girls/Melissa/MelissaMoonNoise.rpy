# The ordered post-roof lunar investigation is owned by melissaMoonNoise.

init python:
    def moon_stove_npc_available(npc_id):
        npc = people.get_info(npc_id)
        location = str(people.location(npc_id) or "")
        return (npc_id in household.resident_ids()
                and (location.startswith("Tavern") or location in ("Backyard", "Shed", "ShedRuinedChamber"))
                and not npc.sex_busy() and not npc.is_working())


label story_melissa_moon_noise_0:
    $ main_ui_begin_native_scene_state("Ночной шум")
    show screen main_ui
    vscene "images/tavern/secondfloor/second_floor.png"
    $ scene_runtime.text = "Верхний коридор уже затих. Крыша починена, летучих мышей больше нет, но за дверями жилых комнат снова не спят."
    if Amanda.sex_stat("virginity", True):
        $ scene_runtime.text += "\n\nАманда спрашивает из своей комнаты, слышит ли Мелисса шум над крышей."
    if Melissa.sex_stat("virginity", True):
        $ scene_runtime.text += " Из комнаты Мелиссы доносится: «Ты тоже слышишь этот стук?»"
    if Clara.tavern_resident() and Clara.sex_stat("virginity", True):
        $ scene_runtime.text += " За другой дверью Кларисса спрашивает, кто опять стучит над крышей."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Запомнить, откуда доносится шум":
            pass
    $ calendar_v2.advance_minutes(10)
    $ event_runtime.active_thread.advance()
    $ event_runtime.active_thread.setDay()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_breakfast_1:
    $ main_ui_begin_native_scene_state("Завтрак: шум вернулся")
    show screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "За столом вспоминают ночной стук над спальнями. После ремонта крыши обвинить в нем летучих мышей уже не выходит."
    if "amanda" in tavern_breakfast_present_ids() and Amanda.sex_stat("virginity", True):
        $ scene_runtime.text += "\n\nАманда подтверждает, что тоже слышала ночной шум."
    if "melissa" in tavern_breakfast_present_ids() and Melissa.sex_stat("virginity", True):
        $ scene_runtime.text += "\n\nМелисса сердито отодвигает миску: «Снова всю ночь слышала. Не надо говорить, что мне показалось. Я эту крышу теперь наизусть знаю»."
    if "clara" in tavern_breakfast_present_ids() and Clara.tavern_resident() and Clara.sex_stat("virginity", True):
        $ scene_runtime.text += "\n\nКларисса неожиданно перестает улыбаться: «И я слышала. Это не мыши и не ветер»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пообещать снова осмотреть чердак":
            pass
    $ calendar_v2.advance_minutes(10)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_roof_check_2:
    $ main_ui_begin_native_scene_state("Повторный осмотр чердака")
    show screen main_ui
    vscene attic_room_picture_path()
    $ scene_runtime.text = "Вы снова перебираетесь между балками над комнатами. Новые доски сухие и целые, щели заделаны, а в старом гнездовье пусто. Ни летучих мышей, ни свежего помета, ни следов того, кто мог стучать здесь ночью."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться вниз с этим известием":
            pass
    $ calendar_v2.advance_minutes(20)
    $ event_runtime.active_thread.advance()
    $ event_runtime.active_thread.setDay()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_sandra_story_3:
    $ main_ui_begin_native_scene_state("Завтрак: старая история")
    show screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "Услышав, что на чердаке опять пусто, Сандра откладывает ложку. «Перед полнолунием у нас в деревне тоже стучало над крышей. Старухи говорили: это козёл-оборотень ищет девственниц. Сначала стук, потом такой сон, что просыпаешься горячая и сама тянешься под одеяло. Остальные ничего не слышат. Я слышала»."
    if "amanda" in tavern_breakfast_present_ids():
        if Amanda.sex_stat("virginity", True):
            $ scene_runtime.text += "\n\n«Правда? — Аманда вскидывает брови. — Я тоже слышала. Только мне после этих снов вовсе не плохо: просыпаюсь горячая и довольная, а потом весь день хочется смеяться». Сандра бросает на неё внимательный взгляд."
        else:
            $ scene_runtime.text += "\n\nАманда молча вертит ложку в пальцах. На этот раз ей нечего прибавить к разговору."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Попросить Сандру продолжить":
            pass
    $ scene_runtime.text = "«Мать отвела меня к брату Илматтера. Он выспросил всё, что мне снилось, пообещал избавить от ночей с этим стуком, а потом изнасиловал. Девственности не стало — стук стих. Но не называйте это чудом и не верьте тому, кто требует вашего тела ради защиты», — говорит Сандра. За столом становится тихо."
    if "melissa" in tavern_breakfast_present_ids() and Melissa.sex_stat("virginity", True):
        $ scene_runtime.text += "\n\nМелисса первой нарушает молчание: «И что же нам делать? Неужели другого способа нет?»"
    if "amanda" in tavern_breakfast_present_ids() and Amanda.sex_stat("virginity", True):
        $ scene_runtime.text += "\n\nАманда уже без смешков кивает: «Вот это и я хотела спросить»."
    if "clara" in tavern_breakfast_present_ids() and Clara.sex_stat("virginity", True):
        $ scene_runtime.text += "\n\nКларисса сжимает край скатерти: «Должен же быть способ не отдавать себя первому встречному»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выслушать ответ Сандры":
            pass
    $ scene_runtime.text = "«Одна девчонка у нас каждую ночь натирала свою киску до оргазма — говорила, так легче уснуть, хотя стук потом возвращался. Можно найти и любовника, если сама ему доверяешь. Но старухи знали ещё один способ», — продолжает Сандра и, оглядев притихший стол, понижает голос."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Слушать про старую печь":
            pass
    $ scene_runtime.text = "«В старой печи, говорили, живёт домовой Олли. В полнолуние ровно в полночь надо подойти к печному окошку и три раза сказать: „Олли, Олли, защити меня от того, кто приходит во сне“. Потом поднять сорочку и подставить зад к окошку. Если Олли сочтёт тебя доброй и послушной, из темноты покажется мягкая мохнатая рука и коснётся тебя — значит, он согласен помочь. Не коснётся — не обижайся: домового не заставишь. Я бы на вашем месте сперва подумала, кому из живых можно довериться», — заканчивает Сандра."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вспомнить старую печь в сарае":
            pass
    $ calendar_v2.advance_minutes(15)
    $ event_runtime.active_thread.advance()
    $ event_runtime.active_thread.setDay()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_noise_repeat:
    $ main_ui_begin_native_scene_state("Ночной шум")
    show screen main_ui
    vscene "images/tavern/secondfloor/second_floor.png"
    $ scene_runtime.text = "С наступлением нового лунного месяца женщины, которые всё ещё слышат ночной шум, снова жалуются на него. После осмотра крыши винить летучих мышей вы уже не можете."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Запомнить эту ночь":
            pass
    $ calendar_v2.advance_minutes(5)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_window_clue_0:
    $ main_ui_begin_native_scene_state("Окно во двор")
    show screen main_ui
    $ renpy.dynamic("_moon_follow", "_moon_destination", "_moon_exit")
    vscene "images/player_room/windowAmand.png"
    $ scene_runtime.text = "Во дворе Аманда,.пописав,она встала , промакнула подолом ночнушки свой лобок, не пошла как обычно спать,а оглянувшись вокруг направилась к сараю."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_enters_shed.png"
    $ scene_runtime.text = "И шмыгнула во внутрь. Вас просто распирает от любопытсва, А не пойти ли и посмотреть?"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Да":
            $ _moon_follow = True
        "Нет":
            $ _moon_follow = False
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    if _moon_follow:
        python:
            for _moon_destination in ["TavernUpstairs","TavernMain","TavernKitchen","Backyard","Shed"]:
                _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
                apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
                rooms.enter(_moon_destination)
        call checkTriggers("Shed", "enter", 0)
        python:
            for _moon_destination in ["Backyard","TavernKitchen","TavernMain","TavernUpstairs","TavernMyRoom"]:
                _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
                apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
                rooms.enter(_moon_destination)
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    $ main_ui_runtime.object_id = ""
    $ main_ui_runtime.action_items = tavern_my_room_action_items()
    $ scene_runtime.picture = tavern_my_room_dynamic_picture()
    $ scene_runtime.text = tavern_my_room_dynamic_text()
    $ scene_runtime.location_text = scene_runtime.text
    return True


label story_melissa_moon_shed_check_1:
    $ main_ui_begin_native_scene_state("Аманда у старой печи")
    show screen main_ui
    $ renpy.dynamic("_moon_destination", "_moon_exit")
    python:
        for _moon_destination in ["ShedRuinedChamber"]:
            _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
            apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
            rooms.enter(_moon_destination)
    vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    $ scene_runtime.text = "Вы потихонечку заглядываете во внутрь, Аманда внимательно изучает старинную печь и даже заглядывает во внутрь!"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    $ scene_runtime.text = "вот так история! подумали Вы, видать рассказ Сандры был воспринят чертовкой всерьёз"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_surprised_closeup.png"
    $ scene_runtime.text = "Друг из-печи раздался странный звук, глухой полу-стон полу вой, преведший Аманду в ужас,\nОхнув она поспешно ретировалась и , пулей вылетев из сарайчика,поспешно ретировалась в трактир!\nВы еле увернулись и чудом не были замечены."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "пойду-ка я отсюда.":
            pass
    $ calendar_v2.advance_minutes(5)
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    python:
        for _moon_destination in ["Shed"]:
            _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
            apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
            rooms.enter(_moon_destination)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_second_window_2:
    $ main_ui_begin_native_scene_state("Две сорочки у сарая")
    show screen main_ui
    $ renpy.dynamic("_moon_follow", "_moon_destination", "_moon_exit")
    vscene "images/tavern/backyard/shed/ghostEvent/window_clue.png"
    $ scene_runtime.text = "Сегодня у сарая уже две белые сорочки. Аманда что-то объясняет, указывая на дверь; Мелисса слушает и поглядывает на окна. Потом обе скрываются внутри"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пойти проверить":
            $ _moon_follow = True
        "Пока остаться у окна":
            $ _moon_follow = False
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    if _moon_follow:
        python:
            for _moon_destination in ["TavernUpstairs","TavernMain","TavernKitchen","Backyard","Shed"]:
                _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
                apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
                rooms.enter(_moon_destination)
        call checkTriggers("Shed", "enter", 0)
        python:
            for _moon_destination in ["Backyard","TavernKitchen","TavernMain","TavernUpstairs","TavernMyRoom"]:
                _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
                apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
                rooms.enter(_moon_destination)
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    $ main_ui_runtime.object_id = ""
    $ main_ui_runtime.action_items = tavern_my_room_action_items()
    $ scene_runtime.picture = tavern_my_room_dynamic_picture()
    $ scene_runtime.text = tavern_my_room_dynamic_text()
    $ scene_runtime.location_text = scene_runtime.text
    return True


label story_melissa_moon_shed_conversation_3:
    $ main_ui_begin_native_scene_state("Разговор у печи")
    show screen main_ui
    $ renpy.dynamic("_moon_destination", "_moon_exit")
    python:
        for _moon_destination in ["ShedRuinedChamber"]:
            _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
            apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
            rooms.enter(_moon_destination)
    vscene "images/tavern/backyard/shed/ghostEvent/stove_conversation.png"
    $ scene_runtime.text = "Вы останавливаетесь за перегородкой. Аманда и Мелисса стоят перед разваленной печью и говорят вполголоса"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Послушать":
            pass
    $ scene_runtime.text = "Аманда: «Если Олли правда такой мохнатый, как Сандра говорит, зимой ему цены не будет»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Мелисса: «Ахаха эт же не кошечка какая в кровать тащить\nСперва узнай, дома ли он. Свободен ли он, Вдруг ты с чужим домовым заигрываешь?)\nИли вдруг ты ему на ощупь не понравишься? ааа?»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Аманда: «Ой ой смотрите королева сранделей нашлась,хаха Посмотрим чья попка лучше хаха.»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    if Amanda.sex_stat("virginity", True):
        $ scene_runtime.text = "Аманда: «Так,кароче не хочешь,так и скажи Мэл. Мне тож ссыкотно, но козел с снов надоел. Он на Херхарда похож.»"
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Далее":
                pass
    $ scene_runtime.text = "Меллисса: «не вместе пойдем. По очереди,есличто будем орать»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Мелисса: «Ну всё) договорились, панталоны снять не забудь только!»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Аманда: «Тише,ты корова.»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Мелисса: «Сама, корова»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Мелисса: «или попкой как вертеть будешь», ехидно говорит Мелисса."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Аманда: «не ссы ты»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Сквозняк протискивается в трещину над топкой. Из каменного нутра выходит низкое, глухое „у-у-ум“. Обе разом перестают улыбаться\n\nАманда: «Это ты?»\nМелисса: «Че совсем дура,вааще...блин!»\nАманда: «Тогда завтра. Сегодня он, кажется, занят»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Далее":
            pass
    $ scene_runtime.text = "Они торопливо выбираются из каморки. Вы остаётесь у перегородки, пока их шаги не стихают во дворе. Теперь вы знаете и место, и время"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться в трактир и подготовиться к завтрашней ночи":
            pass
    $ calendar_v2.advance_minutes(10)
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    python:
        for _moon_destination in ["Shed"]:
            _moon_exit = next(exit for exit in rooms.current.exits if exit.target == _moon_destination)
            apply_movement_time(_moon_exit.minutes_to_pass, _moon_destination)
            rooms.enter(_moon_destination)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_stove_wait_1:
    $ main_ui_begin_native_scene_state("В старой печи")
    show screen main_ui
    $ renpy.dynamic("_moon_route", "_moon_participants", "_moon_ritual_participants", "_moon_npc", "_moon_npc_id")
    vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    $ scene_runtime.text = "Вы пригибаетесь и забираетесь во внутрь печи. Под ладонью холодная кирпичная кладка. Из каморки вас не видно, зато отсюда слышен каждый шаг и хорошо видно окно в печь"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Затаиться до полуночи":
            pass
        "Надеть меховую перчатку и ждать" if player.item_count("fur_glove_001") > 0 and player.equipment.hand != "fur_glove_001":
            $ player.equip("fur_glove_001", "hand")
        "Передумать и выбраться":
            $ main_ui_end_native_scene_state()
            return True
    $ _moon_route = "glove" if player.item_count("fur_glove_001") > 0 and player.equipment.hand == "fur_glove_001" else "no_glove"
    $ _moon_participants = ["amanda", "melissa"]
    $ _moon_ritual_participants = [npc_id for npc_id in _moon_participants if people.get_info(npc_id).sex_stat("virginity", True)]
    $ calendar_v2.advance_minutes(1440 - calendar_v2.clock_minutes())
    vscene "images/tavern/backyard/shed/ghostEvent/stove_conversation.png"
    $ scene_runtime.text = "Дверь скрипит. Сегодня девушки говорят ещё тише, но шутить Аманда всё равно не перестаёт\n\nАманда: «Ну, Олли, надеюсь, ты не пригласил сюда всех своих друзей извращенцев»\nМелисса: «И надеюсь, ты не собираешься знакомиться сразу со всеми его родственниками»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Остаться в укрытии":
            pass
    if _moon_route == "glove":
        if "amanda" in _moon_ritual_participants:
            vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_stove.png"
            $ scene_runtime.text = "Аманда подходит к печи первая, задирает подол ночнушки и сует попку во внутрь.\n- Ну ,Мелиска была не была."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/amanda/AmandaTrialF.png"
            $ scene_runtime.text = "Перед вами открылись соблазнительные округлости. Аманда нетерпеливо шевелила орешками из стороны в сторону."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_fur_touch.png"
            $ scene_runtime.text = "Вы осторожно протягиваете руку в перчатке и проводите Мехом по промежности Аманды. Она вздрагивает и тихо стонет."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_surprised_closeup.png"
            $ scene_runtime.text = "От неожиданности Аманда взвизгивает и невольно сжимает промежность. Ой,вау щикотно и приятно...Хи хи... невольно вглядывается в темноту и расслабляет булки,что позволяет вам безопасно убрать руку. Слышен легкий смешок.  Вау,Мелиска..."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_laughing_stove_closeup.png"
            $ scene_runtime.text = "-Мелисса: Ну ты даешь! Че правда? потрогал? а ты меня не дуришь?\nАманда одергивает подол и чепчет ,давай суй жопу пока не поздно,пока он не передумал..."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
        if "melissa" in _moon_ritual_participants:
            vscene "images/tavern/backyard/shed/ghostEvent/melissa/melissa_stove.png"
            $ scene_runtime.text = "Мелисса неуверенно подходит к печи, задирает подол ночнушки и ,изогнув изящно свою смуглую попку,суёт её во внутрь."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/melissa/MelissaTrialF.png"
            $ scene_runtime.text = "Вы, выждав момент, нежно касаетесь ягодиц Мелиссы,и чувствуете как податливо они прижимаются к вам. Оухх ххх Ам.... Аххх! Вау вы,сжали одну из ягодиц и шлепнули легонько по её промежности. Ай ..хи хи"
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/melissa/melissa_fur_touch.png"
            $ scene_runtime.text = "Немпого могладив и помяв слегка промежность вы решили,что этого достаточно и легонько шлёпнув по оттопыренным навстречу ягодицам,вы осторожно убираете руку. Мелисса тихо вздыхает и шепчет: \"Ой,вау щикотно и приятно...аж горит всё ...\"."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/melissa/melissa_surprised_closeup.png"
            $ scene_runtime.text = "Аманда похотливо улыбаясь, смотрит на расшриренные от изумления и приятных ощущений глаза Мелиссы. Она тихо шепчет: \"Вау,ты даёшь! Че правда? потрогал? а ты меня не дуришь?\"а!? я ж тебе говорила."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
            vscene "images/tavern/backyard/shed/ghostEvent/melissa/melissa_laughing_stove_closeup.png"
            $ scene_runtime.text = "Мелисса не обращая внимания на колькости товарки,признается Вау! кажется я кончила,аж коленки подогнулись такой пушистик ласковый... И итерично захохотала..."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Далее":
                    pass
        vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
        $ scene_runtime.text = "Пару минут удовлетворенного и похотливого хихиканья прервались, протяжным гулом с причмокиванием. Звучало низко гулко и зловеще в сарае пописла тишина...\n\nАманда: «Мош он тоже того, кончил?!»\nМелисса: «Ну оннам об этом не скажет,но звучало пугающе... пошли отсюд поскорей а то у меня аж соски затвердели дубор такой»"
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Далее":
                pass
        vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
        $ scene_runtime.text = "Дверь хлопает. Шаги и хихиканье поспешно удаляются через двор. Вы ещё немного сидите в печи, потом выбираетесь наружу. \nНочная затея закончилась приятно и удачно,у вас дымится шишка,Перчатка покрыта липкой смазкой странно пахнущей смазкой.После ночной авантюры вам необходимо выспаться и отдохнуть,а завтра будет новый день."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Выбраться из печи и вернуться в трактир":
                pass
    else:
        vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_surprised_closeup.png"
        $ scene_runtime.text = "Девушки ждут ответа от Олли, но из холодной печи никто не отзывается."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Далее":
                pass
        vscene "images/tavern/backyard/shed/ghostEvent/melissa/melissa_surprised_closeup.png"
        $ scene_runtime.text = "Над головой снова протяжно загудело. На этот раз звук прошёл прямо по кирпичам."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Далее":
                pass
        vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
        $ scene_runtime.text = "Аманда: «А вот это он сказал по-настоящему!»\nМелисса: «Поговорим с ним, когда он научится говорить словами!»\n\nДверь хлопает. Шаги поспешно удаляются через двор. Вы ещё немного ждёте в золе, потом выбираетесь наружу. Ночная затея закончилась; вопрос о том, кто тревожит девушек перед полнолунием, остался."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Выбраться из печи и вернуться в трактир":
                pass
    python:
        if event_runtime.active_thread.ritual_result is None:
            event_runtime.active_thread.ritual_result = {
                "route": _moon_route,
                "participants": _moon_participants,
                "ritual_participants": _moon_ritual_participants,
            }
            player.change_stat("fun", 5 if _moon_route == "glove" else 3)
            player.intimacy.add_arousal(10 if _moon_route == "glove" else 5)
            for _moon_npc_id in _moon_participants:
                _moon_npc = people.get_info(_moon_npc_id)
                _moon_npc.fun = max(0, min(100, int(_moon_npc.fun or 0) + (3 if _moon_route == "glove" else 2)))
                _moon_npc.add_arousal(10 if _moon_route == "glove" else 5)
                _moon_npc.change_social(open_delta=1)
    $ calendar_v2.advance_minutes(10)
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_stove_not_needed:
    $ main_ui_begin_native_scene_state("Старая печь")
    show screen main_ui
    vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    $ scene_runtime.text = "Аманда и Мелисса объясняют, что ночной шум больше их не тревожит. Проверять старую печь теперь незачем."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться в трактир":
            pass
    $ event_runtime.active_thread.ritual_result = {"route": "not_needed", "participants": ["amanda", "melissa"], "ritual_participants": []}
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_amanda_moon_protection_0:
    $ main_ui_begin_native_scene_state("Ночная гостья")
    show screen main_ui
    vscene "images/player_room/amandaVisits/amanda_visit_0.jpg"
    $ scene_runtime.text = "У двери мнётся Аманда. «Не смей смеяться. Домовой нас выставил, а наверху опять стучит. Я немного побуду здесь. Если усну — утром скажешь, что пришла проверить окна»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пустить её и выслушать":
            $ event_runtime.active_thread.advance()
        "Проводить её обратно":
            pass
    $ calendar_v2.advance_minutes(15)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_protection_0:
    $ main_ui_begin_native_scene_state("Ночная гостья")
    show screen main_ui
    vscene "images/player_room/batsProblem/melissa in the room.png"
    $ scene_runtime.text = "Позже Мелисса тихо стучит в дверь. «У тебя тоже слышно? Я думала, после печи станет легче. Можно сегодня побыть здесь? Только не рассказывай утром всем за столом»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пригласить Мелиссу":
            $ event_runtime.active_thread.advance()
        "Проводить её в комнату":
            pass
    $ calendar_v2.advance_minutes(15)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_amanda_stove_debrief_0:
    $ main_ui_begin_native_scene_state("Ночной поход в сарай")
    show screen main_ui
    vscene "images/tavern/backyard/shed/ghostEvent/amanda/amanda_surprised_closeup.png"
    $ scene_runtime.text = "Защиту, конечно. А что ты подумал? — Аманда прищуривается. — Мелисса говорит, это был сквозняк. Очень воспитанный сквозняк: выслушал нас, а потом выставил обеих. Только Сандре не рассказывай, ладно?"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ Amanda.mark_asked()
    $ Amanda.mark_talked()
    $ calendar_v2.advance_minutes(5)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_stove_debrief_0:
    $ main_ui_begin_native_scene_state("Ночной поход в сарай")
    show screen main_ui
    vscene "images/tavern/backyard/shed/ghostEvent/melissa/melissa_surprised_closeup.png"
    $ scene_runtime.text = "Мы проверяли слова Сандры. Аманда делала вид, что ей совсем не страшно. Я ей почти поверила — до того самого звука. Печь как вздохнула, так у нас обеих вся смелость и кончилась."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ Melissa.mark_asked()
    $ Melissa.mark_talked()
    $ calendar_v2.advance_minutes(5)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_church_full_moon_bats_0:
    $ main_ui_begin_native_scene_state("Летучие мыши над собором")
    show screen main_ui
    vscene "images/church/fullMoonBatsEntry.png"
    $ scene_runtime.text = "Над шпилями мелькают тёмные крылья. Летучие мыши вылетают из-под каменного карниза, кружат перед луной и снова теряются у башни. На починенном чердаке трактира вы их не нашли. Здесь же, у собора, они явно чувствуют себя как дома."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Понаблюдать за карнизом":
            pass
        "Продолжить путь":
            pass
    $ Gerhard.set_var("church_full_moon_bats_seen", True)
    $ calendar_v2.advance_minutes(5)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True
