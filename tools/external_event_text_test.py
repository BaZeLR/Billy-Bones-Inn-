#!/usr/bin/env python3
"""Check actual event text rendering in an isolated Ren'Py game copy."""

from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

import external_tavern_premium_test as isolated


TEST_RPY = r'''
define external_event_text_speaker = Character("EXTERNAL_SPEAKER_NAME")

init python:
    def external_event_text_boxes():
        from renpy.test.testfocus import focus_from_displayable
        from renpy.text.text import Text

        rows = []
        seen = set()

        def collect(displayable):
            if id(displayable) in seen or not isinstance(displayable, Text):
                return
            seen.add(id(displayable))
            # The test engine's render-tree lookup excludes unrendered widgets.
            focus = focus_from_displayable(displayable)
            if focus is None:
                return
            content = "".join(part for part in displayable.text if isinstance(part, str))
            rows.append((content, focus.x, focus.y, focus.w, focus.h))

        for screen_name in ("main_ui", "say"):
            screen = renpy.get_screen(screen_name)
            if screen is not None:
                screen.visit_all(collect)
        return rows

    def external_event_text_count(sentinel):
        return sum(row[0].count(sentinel) for row in external_event_text_boxes())

    def external_event_text_position(sentinel):
        matches = [row for row in external_event_text_boxes() if sentinel in row[0]]
        if len(matches) != 1:
            return None
        return matches[0][1:3]

    def external_event_text_same_position(first, second):
        return first is not None and second is not None and all(
            abs(a - b) <= 1 for a, b in zip(first, second)
        )

    def external_prepare_event_text():
        rooms.enter("TavernSandraRoom")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.talk_picture = ""
        main_ui_runtime.action_title = "External event text test"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []
        scene_runtime.picture = tavern_sandra_room_picture()
        scene_runtime.text = "EXTERNAL_STATIC_ROOM_TEXT"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")
        renpy.restart_interaction()


label ExternalEventTextScenario(text_test_mode="scene"):
    if text_test_mode == "talk":
        $ main_ui_begin_talk_state("External event text test", "georgett")
    else:
        $ main_ui_begin_native_scene_state("External event text test")
    show screen main_ui
    "EXTERNAL_EVENT_FIRST_LINE"
    "EXTERNAL_EVENT_SECOND_LINE"
    menu:
        "Continue with explicit menu text":
            pass
    $ scene_runtime.text = "EXTERNAL_EVENT_MENU_TEXT"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Finish external event test":
            pass
    if text_test_mode == "talk":
        $ main_ui_end_talk_state()
    else:
        $ main_ui_end_native_scene_state()
    return


label ExternalStandaloneTextScenario:
    hide screen main_ui
    "EXTERNAL_STANDALONE_FIRST_LINE"
    external_event_text_speaker "EXTERNAL_STANDALONE_NAMED_LINE"
    $ _external_standalone_returned = True
    show screen main_ui
    return


testsuite global:
    teardown:
        exit
'''


for mode in ("scene", "talk"):
    TEST_RPY += r'''

testcase external_event_text_MODE:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ external_prepare_event_text()
    assert eval (external_event_text_count("EXTERNAL_STATIC_ROOM_TEXT") == 1) timeout 5.0
    run Call("ExternalEventTextScenario", "MODE")
    advance until eval (external_event_text_count("EXTERNAL_EVENT_FIRST_LINE") == 1) timeout 20.0
    assert eval (external_event_text_count("EXTERNAL_STATIC_ROOM_TEXT") == 0) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_FIRST_LINE") == 1) timeout 5.0
    $ _external_first_text_position = external_event_text_position("EXTERNAL_EVENT_FIRST_LINE")
    advance until eval (external_event_text_count("EXTERNAL_EVENT_SECOND_LINE") == 1) timeout 20.0
    assert eval (external_event_text_count("EXTERNAL_STATIC_ROOM_TEXT") == 0) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_FIRST_LINE") == 0) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_SECOND_LINE") == 1) timeout 5.0
    assert eval (external_event_text_same_position(_external_first_text_position, external_event_text_position("EXTERNAL_EVENT_SECOND_LINE"))) timeout 5.0
    advance until screen "choice" timeout 20.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_SECOND_LINE") == 1) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_STATIC_ROOM_TEXT") == 0) timeout 5.0
    assert eval (str(scene_runtime.text or "") == "EXTERNAL_EVENT_SECOND_LINE" and str(scene_runtime.location_text or "") == "EXTERNAL_STATIC_ROOM_TEXT") timeout 5.0
    assert eval (external_event_text_same_position(_external_first_text_position, external_event_text_position("EXTERNAL_EVENT_SECOND_LINE"))) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (external_event_text_count("EXTERNAL_EVENT_MENU_TEXT") == 1) timeout 20.0
    assert eval (external_event_text_count("EXTERNAL_STATIC_ROOM_TEXT") == 0) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_SECOND_LINE") == 0) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_MENU_TEXT") == 1) timeout 5.0
    $ print("EVENT_TEXT MODE first=%r menu=%r" % (_external_first_text_position, external_event_text_position("EXTERNAL_EVENT_MENU_TEXT")))
    assert eval (external_event_text_same_position(_external_first_text_position, external_event_text_position("EXTERNAL_EVENT_MENU_TEXT"))) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (external_event_text_count("EXTERNAL_STATIC_ROOM_TEXT") == 1) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_MENU_TEXT") == 0) timeout 5.0
    assert eval (main_ui_runtime.scene_origin is None and main_ui_runtime.talk_origin is None) timeout 5.0
'''.replace("MODE", mode)


