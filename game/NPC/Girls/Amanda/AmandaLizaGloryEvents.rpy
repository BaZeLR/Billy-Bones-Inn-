label story_amanda_liza_talk_work_0:
    $ renpy.dynamic("_amanda_liza_work_row", "_amanda_liza_event_text")
    $ _amanda_liza_work_row = tavern_work_pop_planned_code("AmandaLizaTalk", calendar_v2.time_slot(), True, "TavernMain")
    if not _amanda_liza_work_row:
        return False
    call EventAmandaLizettTalk(1)
    $ _amanda_liza_event_text = str(_return or "")
    if str(_amanda_liza_event_text or "").strip():
        $ scene_runtime.text = _amanda_liza_event_text
        $ scene_runtime.location_text = scene_runtime.text
    return True
