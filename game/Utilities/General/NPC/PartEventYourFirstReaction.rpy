    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default tavern_event_panel_raw_text = ""
default tavern_event_pages = []
default tavern_event_page_index = 0
default tavern_event_next_title = ""
default tavern_event_next_items = []
default panel_paged_raw_text = ""
default panel_paged_pages = []
default panel_paged_page_index = 0
default panel_paged_next_title = ""
default panel_paged_next_items = []
default panel_paged_style = "plain"
default panel_paged_pending_text = ""
default panel_paged_pending_title = ""
default panel_paged_pending_items = []
default panel_paged_pending_style = "plain"

default tavern_event_panel_raw_text = ""
default tavern_event_pages = []
default tavern_event_page_index = 0
default tavern_event_next_title = ""
default tavern_event_next_items = []
default panel_paged_raw_text = ""
default panel_paged_pages = []
default panel_paged_page_index = 0
default panel_paged_next_title = ""
default panel_paged_next_items = []
default panel_paged_style = "plain"
default panel_paged_pending_text = ""
default panel_paged_pending_title = ""
default panel_paged_pending_items = []
default panel_paged_pending_style = "plain"

default tavern_event_panel_raw_text = ""
default tavern_event_pages = []
default tavern_event_page_index = 0
default tavern_event_next_title = ""
default tavern_event_next_items = []
default panel_paged_raw_text = ""
default panel_paged_pages = []
default panel_paged_page_index = 0
default panel_paged_next_title = ""
default panel_paged_next_items = []
default panel_paged_style = "plain"
default panel_paged_pending_text = ""
default panel_paged_pending_title = ""
default panel_paged_pending_items = []
default panel_paged_pending_style = "plain"

init -40 python:
    import re
    import renpy
    import renpy
    import renpy

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

    def set_panel_paged_text(text, style_code=None):
        normalized = _normalize_tavern_event_text(text)
        renpy.store.panel_paged_raw_text = normalized
        renpy.store.MainTxt = format_panel_paged_text(normalized, style_code or getattr(renpy.store, "panel_paged_style", "plain"))
        renpy.store.CurLocDesc = renpy.store.MainTxt

    def set_tavern_event_panel_text(text):
        normalized = _normalize_tavern_event_text(text)
        renpy.store.tavern_event_panel_raw_text = normalized
        set_panel_paged_text(normalized, "event")

    def append_tavern_event_panel_text(text):
        chunk = _normalize_tavern_event_text(text)
        if not chunk:
            return
        current = _normalize_tavern_event_text(getattr(renpy.store, "tavern_event_panel_raw_text", ""))
        if current:
            current = current + "\n\n" + chunk
        else:
            current = chunk
        set_tavern_event_panel_text(current)

    def _split_tavern_event_paragraph(paragraph, page_limit=420):
        paragraph = _normalize_tavern_event_text(paragraph)
        if not paragraph:
            return []
        if len(paragraph) <= page_limit:
            return [paragraph]

        pages = []
        sentences = [part.strip() for part in re.findall(r'[^.!?…]+(?:[.!?…]+["»”]?|$)', paragraph) if part.strip()]
        if len(sentences) <= 1:
            sentences = paragraph.split()

        current = ""
        for sentence in sentences:
            candidate = sentence if not current else current + " " + sentence
            if current and len(candidate) > page_limit:
                pages.append(current.strip())
                current = sentence
            else:
                current = candidate

        if current.strip():
            pages.append(current.strip())

        return pages or [paragraph]

    def build_tavern_event_pages(text, page_limit=420):
        normalized = _normalize_tavern_event_text(text)
        if not normalized:
            return [""]

        pages = []
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]
        for paragraph in paragraphs:
            pages.extend(_split_tavern_event_paragraph(paragraph, page_limit))

        return pages or [normalized]

    def stage_paged_panel_text(panel_text="", next_title="", next_items=None, style_code="plain"):
        raw_text = _coerce_panel_text_value(panel_text)
        renpy.store.panel_paged_pending_text = str(raw_text or "")
        renpy.store.panel_paged_pending_title = str(next_title or "")
        renpy.store.panel_paged_pending_items = list(next_items or [])
        renpy.store.panel_paged_pending_style = str(style_code or "plain")

    def stage_tavern_event_pages(event_text="", next_title="", next_items=None):
        stage_paged_panel_text(event_text, next_title, next_items, "event")

    def apply_paged_panel_state():
        pages = list(getattr(renpy.store, "panel_paged_pages", []) or [])
        if len(pages) == 0:
            pages = [""]
            renpy.store.panel_paged_pages = pages

        page_index = int(getattr(renpy.store, "panel_paged_page_index", 0) or 0)
        if page_index < 0:
            page_index = 0
        if page_index >= len(pages):
            page_index = len(pages) - 1
        renpy.store.panel_paged_page_index = page_index

        set_panel_paged_text(pages[page_index], getattr(renpy.store, "panel_paged_style", "plain"))
        renpy.store.current_action_content = None

        if page_index < (len(pages) - 1):
            renpy.store.current_action_title = ""
            renpy.store.current_action_items = [MenuItem("Продолжить", Function(advance_paged_panel_text))]
        else:
            renpy.store.current_action_title = str(getattr(renpy.store, "panel_paged_next_title", "") or "")
            renpy.store.current_action_items = list(getattr(renpy.store, "panel_paged_next_items", []) or [])

    def advance_paged_panel_text():
        page_index = int(getattr(renpy.store, "panel_paged_page_index", 0) or 0)
        pages = list(getattr(renpy.store, "panel_paged_pages", []) or [])
        if page_index < (len(pages) - 1):
            renpy.store.panel_paged_page_index = page_index + 1
        apply_paged_panel_state()
        renpy.restart_interaction()

