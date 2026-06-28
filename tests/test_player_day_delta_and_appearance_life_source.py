from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (PROJECT_ROOT / path).read_text(encoding="utf-8-sig")


def test_day_delta_helpers_exist_and_random_seed_uses_current_game_day():
    source = read_rel("game/script.rpy")

    assert "def current_game_day(day_value=None):" in source
    assert "def day_delta_since(start_day, current_day=None):" in source
    assert "def day_delta_ready(start_day, delta_days=1, current_day=None):" in source
    assert "def day_timer_decrement(value, amount=1):" in source
    assert "current_game_day() * 1009" in source


def test_player_appearance_owns_wash_haircut_and_life_timers():
    source = read_rel("game/Utilities/General/Player/Player.rpy")

    assert "WASH_FRESH_DAYS = 3" in source
    assert "HAIRCUT_FRESH_DAYS = 14" in source
    assert "DRESS_LIFE_DAYS = 42" in source
    assert "self.washDays = self.WASH_FRESH_DAYS" in source
    assert "self.hairCutdays = self.HAIRCUT_FRESH_DAYS" in source
    assert "self.dress_life_days = {\"villagedress\": self.DRESS_LIFE_DAYS}" in source
    assert "self.item_life_days = {}" in source
    assert "def age_daily(self, days=1, item_ids=None):" in source


def test_next_day_ages_player_appearance_once_per_day():
    source = read_rel("game/Utilities/Time/NextDay.rpy")

    assert "player_state(False).daily_maintenance(1)" in source


def test_story_and_random_cooldowns_use_day_delta_helper():
    story_source = read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    town_source = read_rel("game/Town/RandomTownEvents.rpy")

    assert "return day_delta_since(last_day) < self._int(cooldown_days, 1)" in town_source
