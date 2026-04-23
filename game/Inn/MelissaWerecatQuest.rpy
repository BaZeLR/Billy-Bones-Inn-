default WerecatVar = {
    "rats_problem_active": 0,
    "rat_breakfast_seen": 0,
    "adoption_breakfast_seen": 0,
    "woods_exploration": 0,
    "tracks_seen": 0,
    "tracks_room": "",
    "trap_active": 0,
    "trap_room": "",
    "trap_day": -1,
    "caught": 0,
    "adopted": 0,
    "sold": 0,
    "name": "",
    "adopted_day": -1,
    "first_month_thanks_day": -1,
    "hunter_tease_day": -1,
    "hunter_tease_offer_day": -1,
    "hunter_tease_offer_ready": 0,
    "rat_carcass_cached": 0,
    "rat_food_loss_next_day": -1,
}

init 3 python:
    import random
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
        return str(WerecatVar.get("name", "") or "").strip()

    def werecat_display_name():
        return werecat_name_value() or "оборотница-кошка"

    def werecat_hunter_rumor_seen():
        return int(WerecatVar.get("hunter_tease_day", -1) or -1) >= 0

    def werecat_month_thanks_ready():
        adopted_day = int(WerecatVar.get("adopted_day", -1) or -1)
        return (
            int(WerecatVar.get("adopted", 0) or 0) == 1
            and int(WerecatVar.get("adoption_breakfast_seen", 0) or 0) == 1
            and adopted_day >= 0
            and int(dayspassed or 0) >= adopted_day + 30
            and int(WerecatVar.get("first_month_thanks_day", -1) or -1) < adopted_day + 30
            and not bool(BreakfastToday)
        )

    def werecat_adoption_breakfast_ready():
        adopted_day = int(WerecatVar.get("adopted_day", -1) or -1)
        return (
            int(WerecatVar.get("adopted", 0) or 0) == 1
            and int(WerecatVar.get("adoption_breakfast_seen", 0) or 0) == 0
            and adopted_day >= 0
            and int(dayspassed or 0) > adopted_day
            and not bool(BreakfastToday)
        )

    def werecat_rat_breakfast_ready():
        return (
            int(WerecatVar.get("rats_problem_active", 0) or 0) == 1
            and int(WerecatVar.get("rat_breakfast_seen", 0) or 0) == 0
            and int(MelissaVar.get("storage_rat_cleared", 0) or 0) == 1
            and int(MelissaVar.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(dayspassed or 0) >= int(MelissaVar.get("storage_rat_last_help_day", -1) or -1) + 1
            and not bool(BreakfastToday)
        )

    def werecat_hunter_tease_ready():
        return (
            str(CurLoc or "") == "HunterClub"
            and int(WerecatVar.get("rats_problem_active", 0) or 0) == 1
            and int(WerecatVar.get("rat_breakfast_seen", 0) or 0) == 1
            and int(WerecatVar.get("adopted", 0) or 0) == 0
            and int(WerecatVar.get("sold", 0) or 0) == 0
            and not werecat_hunter_rumor_seen()
        )

    def werecat_hunter_tease_offer_ready():
        if not werecat_hunter_tease_ready():
            return False
        WerecatVar["hunter_tease_offer_day"] = int(dayspassed or 0)
        WerecatVar["hunter_tease_offer_ready"] = 1
        return True

    def werecat_can_track_here(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        return room_key in ("Forest", "ForestClearing", "ForestHiddenPath", "ForestWaterfall", "ForestDarkWoods", "ForestLake", "ForestSpring")

    def werecat_can_search(room_code=""):
        return (
            werecat_can_track_here(room_code)
            and int(WerecatVar.get("adopted", 0) or 0) == 0
            and int(WerecatVar.get("sold", 0) or 0) == 0
        )

    def werecat_can_set_bait(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        return (
            werecat_can_search(room_key)
            and int(WerecatVar.get("tracks_seen", 0) or 0) == 1
            and str(WerecatVar.get("tracks_room", "") or "") == room_key
            and int(WerecatVar.get("trap_active", 0) or 0) == 0
            and int(WerecatVar.get("rat_carcass_cached", 0) or 0) == 1
        )

    def werecat_can_check_bait(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        return (
            int(WerecatVar.get("trap_active", 0) or 0) == 1
            and str(WerecatVar.get("trap_room", "") or "") == room_key
            and int(WerecatVar.get("caught", 0) or 0) == 0
        )

    def werecat_trap_success_chance():
        exploration_value = int(WerecatVar.get("woods_exploration", 0) or 0)
        if exploration_value >= 200:
            return 100
        if exploration_value >= 150:
            return 40
        if exploration_value >= 100:
            return 30
        return 0

    def werecat_register_search(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        gain = random.randint(10, 25)
        total = int(WerecatVar.get("woods_exploration", 0) or 0) + gain
        WerecatVar["woods_exploration"] = total
        if not werecat_hunter_rumor_seen():
            return {
                "gain": gain,
                "found_tracks": False,
                "text": "Следов в лесу хватает, но без наводки вы пока не понимаете, какие из них стоит считать по-настоящему странными. Похоже, сначала надо услышать хоть что-то конкретнее, чем одни только смутные трактирные разговоры.",
            }
        if int(WerecatVar.get("tracks_seen", 0) or 0) == 0:
            WerecatVar["tracks_seen"] = 1
            WerecatVar["tracks_room"] = room_key
            return {
                "gain": gain,
                "found_tracks": True,
                "text": "Вы натыкаетесь на странный след: в сырой земле отпечатались кошачьи лапы, а рядом будто на миг проступил почти человеческий босой шаг. Между корней зацепились мягкие блестящие клочки шерсти, слишком нежные для обычного зверя. Похоже, здесь и правда шастает нечто куда любопытнее простой лесной кошки.",
            }
        return {
            "gain": gain,
            "found_tracks": False,
            "text": "Вы снова внимательно прочесываете лес, примечая тропы, запахи и следы зверья. Теперь вы уже знаете, что странная тварь здесь действительно бывает, но сегодня она будто нарочно уходит с вашего пути.",
        }


label MelissaRatBreakfastScene:
    $ WerecatVar["rat_breakfast_seen"] = 1
    $ BreakfastToday = True
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ TavernBreakfastDay = int(dayspassed or 0)
    $ TavernBreakfastEventActive = True
    hide screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    $ MainTxt = "Мягкий утренний свет ползет по кухне, в мисках парит каша, воздух пахнет молоком, овсом и горячим хлебом. За общим столом сегодня сидят все трое.\n\nСандра, помешивая кашу с лишней силой, первой возвращается к вчерашнему: \"Крысы в доме совсем распоясались. Уже по три полных тюка припасов за неделю портят. Если так пойдет дальше, к зиме сами у пустых мешков сядем.\"\n\nАманда разваливается на скамье и, как всегда, пытается рассечь тревогу шуткой: \"А знаешь, чего этому дому по-настоящему не хватает? Хорошей сильной киски. Такой, чтоб и мышей ловила, и с вредителями умела разбираться как следует.\" Она лукаво подмигивает.\n\nМелисса сперва краснеет, потом все же хихикает: \"Да... большой, гибкой охотницы. Чтобы маленьких пакостников душила без жалости... и ночами было бы с кем согреться.\"\n\nСмех за столом быстро снимает лишнее напряжение. Даже Сандра, отвернувшись к котлу, ворчит уже заметно мягче."
    $ CurLocDesc = MainTxt
    $ fun = _player_clamp(int(fun or 0) + 5, 0, 100)
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ TavernKitchenSavedText = MainTxt
    call stat
    return


label WerecatAdoptionBreakfastScene:
    $ WerecatVar["adoption_breakfast_seen"] = 1
    $ BreakfastToday = True
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ TavernBreakfastDay = int(dayspassed or 0)
    $ TavernBreakfastEventActive = True
    hide screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    $ MainTxt = "За завтраком сегодня разговор быстро сворачивает к новой обитательнице трактира. У самого очага, настороженно щурясь, устроилась ваша необычная лесная кошка, и даже с такого расстояния видно, что она следит за каждым шорохом куда внимательнее обычного зверя.\n\nСандра первой признает очевидное: \"В кладовой ночью впервые было тихо. Если эта хвостатая и правда останется у нас, припасы хоть поживут спокойно.\" Аманда тут же расплывается в ухмылке: \"Говорила же, дому нужна хорошая киска. А эта еще и красавица, не только охотница.\" Мелисса тихо фыркает, но спорить не спешит: \"Главное, чтобы она крыс душила так же ловко, как на всех смотрит.\"\n\nПохоже, в трактире уже начинают принимать вашу странную добычу как свою. История на этом не кончается, но теперь у нее наконец есть продолжение дома, а не только в лесу."
    $ CurLocDesc = MainTxt
    $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ TavernKitchenSavedText = MainTxt
    return


label WerecatMonthThanksScene:
    $ WerecatVar["first_month_thanks_day"] = int(dayspassed or 0)
    $ BreakfastToday = True
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ TavernBreakfastDay = int(dayspassed or 0)
    $ TavernBreakfastEventActive = True
    hide screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    $ MainTxt = "За общим столом сегодня куда спокойнее обычного. В кладовой уже давно не слышно прежней возни, а у самого очага, свернувшись теплым клубком, дремлет ваша необычная кошка.\n\nСандра первой нарушает молчание: \"Эта малышка и правда спасла нам припасы. Если бы не она, мы бы еще долго слушали шорох в мешках и считали, сколько еды уходит в никуда.\" Потом она смотрит уже прямо на вас и говорит мягче: \"Хорошее дело вы все-таки сделали. Такой зверь дому в радость.\"\n\nОстальные тоже заметно теплеют. Даже обычная утренняя суета сегодня кажется куда уютнее."
    if int(MelissaVar.get("bats_episode", 0) or 0) >= 6:
        $ MainTxt = str(MainTxt or "") + "\n\nПосле короткой паузы Сандра добавляет уже совсем иначе: \"А ту глупую историю с чердаком пора бы и отпустить. Дом у нас старый, люди живые, а дурных случаев без того хватает. Главное, что теперь ты не отмахнулся от настоящей беды и довел дело до ума.\" Похоже, за столом наконец начинают считать тот позорный случай скорее нелепостью, чем клеймом."
    $ CurLocDesc = MainTxt
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ TavernKitchenSavedText = MainTxt
    return


label WerecatHunterClubTease:
    $ WerecatVar["hunter_tease_day"] = int(dayspassed or 0)
    $ WerecatVar["hunter_tease_offer_ready"] = 0
    $ MainTxt = "У дальней стены двое охотников переговариваются вполголоса, но так, чтобы половина зала все равно слышала.\n\n\"Говорят, в чаще теперь водится лесная кошка не из простых. Хвостом водит, ушами прядает, а тело такое, что у мужика колени подломятся быстрее, чем он лук натянет.\"\n\nВторой хмыкает, уже явно смакуя чужую байку: \"Если далеко заберешься, можно и след взять. А если удача с умением сходятся, такую тварь будто бы и поймать можно. Только не для всякого поводка она годится.\"\n\nПахнет дешевой бравадой и мужицкой похабщиной, но зерно в слухе, похоже, есть."
    $ CurLocDesc = MainTxt
    hide screen main_ui
    vscene werecat_info_picture_path()
    "[MainTxt]"
    call HunterClubBuildActions
    return


label WerecatSetTrap(room_code=""):
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    if not werecat_can_set_bait(_werecat_room):
        $ MainTxt = "Сейчас вы не можете устроить здесь такую приманку."
        $ CurLocDesc = MainTxt
        call RefreshCurrentActionMenu(_werecat_room, "", True)
        return
    $ WerecatVar["trap_active"] = 1
    $ WerecatVar["trap_room"] = _werecat_room
    $ WerecatVar["trap_day"] = int(dayspassed or 0)
    $ WerecatVar["rat_carcass_cached"] = 0
    $ MainTxt = "Вы устраиваете пахучую крысиную приманку там, где нашли странные следы, и отходите подальше. Если слухи не врут, сюда должно прийти нечто куда умнее обычного зверя."
    $ CurLocDesc = MainTxt
    call RefreshCurrentActionMenu(_werecat_room, "", True)
    return


label WerecatCheckTrap(room_code=""):
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    if not werecat_can_check_bait(_werecat_room):
        $ MainTxt = "Проверять здесь пока нечего."
        $ CurLocDesc = MainTxt
        call RefreshCurrentActionMenu(_werecat_room, "", True)
        return
    $ WerecatVar["trap_active"] = 0
    $ WerecatVar["trap_room"] = ""
    if renpy.random.randint(1, 100) > werecat_trap_success_chance():
        $ MainTxt = "К приманке кто-то подходил: земля примята, кости растащены, на ветке опять висит мягкий блестящий клочок шерсти. Но сама тварь оказалась слишком осторожной и ушла, едва вы приблизились."
        $ CurLocDesc = MainTxt
        call RefreshCurrentActionMenu(_werecat_room, "", True)
        return
    $ WerecatVar["caught"] = 1
    $ MainTxt = "В тени между деревьями вы замечаете ее почти сразу. Не зверя и не женщину, а странную, тревожно красивую смесь обоих. Кошачьи уши вздрагивают от каждого звука, пушистый хвост нервно ходит из стороны в сторону, по плечам и бедрам легли тонкие узоры мягкой шерсти, а глаза у нее золотые, настороженные и слишком умные для простой лесной твари. Она явно напугана, но не шипит и не бросается, только смотрит так, будто еще сама не решила, считать ли вас охотником или спасением."
    $ CurLocDesc = MainTxt
    hide screen main_ui
    vscene werecat_caught_picture_path()
    "[MainTxt]"
    menu:
        "Что сделать?"
        "Забрать ее домой":
            call WerecatAdoptChoice("adopt")
        "Продать работорговцам за 5000":
            call WerecatAdoptChoice("sell")
    return


label WerecatAdoptChoice(choice_code="adopt"):
    $ _werecat_choice = str(choice_code or "").strip().lower()
    if _werecat_choice == "sell":
        $ WerecatVar["caught"] = 0
        $ WerecatVar["sold"] = 1
        $ werecat_sync_profile()
        $ money = int(money or 0) + 5000
        $ tavernfame = int(tavernfame or 0) - 3
        $ notoriety = min(100, int(notoriety or 0) + 12)
        $ Friends["sandra"] = max(0, int(Friends.get("sandra", 0) or 0) - 2)
        $ Friends["melissa"] = max(0, int(Friends.get("melissa", 0) or 0) - 3)
        $ Friends["amanda"] = max(0, int(Friends.get("amanda", 0) or 0) - 2)
        $ MainTxt = "Вы выбираете самый жесткий и самый выгодный путь. За такую необычную добычу быстро дают большие деньги, но запах этой сделки остается при вас надолго. Крысы в доме от этого, разумеется, никуда не деваются."
        $ CurLocDesc = MainTxt
        call stat
        jump ForestRestore
    $ WerecatVar["adopted"] = 1
    $ WerecatVar["caught"] = 0
    $ WerecatVar["rats_problem_active"] = 0
    $ WerecatVar["rat_food_loss_next_day"] = -1
    $ WerecatVar["name"] = "Луна"
    $ WerecatVar["adopted_day"] = int(dayspassed or 0)
    $ tavernfame = int(tavernfame or 0) + 2
    $ charisma = min(100, int(charisma or 0) + 15)
    $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ neshlush["sandra"] = max(0, int(neshlush.get("sandra", 0) or 0) - 1)
    $ neshlush["melissa"] = max(0, int(neshlush.get("melissa", 0) or 0) - 1)
    $ neshlush["amanda"] = max(0, int(neshlush.get("amanda", 0) or 0) - 1)
    $ WerecatNPCState["trust"] = max(6, int(WerecatNPCState.get("trust", 0) or 0))
    $ WerecatNPCState["comfort"] = max(8, int(WerecatNPCState.get("comfort", 0) or 0))
    $ werecat_sync_profile()
    $ MainTxt = "Вы не тянете поводок, не орете и не делаете резких движений. Просто тихо уводите странную лесную кошку с собой, будто она сама уже наполовину решила вам довериться. Дом быстро принимает ее как новую, немного диковатую, но полезную тварь. В кладовых с этого дня становится спокойнее: теперь у крыс появился настоящий враг."
    $ CurLocDesc = MainTxt
    call stat
    jump ForestRestore
