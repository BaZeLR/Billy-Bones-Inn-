from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "game/Inn/HouseholdRuntimeEvents.rpy"
HOUSEHOLD = ROOT / "game/Utilities/General/NPC/HouseholdAI_ren.rpy"
PURCHASE = ROOT / "game/NPC/Girls/Common/GirlDressSuggest.rpy"
REFUSAL = ROOT / "game/NPC/Girls/Common/GirlDressBuy.rpy"
NO_SHOW = ROOT / "game/Utilities/General/Clothes/DressNoShow.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def _label_block(source, label_name, next_label):
    return source.split(f"label {label_name}", 1)[1].split(f"label {next_label}", 1)[0]


def test_outfit_request_has_one_household_payload_and_one_daily_event_lifecycle():
    events = _source(EVENTS)
    household = _source(HOUSEHOLD)
    purchase = _source(PURCHASE)
    refusal = _source(REFUSAL)
    no_show = _source(NO_SHOW)

    assert '"outfit_requests"' in household
    assert "household.outfit_requests[girl] = favor" in events
    assert 'daily_events.add(girl, "alllocs", -1, ">", 1, 7, "OutfitReward", "HouseholdOutfitRewardEvent", "girl")' in events
    assert "household_schedule_outfit_reward(g)" in purchase
    assert "household_mark_revealing_dress_order(g, d)" in purchase
    assert "except Exception" not in purchase.split("def _gds_apply_purchase", 1)[1].split("def _gds_relative_callout_name", 1)[0]
    assert "household_cancel_outfit_request(GirlName)" in refusal
    assert no_show.count("household_cancel_outfit_request(_dns_girl)") == 2


def test_outfit_request_and_reward_are_native_returnable_scene_procedures():
    source = _source(EVENTS)
    terms = _label_block(source, "HouseholdOutfitRequestTerms", "SandraDressInitiativeEvent")
    reward = _label_block(source, "HouseholdOutfitRewardEvent", "HouseholdOutfitRewardShowScene")
    handjob = _label_block(source, "HouseholdOutfitRewardHandjobScene", "HouseholdOutfitRewardOralScene")
    oral = _label_block(source, "HouseholdOutfitRewardOralScene", "TavernStorageRatEvent")

    assert "\n    menu:\n" in terms
    assert 'household_outfit_favor_available(_outfit_girl, "show")' in terms
    assert 'household_outfit_favor_available(_outfit_girl, "handjob")' in terms
    assert 'household_outfit_favor_available(_outfit_girl, "oral")' in terms
    assert "main_ui_begin_native_scene_state" in reward
    assert "main_ui_end_native_scene_state" in reward
    assert "household_reschedule_outfit_reward" in reward
    assert '_outfit_hand_info.player_cum("outside")' in handjob
    assert '_outfit_oral_info.player_cum("mouth")' in oral
    assert "player_record_orgasm" not in handjob + oral
    assert "while True" not in terms + reward + handjob + oral
    assert "MenuItem(" not in terms + reward + handjob + oral


def test_each_tavern_outfit_requester_owns_only_her_scene_images():
    expected = {
        "amanda": ROOT / "game/NPC/Girls/Amanda/InitAmanda.rpy",
        "melissa": ROOT / "game/NPC/Girls/Melissa/InitMelissa.rpy",
        "sandra": ROOT / "game/NPC/Girls/Sandra/InitSandra.rpy",
    }

    for girl_name, path in expected.items():
        source = _source(path)
        manifest = source.split('"outfit_reward": {', 1)[1].split("},", 1)[0]
        assert f'images/{girl_name}/' in manifest
        assert all(key in manifest for key in ('"show"', '"handjob"', '"oral"'))
