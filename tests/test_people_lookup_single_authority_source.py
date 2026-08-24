from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_people_lookup_returns_the_registered_owner_without_refresh_side_effects():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    lookup = runtime.split('def get_info(self, person=""):', 1)[1].split(
        "def ids(self):", 1
    )[0]

    assert "people_sync_person" not in game_sources
    assert "people_sync_all" not in game_sources
    assert "return info.update()" not in lookup
    assert "return self.runtime.get(people_normalize_id(person), None)" in lookup
    assert "def getPersonInfo(" not in runtime
    assert "def getPersonData(" not in runtime
    assert "def people_known_ids(" not in runtime


def test_relationship_and_daily_flags_have_single_storage_fields():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert ".relationship =" not in game_sources
    assert "self.relationship =" not in game_sources
    assert "def flirtToday(self):" in runtime
    assert "return people_to_int(getattr(self, \"flirted_today\", 0), 0) > 0" in runtime
    assert "def giftToday(self):" in runtime
    assert "return people_to_int(getattr(self, \"gifted_today\", 0), 0) > 0" in runtime


def test_people_name_has_one_runtime_definition():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert runtime.count('def people_name(person="", grammatical_case="nominative", fallback=""):') == 1


def test_people_registry_is_the_only_live_people_collection_owner():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "class PeopleRegistry(object):" in runtime
    assert "default people = PeopleRegistry()" in runtime
    for retired_name in ("peopleData", "peopleInfo", "secondary_npcs"):
        assert retired_name not in game_sources
