# Becky Story Chronology and Event/Thread Map

Scope: planning document only. This file maps current Becky runtime logic and extracted dialogue coverage before refactoring Becky into the class-first event/thread model.

Runtime source: live `.rpy` files under `game/NPC/Girls/Becky/`, `game/Town/BeckyHome*.rpy`, `game/Town/GroceryStore.rpy`, and linked Eddie/Sherwood/Birth files.

Dialogue source: `dialogue.tab`, filtered by Becky filenames, Becky identifiers, and Becky/Rebekka text mentions.

## Current Runtime Sources

Primary Becky files:

| File | Current role |
| --- | --- |
| `game/NPC/Girls/Becky/InitBecky.rpy` | Legacy initialization, schedule, partial `class Becky(Girl)` bridge. |
| `game/NPC/Girls/Becky/IntBeckyTalk.rpy` | Main Becky talk menu gates. Currently wrapper/action-item style. |
| `game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy` | Main talk topic scene text and state updates. |
| `game/NPC/Girls/Becky/IntBeckyTalkSherwood.rpy` | Sherwood/Blackwood trade talk tree. Currently wrapper/action-item style. |
| `game/NPC/Girls/Becky/IntBeckyDance.rpy` | Friday dance interaction and invitation setup. |
| `game/NPC/Girls/Becky/BeckyInviteHome.rpy` | Dance/home invitation scene. |
| `game/NPC/Girls/Becky/IntBeckyGuest.rpy` | Dinner/home visit flow. Uses classic menu style and owns major home visit progression. |
| `game/NPC/Girls/Becky/IntBeckySex.rpy` | Becky sex interaction engine. Not first conversion target. |
| `game/NPC/Girls/Becky/IntBeckyAfterCermon.rpy` | Church after-ceremony Becky content. |
| `game/NPC/Girls/Becky/GeorgettBeckyVisit.rpy` | Georgett/Eddie/Becky home crossover. |
| `game/NPC/Girls/Becky/BeckyEddieJoinFirst.rpy` | First Eddie-joins-Becky scene and failure/success branch. |
| `game/NPC/Girls/Becky/BeckyQuestInit.rpy` | Starts Sherwood trade offer. |
| `game/NPC/Girls/Becky/BeckyLoversInStore.rpy` | Grocery store lover/random scenes. |
| `game/NPC/Girls/Becky/BeckyEvents.rpy` | Mixed Becky event labels: home visit, Eddie black eye, Blackwood/Sherwood hooks. |
| `game/Town/BeckyHomeFront.rpy` | Becky house exterior / spying / Inga-Lucas discovery. |
| `game/Town/BeckyHome.rpy` | Becky house interior and dinner entry. |
| `game/Town/GroceryStore.rpy` | Becky workplace access and store actions. |

Linked non-Becky files:

| File | Current role |
| --- | --- |
| `game/NPC/Secondary/IntEddieBeckySex.rpy` | Eddie-specific Becky sex interaction. |
| `game/NPC/Secondary/SherwoodTravel.rpy` | Sherwood trade travel outcome. |
| `game/Town/Temple/GiveBirth.rpy` | Birth scenes involving Becky/Inga. |
| `game/Town/Temple/GiveBirthFinish.rpy` | Birth finish scenes involving Becky. |
| `game/Town/Temple/GiveBirthStep2.rpy` | Birth middle step involving Becky. |

## Extracted Dialogue Coverage

Filtered `dialogue.tab` coverage found 556 Becky-related dialogue rows:

