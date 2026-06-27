default TownStreetEventsToday = 0
default TownStreetPatrolsToday = 0
default TownStreetFightToday = 0
default TownCurfewCaughtToday = 0
default TownStreetStorySeenKeys = []
default TownStreetDailyPlan = {}
default TownStreetLastEventText = ""
default TownStreetContext = {}
default TownStreetFiredLabelsToday = []
default TownStreetFiredLocationsToday = []
default TownStreetCooldowns = {}

default GuardCaptainVar = {}
default TavernBlackworkers = []
default TavernBlackworkerCandidates = []

init -20 python:

    class TownStreetRuntime(object):
        LOCATIONS = ("StreetTavern", "MarketPlace", "PortStreets", "ArtisansQuarter")

        STREET_NAMES = {
            "пекарей": "улице Пекарей",
            "кожевенников": "на Кожевенной",
            "мясников": "на Мясницкой",
            "шорников": "в переулке Шорников",
            "бочкарей": "во дворе Бочкарей",
            "шляпников": "на Проходе Шляпников",
            "портных": "на Портняжьей",
        }

        OCCUPATIONS = {
            "male": (
                "крестьянин",
                "мастеровой",
                "матрос",
                "грузчик",
                "стражник",
                "торговец",
                "горожанин",
            ),
            "female": (
                "крестьянка",
                "мастеровая",
                "служанка",
                "торговка",
                "горожанка",
                "прачка",
                "швея",
                "травница",
            ),
        }

        PASSIVE_GUARDS = (
            " Мимо лениво проходят двое стражников, посмеиваются, но даже пальцем не шевелят.",
            " Стражники стоят в стороне с фляжкой и только качают головами.",
            " Один стражник опирается на алебарду и ухмыляется: «Пусть сами разбираются».",
            " Городская стража слишком занята своей выпивкой, чтобы обращать внимание на крики.",
        )

        TIME_EVENTS = {
            "morning": (
                {"hooks": ("bounty", "werewolf", "corpse"), "text": "На [улица] бьет колокол. Городской глашатай в красном камзоле громко зачитывает указ бургомистра: «Всем добрым христианам! За голову лесного оборотня, что уже загрыз трех пастухов и одну девку, - награда 100 золотых и прощение всех грехов!» Толпа шепчется о проклятии, а в канаве лежит обглоданный труп бродяги - кровь еще не свернулась."},
                {"hooks": ("vampire", "witch", "corpse"), "gender": "male", "text": "Утренний туман на [улица] скрывает страшную находку. [имя] - [занятие] наткнулся на полностью обескровленное тело девушки. «Опять упырь из леса! Или та ведьма, что сбежала с костра прошлой весной!» - кричит он. Прохожие крестятся, а стражники только пожимают плечами и пьют из фляжки."},
                {"hooks": ("stocks", "moral", "shame"), "gender": "female", "text": "У позорного столба на [улица] стоит голая по пояс [имя] - [занятие], с табличкой «За блуд и содомию». Толпа плюет, бросает гнилые овощи и камни. Рядом глашатай объявляет: «Так будет со всяким, кто нарушит чистоту нравов!»"},
                {"hooks": ("gallows", "mayor", "forest"), "text": "Рассвет на [улица] озаряет виселицу. Тело вчерашнего вора еще качается на ветру, вороны выклевывают глаза. «Бургомистр сказал - пример для остальных», - бормочет [имя] - [занятие], а из леса доносится вой, от которого мурашки по коже."},
                {"hooks": ("black_dog", "curse", "abduction"), "gender": "female", "text": "Молодая [имя] бежит по [улица], юбки в крови, кричит: «Он вышел из леса! Черный пес с горящими глазами! Утащил мою сестру!» Толпа крестится и шепчет о старом проклятии, что легло на город после той алхимической вспышки в прошлом году."},
                {"hooks": ("plague", "potion", "ghost"), "gender": "male", "text": "На [улица] [имя] - [занятие] продает «чудодейственное» зелье от французской болезни. «Пейте, пока чума не вернулась!» - орет он. В толпе шепчутся, что вчера ночью видели призрак повешенной ведьмы именно на этой улице."},
            ),
            "noon": (
                {"hooks": ("edict", "witch", "smuggling"), "text": "Полдень на [улица] - жара и вонь. Глашатай кричит: «Указ бургомистра! Всех, кто прячет беглых ведьм или оборотней, - на костер вместе с ними!» Рядом [имя] - [занятие] публично порют кнутом за укрывательство контрабанды из леса."},
                {"hooks": ("fight", "gambling", "fine"), "text": "На площади вспыхивает драка из-за последней бочки эля. Двое мужчин режут друг друга ножами, кровь льется в пыль. Толпа делает ставки, а глашатай спокойно объявляет: «Победитель платит штраф за нарушение тишины!»"},
                {"hooks": ("horse", "curse", "black_slime"), "text": "Жеребец [stallion] вдруг встает на дыбы и сбрасывает седока. Из его глаз капает черная слизь. «Проклят лесом!» - вопит [имя] - [занятие]. Люди разбегаются, вспоминая прошлогоднюю историю, когда все лошади в городе сошли с ума."},
                {"hooks": ("confession", "demon", "sin"), "gender": "male", "text": "В полдень на [улица] [имя] - [занятие] стоит на коленях перед женой и умоляет простить за то, что «продал душу лесному демону за одну ночь с блудницей». Толпа смеется, но многие крестятся - слухи о договорах с нечистью ходят уже второй месяц."},
                {"hooks": ("cart", "corpse", "bandits"), "text": "Опрокинутая телега на [улица]. Среди рассыпанных яблок - окровавленный труп контрабандиста со вспоротым животом. «Это дело рук лесных разбойников», - шепчут люди, а глашатай уже объявляет награду за их головы."},
                {"hooks": ("public_sin", "plague", "guards"), "gender": "male", "text": "На [улица] толстый [имя] - [занятие] публично совокупляется с служанкой прямо у стены, не стесняясь толпы. «Пусть смотрят! После чумы жизнь коротка!» - орет он. Стражники проходят мимо и только ржут."},
            ),
            "weekends": (
                {"hooks": ("market_day", "witch_bounty", "amulets"), "text": "Базарный день на [улица] - сплошной грех. Глашатай объявляет: «Бургомистр обещает 50 золотых тому, кто принесет доказательство, что ведьма из леса мертва!» Толпа ревет, а рядом уже торгуют «волшебными» амулетами от оборотней."},
                {"hooks": ("horse", "curse", "accident"), "text": "Выходной разгул: [имя] - [занятие] после эля пытается оседлать [stallion], но конь сбрасывает его и топчет. Из раны хлещет черная кровь. «Проклятие леса!» - вопит толпа."},
                {"hooks": ("cockfight", "witch_hunt", "guards"), "text": "На площади устроили петушиный бой, но вдруг кто-то кричит: «Ведьма! Она здесь!» Начинается охота на нищую старуху. Стражники делают ставки, кто первый поймает."},
                {"hooks": ("barrel_dance", "sin_tax", "crowd"), "text": "Пышная девица танцует на бочке, юбки задраны. Мужики лезут руками, она бьет каблуком в зубы. Глашатай кричит: «Так будет со всеми блудницами, если не заплатят налог на грех!»"},
                {"hooks": ("balcony", "black_beast", "forest"), "gender": "male", "text": "Выходной хаос на [улица]: [имя] показывает голую задницу с балкона, а друзья закидывают его гнилыми овощами. Вдруг из леса доносится вой - все замолкают. «Опять он... черный зверь», - шепчут люди."},
                {"hooks": ("horse_fair", "fight", "mayor_decree"), "text": "Ярмарка лошадей на [улица]. Двое спорят о плате за случку, дерутся до крови. Глашатай объявляет: «Победитель получает право первой ночи с любой вдовой города - указ бургомистра!»"},
            ),
            "evening": (
                {"hooks": ("curfew", "alley", "edict"), "text": "Сумерки на [улица]. Из темного переулка доносятся стоны и хрипы - пара совокупляется у стены, даже не прячась. Рядом глашатай вешает новый указ: «Комендантский час после заката! Лесные твари выходят на охоту»."},
                {"hooks": ("bandits", "message", "witch"), "gender": "male", "text": "Вечером на [улица] [имя] - [занятие] находит у порога отрезанную голову своего брата. «Это послание от лесных разбойников... или от той ведьмы», - шепчет он. Толпа крестится."},
                {"hooks": ("music", "dance", "ghost"), "gender": "male", "text": "На площади играет скрипач. [имя] - [занятие] крутит партнершу так, что корсаж лопается. Но вдруг музыка обрывается - кто-то кричит: «Призрак! Призрак повешенной ведьмы!» Все разбегаются."},
                {"hooks": ("knife_fight", "werewolf_notice", "town_law"), "text": "Пьяная драка на [улица] перерастает в поножовщину. Один падает с распоротым животом. Глашатай спокойно проходит мимо: «Пусть сами разбираются. У меня указ о поимке оборотня»."},
                {"hooks": ("horse", "forest_shadow", "curse"), "gender": "male", "text": "Сумерки на [улица]: [stallion] вырывается и несется в лес. За ним - черная тень. Хозяин [имя] - [занятие] падает на колени: «Он забрал его... лес забрал!»"},
                {"hooks": ("bribe", "plague", "street_sin"), "gender": "male", "text": "Вечерний свет на [улица]. [имя] - [занятие] сует монеты служанке, пока муж смотрит. «После заката все позволено», - смеется он. В толпе шепчутся о чуме, которая якобы вернулась."},
            ),
            "night": (
                {"hooks": ("curfew", "black_dog", "stable"), "text": "Под луной на [улица] пара яростно совокупляется у конюшни. Их стоны заглушает вой из леса. Глашатай уже ушел, но на столбе висит свежий указ: «Кто увидит черного пса - немедленно к бургомистру!»"},
                {"hooks": ("thief", "stocks", "mob"), "text": "Глубокой ночью на площади толпа раздевает пойманного вора и гонит его прутьями. «А теперь - на костер, как ведьму!» - орет кто-то. Кровь течет по булыжникам."},
                {"hooks": ("sailors", "werewolf", "corpse"), "text": "На [улица] два матроса делят женщину по очереди за таверной. Вдруг один падает мертвым - горло разорвано. «Оборотень!» - кричит второй и убегает в ночь."},
                {"hooks": ("murder", "paw_tracks", "dog"), "gender": "male", "text": "В ночной тишине на [улица] [имя] - [занятие] валяется в канаве, штаны спущены, горло перерезано. Рядом - следы огромных лап. Собака обнюхивает кровь."},
                {"hooks": ("street_worker", "curse", "mystery_laugh"), "text": "Полночь на [улица]: шлюха торгуется с клиентом. «Еще два пенса - и возьму в рот... если не боишься проклятия леса». Вдруг из тьмы раздается женский смех - никто не видит лица."},
                {"hooks": ("horse", "night_panic", "forest_demon"), "text": "В глухую ночь [stallion] вышибает забор. Полураздетые горожане бегают с факелами. «Он вернулся! Лесной демон в теле коня!» - вопит [имя] - [занятие]."},
            ),
        }

        def _get(self, name, default=None):
            key = str(name or "")
            if key == "clock_minutes":
                return clock_minutes
            if key == "CurLoc":
                return CurLoc
            if key == "dayspassed":
                return dayspassed
            if key == "energy":
                return energy
            if key == "exploration":
                return exploration
            if key == "GuardCaptainVar":
                return GuardCaptainVar
            if key == "health":
                return health
            if key == "hour":
                return hour
            if key == "minute":
                return minute
            if key == "notoriety":
                return notoriety
            if key == "RandomNameCode":
                return RandomNameCode
            if key == "RandomStallionNameCode":
                return RandomStallionNameCode
            if key == "RandomStreetNameCode":
                return RandomStreetNameCode
            if key == "TavernBlackworkerCandidates":
                return TavernBlackworkerCandidates
            if key == "TavernBlackworkers":
                return TavernBlackworkers
            if key == "time":
                return time
            if key == "TownStreetContext":
                return TownStreetContext
            if key == "TownStreetCooldowns":
                return TownStreetCooldowns
            if key == "TownStreetDailyPlan":
                return TownStreetDailyPlan
            if key == "TownStreetEventsToday":
                return TownStreetEventsToday
            if key == "TownStreetFightToday":
                return TownStreetFightToday
            if key == "TownStreetFiredLabelsToday":
                return TownStreetFiredLabelsToday
            if key == "TownStreetFiredLocationsToday":
                return TownStreetFiredLocationsToday
            if key == "TownStreetStorySeenKeys":
                return TownStreetStorySeenKeys
            if key == "week":
                return week
            return default

        def _int(self, value, default=0):
            try:
                return int(value)
            except Exception:
                try:
                    return int(float(value))
                except Exception:
                    return default

        def _screen_text(self, value):
            return str(value).replace("[", "[[").replace("{", "{{")

        def _call_name(self, gender=None):
            fn = self._get("RandomNameCode", None)
            key = self._gender_key(gender)
            if callable(fn):
                return fn(gender=key, nationality=procedural_choice(["German", "French", "Italian"], key="procedural:Town/RandomTownEvents.rpy:procedural_choice:174:1"))
            fallback = {
                "male": ("Ганс", "Пьер", "Томас", "Сергио"),
                "female": ("Мария", "Лючия", "Анна", "Франческа"),
            }
            return procedural_choice(fallback.get(key, fallback["male"]), key="procedural:Town/RandomTownEvents.rpy:procedural_choice:179:2")

        def _gender_key(self, gender=None):
            key = str(gender or "").strip().lower()
            if key in ("male", "female"):
                return key
            return procedural_choice(["male", "female"], key="procedural:Town/RandomTownEvents.rpy:procedural_choice:185:3")

        def _call_occupation(self, gender=None):
            key = self._gender_key(gender)
            return procedural_choice(self.OCCUPATIONS.get(key, self.OCCUPATIONS["male"]), key="procedural:Town/RandomTownEvents.rpy:procedural_choice:189:4")

        def _call_stallion(self):
            fn = self._get("RandomStallionNameCode", None)
            if callable(fn):
                return fn()
            return procedural_choice(["Черный", "Буян", "Гром"], key="procedural:Town/RandomTownEvents.rpy:procedural_choice:195:5")

        def location_allowed(self, location_name=""):
            return str(location_name or self._get("CurLoc", "") or "") in self.LOCATIONS

        def event_key(self, location_name="", label_name=""):
            return "%s:%s:%s" % (
                self._int(self._get("dayspassed", 0), 0),
                str(location_name or self._get("CurLoc", "") or ""),
                str(label_name or "day"),
            )

        def probability_roll(self, label_name="", location_name="", chance=0):
            chance_value = max(0, min(100, self._int(chance, 0)))
            if chance_value <= 0:
                return False
            if chance_value >= 100:
                return True
            key = "town_event_%s_%s_%s_%s_%s" % (
                str(label_name or ""),
                str(location_name or self._get("CurLoc", "") or ""),
                self._int(self._get("dayspassed", 0), 0),
                self._int(self._get("clock_minutes", 0), 0),
                self._int(self._get("notoriety", 0), 0),
            )
            return procedural_randint(1, 100, key) <= chance_value

        def beggar_chance(self):
            return 10

        def thug_chance(self):
            return 10

        def patrol_chance(self):
            return min(100, 25 + max(0, self._int(self._get("notoriety", 0), 0) // 2))

        def chronicle_chance(self):
            return 25

        def curfew_active(self):
            clock_value = self._int(self._get("clock_minutes", -1), -1)
            hour_value = self._int(self._get("hour", -1), -1)
            minute_part = self._int(self._get("minute", 0), 0) % 60
            if 0 <= hour_value <= 23:
                visible_minutes = (hour_value * 60) + minute_part
                # Location/event code sometimes sets legacy hour/minute before the
                # canonical clock mirror is synced. For curfew, visible time wins.
                if clock_value < 0 or abs((clock_value % 1440) - visible_minutes) > 1:
                    minute_value = visible_minutes
                else:
                    minute_value = clock_value % 1440
            else:
                minute_value = clock_value % 1440
            return minute_value >= 21 * 60 + 30 or minute_value <= 5 * 60 + 30

        def random_seen_this_slot(self, location_name="", label_name=""):
            keys = self._get("TownStreetStorySeenKeys", [])
            location_key = str(location_name or self._get("CurLoc", "") or "")
            label_key = str(label_name or self.planned_label(location_key) or "day")
            return (
                self.event_key(location_key, "day") in list(keys or [])
                or self.event_key(location_key, label_key) in list(keys or [])
                or location_key in list(self._get("TownStreetFiredLocationsToday", []) or [])
                or (label_key != "day" and label_key in list(self._get("TownStreetFiredLabelsToday", []) or []))
            )

        def mark_seen(self, location_name="", label_name=""):
            keys = self._get("TownStreetStorySeenKeys", [])
            location_key = str(location_name or self._get("CurLoc", "") or "")
            label_key = str(label_name or self.planned_label(location_key) or "day")
            for key in (self.event_key(location_key, "day"), self.event_key(location_key, label_key)):
                if key not in keys:
                    keys.append(key)

            fired_locations = self._get("TownStreetFiredLocationsToday", [])
            if location_key and location_key not in fired_locations:
                fired_locations.append(location_key)

            fired_labels = self._get("TownStreetFiredLabelsToday", [])
            if label_key and label_key != "day" and label_key not in fired_labels:
                fired_labels.append(label_key)

            cooldowns = self._get("TownStreetCooldowns", {})
            if isinstance(cooldowns, dict) and label_key and label_key != "day":
                cooldowns[label_key] = max(
                    self._int(cooldowns.get(label_key, -1), -1),
                    self._int(self._get("dayspassed", 0), 0),
                )

        def event_on_cooldown(self, label_name="", cooldown_days=1):
            label_key = str(label_name or "")
            cooldowns = self._get("TownStreetCooldowns", {})
            if not isinstance(cooldowns, dict) or not label_key:
                return False
            last_day = self._int(cooldowns.get(label_key, -9999), -9999)
            return day_delta_since(last_day) < self._int(cooldown_days, 1)

        def ensure_daily_plan(self):
            plan = self._get("TownStreetDailyPlan", {})
            if not isinstance(plan, dict):
                TownStreetDailyPlan.clear()
                plan = TownStreetDailyPlan
            plan["day"] = self._int(self._get("dayspassed", 0), 0)
            plan["model"] = "probability"
            plan["events"] = {
                "beggar": self.beggar_chance(),
                "thugs": self.thug_chance(),
                "patrol": self.patrol_chance(),
                "patrol_base": 25,
                "patrol_notoriety_bonus": max(0, self._int(self._get("notoriety", 0), 0) // 2),
                "chronicle": self.chronicle_chance(),
                "chronicle_cooldown_days": 3,
            }
            return dict(plan["events"])

        def planned_label(self, location_name=""):
            return ""

        def planned_for(self, location_name="", label_name=""):
            label_key = str(label_name or "")
            if label_key == "TownStreetPatrolEvent":
                return self.patrol_allowed(location_name)
            if label_key == "TownStreetThugsEvent":
                return self.thug_allowed(location_name)
            if label_key == "TownStreetHelpEvent":
                return self.help_allowed(location_name)
            if label_key == "TownRandomChronicleEvent":
                return self.chronicle_allowed(location_name)
            return False

        def time_event_key(self):
            if self._int(self._get("week", 1), 1) in (6, 7):
                return "weekends"
            slot = self._int(self._get("time", 0), 0)
            if slot == 0:
                return "morning"
            if slot in (1, 2):
                return "noon"
            if slot == 3:
                return "evening"
            return "night"

        def street_display(self):
            fn = self._get("RandomStreetNameCode", None)
            rus = fn() if callable(fn) else "пекарей"
            return self.STREET_NAMES.get(rus, "на Рыночной площади")

        def random_chronicle(self, time_of_day="morning"):
            key = str(time_of_day or "morning")
            if key not in self.TIME_EVENTS:
                key = "morning"
            entry = procedural_choice(self.TIME_EVENTS[key], key="procedural:Town/RandomTownEvents.rpy:procedural_choice:346:6")
            text = str(entry.get("text", "") if isinstance(entry, dict) else entry)
            gender = self._gender_key(entry.get("gender", None) if isinstance(entry, dict) else None)
            if procedural_random(key="procedural:Town/RandomTownEvents.rpy:procedural_random:349:1") < float(entry.get("guard_chance", 0.45) if isinstance(entry, dict) else 0.45):
                text += procedural_choice(self.PASSIVE_GUARDS, key="procedural:Town/RandomTownEvents.rpy:procedural_choice:350:7")
            return (
                text
                .replace("[улица]", self.street_display())
                .replace("[имя]", self._call_name(gender))
                .replace("[занятие]", self._call_occupation(gender))
                .replace("[stallion]", self._call_stallion())
            )

        def interactive_allowed(self, location_name=""):
            location_key = str(location_name or self._get("CurLoc", "") or "")
            return (
                self.location_allowed(location_key)
                and location_key not in list(self._get("TownStreetFiredLocationsToday", []) or [])
                and self._int(self._get("TownStreetEventsToday", 0), 0) < 2
            )

        def patrol_pass_active(self):
            guard = self._get("GuardCaptainVar", {})
            try:
                return self._int(guard.get("street_pass", 0), 0) > 0
            except Exception:
                return False

        def patrol_allowed(self, location_name=""):
            if not self.interactive_allowed(location_name):
                return False
            if not self.curfew_active():
                return False
            if self.patrol_pass_active():
                return False
            if self.random_seen_this_slot(location_name, "TownStreetPatrolEvent"):
                return False
            return self.probability_roll("TownStreetPatrolEvent", location_name, self.patrol_chance())

        def thug_allowed(self, location_name=""):
            if not self.interactive_allowed(location_name):
                return False
            if self._int(self._get("TownStreetFightToday", 0), 0) > 0:
                return False
            if self.random_seen_this_slot(location_name, "TownStreetThugsEvent"):
                return False
            return self.probability_roll("TownStreetThugsEvent", location_name, self.thug_chance())

        def help_allowed(self, location_name=""):
            if not self.interactive_allowed(location_name):
                return False
            if self.random_seen_this_slot(location_name, "TownStreetHelpEvent"):
                return False
            return self.probability_roll("TownStreetHelpEvent", location_name, self.beggar_chance())

        def chronicle_allowed(self, location_name=""):
            if not self.interactive_allowed(location_name):
                return False
            if self.random_seen_this_slot(location_name, "TownRandomChronicleEvent"):
                return False
            if self.event_on_cooldown("TownRandomChronicleEvent", 3):
                return False
            return self.probability_roll("TownRandomChronicleEvent", location_name, self.chronicle_chance())

        def fine_amount(self, reason="fight"):
            if str(reason or "") == "counter_bribe":
                return 200
            return 50

        def escape_success(self, challenge=100):
            exploration_value = self._int(self._get("exploration", 0), 0)
            score = exploration_value + procedural_randint(1, 100, key="procedural:Town/RandomTownEvents.rpy:procedural_randint:417:1")
            if exploration_value >= 150:
                score += 35
            return score >= self._int(challenge, 100)

        def fight_success(self, enemy_level=2):
            fight_level = player_state(False).combat.fight_level
            try:
                you = self._int(fight_level.get("you", 1), 1)
            except Exception:
                you = 1
            score = you * 20 + (self._int(self._get("exploration", 0), 0) // 10) + procedural_randint(1, 60, key="procedural:Town/RandomTownEvents.rpy:procedural_randint:428:2")
            return score >= (self._int(enemy_level, 2) * 30 + 30)

        def apply_cloth_damage(self, amount=15):
            appearance = player_state().appearance
            appearance.costume_condition = max(0, self._int(appearance.costume_condition, 100) - self._int(amount, 15))
            appearance.apply_to_store()

        def apply_health_damage(self, amount=15):
            global health, energy
            amount_int = self._int(amount, 15)
            health = max(0, self._int(self._get("health", 100), 100) - amount_int)
            energy = max(0, self._int(self._get("energy", 100), 100) - max(5, amount_int // 2))

        def make_help_context(self):
            ctx = self._get("TownStreetContext", {})
            gender = self._gender_key()
            ctx["help_gender"] = gender
            ctx["help_name"] = self._call_name(gender)
            ctx["help_job"] = self._call_occupation(gender)
            return ctx

        def settle_blackworker_candidates(self):
            candidates = self._get("TavernBlackworkerCandidates", [])
            workers = self._get("TavernBlackworkers", [])
            joined = 0
            while len(candidates) > 0:
                worker = candidates.pop(0)
                try:
                    worker["active_day"] = self._int(self._get("dayspassed", 0), 0) + 1
                    worker["trust"] = max(0, self._int(worker.get("trust", 0), 0))
                except Exception:
                    pass
                workers.append(worker)
                joined += 1
            return joined

    town_street = TownStreetRuntime()


label TownRandomChronicleEvent:
    $ SignalBlockTime = 1
    $ TownStreetEventsToday = int(TownStreetEventsToday or 0) + 1
    $ town_street.mark_seen(CurLoc, "TownRandomChronicleEvent")
    $ town_street.mark_seen(location, "TownRandomChronicleEvent")
    $ town_street.mark_seen(getattr(CurrentRoom, "code_name", ""), "TownRandomChronicleEvent")
    $ TownStreetLastEventText = town_street.random_chronicle(town_street.time_event_key())
    $ MainTxt = TownStreetLastEventText
    $ CurLocDesc = MainTxt
    $ current_action_title = "Городские слухи"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Идти дальше", Function(renpy.return_statement, True))]
    call screen main_ui
    return True


label TownStreetHelpEvent:
    $ SignalBlockTime = 1
    $ TownStreetEventsToday = int(TownStreetEventsToday or 0) + 1
    $ town_street.mark_seen(CurLoc, "TownStreetHelpEvent")
    $ town_street.mark_seen(location, "TownStreetHelpEvent")
    $ town_street.mark_seen(getattr(CurrentRoom, "code_name", ""), "TownStreetHelpEvent")
    $ _town_ctx = town_street.make_help_context()
    $ MainTxt = "У стены сидит измученный человек. По виду это %s - %s. Он просит не денег, а куска еды и места, где можно переждать ночь. Рядом двое прохожих делают вид, что не слышат." % (_town_ctx.get("help_name", "бродяга"), _town_ctx.get("help_job", "без ремесла"))
    $ CurLocDesc = MainTxt
    $ current_action_title = "Уличная просьба"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Дать еды и предложить грязную работу при трактире", Call("TownStreetHelpRecruit")),
        MenuItem("Дать пару мараведи", Call("TownStreetHelpMoney")),
        MenuItem("Пройти мимо", Function(renpy.return_statement, True)),
    ]
    call screen main_ui
    return True


label TownStreetHelpRecruit:
    $ _candidate_id = "bw_%03d" % (len(TavernBlackworkerCandidates) + len(TavernBlackworkers) + 1)
    $ TavernBlackworkerCandidates.append({"id": _candidate_id, "name": TownStreetContext.get("help_name", "бродяга"), "origin": "street_help", "day": int(dayspassed or 0), "sleep_place": "TavernStable", "trust": 0})
    $ exploration += 5
    $ tavernfame += 1
    $ MainTxt = "Вы обещаете еду, угол в конюшне и простую грязную работу. Человек хватается за это предложение так, будто вы протянули ему не хлеб, а целую жизнь. Если он не сбежит от страха, утром у трактира появится новый чернорабочий."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Function(renpy.return_statement, True))]
    return


label TownStreetHelpMoney:
    if money >= 2:
        $ money -= 2
        $ exploration += 3
        $ notoriety = max(0, int(notoriety or 0) - 10)
        $ MainTxt = "Вы даете пару мараведи. Благодарность выходит тихой и неловкой, но несколько прохожих это замечают."
    else:
        $ MainTxt = "Вы хлопаете по пустому кошелю и понимаете, что сейчас вам самому впору просить милостыню."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Function(renpy.return_statement, True))]
    return


label TownStreetThugsEvent:
    $ SignalBlockTime = 1
    $ TownStreetEventsToday = int(TownStreetEventsToday or 0) + 1
    $ TownStreetFightToday = int(TownStreetFightToday or 0) + 1
    $ town_street.mark_seen(CurLoc, "TownStreetThugsEvent")
    $ town_street.mark_seen(location, "TownStreetThugsEvent")
    $ town_street.mark_seen(getattr(CurrentRoom, "code_name", ""), "TownStreetThugsEvent")
    $ MainTxt = "Из бокового переулка вы слышите короткий вскрик. Двое крепких парней прижимают к стене растерянного горожанина и выворачивают ему руки. Увидев вас, один ухмыляется: «Проходи мимо, трактирщик. Не твое дело»."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Уличные громилы"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вмешаться и драться", Call("TownStreetThugsFight")),
        MenuItem("Попробовать спугнуть их криком", Call("TownStreetThugsShout")),
        MenuItem("Пройти мимо", Function(renpy.return_statement, True)),
    ]
    call screen main_ui
    return True


