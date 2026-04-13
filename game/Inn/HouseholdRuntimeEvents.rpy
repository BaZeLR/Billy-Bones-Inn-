default HouseholdRuntimeEventSeen = {}
default HouseholdInsightState = {}

init python:
    import random
    import renpy.exports as renpy

    def _household_seen_key(event_code="", day_marker=None):
        return "%s:%s" % (str(event_code or ""), int(dayspassed if day_marker is None else day_marker or 0))

    def household_runtime_event_seen_today(event_code="", day_marker=None):
        return int(HouseholdRuntimeEventSeen.get(_household_seen_key(event_code, day_marker), 0) or 0) == 1

    def household_mark_runtime_event_seen(event_code="", day_marker=None):
        HouseholdRuntimeEventSeen[_household_seen_key(event_code, day_marker)] = 1
        return 1

    def _household_insight_topics(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "melissa":
            return [
                {
                    "min_friend": 8,
                    "label": "Спросить Мелиссу о слухах в трактире",
                    "text": "Вы просите Мелиссу рассказать, что она успела заметить и услышать в трактире. Она понижает голос и спокойно отвечает, что больше всего правды всплывает не в криках, а в полушепоте: у стойки, на лестнице и у дверей комнат. \"Если хочешь понимать, что у людей на уме, слушай не тех, кто шумит, а тех, кто думает, что их никто не слышит,\" замечает она.",
                },
                {
                    "min_friend": 10,
                    "label": "Спросить Мелиссу о полезных хозяйственных хитростях",
                    "text": "Мелисса неожиданно делится вполне практичной хитростью: сухой мох в хозяйстве ценится куда выше сырого. \"Высушишь как следует, истолчешь, и уже можно думать не только о растопке. А если еще есть тряпье, из полос ткани и сухого мха выходят неплохие перевязки. Пять хороших полос ткани и вовсе можно пустить на крепкую веревку,\" объясняет она.",
                },
                {
                    "min_friend": 12,
                    "label": "Спросить Мелиссу о том, что ее по-настоящему тревожит",
                    "text": "После недолгой паузы Мелисса признается, что ее сильнее всего изматывает не сама работа, а ощущение, будто в доме никогда не бывает по-настоящему тихо. \"Когда в кладовой крысы, под потолком шуршат мыши, а по коридору кто-то топает среди ночи, начинаешь злиться не на людей, а на весь дом сразу. Если в доме спокойно, и мне легче дышится,\" говорит она уже без привычной резкости.",
                },
                {
                    "min_friend": 15,
                    "label": "Спросить Мелиссу о самых неловких разговорах и желаниях",
                    "text": "Мелисса сначала смотрит на вас испытующе, но все же решается говорить откровеннее. Она признается, что в большом доме люди очень быстро начинают слышать больше, чем им положено: ночные шаги, тихие стоны, чужие шепоты и разговоры о том, кто к кому тянется. \"Иногда это просто слухи. А иногда по таким мелочам заранее понимаешь, где скоро начнется новая история,\" произносит она и чуть заметно отводит взгляд.",
                },
            ]
        if girl == "sandra":
            return [
                {
                    "min_friend": 8,
                    "label": "Спросить Сандру о припасах и кухонных хитростях",
                    "text": "Сандра сразу уходит в хозяйственные подробности. Она напоминает, что ягоды, грибы, мед и мясо лучше не таскать без толку по карманам, а сразу нести на кухню. \"Из таких вещей потом и завтрак выходит, и похлебка, и нормальный стол для всей челяди. Если дом сытый, всем проще и работать, и не грызться друг с другом,\" говорит она.",
                },
                {
                    "min_friend": 10,
                    "label": "Спросить Сандру о мыле и полезных заготовках",
                    "text": "Сандра охотно возвращается к мыловарению и объясняет, что хорошее домашнее мыло любит терпение. \"Лаванда и роза для такого дела самое оно. Только не думай, что сварил и сразу пользуйся: мылу надо вылежаться как следует. Зато потом и людям приятно, и в доме будто чище дышится,\" деловито замечает она.",
                },
                {
                    "min_friend": 12,
                    "label": "Спросить Сандру о старых местных историях",
                    "text": "Сандра, понизив голос, говорит, что в округе полно мест, о которых лучше знать заранее, чем натыкаться на них случайно. По ее словам, люди годами передают друг другу полузабытые рассказы про запертые комнаты, тайные проходы и странные углы, куда никто не ходит без причины. \"Легенды легендами, а лишняя осторожность еще никому не вредила,\" подводит она итог.",
                },
                {
                    "min_friend": 15,
                    "label": "Спросить Сандру о людях, вине и танцах",
                    "text": "Сандра признается, что лучше всего характер людей виден в те вечера, когда всем становится чуть веселее обычного. За столом, после хорошей еды, кружки вина или перед самыми танцами многие начинают говорить свободнее и смотреть друг на друга уже не так, как днем. \"Кто чего стоит, проще всего понять не в работе, а когда людям кажется, что за ними никто особенно не следит,\" сухо замечает она.",
                },
            ]
        if girl == "amanda":
            return [
                {
                    "min_friend": 8,
                    "label": "Спросить Аманду о сплетнях и городских слухах",
                    "text": "Аманда оживляется почти сразу и начинает пересказывать, как быстро по городу расходятся слухи о клиентах, танцах и чужих романах. По ее словам, на рынке и в трактире люди сами выкладывают половину нужной правды, если дать им возможность почувствовать себя интересными. \"Хочешь знать, кто с кем водится, просто слушай, кто о ком слишком часто вспоминает,\" весело советует она.",
                },
                {
                    "min_friend": 10,
                    "label": "Спросить Аманду о тайных местах и прогулках",
                    "text": "Аманда, чуть понизив голос, рассказывает, что за лесом люди знают не только обычные тропы, но и места, куда забредают затем, чтобы их не тревожили. Она вспоминает старую водокачку, беседку и другие укромные уголки, где можно и поболтать, и спрятаться от лишних глаз. \"Если кто-то хочет секретов, он почти всегда идет не по дороге, а чуть в сторону,\" говорит она с понимающей улыбкой.",
                },
                {
                    "min_friend": 12,
                    "label": "Спросить Аманду о том, как люди флиртуют и чего хотят",
                    "text": "Аманда без особого смущения рассуждает о том, что люди очень редко говорят прямо, чего им хочется. Кто-то начинает чаще вертеться у стойки, кто-то ищет повод задержаться после разговора, а кто-то вдруг становится слишком щедрым на подарки и угощение. \"Если смотреть внимательно, почти любой флирт видно заранее. Особенно когда человек уверен, что отлично все скрывает,\" смеется она.",
                },
                {
                    "min_friend": 15,
                    "label": "Спросить Аманду о желаниях, платьях и смелых решениях",
                    "text": "Аманда неожиданно серьезнеет и говорит, что в доме многое меняется, когда кто-то один перестает стесняться чуть больше обычного. Новое платье, смелый танец, лишняя кружка или даже просто более дерзкий взгляд быстро подталкивают остальных попробовать то же самое. \"Стоит одной решиться, и всем остальным уже легче признаться, чего им самим давно хотелось,\" тихо замечает она.",
                },
            ]
        return []

    def household_special_talk_available(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        topics = list(_household_insight_topics(girl))
        if len(topics) <= 0:
            return False
        friend_value = int(Friends.get(girl, 0) or 0)
        for topic in topics:
            if friend_value >= int(topic.get("min_friend", 0) or 0):
                return True
        return False

    def household_special_talk_entry(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        topics = [topic for topic in _household_insight_topics(girl) if int(Friends.get(girl, 0) or 0) >= int(topic.get("min_friend", 0) or 0)]
        if len(topics) <= 0:
            return None
        topic_index = int(HouseholdInsightState.get(girl, 0) or 0) % len(topics)
        return dict(topics[topic_index])

    def household_advance_special_talk(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        HouseholdInsightState[girl] = int(HouseholdInsightState.get(girl, 0) or 0) + 1
        return int(HouseholdInsightState.get(girl, 0) or 0)

    def melissa_storage_thanks_available():
        return (
            str(CurLoc or "") == "TavernStorage"
            and int(MelissaVar.get("storage_rat_last_help_day", -1) or -1) >= 0
            and int(MelissaVar.get("StorageThanksDay", -1) or -1) != int(dayspassed or 0)
        )

    def melissa_room_problem_available():
        return (
            str(CurLoc or "") == "TavernMelissaRoom"
            and (
                int(MelissaVar.get("room_pests_last_help_day", -1) or -1) >= 0
                or int(MelissaVar.get("room_pests_cleared", 0) or 0) > 0
            )
            and int(MelissaVar.get("RoomProblemAskDay", -1) or -1) != int(dayspassed or 0)
        )

    def household_dress_revealing_score(dress_code=""):
        dress_name = str(dress_code or "").strip()
        if dress_name == "":
            return 0
        top_part = str((DressTopPart or {}).get(dress_name, "") or "")
        bottom_part = str((DressBottomPart or {}).get(dress_name, "") or "")
        top_score = int((DressPartSlut or {}).get(top_part, 0) or 0)
        bottom_score = int((DressPartSlut or {}).get(bottom_part, 0) or 0)
        return max(top_score, bottom_score)

    def household_is_revealing_dress(dress_code=""):
        return household_dress_revealing_score(dress_code) >= 3

    def household_mark_revealing_dress_order(girl_name="", dress_code=""):
        girl = str(girl_name or "").strip().lower()
        dress_name = str(dress_code or "").strip()
        if girl == "" or dress_name == "" or not household_is_revealing_dress(dress_name):
            return 0

        if girl == "sandra":
            SandraVar["revealing_dress_ordered"] = 1
            SandraVar["revealing_dress_code"] = dress_name
        elif girl == "melissa":
            MelissaVar["revealing_dress_ordered"] = 1
            MelissaVar["revealing_dress_code"] = dress_name
        elif girl == "amanda":
            AmandaVar["revealing_dress_ordered"] = 1
            AmandaVar["revealing_dress_code"] = dress_name
        else:
            return 0
        return 1

    def sandra_revealing_dress_initiative_ready():
        return (
            int(BeckyVar.get("visitedhome", 0) or 0) >= 3
            and int(SandraVar.get("revealing_dress_ordered", 0) or 0) == 0
            and int(SandraVar.get("revealing_dress_initiative_seen", 0) or 0) == 0
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists("sandra", "BuyDress", "") == 0
            and int(Friends.get("sandra", 0) or 0) >= 7
            and int(TalkedToday.get("sandra", 0) or 0) == 0
        )

    def melissa_revealing_dress_request_ready():
        return (
            int(SandraVar.get("revealing_dress_ordered", 0) or 0) == 1
            and int(MelissaVar.get("revealing_dress_ordered", 0) or 0) == 0
            and int(MelissaVar.get("revealing_dress_request_seen", 0) or 0) == 0
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists("melissa", "BuyDress", "") == 0
            and int(Friends.get("melissa", 0) or 0) >= 6
            and int(TalkedToday.get("melissa", 0) or 0) == 0
        )

    def amanda_revealing_dress_request_ready():
        return (
            int(SandraVar.get("revealing_dress_ordered", 0) or 0) == 1
            and int(MelissaVar.get("revealing_dress_ordered", 0) or 0) == 1
            and int(AmandaVar.get("revealing_dress_ordered", 0) or 0) == 0
            and int(AmandaVar.get("revealing_dress_request_seen", 0) or 0) == 0
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists("amanda", "BuyDress", "") == 0
            and int(Friends.get("amanda", 0) or 0) >= 5
            and int(TalkedToday.get("amanda", 0) or 0) == 0
        )

    def melissa_clara_overhear_ready():
        return (
            str(CurLoc or "") == "TavernMain"
            and clara_visible_in_location("TavernMain")
            and _tavern_is_in_room("melissa", "TavernMain")
            and not household_runtime_event_seen_today("melissa_clara_overhear")
        )

    def melissa_clara_overhear_variant():
        return int((dayspassed or 0) + (week or 0) + (hour or 0)) % 2

    def tavern_storage_rat_event_ready():
        return (
            str(CurLoc or "") == "TavernStorage"
            and _tavern_is_in_room("melissa", "TavernStorage")
            and not household_runtime_event_seen_today("melissa_storage_rat")
        )

    def tavern_melissa_room_pests_event_ready():
        return (
            str(CurLoc or "") == "TavernMelissaRoom"
            and _tavern_is_in_room("melissa", "TavernMelissaRoom")
            and not household_runtime_event_seen_today("melissa_room_pests")
        )

    def melissa_night_wake_event_ready(return_location=""):
        return (
            str(return_location or "") == "TavernMyRoom"
            and int(dayspassed or 0) >= 21
            and not household_runtime_event_seen_today("melissa_night_wake")
            and random.randint(1, 4) == 1
        )

    def household_return_current_room_label():
        current_room = str(CurLoc or "").strip()
        if current_room in ("TavernMain", "TavernKitchen", "TavernStorage"):
            return current_room
        return "TavernMain"


label HouseholdReturnCurrentRoom:
    $ _household_return_room = household_return_current_room_label()
    jump expression _household_return_room


label SandraDressInitiativeEvent:
    $ SandraVar["revealing_dress_initiative_seen"] = 1
    $ _sandra_scene = tavern_kitchen_random_sandra_scene() if renpy.has_label("TavernKitchen") else ""
    if str(_sandra_scene or "").strip():
        $ _layout_last_picture = _sandra_scene
    $ MainTxt = "Сандра, улучив минуту без лишних ушей, задерживает вас у стола и вдруг говорит куда мягче обычного.\n\n\"Слушай, Стефан... после всех этих разговоров о Бекки я тут подумала. Если уж вдова может себе позволить иногда выглядеть поинтереснее, то, может, и мне пора перестать рядиться только в самое практичное. Не в девках ведь дело, а в том, чтобы и на меня иной раз посмотрели как на женщину. Если надумаешь, подбери мне у Ирмы что-нибудь посмелее обычного.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ваш ответ"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Пообещать подобрать Сандре более смелый наряд", Call("HouseholdRevealDressRequestChoice", "sandra", 1)),
        MenuItem("Сказать, что пока не время", Call("HouseholdRevealDressRequestChoice", "sandra", 0)),
    ]
    return


label MelissaDressRequestEvent:
    $ MelissaVar["revealing_dress_request_seen"] = 1
    if renpy.loadable("images/melissa/tavern/melissa_portrait.png"):
        $ _layout_last_picture = "images/melissa/tavern/melissa_portrait.png"
    $ MainTxt = "Мелисса, дождавшись пока вокруг станет потише, смущенно признается: \"Я видела, какой наряд ты выбрал для Сандры. Если уж ей можно что-то посмелее, может и мне когда-нибудь подберешь платье не только для работы, но и чтобы самой себе нравиться?\"\n\nСказав это, она тут же опускает глаза, но по голосу слышно, что мысль ей давно не дает покоя."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ваш ответ"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Согласиться подобрать Мелиссе похожий наряд", Call("HouseholdRevealDressRequestChoice", "melissa", 1)),
        MenuItem("Посоветовать ей пока не спешить", Call("HouseholdRevealDressRequestChoice", "melissa", 0)),
    ]
    return


label AmandaDressRequestEvent:
    $ AmandaVar["revealing_dress_request_seen"] = 1
    if renpy.loadable("images/amanda/amanda_portrate.jpg"):
        $ _layout_last_picture = "images/amanda/amanda_portrate.jpg"
    $ MainTxt = "Аманда сама подскакивает к вам, едва улучив момент. \"Стефан, это нечестно! У Сандры теперь наряд посмелее, Мелиссе ты тоже обещаешь что-то красивое, а я что, хуже? Мне тоже хочется платье, чтобы ахнули, а не только подносы таскать!\"\n\nПохоже, увиденное окончательно раззадорило ее самолюбие."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ваш ответ"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Пообещать подобрать Аманде такой же смелый наряд", Call("HouseholdRevealDressRequestChoice", "amanda", 1)),
        MenuItem("Сказать, что пока хватит и чужих обновок", Call("HouseholdRevealDressRequestChoice", "amanda", 0)),
    ]
    return


