from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "game/NPC/Secondary/IntAlberTalk.rpy").read_text(encoding="utf-8")
INIT = (ROOT / "game/NPC/Secondary/InitAlber.rpy").read_text(encoding="utf-8")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8")


def test_alber_owns_explicit_story_state_without_generic_map():
    info_class = INIT.split("class AlberInfo(BaseNPC):", 1)[1]

    assert "STORY_DEFAULTS" not in info_class
    assert "uses_own_var_state" not in info_class
    assert "self.var =" not in info_class
    assert "ensure_story_defaults" not in info_class
    assert "whore_visit_frequency = 3" in info_class
    for field_name in (
        "liza_encounter_seen", "talked_about_liza", "heard_about_wife",
        "amanda_conflict_stage",
    ):
        assert "self.%s =" % field_name in info_class


def test_alber_talk_has_one_native_menu_source_without_dispatch_layers():
    assert "label IntAlberTalkMenu:" not in SOURCE
    assert "while True:" in SOURCE
    assert "jump IntAlberTalkMenu" not in SOURCE
    assert "menu:" in SOURCE
    assert "def int_alber_talk_action_items():" not in SOURCE
    assert "label IntAlberTalkApply" not in SOURCE
    assert "main_ui_runtime.action_items" not in SOURCE
    assert "label IntAlberTalkRefresh:" not in SOURCE
    assert "call IntAlberTalkRefresh" not in SOURCE
    assert "if _alber_talk_new:" in SOURCE
    assert 'jump IntAlberTalk' not in SOURCE


def test_alber_talk_preserves_all_authored_choices():
    for choice in (
        "Поболтать со мессиром Легаре о разной всячине.",
        "Поболтать с мессиром Легаре о более личных вещах",
        "Спросить мессира Легаре о Лизетте",
        "Попробовать помириться",
        "Проигнорировать",
        "Обругать месье",
        "Заехать с правой",
        "Закончить разговор",
    ):
        assert '"%s"' % choice in SOURCE
    assert "Alber.finish_talk()" in SOURCE
    assert "$ main_ui_end_talk_state()" in SOURCE
    assert '$ apply_movement_time(5, "MarketPlace")' in SOURCE
    assert "jump MarketPlace" in SOURCE


def test_alber_provocation_is_label_local_not_persistent_npc_state():
    assert '$ _alber_provoked = 0' in SOURCE
    assert '$ _alber_provoked = 1' in SOURCE
    assert 'Alber.set_var_int("LegareProvokeYou"' not in SOURCE
    assert 'Alber.var_int("LegareProvokeYou"' not in SOURCE
    assert "self.LegareProvokeYou" not in INIT


def test_alber_v56_migration_consumes_old_map_and_scalar_once():
    block = MIGRATION.split("def updateSave_V56():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 81" in MIGRATION
    assert "if loaded_version < 57:" in MIGRATION
    assert "updateSave_V56()" in MIGRATION
    for old_key, field_name in (
        ("sawwithliza", "liza_encounter_seen"),
        ("talkedaboutliza", "talked_about_liza"),
        ("hearabouthiswife", "heard_about_wife"),
        ("FightYouAmanda", "amanda_conflict_stage"),
    ):
        assert 'alber_var.pop("%s"' % old_key in block
        assert "Alber.%s =" % field_name in block
    assert 'alber_var.pop("WhoreVisitFreq", None)' in block
    assert 'alber_var.pop("LegareProvokeYou", None)' in block
    assert 'globals().pop("LegareProvokeYou", None)' in block
    assert 'globals().pop("AlberVar", None)' in block
