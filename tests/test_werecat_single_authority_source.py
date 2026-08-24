from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_werecat_state_is_not_copied_into_people_profile():
    werecat = (ROOT / "game/NPC/Secondary/WerecatNPC.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "werecat_sync_profile" not in game_sources
    assert "info.known =" not in werecat
    assert "info.location =" not in werecat
    assert "def werecat_display_name():" in game_sources
    assert "def werecat_is_in_room(" in werecat


def test_werecat_is_a_registered_singleton_without_live_repairs():
    source = (ROOT / "game/NPC/Secondary/WerecatNPC.rpy").read_text(encoding="utf-8-sig")
    people = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert "class WerecatInfo(BaseNPC):" in source
    assert "define WerecatStaticData = PeopleData(" in source
    assert "default werecat = WerecatInfo()" in source
    assert "label InitWerecat:" in source
    assert "def werecat_info()" not in source
    assert "return werecat.var" in source
    assert "return werecat.stats" in source
    assert "call InitWerecat" in people
    assert "def tractir_save_promote_werecat():" not in migration
    assert "people.register(WerecatStaticData, werecat)" in source
    assert 'getattr(werecat_obj, "state", None)' not in migration


def test_werecat_adoption_and_gift_have_one_owner_and_direct_menu_outcomes():
    quest = (ROOT / "game/NPC/Secondary/MelissaWerecatQuest.rpy").read_text(
        encoding="utf-8-sig"
    )
    clara = (ROOT / "game/NPC/Girls/Clara/InitClara.rpy").read_text(
        encoding="utf-8-sig"
    )
    adopted_count = quest.split("def werecat_adopted_count():", 1)[1].split(
        "def werecat_first_home_exists", 1
    )[0]

    assert 'werecat_state()["adopted_count"] =' not in adopted_count
    assert "werecat_gifted" not in clara
    assert "werecat_gift_day" not in clara
    assert "WerecatAdoptChoice" not in quest
    assert '"Забрать ее домой":' in quest
    assert '"Продать работорговцам за 5000":' in quest


def test_werecat_traps_use_only_the_per_room_map():
    quest = (ROOT / "game/NPC/Secondary/MelissaWerecatQuest.rpy").read_text(
        encoding="utf-8-sig"
    )
    model = (ROOT / "game/NPC/Secondary/WerecatNPC.rpy").read_text(
        encoding="utf-8-sig"
    )
    trap_reader = quest.split("def werecat_trap_rooms():", 1)[1].split(
        "def werecat_can_set_bait", 1
    )[0]

    assert '"trap_rooms": {}' in model
    assert '"trap_active"' not in model
    assert '"trap_room"' not in model
    assert '"trap_day"' not in model
    assert "werecat_state()[" not in trap_reader
    assert "return dict(trap_rows or {})" in trap_reader
    assert "isinstance(trap_rows, dict)" not in trap_reader


def test_werecat_roaming_has_one_daily_schedule_definition():
    source = (ROOT / "game/NPC/Secondary/WerecatNPC.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "WerecatStaticData.set_daily_schedule(" in source
    assert 'npc_schedule_set("werecat"' not in source
    assert "WERECAT_ROAM_ROOMS" not in source
    assert "WERECAT_ROAM_CONDITIONS" not in source
    assert "def werecat_roam_location(" not in source
    assert "def werecat_schedule_" not in source
