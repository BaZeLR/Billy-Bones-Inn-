import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def _label(source, name):
    return source.split("label %s:" % name, 1)[1].split("\nlabel ", 1)[0]


def test_clara_fiance_case_replaces_the_old_tail_in_one_linear_thread():
    runtime = _source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    block = runtime.split('LThreadData(1, "clara", "PaintingsPath"', 1)[1].split(
        'LThreadData(1, "clara", "ForestSofa"', 1
    )[0]

    ordered_targets = [
        "story_clara_paintings_church_6",
        "story_clara_paintings_secret_date_7",
        "story_clara_paintings_barber_closed_8",
        "story_clara_paintings_luisa_report_9",
        "story_clara_paintings_zimmer_wine_10",
        "story_clara_paintings_zimmer_puzzle_11",
        "story_clara_paintings_sergio_followup_12",
        "story_clara_paintings_tavern_arrival_13",
        "story_clara_paintings_confession_14",
        "story_clara_paintings_ointment_15",
    ]
    assert [block.index(name) for name in ordered_targets] == sorted(
        block.index(name) for name in ordered_targets
    )
    assert '"ArtisansQuarter",\n            "enter",\n            7,' in block
    assert block.count('"BarberShop",\n                "enter",\n                8,') == 2
    assert '"talk_luisa",\n            "clara_fiance_case",\n            9,' in block
    assert block.count('"talk_zimmer",\n                "clara_fiance_case",') == 6
    assert block.count('"talk_sergio",\n                "clara_fiance_case",\n                12,') == 2
    assert '"TavernMain",\n            "enter",\n            13,' in block
    assert '"TavernMelissaRoom",\n            "enter",\n            14,' in block
    assert '"special_cream_001",\n            "TavernMelissaRoom",\n            "clara_ointment",\n            15,' in block
    ointment_block = block.split('"story_clara_paintings_ointment_15"', 1)[1]
    for condition in (
        "#str(people.location('clara') or '') == 'TavernMelissaRoom'",
        "#people.is_awake('clara')",
        "#people.can_talk('clara')",
        "#not Clara.sex_busy()",
    ):
        assert condition in ointment_block

    for obsolete_target in (
        "story_clara_paintings_barber_7",
        "story_clara_paintings_commission_8",
        "story_clara_paintings_commission_followup_9",
        "story_clara_paintings_evening_peek_10",
        "story_clara_paintings_confession_11",
        "story_clara_paintings_murder_12",
    ):
        assert obsolete_target not in block


def test_clara_fiance_labels_own_choices_and_only_success_advances():
    source = _source("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy")

    secret_date = _label(source, "story_clara_paintings_secret_date_7")
    assert '"Осторожно заглянуть внутрь":' in secret_date
    assert '"Не вмешиваться и уйти":' in secret_date
    assert "if int(player.stats.exploration or 0) < 200:" in secret_date
    assert secret_date.count("event_runtime.active_thread.advance()") == 1
    assert secret_date.count("calendar_v2.advance_minutes(15)") == 2

    no_wine = _label(source, "story_clara_paintings_zimmer_needs_wine_10")
    wine = _label(source, "story_clara_paintings_zimmer_wine_10")
    assert "winenum" not in no_wine
    assert "active_thread.advance" not in no_wine
    assert "player.tavern_management.winenum -= 1" in wine
    assert wine.index("winenum -= 1") < wine.index("active_thread.advance()")
    assert "jump story_clara_paintings_zimmer_puzzle_11" in wine

    puzzle = _label(source, "story_clara_paintings_zimmer_puzzle_11")
    for answer in ("Горничная", "Повар", "Дворецкий", "Садовник", "Жена"):
        assert '"%s":' % answer in puzzle
    assert puzzle.count("active_thread.advance()") == 1
    assert "Zimmer.mark_talked(max(0, 2 - int(Zimmer.talked_today or 0)))" in puzzle

    followup = _label(source, "story_clara_paintings_sergio_followup_12")
    assert "crafting.special_cream_recipe_unlocked = True" in followup
    assert "sergio_discount_percent = max(25," in followup

    treatment = _label(source, "story_clara_paintings_ointment_15")
    assert treatment.count('player.remove_item("special_cream_001", 1)') == 1
    assert treatment.count("event_runtime.active_thread.complete()") == 1
    assert "main_ui_runtime.action_items" not in treatment

    success = treatment.split('"Нанести мазь по просьбе Клариссы":', 1)[1].split(
        '"Убрать мазь и вернуться позже":', 1
    )[0]
    retry = treatment.split('"Убрать мазь и вернуться позже":', 1)[1]
    assert success.index('player.remove_item("special_cream_001", 1)') < success.index(
        "event_runtime.active_thread.complete()"
    )
    assert 'player.remove_item("special_cream_001", 1)' not in retry
    assert "event_runtime.active_thread.complete()" not in retry

    confession = _label(source, "story_clara_paintings_confession_14")
    assert "Я взрослая женщина и умею говорить, чего хочу" in confession
    assert "только по моей просьбе" in confession
    assert "Скажу “стоп”" in treatment
    assert "она ясно просит продолжать" in treatment
    assert treatment.index("потайное окошко") < treatment.index("глорихол")
    assert treatment.index("глорихол") < treatment.index("Монгола")
    assert treatment.index("Монгола") < treatment.index("старинный диван")
    assert treatment.index("старинный диван") < treatment.index(
        "event_runtime.active_thread.complete()"
    )

    for scene_label in (
        "story_clara_paintings_luisa_report_9",
        "story_clara_paintings_sergio_followup_12",
        "story_clara_paintings_tavern_arrival_13",
        "story_clara_paintings_confession_14",
        "story_clara_paintings_ointment_15",
    ):
        assert "vscene " in _label(source, scene_label)


