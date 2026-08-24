from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAMES = ("ViewIngaSex", "ArriveMode", "RandIngaFuck", "_becky_home_front_resume")


def test_becky_home_front_keeps_context_but_not_a_duplicate_menu_stage():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    for field in ("arrival_mode", "inga_scene_roll"):
        assert 'rooms.get(\"BeckyHomeFront\").state["%s"]' % field in runtime
    front = (ROOT / "game/Town/BeckyHomeFront.rpy").read_text(encoding="utf-8-sig")
    assert "inga_scene_stage" not in runtime
    assert "BeckyAdmit" not in runtime
    assert "while True:" not in front
    assert front.index('"Поделится с вдовой своим открытием"') < front.index('"Предложить подойти к парочке"')
    assert '"resume"' not in front
    assert "label BeckyHomeFrontMenu:" not in front
    assert "jump BeckyHomeFront" not in front
    for legacy_name in LEGACY_NAMES:
        assert legacy_name not in runtime


def test_becky_home_front_has_no_legacy_save_authority():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in LEGACY_NAMES:
        assert legacy_name not in migration
    assert 'globals().pop("BeckyAdmit", None)' in migration


def test_becky_home_flows_use_inga_as_pregnancy_owner():
    sources = "\n".join(
        (ROOT / relative_path).read_text(encoding="utf-8-sig")
        for relative_path in (
            "game/Town/BeckyHomeFront.rpy",
            "game/Town/BeckyHome.rpy",
        )
    )

    assert "pregnancy.setdefault" not in sources
    assert '$ pregnancy_check("inga"' in sources
    assert "Inga.ensure_story_defaults()" not in sources
    assert "Inga.acquaintance_stage" in sources
    assert "Inga.saw_lucas_sex" in sources


def test_becky_home_arrivals_have_one_live_label_not_duplicate_threads():
    home = (ROOT / "game/Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")
    runtime = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    init_becky = (ROOT / "game/NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")

    assert not (ROOT / "game/NPC/Girls/Becky/BeckyHomeEvents.rpy").exists()
    for retired in (
        "HomeVisitEntry",
        "HomeDanceArrival",
        "HomeDinnerBedroom",
        "HomeEddieBedroom",
        "story_becky_home_visit_0",
        "story_becky_home_from_dances_0",
        "story_becky_home_from_dinner_0",
        "story_becky_home_svalnyi_greh_0",
    ):
        assert retired not in runtime
    assert "HomeEnterCheckedDay" not in home + init_becky
    assert "becky_home_after_sex_text" not in home
    assert home.count("becky_home_restore_text()") >= 3
