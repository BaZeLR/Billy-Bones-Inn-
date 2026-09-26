define NOSTAR_ROSARIO_FIELDS = (
    ("color", "Фасад", (("saffron", "Шафрановый"), ("azure", "Лазурный"), ("crimson", "Багряный"), ("ivory", "Слоновая кость"), ("green", "Зелёный"))),
    ("resident", "Хозяйка", (("dwarf", "Гномья матрона"), ("halfelf", "Полуэльфийка"), ("human", "Человеческая госпожа"), ("goblin", "Гоблинская королева"), ("tiefling", "Тифлинг-колдунья"))),
    ("drink", "Напиток", (("water", "Вода"), ("tea", "Чай"), ("milk", "Молоко"), ("coffee", "Кофе"), ("orange", "Севильский сок"))),
    ("pet", "Питомец", (("fox", "Лиса"), ("horse", "Лошадь"), ("snails", "Пара улиток"), ("hound", "Гончая"), ("chinchilla", "Розарио"))),
    ("implement", "Пристрастие", (("tawse", "Кожаная тавза"), ("ribbons", "Бархатные ленты"), ("cords", "Шёлковые шнуры"), ("collar", "Золотой ошейник"), ("gyves", "Железные кандалы"))),
)

init python:
    class NostarData(PeopleData):
        code_name = "nostar"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Леди Ностар Линк",
                fullname="Леди Ностар Линк",
                genitive="леди Ностар Линк",
                dative="леди Ностар Линк",
                default_location="NostarHouse",
                description="Леди Ностар Линк — богатая, остроумная и своенравная жительница квартала знати. Пропажа её шиншиллы Розарио не даёт ей покоя.",
                portrait="images/nostar/lady_nostar.png",
                schedule_entries=[
                    NPCScheduleEntry(
                        location="NostarHouse",
                        weekdays=[1, 2, 3, 4, 5, 6, 7],
                        start_hour=9,
                        end_hour=21,
                        label="receiving_visitors",
                    ),
                ],
            )

    class NostarInfo(BaseNPC):
        talk_label = "IntNostarTalk"
        unknown_name = "Знатная дама"

        def __init__(self, name="nostar", **kwargs):
            super().__init__(name, **kwargs)
            self.data = NostarStaticData
            self.known = False
            self.rosario_notes = {}

        def rosario_cell(self, field, house):
            return str(getattr(self, "rosario_notes", {}).get(field, {}).get(house, "") or "")

        def set_rosario_cell(self, field, house, value):
            row = next((entry for entry in NOSTAR_ROSARIO_FIELDS if entry[0] == field), None)
            if row is None or house not in range(5) or (value and value not in [code for code, _ in row[2]]):
                return
            if not hasattr(self, "rosario_notes"):
                self.rosario_notes = {}
            notes = self.rosario_notes.setdefault(field, {})
            if value:
                for other_house, other_value in list(notes.items()):
                    if other_house != house and other_value == value:
                        del notes[other_house]
                notes[house] = value
            else:
                notes.pop(house, None)

        def rosario_count(self):
            return sum(bool(self.rosario_cell(field, house)) for field, _, _ in NOSTAR_ROSARIO_FIELDS for house in range(5))

        def rosario_filled(self):
            return self.rosario_count() == 25

        def rosario_answer(self):
            if not self.rosario_filled():
                return ""
            for house in range(5):
                if self.rosario_cell("pet", house) == "chinchilla":
                    return self.rosario_cell("resident", house)
            return ""

        def update(self):
            super(NostarInfo, self).update()
            self.data = NostarStaticData
            return self


define NostarStaticData = NostarData()
default Nostar = NostarInfo()


label register_nostar_secondary:
    $ people.register(NostarStaticData, Nostar)
    return
