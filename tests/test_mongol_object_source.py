from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_mongol_has_own_data_info_and_explicit_state():
    source = read_rel("game/NPC/Secondary/InitMongol.rpy")

    assert "class MongolData(PeopleData):" in source
    assert "class MongolInfo(BaseNPC):" in source
    assert "define MongolStaticData = MongolData()" in source
    assert "default Mongol = MongolInfo()" in source
    assert "self.var =" not in source
    assert "STORY_DEFAULTS" not in source
    assert "ensure_story_defaults" not in source
    assert "def mongol_story_defaults(" not in source
    assert "def is_market_visible(self):" in source
    assert "try:" not in source.split("def is_market_visible(self):", 1)[1]

    for field_name in (
        "will_try_to_steal", "stocks_food_day", "stocks_arrest_day",
        "guard_captain_known", "market_roll_day", "market_roll",
        "asked_about_gypsy", "asked_price_increase",
        "zimmer_knows_horse_theft", "horse_price", "discount_asked",
        "theft_asked", "asked_about_seen_stolen", "seen_with_stolen_horse",
        "horses_bought",
    ):
        assert "self.%s =" % field_name in source


def test_mongol_uses_class_state_not_old_var_bridge():
    combined = "\n".join(
        [
            read_rel("game/NPC/Secondary/InitMongol.rpy"),
            read_rel("game/NPC/Secondary/IntMongolTalk.rpy"),
            read_rel("game/Town/Market/MarketPlace.rpy"),
            read_rel("game/Inn/TavernStable.rpy"),
            read_rel("game/Utilities/Time/NextDay_NewDayEvents.rpy"),
        ]
    )

    assert "MongolVar" not in combined
    assert "Mongol.var =" not in combined
    assert 'getattr(renpy.store, "Mongol.var"' not in combined
    assert "getattr(renpy.store, 'Mongol.var'" not in combined
    assert '_ensure_dict("Mongol.var")' not in combined
    assert '"var": Mongol.var' not in combined
    assert "Mongol(var=" not in combined
    assert "MongolInfo(var=" not in combined
    assert "Mongol.var" not in combined
    assert "Mongol.var_int" not in combined
    assert "Mongol.set_var_int" not in combined


def test_mongol_market_flow_uses_class_methods():
    source = read_rel("game/Town/Market/MarketPlace.rpy")

    assert "return bool(Mongol.is_market_visible())" in source
    assert "Mongol.reset_market_trade()" in source
    assert "Mongol.horse_price" in source
    assert 'threads.get("claraBookletMarket")' in source


def test_mongol_talk_uses_one_native_menu_without_recursive_loop_or_dispatcher():
    source = read_rel("game/NPC/Secondary/IntMongolTalk.rpy")
    talk = source.split("label MongolTalk:", 1)[1].split("\n\nlabel ClaraSecretMerchantMenu:", 1)[0]

    assert "menu:" in talk
    assert "while True:" in talk
    assert "MongolTalkApply" not in source
    assert "main_ui_runtime.action_items" not in talk
    assert 'jump MongolTalk' not in talk
    assert 'if _mongol_talk_new:' in talk


def test_mongol_purchase_keeps_qsp_stable_destination():
    source = read_rel("game/NPC/Secondary/IntMongolTalk.rpy")
    talk = source.split("label MongolTalk:", 1)[1].split("\n\nlabel ClaraSecretMerchantMenu:", 1)[0]

    assert talk.count("jump TavernStable") == 2
    assert '"Беру" if player.economy.money >= Mongol.horse_price:' in talk


def test_mongol_stocks_progress_uses_thread_stage_without_mirror_flags():
    runtime = read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    labels = read_rel("game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy")
    market = read_rel("game/Town/Market/MarketPlace.rpy")

    combined = "\n".join((runtime, labels, market))
    assert "StocksSeen" not in combined
    assert "StocksReleased" not in combined
    assert 'threads.get("claraBookletMarket")' in market
    assert "stage == 5" in market
    assert "stage == 6" in market
    assert "stage == 8" in market


def test_mongol_v61_migration_consumes_old_map_once():
    migration = read_rel("game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V61():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 73" in migration
    assert "if loaded_version < 62:" in migration
    assert "updateSave_V61()" in migration
    for old_key, field_name in (
        ("WillTryToSteal", "will_try_to_steal"),
        ("StocksFoodDay", "stocks_food_day"),
        ("StocksArrestDay", "stocks_arrest_day"),
        ("GuardCaptainKnown", "guard_captain_known"),
        ("MarketRollDay", "market_roll_day"),
        ("MarketRoll", "market_roll"),
        ("GypsyAsk", "asked_about_gypsy"),
        ("AskPriceIncr", "asked_price_increase"),
        ("ZimmerKnow", "zimmer_knows_horse_theft"),
        ("HorsePrice", "horse_price"),
        ("DiscountAsk", "discount_asked"),
        ("TheftAsk", "theft_asked"),
        ("AskSawStolen", "asked_about_seen_stolen"),
        ("SawStolen", "seen_with_stolen_horse"),
        ("HorsesBought", "horses_bought"),
    ):
        assert 'mongol_var.pop("%s"' % old_key in block
        assert "Mongol.%s =" % field_name in block
    assert 'mongol_var.pop("StocksSeen", None)' in block
    assert 'mongol_var.pop("StocksReleased", None)' in block
    assert 'globals().pop("MongolVar", None)' in block
