# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitGeorgett:
    python:
        Georgett.initialize_new_game_state()
        people.register(GeorgettStaticData, Georgett)

    call WhoreNextDayClients(Georgett.code_name, 3, 3)
    return

init python:
    class GeorgettData(PeopleData):
        code_name = "georgett"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Жоржетта",
                fullname="Жоржетта",
                genitive="Жоржетты",
                dative="Жоржетте",
                portrait="images/georgett/portraits/portrait.jpg",
                default_location="",
                description="Жоржетта Брюно - молодая женщина, не очень высокого роста, чуть пухленькая и с большой налитой грудью. Она белокура и кареглаза. Ее внешность и повадки не дают никаких сомнений в том, что она выбрала себе путь отнюдь не монашки.",
                gift_preferences=["drink_ale_001", "wild_rose_001", "soap_001", "libido_tincture_001", "ethanol_001"],
            )
            self.birth_date = {"day": 22, "period": 13, "cycle": 1072}
            self.schedule_source = "schedules/georgett.json"

    class GeorgettInfo(Girl):
        """Georgette runtime: port work, tavern relocation, church story, pregnancy state."""

        talk_label = "IntGeorgettTalk"
        ORGASM_FRIENDSHIP_GAIN = 1
        OPENNESS_RELATIONSHIP_STEPS = ((5, 3), (8, 5), (9, 6), (10, 7))

        STORY_DEFAULTS = {
            "seeclients": 0,
            "askclients": 0,
            "askkids": 0,
            "askparents": 0,
            "askpregnancy": 0,
            "asksex": 0,
            "TellAboutEddieMomSex": 0,
            "foundinchurch": 0,
            "fuckinchurch": 0,
            "lizasawinchurch": 0,
            "georgettadmit": 0,
            "churchgeorgettadmit": 0,
            "churchlizaadmit": 0,
            "SawChurchAfterCermon": 0,
            "TalkChurchAfterCermon": 0,
            "TalkChurchAfterCermonLiza": 0,
            "GloryHoleExplained": 0,
            "GloryHoleAgreed": 0,
        }

        uses_tavern_client_room = True
        unknown_name = "Молодая женщина"

        def __init__(self):
            super().__init__("georgett")
            self.code_name = "georgett"
            self.data = GeorgettStaticData
            self.uses_own_var_state = True
            self.rel = 0
            self.openness = 0
            self.corruption = 80
            self.known = False
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
            self.ensure_story_defaults()
            self.ensure_sex_state()
            return self

        def ensure_sex_state(self):
            state = super(GeorgettInfo, self).ensure_sex_state()
            for key, value in {
                "location": "street",
                "lick_pussy": 0,
                "top_removed": 0,
                "bottom_removed": 0,
                "top_raised": 0,
                "bottom_raised": 0,
            }.items():
                state.setdefault(key, value)
            state.pop("tits_visible", None)
            state.pop("pussy_visible", None)
            return state

        def initialize_new_game_state(self):
            self.ensure_story_defaults()
            self.ensure_sex_state()
            return self

        def reset_daily(self, full=False):
            super(GeorgettInfo, self).reset_daily(full)
            self.var["portstreet_clients_seen_today"] = 0
            return self

        def real_name(self):
            return self.data.fullname

        def real_name2(self):
            return self.data.genitive

        def real_name3(self):
            return self.data.dative

        def sex_setup(self, location="street"):
            self.ensure_sex_state()
            self.sex_state["location"] = str(location or "street")
            self.sex_state["somebody_cums"] = 0
            self.sex_state["top_removed"] = 0
            self.sex_state["bottom_removed"] = 0
            self.sex_state["top_raised"] = 0
            self.sex_state["bottom_raised"] = 0
            return self.sex_state

        def sex_location(self):
            return str(self.ensure_sex_state().get("location", "street") or "street")

        def needs_dress_up(self):
            state = self.ensure_sex_state()
            return (
                people_to_int(state.get("top_removed", 0), 0) != 0
                and people_to_int(state.get("bottom_removed", 0), 0) != 0
                and str(self.wardrobe.get("current_dress", "") or "") != ""
            )

        def remove_blouse_for_sex(self):
            self.ensure_sex_state()["top_removed"] = 1
            self.set_cock_position("none")
            return self.sex_state

        def unbutton_blouse_for_sex(self):
            self.ensure_sex_state()["top_raised"] = 1
            self.set_cock_position("none")
            return self.sex_state

        def raise_skirt_for_sex(self):
            self.ensure_sex_state()["bottom_raised"] = 1
            self.set_cock_position("none")
            return self.sex_state

        def clear_cum(self, *keys):
            state = self.ensure_sex_state()
            for key in keys:
                state[str(key)] = 0
            self.set_cock_position("none")
            return state

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
                    and people_to_int(self.sex_stat("orgasms_given", 0), 0) >= 3
                )
            if key == "family":
                return (
                    people_to_int(self.story_value("asksex", 0), 0) > 0
                    and rel_value >= 7
                    and people_to_int(self.sex_stat("orgasms_given", 0), 0) >= 4
                )
            if key == "pregnancy":
                return (
                    people_to_int(self.story_value("askparents", 0), 0) > 0
                    and rel_value >= 7
                    and people_to_int(self.sex_stat("orgasms_given", 0), 0) >= 4
                )
            if key == "kids":
                return (
                    people_to_int(self.story_value("askpregnancy", 0), 0) > 0
                    and rel_value >= 7
                    and people_to_int(self.sex_stat("orgasms_given", 0), 0) >= 5
                )
            if key == "gerhard":
                return people_to_int(self.story_value("SawChurchAfterCermon", 0), 0) > 0
            return False

        def can_work_portstreets(self):
            return str(self.getLocation() or "") == "PortStreets" and not self.can_work_tavern()

        def portstreet_story_unblocked(self):
            return not (
                people_to_int(self.story_value("TalkChurchAfterCermonLiza", 0), 0) != 0
                and not Liza.prostitution_started
            )

        def portstreet_work_active(self):
            return self.can_work_portstreets() and self.portstreet_story_unblocked()

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() == "PortStreets":
                return self.portstreet_visible_now()
            return super(GeorgettInfo, self).interaction_visible(room_code)

        def action_data(self, where_id=""):
            data = super(GeorgettInfo, self).action_data(where_id)
            room_key = str(where_id or "").strip()
            if room_key == "PortStreets":
                data["talk_args"] = (self.name, "street")
                data["picture_path"] = "images/georgett/portraits/portrait.jpg"
                data["idle_picture"] = data["picture_path"]
                data["talk_picture"] = data["picture_path"]
            elif room_key == "TavernMain":
                data["talk_args"] = (self.name, "tavern")
            return data

        def portstreet_scene_pictures(self):
            return [
                path for path in [
                    "images/georgett/Port/portStreets.png",
                    "images/georgett/Port/portstreets1.png",
                    "images/georgett/Port/portStreetsG_1.png",
                    "images/georgett/Port/port1.jpg",
                    "images/georgett/Port/port2.jpg",
                    "images/georgett/Port/port3.jpg",
                ] if renpy.loadable(path)
            ]

        def portstreet_scene_picture(self):
            pictures = self.portstreet_scene_pictures()
            if not pictures:
                return self.data.portrait
            if len(pictures) == 1:
                return pictures[0]
            return pictures[procedural_randint(0, len(pictures) - 1, "georgett_portstreets_scene_%s" % people_to_int(current_game_day(), 0))]

        def portstreet_client_event_available(self):
            has_player_history = any(
                str(row.get("partner", row.get("DudeName", "")) or "").strip().lower() in ("you", "вы")
                for row in list(getattr(self, "detailed_sex_history", []) or [])
            )
            return has_player_history and self.portstreet_work_active() and people_to_int(self.var.get("portstreet_clients_seen_today", 0), 0) == 0 and CheckIfSexEventExist(self.code_name, 3, "Prostitution") > 0

        def can_invite_to_tavern(self):
            return (
                Alber.talked_about_liza
                and people_to_int(self.rel, 0) >= 7
                and str(self.getLocation() or "") == "PortStreets"
            )

        def can_trigger_after_sermon_event(self):
            return people_to_int(self.story_value("churchgeorgettadmit", 0), 0) > 0

define GeorgettStaticData = GeorgettData()
default Georgett = GeorgettInfo()
