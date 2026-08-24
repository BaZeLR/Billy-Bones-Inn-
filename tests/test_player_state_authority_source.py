from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PLAYER_SOURCE = ROOT / "game" / "Utilities" / "General" / "Player" / "Player.rpy"
PLAYER_CARD_SOURCE = ROOT / "game" / "Utilities" / "General" / "Screens" / "PlayerCard.rpy"
NEXT_DAY_SOURCE = ROOT / "game" / "Utilities" / "Time" / "NextDay.rpy"
SCRIPT_SOURCE = ROOT / "game" / "script.rpy"


def _function_body(source, function_name):
    match = re.search(
        rf"^(?P<indent> +)def {re.escape(function_name)}\([^\n]*\):\n(?P<body>(?:(?P=indent)    .*\n|\n)+)",
        source,
        re.MULTILINE,
    )
    assert match, f"missing function: {function_name}"
    return match.group(0)


def _function_bodies(source, function_name):
    pattern = re.compile(
        rf"^(?P<indent> +)def {re.escape(function_name)}\([^\n]*\):\n(?P<body>(?:(?P=indent)    .*\n|\n)+)",
        re.MULTILINE,
    )
    bodies = [match.group(0) for match in pattern.finditer(source)]
    assert bodies, f"missing function: {function_name}"
    return bodies


def test_player_state_compatibility_accessor_is_removed():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")
    assert "def player_state(" not in source
    assert "sync_player_state_from_store" not in source
    assert "sync_player_state_to_store" not in source


def test_player_card_reads_class_owned_state():
    source = PLAYER_CARD_SOURCE.read_text(encoding="utf-8")
    body = _function_body(source, "player_card_state")

    assert "return player" in body
    assert "player_state(" not in body


def test_after_load_store_promotion_is_removed():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")
    assert "player_after_load_init" not in source
    assert "config.after_load_callbacks" not in source


def test_next_day_cash_settlement_uses_player_economy():
    source = NEXT_DAY_SOURCE.read_text(encoding="utf-8")

    assert "player.add_money(_nextday_money_delta)" in source
    assert "player.spend_money(5)" in source
    assert not re.search(r"(?m)^\s*(?:\$\s*)?money\s*(?:\+=|-=|=(?!=))", source)


def test_money_has_no_scalar_store_authority():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")

    assert "default money =" not in script_source
    assert 'globals().get("money"' not in player_source
    assert 'globals()["money"]' not in player_source

    for function_name in ("add_money", "set_money", "spend_money"):
        for body in _function_bodies(player_source, function_name):
            assert "sync_from_store" not in body
            assert "apply_to_store" not in body


def test_condition_has_no_scalar_store_authority():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")

    for stat_name in ("health", "energy", "fun"):
        assert f"default {stat_name} =" not in script_source
        assert f'g.get("{stat_name}"' not in player_source
        assert f'g["{stat_name}"]' not in player_source

    change_body = _function_body(player_source, "change_stat")
    assert "self.sync_from_store()" not in change_body
    assert "self.condition.apply_to_store()" not in change_body


def test_inventory_has_no_store_mirror_or_compatibility_helpers():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "default playerItems =" not in script_source
    assert 'globals().get("playerItems"' not in player_source
    assert 'globals()["playerItems"]' not in player_source
    assert "_ensure_player_inventory_store" not in game_sources
    assert "_player_item_count_by_id" not in game_sources
    assert "_player_add_item_by_id" not in game_sources
    assert "_player_remove_item_by_id" not in game_sources
    assert "_player_has_item_by_id" not in game_sources


def test_equipment_has_no_scalar_store_authority():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "default EquippedWeapon =" not in script_source
    assert "default EquippedArmor =" not in script_source
    assert "EquippedWeapon" not in game_sources
    assert "EquippedArmor" not in game_sources
    assert 'globals().get("Equipped' not in player_source
    assert 'globals()["Equipped' not in player_source


