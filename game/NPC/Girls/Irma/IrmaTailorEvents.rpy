# ================================================================================
# Irma and Clara tailor interaction scene.
# ================================================================================


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
