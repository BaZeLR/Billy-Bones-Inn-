default WerecatNPCState = {
    "pet_day": -1,
    "trust": 0,
    "comfort": 0,
}

init -8 python:
    def werecat_is_active():
        return int(WerecatVar.get("adopted", 0) or 0) == 1 and int(WerecatVar.get("sold", 0) or 0) == 0

    def werecat_sleep_location():
        return "Backyard"

    def werecat_sync_profile():
        RealName["werecat"] = str(werecat_display_name() or "Луна")
        RealName2["werecat"] = str(werecat_display_name() or "Луны")
        RealName3["werecat"] = str(werecat_display_name() or "Луне")
        age_girls["werecat"] = int(age_girls.get("werecat", 19) or 19)
        DateOfBirth["werecat"] = DateOfBirth.get("werecat", calendar_make_birth_record(age_girls["werecat"]))
        girltextdesc["werecat"] = "Невысокая гибкая кошкодевочка с внимательными золотистыми глазами, мягкими ушами и пушистым хвостом. Двигается бесшумно, настороженно и слишком ловко для обычной домашней любимицы."
        knowsMC["werecat"] = True if werecat_is_active() else bool(knowsMC.get("werecat", False))
        if not werecat_is_active():
            CurrentLoc["werecat"] = ""
            return ""
        try:
            return npc_schedule_sync_currentloc("werecat")
        except Exception:
            CurrentLoc["werecat"] = "Backyard"
            return "Backyard"

    def werecat_npc_present(room_code=""):
        if not werecat_is_active():
            return False
        room_key = str(room_code or CurLoc or "").strip()
        try:
            current_room = str(getLocation("werecat") or "")
        except Exception:
            current_room = str(CurrentLoc.get("werecat", "") or "")
        return current_room == room_key

    def werecat_picture_path():
        for picture_path in (
            "images/general/kitty.png",
            "images/general/kitty_splash.png",
            "images/general/hunter_store_catInfo.png",
            "images/rpg_message_bg.png",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def werecat_scene_seed():
        return int(dayspassed or 0) + int(day or 0) + int(month or 0) + int(time or 0)

    def werecat_talk_intro_text(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if room_key == "TavernKitchen":
            if werecat_scene_seed() % 2 == 0:
                return "%s устроилась у самого очага и с деловым видом лакает оставленное ей блюдце молока. Кажется, кухню она уже считает своим законным теплым углом." % str(werecat_display_name() or "Кошка")
            return "%s осторожно сидит у очага и следит за кухней так, будто все еще не до конца решила, дом это или просто временная стоянка." % str(werecat_display_name() or "Кошка")
        if room_key == "TavernMain":
            if werecat_scene_seed() % 2 == 0:
                return "%s разлеглась у камина, лениво прищурив глаза на огонь. Со стороны она уже почти выглядит обычной трактирной кошкой, если не считать слишком умного взгляда." % str(werecat_display_name() or "Кошка")
            return "%s держится в стороне от главной залы, но внимательно следит за каждым новым запахом и движением." % str(werecat_display_name() or "Кошка")
        return "%s устроилась тихо, по-кошачьи свернувшись, но янтарные глаза все равно следят за вами слишком осмысленно." % str(werecat_display_name() or "Кошка")

    def werecat_card_lines():
        lines = [
            "Имя: %s." % str(werecat_display_name() or "Луна"),
            "В трактире она появилась после лесной ловушки и с тех пор постепенно привыкает к дому.",
            "Крыс и прочую мелкую дрянь она чует куда лучше обычной кошки, а людей изучает почти по-человечески внимательно.",
        ]
        if int(WerecatVar.get("rats_problem_active", 0) or 0) == 0:
            lines.append("С тех пор в кладовой стало заметно тише: крысы больше не хозяйничают, как раньше.")
        if werecat_npc_present("TavernKitchen"):
            lines.append("Сейчас держится поближе к теплу кухни и временами лакает оставленное для нее молоко.")
        elif werecat_npc_present("TavernMain"):
            lines.append("Сейчас осваивается в общем зале и любит дремать поближе к камину.")
        elif werecat_npc_present("Backyard"):
            lines.append("Сейчас предпочитает двор, где можно и спрятаться, и выбрать удобный угол.")
        return lines

    def werecat_card_title():
        return str(werecat_display_name() or "Луна")

    def werecat_card_stat_rows():
        trust_value = int(WerecatNPCState.get("trust", 0) or 0)
        comfort_value = int(WerecatNPCState.get("comfort", 0) or 0)
        if trust_value >= 12:
            trust_text = "домашняя"
        elif trust_value >= 8:
            trust_text = "доверяет"
        elif trust_value >= 4:
            trust_text = "привыкает"
        else:
            trust_text = "насторожена"
        return [
            ("Доверие", str(trust_value)),
            ("Уют", str(comfort_value)),
            ("Состояние", trust_text),
            ("Дом", str(CurrentLoc.get("werecat", "нет") or "нет")),
        ]

    def werecat_npc_entry(room_code=""):
        if not werecat_npc_present(room_code):
            return None
        return {
            "npc_id": "werecat",
            "name": str(werecat_display_name() or "Луна"),
            "talk_label": "IntWerecatTalk",
            "auto_card": True,
        }

    def show_werecat_card_main_ui_state():
        import renpy as renpy_pkg
        store = renpy_pkg.store
        store.UI_mode = "werecat"
        store.UI_selected_char = "werecat"
        store.current_girl_key = "werecat"
        store.current_action_title = werecat_card_title()
        store.current_action_content = None
        store.current_action_items = []
        restart_fn = getattr(renpy, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()


init 2 python:
    npc_schedule_set("werecat", [
        NPCScheduleEntry(
            location="TavernKitchen",
            weekdays=[1, 2, 3, 4, 5, 6, 7],
            time_slots=[0],
            awake=True,
            talkable=True,
            condition=npc_schedule_rule("werecat_active"),
            priority=120,
            label="werecat_breakfast",
        ),
        NPCScheduleEntry(
            location="Backyard",
            weekdays=[1, 2, 3, 4, 5, 6, 7],
            time_slots=[1, 2],
            awake=True,
            talkable=True,
            condition=npc_schedule_rule("werecat_active"),
            priority=110,
            label="werecat_day",
        ),
        NPCScheduleEntry(
            location="TavernMain",
            weekdays=[1, 2, 3, 4, 5, 6, 7],
            time_slots=[3],
            awake=True,
            talkable=True,
            condition=npc_schedule_rule("werecat_active"),
            priority=105,
            label="werecat_evening",
        ),
        NPCScheduleEntry(
            location=werecat_sleep_location(),
            weekdays=[1, 2, 3, 4, 5, 6, 7],
            time_slots=[4],
            awake=False,
            talkable=False,
            condition=npc_schedule_rule("werecat_active"),
            priority=100,
            label="werecat_sleep",
        ),
    ])

    def _werecat_after_load_init():
        try:
            werecat_sync_profile()
        except Exception:
            pass

    if _werecat_after_load_init not in config.after_load_callbacks:
        config.after_load_callbacks.append(_werecat_after_load_init)


label IntWerecatTalk(room_code=""):
    $ werecat_sync_profile()
    if not werecat_is_active():
        return
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    $ main_ui_begin_talk_state(str(werecat_display_name() or "Луна"), "werecat")
    $ current_action_title = str(werecat_display_name() or "Луна")
    $ current_action_content = None
    $ _werecat_picture = werecat_picture_path()
    if str(_werecat_picture or "").strip():
        $ _layout_last_picture = _werecat_picture
    $ MainTxt = werecat_talk_intro_text(_werecat_room)
    $ CurLocDesc = MainTxt
    call IntWerecatTalkRefresh(_werecat_room)
    return


label IntWerecatTalkRefresh(room_code=""):
    $ werecat_sync_profile()
    if not werecat_is_active():
        $ main_ui_end_talk_state()
        return
    $ _werecat_room = str(room_code or CurLoc or "").strip()
    $ main_ui_begin_talk_state(str(werecat_display_name() or "Луна"), "werecat")
    $ current_action_title = str(werecat_display_name() or "Луна")
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Осмотреть", Function(show_werecat_card_main_ui_state)),
    ]
    if int(WerecatNPCState.get("pet_day", -1) or -1) != int(dayspassed or 0):
        $ current_action_items.append(MenuItem("Погладить кошку", Function(main_ui_call_label, "IntWerecatTalkApply", _werecat_room, "pet")))
    $ current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
    return


label IntWerecatTalkApply(room_code="", choice_code=""):
    $ _werecat_choice = str(choice_code or "").strip().lower()
    if _werecat_choice == "pet":
        $ WerecatNPCState["pet_day"] = int(dayspassed or 0)
        $ WerecatNPCState["trust"] = min(20, int(WerecatNPCState.get("trust", 0) or 0) + 1)
        $ WerecatNPCState["comfort"] = min(20, int(WerecatNPCState.get("comfort", 0) or 0) + 1)
        $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
        $ MainTxt = "%s сперва настораживается, но потом все же позволяет вам осторожно провести ладонью по ушам и мягкой шерсти у шеи. Похоже, к дому и к вам она постепенно привыкает." % str(werecat_display_name() or "Кошка")
        $ CurLocDesc = MainTxt
        call stat
        call IntWerecatTalkRefresh(room_code)
        return
    call IntWerecatTalkRefresh(room_code)
    return


label ShowWerecatCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ show_werecat_card_main_ui_state()
        return
    show screen werecat_card_overlay(return_label)
    return


label HideWerecatCard(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ main_ui_restore_room_scene_state()
        return
    hide screen werecat_card_overlay
    if str(return_label or "") != "":
        call expression return_label
    return


screen werecat_card_overlay(return_label=""):
    zorder 120

    $ _title = werecat_card_title()
    $ _portrait = werecat_picture_path()
    $ _stats = werecat_card_stat_rows()
    $ _lines = werecat_card_lines()
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add im.Scale("images/rpg_message_bg.png", _left_w, _left_h)

        viewport:
            xpos 28
            ypos 24
            xsize _left_w - 56
            ysize _left_h - 48
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title.upper() size 30 color "#1e130c" xalign 0.5

                hbox:
                    spacing 12

                    add im.Scale(_portrait, 180, 240)

                    vbox:
                        spacing 3
                        for _row in _stats:
                            text "%s: %s" % (_row[0], _row[1]) size 18 color "#1e130c"

                for _line in _lines:
                    text _line size 16 color "#2d1d12"

                null height 8

                textbutton "Назад":
                    xminimum 220
                    text_size 22
                    text_bold True
                    text_color "#5c0f1b"
                    text_hover_color "#7d1a2c"
                    if str(return_label or "") == "__return__":
                        action Return()
                    else:
                        action Call("HideWerecatCard", return_label)
