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
        return count_value

    def werecat_first_home_exists():
        return int(werecat_state().get("sold", 0) or 0) == 0 and werecat_adopted_count() >= 1

    def werecat_second_gift_available():
        return werecat_first_home_exists() and int(werecat_state().get("gifted_clara", 0) or 0) == 0

    def werecat_apply_clara_gift_bonus():
        werecat_state()["caught"] = 0
        werecat_state()["gifted_clara"] = 1
        werecat_state()["clara_gift_day"] = current_game_day()
        Clara.change_social(friend_delta=3, open_delta=2, corruption_delta=4)
        Clara.stats["PussyWetStart"] = max(35, int(Clara.stats.get("PussyWetStart", 0) or 0) + 15)

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
            and people_to_int(Melissa.storage_rat_help_day, -1) >= 0
            and day_delta_ready(Melissa.storage_rat_help_day, 1)
            and not bool(player.tavern_management.breakfast.today)
        )

    def werecat_hunter_tease_ready():
        if werecat_first_home_exists():
            return False
        return (
            str(rooms.current_code or "") == "HunterClub"
            and int(werecat_state().get("rats_problem_active", 0) or 0) == 1
            and people_to_int(Melissa.storage_rat_help_day, -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_can_track_here(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
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
            and people_to_int(Melissa.storage_rat_help_day, -1) >= 0
            and int(werecat_state().get("adopted", 0) or 0) == 0
            and int(werecat_state().get("sold", 0) or 0) == 0
        )

    def werecat_trap_rooms():
        trap_rows = werecat_state().get("trap_rooms", {})
        try:
            return dict(trap_rows or {})
        except (TypeError, ValueError):
            return {}

    def werecat_can_set_bait(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        trap_rows = werecat_trap_rooms()
        return (
            werecat_can_search(room_key)
            and int(werecat_state().get("tracks_seen", 0) or 0) == 1
            and int(player.item_count("hunting_trap_001") or 0) > 0
            and room_key not in trap_rows
        )

    def werecat_can_check_bait(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        trap_rows = werecat_trap_rooms()
        return (
            room_key in trap_rows
            and int(werecat_state().get("caught", 0) or 0) == 0
            and current_game_day() > int(dict(trap_rows.get(room_key, {}) or {}).get("day", -1) or -1)
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
        room_key = str(room_code or rooms.current_code or "").strip()
        gain = procedural_randint(10, 25, "werecat_search_%s_%s" % (room_key, current_game_day()))
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


label WerecatSetTrap(room_code=""):
    $ renpy.dynamic("_werecat_room", "_werecat_trap_rooms")
    $ _werecat_room = str(room_code or rooms.current_code or "").strip()
    if not werecat_can_set_bait(_werecat_room):
        $ scene_runtime.text = "Сейчас вы не можете устроить здесь такую приманку."
        $ scene_runtime.location_text = scene_runtime.text
        if _werecat_room == "Forest":
            $ main_ui_runtime.action_items = forest_action_items()
        else:
            $ main_ui_runtime.action_items = forest_subroom_action_items()
        return
    $ player.remove_item("hunting_trap_001", 1)
    $ _werecat_trap_rooms = werecat_trap_rooms()
    $ _werecat_trap_rooms[_werecat_room] = {"day": current_game_day()}
    $ werecat_state()["trap_rooms"] = dict(_werecat_trap_rooms)
    $ scene_runtime.text = "Вы ставите охотничью ловушку там, где нашли странные следы, и тщательно маскируете ее листвой. Если слухи не врут, сюда должно прийти нечто куда умнее обычного зверя."
    $ scene_runtime.location_text = scene_runtime.text
    if _werecat_room == "Forest":
        $ main_ui_runtime.action_items = forest_action_items()
    else:
        $ main_ui_runtime.action_items = forest_subroom_action_items()
    return


label WerecatCheckTrap(room_code=""):
    $ renpy.dynamic("_werecat_room", "_werecat_trap_rooms", "_werecat_pet_state")
    $ _werecat_room = str(room_code or rooms.current_code or "").strip()
    if not werecat_can_check_bait(_werecat_room):
        $ scene_runtime.text = "Проверять здесь пока нечего."
        $ scene_runtime.location_text = scene_runtime.text
        if _werecat_room == "Forest":
            $ main_ui_runtime.action_items = forest_action_items()
        else:
            $ main_ui_runtime.action_items = forest_subroom_action_items()
        return
    $ _werecat_trap_rooms = werecat_trap_rooms()
    $ _werecat_trap_rooms.pop(_werecat_room, None)
    $ werecat_state()["trap_rooms"] = dict(_werecat_trap_rooms)
    if procedural_randint(1, 100, "werecat_trap_%s_%s" % (_werecat_room, current_game_day())) > werecat_trap_success_chance():
        $ scene_runtime.text = "К приманке кто-то подходил: земля примята, кости растащены, на ветке опять висит мягкий блестящий клочок шерсти. Но сама тварь оказалась слишком осторожной и ушла, едва вы приблизились."
        $ scene_runtime.location_text = scene_runtime.text
        if _werecat_room == "Forest":
            $ main_ui_runtime.action_items = forest_action_items()
        else:
            $ main_ui_runtime.action_items = forest_subroom_action_items()
        return
    $ werecat_state()["caught"] = 1
    $ scene_runtime.text = "В тени между деревьями вы замечаете ее почти сразу. Не зверя и не женщину, а странную, тревожно красивую смесь обоих. Кошачьи уши вздрагивают от каждого звука, пушистый хвост нервно ходит из стороны в сторону, по плечам и бедрам легли тонкие узоры мягкой шерсти, а глаза у нее золотые, настороженные и слишком умные для простой лесной твари. Она явно напугана, но не шипит и не бросается, только смотрит так, будто еще сама не решила, считать ли вас охотником или спасением."
    $ scene_runtime.location_text = scene_runtime.text
    vscene werecat_caught_picture_path()
    "[scene_runtime.text]"
    if werecat_second_gift_available():
        menu:
            "Что сделать?"
            "Подарить ее Клариссе":
                $ werecat_apply_clara_gift_bonus()
                $ scene_runtime.text = "Вы решаете, что второй лесной кошке лучше не тесниться в трактире, а стать подарком для Клариссы. Такой редкий живой подарок она точно поймет: не безделушка, а полезная, красивая и опасная спутница. После этого Кларисса смотрит на вас теплее обычного, будто подарок попал именно туда, куда нужно."
                $ scene_runtime.location_text = scene_runtime.text
                call stat
            "Отпустить":
                $ werecat_state()["caught"] = 0
                $ werecat_state()["tracks_seen"] = 1
                $ werecat_state()["tracks_first_text_seen"] = 1
                $ scene_runtime.text = "Вы осторожно освобождаете пойманную тварь и отходите, давая ей путь к лесу. Она исчезает между стволами почти бесшумно, но теперь вы точно знаете: в этих местах есть не только одна такая кошка."
                $ scene_runtime.location_text = scene_runtime.text
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
                $ werecat_state()["adopted_day"] = current_game_day()
                $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 2
                $ player.change_stat("charisma", 15)
                $ player.change_stat("fun", 3)
                $ Sandra.change_social(friend_delta=1)
                $ Melissa.change_social(friend_delta=1)
                $ Amanda.change_social(friend_delta=1)
                $ Sandra.rebel_baseline = max(0, int(Sandra.rebel_baseline or 0) - 1)
                $ Melissa.rebel_baseline = max(0, int(Melissa.rebel_baseline or 0) - 1)
                $ Amanda.rebel_baseline = max(0, int(Amanda.rebel_baseline or 0) - 1)
                $ _werecat_pet_state = werecat_pet_state()
                $ _werecat_pet_state["trust"] = max(6, int(_werecat_pet_state.get("trust", 0) or 0))
                $ _werecat_pet_state["comfort"] = max(8, int(_werecat_pet_state.get("comfort", 0) or 0))
                $ WerecatStaticData.invalidate_daily_schedule()
                $ scene_runtime.text = "Вы не тянете поводок, не орете и не делаете резких движений. Просто тихо уводите странную лесную кошку с собой, будто она сама уже наполовину решила вам довериться. Дом быстро принимает ее как новую, немного диковатую, но полезную тварь. В кладовых с этого дня становится спокойнее: теперь у крыс появился настоящий враг."
                $ scene_runtime.location_text = scene_runtime.text
                call stat
            "Продать работорговцам за 5000":
                $ werecat_state()["caught"] = 0
                $ werecat_state()["sold"] = 1
                $ player.add_money(5000)
                $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) - 3
                $ Sandra.change_social(friend_delta=-2)
                $ Melissa.change_social(friend_delta=-3)
                $ Amanda.change_social(friend_delta=-2)
                $ scene_runtime.text = "Вы выбираете самый жесткий и самый выгодный путь. За такую необычную добычу быстро дают большие деньги, но запах этой сделки остается при вас надолго. Крысы в доме от этого, разумеется, никуда не деваются."
                $ scene_runtime.location_text = scene_runtime.text
                call stat
    $ main_ui_runtime.action_items = forest_action_items() if str(rooms.current_code or "") == "Forest" else forest_subroom_action_items()
    return
