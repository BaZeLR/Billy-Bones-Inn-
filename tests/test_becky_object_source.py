from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
INIT = (GAME / "NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (GAME / "TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


def test_becky_personal_story_facts_are_explicit_object_properties():
    info = INIT.split("class BeckyInfo", 1)[1].split("define BeckyStaticData", 1)[0]
    for field in (
        "left_dances",
        "home_visit_stage",
        "inga_sex_greeting_seen",
        "uninvited_visit_scolded",
        "home_front_checked_today",
        "home_sex_unlocked",
        "eddie_georgett_stage",
        "eddie_home_visit_state",
        "open_oral_stage",
        "home_visit_count",
        "talked_about_eddie",
        "georgett_mentioned",
        "eddie_intervention_reaction",
        "priest_advice_stage",
        "gerhard_talk_stage",
        "asked_about_eddie_sex_stage",
        "eddie_join_stage",
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
        "sandra_kitchen_visit_period",
        "last_store_orgasm_day",
    ):
        assert f"self.{field} =" in info

    assert "STORY_DEFAULTS = {" not in info
    assert "uses_own_var_state" not in info
    assert "self.var =" not in info
    assert "self.ensure_story_defaults()" not in info


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

    always_cleanup = MIGRATION.split("def tractir_save_clear_retired_npc_state():", 1)[1].split(
        "def tractir_save_normalize_sex_positions", 1
    )[0]
    assert "becky_var" not in always_cleanup
    assert "BeckyAdmit" not in always_cleanup
    assert "define currentVersion = 74" in MIGRATION
    assert "if loaded_version < 53:" in MIGRATION
    assert "updateSave_V52()" in MIGRATION
