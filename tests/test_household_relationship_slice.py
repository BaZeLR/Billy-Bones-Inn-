from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"


GIRL_FILES = {
    "amanda": "Amanda/InitAmanda.rpy",
    "becky": "Becky/InitBecky.rpy",
    "clara": "Clara/InitClara.rpy",
    "georgett": "Georgett/InitGeorgett.rpy",
    "inga": "Inga/InitInga.rpy",
    "irma": "Irma/InitIrma.rpy",
    "liza": "Liza/InitLiza.rpy",
    "melissa": "Melissa/InitMelissa.rpy",
    "sandra": "Sandra/InitSandra.rpy",
}


def read(relative):
    return (GAME / relative).read_text(encoding="utf-8-sig")


def test_soap_preferences_have_one_immutable_owner_and_every_talk_menu_can_gift():
    for relative in GIRL_FILES.values():
        source = read("NPC/Girls/" + relative)
        assert 'gift_preferences=[' in source, relative
        data_block = source.split("class ", 1)[1].split("class ", 1)[0]
        assert '"soap_001"' in data_block, relative
        assert "self.gift_preferences" not in source, relative

    talk_sources = {
        "amanda": read("NPC/Girls/Amanda/IntAmandaTalk.rpy"),
        "becky": read("NPC/Girls/Becky/IntBeckyTalk.rpy"),
        "clara": read("NPC/Girls/Clara/IntClaraTalk.rpy"),
        "georgett": read("NPC/Girls/Georgett/IntGeorgettTalk.rpy"),
        "inga": read("NPC/Girls/Inga/IntIngaTalk.rpy"),
        "irma": read("NPC/Girls/Irma/IntIrmaTalk.rpy"),
        "liza": read("NPC/Girls/Liza/IntLizaTalk.rpy"),
        "melissa": read("NPC/Girls/Melissa/IntMelissaTalk.rpy"),
        "sandra": read("NPC/Girls/Sandra/IntSandraTalk.rpy"),
    }
    for girl, source in talk_sources.items():
        assert 'Подарить маленький подарок' in source, girl
    assert 'call ClaraGiveGift(girl_name, "soap_001")' in talk_sources["clara"]
    for girl in set(talk_sources) - {"clara"}:
        assert "PlayerCardGiftToFixedTargetMenu" in talk_sources[girl], girl

    runtime = read("Utilities/General/NPC/PeopleRuntime.rpy")
    migration = read("TractirSaveSync.rpy")
    assert "return list(data.gift_preferences or [])" in runtime
    assert 'person.__dict__.pop("gift_preferences", None)' in migration


def test_breakfast_attendance_is_household_rule_not_current_schedule_projection():
    source = read("Inn/menu_tavernstat.rpy")
    block = source.split("def household_breakfast_attendee_ids():", 1)[1].split(
        "def household_breakfast_absence_lines():", 1
    )[0]

    assert 'for npc_id in ("sandra", "melissa", "amanda")' in block
    assert 'household_morning_issue_type(npc_id) == ""' in block
    assert 'people.location("becky")' in block
    assert "people.ids_at" not in block


def test_sandra_and_melissa_share_one_intimacy_procedure_with_distinct_gates():
    engine = read("NPC/Girls/Melissa/IntMelissaSex.rpy")
    sandra_events = read("NPC/Girls/Sandra/SandraEvents.rpy")
    melissa_talk = read("NPC/Girls/Melissa/IntMelissaTalk.rpy")
    sandra_talk = read("NPC/Girls/Sandra/IntSandraTalk.rpy")

    assert engine.count("label HouseholdSexEngine(") == 1
    assert "label SandraSexEngine" not in sandra_events
    assert "label IntMelissaSex" not in engine
    assert 'if girl == "melissa":' in engine
    assert 'return bool(info.relationship_allows(action_code))' in engine
    assert 'if girl == "sandra":' in engine
    assert 'threads["sandraWeeklyEvaluation"].completed' in engine
    assert 'call HouseholdSexEngine("sandra", "TavernSandraRoom")' in sandra_events
    assert "call HouseholdSexEngine" in melissa_talk
    assert "call HouseholdSexEngine" in sandra_talk
    assert '"Попросить помочь рукой" if _hse_full_engine' in engine
    assert '"Попросить сделать минет" if _hse_full_engine' in engine
    assert '"Кончить в рот" if _hse_can_cum' in engine
    assert '"Кончить в киску" if _hse_can_cum' in engine
    assert '"Кончить в попку" if _hse_can_cum' in engine
    assert '"Кончить на грудь" if _hse_can_cum' in engine
    assert '"Кончить на лицо" if _hse_can_cum' in engine


def test_anal_finish_is_recorded_without_using_vaginal_conception_state():
    engine = read("NPC/Girls/Melissa/IntMelissaSex.rpy")
    pregnancy = read("NPC/Girls/Common/PregnancyCheck.rpy")

    assert '$ pregnancy_check(_hse_girl, "ass", 1, "Вы")' in engine
    assert "['inside', 'ass', 'mouth', 'tits', 'mouthface', 'face', 'outside']" in pregnancy
    assert "if cum_place == 'inside':" in pregnancy
    assert '"CumTarget": str(cum_place or "")' in pregnancy
    for finish in ('"Кончить в рот"', '"Кончить на грудь"', '"Кончить на лицо"', '"Кончить в киску"', '"Кончить в попку"'):
        assert finish in engine


def test_kitchen_respect_and_harassment_choices_use_existing_story_and_npc_owners():
    runtime = read("Utilities/General/Classes/StoryEventRuntime.rpy")
    sandra_events = read("NPC/Girls/Sandra/SandraEvents.rpy")
    discussion = read("NPC/Girls/Common/IntHarrassmentDiscuss.rpy")
    save_sync = read("TractirSaveSync.rpy")

    assert 'LThreadData(0, "sandra", "KitchenHouseholdRespect"' in runtime
    assert '"TavernKitchen",' in runtime
    assert '"enter",' in runtime
    assert "label story_sandra_kitchen_household_respect_0:" in sandra_events
    assert "$ event_runtime.active_thread.complete()" in sandra_events
    assert '"Выгнать наглого клиента" if _girl_unhappy:' in discussion
    assert '"Сказать, что вы обдумаете проблему" if _girl_unhappy:' in discussion
    assert '$ _girl_info.set_harass_instruction("notallow")' in discussion
    assert "$ player.change_tavern_fame(-1)" in discussion
    assert "kitchen_household_respect_seen" not in runtime + sandra_events + save_sync
