# Character Worklist: Кларисса (Clara)

## Identity
- Canonical id: clarisse
- Legacy keys/tokens: Clara, Кларисса, clara
- Init source: InitSecondaryNPC.txt
- Main var store: Friends/Talked key Clara

## Presence/Schedule (TXT-driven notes)
- Утренняя продавщица в WineStore (time == 0).
- Вне утра заменяется на Альбера; прямые ветки Клариссы скрыты.
- Упоминается в церковных/легаре сценах как часть семьи.

## Flags/Variables (Init authority)
- Friends[Clara]
- Talked[Clara]

## Primary Scenes/Dialogs/Features (TXT files)
- WineStore.txt -> WineStore.rpy (rpy_exists)
- Church.txt -> Church.rpy (rpy_exists)
- AfterDanceSexLegare.txt -> AfterDanceSexLegare.rpy (rpy_exists)
- InitSecondaryNPC.txt -> InitSecondaryNPC.rpy (rpy_exists)

## Full TXT Coverage (anti-omission list)
- AfterDanceSexLegare.txt
- Church.txt
- InitSecondaryNPC.txt
- WineStore.txt

## Port TODO
- [ ] Confirm schedule conditions per location/time against source TXT lines.
- [ ] Map every visible non-sex action into character dialog UI buttons.
- [ ] Keep sex/special-event actions excluded in first pass (hide, do not delete).
- [ ] Verify all referenced flags are initialized before first interaction.
- [ ] Add/verify compatibility aliases for legacy calls.
