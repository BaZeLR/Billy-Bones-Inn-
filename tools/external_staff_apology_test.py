#!/usr/bin/env python3
"""Click native staff apology/favor menus in an isolated, headless Ren'Py game."""

from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

import external_tavern_premium_test as premium


TEST_RPY = r'''
init python:
    def external_apology_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_apology_button(caption):
        return "choice_panel_button_%d" % external_apology_choices().index(caption)

    def external_apology_talk_visible(girl):
        return (renpy.get_screen("main_ui") is not None
            and main_ui_runtime.mode == "talk"
            and main_ui_runtime.selected_char == girl
            and "Осмотреть" in external_apology_choices())

    def external_apology_seed(accepted):
        for seed in range(100):
            renpy.random.seed(seed)
            result = renpy.random.randint(1, 2) == 1
            gain = renpy.random.randint(1, 5) if result else 0
            if result == accepted:
                renpy.random.seed(seed)
                return gain
        raise AssertionError("No deterministic apology seed found")

    def external_apology_prepare(girl, relation):
        info = people.get_info(girl)
        info.rel = relation
        info.known = True
        info.talked_today = 0
        info.asked_today = 0
        info.anger_with_player = 0
        relationship_calm(girl, 100)
        household.outfit_requests.pop(girl, None)
        household.barber_appointments.pop(girl, None)
        household.barber_request_last_day.pop(girl, None)
        household.barber_visit_last_day.pop(girl, None)
        daily_events.delete(girl, "BuyDressTom", "")
        daily_events.delete(girl, "BuyDress", "")
        player.tavern_management.breakfast.event_active = False
        rooms.enter("TavernSandraRoom")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.talk_picture = ""
        main_ui_runtime.action_title = "Комната Сандры"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = tavern_sandra_room_action_items()
        scene_runtime.picture = tavern_sandra_room_picture()
        scene_runtime.text = tavern_sandra_room_text()
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")
        assert info.can_request_favor("tailor") and info.can_request_favor("barber")
        return info

testsuite global:
    teardown:
        exit
'''


def start_talk(girl: str, label: str, relation: int) -> str:
    return f'''
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ _staff_info = external_apology_prepare("{girl}", {relation})
    run Call("{label}", "{girl}")
    advance until eval (external_apology_talk_visible("{girl}")) timeout 20.0
    assert eval (main_ui_runtime.action_items == []) timeout 5.0
'''


def refuse_grope(girl: str, relation: int) -> str:
    return f'''
    click id (external_apology_button("Лапать")) pos (0.5, 0.5) until eval (_staff_info.anger_with_player == 1) timeout 20.0
    assert eval (_staff_info.rel == {max(0, relation - 5)} and _staff_info.can_apologize()) timeout 5.0
    assert eval (external_apology_talk_visible("{girl}") and _staff_info.talked_today == 0) timeout 5.0
    assert eval (not _staff_info.can_request_favor("tailor") and not _staff_info.can_request_favor("barber")) timeout 5.0
    assert eval ("Сначала заплати" in scene_runtime.text or "сначала заплатить" in scene_runtime.text) timeout 5.0
'''


def apologize(caption: str, accepted: bool) -> str:
    condition = '"Вернуться к разговору" in external_apology_choices()' if accepted else '_staff_info.talked_today == 1'
    return f'''
    $ _staff_before_rel = _staff_info.rel
    $ _staff_expected_gain = external_apology_seed({accepted})
    click id (external_apology_button("{caption}")) pos (0.5, 0.5) until eval ({condition}) timeout 20.0
    assert eval (_staff_info.rel == _staff_before_rel + _staff_expected_gain and _staff_info.talked_today == 1) timeout 5.0
    assert eval (_staff_info.anger_with_player == {0 if accepted else 1}) timeout 5.0
'''


def finish_talk(girl: str, caption: str = "Закончить разговор") -> str:
    return f'''
    assert eval (external_apology_talk_visible("{girl}")) timeout 5.0
    click id (external_apology_button("{caption}")) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and main_ui_runtime.mode == "scene") timeout 20.0
'''


TEST_RPY += '\ntestcase external_liza_refusal_apology_tailor:\n'
TEST_RPY += start_talk("liza", "IntLizaTalk", 4) + refuse_grope("liza", 4)
TEST_RPY += apologize("Извиниться перед Лизеттой", True)
TEST_RPY += r'''
    assert eval (1 <= _staff_expected_gain <= 5 and "Отношения: +%d." % _staff_expected_gain in scene_runtime.text) timeout 5.0
    assert eval (external_apology_choices() == ["Договориться о покупке обновки у Ирмы", "Договориться о визите к цирюльнику", "Вернуться к разговору"]) timeout 5.0
    assert eval (renpy.get_screen("main_ui") is not None and main_ui_runtime.mode == "talk" and main_ui_runtime.action_items == []) timeout 5.0
    click id (external_apology_button("Договориться о покупке обновки у Ирмы")) pos (0.5, 0.5) until eval (external_apology_talk_visible("liza")) timeout 20.0
    assert eval (household.outfit_requests.get("liza") == "surprise" and daily_events.exists("liza", "BuyDressTom", "") == 1) timeout 5.0
    assert eval (not Liza.can_request_favor("tailor") and Liza.can_request_favor("barber")) timeout 5.0
    assert eval (Liza.rel == _staff_before_rel + _staff_expected_gain and Liza.talked_today == 1) timeout 5.0
'''
TEST_RPY += finish_talk("liza")

