init -20 python:

    class TownStreetRuntime(object):
        LOCATIONS = ("StreetTavern", "MarketPlace", "PortStreets", "ArtisansQuarter")

        def __init__(self):
            self.events_today = 0
            self.patrols_today = 0
            self.fights_today = 0
            self.curfew_caught_today = False
            self.story_seen_keys = []
            self.cooldowns = {}
            self.blackworkers = []
            self.blackworker_candidates = []

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
            key = self._gender_key(gender)
            return RandomNameCode(
                gender=key,
                nationality=procedural_choice(["German", "French", "Italian"], key="procedural:Town/RandomTownEvents.rpy:procedural_choice:174:1"),
            )

        def _gender_key(self, gender=None):
            key = str(gender or "").strip().lower()
            if key in ("male", "female"):
                return key
            return procedural_choice(["male", "female"], key="procedural:Town/RandomTownEvents.rpy:procedural_choice:185:3")

        def _call_occupation(self, gender=None):
            key = self._gender_key(gender)
            return procedural_choice(self.OCCUPATIONS.get(key, self.OCCUPATIONS["male"]), key="procedural:Town/RandomTownEvents.rpy:procedural_choice:189:4")

        def _call_stallion(self):
            return RandomStallionNameCode()

        def location_allowed(self, location_name=""):
            return str(location_name or rooms.current_code or "") in self.LOCATIONS

        def event_key(self, location_name="", label_name=""):
            return "%s:%s:%s" % (
                self._int(calendar_v2.daysInGame, 0),
                str(location_name or rooms.current_code or ""),
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
                str(location_name or rooms.current_code or ""),
                self._int(calendar_v2.daysInGame, 0),
                self._int(calendar_v2.clock_minutes(), 0),
                self._int(player.stats.notoriety, 0),
            )
            return procedural_randint(1, 100, key) <= chance_value

        def beggar_chance(self):
            return 10

        def thug_chance(self):
            return 10

        def patrol_chance(self):
            return min(100, 25 + max(0, self._int(player.stats.notoriety, 0) // 2))

        def chronicle_chance(self):
            return 25

        def curfew_active(self):
            minute_value = self._int(calendar_v2.clock_minutes(), 0) % 1440
            return minute_value >= 21 * 60 + 30 or minute_value <= 5 * 60 + 30

        def random_seen_this_slot(self, location_name="", label_name=""):
            location_key = str(location_name or rooms.current_code or "")
            label_key = str(label_name or "day")
            return (
                self.event_key(location_key, "day") in self.story_seen_keys
                or self.event_key(location_key, label_key) in self.story_seen_keys
            )

        def mark_seen(self, location_name="", label_name=""):
            keys = self.story_seen_keys
            location_key = str(location_name or rooms.current_code or "")
            label_key = str(label_name or "day")
            for key in (self.event_key(location_key, "day"), self.event_key(location_key, label_key)):
                if key not in keys:
                    keys.append(key)

            cooldowns = self.cooldowns
            if label_key and label_key != "day":
                cooldowns[label_key] = max(
                    self._int(cooldowns.get(label_key, -1), -1),
                    self._int(calendar_v2.daysInGame, 0),
                )

        def event_on_cooldown(self, label_name="", cooldown_days=1):
            label_key = str(label_name or "")
            cooldowns = self.cooldowns
            if not label_key:
                return False
            last_day = self._int(cooldowns.get(label_key, -9999), -9999)
            return day_delta_since(last_day) < self._int(cooldown_days, 1)

        def probability_summary(self):
            return {
                "beggar": self.beggar_chance(),
                "thugs": self.thug_chance(),
                "patrol": self.patrol_chance(),
                "patrol_base": 25,
                "patrol_notoriety_bonus": max(0, self._int(player.stats.notoriety, 0) // 2),
                "chronicle": self.chronicle_chance(),
                "chronicle_cooldown_days": 3,
            }

        def reset_day(self):
            self.events_today = 0
            self.patrols_today = 0
            self.fights_today = 0
            self.curfew_caught_today = False
            self.story_seen_keys = []

        def time_event_key(self):
            if self._int(calendar_v2.week, 1) in (6, 7):
                return "weekends"
            slot = self._int(calendar_v2.time_slot(), 0)
            if slot == 0:
                return "morning"
            if slot in (1, 2):
                return "noon"
            if slot == 3:
                return "evening"
            return "night"

        def street_display(self):
            rus = RandomStreetNameCode()
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
            location_key = str(location_name or rooms.current_code or "")
            return (
                self.location_allowed(location_key)
                and self.event_key(location_key, "day") not in self.story_seen_keys
                and self.events_today < 2
            )

        def patrol_pass_active(self):
            return bool(Zimmer.street_patrol_pass)

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
            if self.fights_today > 0:
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
            exploration_value = self._int(player.stats.exploration, 0)
            score = exploration_value + procedural_randint(1, 100, key="procedural:Town/RandomTownEvents.rpy:procedural_randint:417:1")
            if exploration_value >= 150:
                score += 35
            return score >= self._int(challenge, 100)

        def fight_success(self, enemy_level=2):
            you = fight_player_level()
            score = you * 20 + (self._int(player.stats.exploration, 0) // 10) + procedural_randint(1, 60, key="procedural:Town/RandomTownEvents.rpy:procedural_randint:428:2")
            return score >= (self._int(enemy_level, 2) * 30 + 30)

        def apply_cloth_damage(self, amount=15):
            player.appearance.damage_dress(condition_loss=self._int(amount, 15))

        def apply_health_damage(self, amount=15):
            amount_int = self._int(amount, 15)
            player.change_stat("health", -amount_int)
            player.change_stat("energy", -max(5, amount_int // 2))

        def make_help_context(self):
            gender = self._gender_key()
            return {
                "help_gender": gender,
                "help_name": self._call_name(gender),
                "help_job": self._call_occupation(gender),
            }

        def settle_blackworker_candidates(self):
            candidates = self.blackworker_candidates
            workers = self.blackworkers
            joined = 0
            while len(candidates) > 0:
                worker = candidates.pop(0)
                worker["active_day"] = self._int(calendar_v2.daysInGame, 0) + 1
                worker["trust"] = max(0, self._int(worker.get("trust", 0), 0))
                workers.append(worker)
                joined += 1
            return joined

default TownStreet = TownStreetRuntime()


label TownRandomChronicleEvent:
    $ main_ui_begin_native_scene_state("Случайное событие")
    $ TownStreet.events_today += 1
    $ TownStreet.mark_seen(rooms.current_code, "TownRandomChronicleEvent")
    $ scene_runtime.text = TownStreet.random_chronicle(TownStreet.time_event_key())
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Идти дальше":
            pass
    $ main_ui_end_native_scene_state()
    return True


label TownStreetHelpEvent:
    $ renpy.dynamic("_town_ctx")
    $ TownStreet.events_today += 1
    $ TownStreet.mark_seen(rooms.current_code, "TownStreetHelpEvent")
    $ _town_ctx = TownStreet.make_help_context()
    $ scene_runtime.text = "У стены сидит измученный человек. По виду это %s - %s. Он просит не денег, а куска еды и места, где можно переждать ночь. Рядом двое прохожих делают вид, что не слышат." % (_town_ctx.get("help_name", "бродяга"), _town_ctx.get("help_job", "без ремесла"))
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    "[scene_runtime.text]"
    menu:
        "Дать еды и предложить грязную работу при трактире":
            call TownStreetHelpRecruit(_town_ctx.get("help_name", "бродяга"))
            "[scene_runtime.text]"
        "Дать пару мараведи":
            call TownStreetHelpMoney
            "[scene_runtime.text]"
        "Пройти мимо":
            pass
    return True


label TownStreetHelpRecruit(help_name="бродяга"):
    $ renpy.dynamic("_candidate_id")
    $ _candidate_id = "bw_%03d" % (len(TownStreet.blackworker_candidates) + len(TownStreet.blackworkers) + 1)
    $ TownStreet.blackworker_candidates.append({"id": _candidate_id, "name": str(help_name or "бродяга"), "origin": "street_help", "day": int(calendar_v2.daysInGame or 0), "sleep_place": "TavernStable", "trust": 0})
    $ player.change_stat("exploration", 5)
    $ player.economy.tavern_fame += 1
    $ scene_runtime.text = "Вы обещаете еду, угол в конюшне и простую грязную работу. Человек хватается за это предложение так, будто вы протянули ему не хлеб, а целую жизнь. Если он не сбежит от страха, утром у трактира появится новый чернорабочий."
    $ scene_runtime.location_text = scene_runtime.text
    return


label TownStreetHelpMoney:
    if player.economy.money >= 2:
        $ player.spend_money(2)
        $ player.change_stat("exploration", 3)
        $ player.change_stat("notoriety", -10)
        $ scene_runtime.text = "Вы даете пару мараведи. Благодарность выходит тихой и неловкой, но несколько прохожих это замечают."
    else:
        $ scene_runtime.text = "Вы хлопаете по пустому кошелю и понимаете, что сейчас вам самому впору просить милостыню."
    $ scene_runtime.location_text = scene_runtime.text
    return


label TownStreetThugsEvent:
    $ TownStreet.events_today += 1
    $ TownStreet.fights_today += 1
    $ TownStreet.mark_seen(rooms.current_code, "TownStreetThugsEvent")
    $ scene_runtime.text = "Из бокового переулка вы слышите короткий вскрик. Двое крепких парней прижимают к стене растерянного горожанина и выворачивают ему руки. Увидев вас, один ухмыляется: «Проходи мимо, трактирщик. Не твое дело»."
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    "[scene_runtime.text]"
    menu:
        "Вмешаться и драться":
            call TownStreetThugsFight
        "Попробовать спугнуть их криком":
            call TownStreetThugsShout
        "Пройти мимо":
            pass
    return True


label TownStreetThugsFight:
    $ renpy.dynamic("_thug_reputation_before", "_thug_tavernfame_before", "_thug_notoriety_before", "_thug_return_room", "_thug_picture", "_thug_intro", "_thug_outcome")
    $ _thug_reputation_before = int(player.stats.reputation or 0)
    $ _thug_tavernfame_before = int(player.economy.tavern_fame or 0)
    $ _thug_notoriety_before = int(player.stats.notoriety or 0)
    $ player.set_stat("notoriety", _thug_notoriety_before + 3)
    $ _thug_return_room = str(rooms.current_code or "StreetTavern")
    $ _thug_picture = str(scene_runtime.picture or "")
    $ _thug_intro = "Вы встаете между жертвой и громилами. Один сплевывает на мостовую и перехватывает дубинку: теперь разговор закончится только дракой."
    $ fight_begin("street_crook", 2, _thug_return_room, _thug_picture, _thug_intro)
    call FightLoop
    $ _thug_outcome = str(fight.last_result.get("outcome", "") or "")
    if _thug_outcome == "victory":
        $ player.set_stat("reputation", _thug_reputation_before + 3)
        $ player.economy.tavern_fame = _thug_tavernfame_before + 1
        $ player.set_stat("notoriety", _thug_notoriety_before + 3)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВы отбили прохожего у громил. На улице это быстро запоминают: репутация +3, слава трактира +1."
        $ scene_runtime.location_text = scene_runtime.text
        $ renpy.notify("Репутация +3, слава трактира +1")
    elif _thug_outcome == "defeat":
        $ player.change_stat("notoriety", -2)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nГромилы уходят, убедившись, что вы больше не мешаете. Прохожие делают вид, что ничего не видели."
        $ scene_runtime.location_text = scene_runtime.text
    elif _thug_outcome == "retreat":
        $ player.change_stat("reputation", -1)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВы уходите из драки живым, но жертва остается на улице без вашей помощи: репутация -1."
        $ scene_runtime.location_text = scene_runtime.text
        $ renpy.notify("Репутация -1")
    if _thug_outcome in ("victory", "defeat", "retreat"):
        "[scene_runtime.text]"
        menu:
            "Вернуться":
                pass
    return True


label TownStreetThugsShout:
    $ renpy.dynamic("_shout_score", "_shout_reputation_before", "_shout_notoriety_before", "_thug_return_room", "_thug_picture", "_thug_intro", "_thug_outcome")
    $ _shout_reputation_before = int(player.stats.reputation or 0)
    $ _shout_notoriety_before = int(player.stats.notoriety or 0)
    $ _thug_return_room = str(rooms.current_code or "StreetTavern")
    $ _thug_picture = str(scene_runtime.picture or "")
    $ _shout_score = int(player.stats.exploration or 0) + procedural_randint(1, 100, "town_thugs_shout_%s_%s_%s" % (int(calendar_v2.daysInGame or 0), _thug_return_room, int(calendar_v2.clock_minutes() or 0)))
    if int(player.stats.exploration or 0) >= 150:
        $ _shout_score += 35
    if _shout_score >= 85:
        $ player.change_stat("exploration", 6)
        $ player.change_stat("reputation", 2)
        $ player.change_stat("notoriety", 4)
        $ scene_runtime.text = "Вы громко зовете стражу и называете ближайшие дома так уверенно, будто уже знаете, куда побежите за подкреплением. Громилы переглядываются, ругаются и отступают в переулок. Прохожие запоминают, что вы не прошли мимо: репутация +2, дурная слава +4."
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        menu:
            "Вернуться":
                pass
        return True
    else:
        $ player.set_stat("notoriety", _shout_notoriety_before + 2)
        $ _thug_intro = "Ваш крик только злит громил. Один толкает жертву в грязь, второй разворачивается к вам с дубинкой: теперь они хотят наказать именно вас."
        $ fight_begin("street_crook", 2, _thug_return_room, _thug_picture, _thug_intro)
        call FightLoop
        $ _thug_outcome = str(fight.last_result.get("outcome", "") or "")
        if _thug_outcome == "victory":
            $ player.set_stat("reputation", _shout_reputation_before + 2)
            $ player.set_stat("notoriety", _shout_notoriety_before + 2)
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nКрик не испугал громил, зато драка закончилась в вашу пользу. Прохожие запоминают это: репутация +2."
            $ scene_runtime.location_text = scene_runtime.text
            $ renpy.notify("Репутация +2")
        elif _thug_outcome == "retreat":
            $ player.change_stat("reputation", -1)
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВы отступаете, и громилы остаются хозяевами улицы. Это не выглядит геройством: репутация -1."
            $ scene_runtime.location_text = scene_runtime.text
            $ renpy.notify("Репутация -1")
        if _thug_outcome in ("victory", "defeat", "retreat"):
            "[scene_runtime.text]"
            menu:
                "Вернуться":
                    pass
        return True


label TownStreetPatrolEvent:
    $ renpy.dynamic("_fine")
    if not TownStreet.curfew_active():
        return False
    $ TownStreet.events_today += 1
    $ TownStreet.patrols_today += 1
    $ TownStreet.mark_seen(rooms.current_code, "TownStreetPatrolEvent")
    $ scene_runtime.picture = "images/general/cityguard.jpg"
    vscene scene_runtime.picture
    $ scene_runtime.text = "Из темноты выступает ночной патруль капитана Циммера. Старший лениво поднимает фонарь к вашему лицу: «Комендантский час, добрый человек. Документы, пропуск или деньги. А если нет - пройдем до колодок»."
    $ scene_runtime.location_text = scene_runtime.text
    $ _fine = TownStreet.fine_amount("fight")
    show screen main_ui
    "[scene_runtime.text]"
    menu:
        "Показать пропуск" if TownStreet.patrol_pass_active():
            call TownStreetPatrolPass
            "[scene_runtime.text]"
        "Заплатить штраф [_fine] мараведи":
            call TownStreetPatrolBribe
            "[scene_runtime.text]"
        "Спрятаться и уйти дворами":
            call TownStreetPatrolHide
            "[scene_runtime.text]"
        "Бежать":
            call TownStreetPatrolRun
            "[scene_runtime.text]"
        "Драться со стражей":
            call TownStreetPatrolFight
    return True


label TownStreetPatrolPass:
    if TownStreet.patrol_pass_active():
        $ player.change_stat("exploration", 2)
        $ scene_runtime.text = "Вы показываете пропуск с отметкой капитана Циммера. Старший патруля недовольно кривится, но возвращает бумагу и велит не шататься без дела."
    else:
        $ scene_runtime.text = "Никакого пропуска у вас нет. Старший патруля смотрит на пустые руки с усталой усмешкой."
    $ scene_runtime.location_text = scene_runtime.text
    return


label TownStreetPatrolBribe:
    $ renpy.dynamic("_fine")
    $ _fine = TownStreet.fine_amount("fight")
    if player.economy.money >= _fine:
        $ player.spend_money(_fine)
        $ player.change_stat("notoriety", -3)
        $ player.economy.tavern_fame = max(0, int(player.economy.tavern_fame or 0) - 1)
        $ calendar_v2.advance_minutes(10)
        $ scene_runtime.text = "Монеты быстро исчезают в руке старшего. Патруль сразу теряет к вам интерес, будто никакого комендантского часа и не было. Вы теряете десять минут, дурная слава снижается на 3, но слух о ночной плате слегка бьет по славе трактира."
    else:
        jump TownStreetPatrolStocks
    $ scene_runtime.location_text = scene_runtime.text
    return


label TownStreetPatrolHide:
    if TownStreet.escape_success(115):
        $ player.change_stat("exploration", 8)
        $ player.change_stat("notoriety", 1)
        $ calendar_v2.advance_minutes(20)
        $ scene_runtime.text = "Вы вовремя ныряете в темный проход, пережидаете шаги патруля и выбираетесь уже на другой стороне улицы. Обход занимает двадцать минут: исследование +8, дурная слава +1."
    else:
        $ scene_runtime.text = "Вы пробуете уйти дворами, но задеваете ведро. Патруль мгновенно разворачивается на шум."
        jump TownStreetPatrolStocks
    $ scene_runtime.location_text = scene_runtime.text
    return


label TownStreetPatrolRun:
    if TownStreet.escape_success(130):
        $ player.change_stat("exploration", 10)
        $ player.change_stat("notoriety", 4)
        $ player.economy.tavern_fame = max(0, int(player.economy.tavern_fame or 0) - 1)
        $ calendar_v2.advance_minutes(15)
        $ scene_runtime.text = "Вы срываетесь с места и уходите от патруля через узкие проходы. За спиной ругаются, но догнать вас уже не могут. Побег занимает пятнадцать минут: исследование +10, дурная слава +4, слава трактира -1."
    else:
        $ scene_runtime.text = "Вы бросаетесь бежать, но улица оказывается слишком открытой. Вас сбивают древком алебарды и поднимают уже под смех патрульных."
        jump TownStreetPatrolStocks
    $ scene_runtime.location_text = scene_runtime.text
    return


label TownStreetPatrolFight:
    $ renpy.dynamic("_patrol_return_room", "_patrol_picture", "_patrol_intro", "_patrol_outcome")
    $ player.change_stat("notoriety", 12)
    $ player.economy.tavern_fame -= 2
    $ calendar_v2.advance_minutes(10)
    $ _patrol_return_room = str(rooms.current_code or "StreetTavern")
    $ _patrol_picture = "images/fight/patrol_guard.png"
    $ _patrol_intro = "Вы решаете не платить и не прятаться. Стражники переглядываются, опускают алебарды и берут вас в клещи. Теперь это настоящая драка с патрулем."
    $ fight_begin("patrol_guard", 2, _patrol_return_room, _patrol_picture, _patrol_intro)
    call FightLoop
    $ _patrol_outcome = str(fight.last_result.get("outcome", "") or "")
    if _patrol_outcome == "victory":
        $ player.change_stat("notoriety", 18)
        $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) - 3
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВы отбились от патруля, но это уже не мелкая ссора с ночной стражей. Дурная слава +18, слава трактира -3."
        $ scene_runtime.location_text = scene_runtime.text
        $ renpy.notify("Дурная слава +18, слава трактира -3")
    elif _patrol_outcome == "retreat":
        $ player.change_stat("notoriety", 4)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВы уходите от патруля, но теперь вас будут искать внимательнее: дурная слава +4."
        $ scene_runtime.location_text = scene_runtime.text
        $ renpy.notify("Дурная слава +4")
    elif _patrol_outcome == "defeat":
        jump TownStreetPatrolStocks
    if _patrol_outcome in ("victory", "retreat"):
        "[scene_runtime.text]"
        menu:
            "Вернуться":
                pass
    return True


label TownStreetPatrolStocks:
    $ TownStreet.curfew_caught_today = True
    $ TownStreet.patrols_today += 1
    $ player.economy.tavern_fame = int(player.economy.tavern_fame * 0.4)
    $ player.set_stat("notoriety", 0)
    $ scene_runtime.text = "Патруль тащит вас к колодкам. Ночь проходит унизительно: холод, смех поздних прохожих и тупая боль в плечах. К утру о вашем приключении уже знают слишком многие."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Дождаться утра":
            call NextDay("StreetTavern", 1)
    return


label DebugTownRandomEvents:
    $ renpy.dynamic("_debug_town_plan")
    $ rooms.enter("StreetTavern")
    $ _debug_town_plan = TownStreet.probability_summary()
    $ scene_runtime.text = "День: %s\nСлот времени: %s\nСобытий сегодня: %s/2\nВероятности: %s\nКлючи: %s\nКулдауны: %s" % (calendar_v2.daysInGame, calendar_v2.time_slot(), TownStreet.events_today, TownStreet._screen_text(_debug_town_plan), TownStreet._screen_text(TownStreet.story_seen_keys), TownStreet._screen_text(TownStreet.cooldowns))
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Отладка городских случайных событий"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [
        MenuItem("Форсировать городскую хронику", Call("TownRandomChronicleEvent")),
        MenuItem("Форсировать просьбу на улице", Call("TownStreetHelpEvent")),
        MenuItem("Форсировать громил", Call("TownStreetThugsEvent")),
        MenuItem("Форсировать патруль", Call("TownStreetPatrolEvent")),
        MenuItem("Выйти на улицу трактира", Jump("StreetTavern")),
    ]
    while True:
        call screen main_ui