label TownStreetThugsFight:
    $ _thug_reputation_before = int(reputation or 0)
    $ _thug_tavernfame_before = int(tavernfame or 0)
    $ _thug_notoriety_before = int(notoriety or 0)
    $ notoriety = min(100, _thug_notoriety_before + 3)
    $ _thug_return_room = str(CurLoc or location or "StreetTavern")
    $ _thug_picture = str(_layout_last_picture or scene_image or "")
    $ _thug_intro = "Вы встаете между жертвой и громилами. Один сплевывает на мостовую и перехватывает дубинку: теперь разговор закончится только дракой."
    $ fight_begin("street_crook", 2, _thug_return_room, _thug_picture, _thug_intro)
    call FightLoop
    $ _thug_outcome = str(HuntLastResult.get("outcome", "") if isinstance(HuntLastResult, dict) else "")
    if _thug_outcome == "victory":
        $ reputation = min(100, _thug_reputation_before + 3)
        $ tavernfame = _thug_tavernfame_before + 1
        $ notoriety = min(100, _thug_notoriety_before + 3)
        $ MainTxt = str(MainTxt or "") + "\n\nВы отбили прохожего у громил. На улице это быстро запоминают: репутация +3, слава трактира +1."
        $ CurLocDesc = MainTxt
        $ renpy.notify("Репутация +3, слава трактира +1")
    elif _thug_outcome == "defeat":
        $ notoriety = max(0, int(notoriety or 0) - 2)
        $ MainTxt = str(MainTxt or "") + "\n\nГромилы уходят, убедившись, что вы больше не мешаете. Прохожие делают вид, что ничего не видели."
        $ CurLocDesc = MainTxt
    elif _thug_outcome == "retreat":
        $ reputation = max(0, int(reputation or 0) - 1)
        $ MainTxt = str(MainTxt or "") + "\n\nВы уходите из драки живым, но жертва остается на улице без вашей помощи: репутация -1."
        $ CurLocDesc = MainTxt
        $ renpy.notify("Репутация -1")
    if _thug_outcome in ("victory", "defeat", "retreat"):
        $ current_action_title = "Итог драки"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться", Function(renpy.return_statement, True))]
        call screen main_ui
    return True