| Dialogue file | Rows |
| --- | ---: |
| `game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy` | 99 |
| `game/NPC/Girls/Becky/IntBeckySex.rpy` | 89 |
| `game/Town/BeckyHomeFront.rpy` | 74 |
| `game/NPC/Girls/Becky/IntBeckyGuest.rpy` | 54 |
| `game/NPC/Secondary/IntEddieBeckySex.rpy` | 44 |
| `game/NPC/Girls/Becky/IntBeckyDance.rpy` | 41 |
| `game/NPC/Girls/Becky/GeorgettBeckyVisit.rpy` | 35 |
| `game/NPC/Girls/Becky/IntBeckyDressChange.rpy` | 32 |
| `game/NPC/Girls/Becky/BeckyEddieJoinFirst.rpy` | 30 |
| `game/Town/BeckyHome.rpy` | 20 |
| `game/Town/Temple/GiveBirth.rpy` | 9 |
| `game/NPC/Girls/Becky/BeckyLoversInStore.rpy` | 8 |
| `game/NPC/Girls/Becky/BeckyQuestInit.rpy` | 8 |
| `game/NPC/Girls/Becky/BeckyInviteHome.rpy` | 3 |
| `game/Utilities/General/Sex/ShowCurrentSex.rpy` | 3 |
| `game/Inn/TavernStable.rpy` | 2 |
| `game/NPC/Secondary/SherwoodTravel.rpy` | 2 |
| `game/Town/Temple/GiveBirthFinish.rpy` | 2 |
| `game/Town/Temple/GiveBirthStep2.rpy` | 1 |

Important extracted dialogue line anchors:

| File | Extracted line anchors |
| --- | --- |
| `BeckyEddieJoinFirst.rpy` | 17, 25, 29, 107, 108 |
| `BeckyInviteHome.rpy` | 18, 20, 22 |
| `BeckyLoversInStore.rpy` | 13, 15, 17, 30, 32 |
| `BeckyQuestInit.rpy` | 7, 8, 9, 24, 25 |
| `GeorgettBeckyVisit.rpy` | 19, 21, 22, 155, 157 |
| `IntBeckyDance.rpy` | 69, 71, 75, 226, 234 |
| `IntBeckyDressChange.rpy` | 95, 98, 100, 203, 215 |
| `IntBeckyGuest.rpy` | 46, 48, 51, 248, 250 |
| `IntBeckySex.rpy` | 100, 104, 110, 493, 495 |
| `IntBeckyTalkTopics.rpy` | 5, 7, 10, 322, 323 |
| `IntEddieBeckySex.rpy` | 66, 68, 80, 270, 274 |
| `BeckyHomeFront.rpy` | 149, 152, 157, 363, 365 |
| `BeckyHome.rpy` | 134, 135, 136, 217, 219 |
| `GiveBirth.rpy` | 61, 62, 70, 262, 263 |
| `GiveBirthFinish.rpy` | 22, 63 |
| `GiveBirthStep2.rpy` | 34 |

## Current State Variables

Current legacy initialization in `InitBecky.rpy` sets:

| Group | Current fields |
| --- | --- |
| Identity/display | `RealName`, `RealName2`, `RealName3`, `girltextdesc` |
| Body/basic stats | `age_girls`, `kids`, `beauty`, `sluttiness`, `virginity` |
| Sex/pregnancy | `sexacts`, `cuminside`, `pregnancy`, `pregfather`, `ConceptionChance`, `PussyWetStart` |
| Dress | `dressdefault`, `bradef`, `pantiesdef`, `legsdef`, `shoesdef` |
| Work skills | `cooking`, `cleaning`, `waitress` |
| Tavern jobs | `jobkitchen`, `jobcleaning`, `jobwaitress`, `jobHallAvail`, `jobWhoreAvail`, `jobwhore`, `jobgloryhole` |
| Relationship | `Friends`, `otkroven` |
| Gifts | `GiftPreferences["becky"]` |

Current `BeckyVar` flags:

