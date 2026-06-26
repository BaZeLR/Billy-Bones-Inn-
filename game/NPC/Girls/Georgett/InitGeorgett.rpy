# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitGeorgett:
    python:
        GirlName = Georgett.code_name
        peopleData[GirlName] = GeorgettStaticData
        Georgett.initialize_new_game_state()
        peopleInfo[GirlName] = Georgett
        if Georgett not in girls:
            girls.append(Georgett)

    call WhoreNextDayClients(GirlName, 3, 3)
    return

init python:
    def georgett_story_defaults():
        return {
            "seeclients": 0,
            "askclients": 0,
            "askkids": 0,
            "askparents": 0,
            "askpregnancy": 0,
            "asksex": 0,
            "TellAboutEddieMomSex": 0,
            "foundinchurch": 0,
            "fuckinchurch": 0,
            "church_bench_seen": 0,
            "church_doggy_seen": 0,
            "church_liza_seen": 0,
            "lizasawinchurch": 0,
            "georgettadmit": 0,
            "churchgeorgettadmit": 0,
            "churchlizaadmit": 0,
            "SawChurchAfterCermon": 0,
            "TalkChurchAfterCermon": 0,
            "TalkChurchAfterCermonLiza": 0,
            "after_sermon_stage": 0,
            "GloryHoleExplained": 0,
            "GloryHoleAgreed": 0,
        }

    class GeorgettData(PeopleData):
        code_name = "georgett"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Жоржетта",
                fullname="Жоржетта",
                genitive="Жоржетты",
                dative="Жоржетте",
                portrait="images/georgett/portraits/portrait1.jpg",
                default_location="PortStreets",
                description="Жоржетта Брюно - молодая женщина, не очень высокого роста, чуть пухленькая и с большой налитой грудью. Она белокура и кареглаза. Ее внешность и повадки не дают никаких сомнений в том, что она выбрала себе путь отнюдь не монашки.",
                gift_preferences=["drink_ale_001", "wild_rose_001", "soap_001", "libido_tincture_001", "ethanol_001"],
            )
            self.birth_date = {"day": 22, "period": 13, "cycle": 1072}
            self.schedule_source = "schedules/georgett.json"

    class GeorgettInfo(Girl):
        """Georgette runtime: port work, tavern relocation, church story, pregnancy state."""
        unknown_name = "Молодая женщина"

        def __init__(self):
            super().__init__("georgett")
            self.code_name = "georgett"
            self.data = GeorgettStaticData
            self.uses_own_var_state = True
            self.rel = 0
            self.relationship = self.rel
            self.openness = 0
            self.corruption = 80
            self.known = False
            self.hired = False
            self.talked_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.stats = {
                "kids": 4,
                "beauty": 67,
                "sexacts": 6452,
                "cuminside": 3276,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 5,
                "PussyWetStart": 30,
                "virginity": False,
                "breastfeed": 0,
                "orgasms_given": 0,
            }
            self.skills = {
                "cooking": 50,
                "cleaning": 20,
                "waitress": 50,
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
            self.gift_preferences = list(GeorgettStaticData.gift_preferences)
            self.schedule_source = GeorgettStaticData.schedule_source
            self.current_location = "PortStreets"
            self.talk_preferences = {
                "favorite_topics": ["clients", "sex", "family", "pregnancy", "kids"],
                "blocked_topics": ["flirt"],
            }
            self.wardrobe = {
                "owned": ["slutdress", "blackstockings", "highshoes"],
                "gifted": [],
                "current_dress": "slutdress",
                "current_underwear": {
                    "bra": "",
                    "panties": "",
                    "legs": "blackstockings",
                    "shoes": "highshoes",
                },
            }
            self.var = {}
            self.sex_state = {}
            self.ensure_story_defaults()
            self.ensure_sex_state()

        def update(self):
            super(GeorgettInfo, self).update()
            self.data = GeorgettStaticData
            self.relationship = self.rel
            self.ensure_story_defaults()
            self.ensure_sex_state()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in georgett_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def ensure_sex_state(self):
            if not isinstance(self.sex_state, dict):
                self.sex_state = {}
            for key, value in {
                "location": "street",
                "somebody_cums": 0,
                "arousal": 0,
                "lick_pussy": 0,
                "tits_visible": 0,
                "pussy_visible": 0,
                "cock_position": "none",
                "top_removed": 0,
                "bottom_removed": 0,
                "top_raised": 0,
                "bottom_raised": 0,
                "cum_face_you": 0,
                "cum_face_others": 0,
                "cum_tits_you": 0,
                "cum_tits_others": 0,
                "cum_mouth_you": 0,
                "cum_mouth_others": 0,
                "cum_inside_you": 0,
                "cum_inside_others": 0,
            }.items():
                self.sex_state.setdefault(key, value)
            return self.sex_state

        def initialize_new_game_state(self):
            self.ensure_story_defaults()
            self.ensure_sex_state()
            return self

        def reset_daily(self, full=False):
            super(GeorgettInfo, self).reset_daily(full)
            self.talked_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.var["after_sermon_stage"] = 0
            self.var["portstreet_clients_seen_today"] = 0
            return self

        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()[key] = value
            return value

        def real_name(self):
            return self.data.fullname

        def real_name2(self):
            return self.data.genitive

        def real_name3(self):
            return self.data.dative

        def display_name(self):
            if people_to_int(self.rel, 0) <= 0:
                return str(self.unknown_name or "Молодая женщина")
            return str(self.data.fullname or self.code_name)

        def orgasm_count_given(self):
            return people_to_int(self.stats.get("orgasms_given", 0), 0)

        def had_sex_count(self):
            return people_to_int(self.stats.get("sexacts", 0), 0)

        def sex_setup(self, location="street"):
            sync_player_state_from_store()
            self.ensure_sex_state()
            self.sex_state["location"] = str(location or "street")
            self.sex_state["somebody_cums"] = 0
            self.sex_state["top_removed"] = 0
            self.sex_state["bottom_removed"] = 0
            self.sex_state["top_raised"] = 0
            self.sex_state["bottom_raised"] = 0
            self.refresh_sex_visibility()
            return self.sex_state

        def _player_intimacy(self):
            return player_state(False).intimacy

        def player_arousal(self):
            return self._player_intimacy().arousal_value("You")

        def set_player_arousal(self, value):
            intimacy = self._player_intimacy()
            new_value = intimacy.set_arousal(value, "You")
            intimacy.apply_to_store()
            return new_value

        def add_player_arousal(self, amount=0, cap=100):
            intimacy = self._player_intimacy()
            new_value = intimacy.add_arousal(amount, cap, "You")
            intimacy.apply_to_store()
            return new_value

        def can_player_cum(self):
            return self._player_intimacy().can_cum()

        def arousal_value(self):
            return people_to_int(self.ensure_sex_state().get("arousal", 0), 0)

        def set_arousal(self, value):
            self.ensure_sex_state()["arousal"] = max(0, min(100, people_to_int(value, 0)))
            return self.sex_state["arousal"]

        def add_arousal(self, amount=0, cap=100):
            state = self.ensure_sex_state()
            state["arousal"] = max(0, min(people_to_int(cap, 100), self.arousal_value() + people_to_int(amount, 0)))
            return state["arousal"]

        def set_cock_position(self, position="none", actor="You"):
            position_key = str(position or "none").strip().lower()
            if position_key not in ("none", "mouth", "pussy", "tits", "ass"):
                position_key = "none"
            actor_key = str(actor or "You").strip() or "You"
            state = self.ensure_sex_state()
            state.setdefault("partner_positions", {})[actor_key] = position_key
            if actor_key.lower() == "you":
                state["cock_position"] = position_key
            return position_key

        def cock_in(self, position="", actor="You"):
            actor_key = str(actor or "You").strip() or "You"
            state = self.ensure_sex_state()
            return state.get("partner_positions", {}).get(actor_key, state.get("cock_position", "none")) == str(position or "").strip().lower()

        def sex_busy(self):
            return people_to_int(self.ensure_sex_state().get("somebody_cums", 0), 0) != 0

        def set_sex_busy(self, value):
            self.ensure_sex_state()["somebody_cums"] = 1 if value else 0
            return self.sex_state["somebody_cums"]

        def visible_tits(self):
            return people_to_int(self.ensure_sex_state().get("tits_visible", 0), 0) > 0

        def visible_pussy(self):
            return people_to_int(self.ensure_sex_state().get("pussy_visible", 0), 0) > 0

        def has_top(self):
            return str(self.wardrobe.get("current_dress", "") or "") != "" and not people_to_int(self.ensure_sex_state().get("top_removed", 0), 0)

        def has_bottom(self):
            return str(self.wardrobe.get("current_dress", "") or "") != "" and not people_to_int(self.ensure_sex_state().get("bottom_removed", 0), 0)

        def top_is_raised(self):
            return people_to_int(self.ensure_sex_state().get("top_raised", 0), 0) != 0

        def bottom_is_raised(self):
            return people_to_int(self.ensure_sex_state().get("bottom_raised", 0), 0) != 0

        def needs_dress_up(self):
            state = self.ensure_sex_state()
            return (
                people_to_int(state.get("top_removed", 0), 0) != 0
                and people_to_int(state.get("bottom_removed", 0), 0) != 0
                and str(self.wardrobe.get("current_dress", "") or "") != ""
            )

        def refresh_sex_visibility(self):
            state = self.ensure_sex_state()
            underwear = self.wardrobe.get("current_underwear", {})
            state["tits_visible"] = 1 if str(underwear.get("bra", "") or "") == "" and (not self.has_top() or self.top_is_raised()) else 0
            state["pussy_visible"] = 1 if str(underwear.get("panties", "") or "") == "" and (not self.has_bottom() or self.bottom_is_raised()) else 0
            return state

        def remove_blouse_for_sex(self):
            self.ensure_sex_state()["top_removed"] = 1
            self.refresh_sex_visibility()
            self.set_cock_position("none")
            return self.sex_state

        def unbutton_blouse_for_sex(self):
            self.ensure_sex_state()["top_raised"] = 1
            self.refresh_sex_visibility()
            self.set_cock_position("none")
            return self.sex_state

        def raise_skirt_for_sex(self):
            self.ensure_sex_state()["bottom_raised"] = 1
            self.refresh_sex_visibility()
            self.set_cock_position("none")
            return self.sex_state

        def cum_state(self, key):
            return people_to_int(self.ensure_sex_state().get(str(key or ""), 0), 0)

        def clear_cum(self, *keys):
            state = self.ensure_sex_state()
            for key in keys:
                state[str(key)] = 0
            self.refresh_sex_visibility()
            self.set_cock_position("none")
            return state

        def add_lick_pussy(self):
            state = self.ensure_sex_state()
            state["lick_pussy"] = people_to_int(state.get("lick_pussy", 0), 0) + 1
            return state["lick_pussy"]

        def pregnancy_days(self):
            return people_to_int(self.stats.get("pregnancy", 0), 0)

        def record_orgasm_given(self):
            self.stats["orgasms_given"] = people_to_int(self.stats.get("orgasms_given", 0), 0) + 1
            self.stats["last_orgasm_day"] = people_to_int(dayspassed, 0)
            return self.stats["orgasms_given"]

        def player_cum(self, place):
            place_key = str(place or "").strip().lower()
            if place_key not in ("inside", "mouth", "tits", "face"):
                place_key = "outside"
            intimacy = self._player_intimacy()
            intimacy.record_cum(dayspassed)
            self.stats["sexacts"] = people_to_int(self.stats.get("sexacts", 0), 0) + 1
            self.fucked_today = people_to_int(self.fucked_today, 0) + 1
            if place_key == "inside":
                self.sex_state["cum_inside_you"] = 1
                self.stats["cuminside"] = people_to_int(self.stats.get("cuminside", 0), 0) + 1
                if people_to_int(self.stats.get("pregnancy", 0), 0) == 0:
                    chance = min(800, people_to_int(self.stats.get("ConceptionChance", 0), 0) * 3)
                    if renpy.random.randint(1, 1000) <= chance:
                        self.stats["pregnancy"] = 1
                        self.stats["pregfather"] = "Вы"
            elif place_key == "tits":
                self.sex_state["cum_tits_you"] = 1
            elif place_key == "mouth":
                self.sex_state["cum_mouth_you"] = 1
            elif place_key == "face":
                self.sex_state["cum_face_you"] = 1
            self.set_cock_position("none")
            self.set_sex_busy(1)
            intimacy.apply_to_store()
            return self.sex_state

        def talk_count(self):
            return people_to_int(self.talked_today, 0)

        def can_talk_today(self, limit=2):
            return self.talk_count() < people_to_int(limit, 2)

        def add_relation(self, amount=1, cap=20):
            self.rel = max(0, min(people_to_int(cap, 20), people_to_int(self.rel, 0) + people_to_int(amount, 0)))
            self.relationship = self.rel
            return self.rel

        def finish_talk(self):
            self.talked_today = people_to_int(self.talked_today, 0) + 1
            return self.talked_today

        def mark_asked_topic(self, topic_flag, relation_gain=1):
            flag = str(topic_flag or "")
            first_time = people_to_int(self.story_value(flag, 0), 0) == 0
            if first_time:
                self.set_story_value(flag, 1)
                if relation_gain:
                    self.add_relation(relation_gain)
            self.asked_today = people_to_int(self.asked_today, 0) + 1
            return first_time

        def can_ask_topic(self, topic):
            key = str(topic or "")
            if not self.can_talk_today():
                return False
            rel_value = people_to_int(self.rel, 0)
            if key == "clients":
                return people_to_int(self.story_value("seeclients", 0), 0) > 0 and rel_value >= 7
            if key == "sex":
                return (
                    people_to_int(self.story_value("askclients", 0), 0) > 0
                    and rel_value >= 7
                    and self.orgasm_count_given() >= 3
                )
            if key == "family":
                return (
                    people_to_int(self.story_value("asksex", 0), 0) > 0
                    and rel_value >= 7
                    and self.orgasm_count_given() >= 4
                )
            if key == "pregnancy":
                return (
                    people_to_int(self.story_value("askparents", 0), 0) > 0
                    and rel_value >= 7
                    and self.orgasm_count_given() >= 4
                )
            if key == "kids":
                return (
                    people_to_int(self.story_value("askpregnancy", 0), 0) > 0
                    and rel_value >= 7
                    and self.orgasm_count_given() >= 5
                )
            if key == "gerhard":
                return people_to_int(self.story_value("SawChurchAfterCermon", 0), 0) > 0
            return False

        def getLocation(self, wday=None, hour=None):
            location_value = super(GeorgettInfo, self).getLocation(wday, hour)
            if str(location_value or "") == "PortStreets":
                if self.portstreet_visible_now():
                    self.location = "PortStreets"
                    return "PortStreets"
                if (
                    people_to_int(self.var.get("portstreet_clients_seen_today", 0), 0) == 0
                    and CheckIfSexEventExist(self.code_name, 3, "Prostitution") > 0
                ):
                    self.location = "PortStreetsBackAlley"
                    return "PortStreetsBackAlley"
            return location_value

        def can_work_portstreets(self):
            return str(self.getLocation() or "") in ("PortStreets", "PortStreetsBackAlley") and not self.can_work_tavern()

        def portstreet_story_unblocked(self):
            return not (
                people_to_int(self.story_value("TalkChurchAfterCermonLiza", 0), 0) != 0
                and people_to_int(Liza.story_value("ProstStart", 0), 0) == 0
            )

        def portstreet_work_hour(self):
            calendar_v2.sync_state()
            return people_to_int(calendar_v2.hour, 0) >= 19 and people_to_int(week, 0) != 5

        def portstreet_work_active(self):
            return self.can_work_portstreets() and self.portstreet_story_unblocked() and self.portstreet_work_hour()

        def set_portstreet_visible(self, visible=True):
            self.var["portstreet_visible_now"] = 1 if visible else 0
            return bool(visible)

        def portstreet_visible_now(self):
            return people_to_int(self.var.get("portstreet_visible_now", 0), 0) > 0

        def portstreet_client_event_available(self):
            return self.portstreet_work_active() and people_to_int(self.var.get("portstreet_clients_seen_today", 0), 0) == 0 and CheckIfSexEventExist(self.code_name, 3, "Prostitution") > 0

        def mark_portstreet_clients_seen(self):
            self.var["portstreet_clients_seen_today"] = 1
            return self.set_story_value("seeclients", 1)

        def can_work_tavern(self):
            self.hired = people_to_int(self.jobs.get("jobWhoreAvail", 0), 0) > 0
            return self.hired

        def set_hired(self, hired=True):
            self.hired = bool(hired)
            self.jobs["jobWhoreAvail"] = 1 if self.hired else 0
            self.jobs["jobwhore"] = 1 if self.hired else 0
            self.current_location = "TavernMain" if self.hired else "PortStreets"
            return self.hired

        def can_use_gloryhole(self):
            return people_to_int(self.jobs.get("jobGloryHoleAvail", 0), 0) > 0

        def can_invite_to_tavern(self):
            return (
                Alber.var_int("talkedaboutliza", 0) > 0
                and people_to_int(self.rel, 0) >= 7
                and str(self.getLocation() or "") == "PortStreets"
            )

        def can_ask_about_priest(self):
            return people_to_int(self.story_value("SawChurchAfterCermon", 0), 0) > 0

        def can_trigger_after_sermon_event(self):
            return people_to_int(self.story_value("churchgeorgettadmit", 0), 0) > 0

        def after_sermon_stage(self):
            return people_to_int(self.story_value("after_sermon_stage", 0), 0)

        def set_after_sermon_stage(self, value):
            return self.set_story_value("after_sermon_stage", people_to_int(value, 0))

        def church_after_sermon_event_available(self):
            return (
                church_after_cermon_action_visible()
                and self.can_trigger_after_sermon_event()
                and self.after_sermon_stage() < 4
                and CheckIfSexEventExist(self.code_name, 99, "Priest") > 0
            )

        def can_schedule_dress_shop_visit(self):
            return people_to_int(self.rel, 0) > 8

        def can_schedule_barber_visit(self):
            return self.can_work_tavern()

        def pregnancy_stage(self):
            days = people_to_int(self.stats.get("pregnancy", 0), 0)
            if days <= 0:
                return "none"
            if days < 120:
                return "early"
            if days < 210:
                return "visible"
            if days < 270:
                return "late"
            return "birth_due"

define GeorgettStaticData = GeorgettData()
default Georgett = GeorgettInfo()
