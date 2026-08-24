# Georgett (Жоржетта Брюно) — Story Milestones (GeorgettVar Flags) + Event Requirements

**Purpose**: Canonical reference for all Georgett story progression. Every flag is a direct int milestone in GeorgettVar. All events, talk options, and repeatable content (especially the post-hire sex engine path) must be defined/defaulted with pictures and texts using only these flags. No boolean wrappers, no middleware, no bridges, no fallbacks, no bloat.

**Rules (ordered `thread.num` stage precedent + strict project standard)**:
- All checks: `int(GeorgettVar.get("key", 0) or 0) == 1` (or `> 0`, `>= N`).
- No `def georgett_*_ready():` functions that return booleans.
- No extra layers. Logic lives only in `game/NPC/Girls/Georgett/` files.
- Interactions belong to the NPC, not the room she is currently in.
- Every milestone must have associated event(s) with pictures + text.
- Repeatable content (post-hire sex engine) must react to current flag state + relationship + arousal/cum state.

## Core GeorgettVar Flags (Story Milestones)

### Church / Priest Arc
- `foundinchurch` (0/1) — Georgett found in church (peeping trigger).
- `fuckinchurch` (0/1) — Explicit sex in church occurred.
- `lizasawinchurch` (0/1) — Liza witnessed church events.
- `georgettadmit` (0/1) — Admitted church sex to player on street.
- `churchgeorgettadmit` (0/1) — Admission during confession.
- `churchlizaadmit` (0/1) — Liza-related church admission.
- `SawChurchAfterCermon` (0/1) — Saw Georgett after sermon.
- `TalkChurchAfterCermon` (0/1) — Talked about church after sermon.
- `TalkChurchAfterCermonLiza` (0/1) — Discussed Liza's church experience (cross-link to Liza arc).

**Associated events** (must have pics + text):
- Church peeping scenes (IntGeorgettAfterCermon)
- Street admission (georgett_church_admit)
- Liza reveal (georgett_liza_church_reveal)
- Confession variants (ChurchIspoved)

### Gloryhole / Hire Arc (Core Hire Path from Port Streets)
- `GloryHoleExplained` (0/1) — Explained previous job gloryhole.
- `GloryHoleAgreed` (0/1) — Agreed to terms (unlocks gloryhole work for both Georgett + Liza).
- `hired_to_tavern` (0/1) — Officially hired to work at the tavern (primary milestone after Port Streets hiring).

**Associated events** (must have pics + text):
- Street hiring talk (georgett_hire_invite / georgett_hire_complete in GeorgettEvents.rpy + IntGeorgettTalk)
- Gloryhole explanation + terms (georgett_gloryhole_explain, georgett_gloryhole_terms)
- **Repeatable post-hire sex engine** (see dedicated section below)

### Eddie / Becky Sponsorship Arc
- `TellAboutEddieMomSex` (0/1) — Player told Georgett about Eddie/Becky home events.

**Associated events**:
- Street Eddie story (georgett_eddie_story)
- Paid home sponsorship scenes

### Family / Explicit Life Stories
- `askclients` (0/1)
- `askkids` (0/1)
- `askparents` (0/1)
- `askpregnancy` (0/1)
- `asksex` (0/1)
- `family_story_done` (0/1)

**Associated events**:
- Street family/sex/kids/pregnancy talks (repeatable until flag set)

### Street / Work Visibility
- `seeclients` (0/1) — Player has seen her with clients on the street (unlocks talk topics).

## Repeatable Post-Hire Sex Engine Event (Critical)

**Trigger**:
- Hire Georgett on Port Streets (`hired_to_tavern` becomes 1, usually together with jobWhoreAvail["georgett"] = 1).
- Player pays her as a tavern prostitute (SexProstTavern path) or uses her sex menu in tavern context.
- This is explicitly a **repeatable paid client interaction**.

**Current flow (RPY)**:
- `SexProstTavern(1, "georgett")` → short intro text → BeginPaidSexModule → "You are in a modestly furnished room with passionate Georgett." → `IntGeorgettSex(..., "tavern")` → FinishPaidSexModule.

**Requirements (must be fully defined with pics + texts)**:
- Intro text must vary based on current milestones (e.g., whether GloryHoleAgreed, relationship level, previous sex, cum state, drunk, etc.).
- Full sex menu (examine, layer undress, cum cleanup, kissing, groping, oral, titfuck, vaginal, anal, positions) must be present with appropriate pictures from `images/georgett/sex/` (minet1.jpg, minet2.jpg, doggy*, cowgirl*, grope.jpg, cummouth.jpg, etc.) and tavern-appropriate variants.
- Use `ShowGeorgettPortrait` + direct `vscene` or `ShowImage` calls for key moments (no missing assets).
- State changes (Arousal, cum, relationship bumps, specific flag reactions) must be direct on GeorgettVar + globals.
- No extra wrappers. All conditions are direct `int(GeorgettVar.get("key", 0) or 0)` checks inside the sex labels or setup.

**Pictures available (sex/ subfolder)**: cowgirl1-4, doggy1-3 + doggyinside, minet1-2, grope, cummouth, and others in the broader georgett tree (port, church, etc.).

**Text source of truth**: Original `textLocRef/IntGeorgettSex.txt` + `SexProstTavern.txt` (the large dynamic menu with explicit Russian text for every action and state combination).

## Implementation Notes

