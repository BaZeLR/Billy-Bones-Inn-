from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dog_companion_does_not_copy_state_into_people_profile():
    dog = (ROOT / "game/NPC/Secondary/DogCompanion.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "dog_sync_profile" not in game_sources
    assert "self.location =" not in dog
    assert "d.location" not in dog
    assert "spawn_day" not in dog
    assert "spawn_location" not in dog
    assert "wearing_bloomers" not in dog
    assert "set_bloomers" not in dog
    assert "calendar_v2.time_slot()" not in dog
    assert "def dog_prepare_current_spawn" not in dog
    assert "stray_hidden_day" in dog
    assert "DogStaticData.stray_roam_locations" in dog
    assert "def dog_display_name():" in dog
    assert "dog_home_roam_active()" in dog


def test_dog_is_registered_once_without_live_compatibility_repairs():
    dog_source = (ROOT / "game/NPC/Secondary/DogCompanion.rpy").read_text(encoding="utf-8-sig")
    people = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    gameplay = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert "def ensure_dog_runtime" not in gameplay
    assert "ensure_dog_runtime()" not in gameplay
    assert "define DogStaticData = DogData()" in dog_source
    assert "label InitDog:" in dog_source
    assert "call InitDog" in people
    assert "if not isinstance(dog_obj, DogCompanion):" in migration
