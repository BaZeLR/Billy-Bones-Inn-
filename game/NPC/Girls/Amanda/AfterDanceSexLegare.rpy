# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label AmandaLegareReactOnYouSee:
    $ renpy.dynamic("AmandaLegareReactionRoll")
    if not Amanda.knows_player_is_watching_legare_sex:
        return

    $ AmandaLegareReactionRoll = procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:27:1")
    if AmandaLegareReactionRoll == 1:
        "Вспомнив о вас, Аманда обернулась и подмигнула в сторону бочек."
    elif AmandaLegareReactionRoll == 2:
        "Аманда обернулась к укрытию и демонстративно провела рукой между ног."
    elif AmandaLegareReactionRoll == 3:
        "Аманда явно помнит, что вы наблюдаете, и посылает вам воздушный поцелуй."
    return


label AmandaLegareMinetFinish:
    if procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:36:2") == 1:
        "Легаре не предупредил Аманду и кончил ей прямо в рот."
        if Amanda.corruption >= 40 or Amanda.sex_stat("sexacts", 0) > 12:
            "Аманда проглотила почти все, лишь несколько струек осталось на лице."
        else:
            "Она растерялась, но быстро начала сглатывать семя."
    else:
        "Легаре вытащил член и обрызгал спермой лицо Аманды."

    $ Amanda.performed_oral_with_legare = True
    $ Amanda.legare_affection += 1
    $ Amanda.change_social(corruption_delta=1)
    $ Amanda.pregnancy_check("mouthface", 1, "legare")
    return