| Group | Flags |
| --- | --- |
| Dance/home access | `leftdances`, `danceinvitehome`, `visitedhome`, `TimesVisited` |
| Talk chains | `husbandtalk`, `eddietalk`, `SawIngaFuck`, `IngaSexGreet`, `TalkAboutEddie`, `GeorgMention`, `EddieIntrReact`, `AskedEddieFuck` |
| Home/Eddie/Georgett | `VisitScolded`, `TodayFrontSexCheck`, `HomeSex`, `EddieGeorg`, `EddieWhoreHome`, `BeckyOpenMinet`, `EddieTryToFuck`, `EddieFailures` |
| Church | `PriestAdvice`, `GerhardBeckyTalk` |
| Sherwood/Blackwood | `EddieRobbedDay`, `KnowSherwood`, `SherwoodSuspect`, `TradeOffer`, `TradeOfferText`, `SherwoodWarn`, `AskTradeElf`, `FingalClarify`, `AdmitSherwood`, `RobbedByRobin`, `ConsoleRobbery` |
| Sandra visit | `SandraKitchenVisitMonth` |

## Target Class Split

`BeckyData` should contain only values that do not change during play:

| Field | Candidate value/source |
| --- | --- |
| `code_name` | `"becky"` |
| `display_name` | `"Бекки"` |
| `full_name` | `"Ребекка Блэнкеншип"` |
| `description` | Current `girltextdesc["becky"]` |
| `default_clothing` | `openworkdress`, default underwear/stockings/shoes |
| `base_skills` | cooking 70, cleaning 50, waitress 40 |
| `gift_preferences` | soap, wild rose, pig lard, libido tincture, ale |
| `schedule_source` | current schedule/json once hourly schedule is finalized |
| `portrait/card paths` | to be verified from image folders before class conversion |

`BeckyInfo` should contain mutable state:

| Field group | Candidate fields |
| --- | --- |
| Relationship/runtime | `relationship`, `openness`, current location, current schedule result |
| Daily flags | talked today, asked today, gifted today, flirted today if Becky uses them, drunk state |
| Body/runtime | current beauty, pregnancy, pregfather, conception chance, sex history |
| Clothing/runtime | current dress, underwear state, gifted wardrobe |
| Story flags | all current `BeckyVar` story flags as real class attributes |
| Talk state | husband chain, Eddie chain, Inga chain, Sherwood chain |
| Home state | visited home stage, home sex unlocked, dinner/home visit counters |
| Church state | priest advice, Gerhard talk state |
| Sherwood state | trade offer, suspicion, warning, robbery, admission |

Final target: Becky class instance is the source of truth. Legacy dict writes should not be kept as parallel state after a phase is converted.

## Chronological Story Order

