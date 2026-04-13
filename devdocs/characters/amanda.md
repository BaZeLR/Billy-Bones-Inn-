# Character Worklist: Аманда

## Identity
- Canonical id: amanda
- Legacy keys/tokens: amanda, AmandaVar
- Init source: InitAmanda.txt
- Main var store: AmandaVar

## Presence/Schedule (TXT-driven notes)
- Основная локация старта: TavernMain.
- Собственная локация: TavernAmandaRoom (ночные ветки и доступ по условиям).
- Участвует в FridayDance, событиях таверны и глорихоле по условиям флагов.

## Flags/Variables (Init authority)
- lizafriends
- prohibitliza
- alberfriends
- albernowdances
- alberdanceadvance
- leftdances
- alberprohibit
- LegareGo
- EscapeUnnoticed
- glorytried
- gloryyouknow
- gloryscold
- glorywalkout
- glorysuck
- glorydeflower
- suckyou
- fuckyou
- knowsexactive
- knownotvirgin
- knowlegaresex
- sawlegaresex
- sucklegare
- fucklegare
- deflowerlegare
- knowdeflowerlegare
- beddeflower
- kickyoufromroom
- kickyoufromroomcount
- kickedwithmomhelp
- knowyousawlegaresex
- knowyouseesex
- warnnotwork
- sawwithguys
- prohibitwithguys
- askzalettoday
- MomDressComplaint

## Primary Scenes/Dialogs/Features (TXT files)
- InitAmanda.txt -> InitAmanda.rpy (rpy_exists)
- IntAmandaTalk.txt -> IntAmandaTalk.rpy (rpy_exists)
- IntAmandaSex.txt -> IntAmandaSex.rpy (rpy_exists)
- IntAmandaDance.txt -> IntAmandaDance.rpy (rpy_exists)
- IntAmandaDressChange.txt -> IntAmandaDressChange.rpy (rpy_exists)
- TavernAmandaRoom.txt -> TavernAmandaRoom.rpy (rpy_exists)
- AmandaAtHomeCode.txt -> AmandaAtHomeCode.rpy (rpy_exists)
- AmandaAtGloryHole.txt -> AmandaAtGloryHole.rpy (rpy_exists)
- AmandaLoverSex.txt -> AmandaLoverSex.rpy (rpy_exists)
- AmandaLegareDanceSequence.txt -> AmandaLegareDanceSequence.rpy (rpy_exists)
- AfterDanceLegare.txt -> AfterDanceLegare.rpy (rpy_exists)
- AfterDanceSexLegare.txt -> AfterDanceSexLegare.rpy (rpy_exists)
- EventAmandaLegareCreateDance.txt -> EventAmandaLegareCreateDance.rpy (rpy_exists)

## Full TXT Coverage (anti-omission list)
- $menu_f.txt
- AdjustOtkroven.txt
- AfterDanceLegare.txt
- AfterDanceSexLegare.txt
- AmandaAtGloryHole.txt
- AmandaAtHomeCode.txt
- AmandaDynamicCommonBlocks.txt
- AmandaLegareDanceSequence.txt
- AmandaLoverSex.txt
- AmandaSexDanceStreet.txt
- Church.txt
- CreateMandatoryEvents.txt
- CreateTavernEventsPeriod.txt
- DailySetstatdefault.txt
- DisplayTavernEventShort.txt
- DressNoShow.txt
- EllonaBirthPrayMenu.txt
- EventAmandaLegareCreateDance.txt
- EventAmandaLizettTalk.txt
- EventAmandaLizettTalk2.txt
- FridayDance.txt
- GirlDressSuggest.txt
- GirlsDesc.txt
- GirlSuggestDressFunc.txt
- GiveBirth.txt
- GiveBirthFinish.txt
- GiveBirthStep2.txt
- HarassDiscussImage.txt
- HarassShowImage.txt
- InitAmanda.txt
- InitAmandaLizaTalkItems.txt
- InitSecondaryNPC.txt
- IntAlberTalk.txt
- IntAmandaDance.txt
- IntAmandaDressChange.txt
- IntAmandaSex.txt
- IntAmandaTalk.txt
- IntLizaDressChange.txt
- Intro.txt
- KidsFunctions.txt
- Loc.txt
- menu_tavernstat.txt
- MomDressComplaint.txt
- MorningSickness.txt
- NextDay_FinishDayEvents.txt
- NextDay_NewDayEvents.txt
- NextDay_TavernDaily.txt
- NextDay.txt
- RelationshipDesc1.txt
- SetTavernServiceLevels.txt
- SexEventsTableCode.txt
- ShowAmandaPortrait.txt
- ShowCurrentSex.txt
- TavernAmandaRoom.txt
- TavernGloryHole.txt
- TavernMain.txt
- TavernShowImage.txt
- WineStore.txt
- ZaletOpinionCalc.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event actions excluded in first pass (hide, do not delete).
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.

## Planning Docs
- `devdocs/characters/amanda_event_plan.md` - Amanda-only event object definition, menu object map, and canonical Amanda event list with menus/scenes.
