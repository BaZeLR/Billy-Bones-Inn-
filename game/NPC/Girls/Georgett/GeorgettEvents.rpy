# ================================================================================
# Georgett story event entry labels.
# ================================================================================

label story_georgett_portstreet_first_meet:
    $ scene_runtime.text = "-Привет красавчик! Не хочешь ли поразвлечься? Всего восемь мараведи!\n\nВы поговорили с ней и узнали, что ее зовут Жоржетта Брюно, она шлюха и промышляет здесь уже давно."
    $ scene_runtime.location_text = scene_runtime.text
    $ Georgett.add_relation(1)
    $ Georgett.mark_known()
    if event_runtime.active_thread is threads.get("georgettPortStreet") and not event_runtime.active_thread.done[0]:
        $ event_runtime.active_thread.seen(0)
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
    return


label story_georgett_portstreet_clients:
    $ renpy.dynamic("_georgett_first_client_watch")
    $ _georgett_first_client_watch = int(Georgett.story_value("seeclients", 0) or 0) == 0
    call street_clients_watch(1, "georgett", calendar_v2.time_slot())
    if _georgett_first_client_watch and int(Georgett.story_value("seeclients", 0) or 0) > 0 and event_runtime.active_thread is threads.get("georgettPortStreet") and not event_runtime.active_thread.done[1]:
        $ event_runtime.active_thread.seen(1)
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
    return
