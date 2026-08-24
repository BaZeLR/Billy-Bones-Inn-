from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "game/NPC/Girls/Inga/InitInga.rpy").read_text(encoding="utf-8-sig")
BECKY = (ROOT / "game/NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")
PEOPLE_RUNTIME = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


def test_inga_data_object_owns_its_hourly_schedule():
    data_class = SOURCE.split("class IngaData(PeopleData):", 1)[1]
    data_class = data_class.split("class IngaInfo(Girl):", 1)[0]
    init_label = SOURCE.split("label InitInga:", 1)[1].split("init python:", 1)[0]

    assert "schedule_entries=[" in data_class
    assert "start_hour=" in data_class
    assert "end_hour=" in data_class
    assert "calendar_v2.time_slot()" not in data_class
    assert "npc_schedule_set" not in init_label


def test_inga_owns_personal_story_facts_as_explicit_properties():
    info_class = SOURCE.split("class IngaInfo(Girl):", 1)[1]
    init_label = SOURCE.split("label InitInga:", 1)[1].split("init python:", 1)[0]

    assert "self.saw_lucas_sex = False" in info_class
    assert "self.acquaintance_stage = 0" in info_class
    assert "STORY_DEFAULTS = {" not in info_class
    assert "self.ensure_story_defaults()" not in info_class
    assert 'registry_group = "secondary"' in info_class
    assert "SECONDARY_NPC_KEYS" not in SOURCE
    assert "people.register(IngaStaticData, Inga)" in init_label
    for retired_call in ("set_sex_stat", "set_skill", "set_job_value", "set_story_value"):
        assert retired_call not in init_label


def test_inga_class_owns_new_game_body_skill_and_job_defaults():
    info_class = SOURCE.split("class IngaInfo(Girl):", 1)[1]
    for source_line in (
        'self.corruption = 30',
        '"beauty": 55',
        '"sexacts": 134',
        '"cuminside": 42',
        '"ConceptionChance": 10',
        '"PussyWetStart": 25',
        '"cooking": 40',
        '"cleaning": 20',
        '"waitress": 40',
        '"jobWhoreAvail": 0',
    ):
        assert source_line in info_class


def test_live_runtime_has_no_inga_story_map_access():
    live_source = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    for retired_access in (
        "Inga.var",
        "Inga.story_value(",
        "Inga.set_story_value(",
        "Inga.set_story_value_min(",
        "Inga.var_int(",
        "Inga.set_var_int(",
        "Inga.ensure_story_defaults()",
        "IngaVar",
    ):
        assert retired_access not in live_source


def test_v53_migrates_inga_map_once():
    migration = MIGRATION.split("def updateSave_V53():", 1)[1].split("label before_load:", 1)[0]
    assert 'inga_var.pop("SawLucassex"' in migration
    assert 'inga_var.pop("Knowher"' in migration
    assert 'globals().pop("IngaVar", None)' in migration
    assert "if loaded_version < 54:" in MIGRATION
    assert "updateSave_V53()" in MIGRATION
    assert "define currentVersion = 69" in MIGRATION


def test_becky_daily_reset_extends_base_without_repeating_base_fields():
    reset = BECKY.split("def reset_daily(self, full=False):", 1)[1]
    reset = reset.split("def add_corruption", 1)[0]

    assert "super(BeckyInfo, self).reset_daily(full)" in reset
    assert "self.home_front_checked_today = False" in reset
    assert "after_sermon_stage" not in reset
    for field in ("talked_today", "flirted_today", "gifted_today", "asked_today", "fucked_today", "drunk"):
        assert "self.%s = 0" % field not in reset


def test_becky_uses_inherited_change_social_without_identity_override():
    info_class = BECKY.split("class BeckyInfo(Girl):", 1)[1]

    assert "def change_social(" not in info_class


def test_becky_inherits_common_state_methods_and_keeps_only_becky_behavior():
    info_class = BECKY.split("class BeckyInfo(Girl):", 1)[1]

    assert "STORY_DEFAULTS = {" not in info_class
    assert "uses_own_var_state" not in info_class
    assert "self.ensure_story_defaults()" not in info_class
    for method in (
        "ensure_story_defaults",
        "story_value",
        "set_story_value",
        "add_story_value",
        "pregnancy_days",
        "record_orgasm_given",
        "apply_pregnancy_check",
        "has_panties",
    ):
        assert "def %s(" % method not in info_class
