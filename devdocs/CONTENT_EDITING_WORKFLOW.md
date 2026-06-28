# Content Editing Workflow

Purpose: make event text, picture usage, and right-panel choices easier to find and edit without damaging the current UI.

## Fast Lookup Files

- `devdocs/LABEL_TEXT_MEDIA_INDEX.tsv` - generated index of every label, file, line, detected picture/video calls, text assignments, menu items, and event calls.
- `devdocs/RENpy_ENGINE_PROJECT_KNOWLEDGE_BASE.md` - explains the correct project structure.
- `devdocs/PROJECT_MAP_AND_DEPENDENCIES.md` - maps runtime systems and dependencies.

Open the TSV in a spreadsheet or search it directly.

Examples:

```powershell
rg -n "TavernKitchenBreakfastMelissaAmandaGerhard|underBed|ShowImage|SceneActionPanel" devdocs/LABEL_TEXT_MEDIA_INDEX.tsv
rg -n "label TavernKitchenBreakfastMelissaAmandaGerhard|underBed|MelissaAmandaGerhard" game/Inn
```

## Clean Event Shape

Readable event files should follow this shape:

```renpy
label event_name:
    vscene "images/path/picture.png"
    "Editable event text."

    menu:
        "Choice text":
            $ SomeVar["state"] = 1
            $ calendar_advance_minutes(5)
            $ thread.advance()
            jump event_name_choice

        "Back":
            jump expression CurLoc

label event_name_choice:
    vscene "images/path/result.png"
    "Result text."
    call stat
    jump expression CurLoc
```

This keeps the human-editable parts visible:

- label name;
- picture path;
- text;
- event choices;
- consequence labels.

## Picture And Video Rules

- Use `vscene "path"` for scene media.
- Use `call ShowImage(...)` when ported legacy code depends on old folder/name resolution.
- Use `.webm` as the safest Ren'Py-first format.
- `.mp4` is now recognized by this project as video too, but codec/platform support still depends on Ren'Py/browser playback.
- For web/Safari, Ren'Py documentation says web video can try `.mp4` fallback when `.webm` is unsupported.

## What Not To Do

- Do not hide normal gameplay actions in native `menu:` blocks if the right panel should stay active.
- Do not replace `screen main_ui`.
- Do not scatter one event across unrelated files unless it is a shared system.
- Do not hand-roll image path variants if `ShowImage` or `vscene` can handle it.

## Regenerate Label Index

After large content changes, regenerate:

```powershell
$out = @()
$files = rg --files game -g '*.rpy'
foreach ($file in $files) {
    $lines = Get-Content -LiteralPath $file
    $labelStarts = @()
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^label\s+([A-Za-z_][A-Za-z0-9_]*)') {
            $labelStarts += [pscustomobject]@{ Name=$Matches[1]; Line=$i+1; Index=$i }
        }
    }
    for ($j = 0; $j -lt $labelStarts.Count; $j++) {
        $start = $labelStarts[$j].Index
        $end = if ($j + 1 -lt $labelStarts.Count) { $labelStarts[$j+1].Index - 1 } else { $lines.Count - 1 }
        if ($end -lt $start) { $end = $start }
        $block = $lines[$start..$end]
        $out += [pscustomobject]@{
            Label=$labelStarts[$j].Name
            File=$file
            Line=$labelStarts[$j].Line
            Lines=($end - $start + 1)
            Media=(@($block | Where-Object { $_ -match 'vscene\s+|ShowImage\(|ShowImageSeq\(|call\s+ShowImage|call\s+ShowImageSeq' } | ForEach-Object { ($_ -replace '\s+', ' ').Trim() } | Select-Object -First 3) -join ' || ')
            Text=(@($block | Where-Object { $_ -match 'MainTxt\s*=|CurLocDesc\s*=|QueuePagedPanelText|TavernKitchenBreakfastShowText|SceneActionPanel\(' } | ForEach-Object { ($_ -replace '\s+', ' ').Trim() } | Select-Object -First 3) -join ' || ')
            Menu=(@($block | Where-Object { $_ -match 'MenuItem\(|^\s*menu\s*:' } | ForEach-Object { ($_ -replace '\s+', ' ').Trim() } | Select-Object -First 3) -join ' || ')
            Events=(@($block | Where-Object { $_ -match 'CheckDailyEvent|checkTriggers|story_event_available|DailyEventsList|story_thread_advance_current' } | ForEach-Object { ($_ -replace '\s+', ' ').Trim() } | Select-Object -First 3) -join ' || ')
        }
    }
}
$out | Sort-Object File,Line | Export-Csv -Path 'devdocs\LABEL_TEXT_MEDIA_INDEX.tsv' -Delimiter "`t" -NoTypeInformation -Encoding UTF8
```
