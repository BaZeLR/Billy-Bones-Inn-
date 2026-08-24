init python:
    def eddie_talk_robbed_window():
        robbed_day = int(Becky.eddie_robbed_day or 0)
        return robbed_day > 0 and robbed_day + 12 >= int(current_game_day() or 0)

    def eddie_talk_intro_text():
        if str(rooms.current_code or "") == "GroceryStore":
            text = "Сейчас за прилавком стоит Эдди, старший сын вдовы Блэнкеншип. Это здоровый рыжий парень примерно вашего возраста."
            if eddie_talk_robbed_window():
                text += "\n\nВы замечаете, что у Эдди красуется большой синяк под глазом и распухло ухо."
            return text
        return "Эдди вопросительно смотрит на вас, ожидая, о чем вы заговорите."

    def eddie_talk_can_personal(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return int(getattr(info, "rel", 0) or 0) >= 5

    def eddie_talk_can_whores(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return (
            int(getattr(info, "rel", 0) or 0) >= 5
            and str(people.location("georgett") or "") == "TavernMain"
            and not info.told_about_tavern_whores
            and int(getattr(info, "talked_today", 0) or 0) < 2
        )

    def eddie_talk_can_girls(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return (
            int(getattr(info, "rel", 0) or 0) >= 5
            and str(people.location("georgett") or "") == "TavernMain"
            and info.seen_with_georgett
            and not info.talked_about_georgett
            and int(getattr(info, "talked_today", 0) or 0) < 2
        )

    def eddie_talk_can_mom_helper(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return (
            int(getattr(info, "rel", 0) or 0) >= 3
            and bool(Becky.home_sex_unlocked)
            and info.saw_mother_sex
            and info.seen_with_georgett
            and int(Becky.eddie_join_stage or 0) != 1
            and int(getattr(info, "talked_today", 0) or 0) < 2
        )

    def eddie_talk_can_bruise(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return (
            int(getattr(info, "rel", 0) or 0) >= 3
            and int(getattr(info, "talked_today", 0) or 0) < 2
            and eddie_talk_robbed_window()
            and info.fingal_talk_stage == 0
        )

    def eddie_talk_can_who_hit(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return (
            int(getattr(info, "rel", 0) or 0) >= 7
            and int(getattr(info, "talked_today", 0) or 0) < 2
            and eddie_talk_robbed_window()
            and info.fingal_talk_stage == 1
        )

    def eddie_talk_can_destination(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return (
            int(getattr(info, "rel", 0) or 0) >= 7
            and int(getattr(info, "talked_today", 0) or 0) < 2
            and eddie_talk_robbed_window()
            and info.fingal_talk_stage == 2
            and not info.asked_fingal_destination
        )

    def eddie_talk_can_complain(eddie_name="eddie"):
        info = people.get_info(eddie_name)
        return (
            int(getattr(info, "rel", 0) or 0) >= 7
            and int(getattr(info, "talked_today", 0) or 0) < 2
            and eddie_talk_robbed_window()
            and info.fingal_talk_stage == 2
            and not info.asked_fingal_guard_complaint
        )