label TownStreetThugsShout:
    $ _shout_reputation_before = int(reputation or 0)
    $ _shout_notoriety_before = int(notoriety or 0)
    $ _thug_return_room = str(CurLoc or location or "StreetTavern")
    $ _thug_picture = str(_layout_last_picture or scene_image or "")
    $ _shout_score = int(exploration or 0) + procedural_randint(1, 100, "town_thugs_shout_%s_%s_%s" % (int(dayspassed or 0), _thug_return_room, int(clock_minutes or 0)))
    if int(exploration or 0) >= 150:
        $ _shout_score += 35
    if _shout_score >= 85:
        $ exploration += 6
        $ reputation = min(100, int(reputation or 0) + 2)
        $ notoriety = min(100, int(notoriety or 0) + 4)
        $ MainTxt = "Вы громко зовете стражу и называете ближайшие дома так уверенно, будто уже знаете, куда побежите за подкреплением. Громилы переглядываются, ругаются и отступают в переулок. Прохожие запоминают, что вы не прошли мимо: репутация +2, дурная слава +4."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Громилы отступили"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться", Function(renpy.return_statement, True))]
        call screen main_ui
        return True
    else:
        $ notoriety = min(100, _shout_notoriety_before + 2)
        $ _thug_intro = "Ваш крик только злит громил. Один толкает жертву в грязь, второй разворачивается к вам с дубинкой: теперь они хотят наказать именно вас."
        $ fight_begin("street_crook", 2, _thug_return_room, _thug_picture, _thug_intro)
        call FightLoop
        $ _thug_outcome = str(HuntLastResult.get("outcome", "") if isinstance(HuntLastResult, dict) else "")
        if _thug_outcome == "victory":
            $ reputation = min(100, _shout_reputation_before + 2)
            $ notoriety = min(100, _shout_notoriety_before + 2)
            $ MainTxt = str(MainTxt or "") + "\n\nКрик не испугал громил, зато драка закончилась в вашу пользу. Прохожие запоминают это: репутация +2."
            $ CurLocDesc = MainTxt
            $ renpy.notify("Репутация +2")
        elif _thug_outcome == "retreat":
            $ reputation = max(0, int(reputation or 0) - 1)
            $ MainTxt = str(MainTxt or "") + "\n\nВы отступаете, и громилы остаются хозяевами улицы. Это не выглядит геройством: репутация -1."
            $ CurLocDesc = MainTxt
            $ renpy.notify("Репутация -1")
        if _thug_outcome in ("victory", "defeat", "retreat"):
            $ current_action_title = "Итог драки"
            $ current_action_content = None
            $ current_action_items = [MenuItem("Вернуться", Function(renpy.return_statement, True))]
            call screen main_ui
        return True


