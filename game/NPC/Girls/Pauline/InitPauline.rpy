init python:
    class PaulineData(PeopleData):
        code_name = "pauline"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Полина",
                fullname="Полина",
                genitive="Полины",
                dative="Полине",
                description="Полина — взрослая воспитанница пансиона Элоизы, приехавшая из далёкой деревни. Пока Кларисса живёт в трактире, Полина помогает в винной лавке.",
                birth_date={"day": 1, "period": 1, "cycle": 1082},
                # No separate Pauline portrait has been approved yet.
                portrait="#000",
                base_clothing={"day_dress": "modestworkdress", "bra": "simplebra", "panties": "simplepanties", "legs": "", "shoes": "simpleshoes"},
                schedule_entries=[
                    NPCHourScheduleEntry(
                        npc_id=self.code_name,
                        location="WineStore",
                        follows_room_schedule=True,
                        working=True,
                        condition={"rule": "clara_tavern_resident"},
                        label="wine_store_replacement",
                        source="rpy",
                    ),
                ],
            )

    class PaulineInfo(Girl):
        talk_label = "IntPaulineTalk"
        unknown_name = "Новая продавщица"
        work_socializing_locations = ("WineStore",)

        def __init__(self):
            super().__init__("pauline")
            self.data = PaulineStaticData
            self.stats = {}
            self.wardrobe = GirlWardrobeState.from_base(self.data.base_clothing)

        def update(self):
            super(PaulineInfo, self).update()
            self.data = PaulineStaticData
            return self


define PaulineStaticData = PaulineData()
default Pauline = PaulineInfo()

label InitPauline:
    $ people.register(PaulineStaticData, Pauline)
    return


label IntPaulineTalk:
    if str(people.location("pauline") or "") != "WineStore" or not rooms.get("WineStore").is_open():
        return
    $ main_ui_begin_talk_state("Разговор с Полиной", "pauline")
    show screen main_ui
    vscene PaulineStaticData.portrait
    if not Pauline.known:
        $ Pauline.mark_known()
        $ scene_runtime.text = "— Меня зовут Полина. Пока Кларисса живёт у вас, здесь буду помогать я, — представляется девушка. — За вином пришли? Бочки на прежнем месте."
    else:
        $ scene_runtime.text = "— Здравствуйте, Стефан. Вино для трактира понадобилось? — Полина откладывает записи и поворачивается к вам."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Назад":
            pass
    $ main_ui_end_talk_state()
    return
