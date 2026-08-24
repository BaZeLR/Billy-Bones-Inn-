# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:

    AllGirlNames = [
        "sandra",
        "melissa",
        "amanda",
        "georgett",
        "liza",
        "becky",
        "irma",
        "clara",
    ]

    OccupationsList = [
        "крестьянин",
        "мастеровой",
        "матрос",
        "грузчик",
        "стражник",
        "торговец",
        "горожанин",
        "негр",
    ]

    GermanMaleName = [
        "Питер", "Майкл", "Томас", "Андреас", "Вольфганг", "Клаус", "Юрген",
        "Гюнтер", "Уве", "Вернер", "Хорст", "Франк", "Дитер", "Манфред",
        "Герхардт", "Ганс", "Бернт", "Торстен", "Маттиас", "Гельмут",
        "Вальтер", "Гейнц", "Мартин", "Йорг", "Рольф", "Йенс", "Свен",
        "Александер",
    ]

    GermanFemaleName = [
        "Урсула", "Карин", "Хельга", "Сабина", "Ингрид", "Рената", "Моника",
        "Сюзанна", "Жизель", "Петра", "Бирджит", "Андреа", "Анна", "Бригит",
        "Клаудиа", "Эрика", "Криста", "Эльке", "Стефани", "Гертруда",
        "Элизабет", "Мария", "Хейке", "Габриэла", "Катрин", "Ильза", "Николь",
        "Анхель", "Барбара",
    ]

    FrenchMaleName = [
        "Жан", "Мишель", "Филипп", "Алан", "Патрик", "Пьер", "Николас",
        "Кристоф", "Кристиан", "Даниель", "Бернар", "Эрик", "Фредерик",
        "Лаурен", "Стефан", "Паскаль", "Себастьен", "Давид", "Жерар", "Тьер",
        "Жульен", "Оливер", "Жак", "Александр", "Тома", "Клод", "Дидье",
        "Франсуа", "Доминик", "Винсент",
    ]

    FrenchFemaleName = [
        "Мари", "Натали", "Изабель", "Сильви", "Катерина", "Франсуаза",
        "Мартина", "Кристина", "Моник", "Валери", "Сандрина", "Вероника",
        "Николь", "Стефани", "Софи", "Анна", "Шантал", "Селин", "Патрисия",
        "Бриджит", "Анни", "Жюли", "Аурель", "Лорен", "Кристиана", "Жаклин",
        "Доминик", "Вирджиния", "Мишель", "Корин",
    ]

    NegrMaleName = [
        "Мнгуни", "Лузумана", "Маландела", "Зулу", "Пунга", "Магеба", "Ндаба",
        "Джама", "Сензангакона", "Чака", "Дингане", "Мпанде", "Кечвайо",
        "Динузулу",
    ]

    ItalianMaleName = [
        "Джузеппе", "Антонио", "Джованни", "Франческо", "Марио", "Луиджи",
        "Сальваторе", "Винсенто", "Анджело", "Роберто", "Пьетро", "Паоло",
        "Доменико", "Франко", "Карло", "Мишель", "Бруно", "Джорджио",
        "Сергио", "Люциано", "Марко", "Паскаль", "Николя", "Клаудио",
        "Массимо", "Андреа", "Стефано", "Алессандро", "Алберто", "Маурицио",
    ]

    ItalianFemaleName = [
        "Мария", "Анна", "Роза", "Джузеппина", "Анджела", "Джованна", "Люция",
        "Анна Мария", "Франческа", "Тереза", "Паола", "Кармела", "Катерина",
        "Лаура", "Рита", "Антуанетта", "Карла", "Патриция", "Конкетта",
        "Елена", "Даниэла", "Франка", "Антония", "Сильвана", "Маргерита",
        "Габриела", "Антонелла", "Луиза", "Мария Тереза",
    ]

    StreetNameList = [
        "пекарей",
        "кожевенников",
        "мясников",
        "шорников",
        "бочкарей",
        "шляпников",
        "портных",
    ]

    StallionName = [
        "Алегаро ", "Ангел ", "Виски ", "Галс ", "Гектор ", "Геликон ",
        "Гладиатор ", "Голкипер ", "Графит ", "Дамеон ", "Данат",
        "Единорог ", "Жибек ", "Жокер ", "Зуфар ", "Иллан ", "Иллис ",
        "Иракли ", "Кальваро ", "Камелот ", "Капрал ", "Касмир ", "Купер ",
        "Лакей ", "Лацио ", "Ленси ", "Мажор ", "Меррик ", "Орион ",
        "Орфей ", "Пабло ", "Радужный ", "Рико ", "Риф ", "Романтик  ",
        "Сократ ", "Фаворит ", "Фактор ", "Феникс ", "Феномен ", "Флеш ",
        "Хакан ", "Хигир ", "Чек ", "Чудо ", "Шармен ", "Энем ",
    ]

    def RandomOccupCode(*_args):
        return procedural_choice(OccupationsList, key="procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:165:1")

    def RandomNameCode(gender="", nationality=""):
        if nationality == "":
            nationality = procedural_choice(["German", "Italian", "French"], key="procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:169:2")

        suffix = "MaleName" if str(gender).lower() == "male" else "FemaleName"
        name_map = {
            "GermanMaleName": GermanMaleName,
            "GermanFemaleName": GermanFemaleName,
            "FrenchMaleName": FrenchMaleName,
            "FrenchFemaleName": FrenchFemaleName,
            "ItalianMaleName": ItalianMaleName,
            "ItalianFemaleName": ItalianFemaleName,
        }
        list_name = nationality + suffix
        name_list = name_map.get(list_name, [])

        if not name_list:
            fallback = GermanMaleName if suffix == "MaleName" else GermanFemaleName
            return procedural_choice(fallback, key="procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:185:3")

        return procedural_choice(name_list, key="procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:187:4")

    def RandomStreetNameCode(*_args):
        return procedural_choice(StreetNameList, key="procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:190:5")

    def RandomStallionNameCode(*_args):
        return procedural_choice(StallionName, key="procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:193:6")

label NamesSet:
    return
