from pathlib import Path
from types import SimpleNamespace
import textwrap


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Utilities/General/NPC/SetTavernServiceLevels.rpy"


class Worker:
    def __init__(self, name, jobs, skills, hired=True):
        self.name = name
        self.jobs = dict(jobs)
        self.skills = dict(skills)
        self.hired = hired

    def is_tavern_worker(self):
        return self.hired

    def job_value(self, key, default=0):
        return self.jobs.get(key, default)

    def skill_value(self, key, default=0):
        return self.skills.get(key, default)


def run_service_calculation(workers):
    source = SOURCE.read_text(encoding="utf-8-sig")
    body = source.split("init python:", 1)[1].split("\n\nlabel SetTavernServiceLevels:", 1)[0]
    namespace = {
        "people": SimpleNamespace(girl_items=lambda: [(worker.name, worker) for worker in workers]),
        "player": SimpleNamespace(
            tavern_management=SimpleNamespace(
                service=SimpleNamespace(
                    kitchen_score=0,
                    cleanliness_score=0,
                    waitress_score=0,
                )
            )
        ),
    }
    exec(textwrap.dedent(body), namespace)
    namespace["update_tavern_service_levels"]()
    return namespace["player"].tavern_management.service


def test_hired_liza_is_part_of_the_same_service_calculation_as_existing_staff():
    sandra = Worker("sandra", {"jobwaitress": 1}, {"waitress": 10})
    liza = Worker("liza", {"jobwaitress": 1}, {"waitress": 25})
    visitor = Worker("visitor", {"jobwaitress": 1}, {"waitress": 99}, hired=False)

    without_liza = run_service_calculation([sandra, visitor])
    with_liza = run_service_calculation([sandra, liza, visitor])

    assert without_liza.waitress_score == 10
    assert with_liza.waitress_score == 25
