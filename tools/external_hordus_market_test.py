#!/usr/bin/env python3
"""Exercise real Hordus/Clara/sofa menus in a temporary Ren'Py project.

Uses the installed Ren'Py 8.5.2 native testcase runner and the existing isolated
project builder. No user save is loaded; all saves and reports stay in temp.
"""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import external_tavern_premium_test as isolated


TEST_RPY = r'''
init python:
    def external_hordus_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_hordus_button(prefix):
        index = next(index for index, caption in enumerate(external_hordus_choices()) if caption.startswith(prefix))
        return "choice_panel_button_%d" % index

    def external_hordus_date(day):
        calendar_v2.day = int(day)
        calendar_v2.week = (int(day) - 1) % 7 + 1
        calendar_v2.daysInGame = 280 + int(day) - 1
        calendar_v2.hour = 13
        calendar_v2.minute = 0
        event_runtime.fired_day = -1
        event_runtime.fired_keys_today = []
        event_runtime.evaluation_time = None
        findAvailableEvents(True)

    def external_hordus_prepare(known=False):
        for thread in threads.values():
            thread.abort()
        threads["claraBookletMarket"].advanceTo(0, force_active=True)
        threads["claraHordusMarket"].forceEnable()
        threads["claraPaintingsPath"].num = 0
        threads["claraPaintingsPath"].completed = False
        threads["claraTavernVisit"].num = 6
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        player.tavern_management.client_room_hole = 0
        player.tavern_management.glory_hole = 0
        for _, info in people.girl_items():
            for job_key in list(info.jobs.keys()):
                info.set_job_value(job_key, 0)
        Clara.day_location_override_day = -1
        Clara.day_location_override_code = ""
        Clara.market_intro_seen = False
        Clara.market_follow_failed_day = -1
        Clara.market_follow_failed_hour = -1
        Clara.drawings_secret_known = False
        Melissa.drawings_found = False
        player.stats.exploration = 100
        player.set_money(1000)
        Hordus.known = bool(known)
        Hordus.last_meeting_day = -1
        Hordus.last_trade_month = -1
        Sofa.installed = False
        calendar_v2.cycle = 1100
        calendar_v2.period = 1
        external_hordus_date(1)
        dates = HordusStaticData.monthly_visit_days()
        assert len(dates) == 2
        external_hordus_date(dates[0])
        assert people.location("clara") == "MarketPlace"
        assert people.location("hordus") == "MarketPlace"
        rooms.enter("MarketPlace")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_items = marketplace_action_items()
        scene_runtime.picture = rooms.get("MarketPlace").bg_picture
        scene_runtime.text = "EXTERNAL_HORDUS_MARKET_ORIGIN"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")
        return dates

testsuite global:
    teardown:
        exit

testcase external_hordus_first_second_and_recurring_meetings:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ _hordus_dates = external_hordus_prepare()
    assert eval (event_runtime.available["MarketPlace"]["enter"].target == "story_clara_market_booklet_0") timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until eval ("Проследить за Клариссой" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Проследить за Клариссой")) pos (0.5, 0.5)
    advance until eval ("Тихо уйти" in external_hordus_choices()) timeout 20.0
    assert eval (not Hordus.known and "Подойти к Клариссе и торговцу" not in external_hordus_choices()) timeout 5.0
    click id (external_hordus_button("Тихо уйти")) pos (0.5, 0.5) until eval (int(threads["claraBookletMarket"].num) == 1 and not external_hordus_choices()) timeout 20.0
    assert eval (not Hordus.known and Hordus.last_meeting_day == calendar_v2.daysInGame) timeout 5.0
    $ findAvailableEvents(True)
    assert eval (not story_event_available("MarketPlace", "enter")) timeout 5.0
    $ external_hordus_date(_hordus_dates[1])
    assert eval (event_runtime.available["MarketPlace"]["enter"].target == "story_clara_hordus_market") timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until eval ("Подойти" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Подойти")) pos (0.5, 0.5)
    advance until eval ("Познакомиться с торговцем" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Познакомиться с торговцем")) pos (0.5, 0.5)
    advance until eval ("Посмотреть товары Хордуса" in external_hordus_choices()) timeout 20.0
    assert eval (Hordus.known and threads["claraBookletMarket"].num == 1) timeout 5.0
    assert eval (scene_runtime.picture == "images/market/mistery_merchant.png") timeout 5.0
    click id (external_hordus_button("Вернуться к своим делам")) pos (0.5, 0.5) until eval (not external_hordus_choices()) timeout 20.0
    python:
        threads["claraBookletMarket"].advanceTo(threads["claraBookletMarket"].data.length, complete_at_end=True)
        calendar_v2.period = 2
        external_hordus_date(1)
        external_hordus_date(HordusStaticData.monthly_visit_days()[0])
    assert eval (event_runtime.available["MarketPlace"]["enter"].target == "story_clara_hordus_market") timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until eval ("Посмотреть товары Хордуса" in external_hordus_choices()) timeout 20.0
    assert eval ("Познакомиться с торговцем" not in external_hordus_choices() and threads["claraBookletMarket"].completed) timeout 5.0
    click id (external_hordus_button("Вернуться к своим делам")) pos (0.5, 0.5) until eval (not external_hordus_choices()) timeout 20.0
    assert eval (threads["claraBookletMarket"].completed and Hordus.known) timeout 5.0

testcase external_hordus_shop_cash_monthly_cap_and_back:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_hordus_prepare(True)
    $ player.set_money(0)
    $ _hordus_soap_before = player.item_count("luxury_soap_001")
    $ _hordus_tincture_before = player.item_count("libido_tincture_001")
    run Call("IntHordusTalk")
    advance until eval ("Посмотреть товары" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Посмотреть товары")) pos (0.5, 0.5) until eval ("Назад" in external_hordus_choices()) timeout 20.0
    assert eval (not any(caption.startswith("Старинный диван") for caption in external_hordus_choices())) timeout 5.0
    click id (external_hordus_button("Роскошное мыло")) pos (0.5, 0.5) until eval ("не хватает денег" in scene_runtime.text) timeout 20.0
    assert eval (player.economy.money == 0 and Hordus.last_trade_month == -1 and player.item_count("luxury_soap_001") == _hordus_soap_before) timeout 5.0
    $ player.set_money(100)
    click id (external_hordus_button("Роскошное мыло")) pos (0.5, 0.5) until eval (player.item_count("luxury_soap_001") == _hordus_soap_before + 1) timeout 20.0
    assert eval (player.economy.money == 55 and Hordus.last_trade_month == calendar_v2.cycle * 100 + calendar_v2.period) timeout 5.0
    click id (external_hordus_button("Пряная настойка")) pos (0.5, 0.5) until eval ("уже сделал выбор" in scene_runtime.text) timeout 20.0
    assert eval (player.economy.money == 55 and player.item_count("libido_tincture_001") == _hordus_tincture_before) timeout 5.0
    click id (external_hordus_button("Назад")) pos (0.5, 0.5) until eval ("Спросить о столице" in external_hordus_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "talk" and main_ui_runtime.selected_char == "hordus" and "Посмотреть товары" in external_hordus_choices()) timeout 5.0
    assert eval (scene_runtime.picture == "images/market/mistery_merchant.png") timeout 5.0
    click id (external_hordus_button("Закончить разговор")) pos (0.5, 0.5) until eval (not external_hordus_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "scene" and rooms.current_code == "MarketPlace") timeout 5.0

testcase external_hordus_sofa_prerequisites:
    parameter missing = ["paintings", "window", "glory", "forest"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    python:
        external_hordus_prepare(True)
        threads["claraPaintingsPath"].completed = missing != "paintings"
        player.tavern_management.client_room_hole = 0 if missing == "window" else 1
        player.tavern_management.glory_hole = 1 if missing == "glory" else 2
        threads["claraForestSofa"].num = 5 if missing == "forest" else 6
    run Call("IntHordusTalk")
    advance until eval ("Посмотреть товары" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Посмотреть товары")) pos (0.5, 0.5) until eval ("Назад" in external_hordus_choices()) timeout 20.0
    assert eval (not any(caption.startswith("Старинный диван") for caption in external_hordus_choices())) timeout 5.0
    click id (external_hordus_button("Назад")) pos (0.5, 0.5) until eval ("Спросить о столице" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Закончить разговор")) pos (0.5, 0.5) until eval (not external_hordus_choices()) timeout 20.0

testcase external_hordus_sofa_purchase_and_npc_presence:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    python:
        external_hordus_prepare(True)
        threads["claraPaintingsPath"].completed = True
        player.tavern_management.client_room_hole = 1
        player.tavern_management.glory_hole = 2
        Clara.rel = 5
        threads["claraBookletMarket"].advanceTo(threads["claraBookletMarket"].data.length, complete_at_end=True)
        threads["claraForestSofa"].advanceTo(6, force_active=True)
        player.set_money(599)
    run Call("IntHordusTalk")
    advance until eval ("Посмотреть товары" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Посмотреть товары")) pos (0.5, 0.5) until eval ("Назад" in external_hordus_choices()) timeout 20.0
    assert eval (any(caption.startswith("Старинный диван") for caption in external_hordus_choices())) timeout 5.0
    click id (external_hordus_button("Старинный диван")) pos (0.5, 0.5) until eval ("не хватает денег" in scene_runtime.text) timeout 20.0
    assert eval (not Sofa.installed and player.economy.money == 599 and Hordus.last_trade_month == -1) timeout 5.0
    $ player.set_money(600)
    click id (external_hordus_button("Старинный диван")) pos (0.5, 0.5) until eval (Sofa.installed) timeout 20.0
    assert eval (player.economy.money == 0 and player.item_count("cursed_sofa_001") == 0) timeout 5.0
    assert eval (not any(caption.startswith("Старинный диван") for caption in external_hordus_choices())) timeout 5.0
    assert eval (people.get_info("sofa") is Sofa and Sofa.registry_group == "secondary" and people.ids_at("TavernMain").count("sofa") == 1) timeout 5.0
    assert eval (not any(getattr(obj, "object_id", "") == "cursed_sofa_001" for obj in rooms.get("TavernMain").visible_objects())) timeout 5.0
    click id (external_hordus_button("Назад")) pos (0.5, 0.5) until eval ("Спросить о столице" in external_hordus_choices()) timeout 20.0
    click id (external_hordus_button("Закончить разговор")) pos (0.5, 0.5) until eval (not external_hordus_choices()) timeout 20.0
    run Jump("TavernMain")
    advance until eval (rooms.current_code == "TavernMain" and renpy.get_displayable("main_ui", "main_ui_entity_button_npc_sofa") is not None) timeout 20.0
    click id "main_ui_entity_button_npc_sofa" pos (0.5, 0.5)
    advance until eval ("Поговорить с диваном" in external_hordus_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "talk" and main_ui_runtime.selected_char == "sofa") timeout 5.0
    click id (external_hordus_button("Закончить разговор")) pos (0.5, 0.5) until eval (not external_hordus_choices()) timeout 20.0
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.is_file():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_hordus_market_"))
    try:
        isolated.TEST_RPY = TEST_RPY
        project = isolated.build_temp_project(isolated.project_root(), temp_root)
        print(f"Temporary Hordus market test project: {project}", flush=True)
        if args.compile_lint:
            for command in ("compile", "lint"):
                result = subprocess.run(
                    [str(renpy_exe), str(project), "--savedir", str(project / ".test-saves"), command],
                    text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                (project / f"hordus-{command}.log").write_text(result.stdout, encoding="utf-8")
                print(f"Ren'Py {command}: exit {result.returncode}; log {project / ('hordus-' + command + '.log')}", flush=True)
                if result.returncode:
                    isolated.safe_print(result.stdout)
                    return int(result.returncode)
        return isolated.run_renpy(renpy_exe, project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Hordus market test project: {temp_root}")
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_hordus_market_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            isolated.remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
