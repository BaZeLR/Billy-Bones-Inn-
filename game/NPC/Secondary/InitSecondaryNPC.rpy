# Secondary NPC registration (PeopleInfo instance-owned identity model)
# NPC identity and story state are owned by their PeopleInfo instances.
# Most secondary classes live here. Larger NPCs can own their own Init*.rpy
# files, following the same pattern used for girls.
# Instantiation + list append stays in the thin label registrations.
# References:
# - textLocRef\InitSecondaryNPC.txt (legacy defaults)
# - devdocs/people.rpy (historical model)
# - game/Utilities/General/NPC/PeopleRuntime.rpy (BaseNPC + authoritative PeopleRegistry)
# - User request: finish all secondaries including Luisa and Sergio.
#
# Robin (the "Robin Hood" parody leader of the обездоленные in the Blackwood/Sherwood cut)
# Dialog ready in textLocRef\IntRobinTalk.txt
# Pictures ready (portrait, robin1, robin2 sequences used in SherwoodTravel + IntRobinTalk)

init python:
    # --- All secondary class definitions live here in the normal Init file (init python block) ---
    # Per user request: specific classes in the per-NPC init file, inheriting BaseNPC from the people rpy file.
    # Story state stays on each NPC instance's .var dictionary.

    class LuisaData(PeopleData):
        code_name = "luisa"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Луиза",
                fullname="Толстушка Луиза",
                genitive="Луизы",
                dative="Луизе",
                default_location="",
                description="Луиза - полная городская знакомая из охотничьей лавки и городских социальных сцен.",
                birth_date={"day": 1, "period": 1, "cycle": 1072},
                schedule_entries=[
                    NPCScheduleEntry(
                        location="HunterClub",
                        weekdays=[1, 2, 3, 4, 6],
                        start_hour=8,
                        end_hour=19,
                        label="hunter_club",
                    ),
                ],
            )

    class LuisaInfo(BaseNPC):
        """Fat Luisa: secondary female NPC for hunter store and social scenes."""
        talk_label = "HunterClubLuiseTalk"
        unknown_name = "Луиза"
        STORY_DEFAULTS = {
            "met": 0,
            "lasttalkday": -1,
        }

        def __init__(self, name="luisa", **kwargs):
            super().__init__(name, **kwargs)
            self.var = dict(kwargs.get("var", {}) or {})
            self.ensure_story_defaults()

    class SergioData(PeopleData):
        code_name = "sergio"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Серджио",
                fullname="Серджио",
                genitive="Серджио",
                dative="Серджио",
                default_location="",
                description="Серджио - цирюльник из квартала ремесленников, связан с тайными визитами столичного жениха Клариссы.",
                birth_date={"day": 1, "period": 1, "cycle": 1065},
            )
            self.schedule_source = "schedules/sergio.json"

    class SergioInfo(BaseNPC):
        """Sergio (secondary artisan / town NPC, discount/quest hooks)."""
        talk_label = "BarberShopTalk"
        unknown_name = "Серджио"
        STORY_DEFAULTS = {
            "met": 0,
            "lasttalkday": -1,
        }

        def __init__(self, name="sergio", **kwargs):
            super().__init__(name, **kwargs)
            self.var = dict(kwargs.get("var", {}) or {})
            self.ensure_story_defaults()

    class GerhardData(PeopleData):
        code_name = "gerhard"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Брат Герхард",
                fullname="Брат Герхард",
                genitive="брата Герхарда",
                dative="брату Герхарду",
                default_location="",
                description="Брат Герхард - священник городского храма, принимает исповеди и ведет воскресные наставления.",
                birth_date={"day": 1, "period": 1, "cycle": 1052},
                portrait="images/gerhard/portrait.png",
                schedule_entries=[
                    NPCScheduleEntry(
                        location="Church",
                        weekdays=[7],
                        start_hour=8,
                        end_hour=13,
                        label="sunday_service",
                    ),
                ],
            )

    class GerhardInfo(BaseNPC):
        """Brother Gerhardt: church priest runtime object."""
        talk_label = "ChurchIspoved"
        talk_args = (1,)
        unknown_name = "Брат Герхард"

        def __init__(self, name="gerhard", **kwargs):
            super().__init__(name, **kwargs)
            self.var = dict(kwargs.get("var", {}) or {})

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() == "Church":
                return church_confession_action_visible()
            return super(GerhardInfo, self).interaction_visible(room_code)

define GerhardStaticData = GerhardData()
default Gerhard = GerhardInfo()
define LuisaStaticData = LuisaData()
default Luisa = LuisaInfo()
define SergioStaticData = SergioData()
default Sergio = SergioInfo()

label register_gerhard_secondary:
    python:
        people.register(GerhardStaticData, Gerhard)
    return


label register_luisa_secondary:
    python:
        people.register(LuisaStaticData, Luisa)
    return


label register_sergio_secondary:
    python:
        people.register(SergioStaticData, Sergio)
    return
