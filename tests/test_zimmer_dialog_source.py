    assert "CityGuardBuildActions" not in source    assert "CityGuardBuildActions" not in source    assert "CityGuardBuildActions" not in sourcefrom pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIMMER_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntZimmerTalk.rpy"
CITY_GUARD = ROOT / "game" / "Town" / "CityGuard.rpy"
CITY_GUARD = ROOT / "game" / "Town" / "CityGuard.rpy"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_zimmer_dialogs_are_explicit_sublabels_not_dispatcher():
    source = _source(ZIMMER_TALK)

    assert "label IntZimmerTalkRefresh" not in source
    assert "label IntZimmerTalkApply" not in source
    assert 'str(choice_code or "")' not in source
    assert "Zimmer.var" in source
    assert "ZimmerVar" not in source
    assert "renpy.random" not in source
    assert "CityGuardRestore" not in source
    assert "action_menu_specs" not in source

    for label in [
        "label IntZimmerTalkLook:",
        "label IntZimmerTalkHorseReport:",
        "label IntZimmerTalkHorseProgress:",
        "label IntZimmerTalkSherwoodStory1:",
        "label IntZimmerTalkSherwoodStory2:",
        "label IntZimmerTalkRobinReport:",
        "label IntZimmerTalkPay100:",
        "label IntZimmerTalkHaggle:",
        "label IntZimmerTalkInvestigation:",
        "label IntZimmerTalkMongolWineDistraction:",
    ]:
        assert label in source


def test_city_guard_builds_real_actions_inline_without_room_loop_wrapper():
    source = _source(CITY_GUARD)

    assert "label CityGuardBuildActions:" not in source
    assert "call CityGuardBuildActions" not in source
    assert 'Call("CityGuardShowPlacat")' in source
    assert 'Call("IntZimmerTalk")' in source
    assert 'Call("checkTriggers", "CityGuard", "enter", 0)' in source
    assert "CityGuardRoom.build_exit_items()" in source


def test_city_guard_builds_real_actions_inline_without_room_loop_wrapper():
    source = _source(CITY_GUARD)

    assert "label CityGuardBuildActions:" not in source
    assert "call CityGuardBuildActions" not in source
    assert 'Call("CityGuardShowPlacat")' in source
    assert 'Call("IntZimmerTalk")' in source
    assert 'Call("checkTriggers", "CityGuard", "enter", 0)' in source
    assert "CityGuardRoom.build_exit_items()" in source


def test_zimmer_dialog_menu_has_reference_choices_and_mongol_distraction():
    source = _source(ZIMMER_TALK)

    for choice in [
        "Посмотреть на десятника",
        "Сообщить о краже лошади",
        "Узнать, как продвигаются поиски украденной лошади",
        "Спросить о Шервудском лесе",
        "И что с лесом теперь?",
        "Пожаловаться на Робин Гуда",
        "Отдать сотню мараведи",
        "Поторговаться",
        "Узнать как там расследование",
        "Похвастаться вином для ночной стражи",
    ]:
        assert choice in source

    assert 'int(_mongol_var.get("StocksSeen", 0) or 0) == 1' in source
    assert 'int(_mongol_var.get("StocksFoodDay", -1)) >= 0' in source
    assert '_mongol_var["GuardCaptainKnown"] = 1' in source


def test_zimmer_dialog_uses_vscene_and_room_restore_end():
    source = _source(ZIMMER_TALK)

    assert 'vscene "images/zimmer/Portrait1.jpg"' in source
    assert 'vscene "images/zimmer/Talk.jpg"' in source
    assert 'MenuItem("Закончить разговор", Function(main_ui_end_talk_state))' in source
    assert "jump CityGuard" not in source