label QueueTavernEventPages(event_text="", next_title="", next_items=None):
    $ stage_tavern_event_pages(event_text, next_title, next_items)
    call QueuePagedPanelTextFromStore
    return MainTxt

label QueuePagedPanelText(panel_text="", next_title="", next_items=None, style_code="plain"):
    $ stage_paged_panel_text(panel_text, next_title, next_items, style_code)
    call QueuePagedPanelTextFromStore
    return MainTxt

label QueuePagedPanelTextFromStore:
    $ panel_paged_pages = build_tavern_event_pages(panel_paged_pending_text)
    $ panel_paged_page_index = 0
    $ panel_paged_next_title = str(panel_paged_pending_title or "")
    $ panel_paged_next_items = list(panel_paged_pending_items or [])
    $ panel_paged_style = str(panel_paged_pending_style or "plain")
    call ApplyPagedPanelState
    return MainTxt

label ApplyPagedPanelState:
    $ apply_paged_panel_state()
    return

label AdvancePagedPanelText:
    $ advance_paged_panel_text()
    return

label ApplyTavernEventPageState:
    call ApplyPagedPanelState
    return

label AdvanceTavernEventPage:
    call AdvancePagedPanelText
    return

    def set_panel_paged_text(text, style_code=None):
        normalized = _normalize_tavern_event_text(text)
        renpy.store.panel_paged_raw_text = normalized
        renpy.store.MainTxt = format_panel_paged_text(normalized, style_code or getattr(renpy.store, "panel_paged_style", "plain"))
        renpy.store.CurLocDesc = renpy.store.MainTxt

    def set_tavern_event_panel_text(text):
        normalized = _normalize_tavern_event_text(text)
        renpy.store.tavern_event_panel_raw_text = normalized
        set_panel_paged_text(normalized, "event")

    def append_tavern_event_panel_text(text):
        chunk = _normalize_tavern_event_text(text)
        if not chunk:
            return
        current = _normalize_tavern_event_text(getattr(renpy.store, "tavern_event_panel_raw_text", ""))
        if current:
            current = current + "\n\n" + chunk
        else:
            current = chunk
        set_tavern_event_panel_text(current)

    def _split_tavern_event_paragraph(paragraph, page_limit=420):
        paragraph = _normalize_tavern_event_text(paragraph)
        if not paragraph:
            return []
        if len(paragraph) <= page_limit:
            return [paragraph]

        pages = []
        sentences = [part.strip() for part in re.findall(r'[^.!?…]+(?:[.!?…]+["»”]?|$)', paragraph) if part.strip()]
        if len(sentences) <= 1:
            sentences = paragraph.split()

        current = ""
        for sentence in sentences:
            candidate = sentence if not current else current + " " + sentence
            if current and len(candidate) > page_limit:
                pages.append(current.strip())
                current = sentence
            else:
                current = candidate

        if current.strip():
            pages.append(current.strip())

        return pages or [paragraph]

    def build_tavern_event_pages(text, page_limit=420):
        normalized = _normalize_tavern_event_text(text)
        if not normalized:
            return [""]

        pages = []
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]
        for paragraph in paragraphs:
            pages.extend(_split_tavern_event_paragraph(paragraph, page_limit))

        return pages or [normalized]

    def stage_paged_panel_text(panel_text="", next_title="", next_items=None, style_code="plain"):
        raw_text = _coerce_panel_text_value(panel_text)
        renpy.store.panel_paged_pending_text = str(raw_text or "")
        renpy.store.panel_paged_pending_title = str(next_title or "")
        renpy.store.panel_paged_pending_items = list(next_items or [])
        renpy.store.panel_paged_pending_style = str(style_code or "plain")

    def stage_tavern_event_pages(event_text="", next_title="", next_items=None):
        stage_paged_panel_text(event_text, next_title, next_items, "event")

    def apply_paged_panel_state():
        pages = list(getattr(renpy.store, "panel_paged_pages", []) or [])
        if len(pages) == 0:
            pages = [""]
            renpy.store.panel_paged_pages = pages

        page_index = int(getattr(renpy.store, "panel_paged_page_index", 0) or 0)
        if page_index < 0:
            page_index = 0
        if page_index >= len(pages):
            page_index = len(pages) - 1
        renpy.store.panel_paged_page_index = page_index

        set_panel_paged_text(pages[page_index], getattr(renpy.store, "panel_paged_style", "plain"))
        renpy.store.current_action_content = None

        if page_index < (len(pages) - 1):
            renpy.store.current_action_title = ""
            renpy.store.current_action_items = [MenuItem("Продолжить", Function(advance_paged_panel_text))]
        else:
            renpy.store.current_action_title = str(getattr(renpy.store, "panel_paged_next_title", "") or "")
            renpy.store.current_action_items = list(getattr(renpy.store, "panel_paged_next_items", []) or [])

    def advance_paged_panel_text():
        page_index = int(getattr(renpy.store, "panel_paged_page_index", 0) or 0)
        pages = list(getattr(renpy.store, "panel_paged_pages", []) or [])
        if page_index < (len(pages) - 1):
            renpy.store.panel_paged_page_index = page_index + 1
        apply_paged_panel_state()
        renpy.restart_interaction()

