# Character Worklist: Бекки

## Identity
- Canonical id: becky
- Legacy keys/tokens: becky, BeckyVar
- Init source: InitBecky.txt
- Main var store: BeckyVar

## Presence/Schedule (TXT-driven notes)
- Днем обычно в GroceryStore (по time), поздние ветки в BeckyHomeFront/BeckyHome.
- Доступ к дому открывается по квестовым условиям (невидимая локация до прогресса).
- Имеет отдельные ветки Шервуда и церковных событий.

## Flags/Variables (Init authority)
- leftdances
- danceinvitehome
- visitedhome
- husbandtalk
- eddietalk
- SawIngaFuck
- IngaSexGreet
- VisitScolded
- TodayFrontSexCheck
- HomeSex
- EddieGeorg
- EddieWhoreHome
- BeckyOpenMinet
- TimesVisited
- TalkAboutEddie
- GeorgMention
- EddieIntrReact
- PriestAdvice
- GerhardBeckyTalk
- AskedEddieFuck
- EddieTryToFuck
- EddieFailures
- EddieRobbedDay
- KnowSherwood
- SherwoodSuspect
- TradeOffer
- SherwoodWarn
- AskTradeElf
- FingalClarify
- AdmitSherwood
- RobbedByRobin
- ConsoleRobbery

## Primary Scenes/Dialogs/Features (TXT files)
- InitBecky.txt -> InitBecky.rpy (rpy_exists)
- IntBeckyTalk.txt -> IntBeckyTalk.rpy (rpy_exists)
- IntBeckyTalkSherwood.txt -> IntBeckyTalkSherwood.rpy (rpy_exists)
- IntBeckySex.txt -> IntBeckySex.rpy (rpy_exists)
- IntBeckyDance.txt -> IntBeckyDance.rpy (rpy_exists)
- IntBeckyDressChange.txt -> IntBeckyDressChange.rpy (rpy_exists)
- IntBeckyGuest.txt -> IntBeckyGuest.rpy (rpy_exists)
- BeckyHomeFront.txt -> BeckyHomeFront.rpy (rpy_exists)
- BeckyHome.txt -> BeckyHome.rpy (rpy_exists)
- GroceryStore.txt -> GroceryStore.rpy (rpy_exists)
- BeckyQuestInit.txt -> BeckyQuestInit.rpy (rpy_exists)
- BeckyInviteHome.txt -> BeckyInviteHome.rpy (rpy_exists)
- ShowBeckyPortrait.txt -> ShowBeckyPortrait.rpy (rpy_exists)

## Full TXT Coverage (anti-omission list)
- BeckyEddieJoinFirst.txt
- BeckyHome.txt
- BeckyHomeFront.txt
- BeckyInviteHome.txt
- BeckyLoversInStore.txt
- BeckyQuestInit.txt
- Church.txt
- ChurchAfterCermon.txt
- DailySetstatdefault.txt
- DressNoShow.txt
- FridayDance.txt
- GeorgettBeckyVisit.txt
- GirlDressSuggest.txt
- GirlsDesc.txt
- GiveBirth.txt
- GiveBirthFinish.txt
- GiveBirthStep2.txt
- GroceryStore.txt
- InitBecky.txt
- IntBeckyAfterCermon.txt
- IntBeckyDance.txt
- IntBeckyDressChange.txt
- IntBeckyGuest.txt
- IntBeckySex.txt
- IntBeckyTalk.txt
- IntBeckyTalkSherwood.txt
- IntEddieBeckySex.txt
- IntEddieTalk.txt
- IntGeorgettTalk.txt
- Intro.txt
- IntZimmerTalk.txt
- KidsFunctions.txt
- Loc.txt
- MarketPlace.txt
- NextDay_FinishDayEvents.txt
- NextDay_NewDayEvents.txt
- SherwoodTravel.txt
- ShowBeckyPortrait.txt
- ShowCurrentSex.txt
- TavernProstClients.txt
- TavernStable.txt
- ZaletOpinionCalc.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event actions excluded in first pass (hide, do not delete).
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.
