from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "game/Town/StolyarWorkshop.rpy").read_text(encoding="utf-8")
TALK = (ROOT / "game/NPC/Secondary/IntDraupnirTalk.rpy").read_text(encoding="utf-8")
INIT = (ROOT / "game/NPC/Secondary/InitDraupnir.rpy").read_text(encoding="utf-8")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8")


def test_workshop_orders_are_room_actions_without_legacy_menu_wrappers():
    assert "def stolyar_workshop_action_items():" not in SOURCE
    assert "label StolyarWorkshopBuildActions:" not in SOURCE
    assert "call StolyarWorkshopBuildActions" not in SOURCE
    assert "StolyarWorkshopSavedText" not in SOURCE
    assert "while _stolyar_ui_return is None:" not in SOURCE
    assert "_stolyar_closed_ui_return" not in SOURCE
    assert "_stolyar_order_ui_return" not in SOURCE
    assert "jump StolyarWorkshop" not in SOURCE
    assert "action_menus=[" in SOURCE
    assert 'RoomAction(action_id="inspect_draupnir", label="Осмотреть", hook="call", target="StolyarWorkshopLook")' in SOURCE
    assert 'condition=stolyar_workshop_can_ask_slogan' in SOURCE
    assert 'condition=stolyar_workshop_can_pay_slogan' in SOURCE
    assert 'main_ui_begin_talk_state("Разговор с Драупниром", "draupnir")' in TALK
    assert "menu:" in TALK
    assert "while True:" in TALK
    assert "jump IntDraupnirTalk" not in TALK
    assert "IntDraupnirTalkApply" not in TALK
    assert "main_ui_runtime.action_items" not in TALK
    assert "if _draupnir_talk_new:" in TALK
    assert '"Поболтать с гномом":' in TALK
    assert '"Спросить о ремонте вывески"' not in TALK
    assert '"Поговорить с Драупниром об отмычках"' not in TALK


def test_workshop_preserves_every_order_and_lockpick_event():
    actions = (
        "StolyarWorkshopLook", "StolyarWorkshopAskSlogan", "StolyarWorkshopPaySlogan",
        "StolyarWorkshopAskHole", "StolyarWorkshopPayHole", "StolyarWorkshopAskGlory",
        "StolyarWorkshopPayGlory", "StolyarWorkshopAskSoapBarrel",
        "StolyarWorkshopPaySoapBarrel", "StolyarWorkshopAskDogBooth",
        "StolyarWorkshopPayDogBooth",
    )
    for action in actions:
        assert f'target="{action}"' in SOURCE
        assert f"label {action}:" in SOURCE
        assert f"call {action}" not in TALK
    assert "StolyarWorkshopApply" not in SOURCE
    assert "choice_code" not in SOURCE
    assert 'target="checkTriggers", args=("StolyarWorkshop", "enter", 0)' in SOURCE
    assert 'condition=stolyar_workshop_lockpick_event_available' in SOURCE
    assert "player.spend_money(200)" in SOURCE
    assert "player.spend_money(100)" in SOURCE
    assert "player.spend_money(700)" in SOURCE
    assert "player.spend_money(75)" in SOURCE
    assert 'Draupnir.location = "StreetTavern"' not in SOURCE


def test_secondary_npc_talk_portrait_uses_registered_people_data():
    layout = (ROOT / "game/Utilities/General/Screens/main_layout.rpy").read_text(encoding="utf-8-sig")

    assert 'npc_data = people.get_data(key)' in layout
    assert 'candidates.append(getattr(npc_data, "portrait", ""))' in layout
    assert 'portrait="images/draupnir/dwarf1.jpg"' in INIT


def test_draupnir_story_state_is_explicit_and_instance_owned():
    assert "STORY_DEFAULTS" not in INIT
    assert "ensure_story_defaults" not in INIT
    assert "self.var =" not in INIT
    for field_name in (
        "slogan_quote_received", "peep_hole_quote_received",
        "glory_hole_quote_received", "soap_barrel_quote_received",
        "dog_booth_quote_received", "mongol_lockpick_order_day",
    ):
        assert "self.%s =" % field_name in INIT

    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    assert "Draupnir.var" not in live_sources
    assert "Draupnir.var_int" not in live_sources
    assert "Draupnir.set_var_int" not in live_sources


def test_draupnir_v59_migration_consumes_old_map_once():
    block = MIGRATION.split("def updateSave_V59():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 79" in MIGRATION
    assert "if loaded_version < 60:" in MIGRATION
    assert "updateSave_V59()" in MIGRATION
    for old_key, field_name in (
        ("SloganAsked", "slogan_quote_received"),
        ("HoleAsked", "peep_hole_quote_received"),
        ("GloryHoleAsked", "glory_hole_quote_received"),
        ("SoapBarrelAsked", "soap_barrel_quote_received"),
        ("DogBoothAsked", "dog_booth_quote_received"),
        ("MongolLockpickOrderDay", "mongol_lockpick_order_day"),
    ):
        assert 'draupnir_var.pop("%s"' % old_key in block
        assert "Draupnir.%s =" % field_name in block
    assert 'globals().pop("DraupnirVar", None)' in block