label HouseholdRevealDressRequestChoice(girl_name="", agree=0):
    $ _request_girl = str(girl_name or "").strip().lower()
    if _request_girl == "":
        call HouseholdReturnCurrentRoom

    if int(agree or 0) == 1:
        $ DailyEventsList_Add(_request_girl, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
        if _request_girl == "sandra":
            $ MainTxt = "Вы киваете Сандре и обещаете, что в ближайшее время заглянете с ней к Ирме и подберете что-нибудь заметно смелее ее обычных платьев. Сандра делает вид, что это пустяк, но по довольной полуулыбке видно: такой ответ ей пришелся по душе."
            $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
        elif _request_girl == "melissa":
            $ MainTxt = "Вы обещаете Мелиссе, что не забудете о ее просьбе и подберете у Ирмы что-нибудь похожее, но по ее характеру. Мелисса заметно оживляется и тихо благодарит вас."
            $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
        else:
            $ MainTxt = "Вы соглашаетесь, что раз уж в доме одна за другой появляются новые наряды, то и Аманду обделять не стоит. Услышав это, девушка сияет так, будто обновка уже висит у нее в шкафу."
            $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    else:
        if _request_girl == "sandra":
            $ MainTxt = "Вы отвечаете Сандре, что с этим пока лучше не торопиться. Она только фыркает, возвращается к кастрюлям и делает вид, что разговор ничего для нее не значил."
        elif _request_girl == "melissa":
            $ MainTxt = "Вы мягко советуете Мелиссе пока не спешить с такими обновками. Девушка кивает, хотя по голосу слышно, что надеялась на другой ответ."
        else:
            $ MainTxt = "Вы осаживаете Аманду и говорите, что пока хватит и тех обновок, что уже обсуждаются в доме. Аманда недовольно надувает губы, но спорить не продолжает."
    $ CurLocDesc = MainTxt
    call HouseholdReturnCurrentRoom


label MelissaClaraOverhearEvent:
    $ household_mark_runtime_event_seen("melissa_clara_overhear")
    if melissa_clara_overhear_variant() == 0:
        $ MainTxt = "Вы невольно задерживаетесь у соседнего стола и успеваете услышать, как Кларисса, давясь смехом, шепчет Мелиссе: \"У старой водокачки за лесом, где беседка, играли две собачки, как папа и соседка\".\n\nМелисса сначала краснеет до самых ушей, потом тоже не выдерживает и тихо прыскает. Похоже, такая пошлая прибаутка оседает у нее в голове куда глубже, чем она хотела бы признать."
        $ sluttiness["melissa"] = min(100, int(sluttiness.get("melissa", 0) or 0) + 3)
    else:
        $ MainTxt = "Проходя через зал, вы замечаете, как Мелисса с Клариссой о чем-то переговариваются в стороне от общего шума. Разобрать слова не удается, зато до вас вполне отчетливо доносятся тихие хихиканья, влажные чмокающие звуки и приглушенные стоны. Когда вы оборачиваетесь, обе уже делают вид, что обсуждали что-то совершенно невинное."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    return


label TavernStorageRatEvent:
    $ household_mark_runtime_event_seen("melissa_storage_rat")
    if renpy.loadable("game/images/melissa/tavern/rat_in_basement_melissa.png"):
        $ _layout_last_picture = "game/images/melissa/tavern/rat_in_basement_melissa.png"
    elif renpy.loadable("images/melissa/tavern/rat_in_basement_melissa.png"):
        $ _layout_last_picture = "images/melissa/tavern/rat_in_basement_melissa.png"
    $ MainTxt = "В кладовой вас встречает раздраженная Мелисса: у мешков с крупой шуршит крупная крыса, а девушка уже стоит наготове с метлой в руках. \"Опять эта тварь сюда лазит,\" шепчет она. \"Если ее сейчас не прогнать, потом весь угол придется перебирать заново.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Крыса в кладовой"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Прибить крысу", Call("TavernStorageRatChoice", 1)),
        MenuItem("Оставить все как есть", Call("TavernStorageRatChoice", 0)),
    ]
    return