label TownStreetPatrolEvent:
    if not town_street.curfew_active():
        return False
    $ SignalBlockTime = 1
    $ TownStreetEventsToday = int(TownStreetEventsToday or 0) + 1
    $ TownStreetPatrolsToday = int(TownStreetPatrolsToday or 0) + 1
    $ town_street.mark_seen(CurLoc, "TownStreetPatrolEvent")
    $ town_street.mark_seen(location, "TownStreetPatrolEvent")
    $ town_street.mark_seen(getattr(CurrentRoom, "code_name", ""), "TownStreetPatrolEvent")
    $ scene_image = "images/general/cityguard.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image
    $ MainTxt = "Из темноты выступает ночной патруль капитана Циммера. Старший лениво поднимает фонарь к вашему лицу: «Комендантский час, добрый человек. Документы, пропуск или деньги. А если нет - пройдем до колодок»."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ночной патруль"
    $ current_action_content = None
    $ _fine = town_street.fine_amount("fight")
    $ current_action_items = [
        MenuItem("Заплатить штраф %d мараведи" % _fine, Call("TownStreetPatrolBribe")),
        MenuItem("Спрятаться и уйти дворами", Call("TownStreetPatrolHide")),
        MenuItem("Бежать", Call("TownStreetPatrolRun")),
        MenuItem("Драться со стражей", Call("TownStreetPatrolFight")),
    ]
    call screen main_ui
    return True


