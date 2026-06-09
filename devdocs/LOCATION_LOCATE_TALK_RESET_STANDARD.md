# Location, Locate, Talk Reset Standard

FamilyLife pattern used as reference:

- Location entry sets the current location, refreshes available events, then rebuilds the room/menu state.
- Locate reads each NPC through `PeopleData.getLocation()` and uses that same location for the icon/menu presence check.
- Dialogue/talk actions mutate the per-person interaction state.
- New day/sleep clears per-person `talkToday`, `flirtToday`, `giftToday` centrally.

Tractir current implementation:

- Room menus and NPC visibility continue to use `getLocation(person)` from `NPCScheduleModel.rpy`.
- `PeopleInfo` now mirrors the daily maps (`TalkedToday`, `FlirtedToday`, `GiftedToday`, `AskedToday`) and has `reset_daily()`.
- `people_reset_daily_interactions()` is called from `NextDay_FinishDayEvents.rpy`, alongside the existing daily stat reset.
- Social actions call `people_sync_person()` after mutating the old maps, so the object layer and dict layer stay aligned.
- `people_locate_overlay` shows the current schedule location and talk state through the same path used by room NPC actions.

Target dialogue model:

- NPC `talk` is an event-like action, not a generic action dispatcher.
- The clicked NPC talk action opens the real `Int<Npc>Talk` label.
- That label owns the picture/text/menu choices for talk, flirt, gift, questions, apologies, and story-specific dialogue.
- Choices must be visible in the same event/talk scene layout as story-event choices.
- The branch where the player chooses the topic/gift/flirt owns the mutation:
  `Talked`, `TalkedToday`, `FlirtedToday`, `GiftedToday`, `AskedToday`, friendship, openness, sluttiness, trust, and NPC-specific variables.
- New day/sleep remains the central reset point for daily interaction counters.
- Topic preferences and gift preferences belong to the NPC's data/init/object. Amanda, Melissa, Sandra, and Clarissa currently have shared talk theme and gift mechanics; that data may be reused, but the visible menu and consequences should still be owned by their talk labels.
- Other NPCs with their own talk procedures can stay direct until migrated.

Compatibility/bloat to reduce:

- `SocialTalkTopicMenu`, `SocialTalkTopicApply`, `social_core_action_items()`, and `Int<Npc>TalkRefresh`/`Int<Npc>TalkApply` are current compatibility layers, not the desired authoring model.
- Shared helper functions may calculate a topic score or gift affinity, but they should not hide the authored menu, the chosen branch, or the state mutation.
- Do not add refresh/apply/rebuild labels for new talk content.

When adding a new NPC:

1. Add schedule/default location data in the existing schedule/current-location sources.
2. Add or confirm `NPC_META` action data if the NPC can be selected in rooms.
3. Let `initPeople()` build `PeopleData`/`PeopleInfo`; do not create a separate parallel location system.
4. Add a direct `Int<Npc>Talk` label as the dialogue owner.
5. Put topic preferences and gift preferences in the NPC's own data/init/object.
6. Reset daily interaction counters centrally; increment them in the talk/gift/flirt branch where the action actually happens.