label TavernStorageRatChoice(kill_rat=0):
    if int(kill_rat or 0) == 1:
        $ MelissaVar["storage_rat_cleared"] = 1
        $ MelissaVar["storage_rat_last_help_day"] = int(dayspassed or 0)
        $ MelissaVar["work_attitude"] = int(MelissaVar.get("work_attitude", 0) or 0) + 1
        $ cleaning["melissa"] = min(100, int(cleaning.get("melissa", 0) or 0) + 1)
        $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
        $ MainTxt = "Вы быстро расправляетесь с крысой, и Мелисса заметно расслабляется. \"Вот теперь другое дело,\" тихо говорит она, уже без прежнего раздражения. Похоже, такая помощь только укрепляет ее привычку относиться к хозяйству всерьез."
    else:
        $ MainTxt = "Вы решаете не возиться с крысой прямо сейчас. Мелисса поджимает губы и берется переставлять мешки подальше от шороха, явно недовольная тем, что проблему придется терпеть еще какое-то время."
    $ CurLocDesc = MainTxt
    call HouseholdReturnCurrentRoom


label MelissaRoomPestsEvent:
    $ household_mark_runtime_event_seen("melissa_room_pests")
    $ MainTxt = "В комнате Мелиссы явно не все спокойно: в углах висит свежая паутина, под потолком шуршат летучие мыши, а сама она сердито косится то на темные балки, то на кровать. \"То крысы внизу, то пауки тут, то опять эти мерзкие крылатые твари над головой,\" ворчит девушка. \"Ночью от них никакого покоя.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Непрошеные твари"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вымести паутину и прогнать мышей", Call("MelissaRoomPestsChoice", 1)),
        MenuItem("Оставить это на потом", Call("MelissaRoomPestsChoice", 0)),
    ]
    return


