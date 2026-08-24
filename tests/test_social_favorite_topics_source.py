import ast
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOCIAL_TOPICS = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "SocialTalkTopics.rpy"
MELISSA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "InitMelissa.rpy"
SANDRA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "InitSandra.rpy"
AMANDA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmanda.rpy"


def _topic_ids_from_social_talk_source():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")
    match = re.search(r"SOCIAL_TALK_TOPICS\s*=\s*\[(.*?)\n\s*\]", source, re.S)
    assert match is not None
    return set(re.findall(r'\{"id": "([^"]+)"', match.group(1)))


def _favorite_topics_from_init(path):
    source = path.read_text(encoding="utf-8-sig")
    match = re.search(r'"favorite_topics":\s*(\[[^\]]+\])', source)
    assert match is not None
    return ast.literal_eval(match.group(1))


def test_class_based_girls_have_five_valid_favorite_topics():
    valid_topics = _topic_ids_from_social_talk_source()

    for path in [AMANDA_INIT, MELISSA_INIT, SANDRA_INIT]:
        favorites = _favorite_topics_from_init(path)
        assert len(favorites) == 5
        assert len(set(favorites)) == 5
        assert all(topic in valid_topics for topic in favorites)


def test_amanda_favorite_topics_match_character_brief():
    assert _favorite_topics_from_init(AMANDA_INIT) == ["fashion", "dances", "gossip", "money", "stories"]


def test_favorite_topics_are_used_by_authoritative_social_topics():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")

    assert "def social_favorite_topic_ids" in source
    assert 'getattr(info, "talk_preferences", {})' in source
    assert "topic_key in social_favorite_topic_ids(key)" in source
    assert "mood += 2" in source


def test_seen_topics_are_owned_by_each_npc_not_a_global_mirror():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")

    assert "def social_topic_seen_state" in source
    assert 'info.var["social_topic_seen"] = state' in source
    assert "SocialTalkTopicSeen" not in source