def test_clara_fiance_case_uses_existing_room_and_talk_owners():
    paintings = _source("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy")
    barber = _source("game/Town/Arts/BarberShop.rpy")
    people_runtime = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    luisa = _source("game/Town/HunterClub.rpy")
    zimmer = _source("game/NPC/Secondary/IntZimmerTalk.rpy")
    melissa_room = _source("game/Inn/TavernMelissaRoom.rpy")

    barber_entry = barber.split("label BarberShop:", 1)[1].split("label BarberShopTalk:", 1)[0]
    assert barber_entry.index("call RoomEnterEventGate") < barber_entry.index(
        'if rooms.get("BarberShop").is_open():'
    )
    assert "if _return:" in barber_entry
    assert "jump ArtisansQuarter" in barber_entry
    assert 'story_event_available("talk_sergio", "clara_fiance_case")' in barber
    assert 'story_event_available("talk_luisa", "clara_fiance_case")' in luisa
    assert 'story_event_available("talk_zimmer", "clara_fiance_case")' in zimmer
    luisa_report = _label(paintings, "story_clara_paintings_luisa_report_9")
    assert "call HunterClubLuiseTalk" not in luisa_report
    zimmer_case = zimmer.split('"Поговорить о деле Клариссы и Серджио"', 1)[1].split(
        '"Посмотреть на десятника"', 1
    )[0]
    assert "main_ui_end_talk_state" not in zimmer_case
    assert "return" not in zimmer_case
    assert 'story_event_available("TavernMelissaRoom", "clara_ointment")' in melissa_room
    assert 'ointment_event = event_runtime.available["TavernMelissaRoom"]["clara_ointment"]' in melissa_room
    assert "if ointment_event.checkItem():" in melissa_room
    assert 'player.item_count("special_cream_001")' not in melissa_room
    assert 'SetField(main_ui_runtime, "action_items", post_event_items)' in melissa_room
    assert 'barber_shop_is_open(wday, hour)' in people_runtime
    assert 'barber_shop_is_open_at(wday, hour)' not in people_runtime


def test_detention_and_residence_project_from_the_thread_without_flags():
    clara = _source("game/NPC/Girls/Clara/InitClara.rpy")
    secondary = _source("game/NPC/Secondary/InitSecondaryNPC.rpy")
    room_rules = _source("game/Utilities/General/Classes/GameObjectTemplate.rpy")
    clara_schedule = json.loads(_source("game/NPC/Schedules/clara.json"))
    melissa_schedule = json.loads(_source("game/NPC/Schedules/melissa.json"))

    assert "def fiance_case_detained(self):" in clara
    assert "8 <= int(thread_info.num or 0) <= 11" in clara
    assert "def tavern_resident(self):" in clara
    assert "bool(thread_info.completed) or int(thread_info.num or 0) >= 14" in clara
    assert "if Clara.fiance_case_detained():" in secondary
    assert 'if rule_name == "clara_tavern_resident":' in room_rules
    assert "fiance_seen =" not in clara
    assert "clara_released =" not in clara
    assert "lives_at_tavern =" not in clara

    residence_rows = [
        row for row in clara_schedule["entries"]
        if row.get("condition", {}).get("rule") == "clara_tavern_resident"
        and row.get("condition", {}).get("resident", True)
        and row["label"].startswith("tavern_resident_")
    ]
    assert {row["label"] for row in residence_rows} == {
        "tavern_resident_sleep",
        "tavern_resident_day",
        "tavern_resident_evening",
    }
    resident_priorities = {row["label"]: row["priority"] for row in residence_rows}
    assert resident_priorities["tavern_resident_sleep"] > 700
    assert resident_priorities["tavern_resident_day"] < 200
    assert resident_priorities["tavern_resident_evening"] < 200
    for schedule, label in (
        (clara_schedule, "paintings_confession"),
        (melissa_schedule, "clara_paintings_confession"),
    ):
        confession = next(row for row in schedule["entries"] if row["label"] == label)
        assert confession["start"] == "20:00"
        assert confession["end"] == "22:59"
        assert confession["condition"] == {
            "rule": "thread_step",
            "thread": "claraPaintingsPath",
            "step": 14,
        }


def test_v91_migration_maps_only_old_thread_progress_and_retires_day_markers():
    migration = _source("game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V91():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]
    clara = _source("game/NPC/Girls/Clara/InitClara.rpy")

    assert "define currentVersion = 92" in migration
    assert "if loaded_version < 92:" in migration
    assert "updateSave_V91()" in migration
    assert "bool(crafting.special_cream_recipe_unlocked)\n                    and int(tractir_progress.sergio_discount_percent or 0) >= 25" in block
    assert "mapped_num = 13 if rewards_received else 12" in block
    assert "elif old_num <= 6:" in block
    assert "elif old_num <= 10:" in block
    assert "mapped_num = 7" in block
    assert "mapped_num = 8" in block
    assert "paintings.day = old_day" in block
    assert 'Clara.__dict__.pop("commission_followup_day", None)' in block
    assert 'Clara.__dict__.pop("murder_day", None)' in block
    assert "self.commission_followup_day" not in clara
    assert "self.murder_day" not in clara
