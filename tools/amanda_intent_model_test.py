from pathlib import Path
import importlib.util
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "game" / "Utilities" / "General" / "NPC" / "AmandaIntent_ren.py"


def load_model():
    spec = importlib.util.spec_from_file_location("AmandaIntent_ren", MODEL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AmandaIntentModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_model()

    def base_context(self):
        return {
            "day": 4,
            "cycle_offset": 0,
            "hour": 8,
            "location": "TavernKitchen",
            "witnesses": ["sandra", "melissa"],
            "friend": 5,
            "openness": 3,
            "sexual_openness": 0,
            "arousal": 0,
            "wetness": 0,
            "anger": 0,
            "rebel": 0,
            "pregnancy": 0,
            "money_pressure": 0.3,
            "household_order": 0.6,
            "attention_gap": 0.2,
            "jealousy": 0.0,
            "melissa_friend": 5,
            "amanda_var": {
                "alberfriends": 0,
                "alberprohibit": 0,
                "lizafriends": 0,
            },
            "appearance": {
                "hygiene": 0.3,
                "skin": 0.2,
                "scent": 0.1,
                "hair": 0.3,
                "body_grooming": 0.1,
                "dress": 0.2,
                "manners": 0.0,
                "clara_training": 0.0,
            },
            "daily_work_report": {
                "cleaning": "none",
                "waitress": "none",
                "cooking": "none",
                "complaints": 0,
                "rude_clients": 0,
                "tips": 0,
            },
        }

    def test_cycle_changes_desire_need(self):
        steady = self.base_context()
        fertile = self.base_context()
        fertile["day"] = 11

        steady_state = self.model.amanda_choose_intent(steady)
        fertile_state = self.model.amanda_choose_intent(fertile)

        self.assertLess(steady_state["needs"]["desire"], fertile_state["needs"]["desire"])
        self.assertEqual(fertile_state["profile"]["cycle_phase"], "fertile")

    def test_bad_work_report_reduces_reward_path(self):
        good = self.base_context()
        bad = self.base_context()
        good["daily_work_report"] = {
            "cleaning": "good",
            "waitress": "good",
            "cooking": "none",
            "complaints": 0,
            "rude_clients": 0,
            "tips": 8,
        }
        bad["daily_work_report"] = {
            "cleaning": "bad",
            "waitress": "skipped",
            "cooking": "none",
            "complaints": 2,
            "rude_clients": 1,
            "tips": 0,
        }

        good_rows = {row["intent"]: row for row in self.model.amanda_score_intents(good)["intents"]}
        bad_rows = {row["intent"]: row for row in self.model.amanda_score_intents(bad)["intents"]}

        self.assertGreater(good_rows["ask_player_reward_for_work"]["score"], bad_rows["ask_player_reward_for_work"]["score"])
        self.assertGreater(bad_rows["obey_and_work"]["score"], good_rows["obey_and_work"]["score"])

    def test_legare_help_becomes_candidate_after_blocked_need(self):
        context = self.base_context()
        context.update({
            "location": "MarketPlace",
            "player_blocked_recent_need": 1,
            "money_pressure": 0.9,
            "attention_gap": 0.7,
            "rebel": 4,
        })
        context["amanda_var"] = {
            "alberfriends": 8,
            "albernowdances": 1,
            "alberprohibit": 0,
            "lizafriends": 0,
        }

        rows = {row["intent"]: row for row in self.model.amanda_score_intents(context)["intents"]}

        self.assertTrue(rows["ask_legare_help"]["allowed"])
        self.assertGreater(rows["ask_legare_help"]["score"], 0.35)

    def test_feedback_changes_future_bias(self):
        memory = {}
        memory = self.model.amanda_apply_feedback(memory, "ask_player_beauty_help", "approved", day=3)
        approved_bias = memory["ask_player_beauty_help"]["bias"]
        memory = self.model.amanda_apply_feedback(memory, "ask_player_beauty_help", "refused_badly", day=4, public=True)

        self.assertGreater(approved_bias, 0)
        self.assertLess(memory["ask_player_beauty_help"]["bias"], approved_bias)
        self.assertEqual(memory["ask_player_beauty_help"]["public_refusals"], 1)

    def test_satisfied_beauty_help_stops_repeat_request(self):
        context = self.base_context()
        context["beauty_help_satisfied"] = 1
        context["money_pressure"] = 0.1
        context["attention_gap"] = 0.6
        context["appearance"] = {
            "hygiene": 0.8,
            "skin": 0.8,
            "scent": 0.8,
            "hair": 0.8,
            "body_grooming": 0.8,
            "dress": 0.8,
            "manners": 0.2,
            "clara_training": 0.0,
        }

        rows = {row["intent"]: row for row in self.model.amanda_score_intents(context)["intents"]}

        self.assertFalse(rows["ask_player_beauty_help"]["allowed"])
        self.assertEqual(rows["ask_player_beauty_help"]["blocked_reason"], "beauty_help_already_done")

    def test_flow_gates_block_wrong_context(self):
        breakfast = self.base_context()
        breakfast["mode"] = "breakfast"
        breakfast["location"] = "TavernKitchen"
        breakfast_rows = {row["intent"]: row for row in self.model.amanda_score_intents(breakfast)["intents"]}

        self.assertFalse(breakfast_rows["visit_player_room"]["allowed"])
        self.assertEqual(breakfast_rows["visit_player_room"]["blocked_reason"], "not_breakfast_flow")

        room = self.base_context()
        room["mode"] = "room"
        room["location"] = "TavernMyRoom"
        room["daily_work_report"] = {
            "cleaning": "bad",
            "waitress": "none",
            "cooking": "none",
            "complaints": 2,
            "rude_clients": 0,
            "tips": 0,
        }
        room_rows = {row["intent"]: row for row in self.model.amanda_score_intents(room)["intents"]}

        self.assertTrue(room_rows["obey_and_work"]["allowed"])

    def test_nonnumeric_context_values_do_not_crash(self):
        context = self.base_context()
        context["money_pressure"] = "bad-data"
        context["appearance"]["hair"] = "unknown"
        context["preference_weights"] = {"teasing": "high"}

        state = self.model.amanda_score_intents(context)

        self.assertIn("intents", state)
        self.assertGreater(len(state["intents"]), 0)


if __name__ == "__main__":
    unittest.main()