TEST_RPY += '\ntestcase external_georgett_refusal_apology_barber:\n'
TEST_RPY += start_talk("georgett", "IntGeorgettTalk", 9) + refuse_grope("georgett", 9)
TEST_RPY += apologize("Извиниться перед Жоржеттой", True)
TEST_RPY += r'''
    click id (external_apology_button("Договориться о визите к цирюльнику")) pos (0.5, 0.5) until eval ("Пообещать визит к Серджио" in external_apology_choices()) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and main_ui_runtime.mode == "talk" and main_ui_runtime.selected_char == "georgett") timeout 5.0
    assert eval ("загладить обиду" in scene_runtime.text and "За завтраком" not in scene_runtime.text) timeout 5.0
    assert eval (Georgett.talked_today == 1 and household.barber_request_last_day["georgett"] == current_game_day()) timeout 5.0
    click id (external_apology_button("Пообещать визит к Серджио")) pos (0.5, 0.5) until eval (external_apology_talk_visible("georgett")) timeout 20.0
    assert eval (household.barber_appointments.get("georgett") == 1 and not Georgett.can_request_favor("barber")) timeout 5.0
    assert eval (Georgett.rel == _staff_before_rel + _staff_expected_gain and Georgett.talked_today == 1) timeout 5.0
'''
TEST_RPY += finish_talk("georgett")

TEST_RPY += '\ntestcase external_liza_and_georgett_rejected_apologies:\n'
for girl, label, caption, relation in (
    ("liza", "IntLizaTalk", "Извиниться перед Лизеттой", 4),
    ("georgett", "IntGeorgettTalk", "Извиниться перед Жоржеттой", 9),
):
    TEST_RPY += start_talk(girl, label, relation) + refuse_grope(girl, relation)
    TEST_RPY += apologize(caption, False)
    TEST_RPY += r'''
    assert eval ("все еще сердится" in scene_runtime.text and "Вернуться к разговору" not in external_apology_choices()) timeout 5.0
    assert eval (not _staff_info.can_request_favor("tailor") and not _staff_info.can_request_favor("barber")) timeout 5.0
    assert eval (_staff_info.can_apologize() and _staff_info.name not in household.outfit_requests and not household.barber_appointments.get(_staff_info.name, 0)) timeout 5.0
'''
    TEST_RPY += finish_talk(girl)

TEST_RPY += '\ntestcase external_original_three_reconciliation_and_back:\n'
for girl, label, caption, original_text in (
    ("amanda", "IntAmandaTalk", "Извиниться перед Амандой", "Аманда благосклонно выслушала вас, трогательно обняла и сказала, что очень к вам привязана!"),
    ("sandra", "IntSandraTalk", "Попробовать помириться с Сандрой", "Сандра благосклонно выслушала вас, обняла и сказала, что она всегда будет вас любить, несмотря ни на что!"),
    ("melissa", "IntMelissaTalk", "Попробовать помириться с Мелиссой", "Мелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что ценит вас и все понимает!"),
):
    TEST_RPY += start_talk(girl, label, 4)
    TEST_RPY += '    $ _staff_info.change_anger(1, "external_apology_test")\n'
    TEST_RPY += apologize(caption, True)
    TEST_RPY += f'''
    assert eval ("{original_text}" in scene_runtime.text) timeout 5.0
    $ _staff_apology_text = scene_runtime.text
    click id (external_apology_button("Вернуться к разговору")) pos (0.5, 0.5) until eval (external_apology_talk_visible("{girl}")) timeout 20.0
    assert eval (scene_runtime.text == _staff_apology_text and _staff_info.talked_today == 1) timeout 5.0
    assert eval (_staff_info.name not in household.outfit_requests and not household.barber_appointments.get(_staff_info.name, 0)) timeout 5.0
'''
    TEST_RPY += finish_talk(girl, "Назад")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=premium.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=480)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")
    os.environ.update(SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy", RENPY_RENDERER="sw")
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_staff_apology_"))
    try:
        premium.TEST_RPY = TEST_RPY
        temp_project = premium.build_temp_project(premium.project_root(), temp_root)
        print(f"Temporary headless staff apology test project: {temp_project}", flush=True)
        if args.compile_lint:
            savedir = temp_project / ".test-saves"
            savedir.mkdir(exist_ok=True)
            for command in ("compile", "lint"):
                completed = subprocess.run(
                    [str(renpy_exe), str(temp_project), "--savedir", str(savedir), command],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                )
                print(f"Ren'Py {command}: exit {completed.returncode}", flush=True)
                premium.safe_print(completed.stdout)
                if completed.returncode:
                    return completed.returncode
        return premium.run_renpy(renpy_exe, temp_project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary staff apology test project: {temp_root}")
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_staff_apology_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            premium.remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
