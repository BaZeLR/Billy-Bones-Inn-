from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "game"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_tavern_entry_stops_after_first_event():
    scene = read("Inn/TavernMain.rpy").split("label TavernMain:", 1)[1].split("label TavernMainObjectMenu", 1)[0]
    assert "_tavern_entry_event_played = bool(_return)" in scene
    assert scene.count("if not _tavern_entry_event_played and") >= 5
    assert "if not _tavern_entry_event_played and tavern_main_closed_text() == \"\":" in scene


def test_premium_is_paid_into_each_workers_personal_purse():
    ledger = read("Inn/TavernSandraRoom.rpy")
    assert "_premium_info.receive_personal_money(_premium_amount)" in ledger
    assert "_premium_person_info.receive_personal_money(_premium_amount)" in ledger


def test_amanda_service_earnings_share_the_premium_purse():
    amanda = read("NPC/Girls/Amanda/InitAmanda.rpy")
    next_day = read("Utilities/Time/NextDay.rpy")
    barber = read("Town/Arts/BarberShop.rpy")
    dress = read("NPC/Girls/Amanda/AmandaLegareChoice.rpy")
    assert 'self.receive_personal_money(self.var.pop("legare_service_savings"))' in amanda
    assert '"legare_service_savings": 0' not in amanda
    assert 'Amanda.receive_personal_money(tavern.service_worker_revenue(' in next_day
    assert 'Amanda.spend_personal_money(_barber_guest_price)' in barber
    assert 'Amanda.spend_personal_money(_amanda_dress_price)' in dress


def test_paid_household_worker_keeps_tailor_anger_private():
    scene = read("Utilities/General/Clothes/DressNoShow.rpy")
    assert 'if _dns_girl in ("sandra", "melissa", "amanda") and int(getattr(people.get_info(_dns_girl), "personal_money", 0) or 0) > 0:' in scene
    assert 'change_anger(2, "missed_tailor_with_premium")' in scene
    assert "if not _dns_silent:" in scene


def test_unfunded_promises_end_once_and_hurt_relationships():
    barber = read("Town/Arts/BarberShop.rpy")
    tailor = read("NPC/Girls/Common/GirlDressBuy.rpy")
    assert "people.get_info(_barber_guest).record_broken_care_promise()" in barber
    assert "household.barber_appointments.pop(_barber_guest, None)" in barber
    assert "people.get_info(GirlName).record_broken_care_promise()" in tailor
    assert "household_cancel_outfit_request(GirlName)" in tailor
