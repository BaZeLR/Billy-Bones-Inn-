# Private bedroom relief heard from the upstairs corridor.
# Each Event owns its own daily cadence and the authored labels own the outcome.

init -24 python:
    class TavernUpstairsBedroomReliefEvent(Event):
        def __init__(self, npc_id, room_code, target, hours):
            super(TavernUpstairsBedroomReliefEvent, self).__init__(
                (
                    target,
                    None,
                    hours,
                    None,
                    1,
                    None,
                    None,
                    None,
                    "TavernUpstairs",
                    "enter",
                    500,
                ),
                "",
                False,
            )
            self.npc_id = str(npc_id or "").strip().lower()
            self.room_code = str(room_code or "").strip()
            self.code_name = "%s_upstairs_bedroom_relief" % self.npc_id
            self.daily_key = "tavern_upstairs_bedroom_relief:%s" % self.npc_id
            self.repeatable = False
            self.source_refs = ["TavernUpstairs.rpy"]

        def checkConditions(self):
            info = people.get_info(self.npc_id)
            return (
                info is not None
                and str(people.location(self.npc_id) or "") == self.room_code
                and people.is_awake(self.npc_id)
                and npc_friend_level(self.npc_id) >= 2
                and npc_corruption_level(self.npc_id) >= 2
                and int(info.arousal_value() or 0) >= 65
                and tavern_kitchen_fertility_bonus_active()
            )


    AmandaUpstairsBedroomRelief = TavernUpstairsBedroomReliefEvent(
        "amanda",
        "TavernAmandaRoom",
        "story_amanda_upstairs_bedroom_relief",
        (20, 22),
    )
    MelissaUpstairsBedroomRelief = TavernUpstairsBedroomReliefEvent(
        "melissa",
        "TavernMelissaRoom",
        "story_melissa_upstairs_bedroom_relief",
        (20, 22),
    )
    SandraUpstairsBedroomRelief = TavernUpstairsBedroomReliefEvent(
        "sandra",
        "TavernSandraRoom",
        "story_sandra_upstairs_bedroom_relief",
        (20, 23),
    )


label story_amanda_upstairs_bedroom_relief:
    $ main_ui_begin_native_scene_state("За дверью комнаты Аманды")
    show screen main_ui
    $ scene_runtime.text = "Дверь комнаты Аманды плотно закрыта. Из-за нее доносится тихий скрип кровати, прерывистое дыхание и едва сдержанный стон. Через несколько минут все стихает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ Amanda.set_arousal(0)
    $ Amanda.apply_social_chance(20, 1, 1, 0, 0, 0, "upstairs_bedroom_relief")
    $ calendar_v2.advance_minutes(15)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_upstairs_bedroom_relief:
    $ main_ui_begin_native_scene_state("За дверью комнаты Мелиссы")
    show screen main_ui
    $ scene_runtime.text = "Дверь комнаты Мелиссы закрыта. За ней слышатся осторожный скрип кровати, сбившееся дыхание и приглушенный девичий стон. Через несколько минут коридор снова погружается в тишину."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ Melissa.set_arousal(0)
    $ Melissa.apply_social_chance(20, 1, 1, 0, 0, 0, "upstairs_bedroom_relief")
    $ calendar_v2.advance_minutes(15)
    $ main_ui_end_native_scene_state()
    return True


label story_sandra_upstairs_bedroom_relief:
    $ main_ui_begin_native_scene_state("За дверью комнаты Сандры")
    show screen main_ui
    $ scene_runtime.text = "Дверь комнаты Сандры закрыта. Из-за нее доносятся размеренный скрип кровати, тяжелое дыхание и короткий подавленный стон. Спустя несколько минут наверху вновь становится тихо."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ Sandra.set_arousal(0)
    $ Sandra.apply_social_chance(20, 1, 1, 0, 0, 0, "upstairs_bedroom_relief")
    $ calendar_v2.advance_minutes(15)
    $ main_ui_end_native_scene_state()
    return True
