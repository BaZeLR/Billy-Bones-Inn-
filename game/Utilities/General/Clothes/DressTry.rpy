init python:
    def dress_try_display_name(dress_code=""):
        code = str(dress_code or "").strip()
        item_obj = get_game_item("dress_" + code)
        item_name = str(getattr(item_obj, "name", "") or "").strip() if item_obj is not None else ""
        return item_name or str(ShortDressName.get(code, code) or code)


label DressTry(dress_buyer="You", dress_code=""):
    $ dress_shop.produced = str(dress_code or "")
    $ dress_shop.buyer = str(dress_buyer or "You")
    $ scene_runtime.picture = irma_measure_picture_path(0)
    $ scene_runtime.text = "Не говоря ни слова, вы подходите к Ирме и вываливаете перед ней на стол горку монет. Ловя на себе ее удивленный взгляд, вы говорите ей, что это не подарок, а вы просто хотите у нее заказать " + dress_try_display_name(dress_shop.produced).lower() + ". Портниха тщательно пересчитывает деньги, и, удостоверившись что все правильно, ведет вас за ширмочку, дабы снять мерку. Как вы хотите, чтобы с вас сняли мерку?"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Раздеться до белья":
            call DressTryUnderwear

        "Полностью раздеться и думать о высоком" if player.intimacy.had_sex_count >= 3:
            call DressTryNakedThink

        "Полностью раздеться и представить, как вы имеете Ирму" if player.intimacy.had_sex_count >= 5 and player.intimacy.came_today < player.intimacy.can_cum_daily:
            call DressTryNakedFantasy
    return


label DressTryUnderwear:
    $ scene_runtime.picture = irma_measure_picture_path(1)
    $ scene_runtime.text = "Вы быстро разделись до нижнего белья. Ирма ловко и быстро сняла с вас мерку, сказав, что она начнет шить немедленно, а работа будет готова к утру."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Одеться и уйти":
            return
    return


label DressTryNakedThink:
    $ scene_runtime.picture = irma_measure_picture_path(2)
    $ scene_runtime.text = "Вы быстро и решительно сняли с себя все. Однако, дабы не смущать портниху возможной эрекцией, вы начали думать о птичках, облаках, способах постройки домов, счетах за вино и прочих отвлеченных вещах. Ирма ловко и быстро сняла с вас мерку. Заодно она измерила и вашего скукожившегося от холода друга. Судя по ее выражению лица результат ее если и удивил, то в худшую сторону. Закончив мерять, Ирма сказала, что она начнет шить немедленно, а работа будет готова к утру."
    $ scene_runtime.location_text = scene_runtime.text
    call SlutFriendsIncrease("irma", 0, 1, -1, 0, 0, 0)
    menu:
        "Одеться и уйти":
            return
    return


label DressTryNakedFantasy:
    $ scene_runtime.picture = irma_measure_picture_path(3)
    if Irma.rel < 3 or player.intimacy.came_today >= player.intimacy.can_cum_daily or Irma.extra_fee_refused:
        $ scene_runtime.text = "Вы быстро и решительно сняли с себя все. А сняв, предались приятным грезам о том, как и в каких позах вы хотели бы поиметь смазливую полуэльфийку. Такие мечты не замедлили сказаться на состоянии вашего члена - реагируя на ваши мысли он с готовностью напрягся, приходя в полную боевую. Это не прошло незамеченным Ирмой: снимая с вас мерку, она улыбнулась, спросила \"Это я тебе настолько нравлюсь?\" и, не дожидаясь ответа, измерила и ваш вздыбленный член. Судя по ее выражению лица результат ей скорее всего понравился. Закончив мерять, Ирма сказала, что она начнет шить немедленно, а работа будет готова к утру."
        $ scene_runtime.location_text = scene_runtime.text
        call SlutFriendsIncrease("irma", 5, 1, 1, 0, 0, 0)
        menu:
            "Одеться и уйти":
                return
    $ scene_runtime.text = "Пока с вас снимали мерку вы, как обычно, закрыли глаза и начали представлять себе Ирму в непотребном виде. Вдруг, с удивлением и радостью, вы ощутили чей-то горячий ротик на своем эрегированном друге. Вы открыли глаза и обнаружили что портниха решила сделать процесс снятия мерки более приятным. Ирма на секунду выпустила свою игрушку изо рта и сказала: \"Для постоянных и щедрых клиентов - особое обслуживание!\", после чего вернулась к своему занятию. Вы просто стояли и балдели, пока полуэльфийка отсасывала у вас. Делала она это умело, можно сказать с огоньком, и вскоре вы почувствовали что кончаете."
    $ scene_runtime.location_text = scene_runtime.text
    $ scene_runtime.picture = irma_sex_picture_path(0)
    menu:
        "Кончить на лицо":
            call DressTryServiceFinish("face")
        "Кончить в рот":
            call DressTryServiceFinish("mouth")
    return


label DressTryServiceFinish(finish=""):
    if str(finish or "") == "face":
        $ scene_runtime.picture = irma_sex_picture_path(8)
        $ scene_runtime.text = "Поняв, что вы вот-вот кончите, вы вынули своего друга изо рта Ирмы и направили его на ее личико. Та зажмурила глаза в последний момент перед тем, как ваша сперма приземлилась на ее щечках, веках и заостренных ушках. Дождавшись чтобы вы закончили, портниха вынула красивый батистовый платочек и, смотрясь в одно из зеркал, вытерла свое личико."
    else:
        $ scene_runtime.picture = irma_sex_picture_path(9)
        $ scene_runtime.text = "Вы и не подумали предупредить портниху о том, что вы уже близки к оргазму и без предупреждения начали спускать прямо ей в ротик. Это застало ее врасплох, она даже поперхнулась, но продолжила сосать, пока не выдоила все до капельки."
    $ scene_runtime.location_text = scene_runtime.text
    $ pregnancy_check("irma", "mouth", 1, "Вы")
    $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nРасплачиваясь за костюмчик, вы заметили что мисс Фараго прибавила к счету 20 мараведи."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Промолчать и оплатить" if player.economy.money >= 20:
            $ scene_runtime.text = "Вы хотели было возмутиться, но потом вспомнили жаркий ротик Ирмы и решили промолчать."
            $ scene_runtime.location_text = scene_runtime.text
            call SlutFriendsIncrease("irma", 10, 1, 1, 0, 0, 0)
            $ player.spend_money(20)
            call stat
            menu:
                "Одеться и уйти":
                    return

        "Возмутиться":
            $ scene_runtime.picture = irma_angry_picture_path()
            $ scene_runtime.text = "Заметив такую обдираловку вы не замедлили бурно выразить свое несогласие. Мисс Фараго выслушала вас и тихо сказала: \"Что ж, значит вы клиент постоянный, но не щедрый, будем знать,\" и исправила счет обратно."
            $ scene_runtime.location_text = scene_runtime.text
            $ Irma.change_social(friend_delta=-3)
            $ Irma.extra_fee_refused = True
            menu:
                "Одеться и уйти":
                    return
    return
