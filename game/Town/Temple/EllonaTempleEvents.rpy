label story_ellona_temple_sunday_stories:
    $ main_ui_begin_native_scene_state("Воскресные истории")
    vscene "images/ellona/Fran5.png"
    $ Francheska.sunday_stories_seen_day = int(current_game_day() or 0)
    $ scene_runtime.text = "Во дворике храма Франческа сегодня не одна. Вокруг нее устроилась ребятня, и старая жрица, размахивая руками, рассказывает им воскресные легенды об Эллоне, Грациях и давних временах.\n\n\"...и звали их пионеры... А когда вожатые занимались тем, чем велела им Эллона и Грации, они били в барабаны и трубили в горны...\"\n\nВы решили не мешать Франческе."
    show screen main_ui
    menu:
        "Осмотреться в храме":
            pass
    $ main_ui_end_native_scene_state()
    return True
