init python:
    class SofaData(PeopleData):
        code_name = "sofa"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Старинный диван",
                fullname="Старинный диван",
                genitive="старинного дивана",
                dative="старинному дивану",
                default_location="",
                description="Неожиданно роскошный для вашего трактира диван. Резные ножки похожи на звериные лапы, а из глубины обивки временами доносится недовольное ворчание.",
                schedule_entries=[NPCScheduleEntry(location="TavernMain")],
            )

        def schedule_resolve(self, weekday_value=None, time_value=None):
            if not Sofa.installed:
                return None
            return super(SofaData, self).schedule_resolve(weekday_value, time_value)

    class SofaInfo(BaseNPC):
        talk_label = "IntSofaTalk"

        def __init__(self, name="sofa", **kwargs):
            super().__init__(name, **kwargs)
            self.data = SofaStaticData
            self.known = True
            self.installed = False

        def update(self):
            super(SofaInfo, self).update()
            self.data = SofaStaticData
            return self


define SofaStaticData = SofaData()
default Sofa = SofaInfo()


label register_sofa_secondary:
    $ people.register(SofaStaticData, Sofa)
    return


label IntSofaTalk:
    $ main_ui_begin_talk_state("Говорящий диван", "sofa")
    vscene resolve_room_background_media(rooms.get("TavernMain"))
    $ scene_runtime.text = SofaStaticData.description
    while True:
        menu:
            "Поговорить с диваном" if story_event_available("CursedSofa", "talk"):
                call checkTriggers("CursedSofa", "talk", 0)
            "Спросить диван о проклятии" if not threads["claraForestSofa"].completed and int(threads["claraForestSofa"].num or 0) == 7 and not story_event_available("CursedSofa", "talk"):
                call CursedSofaRitualRequirements
            "Послушать новую историю" if threads["claraForestSofa"].completed:
                call CursedSofaRepeatStory
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return

label story_clara_sofa_first_talk_6:
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
    elif not tavern.renovation_complete('peephole'):
        $ scene_runtime.text = "Диван требует сначала просверлить потайное окошко в стене гостевой комнаты. Без этого обзорного отверстия Кларисса не считает условленное улучшение трактира законченным."
    elif not tavern.renovation_complete('glory_hole'):
        $ scene_runtime.text = "Диван ворчит, что трактиру все еще не хватает построенного глорихола: именно он должен отвести лишние взгляды от гостевой комнаты во время ритуала."
    elif not Clara.sex_stat("virginity", True) or not Melissa.sex_stat("virginity", True):
        $ scene_runtime.text = "Диван долго сопит обивкой и признает, что условие проклятия уже нельзя выполнить этой парой: обе девушки должны сохранить невинность до ритуала."
    elif str(people.location("clara") or "") != "TavernMain" or str(people.location("melissa") or "") != "TavernMain":
        $ scene_runtime.text = "Диван требует привести Клариссу и Мелиссу вместе в главную залу. Одной девушки или разговоров о них ему недостаточно."
    else:
        $ scene_runtime.text = "Все условия выполнены. Похоже, стоит снова заговорить с диваном."
    $ scene_runtime.location_text = scene_runtime.text
    return


label story_clara_sofa_ritual_7:
    $ main_ui_begin_native_scene_state("Пробуждение дивана")
    show screen main_ui
    $ scene_runtime.text = "Кларисса и Мелисса сначала принимают вашу просьбу за очередную нелепую шутку. Но диван сам приветствует их, жалуется на три века чужих сапог и объясняет настоящее условие: обе должны добровольно доверить вам свою невинность в один вечер. Гостевая комната закрыта, глорихол отвлекает любопытных посетителей, и девушки после короткого разговора вместе соглашаются."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "На старинных подушках Кларисса и Мелисса по очереди принимают вас, поддерживая друг друга и не позволяя страху разрушить добровольное решение. Когда обе перестают быть девственницами, обивка вспыхивает теплым золотым светом, резные лапы переступают по полу, и диван с облегчением вытягивается, будто живое существо после долгого сна.\n\nОсвобожденная душа не покидает мебель: ей понравился трактир. В благодарность она делится с вами избытком древней жизненной силы. Теперь вы способны кончать еще один дополнительный раз в день."
    $ scene_runtime.location_text = scene_runtime.text
    $ Clara.set_sex_stat("virginity", False)
    $ Melissa.set_sex_stat("virginity", False)
    $ Clara.add_sex_stat("sexacts", 1)
    $ Melissa.add_sex_stat("sexacts", 1)
    $ Clara.mark_fucked(1)
    $ Melissa.mark_fucked(1)
    $ Clara.record_sex_history("You", "CursedSofa", "virginity")
    $ Melissa.record_sex_history("You", "CursedSofa", "virginity")
    $ player.intimacy.record_cum(current_game_day())
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