def test_appearance_has_no_scalar_store_mirrors():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    legacy_names = (
        "washDays", "hairCutdays", "dayssincewash", "dayssincehaircut",
        "PlayerHaircutDaySt", "PlayerDressDaySt", "PlayerDressLifeDays",
        "PlayerDestroyedDresses", "PlayerItemLifeDays", "costumecondition",
    )

    for name in legacy_names:
        assert f"default {name} =" not in script_source
        assert f'g.get("{name}"' not in player_source
        assert f'g["{name}"]' not in player_source

    assert "appearance.sync_from_store()" not in player_source
    assert "appearance.apply_to_store()" not in player_source


def test_player_intimacy_has_no_scalar_or_had_sex_mirror():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    intimacy_source = (ROOT / "game/Utilities/General/Sex/PlayerIntimacyState.rpy").read_text(encoding="utf-8-sig")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    for name in ("cametoday", "cancumdaily", "LastDaySex", "PlayerLastCumDay"):
        assert f"default {name} =" not in script_source
        assert not re.search(rf"\b{re.escape(name)}\b", game_sources)

    assert 'HadSex.get("You"' not in game_sources
    assert 'HadSex["You"]' not in game_sources
    assert "intimacy.sync_from_store()" not in game_sources
    assert "intimacy.apply_to_store()" not in game_sources
    assert "people_display_name(key)" in intimacy_source
    assert "RealName.get(key" not in intimacy_source


def test_player_arousal_is_one_scalar_authority():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    player_card_source = PLAYER_CARD_SOURCE.read_text(encoding="utf-8-sig")
    migration_source = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "self.arousal = 0" in player_source
    assert "def arousal_value(self):" in player_source
    assert "def set_arousal(self, value):" in player_source
    assert "def add_arousal(self, amount=0, cap=100):" in player_source
    assert "def normalize_arousal(self):" not in player_source
    assert 'globals().pop("Arousal", None)' in migration_source
    assert 'saved_arousal.get("You", saved_arousal.get("you", 0))' in migration_source
    assert 'legacy_arousal.get("You", legacy_arousal.get("you", saved_arousal))' in migration_source
    assert 'player.intimacy.arousal = player_clamp_value(saved_arousal, 0, 100)' in migration_source
    assert 'self.arousal["You"]' not in game_sources
    assert 'self.arousal["you"]' not in game_sources
    assert '.arousal_value("You")' not in game_sources
    assert re.search(r"\.set_arousal\([^\n]*,\s*[\"']You[\"']\)", game_sources) is None
    assert re.search(r"\.add_arousal\([^\n]*,\s*[\"']You[\"']\)", game_sources) is None
    assert 'state.intimacy.arousal_value()' in player_card_source


def test_player_chores_have_one_weekly_state_map():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    legacy_names = (
        "PlayerChoresWeek", "UI_chores", "bring_woods", "chop_wood",
        "make_fire", "clean_ashes", "boil_water", "clean_upstairs_rooms",
    )

    for name in legacy_names:
        assert f"default {name} =" not in script_source
    assert "PlayerChoresWeek" not in game_sources
    assert "UI_chores" not in game_sources
    assert "_pc_sync_ui_chores" not in game_sources
    assert "self.ui =" not in player_source
    assert "self.counters =" not in player_source
    assert "chores.sync_from_store()" not in game_sources
    assert "chores.apply_to_store()" not in game_sources


def test_tavern_management_has_no_scalar_store_mirrors():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    legacy_names = (
        "productnum", "winenum", "taverncleanliness", "upstairsroomsdirty",
        "ashesdirtydays", "WeeklyVisitorsTrack",
    )

    for name in legacy_names:
        assert f"default {name} =" not in script_source
        assert f'g.get("{name}"' not in player_source
        assert f'g["{name}"]' not in player_source
    assert "tavern_management.sync_from_store()" not in player_source
    assert "tavern_management.apply_to_store()" not in player_source


def test_player_combat_has_no_party_level_or_supply_mirrors():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    for legacy_name in ("player_company", "company_list", "FightLevel", "PlayerFightSupply"):
        assert not re.search(rf"\b{legacy_name}\b", game_sources)
    assert 'g.get("player_company"' not in player_source
    assert 'g["player_company"]' not in player_source
    assert "combat.sync_from_store()" not in game_sources
    assert "combat.apply_to_store()" not in game_sources


