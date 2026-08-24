from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_both_room_exit_renderers_preserve_the_exit_time_cost():
    room_template = (ROOT / "game/Utilities/General/Classes/RoomTemplate.rpy").read_text(encoding="utf-8-sig")
    fallback_builder = (ROOT / "game/Utilities/General/Screens/build_room_action_items.rpy").read_text(encoding="utf-8-sig")

    assert 'movement_actions(ex.target, getattr(ex, "minutes_to_pass", 5))' in room_template
    assert 'movement_actions(exit_obj.target, getattr(exit_obj, "minutes_to_pass", 5))' in fallback_builder


def test_custom_shop_menus_reuse_their_room_exit_actions():
    barber = (ROOT / "game/Town/Arts/BarberShop.rpy").read_text(encoding="utf-8-sig")
    stolyar = (ROOT / "game/Town/StolyarWorkshop.rpy").read_text(encoding="utf-8-sig")
    grocery = (ROOT / "game/Town/GroceryStore.rpy").read_text(encoding="utf-8-sig")

    assert barber.count("rooms.get(\"BarberShop\").build_exit_items()") == 2
    assert 'Jump("ArtisansQuarter")' not in barber
    assert stolyar.count("rooms.get(\"StolyarWorkshop\").build_exit_items()") == 3
    assert 'Jump("ArtisansQuarter")' not in stolyar
    assert "rooms.get(\"GroceryStore\").build_exit_items()" in grocery
    assert 'MenuItem("Вернуться на рынок", Jump("MarketPlace"))' not in grocery


def test_amanda_door_charges_only_when_entering_the_room():
    source = (ROOT / "game/Inn/TavernAmandaRoom.rpy").read_text(encoding="utf-8-sig")
    enter_without_knock = source.split("label TavernAmandaRoomEnterWithoutKnock:", 1)[1].split(
        "label TavernAmandaRoomApologizeForEntry:", 1
    )[0]

    assert source.count('MenuItem("Войти", movement_actions("TavernAmandaRoom"))') == 2
    assert '$ apply_movement_time(5, "TavernAmandaRoom")' in enter_without_knock
    assert 'MenuItem("Уйти", Jump("TavernUpstairs"))' in source
    assert "rooms.get(\"TavernAmandaRoom\").build_exit_items()" in source
