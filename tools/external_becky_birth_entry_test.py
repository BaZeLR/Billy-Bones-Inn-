#!/usr/bin/env python3
"""Run pregnancy entry regressions through the existing isolated Ren'Py harness."""

import external_becky_branch_test as harness


SETUP = '''
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 19
        calendar_v2.minute = 0
        daily_events.rows = []
        event_runtime.fired_keys_today = []
        threads["beckyHome"].advanceTo(3, complete_at_end=True)
        threads["beckyEddieSex"].reset()
        threads["sandraWeeklyEvaluation"].advanceTo(4, force_active=True)
        Becky.rel = 20
        Becky.set_sex_stat("pregnancy", 0)
        Inga.set_sex_stat("pregnancy", 0)
        Inga.acquaintance_stage = 2
        player.appearance.current_dress = "citydress"
'''


DELIVERY = '''
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
''' + '''
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
''' * 7 + '''
    assert eval (_test_birth_info.pregnancy_days() == 0)
    assert eval (int(_test_birth_info.sex_stat("kids", 0)) == _test_kids_before + 1)
    assert eval (daily_events.exists(_test_birth_girl, "GiveBirth") == 0)
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until screen "nextday_report_card_overlay" timeout 60.0
    scroll amount 20 pos (960, 500)
    click id "nextday_report_back_button" pos (0.5, 0.5) until eval (renpy.get_screen("nextday_report_card_overlay") is None) timeout 20.0
    advance until screen "main_ui" timeout 30.0
    assert eval (rooms.current_code == "TavernMyRoom")
    assert eval (_test_birth_info.pregnancy_days() == 0)
    assert eval (int(_test_birth_info.sex_stat("kids", 0)) == _test_kids_before + 1)
    assert eval (daily_events.exists(_test_birth_girl, "GiveBirth") == 0)
'''


def birth_cases():
    cases = ['testsuite global:\n    teardown:\n        exit\n']
    for girl in ("becky", "inga"):
        cases.append('testcase %s_scheduled_birth_at_normal_home_entry:\n' % girl + SETUP + '''
    python:
        _test_birth_girl = "%s"
        _test_birth_info = people.get_info(_test_birth_girl)
        _test_birth_info.set_sex_stat("pregnancy", 241)
        _test_birth_info.set_sex_stat("pregfather", "You")
        _test_kids_before = int(_test_birth_info.sex_stat("kids", 0))
        daily_events.add(_test_birth_girl, "alllocs", -1, ">", 1, 9999, "GiveBirth", "GiveBirth", "girl")
        initStoryEventRuntime(True)
    run Call("BeckyHome", "")
    advance until screen "choice" timeout 20.0
    assert eval (GirlName == _test_birth_girl)
    assert eval (any(item.caption == "Идти в храм" for item in renpy.get_screen("choice").scope["items"]))
    assert eval (daily_events.exists(_test_birth_girl, "GiveBirth") == 0)
    assert eval (_test_birth_info.pregnancy_days() == 241)
    assert eval (int(_test_birth_info.sex_stat("kids", 0)) == _test_kids_before)
''' % girl + DELIVERY)
        cases.append('testcase %s_offscreen_birth_at_normal_home_entry:\n' % girl + SETUP + '''
    python:
        _test_birth_girl = "%s"
        _test_birth_info = people.get_info(_test_birth_girl)
        _test_birth_info.set_sex_stat("pregnancy", 285)
        _test_birth_info.set_sex_stat("pregfather", "You")
        _test_kids_before = int(_test_birth_info.sex_stat("kids", 0))
        daily_events.add(_test_birth_girl, "alllocs", -1, ">", 1, 9999, "GiveBirth", "CreateKid", "girl_location")
        initStoryEventRuntime(True)
    run Call("BeckyHome", "")
    advance until screen "choice" timeout 20.0
    assert eval (daily_events.exists(_test_birth_girl, "GiveBirth") == 0)
    assert eval (_test_birth_info.pregnancy_days() == 0)
    assert eval (int(_test_birth_info.sex_stat("kids", 0)) == _test_kids_before + 1)
    assert eval (rooms.current_code == "BeckyHome")
    assert eval (not story_event_available("BeckyHome", "enter"))
''' % girl)
    cases.append('testcase late_pregnancy_without_due_row_does_not_start_birth:\n' + SETUP + '''
    python:
        Becky.set_sex_stat("pregnancy", 285)
        Becky.set_sex_stat("pregfather", "You")
        initStoryEventRuntime(True)
    run Call("BeckyHome", "")
    advance until screen "choice" timeout 20.0
    assert eval (not any(item.caption == "Идти в храм" for item in renpy.get_screen("choice").scope["items"]))
    assert eval (Becky.pregnancy_days() == 285)
    assert eval (not story_event_available("BeckyHome", "enter"))
''')
    cases.append('testcase amanda_typed_birth_requires_and_consumes_the_daily_row:\n' + SETUP + '''
    python:
        Amanda.set_sex_stat("pregnancy", 285)
        Amanda.set_sex_stat("pregfather", "")
        _test_kids_before = int(Amanda.sex_stat("kids", 0))
    assert eval (isinstance(AmandaBirth, AmandaBirthEvent))
    assert eval (not Amanda.birth_ready() and not AmandaBirth.checkAmandaConditions())
    python:
        daily_events.add("amanda", "alllocs", -1, ">", 1, 9999, "GiveBirth", "GiveBirth", "girl")
        rooms.enter("TavernMain")
        initStoryEventRuntime(True)
    assert eval (Amanda.birth_ready() and AmandaBirth.checkAmandaConditions())
    assert eval (story_event_available("TavernMain", "enter"))
    assert eval (event_runtime.available["TavernMain"]["enter"].target == "story_amanda_give_birth_0")
    run Call("checkTriggers", "TavernMain", "enter", 0)
    advance until screen "choice" timeout 20.0
    assert eval (GirlName == "amanda")
    assert eval (any(item.caption == "Идти в храм" for item in renpy.get_screen("choice").scope["items"]))
    assert eval (daily_events.exists("amanda", "GiveBirth") == 0)
    assert eval (not Amanda.birth_ready())
    assert eval (Amanda.pregnancy_days() == 285 and int(Amanda.sex_stat("kids", 0)) == _test_kids_before)
''')
    for callback, mode in (("GiveBirth", "girl"), ("CreateKid", "girl_location")):
        cases.append('testcase stale_%s_row_is_discarded_without_another_child:\n' % callback.lower() + SETUP + '''
    python:
        _test_kids_before = int(Becky.sex_stat("kids", 0))
        daily_events.add("becky", "alllocs", -1, ">", 1, 9999, "GiveBirth", "%s", "%s")
    run Call("story_give_birth_becky")
    advance until screen "main_ui" timeout 20.0
    assert eval (daily_events.exists("becky", "GiveBirth") == 0)
    assert eval (Becky.pregnancy_days() == 0)
    assert eval (int(Becky.sex_stat("kids", 0)) == _test_kids_before)
''' % (callback, mode))
    return "\n".join(cases)


if __name__ == "__main__":
    harness.TEST_RPY = birth_cases()
    raise SystemExit(harness.main())