label QueueTavernEventPages(event_text="", next_title="", next_items=None):
    $ stage_tavern_event_pages(event_text, next_title, next_items)
    call QueuePagedPanelTextFromStore
    return MainTxt

label QueuePagedPanelText(panel_text="", next_title="", next_items=None, style_code="plain"):
    $ stage_paged_panel_text(panel_text, next_title, next_items, style_code)
    call QueuePagedPanelTextFromStore
    return MainTxt

label QueuePagedPanelTextFromStore:
    $ panel_paged_pages = build_tavern_event_pages(panel_paged_pending_text)
    $ panel_paged_page_index = 0
    $ panel_paged_next_title = str(panel_paged_pending_title or "")
    $ panel_paged_next_items = list(panel_paged_pending_items or [])
    $ panel_paged_style = str(panel_paged_pending_style or "plain")
    call ApplyPagedPanelState
    return MainTxt

label ApplyPagedPanelState:
    $ apply_paged_panel_state()
    return

label AdvancePagedPanelText:
    $ advance_paged_panel_text()
    return

label ApplyTavernEventPageState:
    call ApplyPagedPanelState
    return

label AdvanceTavernEventPage:
    call AdvancePagedPanelText
    return

    def set_panel_paged_text(text, style_code=None):
        normalized = _normalize_tavern_event_text(text)
        renpy.store.panel_paged_raw_text = normalized
        renpy.store.MainTxt = format_panel_paged_text(normalized, style_code or getattr(renpy.store, "panel_paged_style", "plain"))
        renpy.store.CurLocDesc = renpy.store.MainTxt

    def set_tavern_event_panel_text(text):
        normalized = _normalize_tavern_event_text(text)
        renpy.store.tavern_event_panel_raw_text = normalized
        set_panel_paged_text(normalized, "event")

    def append_tavern_event_panel_text(text):
        chunk = _normalize_tavern_event_text(text)
        if not chunk:
            return
        current = _normalize_tavern_event_text(getattr(renpy.store, "tavern_event_panel_raw_text", ""))
        if current:
            current = current + "\n\n" + chunk
        else:
            current = chunk
        set_tavern_event_panel_text(current)

    def _split_tavern_event_paragraph(paragraph, page_limit=420):
        paragraph = _normalize_tavern_event_text(paragraph)
        if not paragraph:
            return []
        if len(paragraph) <= page_limit:
            return [paragraph]

        pages = []
        sentences = [part.strip() for part in re.findall(r'[^.!?…]+(?:[.!?…]+["»”]?|$)', paragraph) if part.strip()]
        if len(sentences) <= 1:
            sentences = paragraph.split()

        current = ""
        for sentence in sentences:
            candidate = sentence if not current else current + " " + sentence
            if current and len(candidate) > page_limit:
                pages.append(current.strip())
                current = sentence
            else:
                current = candidate

        if current.strip():
            pages.append(current.strip())

        return pages or [paragraph]

    def build_tavern_event_pages(text, page_limit=420):
        normalized = _normalize_tavern_event_text(text)
        if not normalized:
            return [""]

        pages = []
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]
        for paragraph in paragraphs:
            pages.extend(_split_tavern_event_paragraph(paragraph, page_limit))

        return pages or [normalized]

    def stage_paged_panel_text(panel_text="", next_title="", next_items=None, style_code="plain"):
        raw_text = _coerce_panel_text_value(panel_text)
        renpy.store.panel_paged_pending_text = str(raw_text or "")
        renpy.store.panel_paged_pending_title = str(next_title or "")
        renpy.store.panel_paged_pending_items = list(next_items or [])
        renpy.store.panel_paged_pending_style = str(style_code or "plain")

    def stage_tavern_event_pages(event_text="", next_title="", next_items=None):
        stage_paged_panel_text(event_text, next_title, next_items, "event")

    def apply_paged_panel_state():
        pages = list(getattr(renpy.store, "panel_paged_pages", []) or [])
        if len(pages) == 0:
            pages = [""]
            renpy.store.panel_paged_pages = pages

        page_index = int(getattr(renpy.store, "panel_paged_page_index", 0) or 0)
        if page_index < 0:
            page_index = 0
        if page_index >= len(pages):
            page_index = len(pages) - 1
        renpy.store.panel_paged_page_index = page_index

        set_panel_paged_text(pages[page_index], getattr(renpy.store, "panel_paged_style", "plain"))
        renpy.store.current_action_content = None

        if page_index < (len(pages) - 1):
            renpy.store.current_action_title = ""
            renpy.store.current_action_items = [MenuItem("Продолжить", Function(advance_paged_panel_text))]
        else:
            renpy.store.current_action_title = str(getattr(renpy.store, "panel_paged_next_title", "") or "")
            renpy.store.current_action_items = list(getattr(renpy.store, "panel_paged_next_items", []) or [])

    def advance_paged_panel_text():
        page_index = int(getattr(renpy.store, "panel_paged_page_index", 0) or 0)
        pages = list(getattr(renpy.store, "panel_paged_pages", []) or [])
        if page_index < (len(pages) - 1):
            renpy.store.panel_paged_page_index = page_index + 1
        apply_paged_panel_state()
        renpy.restart_interaction()

