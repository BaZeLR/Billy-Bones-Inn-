from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PEOPLE = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8")
PLAYER = (ROOT / "game/Utilities/General/Player/Player.rpy").read_text(encoding="utf-8")
NARRATOR = (ROOT / "game/Utilities/General/Common/NarratorRuntime.rpy").read_text(encoding="utf-8")
BREAKFAST = (ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8")
INVITE = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8")
DISCUSS = (ROOT / "game/NPC/Girls/Common/IntHarrassmentDiscuss.rpy").read_text(encoding="utf-8")
EVENTS = (ROOT / "game/Inn/TavernRandomEvents.rpy").read_text(encoding="utf-8")
DECISIONS = (ROOT / "game/Utilities/General/NPC/GirlDecisionModel.rpy").read_text(encoding="utf-8")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8")


def test_dialogue_characters_read_canonical_names_and_exclude_pets():
    assert "def character(self):" in PEOPLE and "Character(self.display_name()" in PEOPLE
    assert 'self.name in ("dog", "werecat")' in PEOPLE
    assert "Character(self.display_name," in PLAYER
    assert '"Рассказчик"' in NARRATOR and "who_color=" in NARRATOR
    for npc_id in ("sandra", "melissa", "amanda", "georgett", "liza", "clara"):
        assert '"%s": "#' % npc_id in PEOPLE


def test_hiring_defers_both_shifts_until_the_once_only_announcement():
    invite = INVITE.split("label IntGeorgettInviteTavern", 1)[1].split("label IntGeorgettAskWork", 1)[0]
    welcome = BREAKFAST.split("label TavernKitchenBreakfastAnnounceGeorgetteLiza:", 1)[1].split("label TavernKitchenBreakfastDanceMenu:", 1)[0]
    for name in ("Georgett", "Liza"):
        assert '%s.assign_tavern_service("", False)' % name in invite
        assert '%s.assign_tavern_service("", True)' % name in invite
        assert '%s.assign_tavern_service("intimate", False)' % name in welcome
        assert '%s.assign_tavern_service("intimate", True)' % name in welcome
    assert BREAKFAST.index("call TavernKitchenBreakfastAnnounceGeorgetteLiza") < BREAKFAST.index('call checkTriggers("TavernKitchen", "breakfast", 0)')
    assert '"Объявить о Жоржетте и Лизетте" if' not in BREAKFAST
    assert welcome.index('player.tavern_management.breakfast.georgett_liza_pending = 0') > welcome.index('"Продолжить завтрак"')


def test_house_rule_keeps_reports_and_each_workers_choice():
    welcome = BREAKFAST.split("label TavernKitchenBreakfastAnnounceGeorgetteLiza:", 1)[1].split("label TavernKitchenBreakfastDanceMenu:", 1)[0]
    assert 'tavern.client_touch_policy = "hands_off"' in welcome
    assert 'girl_info.set_harass_instruction("notallow")' in welcome
    assert 'renpy.say(Georgett.character' in welcome
    assert 'renpy.say(Liza.character' in welcome
    assert 'зовите меня или Сандру' in welcome
    assert 'tavern.client_touch_policy != "hands_off"' in DISCUSS
    assert '_girl_info.decide("customer_touch")' in DISCUSS
    assert '"customer_referral": {' in DECISIONS
    referral = EVENTS.split("label event_tavern_client_referral(eyewitness=0):", 1)[1]
    assert 'people.get_info(_referral_source).decide("customer_referral")' in referral
    assert 'if _referral_decision["reaction"] not in ("good", "capricious_bad_is_good"):' in referral
    assert 'define currentVersion = 113' in MIGRATION
    assert 'def updateSave_V112():' in MIGRATION
