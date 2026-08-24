from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "game/Town/Arts/BarberShop.rpy").read_text(encoding="utf-8-sig")


def test_barber_services_belong_to_sergio_talk_not_the_room_menu():
    assert "def barber_shop_action_items():" not in SOURCE
    assert "label BarberShopBuildActions:" not in SOURCE
    assert "call BarberShopBuildActions" not in SOURCE
    assert "BarberShopSavedText" not in SOURCE
    assert SOURCE.count("while True:") == 3
    assert SOURCE.count("call screen main_ui") == 2
    assert 'main_ui_begin_talk_state("Разговор с Серджио", "sergio")' in SOURCE
    assert "rooms.get(\"BarberShop\").build_exit_items()" in SOURCE


def test_barber_shop_preserves_services_event_and_oop_owners():
    for label in (
        "BarberShopHaircut", "BarberShopBuyOliveOil", "BarberShopRefineLuxurySoap",
        "BarberShopSellLuxurySoap", "BarberShopServePendingGuest",
    ):
        assert f"call {label}" in SOURCE
    assert 'story_event_available("BarberShop", "clara_fiance")' in SOURCE
    assert 'call checkTriggers("BarberShop", "clara_fiance", 0)' in SOURCE
    assert "player.economy.money" in SOURCE
    assert "player.appearance.mark_haircut" in SOURCE
    assert "player.add_item(" in SOURCE
    assert "player.remove_item(" in SOURCE
    assert "player.economy.tavern_fame" in SOURCE
    assert "BarberInvitePending" not in SOURCE
    assert '_barber_guest_info.set_var_int("barber_invite_pending", 0)' in SOURCE


def test_barber_event_gate_continues_to_the_room_interaction_owner():
    event_gate = SOURCE.split('if story_event_available("BarberShop", "clara_fiance"):', 1)[1].split("if not rooms.get(\"BarberShop\").is_open():", 1)[0]

    assert 'call checkTriggers("BarberShop", "clara_fiance", 0)' in event_gate
    assert "call screen main_ui" not in event_gate
    assert "jump BarberShop" not in event_gate
