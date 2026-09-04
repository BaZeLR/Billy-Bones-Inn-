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


def test_boar_meat_deposit_is_the_single_owner_of_team_arousal_and_dog_bones():
    item_source = (GAME / "Items/Shops/HunterClubItems.rpy").read_text(encoding="utf-8-sig")
    actions = (GAME / "Utilities/General/Common/Actions.rpy").read_text(encoding="utf-8-sig")
    boar_branch = KITCHEN.split('if item_key == "boar_meat_001":', 2)[2].split('\n        if item_key == "milk_pitcher_001":', 1)[0]

    assert '"kitchen_deposit_team_arousal_bonus": 5' in item_source
    assert '"kitchen_deposit_outputs": (("dog_bone_001", 3),)' in item_source
    assert 'npc_info.add_arousal(arousal_bonus)' in boar_branch
    assert 'properties.get("kitchen_deposit_outputs", ())' in boar_branch
    assert 'player.add_item(output_key, output_total)' in boar_branch
    assert 'tavern_kitchen_apply_deposit_effect(item_key, deposit_count)' in KITCHEN
    assert "kitchen_deposit_outputs" not in BREAKFAST + actions


def test_kitchen_food_catalog_and_transfer_quantities_have_one_authority():
    item_sources = "\n".join(
        (GAME / relative).read_text(encoding="utf-8-sig")
        for relative in (
            "Items/Resources/BerriesItem.rpy",
            "Items/Resources/MushroomItem.rpy",
            "Items/Resources/HoneyCombItem.rpy",
            "Items/Resources/FoodBaleItem.rpy",
            "Items/Shops/HunterClubItems.rpy",
            "Items/Shops/GroceryStoreItems.rpy",
        )
    )
    catalog = KITCHEN.split("def tavern_kitchen_depositable_food_ids():", 1)[1].split("\n    def ", 1)[0]
    deposit = KITCHEN.split('def tavern_kitchen_deposit_food(item_id="", quantity=0):', 1)[1].split("\n    def ", 1)[0]

    assert item_sources.count('"kitchen_depositable": True') == 6
    assert "game_item_registry" in catalog
    assert 'properties.get("kitchen_depositable", False)' in catalog
    assert 'return ("berries_001"' not in catalog
    assert "deposit_count = item_count if requested_count <= 0 else min(item_count, requested_count)" in deposit
    assert 'MenuItem("Отнести все съедобные припасы", Call("TavernKitchenDepositAll"))' in KITCHEN
    assert 'Call("TavernKitchenDepositApply", _deposit_item_id, 1)' in KITCHEN
    assert 'Call("TavernKitchenDepositApply", _deposit_item_id, _deposit_count)' in KITCHEN


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
    assert 'main_ui_begin_native_scene_state("Воскресный обед")' in dinner
    assert "while _sunday_dinner_active:" in dinner
    assert '"Закончить воскресный обед"' in dinner
    assert dinner.index("sunday_dinner_last_day = current_game_day()") > dinner.index('"Закончить воскресный обед"')
    assert '"[scene_runtime.text]"' not in dinner


def test_sunday_dinner_keeps_church_jokes_and_soap_gifts_inside_its_native_event_menu():
    dinner = BREAKFAST.split("label TavernKitchenSundayDinner(serve_spicy=0):", 1)[1]

    assert '"Послушать воскресные шутки"' in dinner
    assert "Летучие мыши — дурной знак" in BREAKFAST
    assert "Всю службу глаза от наших грудей отвести не мог" in BREAKFAST
    assert "А хозяину Стефану так смотреть можно?" in BREAKFAST
    assert "Поймаю вас за рукоблудием" in BREAKFAST
    assert "Спросить, как прошла служба" not in dinner
    for npc_id, name in (("sandra", "Сандре"), ("melissa", "Мелиссе"), ("amanda", "Аманде"), ("becky", "Бекки")):
        assert '"Подарить мыло %s" if tavern_sunday_dinner_can_gift_soap_to("%s", _sunday_present_ids)' % (name, npc_id) in dinner
    assert "soap_total_piece_count() > 0" in BREAKFAST
    assert "social_gifted_today_value(key) <= 0" in BREAKFAST
    assert "call PlayerCardGiftItemTo(_sunday_gift_item, _sunday_gift_target)" in dinner
    assert 'main_ui_end_native_scene_state()' in dinner
