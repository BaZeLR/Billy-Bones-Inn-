# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def mom_dress_corruption(girl_name=""):
        info = people.get_info(girl_name)
        return int(info.corruption or 0) if info is not None and hasattr(info, "corruption") else 0

    def mom_dress_complaint_kids_or_preg(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        info = people.get_info(girl)
        if info is not None and int(info.sex_stat("kids", 0) or 0) > 0:
            return 2
        if info is not None and info.pregnancy_days() > 150:
            return 1
        return 0

    def mom_dress_complaint_mark_seen(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        info = people.get_info(girl)
        if info is None:
            return 0
        if girl == "melissa":
            seen_before = int(Melissa.mom_dress_complaint_count or 0)
            Melissa.mom_dress_complaint_count = seen_before + 1
        elif girl == "amanda":
            seen_before = int(Amanda.mom_dress_complaint_count or 0)
            Amanda.mom_dress_complaint_count = seen_before + 1
        else:
            seen_before = int(info.var.get("MomDressComplaint", 0) or 0)
            info.var["MomDressComplaint"] = seen_before + 1
        return seen_before

    def mom_dress_complaint_scold_tail(girl_name="", georgett_present=False, strict_callout=False):
        girl = str(girl_name or "").strip().lower()
        corruption_value = mom_dress_corruption(girl)
        rebellious = (
            corruption_value >= 60
            or (corruption_value >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:rebellious45") == 1)
            or (corruption_value >= 35 and procedural_randint(1, 4, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:rebellious35") == 1)
        )
        if rebellious:
            slut_friends_increase(girl, 5, 1, -2, 65, 1, 2)
            if bool(strict_callout) and bool(georgett_present):
                return "прокричав напоследок, что вы бы лучше на себя сначала посмотрели, как вам со шлюхами путаться так все нормально, а как ей чуть-чуть понаряднее платье одеть - так уже трагедия."
            return "прокричав напоследок, что вы ей не указ и она лучше знает как ей себя вести."

        if bool(georgett_present) and girl == "amanda":
            Amanda.set_var_int("prohibitliza", 1)
            tail = "пообещав напоследок что будет себя скромнее вести и не будет больше болтать с Лизеттой."
        else:
            tail = "пообещав напоследок что будет себя скромнее вести и одеваться."
        slut_friends_increase(girl, 5, 1, -1, 25, 1, -2)
        return tail

    def mom_dress_complaint_finish_scold(girl_name="", georgett_present=False, sandra_friend_delta=2, strict_callout=False):
        tail = mom_dress_complaint_scold_tail(girl_name, georgett_present, strict_callout)
        slut_friends_increase("sandra", 15, 1, sandra_friend_delta, 30, 1, -1)
        return tail

    def mom_dress_complaint_skill_drop_data():
        prof_choice = procedural_randint(1, 3, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:procedural_randint:56:1")
        prof_name = "cooking" if prof_choice == 1 else ("cleaning" if prof_choice == 2 else "waitress")
        prof_desc = "ГОТОВКИ" if prof_name == "cooking" else ("УБОРКИ" if prof_name == "cleaning" else "ОФИЦИАНТКИ")
        current_value = max(0, int(Sandra.skill_value(prof_name, 0) or 0))
        drop_value = max(0, min(procedural_randint(0, 3, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:procedural_randint:60:2"), current_value - 10))
        return {
            "prof_name": prof_name,
            "prof_desc": prof_desc,
            "drop_value": drop_value,
        }


label MomDressComplaint(girl_name):
    $ renpy.dynamic("_mdc_girl", "GirlSillyName", "TalkedBeforeTmp", "KidsOrPregTmp", "_mdc_real_name", "_mdc_georgett_present", "_mdc_intro_text")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    if _mdc_girl == "":
        return

    $ GirlSillyName = "Амандочк" if _mdc_girl == "amanda" else "Меллисочк"
    $ TalkedBeforeTmp = mom_dress_complaint_mark_seen(_mdc_girl)
    $ KidsOrPregTmp = mom_dress_complaint_kids_or_preg(_mdc_girl)
    $ _mdc_real_name = people_display_name(_mdc_girl)
    $ _mdc_georgett_present = str(people.location("georgett") or "") == "TavernMain"
    $ main_ui_begin_native_scene_state("Разговор с Сандрой")
    if renpy.loadable("images/sandra/tavern/cleaning1.jpg"):
        $ scene_runtime.picture = "images/sandra/tavern/cleaning1.jpg"
    elif renpy.loadable("images/tavern/mainhall/tavern_crew.jpg"):
        $ scene_runtime.picture = "images/tavern/mainhall/tavern_crew.jpg"
    if mom_dress_corruption("sandra") < 50:
        $ _mdc_intro_text = "Вы мирно и спокойно шли по своим делам, когда вас вдруг остановила Сандра: \"Стефан, мне надо с тобой поговорить.\"\n\nОтведя вас в сторонку, она продолжила: \"{}Ты видел как {} вырядилась? Как блядь последняя, извини за выражение! Сиськи практически наружу, подол короче некуда! Мне порой кажется, что она и нижнего белья-то не надевает!\"".format("Я знаю, мы уже про это говорили, но не могу дальше молчать. " if TalkedBeforeTmp > 0 else "", _mdc_real_name)
        if _mdc_georgett_present:
            $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nЭто все от Жоржи с Лизкой идет! Стефан, я конечно понимаю, что от этих шлюх нам доходик капает, но ты посмотри, как они на нашу {}у влияют!".format(GirlSillyName)
            if _mdc_girl == "amanda" and Amanda.var_int("prohibitliza", 0):
                $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nТы хоть и запретил Аманде с Лизкой трепаться, но ты ж ее знаешь, она сама лучше всех все знает! Я уже несколько раз видела, как Аманда плевала на все запреты и с этой профурсеткой болтала."
            else:
                $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nКак не посмотрю, она с Лизкой все время о чем-то шушукается!"
            $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nИ вот результат!"
        "[_mdc_intro_text]"
        menu:
            "А чо такого? Мне нравится":
                call MomDressComplaintLikeIt(_mdc_girl, KidsOrPregTmp, _mdc_real_name, _mdc_georgett_present)

            "Ты права":
                call MomDressComplaintYouAreRight(_mdc_girl, _mdc_real_name, _mdc_georgett_present)

            "Так я ей это платье и купил":
                call MomDressComplaintBoughtDress(_mdc_girl, KidsOrPregTmp, _mdc_real_name, _mdc_georgett_present)

            "Видел, тебе бы тоже не мешало так одеться":
                call MomDressComplaintSandraShouldDress(_mdc_girl, _mdc_real_name, _mdc_georgett_present)
    else:
        $ _mdc_intro_text = "Вы шли себе по своим делам, и пересеклись с Сандрой. Увидев вас та заметила: \"{}{}а наша совсем большая стала. Уже одевается, как взрослая, знает как себя подать. Смотри как на нее не то, что мальчишки всякие, а даже взрослые мужики у нас в трактире смотрят. Умничка!\"".format("Я уже про это говорила, но все таки " if TalkedBeforeTmp > 0 else "", GirlSillyName)
        "[_mdc_intro_text]"
        menu:
            "Да как ты можешь так про это говорить":
                call MomDressComplaintHowCanYouSayThat(_mdc_girl, _mdc_real_name, _mdc_georgett_present)

            "Так я ей это платье и купил":
                call MomDressComplaintBoughtDressHighSandra(_mdc_girl, KidsOrPregTmp, _mdc_real_name)
    return


label MomDressComplaintLikeIt(girl_name="", kids_or_preg=0, real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_girl", "_mdc_real_name", "_mdc_kids", "_mdc_follow_text")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_real_name = str(real_name or "").strip()
    $ _mdc_kids = int(kids_or_preg or 0)
    $ _mdc_follow_text = "\"Да ладно тебе, Сандра,\" попытались успокоить страсти вы. \"Что тут такого? Сейчас так модно, много девчонок так ходит. Да и посетителям приятней таких видеть, они же к нам отдыхать приходят. Это ее дело, в конце концов, как хочет, так и одевается.\"\n\n\"Ну ты и фрукт! Тебе пофигу значит, что {} стала одеваться как гулящая девка! И что ее лапают кто ни попадя тебе тоже получается плевать?".format(_mdc_real_name)
    if _mdc_kids > 0:
        if _mdc_kids == 2:
            $ _mdc_follow_text = str(_mdc_follow_text or "") + " И связи ее повадок с тем, что она уже байстрюка себе нагуляла ты тоже не видишь?\""
        else:
            $ _mdc_follow_text = str(_mdc_follow_text or "") + " И связи ее повадок с тем, что она уже пузо себе нагуляла ты тоже не видишь?\""
    else:
        $ _mdc_follow_text = str(_mdc_follow_text or "") + "\""
    $ slut_friends_increase("sandra", 8, 2, -1, 0, 0, 0)
    "[_mdc_follow_text]"
    menu:
        "Ага, пофигу":
            call MomDressComplaintLikeItDontCare

        "Может и не пофигу":
            call MomDressComplaintLikeItMaybeNot(_mdc_girl, _mdc_real_name, bool(georgett_present))
    return


label MomDressComplaintLikeItDontCare:
    $ scene_runtime.text = "\"Я уже сказал, как хочет, так и одевается! Не трогай ее!\" продолжали стоять на своем вы.\n\n\"Ну знаешь,\" гневно выдохнула Сандра, развернулась и ушла."
    $ scene_runtime.location_text = scene_runtime.text
    $ slut_friends_increase("sandra", 4, 1, -1, 0, 0, 0)
    jump MomDressComplaintFinish


label MomDressComplaintLikeItMaybeNot(girl_name="", real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_girl", "_mdc_tail")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), 2)
    $ scene_runtime.text = "\"Ну, может и не пофигу,\" сказали вы, убежденные логикой и аргументами Сандры. \"Я с ней поговорю.\"\n\n\"Мы поговорим. Сейчас.\" проявила жесткость Сандра.\n\nНичего не поделаешь, пришлось идти и говорить. Вернее слушать, как Сандра чуть ли не полчаса на повышенных тонах учила {} скромности и целомудренности и изредка поддакивать. В конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), str(real_name or ""), _mdc_tail)
    $ scene_runtime.location_text = scene_runtime.text
    jump MomDressComplaintFinish


label MomDressComplaintYouAreRight(girl_name="", real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_girl", "_mdc_tail")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), 2)
    $ scene_runtime.text = "\"Да, я тоже это заметил и мне это не понравилось.\"\n\n\"Так пошли же с ней поговорим. {} надо спасать.\"\n\nНичего не поделаешь, пришлось идти и говорить. Вернее слушать, как Сандра чуть ли не полчаса на повышенных тонах учила {} скромности и целомудренности и изредка поддакивать. В конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), str(real_name or ""), str(real_name or ""), _mdc_tail)
    $ scene_runtime.location_text = scene_runtime.text
    jump MomDressComplaintFinish


label MomDressComplaintBoughtDress(girl_name="", kids_or_preg=0, real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_girl", "_mdc_real_name", "_mdc_kids", "_mdc_body_part", "_mdc_follow_text")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_real_name = str(real_name or "").strip()
    $ _mdc_kids = int(kids_or_preg or 0)
    $ _mdc_body_part = "задницу" if procedural_randint(1, 2, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:procedural_randint:166:3") == 1 else "сиськи"
    $ _mdc_follow_text = "\"А чего бы не заметить-то?\" сказали вы глядя Сандре в глаза. \"Это ж я ей это платье и купил. Думаю оно ей идет. И посетителям нравится, смотри как они на ее {} пялятся.\"\n\n\"Ты, ты...\" потрясенно ответила вам Сандра. \"Значит ты покупаешь {} такие шмотки, чтобы на нее бухие мужики пялились и за задницу хватали?\"\n\n\"Ага,\" довольно ответили вы. \"Да ей и самой внимание приятно.\"\n\n\"И не стыдно тебе из нее блядь делать? Ты должен ее защищать!".format(_mdc_body_part, _mdc_real_name)
    if _mdc_kids > 0:
        if _mdc_kids == 2:
            $ _mdc_follow_text = str(_mdc_follow_text or "") + " Она ведь из-за твоего попустительства уже байстрюка себе нагуляла.\""
        else:
            $ _mdc_follow_text = str(_mdc_follow_text or "") + " Она ведь из-за твоего попустительства уже пузо себе нагуляла.\""
    else:
        $ _mdc_follow_text = str(_mdc_follow_text or "") + "\""
    "[_mdc_follow_text]"
    menu:
        "Может и стыдно":
            call MomDressComplaintBoughtDressMaybeAshamed(_mdc_girl, _mdc_real_name, bool(georgett_present))

        "Не, ни капельки":
            call MomDressComplaintBoughtDressNope
    return


label MomDressComplaintBoughtDressMaybeAshamed(girl_name="", real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_girl", "_mdc_tail")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), 2)
    $ scene_runtime.text = "\"Знаешь может я действительно погорячился,\" виновато сказали вы. \"Думал что если она себя свободней будет чувствовать, то это неплохо. Но наверное ты права. Я с ней поговорю.\"\n\n\"Вот мы вместе сейчас и поговорим.\" строго ответила Сандра.\n\nНичего не поделаешь, пришлось идти и говорить. Вернее слушать, как Сандра чуть ли не полчаса на повышенных тонах учила {} скромности и целомудренности и изредка поддакивать. В конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), str(real_name or ""), _mdc_tail)
    $ scene_runtime.location_text = scene_runtime.text
    jump MomDressComplaintFinish


label MomDressComplaintBoughtDressNope:
    $ scene_runtime.text = "\"Я уже все сказал, на мой взгляд она прекрасно одевается, не вижу проблемы!\" продолжали стоять на своем вы.\n\n\"Ну знаешь,\" гневно выдохнула Сандра, развернулась и ушла."
    $ scene_runtime.location_text = scene_runtime.text
    $ slut_friends_increase("sandra", 4, 1, -1, 35, 2, 1)
    jump MomDressComplaintFinish


label MomDressComplaintSandraShouldDress(girl_name="", real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_reacts", "_mdc_intro_text", "_mdc_drop_data")
    $ _mdc_reacts = (
        (mom_dress_corruption("sandra") >= 20 and procedural_randint(1, 4, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:procedural_randint:205:4") == 1)
        or (mom_dress_corruption("sandra") >= 38 and procedural_randint(1, 2, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:procedural_randint:206:5") == 1)
        or mom_dress_corruption("sandra") >= 47
    )
    $ _mdc_intro_text = "\"Конечно видел, и на мой взгляд, ее выбор гардероба получше твоего,\" нагло заявили вы.\n\n\"Что?!\" гневно воскликнула Сандра. \"Это ты о чем вообще?\"\n\n\"Ты прекрасно знаешь, о чем. У нас трактир, а не богадельня. Все работницы должны быть привлекательны собой. И одеты тоже привлекательно. Ты собой хороша,\" при этих словах Сандра слегка зарделась, \"а вот одеваешься излишне скромно. Если к нам никто ходить не будет, то мы все окажемся на улице, побираться будем. Да и вообще, ты после смерти мужа слегка зачахла, а ты ведь еще совсем не старая.\""
    if _mdc_reacts:
        $ scene_runtime.text = str(_mdc_intro_text or "") + "\n\nПри последних ваших словах Сандра вспыхнула: \"А это вообще не твое дело. Хотя может в чем-то ты и прав. {} получается думает о нашем общем деле, а я только о себе. Спасибо, что объяснил.\" и в раздумьях Сандра удалилась.".format(str(real_name or ""))
        $ slut_friends_increase("sandra", 12, 1, 1, 38, 1, 1)
    else:
        $ scene_runtime.text = str(_mdc_intro_text or "") + "\n\n\"Значит тебе не нравится, что Сандра у тебя не одевается как шлюха?!"
        if bool(georgett_present):
            $ scene_runtime.text = str(scene_runtime.text or "") + " По твоему я как Жоржетта твоя ненаглядная должна наряжаться? Пиздой всем светить?"
        $ scene_runtime.text = str(scene_runtime.text or "") + "\" в ярости начала орать на вас Сандра. \"Ты совсем с глузду съехал! Работай тут на него еще.\"\n\nВы молча стояли, не пытаясь уже что-то ответить. В конце концов орать Сандре надоело и она ушла."
        $ _mdc_drop_data = mom_dress_complaint_skill_drop_data()
        if int(_mdc_drop_data.get("drop_value", 0) or 0) > 0:
            $ Sandra.change_skill(str(_mdc_drop_data.get("prof_name", "") or "cooking"), -int(_mdc_drop_data.get("drop_value", 0) or 0))
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nОТ ПЕРЕНЕСЕННОЙ ОБИДЫ ЕЕ НАВЫКИ {} УПАЛИ НА {} {}".format(
                str(_mdc_drop_data.get("prof_desc", "") or ""),
                int(_mdc_drop_data.get("drop_value", 0) or 0),
                "ЕДИНИЦУ" if int(_mdc_drop_data.get("drop_value", 0) or 0) == 1 else "ЕДИНИЦЫ",
            )
        $ slut_friends_increase("sandra", 3, 1, -2, 21, 1, -3)
    $ scene_runtime.location_text = scene_runtime.text
    jump MomDressComplaintFinish


label MomDressComplaintHowCanYouSayThat(girl_name="", real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_girl", "_mdc_real_name", "_mdc_follow_text")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_real_name = str(real_name or "").strip()
    $ _mdc_follow_text = "\"Да ты что, Сандра?\" удивились вы. \"Она же как шлюха какая-то разоделась. Мне вообще кажется, что она и нижнее белье порой не пододевает."
    if bool(georgett_present):
        $ _mdc_follow_text = str(_mdc_follow_text or "") + " Зря я этим блядям, Жоржетте с Лизкой, у нас работать разрешил. К {} плохое быстро прилипает, вот она от Лизки думаю и научилась.\"".format(_mdc_real_name)
    else:
        $ _mdc_follow_text = str(_mdc_follow_text or "") + "\""
    $ _mdc_follow_text = str(_mdc_follow_text or "") + "\n\n\"Да ну, ты наговариваешь на нее,\" постаралась вас успокоить Сандра. \"Она уже взрослая, а ты все к ней как к малышке какой-то относишься.\""
    "[_mdc_follow_text]"
    menu:
        "Нет, не наговариваю, все так и есть":
            call MomDressComplaintHowCanYouSayThatInsist(_mdc_girl, _mdc_real_name, bool(georgett_present))

        "Может я погорячился":
            call MomDressComplaintHowCanYouSayThatBackOff
    return


label MomDressComplaintHowCanYouSayThatInsist(girl_name="", real_name="", georgett_present=False):
    $ renpy.dynamic("_mdc_girl", "_mdc_tail")
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), -1, True)
    $ scene_runtime.text = "\"Тебе может забота глаза застилает, а я вижу все как есть,\" ответили вы. \"Пойдем, поговорим с ней, нас двоих она должна послушать.\"\n\nСандре ничего не оставалось, как пойти за вами следом. Вы строго отчитали {}, научив ее уму разуму.".format(str(real_name or ""))
    if _mdc_girl == "amanda":
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nЗаодно вы {}запретили ей болтать с Лизеттой, источником грязи и разврата.".format("еще раз " if Amanda.var_int("prohibitliza", 0) else "")
        $ Amanda.set_var_int("prohibitliza", 1)
    $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВ конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), _mdc_tail)
    $ scene_runtime.location_text = scene_runtime.text
    jump MomDressComplaintFinish


label MomDressComplaintHowCanYouSayThatBackOff:
    $ scene_runtime.text = "\"Да, ты права, я чего-то слишком строг с ней. Все-таки я о ней слишком навязчиво забочусь.\"\n\n\"Стефан, все нормально, я и хотела бы чтобы ты о ней заботился, просто не будь слишком навязчивым.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ slut_friends_increase("sandra", 12, 2, 1, 0, 0, 0)
    jump MomDressComplaintFinish


label MomDressComplaintBoughtDressHighSandra(girl_name="", kids_or_preg=0, real_name=""):
    $ renpy.dynamic("_mdc_body_part", "_mdc_kids")
    $ _mdc_body_part = "задницу" if procedural_randint(1, 2, key="procedural:NPC/Girls/Common/MomDressComplaint.rpy:procedural_randint:275:6") == 1 else "сиськи"
    $ _mdc_kids = int(kids_or_preg or 0)
    $ scene_runtime.text = "\"Да, оно ей очень идет,\" отозвались вы. \"Это ж я ей этот наряд и купил. И посетителям нравится, смотри как они на ее {} пялятся. Даже щипают порой, вот как она им нравится.\"\n\n\"Ну, может это все-таки уже слишком,\" неуверенно ответила вам Сандра.\n\n\"Да ладно тебе, Сандра!".format(_mdc_body_part)
    if _mdc_kids > 0:
        if _mdc_kids == 2:
            $ scene_runtime.text = str(scene_runtime.text or "") + " Она ведь действительно взрослая, уже байстрюка успела себе нагулять.\""
        else:
            $ scene_runtime.text = str(scene_runtime.text or "") + " Она ведь действительно взрослая, уже пузо успела себе нагулять.\""
    else:
        $ scene_runtime.text = str(scene_runtime.text or "") + " Ты же сама говоришь, что она уже взрослая!\""
    $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n\"Ну, наверное ты прав. Я же вам только добра желаю, мне главное чтобы {}е больно никто не сделал. Но если ей нравится, то что ж в этом плохого?\"\n\n\"Нравится-нравится,\" заверили Сандру вы.".format("Амандочк" if str(girl_name or "").strip().lower() == "amanda" else "Меллисочк")
    $ scene_runtime.location_text = scene_runtime.text
    $ slut_friends_increase("sandra", 14, 2, 1, 68, 1, 1)
    jump MomDressComplaintFinish


label MomDressComplaintFinish:
    "[scene_runtime.text]"
    menu:
        "Вернуться к делам":
            $ main_ui_end_native_scene_state()
            return
