from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SANDRA_ROOM = (ROOT / "game/Inn/TavernSandraRoom.rpy").read_text(encoding="utf-8-sig")
PLAYER = (ROOT / "game/Utilities/General/Player/Player.rpy").read_text(encoding="utf-8-sig")
SAVE_SYNC = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


def _ledger_scene():
    return SANDRA_ROOM.split("label TavernSandraLedgerScene:", 1)[1]


def test_ledger_owns_the_native_weekly_premium_decision():
    scene = _ledger_scene()

    assert 'main_ui_begin_native_scene_state("Трактирные книги")' in scene
    assert "show screen main_ui" in scene
    assert '"Продолжить":' in scene
    assert "main_ui_end_native_scene_state()" in scene
    assert "for girl_id, info in people.girl_items()" in scene
    assert "if info.is_tavern_worker()" in scene
    assert "_tavern_team_keys" not in scene
    assert "while _premium_index" not in scene
    assert "Рассмотреть следующую кандидатуру" not in scene

    for amount in (25, 50, 100, 200, 500):
        assert '"Выдать по %d мараведи' % amount in scene
        assert "%d: (" % amount in SANDRA_ROOM


def test_premium_uses_one_evaluation_stamp_and_player_money_authority():
    scene = _ledger_scene()

    assert "weekly_chores_last_eval_stamp" in scene
    assert "team_premium_last_eval_stamp" in scene
    assert "player.spend_money(_premium_total)" in scene
    assert "player.spend_money(_premium_amount)" in scene
    assert "household_runtime_event_seen_today" not in scene
    assert "household_mark_runtime_event_seen" not in scene
    assert "calendar_v2.week" not in scene
    assert "player.chores.last_score" not in scene

    deferred = scene.split('"Вернуться к решению позже":', 1)[1].split('if _premium_decision == "declined":', 1)[0]
    assert "team_premium_last_eval_stamp" not in deferred


def test_team_and_personal_rewards_mutate_only_existing_owners():
    scene = _ledger_scene()

    assert '_premium_info.change_social(friend_delta=1)' in scene
    assert '_premium_info.reward_need_fulfilled(_premium_mana_gain, "team_premium")' in scene
    assert "_premium_info.change_skill(_premium_skill_key, _premium_skill_gain)" in scene
    assert "_premium_info.record_skill_gain(" in scene
    assert '_premium_person_info.change_social(friend_delta=1, corruption_delta=1)' in scene
    assert '_premium_person_info.reward_need_fulfilled(max(2, _premium_mana_gain), "personal_premium")' in scene
    assert ".corruption =" not in scene
    assert "willing" not in scene.lower()

    for job_key, skill_key in (
        ("jobkitchen", "cooking"),
        ("jobcleaning", "cleaning"),
        ("jobwaitress", "waitress"),
    ):
        assert '("%s", "%s")' % (job_key, skill_key) in SANDRA_ROOM
    skill_map = SANDRA_ROOM.split("TAVERN_TEAM_PREMIUM_JOB_SKILLS", 1)[1].split("init 6 python:", 1)[0]
    assert '"jobwhore"' not in skill_map


def test_premium_stamp_is_player_tavern_owned_and_old_markers_are_consumed_once():
    assert PLAYER.count('self.team_premium_last_eval_stamp = ""') == 1
    assert "define currentVersion = 89" in SAVE_SYNC
    assert "def updateSave_V89():" not in SAVE_SYNC

    repair = SAVE_SYNC.split("def tractir_save_patch_loaded_state():", 1)[1].split("def tractir_save_normalize_tavern_staff_jobs():", 1)[0]
    assert 'startswith("tavern_team_premium:")' in repair
    assert 'getattr(player.tavern_management, "weekly_chores_last_eval_stamp", "")' in repair
    assert "team_premium_last_eval_stamp" in repair
    assert "calendar_v2.day_number_to_parts(premium_marker_day)" in repair
    assert "calendar_v2.day_number_to_parts(max(0, premium_marker_day - 1))" in repair
    assert "old_premium_paid_for_eval" in repair
    assert "premium_event_seen.pop(event_key, None)" in repair
