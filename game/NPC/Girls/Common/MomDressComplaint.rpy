# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import random as _mom_dress_random

    def mom_dress_complaint_kids_or_preg(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if int(kids.get(girl, 0) or 0) > 0:
            return 2
        if int(pregnancy.get(girl, 0) or 0) > 150:
            return 1
        return 0

    def mom_dress_complaint_mark_seen(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        girl_var_name = "%sVar" % girl.capitalize()
        girl_var = getattr(renpy.store, girl_var_name, None)
        if not isinstance(girl_var, dict):
            girl_var = {}
            setattr(renpy.store, girl_var_name, girl_var)
        seen_before = int(girl_var.get("MomDressComplaint", 0) or 0)
        girl_var["MomDressComplaint"] = seen_before + 1
        return seen_before

    def mom_dress_complaint_scold_tail(girl_name="", georgett_present=False, strict_callout=False):
        girl = str(girl_name or "").strip().lower()
        rebellious = (
            int(sluttiness.get(girl, 0) or 0) >= 60
            or (int(sluttiness.get(girl, 0) or 0) >= 45 and _mom_dress_random.randint(1, 2) == 1)
            or (int(sluttiness.get(girl, 0) or 0) >= 35 and _mom_dress_random.randint(1, 4) == 1)
        )
        if rebellious:
            slut_friends_increase(girl, 5, 1, -2, 65, 1, 2)
            if bool(strict_callout) and bool(georgett_present):
                return "прокричав напоследок, что вы бы лучше на себя сначала посмотрели, как вам со шлюхами путаться так все нормально, а как ей чуть-чуть понаряднее платье одеть - так уже трагедия."
            return "прокричав напоследок, что вы ей не указ и она лучше знает как ей себя вести."

        if bool(georgett_present) and girl == "amanda":
            AmandaVar["prohibitliza"] = 1
            tail = "пообещав напоследок что будет себя скромнее вести и не будет больше болтать с Лизеттой."
        else:
            tail = "пообещав напоследок что будет себя скромнее вести и одеваться."
        slut_friends_increase(girl, 5, 1, -1, 25, 1, -2)
        return tail

    def mom_dress_complaint_finish_scold(girl_name="", georgett_present=False, sandra_friend_delta=2, strict_callout=False):
        tail = mom_dress_complaint_scold_tail(girl_name, georgett_present, strict_callout)
        slut_friends_increase("sandra", 15, 1, sandra_friend_delta, 30, 1, -1)
        return tail

    def mom_dress_complaint_return_items():
        return [MenuItem("Вернуться к делам", Jump("TavernMain"))]

    def mom_dress_complaint_skill_drop_data():
        prof_choice = renpy.random.randint(1, 3)
        prof_name = "cooking" if prof_choice == 1 else ("cleaning" if prof_choice == 2 else "waitress")
        prof_desc = "ГОТОВКИ" if prof_name == "cooking" else ("УБОРКИ" if prof_name == "cleaning" else "ОФИЦИАНТКИ")
        current_value = max(0, int(getattr(renpy.store, prof_name).get("sandra", 0) or 0))
        drop_value = max(0, min(renpy.random.randint(0, 3), current_value - 10))
        return {
            "prof_name": prof_name,
            "prof_desc": prof_desc,
            "drop_value": drop_value,
        }


label MomDressComplaint(girl_name):
    $ _mdc_girl = str(girl_name or "").strip().lower()
    if _mdc_girl == "":
        return

    $ GirlSillyName = "Амандочк" if _mdc_girl == "amanda" else "Меллисочк"
    $ TalkedBeforeTmp = mom_dress_complaint_mark_seen(_mdc_girl)
    $ KidsOrPregTmp = mom_dress_complaint_kids_or_preg(_mdc_girl)
    $ _mdc_real_name = RealName.get(_mdc_girl, _mdc_girl)
    $ _mdc_georgett_present = str(getLocation("georgett") or "") == "TavernMain"
    hide screen main_ui
    $ main_ui_begin_native_scene_state("Разговор с Сандрой")
    $ TavernMainBlockEvents = 1
    if renpy.loadable("images/sandra/tavern/cleaning1.jpg"):
        $ _layout_last_picture = "images/sandra/tavern/cleaning1.jpg"
    elif renpy.loadable("images/tavern/mainhall/tavern_crew.jpg"):
        $ _layout_last_picture = "images/tavern/mainhall/tavern_crew.jpg"
    if sluttiness.get("sandra", 0) < 50:
        $ _mdc_intro_text = "Вы мирно и спокойно шли по своим делам, когда вас вдруг остановила Сандра: \"Стефан, мне надо с тобой поговорить.\"\n\nОтведя вас в сторонку, она продолжила: \"{}Ты видел как {} вырядилась? Как блядь последняя, извини за выражение! Сиськи практически наружу, подол короче некуда! Мне порой кажется, что она и нижнего белья-то не надевает!\"".format("Я знаю, мы уже про это говорили, но не могу дальше молчать. " if TalkedBeforeTmp > 0 else "", _mdc_real_name)
        if _mdc_georgett_present:
            $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nЭто все от Жоржи с Лизкой идет! Стефан, я конечно понимаю, что от этих шлюх нам доходик капает, но ты посмотри, как они на нашу {}у влияют!".format(GirlSillyName)
            if _mdc_girl == "amanda" and AmandaVar.get("prohibitliza", 0):
                $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nТы хоть и запретил Аманде с Лизкой трепаться, но ты ж ее знаешь, она сама лучше всех все знает! Я уже несколько раз видела, как Аманда плевала на все запреты и с этой профурсеткой болтала."
            else:
                $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nКак не посмотрю, она с Лизкой все время о чем-то шушукается!"
            $ _mdc_intro_text = str(_mdc_intro_text or "") + "\n\nИ вот результат!"
        $ _mdc_intro_items = [
            MenuItem("А чо такого? Мне нравится", Call("MomDressComplaintLikeIt", _mdc_girl, KidsOrPregTmp, _mdc_real_name, _mdc_georgett_present)),
            MenuItem("Ты права", Call("MomDressComplaintYouAreRight", _mdc_girl, _mdc_real_name, _mdc_georgett_present)),
            MenuItem("Так я ей это платье и купил", Call("MomDressComplaintBoughtDress", _mdc_girl, KidsOrPregTmp, _mdc_real_name, _mdc_georgett_present)),
            MenuItem("Видел, тебе бы тоже не мешало так одеться", Call("MomDressComplaintSandraShouldDress", _mdc_girl, _mdc_real_name, _mdc_georgett_present)),
        ]
        call QueuePagedPanelText(_mdc_intro_text, "Что ответить Сандре?", _mdc_intro_items, "plain")
    else:
        $ _mdc_intro_text = "Вы шли себе по своим делам, и пересеклись с Сандрой. Увидев вас та заметила: \"{}{}а наша совсем большая стала. Уже одевается, как взрослая, знает как себя подать. Смотри как на нее не то, что мальчишки всякие, а даже взрослые мужики у нас в трактире смотрят. Умничка!\"".format("Я уже про это говорила, но все таки " if TalkedBeforeTmp > 0 else "", GirlSillyName)
        $ _mdc_intro_items = [
            MenuItem("Да как ты можешь так про это говорить", Call("MomDressComplaintHowCanYouSayThat", _mdc_girl, _mdc_real_name, _mdc_georgett_present)),
            MenuItem("Так я ей это платье и купил", Call("MomDressComplaintBoughtDressHighSandra", _mdc_girl, KidsOrPregTmp, _mdc_real_name)),
        ]
        call QueuePagedPanelText(_mdc_intro_text, "Что ответить Сандре?", _mdc_intro_items, "plain")
    call ReturnToMainUI
    return


label MomDressComplaintLikeIt(girl_name="", kids_or_preg=0, real_name="", georgett_present=False):
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
    $ _mdc_follow_items = [
        MenuItem("Ага, пофигу", Call("MomDressComplaintLikeItDontCare")),
        MenuItem("Может и не пофигу", Call("MomDressComplaintLikeItMaybeNot", _mdc_girl, _mdc_real_name, bool(georgett_present))),
    ]
    call QueuePagedPanelText(_mdc_follow_text, "Что ответить дальше?", _mdc_follow_items, "plain")
    call ReturnToMainUI
    return


label MomDressComplaintLikeItDontCare:
    $ MainTxt = "\"Я уже сказал, как хочет, так и одевается! Не трогай ее!\" продолжали стоять на своем вы.\n\n\"Ну знаешь,\" гневно выдохнула Сандра, развернулась и ушла."
    $ CurLocDesc = MainTxt
    $ slut_friends_increase("sandra", 4, 1, -1, 0, 0, 0)
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintLikeItMaybeNot(girl_name="", real_name="", georgett_present=False):
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), 2)
    $ MainTxt = "\"Ну, может и не пофигу,\" сказали вы, убежденные логикой и аргументами Сандры. \"Я с ней поговорю.\"\n\n\"Мы поговорим. Сейчас.\" проявила жесткость Сандра.\n\nНичего не поделаешь, пришлось идти и говорить. Вернее слушать, как Сандра чуть ли не полчаса на повышенных тонах учила {} скромности и целомудренности и изредка поддакивать. В конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), str(real_name or ""), _mdc_tail)
    $ CurLocDesc = MainTxt
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintYouAreRight(girl_name="", real_name="", georgett_present=False):
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), 2)
    $ MainTxt = "\"Да, я тоже это заметил и мне это не понравилось.\"\n\n\"Так пошли же с ней поговорим. {} надо спасать.\"\n\nНичего не поделаешь, пришлось идти и говорить. Вернее слушать, как Сандра чуть ли не полчаса на повышенных тонах учила {} скромности и целомудренности и изредка поддакивать. В конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), str(real_name or ""), str(real_name or ""), _mdc_tail)
    $ CurLocDesc = MainTxt
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintBoughtDress(girl_name="", kids_or_preg=0, real_name="", georgett_present=False):
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_real_name = str(real_name or "").strip()
    $ _mdc_kids = int(kids_or_preg or 0)
    $ _mdc_body_part = "задницу" if renpy.random.randint(1, 2) == 1 else "сиськи"
    $ _mdc_follow_text = "\"А чего бы не заметить-то?\" сказали вы глядя Сандре в глаза. \"Это ж я ей это платье и купил. Думаю оно ей идет. И посетителям нравится, смотри как они на ее {} пялятся.\"\n\n\"Ты, ты...\" потрясенно ответила вам Сандра. \"Значит ты покупаешь {} такие шмотки, чтобы на нее бухие мужики пялились и за задницу хватали?\"\n\n\"Ага,\" довольно ответили вы. \"Да ей и самой внимание приятно.\"\n\n\"И не стыдно тебе из нее блядь делать? Ты должен ее защищать!".format(_mdc_body_part, _mdc_real_name)
    if _mdc_kids > 0:
        if _mdc_kids == 2:
            $ _mdc_follow_text = str(_mdc_follow_text or "") + " Она ведь из-за твоего попустительства уже байстрюка себе нагуляла.\""
        else:
            $ _mdc_follow_text = str(_mdc_follow_text or "") + " Она ведь из-за твоего попустительства уже пузо себе нагуляла.\""
    else:
        $ _mdc_follow_text = str(_mdc_follow_text or "") + "\""
    $ _mdc_follow_items = [
        MenuItem("Может и стыдно", Call("MomDressComplaintBoughtDressMaybeAshamed", _mdc_girl, _mdc_real_name, bool(georgett_present))),
        MenuItem("Не, ни капельки", Call("MomDressComplaintBoughtDressNope")),
    ]
    call QueuePagedPanelText(_mdc_follow_text, "Что ответить дальше?", _mdc_follow_items, "plain")
    call ReturnToMainUI
    return