label MelissaRoomPestsChoice(help_pests=0):
    if int(help_pests or 0) == 1:
        $ MelissaVar["room_pests_cleared"] = 1
        $ MelissaVar["room_pests_last_help_day"] = int(dayspassed or 0)
        $ MelissaVar["work_attitude"] = int(MelissaVar.get("work_attitude", 0) or 0) + 1
        $ cleaning["melissa"] = min(100, int(cleaning.get("melissa", 0) or 0) + 1)
        $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
        $ MainTxt = "Вы быстро смахиваете паутину, шумом поднимаете с балок летучих мышей и выпроваживаете их наружу. Мелисса облегченно выдыхает: похоже, порядок в ее комнате для нее и правда важен."
    else:
        $ MainTxt = "Вы решаете пока не возиться с пауками и мышами. Мелисса кривится и недовольно косится на потолок, понимая, что вечером ей снова придется слушать это шуршание."
    $ CurLocDesc = MainTxt
    jump TavernMelissaRoom


label HouseholdMorningIssueCure(girl_name=""):
    $ _issue_girl = str(girl_name or "").strip().lower()
    if household_morning_issue_type(_issue_girl) != "sick":
        call HouseholdReturnCurrentRoom
        return
    if int(_player_item_count_by_id("healing_potion_001") or 0) <= 0:
        $ MainTxt = "Без лечебного зелья тут пока не обойтись."
        $ CurLocDesc = MainTxt
        call HouseholdReturnCurrentRoom
        return
    $ _player_remove_item_by_id("healing_potion_001", 1)
    $ household_clear_morning_issue(_issue_girl)
    $ Friends[_issue_girl] = min(20, int(Friends.get(_issue_girl, 0) or 0) + 1)
    $ otkroven[_issue_girl] = min(20, int(otkroven.get(_issue_girl, 0) or 0) + 1)
    $ MainTxt = "%s с благодарностью принимает лечебное зелье. Через несколько минут ей заметно легчает, и она уже выглядит так, будто сможет вернуться к обычным делам." % _action_display_name(_issue_girl)
    $ CurLocDesc = MainTxt
    call HouseholdReturnCurrentRoom
    return


