# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import os
    import re
    import renpy.exports as renpy

    _FRAN_PHRASE_CACHE = None

    def _fran_read_source_text():
        text = ""
        rel_path = "Inn/FrancheskaTalk.txt"
        # Use Ren'Py VFS loader first (works for packed/unpacked projects).
        try:
            if renpy.loadable(rel_path):
                raw = renpy.file(rel_path).read()
                for enc in ("utf-8", "utf-8-sig", "cp1251"):
                    try:
                        text = raw.decode(enc)
                        break
                    except Exception:
                        text = ""
        except Exception:
            text = ""

        if text:
            return text

        # Fallback to direct filesystem read.
        root_dir = os.path.dirname(renpy.config.gamedir)
        for path in (
            os.path.join(renpy.config.gamedir, "Inn", "FrancheskaTalk.txt"),
            os.path.join(root_dir, "textLocRef", "FrancheskaTalk.txt"),
            os.path.join(renpy.config.gamedir, "textLocRef", "FrancheskaTalk.txt"),
        ):
            for enc in ("utf-8", "utf-8-sig", "cp1251"):
                try:
                    with open(path, "r", encoding=enc) as fh:
                        text = fh.read()
                    break
                except Exception:
                    text = ""
            if text:
                break
        return text

    def _fran_normalize_text(raw):
        val = str(raw or "")
        val = val.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
        return val.strip()

    def _fran_extract_phrase_map(source_text, var_name):
        out = {}
        # Capture QSP single-quoted payloads, including doubled quote escapes.
        pattern = r"\$%s\[(\d+)\]='((?:''|[^'])*)'" % re.escape(var_name)
        for m in re.finditer(pattern, source_text, flags=re.S):
            idx = int(m.group(1))
            out[idx] = _fran_normalize_text(m.group(2).replace("''", "'"))
        return out

    def _fran_extract_phrase_single(source_text, var_name, idx):
        # Exact-index fallback for cases where bulk map extraction misses an entry.
        pattern = (
            r"\$%s\[%d\]='(.*?)'\s*(?=\r?\n\s*\$|\r?\n\s*GS\s+'Menu\.Create'|$)"
            % (re.escape(str(var_name or "")), int(idx or 0))
        )
        m = re.search(pattern, str(source_text or ""), flags=re.S)
        if not m:
            return ""
        return _fran_normalize_text(m.group(1).replace("''", "'"))

    def _fran_load_phrases():
        global _FRAN_PHRASE_CACHE
        if (
            isinstance(_FRAN_PHRASE_CACHE, dict)
            and isinstance(_FRAN_PHRASE_CACHE.get("main", None), dict)
            and len(_FRAN_PHRASE_CACHE.get("main", {})) > 0
        ):
            return _FRAN_PHRASE_CACHE

        source = _fran_read_source_text()
        start_map = _fran_extract_phrase_map(source, "FranPhraseStart")
        second_map = _fran_extract_phrase_map(source, "FranPhraseSecond")
        main_map = _fran_extract_phrase_map(source, "FranPhrase")

        # In TXT several second-phrases are aliases to start-phrases.
        for m in re.finditer(
            r"\$FranPhraseSecond\[(\d+)\]=\$FranPhraseStart\[(\d+)\]",
            source,
            flags=re.S,
        ):
            second_idx = int(m.group(1))
            start_idx = int(m.group(2))
            if second_idx not in second_map and start_idx in start_map:
                second_map[second_idx] = start_map[start_idx]

        _FRAN_PHRASE_CACHE = {
            "start": start_map,
            "second": second_map,
            "main": main_map,
            "source": source,
        }
        return _FRAN_PHRASE_CACHE

    def _fran_phrase(kind, idx):
        data = _fran_load_phrases()
        k = str(kind or "main").lower()
        i = int(idx or 0)
        if k == "start":
            val = data.get("start", {}).get(i, "")
            if not val:
                val = _fran_extract_phrase_single(data.get("source", ""), "FranPhraseStart", i)
            return val
        if k == "second":
            val = data.get("second", {}).get(i, data.get("start", {}).get(i, ""))
            if not val:
                val = _fran_extract_phrase_single(data.get("source", ""), "FranPhraseSecond", i)
            if not val:
                val = _fran_extract_phrase_single(data.get("source", ""), "FranPhraseStart", i)
            return val
        val = data.get("main", {}).get(i, "")
        if not val:
            val = _fran_extract_phrase_single(data.get("source", ""), "FranPhrase", i)
        return val

    def _fran_publish_location_text(start_text, main_text):
        global CurLocDesc
        global MainTxt
        chunks = []
        if start_text:
            chunks.append(str(start_text))
        if main_text:
            chunks.append(str(main_text))
        if not chunks:
            return
        combined = "\n\n".join(chunks).strip()
        if combined:
            CurLocDesc = combined
            MainTxt = combined

    def _fran_clean(lines=2):
        if renpy.has_label("CleanScreenOverflow"):
            try:
                renpy.call("CleanScreenOverflow", int(lines or 1))
            except Exception:
                renpy.call("CleanScreenOverflow")
        elif renpy.has_label("clean_screen_overflow"):
            try:
                renpy.call("clean_screen_overflow", int(lines or 1))
            except Exception:
                renpy.call("clean_screen_overflow")
        else:
            renpy.say(None, "\n")

    def _fran_inc_talk():
        global Talked
        Talked["fran"] = int(Talked.get("fran", 0) or 0) + 1

    def _fran_topic(start_idx, main_idx, clean_lines=2, update_key=None, update_val=1):
        global FranVar
        start_text = _fran_phrase("start", start_idx)
        main_text = _fran_phrase("main", main_idx)
        _fran_publish_location_text(start_text, main_text)
        if update_key:
            FranVar[update_key] = update_val
        _fran_inc_talk()

    def _fran_random_topic(clean_lines=3):
        idx = renpy.random.randint(0, 10)
        second_text = _fran_phrase("second", idx)
        main_text = _fran_phrase("main", idx)
        _fran_publish_location_text(second_text, main_text)
        _fran_inc_talk()

    def _fran_show_picture_path(picture_paths):
        for picture_path in list(picture_paths or []):
            if renpy.loadable(str(picture_path or "")):
                ShowImage("", "", str(picture_path or ""))
                return
        try:
            ShowImageSeq("ellona", "", "Fran", 4)
        except Exception:
            pass

    def _fran_show_topic_picture(topic_code=""):
        code = str(topic_code or "")
        if code == "meet":
            _fran_show_picture_path(("images/ellona/Fran2.jpg", "images/ellona/Fran1.jpg"))
            return
        if code in ("ellona", "grace"):
            _fran_show_picture_path(("images/ellona/stories.png", "images/ellona/statue1.jpg"))
            return
        if code == "grace_more":
            _fran_show_picture_path(("images/ellona/agla1.jpg", "images/ellona/agla2.jpg", "images/ellona/alga3.jpg"))
            return
        if code in ("conchita", "duke", "stark", "state", "king", "rebel"):
            _fran_show_picture_path(("images/ellona/Fran4.jpg", "images/ellona/Fran2.jpg"))
            return
        if code == "alien":
            _fran_show_picture_path(("images/ellona/aliens.png", "images/ellona/Fran4.jpg"))
            return
        if code == "random":
            _fran_show_picture_path(("images/ellona/Fran4.jpg", "images/ellona/stories.png", "images/ellona/Fran2.jpg"))
            return
        _fran_show_picture_path(("images/ellona/Fran1.jpg",))

    def _fran_prepare_state():
        global FranVar
        global Talked
        global dayspassed

        def _fran_i(value, default=0):
            try:
                return int(value)
            except Exception:
                return default

        day_now = max(0, _fran_i(dayspassed, 0))
        last_talk_day = _fran_i(FranVar.get("lasttalkday", -1), -1)
        if last_talk_day != day_now:
            Talked["fran"] = 0
            FranVar["lasttalkday"] = day_now
        else:
            Talked["fran"] = max(0, _fran_i(Talked.get("fran", 0), 0))
        FranVar["meet"] = max(0, _fran_i(FranVar.get("meet", 0), 0))
        FranVar["ellonaask"] = max(0, _fran_i(FranVar.get("ellonaask", 0), 0))
        FranVar["graceask"] = max(0, _fran_i(FranVar.get("graceask", 0), 0))
        FranVar["conchitaask"] = max(0, _fran_i(FranVar.get("conchitaask", 0), 0))
        FranVar["dukeask"] = max(0, _fran_i(FranVar.get("dukeask", 0), 0))
        FranVar["starkask"] = max(0, _fran_i(FranVar.get("starkask", 0), 0))
        FranVar["stateask"] = max(0, _fran_i(FranVar.get("stateask", 0), 0))
        FranVar["kingask"] = max(0, _fran_i(FranVar.get("kingask", 0), 0))
        FranVar["rebelask"] = max(0, _fran_i(FranVar.get("rebelask", 0), 0))
        FranVar["alienask"] = max(0, _fran_i(FranVar.get("alienask", 0), 0))
        return FranVar, Talked

    def _fran_topic_select(topic_code):
        code = str(topic_code or "")

        # Keep the location picture synced with dialog actions.
        _fran_show_topic_picture(code)

        if code == "meet":
            _fran_topic(0, 0, 3, "meet", 1)
            Francheska.mark_met()
            return
        if code == "ellona":
            _fran_topic(1, 1, 2, "ellonaask", 1)
            return
        if code == "grace":
            _fran_topic(2, 2, 2, "graceask", 1)
            return
        if code == "grace_more":
            _fran_topic(10, 10, 2, "graceask", 2)
            return
        if code == "conchita":
            _fran_topic(3, 3, 3, "conchitaask", 1)
            return
        if code == "duke":
            _fran_topic(4, 4, 3, "dukeask", 1)
            return
        if code == "stark":
            _fran_topic(5, 5, 3, "starkask", 1)
            return
        if code == "state":
            _fran_topic(6, 6, 2, "stateask", 1)
            return
        if code == "king":
            _fran_topic(7, 7, 3, "kingask", 1)
            return
        if code == "rebel":
            _fran_topic(8, 8, 2, "rebelask", 1)
            return
        if code == "alien":
            _fran_topic(9, 9, 2, "alienask", 1)
            return
        if code == "random":
            _fran_random_topic(3)
            return

