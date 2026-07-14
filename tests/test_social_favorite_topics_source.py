import ast
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TALK_SYSTEM = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Common" / "TalkSystem.rpy"
MELISSA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "InitMelissa.rpy"
SANDRA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "InitSandra.rpy"
AMANDA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmanda.rpy"


def _topic_ids_from_talk_system_talk_source():
    source = TALK_SYSTEM.read_text(encoding="utf-8-sig")
    match = re.search(r"TALK_SYSTEM_TOPICS\s*=\s*\((.*?)\n\s*\)", source, re.S)
    assert match is not None
    return set(re.findall(r'\("([^"]+)",', match.group(1)))


def _favorite_topics_from_init(path):
    source = path.read_text(encoding="utf-8-sig")
    match = re.search(r'"favorite_topics":\s*(\[[^\]]+\])', source)
    assert match is not None
    return ast.literal_eval(match.group(1))


def test_class_based_girls_have_five_valid_favorite_topics():
    valid_topics = _topic_ids_from_talk_system_talk_source()

    for path in [AMANDA_INIT, MELISSA_INIT, SANDRA_INIT]:
        favorites = _favorite_topics_from_init(path)
        assert len(favorites) == 5
        assert len(set(favorites)) == 5
        assert all(topic in valid_topics for topic in favorites)


def test_amanda_favorite_topics_match_character_brief():
    assert _favorite_topics_from_init(AMANDA_INIT) == ["fashion", "dances", "gossip", "money", "stories"]


def test_favorite_topics_are_used_by_talk_system_smalltalk():
    source = TALK_SYSTEM.read_text(encoding="utf-8-sig")

    assert "def talk_system_preferred_topics" in source
    assert 'preferences.get("favorite_topics", [])' in source
    assert "preferred = topic_key in talk_system_preferred_topics(key)" in source
    assert "if preferred:" in source
