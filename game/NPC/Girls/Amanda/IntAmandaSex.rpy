# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _ias_set_arousal(who, value):
        value = min(100, max(0, int(value or 0)))
        if str(who or "").lower() == "you":
            player.intimacy.set_arousal(value)
            return
        if str(who or "").strip().lower() == "amanda":
            Amanda.set_arousal(value)

    def _ias_inc_arousal(who, amount):
        if str(who or "").lower() == "you":
            intimacy = player.intimacy
            intimacy.add_arousal(int(amount or 0), 100)
            return
        if str(who or "").strip().lower() == "amanda":
            Amanda.add_arousal(int(amount or 0), 100)

    def _ias_arousal(who):
        if str(who or "").lower() == "you":
            return player.intimacy.arousal_value()
        if str(who or "").strip().lower() == "amanda":
            return Amanda.arousal_value()
        return 0

label IntAmandaSex(GirlNameASDS="amanda", GirlLocASDS="home", GirlModeASDS=""):
    $ renpy.dynamic("_amanda_cumpussy_pic", "_amanda_naked_pic", "_was_fucking_amanda", "_amanda_street_fuck_pic", "_amanda_room_fuck_pic", "tmpCumInside", "CurAmandaOrgasmCount", "_cametoday", "_cancumdaily", "_ias_started_native_scene", "_ias_parent_title", "_ias_text_parts", "_ias_scene_active")
    python:
        Amanda.ensure_sex_state()
        CurAmandaOrgasmCount = Amanda.sex_stat("orgasms_given", 0)
        _ias_started_native_scene = main_ui_runtime.scene_origin is None
        _ias_parent_title = str(main_ui_runtime.action_title or "")
        _ias_scene_active = True
    $ main_ui_begin_native_scene_state("Аманда")
    call ShowAmandaPortrait
    $ scene_runtime.text = str(Amanda.data.description or "")
    $ scene_runtime.location_text = scene_runtime.text

    label int_amanda_sex_menu:
        while True:
            if not _ias_scene_active:
                if _ias_started_native_scene:
                    $ main_ui_end_native_scene_state()
                else:
                    $ main_ui_runtime.mode = "event"
                    $ main_ui_runtime.action_title = _ias_parent_title
                    $ main_ui_restart_interaction()
                return
            python:
                _cametoday = int(player.intimacy.came_today or 0)
                _cancumdaily = max(1, int(player.intimacy.can_cum_daily or 1))

            menu:
                "Осмотреть":
                    $ scene_runtime.text = str(Amanda.data.description or "")
                    $ scene_runtime.location_text = scene_runtime.text

                "Снять блузку" if Amanda.clothing_layer("top") != "" and not Amanda.sex_busy() and GirlModeASDS != "minet":
                    if Amanda.clothing_slut("top") >= 4 or Amanda.layer_raised("top"):
                        "Хотя Амандина блузка и так не скрывала почти ничего, вы решили ее полностью снять. Расстегнув последние крючки и застежки, вы стянули этот явно лишний предмет."
                        if Amanda.clothing_layer("bra") == "":
                            "Так вы обнажили ее до пояса."
                        else:
                            "И теперь на ней оставался лишь лиф."
                    else:
                        "На ваш нескромный взгляд, тело [people_name(GirlNameASDS, 'genitive')] было слишком закутано. Решив помочь Аманде почувствовать себя открытой и свободной, вы с энтузиазмом взялись за дело, смело вступив в битву с многочисленными крючками и застежками, скрепляющими верхнюю часть платья вместе."
                        if Amanda.clothing_layer("bra") == "":
                            "Победа над ними принесла вам приятное открытие: ваша маленькая проказница не надела лиф! Ее маленькие острые грудки доступны вашим нескромным взорам и не только им."
                        else:
                            "И вот наконец победа близка: от вожделенных сисечек вас отделяет только лиф!"
                    if Amanda.clothing_slut("top") < 4 and Amanda.layer_raised("top") == 0 and Amanda.pregnancy_days() >= 120:
                        "Также, после избавления от блузки, стал хорошо заметен округлившийся животик [people_name(GirlNameASDS, 'genitive')]."
                    $ Amanda.remove_clothing_layer("top")
                    $ Amanda.set_layer_raised("top", 0)
                    call ShowAmandaPortrait

                "Растегнуть блузку" if Amanda.clothing_layer("top") != "" and Amanda.layer_raised("top") == 0 and not Amanda.sex_busy() and GirlModeASDS != "minet":
                    if Amanda.clothing_layer("bra") == "":
                        if Amanda.clothing_slut("top") >= 4:
                            "Вы начали поглаживать и сжимать грудки [people_name(GirlNameASDS, 'genitive')] сквозь одежду, вызвав несколько сдержанных стонов у девушки. Дабы облегчить себе доступ к ним, вы начали расстегивать ее блузку и вскоре преуспели в этом, тем более что под ней не оказалось лифа. Теперь сисечки [people_name(GirlNameASDS, 'genitive')] с задорно торчащими сосками на свободе, блузка расстегнута до пупа."
                        else:
                            "Ваша скромница оделась уж как-то слишком консервативно. Непорядок. Вы начали расстегивать явно стесняющую ее блузку и не прогадали: под скромной с виду одеждой не оказалось лифчика и ее маленькие сисечки оказались полностью в вашем распоряжении."
                    else:
                        if Amanda.clothing_slut("top") >= 4:
                            "Вы начали поглаживать и сжимать грудки [people_name(GirlNameASDS, 'genitive')] сквозь одежду, вызвав несколько сдержанных стонов у девушки. Дабы облегчить себе доступ к ним, вы начали расстегивать ее блузку и вскоре преуспели в этом, хотя между вами и ее грудями все еще остается лифчик."
                        else:
                            "Ваша скромница оделась уж как-то слишком консервативно. Непорядок. Вы начали расстегивать явно стесняющую ее блузку, не встречая никаких возражений со стороны [people_name(GirlNameASDS, 'genitive')]. Как и следовало ожидать, под ней оказался лиф, последнее препятствие, лежащее между вами и ее грудями."
                    if Amanda.clothing_slut("top") < 4 and Amanda.pregnancy_days() >= 120:
                        "Распахнутая блузка также теперь не мешает вам лицезреть округлившийся животик [people_name(GirlNameASDS, 'genitive')]."
                    $ Amanda.set_layer_raised("top", 1)
                    call ShowAmandaPortrait

                "Снять лифчик" if Amanda.clothing_layer("bra") != "" and (Amanda.clothing_layer("top") == "" or Amanda.layer_raised("top")) and not Amanda.sex_busy() and GirlModeASDS != "minet":
                    if Amanda.clothing_layer("top") == "":
                        "Выше пояса на [people_name(GirlNameASDS, 'dative')] теперь остается лишь лифчик. Поцеловав и обняв Аманду, вы запустили руки ей за спину и начали его на ощупь расстегивать."
                    else:
                        "Хоть блузка и распахнута настежь, но между вами и сиськами еще остается лифчик. Засунув руки под ткань блузки, вы начинаете расстегивать его на ощупь."
                    if (player.intimacy.had_sex_count >= 8 and Amanda.clothing_layer("top") == "") or player.intimacy.had_sex_count >= 16:
                        "С легкостью справившись с застежками и завязками, вы отбрасываете лиф прочь, обнажив маленькие упругие груди."
                    else:
                        "Вы провозились с бесчисленными застежками и завязками довольно долго, не смотря на подаваемые без конца советы Аманды. И вот наконец лифчик снят, сиськи [people_name(GirlNameASDS, 'genitive')] на вашем обозрении."
                    $ Amanda.remove_clothing_layer("bra")
                    call ShowAmandaPortrait

                "Поднять подол" if Amanda.clothing_layer("bottom") != "" and Amanda.layer_raised("bottom") == 0 and not Amanda.sex_busy() and GirlModeASDS != "minet":
                    if Amanda.clothing_slut("bottom") >= 4:
                        if Amanda.clothing_layer("panties") != "":
                            "Вы впились жарким поцелуем в губы [people_name(GirlNameASDS, 'genitive')]. Ну а затем задрали и без того короткую юбочку Аманды до пояса, выставив ее панталончики на ваше обозрение."
                        elif Amanda.current_underwear("panties", "") == "":
                            "\"А что, [people_display_name(GirlNameASDS)],\" — спросили вы, — \"юбчишку ты носишь коротенькую, небось под ней и нижнего белья-то нет?\""
                            "\"Угадал,\" — игриво ответила вам [people_display_name(GirlNameASDS)] и заткнула за пояс подол своей юбки, показывая, что под ним и правда ничего не было."
                        else:
                            "Вы впились жарким поцелуем в губы [people_name(GirlNameASDS, 'genitive')]. Ну а затем задрали и без того короткую юбочку Аманды до пояса, выставив ее голенькую щелку на свое обозрение."
                    else:
                        if Amanda.clothing_layer("panties") != "":
                            "Вы впились жарким поцелуем в губы [people_name(GirlNameASDS, 'genitive')]. Ну а затем оборочка за оборочкой подняли длинный подол ее платья и завернули его за пояс, выставляя Амандины панталончики на ваше обозрение."
                        elif Amanda.current_underwear("panties", "") == "":
                            "\"А что, [people_display_name(GirlNameASDS)],\" — скептически спросили вы, — \"юбка у тебя почти до пят, раз ты такая скромница, то небось под ней у тебя еще несколько юбок и уж затем панталончики?\""
                            "\"А вот и не угадал,\" — ответила вам Аманда слегка покраснев. \"Под ней у меня вообще ничего нет. Смотри!\" И она сноровисто приподняла и заткнула за пояс длинный подол своего платья. Вы были приятно удивлены, не обнаружив под ним и следов нижнего белья."
                        else:
                            "Вы впились жарким поцелуем в губы [people_name(GirlNameASDS, 'genitive')]. Ну а затем оборочка за оборочкой подняли длинный подол ее платья и завернули его за пояс, выставив голенькую щелку Аманды на свое обозрение."
                    $ Amanda.set_layer_raised("bottom", 1)
                    call ShowAmandaPortrait

                "Снять платье" if Amanda.clothing_layer("bottom") != "" and not Amanda.sex_busy() and GirlModeASDS != "minet":
                    if Amanda.layer_raised("bottom"):
                        "Решив, что задранного подола вам мало, вы развязали на [people_name(GirlNameASDS, 'dative')] поясок и несколько завязочек и наконец окончательно стянули с нее платье."
                    else:
                        if Amanda.clothing_layer("panties") != "":
                            "Вы поцеловали [people_name(GirlNameASDS, 'genitive')] в губы, а затем развязали поясок, и юбка упала к ногам Аманды, выставив ее кружевные панталончики на ваше обозрение."
                        elif Amanda.current_underwear("panties", "") == "":
                            "\"[people_display_name(GirlNameASDS)], мне кажется что ты будешь куда лучше выглядеть в одних панталонах,\" — нагло заявили вы. — \"А ты как считаешь? Давай заценим!\""
                            "\"Не знаю,\" — ответила вам Аманда слегка покраснев. \"Я ведь под платьем совсем голенькая. Смотри!\" И она сноровисто распустила завязки на платье, которое незамедлительно упало к ее ногам. Вы были приятно удивлены, воочию убедившись в том, что она сказала чистую правду."
                        else:
                            "Вы поцеловали [people_name(GirlNameASDS, 'genitive')] в губы, а затем развязали поясок, и юбка упала к ее ногам, выставив ее голенькую щелку на ваше обозрение."
                    $ Amanda.remove_clothing_layer("bottom")
                    $ Amanda.set_layer_raised("bottom", 0)
                    call ShowAmandaPortrait

                "Снять панталончики" if Amanda.clothing_layer("panties") != "" and not Amanda.sex_busy() and GirlModeASDS != "minet":
                    if Amanda.layer_raised("bottom") == 0 and Amanda.clothing_layer("bottom") != "" and Amanda.clothing_slut("bottom") >= 4:
                        "Вы засунули свои шаловливые ручки под короткую юбчонку Аманды и стащили с нее панталончики."
                    elif Amanda.layer_raised("bottom") == 0 and Amanda.clothing_layer("bottom") != "":
                        "Вы присели перед Амандой на колени, залезли под длинный подол ее платья и медленно повели свои руки вверх. [people_display_name(GirlNameASDS)] захихикала, видно ей было немного щекотно. Наконец вы нащупали панталоны и спустили их вниз. [people_display_name(GirlNameASDS)] переступила через них, но длинный подол опять скрыл ее прелести."
                    else:
                        "Вы решаете избавиться от последнего препятствия, отделяющего вас от ее пещерки. Не теряя времени, вы аккуратно стягиваете с нее панталончики. Досадная помеха убрана, киска [people_name(GirlNameASDS, 'genitive')] беззащитна перед вами."
                    $ Amanda.remove_clothing_layer("panties")
                    call ShowAmandaPortrait

                "Вытереть сперму с лица" if (Amanda.cum_state("cum_face_you") or Amanda.cum_state("cum_face_others")) and not Amanda.sex_busy():
                    "Вы попросили Аманду убрать с лица свидетельства ее половой жизни. [people_display_name(GirlNameASDS)] покраснела, достала платочек и вытерла лицо и волосы от спермы."
                    $ Amanda.clear_cum("cum_face_you", "cum_face_others")
                    call ShowAmandaPortrait

                "Вытереть сперму с грудей" if (Amanda.cum_state("cum_tits_you") or Amanda.cum_state("cum_tits_others")) and Amanda.tits_visible() and not Amanda.sex_busy():
                    "Вы попросили Аманду убрать свидетельства ее половой жизни с сисек. [people_display_name(GirlNameASDS)] достала платочек и, улыбаясь чуть стыдливо, вытерла сперму со своих маленьких грудок."
                    $ Amanda.clear_cum("cum_tits_you", "cum_tits_others")
                    call ShowAmandaPortrait

                "Вытереть сперму с бедер" if (Amanda.cum_state("cum_inside_you") or Amanda.cum_state("cum_inside_others")) and Amanda.pussy_visible() and not Amanda.sex_busy():
                    "\"[people_display_name(GirlNameASDS)]\", сказали вы, \"прибери пожалуйста свою делянку. Чтобы не так очевидно было то, что ее недавно засеяли.\" Та рассмеялась, достала платочек и, чуть виновато посматривая на вас, вытерла бедра и лобок от спермы. Скорее всего сперма во влагалище еще осталась, но вы ее теперь вряд ли почувствуете."
                    $ Amanda.clear_cum("cum_inside_you", "cum_inside_others")
                    call ShowAmandaPortrait

                "Целовать" if not Amanda.sex_busy():
                    $ _ias_text_parts = ["[people_display_name(GirlNameASDS)] прижимается к вам всем телом и со всей страстью молодости целует вас отнюдь не семейным поцелуем."]
                    if Amanda.cum_state("cum_face_you") > 0:
                        $ _ias_text_parts.append("На язык вам попадают капли вашего семени, которым вы обкончали девушку раньше.")
                    elif Amanda.cum_state("cum_face_others") > 0:
                        $ _ias_text_parts.append("Вы чувствуете солоноватый привкус чужой спермы. Похоже, Аманда уже успела сегодня у кого-то отсосать!")
                    $ _ias_inc_arousal(GirlNameASDS, 14)
                    if _ias_arousal("You") < 50:
                        $ _ias_inc_arousal("You", 9)
                    if GirlLocASDS != "street":
                        if Amanda.tits_visible() and Amanda.pussy_visible():
                            $ show_image(GirlNameASDS, "sexroom", "kissnaked")
                        else:
                            $ show_image(GirlNameASDS, "sexroom", "kiss")
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)

                "Лапать" if not Amanda.sex_busy():
                    $ _ias_text_parts = []
                    if not Amanda.tits_visible():
                        if Amanda.clothing_slut("top") == 3 and Amanda.clothing_layer("bra") == "":
                            $ _ias_text_parts.append("Вы начали поглаживать маленькую грудь [people_name(GirlNameASDS, 'genitive')] через тонкую ткань ее блузки.")
                        elif Amanda.clothing_slut("top") >= 4 and Amanda.clothing_layer("bra") == "":
                            $ _ias_text_parts.append("Ваши руки забрались под декольте Аманды и, не обнаружив там лифчика, начали гладить ее небольшие груди и теребить напрягшиеся сосочки.")
                        elif Amanda.clothing_slut("top") >= 4 and Amanda.clothing_layer("bra") != "":
                            $ _ias_text_parts.append("Ваши руки забрались под декольте [people_name(GirlNameASDS, 'genitive')] и начали мять ее сисечки через лифчик.")
                        else:
                            $ _ias_text_parts.append("Скромное одеяние девушки не отвратило вас от пошлых мыслей, вы начали гладить и мять маленькие сисечки [people_name(GirlNameASDS, 'genitive')] и через него.")
                    else:
                        if Amanda.cum_state("cum_tits_you") > 0:
                            $ _ias_text_parts.append("Вы припали к маленьким грудям [people_name(GirlNameASDS, 'genitive')], благо они помещались у вас во рту почти целиком. На языке вы почувствовали солоноватый привкус своей спермы.")
                        elif Amanda.cum_state("cum_tits_others") > 0:
                            $ _ias_text_parts.append("Вы припали к маленьким грудям [people_name(GirlNameASDS, 'genitive')], благо они помещались у вас во рту почти целиком. На языке вы почувствовали солоноватый привкус чьей-то спермы.")
                        else:
                            $ _ias_text_parts.append("Вы припали к маленьким грудям [people_name(GirlNameASDS, 'genitive')], благо они помещались у вас во рту почти целиком.")

                    if Amanda.pussy_visible():
                        $ _ias_text_parts.append("Вы медленно опустили руку вниз, к вульве Аманды. Она вздрогнула от вашего прикосновения. На этом вы не остановились, запустив пару пальцев внутрь текущей девушки.")
                    else:
                        if Amanda.layer_raised("bottom") == 0 and Amanda.clothing_layer("bottom") != "":
                            if Amanda.clothing_slut("bottom") >= 4:
                                if Amanda.clothing_layer("panties") != "":
                                    $ _ias_text_parts.append("Вы сунули руку под короткую юбчонку Аманды и начали натирать ее киску сквозь панталончики.")
                                else:
                                    $ _ias_text_parts.append("Вы сунули руку под короткую юбчонку Аманды и пролезли ловким пальчиком в ее не стесненную нижним бельем киску.")
                            else:
                                if Amanda.clothing_layer("panties") != "":
                                    $ _ias_text_parts.append("Вы наклонились дабы залезть шаловливыми ручонками под длинную юбку Аманды. На этом вы не остановились, а стали потихоньку двигаться наверх, к заветному месту и начали натирать ее киску сквозь панталончики.")
                                else:
                                    $ _ias_text_parts.append("Вы наклонились дабы залезть шаловливыми ручонками под длинную юбку Аманды. На этом вы не остановились, а стали потихоньку двигаться наверх, к заветному месту и пролезли ловким пальчиком в ее не стесненную нижним бельем киску.")
                        else:
                            $ _ias_text_parts.append("Вы начали натирать киску Аманды сквозь панталончики.")
                    if Amanda.clothing_layer("panties") == "":
                        if Amanda.cum_state("cum_inside_you") > 0:
                            $ _ias_text_parts.append("Вдруг вы почувствовали свою сперму в пещерке [people_name(GirlNameASDS, 'genitive')].")
                        elif Amanda.cum_state("cum_inside_others") > 0:
                            $ _ias_text_parts.append("Ваши пальцы легко заскользили по пещерке [people_name(GirlNameASDS, 'genitive')]: похоже кто-то уже кончил в нее.")
                    $ _ias_inc_arousal(GirlNameASDS, 12)
                    if GirlLocASDS != "street":
                        if Amanda.tits_visible() and Amanda.pussy_visible():
                            $ show_image(GirlNameASDS, "sexroom", "grope2")
                        elif Amanda.pussy_visible():
                            $ show_image(GirlNameASDS, "sexroom", "grope1")
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)

                "Лизать киску" if Amanda.pussy_visible() and not Amanda.sex_busy() and GirlModeASDS != "minet":
                    $ _ias_text_parts = ["Вы пролезли между раздвинутых ножек [people_name(GirlNameASDS, 'genitive')] и начали делать Аманде куни. Это пришлось ей по душе и по кое-чему еще. [people_display_name(GirlNameASDS)] откинулась назад и сладко стонет от ваших ласк."]
                    if Amanda.cum_state("cum_inside_you") > 0:
                        $ _ias_text_parts.append("Ну а вы ощущаете привкус собственной спермы, медленно вытекающей из ее влагалища.")
                    elif Amanda.cum_state("cum_inside_others") > 0:
                        $ _ias_text_parts.append("Ну а вы ощущаете привкус чьей-то спермы, медленно вытекающей из ее влагалища. Похоже, Аманда уже успела сегодня кому-то дать.")
                    $ Amanda.record_lick_pussy()
                    if Amanda.lick_pussy_count() == 6:
                        $ _ias_text_parts.append('"Стефанчик, приятно-то как!", смеясь говорит [people_display_name(GirlNameASDS)], "где это с кем это ты так научился? Впрочем не важно, эх, приятно-то как!"')
                        $ Amanda.change_social(friend_delta=1)
                    $ _ias_inc_arousal(GirlNameASDS, 25)
                    if GirlLocASDS != "street":
                        $ show_image(GirlNameASDS, "sexroom", "cuni")
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)

                "Минет" if _cametoday < _cancumdaily and not Amanda.sex_busy():
                    $ _ias_text_parts = []
                    if GirlLocASDS == "street":
                        if Amanda.cock_in("mouth"):
                            $ _ias_text_parts.append("[people_display_name(GirlNameASDS)], не забывая посматривать по сторонам, продолжает.")
                        else:
                            $ _ias_text_parts.append("Вы расстегнули штаны. [people_display_name(GirlNameASDS)] метнула взгляд к выходу из переулка, убедилась что никого нет, опустилась перед вами на коленки и стала.")
                    elif GirlLocASDS == "kitchen":
                        if Amanda.cock_in("mouth"):
                            $ _ias_text_parts.append("Спрятавшись с вами в укромном углу кухни, [people_display_name(GirlNameASDS)] продолжает возвращать обещанную услугу.")
                        else:
                            $ _ias_text_parts.append("Вы вместе отходите в укромный угол кухни. [people_display_name(GirlNameASDS)] еще раз убеждается, что никто не смотрит, опускается перед вами на колени и принимается возвращать обещанную услугу.")
                    else:
                        if Amanda.cock_in("mouth"):
                            $ _ias_text_parts.append("Вы расселись на кровати и ловите кайф, в то время как [people_display_name(GirlNameASDS)] стоит перед вами на коленях и продолжает.")
                        else:
                            $ _ias_text_parts.append("Вы уселись поудобней на кровати и расстегнули штаны. Умненькая [people_display_name(GirlNameASDS)] сразу поняла что от нее требуется. Аманда слезла с кровати, опустилась на колени и стала.")
                    if _ias_arousal("You") < 20:
                        $ _ias_text_parts.append("Облизывать ваш вялый член.")
                    elif _ias_arousal("You") < 40:
                        $ _ias_text_parts.append("Облизывать головку вашего напрягшегося члена.")
                    elif Amanda.corruption < 40:
                        $ _ias_text_parts.append("Неумело, но с энтузиазмом сосать ваш член.")
                    elif _ias_arousal("You") < 60:
                        $ _ias_text_parts.append("Умело сосать ваш член.")
                    else:
                        $ _ias_text_parts.append("Заглатывать ваш член по самые яйца.")
                    $ Amanda.set_cock_position("mouth")
                    if Amanda.corruption < 40:
                        $ _ias_inc_arousal("You", 18)
                    else:
                        $ _ias_inc_arousal("You", 22)
                    $ Amanda.set_var_int("suckyou", 1)
                    if GirlLocASDS == "street":
                        if _ias_arousal("You") < 20:
                            $ show_image(GirlNameASDS, "sexafterdance", "minet1")
                        elif _ias_arousal("You") < 40:
                            $ show_image(GirlNameASDS, "sexafterdance", "minet2")
                        elif Amanda.corruption < 40:
                            $ show_image(GirlNameASDS, "sexafterdance", "minet3")
                        elif _ias_arousal("You") < 60:
                            $ show_image(GirlNameASDS, "sexafterdance", "minet4")
                        else:
                            $ show_image(GirlNameASDS, "sexafterdance", "minet5")
                    else:
                        $ show_image_seq(GirlNameASDS, "sexroom", "minet", 12)
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)

                "Трахать" if _cametoday < _cancumdaily and not Amanda.sex_busy() and _ias_arousal("You") >= 20 and _ias_arousal(GirlNameASDS) >= 20 and Amanda.pussy_visible() and not Amanda.cock_in("pussy", "eddie") and GirlModeASDS != "minet":
                    $ _was_fucking_amanda = int(Amanda.cock_in("pussy") or 0)
                    $ _ias_text_parts = []
                    if GirlLocASDS == "street":
                        if Amanda.pregnancy_days() < 130:
                            if _was_fucking_amanda == 0:
                                $ _ias_text_parts.append("Вы посмотрели Аманде прямо в глаза и, убедившись что она вас поняла, перевели взгляд на своего стоящего колом дружка. Как загипнотизированная [people_display_name(GirlNameASDS)] последовала своим взглядом за вашим. Решив что медлить дальше не имеет смысла, вы притянули девушку к себе, крепко ее поцеловав, а затем подхватили ее и насадили прямо на свой член. [people_display_name(GirlNameASDS)] слегка охнула, обхватила вас за шею и сжала ногами.")
                            else:
                                $ _ias_text_parts.append("Вы стоите в переулке и сношаете на весу свою блудливую любовницу. Слава Ильматеру, она стройная и легкая, тростиночка ваша. И вы, и она, время от времени оглядываетесь по сторонам, но, к вашему счастью, никто сюда не идет. Впрочем, даже если кто вас и засечет, уличным трахом в Коитополисе никого не удивить. Ваша поза позволяет загонять вам свой член в тесное влагалище Аманды по самые яйца, почти доставая до матки.")
                        else:
                            if _was_fucking_amanda == 0:
                                $ _ias_text_parts.append("На ваше счастье в подворотне нашлась какая-то тележка, типа той на которой в ваш трактир привозили заказы. Быстро сориентировавшись в обстановке вы уложили свою залетную красотку на эту телегу пузом вверх и, закинув ее ножки себе на плечи, начали сношать девицу. Впрочем [people_display_name(GirlNameASDS)] быстро устала держать ноги на весу и вам пришлось поменять позу, дав Аманде встать и прислониться к пресловутой тележке.")
                            else:
                                $ _ias_text_parts.append("Маленький переулок стал весьма шумным местом - ваша беременная подруга стоит облокотившись на какую-то телегу, а вы трахаете ее сзади. [people_display_name(GirlNameASDS)] уже не сдерживает стоны, но вроде пока к вам никто еще не заглянул.")
                                if Amanda.pregnancy_days() > 120:
                                    $ _ias_text_parts.append("Вы чувствуете как ребенок в животике у маленькой [people_name(GirlNameASDS, 'genitive')] двигается каждый раз когда ваш член входит в нее.")
                    else:
                        if _was_fucking_amanda == 0:
                            $ _ias_text_parts.append("Бесстыжая [people_display_name(GirlNameASDS)] откинулась на кровати, задрав ножки и открыв свою киску вашим нескромным взглядам. Решив не пренебрегать таким приглашением вы нацелили свой член на вход в ее пещерку. Найдя заветную дырочку вы легко проскользнули в мокренькую Аманду.")
                        else:
                            $ _ias_text_parts.append("Вы имеете свою не слишком целомудренную любовницу на ее собственной кровати. Ее ножки красиво обрамляют ваши плечи, а удобная поза позволяет вам загонять свой член в нее по самые яйца.")
                            if Amanda.pregnancy_days() > 120:
                                $ _ias_text_parts.append("Руками вы то теребите [people_name(GirlNameASDS, 'dative')] клитор, то поглаживаете пузатый живот который та себе нагуляла.")
                            else:
                                $ _ias_text_parts.append("Руками вы то теребите [people_name(GirlNameASDS, 'dative')] клитор, то ласкаете ее груди.")
                    $ Amanda.set_cock_position("pussy")
                    $ _ias_inc_arousal("You", 25)
                    $ _ias_inc_arousal(GirlNameASDS, 20)
                    $ Amanda.set_var_int("fuckyou", 1)
                    if Amanda.var_int("knownotvirgin", 0) == 0 and Amanda.sex_stat("virginity", True) == False:
                        $ _ias_text_parts.append("Кстати, вы легко и без препятствий вошли в Аманду. Похоже, она уже не девочка. Может стоит потом ее об этом расспросить.")
                        $ Amanda.set_var_int("knownotvirgin", 1)
                    if Amanda.sex_stat("virginity", True):
                        $ Amanda.set_sex_stat("virginity", False)
                        $ Amanda.set_var_int("knownotvirgin", 1)
                    if GirlLocASDS == "street":
                        if Amanda.pregnancy_days() < 130:
                            $ _amanda_street_fuck_pic = "fuck" + str(procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/IntAmandaSex.rpy:procedural_randint:367:1"))
                            $ show_image(GirlNameASDS, "sexafterdance", _amanda_street_fuck_pic)
                        else:
                            if _was_fucking_amanda == 0:
                                $ show_image(GirlNameASDS, "sexafterdance", "fuckarba1")
                            else:
                                $ show_image(GirlNameASDS, "sexafterdance", "fuckarba2")
                    else:
                        if _was_fucking_amanda == 1:
                            $ _amanda_room_fuck_pic = "fuck" + str(procedural_randint(1, 6, key="procedural:NPC/Girls/Amanda/IntAmandaSex.rpy:procedural_randint:376:2"))
                            $ show_image(GirlNameASDS, "sexroom", _amanda_room_fuck_pic)
                        else:
                            $ show_image(GirlNameASDS, "sexroom", "fuckstart")
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)

                "Кончить в ротик" if _cametoday < _cancumdaily and _ias_arousal("You") >= 100 and (Amanda.cock_in("mouth") or Amanda.cock_in("tits")):
                    $ _ias_text_parts = ["Вы кончили, заливая горло и рот [people_name(GirlNameASDS, 'genitive')] своей спермой. Девушка не сделала ни малейшей попытки отстраниться и начала жадно глотать ваше семя. Его было много, она не успела сглотнуть все, и вязкая белая жидкость потекла из уголков ее очаровательного ротика. [people_display_name(GirlNameASDS)] выпустила ваш обмякший член из сладкого плена, облизала губы и, с томной улыбкой сказала: надеюсь тебе понравилось. Вы поспешили заверить девушку что вам очень и очень понравилось."]
                    $ _ias_set_arousal("You", 0)
                    $ Amanda.pregnancy_check("mouth", 1, "Вы")
                    $ Amanda.set_cock_position("none")
                    $ Amanda.set_sex_busy(True)
                    $ Amanda.set_cum_state("cum_face_you", 1)
                    if GirlLocASDS == "street":
                        $ show_image(GirlNameASDS, "sexafterdance", "cumface")
                    else:
                        $ show_image_seq(GirlNameASDS, "sexroom", "come", 2)
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)
                    call int_amanda_sex_after_cum
                    if _return:
                        $ _ias_scene_active = False

                "Кончить на лицо" if _cametoday < _cancumdaily and _ias_arousal("You") >= 100:
                    $ _ias_text_parts = ["Перед самым оргазмом"]
                    if Amanda.cock_in("mouth"):
                        $ _ias_text_parts.append("вы вытащили член изо рта Аманды и кончили ей на мордашку.")
                    elif Amanda.cock_in("pussy"):
                        $ _ias_text_parts.append("колоссальным усилием воли вы вынули член из киски Аманды и направили его на ее смазливую мордашку.")
                    else:
                        $ _ias_text_parts.append("вы направили свой член на ее смазливую мордашку.")
                    $ _ias_text_parts.append("Густая белая струя брызнула прямо [people_name(GirlNameASDS, 'dative')] в лицо. Крупные белые капли потекли по ее щечкам и подбородку, одна струйка попала ей в левый глаз, отчего она зажмурилась, а пара капель осталась в ее белокурых локонах. Очень романтично!")
                    $ _ias_set_arousal("You", 0)
                    $ Amanda.pregnancy_check("face", 1, "Вы")
                    $ Amanda.set_cock_position("none")
                    $ Amanda.set_sex_busy(True)
                    $ Amanda.set_cum_state("cum_face_you", 1)
                    if GirlLocASDS == "street":
                        $ show_image(GirlNameASDS, "sexafterdance", "cumface")
                    else:
                        $ show_image(GirlNameASDS, "sexroom", "comeface")
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)
                    call int_amanda_sex_after_cum
                    if _return:
                        $ _ias_scene_active = False

                "Кончить на груди" if _cametoday < _cancumdaily and _ias_arousal("You") >= 100 and Amanda.tits_visible() and GirlModeASDS != "minet":
                    $ _ias_text_parts = ["Почувствовав наступление оргазма"]
                    if Amanda.cock_in("mouth"):
                        $ _ias_text_parts.append("вы вытащили член изо рта Аманды и нацелили его на маленькие сисечки.")
                    elif Amanda.cock_in("pussy"):
                        $ _ias_text_parts.append("колоссальным усилием воли вы вынули член из киски Аманды и направили его на маленькие сисечки.")
                    else:
                        $ _ias_text_parts.append("вы решили обкончать ее маленькие сисечки.")
                    $ _ias_text_parts.append("Сказано - сделано! Двумя точными струями вы заляпали оба шарика своим семенем.")
                    $ _ias_set_arousal("You", 0)
                    $ Amanda.pregnancy_check("tits", 1, "Вы")
                    $ Amanda.set_cock_position("none")
                    $ Amanda.set_sex_busy(True)
                    $ Amanda.set_cum_state("cum_tits_you", 1)
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)
                    call int_amanda_sex_after_cum
                    if _return:
                        $ _ias_scene_active = False

                "Кончить в Аманду" if _cametoday < _cancumdaily and _ias_arousal("You") >= 100 and Amanda.cock_in("pussy") and GirlModeASDS != "minet":
                    $ tmpCumInside = Amanda.sex_count("you", "inside")
                    $ _ias_text_parts = []
                    if Amanda.pregnancy_days() < 120 and Amanda.corruption < 60:
                        $ _ias_text_parts.append("Вы не особо-то прислушались к просьбе Аманды и даже не попытались вовремя вытащить. Почувствовав что ее заполняет ваше семя, Аманда попробовала оттолкнуть вас, но все было без толку: пока вы не заполнили ее киску своей спермой - члена вы не вытащили. [people_display_name(GirlNameASDS)] с ужасом посмотрела на белую струйку, вытекающую из нее.")
                        if tmpCumInside == 0 and int(Amanda.sex_stat("cuminside", 0) or 0) >= 2:
                            $ _ias_text_parts.append('"Эх, и ты тоже такой же как все, кончаешь внутрь, а о последствиях и не думаешь," несколько туманно заметила Аманда.')
                        elif tmpCumInside > 4:
                            $ _ias_text_parts.append('"Да сколько раз тебе говорить, чтобы в меня не кончал!" сердито воскликнула [people_display_name(GirlNameASDS)]. "Вот доиграемся до детей и что тогда? Только тебе это все как об стенку горох! Мог бы хоть разок не о себе, а обо мне подумать!"')
                        else:
                            $ _ias_text_parts.append('"Стефан, ты чего, оглох? Я тебе сказала вытащить. А теперь что делать? А если я залечу? Чтобы это в последний раз было!" строго отчитала вас девушка.')
                        if GirlLocASDS != "street":
                            $ show_image(GirlNameASDS, "sexroom", "cumpussyangry")
                    elif Amanda.pregnancy_days() >= 120:
                        $ _ias_text_parts.append('Рассудив про себя что более беременной чем она есть уже не станет, вы спустили прямо в нее. Судя по всему [people_display_name(GirlNameASDS)] разделяла ваше мнение, так как почувствовав в себе ваше горячее семя она лишь улыбнулась и сказала: "Смотри не утопи моего маленького!"')
                        if GirlLocASDS != "street":
                            $ _amanda_cumpussy_pic = "cumpussy" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaSex.rpy:procedural_randint:455:3"))
                            $ show_image(GirlNameASDS, "sexroom", _amanda_cumpussy_pic)
                    else:
                        $ _ias_text_parts.append("Решив не утруждать себя вы не стали вытаскивать а кончили прямо в тесную киску [people_name(GirlNameASDS, 'genitive')].")
                        $ _ias_text_parts.append('"Ох ты," игриво заметила Аманда. "Ты и в самом деле пытаешься меня обрюхатить! Посмотри, сколько ты накончал!"')
                        $ _ias_text_parts.append("С этими словами Аманда раздвинула ножки, предоставив вам на обозрение свою полную вашей спермы киску.")
                        if GirlLocASDS != "street":
                            $ _amanda_cumpussy_pic = "cumpussy" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaSex.rpy:procedural_randint:462:4"))
                            $ show_image(GirlNameASDS, "sexroom", _amanda_cumpussy_pic)
                    $ _ias_set_arousal("You", 0)
                    $ _ias_inc_arousal(GirlNameASDS, 3)
                    $ Amanda.pregnancy_check("inside", 1, "Вы")
                    $ Amanda.set_cock_position("none")
                    $ Amanda.set_sex_busy(True)
                    $ Amanda.set_cum_state("cum_inside_you", 1)
                    $ scene_runtime.text = "\n\n".join([renpy.substitute(_ias_line) for _ias_line in _ias_text_parts])
                    $ scene_runtime.location_text = scene_runtime.text
                    if str(scene_runtime.picture or "").strip():
                        vscene scene_runtime.picture
                    call ShowCurrentSex(GirlNameASDS)
                    call int_amanda_sex_after_cum
                    if _return:
                        $ _ias_scene_active = False

                "Попрощаться и уйти" if not Amanda.sex_busy() and GirlLocASDS == "home" and GirlModeASDS != "minet":
                    if CurAmandaOrgasmCount == Amanda.sex_stat("orgasms_given", 0):
                        "\"Ну все, пока!\" бодро сказали вы направляясь к выходу. \"Надеюсь тебе понравилось!\""
                        "\"Да ты издеваешься что ли?\" возмутилась та. \"Я же еще не кончила!\""
                        "\"Ну, если тебе это так важно, то можешь ручкой там или пальчиком. Ну, да не мне тебя учить. А лично я уже все что хотел получил. До встречи завтра!\" и с этими словами вы закрыли за собой дверь. С той стороны."
                        $ Amanda.apply_social_chance(3, 1, -1, 25, 1, -2, "amanda_sex_after")
                        call ShowImage(GirlNameASDS, "sexroom", "angry")
                    elif Amanda.sex_stat("orgasms_given", 0) >= CurAmandaOrgasmCount + 3:
                        "Увидев что [people_display_name(GirlNameASDS)], измотанная серией оргазмов, усталая лежит на кровати вы решили что хорошенького понемножку и, чмокнув ее, пошли к выходу."
                        "\"Ну пока, я пошел, а то завтра тебе надо работать, да и мне надо выспаться,\" заметили вы по пути."
                        "\"Стефан, это было просто нечто, дай мне отдохнуть, а завтра приходи еще!\" слабым голосом ответила вам она, слегка привстав на кровати."
                        "И вы вышли в коридор."
                        $ Amanda.apply_social_chance(20, 1, 1, 50, 1, 2, "amanda_sex_after")
                        $ _amanda_naked_pic = "naked" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/IntAmandaSex.rpy:procedural_randint:488:5"))
                        call ShowImage(GirlNameASDS, "sexroom", _amanda_naked_pic)
                    else:
                        "[people_display_name(GirlNameASDS)], после пережитого оргазма, тяжело дыша лежала на кровати."
                        "\"Ну пока, я пошел, а то завтра тебе надо работать, да и мне надо выспаться,\" заметили вы идя к дверям."
                        "\"Да, конечно,\" ответила вам довольная [people_display_name(GirlNameASDS)], привстав на кровати, \"все было здорово, но теперь надо и поспать.\""
                        "И вы вышли в коридор."
                        $ Amanda.apply_social_chance(16, 2, 1, 42, 1, 1, "amanda_sex_after")
                        $ _amanda_naked_pic = "naked" + str(procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/IntAmandaSex.rpy:procedural_randint:496:6"))
                        call ShowImage(GirlNameASDS, "sexroom", _amanda_naked_pic)
                    $ _ias_set_arousal("You", 0)
                    $ _ias_set_arousal(GirlNameASDS, 0)
                    $ Amanda.room_entry_blocked_today = True
                    $ Amanda.set_sex_busy(False)
                    call ShowCurrentSex(GirlNameASDS)
                    $ Amanda.reset_sex_clothing_state()
                    $ main_ui_end_native_scene_state()
                    jump TavernMain

                "Привести себя в порядок и вернуться" if not Amanda.sex_busy() and GirlLocASDS == "street" and GirlModeASDS != "minet":
                    if CurAmandaOrgasmCount == Amanda.sex_stat("orgasms_given", 0):
                        "\"Ну вот и все, идем обратно к трактиру!\" весело заявили вы, застегивая штаны."
                        "\"Как обратно? Ты разве не дашь мне кончить?\" поразилась Аманда."
                        "\"Почему не дам? Хочешь ручкой себя доведи, хочешь пальчиком, я тебе не запрещаю!\" искрометно пошутили вы, продолжая одеваться."
                        "\"Ах ты козел!\" только и смогла ответить вам Аманда, впрочем вы уже оделись и весело пошли широкой походкой к трактиру, оставив хамящую девушку в подворотне."
                        $ Amanda.apply_social_chance(3, 1, -2, 25, 1, -2, "amanda_sex_after")
                    elif Amanda.sex_stat("orgasms_given", 0) >= CurAmandaOrgasmCount + 3:
                        "[people_display_name(GirlNameASDS)] от пережитых оргазмов едва стоит на ногах. Решив что хорошего должно быть в меру, вы начали одеваться сами, одновременно помогая Аманде привести себя в порядок. Одевшись, вы пошли обратно к трактиру."
                        "\"Это было просто нечто, ты самый лучший!\" сказала вам по дороге удовлетворенная Аманда. \"Ну все, пока, я в свою комнату пойду отлежаться,\" и девица упорхнула."
                        $ Amanda.apply_social_chance(20, 1, 1, 50, 1, 2, "amanda_sex_after")
                    else:
                        "Что ж, [people_display_name(GirlNameASDS)] кончила, пора и домой. Вы начали одеваться сами, одновременно помогая Аманде привести себя в порядок. Ну а затем вы пошли обратно к трактиру."
                        "У входа в него Аманда сказала вам: \"Ну все, пока, я наверное уже баиньки пойду,\" и с этими словами упорхнула."
                        $ Amanda.apply_social_chance(16, 2, 1, 42, 1, 1, "amanda_sex_after")
                    $ _ias_set_arousal("You", 0)
                    $ _ias_set_arousal(GirlNameASDS, 0)
                    $ Amanda.room_entry_blocked_today = True
                    call ShowCurrentSex(GirlNameASDS)
                    $ Amanda.reset_sex_clothing_state()
                    $ calendar_v2.advance_minutes(60)
                    $ Amanda.set_sex_busy(False)
                    $ main_ui_end_native_scene_state()
                    jump TavernMain

                "Закончить":
                    $ _ias_scene_active = False

    label int_amanda_sex_after_cum:
        menu:
            "Продолжить":
                $ Amanda.set_sex_busy(False)
                return False

            "Закончить":
                $ Amanda.set_sex_busy(False)
                return True
