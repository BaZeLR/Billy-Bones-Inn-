from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Inn/HouseholdRuntimeEvents.rpy"


def _label_block(source, label_name, next_label):
    return source.split(f"label {label_name}", 1)[1].split(f"label {next_label}", 1)[0]


def test_household_authored_requests_use_native_label_menus():
    source = SOURCE.read_text(encoding="utf-8-sig")
    slices = (
        ("HouseholdSoapRequestEvent", "HouseholdSoapRequestGiveNow"),
        ("HouseholdSoapRequestFulfillMenu", "HouseholdBarberRequestEvent"),
        ("HouseholdBarberRequestEvent", "HouseholdOutfitRequestTerms"),
        ("HouseholdOutfitRequestTerms", "SandraDressInitiativeEvent"),
        ("HouseholdOutfitRewardEvent", "HouseholdOutfitRewardShowScene"),
        ("HouseholdOutfitRewardShowScene", "HouseholdOutfitRewardHandjobScene"),
        ("HouseholdOutfitRewardHandjobScene", "HouseholdOutfitRewardOralScene"),
        ("HouseholdOutfitRewardOralScene", "TavernStorageRatEvent"),
    )

    for label_name, next_label in slices:
        block = _label_block(source, label_name, next_label)
        assert "\n    menu:\n" in block
        assert "QueuePagedPanelText" not in block
        assert "ReturnToMainUI" not in block
        assert "MenuItem(" not in block

    for girl_name, label_name, next_label in (
        ("sandra", "SandraDressInitiativeEvent", "MelissaDressRequestEvent"),
        ("melissa", "MelissaDressRequestEvent", "AmandaDressRequestEvent"),
        ("amanda", "AmandaDressRequestEvent", "HouseholdOutfitRewardEvent"),
    ):
        block = _label_block(source, label_name, next_label)
        assert f'call HouseholdOutfitRequestTerms("{girl_name}")' in block
        assert "MenuItem(" not in block

    assert "label HouseholdBarberRequestChoice" not in source
    assert "label HouseholdRevealDressRequestChoice" not in source
    assert "label HouseholdSoapRequestAcknowledge" not in source
    assert "label MelissaRoomPestsChoice" not in source

    assert "label MelissaNightWakeEvent" not in source
    assert "label MelissaNightWakeChoice" not in source


def test_household_event_procedures_return_without_room_dispatch_jump():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert "HouseholdReturnCurrentRoom" not in source
    assert "household_return_current_room_label" not in source
    assert "jump expression _household_return_room" not in source
    assert "call TavernKitchenBreakfastShowText(scene_runtime.text)" in source
