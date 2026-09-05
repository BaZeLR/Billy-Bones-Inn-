# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitLiza:
    python:
        Liza.initialize_new_game_state()
        people.register(LizaStaticData, Liza)

    return

init python:
    class LizaData(PeopleData):
        code_name = "liza"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Лизетта",
                fullname="Лизетта",
                genitive="Лизетты",
                dative="Лизетте",
                default_location="",
                description="Лизетта Брюно - худенькая молоденькая мулатка, ростом чуть меньше 145 сантиметров. У нее шоколадная кожа, зеленые глаза и маленькие грудки. Ее длинные темные волосы собранны в две косички. У нее стройные длинные ножки и немного оттопыреная попка, привлекающая мужские взгляды.",
                gift_preferences=["berries_001", "wild_rose_001", "soap_001"],
            )
            self.birth_date = {"day": 1, "period": 1, "cycle": 1082}
            self.schedule_source = "schedules/liza.json"

    class LizaInfo(Girl):
        """Lizette runtime: port work, tavern relocation, church story, pregnancy state."""

        talk_label = "IntLizaTalk"
        ORGASM_FRIENDSHIP_GAIN = 1
        LICK_FRIENDSHIP_MILESTONES = {7: 1}
        OPENNESS_RELATIONSHIP_STEPS = ((4, 3), (7, 5), (6, 6), (8, 7))

        uses_tavern_client_room = True
        unknown_name = "Молодая женщина"
        work_socializing_locations = ("TavernMain", "PortStreets")

        def __init__(self):
            super().__init__("liza")
            self.code_name = "liza"
            self.data = LizaStaticData
            self.rel = 0
            self.openness = 0
            self.corruption = 35
            self.known = False
            self.witnessed_church_after_sermon = False
            self.discussed_georgett_gerhard = False
            self.prostitution_started = False
            self.has_seen_clients = False
            self.asked_about_clients = False
            self.asked_about_pregnancy = False
            self.asked_about_sex = False
            self.glory_hole_mentioned = False
            self.glory_hole_asked = False
            self.portstreet_clients_seen_today = False
            self.talked_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.stats = {
                "kids": 0,
                "beauty": 72,
                "sexacts": 89,
                "cuminside": 7,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 10,
                "PussyWetStart": 20,
                "virginity": False,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 20,
                "cleaning": 20,
                "waitress": 25,
            }
            self.jobs = {
                "jobkitchen": 0,
                "jobcleaning": 0,
                "jobwaitress": 0,
                "jobHallAvail": 0,
                "jobWhoreAvail": 0,
                "jobGloryHoleAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
                "jobwhoreTommorow": 0,
                "jobgloryholeTommorow": 0,
            }
            self.talk_preferences = {
                "favorite_topics": ["clients", "sex", "pregnancy", "family", "work"],
                "blocked_topics": ["flirt"],
            }
            self.wardrobe = {
                "owned": ["minidress", "simplepanties", "blackstockings", "highshoes"],
                "gifted": [],
                "current_dress": "minidress",
                "current_underwear": {
                    "bra": "",
                    "panties": "simplepanties",
                    "legs": "blackstockings",
                    "shoes": "highshoes",
                },
            }
        def update(self):
            super(LizaInfo, self).update()
            self.data = LizaStaticData
            self.ensure_sex_state()
            return self

        def ensure_sex_state(self):
            state = super(LizaInfo, self).ensure_sex_state()
            for key, value in {
                "location": "street",
                "lick_pussy": 0,
                "top_removed": 0,
                "bottom_removed": 0,
                "bra_removed": 0,
                "panties_removed": 0,
                "top_raised": 0,
                "bottom_raised": 0,
            }.items():
                state.setdefault(key, value)
            return state

        def sex_setup(self, location="street"):
            self.ensure_sex_state()
            self.sex_state["location"] = str(location or "street")
            self.sex_state["somebody_cums"] = 0
            self.reset_sex_clothing_state()
            self.set_cock_position("none")
            return self.sex_state

        def remove_top_for_sex(self):
            self.remove_clothing_layer("top")
            self.set_cock_position("none")
            return self.sex_state

        def raise_top_for_sex(self):
            self.set_layer_raised("top", 1)
            self.set_cock_position("none")
            return self.sex_state

        def raise_bottom_for_sex(self):
            self.set_layer_raised("bottom", 1)
            self.set_cock_position("none")
            return self.sex_state

        def remove_panties_for_sex(self):
            self.remove_clothing_layer("panties")
            self.set_cock_position("none")
            return self.sex_state

        def clear_visible_cum(self, *keys):
            self.clear_cum(*keys)
            self.set_cock_position("none")
            return self.sex_state

        def initialize_new_game_state(self):
            self.ensure_sex_state()
            return self

        def reset_daily(self, full=False):
            super(LizaInfo, self).reset_daily(full)
            self.portstreet_clients_seen_today = False
            return self

        def reset_tavern_work_day(self):
            self.jobs["jobwhore"] = 0
            self.jobs["jobgloryhole"] = 0
            return self.jobs

        def dress_change_other_saw_text(self, agreed_to_redress=0):
            if agreed_to_redress != 1 or int(self.corruption or 0) < 50:
                return ""
            rand_var = procedural_randint(1, 9, key="procedural:NPC/Girls/Liza/IntLizaDressChange.rpy:procedural_randint:10:1")
            if rand_var == 1:
                if int(Sandra.corruption or 0) >= 35:
                    text = "Обернувшись, вы вдруг встретились взглядом с Сандрой, наблюдающей за этой сценкой. Но она всего лишь усмехнулась, покачала головой и пошла по своим делам."
                else:
                    text = 'Обернувшись, вы вдруг встретились взглядом с Сандрой, наблюдающей за этой сценкой. И увиденное ей явно не понравилось. Она подошла и сердито сказала: "Стефан, я понимаю что без этих шлюх мы можем концы с концами не свести, но хоть крупицу стыда иметь надо?"\nВы еле смогли успокоить Сандру и заболтать тему.'
            elif rand_var == 2:
                if int(Melissa.corruption or 0) >= 35:
                    text = "Вы заметили, что за вами наблюдала Мелисса. Но увиденное ее совсем не шокировало, скорее позабавило."
                else:
                    text = 'Вы заметили, что за вами наблюдала Мелисса. И этот стриптиз ее немного шокировал. Она подошла и выговорила вам: "Знаешь что, Стефан, держи своих шлюх так, чтобы по крайней мере девочкам не приходилось пялиться на их прелести. У тебя ведь и младшая есть, она еще мала на такое смотреть!"'
            elif rand_var == 3:
                if int(Amanda.corruption or 0) >= 35:
                    text = "Вы заметили, что за вами наблюдала Аманда. Стриптиз подруги ее позабавил, она даже от возбуждения слегка потерла у себя между ножек."
                else:
                    text = 'Вы заметили, что за вами наблюдала Аманда. Причем наблюдала с открытым ртом, публичное раздевание для нее явно было в новинку и шокировало. "Пусть учится смотреть на вещи шире," подумали вы.'
                    Amanda.apply_social_chance(0, 0, 0, 21, 1, 1, "liza_dress_change_seen")
            elif rand_var == 4:
                text = "Вы заметили, что за снимающей на людях панталоны дочкой с улыбкой наблюдала Жоржетта, одобрительно кивая."
            elif rand_var == 5:
                text = "Из-за ближайшего стола послышался одобрительный свист, посетителям стриптиз Лизетты пришелся по душе."
            elif rand_var == 6:
                text = "Один из увидевших это непотребство посетителей не выдержал, подскочил к Лизетте и крепко ее поцеловал, а рукой залез под ее подол, лаская пальцами киску. Его друзья встретили такой поступок одобрительным улюлюканием."
            elif rand_var == 7:
                text = 'Один из посетителей наблюдал за этой сценкой с отвалившей челюстью. Лизетта весело подмигнула ему и сказала: "Десять мараведи, красавчик!" смутив скромнягу еще больше.'
            else:
                text = ""
            if rand_var <= 2:
                self.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_seen")
            if 5 <= rand_var <= 7:
                self.apply_social_chance(0, 0, 0, 60, 1, 1, "dress_change_seen")
                player.economy.tavern_fame += 1
            return text

        def can_ask_topic(self, topic):
            key = str(topic or "")
            if not self.can_talk_today():
                return False
            rel_value = people_to_int(self.rel, 0)
            if key == "clients":
                return self.has_seen_clients and rel_value >= 5
            if key in ("sex", "pregnancy"):
                return self.asked_about_clients and rel_value >= 5
            if key == "georgett_gerhard":
                return (
                    people_to_int(Georgett.story_value("SawChurchAfterCermon", 0), 0) > 0
                    and rel_value >= 5
                    and not self.discussed_georgett_gerhard
                )
            if key == "work":
                return self.can_work_tavern()
            if key == "holglor":
                return self.can_work_tavern() and not self.glory_hole_asked and self.glory_hole_mentioned
            return False

        def can_work_portstreets(self):
            return self.prostitution_started and not self.can_work_tavern()

        def portstreet_work_active(self):
            return (
                self.can_work_portstreets()
                and str(self.getLocation() or "") == "PortStreets"
                and Georgett.portstreet_story_unblocked()
            )

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() == "PortStreets":
                return self.portstreet_visible_now()
            return super(LizaInfo, self).interaction_visible(room_code)

        def portstreet_client_event_available(self):
            return self.portstreet_work_active() and not self.portstreet_clients_seen_today and CheckIfSexEventExist(self.code_name, 3, "Prostitution") > 0

        def can_ask_about_clients(self):
            return self.has_seen_clients and people_to_int(self.rel, 0) >= 5

        def can_trigger_after_sermon_event(self):
            return people_to_int(Georgett.story_value("churchlizaadmit", 0), 0) > 0

define LizaStaticData = LizaData()
default Liza = LizaInfo()
