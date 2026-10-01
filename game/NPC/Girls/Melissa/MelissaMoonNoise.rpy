# The ordered post-roof lunar investigation is owned by melissaMoonNoise.

label story_melissa_moon_noise_0:
    $ main_ui_begin_native_scene_state("Ночной шум")
    show screen main_ui
    vscene "images/tavern/secondfloor/second_floor.png"
    $ scene_runtime.text = "Верхний коридор уже затих, когда над жилыми комнатами снова раздается глухой, размеренный стук. Крыша починена, летучих мышей больше нет."
    if Melissa.sex_stat("virginity", True):
        $ scene_runtime.text += " Но за дверью Мелиссы не спят: вы слышите, как она беспокойно ворочается."
    if Clara.tavern_resident() and Clara.sex_stat("virginity", True):
        $ scene_runtime.text += " За другой дверью замирают шаги Клариссы."
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
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_old_stove_4:
    $ main_ui_begin_native_scene_state("Старая печь")
    show screen main_ui
    vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    $ scene_runtime.text = "Вы возвращаетесь в каморку за перегородкой. При лунном свете старая печь кажется еще глубже и темнее. Под сводом по-прежнему только холодная зола. Рассказ Сандры указал место, но не дал ответа, что именно тревожит девушек."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Оставить печь и продолжить расследование позже":
            pass
    $ calendar_v2.advance_minutes(15)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_noise_repeat:
    $ main_ui_begin_native_scene_state("Ночной шум")
    show screen main_ui
    vscene "images/tavern/secondfloor/second_floor.png"
    $ scene_runtime.text = "Над комнатами опять раздается знакомый ночной стук. С наступлением нового лунного месяца он возвращается к тем, кто все еще его слышит. После осмотра крыши винить летучих мышей вы уже не можете."
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
    vscene "images/tavern/backyard/shed/moon_ritual/window_clue.png"
    $ scene_runtime.text = "За маленьким окном мелькают две белые ночные сорочки. Аманда и Мелисса стоят у сарая, шепчутся и по очереди оглядываются на окна трактира. «Завтра попробуем по одной, — доносится голос Аманды. — Ровно в полночь. Ты ведь помнишь слова Сандры?» Мелисса кивает и притворяет дверь сарая. Теперь вы знаете, куда они собрались."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закрыть окно и обдумать услышанное":
            pass
    $ scene_runtime.text = "В холодной печи за перегородкой можно спрятаться заранее. Для истории о мохнатой руке понадобится мягкая меховая перчатка: кусочек меха можно срезать с вашего плаща или меховой постели, если они лежат в сумке. Готовую перчатку нужно надеть через инвентарь."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Запомнить их уговор":
            pass
    $ event_runtime.active_thread.setDay()
    $ calendar_v2.advance_minutes(5)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_stove_wait_1:
    $ main_ui_begin_native_scene_state("В старой печи")
    show screen main_ui
    vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    $ scene_runtime.text = "До полуночи ещё есть время. Вы надеваете меховую перчатку, забираетесь в холодное нутро старой печи и устраиваетесь за кирпичным выступом. Отсюда видно окошко топки, а из каморки вас не разглядеть."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Притаиться и дождаться полуночи":
            pass
    $ calendar_v2.advance_minutes(60 - int(calendar_v2.minute or 0))
    if Amanda.sex_stat("virginity", True):
        vscene "images/tavern/backyard/shed/moon_ritual/amanda_stove.png"
        $ scene_runtime.text = "Первой входит Аманда в лёгкой хлопковой сорочке. Она трижды шепчет: «Олли, Олли, защити меня от того, кто приходит во сне». Потом подходит к печному окошку и, всё ещё оглядываясь, приподнимает подол. Мягкая перчатка появляется из темноты, но Аманда замечает ваши сапоги под сводом: «Стефан? Так это ты? Ну и домовой!»"
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Назваться и спросить, нужна ли ей ваша помощь":
                $ scene_runtime.text = "Вы выбираетесь из печи и говорите правду. Аманда фыркает, но не уходит: «Напугал меня, дурак. Если хочешь помочь — сначала спроси. Сегодня просто проводи меня обратно». Она сама берёт вас за руку в меховой перчатке."
            "Остаться на месте и дать ей уйти":
                $ scene_runtime.text = "Вы не шевелитесь. Аманда опускает сорочку и выходит, так и не дождавшись ответа от старой печи."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Подождать, кто придёт следом":
                pass
    if Melissa.sex_stat("virginity", True):
        vscene "images/tavern/backyard/shed/moon_ritual/melissa_stove.png"
        $ scene_runtime.text = "Позднее скрипит дверь. Мелисса в простой ночной сорочке повторяет просьбу к Олли три раза и медленно приближается к остывшей печи. На пороге топки мелькает меховая перчатка. «Кто там?» — спрашивает она и, услышав ваше дыхание, прищуривается: «Стефан, выходи. Я хочу знать, кому доверяю»."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Выйти и поговорить с Мелиссой":
                $ scene_runtime.text = "Вы вылезаете из-за кирпичей. Мелисса сердится на уловку, но выслушивает вас. «Никаких тайн за моей спиной. Если хочешь помочь нам, начни с правды». Вы обещаете не выдавать её ночной поход."
            "Остаться в темноте":
                $ scene_runtime.text = "Вы молчите. Мелисса отступает от печи и уходит, решив, что с этим домовым лучше не связываться."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Покинуть холодную печь":
                pass
    $ calendar_v2.advance_minutes(10)
    $ event_runtime.active_thread.advance()
    $ event_runtime.active_thread.setDay()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_moon_room_protection_2:
    $ main_ui_begin_native_scene_state("Ночные гостьи")
    show screen main_ui
    vscene "images/tavern/backyard/shed/moon_ritual/night_visit.png"
    $ scene_runtime.text = "К вашей комнате неслышно подходят Аманда и Мелисса. Вчерашняя печь не дала ответа о ночном стуке, зато обе теперь знают, что вы слушаете их всерьёз. «Если опять начнётся, можно мы посидим здесь, пока не успокоимся?» — спрашивает Мелисса. Аманда заглядывает через её плечо: «И без маскарада с домовыми, договорились?»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пригласить их войти и поговорить о ночном шуме":
            $ scene_runtime.text = "Вы ставите на стол свечу и даёте девушкам высказать всё, что они слышали. Аманда то шутит, то вздрагивает от скрипа крыши; Мелисса внимательно слушает ваши вопросы. Когда за окном стихает ветер, обе благодарят вас и возвращаются в спальню."
        "Проводить их обратно":
            $ scene_runtime.text = "Вы провожаете их по коридору и обещаете утром ещё раз проверить, откуда доносится стук."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пожелать им спокойной ночи":
            pass
    $ calendar_v2.advance_minutes(15)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True
