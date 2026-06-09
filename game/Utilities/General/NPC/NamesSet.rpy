# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import store

    RealName = {
        "sandra": "Сандра",
        "melissa": "Мелисса",
        "amanda": "Аманда",
        "georgett": "Жоржетта",
        "liza": "Лизетта",
        "becky": "Бекки",
        "irma": "Ирма",
        "inga": "Инга",
        "clara": "Кларисса",
        "eddie": "Эдди",
        "gerhard": "Герхард",
        "alber": "Альбер",
        "fran": "Франческа",
        "robin": "Робин",
        "mongol": "Монгол",
        "zimmer": "Циммер",
        "draupnir": "Драупнир",
    }

    AllGirlNames = [
        "sandra",
        "melissa",
        "amanda",
        "georgett",
        "liza",
        "becky",
        "irma",
        "inga",
        "clara",
    ]

    RealName2 = {
        "sandra": "Сандры",
        "melissa": "Мелиссы",
        "amanda": "Аманды",
        "georgett": "Жоржетты",
        "liza": "Лизетты",
        "becky": "Бекки",
        "irma": "Ирмы",
        "inga": "Инги",
        "clara": "Клариссы",
        "eddie": "Эдди",
        "gerhard": "Герхарда",
        "alber": "Альбера",
        "fran": "Франчески",
        "robin": "Робина",
        "mongol": "Монгола",
        "zimmer": "Циммера",
        "draupnir": "Драупнира",
    }

    RealName3 = {
        "sandra": "Сандре",
        "melissa": "Мелиссе",
        "amanda": "Аманде",
        "georgett": "Жоржетте",
        "liza": "Лизетте",
        "becky": "Бекки",
        "irma": "Ирме",
        "inga": "Инге",
        "clara": "Клариссе",
        "eddie": "Эдди",
        "gerhard": "Герхарду",
        "alber": "Альберу",
        "fran": "Франческе",
        "robin": "Робину",
        "mongol": "Монголу",
        "zimmer": "Циммеру",
        "draupnir": "Драупниру",
    }

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
        return renpy.random.choice(OccupationsList)

    def RandomNameCode(gender="", nationality=""):
        if nationality == "":
            nationality = renpy.random.choice(["German", "Italian", "French"])

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
            return renpy.random.choice(fallback)

        return renpy.random.choice(name_list)

    def RandomStreetNameCode(*_args):
        return renpy.random.choice(StreetNameList)

    def RandomStallionNameCode(*_args):
        return renpy.random.choice(StallionName)

label NamesSet:
    return