label TownStreetPatrolPass:
    if town_street.patrol_pass_active():
        $ exploration += 2
        $ MainTxt = "Вы показываете пропуск с отметкой капитана Циммера. Старший патруля недовольно кривится, но возвращает бумагу и велит не шататься без дела."
    else:
        $ MainTxt = "Никакого пропуска у вас нет. Старший патруля смотрит на пустые руки с усталой усмешкой."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Function(renpy.return_statement, True))]
    return


label TownStreetPatrolBribe:
    $ _fine = town_street.fine_amount("fight")
    if money >= _fine:
        $ money -= _fine
        $ notoriety = max(0, int(notoriety or 0) - 3)
        $ tavernfame = max(0, int(tavernfame or 0) - 1)
        $ LastAdvancedMinutes = 10
        $ calendar_v2.advance_minutes(10)
        $ MainTxt = "Монеты быстро исчезают в руке старшего. Патруль сразу теряет к вам интерес, будто никакого комендантского часа и не было. Вы теряете десять минут, дурная слава снижается на 3, но слух о ночной плате слегка бьет по славе трактира."
    else:
        jump TownStreetPatrolStocks
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Function(renpy.return_statement, True))]
    return


label TownStreetPatrolHide:
    if town_street.escape_success(115):
        $ exploration += 8
        $ notoriety = min(100, int(notoriety or 0) + 1)
        $ LastAdvancedMinutes = 20
        $ calendar_v2.advance_minutes(20)
        $ MainTxt = "Вы вовремя ныряете в темный проход, пережидаете шаги патруля и выбираетесь уже на другой стороне улицы. Обход занимает двадцать минут: исследование +8, дурная слава +1."
    else:
        $ MainTxt = "Вы пробуете уйти дворами, но задеваете ведро. Патруль мгновенно разворачивается на шум."
        jump TownStreetPatrolStocks
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Function(renpy.return_statement, True))]
    return


