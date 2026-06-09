# Georgette / Lizette Class And Thread Conversion Plan

Purpose: convert Georgette and Lizette one by one to the same class-first model used for Sandra and Melissa.

Runtime rule:
- `GeorgettInfo` and `LizaInfo` must be the mutable source of truth.
- `GeorgettData` and `LizaData` must hold only immutable/static identity data.
- Legacy tables (`GeorgettVar`, `LizaVar`, `Friends`, `pregnancy`, `jobWhoreAvail`, etc.) are migration/input mirrors only while old systems still need them.
- Event/thread conditions should call class methods or read class attributes, not raw dict expressions.
- Labels present scenes, pictures, menus, and direct consequences; they do not own the availability model.

## Shared Character Model

Both characters are `Girl` runtime objects.

Required static data:
- `code_name`
- display names: nominative/genitive/dative
- description
- card/portrait paths
- birth date / starting age
- default location
- schedule source
- default clothing
- gift preferences

Required runtime state:
- relationship/openness/corruption
- daily talk counters
- known flag
- current location
- work availability: port, tavern, gloryhole
- pregnancy/birth state access
- sex/body state access
- church confession / after-sermon story flags
- tavern relocation state
- dress-shop invitation state
- barber-shop invitation state, when implemented

No generic flirt mechanics:
- Do not add generic `flirt` unlocks.
- Their intimacy path is service/prostitution, church story, tavern work, and authored talk/event gates.

Pregnancy/birth:
- They must remain compatible with the common pregnancy/birth labels.
- Class methods should expose pregnancy stage/status.
- Pregnancy labels may still present birth scenes, but class state must be the source for pregnancy fields once migration reaches that system.

## Georgette Conversion

Current weak runtime:
- `class Georgett(Girl)` exists in `game/NPC/Girls/Georgett/InitGeorgett.rpy`.
- It is only a wrapper around `GeorgettVar`.
- It lacks `GeorgettData`, `GeorgettStaticData`, and `default Georgett = GeorgettInfo()`.
- `georgettThreadList` is empty.

Target classes:
- `GeorgettData(PeopleData)`
- `GeorgettInfo(Girl)`

Core Georgette flags/methods:
- `ask_clients_done`
- `ask_sex_done`
- `ask_family_done`
- `ask_pregnancy_done`
- `ask_kids_done`
- `found_in_church`
- `church_sex_seen`
- `liza_saw_church`
- `church_georgett_admitted`
- `church_liza_admitted`
- `saw_after_sermon`
- `talked_after_sermon`
- `talked_after_sermon_liza`
- `gloryhole_explained`
- `gloryhole_agreed`
- `tell_about_eddie_mom_sex`

Required Georgette methods:
- `sync_georgett_maps()` while legacy compatibility remains.
- `initialize_new_game_state()`.
- `talk_choice_available(choice_id)`.
- `apply_talk_choice(choice_id)`.
- `can_work_portstreets()`.
- `can_work_tavern()`.
- `can_use_gloryhole()`.
- `can_invite_to_tavern()`.
- `invite_to_tavern_result()`.
- `can_ask_about_priest()`.
- `can_trigger_church_service_event()`.
- `can_trigger_after_sermon_event()`.
- `can_schedule_dress_shop_visit()`.
- `can_schedule_barber_visit()`.
- `pregnancy_stage()`.

Georgette event/thread surfaces:
- PortStreets first meeting / work visibility.
- PortStreets prostitution client event.
- Tavern work relocation.
- Tavern prostitution / gloryhole work.
- Church service encounter.
- Church confession admissions.
- After-sermon priest event.
- Dress-shop invitation/buy-dress event.
- Barber-shop visit event, when implemented.
- Becky/Eddie crossover remains a Becky/Eddie thread with Georgette as participant unless promoted later.

## Lizette Conversion

Current weak runtime:
- `class Liza(Girl)` exists in `game/NPC/Girls/Liza/InitLiza.rpy`.
- It is only a wrapper around `LizaVar`.
- It lacks `LizaData`, `LizaStaticData`, and `default Liza = LizaInfo()`.
- `lizaThreadList` is empty.

Target classes:
- `LizaData(PeopleData)`
- `LizaInfo(Girl)`

Core Lizette flags/methods:
- `prost_start`
- `see_clients_done`
- `ask_clients_done`
- `ask_sex_done`
- `ask_pregnancy_done`
- `saw_after_sermon`
- `talked_after_sermon`
- `talked_after_sermon_georgett`
- `gloryhole_mentioned`
- `gloryhole_asked`

Required Lizette methods:
- `sync_liza_maps()` while legacy compatibility remains.
- `initialize_new_game_state()`.
- `talk_choice_available(choice_id)`.
- `apply_talk_choice(choice_id)`.
- `can_work_portstreets()`.
- `can_work_tavern()`.
- `can_use_gloryhole()`.
- `can_trigger_after_sermon_event()`.
- `can_schedule_dress_shop_visit()`.
- `can_schedule_barber_visit()`.
- `pregnancy_stage()`.
- `is_modest_about_pregnancy()` for the unique Lizette talk/sex text branches.

Lizette event/thread surfaces:
- PortStreets availability after Georgette/Gerhard story gate.
- PortStreets prostitution client event.
- Tavern work after Georgette relocation.
- Tavern prostitution / gloryhole work.
- After-sermon priest event.
- Dress-shop invitation/buy-dress event.
- Barber-shop visit event, when implemented.

## Thread/Event Target Lists

`georgettThreadList` should stop being empty and own:
- `georgettPortFirstMeet`
- `georgettChurchService`
- `georgettChurchConfession`
- `georgettAfterSermon`
- `georgettTavernWork`
- `georgettDressShopInvite`
- `georgettBarberVisit`

`lizaThreadList` should stop being empty and own:
- `lizaPortStart`
- `lizaAfterSermon`
- `lizaTavernWork`
- `lizaDressShopInvite`
- `lizaBarberVisit`

PortStreets room should not own these story rules.
It should ask the classes/event manager:
- who is visible here;
- which event is available;
- what object/action labels are available.

## First Implementation Order

1. Georgette class source-of-truth.
2. Georgette source/unit tests.
3. Lizette class source-of-truth.
4. Lizette source/unit tests.
5. PortStreets visibility converted to class methods.
6. PortStreets external click test.
7. Church/after-sermon event definitions and labels.
8. Dress-shop/barber scheduling as event definitions.
9. Pregnancy/birth compatibility tests for both.

Do not refactor talk labels into full event/thread form until class methods exist.