| Order | Phase/thread | Current labels/files | Trigger/gates | State read/written | Target model |
| ---: | --- | --- | --- | --- | --- |
| 0 | Initialization and town presence | `InitBecky`, `GroceryStore`, `BeckyHome`, `BeckyHomeFront` | Game init, room entry, schedule lookup | identity, schedule, grocery access | `BeckyData` + `BeckyInfo`; hourly schedule; room/NPC visibility uses class schedule result |
| 1 | Basic acquaintance and grocery talk | `IntBeckyTalk`, `IntBeckyTalkTopics` | Becky visible/talkable, player chooses talk | `Friends`, `Talked`, relationship, smalltalk/personal gates | Becky unique talk interaction, classic `menu:`, class methods for available topics |
| 2 | Personal trust and husband history | `_husband1` to `_husband4` in `IntBeckyTalkTopics` | `Friends` thresholds, `husbandtalk` stage | `husbandtalk`, relationship/openness | `becky_husband_backstory` repeat/progression thread or Becky talk subthread |
| 3 | Inga/Lucas discovery | `BeckyHomeFront`, `_inga1`, `_inga2`, `_lucas` | Home-front spying and talk gates | `SawIngaFuck`, `IngaSexGreet` | `becky_inga_lucas_discovery` thread; exterior labels own spy scenes |
| 4 | Friday dance relationship path | `IntBeckyDance`, `BeckyInviteHome` | Friday dance schedule, dance choices | `leftdances`, `danceinvitehome` | `becky_friday_dance` event set; dance label uses classic menus and advances invite state |
| 5 | First home invitation | `BeckyInviteHome`, `BeckyHome`, `IntBeckyGuest` | Dance/home invitation or talk invite | `visitedhome`, `TimesVisited`, dinner local vars | `becky_home_invitation` thread; starts home/dinner visit |
| 6 | Home dinner progression | `IntBeckyGuest` | Enter Becky home with visit mode | `visitedhome`, `HomeSex`, `GiveOrgasms`, relationship, time | `becky_home_dinner` event labels; choices update class attributes after scene |
| 7 | Home erotic unlock | `IntBeckyGuest`, `IntBeckySex` | `visitedhome` and arousal/sluttiness/home state gates | `HomeSex`, sex counters, pregnancy risk | Becky sex remains sex-engine call target; access gate belongs to Becky class/story flags |
| 8 | Eddie concern and talk chain | `_eddie1` to `_eddie7`, `BeckyEddieJoinFirst` | Eddie/Georgett events, home visits, priest advice | `eddietalk`, `TalkAboutEddie`, `GeorgMention`, `EddieIntrReact`, `AskedEddieFuck`, `EddieTryToFuck`, `EddieFailures` | `becky_eddie_boundary` thread; talk options are Becky-specific, not generic social topics |
| 9 | Georgett/Eddie/Becky home crossover | `GeorgettBeckyVisit`, `BeckyEvents` home visit labels | Georgett/Eddie home stage | `EddieWhoreHome`, `BeckyOpenMinet`, `visitedhome` | `becky_georgett_home_visit` thread; authored labels in Becky event file |
| 10 | Church and priest advice | `IntBeckyAfterCermon`, linked church/confession labels | Sunday ceremony/after ceremony, knows Becky, Eddie state | `PriestAdvice`, `GerhardBeckyTalk`, `visitedhome` | `becky_church_advice` thread; conditions check event attributes directly |
| 11 | Grocery lover/random scenes | `BeckyLoversInStore`, `GroceryStore` | Grocery room, store open, lover/day conditions | store lover flags, possible relationship changes | Store random/mandatory event definitions; labels in Becky event file |
| 12 | Sherwood trade offer | `BeckyQuestInit`, `IntBeckyTalkSherwood`, `TavernStable`, `SherwoodTravel` | Trade offer gate, trust/suspicion, travel ability | `TradeOffer`, `TradeOfferText`, `KnowSherwood`, `SherwoodWarn`, `SherwoodSuspect`, `AskTradeElf`, `FingalClarify`, `AdmitSherwood`, `RobbedByRobin`, `ConsoleRobbery` | `becky_sherwood_trade` thread; travel events use existing travel/combat systems |
| 13 | Blackwood/road consequences | `BeckyEvents`, `SherwoodTravel`, Zimmer/Robin labels | Sherwood progress, robbed/warned/vouched states | `KnowBlackwood`, `SherwoodQuestScheduled`, robbery/guard progress | `becky_blackwood_road` thread linked to Sherwood thread |
| 14 | Pregnancy and birth | `GiveBirth`, `GiveBirthStep2`, `GiveBirthFinish`, `ShowCurrentSex` | pregnancy counters and father state | `pregnancy`, `pregfather`, `kids`, birth result | General pregnancy/birth mechanics on Girl class; Becky/Inga content labels remain authored scenes |

## Becky Talk Mechanism

Becky should not be converted to the generic topic grid only. Her talk is stateful like Georgett:

- relationship/trust changes unlock personal topics;
- husband history is a staged chain;
- Inga/Lucas discovery changes what can be asked;
- Eddie discussion depends on several external events;
- Sherwood trade talk is its own branch and should remain Becky-specific;
- pregnancy question depends on pregnancy progress and talk count.

Target structure:

| Responsibility | Owner |
| --- | --- |
| Which Becky talk options are available | Becky class methods or event/thread condition checks |
| Text and player choices for a selected talk topic | Ren'Py labels with classic `menu:` |
| State mutation after a topic is played | Label applies direct class attribute changes after displayed scene |
| HUD/persistent right side | `main_ui` remains visible; no modal event overlay |
| Daily reset | Becky daily reset method called from the daily reset system |

Current wrappers to remove during conversion:

- `IntBeckyTalkRefresh`
- `IntBeckyTalkApply`
- `IntBeckyTalkSherwoodRefresh`
- `IntBeckyTalkSherwoodApply`
- one-choice dispatch labels that only call another story label

## Event/Thread Conversion Rules For Becky

1. Convert one coherent phase at a time.
2. Before conversion, list every current flag read/write for that phase.
3. Move phase flags to Becky class attributes and stop writing a parallel dict for converted fields.
4. Event/thread definition owns trigger location, hour/minute window, repeat policy, active/completed state, and condition checks.
5. Event labels own scene text, `vscene` path, classic `menu:`, and final consequences.
6. At the end of the chosen branch, update Becky/player/tavern state, call direct calendar advance if the event costs time, and advance/complete the thread.
7. Return/jump to the event origin location according to how the label was entered.
8. Do not introduce refresh/rebuild/apply/dispatcher/fallback wrappers.

## Proposed Thread List

| Thread id | Purpose | Repeat |
| --- | --- | --- |
| `becky_basic_talk` | Smalltalk/personal topics and daily talk limits | Repeatable |
| `becky_husband_backstory` | Erik/husband staged talk chain | Stage progression |
| `becky_inga_lucas_discovery` | Home-front spying and daughter/fiance reveal | Stage progression |
| `becky_friday_dance` | Friday dance, flirting, home invitation | Weekly/repeatable with stages |
| `becky_home_invitation` | Invite and first entry into Becky home | Stage progression |
| `becky_home_dinner` | Dinner visit choices and home relationship progression | Repeatable with gated stages |
| `becky_home_sex_unlock` | Unlock and route into Becky sex engine | Repeatable after unlock |
| `becky_eddie_boundary` | Eddie discussion, advice, first join attempt | Stage progression |
| `becky_georgett_home_visit` | Georgett/Eddie/Becky home crossover | Stage progression |
| `becky_church_advice` | Church/after-ceremony/Gerhard advice | Stage progression/repeatable scenes |
| `becky_store_lovers` | Store lover scenes | Random/repeatable with daily cooldown |
| `becky_sherwood_trade` | Trade offer and route to Sherwood | Stage progression |
| `becky_blackwood_road` | Robbery/Robin/Zimmer road consequences | Stage progression |
| `becky_pregnancy_birth` | Pregnancy/birth scenes and family effects | General Girl mechanics plus Becky-specific scenes |

## First Safe Conversion Target

Recommended first Becky conversion: `becky_basic_talk` plus `becky_husband_backstory`.

Reason:

- all content is concentrated in `IntBeckyTalk.rpy` and `IntBeckyTalkTopics.rpy`;
- it is visibly broken into discrete talk choices already;
- it exercises Becky-specific talk mechanics without touching sex engine, birth, or Sherwood travel;
- it lets us prove class attributes and classic menus before converting larger event branches.

Minimum acceptance for first conversion:

- Becky class has explicit fields for talk chains used by this phase;
- `IntBeckyTalk` is readable and uses classic Ren'Py `menu:`;
- no refresh/apply wrapper is needed for converted choices;
- current dialogue text is preserved;
- after a topic, state changes happen once and player returns to the normal room/NPC interaction flow;
- compile passes;
- visual debug board can jump to Becky talk and show current Becky state.

## Open Questions Before Class Conversion

- Becky currently has `age_girls["becky"] = 36`, but no immutable birth date. If age becomes calendar-driven, define `birth_day`, `birth_period`, and starting cycle.
- Confirm final hourly/half-hour Becky schedule before converting schedule into class/json truth.
- Decide whether Eddie-linked story state lives on Becky, Eddie, or a shared family/thread object. Do not duplicate it.
- Decide which `BeckyLoversInStore` scenes are random daily grocery events and which are story-gated mandatory events.
- Verify card/portrait paths for Becky before adding them to `BeckyData`.
- Pregnancy/birth should use the general Girl pregnancy mechanics once finalized; Becky labels should only provide authored presentation.