def test_player_condition_has_no_sickness_or_forest_ban_mirrors():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    for legacy_name in ("SickDays", "PlayerForestBanUntilDay"):
        assert f"default {legacy_name} =" not in script_source
        assert not re.search(rf"\b{legacy_name}\b", game_sources)
    assert "def sync_from_store(" not in player_source
    assert "def apply_to_store(" not in player_source


def test_player_economy_has_no_fame_or_child_support_mirrors():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    for legacy_name in ("tavernfame", "KidsPosobie"):
        assert f"default {legacy_name}" not in script_source
        assert not re.search(rf"(?<![.\"'])\b{legacy_name}\b", game_sources)
    assert "def sync_from_store(" not in player_source
    assert "def apply_to_store(" not in player_source
    change_body = _function_body(player_source, "change_tavern_fame")
    assert "sync_from_store" not in change_body
    assert "apply_to_store" not in change_body


def test_player_identity_and_stats_have_no_store_sync_layer():
    player_source = PLAYER_SOURCE.read_text(encoding="utf-8")
    script_source = SCRIPT_SOURCE.read_text(encoding="utf-8")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    for legacy_name in ("age", "charisma", "reputation", "notoriety", "exploration", "rebellion", "look"):
        assert f"default {legacy_name} =" not in script_source
    assert "def sync_from_store(" not in player_source
    assert "def apply_to_store(" not in player_source
    assert "sync_player_state" not in game_sources
    assert "player_state(" not in game_sources
    assert "ensure_player_runtime(" not in game_sources
    assert "player.sync_from_store()" not in game_sources
    assert ".apply_to_store()" not in game_sources

    for stat_name in ("charisma", "reputation", "notoriety", "exploration", "rebellion", "look"):
        assert f'globals().get("{stat_name}"' not in game_sources


def test_progression_stats_have_no_bare_scalar_reads_or_writes():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    for stat_name in ("charisma", "reputation", "notoriety", "exploration", "look"):
        assert not re.search(
            rf"(?m)^\s*(?:\$\s*)?{stat_name}\s*(?:\+=|-=|=(?!=))",
            game_sources,
        )
        assert not re.search(rf"\bint\(\s*{stat_name}\b", game_sources)
        assert not re.search(rf"\bglobal\b[^\n]*\b{stat_name}\b", game_sources)


def test_exploration_owner_preserves_authored_high_progression_thresholds():
    source = PLAYER_SOURCE.read_text(encoding="utf-8")
    stats_source = source.split("class PlayerStats(object):", 1)[1].split("class PlayerEconomy(object):", 1)[0]
    condition_source = source.split("class PlayerCondition(object):", 1)[1].split("class PlayerStats(object):", 1)[0]

    assert 'if key == "exploration" and maximum == 100:' in stats_source
    assert "value = max(player_to_int(minimum, 0), raw_value)" in stats_source
    assert 'key == "exploration"' not in condition_source
    assert 'target is self.stats and key == "exploration" and maximum == 100' in source


def test_charisma_and_reputation_are_read_only_projections_of_owned_state():
    source = (ROOT / "game/Utilities/General/Screens/stat.rpy").read_text(
        encoding="utf-8-sig"
    )
    update_body = _function_body(source, "update_stat_state")

    assert "progression_value = _player_int(player.stats.charisma, 0)" in source
    assert "progression_value = _player_int(player.stats.reputation, 0)" in source
    assert "global look" not in update_body
    assert "global reputation" not in update_body
    assert "look =" not in update_body
    assert "reputation =" not in update_body


def test_derived_player_stats_do_not_hide_missing_runtime_owners():
    source = (ROOT / "game/Utilities/General/Screens/stat.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert source.count("except Exception:") == 1
    assert "if dog.owned:" in source
    assert 'if not rooms.get("Forest").is_first_visit():' in source
    assert "dog_bonus = 1 if dog.owned else 0" in source
    assert "appearance.HAIRCUT_FRESH_DAYS" in source
    assert "appearance.WASH_FRESH_DAYS" in source
