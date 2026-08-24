# ================================================================================
# Irma tailor interaction/event scenes.
# ================================================================================

label IrmaShopFlirtScene:
    $ main_ui_begin_native_scene_state("Ирма")
    $ scene_runtime.text = "Ирма отрывается от работы, одаривает вас внимательным взглядом и поправляет сантиметровую ленту на шее. Разговор быстро уходит от ткани, выкроек и ниток к намекам, в которых портниха чувствует себя не менее уверенно, чем за рабочим столом."
    $ scene_runtime.location_text = scene_runtime.text
    $ scene_runtime.picture = irma_flirting_picture_path()
    menu:
        "Поговорить с Ирмой":
            call IntIrmaTalk
            jump IrmaShopFlirtScene

        "Примерочная Ирмы":
            jump IrmaMeasureRoomMenu

        "Назад в лавку":
            $ main_ui_end_native_scene_state()
            return


label IrmaMeasureRoomMenu(irma_measure_stage=0):
    $ main_ui_begin_native_scene_state("Примерочная Ирмы")
    $ scene_runtime.text = "За ширмой стоит узкая скамья, большое зеркало и манекен с наколотыми булавками лентами. Ирма держит мерную ленту наготове и предлагает выбрать, насколько тщательно снимать мерки."
    $ scene_runtime.location_text = scene_runtime.text
    $ scene_runtime.picture = irma_measure_picture_path(0)
    menu:
        "Обычные мерки":
            $ irma_measure_stage = 0
        "Мерки в белье":
            $ irma_measure_stage = 1
        "Белье и размышления":
            $ irma_measure_stage = 2
        "Войти без одежды":
            $ irma_measure_stage = 3
        "Назад в лавку":
            $ main_ui_end_native_scene_state()
            return

    while True:
        $ scene_runtime.picture = irma_measure_picture_path(irma_measure_stage)
        if irma_measure_stage == 0:
            $ scene_runtime.text = "Ирма снимает обычные мерки быстро и профессионально: плечи, грудь, талия, длина рукавов. Ее пальцы едва касаются ткани, но ни одно движение не выглядит случайным."
        elif irma_measure_stage == 1:
            $ scene_runtime.text = "Ирма просит убрать лишнюю одежду, чтобы посадка была точнее. В примерочной становится тише; слышно только, как скользит сантиметровая лента и как портниха негромко отмечает размеры."
        elif irma_measure_stage == 2:
            $ scene_runtime.text = "Вы остаетесь в белье и стараетесь держаться спокойно, пока Ирма задумчиво сверяет мерки. Она смотрит то на ленту, то на зеркало, будто уже видит готовую вещь на теле."
        else:
            $ scene_runtime.text = "В примерочную входят уже без лишней одежды. Ирма снимает последнюю, самую смелую мерку, задерживает взгляд и оставляет за вами выбор: закончить сцену сейчас или перейти к более смелому продолжению."
        $ scene_runtime.location_text = scene_runtime.text

        menu:
            "Следующая стадия" if irma_measure_stage < 3:
                $ irma_measure_stage += 1

            "Продолжить за ширмой" if irma_measure_stage >= 3:
                call IrmaSexSequence
                if _return == "shop":
                    $ main_ui_end_native_scene_state()
                    return

            "Выбрать другую стадию":
                jump IrmaMeasureRoomMenu

            "Закончить примерку":
                $ scene_runtime.text = "Ирма собирает ленты и булавки, снова превращаясь в деловую хозяйку лавки. Но на прощание она задерживает улыбку чуть дольше, чем требуется для простой вежливости."
                $ scene_runtime.location_text = scene_runtime.text
                $ scene_runtime.picture = irma_shop_end_picture_path()
                menu:
                    "Поговорить с Ирмой":
                        call IntIrmaTalk
                    "Вернуться к примерке":
                        jump IrmaMeasureRoomMenu
                    "Назад в лавку":
                        pass
                $ main_ui_end_native_scene_state()
                return

            "Назад в лавку":
                $ main_ui_end_native_scene_state()
                return


