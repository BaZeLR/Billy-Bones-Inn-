from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
KITCHEN = (GAME / "Inn/TavernKitchen.rpy").read_text(encoding="utf-8-sig")
BREAKFAST = (GAME / "Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
RELATED = "\n".join(
    (GAME / relative).read_text(encoding="utf-8-sig")
    for relative in (
        "NPC/Secondary/MelissaWerecatQuest.rpy", "NPC/Girls/Melissa/MelissaEvents.rpy",
        "Inn/HouseholdRuntimeEvents.rpy", "Inn/EventWineForDance.rpy",
    )
)


def test_kitchen_uses_room_state_for_shared_text_without_boolean_notice_mirrors():
    source = KITCHEN + BREAKFAST + RELATED
    assert 'rooms.get(\"TavernKitchen\").state.get("saved_text", "")' in KITCHEN
    assert 'rooms.get(\"TavernKitchen\").state["saved_text"]' in KITCHEN
    for legacy in ("TavernKitchenSavedText", "TavernKitchenNoticeText", "TavernKitchenNoticePending", "BeckyKitchenVisitActive"):
        assert legacy not in source


def test_kitchen_has_one_action_source_without_builder_or_recursive_loop():
    source = KITCHEN + BREAKFAST + RELATED
    assert "def tavern_kitchen_action_items():" in KITCHEN
    assert "label TavernKitchenBuildActions:" not in KITCHEN
    assert "TavernKitchenBuildActions" not in source
    assert "while _kitchen_ui_return is None:" not in KITCHEN
    assert "label TavernKitchenRefreshBreakfastEvent:" not in BREAKFAST


def test_kitchen_preserves_meals_storage_tea_sandra_objects_and_breakfast():
    for token in (
        'Call("TavernKitchenBreakfast")', '"TavernKitchenSundayDinnerMenu"',
        'Call("TavernKitchenDepositMenu")', 'Call("TavernKitchenShareTeaWithSandraAndBecky")',
        'Call("TavernKitchenAskSandraBreakfasts")', 'Call("TavernKitchenAskSandraClients")',
        "rooms.get(\"TavernKitchen\").build_menu_sections()", "tavern_kitchen_hearth_wood_stock()",
    ):
        assert token in KITCHEN
    assert "Call(target)" in KITCHEN
    assert "label TavernKitchenBreakfast:" in BREAKFAST
    assert "label TavernKitchenFinishBreakfastEvent:" in BREAKFAST


def test_sunday_dinner_uses_schedule_attendance_and_applies_each_girls_planned_reward():
    availability = BREAKFAST.split("def tavern_sunday_dinner_available():", 1)[1].split("\n    def ", 1)[0]
    attendance = BREAKFAST.split("def tavern_sunday_dinner_present_ids():", 1)[1].split("\n    def ", 1)[0]
    reward = BREAKFAST.split("def tavern_sunday_dinner_apply_social_bonus(present_ids=None):", 1)[1].split("\n    def ", 1)[0]
    dinner = BREAKFAST.split("label TavernKitchenSundayDinner(serve_spicy=0):", 1)[1]

    assert 'people.schedule_state(npc_id).get("label", "")' in availability
    assert 'people.schedule_state(npc_id).get("location", "")' in availability
    assert 'for npc_id in ("sandra", "melissa", "amanda")' in availability
    assert "current_minutes" not in availability
    assert 'kitchen_ids = set(people.ids_at("TavernKitchen") or [])' in attendance
    assert 'if npc_id not in kitchen_ids:' in attendance
    assert 'if "becky" in kitchen_ids:' in attendance
    assert 'people.location("becky")' not in attendance
    assert "info.change_social(friend_delta=1)" in reward
    assert "_sunday_present_ids = list(tavern_sunday_dinner_present_ids() or [])" in dinner
    assert "tavern_sunday_dinner_apply_social_bonus(_sunday_present_ids)" in dinner
    assert 'player_eat_meal("воскресный обед для всей челяди", 22, 45)' in dinner
    assert "calendar_v2.advance_minutes(45)" not in dinner
