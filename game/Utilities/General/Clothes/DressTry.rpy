# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default DressTryStep = 0

label DressTry(dress_buyer="You", dress_code=""):
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ DressProduced = str(dress_code or "")
    $ DressBuyer = str(dress_buyer or "You")
    $ Friends.setdefault("irma", 0)
    $ IrmaVar.setdefault("DeniedMinetMoney", 0)
    $ HadSex.setdefault("You", 0)
    $ DressTryStep = 0
    $ _layout_last_picture = irma_measure_picture_path(0)
    $ MainTxt = "Не говоря ни слова, вы подходите к Ирме и вываливаете перед ней на стол горку монет. Ловя на себе ее удивленный взгляд, вы говорите ей, что это не подарок, а вы просто хотите у нее заказать " + ShortDressName.get(DressProduced, DressProduced).lower() + ". Портниха тщательно пересчитывает деньги, и, удостоверившись что все правильно, ведет вас за ширмочку, дабы снять мерку. Как вы хотите, чтобы с вас сняли мерку?"
    $ CurLocDesc = MainTxt
    $ current_action_title = "Снятие мерки"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Раздеться до белья", Call("DressTryUnderwear"))]
    if HadSex.get("You", 0) >= 3:
        $ current_action_items.append(MenuItem("Полностью раздеться и думать о высоком", Call("DressTryNakedThink")))
    if HadSex.get("You", 0) >= 5 and cametoday < cancumdaily:
        $ current_action_items.append(MenuItem("Полностью раздеться и представить Ирму", Call("DressTryNakedFantasy")))
    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRestore")))
    return


label DressTryUnderwear:
    $ _layout_last_picture = irma_measure_picture_path(1)
    $ MainTxt = "Вы быстро разделись до нижнего белья. Ирма ловко и быстро сняла с вас мерку, сказав, что она начнет шить немедленно, а работа будет готова к утру."
    $ CurLocDesc = MainTxt
    $ DressTryStep += 1
    $ current_action_title = "Снятие мерки"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Одеться и вернуться в лавку", Call("DressShopRestore"))]
    return


label DressTryNakedThink:
    $ _layout_last_picture = irma_measure_picture_path(2)
    $ MainTxt = "Вы быстро и решительно сняли с себя все. Однако, дабы не смущать портниху возможной эрекцией, вы начали думать о птичках, облаках, способах постройки домов, счетах за вино и прочих отвлеченных вещах. Ирма ловко и быстро сняла с вас мерку. Заодно она измерила и вашего скукожившегося от холода друга. Судя по ее выражению лица результат ее если и удивил, то в худшую сторону. Закончив мерять, Ирма сказала, что она начнет шить немедленно, а работа будет готова к утру."
    $ CurLocDesc = MainTxt
    call SlutFriendsIncrease("irma", 0, 1, -1, 0, 0, 0)
    $ DressTryStep += 1
    $ current_action_title = "Снятие мерки"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Одеться и вернуться в лавку", Call("DressShopRestore"))]
    return


