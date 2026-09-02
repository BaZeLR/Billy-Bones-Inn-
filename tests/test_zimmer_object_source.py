from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_zimmer_has_own_data_info_and_explicit_state_owner():
    source = read_rel("game/NPC/Secondary/InitZimmer.rpy")

    assert "class ZimmerData(PeopleData):" in source
    assert "class ZimmerInfo(BaseNPC):" in source
    assert "define ZimmerStaticData = ZimmerData()" in source
    assert "default Zimmer = ZimmerInfo()" in source
    for field in (
        "horse_complaint_stage",
        "sherwood_story_stage",
        "robin_complaint_stage",
        "robin_investigation_day",
        "street_patrol_pass",
    ):
        assert f"self.{field} =" in source
    assert "self.var = {}" not in source
    assert "STORY_DEFAULTS = {" not in source
    assert "self.ensure_story_defaults()" not in source


def test_zimmer_uses_class_state_not_old_var_bridge():
    combined = "\n".join(
        [
            read_rel("game/NPC/Secondary/InitZimmer.rpy"),
            read_rel("game/NPC/Secondary/IntZimmerTalk.rpy"),
            read_rel("game/Utilities/Time/NextDay_TavernDaily.rpy"),
            read_rel("game/Utilities/General/Screens/stat.rpy"),
            read_rel("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy"),
        ]
    )

    assert "ZimmerVar" not in combined
    assert "Zimmer.var" not in combined
    assert "_zimmer_var" not in combined
    assert 'getattr(renpy.store, "Zimmer.var"' not in combined
    assert "getattr(renpy.store, 'Zimmer.var'" not in combined
    assert '_ensure_dict("Zimmer.var")' not in combined
    assert '"var": Zimmer.var' not in combined
    assert "Zimmer(var=" not in combined
    assert "ZimmerInfo(var=" not in combined
    assert "Zimmer.var.setdefault" not in combined


def test_zimmer_dialog_uses_explicit_properties_without_placeholder_events():
    init_source = read_rel("game/NPC/Secondary/InitZimmer.rpy")
    talk_source = read_rel("game/NPC/Secondary/IntZimmerTalk.rpy")

    assert "Zimmer.ensure_story_defaults()" not in talk_source
    assert "label IntZimmerTalkRefresh" not in talk_source
    assert "label IntZimmerTalkApply" not in talk_source
    assert 'str(choice_code or "")' not in talk_source
    assert "self.sherwood_story_stage = 0" in init_source
    assert "self.robin_complaint_stage = 0" in init_source
    assert "self.robin_investigation_day = 0" in init_source
    assert "MissionUpdatedByPlayer" not in init_source + talk_source
    assert "PlayerHandledRobin" not in init_source + talk_source
    assert "zimmer_guard_mission_update" not in init_source + talk_source


def test_zimmer_v54_migration_consumes_old_map_once():
    migration_source = read_rel("game/TractirSaveSync.rpy")
    migration = migration_source.split("def updateSave_V54():", 1)[1].split("label before_load:", 1)[0]
    for key in ("ComplainHorse", "SherwoodStory", "ComplainRobin", "RobinInvestigationDay", "street_pass"):
        assert f'zimmer_var.pop("{key}"' in migration
    assert 'globals().pop("ZimmerVar", None)' in migration
    assert "define currentVersion = 80" in migration_source
    assert "if loaded_version < 55:" in migration_source