label TownStreetPatrolRun:
    if town_street.escape_success(130):
        $ exploration += 10
        $ notoriety = min(100, int(notoriety or 0) + 4)
        $ tavernfame = max(0, int(tavernfame or 0) - 1)
        $ LastAdvancedMinutes = 15
        $ calendar_v2.advance_minutes(15)
        $ MainTxt = "Вы срываетесь с места и уходите от патруля через узкие проходы. За спиной ругаются, но догнать вас уже не могут. Побег занимает пятнадцать минут: исследование +10, дурная слава +4, слава трактира -1."
    else:
        $ MainTxt = "Вы бросаетесь бежать, но улица оказывается слишком открытой. Вас сбивают древком алебарды и поднимают уже под смех патрульных."
        jump TownStreetPatrolStocks
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Function(renpy.return_statement, True))]
    return


label TownStreetPatrolFight:
    $ notoriety = min(100, int(notoriety or 0) + 12)
    $ tavernfame -= 2
    $ LastAdvancedMinutes = 10
    $ calendar_v2.advance_minutes(10)
    $ _patrol_return_room = str(CurLoc or location or "StreetTavern")
    $ _patrol_picture = "images/fight/patrol_guard.png"
    $ _patrol_intro = "Вы решаете не платить и не прятаться. Стражники переглядываются, опускают алебарды и берут вас в клещи. Теперь это настоящая драка с патрулем."
    $ fight_begin("patrol_guard", 2, _patrol_return_room, _patrol_picture, _patrol_intro)
    call FightLoop
    $ _patrol_outcome = str(HuntLastResult.get("outcome", "") if isinstance(HuntLastResult, dict) else "")
    if _patrol_outcome == "victory":
        $ notoriety = min(100, int(notoriety or 0) + 18)
        $ tavernfame = int(tavernfame or 0) - 3
        $ MainTxt = str(MainTxt or "") + "\n\nВы отбились от патруля, но это уже не мелкая ссора с ночной стражей. Дурная слава +18, слава трактира -3."
        $ CurLocDesc = MainTxt
        $ renpy.notify("Дурная слава +18, слава трактира -3")
    elif _patrol_outcome == "retreat":
        $ notoriety = min(100, int(notoriety or 0) + 4)
        $ MainTxt = str(MainTxt or "") + "\n\nВы уходите от патруля, но теперь вас будут искать внимательнее: дурная слава +4."
        $ CurLocDesc = MainTxt
        $ renpy.notify("Дурная слава +4")
    elif _patrol_outcome == "defeat":
        jump TownStreetPatrolStocks
    if _patrol_outcome in ("victory", "retreat"):
        $ current_action_title = "Итог драки с патрулем"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться", Function(renpy.return_statement, True))]
        call screen main_ui
    return True


