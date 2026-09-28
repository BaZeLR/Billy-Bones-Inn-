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
    $ scene_runtime.text = "Услышав, что на чердаке опять пусто, Сандра откладывает ложку. «В моей деревне в такие ночи тоже стучало. Старухи говорили: оборотень-козёл зовёт девственниц по ночам и насылает сны, после которых они просыпаются возбуждёнными. Не смешно, Аманда. Я сама это слышала». Аманда хочет возразить, но, заметив лицо Мелиссы, прикусывает язык."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Попросить Сандру продолжить":
            pass
    $ scene_runtime.text = "«Мать отвела меня к брату Илматтера. Он обещал избавить меня от этих ночей, а вместо этого изнасиловал. Так что не верьте священнику, который требует вашего тела за защиту», — говорит Сандра. Помолчав, она вспоминает другое деревенское поверье: в старой печи может жить домашний дух; в полнолуние к нему обращались, чтобы отогнать оборотня-козла."
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