TEST_RPY += r'''

testcase external_event_text_callback_save:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ external_prepare_event_text()
    assert eval (main_ui_dialogue_text.__name__ == "main_ui_dialogue_text" and main_ui_dialogue_text.__module__ == "store") timeout 5.0
    assert eval (sum(callback is main_ui_dialogue_text for callback in config.all_character_callbacks) == 1) timeout 5.0
    $ _external_callback_copy = renpy.compat.pickle.loads(renpy.compat.pickle.dumps([main_ui_dialogue_text]))
    assert eval (_external_callback_copy == [main_ui_dialogue_text]) timeout 5.0
    run Call("ExternalEventTextScenario", "scene")
    advance until eval (external_event_text_count("EXTERNAL_EVENT_FIRST_LINE") == 1) timeout 20.0
    assert eval (str(scene_runtime.text or "") == "EXTERNAL_EVENT_FIRST_LINE" and str(scene_runtime.location_text or "") == "EXTERNAL_STATIC_ROOM_TEXT") timeout 5.0
    advance until eval (external_event_text_count("EXTERNAL_EVENT_SECOND_LINE") == 1) timeout 20.0
    advance until screen "choice" timeout 20.0
    $ renpy.save("external-event-text-callback", include_screenshot=False)
    assert eval (renpy.can_load("external-event-text-callback")) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_EVENT_SECOND_LINE") == 1) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (external_event_text_count("EXTERNAL_EVENT_MENU_TEXT") == 1) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (external_event_text_count("EXTERNAL_STATIC_ROOM_TEXT") == 1) timeout 5.0

testcase external_standalone_say_still_owns_required_widgets:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ _external_standalone_returned = False
    run Call("ExternalStandaloneTextScenario")
    advance until eval (external_event_text_count("EXTERNAL_STANDALONE_FIRST_LINE") == 1) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is None) timeout 5.0
    assert eval (renpy.get_displayable("say", "what") is not None and renpy.get_displayable("say", "window") is not None) timeout 5.0
    advance until eval (external_event_text_count("EXTERNAL_STANDALONE_NAMED_LINE") == 1) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is None) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_STANDALONE_FIRST_LINE") == 0) timeout 5.0
    assert eval (external_event_text_count("EXTERNAL_SPEAKER_NAME") == 1) timeout 5.0
    assert eval (renpy.get_displayable("say", "who") is not None and renpy.get_displayable("say", "what") is not None and renpy.get_displayable("say", "window") is not None) timeout 5.0
    advance until eval (_external_standalone_returned) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None) timeout 5.0
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.is_file():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")

    temp_root = Path(tempfile.mkdtemp(prefix="tractir_event_text_"))
    try:
        # Reuse the established isolated-project builder with this test payload.
        isolated.TEST_RPY = TEST_RPY
        project = isolated.build_temp_project(isolated.project_root(), temp_root)
        print(f"Temporary event text test project: {project}")
        return isolated.run_renpy(renpy_exe, project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary event text test project: {temp_root}")
        else:
            isolated.remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
