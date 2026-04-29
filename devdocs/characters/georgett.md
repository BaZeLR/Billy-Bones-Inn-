# Character Worklist: Жоржетта

## Identity
- Canonical id: georgett
- Legacy keys/tokens: georgett, GeorgettVar
- Init source: InitGeorgett.txt
- Main var store: GeorgettVar

## Presence/Schedule (TXT-driven notes)
- Базовая локация старта: PortStreets.
- Может быть перемещена в TavernMain через ветки найма/работы.
- Наличие и клиенты зависят от времени (time), флагов проституции и событий.

## Flags/Variables (Init authority)
- seeclients
- askclients
- askkids
- askparents
- askpregnancy
- asksex
- TellAboutEddieMomSex
- foundinchurch
- fuckinchurch
- lizasawinchurch
- georgettadmit
- churchgeorgettadmit
- churchlizaadmit
- SawChurchAfterCermon
- TalkChurchAfterCermon
- TalkChurchAfterCermonLiza
- GloryHoleExplained
- GloryHoleAgreed

## Primary Scenes/Dialogs/Features (TXT files)
- InitGeorgett.txt -> InitGeorgett.rpy (rpy_exists)
- IntGeorgettTalk.txt -> IntGeorgettTalk.rpy (rpy_exists)
- IntGeorgettSex.txt -> IntGeorgettSex.rpy (rpy_exists)
- IntGeorgettDressChange.txt -> IntGeorgettDressChange.rpy (rpy_exists)
- IntGeorgettAfterCermon.txt -> IntGeorgettAfterCermon.rpy (rpy_exists)
- PortStreets.txt -> PortStreets.rpy (rpy_exists)
- SexPort.txt -> SexPort.rpy (rpy_exists)
- SexProstTavern.txt -> SexProstTavern.rpy (rpy_exists)
- StreetClients.txt -> StreetClients.rpy (rpy_exists)
- TavernProstClients.txt -> TavernProstClients.rpy (rpy_exists)
- ShowGeorgettPortrait.txt -> ShowGeorgettPortrait.rpy (rpy_exists)

## Full TXT Coverage (anti-omission list)
- AdjustOtkroven.txt
- Church.txt
- ChurchAfterCermon.txt
- ChurchIspoved.txt
- DailySetstatdefault.txt
- DressNoShow.txt
- EllonaBirthPrayMenu.txt
- GeorgettBeckyVisit.txt
- GirlDressSuggest.txt
- GirlsDesc.txt
- GirlSuggestDressFunc.txt
- GiveBirth.txt
- GiveBirthFinish.txt
- GiveBirthStep2.txt
- GloryHoleBusy.txt
- InitGeorgett.txt
- InitLiza.txt
- InitSecondaryNPC.txt
- IntAmandaDressChange.txt
- IntBeckyGuest.txt
- IntBeckyTalk.txt
- IntEddieTalk.txt
- IntGeorgettAfterCermon.txt
- IntGeorgettDressChange.txt
- IntGeorgettSex.txt
- IntGeorgettTalk.txt
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
- ShowGeorgettPortrait.txt
- StolyarWorkshop.txt
- StreetClients.txt
- TavernGloryHole.txt
- TavernMain.txt
- TavernProstClients.txt
- TavernShowImage.txt
- ZaletOpinionCalc.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event actions included
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.
