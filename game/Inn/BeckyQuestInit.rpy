# BeckyQuestInit.rpy
# Converted from legacy script. Handles Becky quest offer event in the market.
# All logic, conditions, and dev notes preserved.

label BeckyQuestInit():
    # Assumes BeckyVar, Friends, giveorgasms, etc. are defaulted globals
    # BeckyVar['TradeOfferText'] is set before this label is called
    narrator "Стефан, я вижу ты человек надежный, тебе можно доверять..."
    narrator "Неожиданно обратилась к вам Бекки, прервав ваше разглядование огурцов."

    "Вы подумали было что торговка решила таким образом отвести ваше внимание от особенно гнилой кучки репы но все-таки решили ответить: 'Да, я такой, ну просто супернадежный. Если кому здесь и можно доверять то мне. Вера и надежность - это я,' тут вы запутались и замолкли."
    
    narrator "'Вот и ладушки,' обрадованно сказала вдова. 'Заработать хочешь?'"
    narrator   "Как ответить?"
    $ GirlsDesc('becky')
    menu:
        
        "А кто ж не хочет?":
            narrator "Это правильно, денежки все любят," 
            narrator "согласилась с вами вдова."
            "[BeckyVar['TradeOfferText']]"
            if Friends['becky'] >= 17 and giveorgasms['becky'] >= 9:
                "Правда, есть тут небольшая загвоздка, 'чуть менее радостным тоном заметила Ребекка, а, впрочем ерунда, вряд ли это что серьезное."
                $ BeckyVar['SherwoodWarn'] = 1
                $ BeckyVar['SherwoodSuspect'] += 1
            $ BeckyVar['TradeOffer'] = 1
            menu:
                "Пойти подумать над предложением":
                    jump MarketPlace
        "Неа. Меня ни работа, ни деньги не интересуют":
            "Ну ладно, раз так. Но если передумаешь, то не стесняйся, спроси, разочарованно сказала вдовушка.Я хоть и не стесняюсь, но спрашивать пока не буду, гордо сказали вы."
            $ BeckyVar['TradeOffer'] = 2
            menu:
                "Вернуться на рыночную площадь":
                    jump MarketPlace
    return

# --- END ---
# This label can be called with `call BeckyQuestInit` to trigger the event. All logic and text are preserved and mapped to Ren'Py idioms.
