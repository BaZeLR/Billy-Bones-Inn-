# Character Worklist: Лизетта

## Identity
- Canonical id: liza
- Legacy keys/tokens: liza, LizaVar
- Init source: InitLiza.txt
- Main var store: LizaVar

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
- [ ] Keep sex/special-event actions excluded in first pass (hide, do not delete).
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.
