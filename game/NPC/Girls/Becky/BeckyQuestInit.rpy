# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# BeckyQuestInit.rpy
# Converted from legacy script. Handles Becky quest offer event in the market.
# All logic, conditions, and dev notes preserved.

define BECKY_TRADE_OFFER_TEXT = "\"Значит так, может ты слышал, часах в 6 езды от города есть эльфийский замок. Куниделл называется. Так вот, с едой там дела не очень обстоят. Эльфы, сам понимаешь, что с них взять. Каждую грядку им надо, видишь ли, расположить в согласии с музыкой сфер, на это у них время есть. А скажем полить или прополоть - так на это у них ни желания, ни времени нет.\"\n\n\"И как урожаи у них?\" решили уточнить вы.\n\n\"А никак. Поэтому и цены у них повыше. В общем смотри. Тебе нужна лошадь. Я тебе продам 4 больших мешка всяких овощей - по полквинтала каждый, 50 мараведи штука. Навьючишь их, утром в путь, там продашь с наваром не меньше, чем полсотни мараведи. А может и три сотни выручишь. А на следующий день опять так можешь. Эльфы они такие, хоть и возвышенные, но прожорливые. В общем, утром в любой день заходи, ну кроме воскресенья, конечно.\""

label BeckyQuestInit():
    $ main_ui_begin_native_scene_state("Предложение Бекки")
    show screen main_ui
    vscene grocery_store_grocer_picture("becky")
    $ scene_runtime.text = "\"Стефан, я вижу ты человек надежный, тебе можно доверять,\" неожиданно обратилась к вам Бекки, прервав ваше глубокомысленное разглядование выложенных на продажу огурцов и прочей репы.\n\nВы подумали было что торговка решила таким образом отвести ваше внимание от особенно гнилой кучки репы но все-таки решили ответить: \"Да, я такой, ну просто супернадежный. Если кому здесь и можно доверять то мне. Вера и надежность - это я,\" тут вы запутались и замолкли.\n\n\"Вот и ладушки,\" обрадованно сказала вдова. \"Заработать хочешь?\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "А кто ж не хочет?":
            $ scene_runtime.text = "\"Это правильно, денежки все любят,\" согласилась с вами вдова.\n\n" + BECKY_TRADE_OFFER_TEXT
            $ scene_runtime.location_text = scene_runtime.text
            if Becky.rel >= 17 and Becky.stats.get('orgasms_given', 0) >= 9:
                $ scene_runtime.text += "\n\n\"Правда, есть тут небольшая загвоздка,\" чуть менее радостным тоном заметила Ребекка, \"а, впрочем ерунда, вряд ли это что серьезное.\""
                $ scene_runtime.location_text = scene_runtime.text
                $ Becky.sherwood_warning_stage = 1
                $ Becky.sherwood_suspicion += 1
            $ event_runtime.active_thread.advanceTo(2, force_active=True)
            menu:
                "Пойти подумать над предложением":
                    $ main_ui_end_native_scene_state()
                    jump MarketPlace
        "Неа. Меня ни работа, ни деньги не интересуют":
            $ scene_runtime.text = "\"Ну ладно, раз так. Но если передумаешь, то не стесняйся, спроси,\" разочарованно сказала вдовушка.\n\n\"Я хоть и не стесняюсь, но спрашивать пока не буду,\" гордо сказали вы."
            $ scene_runtime.location_text = scene_runtime.text
            $ event_runtime.active_thread.advance()
            menu:
                "Вернуться на рыночную площадь":
                    $ main_ui_end_native_scene_state()
                    jump MarketPlace
    return
