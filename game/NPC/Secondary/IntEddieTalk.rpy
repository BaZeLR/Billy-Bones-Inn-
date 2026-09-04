# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

label IntEddieTalk:
    $ renpy.dynamic("_eddie_name", "_eddie_talk_new", "_eddie_picture", "_eddie_talk_count")
    $ Eddie.mark_known()
    $ Becky.update()
    $ _eddie_name = "eddie"
    $ Eddie.update()
    $ _eddie_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != "eddie"
    $ main_ui_begin_talk_state("Разговор с Эдди", _eddie_name)
    if _eddie_talk_new:
        if str(rooms.current_code or "") == "GroceryStore":
            vscene grocery_store_grocer_picture("eddie")
        else:
            $ _eddie_picture = str(Eddie.data.portrait or "images/eddie/portraits/portrait_0.png")
            if str(_eddie_picture or "").strip():
                vscene _eddie_picture
    if _eddie_talk_new:
        $ scene_runtime.text = eddie_talk_intro_text()
        $ scene_runtime.location_text = scene_runtime.text

    while True:
        menu:
            "Поболтать с Эдди о разной фигне.":
                call IntEddieTalkSmalltalk
            "Поболтать с Эдди о личных вещах." if eddie_talk_can_personal(_eddie_name):
                call IntEddieTalkPersonal
            "Рассказать Эдди о том, что у вас теперь работают девочки." if eddie_talk_can_whores(_eddie_name):
                call IntEddieTalkWhores
            "Поинтересоваться у Эдди как ему ваши девочки." if eddie_talk_can_girls(_eddie_name):
                call IntEddieTalkGirls
            "Предложить помочь подкатится к хозяйке лавки." if eddie_talk_can_mom_helper(_eddie_name):
                if story_event_available("talk_eddie", "becky_eddie_sex"):
                    call checkTriggers("talk_eddie", "becky_eddie_sex", 0)
                else:
                    call IntEddieTalkMomHelper
            "Спросить о синяке." if eddie_talk_can_bruise(_eddie_name):
                call IntEddieTalkBruise
            "А все таки расскажи, кто это тебе так вмазал?" if eddie_talk_can_who_hit(_eddie_name):
                call IntEddieTalkWhoHit
            "А куда это ты ездил?" if eddie_talk_can_destination(_eddie_name):
                call IntEddieTalkDestination
            "Страже жаловался?" if eddie_talk_can_complain(_eddie_name):
                call IntEddieTalkComplain
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return


