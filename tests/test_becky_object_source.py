from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
INIT = (GAME / "NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (GAME / "TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


def test_becky_personal_story_facts_are_explicit_object_properties():
    info = INIT.split("class BeckyInfo", 1)[1].split("define BeckyStaticData", 1)[0]
    for field in (
        "left_dances",
        "inga_sex_greeting_seen",
        "uninvited_visit_scolded",
        "home_front_checked_today",
        "sandra_kitchen_friendship_progress",
        "eddie_georgett_stage",
        "eddie_home_visit_state",
        "home_visit_count",
        "talked_about_eddie",
        "georgett_mentioned",
        "eddie_intervention_reaction",
        "priest_advice_stage",
        "gerhard_talk_stage",
        "asked_about_eddie_sex_stage",
        "eddie_join_failures",
        "eddie_robbed_day",
        "knows_blackwood",
        "sherwood_suspicion",
        "trade_offer_stage",
        "sherwood_warning_stage",
        "asked_about_elf_trade",
        "fingal_connection_clarified",
        "admitted_sherwood_stage",
        "robin_robbery_stage",
        "robbery_consolation_count",
    ):
        assert f"self.{field} =" in info

    for retired_stage in (
        "home_visit_stage",
        "home_sex_unlocked",
        "open_oral_stage",
        "eddie_join_stage",
    ):
        assert f"self.{retired_stage} =" not in info

    assert "def sandra_friendship_stage(self):" in info
    assert "self.sandra_kitchen_friendship_progress" in info
    assert "day_value > 70" not in info
    assert "self.sandra_kitchen_visit_period" not in info
    assert '"last_orgasm_day": -1' in info
    assert "self.last_store_orgasm_day" not in info

    assert "STORY_DEFAULTS = {" not in info
    assert "uses_own_var_state" not in info
    assert "self.var =" not in info
    assert "self.ensure_story_defaults()" not in info


def test_becky_authored_gift_preferences_include_furs_and_soap():
    data = INIT.split("class BeckyData", 1)[1].split("class BeckyInfo", 1)[0]

    for item_code in (
        "soap_001",
        "wolf_skin_001",
        "white_wolf_skin_001",
        "bear_fur_brown_001",
        "bear_fur_grizzly_001",
    ):
        assert f'"{item_code}"' in data


def test_live_runtime_has_no_becky_story_map_or_generic_map_access():
    live_source = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in GAME.rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    for retired_access in (
        "Becky.var",
        "Becky.story_value(",
        "Becky.set_story_value(",
        "Becky.set_story_value_min(",
        "Becky.var_int(",
        "Becky.set_var_int(",
        "Becky.add_var_int(",
        "_becky_var",
        "_becky_story",
        "BeckyVar",
    ):
        assert retired_access not in live_source


def test_v52_migrates_becky_map_once_and_every_load_does_not_clean_it():
    migration = MIGRATION.split("def updateSave_V52():", 1)[1].split("label before_load:", 1)[0]
    for key in (
        "leftdances",
        "visitedhome",
        "HomeSex",
        "EddieWhoreHome",
        "PriestAdvice",
        "EddieTryToFuck",
        "EddieRobbedDay",
        "KnowBlackwood",
        "SherwoodSuspect",
        "TradeOffer",
        "RobbedByRobin",
        "SandraKitchenVisitMonth",
        "last_store_orgasm_day",
    ):
        assert f'becky_var.pop("{key}"' in migration

    assert "Becky.sandra_kitchen_visit_period =" not in migration

    always_cleanup = MIGRATION.split("def tractir_save_clear_retired_npc_state():", 1)[1].split(
        "def tractir_save_normalize_sex_positions", 1
    )[0]
    assert "becky_var" not in always_cleanup
    assert "BeckyAdmit" not in always_cleanup
    assert "define currentVersion = 87" in MIGRATION
    assert "if loaded_version < 53:" in MIGRATION
    assert "updateSave_V52()" in MIGRATION


def test_v81_moves_retired_becky_stages_to_threads_and_deletes_mirrors():
    migration = MIGRATION.split("def updateSave_V81():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]

    for thread_name in ("beckyHome", "beckyDinner", "beckySex", "beckyEddieSex"):
        assert f'threads["{thread_name}"]' in migration
    for retired_stage in (
        "home_visit_stage",
        "home_sex_unlocked",
        "open_oral_stage",
        "eddie_join_stage",
    ):
        assert f'Becky.__dict__.pop("{retired_stage}", None)' in migration


def test_v84_repairs_becky_corruption_from_retired_church_purity_state():
    migration = MIGRATION.split("def updateSave_V84():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]

    assert 'purity_report.get("becky", None) is not None' in migration
    assert "Becky.corruption = max(25, people_to_int(Becky.corruption, 0))" in migration
    assert 'church_state.pop("purity_last_day", None)' in migration
    assert 'church_state.pop("purity_report", None)' in migration
    assert "if loaded_version < 85:" in MIGRATION
    assert "updateSave_V84()" in MIGRATION


def test_v85_adds_becky_sandra_visit_progress_to_existing_saves():
    migration = MIGRATION.split("def updateSave_V85():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]

    assert 'getattr(Becky, "sandra_kitchen_friendship_progress", 0)' in migration
    assert "Becky.sandra_kitchen_friendship_progress =" in migration
    assert "if loaded_version < 86:" in MIGRATION
    assert "updateSave_V85()" in MIGRATION


def test_v86_moves_becky_store_cooldown_to_generic_sex_stats():
    migration = MIGRATION.split("def updateSave_V86():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]

    assert 'Becky.sex_stat("last_orgasm_day", -1)' in migration
    assert 'Becky.set_sex_stat("last_orgasm_day", max(' in migration
    assert 'Becky.__dict__.pop("last_store_orgasm_day", None)' in migration
    assert "if loaded_version < 87:" in MIGRATION
    assert "updateSave_V86()" in MIGRATION
