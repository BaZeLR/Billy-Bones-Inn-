# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default SocialTalkTopicSeen = {}

init -39 python:
    SOCIAL_TALK_SESSION_LIMIT = 10
    SOCIAL_TALK_SESSION_POSITIVE_CAP = 5

    SOCIAL_TALK_TOPICS = [
        {"id": "job_routine", "label": "О работе и распорядке", "min_friend": 0, "min_open": 0},
        {"id": "chat", "label": "Просто поболтать", "min_friend": 0, "min_open": 0},
        {"id": "dances", "label": "О танцах", "min_friend": 2, "min_open": 0},
        {"id": "gossip", "label": "О слухах", "min_friend": 2, "min_open": 1},
        {"id": "forest", "label": "О лесе", "min_friend": 1, "min_open": 0},
        {"id": "stories", "label": "Послушать истории", "min_friend": 3, "min_open": 2, "private": True},
        {"id": "food", "label": "О еде", "min_friend": 0, "min_open": 0},
        {"id": "fashion", "label": "Об одежде и внешности", "min_friend": 3, "min_open": 2, "private": True},
        {"id": "money", "label": "О деньгах", "min_friend": 4, "min_open": 2, "private": True},
        {"id": "family_life", "label": "О семье и доме", "min_friend": 1, "min_open": 0},
    ]

    SOCIAL_FLIRT_TOPICS = [
        {"id": "joke", "label": "Сказать игривую шутку", "min_friend": 5, "min_open": 0, "min_slut": 0},
        {"id": "kino", "label": "Мягко перейти к прикосновениям", "min_friend": 6, "min_open": 2, "min_slut": 0},
        {"id": "flirt", "label": "Открыто заигрывать", "min_friend": 7, "min_open": 3, "min_slut": 4},
        {"id": "sex_topics", "label": "Заговорить о близости", "min_friend": 9, "min_open": 5, "min_slut": 8},
    ]

    SOCIAL_NPC_TOPIC_PACKS = {
        "amanda": {
            "talk": [
                {"id": "amanda_freedom", "label": "О свободе и запретах", "min_friend": 4, "min_open": 1},
                {"id": "amanda_future", "label": "О ее будущем", "min_friend": 7, "min_open": 2, "private": True},
                {"id": "amanda_attention", "label": "О том, чего ей не хватает", "min_friend": 10, "min_open": 4, "private": True},
            ],
            "flirt": [
                {"id": "amanda_tease", "label": "Мягко подразнить Аманду", "min_friend": 6, "min_open": 1, "min_slut": 0},
                {"id": "amanda_dance_hint", "label": "Намекнуть на танцы и взгляды", "min_friend": 8, "min_open": 3, "min_slut": 4},
            ],
        },
        "melissa": {
            "talk": [
                {"id": "melissa_safety", "label": "О безопасности и доме", "min_friend": 3, "min_open": 1},
                {"id": "melissa_quiet", "label": "О тихом вечере без шума", "min_friend": 5, "min_open": 2},
                {"id": "melissa_secrets", "label": "О ее тайнах", "min_friend": 9, "min_open": 4, "private": True},
            ],
            "flirt": [
                {"id": "melissa_gentle", "label": "Сблизиться без нажима", "min_friend": 7, "min_open": 2, "min_slut": 0},
                {"id": "melissa_private_place", "label": "Намекнуть на укромное место", "min_friend": 10, "min_open": 5, "min_slut": 8},
            ],
        },
        "sandra": {
            "talk": [
                {"id": "sandra_household", "label": "О порядке в доме", "min_friend": 2, "min_open": 0},
                {"id": "sandra_tavern_plan", "label": "О будущем трактира", "min_friend": 6, "min_open": 2},
                {"id": "sandra_burden", "label": "О том, что она тянет на себе", "min_friend": 9, "min_open": 3, "private": True},
            ],
            "flirt": [
                {"id": "sandra_respect", "label": "Сделать уважительный комплимент", "min_friend": 7, "min_open": 2, "min_slut": 0},
                {"id": "sandra_warmth", "label": "Поблагодарить ее теплее обычного", "min_friend": 10, "min_open": 4, "min_slut": 0},
            ],
        },
        "clara": {
            "talk": [
                {"id": "clara_wine_trade", "label": "О винной лавке и рынке", "min_friend": 2, "min_open": 0},
                {"id": "clara_city_masks", "label": "О городских масках и слухах", "min_friend": 5, "min_open": 2},
                {"id": "clara_drawings", "label": "О рисунках и тайных увлечениях", "min_friend": 8, "min_open": 3, "private": True},
            ],
            "flirt": [
                {"id": "clara_clever_game", "label": "Затеять светскую игру", "min_friend": 5, "min_open": 2, "min_slut": 0},
                {"id": "clara_between_lines", "label": "Говорить намеками", "min_friend": 8, "min_open": 4, "min_slut": 2},
            ],
        },
    }

    SOCIAL_DEFAULT_PROFILE = {
        "talk": {"job_routine": 1, "chat": 1, "dances": 1, "gossip": 1, "forest": 1, "stories": 1, "food": 1, "fashion": 1, "money": 1, "family_life": 1},
        "flirt": {"joke": 1, "kino": 1, "flirt": 1, "sex_topics": 1},
    }

    SOCIAL_FLIRT_STAT_REQUIREMENTS = {
        "amanda": {"look": 45},
        "melissa": {"charisma": 40},
        "sandra": {"reputation": 20},
        "clara": {"charisma": 70, "exploration": 50},
    }

    SOCIAL_TALK_PROFILES = {
        "amanda": {
            "talk": {"job_routine": -1, "chat": 2, "dances": 4, "gossip": 2, "forest": 0, "stories": 1, "food": 1, "fashion": 4, "money": 1, "family_life": 2, "amanda_freedom": 3, "amanda_future": 2, "amanda_attention": 4},
            "flirt": {"joke": 3, "kino": 2, "flirt": 3, "sex_topics": 2, "amanda_tease": 3, "amanda_dance_hint": 4},
        },
        "melissa": {
            "talk": {"job_routine": 3, "chat": 1, "dances": 0, "gossip": -1, "forest": 2, "stories": 3, "food": 2, "fashion": 1, "money": 0, "family_life": 4, "melissa_safety": 4, "melissa_quiet": 3, "melissa_secrets": 3},
            "flirt": {"joke": 1, "kino": 2, "flirt": 1, "sex_topics": -2, "melissa_gentle": 4, "melissa_private_place": 3},
        },
        "sandra": {
            "talk": {"job_routine": 4, "chat": 0, "dances": -1, "gossip": 1, "forest": 1, "stories": 0, "food": 4, "fashion": 2, "money": 3, "family_life": 4, "sandra_household": 4, "sandra_tavern_plan": 4, "sandra_burden": 3},
            "flirt": {"joke": 0, "kino": -1, "flirt": -2, "sex_topics": -4, "sandra_respect": 3, "sandra_warmth": 2},
        },
        "clara": {
            "talk": {"job_routine": 1, "chat": 2, "dances": 2, "gossip": 4, "forest": 3, "stories": 3, "food": 0, "fashion": 4, "money": 2, "family_life": 1, "clara_wine_trade": 3, "clara_city_masks": 4, "clara_drawings": 4},
            "flirt": {"joke": 2, "kino": 3, "flirt": 4, "sex_topics": 3, "clara_clever_game": 4, "clara_between_lines": 4},
        },
        "becky": {
            "talk": {"job_routine": 1, "chat": 3, "dances": 3, "gossip": 2, "forest": 2, "stories": 4, "food": 2, "fashion": 2, "money": 3},
            "flirt": {"joke": 3, "kino": 2, "flirt": 3, "sex_topics": 2},
        },
        "irma": {
            "talk": {"job_routine": 3, "chat": 1, "dances": 0, "gossip": 1, "forest": 1, "stories": 1, "food": 0, "fashion": 4, "money": 3},
            "flirt": {"joke": 1, "kino": 1, "flirt": 2, "sex_topics": 0},
        },
        "inga": {
            "talk": {"job_routine": 1, "chat": 2, "dances": 1, "gossip": 2, "forest": 1, "stories": 1, "food": 1, "fashion": 2, "money": 1},
            "flirt": {"joke": 1, "kino": 1, "flirt": 1, "sex_topics": 0},
        },
        "liza": {
            "talk": {"job_routine": 0, "chat": 3, "dances": 2, "gossip": 3, "forest": 0, "stories": 2, "food": 1, "fashion": 3, "money": 2},
            "flirt": {"joke": 2, "kino": 2, "flirt": 3, "sex_topics": 2},
        },
        "georgett": {
            "talk": {"job_routine": 0, "chat": 2, "dances": 2, "gossip": 3, "forest": 0, "stories": 3, "food": 1, "fashion": 3, "money": 2},
            "flirt": {"joke": 2, "kino": 2, "flirt": 3, "sex_topics": 3},
        },
    }

    SOCIAL_EARLY_CARE_GIFT_IDS = ("soap_001", "luxury_soap_001", "energy_tea_001", "berries_001", "lavender_001", "wild_rose_001")

    SOCIAL_CUSTOM_GIFT_AFFINITY = {
        "amanda": {
            "good": ("lavender_001", "wild_rose_001", "luxury_soap_001", "libido_tincture_001"),
            "bad": ("lumber_001", "chopped_wood_001"),
        },
        "melissa": {
            "good": ("honeycomb_001", "berries_001", "energy_tea_001", "bandage_001"),
            "bad": ("libido_tincture_001",),
        },
        "sandra": {
            "good": ("soap_001", "luxury_soap_001", "energy_tea_001", "food_bale_001"),
            "bad": ("libido_tincture_001",),
        },
        "clara": {
            "good": ("lavender_001", "wild_rose_001", "luxury_soap_001", "special_mushroom_001", "libido_tincture_001"),
            "bad": ("chopped_wood_001",),
        },
    }

    SOCIAL_TOPIC_TEXT = {
        "talk": {
            "job_routine": {
                "good": "Вы обсуждаете работу в трактире спокойно и по делу. {name} отвечает охотно: ей нравится, когда вы говорите не приказами, а как хозяин, который понимает общий труд.",
                "neutral": "Вы говорите о работе и распорядке. {name} слушает, отвечает коротко и без особого тепла, но разговор остается полезным.",
                "bad": "Вы заводите разговор о работе неудачно. {name} явно слышит в этом очередную придирку и отвечает холоднее обычного.",
            },
            "chat": {
                "good": "Вы просто болтаете с {name} о пустяках, и разговор неожиданно выходит теплым. Несколько минут проходят легко.",
                "neutral": "Вы немного болтаете с {name}. Ничего важного не всплывает, но и неловкости не возникает.",
                "bad": "Вы пытаетесь поболтать с {name}, но настроение не сходится. Разговор быстро вязнет.",
            },
            "dances": {
                "good": "Разговор о танцах оживляет {name}. В голосе появляется улыбка, а вместе с ней и больше доверия.",
                "neutral": "Вы говорите о танцах. {name} поддерживает тему, но без особого блеска.",
                "bad": "Тема танцев сейчас задевает {name} не с той стороны. Она отвечает сухо и быстро переводит разговор.",
            },
            "gossip": {
                "good": "{name} охотно делится парой трактирных слухов. Вы оба понимаете, что такие разговоры иногда полезны для дела.",
                "neutral": "Вы осторожно обсуждаете слухи. {name} слушает, но лишнего не говорит.",
                "bad": "{name} не нравится, что вы тянете ее в сплетни. Разговор становится заметно прохладнее.",
            },
            "forest": {
                "good": "Вы говорите о лесе, дороге и добыче. {name} слушает внимательно и явно ценит, что это связано с выживанием трактира.",
                "neutral": "Разговор о лесе выходит спокойным, но коротким. {name} признает, что знать это полезно.",
                "bad": "Вы заводите тему леса не к месту. {name} отмахивается: сейчас у нее хватает дел в доме.",
            },
            "stories": {
                "good": "{name} задерживается рядом и слушает историю до конца. В ответ она тоже рассказывает немного больше, чем собиралась.",
                "neutral": "Вы рассказываете историю. {name} слушает вежливо, но держит привычную дистанцию.",
                "bad": "История не цепляет {name}. Она выслушивает из вежливости и явно ждет, когда можно будет вернуться к делам.",
            },
            "food": {
                "good": "Разговор о еде быстро становится разговором о том, как сделать общий стол лучше. {name} явно нравится такой практичный подход.",
                "neutral": "Вы обсуждаете еду и запасы. {name} кивает: тема полезная, пусть и будничная.",
                "bad": "{name} воспринимает разговор о еде как мелочную проверку и отвечает раздраженно.",
            },
            "fashion": {
                "good": "Вы говорите об одежде и чистом виде без грубости. {name} слышит в этом заботу, а не насмешку.",
                "neutral": "Тема одежды проходит ровно. {name} не возражает, но и особенно не раскрывается.",
                "bad": "Вы задеваете тему внешности слишком неуклюже. {name} принимает это как давление.",
            },
            "money": {
                "good": "Вы говорите о деньгах прямо: трактиру нужно выжить, а хороший доход значит больше уважения и лучшую жизнь для всех. {name} принимает этот довод всерьез.",
                "neutral": "Разговор о деньгах выходит сухим, но понятным. {name} соглашается, что без счета трактир не удержать.",
                "bad": "Денежный разговор звучит для {name} слишком холодно. Она отвечает, что люди не монеты в трактирной книге.",
            },
            "family_life": {
                "good": "Вы говорите о доме и семье без нажима. {name} слышит в этом не приказ, а попытку понять, как ей живется рядом с вами.",
                "neutral": "Разговор о доме проходит спокойно. {name} отвечает осторожно, но не уходит от темы.",
                "bad": "Тема семьи звучит неуклюже. {name} воспринимает ее как попытку напомнить о долге вместо живого внимания.",
            },
        },
        "flirt": {
            "joke": {
                "good": "Вы отпускаете легкую игривую шутку. {name} улыбается и отвечает уже заметно мягче.",
                "neutral": "Шутка выходит осторожной. {name} замечает ее, но не спешит подыгрывать.",
                "bad": "Шутка попадает мимо. {name} смотрит на вас так, что продолжать сейчас явно не стоит.",
            },
            "kino": {
                "good": "Вы осторожно сокращаете дистанцию, не давя. {name} не отстраняется, и между вами становится теплее.",
                "neutral": "Вы пробуете перейти к более близкому тону. {name} позволяет это, но держит границу.",
                "bad": "Вы торопитесь с близостью. {name} отстраняется и дает понять, что сейчас это лишнее.",
            },
            "flirt": {
                "good": "Вы заигрываете открыто, но без нажима. {name} отвечает взглядом и явно запоминает этот тон.",
                "neutral": "Вы флиртуете с {name}. Ответ сдержанный, но дверь не закрыта.",
                "bad": "Флирт звучит слишком рано или слишком резко. {name} холодеет и закрывается.",
            },
            "sex_topics": {
                "good": "Вы осторожно переводите разговор к близости. {name} краснеет, но не уходит от темы.",
                "neutral": "Вы пробуете заговорить о близости. {name} слушает настороженно и отвечает очень аккуратно.",
                "bad": "Тема близости оказывается преждевременной. {name} резко обрывает разговор.",
            },
        },
    }

    SOCIAL_CUSTOM_TOPIC_TEXT = {
        "talk": {
            "amanda_freedom": {
                "good": "Вы говорите с Амандой о свободе без приказного тона. Она сперва держится дерзко, но быстро понимает, что вы слушаете ее всерьез.",
                "neutral": "Аманда охотно спорит о запретах и свободе, но пока больше проверяет ваши границы, чем раскрывается.",
                "bad": "Разговор о свободе звучит для Аманды как новый запрет в мягкой обертке. Она замыкается.",
            },
            "amanda_future": {
                "good": "Вы спрашиваете Аманду о будущем, и она неожиданно говорит честнее обычного: ей хочется выбора, внимания и места, где ее не будут только использовать.",
                "neutral": "Аманда слушает разговор о будущем, но отвечает осторожно, словно не уверена, что такие планы вообще имеют вес.",
                "bad": "Разговор о будущем раздражает Аманду. Сейчас ей кажется, что вы просто хотите заранее решить все за нее.",
            },
            "amanda_attention": {
                "good": "Вы прямо спрашиваете, чего Аманде не хватает. Она прячет улыбку, но отвечает почти без бравады: ей важно, чтобы ее замечали не только тогда, когда она полезна.",
                "neutral": "Аманда принимает вопрос о внимании с привычной насмешкой. Тема задевает ее, но она пока не готова говорить глубже.",
                "bad": "Вопрос о том, чего ей не хватает, выходит слишком резким. Аманда решает, что ее снова пытаются поймать на слабости.",
            },
            "melissa_safety": {
                "good": "Вы обсуждаете с Мелиссой безопасность дома. Практичный тон успокаивает ее, и она заметно теплеет.",
                "neutral": "Мелисса кивает: безопасность важна, но разговор остается сухим и коротким.",
                "bad": "Мелисса слышит в разговоре о безопасности только тревогу и давление. Она становится тише.",
            },
            "melissa_quiet": {
                "good": "Вы говорите о тихом вечере без суеты. Мелисса улыбается почти незаметно: такой покой ей действительно нужен.",
                "neutral": "Мелисса поддерживает разговор о спокойном вечере, но не спешит показывать, насколько ей это важно.",
                "bad": "Тема тихого вечера звучит не вовремя. Мелисса думает о делах и не входит в настроение.",
            },
            "melissa_secrets": {
                "good": "Вы осторожно касаетесь ее тайн и не давите. Мелисса не рассказывает всего, но явно ценит, что вы оставляете ей право молчать.",
                "neutral": "Мелисса слушает вопрос о тайнах с настороженной улыбкой. Она отвечает уклончиво, но без холода.",
                "bad": "Вы заходите слишком далеко. Мелисса закрывается и дает понять, что доверие нельзя вытянуть силой.",
            },
            "sandra_household": {
                "good": "Вы обсуждаете порядок в доме как общее дело. Сандра отвечает деловито, но в голосе появляется больше уважения.",
                "neutral": "Сандра спокойно говорит о хозяйстве. Разговор полезный, хотя без особого тепла.",
                "bad": "Разговор о порядке звучит как придирка. Сандра устало смотрит на вас и отвечает коротко.",
            },
            "sandra_tavern_plan": {
                "good": "Вы говорите о будущем трактира и признаете вклад Сандры. Это попадает точно: она любит, когда планы подкреплены делом.",
                "neutral": "Сандра слушает ваши планы по трактиру и задает несколько практичных вопросов.",
                "bad": "Планы звучат пустовато. Сандра не спорит, но явно ждет не слов, а работы.",
            },
            "sandra_burden": {
                "good": "Вы замечаете, сколько Сандра тянет на себе. Она не размякает, но благодарность слышна даже в сдержанном ответе.",
                "neutral": "Сандра принимает ваши слова о ее нагрузке, хотя привычно отмахивается: дела сами себя не сделают.",
                "bad": "Попытка поговорить о ее усталости выходит неуклюжей. Сандра воспринимает это как жалость.",
            },
            "clara_wine_trade": {
                "good": "Вы обсуждаете с Клариссой винную лавку и рынок. Она оживляется: в этой теме есть и расчет, и игра, которые ей нравятся.",
                "neutral": "Кларисса отвечает о торговле охотно, но держит разговор на безопасной светской дистанции.",
                "bad": "Вы говорите о лавке слишком прямолинейно. Кларисса улыбается, но за улыбкой прячется скука.",
            },
            "clara_city_masks": {
                "good": "Разговор о городских масках и слухах явно забавляет Клариссу. Она отвечает намеками и смотрит внимательнее обычного.",
                "neutral": "Кларисса поддерживает разговор о слухах, оставляя за каждым ответом недосказанность.",
                "bad": "Кларисса решает, что вы путаете тонкую игру со сплетней. Ее ответы становятся холоднее.",
            },
            "clara_drawings": {
                "good": "Вы говорите о рисунках осторожно и без насмешки. Кларисса заметно напряжена, но в конце разговора доверия становится больше.",
                "neutral": "Кларисса не отрицает тему рисунков, но почти все оставляет между строк.",
                "bad": "Вы задеваете тайное увлечение слишком резко. Кларисса закрывает тему улыбкой, в которой нет тепла.",
            },
        },
        "flirt": {
            "amanda_tease": {
                "good": "Вы мягко поддразниваете Аманду, и она отвечает той же монетой. В этот раз дерзость работает на сближение.",
                "neutral": "Аманда подхватывает шутку, но держит флирт на легкой дистанции.",
                "bad": "Поддразнивание звучит слишком остро. Аманда улыбается, но улыбка выходит колючей.",
            },
            "amanda_dance_hint": {
                "good": "Намек на танцы и взгляды попадает в настроение Аманды. Она явно понимает подтекст и не спешит уходить от игры.",
                "neutral": "Аманда замечает намек, но пока отвечает только насмешливым взглядом.",
                "bad": "Намек на танцы звучит не к месту. Аманда быстро переводит разговор.",
            },
            "melissa_gentle": {
                "good": "Вы сближаетесь с Мелиссой без нажима. Именно эта мягкость позволяет ей не отступить.",
                "neutral": "Мелисса замечает теплый тон, но осторожность пока сильнее ответного движения.",
                "bad": "Даже мягкий флирт сейчас оказывается лишним. Мелисса закрывается.",
            },
            "melissa_private_place": {
                "good": "Намек на укромное место звучит тихо и достаточно бережно. Мелисса смущается, но не обрывает разговор.",
                "neutral": "Мелисса понимает намек и отвечает неопределенно. Решение она оставляет на потом.",
                "bad": "Намек оказывается слишком ранним. Мелисса дает понять, что сейчас это давит на нее.",
            },
            "sandra_respect": {
                "good": "Вы делаете Сандре комплимент через уважение, а не пустые сладкие слова. Такой тон она принимает гораздо охотнее.",
                "neutral": "Сандра выслушивает комплимент спокойно. Ей приятно, но она не показывает этого прямо.",
                "bad": "Комплимент звучит для Сандры как попытка отвлечь ее от дел. Она не подыгрывает.",
            },
            "sandra_warmth": {
                "good": "Вы благодарите Сандру теплее обычного. Она отвечает сдержанно, но между вами становится мягче.",
                "neutral": "Сандра принимает теплую благодарность без лишних слов.",
                "bad": "Теплый тон выходит неожиданно неловким. Сандра решает, что за ним что-то скрывается.",
            },
            "clara_clever_game": {
                "good": "Вы затеваете с Клариссой светскую игру, и она охотно входит в нее. Флирт получается умным и живым.",
                "neutral": "Кларисса принимает игру, но держит инициативу при себе.",
                "bad": "Игра кажется Клариссе слишком простой. Она улыбается вежливо и ускользает из темы.",
            },
            "clara_between_lines": {
                "good": "Вы говорите с Клариссой намеками. Она отвечает тем же, и разговор становится куда интимнее прямых слов.",
                "neutral": "Кларисса слышит подтекст, но оставляет вам только тонкую улыбку вместо ясного ответа.",
                "bad": "Намеки звучат неуклюже. Кларисса делает вид, что не поняла, и этим закрывает флирт.",
            },
        },
    }

    def social_topic_key(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if key == "clarissa":
            return "clara"
        return key

    def social_topic_return_label(girl_name=""):
        key = social_topic_key(girl_name)
        if key == "amanda":
            return "IntAmandaTalkRefresh"
        if key == "melissa":
            return "IntMelissaTalkRefresh"
        if key == "sandra":
            return "IntSandraTalkRefresh"
        if key == "clara":
            return "IntClaraTalkRefresh"
        if key == "becky":
            return "IntBeckyTalkRefresh"
        if key == "irma":
            return "IntIrmaTalkRefresh"
        if key == "inga":
            return "IntIngaTalk"
        if key == "liza":
            return "IntLizaTalkRefresh"
        if key == "georgett":
            return "IntGeorgettTalkRefresh"
        return ""

    def social_topic_seen_key(girl_name="", mode="talk", topic_id=""):
        return "%s:%s:%s:%s" % (int(dayspassed or 0), social_topic_key(girl_name), str(mode or "talk").strip().lower(), str(topic_id or "").strip())

    def social_topic_already_seen(girl_name="", mode="talk", topic_id=""):
        return social_topic_seen_key(girl_name, mode, topic_id) in dict(SocialTalkTopicSeen or {})

    def social_topic_seen_count(girl_name="", mode="talk"):
        prefix = "%s:%s:%s:" % (int(dayspassed or 0), social_topic_key(girl_name), str(mode or "talk").strip().lower())
        count = 0
        for seen_key in list(dict(SocialTalkTopicSeen or {}).keys()):
            if str(seen_key or "").startswith(prefix):
                count += 1
        return count

    def social_talk_session_remaining(girl_name=""):
        return max(0, int(SOCIAL_TALK_SESSION_LIMIT or 10) - social_topic_seen_count(girl_name, "talk"))

    def social_talk_positive_score_today(girl_name=""):
        prefix = "%s:%s:talk:" % (int(dayspassed or 0), social_topic_key(girl_name))
        total = 0
        for seen_key, seen_value in dict(SocialTalkTopicSeen or {}).items():
            if str(seen_key or "").startswith(prefix):
                total += max(0, int(seen_value or 0))
        return total

    def social_talk_positive_score_remaining(girl_name=""):
        return max(0, int(SOCIAL_TALK_SESSION_POSITIVE_CAP or 5) - social_talk_positive_score_today(girl_name))

    def social_player_stat_value(stat_name=""):
        stat_key = str(stat_name or "").strip().lower()
        try:
            if stat_key == "charisma":
                return int(charisma or 0)
            if stat_key == "look":
                return int(look or 0)
            if stat_key == "reputation":
                return int(reputation or 0)
            if stat_key == "exploration":
                return int(effective_player_exploration() or 0)
        except Exception:
            return 0
        return 0

    def social_external_requirement_met(girl_name="", action=""):
        key = social_topic_key(girl_name)
        action_key = str(action or "").strip().lower()
        if action_key != "flirt":
            return True
        requirements = dict(SOCIAL_FLIRT_STAT_REQUIREMENTS.get(key, {}) or {})
        for stat_key, needed in requirements.items():
            if social_player_stat_value(stat_key) < int(needed or 0):
                return False
        return True

    def social_topic_entries(mode="talk", girl_name=""):
        mode_key = str(mode or "").strip().lower()
        key = social_topic_key(girl_name)
        base_rows = list(SOCIAL_FLIRT_TOPICS if mode_key == "flirt" else SOCIAL_TALK_TOPICS)
        if mode_key == "talk":
            return base_rows
        custom_rows = list(dict(SOCIAL_NPC_TOPIC_PACKS.get(key, {}) or {}).get(mode_key, []) or [])
        rows = list(custom_rows)
        rows.extend(base_rows)
        return rows

    def social_topic_label(mode="talk", topic_id="", girl_name=""):
        topic_key = str(topic_id or "").strip()
        for row in social_topic_entries(mode, girl_name):
            if str(row.get("id", "") or "") == topic_key:
                return str(row.get("label", "") or topic_key)
        return topic_key

    def social_topic_profile(girl_name="", mode="talk"):
        key = social_topic_key(girl_name)
        mode_key = str(mode or "talk").strip().lower()
        profile = dict(dict(SOCIAL_DEFAULT_PROFILE.get(mode_key, {}) or {}))
        profile.update(dict(dict(SOCIAL_TALK_PROFILES.get(key, {}) or {}).get(mode_key, {}) or {}))
        return profile

    def social_topic_visible(girl_name="", mode="talk", topic_id=""):
        key = social_topic_key(girl_name)
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        if key == "":
            return False
        if key == "clara" and mode_key == "flirt":
            try:
                if not clara_can_start_social_events():
                    return False
            except Exception:
                return False
        if mode_key == "talk" and social_talk_session_remaining(key) <= 0:
            return False
        if mode_key == "talk" and social_topic_already_seen(key, mode_key, topic_key):
            return False
        if mode_key == "flirt" and int(FlirtedToday.get(key, 0) or 0) > 0:
            return False
        if mode_key == "flirt" and not social_external_requirement_met(key, "flirt"):
            return False
        allowed, reason = relationship_social_action_allowed(key, mode_key)
        if not allowed:
            return False
        for row in social_topic_entries(mode_key, key):
            if str(row.get("id", "") or "") != topic_key:
                continue
            if int(Friends.get(key, 0) or 0) < int(row.get("min_friend", 0) or 0):
                return False
            if int(otkroven.get(key, 0) or 0) < int(row.get("min_open", 0) or 0):
                return False
            if mode_key == "talk" and bool(row.get("private", False)):
                private_allowed, private_reason = relationship_social_action_allowed(key, "private_talk")
                if not private_allowed:
                    return False
            if mode_key == "flirt" and int(sluttiness.get(key, 0) or 0) < int(row.get("min_slut", 0) or 0):
                return False
            return True
        return False

    def social_visible_topic_entries(girl_name="", mode="talk"):
        rows = []
        for row in social_topic_entries(mode, girl_name):
            if social_topic_visible(girl_name, mode, row.get("id", "")):
                rows.append(dict(row))
        return rows

    def social_has_visible_topics(girl_name="", mode="talk"):
        return len(social_visible_topic_entries(girl_name, mode)) > 0

    def social_topic_score(girl_name="", mode="talk", topic_id=""):
        key = social_topic_key(girl_name)
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        base = int(social_topic_profile(key, mode_key).get(topic_key, 0) or 0)
        mood = 0
        if int(Friends.get(key, 0) or 0) >= 10:
            mood += 1
        if int(otkroven.get(key, 0) or 0) >= 8:
            mood += 1
        if mode_key == "flirt" and int(sluttiness.get(key, 0) or 0) >= 15:
            mood += 1
        if int(Drunk.get(key, 0) or 0) > 0:
            mood += 1
        adjusted = relationship_adjust_social_score(key, mode_key, max(-5, min(5, base + mood)))
        try:
            adjusted = player_social_adjusted_delta(key, mode_key, adjusted)
        except Exception:
            pass
        return adjusted

    def social_topic_notify_result(girl_name="", mode="talk", topic_id="", topic_score=0, final_score=0, relation_delta=0):
        topic_name = social_topic_label(mode, topic_id, girl_name)
        base_value = int(topic_score or 0)
        final_value = int(final_score or 0)
        relation_value = int(relation_delta or 0)
        base_text = "+%d" % base_value if base_value > 0 else str(base_value)
        final_text = "+%d" % final_value if final_value > 0 else str(final_value)
        relation_text = "+%d" % relation_value if relation_value > 0 else str(relation_value)
        if base_value == final_value:
            message = "Тема: %s (%s). Отношения: %s." % (topic_name, base_text, relation_text)
        else:
            message = "Тема: %s (%s -> %s). Отношения: %s." % (topic_name, base_text, final_text, relation_text)
        try:
            renpy.notify(message)
        except Exception:
            pass
        return message

    def social_topic_result_kind(score=0):
        value = int(score or 0)
        if value >= 2:
            return "good"
        if value <= -2:
            return "bad"
        return "neutral"

    def social_topic_text(girl_name="", mode="talk", topic_id="", score=0):
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        kind = social_topic_result_kind(score)
        text = str(dict(dict(SOCIAL_CUSTOM_TOPIC_TEXT.get(mode_key, {}) or {}).get(topic_key, {}) or {}).get(kind, "") or "")
        if not text:
            text = str(dict(dict(SOCIAL_TOPIC_TEXT.get(mode_key, {}) or {}).get(topic_key, {}) or {}).get(kind, "") or "")
        if not text:
            text = "Вы некоторое время говорите с {name}."
        return text.format(name=_action_display_name(girl_name))

    def social_apply_topic(girl_name="", mode="talk", topic_id=""):
        key = social_topic_key(girl_name)
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        if not social_topic_visible(key, mode_key, topic_key):
            allowed, reason = relationship_social_action_allowed(key, mode_key)
            return {"ok": False, "text": str(reason or "Сейчас этот разговор не складывается."), "score": 0}
        friends_before = int(Friends.get(key, 0) or 0)
        topic_score = int(social_topic_profile(key, mode_key).get(topic_key, 0) or 0)
        score = social_topic_score(key, mode_key, topic_key)
        if mode_key == "talk" and score > 0:
            score = min(score, social_talk_positive_score_remaining(key))
        if mode_key == "flirt":
            apply_social_interaction_base(key, "flirt", score, 2 if score > 0 else 0, 30, 1, 1, 0, 0, True)
            if score > 0:
                add_to_stat_dict(sluttiness, key, max(1, score), 0, 100)
            elif score < 0:
                add_to_stat_dict(otkroven, key, score, 0, 20)
        else:
            apply_social_interaction_base(key, "talk", score, 1 if score > 0 else 0, 30, 1, 0, 0, 1, True)
            if score > 0:
                add_to_stat_dict(otkroven, key, max(1, score // 2), 0, 20)
        actual_score = social_score_delta_for(key, friends_before)
        SocialTalkTopicSeen[social_topic_seen_key(key, mode_key, topic_key)] = score
        try:
            info = getPersonInfo(key)
            if info is not None and mode_key == "talk":
                info.talkToday.add(topic_key)
        except Exception:
            pass
        relationship_after_social_result(key, mode_key, score, True)
        result_text = append_social_score_message(social_topic_text(key, mode_key, topic_key, score), actual_score, True)
        social_topic_notify_result(key, mode_key, topic_key, topic_score, score, actual_score)
        try:
            player_social_condition_notify(key)
        except Exception:
            pass
        return {"ok": True, "text": result_text, "score": actual_score, "raw_score": score}

    def social_gift_score(girl_name="", item_id="", base_gain=2):
        key = social_topic_key(girl_name)
        item_key = str(item_id or "").strip()
        allowed, reason = relationship_social_action_allowed(key, "gift", item_key)
        if not allowed:
            return -3
        base = max(0, min(5, int(base_gain or 0)))
        try:
            preferred = item_key in tuple(preferred_gift_item_ids(key) or ())
        except Exception:
            preferred = False
        if preferred:
            score = max(2, base + 1)
        elif item_key in SOCIAL_EARLY_CARE_GIFT_IDS:
            score = max(1, min(4, base))
        else:
            score = 0
            if key in SOCIAL_TALK_PROFILES and int(Friends.get(key, 0) or 0) < 5:
                score = -2
        affinity = social_custom_gift_affinity(key, item_key)
        if affinity > 0:
            score = max(score, base + affinity)
        elif affinity < 0:
            score += affinity
        if int(Friends.get(key, 0) or 0) >= 10:
            score += 1
        if int(GiftedToday.get(key, 0) or 0) > 0:
            score -= 3
        return relationship_adjust_social_score(key, "gift", max(-5, min(5, score)))

    def social_gift_acceptance(girl_name="", item_id="", base_gain=2):
        key = social_topic_key(girl_name)
        item_key = str(item_id or "").strip()
        allowed, reason = relationship_social_action_allowed(key, "gift", item_key)
        if not allowed:
            return False, -3
        score = social_gift_score(key, item_key, base_gain)
        if item_key in SOCIAL_EARLY_CARE_GIFT_IDS:
            return True, score
        if key in SOCIAL_TALK_PROFILES and int(Friends.get(key, 0) or 0) < 3 and score <= 0:
            return False, score
        return True, score

    def social_gift_text(girl_name="", gift_name="", item_id="", score=0):
        key = social_topic_key(girl_name)
        gift = str(gift_name or "подарок").strip()
        item_key = str(item_id or "").strip()
        value = int(score or 0)
        name = _action_display_name(key)
        affinity = social_custom_gift_affinity(key, item_key)
        if affinity > 0 and value > 0:
            return "%s принимает %s с личным интересом. Видно, что этот подарок подходит именно ей, и разговор сразу становится теплее." % (name, gift)
        if affinity < 0 and value < 0:
            return "%s смотрит на %s без радости. Для нее это выглядит не как внимание, а как неверно выбранный жест." % (name, gift)
        if value >= 3:
            return "%s принимает %s с явным удовольствием. Похоже, вы угадали не только с вещью, но и с моментом." % (name, gift)
        if value > 0:
            return "%s принимает %s спокойно, но теплеет к вам: подарок оказался уместным." % (name, gift)
        if value == 0:
            return "%s принимает %s вежливо. Это не задевает ее, но и особенного впечатления не производит." % (name, gift)
        return "%s не хочет брать %s. Сейчас такой подарок кажется ей не заботой, а давлением." % (name, gift)

    def social_custom_gift_affinity(girl_name="", item_id=""):
        key = social_topic_key(girl_name)
        item_key = str(item_id or "").strip()
        row = dict(SOCIAL_CUSTOM_GIFT_AFFINITY.get(key, {}) or {})
        if item_key != "" and item_key in tuple(row.get("good", ()) or ()):
            return 2
        if item_key != "" and item_key in tuple(row.get("bad", ()) or ()):
            return -2
        return 0

    def social_interaction_allowed_for_npc(girl_name="", action="", item_id=""):
        key = social_topic_key(girl_name)
        action_key = str(action or "").strip().lower()
        item_key = str(item_id or "").strip()
        if key == "":
            return False
        if key == "melissa" and action_key in ("flirt", "gift", "share"):
            if action_key in ("gift", "share") and int(FlirtedToday.get(key, 0) or 0) <= 0:
                return False
            try:
                return bool(melissa_relationship_allows(key, action_key))
            except Exception:
                return False
        if key == "clara":
            if action_key == "flirt":
                try:
                    return bool(clara_can_start_social_events()) and social_external_requirement_met(key, "flirt")
                except Exception:
                    return False
            if action_key == "gift":
                if int(FlirtedToday.get(key, 0) or 0) <= 0:
                    return False
                try:
                    return bool((clara_can_receive_gifts() or clara_has_caught_cat_gift()) and clara_has_giftable_entries())
                except Exception:
                    return False
            if action_key == "share":
                if int(FlirtedToday.get(key, 0) or 0) <= 0:
                    return False
                allowed, reason = relationship_social_action_allowed(key, action_key, item_key)
                return bool(allowed)
        if action_key == "flirt" and not social_external_requirement_met(key, "flirt"):
            return False
        if action_key == "gift":
            if int(FlirtedToday.get(key, 0) or 0) <= 0:
                return False
            return bool(relationship_any_gift_allowed(key))
        if action_key == "share" and int(FlirtedToday.get(key, 0) or 0) <= 0:
            return False
        allowed, reason = relationship_social_action_allowed(key, action_key, item_key)
        return bool(allowed)

    def social_core_action_items(girl_name="", return_label=""):
        key = social_topic_key(girl_name)
        ret = str(return_label or social_topic_return_label(key) or "").strip()
        items = []
        if social_has_visible_topics(key, "talk"):
            items.append(MenuItem("Поговорить о...", Function(main_ui_call_label, "SocialTalkTopicMenu", key, "talk", ret)))
        if social_has_visible_topics(key, "flirt") and social_interaction_allowed_for_npc(key, "flirt"):
            items.append(MenuItem("Флиртовать...", Function(main_ui_call_label, "SocialTalkTopicMenu", key, "flirt", ret)))
        if int(GiftedToday.get(key, 0) or 0) == 0 and social_interaction_allowed_for_npc(key, "gift"):
            if key == "clara":
                items.append(MenuItem("Сделать Клариссе подарок", Function(main_ui_call_label, "IntClaraGiftMenu", key)))
            else:
                items.append(MenuItem("Подарить что-нибудь", Function(main_ui_call_label, "PlayerCardGiftToFixedTargetMenu", key)))
            if player_card_has_shareable_items() and social_interaction_allowed_for_npc(key, "share"):
                items.append(MenuItem("Поделиться угощением", Function(main_ui_call_label, "PlayerCardShareToFixedTargetMenu", key)))
        return items


label SocialTalkTopicMenu(girl_name="", mode="talk", return_label=""):
    $ _social_girl = social_topic_key(girl_name)
    $ _social_mode = str(mode or "talk").strip().lower()
    $ _social_return = str(return_label or social_topic_return_label(_social_girl) or "").strip()
    $ main_ui_begin_talk_state("Разговор с %s" % _action_display_name(_social_girl), _social_girl)
    $ current_action_title = "О чем говорить" if _social_mode == "talk" else "Как флиртовать"
    $ current_action_content = None
    $ current_action_items = []
    python:
        _remaining_topics = social_talk_session_remaining(_social_girl) if _social_mode == "talk" else 999
        for _topic in social_visible_topic_entries(_social_girl, _social_mode):
            if _remaining_topics <= 0:
                break
            current_action_items.append(MenuItem(str(_topic.get("label", "") or ""), Function(main_ui_call_label, "SocialTalkTopicApply", _social_girl, _social_mode, str(_topic.get("id", "") or ""), _social_return)))
            _remaining_topics -= 1
        if len(current_action_items) <= 0:
            if _social_mode == "talk" and social_talk_session_remaining(_social_girl) <= 0:
                MainTxt = "На сегодня вы уже достаточно поговорили."
            else:
                MainTxt = "Сейчас подходящих тем нет."
            CurLocDesc = MainTxt
    if _social_return != "":
        $ current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, _social_return, _social_girl)))
    else:
        $ current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
    return


label SocialTalkTopicApply(girl_name="", mode="talk", topic_id="", return_label=""):
    $ _social_girl = social_topic_key(girl_name)
    $ _social_return = str(return_label or social_topic_return_label(_social_girl) or "").strip()
    $ _social_result = social_apply_topic(_social_girl, mode, topic_id)
    $ MainTxt = str(_social_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    if str(mode or "talk").strip().lower() == "talk" and social_talk_session_remaining(_social_girl) > 0 and social_has_visible_topics(_social_girl, "talk"):
        call SocialTalkTopicMenu(_social_girl, "talk", _social_return)
        return
    if _social_return != "":
        call expression _social_return pass (_social_girl)
    return