label HouseholdWakeSleepyGirl(girl_name=""):
    $ _wake_girl = str(girl_name or "").strip().lower()
    if household_morning_issue_type(_wake_girl) != "sleepy":
        call HouseholdReturnCurrentRoom
        return
    $ _wake_indecent = household_morning_issue_indecent(_wake_girl)
    $ _wake_bulge = 1 if _wake_indecent and player_has_visible_morning_bulge() else 0
    $ calendar_advance_minutes(20)
    $ household_clear_morning_issue(_wake_girl)
    $ Friends[_wake_girl] = min(20, int(Friends.get(_wake_girl, 0) or 0) + 1)
    if _wake_girl == "sandra":
        $ MainTxt = "Вы осторожно будите Сандру. Та сначала недовольно морщится, потом резко собирается, будто сама сердится не на вас, а на то, что дала себе лишнюю слабину."
        if _wake_indecent:
            $ MainTxt = str(MainTxt or "") + "\n\nПока Сандра поднималась, вы невольно успели заметить, что рубаха на ней сбилась куда выше приличного. Поймав ваш взгляд, она без лишней суеты поправляет ткань, но в ее лице на миг мелькает совсем не хозяйская, а женская неловкость."
            $ sluttiness["sandra"] = min(100, int(sluttiness.get("sandra", 0) or 0) + 1)
        if _wake_bulge:
            if int(Friends.get("sandra", 0) or 0) >= 10 or int(sluttiness.get("sandra", 0) or 0) >= 20:
                $ MainTxt = str(MainTxt or "") + "\n\nСандра успевает заметить и вашу слишком уж явную выпуклость под одеждой. Вместо скандала она только сухо хмыкает: \"Вот и думай после этого, кто тут проспал по-настоящему.\""
                $ otkroven["sandra"] = min(20, int(otkroven.get("sandra", 0) or 0) + 1)
            else:
                $ MainTxt = str(MainTxt or "") + "\n\nКогда Сандра замечает, что у вас под одеждой все слишком уж на виду, она мгновенно щурится и велит вам сперва привести себя в порядок, а уже потом лезть кого-то будить."
    elif _wake_girl == "melissa":
        $ MainTxt = "Вы будите Мелиссу тихо, но настойчиво. Она вздрагивает, садится на кровати и явно с трудом возвращается в явь, потом понимает, который час, и недовольно выдыхает себе под нос."
        if _wake_indecent:
            $ MainTxt = str(MainTxt or "") + "\n\nВо сне одеяло успело сползти, и вам открывается куда больше, чем Мелисса обычно позволяет увидеть днем. Осознав это, она быстро оправляется, но вместо злости в ее лице остается скорее смущенное раздражение."
            $ sluttiness["melissa"] = min(100, int(sluttiness.get("melissa", 0) or 0) + 1)
        if _wake_bulge:
            if int(Friends.get("melissa", 0) or 0) >= 10 or int(sluttiness.get("melissa", 0) or 0) >= 18:
                $ MainTxt = str(MainTxt or "") + "\n\nМелисса замечает вашу выпуклость под штанами, замолкает на полуслове и опускает взгляд. Потом, уже тише, чем прежде, бросает: \"Ну... в следующий раз хоть стучи чуть дольше.\""
                $ otkroven["melissa"] = min(20, int(otkroven.get("melissa", 0) or 0) + 1)
            else:
                $ MainTxt = str(MainTxt or "") + "\n\nКогда Мелисса замечает, что вы явились будить ее в слишком уж красноречивом состоянии, она вспыхивает и немедленно отворачивается, явно желая закончить разговор как можно быстрее."
    else:
        $ MainTxt = "Вы будите Аманду, и та сперва лишь что-то недовольно бурчит в подушку. Но стоит ей понять, что утренний стол уже давно собирается без нее, как она мигом оживает и принимается оправдываться."
        if _wake_indecent:
            $ MainTxt = str(MainTxt or "") + "\n\nВо сне Аманда успела раскрыться куда сильнее приличного, и вам открывается достаточно, чтобы понять: спать скромницей она умеет не всегда. Поняв по вашему лицу, что вы успели увидеть лишнее, она сперва краснеет, а потом упрямо делает вид, будто это пустяк."
            $ sluttiness["amanda"] = min(100, int(sluttiness.get("amanda", 0) or 0) + 1)
        if _wake_bulge:
            if int(Friends.get("amanda", 0) or 0) >= 10 or int(sluttiness.get("amanda", 0) or 0) >= 30:
                $ MainTxt = str(MainTxt or "") + "\n\nАманда быстро замечает и вашу предательскую выпуклость. Вместо того чтобы смутиться, она хихикает, бросает на вас хитрый взгляд и только потом начинает поспешно поправлять одежду."
                $ sluttiness["amanda"] = min(100, int(sluttiness.get("amanda", 0) or 0) + 1)
            else:
                $ MainTxt = str(MainTxt or "") + "\n\nСтоит Аманде заметить ваш слишком уж выразительный стояк, как она фыркает, закатывает глаза и тут же прикрывается одеялом уже куда тщательнее."
    $ CurLocDesc = MainTxt
    call HouseholdReturnCurrentRoom
    return