label MomDressComplaintBoughtDressMaybeAshamed(girl_name="", real_name="", georgett_present=False):
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), 2)
    $ MainTxt = "\"Знаешь может я действительно погорячился,\" виновато сказали вы. \"Думал что если она себя свободней будет чувствовать, то это неплохо. Но наверное ты права. Я с ней поговорю.\"\n\n\"Вот мы вместе сейчас и поговорим.\" строго ответила Сандра.\n\nНичего не поделаешь, пришлось идти и говорить. Вернее слушать, как Сандра чуть ли не полчаса на повышенных тонах учила {} скромности и целомудренности и изредка поддакивать. В конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), str(real_name or ""), _mdc_tail)
    $ CurLocDesc = MainTxt
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintBoughtDressNope:
    $ MainTxt = "\"Я уже все сказал, на мой взгляд она прекрасно одевается, не вижу проблемы!\" продолжали стоять на своем вы.\n\n\"Ну знаешь,\" гневно выдохнула Сандра, развернулась и ушла."
    $ CurLocDesc = MainTxt
    $ slut_friends_increase("sandra", 4, 1, -1, 35, 2, 1)
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintSandraShouldDress(girl_name="", real_name="", georgett_present=False):
    $ _mdc_reacts = (
        (sluttiness.get("sandra", 0) >= 20 and renpy.random.randint(1, 4) == 1)
        or (sluttiness.get("sandra", 0) >= 38 and renpy.random.randint(1, 2) == 1)
        or sluttiness.get("sandra", 0) >= 47
    )
    $ _mdc_intro_text = "\"Конечно видел, и на мой взгляд, ее выбор гардероба получше твоего,\" нагло заявили вы.\n\n\"Что?!\" гневно воскликнула Сандра. \"Это ты о чем вообще?\"\n\n\"Ты прекрасно знаешь, о чем. У нас трактир, а не богадельня. Все работницы должны быть привлекательны собой. И одеты тоже привлекательно. Ты собой хороша,\" при этих словах Сандра слегка зарделась, \"а вот одеваешься излишне скромно. Если к нам никто ходить не будет, то мы все окажемся на улице, побираться будем. Да и вообще, ты после смерти мужа слегка зачахла, а ты ведь еще совсем не старая.\""
    if _mdc_reacts:
        $ MainTxt = str(_mdc_intro_text or "") + "\n\nПри последних ваших словах Сандра вспыхнула: \"А это вообще не твое дело. Хотя может в чем-то ты и прав. {} получается думает о нашем общем деле, а я только о себе. Спасибо, что объяснил.\" и в раздумьях Сандра удалилась.".format(str(real_name or ""))
        $ slut_friends_increase("sandra", 12, 1, 1, 38, 1, 1)
    else:
        $ MainTxt = str(_mdc_intro_text or "") + "\n\n\"Значит тебе не нравится, что Сандра у тебя не одевается как шлюха?!"
        if bool(georgett_present):
            $ MainTxt = str(MainTxt or "") + " По твоему я как Жоржетта твоя ненаглядная должна наряжаться? Пиздой всем светить?"
        $ MainTxt = str(MainTxt or "") + "\" в ярости начала орать на вас Сандра. \"Ты совсем с глузду съехал! Работай тут на него еще.\"\n\nВы молча стояли, не пытаясь уже что-то ответить. В конце концов орать Сандре надоело и она ушла."
        $ _mdc_drop_data = mom_dress_complaint_skill_drop_data()
        if int(_mdc_drop_data.get("drop_value", 0) or 0) > 0:
            $ getattr(renpy.store, str(_mdc_drop_data.get("prof_name", "") or "cooking"))["sandra"] -= int(_mdc_drop_data.get("drop_value", 0) or 0)
            $ MainTxt = str(MainTxt or "") + "\n\nОТ ПЕРЕНЕСЕННОЙ ОБИДЫ ЕЕ НАВЫКИ {} УПАЛИ НА {} {}".format(
                str(_mdc_drop_data.get("prof_desc", "") or ""),
                int(_mdc_drop_data.get("drop_value", 0) or 0),
                "ЕДИНИЦУ" if int(_mdc_drop_data.get("drop_value", 0) or 0) == 1 else "ЕДИНИЦЫ",
            )
        $ slut_friends_increase("sandra", 3, 1, -2, 21, 1, -3)
    $ CurLocDesc = MainTxt
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintHowCanYouSayThat(girl_name="", real_name="", georgett_present=False):
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_real_name = str(real_name or "").strip()
    $ _mdc_follow_text = "\"Да ты что, Сандра?\" удивились вы. \"Она же как шлюха какая-то разоделась. Мне вообще кажется, что она и нижнее белье порой не пододевает."
    if bool(georgett_present):
        $ _mdc_follow_text = str(_mdc_follow_text or "") + " Зря я этим блядям, Жоржетте с Лизкой, у нас работать разрешил. К {} плохое быстро прилипает, вот она от Лизки думаю и научилась.\"".format(_mdc_real_name)
    else:
        $ _mdc_follow_text = str(_mdc_follow_text or "") + "\""
    $ _mdc_follow_text = str(_mdc_follow_text or "") + "\n\n\"Да ну, ты наговариваешь на нее,\" постаралась вас успокоить Сандра. \"Она уже взрослая, а ты все к ней как к малышке какой-то относишься.\""
    $ _mdc_follow_items = [
        MenuItem("Нет, не наговариваю, все так и есть", Call("MomDressComplaintHowCanYouSayThatInsist", _mdc_girl, _mdc_real_name, bool(georgett_present))),
        MenuItem("Может я погорячился", Call("MomDressComplaintHowCanYouSayThatBackOff")),
    ]
    call QueuePagedPanelText(_mdc_follow_text, "Что ответить дальше?", _mdc_follow_items, "plain")
    call ReturnToMainUI
    return


