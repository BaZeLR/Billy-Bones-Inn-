# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
image side tractir_narrator = Transform("images/general/narrator.png", zoom=0.72)
image side tractir_narrator neutral = Transform("images/narrator/side/neutral.png", zoom=0.72)
image side tractir_narrator mischievous = Transform("images/narrator/side/mischievous.png", zoom=0.72)
image side tractir_narrator surprised = Transform("images/narrator/side/surprised.png", zoom=0.72)
image side tractir_narrator defiant = Transform("images/narrator/side/defiant.png", zoom=0.72)
image side tractir_narrator thoughtful = Transform("images/narrator/side/thoughtful.png", zoom=0.72)
image side tractir_narrator delighted = Transform("images/narrator/side/delighted.png", zoom=0.72)
image side tractir_narrator suspicious = Transform("images/narrator/side/suspicious.png", zoom=0.72)
image side tractir_narrator whispering = Transform("images/narrator/side/whispering.png", zoom=0.72)

image flea_narrator_table = Transform("images/narrator/flea_table.png", xysize=(config.screen_width, config.screen_height), fit="contain")

define tractir_narrator_char = Character(
    "Рассказчик",
    image="tractir_narrator",
    who_color="#C6CCD8",
    what_color="#f0e6d2",
    what_italic=True,
)

define n = tractir_narrator_char

init python:
    def tractir_narrate(text):
        renpy.say(tractir_narrator_char, str(text or ""))

label narrator_test:
    n "The narrator can now speak from ordinary labels while keeping a side portrait in the dialogue window."
    $ tractir_narrate("Python-driven events can use the same narrator through tractir_narrate().")
    n neutral "Нейтрально: начнём нашу историю."
    n mischievous "Лукаво: кажется, я знаю чуть больше, чем говорю."
    n surprised "Удивлённо: вот это поворот!"
    n defiant "Вызывающе: ну что ж, попробуй меня переубедить."
    n thoughtful "Задумчиво: здесь стоит присмотреться к деталям."
    n delighted "Радостно: а вот это уже отличные новости!"
    n suspicious "Подозрительно: что-то здесь не сходится."
    n whispering "Шёпотом: только между нами..."
    n neutral "Проверка выражений рассказчика завершена."
    return
