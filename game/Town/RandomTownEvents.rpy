# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default TownStreetEventsToday = 0
default TownStreetPatrolsToday = 0
default TownStreetFightToday = 0
default TownCurfewCaughtToday = 0
default TownStreetStorySeenKeys = []
default TownStreetLastEventText = ""
default TownStreetContext = {}

default GuardCaptainVar = {}
default TavernBlackworkers = []
default TavernBlackworkerCandidates = []

init -20 python:
    import renpy.store as store

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
            try:
                return getattr(store, name, default)
            except Exception:
                return default

        def _int(self, value, default=0):
            try:
                return int(value)
            except Exception:
                try:
                    return int(float(value))
                except Exception:
                    return default

        def _call_name(self, gender=None):
            fn = self._get("RandomNameCode", None)
            key = self._gender_key(gender)
            if callable(fn):
                return fn(gender=key, nationality=renpy.random.choice(["German", "French", "Italian"]))
            fallback = {
                "male": ("Ганс", "Пьер", "Томас", "Сергио"),
                "female": ("Мария", "Лючия", "Анна", "Франческа"),
            }
            return renpy.random.choice(fallback.get(key, fallback["male"]))

        def _gender_key(self, gender=None):
            key = str(gender or "").strip().lower()
            if key in ("male", "female"):
                return key
            return renpy.random.choice(["male", "female"])

        def _call_occupation(self, gender=None):
            key = self._gender_key(gender)
            return renpy.random.choice(self.OCCUPATIONS.get(key, self.OCCUPATIONS["male"]))

        def _call_stallion(self):
            fn = self._get("RandomStallionNameCode", None)
            if callable(fn):
                return fn()
            return renpy.random.choice(["Черный", "Буян", "Гром"])

        def location_allowed(self, location_name=""):
            return str(location_name or self._get("CurLoc", "") or "") in self.LOCATIONS

        def event_key(self, location_name=""):
            return "%s:%s:%s" % (
                self._int(self._get("dayspassed", 0), 0),
                str(location_name or self._get("CurLoc", "") or ""),
                self._int(self._get("time", 0), 0),
            )

        def random_seen_this_slot(self, location_name=""):
            keys = self._get("TownStreetStorySeenKeys", [])
            return self.event_key(location_name) in list(keys or [])

        def mark_seen(self, location_name=""):
            keys = self._get("TownStreetStorySeenKeys", [])
            key = self.event_key(location_name)
            if key not in keys:
                keys.append(key)

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
            entry = renpy.random.choice(self.TIME_EVENTS[key])
            text = str(entry.get("text", "") if isinstance(entry, dict) else entry)
            gender = self._gender_key(entry.get("gender", None) if isinstance(entry, dict) else None)
            if renpy.random.random() < float(entry.get("guard_chance", 0.45) if isinstance(entry, dict) else 0.45):
                text += renpy.random.choice(self.PASSIVE_GUARDS)
            return (
                text
                .replace("[улица]", self.street_display())
                .replace("[имя]", self._call_name(gender))
                .replace("[занятие]", self._call_occupation(gender))
                .replace("[stallion]", self._call_stallion())
            )

        def interactive_allowed(self, location_name=""):
            return (
                self.location_allowed(location_name)
                and self._int(self._get("TownStreetEventsToday", 0), 0) < 2
                and not self.random_seen_this_slot(location_name)
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
            if self._int(self._get("time", 0), 0) < 3:
                return False
            if self.patrol_pass_active():
                return False
            base = 12 if self._int(self._get("time", 0), 0) == 3 else 30
            heat = min(45, max(0, self._int(self._get("notoriety", 0), 0) // 2))
            loc_bonus = 8 if str(location_name or self._get("CurLoc", "") or "") in ("PortStreets", "ArtisansQuarter") else 0
            chance = max(5, min(80, base + heat + loc_bonus))
            seed = (
                self._int(self._get("dayspassed", 0), 0) * 37
                + self._int(self._get("time", 0), 0) * 17
                + len(str(location_name or self._get("CurLoc", "") or "")) * 11
                + self._int(self._get("notoriety", 0), 0)
            )
            return ((seed % 100) + 1) <= chance

        def thug_allowed(self, location_name=""):
            if not self.interactive_allowed(location_name):
                return False
            if self._int(self._get("TownStreetFightToday", 0), 0) > 0:
                return False
            if self._int(self._get("time", 0), 0) < 2:
                return False
            seed = self._int(self._get("dayspassed", 0), 0) * 19 + self._int(self._get("time", 0), 0) * 23 + len(str(location_name or self._get("CurLoc", "") or ""))
            return ((seed % 100) + 1) <= (20 if self._int(self._get("time", 0), 0) < 4 else 35)

        def help_allowed(self, location_name=""):
            if not self.interactive_allowed(location_name):
                return False
            if self._int(self._get("time", 0), 0) == 4:
                return False
            seed = self._int(self._get("dayspassed", 0), 0) * 13 + self._int(self._get("time", 0), 0) * 7 + len(str(location_name or self._get("CurLoc", "") or ""))
            return ((seed % 100) + 1) <= 12

        def fine_amount(self, reason="fight"):
            if str(reason or "") == "counter_bribe":
                return 200
            return 50

        def escape_success(self, challenge=100):
            exploration_value = self._int(self._get("exploration", 0), 0)
            score = exploration_value + renpy.random.randint(1, 100)
            if exploration_value >= 150:
                score += 35
            return score >= self._int(challenge, 100)

        def fight_success(self, enemy_level=2):
            fight_level = self._get("FightLevel", {})
            try:
                you = self._int(fight_level.get("you", 1), 1)
            except Exception:
                you = 1
            score = you * 20 + (self._int(self._get("exploration", 0), 0) // 10) + renpy.random.randint(1, 60)
            return score >= (self._int(enemy_level, 2) * 30 + 30)

        def apply_cloth_damage(self, amount=15):
            store.costumecondition = max(0, self._int(self._get("costumecondition", 100), 100) - self._int(amount, 15))

        def apply_health_damage(self, amount=15):
            amount_int = self._int(amount, 15)
            store.health = max(0, self._int(self._get("health", 100), 100) - amount_int)
            store.energy = max(0, self._int(self._get("energy", 100), 100) - max(5, amount_int // 2))

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
    $ town_street.mark_seen(CurLoc)
    $ TownStreetLastEventText = town_street.random_chronicle(town_street.time_event_key())
    $ MainTxt = TownStreetLastEventText
    $ CurLocDesc = MainTxt
    $ current_action_title = "Городские слухи"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    call screen main_ui
    jump expression CurLoc


label TownStreetHelpEvent:
    $ SignalBlockTime = 1
    $ TownStreetEventsToday = int(TownStreetEventsToday or 0) + 1
    $ town_street.mark_seen(CurLoc)
    $ _town_ctx = town_street.make_help_context()
    $ MainTxt = "У стены сидит измученный человек. По виду это %s - %s. Он просит не денег, а куска еды и места, где можно переждать ночь. Рядом двое прохожих делают вид, что не слышат." % (_town_ctx.get("help_name", "бродяга"), _town_ctx.get("help_job", "без ремесла"))
    $ CurLocDesc = MainTxt
    $ current_action_title = "Уличная просьба"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Дать еды и предложить грязную работу при трактире", Call("TownStreetHelpRecruit")),
        MenuItem("Дать пару мараведи", Call("TownStreetHelpMoney")),
        MenuItem("Пройти мимо", Jump(CurLoc)),
    ]
    call screen main_ui
    jump expression CurLoc


label TownStreetHelpRecruit:
    $ _candidate_id = "bw_%03d" % (len(TavernBlackworkerCandidates) + len(TavernBlackworkers) + 1)
    $ TavernBlackworkerCandidates.append({"id": _candidate_id, "name": TownStreetContext.get("help_name", "бродяга"), "origin": "street_help", "day": int(dayspassed or 0), "sleep_place": "TavernStable", "trust": 0})
    $ exploration += 5
    $ tavernfame += 1
    $ MainTxt = "Вы обещаете еду, угол в конюшне и простую грязную работу. Человек хватается за это предложение так, будто вы протянули ему не хлеб, а целую жизнь. Если он не сбежит от страха, утром у трактира появится новый чернорабочий."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    return


label TownStreetHelpMoney:
    if money >= 2:
        $ money -= 2
        $ exploration += 3
        $ MainTxt = "Вы даете пару мараведи. Благодарность выходит тихой и неловкой, но несколько прохожих это замечают."
    else:
        $ MainTxt = "Вы хлопаете по пустому кошелю и понимаете, что сейчас вам самому впору просить милостыню."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    return


label TownStreetThugsEvent:
    $ SignalBlockTime = 1
    $ TownStreetEventsToday = int(TownStreetEventsToday or 0) + 1
    $ TownStreetFightToday = int(TownStreetFightToday or 0) + 1
    $ town_street.mark_seen(CurLoc)
    $ MainTxt = "Из бокового переулка вы слышите короткий вскрик. Двое крепких парней прижимают к стене растерянного горожанина и выворачивают ему руки. Увидев вас, один ухмыляется: «Проходи мимо, трактирщик. Не твое дело»."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Уличные громилы"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вмешаться и драться", Call("TownStreetThugsFight")),
        MenuItem("Попробовать спугнуть их криком", Call("TownStreetThugsShout")),
        MenuItem("Пройти мимо", Jump(CurLoc)),
    ]
    call screen main_ui
    jump expression CurLoc


label TownStreetThugsFight:
    if town_street.fight_success(2):
        $ exploration += renpy.random.randint(8, 15)
        $ tavernfame += 2
        $ notoriety += 3
        $ money += renpy.random.randint(3, 10)
        $ MainTxt = "Драка выходит короткой и грязной. Один получает локтем в зубы, второй спотыкается о бочку и решает, что добыча не стоит сломанных ребер. Спасенный горожанин сует вам несколько монет и сбивчиво благодарит."
    else:
        $ town_street.apply_health_damage(25)
        $ town_street.apply_cloth_damage(30)
        $ SickDays += 1 if renpy.random.randint(1, 3) == 1 else 0
        $ notoriety += 2
        $ MainTxt = "Вы лезете в драку, но громилы оказываются слаженнее. Вас валят на мостовую, пару раз бьют ногами и исчезают в переулке. Одежда порвана, тело ноет, а свидетели делают вид, что смотрели в другую сторону."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Подняться и идти дальше", Jump(CurLoc))]
    return


label TownStreetThugsShout:
    if town_street.escape_success(85):
        $ exploration += 6
        $ MainTxt = "Вы громко зовете стражу и называете ближайшие дома так уверенно, будто уже знаете, куда побежите за подкреплением. Громилы ругаются и исчезают."
    else:
        $ town_street.apply_health_damage(12)
        $ MainTxt = "Ваш крик только злит громил. Один толкает вас плечом в стену, второй шипит, что в следующий раз разговор будет длиннее. Потом они все же уходят."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    return


label TownStreetPatrolEvent:
    $ SignalBlockTime = 1
    $ TownStreetEventsToday = int(TownStreetEventsToday or 0) + 1
    $ TownStreetPatrolsToday = int(TownStreetPatrolsToday or 0) + 1
    $ town_street.mark_seen(CurLoc)
    $ MainTxt = "Из темноты выступает ночной патруль капитана Циммера. Старший лениво поднимает фонарь к вашему лицу: «Комендантский час, добрый человек. Документы, пропуск или деньги. А если нет - пройдем до колодок»."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ночной патруль"
    $ current_action_content = None
    $ _fine = town_street.fine_amount("fight")
    $ current_action_items = [
        MenuItem("Показать пропуск", Call("TownStreetPatrolPass")),
        MenuItem("Заплатить штраф %d мараведи" % _fine, Call("TownStreetPatrolBribe")),
        MenuItem("Спрятаться и уйти дворами", Call("TownStreetPatrolHide")),
        MenuItem("Бежать", Call("TownStreetPatrolRun")),
        MenuItem("Драться со стражей", Call("TownStreetPatrolFight")),
    ]
    call screen main_ui
    jump expression CurLoc


label TownStreetPatrolPass:
    if town_street.patrol_pass_active():
        $ exploration += 2
        $ MainTxt = "Вы показываете пропуск с отметкой капитана Циммера. Старший патруля недовольно кривится, но возвращает бумагу и велит не шататься без дела."
    else:
        $ MainTxt = "Никакого пропуска у вас нет. Старший патруля смотрит на пустые руки с усталой усмешкой."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    return


label TownStreetPatrolBribe:
    $ _fine = town_street.fine_amount("fight")
    if money >= _fine:
        $ money -= _fine
        $ notoriety = max(0, int(notoriety or 0) - 3)
        $ MainTxt = "Монеты быстро исчезают в руке старшего. Патруль сразу теряет к вам интерес, будто никакого комендантского часа и не было."
    else:
        jump TownStreetPatrolStocks
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    return


label TownStreetPatrolHide:
    if town_street.escape_success(115):
        $ exploration += 8
        $ MainTxt = "Вы вовремя ныряете в темный проход, пережидаете шаги патруля и выбираетесь уже на другой стороне улицы."
    else:
        $ MainTxt = "Вы пробуете уйти дворами, но задеваете ведро. Патруль мгновенно разворачивается на шум."
        jump TownStreetPatrolStocks
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    return


label TownStreetPatrolRun:
    if town_street.escape_success(130):
        $ exploration += 10
        $ MainTxt = "Вы срываетесь с места и уходите от патруля через узкие проходы. За спиной ругаются, но догнать вас уже не могут."
    else:
        $ MainTxt = "Вы бросаетесь бежать, но улица оказывается слишком открытой. Вас сбивают древком алебарды и поднимают уже под смех патрульных."
        jump TownStreetPatrolStocks
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Идти дальше", Jump(CurLoc))]
    return


label TownStreetPatrolFight:
    if town_street.fight_success(4):
        $ exploration += 15
        $ notoriety += 12
        $ tavernfame -= 2
        $ MainTxt = "Вы бьете первым и на несколько секунд ошеломляете патруль. Этого хватает, чтобы уйти. Но теперь вас точно запомнили."
    else:
        $ town_street.apply_health_damage(35)
        $ town_street.apply_cloth_damage(45)
        $ notoriety += 8
        $ MainTxt = "Драться со стражей оказалось плохой мыслью. Вас валят древками, связывают и волокут к колодкам."
        jump TownStreetPatrolStocks
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Скрыться", Jump(CurLoc))]
    return


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
