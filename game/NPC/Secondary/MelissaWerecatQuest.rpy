    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(CurLoc or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(calendar_v2.daysInGame or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True
    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(dayspassed or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True
label WerecatHunterClubTease:
    $ werecat_state()["hunter_tease_day"] = int(dayspassed or 0)
    $ werecat_state()["hunter_tease_offer_ready"] = 0
    $ MainTxt = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ CurLocDesc = MainTxt
    vscene werecat_info_picture_path()
    "[MainTxt]"
    call HunterClubBuildActions
    return

    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(CurLoc or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(calendar_v2.daysInGame or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True
    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(dayspassed or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True
label WerecatHunterClubTease:
    $ werecat_state()["hunter_tease_day"] = int(dayspassed or 0)
    $ werecat_state()["hunter_tease_offer_ready"] = 0
    $ MainTxt = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ CurLocDesc = MainTxt
    vscene werecat_info_picture_path()
    "[MainTxt]"
    call HunterClubBuildActions
    return

    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(CurLoc or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(calendar_v2.daysInGame or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True
    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(dayspassed or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True
label WerecatHunterClubTease:
    $ werecat_state()["hunter_tease_day"] = int(dayspassed or 0)
    $ werecat_state()["hunter_tease_offer_ready"] = 0
    $ MainTxt = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ CurLocDesc = MainTxt
    vscene werecat_info_picture_path()
    "[MainTxt]"
    call HunterClubBuildActions
    return

# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -1 python:
    import renpy.exports as renpy

    def werecat_info_picture_path():
        for picture_path in (
            "images/hunt/kitty_1.png",
            "images/hunt/kitty free.png",
            "images/hunt/hunt.png",
            "images/general/hunter_store_catInfo.png",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def werecat_caught_picture_path():
        for picture_path in (
            "images/hunt/kitty_trapped.png",
            "images/hunt/kitty_1.png",
            "images/hunt/kitty free.png",
            "images/hunt/hunt.png",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def werecat_name_value():
        return str(werecat_state().get("name", "") or "").strip()

    def werecat_display_name():
        return werecat_name_value() or "оборотница-кошка"

    def werecat_hunter_rumor_seen():
        return int(werecat_state().get("hunter_tease_day", -1) or -1) >= 0

    def werecat_adopted_count():
        count_value = int(werecat_state().get("adopted_count", 0) or 0)
        if int(werecat_state().get("adopted", 0) or 0) == 1:
            count_value = max(1, count_value)
        werecat_state()["adopted_count"] = count_value
        return count_value

    def werecat_first_home_exists():
        return int(werecat_state().get("sold", 0) or 0) == 0 and werecat_adopted_count() >= 1

    def werecat_second_gift_available():
        return werecat_first_home_exists() and int(werecat_state().get("gifted_clara", 0) or 0) == 0

    def werecat_apply_clara_gift_bonus():
        werecat_state()["caught"] = 0
        werecat_state()["gifted_clara"] = 1
        werecat_state()["clara_gift_day"] = int(dayspassed or 0)
        Clara.change_social(friend_delta=3, open_delta=2, corruption_delta=4)
        Clara.stats["PussyWetStart"] = max(35, int(Clara.stats.get("PussyWetStart", 0) or 0) + 15)
        Clara.var["werecat_gifted"] = 1
        Clara.var["werecat_gift_day"] = int(calendar_v2.daysInGame or 0)
        Clara.var["werecat_gifted"] = 1
        Clara.var["werecat_gift_day"] = int(dayspassed or 0)
        Clara.var["werecat_gifted"] = 1
        Clara.var["werecat_gift_day"] = int(calendar_v2.daysInGame or 0)
        Clara.var["werecat_gifted"] = 1
        Clara.var["werecat_gift_day"] = int(dayspassed or 0)
        Clara.var["werecat_gifted"] = 1
        Clara.var["werecat_gift_day"] = int(calendar_v2.daysInGame or 0)
        Clara.var["werecat_gifted"] = 1
        Clara.var["werecat_gift_day"] = int(dayspassed or 0)

    def werecat_month_thanks_ready():
        adopted_day = int(werecat_state().get("adopted_day", -1) or -1)
        return (
            int(werecat_state().get("adopted", 0) or 0) == 1
            and int(werecat_state().get("adoption_breakfast_seen", 0) or 0) == 1
            and adopted_day >= 0
            and day_delta_ready(adopted_day, 30)
            and int(werecat_state().get("first_month_thanks_day", -1) or -1) < adopted_day + 30
            and not bool(player.tavern_management.breakfast.today)
        )

    def werecat_adoption_breakfast_ready():
        adopted_day = int(werecat_state().get("adopted_day", -1) or -1)
        return (
            int(werecat_state().get("adopted", 0) or 0) == 1
            and int(werecat_state().get("adoption_breakfast_seen", 0) or 0) == 0
            and adopted_day >= 0
            and day_delta_ready(adopted_day, 1)
            and not bool(player.tavern_management.breakfast.today)
        )

    def werecat_rat_breakfast_ready():
        return (
            int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(werecat_state().get("rat_breakfast_seen", 0) or 0) == 0
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and day_delta_ready(Melissa.var.get("storage_rat_last_help_day", -1), 1)
            and not bool(player.tavern_management.breakfast.today)
        )

    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(CurLoc or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(CurLoc or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(calendar_v2.daysInGame or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True

    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(CurLoc or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(calendar_v2.daysInGame or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True

    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(CurLoc or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        werecat_state()["hunter_tease_offer_day"] = int(calendar_v2.daysInGame or 0)
        werecat_state()["hunter_tease_offer_ready"] = 1
        return True

    def werecat_can_track_here(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        return room_key in ("Forest", "ForestClearing", "ForestHiddenPath", "ForestWaterfall", "ForestDarkWoods", "ForestLake", "ForestSpring")

    def werecat_can_search(room_code=""):
        if not werecat_can_track_here(room_code):
            return False
        if int(werecat_state().get("caught", 0) or 0) == 1:
            return False
        if int(werecat_state().get("sold", 0) or 0) == 1 and not werecat_first_home_exists():
            return False
        if werecat_first_home_exists():
            return int(werecat_state().get("gifted_clara", 0) or 0) == 0
        return (
            int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 1
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
        )

    def werecat_trap_rooms():
        trap_rows = werecat_state().get("trap_rooms", {})
        if not isinstance(trap_rows, dict):
            trap_rows = {}
        legacy_room = str(werecat_state().get("trap_room", "") or "").strip()
        if legacy_room and int(werecat_state().get("trap_active", 0) or 0) == 1 and legacy_room not in trap_rows:
            trap_rows[legacy_room] = {"day": int(werecat_state().get("trap_day", -1) or -1)}
        werecat_state()["trap_rooms"] = dict(trap_rows)
        werecat_state()["trap_active"] = 1 if len(trap_rows) > 0 else 0
        if len(trap_rows) > 0 and not legacy_room:
            first_room = sorted(trap_rows.keys())[0]
            werecat_state()["trap_room"] = first_room
            werecat_state()["trap_day"] = int(dict(trap_rows.get(first_room, {}) or {}).get("day", -1) or -1)
        elif len(trap_rows) <= 0:
            werecat_state()["trap_room"] = ""
            werecat_state()["trap_day"] = -1
        return dict(trap_rows)

    def werecat_can_set_bait(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        trap_rows = werecat_trap_rooms()
        return (
            werecat_can_search(room_key)
            and int(werecat_state().get("tracks_seen", 0) or 0) == 1
            and int(player.item_count("hunting_trap_001") or 0) > 0
            and room_key not in trap_rows
        )

    def werecat_can_check_bait(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        trap_rows = werecat_trap_rooms()
        return (
            room_key in trap_rows
            and int(werecat_state().get("caught", 0) or 0) == 0
            and int(dayspassed or 0) > int(dict(trap_rows.get(room_key, {}) or {}).get("day", -1) or -1)
        )

    def werecat_trap_success_chance():
        exploration_value = max(int(werecat_state().get("woods_exploration", 0) or 0), int(effective_player_exploration() or 0))
        if exploration_value >= 200:
            return 100
        if exploration_value >= 150:
            return 75
        if exploration_value >= 100:
            return 45
        if exploration_value >= 75:
            return 25
        return 0

    def werecat_register_search(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        gain = procedural_randint(10, 25, "werecat_search_%s_%s" % (room_key, int(dayspassed or 0)))
        total = max(int(werecat_state().get("woods_exploration", 0) or 0), int(effective_player_exploration() or 0)) + gain
        werecat_state()["woods_exploration"] = total
        if not werecat_hunter_rumor_seen():
            return {
                "gain": gain,
                "found_tracks": False,
                "text": "Следов в лесу хватает, но без наводки вы пока не понимаете, какие из них стоит считать по-настоящему странными. Похоже, сначала надо услышать хоть что-то конкретнее, чем одни только смутные трактирные разговоры.",
            }
        werecat_state()["tracks_seen"] = 1
        werecat_state()["tracks_room"] = room_key
        if werecat_first_home_exists():
            return {
                "gain": gain,
                "found_tracks": True,
                "text": "Теперь, зная повадки первой лесной кошки, вы замечаете больше: свежие следы идут иначе, шерсть на ветках темнее, а запах чужой. Похоже, в этих местах бродит еще одна такая тварь. Ее тоже можно брать ловушкой.",
            }
        if int(werecat_state().get("tracks_seen", 0) or 0) == 1 and int(werecat_state().get("tracks_first_text_seen", 0) or 0) == 0:
            werecat_state()["tracks_first_text_seen"] = 1
            return {
                "gain": gain,
                "found_tracks": True,
                "text": "Вы натыкаетесь на странный след: в сырой земле отпечатались кошачьи лапы, а рядом будто на миг проступил почти человеческий босой шаг. Между корней зацепились мягкие блестящие клочки шерсти, слишком нежные для обычного зверя. Похоже, здесь и правда шастает нечто куда любопытнее простой лесной кошки.",
            }
        return {
            "gain": gain,
            "found_tracks": True,
            "text": "Вы снова находите признаки странной кошачьей твари: свежие отпечатки, примятую траву и тонкий клочок мягкой шерсти. Следы ведут через эту часть леса, так что здесь тоже можно ставить ловушку.",
        }


label MelissaRatBreakfastScene:
    $ werecat_state()["rat_breakfast_seen"] = 1
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = int(dayspassed or 0)
    $ player.tavern_management.breakfast.day = int(dayspassed or 0)
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ MainTxt = "Мягкий утренний свет ползет по кухне, в мисках парит каша, воздух пахнет молоком, овсом и горячим хлебом. За общим столом сегодня сидят все трое.\n\nСандра, помешивая кашу с лишней силой, первой возвращается к вчерашнему: \"Крысы в доме совсем распоясались. Уже по три полных тюка припасов за неделю портят. Если так пойдет дальше, к зиме сами у пустых мешков сядем.\"\n\nАманда разваливается на скамье и, как всегда, пытается рассечь тревогу шуткой: \"А знаешь, чего этому дому по-настоящему не хватает? Хорошей сильной киски. Такой, чтоб и мышей ловила, и с вредителями умела разбираться как следует.\" Она лукаво подмигивает.\n\nМелисса сперва краснеет, потом все же хихикает: \"Да... большой, гибкой охотницы. Чтобы маленьких пакостников душила без жалости... и ночами было бы с кем согреться.\"\n\nСмех за столом быстро снимает лишнее напряжение. Даже Сандра, отвернувшись к котлу, ворчит уже заметно мягче."
    if relationship_anger("amanda") > 0 and relationship_anger("melissa") > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nАманда и Мелисса все равно успевают уколоть друг друга. Сандра сразу обрывает их: \"Когти оставьте для крыс. За столом не шипеть.\""
    elif relationship_anger("amanda") > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nАманда шутит привычно, но сегодня в каждой шутке достается именно Мелиссе. Та краснеет, но не опускает глаза."
    elif relationship_anger("melissa") > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nМелисса смеется вместе со всеми, но на амандины насмешки отвечает коротко и зло. Еще одно слово, и завтрак снова скатится в спор."
    $ CurLocDesc = MainTxt
    $ fun = _player_clamp(int(fun or 0) + 5, 0, 100)
    $ Sandra.change_social(friend_delta=1)
    $ Melissa.add_trust(1)
    $ Amanda.change_social(friend_delta=1)
    $ TavernKitchenSavedText = MainTxt
    call stat
    return


label WerecatAdoptionBreakfastScene:
    $ werecat_state()["adoption_breakfast_seen"] = 1
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = int(dayspassed or 0)
    $ player.tavern_management.breakfast.day = int(dayspassed or 0)
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ MainTxt = "За завтраком сегодня разговор быстро сворачивает к новой обитательнице трактира. У самого очага, настороженно щурясь, устроилась ваша необычная лесная кошка, и даже с такого расстояния видно, что она следит за каждым шорохом куда внимательнее обычного зверя.\n\nСандра первой признает очевидное: \"В кладовой ночью впервые было тихо. Если эта хвостатая и правда останется у нас, припасы хоть поживут спокойно.\" Аманда тут же расплывается в ухмылке: \"Говорила же, дому нужна хорошая киска. А эта еще и красавица, не только охотница.\" Мелисса тихо фыркает, но спорить не спешит: \"Главное, чтобы она крыс душила так же ловко, как на всех смотрит.\"\n\nПохоже, в трактире уже начинают принимать вашу странную добычу как свою. История на этом не кончается, но теперь у нее наконец есть продолжение дома, а не только в лесу."
    if relationship_anger("amanda") > 0 and relationship_anger("melissa") > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nАманда и Мелисса опять начинают цеплять друг друга, но кошка вдруг шипит от очага, и обе замолкают. Сандра только хмыкает: \"Вот. Даже зверю надоело.\""
    elif relationship_anger("amanda") > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nАманда цепляет Мелиссу за каждую реплику о кошке. Мелисса держится, но губы у нее сжаты."
    elif relationship_anger("melissa") > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nМелисса сегодня не дает Аманде разгуляться. На каждую шутку отвечает сухо, и Сандра быстро переводит разговор обратно к кладовой."
    $ CurLocDesc = MainTxt
    $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ Sandra.change_social(friend_delta=1)
    $ Melissa.add_trust(1)
    $ Amanda.change_social(friend_delta=1)
    $ TavernKitchenSavedText = MainTxt
    return


label WerecatMonthThanksScene:
    $ werecat_state()["first_month_thanks_day"] = int(dayspassed or 0)
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = int(dayspassed or 0)
    $ player.tavern_management.breakfast.day = int(dayspassed or 0)
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    vscene tavern_kitchen_breakfast_picture()
    $ MainTxt = "За общим столом сегодня куда спокойнее обычного. В кладовой уже давно не слышно прежней возни, а у самого очага, свернувшись теплым клубком, дремлет ваша необычная кошка.\n\nСандра первой нарушает молчание: \"Эта малышка и правда спасла нам припасы. Если бы не она, мы бы еще долго слушали шорох в мешках и считали, сколько еды уходит в никуда.\" Потом она смотрит уже прямо на вас и говорит мягче: \"Хорошее дело вы все-таки сделали. Такой зверь дому в радость.\"\n\nОстальные тоже заметно теплеют. Даже обычная утренняя суета сегодня кажется куда уютнее."
    if Melissa.bats_stage() >= 6:
        $ MainTxt = str(MainTxt or "") + "\n\nПосле короткой паузы Сандра добавляет уже совсем иначе: \"А ту глупую историю с чердаком пора бы и отпустить. Дом у нас старый, люди живые, а дурных случаев без того хватает. Главное, что теперь ты не отмахнулся от настоящей беды и довел дело до ума.\" Похоже, за столом наконец начинают считать тот позорный случай скорее нелепостью, чем клеймом."
    $ CurLocDesc = MainTxt
    $ Sandra.change_social(friend_delta=1)
    $ Melissa.add_trust(1)
    $ Amanda.change_social(friend_delta=1)
    $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ TavernKitchenSavedText = MainTxt
    return


label WerecatHunterClubTease:
    $ werecat_state()["hunter_tease_day"] = int(calendar_v2.daysInGame or 0)
    $ werecat_state()["hunter_tease_offer_ready"] = 0
    $ MainTxt = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ CurLocDesc = MainTxt
    vscene werecat_info_picture_path()
    "[MainTxt]"
    call HunterClubBuildActions
    return


label WerecatHunterClubTease:
    $ werecat_state()["hunter_tease_day"] = int(calendar_v2.daysInGame or 0)
    $ werecat_state()["hunter_tease_offer_ready"] = 0
    $ MainTxt = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ CurLocDesc = MainTxt
    vscene werecat_info_picture_path()
    "[MainTxt]"
    call HunterClubBuildActions
    return


label WerecatHunterClubTease:
    $ werecat_state()["hunter_tease_day"] = int(calendar_v2.daysInGame or 0)
    $ werecat_state()["hunter_tease_offer_ready"] = 0
    $ MainTxt = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ CurLocDesc = MainTxt
    vscene werecat_info_picture_path()
    "[MainTxt]"
    call HunterClubBuildActions
    return


label WerecatSetTrap(room_code=""):
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    if not werecat_can_set_bait(_werecat_room):
        $ MainTxt = "Сейчас вы не можете устроить здесь такую приманку."
        $ CurLocDesc = MainTxt
        if _werecat_room == "Forest":
            call ForestBuildActions
        else:
            call ForestSubroomBuildActions
        return
    $ player.remove_item("hunting_trap_001", 1)
    $ _werecat_trap_rooms = werecat_trap_rooms()
    $ _werecat_trap_rooms[_werecat_room] = {"day": int(dayspassed or 0)}
    $ werecat_state()["trap_rooms"] = dict(_werecat_trap_rooms)
    $ werecat_state()["trap_active"] = 1
    $ werecat_state()["trap_room"] = _werecat_room
    $ werecat_state()["trap_day"] = int(dayspassed or 0)
    $ werecat_state()["trap_active"] = 1
    $ werecat_state()["trap_room"] = _werecat_room
    $ werecat_state()["trap_day"] = int(dayspassed or 0)
    $ werecat_state()["trap_active"] = 1
    $ werecat_state()["trap_room"] = _werecat_room
    $ werecat_state()["trap_day"] = int(dayspassed or 0)
    $ MainTxt = "Вы ставите охотничью ловушку там, где нашли странные следы, и тщательно маскируете ее листвой. Если слухи не врут, сюда должно прийти нечто куда умнее обычного зверя."
    $ CurLocDesc = MainTxt
    if _werecat_room == "Forest":
        call ForestBuildActions
    else:
        call ForestSubroomBuildActions
    return


label WerecatCheckTrap(room_code=""):
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    if not werecat_can_check_bait(_werecat_room):
        $ MainTxt = "Проверять здесь пока нечего."
        $ CurLocDesc = MainTxt
        if _werecat_room == "Forest":
            call ForestBuildActions
        else:
            call ForestSubroomBuildActions
        return
    $ _werecat_trap_rooms = werecat_trap_rooms()
    $ _werecat_trap_rooms.pop(_werecat_room, None)
    $ werecat_state()["trap_rooms"] = dict(_werecat_trap_rooms)
    $ werecat_state()["trap_active"] = 1 if len(_werecat_trap_rooms) > 0 else 0
    $ werecat_state()["trap_room"] = sorted(_werecat_trap_rooms.keys())[0] if len(_werecat_trap_rooms) > 0 else ""
    $ werecat_state()["trap_day"] = int(dict(_werecat_trap_rooms.get(werecat_state()["trap_room"], {}) or {}).get("day", -1) or -1) if len(_werecat_trap_rooms) > 0 else -1
    $ werecat_state()["trap_active"] = 1 if len(_werecat_trap_rooms) > 0 else 0
    $ werecat_state()["trap_room"] = sorted(_werecat_trap_rooms.keys())[0] if len(_werecat_trap_rooms) > 0 else ""
    $ werecat_state()["trap_day"] = int(dict(_werecat_trap_rooms.get(werecat_state()["trap_room"], {}) or {}).get("day", -1) or -1) if len(_werecat_trap_rooms) > 0 else -1
    $ werecat_state()["trap_active"] = 1 if len(_werecat_trap_rooms) > 0 else 0
    $ werecat_state()["trap_room"] = sorted(_werecat_trap_rooms.keys())[0] if len(_werecat_trap_rooms) > 0 else ""
    $ werecat_state()["trap_day"] = int(dict(_werecat_trap_rooms.get(werecat_state()["trap_room"], {}) or {}).get("day", -1) or -1) if len(_werecat_trap_rooms) > 0 else -1
    $ werecat_state()["trap_active"] = 1 if len(_werecat_trap_rooms) > 0 else 0
    $ werecat_state()["trap_room"] = sorted(_werecat_trap_rooms.keys())[0] if len(_werecat_trap_rooms) > 0 else ""
    $ werecat_state()["trap_day"] = int(dict(_werecat_trap_rooms.get(werecat_state()["trap_room"], {}) or {}).get("day", -1) or -1) if len(_werecat_trap_rooms) > 0 else -1
    $ werecat_state()["trap_active"] = 1 if len(_werecat_trap_rooms) > 0 else 0
    $ werecat_state()["trap_room"] = sorted(_werecat_trap_rooms.keys())[0] if len(_werecat_trap_rooms) > 0 else ""
    $ werecat_state()["trap_day"] = int(dict(_werecat_trap_rooms.get(werecat_state()["trap_room"], {}) or {}).get("day", -1) or -1) if len(_werecat_trap_rooms) > 0 else -1
    $ werecat_state()["trap_active"] = 1 if len(_werecat_trap_rooms) > 0 else 0
    $ werecat_state()["trap_room"] = sorted(_werecat_trap_rooms.keys())[0] if len(_werecat_trap_rooms) > 0 else ""
    $ werecat_state()["trap_day"] = int(dict(_werecat_trap_rooms.get(werecat_state()["trap_room"], {}) or {}).get("day", -1) or -1) if len(_werecat_trap_rooms) > 0 else -1
    if procedural_randint(1, 100, "werecat_trap_%s_%s" % (_werecat_room, int(dayspassed or 0))) > werecat_trap_success_chance():
        $ MainTxt = "К приманке кто-то подходил: земля примята, кости растащены, на ветке опять висит мягкий блестящий клочок шерсти. Но сама тварь оказалась слишком осторожной и ушла, едва вы приблизились."
        $ CurLocDesc = MainTxt
        if _werecat_room == "Forest":
            call ForestBuildActions
        else:
            call ForestSubroomBuildActions
        return
    $ werecat_state()["caught"] = 1
    $ MainTxt = "В тени между деревьями вы замечаете ее почти сразу. Не зверя и не женщину, а странную, тревожно красивую смесь обоих. Кошачьи уши вздрагивают от каждого звука, пушистый хвост нервно ходит из стороны в сторону, по плечам и бедрам легли тонкие узоры мягкой шерсти, а глаза у нее золотые, настороженные и слишком умные для простой лесной твари. Она явно напугана, но не шипит и не бросается, только смотрит так, будто еще сама не решила, считать ли вас охотником или спасением."
    $ CurLocDesc = MainTxt
    vscene werecat_caught_picture_path()
    "[MainTxt]"
    if werecat_second_gift_available():
        menu:
            "Что сделать?"
            "Подарить ее Клариссе":
                $ werecat_apply_clara_gift_bonus()
                $ MainTxt = "Вы решаете, что второй лесной кошке лучше не тесниться в трактире, а стать подарком для Клариссы. Такой редкий живой подарок она точно поймет: не безделушка, а полезная, красивая и опасная спутница. После этого Кларисса смотрит на вас теплее обычного, будто подарок попал именно туда, куда нужно."
                $ CurLocDesc = MainTxt
                call stat
            "Отпустить":
                $ werecat_state()["caught"] = 0
                $ werecat_state()["tracks_seen"] = 1
                $ werecat_state()["tracks_first_text_seen"] = 1
                $ MainTxt = "Вы осторожно освобождаете пойманную тварь и отходите, давая ей путь к лесу. Она исчезает между стволами почти бесшумно, но теперь вы точно знаете: в этих местах есть не только одна такая кошка."
                $ CurLocDesc = MainTxt
    else:
        menu:
            "Что сделать?"
            "Забрать ее домой":
                $ werecat_state()["adopted"] = 1
                $ werecat_state()["adopted_count"] = max(1, int(werecat_state().get("adopted_count", 0) or 0))
                $ werecat_state()["caught"] = 0
                $ werecat_state()["rats_problem_active"] = 0
                $ werecat_state()["rat_food_loss_next_day"] = -1
                $ werecat_state()["name"] = "Луна"
                $ werecat_state()["adopted_day"] = int(dayspassed or 0)
                $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 2
                $ charisma = min(100, int(charisma or 0) + 15)
                $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
                $ Sandra.change_social(friend_delta=1)
                $ Melissa.add_trust(1)
                $ Amanda.change_social(friend_delta=1)
                $ Sandra.rebel_baseline = max(0, int(Sandra.rebel_baseline or 0) - 1)
                $ Melissa.rebel_baseline = max(0, int(Melissa.rebel_baseline or 0) - 1)
                $ Amanda.rebel_baseline = max(0, int(Amanda.rebel_baseline or 0) - 1)
                $ _werecat_pet_state = werecat_pet_state()
                $ _werecat_pet_state["trust"] = max(6, int(_werecat_pet_state.get("trust", 0) or 0))
                $ _werecat_pet_state["comfort"] = max(8, int(_werecat_pet_state.get("comfort", 0) or 0))
                $ npc_daily_schedule_build_all(True)
                $ MainTxt = "Вы не тянете поводок, не орете и не делаете резких движений. Просто тихо уводите странную лесную кошку с собой, будто она сама уже наполовину решила вам довериться. Дом быстро принимает ее как новую, немного диковатую, но полезную тварь. В кладовых с этого дня становится спокойнее: теперь у крыс появился настоящий враг."
                $ CurLocDesc = MainTxt
                call stat
            "Продать работорговцам за 5000":
                $ werecat_state()["caught"] = 0
                $ werecat_state()["sold"] = 1
                $ money = int(money or 0) + 5000
                $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) - 3
                $ Sandra.change_social(friend_delta=-2)
                $ Melissa.add_trust(-3)
                $ Amanda.change_social(friend_delta=-2)
                $ MainTxt = "Вы выбираете самый жесткий и самый выгодный путь. За такую необычную добычу быстро дают большие деньги, но запах этой сделки остается при вас надолго. Крысы в доме от этого, разумеется, никуда не деваются."
                $ CurLocDesc = MainTxt
                call stat
    jump ForestRestore
