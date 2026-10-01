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


label story_melissa_moon_stove_gone_4:
    $ main_ui_begin_native_scene_state("След старой печи")
    show screen main_ui
    vscene shed_picture()
    $ scene_runtime.text = "Вы вспоминаете рассказ Сандры и осматриваете место, где прежде стояла старая развалившаяся печь. После ремонта сарая от нее не осталось ничего, кроме следа на камне. Если в истории о ночном шуме есть правда, искать ее придется не внутри этой печи."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить поиски позже":
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