label MomDressComplaintHowCanYouSayThatInsist(girl_name="", real_name="", georgett_present=False):
    $ _mdc_girl = str(girl_name or "").strip().lower()
    $ _mdc_tail = mom_dress_complaint_finish_scold(_mdc_girl, bool(georgett_present), -1, True)
    $ MainTxt = "\"Тебе может забота глаза застилает, а я вижу все как есть,\" ответили вы. \"Пойдем, поговорим с ней, нас двоих она должна послушать.\"\n\nСандре ничего не оставалось, как пойти за вами следом. Вы строго отчитали {}, научив ее уму разуму.".format(str(real_name or ""))
    if _mdc_girl == "amanda":
        $ MainTxt = str(MainTxt or "") + "\n\nЗаодно вы {}запретили ей болтать с Лизеттой, источником грязи и разврата.".format("еще раз " if AmandaVar.get("prohibitliza", 0) else "")
        $ AmandaVar["prohibitliza"] = 1
    $ MainTxt = str(MainTxt or "") + "\n\nВ конце концов {} расплакалась и убежала, {}".format(str(real_name or ""), _mdc_tail)
    $ CurLocDesc = MainTxt
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintHowCanYouSayThatBackOff:
    $ MainTxt = "\"Да, ты права, я чего-то слишком строг с ней. Все-таки я о ней слишком навязчиво забочусь.\"\n\n\"Стефан, все нормально, я и хотела бы чтобы ты о ней заботился, просто не будь слишком навязчивым.\""
    $ CurLocDesc = MainTxt
    $ slut_friends_increase("sandra", 12, 2, 1, 0, 0, 0)
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return


