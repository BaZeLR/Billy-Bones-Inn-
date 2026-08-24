from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_irma_owns_explicit_story_state_without_legacy_map():
    source = (ROOT / "game/NPC/Girls/Irma/InitIrma.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "sync_irma_runtime" not in source
    assert "sync_irma_runtime_tables" not in source
    assert "RealName[name]" not in source
    assert "DateOfBirth[name]" not in source
    assert "dressdefault[name]" not in source
    assert "topdress[name]" not in source
    assert "self.ensure_story_defaults()" not in source
    assert "self.var =" not in source

    info_class = source.split("class IrmaInfo(Girl):", 1)[1]
    assert "STORY_DEFAULTS" not in info_class
    assert "def ensure_story_defaults(" not in info_class
    assert "def irma_story_defaults(" not in source
    for field_name in (
        "extra_fee_refused",
        "infertility_known",
        "father_story_known",
        "mother_story_known",
        "sexual_history_known",
    ):
        assert "self.%s =" % field_name in info_class


def test_irma_live_scenes_use_explicit_state_without_old_var_bridge():
    paths = (
        ROOT / "game/NPC/Girls/Irma/InitIrma.rpy",
        ROOT / "game/NPC/Girls/Irma/IrmaShortStories.rpy",
        ROOT / "game/NPC/Girls/Common/GirlSuggestDressFunc.rpy",
        ROOT / "game/Utilities/General/Clothes/DressTry.rpy",
    )
    combined = "\n".join(path.read_text(encoding="utf-8-sig") for path in paths)

    assert "Irma.var" not in combined
    assert "IrmaVar" not in combined
    assert "DeniedMinetMoney" not in combined
    assert "KnowInfertility" not in combined
    assert "KnowDad" not in combined
    assert "KnowMom" not in combined
    assert "KnowSlut" not in combined


def test_irma_v62_migration_consumes_old_map_once():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    block = migration.split("def updateSave_V62():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 69" in migration
    assert "if loaded_version < 63:" in migration
    assert "updateSave_V62()" in migration
    for old_key, field_name in (
        ("DeniedMinetMoney", "extra_fee_refused"),
        ("KnowInfertility", "infertility_known"),
        ("KnowDad", "father_story_known"),
        ("KnowMom", "mother_story_known"),
        ("KnowSlut", "sexual_history_known"),
    ):
        assert 'irma_var.pop("%s"' % old_key in block
        assert "Irma.%s =" % field_name in block
    assert 'globals().pop("IrmaVar", None)' in block


def test_irma_authored_scenes_use_native_menus_without_action_handlers():
    source = (ROOT / "game/NPC/Girls/Irma/IrmaTailorEvents.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "menu:" in source
    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert "label IrmaMeasureRoomStage" not in source
    assert "label IrmaMeasureEndScene" not in source
    assert "label IrmaMeasureRoomMenu(irma_measure_stage=0):" in source
    assert "label IrmaSexSequence(irma_sex_step=0):" in source
    assert "IrmaMeasureShopStage" not in source
    assert "IrmaSexShopStep" not in source
