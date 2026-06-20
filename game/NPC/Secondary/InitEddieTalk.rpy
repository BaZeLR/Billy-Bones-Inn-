init python:
    def eddie_talk_init_state():
        Talked.setdefault("eddie", 0)
        TalkedToday.setdefault("eddie", 0)
        Friends.setdefault("eddie", 0)
        return True

    def eddie_talk_picture_path(becky_var=None):
        if str(CurLoc or "") != "GroceryStore":
            return ""
        row = becky_var if isinstance(becky_var, dict) else getattr(Becky, "var", {})
        robbed_day = int(row.get("EddieRobbedDay", 0) or 0)
        if robbed_day > 0 and robbed_day + 12 >= int(dayspassed or 0):
            return "images/eddie/portraits/fingal.png"
        return "images/eddie/portraits/portrait_0.png"

    def eddie_talk_robbed_window(becky_var=None):
        row = becky_var if isinstance(becky_var, dict) else getattr(Becky, "var", {})
        robbed_day = int(row.get("EddieRobbedDay", 0) or 0)
        return robbed_day > 0 and robbed_day + 12 >= int(dayspassed or 0)

    def eddie_talk_intro_text():
        if str(CurLoc or "") == "GroceryStore":
            text = "Сейчас за прилавком стоит Эдди, старший сын вдовы Блэнкеншип. Это здоровый рыжий парень примерно вашего возраста."
            if eddie_talk_robbed_window(getattr(Becky, "var", {})):
                text += "\n\nВы замечаете, что у Эдди красуется большой синяк под глазом и распухло ухо."
            return text
        return "Эдди вопросительно смотрит на вас, ожидая, о чем вы заговорите."

    def eddie_talk_can_personal(eddie_name="eddie"):
        return int(Friends.get(eddie_name, 0) or 0) >= 5

    def eddie_talk_can_whores(eddie_var, eddie_name="eddie"):
        return (
            int(Friends.get(eddie_name, 0) or 0) >= 5
            and str(getLocation("georgett") or "") == "TavernMain"
            and int(eddie_var.get("TalkedAboutWhores", 0) or 0) == 0
            and int(Talked.get(eddie_name, 0) or 0) < 2
        )

    def eddie_talk_can_girls(eddie_var, eddie_name="eddie"):
        return (
            int(Friends.get(eddie_name, 0) or 0) >= 5
            and str(getLocation("georgett") or "") == "TavernMain"
            and int(eddie_var.get("SawWithGeorgett", 0) or 0) > 0
            and int(eddie_var.get("TalkedAboutGeorgett", 0) or 0) == 0
            and int(Talked.get(eddie_name, 0) or 0) < 2
        )

    def eddie_talk_can_mom_helper(eddie_var, becky_var, eddie_name="eddie"):
        return (
            int(Friends.get(eddie_name, 0) or 0) >= 3
            and int(becky_var.get("HomeSex", 0) or 0) > 0
            and int(eddie_var.get("SawMomSex", 0) or 0) > 0
            and int(eddie_var.get("SawWithGeorgett", 0) or 0) > 0
            and int(becky_var.get("EddieTryToFuck", 0) or 0) != 1
            and int(Talked.get(eddie_name, 0) or 0) < 2
        )

    def eddie_talk_can_bruise(eddie_var, becky_var, eddie_name="eddie"):
        return (
            int(Friends.get(eddie_name, 0) or 0) >= 3
            and int(Talked.get(eddie_name, 0) or 0) < 2
            and eddie_talk_robbed_window(becky_var)
            and int(eddie_var.get("FingalTalk", 0) or 0) == 0
        )

    def eddie_talk_can_who_hit(eddie_var, becky_var, eddie_name="eddie"):
        return (
            int(Friends.get(eddie_name, 0) or 0) >= 7
            and int(Talked.get(eddie_name, 0) or 0) < 2
            and eddie_talk_robbed_window(becky_var)
            and int(eddie_var.get("FingalTalk", 0) or 0) == 1
        )

    def eddie_talk_can_destination(eddie_var, becky_var, eddie_name="eddie"):
        return (
            int(Friends.get(eddie_name, 0) or 0) >= 7
            and int(Talked.get(eddie_name, 0) or 0) < 2
            and eddie_talk_robbed_window(becky_var)
            and int(eddie_var.get("FingalTalk", 0) or 0) == 2
            and int(eddie_var.get("FingalTalkDestination", 0) or 0) == 0
        )

    def eddie_talk_can_complain(eddie_var, becky_var, eddie_name="eddie"):
        return (
            int(Friends.get(eddie_name, 0) or 0) >= 7
            and int(Talked.get(eddie_name, 0) or 0) < 2
            and eddie_talk_robbed_window(becky_var)
            and int(eddie_var.get("FingalTalk", 0) or 0) == 2
            and int(eddie_var.get("FingalTalkComplain", 0) or 0) == 0
        )

label InitEddieTalk:
    $ eddie_talk_init_state()
    return
