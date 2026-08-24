from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_soap_batches_move_once_from_pending_work_to_inventory_on_new_day():
    soap = source("game/Items/Crafting/SoapCraftAndAtticItems.rpy")
    backyard = source("game/Inn/Backyard.rpy")
    new_day = source("game/Utilities/Time/NextDay_NewDayEvents.rpy")
    screens = source("game/Utilities/General/Screens/stat.rpy") + source(
        "game/Utilities/General/Screens/PlayerCard.rpy"
    )

    assert "def crafting_release_ready_soap_batches():" in soap
    assert "crafting.pending_soap_batches = remaining_pending" in soap
    assert "SoapAshBarrelReadyDay" not in soap + backyard
    assert "player.add_item(item_id, quantity)" in soap
    assert "stored_soap_batches" not in soap
    assert "soap_expire_day" not in soap
    assert "soap_sync_batches" not in soap + screens
    assert "sync_soap_batches_with_day" not in soap + screens
    assert "crafting_release_ready_soap_batches()" in new_day