label IntEddieTalkSmalltalk:
    $ renpy.dynamic("_eddie_talk_count")
    $ _eddie_talk_count = int(Eddie.talked_today or 0)
    $ scene_runtime.text = "Вы некоторое время болтаете с Эдди о несущественных вещах."
    if _eddie_talk_count <= 2 and procedural_randint(1, 2, "eddie_smalltalk_%s_%s" % (current_game_day(), _eddie_talk_count)) == 1 and int(Eddie.rel or 0) <= 5:
        $ scene_runtime.text += "\n\nВы немного сдружились с Эдди."
        $ Eddie.change_social(friend_delta=1)
    elif _eddie_talk_count > 2:
        $ scene_runtime.text += "\n\nНичего нового из разговора вы не узнали."
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkPersonal:
    $ renpy.dynamic("_eddie_talk_count")
    $ _eddie_talk_count = int(Eddie.talked_today or 0)
    $ scene_runtime.text = "Вы некоторое время болтаете с Эдди о том, кто сколько выпил и о том, какие девушки кому нравятся."
    if _eddie_talk_count <= 2 and procedural_randint(1, 2, "eddie_personal_%s_%s" % (current_game_day(), _eddie_talk_count)) == 1 and int(Eddie.rel or 0) <= 10:
        $ scene_runtime.text += "\n\nВы немного сдружились с Эдди."
        $ Eddie.change_social(friend_delta=1)
    elif _eddie_talk_count > 2:
        $ scene_runtime.text += "\n\nНичего нового из разговора вы не узнали."
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkWhores:
    $ scene_runtime.text = "Вы как бы между делом замечаете, что у вас теперь работают девочки не самого тяжелого поведения. Глаза рыжего Эдди загораются, хотя на словах он никак не показывает своей заинтересованности. Вернее, он старательно показывает что ему пофигу."
    $ Eddie.change_social(friend_delta=1)
    $ Eddie.told_about_tavern_whores = True
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkGirls:
    $ scene_runtime.text = "Ведя общий разговор вы неожиданно спрашиваете Эдди, как ему Жоржетта. Эдди густо краснеет, запинается, но все таки отмечает, что она очень даже ничего. При этом парень вас внимательно изучает, как бы пытаясь понять что вам известно. Вы делаете безразличный вид и переводите разговор на другую тему."
    vscene "images/eddie/portraits/surprised.png"
    $ Eddie.change_social(friend_delta=1)
    $ Eddie.talked_about_georgett = True
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkMomHelper:
    $ Becky.update()
    if int(threads["beckyEddieSex"].num or 0) == 0:
        $ scene_runtime.text = "\"Эй, Эдди, я прекрасно знаю чего тебе хочется,\" сказали вы юному бакалейщику. \"Думаешь я не видел, какие ты взгляды на хозяйку лавки кидаешь? Или не знаю в какие ты игры с Жоржеттой играешься?\""
        if int(Eddie.rel or 0) < 9:
            $ scene_runtime.text += "\n\n\"Не понимаю, мастер Стефан, о чем это вы,\" ответил вам Эдди слегка покраснев. Все ваши дальнейшие попытки разговорить его упирались в стену молчания. Судя по всему он вас плохо знает и не доверяет."
        else:
            $ scene_runtime.text += "\n\n\"Это мое дело\", буркнул парень, \"и тебя оно не касается.\" \"Зря ты так,\" вы отнюдь не обиделись на данный им отпор, \"я же помочь тебе хочу. Слушай, когда я в следующий раз после ужина пойду с твоей хозяйкой в спальню, я оставлю дверь открытой. Ты подожди пару минут и заходи. Бекки сама тебя хочет, только решиться не может.\""
            $ scene_runtime.text += "\n\n\"Правда что ли?\" глаза Эдди стали как плошки."
            $ scene_runtime.text += "\n\n\"Точно тебе говорю,\" заверили наивного юношу вы."
            $ scene_runtime.text += "\n\n\"Ну спасибо тебе, не ожидал.\""
            $ event_runtime.active_thread.advance()
        vscene "images/eddie/portraits/surprised.png"
    elif int(threads["beckyEddieSex"].num or 0) in [2, 3]:
        $ scene_runtime.text = "\"Эй Эдди, насчет прошлого раза,\" начали вы свою речь."
        if int(Eddie.rel or 0) < 10:
            $ scene_runtime.text += "\n\n\"Да пошел ты,\" ответил вам Эдди, с ненавистью глядя на вас, \"куда подальше. Не поддамся я еще раз на твое издевательство.\""
            $ scene_runtime.text += "\n\nС этими словами бакалейщик отвернулся и на дальнейшие попытки завязать разговор не реагировал."
        elif Becky.eddie_join_failures > 2:
            $ scene_runtime.text += "\n\n\"Да пошел ты,\" ответил вам Эдди, с ненавистью глядя на вас, \"куда подальше. Со своими подколками. Несколько раз тебе верил, но теперь все, в очередной раз ты меня больше не надуешь.\""
            $ scene_runtime.text += "\n\nС этими словами бакалейщик отвернулся и на дальнейшие попытки завязать разговор не реагировал."
        else:
            $ scene_runtime.text += "\n\n\"Это ты поиздеваться решил надо мной, да?\" ответил вам Эдди смерив вас тяжелым недобрым взглядом."
            if int(threads["beckyEddieSex"].num or 0) == 3:
                $ scene_runtime.text += "\n\n\"Я сделал все так, как ты сказал, а дверь была заперта.\""
                $ scene_runtime.text += "\n\n\"Эээ, извини, я просто забыл засов отодвинуть, в следующий раз обязательно открою, это я не специально.\" заверили вы своего нового друга."
            else:
                $ scene_runtime.text += "\n\n\"Ты говорил, что она сама хочет, а она меня выкинула из комнаты, обозвала подонком и извращенцем и весь день со мной не разговаривала.\""
                $ scene_runtime.text += "\n\n\"Эээ, даже не знаю, что на нее нашло, но я все уладил, все обговорил. Попробуй еще раз зайти, все будет классно, не дрейфь!\" заверили вы своего нового друга."
            $ scene_runtime.text += "\n\n\"Правда что ли?\""
            $ scene_runtime.text += "\n\n\"Точно тебе говорю\""
            $ scene_runtime.text += "\n\n\"Ну ладно, а я уж подумал было...\""
            $ event_runtime.active_thread.advanceTo(1, force_active=True)
        vscene "images/eddie/portraits/surprised.png"
    elif int(threads["beckyEddieSex"].num or 0) >= 4 and not threads["beckyEddieSex"].completed:
        $ scene_runtime.text = "\"И как тебе ночка с хозяйкой лавки?\" подмигнули вы Эдди, делая рукой неприличный жест."
        $ scene_runtime.text += "\n\n\"Ух, классно, спасибо тебе Стефан, ты настоящий друг. Госпожа Блэнкеншип сказала, что теперь я каждый день могу ее трахать, и даже спать с ней иногда,\" сказал Эдди с блаженной улобкой на лице."
        $ scene_runtime.text += "\n\n\"Но и ты, конечно, всегда будешь желанным гостем в нашем доме,\" быстро поправился он."
    else:
        $ scene_runtime.text = "\"И как у тебя идут дела с твоей сисястой начальницей?\" цинично поинтересовались вы у Эдди."
        $ scene_runtime.text += "\n\n\"Благодаря тебе, Стефан, более чем хорошо,\" довольно ответил тот."
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkBruise:
    $ Becky.update()
    $ scene_runtime.text = "\"Слышь, а где это тебя отоварили?\" спросили вы Эдди."
    $ scene_runtime.text += "\n\n\"Да этого, того в общем не с теми связался.\""
    $ scene_runtime.text += "\n\n\"С кем это, не с теми?\" решили уточнить вы."
    $ scene_runtime.text += "\n\n\"Ну не с теми значит не с теми. Мое дело. И вообще, Бекки не велела говорить,\" отбрехался ваш знакомый."
    $ Becky.sherwood_suspicion += 1
    $ Eddie.fingal_talk_stage = 1
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkWhoHit:
    $ Becky.update()
    if threads["beckyEddieSex"].completed and int(Eddie.rel or 0) >= 9:
        $ scene_runtime.text = "\"Знаешь, ты мне удружил, и мою хозяйку мы с тобой классно оттрахали. Врядли бы она мне дала, если бы не ты. Так что скажу, хоть она и не велела. Только ты меня не запали, хорошо? В общем меня уроды эти, из Шервудского леса, отмудохали. Обычно нормально можно было проехать, дашь им пару десятков монет и едешь себе. А надысь еду - только их встретил так мне сразу в табло засветили. Хоть бы объяснили, за что. Деньги отобрали, лошадь забрали. Вот пидорасы!\""
        $ Becky.sherwood_suspicion += 10
        $ Eddie.fingal_talk_stage = 2
        $ Becky.knows_blackwood = True
    else:
        $ scene_runtime.text = "\"Я тебе уже все что хотел сказал. Мало того, что огреб, так еще ты тут с распросами дурацкими. Кто ты такой, что мне вопросы задавать?\" отбрил вас Эдди."
        if int(Eddie.rel or 0) >= 5:
            $ Eddie.change_social(friend_delta=-procedural_randint(0, 1, "eddie_who_hit_rel_%s_%s" % (current_game_day(), int(Eddie.talked_today or 0))))
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkDestination:
    $ scene_runtime.text = "\"По делам. Я и так уже слишком много тебе рассказал.\""
    $ Eddie.asked_fingal_destination = True
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntEddieTalkComplain:
    $ scene_runtime.text = "\"Ну ты шутник,\" развеселился Эдди. \"Я чего, дурак? Денег они слупят, типа за хлопоты, но вряд ли будут связываться. Тем более, что сам Циммерман раньше трепался, что мол ентот лес ничейный, и никого они там ловить не обязанны.\""
    $ Eddie.asked_fingal_guard_complaint = True
    $ Eddie.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return