label QueueTavernEventPages(event_text="", next_title="", next_items=None):
    $ stage_tavern_event_pages(event_text, next_title, next_items)
    call QueuePagedPanelTextFromStore
    return MainTxt

label QueuePagedPanelText(panel_text="", next_title="", next_items=None, style_code="plain"):
    $ stage_paged_panel_text(panel_text, next_title, next_items, style_code)
    call QueuePagedPanelTextFromStore
    return MainTxt

label QueuePagedPanelTextFromStore:
    $ panel_paged_pages = build_tavern_event_pages(panel_paged_pending_text)
    $ panel_paged_page_index = 0
    $ panel_paged_next_title = str(panel_paged_pending_title or "")
    $ panel_paged_next_items = list(panel_paged_pending_items or [])
    $ panel_paged_style = str(panel_paged_pending_style or "plain")
    call ApplyPagedPanelState
    return MainTxt

label ApplyPagedPanelState:
    $ apply_paged_panel_state()
    return

label AdvancePagedPanelText:
    $ advance_paged_panel_text()
    return

label ApplyTavernEventPageState:
    call ApplyPagedPanelState
    return

label AdvanceTavernEventPage:
    call AdvancePagedPanelText
    return

label PartEventYourFirstReaction(GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR=0, HarassTypePEYFR=1):
    $ YourReaction1 = 0
    $ _reaction_choices = []
    $ _reaction_choices.append(MenuItem("Не обращать внимания", [SetVariable("current_action_items", []), Call("PartEventYourFirstReactionApply", GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR, HarassTypePEYFR, 1)]))
    $ _reaction_choices.append(MenuItem("Стоять и смотреть", [SetVariable("current_action_items", []), Call("PartEventYourFirstReactionApply", GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR, HarassTypePEYFR, 2)]))
    $ _reaction_choices.append(MenuItem("Вмешаться и помочь {}".format(RealName3.get(GirlNamePEYFR, GirlNamePEYFR)), [SetVariable("current_action_items", []), Call("PartEventYourFirstReactionApply", GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR, HarassTypePEYFR, 3)]))
    $ Result = {"title": "Что вы будете делать?", "items": _reaction_choices}
    return Result