- All new or cleaned event labels live in `game/NPC/Girls/Georgett/GeorgettEvents.rpy` or the Int*.rpy files in the same folder.
- Talk logic lives only in `IntGeorgettTalk.rpy`.
- Sex logic lives only in `IntGeorgettSex.rpy` (must be completed to match original depth for the repeatable hired path).
- Thread conditions use only direct int expressions on GeorgettVar (and cross LizaVar where needed).
- Every milestone transition must have at least one picture + descriptive text.
- After any hire milestone (`hired_to_tavern`), the repeatable tavern sex path must feel alive and reactive to her current flags + relationship.

## Story Board Update — 2026-06-09

### Church service scenes

Runtime source:
- Thread definitions: `game/Utilities/General/Classes/StoryEventRuntime.rpy`
- Scene labels: `game/NPC/Girls/Georgett/InitGeorgettChurch.rpy`
- Church attendee action: `game/Town/Church/Church.rpy`
- Visual board: `game/Utilities/General/Screens/StoryThreadBoard.rpy`

Thread/event rows now registered under Georgett:
- `ChurchServiceBench` -> `story_georgett_church_service_bench`
- `ChurchServiceDoggy` -> `story_georgett_church_service_doggy`
- `ChurchServiceWithLiza` -> `story_georgett_church_service_with_liza`

Trigger route:
- Church attendee list shows Georgett when player knows her and she is valid for church visibility.
- Clicking Georgett opens `ChurchServiceGeorgett`.
- `ChurchServiceGeorgett` marks `foundinchurch = 1`, refreshes event availability, and offers only event-engine-backed choices through `checkTriggers("Church", action, 0)`.

Explicit event conditions visible on the story board:
- player knows Georgett;
- `npc_schedule_georgett_church_visible()`;
- `foundinchurch > 0`;
- `cametoday < cancumdaily`;
- `Friends["georgett"] >= 6`;
- `Georgett.rel >= 6`;
- `sluttiness["georgett"] >= 50`;
- `Georgett.corruption >= 50`;
- `HadSex["georgett"] >= 3`;
- with-Liza scene also requires `askkids > 0` and `fuckinchurch > 0`.

Scene media:
- Bench: `images/georgett/church/bench/bench1.jpg` through `bench6.jpg`
- Doggy: `images/georgett/church/doggy/doggy1.jpg` through `doggy6.jpg`
- With Liza: `images/georgett/church/withLiza.jpg/withliza1.jpg` through `withliza6.jpg`
- All scene images are shown with `vscene`.
- Sequences advance one visible step at a time through normal Ren'Py `menu` choices.

State changes after the scene is played:
- `money -= 15`
- `fun += 4`, capped at 100
- `fuckinchurch = 1`
- variant flag set: `church_bench_seen`, `church_doggy_seen`, or `church_liza_seen`
- with-Liza scene also sets `lizasawinchurch = 1`
- `player_record_orgasm(...)`
- `PregnancyCheck("georgett", "inside", 1, "Вы")`
- `calendar_v2.advance_minutes(60)` after the final return choice
- scene returns to `Church`

Confession links:
- `ChurchIspoved.rpy` now exposes confession choices for `church_bench_seen`, `church_doggy_seen`, and `church_liza_seen`.
- Confession choices set `churchgeorgettadmit` and, for Liza-related confession, `churchlizaadmit`.

Visual board support:
- `StoryThreadBoard.rpy` now gives readable titles for the Georgett church event labels and action keys.
- The hover detail panel now shows the raw label, action key, and owner file for the new Georgett/Lizette church event rows.
- The board remains read-only and uses the existing `threads`, `threadData`, and `threadListsByGirl` runtime objects.

### After-sermon scene

Runtime source:
- Thread definition: `game/Utilities/General/Classes/StoryEventRuntime.rpy`
- Scene labels: `game/NPC/Girls/Georgett/IntGeorgettAfterCermon.rpy`

Registered row:
- `ChurchAfterSermon` -> `story_georgett_church_after_sermon`
- Trigger: `Church / after_cermon_walk`
- Day/hour gate: Sunday, `11:00-12:00`
- Condition: `Georgett.church_after_sermon_event_available()`

Cleaned labels:
- Removed old dispatcher/refresh-style entry labels.
- Kept direct event label and explicit step labels:
  - `story_georgett_church_after_sermon`
  - `story_georgett_church_after_sermon_look_1`
  - `story_georgett_church_after_sermon_look_2`
  - `story_georgett_church_after_sermon_look_3`
  - `story_georgett_church_after_sermon_look_4`

Media and flow:
- Uses `vscene`.
- `ispovedstep2_1.jpg` and `ispovedstep2_2.jpg` both show with a `Дальше` menu between them.
- Final return advances `calendar_v2.advance_minutes(60)` and returns to `Church`.
- No `MenuItem`, no `current_action_items`, no restore labels, no `AdvanceTimeAndRestore`.

### Verified today

- `python -m pytest tests\test_georgett_liza_object_source.py -q`
- `renpy.exe . compile`
- `python tools\external_click_play_test.py --only external_church_service_action_links_work`
- `python tools\external_click_play_test.py --only external_georgett_liza_church_after_sermon_events`

This document is the single source of truth for Georgett content work. Update it when flags or events change.

**Status**: Reference gathering complete from devdocs, dialogue.tab, and textLocRef TXT sources. Ready for clean implementation of missing event definitions + full repeatable post-hire sex content with pictures and texts.