label AmandaLegareSexFinish(tmpLegareSexType):
    if procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:51:3") <= 2:
        "Легаре засадил Аманде глубже и замер, кончая прямо в нее."
        if Amanda.sex_stat("cuminside", 0) < 2:
            "Аманда наивно разглядывает капли на пальцах и спрашивает про детей."
        if Amanda.sex_stat("pregnancy", 0) > 120:
            "Аманда шутит, что беременнее уже не станет."
        elif Amanda.corruption >= 48:
            "Ей откровенно нравится ощущение тепла внутри."
        elif tmpLegareSexType == 2:
            "Аманда переживает из-за первого раза, а Легаре ее успокаивает."
        else:
            "Аманда укоряет Легаре за риск, а он обещает в следующий раз быть осторожнее."

        if tmpLegareSexType in (2, 3):
            call ShowImage("amanda", "albersex", "cuminside" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:65:4")))
        elif tmpLegareSexType == 4:
            call ShowImage("amanda", "albersex", "spermpussymouth")
        else:
            call ShowImage("amanda", "albersex", "spermpussy")

        $ Amanda.pregnancy_check("inside", 1, "legare")
        $ Amanda.legare_affection += 1
        $ Amanda.change_social(corruption_delta=2)
    else:
        "Легаре вытащил и кончил Аманде на ягодицы."
        if Amanda.sex_stat("cuminside", 0) < 2:
            "Аманда снова интересуется, от этого ли появляются дети."
        if Amanda.sex_stat("pregnancy", 0) > 120:
            "С беременным животом она относится к этому спокойно."
        elif Amanda.corruption >= 48:
            "Аманда признается, что ей было бы приятнее получить все внутрь."
        else:
            "Она радуется, что Легаре не кончил внутрь."

        $ Amanda.pregnancy_check("outside", 1, "legare")
        $ Amanda.legare_affection += 2
        $ Amanda.change_social(corruption_delta=2)

    $ Amanda.had_sex_with_legare = True
    return


label AfterDanceSexLegare(CurSexStep=0, tmpLegareSexType=-1, FollowMode=""):
    $ renpy.dynamic("MaxStep", "AmandaNesluh")
    $ main_ui_begin_native_scene_state("Аманда и Легаре")
    if CurSexStep == 0 and tmpLegareSexType < 0:
        $ tmpLegareSexType = Amanda.legare_sex_type()
        if tmpLegareSexType == 4 and Amanda.sex_stat("pregnancy", 0) <= 120 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:96:5") <= 3:
            $ tmpLegareSexType = 5

    if CurSexStep == 0:
        if FollowMode == "alone":
            "Вы проследили за Амандой и выяснили, что конечной целью ее пути был задний двор магазинчика месье Легаре. У которого ее и встретил оный месье. Прежде чем вы что-то успели сделать, он уже открыл калитку Аманде и завел ее в промежуток между бочками с вином и какой-то повозкой."
        else:
            "Вскоре месье Легаре привел Аманду на задний двор своего магазинчика и завел ее в промежуток между бочками с вином и какой-то повозкой."
        "Вы незаметно последовали за ними, заняв стратегическую позицию с противоположной стороны штабеля бочек. А расторопливый торговец времени не терял: он прижал Аманду к стене, крепко ее поцеловав."
        if Amanda.corruption >= 30:
            "Та с радостью откликнулась на его поцелуй, запустив свой язычок в его рот."
        else:
            "После секундного колебания Аманда все же откликнулась на его поцелуй."
        call ShowImage("amanda", "albersex", "kiss")

    elif CurSexStep == 1:
        "Вы прислушались к их разговору. Легаре успокаивает Аманду, уверяя, что жена ничего не узнает, а здесь им никто не помешает. Аманда то смущается, то хихикает, но уходить явно не собирается."
        $ Alber.heard_about_wife = True

    elif CurSexStep == 2:
        if tmpLegareSexType == 0:
            if Amanda.sex_stat("pregnancy", 0) < 120:
                "Послышалось шуршание юбки и затем голос Аманды: \"Ой, вот он какой. И как быстро растет!\" Легаре показывает ей член и подталкивает к более смелым ласкам."
                call ShowImage("amanda", "alberseduce", "showcock")
            else:
                "Аманда заявляет, что с животом согласна только на минет, и почти сразу берется за дело."
        elif tmpLegareSexType == 1:
            "Послышалось шуршание юбки и затем голос Аманды: \"Ой, Альберчик, я еще не готова так. Давай я тебе как в прошлый раз?\" Заглянув в щель между бочками, вы увидели, что Аманда торопливо расстегивает Альберу штаны, выпуская на свободу его маленького друга."
            call ShowImage("amanda", "alberseduce", "suck")
            $ Amanda.performed_oral_with_legare = True
        elif tmpLegareSexType == 2:
            "Послышалось шуршание юбки и затем голос Аманды: \"Ой, Альберчик, это будет мой первый раз, я ведь еще девочка! Может пока еще не надо?\" Такой ответ отнюдь не обескуражил месье. Он обнял Аманду, положив одну руку на ее талию, а другую на грудь, заглушая слабые протесты ласками и поцелуями."
            call ShowImage("amanda", "albersex", "grope" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:128:6")))
        elif tmpLegareSexType == 3:
            "Послышалось шуршание юбки и затем голос Аманды: \"Ой, Альберчик, ты хочешь меня? Ну давай, только здесь везде всякие бочки, повозки, щепки, я занозу в попу случаем не получу?\" Месье галантно очистил одну из бочек от пыли и щепок, даже вытерев ее своим шелковым платком, а затем принялся за ласки."
            call ShowImage("amanda", "albersex", "grope" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:131:7")))
        elif tmpLegareSexType == 4:
            "Послышалось шуршание юбки и затем голос Аманды: \"Милый, давай я тебя сначала ротиком подниму, а потом ты меня? Только давай я сперва платье сниму, чтобы его не помять и не испачкать.\" Месье с радостью помог Аманде в ее просьбе."
            call ShowImage("amanda", "albersex", "gropenaked")
        else:
            "От поцелуйчиков парочка быстро перешла к менее невинным развлечениям. Зрелый и опытный развратник запустил свои загребущие лапы прямо в декольте Аманды, лапая ее за груди. Впрочем, Аманде такое обращение пришлось по нраву."
            call ShowImage("amanda", "albersex", "grope" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:137:8")))
        $ Amanda.player_knows_legare_sex = True
        $ Amanda.player_saw_legare_sex = True

    elif CurSexStep == 3:
        if tmpLegareSexType == 0:
            "Аманда встает перед Легаре на колени и старательно начинает делать ему минет."
            call ShowImage("amanda", "alberseduce", "suck")
            $ Amanda.performed_oral_with_legare = True
        elif tmpLegareSexType == 1:
            "В конце концов усилия Аманды, старательно обхаживающей член месье Легаре, принесли свои плоды."
            call AmandaLegareMinetFinish
        elif tmpLegareSexType == 2:
            "От ласк месье пошел дальше: он сноровисто стащил с Аманды платье, а затем принялся ласкать ее языком. Убедившись в том, что девочка созрела, он развернул ее, положив ее руки на бочку, и пристроился к ней сзади со своим стоящим колом членом. Писк Аманды, струйка крови, и вот негодяй уже внутри."
            $ Amanda.had_sex_with_legare = True
            $ Amanda.set_sex_stat("virginity", False)
            $ Amanda.lost_virginity_to_legare = True
            $ Amanda.player_knows_legare_deflowered = True
            $ Amanda.set_var_int("knownotvirgin", 1)
            call ShowImage("amanda", "albersex", "fuckbarrelstart")
        elif tmpLegareSexType == 3:
            "От ласк месье пошел дальше: он сноровисто стащил с Аманды платье, а сама Аманда успела аккуратно убрать белье. Потом он усадил ее на бочку, разогрел языком, развернул и пристроился к ней сзади со своим стоящим колом членом. И вот негодяй уже внутри, не встретив никаких преград."
            $ Amanda.had_sex_with_legare = True
            $ Amanda.set_var_int("knownotvirgin", 1)
            call ShowImage("amanda", "albersex", "fuckbarrelstart")
        elif tmpLegareSexType == 4:
            "Аманда быстро доводит Легаре ртом до оргазма."
            $ Amanda.performed_oral_with_legare = True
            call AmandaLegareMinetFinish
        else:
            "Вскоре платье и белье покинули Аманду. Месье поднял ее, без труда насадил на свой член и стал сношать у стены. Впрочем годы берут свое, выносливость у Альбера подкачала."
            if Amanda.current_underwear("bra", "") != "":
                "Лифчик тоже долго не задержался."
            $ Amanda.set_var_int("knownotvirgin", 1)
            $ Amanda.had_sex_with_legare = True
            call ShowImage("amanda", "albersex", "fuckwall")
        call AmandaLegareReactOnYouSee

    elif CurSexStep == 4:
        if tmpLegareSexType == 0:
            "Хоть опыта у Аманды было не так уж и много, возбужденный торговец быстро дошел до конца. Должно быть, его возбуждала сама мысль о новой победе."
            call AmandaLegareMinetFinish
        elif tmpLegareSexType == 1:
            "\"Как тебе, милый?\" спросила Альбера Аманда, вытирая подбородок от остатков спермы. \"Ты была бесподобна, как всегда, мой мышонок!\" куртуазно заверил ее месье, не забывая между тем приводить себя в порядок. \"Давай я тебя провожу, а то уже поздно.\" И они направились на улицу, в сторону трактира."
        elif tmpLegareSexType == 2:
            "Дав своей подруге привыкнуть к новым для нее ощущениям, Альбер начал потрахивать Аманду, сначала медленно, а потом все быстрее и быстрее. Судя по тому, что Аманда начала постанывать, а потом и подмахивать своему любовнику, ей пришлось по вкусу такое обращение. Вдруг девушка на секунду замерла, а потом по ней прошла дрожь: наверное, она только что кончила на члене месье Легаре."
            call ShowImage("amanda", "albersex", "fuckbarrel" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:183:9")))
        elif tmpLegareSexType == 3:
            "Легаре допрашивает Аманду о том, кто лишил ее девственности. Ее ответы только больше заводят месье, а сама Аманда насмешливо тянет слова и подмахивает его толчкам."
            call ShowImage("amanda", "albersex", "fuckbarrel" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:186:10")))
        elif tmpLegareSexType == 4:
            "Забавы парочки были еще далеки от завершения. Аманда продолжила сосать обмякший было член своего кавалера, вернув ему прежнюю бодрость и свежесть. Убедившись в этом, она развернулась и наклонилась, призывно подставив свое сокровище похотливому торгашу. Тот не замедлил воспользоваться приглашением, и, войдя в нее одним быстрым движением, начал сношать уже текущую девушку."
            if Amanda.sex_stat("pregnancy", 0) >= 120:
                "Беременный живот Аманда гладит рукой, пока Легаре продолжает."
            "Аманда быстро доходит до оргазма на его члене."
            $ Amanda.set_var_int("knownotvirgin", 1)
            $ Amanda.had_sex_with_legare = True
            call ShowImage("amanda", "albersex", "fuck" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:194:11")))
        else:
            "Аманду это не смутило. Соскользнув на секунду с члена своего любовника, она тут же развернулась и наклонилась, призывно подставив себя похотливому торгашу. Тот не замедлил воспользоваться приглашением и начал сношать уже потекшую девушку."
            call ShowImage("amanda", "albersex", "fuck" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:197:12")))
        call AmandaLegareReactOnYouSee

    elif CurSexStep == 5:
        if tmpLegareSexType == 0:
            "\"Как тебе, я была не слишком неуклюжа?\" трогательно спросила Альбера Аманда, вытирая подбородок от остатков спермы. \"Тебе понравилось, хоть капельку?\" \"Ты была бесподобна,\" заверил ее месье, приводя себя в порядок. \"Давай я тебя провожу, а то уже поздно.\" И они направились на улицу, в сторону трактира."
        elif tmpLegareSexType >= 2:
            call AmandaLegareSexFinish(tmpLegareSexType)
            call AmandaLegareReactOnYouSee
            if tmpLegareSexType == 2:
                $ Amanda.legare_affection += 2
                $ Amanda.change_social(corruption_delta=2)

    elif CurSexStep == 6:
        if tmpLegareSexType == 2:
            "\"Ох, это был мой первый раз, и он такой прекрасный!\" поделилась Аманда своими переживаниями с Альбером. \"Надеюсь и тебе понравилось?\" \"О да, ты была просто божественна,\" обходительно заверил ее Альбер, приводя себя в порядок. \"Давай я тебя провожу, а то уже поздно.\""
        elif tmpLegareSexType == 3:
            "\"Ты кончила, моя волшебница?\" спросил, чуть отдышавшись, Аманду ее старший любовник. \"Так же как и ты, милый! Мне понравилось, а тебе?\" \"О да, ты была просто божественна,\" обходительно заверил ее Альбер, приводя себя в порядок одновременно с пудрением ей мозгов. \"Давай я тебя провожу, а то уже поздно.\""
        else:
            "\"Как бурно ты кончила, цыпочка!\" поразился страстности Аманды месье. \"А как же, ты меня всегда доводишь, ты такой умелый и опытный!\" комплиментом на комплимент ответила она. \"Для тебя я всегда готов стараться,\" обходительно заверил ее Альбер, приводя себя в порядок одновременно с пудрением ей мозгов. \"Давай я тебя провожу, а то уже поздно.\""

    $ MaxStep = 6
    if tmpLegareSexType == 0:
        $ MaxStep = 5
    elif tmpLegareSexType == 1:
        $ MaxStep = 4

    menu:
        "Послушать о чем они болтают" if CurSexStep == 0 and not Alber.heard_about_wife:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Смотреть чего будет дальше" if CurSexStep == 0 and Alber.heard_about_wife:
            call AfterDanceSexLegare(CurSexStep + 2, tmpLegareSexType, FollowMode)
            return

        "Смотреть чего будет дальше" if CurSexStep == 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Дать им кончить" if CurSexStep == 2 and tmpLegareSexType == 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Подсматривать дальше" if CurSexStep == 2 and tmpLegareSexType != 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Дать им кончить" if CurSexStep == 3 and tmpLegareSexType == 0:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "И что дальше?" if CurSexStep == 3 and tmpLegareSexType == 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Еще посмотреть" if CurSexStep == 3 and tmpLegareSexType >= 2:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "И что дальше?" if CurSexStep == 4 and tmpLegareSexType == 0:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Дать им кончить" if CurSexStep == 4 and tmpLegareSexType >= 2:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "И что дальше?" if CurSexStep == 5 and tmpLegareSexType >= 1:
            call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
            return

        "Прервать это непотребство" if CurSexStep < MaxStep - 1 and not Amanda.knows_player_is_watching_legare_sex:
            $ Amanda.legare_forbidden = True
            $ Amanda.knows_player_saw_legare_sex = True
            $ Amanda.knows_player_is_watching_legare_sex = True
            $ Amanda.legare_affection -= 1
            $ AmandaNesluh = Amanda.nesluh_value()

            if AmandaNesluh == 2:
                "Аманда отреагировала на вашу ругань совсем не так, как вы ожидали. Будучи не в состоянии увидеть вас из-за груды бочек, она заорала чуть в сторону от того места, где вы действительно находились."
                if Amanda.var_int("glorydeflower", 0) > 0 or Amanda.var_int("fuckyou", 0) > 0:
                    "\"Значит ты ревнуешь? С тобой мне можно трахаться, а с Альберчиком получается нет? А что ты можешь сделать? Ничего. Только смотреть. Ну вот и смотри себе и завидуй!\""
                else:
                    "\"Значит ты ревнуешь? Когда я тебе отсосала, ты мне и слова не сказал, а с Альберчиком покувыркаться ты мне запретить пытаешься? А что ты можешь сделать? Ничего. Только смотреть. Ну вот и смотри себе и завидуй!\""
                "Слово с делом у нее не разошлись, и Аманда нагло продолжила свои развлечения с немного ошарашенным Альбером, уже не стесняясь вас."
                $ Amanda.change_social(corruption_delta=3)

                menu:
                    "Ничего не поделаешь, смотреть дальше":
                        call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
                        return
                    "Я на это смотреть не могу и пойду отсюда":
                        if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                            $ Amanda.resolve_legare_let_go(1, tmpLegareSexType)
                        $ calendar_v2.advance_minutes(60)
                        $ main_ui_end_native_scene_state()
                        jump StreetTavern

            elif AmandaNesluh == 1:
                "Ваша тирада не слишком впечатлила Аманду. Она лишь пожала плечами и спросила у своего любовника: \"Альберчик, может мы в дом зайдем, где мой настырный хозяин не будет нас донимать?\" У Альберчика, к вашей досаде, не нашлось никаких возражений, и парочка быстро скрылась в доме, где вы уже не могли им помешать."
                $ Amanda.change_social(friend_delta=(1 if Amanda.rel >= 7 else -1), corruption_delta=2)
                if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                    $ Amanda.resolve_legare_let_go(1, tmpLegareSexType)
                $ calendar_v2.advance_minutes(60)
                $ main_ui_end_native_scene_state()
                jump StreetTavern

            else:
                "Аманда пугается вашего крика, спешно одевается и убегает в трактир."
                $ Amanda.legare_affection -= 2
                $ Amanda.change_social(friend_delta=(1 if Amanda.rel >= 3 else -2), corruption_delta=(1 if Amanda.corruption >= 20 else -3))
                $ calendar_v2.advance_minutes(60)
                $ main_ui_end_native_scene_state()
                jump StreetTavern

        "Дать знать им о том, что вы наблюдаете за ними" if CurSexStep < MaxStep - 1 and not Amanda.knows_player_is_watching_legare_sex and Amanda.knows_player_saw_legare_sex:
            $ Amanda.knows_player_is_watching_legare_sex = True
            "Решив зачем-то намекнуть Аманде о том, что вы за ней подглядываете, вы намеренно с шумом скинули на землю камень, лежавший на одной из бочек. Чтобы ваше присутствие стало совсем явным, вы еще глухо и неразборчиво выругались."

            if Amanda.corruption > 45 or (Amanda.corruption > 32 and procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/AfterDanceSexLegare.rpy:procedural_randint:314:13") == 1):
                "Парочка обернулась на шум. Аманда догадалась сразу и сообщила об этом Легаре. Но это их почти не смутило, и они продолжили свои непотребства мало встревоженные возможным наблюдением."
                $ Amanda.change_social(corruption_delta=2)
                menu:
                    "Ничего не поделаешь, смотреть дальше":
                        call AfterDanceSexLegare(CurSexStep + 1, tmpLegareSexType, FollowMode)
                        return
                    "Плюнуть и идти обратно в трактир":
                        if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                            $ Amanda.resolve_legare_let_go(1, tmpLegareSexType)
                        $ calendar_v2.advance_minutes(60)
                        $ main_ui_end_native_scene_state()
                        jump StreetTavern
            else:
                "После небольшой заминки Аманда заявляет, что так не может, потому что вдруг это действительно Стефан и ей стыдно. С этими словами она утягивает немного ошалевшего Альбера в дом. Почему-то ваша идея обернулась вам не на пользу."
                if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                    $ Amanda.resolve_legare_let_go(1, tmpLegareSexType)
                $ calendar_v2.advance_minutes(60)
                $ main_ui_end_native_scene_state()
                jump StreetTavern

        "Я на это смотреть не могу и пойду отсюда" if CurSexStep < MaxStep - 1 and Amanda.knows_player_is_watching_legare_sex:
            if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                $ Amanda.resolve_legare_let_go(1, tmpLegareSexType)
            $ calendar_v2.advance_minutes(60)
            $ main_ui_end_native_scene_state()
            jump StreetTavern

        "Ухожу, даже и не собираюсь на это смотреть" if CurSexStep < MaxStep and not Amanda.knows_player_is_watching_legare_sex:
            if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                $ Amanda.resolve_legare_let_go(1, tmpLegareSexType)
            $ calendar_v2.advance_minutes(60)
            $ main_ui_end_native_scene_state()
            jump StreetTavern

        "Пойду-ка и я" if (CurSexStep == 4 and tmpLegareSexType == 1) or (CurSexStep == 5 and tmpLegareSexType == 0) or (CurSexStep >= 6):
            if (tmpLegareSexType == 0 and CurSexStep < 4) or (tmpLegareSexType == 1 and CurSexStep < 3) or (tmpLegareSexType >= 2 and CurSexStep < 5):
                $ Amanda.resolve_legare_let_go(1, tmpLegareSexType)
            $ calendar_v2.advance_minutes(60)
            $ main_ui_end_native_scene_state()
            jump StreetTavern

    return