label TownStreetPatrolStocks:
    $ TownCurfewCaughtToday = 1
    $ TownStreetPatrolsToday = int(TownStreetPatrolsToday or 0) + 1
    $ tavernfame = int(tavernfame * 0.4)
    $ notoriety = 0
    $ MainTxt = "Патруль тащит вас к колодкам. Ночь проходит унизительно: холод, смех поздних прохожих и тупая боль в плечах. К утру о вашем приключении уже знают слишком многие."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Колодки"
    $ current_action_items = [MenuItem("Дождаться утра", Call("NextDay", "StreetTavern", 1))]
    return


label DebugTownRandomEvents:
    $ CurLoc = "StreetTavern"
    $ location = CurLoc
    $ CurrentRoom = StreetTavernRoom
    $ _debug_town_plan = town_street.ensure_daily_plan()
    $ MainTxt = "День: %s\nСлот времени: %s\nСобытий сегодня: %s/2\nПлан: %s\nСработали локации: %s\nСработали события: %s\nКлючи: %s\nКулдауны: %s" % (dayspassed, time, TownStreetEventsToday, town_street._screen_text(_debug_town_plan), town_street._screen_text(TownStreetFiredLocationsToday), town_street._screen_text(TownStreetFiredLabelsToday), town_street._screen_text(TownStreetStorySeenKeys), town_street._screen_text(TownStreetCooldowns))
    $ CurLocDesc = MainTxt
    $ current_action_title = "Отладка городских случайных событий"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Обновить экран", Jump("DebugTownRandomEvents")),
        MenuItem("Сбросить события дня", Call("DebugTownRandomEventsResetToday")),
        MenuItem("Форсировать городскую хронику", Call("TownRandomChronicleEvent")),
        MenuItem("Форсировать просьбу на улице", Call("TownStreetHelpEvent")),
        MenuItem("Форсировать громил", Call("TownStreetThugsEvent")),
        MenuItem("Форсировать патруль", Call("TownStreetPatrolEvent")),
        MenuItem("Выйти на улицу трактира", Jump("StreetTavern")),
    ]
    call screen main_ui
    jump DebugTownRandomEvents


label DebugTownRandomEventsResetToday:
    $ TownStreetEventsToday = 0
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ TownStreetDailyPlan = {}
    $ TownStreetLastEventText = ""
    $ TownStreetContext = {}
    $ TownStreetFiredLabelsToday = []
    $ TownStreetFiredLocationsToday = []
    $ TownStreetCooldowns = {}
    return
