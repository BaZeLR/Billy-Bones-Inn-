# TODO: Robin + Blackwood (ex-Sherwood) Quest — Remaining Parts

This document captures the scope explicitly requested in the current session (after the initial hook + Mongol vouch + Zimmer mission choice point were introduced).

## Current State (done in this pass)
- Robin registered as full secondary NPC (game/NPC/Secondary/InitSecondaryNPC.rpy)
  - Direct `knowsMC["robin"]` population (per "you are making fucking classes" rule)
  - RobinVar defaults + MongolSafePass flag
  - Profile / description
- Thin atomic events added (in BeckyEvents.rpy + RobinBlackwood thread registration):
  - `robin_mongol_vouch_safe_passage` — Mongol (after StocksReleased) vouches → safe passage, saves horse + money.
  - `zimmer_bandit_camp_choice` — choice point on the way to Cunidale: destroy the camp (violent) vs peaceful resolution for Zimmer's mission.
- Mongol released flag (`MongolVar["StocksReleased"]`) now protects the player from the usual Robin shakedown (via `RobinVar["MongolSafePass"]`).
- Integration points noted in SherwoodTravel / IntRobinTalk (current robbery paths should check the safe-pass flag first).
- Zimmer mission context already present in IntZimmerTalk.txt ("Пожаловаться на Робин Гуда").

## Remaining Work (explicitly deferred — "this is all for now... we need todo on it")

### 1. Cunidale (Kunidell / Elven Village) — Full Content
- Proper location for the elven village (trade with Becky's vegetables).
- Dialog with elves (Lady Minetuel mentioned in old BeckyQuestInit).
- Multiple visit / repeatable trade mechanics.
- Reactions to the state of the Blackwood/Sherwood cut (bandits destroyed vs peaceful deal).
- Rewards / profit for Becky + player (beyond the basic 50-300m).
- Integration with Becky pregnancy / relationship flags if high trade volume.

### 2. Third Part of Blackwoods (post-camp)
- Full resolution of the choice made at `zimmer_bandit_camp_choice`.
- Violent path consequences:
  - The current camp fight and Zimmer report are only the first playable slice;
    they do not yet grant the final reward package below.
  - MC must carry and use one existing crafted fire bottle
    (`fire_bomb_001`) during the assault. The camp event consumes that item;
    do not create a second quest-only fire-bottle item or mirror its quantity.
  - Unique post-camp reward package, granted exactly once:
    - recover Becky's stolen horse;
    - receive exactly 2,000 maravedi;
    - Mongol joins the tavern household as stableman and servant;
    - one additional horse joins the tavern stable;
    - Mongol's two servant girls join the household;
    - a carriage becomes available for rides with tavern ladies.
  - The two servant girls take responsibility for cleaning, tending the fires,
    and maintaining the wood stock so MC no longer performs those routine
    duties while the servants are active and able to work.
  - Becky unlocks the store intimacy continuation after this resolution. If
    Inga is present in the store, her corresponding store continuation can also
    become available through her own event/thread conditions.
  - Mongol proposes two later tavern improvements: a backyard improvement and
    a bathroom in the shed. His proposal unlocks their authored order/build
    events; it does not instantly complete either room improvement.
  - Reaction from Robin's remaining people (if any).
  - Zimmer settlement and possible investigation complications.
  - Long-term effect on Becky trade safety (or new dangers).
- Peaceful path consequences:
  - Negotiation / deal with Robin.
  - What Zimmer gets (fake investigation? real compromise?).
  - Ongoing "protection" or tribute mechanics.
  - Possible future Robin as recurring contact / quest giver.

### 3. Deeper Robin NPC + Thread
- Full Robin thread with multiple stages (not just the vouch and camp choice).
- Robin-specific dialog hooks (IntRobinTalk already rich — wire more flags).
- Picture / image sequences already referenced — ensure they load correctly for the new events.
- Relationship progression (Friends["robin"], openness, etc.) and how it affects safe passage on later runs.
- Possible recruitment / side jobs with the "обездоленные".

### 4. Zimmer Mission Polish
- Proper investigation timer (`ZimmerVar['RobinInvestigationDay']`).
- What happens when the timer expires depending on player choice at the camp.
- Zimmer's personality reactions (he is already a registered secondary with knowsMC).
- Extend the existing post-victory Zimmer report into a one-time settlement
  stage for the exact reward package in section 2. The Zimmer/Robin thread owns
  the order and completion gate; it must not duplicate money, horse, worker, or
  tavern-improvement state.
- The branch is complete only after the camp victory and this settlement have
  both played. Retreat or defeat grants no part of the package.
- **Done this session**: Zimmer fully converted to secondary NPC (direct knowsMC["zimmer"], profile, defaults + new flags in game/NPC/Secondary/InitSecondaryNPC.rpy). New thin label `zimmer_guard_mission_update` + integration into RobinBlackwood thread. Reacts to destroy vs peaceful choice at bandit camp and updates mission state. CityGuard location + full IntZimmerTalk (horse theft complaints, Sherwood story, paid Robin investigation) already functional.

### 5. Technical / Polish
- Hook the existing SherwoodTravel.txt / .rpy so that `RobinVar["MongolSafePass"] == 1` actually bypasses the donation demand and horse theft.
- Update the Becky home guest / trade offer text to reflect whether the road is now "safe" thanks to the player.
- Add unit tests in ThreadTesting.rpy for the two new Robin events (following the exact georgette / blackwood hook pattern).
- StoryThreadBoard visibility for RobinBlackwood thread.
- Ensure no globals() / gs artifacts were introduced.

### 6. Lunar Fertility Cycles for Female Characters (Hidden System)

**Important Design Note (user directive):**
- Moon phases are directly tied to **reproductive female cycles** (menstrual / fertility cycles).
- This applies specifically to: **Amanda, Melissa, Clarissa (clara), Sandra**.
- The fertility state must remain **completely hidden** from the player (no UI, no direct variable exposure).
- It will later impact:
  - Behavioral decisions (desire, risk assessment, intent models — see `tools/amanda_intent_model_test.py` which already has `cycle_phase` concept).
  - Pregnancy chances (inside `PregnancyCheck` / `ConceptionChance` calculations).

**Current Implementation Status (this session):**
- Foundation added in `game/script.rpy`:
  - `girl_lunar_fertility_offset` dict (hidden, per-girl stagger).
  - `get_girl_lunar_fertility(girl_name)` → returns `{"phase": "...", "strength": 0.0-1.0, "is_peak": bool, ...}`
  - `get_girl_fertility_strength(girl_name)` quick accessor.
- Uses the existing `MoonCalendar` moon phase system as the driver.
- Currently **no visible effects** — prepared for later integration into intent models and pregnancy logic.

Do **not** expose these values. Only use them internally in future development.

### 7. Later Expansions (out of scope for current sprint)
- Full "Robin Hood" parody questline (social responsibility jokes, etc.).
- Interaction with other characters (Georgett? Liza? Amanda?) discovering the player's dealings with the outlaws.
- Long-term fate of the Blackwood cut (reforestation? new bandit group? player-built toll road?).

---

**Owner**: Current development session (Tractir 0.06-billy-bones branch)
**Priority**: High for quest coherence (the Mongol release → safe passage is the key "you already did something that matters" moment).
**Next step recommendation**: Implement the Cunidale location skeleton + wire the MongolSafePass check into the actual travel encounter before expanding the two choice paths.

All file references and architecture rules (thin events, direct knowsMC, no globals, explicit comments, thread registration) must be followed when continuing this work.
