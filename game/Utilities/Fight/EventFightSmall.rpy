# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label EventFightSmall(eyewitness=0, CurMoneyLoss=0, FightRand=0, PhraseEnd1EFS="", CurEventDesc="", _dog_tavern_result=None):
    $ CurMoneyLoss = procedural_randint(10, 16, key="procedural:Utilities/Fight/EventFightSmall.rpy:procedural_randint:5:1")
    $ FightRand = procedural_randint(1, 7, key="procedural:Utilities/Fight/EventFightSmall.rpy:procedural_randint:6:2")

    if FightRand == 1:
        $ CurMoneyLoss *= 2
        $ CurEventDesc = "В вашем трактире произошла драка! Компания грузчиков напилась до полного заполнения тары. Ну а потом неожиданно выяснилось, что Йоаким недостаточно уважает Никласа, а Макс откровенно признался, что он частенко имел мать Юнатана в разных позах и вообще приходится тому отцом. А тот ему, соответсвенно, сынком. Никлас и Юнатан захотели узнать подробности, остальные попробовали их разнять, в итоге компания отправилась гулять дальше, а вы и ваши домочадцы остались разбирать черепки и чинить сломанные скамейки."
        $ PhraseEnd1EFS = "Ущерб составил {} мараведи.".format(CurMoneyLoss)
    elif FightRand == 2:
        $ CurEventDesc = "В вашем трактире произошла драка! Компания мелких воров пару часов спокойно играла себе в кости в дальнем углу, никому не мешая, пока вдруг у одного из игроков из рукава нечаянно не выкатилась пара лишних костяшек. Коллеги растяпы отнеслись к произошедшему бескомпромиссно. Без излишних разговоров ему с ходу разбили кувшин о голову а потом еще малость попинали, отобрав все деньги. Хотя борцы с мухлежом вам честно и заплатили за себя, но валявшемуся в отключке шулеру платить за свою выпивку после расправы было нечем. Да и стоимость разбитого кувшина вам и никто и не подумал возмещать."
        $ PhraseEnd1EFS = "Убыток составил {} мараведи.".format(CurMoneyLoss)
    elif FightRand == 3:
        $ CurMoneyLoss = CurMoneyLoss // 2
        $ CurEventDesc = "Какой-то господин, судя по одежде вполне приличный, вкусно покушал у вас в трактире, запив свой ужин парой стаканов вина. А потом он вскочил на скамью, проорал что и еда и вино - дерьмо, что он имел ваш трактир, вас, ваших домочадцев, всех остальных посетителей, соседние трактиры, их посетителей, а также прохожих в извращенной форме. Пока завсегдатаи осмысливали его смелую речь, этот господин, не дожидаясь аплодисментов, выскочил за дверь и был таков. Естественно, он не и не подумал заплатить {} мараведи которые с него причитались.".format(CurMoneyLoss)
    elif FightRand == 4:
        $ CurMoneyLoss *= 4
        $ CurEventDesc = "В вашем трактире все было тихо и мирно, пока вдруг в двери не ввалилась шумная толпа стражников. Возглавлявший их капитан с торжествующим воплем указал на какого-то мужичонку, мирно сидевшего у дальней стены:\n-\"Вот он гад! Попался! Хватай его робя!\" И служители закона кинулись ловить негодяя не разбирая дороги, опрокидывая лавки и столы. Тот кинулся бежать, также не заботясь о сохранности вашего с трудом нажитого имущества."
        $ PhraseEnd1EFS = "В конечном итоге, пару минут спустя и парой опрокинутых столов больше, преступник был пойман. Стражники торжественно увели свою добычу, смело шагая по похрустывающим черепкам, в которые превратились многие из ваших кружек-плошек. Последним ушел капитан, строго погрозив вам и наказав впредь не давать приюта разыскиваемым воришкам. А вы остались убирать битую посуду и считать убытки. Визит служителей закона и порядка обошелся вам в смешные {} мараведи.\n\"Ради торжества справедливости и вдвое больше потерять не жалко!\" -подумали вы.".format(CurMoneyLoss)
    else:
        $ CurEventDesc = "В вашем трактире произошла драка! Двое пьяных моряков начали выяснять отношения и в процессе расколотили горшков и тарелок на {} мараведи, а потом смылись, не заплатив!".format(CurMoneyLoss)

    if eyewitness > 0:
        $ CurEventDesc += "\n\nЧто вы намеренны предпринять?"
        $ scene_runtime.text = CurEventDesc
        $ scene_runtime.location_text = CurEventDesc
        show screen main_ui
        menu:
            "Выругаться и не делать ничего":
                call EventFightSmallFinish(1, CurMoneyLoss, FightRand, PhraseEnd1EFS)
            "Кинуться бежать вслед" if FightRand == 3:
                call EventFightSmallFinish(2, CurMoneyLoss, FightRand, PhraseEnd1EFS)
            "Преследовать" if FightRand > 4:
                call EventFightSmallFinish(3, CurMoneyLoss, FightRand, PhraseEnd1EFS)
            "Качать права" if FightRand <= 2:
                call EventFightSmallFinish(4, CurMoneyLoss, FightRand, PhraseEnd1EFS)
            "Звать стражу" if FightRand != 4 and player.economy.money >= 4 and player.tavern_management.winenum >= 2:
                call EventFightSmallFinish(5, CurMoneyLoss, FightRand, PhraseEnd1EFS)
            "Помочь ловить" if FightRand == 4 and player.economy.money >= (4 + CurMoneyLoss) and player.tavern_management.winenum >= 2:
                call EventFightSmallFinish(6, CurMoneyLoss, FightRand, PhraseEnd1EFS)
    else:
        $ player.add_money(-CurMoneyLoss)
        if FightRand == 3 or FightRand > 4:
            $ _dog_tavern_result = dog_catch_delinquent_apply("tavern_nonpayment")
            if bool(_dog_tavern_result.get("ok", False)):
                if FightRand == 3:
                    $ player.add_money(CurMoneyLoss)
                $ CurEventDesc += "\n\n" + str(_dog_tavern_result.get("text", "") or "")
        if PhraseEnd1EFS:
            $ CurEventDesc += "\n" + PhraseEnd1EFS

    return CurEventDesc

