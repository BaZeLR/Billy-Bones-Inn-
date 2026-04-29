from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.runtime_logic_tests import run_checks  # noqa: E402


def test_story_runtime_logic_has_no_failures():
    report = run_checks(PROJECT_ROOT)
    assert not report.failures, "\n".join(
        f"{row.area}: {row.detail}" for row in report.failures
    )
