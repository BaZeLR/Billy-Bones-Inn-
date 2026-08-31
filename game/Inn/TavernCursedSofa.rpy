init 4 python:
    CLARA_CURSED_SOFA_PRICE = 600

    def cursed_sofa_installed():
        room_obj = rooms.get("TavernMain")
        return room_obj is not None and _room_has_item_by_id(room_obj, "cursed_sofa_001")

    def cursed_sofa_story_active(_obj=None):
        thread = threads.get("claraForestSofa")
        return thread is not None and not thread.completed and int(thread.num or 0) in (2, 3)

    def cursed_sofa_story_available(_obj=None):
        return cursed_sofa_story_active() and story_event_available("CursedSofa", "talk")

    def cursed_sofa_waiting_for_ritual(_obj=None):
        thread = threads.get("claraForestSofa")
        return thread is not None and not thread.completed and int(thread.num or 0) == 3 and not story_event_available("CursedSofa", "talk")

    def cursed_sofa_freed(_obj=None):
        thread = threads.get("claraForestSofa")
        return thread is not None and bool(thread.completed)

    CursedSofaObject = GameObject(
        object_id="cursed_sofa_001",
        name="старинный диван",
        description="Неожиданно роскошный для вашего трактира диван. Резные ножки похожи на звериные лапы, а из глубины обивки временами доносится недовольное ворчание.",
        actions=[
            ObjectAction(
                action_id="cursed_sofa_story",
                label="Поговорить с диваном",
                hook="call",
                target="checkTriggers",
                args=("CursedSofa", "talk", 0),
                condition=cursed_sofa_story_available,
            ),
            ObjectAction(
                action_id="cursed_sofa_wait",
                label="Спросить диван о проклятии",
                hook="call",
                target="CursedSofaRitualRequirements",
                condition=cursed_sofa_waiting_for_ritual,
            ),
            ObjectAction(
                action_id="cursed_sofa_repeat",
                label="Послушать новую историю",
                hook="call",
                target="CursedSofaRepeatStory",
                condition=cursed_sofa_freed,
            ),
        ],
        custom_properties={
            "object_kind": "talking_furniture",
            "source_thread": "claraForestSofa",
        },
    )


label story_clara_sofa_first_talk_2:
    $ main_ui_begin_native_scene_state("Говорящий диван")
    show screen main_ui
    $ scene_runtime.text = "Едва вы остаетесь рядом с покупкой один, из обивки раздается сухой кашель. Диван представляется душой древнего придворного сказителя, которого ревнивый колдун проклял за слишком удачную шутку о королевском парике. С тех пор его таскают по рынкам, на нем торгуются, спят и однажды даже перевозили козу. Последнее он вспоминает с особенной ненавистью."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Спросить, как снять проклятие":
            pass
    $ scene_runtime.text = "Диван важно сообщает условие: две невинные девушки должны одновременно сесть на него по собственной воле. Клариссу он уже видел рядом с торговцем и считает подходящей; второй называет Мелиссу. Но пока над Клариссой висит договоренность с женихом, она не придет свободно. Сначала придется довести историю у цирюльни до конца, а затем собрать обеих девушек в главной зале."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Запомнить условия":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label CursedSofaRitualRequirements:
    if not threads["claraPaintingsPath"].completed:
        $ scene_runtime.text = "Диван ворчит, что Кларисса не придет по собственной воле, пока история с навязанным женихом не разрешена. След ведет к цирюльне и должен быть доведен до конца."
    elif not Clara.sex_stat("virginity", True) or not Melissa.sex_stat("virginity", True):
        $ scene_runtime.text = "Диван долго сопит обивкой и признает, что условие проклятия уже нельзя выполнить этой парой: обе девушки должны сохранить невинность до ритуала."
    elif str(people.location("clara") or "") != "TavernMain" or str(people.location("melissa") or "") != "TavernMain":
        $ scene_runtime.text = "Диван требует привести Клариссу и Мелиссу вместе в главную залу. Одной девушки или разговоров о них ему недостаточно."
    else:
        $ scene_runtime.text = "Все условия выполнены. Похоже, стоит снова заговорить с диваном."
    $ scene_runtime.location_text = scene_runtime.text
    return


label story_clara_sofa_ritual_3:
    $ main_ui_begin_native_scene_state("Пробуждение дивана")
    show screen main_ui
    $ scene_runtime.text = "Кларисса и Мелисса сначала принимают вашу просьбу за очередную нелепую шутку. Но диван сам приветствует их, жалуется на три века чужих сапог и просит всего лишь сесть рядом. Девушки переглядываются, смеются и одновременно опускаются на подушки."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Обивка вспыхивает теплым золотым светом, резные лапы переступают по полу, и диван с облегчением вытягивается, будто живое существо после долгого сна. Освобожденная душа не покидает мебель: ей, оказывается, понравился трактир. В благодарность она обещает делиться с вами избытком древней жизненной силы. Теперь вы способны кончать еще один дополнительный раз в день."
    $ scene_runtime.location_text = scene_runtime.text
    $ player.intimacy.can_cum_daily += 1
    $ Clara.change_social(friend_delta=2, open_delta=1)
    $ Melissa.change_social(friend_delta=2, open_delta=1)
    menu:
        "Поприветствовать нового жильца":
            pass
    $ event_runtime.active_thread.complete()
    $ main_ui_end_native_scene_state()
    return True


label CursedSofaRepeatStory:
    $ scene_runtime.text = procedural_choice([
        "Диван вспоминает герцога, который двадцать лет хвастался железной волей, но всякий раз засыпал на его подушках раньше, чем слуга успевал снять сапоги.",
        "Диван уверяет, что однажды выиграл спор у стула. На вопрос, как мебель могла спорить, он оскорбленно отвечает, что стул был образованнее большинства придворных.",
        "Диван рассказывает, как его пытались украсть ночью. Воры донесли его до ворот, после чего он начал вслух перечислять их самые постыдные детские прозвища. К утру его вернули на место и даже вытерли пыль.",
    ], "cursed_sofa_repeat_story")
    $ scene_runtime.location_text = scene_runtime.text
    return