label EventFightSmallFinish(reaction_code=1, CurMoneyLoss=0, FightRand=0, PhraseEnd1EFS="", extra_text="", _dog_tavern_result=None):
    $ _dog_tavern_result = {"ok": False, "text": ""}

    if reaction_code == 1:
        $ player.add_money(-CurMoneyLoss)
    elif reaction_code == 2:
        $ player.add_money(-CurMoneyLoss)
        $ extra_text = "Вы кинулись бежать вслед за негодяем, но он оказался намного быстрее вас. Догнать его вы не смогли."
    elif reaction_code == 3:
        $ player.add_money(-CurMoneyLoss)
        $ extra_text = "Вы кинулись бежать за драчунами, но вскоре, когда они углубились в сеть темных переулков, благоразумие взяло верх и вы оставили эту затею."
    elif reaction_code == 4:
        $ player.add_money(-CurMoneyLoss)
        $ extra_text = "Вы попробовали потребовать возмещения ваших убытков, но наткнулись на искренне непонимание. По мнению ваших буйных посетителей они не были вам должны ничего сверх того, что они уже заплатили. А молодецкой силы, позволившей бы набить морды всей их компании, вы в себе не ощущали."
    elif reaction_code == 5:
        $ player.spend_money(4)
        $ player.tavern_management.winenum -= 2
        $ player.add_money(-CurMoneyLoss)
        $ extra_text = "Вы выскочили за дверь и начали кричать \"Стража, Стража!\". Не прошло и каких-то 20 минут, как к вам подошли двое толстых стражников и поинтересовались, в чем собственно дело. Узнав подробности они резонно заметили, что ваши обидчики уже успели уйти далеко и поймать их будет затруднительно. Промочив горло парой кружек вина за счет заведения и взяв 4 мараведи за труды, стражи порядка удалились. Хорошо все-таки, что те, кому положенно, берегут ваш покой и неукоснительно следят за соблюдением законов!"
    elif reaction_code == 6:
        if procedural_randint(1, 2, key="procedural:Utilities/Fight/EventFightSmall.rpy:procedural_randint:87:3") == 1:
            $ extra_text = "Вы кинулись ловить вора. Разбив в процессе пару кружек и сбив со стойки поднос, на котором громоздилась пирамида из грязной посуды, вы отрезали вора от выхода и стражникам удалось в конце концов его поймать."
            $ PhraseEnd1EFS = "Стражники торжественно увели свою добычу, смело шагая по похрустывающим черепкам, в которые превратились многие из ваших кружек-плошек. Последним ушел капитан, поблагодарив вас за неоценимую помощь. А вы остались убирать битую посуду и считать убытки. Визит служителей закона и порядка обошелся вам в смешные {} мараведи.\n\"Ради торжества справедливости и вдвое больше потерять не жалко!\" -подумали вы.".format(CurMoneyLoss)
        else:
            $ extra_text = "Вы кинулись ловить вора, но споткнулись и растянулись на полу, выбыв из участников забавы."
        $ player.add_money(-CurMoneyLoss)

    if FightRand == 3 or FightRand > 4:
        $ _dog_tavern_result = dog_catch_delinquent_apply("tavern_nonpayment")
        if bool(_dog_tavern_result.get("ok", False)):
            if FightRand == 3:
                $ player.add_money(CurMoneyLoss)
            if str(extra_text or "").strip():
                $ extra_text += "\n\n" + str(_dog_tavern_result.get("text", "") or "")
            else:
                $ extra_text = str(_dog_tavern_result.get("text", "") or "")

    if extra_text:
        "[extra_text]"
    if PhraseEnd1EFS:
        "[PhraseEnd1EFS]"

    return
