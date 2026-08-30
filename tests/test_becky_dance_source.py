from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
FRIDAY_DANCE = ROOT / "game" / "Town" / "Market" / "FridayDance.rpy"
BECKY_DANCE_MODEL = ROOT / "game" / "NPC" / "Girls" / "Becky" / "BeckyDanceEventModel.rpy"
BECKY_INIT = ROOT / "game" / "NPC" / "Girls" / "Becky" / "InitBecky.rpy"
BECKY_DANCE = ROOT / "game" / "NPC" / "Girls" / "Becky" / "IntBeckyDance.rpy"
BECKY_INVITE = ROOT / "game" / "NPC" / "Girls" / "Becky" / "BeckyInviteHome.rpy"
TXT_REF = ROOT / "textLocRef" / "IntBeckyDance.txt"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def test_becky_friday_dance_uses_thread_event_and_object_state():
    runtime = _source(RUNTIME)
    friday = _source(FRIDAY_DANCE)
    model = _source(BECKY_DANCE_MODEL)
    init = _source(BECKY_INIT)
    dance = _source(BECKY_DANCE)
    invite = _source(BECKY_INVITE)

    assert 'LThreadData(0, "becky", "FridayDanceMC"' in runtime
    assert "BeckyFridayDanceMC" in runtime
    assert 'BeckyFridayDanceMC = BeckyDanceEvent(' in model
    assert 'call checkTriggers("FridayDance", "becky_dance_mc", 0)' in friday
    assert "call int_becky_dance" not in friday
    assert "BeckyVar" not in friday

    assert "class BeckyDanceEvent(Event):" in model
    assert "return bool(Becky.dance_event_conditions_met(self))" in model
    assert "def friday_dance_base_ready(self):" in init
    assert 'location_now == "FridayDance"' in init
    assert 'people_to_int(self.left_dances, 0) == 0' in init
    assert "def dance_event_conditions_met(self, event_obj):" in init

    assert "label story_becky_friday_dance_mc_0:" in dance
    assert 'rooms.get(\"FridayDance\").becky_home_invited = False' in dance
    assert dance.count('$ rooms.get(\"FridayDance\").dance_count += 1') == 1
    assert '$ rooms.get(\"FridayDance\").dance_count = 5' in dance
    assert 'rooms.get(\"FridayDance\").becky_home_invited' in dance
    assert 'call BeckyInviteHome("becky")' in dance
    assert "BeckyVar" not in dance
    assert "ensure_story_defaults" not in dance
    assert "sync_from_becky_maps" not in dance
    assert "sync_becky_maps" not in dance

    assert 'rooms.get(\"FridayDance\").becky_home_invited = True' in invite
    assert "player.appearance" not in invite
    assert "charisma" not in invite
    assert "danceinvitehome" not in dance
    assert "danceinvitehome" not in invite
    assert "BeckyVar" not in invite
    assert "setdefault" not in invite
    assert "Becky.update()" not in invite


def test_becky_dance_preserves_reference_choices():
    dance = _source(BECKY_DANCE)
    txt_ref = _source(TXT_REF)

    for choice in [
        "Осмотреть",
        "Поболтать",
        "Пригласить потанцевать",
        "Продолжить танцевать",
        "Положить руки на талию",
        "Положить руки на попу",
        "Сжать попу вдовы",
        "Поцеловать Бекки",
        "Принять предложение вдовы",
        "Отойти",
    ]:
        assert choice in txt_ref
        assert choice in dance