label PartEventYourFirstReactionApply(GirlNamePEYFR, SecondPartFuncName, Eyewitness, HarassType, reaction_code=1):
    $ YourReaction1 = reaction_code
    $ _player_reaction_text = ""

    if reaction_code == 1:
        $ _player_reaction_text = "Вы отвернулись от происходящего и пошли по своим делам."
    elif reaction_code == 2:
        $ _player_reaction_text = "Вы начали с интересом осматривать происходящее."
    else:
        $ _player_reaction_text = "Вы со всей поспешностью кинулись на выручку {}.".format(RealName3.get(GirlNamePEYFR, GirlNamePEYFR))

    call expression SecondPartFuncName pass (GirlNamePEYFR, Eyewitness, YourReaction1, HarassType)
    $ _follow_data = _return
    if isinstance(_follow_data, dict):
        $ follow_text = _coerce_panel_text_value(_follow_data.get("text", ""))
        $ _next_title = str(_follow_data.get("title", _next_title) or _next_title)
        $ _next_items = list(_follow_data.get("items", _next_items) or _next_items)
    else:
        $ follow_text = _coerce_panel_text_value(_follow_data)

    $ _followup_text = _player_reaction_text
    if str(follow_text or "").strip():
        if str(_followup_text or "").strip():
            $ _followup_text += "\n\n" + str(follow_text)
        else:
            $ _followup_text = str(follow_text)

    $ stage_tavern_event_pages(_followup_text, _next_title, _next_items)
    $ TavernMainBlockEvents = 1
    call QueuePagedPanelTextFromStore
    call ReturnToMainUI
    return


label PartEventYourFirstReactionShow(GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR=0, HarassTypePEYFR=1, reaction_code=1):
    call PartEventYourFirstReactionApply(GirlNamePEYFR, SecondPartFuncName, EyewitnessPEYFR, HarassTypePEYFR, reaction_code)
    return