label IrmaSexSequence(irma_sex_step=0):
    while True:
        $ scene_runtime.picture = irma_sex_picture_path(irma_sex_step)
        if irma_sex_step <= 0:
            $ scene_runtime.text = "За ширмой Ирма уже не прячет интереса. Сцена начинается с осторожного, но явного приглашения продолжить примерку иначе."
        elif irma_sex_step == 1:
            $ scene_runtime.text = "Ирма подходит ближе, все еще сохраняя вид портнихи, которая просто проверяет посадку ткани."
        elif irma_sex_step == 2:
            $ scene_runtime.text = "Пауза тянется дольше обычного, и ее рабочая строгость постепенно сменяется откровенным любопытством."
        elif irma_sex_step == 3:
            $ scene_runtime.text = "Примерочная окончательно становится местом для игры, а не только для заказа одежды."
        elif irma_sex_step == 4:
            $ scene_runtime.text = "Ирма уверенно ведет сцену дальше, будто заранее знала, чем закончится такая примерка."
        elif irma_sex_step == 5:
            $ scene_runtime.text = "Все лишние слова уже сказаны; остается только следовать ритму, который задает портниха."
        elif irma_sex_step == 6:
            $ scene_runtime.text = "Сцена подходит к кульминации, и Ирма больше не пытается выглядеть равнодушной."
        elif irma_sex_step == 8:
            $ scene_runtime.text = "После горячего продолжения Ирма приводит себя в порядок и проверяет, не осталось ли следов на ткани."
        else:
            $ scene_runtime.text = "Ирма возвращается к работе, но теперь примерочная кажется куда менее невинным местом, чем несколько минут назад."
        $ scene_runtime.location_text = scene_runtime.text

        menu:
            "Продолжить" if irma_sex_step < 6:
                $ irma_sex_step += 1
            "Продолжить" if irma_sex_step == 6:
                $ irma_sex_step = 8
            "Завершить" if irma_sex_step == 8:
                $ irma_sex_step = 9
            "Закончить сцену" if irma_sex_step >= 9:
                return "measure"
            "Вернуться к примерке":
                return "measure"
            "Назад в лавку":
                return "shop"


label IrmaClaraFittingScene(stage=0):
    $ renpy.dynamic("_clara_fit_stage")
    $ main_ui_begin_native_scene_state("Примерка Клариссы")
    $ _clara_fit_stage = max(0, min(int(stage or 0), 3))
    while True:
        $ scene_runtime.picture = irma_clara_fitting_picture_path(_clara_fit_stage)
        if str(people.location("clara") or "") != "DressShop":
            $ scene_runtime.text = "Клариссы сейчас нет в лавке, так что примерочная занята только тканями, манекенами и Ирмиными выкройками."
        elif _clara_fit_stage == 0:
            $ scene_runtime.text = "Кларисса стоит у зеркала, пока Ирма прикладывает к ней тонкую ткань будущего белья и оценивает посадку."
        elif _clara_fit_stage == 1:
            $ scene_runtime.text = "Ирма поправляет ленты и мерки, а Кларисса вполголоса спорит о том, насколько смело должна выглядеть новая вещь."
        elif _clara_fit_stage == 2:
            $ scene_runtime.text = "Примерка превращается в оживленный разговор: Кларисса спрашивает совета, Ирма отвечает профессионально, но с заметной улыбкой."
        else:
            $ scene_runtime.text = "Кларисса наконец соглашается с выбором Ирмы. Обе женщины выглядят довольными результатом, хотя разговор явно можно продолжить позже."
        $ scene_runtime.location_text = scene_runtime.text

        menu:
            "Продолжить примерку" if str(people.location("clara") or "") == "DressShop" and _clara_fit_stage < 3:
                $ _clara_fit_stage += 1
            "Поговорить с Ирмой":
                call IntIrmaTalk
            "Назад в лавку":
                $ main_ui_end_native_scene_state()
                return