label MelissaNightWakeEvent:
    $ household_mark_runtime_event_seen("melissa_night_wake")
    $ MainTxt = "Вы уже почти проваливаетесь в сон, когда в дверь осторожно, но настойчиво стучат. На пороге оказывается встревоженная Мелисса: то ли в ее комнате снова шуршит какая-то дрянь под потолком, то ли из темного угла опять выскочила крыса. Одной ей туда возвращаться совсем не хочется."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ночная просьба Мелиссы"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Спокойно пойти с ней и помочь", Call("MelissaNightWakeChoice", 1)),
        MenuItem("Успокоить, прижать к себе и потом помочь", Call("MelissaNightWakeChoice", 2)),
        MenuItem("Проворчать и отправить ее обратно", Call("MelissaNightWakeChoice", 0)),
    ]
    return


label MelissaNightWakeChoice(choice_value=0):
    $ _melissa_night_choice = int(choice_value or 0)
    if _melissa_night_choice == 1:
        $ calendar_advance_minutes(20)
        $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
        $ MelissaVar["work_attitude"] = int(MelissaVar.get("work_attitude", 0) or 0) + 1
        $ MainTxt = "Вы поднимаетесь вместе с Мелиссой, быстро прогоняете ночную дрянь из ее комнаты и помогаете ей успокоиться. На прощание она благодарит вас уже куда мягче обычного: видно, что такая помощь ей важна."
    elif _melissa_night_choice == 2:
        $ calendar_advance_minutes(30)
        $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
        $ otkroven["melissa"] = min(20, int(otkroven.get("melissa", 0) or 0) + 1)
        $ sluttiness["melissa"] = min(100, int(sluttiness.get("melissa", 0) or 0) + 2)
        $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
        $ MelissaVar["work_attitude"] = int(MelissaVar.get("work_attitude", 0) or 0) + 1
        $ MainTxt = "Вы сначала притягиваете Мелиссу к себе и даете ей выдохнуть в тишине, а уже потом идете разбираться с шорохами. Когда все заканчивается, она еще ненадолго остается рядом, благодарит вас шепотом и уходит заметно теплее и смелее, чем пришла."
    else:
        $ Friends["melissa"] = max(0, int(Friends.get("melissa", 0) or 0) - 1)
        $ MainTxt = "Вы бурчите, что ночью вам не до таких хлопот, и отправляете Мелиссу разбираться самой. Она ничего не отвечает, но по ее лицу видно, что такой ответ ей очень не по душе."
    $ CurLocDesc = MainTxt
    return