label DressTryNakedFantasy:
    $ _layout_last_picture = irma_measure_picture_path(3)
    if Friends.get("irma", 0) < 3 or cametoday >= cancumdaily or IrmaVar.get("DeniedMinetMoney", 0) == 1:
        $ MainTxt = "Вы быстро и решительно сняли с себя все. А сняв, предались приятным грезам о том, как и в каких позах вы хотели бы поиметь смазливую полуэльфийку. Такие мечты не замедлили сказаться на состоянии вашего члена - реагируя на ваши мысли он с готовностью напрягся, приходя в полную боевую. Это не прошло незамеченным Ирмой: снимая с вас мерку, она улыбнулась, спросила \"Это я тебе настолько нравлюсь?\" и, не дожидаясь ответа, измерила и ваш вздыбленный член. Судя по ее выражению лица результат ей скорее всего понравился. Закончив мерять, Ирма сказала, что она начнет шить немедленно, а работа будет готова к утру."
        $ CurLocDesc = MainTxt
        call SlutFriendsIncrease("irma", 5, 1, 1, 0, 0, 0)
        $ DressTryStep += 1
        $ current_action_title = "Снятие мерки"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Одеться и вернуться в лавку", Call("DressShopRestore"))]
    else:
        $ MainTxt = "Пока с вас снимали мерку вы, как обычно, закрыли глаза и начали представлять себе Ирму в непотребном виде. Вдруг, с удивлением и радостью, вы ощутили чей-то горячий ротик на своем эрегированном друге. Вы открыли глаза и обнаружили что портниха решила сделать процесс снятия мерки более приятным. Ирма на секунду выпустила свою игрушку изо рта и сказала: \"Для постоянных и щедрых клиентов - особое обслуживание!\", после чего вернулась к своему занятию. Вы просто стояли и балдели, пока полуэльфийка отсасывала у вас. Делала она это умело, можно сказать с огоньком, и вскоре вы почувствовали что кончаете."
        $ CurLocDesc = MainTxt
        $ _layout_last_picture = irma_sex_picture_path(0)
        $ current_action_title = "Особое обслуживание"
        $ current_action_content = None
        $ current_action_items = [
            MenuItem("Кончить на лицо", Call("DressTryServiceFinish", "face")),
            MenuItem("Кончить в рот", Call("DressTryServiceFinish", "mouth")),
        ]
    return


label DressTryServiceFinish(finish=""):
    if str(finish or "") == "face":
        $ _layout_last_picture = irma_sex_picture_path(8)
        $ MainTxt = "Поняв, что вы вот-вот кончите, вы вынули своего друга изо рта Ирмы и направили его на ее личико. Та зажмурила глаза в последний момент перед тем, как ваша сперма приземлилась на ее щечках, веках и заостренных ушках. Дождавшись, чтобы вы закончили, портниха вынула красивый батистовый платочек и, смотрясь в одно из зеркал, вытерла свое личико."
    else:
        $ _layout_last_picture = irma_sex_picture_path(9)
        $ MainTxt = "Вы и не подумали предупредить портниху о том, что вы уже близки к оргазму и без предупреждения начали спускать прямо ей в ротик. Это застало ее врасплох, она даже поперхнулась, но продолжила сосать, пока не выдоила все до капельки."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Особое обслуживание"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Расплатиться", Call("code_farago_demand_money"))]
    return


label code_farago_demand_money:
    call PregnancyCheck("irma", "mouth", 1, "Вы")
    $ MainTxt = "Расплачиваясь за костюмчик, вы заметили, что мисс Фараго прибавила к счету 20 мараведи."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Счет Ирмы"
    $ current_action_content = None
    $ current_action_items = []
    if money >= 20:
        $ current_action_items.append(MenuItem("Промолчать и оплатить", Call("DressTryPayExtra")))
    $ current_action_items.append(MenuItem("Возмутиться", Call("DressTryRefuseExtra")))
    return


label DressTryPayExtra:
    $ MainTxt = "Вы хотели было возмутиться, но потом вспомнили жаркий ротик Ирмы и решили промолчать."
    $ CurLocDesc = MainTxt
    call SlutFriendsIncrease("irma", 10, 1, 1, 0, 0, 0)
    $ money -= 20
    call stat
    $ current_action_title = "Счет Ирмы"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Одеться и вернуться в лавку", Call("DressShopRestore"))]
    return


label DressTryRefuseExtra:
    $ _layout_last_picture = irma_angry_picture_path()
    $ MainTxt = "Заметив такую обдираловку, вы не замедлили бурно выразить свое несогласие. Мисс Фараго выслушала вас и тихо сказала: \"Что ж, значит вы клиент постоянный, но не щедрый, будем знать,\" и исправила счет обратно."
    $ CurLocDesc = MainTxt
    $ Friends["irma"] = max(Friends.get("irma", 0) - 3, 0)
    $ IrmaVar["DeniedMinetMoney"] = 1
    $ current_action_title = "Счет Ирмы"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Одеться и вернуться в лавку", Call("DressShopRestore"))]
    return