label MomDressComplaintBoughtDressHighSandra(girl_name="", kids_or_preg=0, real_name=""):
    $ _mdc_body_part = "задницу" if renpy.random.randint(1, 2) == 1 else "сиськи"
    $ _mdc_kids = int(kids_or_preg or 0)
    $ MainTxt = "\"Да, оно ей очень идет,\" отозвались вы. \"Это ж я ей этот наряд и купил. И посетителям нравится, смотри как они на ее {} пялятся. Даже щипают порой, вот как она им нравится.\"\n\n\"Ну, может это все-таки уже слишком,\" неуверенно ответила вам Сандра.\n\n\"Да ладно тебе, Сандра!".format(_mdc_body_part)
    if _mdc_kids > 0:
        if _mdc_kids == 2:
            $ MainTxt = str(MainTxt or "") + " Она ведь действительно взрослая, уже байстрюка успела себе нагулять.\""
        else:
            $ MainTxt = str(MainTxt or "") + " Она ведь действительно взрослая, уже пузо успела себе нагулять.\""
    else:
        $ MainTxt = str(MainTxt or "") + " Ты же сама говоришь, что она уже взрослая!\""
    $ MainTxt = str(MainTxt or "") + "\n\n\"Ну, наверное ты прав. Я же вам только добра желаю, мне главное чтобы {}е больно никто не сделал. Но если ей нравится, то что ж в этом плохого?\"\n\n\"Нравится-нравится,\" заверили Сандру вы.".format("Амандочк" if str(girl_name or "").strip().lower() == "amanda" else "Меллисочк")
    $ CurLocDesc = MainTxt
    $ slut_friends_increase("sandra", 14, 2, 1, 68, 1, 1)
    call QueuePagedPanelText(MainTxt, "Ваши действия", mom_dress_complaint_return_items(), "plain")
    call ReturnToMainUI
    return
