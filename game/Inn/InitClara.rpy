init python:
    import random
    import renpy.exports as renpy

    def clara_extra_location_code(day_marker=None, weekday=None, time_slot=None):
        day_value = int(dayspassed if day_marker is None else day_marker or 0)
        week_value = int(week if weekday is None else weekday or 0)
        time_value = int(time if time_slot is None else time_slot or 0)
        parity = (day_value + week_value) % 2
        route = (day_value + week_value) % 3

        if week_value == 5 and time_value == 3:
            return "FridayDance" if parity == 0 else ""

        if time_value == 1:
            if route == 0:
                return "DressShop"
            if route == 1:
                return "MarketPlace"
            return "ForestClearing"

        if time_value == 2:
            if route == 0:
                return "MarketPlace"
            if route == 1:
                return "DressShop"
            return "ForestLake"

        return ""

    def clara_visible_in_location(location_code=""):
        location_key = str(location_code or "").strip()
        if location_key == "WineStore":
            return int(time or 0) == 0
        if location_key == "TavernMain":
            return clara_tavern_visit_active()
        return clara_extra_location_code() == location_key

    def clara_can_start_social_events():
        try:
            update_stat_state()
        except Exception:
            pass
        return int(charisma or 0) >= 70 and int(Friends.get("clara", 0) or 0) >= 5

    def clara_can_receive_gifts():
        try:
            update_stat_state()
        except Exception:
            pass
        return int(charisma or 0) >= 70 and int(Friends.get("clara", 0) or 0) >= 7

    def clara_wine_store_talk_picture():
        candidates = [
            "images/clara/wineSellar_clara_talk.png",
            "images/clara/wine_sellar_clara_talk_2.png",
            "images/clara/wineSellar_clara_talk_3.png",
            "images/clara/wineSellar_clara_talk_4.png",
            "images/clara/wineSellar_clara_talk_5.png",
            "images/clara/wineSellar_clara_talk_6.png",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def clara_wine_store_flirt_picture():
        candidates = [
            "images/clara/wineSellar_clara_flirt_0.png",
            "images/clara/wineSellar_clara_flirt_1.png",
            "images/clara/wineSellar_clara_flirt_2.png",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def clara_forest_picture(location_code=""):
        location_key = str(location_code or "").strip()
        candidates = []
        if location_key == "ForestClearing":
            candidates = [
                "images/clara/forest_clara.png",
                "images/clara/forest_clara_0.png",
                "images/clara/forest_clara_1.png",
                "images/clara/forest_clara_encounter.png",
                "images/clara/forest_clara_encounter_2.png",
            ]
        elif location_key == "ForestSpring":
            candidates = [
                "images/clara/forestSpring_clara.png",
                "images/clara/forest_spring_clara_1.png",
                "images/clara/forest_spring_clara_2.png",
            ]
        elif location_key == "ForestLake":
            candidates = [
                "images/clara/forestlake_clara.png",
                "images/clara/forestlake_clara_0.png",
                "images/clara/forestLake_clara_2.png",
            ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def alber_random_portrait():
        candidates = [
            "images/Alber/portrait1.png",
            "images/Alber/portrat2.png",
            "images/Alber/portrait3.png",
            "images/Alber/portrait4.png",
            "images/Alber/portrait5.jpg",
            "images/Alber/portrait6.jpg",
            "images/Alber/portrait7.jpg",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        return random.choice(loadable) if len(loadable) > 0 else ""

    def clara_tavern_visit_active(day_marker=None, weekday=None, time_slot=None):
        day_value = int(dayspassed if day_marker is None else day_marker or 0)
        week_value = int(week if weekday is None else weekday or 0)
        time_value = int(time if time_slot is None else time_slot or 0)
        if time_value != 2:
            return False
        if ((day_value + week_value) % 4) != 0:
            return False
        try:
            return _tavern_is_in_room("melissa", "TavernMain")
        except Exception:
            return True

    def clara_visible_at_friday_dance():
        if not clara_visible_in_location("FridayDance"):
            return False
        try:
            return int(CheckIfDanceExist("amanda", "legare", int(FridayDancesCount or 0)) or 0) <= 0
        except Exception:
            return True

    def clara_can_accept_horse_ride(location_code=""):
        location_key = str(location_code or CurLoc or "").strip()
        if location_key not in ("ForestClearing", "ForestLake"):
            return False
        if not clara_visible_in_location(location_key):
            return False
        return bool(str(MyStallion or "").strip()) and int(HorseSaddled or 0) == 1

    def clara_giftable_entries():
        entries = []

        item_ids = ("soap_001", "special_mushroom_001", "lavender_001")
        for item_id in item_ids:
            if _player_item_count_by_id(item_id) <= 0:
                continue
            item_obj = get_game_item(item_id)
            if item_obj is None:
                continue
            entries.append({
                "source": "item",
                "gift_id": str(item_id),
                "gift_name": str(getattr(item_obj, "name", item_id) or item_id),
            })

        dress_codes = (
            "thiefdress",
            "simplebra",
            "simplepanties",
            "blackstockings",
            "redstockings",
        )
        for dress_code in dress_codes:
            if str(dress_code or "") not in list(MyDresses or []):
                continue
            if str(MyCurDress or "") == str(dress_code or ""):
                continue
            entries.append({
                "source": "dress",
                "gift_id": "dress_" + str(dress_code),
                "gift_name": str(ShortDressName.get(dress_code, dress_code) or dress_code),
                "dress_code": str(dress_code),
            })

        return entries

    def clara_has_giftable_entries():
        return len(list(clara_giftable_entries() or [])) > 0

    def clara_remove_gift_entry(entry):
        row = dict(entry or {})
        source = str(row.get("source", "") or "")
        if source == "dress":
            dress_code = str(row.get("dress_code", "") or "")
            if dress_code == "" or dress_code not in list(MyDresses or []):
                return False
            if dress_code == str(MyCurDress or ""):
                return False
            try:
                MyDresses.remove(dress_code)
            except Exception:
                return False
            return True

        item_id = str(row.get("gift_id", "") or "")
        if item_id == "":
            return False
        return _player_remove_item_by_id(item_id, 1)

    def clara_social_outcome(interaction_type="talk", gift_item_id=""):
        interaction = str(interaction_type or "talk").strip().lower()
        gift_id = str(gift_item_id or "").strip()
        score = 0
        score += int(charisma or 0) // 15
        score += int(Friends.get("clara", 0) or 0) // 4
        score += int(ClaraVar.get("trust", 0) or 0) // 3
        score += int(sluttiness.get("clara", 0) or 0) // 10

        if str(MyCurDress or "") == "thiefdress":
            score += 1

        if interaction == "flirt":
            score += 2
            score -= int(FlirtedToday.get("clara", 0) or 0) * 3
        elif interaction == "gift":
            score += 1
            score -= int(GiftedToday.get("clara", 0) or 0) * 3
            if gift_id in tuple(preferred_gift_item_ids("clara")):
                score += 3
            elif gift_id != "":
                score -= 2
        else:
            score -= int(TalkedToday.get("clara", 0) or 0) * 2

        score += random.randint(-2, 2)

        if score >= 7:
            return "positive"
        if score >= 4:
            return "neutral"
        return "negative"

label InitClara:
    python:
        GirlName = "clara"
        RealName[GirlName] = "Кларисса"
        RealName2[GirlName] = "Клариссы"
        RealName3[GirlName] = "Клариссе"
        DateOfBirth[GirlName] = renpy.random.randint(15, 350)
        age_girls[GirlName] = 19
        kids[GirlName] = 0
        beauty[GirlName] = 62
        sluttiness[GirlName] = 10
        sexacts[GirlName] = 0
        cuminside[GirlName] = 0
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ""
        ConceptionChance[GirlName] = 10
        CurrentLoc[GirlName] = "WineStore"
        PussyWetStart[GirlName] = 10
        virginity[GirlName] = True

        girltextdesc[GirlName] = "Кларисса, старшая дочь мессира Легаре, молодая девушка из зажиточного купеческого дома. Это очень приветливая и игривая блондинка чуть младше вас, с большими искрящимися серыми глазами, пухлыми губами и удивительно легкой, грациозной походкой. На ней обычно свободное длинное повседневное платье из легкой ткани, похожее на удобный сарафан; на ярком свету ткань кажется чуть прозрачной. Грудь Клариссы размера B мягко и соблазнительно колышется при каждом движении. От нее пахнет лавандой и дорогими модными духами."
        dressdefault[GirlName] = "greenworkdress"
        bradef[GirlName] = "simplebra"
        pantiesdef[GirlName] = "simplepanties"
        legsdef[GirlName] = ""
        shoesdef[GirlName] = "simpleshoes"

        cooking[GirlName] = 10
        cleaning[GirlName] = 8
        waitress[GirlName] = 45
        otkroven[GirlName] = 0

        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        jobHallAvail[GirlName] = 0
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0
        Friends[GirlName] = 0
        Talked[GirlName] = 0
        ClaraVar["flirt"] = 0
        ClaraVar["knownotvirgin"] = 0
        ClaraVar["trust"] = 0
        ClaraVar["positive"] = 0
        ClaraVar["neutral"] = 0
        ClaraVar["negative"] = 0
        ClaraVar["lastsocial"] = ""
        GiftPreferences[GirlName] = [
            "dress_thiefdress",
            "soap_001",
            "special_mushroom_001",
            "dress_simplebra",
            "dress_simplepanties",
            "dress_blackstockings",
            "dress_redstockings",
            "libido_tincture_001",
        ]

        # Uppercase compatibility for legacy references.
        Friends["Clara"] = Friends[GirlName]
        Talked["Clara"] = Talked[GirlName]

    return
