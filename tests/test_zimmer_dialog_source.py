from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIMMER_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntZimmerTalk.rpy"
CITY_GUARD = ROOT / "game" / "Town" / "CityGuard.rpy"
CHARACTER_HUB = ROOT / "game" / "Utilities" / "General" / "NPC" / "CharacterActionHub.rpy"
ZIMMER_INIT = ROOT / "game" / "NPC" / "Secondary" / "InitZimmer.rpy"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_zimmer_dialogs_are_explicit_sublabels_not_dispatcher():
    source = _source(ZIMMER_TALK)

    assert "label IntZimmerTalkMenu:" not in source
    assert "while True:" in source
    assert "jump IntZimmerTalk" not in source
    assert "jump IntZimmerTalkMenu" not in source
    assert "menu:" in source
    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert "label IntZimmerTalkRefresh" not in source
    assert "label IntZimmerTalkApply" not in source
    assert 'str(choice_code or "")' not in source
    assert "Zimmer.var" not in source
    assert "_zimmer_var" not in source
    assert "ZimmerVar" not in source
    assert "renpy.random" not in source
    assert "CityGuardRestore" not in source
    assert "action_menu_specs" not in source
    assert "if _zimmer_talk_new:" in source

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


def test_city_guard_builds_canonical_actions_without_room_loop_label():
    source = _source(CITY_GUARD)
    zimmer_init = _source(ZIMMER_INIT)

    assert "label CityGuardBuildActions:" not in source
    assert "call CityGuardBuildActions" not in source
    assert 'Call("CityGuardShowPlacat")' in source
    assert 'Call("IntZimmerTalk")' not in source
    assert 'talk_label = "IntZimmerTalk"' in zimmer_init
    assert not CHARACTER_HUB.exists()
    assert 'Call("checkTriggers", "CityGuard", "enter", 0)' in source
    assert "rooms.get(\"CityGuard\").build_exit_items()" in source
    assert "calendar_v2.clock_minutes()" in source
    assert "int(clock_minutes or 0)" not in source


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
        "Спросить о покупке лошади",
        "Похвастаться вином для ночной стражи",
    ]:
        assert choice in source

    assert 'int(_clara_booklet_thread.num or 0) == 7' in source
    assert "not Mongol.guard_captain_known" in source
    assert "_mongol_var" not in source
    assert "Mongol.guard_captain_known = True" in source


def test_zimmer_horse_offer_uses_player_owned_resources_and_horse_state():
    source = _source(ZIMMER_TALK)
    purchase = source.split("label IntZimmerTalkHorsePurchase:", 1)[1].split(
        "label IntZimmerTalkMongolWineDistraction:", 1
    )[0]

    assert "define ZIMMER_HORSE_WINE_COST = 5" in source
    assert "define ZIMMER_HORSE_MONEY_COST = 500" in source
    assert "int(Luisa.horse_referral_stage or 0) > 0" in source
    assert "not player.horse.owns_horse()" in source
    assert 'str(player.appearance.current_dress or "") != "nobbledress"' in purchase
    assert "player.tavern_management.winenum - ZIMMER_HORSE_WINE_COST" in purchase
    assert "player.spend_money(ZIMMER_HORSE_MONEY_COST)" in purchase
    assert "player.horse.acquire(RandomStallionNameCode(), ZIMMER_HORSE_MONEY_COST, True)" in purchase
    assert 'jump TavernStable' not in purchase


def test_zimmer_dialog_uses_vscene_and_room_restore_end():
    source = _source(ZIMMER_TALK)

    assert 'vscene "images/zimmer/portrait1.png"' in source
    assert 'vscene "images/zimmer/talk.png"' in source
    assert '"Закончить разговор":' in source
    assert "$ main_ui_end_talk_state()" in source
    assert "jump CityGuard" not in source
