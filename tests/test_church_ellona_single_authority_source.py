from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_church_donations_are_owned_by_player_economy():
    player = source("game/Utilities/General/Player/Player.rpy")
    church = source("game/Town/Church/ShowChurchDraupnirList.rpy")
    definitions = source("game/Utilities/General/Scripts/CreateDonationsList.rpy")
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert "self.church_repairs_donated = [0] * 10" in player
    assert "def record_church_donation(" in player
    assert "CHURCH_REPAIR_DESCRIPTIONS" in definitions
    assert "player.economy.church_repair_is_donated" in church
    assert "player.economy.record_church_donation" in church
    for retired in (
        "ChurchRepairDesc",
        "ChurchRepairCost",
        "ChurchRepairDonat",
        "ChurchDonatedAmount",
        "SawDraupnirChurchList",
    ):
        assert retired not in runtime


def test_ellona_blessing_and_curse_state_is_owned_by_player_intimacy():
    player = source("game/Utilities/General/Player/Player.rpy")
    prayer = source("game/Town/Temple/EllonaBirthPrayMenu.rpy")
    next_day = source("game/Utilities/Time/NextDay.rpy")
    finish_day = source("game/Utilities/Time/NextDay_FinishDayEvents.rpy")
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    for method in (
        "grant_ellona_grace",
        "grant_ellona_blessing",
        "apply_ellona_curse",
        "extend_ellona_curse",
        "lift_ellona_curse",
    ):
        assert "def %s(" % method in player
    assert "player.intimacy.grant_ellona_grace" in prayer
    assert "player.intimacy.apply_ellona_curse(14)" in prayer
    assert "player.intimacy.lift_ellona_curse()" in next_day
    assert "player.intimacy.ellona_curse_days -= 1" in finish_day
    for retired in ("GraceBlessing", "BlessedByEllona", "CursedByEllona"):
        assert retired not in runtime


def test_birth_prayer_flow_does_not_recurse_through_call_stack():
    prayer = source("game/Town/Temple/EllonaBirthPrayMenu.rpy")
    birth = source("game/Town/Temple/GiveBirthStep2.rpy")

    assert "call GiveBirthStep2" not in prayer
    assert "jump GiveBirthStep2" not in prayer
    assert "jump EllonaBirthPrayMenu" not in birth
    assert "call EllonaBirthPrayMenu(girl_name)" in birth
    assert "return 2" in prayer
    assert "$ give_birth_timer += int(_return or 0)" in birth
    assert "while True:" in birth


def test_sunday_tavern_rollover_assigns_zero_visitors_and_uses_direct_dog_api():
    source_text = source("game/Utilities/Time/NextDay_TavernDaily.rpy")

    assert "CurDay['visitors'] = 0" in source_text
    assert "CurDay['visitors'] == 0" not in source_text
    assert "record_weekly_tavern_visitors(CurDay['visitors'])" in source_text
    assert 'if dog.prevents_theft("horse"):' in source_text
    assert "callable(record_weekly_tavern_visitors)" not in source_text
    assert "_dog_catch_apply" not in source_text
