# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -40 python:
    import re

    def _coerce_panel_text_value(value):
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return _coerce_panel_text_value(value.get("text", ""))
        if isinstance(value, (list, tuple)):
            text_parts = []
            for part in value:
                part_text = _coerce_panel_text_value(part).strip()
                if part_text:
                    text_parts.append(part_text)
            return "\n\n".join(text_parts)
        if hasattr(value, "caption") and hasattr(value, "action"):
            return ""
        if isinstance(value, (int, float, bool)):
            return str(value)
        return ""

    def _normalize_tavern_event_text(text):
        value = _coerce_panel_text_value(text).replace("\r\n", "\n").replace("\r", "\n")
        value = re.sub(r"\n[ \t]+\n", "\n\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()

    def format_panel_paged_text(text, style_code="plain"):
        normalized = _normalize_tavern_event_text(text)
        if not normalized:
            return ""
        if str(style_code or "").lower() == "event":
            return "{b}{i}{color=#6d1020}" + normalized + "{/color}{/i}{/b}"
        return normalized

    def format_tavern_event_text(text):
        return format_panel_paged_text(text, "event")

label PartEventYourFirstReaction(GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR=0, HarassTypePEYFR=1, _help_caption=""):
    $ _help_caption = "Вмешаться и помочь {}".format(people_name(GirlNamePEYFR, 'dative', GirlNamePEYFR))
    show screen main_ui
    menu:
        "Не обращать внимания":
            call PartEventYourFirstReactionOutcome(GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR, HarassTypePEYFR, 1)

        "Стоять и смотреть":
            call PartEventYourFirstReactionOutcome(GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR, HarassTypePEYFR, 2)

        "[_help_caption]":
            call PartEventYourFirstReactionOutcome(GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR, HarassTypePEYFR, 3)
    return

label PartEventYourFirstReactionOutcome(GirlNamePEYFR, SecondPartFuncName, Eyewitness, HarassType, reaction_code=1, _player_reaction_text="", follow_text="", _followup_text=""):
    $ _player_reaction_text = ""

    if reaction_code == 1:
        $ _player_reaction_text = "Вы отвернулись от происходящего и пошли по своим делам."
    elif reaction_code == 2:
        $ _player_reaction_text = "Вы начали с интересом осматривать происходящее."
    else:
        $ _player_reaction_text = "Вы со всей поспешностью кинулись на выручку {}.".format(people_name(GirlNamePEYFR, 'dative'))

    call expression SecondPartFuncName pass (GirlNamePEYFR, Eyewitness, reaction_code, HarassType)
    $ follow_text = _coerce_panel_text_value(_return)

    $ _followup_text = _player_reaction_text
    if str(follow_text or "").strip():
        if str(_followup_text or "").strip():
            $ _followup_text += "\n\n" + str(follow_text)
        else:
            $ _followup_text = str(follow_text)

    $ scene_runtime.text = format_tavern_event_text(_followup_text)
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    return
