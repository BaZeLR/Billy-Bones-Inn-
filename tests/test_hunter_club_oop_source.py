from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_hunter_club_preserves_trade_reputation_and_challenges():
    hunter = source("game/Town/HunterClub.rpy")

    for challenge_id in ("wolf_skin", "boar_fang", "white_wolf", "bear_claw"):
        assert '"id": "%s"' % challenge_id in hunter
    assert 'rooms.get(\"HunterClub\").state["completed_challenges"] = completed' in hunter
    assert 'rooms.get(\"HunterClub\").state["reputation"] = hunter_club_reputation() + rep_gain' in hunter
    assert 'player.change_stat("reputation", rep_gain)' in hunter
    assert "player.spend_money(total_price)" in hunter
    assert "player.add_money(total_price)" in hunter
    assert "player.add_item(applied[\"item_id\"], applied[\"quantity\"])" in hunter
    assert "player.remove_item(applied[\"item_id\"], applied[\"quantity\"])" in hunter
    assert 'selection = rooms.get(\"HunterClub\").state.get("trade_selection", {})' in hunter
    assert 'isinstance(rooms.get(\"HunterClub\").state.get("trade_selection", {}), dict)' not in hunter


def test_hunter_club_room_has_no_menu_rebuild_wrappers_or_var_mirror():
    hunter = source("game/Town/HunterClub.rpy")

    assert "rooms.get(\"HunterClub\").build_action_items()" in hunter
    assert "label HunterClubBuildActions:" not in hunter
    assert "label HunterClubRestore:" not in hunter
    assert "label HunterClubResetTrade" not in hunter
    assert "HunterClubVar" not in hunter
    assert "hunter_club_buy_item" not in hunter
    assert "hunter_club_sell_item" not in hunter


def test_hunter_trade_catalog_uses_dedicated_shop_page_without_scrollbar():
    hunter = source("game/Town/HunterClub.rpy")
    buy_menu = hunter.split("label HunterClubBuyMenu:", 1)[1].split(
        "label HunterClubSellMenu:", 1
    )[0]
    sell_menu = hunter.split("label HunterClubSellMenu:", 1)[1].split(
        "label HunterClubApplyTrade", 1
    )[0]

    assert "screen hunter_club_trade_overlay():" in hunter
    assert "screen hunter_club_trade_panel():" not in hunter
    assert "viewport:" in hunter
    assert "vbar" not in hunter
    assert "show screen hunter_club_trade_overlay" in buy_menu
    assert "show screen hunter_club_trade_overlay" in sell_menu
    assert "$ main_ui_runtime.action_content = None" in buy_menu
    assert "$ main_ui_runtime.action_content = None" in sell_menu
    for caption in ("Подтвердить покупку", "Сбросить выбор", "Назад"):
        assert caption in buy_menu
    for caption in ("Подтвердить продажу", "Сбросить выбор", "Назад"):
        assert caption in sell_menu


def test_werecat_hunter_quest_is_authored_in_event_label():
    events = source("game/NPC/Girls/Melissa/MelissaEvents.rpy")
    quest = source("game/NPC/Secondary/MelissaWerecatQuest.rpy")
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    event_block = events.split("label story_melissa_werecat_rumor_0:", 1)[1].split(
        "label story_melissa_werecat_home_0:", 1
    )[0]

    assert '"story_melissa_werecat_rumor_0"' in runtime
    assert '"HunterClub"' in runtime
    assert '"overheard"' in runtime
    assert "vscene werecat_info_picture_path()" in event_block
    assert 'werecat_state()["hunter_tease_day"]' in event_block
    assert "thread.advance()" in event_block
    assert "jump HunterClub" not in event_block
    assert event_block.rstrip().endswith("return True")
    assert "call WerecatHunterClubTease" not in event_block
    assert "WerecatHunterClubTease" not in quest
    assert "hunter_tease_offer_ready" not in events + quest
