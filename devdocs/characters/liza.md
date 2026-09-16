# Character Worklist: Лизетта

> REFERENCE ONLY.
>
> This file preserves source/TXT worklist names. Legacy `*Var` tokens are not
> current runtime owners. Runtime/story state belongs to the character class
> instance and event/thread labels.

## Identity
- Canonical id: liza
- Legacy keys/tokens: liza, LizaVar
- Init source: InitLiza.txt
- Current runtime owner: Liza/Lizette class instance

## Current corrections — 2026-09-16

- `Liza.corruption` remains the sole progression value. Reference start: 35
  (`textLocRef/InitLiza.txt`). No daily floor or automatic save reset was added.
- `SlutFriendsIncrease` direction is preserved by `apply_social_chance`:
  positive changes apply below their limit; negative changes apply above it.
  The dress-shame action can reduce corruption toward 30, not below 30.
  Other authored losses and dress acceptance thresholds remain unchanged.
- Repeating a harassment instruction does not change corruption. This follows
  `textLocRef/IntHarrassmentDiscuss.txt`; instruction and individual reactions
  still belong to the NPC. Premiums retain their existing separate effects.
- Premiums reinforce behavior desired by the MC; they do not define correct
  behavior or buy automatic agreement. Every voluntary Sunday service offer
  uses the girl's own trust, openness, corruption, morale, anger, rebellion and
  unmet needs. These decision weights are new requested tuning, not QSP values.
  Existing story prerequisites still apply; agreement unlocks the role, while
  the existing scheduler owns actual assignment. No daily re-consent roll.
- Liza and Georgette participate in existing soap gifts and barber bookings.
  Care writes their existing beauty stat. Client attraction derives from that
  stat plus the outfit actually worn, using the shared `DressLookValue` catalog.
  Female outfit appeal values (6–12) are new tuning. Owned but unworn gifts do
  not count. Better attraction increases daily slot-fill probability, not the
  reference capacity. Changes after morning generation affect the next day.
- Regular capacity remains Liza 3 (4 without her chosen daytime underwear),
  Georgette 5; Friday regular work and all Sunday service remain off. Anonymous
  glory-hole demand retains its existing visitor-based calculation.
- Free-touch friendship gates remain Liza 5 / Georgette 10. Paid hiring retains
  its 4/8 prices and does not use the voluntary-work decision roll.
- Amanda's glory-hole reveal requires an active working Liza session, the
  queued reveal and its actual discovery. Availability is rechecked at the
  reaction menu after discovery. The consumed queue row is not a second gate.
  Her ordinary Liza work conversation requires Liza hired, not both workers.
- Regression coverage: `test_tavern_client_attraction_runtime.py`,
  `test_tavern_service_decisions_runtime.py`, `external_liza_work_test.py`, and
  the existing tavern-premium runtime test. This is covered-path evidence,
  not a claim that every story branch has been played through.

## Presence/Schedule (TXT-driven notes)
- Базовая локация старта: PortStreets.
- Может быть перемещена в TavernMain при найме вместе с Жоржеттой.
- Ветви зависят от времени, клиентов и церковных/проституционных флагов.

## Flags/Variables (Init authority)
- SawChurchAfterCermon
- TalkChurchAfterCermon
- TalkChurchAfterCermonGeorgett
- ProstStart
- seeclients
- askclients
- askpregnancy
- asksex
- GloryHoleMentioned
- GloryHoleAsked

## Primary Scenes/Dialogs/Features (TXT files)
- InitLiza.txt -> InitLiza.rpy (rpy_exists)
- IntLizaTalk.txt -> IntLizaTalk.rpy (rpy_exists)
- IntLizaSex.txt -> IntLizaSex.rpy (rpy_exists)
- IntLizaDressChange.txt -> IntLizaDressChange.rpy (rpy_exists)
- IntLizettAfterCermon.txt -> IntLizettAfterCermon.rpy (rpy_exists)
- PortStreets.txt -> PortStreets.rpy (rpy_exists)
- SexPort.txt -> SexPort.rpy (rpy_exists)
- SexProstTavern.txt -> SexProstTavern.rpy (rpy_exists)
- StreetClients.txt -> StreetClients.rpy (rpy_exists)
- TavernProstClients.txt -> TavernProstClients.rpy (rpy_exists)
- ShowLizaPortrait.txt -> ShowLizaPortrait.rpy (rpy_exists)

## Full TXT Coverage (anti-omission list)
- AdjustOtkroven.txt
- AmandaAtGloryHole.txt
- AmandaAtHomeCode.txt
- AmandaDynamicCommonBlocks.txt
- Church.txt
- ChurchAfterCermon.txt
- ChurchIspoved.txt
- CreateTavernEventsPeriod.txt
- DailySetstatdefault.txt
- DisplayTavernEventShort.txt
- DressNoShow.txt
- EllonaBirthPrayMenu.txt
- EventAmandaLizettTalk.txt
- EventAmandaLizettTalk2.txt
- GirlDressSuggest.txt
- GirlsDesc.txt
- GirlSuggestDressFunc.txt
- GiveBirth.txt
- GiveBirthFinish.txt
- GiveBirthStep2.txt
- GloryHoleBusy.txt
- InitAmanda.txt
- InitAmandaLizaTalkItems.txt
- InitGeorgett.txt
- InitLiza.txt
- InitSecondaryNPC.txt
- IntAlberTalk.txt
- IntAmandaDressChange.txt
- IntAmandaTalk.txt
- IntGeorgettAfterCermon.txt
- IntGeorgettTalk.txt
- IntLizaDressChange.txt
- IntLizaSex.txt
- IntLizaTalk.txt
- IntLizettAfterCermon.txt
- Intro.txt
- KidsFunctions.txt
- menu_tavernstat.txt
- MomDressComplaint.txt
- NextDay_FinishDayEvents.txt
- NextDay_NewDayEvents.txt
- NextDay_TavernDaily.txt
- NextDay.txt
- PortStreets.txt
- SexPort.txt
- SexProstTavern.txt
- ShowCurrentSex.txt
- ShowLizaPortrait.txt
- StreetClients.txt
- TavernMain.txt
- TavernProstClients.txt
- TavernShowImage.txt
- WhoreNextDayClients.txt
- ZaletOpinionCalc.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event included
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.
