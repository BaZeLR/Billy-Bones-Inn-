# Character Worklist: Ингенборг

## Identity
- Canonical id: inga
- Legacy keys/tokens: inga, IngaVar
- Init source: InitInga.txt
- Main var store: IngaVar

## Presence/Schedule (TXT-driven notes)
- Связана с ветками семьи Бекки (BeckyHome*, GroceryStore).
- Видимость и часть сцен gated по IngaVar[Knowher].

## Flags/Variables (Init authority)
- SawLucassex
- Knowher

## Primary Scenes/Dialogs/Features (TXT files)
- InitInga.txt -> InitInga.rpy (rpy_exists)
- BeckyHomeFront.txt -> BeckyHomeFront.rpy (rpy_exists)
- BeckyHome.txt -> BeckyHome.rpy (rpy_exists)
- IntBeckyGuest.txt -> IntBeckyGuest.rpy (rpy_exists)

## Full TXT Coverage (anti-omission list)
- BeckyHome.txt
- BeckyHomeFront.txt
- DailySetstatdefault.txt
- EllonaBirthPrayMenu.txt
- FrancheskaTalk.txt
- GeorgettBeckyVisit.txt
- GiveBirth.txt
- GiveBirthFinish.txt
- GiveBirthStep2.txt
- GroceryStore.txt
- InitBecky.txt
- InitInga.txt
- InitSecondaryNPC.txt
- IntBeckyGuest.txt
- IntBeckyTalk.txt
- IntBeckyTalkSherwood.txt
- IntEddieTalk.txt
- Intro.txt
- KidsFunctions.txt
- NextDay_FinishDayEvents.txt
- NextDay_NewDayEvents.txt
- ZaletOpinionCalc.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event actions excluded in first pass (hide, do not delete).
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.
