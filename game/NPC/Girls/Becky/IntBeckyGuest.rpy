# ================================================================================
# Becky dinner guest scene.
# Label owns scene text, direct menu choices, state mutation, and flow.
# ================================================================================

label IntBeckyGuest:
    show screen main_ui
    $ dinnertime = 0
    $ dinnerbecky = 0
    $ dinnerbeckyorgasm = 0
    $ dinneringaminet = 0
    $ georgedinnersex = 0
    $ GirlName = "becky"
    $ scene_image = "images/becky/dinner/DinnerStart.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image

    while True:
        if dinnertime > 6 or georgedinnersex != 0:
            return

        menu:
            "Осмотреть Ребекку" if dinnertime <= 5:
                call GirlsDesc("becky")

            "Осмотреть Ингенборг" if dinnertime <= 5:
                call GirlsDesc("inga")

            "Выставить на стол вино и еду из вашего трактира" if dinnertime == 0 and winenum >= 30 and productnum >= 30 and Inga.var_int("Knowher", 0) >= 2:
                "Вы решили, что столоваться на шару у хлебосольной вдовы хотя и безусловно вкусно и питательно, но пора и честь знать."
                "Мучимый уколами совести, вы принесли с собой кувшинчик красненького из запасов вашего заведения и разные закуски, завернутые в тряпицу. Благо этого добра у вас было все равно с избытком."
                "Если закуски смотрелись на фоне угощений вдовы немного бледно, если даже не сказать жалко, то вино явно пришлось по вкусу присутствующим. Лукас с Эдди сразу жахнули по стакану."
                if Becky.can_drink_wine():
                    "Вместе с ними накатила и вдовушка, ее лицо сразу раскраснелось от принятого, а настроение улучшилось."
                    $ Becky.drunk = 1
                else:
                    "Бекки же от вина воздержалась, лишь слегка пригубив свой бокал."
                if pregnancy.get("inga", 0) <= 30:
                    "Ингенборг, игнорируя укоризненный взгляд своей мамочки, тоже налила себе стакан и подняла тост за здоровье всех присутствующих."
                    $ Inga.drunk = 1
                else:
                    "Инга отодвинула предложенный ей стакан, заметив что ей и так весело, да и дури у нее своей хватает, поэтому она разве что для запаха может чуток выпить."
                $ Becky.apply_social_roll(11, 1, 2, 0, 0, 0)
                $ winenum -= 5
                $ productnum -= 5
                $ dinnertime += 1
                call stat
                $ scene_image = "images/becky/dinner/tabledrink.jpg"
                $ _layout_last_picture = scene_image
                vscene scene_image

            "Кушать" if dinnertime <= 5 and georgedinnersex == 0:
                if dinnerbecky > 0:
                    $ dinnerbecky = 0
                    "Вытянув руку из-под стола, и из-под юбки Ребекки, вы решили вернуться к еде."
                $ _eat_roll = procedural_randint(1, 4, "becky_dinner_eat_%s_%s" % (int(dayspassed or 0), dinnertime))
                $ _eat_roll_alt = procedural_randint(1, 4, "becky_dinner_eat_alt_%s_%s" % (int(dayspassed or 0), dinnertime))
                if _eat_roll == 1:
                    "Вы напряженно работаете ложкой, а то, что из нее выпадает или не помещается, вы запихиваете себе в рот пальцами. Совет \"будьте как дома\" вы всегда воспринимали как руководство к действию."
                elif _eat_roll_alt == 1:
                    "Оглянувшись и удостоверившись что на вас никто не смотрит, вы незаметно вытерли измазанные жиром руки о край скатерти."
                else:
                    "Вы как можно энергичнее работаете челюстями. Надо наесться как можно быстрее, а вдруг не хватит?"

                if Becky.var.get("visitedhome", 0) == 4 and procedural_randint(1, 7, "becky_dinner_home5_%s_%s" % (int(dayspassed or 0), dinnertime)) == 1:
                    "Вдруг Ребекка прокашлялась, при этом покраснев, и сказала, вроде бы обращаясь к дочке с женихом, но избегая смотреть им в глаза: \"Ингенборг, Лукас, что же вы на улице-то балуетесь? Я ведь все видела. Там же неудобно, а порой и холодно. Не стесняйтесь меня, я же понимаю, дело молодое, так что коль приспичит вам, заходите прямо к нам.\""
                    "\"Ой, мам, спасибо,\" - ответила ей Инга. \"Лукас, милый, ты останешься тогда сегодня в моей комнате ночевать?\""
                    "\"А почему бы и нет? Только чего нам ждать, идем уже.\""
                    "И с этими словами парочка вскочила из-за стола и понеслась к лестнице на второй этаж."
                    "Бекки им вслед лишь промолвила: \"Эх Ингочка, Ингочка... Совсем большая стала.\""
                    "Вернувшись к еде, вы обратили внимание на похотливые огоньки в глазах Эдди."
                    $ Becky.var["visitedhome"] = 5

                if Becky.var.get("visitedhome", 0) >= 5 and dinneringaminet == 0 and dinnertime <= 2 and procedural_randint(1, 6, "becky_dinner_inga_under_%s_%s" % (int(dayspassed or 0), dinnertime)) == 1:
                    "Неожиданно вы услышали звон ножа по полу. Обернувшись, вы увидели, как Инга, сказав: \"Ой, какая я неуклюжая,\" - полезла за ним под стол."
                    $ dinneringaminet += 1

                if dinneringaminet > 0 and dinneringaminet <= 3:
                    "Вы обратили внимание, что Инга как полезла под стол за ножом, так оттуда и не вылезла. А Лукас, вместо того, чтобы помочь ей в поисках, развалился на стуле с блаженной улыбкой."
                    if procedural_randint(1, 5, "becky_dinner_becky_under_%s_%s" % (int(dayspassed or 0), dinnertime)) == 1:
                        "Тем временем Бекки, приподняв скатерть, заглянула под стол, улыбнулась и продолжила трапезу."
                    if procedural_randint(1, 5, "becky_dinner_eddie_under_%s_%s" % (int(dayspassed or 0), dinnertime)) == 1:
                        "Неуклюжий Эдди уронил салфетку, полез за ней и вскоре вылез, с сальным блеском в глазах."
                        $ Eddie.var["SawMomSex"] = max(Eddie.var.get("SawMomSex", 0), 1)
                    $ dinneringaminet += 1

                if dinneringaminet == 4:
                    "Инга наконец нашла свой нож и вылезла из-под стола. На уголках губ ее что-то поблескивало, впрочем, она быстро вытерла губы салфеткой, так что вам могло и показаться. Вернулся к еде и Лукас."
                    $ Inga.apply_social_chance(0, 1, 0, 40, 2, 1, "becky_dinner_under_table")
                    call PregnancyCheck("inga", "mouth", 1, "Лукас")
                    $ dinneringaminet += 1

                if dinnertime == 5 and story_event_available("BeckyHome", "georgett_home_visit"):
                    call checkTriggers("BeckyHome", "georgett_home_visit", 0)

                $ dinnertime += 1
                $ scene_image = "images/becky/dinner/DinnerStart.jpg"
                $ _layout_last_picture = scene_image
                vscene scene_image

            "Полапать под столом Бекки" if dinnertime <= 5 and dinnerbeckyorgasm == 0 and georgedinnersex == 0:
                if dinnerbecky == 0:
                    "Как можно более незаметно вы запустили руку под стол и положили ее на колено вашей старшей подруги. Та спокойно продолжила есть, как бы не замечая ваших действий."
                elif dinnerbecky == 1:
                    "Ваша шаловливая ручонка стала быстро перебирать платье вдовушки, задирая его подол все выше и выше. И, наконец, устремилась под него, к заветной цели."
                    if panties.get("becky", "") != "":
                        "К сожалению, путь в сладкую пещерку был прегражден бесчувственной тканью, так что вам пришлось натирать вдовушку через нее."
                    else:
                        "К своей радости, вы обнаружили, что под юбкой ничего не было, так что ваши пальчики проникли прямо в сокровищницу."
                    "Щеки Бекки залились румянцем, но она лишь чуть пошире расставила ноги, чтобы вам было удобнее, и продолжила трапезу."
                    $ scene_image = "images/becky/dinner/Grope.jpg"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                else:
                    $ dinnerbeckyorgasm = 0
                    "Вы продолжаете мастурбировать вдовушку прямо под семейным столом. Она сидит вся пунцовая, ее участие в разговоре свелось к репликам типа \"Ага\" и \"Угу\", аппетита у нее тоже поубавилось, но вроде бы пока никто не догадывается о причине."
                    if (dinnerbecky >= 3 or (panties.get("becky", "") == "" and dinnerbecky > 2)) and procedural_randint(1, 3, "becky_dinner_orgasm_%s_%s" % (int(dayspassed or 0), dinnerbecky)) == 1:
                        $ dinnerbeckyorgasm = 1
                    if dinnerbeckyorgasm == 1:
                        "Вдруг по телу Бекки пробежала дрожь наступившего оргазма, она плотно сжала своими ногами вашу руку и прикусила ложку, пытаясь не выпустить наружу сладострастный стон."
                        $ Becky.record_orgasm_given()
                        $ Becky.apply_social_roll(16, 1, 1, 40, 2, 1)
                        $ Becky.var["visitedhome"] = max(Becky.var.get("visitedhome", 0), 4)
                        if procedural_randint(1, 4, "becky_dinner_eddie_notice_%s_%s" % (int(dayspassed or 0), dinnerbecky)) == 1:
                            "Но все-таки ваши игры не остались незамеченными. Эдди пристально посмотрел на маму и, как бы нечаянно, уронил нож и сразу нырнул за ним под стол. Вы убрали руку, но вылезший из-под стола Эдди расплылся в улыбке, а его мама покраснела еще больше."
                            $ scene_image = "images/becky/dinner/GropeEddie.jpg"
                            $ _layout_last_picture = scene_image
                            vscene scene_image
                            $ Eddie.var["SawMomSex"] = max(Eddie.var.get("SawMomSex", 0), 1)
                        elif procedural_randint(1, 4, "becky_dinner_inga_notice_%s_%s" % (int(dayspassed or 0), dinnerbecky)) == 1:
                            "Это не укрылось от Инги, которая, глядя на свою мамашку, понимающе усмехнулась, опустила руку под стол и сделала там что-то такое, отчего Лукас перестал есть и покраснел."
                            $ scene_image = "images/becky/dinner/Grope.jpg"
                            $ _layout_last_picture = scene_image
                            vscene scene_image

                if dinnertime == 5 and dinnerbeckyorgasm == 0:
                    "Вы посмотрели по сторонам, и как раз вовремя. К вашему большому сожалению, Эдди, Инга и Лукас уже доели и начали собирать тарелки. Нехотя вы вытащили свою руку сначала из Бекки, а потом и из-под стола, и закончили свой ужин."

                if dinnertime == 5 and story_event_available("BeckyHome", "georgett_home_visit"):
                    call checkTriggers("BeckyHome", "georgett_home_visit", 0)

                $ dinnerbecky += 1
                $ dinnertime += 1
                if int(Becky.drunk or 0) == 1:
                    $ _drink_pic = procedural_randint(1, 3, "becky_dinner_drink_pic_%s_%s" % (int(dayspassed or 0), dinnertime))
                    $ scene_image = "images/becky/dinner/drink%s.jpg" % _drink_pic
                else:
                    $ scene_image = "images/becky/dinner/eat.jpg"
                $ _layout_last_picture = scene_image
                vscene scene_image

            "Взять Бекки под руку и идти наверх в спальню" if dinnertime == 6 and georgedinnersex == 0:
                $ dinnertime += 1
                if Becky.var.get("visitedhome", 0) < 4:
                    "Вы решительно подошли к вдове, взяли ее под локоток и повели к лестнице, ведущей на второй этаж. Вернее, попытались повести. Бекки сидела на стуле как влитая."
                    "А когда вы попробовали потянуть ее сильнее, она отвесила вам пинок под столом и сказала: \"Стефан, милый, уже наверное поздно, так что мы будем готовиться ко сну, а тебе тоже наверное пора.\""
                    "Вы отпустили ее руку и направились к двери."
                    $ Becky.apply_social_roll(8, 3, -1, 35, 3, -1)
                    $ scene_image = "images/becky/Home/door.jpg"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                elif Becky.var.get("visitedhome", 0) <= 6 and Becky.var.get("visitedhome", 0) >= 4:
                    if Becky.var.get("visitedhome", 0) >= 5 and (Becky.corruption + procedural_randint(1, 5, "becky_dinner_bed_gate_%s" % int(dayspassed or 0)) + dinnerbeckyorgasm * 5 >= 48 or Becky.var.get("HomeSex", 0) == 1):
                        $ Becky.apply_social_roll(18, 2, 1, 50, 2, 1)
                        "Вы, как бы невзначай, подошли к вдове, взяли ее за руку и слегка потянули в направлении лестницы, ведущей на второй этаж. Щеки Бекки зарделись, а на лице появилось выражение решимости."
                        "Она встала и направилась с вами наверх, бросив через плечо: \"Ингочка, собери пожалуйста со стола. А мы со Стефаном обсудим некоторые дела в моей комнате.\""
                        if Becky.var.get("EddieTryToFuck", 0) == 4:
                            "Эдди было дернулся последовать за вами, но Ребекка обожгла его таким взглядом, что он обреченно плюхнулся обратно на стул. Видно, вдова еще не созрела до повторения, а может разволновалась от того, что Эдди в последний момент не послушал ее?"
                        else:
                            "Эдди проводил вас затуманившимся взглядом, а Инга с Лукасом - понимающим."
                        if Becky.var.get("EddieWhoreHome", 0) == 4:
                            "Жоржетта же весело подмигнула вам."
                        $ Becky.var["HomeSex"] = 1
                        $ _kids_watch = procedural_randint(1, 8, "becky_dinner_kids_watch_%s" % int(dayspassed or 0))
                        call BeckyGuestKidsWatchStepsCode(_kids_watch)
                        if _kids_watch > 3 and procedural_randint(1, 2, "becky_dinner_eddie_georg_hint_%s" % int(dayspassed or 0)) == 1 and Becky.var.get("EddieGeorg", 0) == 0:
                            "\"Хм, что-то Эдди изрядно возбужден тем, что я с его мамочкой в спальню иду. Может с Жоржи стоит это обсудить?\" - подумали вы."
                        call BeckyHome("FromDinner")
                        return
                    else:
                        "Вы, как бы невзначай, подошли к вдове, взяли ее за руку и слегка потянули в направлении лестницы, ведущей на второй этаж. Бекки повернула голову в сторону лестницы, на ее лице отразилось сначала предвкушение, а потом смущение и сожаление. Она незаметно покачала головой и высвободила руку."
                        $ scene_image = "images/becky/Home/door.jpg"
                        $ _layout_last_picture = scene_image
                        vscene scene_image
                else:
                    "Вы в который раз подошли к вдове и привычно взяли ее за руку, потянув в направлении лестницы, ведущей на второй этаж."
                    if (Eddie.var.get("RidiculeFollow", 0) > 0 and procedural_randint(1, 10, "becky_dinner_ridicule_repeat_%s" % int(dayspassed or 0)) == 1) or (Eddie.var.get("RidiculeFollow", 0) == 0 and procedural_randint(1, 2, "becky_dinner_ridicule_first_%s" % int(dayspassed or 0)) == 1):
                        "Однако в этот раз к вам попытался присоединиться Беккин сынок Эдди."
                        "Как ни в чем не бывало наглец заявил, вставая со стула и намереваясь последовать за вами: \"Давайте я вас провожу, может и сгожусь на что-нибудь.\""
                        "Ребекка пребывала в явной растеренности, вы же строго отшили нахала: \"Спасибо, Эдди, но мы уж сами. Может я запамятовал чего, но мне кажется, что ни я ни миссис Блэнкеншип тебя не звали. Или ты услыхал чего? Или просто нафантазировал невесть что?\""
                        if procedural_randint(1, 3, "becky_dinner_eddie_ridicule_%s" % int(dayspassed or 0)) == 1:
                            "Эдди такая отповедь не на шутку расстроила. Он едва не разрыдался от нанесенной обиды и выбежал из комнаты, хлопнув дверью."
                            $ Eddie.change_social(friend_delta=-1)
                        else:
                            "Эдди от такой отповеди закусил губу и плюхнулся обратно на стул."
                            if procedural_randint(1, 2, "becky_dinner_eddie_ridicule_friend_%s" % int(dayspassed or 0)) == 1:
                                $ Eddie.change_social(friend_delta=-1)
                        "Лукас и Инга заулыбались от постигшего Эдди облома."
                        if Becky.var.get("EddieWhoreHome", 0) == 4:
                            "А Жоржетта так и вовсе невежливо заржала в голос."
                            if procedural_randint(1, 2, "becky_dinner_eddie_georgett_laugh_%s" % int(dayspassed or 0)) == 1:
                                $ Eddie.change_social(friend_delta=-1)
                        $ Eddie.var["RidiculeFollow"] = 1
                    else:
                        "Эдди, похоже, малость огорчился, что его с собой не взяли, но за вами последовать не попытался, наверное решил, что возьмет свое позже."
                        if procedural_randint(1, 5, "becky_dinner_eddie_left_behind_%s" % int(dayspassed or 0)) == 1:
                            $ Eddie.change_social(friend_delta=-1)
                    "Вы невозбранно последовали со вдовой вдвоем наверх, в ее уютненькую спальню."
                    $ _kids_watch = procedural_randint(1, 8, "becky_dinner_kids_watch_late_%s" % int(dayspassed or 0))
                    call BeckyGuestKidsWatchStepsCode(_kids_watch)
                    $ _ladder_pic = procedural_randint(1, 2, "becky_dinner_ladder_%s" % int(dayspassed or 0))
                    $ scene_image = "images/becky/Home/ladder%s.jpg" % _ladder_pic
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    call BeckyHome("FromDinner")
                    return

            "Идти в спальню вместе с Бекки и Эдди" if dinnertime == 6 and georgedinnersex == 0 and Becky.var.get("visitedhome", 0) >= 7:
                $ dinnertime += 1
                "Вы, как обычно, подошли к вдове после ужина, взяли одинокую женщину за руку и повели к спальне. Она с радостью последовала за вами, но уже на втором шаге, что-то видно вспомнив, тихо прошептала вам: \"А Эдди?\""
                $ _ladder_pic = procedural_randint(1, 2, "becky_dinner_ladder_eddie_%s" % int(dayspassed or 0))
                $ scene_image = "images/becky/Home/ladder%s.jpg" % _ladder_pic
                $ _layout_last_picture = scene_image
                vscene scene_image
                if Becky.corruption >= 60:
                    "Вы с готовностью махнули парню рукой, он подскочил со стула и последовал за вами."
                    if Eddie.var.get("OthersSawWithMom", 0) > 0:
                        "Ингенборг проводила вас понимающим и затуманенным от похоти взглядом. Лукас же, пользуясь тем, что внимание Инги приковано к вашей процессии, лез ей тем временем под подол. Прежде чем он исчез из виду, вы заметили, как он тянется к завязке своих штанов."
                        $ Inga.apply_social_chance(0, 0, 0, 45, 2, 1, "becky_dinner_kids_notice")
                    else:
                        "Ингенборг открыв рот смотрела на братца, шествующего за мамой в спальню и на ходу отнюдь не по-сыновьему щипающего мать за попу. Лукас же быстро посмотрел на эту картину, соориентировался в ситуации и начал заворачивать Инге юбку, пользуясь ее прострацией. Но тем временем вы уже поднялись на второй этаж и так и не узнали, чем дело у них закончилось."
                        $ Eddie.var["OthersSawWithMom"] = 1
                        $ Inga.apply_social_chance(0, 0, 0, 45, 2, 1, "becky_dinner_kids_notice")
                else:
                    "Вы уже было собрались позвать его с вами, но, разгадав ваши намерения, целомудренная Ребекка успела вас одернуть и шепнуть на ушко: \"Ну не так явно же!\""
                    "Решив не ранить чувства бедной вдовы, вы обернулись и как можно незаметнее кивнули в ответ на обращенный к вам полный надежды взгляд Эдди. Тот просветлел лицом. А вы продолжили подниматься по лестнице. Пока вдвоем."
                if Becky.var.get("EddieWhoreHome", 0) == 4:
                    "Жоржетта же показала Эдди поднятые вверх большие пальцы. Похоже, что она ощущала себя в некотором роде тренером юноши перед важным выступлением."
                $ _kids_watch = procedural_randint(1, 8, "becky_dinner_kids_watch_eddie_%s" % int(dayspassed or 0))
                call BeckyGuestKidsWatchStepsCode(_kids_watch)
                if Becky.corruption >= 60:
                    "Втроем вы ввалились в спальню миссис Блэнкеншип, нетерпеливый Эдди только переступил порог, как сбросил с себя всю одежду."
                else:
                    "Вы поднялись по лестнице в спальню Бекки и стали страстно в засос целоваться, не то что не запирая, но даже и не закрывая дверь. Не отрывая своих губ от губ Бекки, вы успели малость потискать ее груди, а она - погладить вам член и даже развязать завязки на штанах. Ваши милые развлечения прервал звук закрывающейся двери. Тут вы увидели Эдди: сорванец успел уже раздеться и голый присоединился к вам."
                call BeckyHome("SvalnyiGreh")
                return

            "Попрощаться и идти домой" if dinnertime > 5 and georgedinnersex == 0:
                "Вы вежливо, отнюдь не по-английски, попрощались с семейством Блэнкеншип, поцеловали в щечку Ингу, погладили попку Бекки и направились на улицу."
                $ calendar_v2.advance_minutes(60)
                jump MarketPlace


label BeckyGuestKidsWatchStepsCode(kids_watch=0):
    if kids_watch <= 3:
        "Поднимаясь вслед за вдовой по лестнице, вы заметили, что из-за угла за вами кто-то подсматривает."
        if kids_watch == 1:
            "Это был Ивар, младший сын вдовы. Встретившись с вами взглядом, он усмехнулся и сделал пошлый жест."
        elif kids_watch == 2:
            "Это была юная Эмма, средняя дочка Бекки. На ее лице застыло мечтательное выражение."
        else:
            "Это была Эмма с маленькой Лаурой, младшей дочкой Бекки. Лаура была явно удивлена происходящим, но Эмма наклонилась к ней и прошептала что-то такое, отчего глазенки Лауры расширились, а щеки стали пунцовыми."
    return