label FrancheskaTalk:
    python:
        global _FRAN_PHRASE_CACHE
        _FRAN_PHRASE_CACHE = None
    $ _fran_prepare_state()
    $ main_ui_begin_talk_state("Что обсудить с Франческой?", "fran")
    $ current_action_title = "Что обсудить с Франческой?"
    $ current_action_content = None
    call BuildFrancheskaTalkMenu
    $ current_action_items = list(_return or [])
    return

label BuildFrancheskaTalkMenu:
    $ Result = []

    if FranVar.get("meet", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Пораспрашивать об этом месте", Call("FrancheskaTalkApply", "meet")))

    if FranVar.get("meet", 0) == 1 and FranVar.get("ellonaask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Пораспрашивать Франческу о богине Эллоне", Call("FrancheskaTalkApply", "ellona")))

    if FranVar.get("ellonaask", 0) == 1 and FranVar.get("graceask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Пораспрашивать Франческу о грациях", Call("FrancheskaTalkApply", "grace")))

    if FranVar.get("graceask", 0) == 1 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Узнать больше о грациях", Call("FrancheskaTalkApply", "grace_more")))

    if FranVar.get("meet", 0) == 1 and FranVar.get("conchitaask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Пораспрашивать Франческу о герцогине", Call("FrancheskaTalkApply", "conchita")))

    if FranVar.get("conchitaask", 0) == 1 and FranVar.get("dukeask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Спросить Франческу о герцоге", Call("FrancheskaTalkApply", "duke")))

    if FranVar.get("dukeask", 0) == 1 and FranVar.get("starkask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Узнать больше о предателе", Call("FrancheskaTalkApply", "stark")))

    if FranVar.get("conchitaask", 0) == 1 and FranVar.get("stateask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Пораспрашивать Франческу о герцогстве", Call("FrancheskaTalkApply", "state")))

    if FranVar.get("stateask", 0) == 1 and FranVar.get("kingask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Узнать больше о короле", Call("FrancheskaTalkApply", "king")))

    if FranVar.get("kingask", 0) == 1 and FranVar.get("rebelask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Узнать больше об отношениях с королевством", Call("FrancheskaTalkApply", "rebel")))

    if FranVar.get("stateask", 0) == 1 and FranVar.get("alienask", 0) == 0 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Расспросить про нелюдей", Call("FrancheskaTalkApply", "alien")))

    if FranVar.get("rebelask", 0) == 1 and FranVar.get("alienask", 0) == 1 and FranVar.get("starkask", 0) == 1 and FranVar.get("graceask", 0) == 2 and Talked.get("fran", 0) < 3:
        $ Result.append(MenuItem("Поболтать с Франческой", Call("FrancheskaTalkApply", "random")))

    $ Result.append(MenuItem("Закончить разговор", Call("FrancheskaTalkEnd")))
    return Result


label FrancheskaTalkApply(topic_code=""):
    $ _fran_topic_select(topic_code)
    call BuildFrancheskaTalkMenu
    $ _fran_menu_items = list(_return or [])
    $ stage_paged_panel_text(MainTxt, "Что обсудить с Франческой?", _fran_menu_items, "plain")
    call QueuePagedPanelTextFromStore
    call ReturnToMainUI
    return


label FrancheskaTalkEnd:
    $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
    if _room_label:
        jump expression _room_label
    return
