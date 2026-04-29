# Location, Locate, Talk Reset Standard

FamilyLife pattern used as reference:

- Location entry sets the current location, refreshes available events, then rebuilds the room/menu state.
- Locate reads each NPC through `PeopleData.getLocation()` and uses that same location for the icon/menu presence check.
- Dialogue/talk actions mutate the per-person interaction state.
- New day/sleep clears per-person `talkToday`, `flirtToday`, `giftToday` centrally.

Tractir implementation:

- Room menus and NPC visibility continue to use `getLocation(person)` from `NPCScheduleModel.rpy`.
- `PeopleInfo` now mirrors the daily maps (`TalkedToday`, `FlirtedToday`, `GiftedToday`, `AskedToday`) and has `reset_daily()`.
- `people_reset_daily_interactions()` is called from `NextDay_FinishDayEvents.rpy`, alongside the existing daily stat reset.
- Social actions call `people_sync_person()` after mutating the old maps, so the object layer and dict layer stay aligned.
- `people_locate_overlay` shows the current schedule location and talk state through the same path used by room NPC actions.

When adding a new NPC:

1. Add schedule/default location data in the existing schedule/current-location sources.
2. Add or confirm `NPC_META` action data if the NPC can be selected in rooms.
3. Let `initPeople()` build `PeopleData`/`PeopleInfo`; do not create a separate parallel location system.
4. Use existing social actions (`SocialTalkTopicMenu`, gift/share menus, `apply_social_interaction_base`) so daily reset and locate state remain consistent.
