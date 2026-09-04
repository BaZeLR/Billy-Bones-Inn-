from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SAVE_SYNC = GAME / "TractirSaveSync.rpy"


def test_npc_sex_state_is_the_single_busy_owner():
    people = (GAME / "Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
    becky = (GAME / "NPC/Girls/Becky/IntBeckySex.rpy").read_text(encoding="utf-8-sig")
    eddie = (GAME / "NPC/Secondary/IntEddieBeckySex.rpy").read_text(encoding="utf-8-sig")
    melissa = (GAME / "NPC/Girls/Melissa/IntMelissaSex.rpy").read_text(encoding="utf-8-sig")
    amanda = (GAME / "NPC/Girls/Amanda/IntAmandaSex.rpy").read_text(encoding="utf-8-sig")
    reset_daily = people.split("def reset_daily(self, full=False):", 1)[1].split("def getLocation", 1)[0]
    amanda_entry = amanda.split('label IntAmandaSex(GirlNameASDS="amanda", GirlLocASDS="home", GirlModeASDS=""):', 1)[1].split("label int_amanda_sex_menu:", 1)[0]
    household_entry = melissa.split('label HouseholdSexEngine(girl_name="melissa", source_room="", initial_action="sex"):', 1)[1].split("label household_sex_menu:", 1)[0]

    assert 'self.sex_state.setdefault("somebody_cums", 0)' in people
    assert "def sex_busy(self):" in people
    assert "def set_sex_busy(self, value):" in people
    assert "self.set_sex_busy(False)" in people
    assert "Becky.sex_busy()" in becky
    assert "Becky.set_sex_busy(True)" in becky
    assert "Becky.set_sex_busy(False)" in becky
    assert "Becky.sex_busy()" in eddie
    assert "_hse_info.sex_busy()" in melissa
    assert "_hse_info.set_sex_busy(True)" in melissa
    assert "_hse_info.set_sex_busy(False)" in melissa
    assert "self.set_sex_busy(False)" in reset_daily
    assert "Amanda.set_sex_busy(False)" in amanda_entry
    assert "_hse_info.set_sex_busy(False)" in household_entry


def test_retired_shared_sex_busy_flag_is_migration_only():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in GAME.rglob("*.rpy")
        if path != SAVE_SYNC
    )
    migration = SAVE_SYNC.read_text(encoding="utf-8-sig")

    assert "SomebodyCums" not in runtime
    assert 'globals().pop("SomebodyCums", None)' in migration
