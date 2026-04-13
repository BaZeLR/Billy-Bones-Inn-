# Amanda Event Plan

Source authority: `game/Inn/*.txt` only.

This plan was built from `devdocs/characters/full_logic/amanda_full_logic.md` after checking `devdocs/agent.txt` and `devdocs/JumpOrCall_usecase.txt`.

## Flow Rules

- Use `call` for Amanda subflows that should return to the current context after local logic or menu handling.
- Use `jump` for Amanda flows that permanently change location, advance scene phase, or end the current context.
- Do not use `renpy.call()` or `renpy.jump()` inside Python blocks. Event/menu objects are planning data for script-side flow only.

### Amanda call targets

- `IntAmandaTalk`
- `IntAmandaDressChange`
- `IntAmandaDance`
- `IntAmandaSex`
- `EventAmandaLizettTalk`
- `EventAmandaLizettTalk2`

### Amanda jump targets

- `TavernMain`
- `TavernAmandaRoom`
- `FridayDance`
- `StreetTavern`
- `AfterDanceLegare`
- `AfterDanceSexLegare`
- `AmandaSexDanceStreet`

## Amanda Branch Scheme

Use this as the branch map before defining final Amanda `MenuObject` and `EventObject` entries.

```text
Amanda
|
+-- 1. Tavern core hub
|   |
|   +-- TavernMain -> IntAmandaTalk
|   |   |
|   |   +-- neutral talk / inspect
|   |   +-- reconciliation branch
|   |   +-- control/release branches
|   |   |   +-- Legare allowed <-> Legare prohibited
|   |   |   +-- Liza contact allowed <-> Liza prohibited
|   |   |   +-- Gloryhole allowed again <-> Glory scold/walkout remembered
|   |   |   +-- Neighbor boys allowed <-> boys prohibited
|   |   |   +-- work-break permission restored
|   |   +-- knowledge branches
|   |   |   +-- lost virginity reveal
|   |   |   +-- sex activity known
|   |   |   +-- zalet risk talk
|   |   |   +-- father-suspect talk after pregnancy
|   |   +-- IntAmandaDressChange subbranch
|   |       +-- suggest more revealing clothes
|   |       +-- shame her for missing underwear
|   |       +-- offer to buy clothes
|   |
|   +-- TavernMain -> TavernAmandaRoom
|       |
|       +-- sleeping-room observation branch
|       +-- approach/grope check
|       +-- room outcome split
|       |   +-- soft refusal -> room ban for current day
|       |   +-- angry refusal + old scolds recalled -> apology/rollback branch
|       |   +-- accept intimacy -> bed sex start
|       |   +-- forced persistence -> CodeAmandaKickFromRoom
|       |
|       +-- bed sex branch
|       |   +-- blowjob only
|       |   +-- bed defloration
|       |   +-- full sex
|       |   +-- cum outside
|       |   +-- cum inside
|       |
|       +-- home eviction consequence branch
|           +-- kickyoufromroom
|           +-- repeated intrusion escalates to kickedwithmomhelp
|           +-- TavernMain hides Amanda room until next-day reset
|           +-- later Amanda/Liza complaint talk can reference this
|   |
|   +-- period tavern events while Amanda is working hall jobs
|       |
|       +-- CreateTavernEventsPeriod
|       |   +-- AmandaLizaTalk is Amanda-specific
|       |   +-- CleaningHarass is shared but can target Amanda through jobcleaning
|       |   +-- WaitressHarass is shared but can target Amanda through jobwaitress
|       |
|       +-- Amanda-specific tavern event
|       |   +-- EventAmandaLizettTalk / Talk2
|       |   +-- changes prohibitliza and lizafriends direction
|       |
|       +-- shared hall-job harassment events
|       |   +-- EventCleaningHarrass -> Amanda if GetRandomGirlByJob('jobcleaning') picks her
|       |   +-- EventWaitressHarrass -> Amanda if GetRandomGirlByJob('jobwaitress') picks her
|       |   +-- eyewitness split: ignore / watch / intervene
|       |   +-- follow-up discussion sets HarassInstructions['amanda']
|       |
|       +-- impacts on Amanda from shared tavern events
|           +-- Friends['amanda'] can rise or fall
|           +-- sluttiness['amanda'] can rise or fall
|           +-- waitress['amanda'] can improve or drop
|           +-- tavernfame can change
|           +-- future harassment behavior is biased by HarassInstructions['amanda']
|
+-- 2. Friday dance branch
|   |
|   +-- FridayDance -> find Amanda
|   |   |
|   |   +-- Amanda alone -> IntAmandaDance
|   |   |   +-- talk/dance/flirt
|   |   |   +-- touch/kiss escalation
|   |   |   +-- invite to walk out -> AmandaSexDanceStreet
|   |   |
|   |   +-- Amanda with Legare
|   |       +-- watch them
|   |       +-- break them up
|   |       +-- transition into AmandaLegareDanceSequence
|   |
|   +-- leave-with-Legare split
|   |   +-- noticed immediately -> AfterDanceLegare
|   |   |   +-- follow
|   |   |   +-- let go
|   |   |   +-- confront Legare
|   |   |   +-- call guards / bribe / punishment fallout
|   |   |
|   |   +-- followed into sex scene -> AfterDanceSexLegare
|   |   |   +-- voyeur path
|   |   |   +-- interrupt path
|   |   |   +-- leave in disgust path
|   |   |
|   |   +-- unnoticed escape -> EscapeUnnoticed
|   |       +-- later "Find Amanda" fails
|   |       +-- Amanda counted as left the dances
|   |
|   +-- Friday dance outputs
|       +-- street sex with player
|       +-- Legare intimacy known / seen
|       +-- control conflict with Amanda increases
|
+-- 3. Street and offscreen encounter branch
|   |
|   +-- daily event generation
|   |   +-- legarerun queued
|   |   +-- lovermeet queued
|   |   +-- glorytry queued
|   |
|   +-- location notice checks
|   |   +-- CheckIfRunToLegare
|   |   |   +-- inspect/follow
|   |   |   +-- ignore
|   |   |   +-- send her back to work
|   |   |
|   |   +-- CheckIfMeetLover
|   |       +-- look closer
|   |       +-- ignore
|   |       +-- enter AmandaLoverSex
|   |
|   +-- AmandaLoverSex branch
|       +-- overhear dialogue first
|       +-- send her back
|       +-- follow them
|       +-- leave them alone
|       +-- unseen resolution if player never intervenes
|
+-- 4. Liza influence branch
|   |
|   +-- tavern event roll -> EventAmandaLizettTalk / Talk2
|   |   +-- Amanda obeys prohibition
|   |   +-- Amanda ignores prohibition
|   |   +-- player praises
|   |   +-- player scolds
|   |   +-- player retracts prohibition
|   |   +-- player eavesdrops only
|   |
|   +-- Liza table content mirrors Amanda state
|       +-- innocence / curiosity about sex
|       +-- Legare fascination
|       +-- gloryhole discussion
|       +-- room-kick complaint
|       +-- pregnancy complaint
|
+-- 5. Gloryhole branch
|   |
|   +-- daily glorytry scheduled
|   +-- TavernGloryHole reveals AmandaAtGloryHole
|   +-- first reaction split
|   |   +-- scold her
|   |   +-- silently walk out
|   |   +-- encourage her to continue
|   |
|   +-- sexual escalation split
|   |   +-- blowjob completed
|   |   +-- kiss after reveal
|   |   +-- direct sex
|   |   +-- cum in mouth / on face / on belly / inside
|   |
|   +-- long-term outputs
|       +-- glorytried
|       +-- gloryscold
|       +-- glorywalkout
|       +-- glorysuck
|       +-- glorydeflower
|       +-- these later feed knowsexactive and talk branches
|
+-- 6. Direct sex branch outside room script
|   |
|   +-- IntAmandaSex in home or street context
|   |   +-- undress / exposure progression
|   |   +-- foreplay
|   |   +-- cunnilingus
|   |   +-- blowjob
|   |   +-- intercourse
|   |   +-- climax choice
|   |   +-- leave / cleanup exit
|   |
|   +-- state outputs
|       +-- suckyou
|       +-- fuckyou
|       +-- knownotvirgin
|       +-- pregnancy checks if inside finish happens
|
+-- 7. Pregnancy and birth branch
|   |
|   +-- pregnancy sources
|   |   +-- player sex
|   |   +-- Legare
|   |   +-- lovers / queued sex events
|   |   +-- rare gloryhole inside cases
|   |
|   +-- awareness phase
|   |   +-- zalet-risk talk before visible pregnancy
|   |   +-- suspect/father calculation after visible pregnancy
|   |   +-- morning sickness event
|   |
|   +-- delivery phase
|       +-- GiveBirth start
|       +-- temple support/prayer step
|       +-- GiveBirthFinish child creation
|
+-- 8. Global consequence/reset branch
    |
    +-- end-of-day propagation
    |   +-- knowsexactive consolidation
    |   +-- glory knowledge consolidation
    |   +-- lover/Legare offscreen event resolution
    |
    +-- daily reset
        +-- kickyoufromroom reset
        +-- askzalettoday reset
        +-- leftdances reset
        +-- bounded friendship counters
```

## Object Shapes

Runtime template lives in `game/engine/story_event_model.rpy`.

Main UI mapping for an active event:

- left picture panel: `Event.picture`
- right actions panel: `Event.menu_items -> UI_actions`
- text window / say screen: `Event.text`

Simple runtime model:

- one active entity in store: `active_event`
- event categories: `random`, `story`, `tavern_work`
- one event class is enough for now
- if an event triggers, the event object itself becomes active and renders in main UI

### EventState

```yaml
EventState:
  inactive:
    condition_list:
      - activation conditions are not met
  active:
    condition_list:
      - activation conditions are met
      - completion conditions are not met
  complete:
    condition_list:
      - completion conditions are met
```

### MenuObject

```yaml
MenuObject:
  menu_name: string
  owner: "amanda"
  entry_context: label or location that creates the menu
  display_check_list:
    - checks that must already be true before calling Menu.Call(menu_name)
  action_list:
    - action_name: visible text
      visible_when:
        - per-item checks from Menu.AddCondition
      flow:
        type: call | jump | inline
        target: label or local branch
      effects:
        - state changes caused by this action
      advances_to: next state, next label, or exit
```

### EventObject

```yaml
Event:
  event_name: string
  event_type: random | story | tavern_work
  state: inactive | active | complete
  activation_condition:
    - inactive -> active checks
  completion_condition:
    - active -> complete checks
  picture: image path or image id for main_ui left panel
  text: text block for say screen
  menu_items:
    - label: visible text
      action: Ren'Py Action()
      condition: optional visibility condition
  source_txt:
    - source authority files
  effects:
    on_activate:
      - variable changes on trigger
    on_complete:
      - variable changes on completion
  updates:
    success:
      - updates after success outcome
    fail:
      - updates after fail outcome
```

## Menu Objects

### MenuAmandaTalk

```yaml
menu_name: MenuAmandaTalk
owner: amanda
entry_context: IntAmandaTalk
display_check_list:
  - Amanda is available in TavernMain talk hub
  - talk flow already entered through IntAmandaTalk
action_list:
  - action_name: Осмотреть
    visible_when: [always]
    flow: { type: call, target: GirlsDesc }
  - action_name: Попробовать помириться с Амандой
    visible_when: [Talked['amanda'] < 3, Friends['amanda'] < 5]
    flow: { type: inline, target: reconciliation branch }
  - action_name: Сказать Аманде что вы передумали и она может встречаться с Альбером
    visible_when: [Talked['amanda'] < 3, AmandaVar['alberprohibit'] > 0]
    flow: { type: inline, target: alber permission branch }
  - action_name: Разрешить Аманде болтать с Лизеттой
    visible_when: [Talked['amanda'] < 3, AmandaVar['prohibitliza'] > 0]
    flow: { type: inline, target: liza permission branch }
  - action_name: Сказать Аманде что вы ошиблись и она может ходить к Лизетте в глорихолл
    visible_when: [Talked['amanda'] < 3, AmandaVar['gloryscold'] > 0]
    flow: { type: inline, target: glory permission branch }
  - action_name: Сказать Аманде что она может встречаться с парнями
    visible_when: [Talked['amanda'] < 3, AmandaVar['prohibitwithguys'] > 0]
    flow: { type: inline, target: neighbor permission branch }
  - action_name: Сказать Аманде что она может иногда брать перерывы
    visible_when: [Talked['amanda'] < 3, AmandaVar['warnnotwork'] > 0]
    flow: { type: inline, target: work break branch }
  - action_name: Спросить где она потеряла девственность
    visible_when: [Talked['amanda'] < 3, AmandaVar['knownotvirgin'] > 0, AmandaVar['knowdeflowerlegare'] == 0, AmandaVar['deflowerlegare'] > 0]
    flow: { type: inline, target: deflower reveal branch }
  - action_name: Запретить ей гулять/трахаться с месье Легаре
    visible_when: [Talked['amanda'] < 3, AmandaVar['knowlegaresex'] > 0, AmandaVar['alberprohibit'] == 0]
    flow: { type: inline, target: legare prohibition branch }
  - action_name: Запретить ей трахаться с соседскими парнями
    visible_when: [Talked['amanda'] < 3, AmandaVar['sawwithguys'] > 0, AmandaVar['prohibitwithguys'] == 0]
    flow: { type: inline, target: neighbor prohibition branch }
  - action_name: Спросить не боиться ли она залететь
    visible_when: [Talked['amanda'] < 3, AmandaVar['knowsexactive'] > 0, pregnancy['amanda'] < 120, AmandaVar['askzalettoday'] == 0, virginity['amanda'] == 0]
    flow: { type: inline, target: pregnancy risk branch }
  - action_name: Спросить, знает ли она от кого пузо нагуляла
    visible_when: [Talked['amanda'] < 3, Friends['amanda'] >= 8, pregnancy['amanda'] >= 120]
    flow: { type: inline, target: daddy suspicion branch }
  - action_name: dress-change extensions
    visible_when: [delegated to IntAmandaDressChange]
    flow: { type: call, target: IntAmandaDressChange }
```

### MenuAmandaDance

```yaml
menu_name: MenuAmandaDance
owner: amanda
entry_context: IntAmandaDance
display_check_list:
  - Friday dance scene already active
  - Amanda has been found from FridayDance
action_list:
  - action_name: Осмотреть
    visible_when: [DanceStep < 10]
  - action_name: Поболтать
    visible_when: [DanceStep == 1, AmandaVar['albernowdances'] == 0]
  - action_name: Пригласить потанцевать
    visible_when: [DanceStep == 1, AmandaVar['albernowdances'] == 0]
  - action_name: Продолжить танцевать
    visible_when: [DanceStep >= 2, DanceStep < DanceMaxIAD, AmandaVar['albernowdances'] == 0]
  - action_name: Положить руки на талию
    visible_when: [DanceStep >= 2, DanceStep < DanceMaxIAD, AmandaVar['albernowdances'] == 0, HandsDance != 'waist']
  - action_name: Положить руки на попу
    visible_when: [DanceStep >= 2, DanceStep < DanceMaxIAD, AmandaVar['albernowdances'] == 0, HandsDance does not match '^ass']
  - action_name: Сжать попу Аманды
    visible_when: [DanceStep >= 2, DanceStep < DanceMaxIAD, AmandaVar['albernowdances'] == 0, HandsDance == 'ass']
  - action_name: Поцеловать Аманду
    visible_when: [DanceStep >= 2, DanceStep < DanceMaxIAD, AmandaVar['albernowdances'] == 0, KissDance == 0]
  - action_name: Предложить Аманде прогулятся
    visible_when: [DanceStep >= 2, DanceStep < DanceMaxIAD, AmandaVar['albernowdances'] == 0, HadSex['amanda'] > 0, HandsDance has ass contact or KissDance > 0]
  - action_name: Наблюдать за Амандой и мессиром Легаре
    visible_when: [DanceStep >= 1, DanceStep < DanceMaxIAD + 2, AmandaVar['albernowdances'] == 1]
  - action_name: Вмешаться и разогнать их
    visible_when: [DanceStep >= 1, DanceStep < DanceMaxIAD + 2, AmandaVar['albernowdances'] == 1]
  - action_name: Отойти
    visible_when: [DanceStep >= DanceMaxIAD or AmandaVar['albernowdances'] == 1 or DanceStep == 1]
```

### MenuAmandaLizaTalk

```yaml
menu_name: MenuAmandaLizaTalk
owner: amanda
entry_context: EventAmandaLizettTalk
display_check_list:
  - jobWhoreAvail['liza'] == 1
  - Eyewitness > 0
  - event text already built
action_list:
  - Похвалить Аманду, за то, что не стала болтать с Лизеттой: [AmandaVar['prohibitliza'] > 0, NotToSpeak == 1]
  - Строго наругать Аманду за то, та болтает с Лизеттой: [AmandaVar['prohibitliza'] > 0, NotToSpeak == 0]
  - Сказать Аманде, чтобы не болтала с Лизеттой: [AmandaVar['prohibitliza'] == 0, NotToSpeak == 0]
  - Сказать Аманде, что она правильно не стала болтать с Лизеттой: [AmandaVar['prohibitliza'] == 0, NotToSpeak == 1]
  - Сказать Аманде, что вы погорячились, когда запретили ей говорить с Лизеттой: [AmandaVar['prohibitliza'] > 0, NotToSpeak == 1]
  - Подслушать: [NotToSpeak == 0]
  - Вернуться к своим делам: [NotToSpeak == 1]
```

### MenuAmandaLizaTalk2

```yaml
menu_name: MenuAmandaLizaTalk2
owner: amanda
entry_context: EventAmandaLizettTalk2
display_check_list:
  - Eyewitness > 0
  - Amanda and Liza have already separated
action_list:
  - Строго наругать Аманду за то, та болтает с Лизеттой: [AmandaVar['prohibitliza'] > 0]
  - Сказать Аманде, чтобы не болтала с Лизеттой: [AmandaVar['prohibitliza'] == 0]
  - Сказать Аманде, что вы погорячились, когда запретили ей говорить с Лизеттой: [AmandaVar['prohibitliza'] > 0]
  - Вернуться к своим делам: [always]
```

### MenuAmandaGloryHole

```yaml
menu_name: MenuAmandaGloryHole
owner: amanda
entry_context: AmandaAtGloryHole
display_check_list:
  - AmandaAtGlory == 1 in TavernGloryHole flow
  - AmandaGloryCurState has been set by the current gloryhole reveal state
action_list:
  - Осмотреть Аманду: [AmandaGloryCurState < 10]
  - Осмотреть Лизетту: [always]
  - Отругать: [AmandaGloryCurState <= 2 or AmandaGloryCurState == 4]
  - Развернуться и уйти, ничего не говоря: [AmandaGloryCurState <= 2 or AmandaGloryCurState == 4]
  - Предложить ей сделать то, что она собиралась: [AmandaGloryCurState == 1]
  - Предложить ей продолжить: [AmandaGloryCurState == 2]
  - Кончить на лицо: [AmandaGloryCurState == 3]
  - Кончить в рот: [AmandaGloryCurState == 3]
  - Поцеловать Аманду: [AmandaGloryCurState == 4]
  - Поблагодарить Аманду: [AmandaGloryCurState == 4 or AmandaGloryCurState == 5]
  - Трахнуть сестру: [AmandaGloryCurState == 5]
  - Кончить в сестренку: [AmandaGloryCurState == 6]
  - Кончить на животик: [AmandaGloryCurState == 6]
```

### AmandaMenuSex

```yaml
menu_name: AmandaMenuSex
owner: amanda
entry_context: IntAmandaSex
display_check_list:
  - Amanda sex scene already active
  - GirlNameASDS == 'amanda'
  - GirlLocASDS in ['street', 'home']
action_list:
  - clothing actions: gated by visible clothes, raised flags, SomebodyCums == 0
  - cleanup actions: gated by cum visibility flags and SomebodyCums == 0
  - foreplay actions: gated by exposure state and arousal thresholds
  - penetration actions: gated by Arousal['You'], Arousal['amanda'], PussyVisible, mode != 'minet'
  - climax actions: gated by Arousal['You'] >= 100 and current cock position
  - exit actions:
      - Попрощаться и уйти: [GirlLocASDS == 'home', SomebodyCums == 0]
      - Привести себя в порядок и вернуться: [GirlLocASDS == 'street', SomebodyCums == 0]
```

## Amanda Event List

```yaml
AmandaEventList:
  - event_name: amanda_talk_hub
    source_txt:
      - IntAmandaTalk.txt
      - IntAmandaDressChange.txt
    scenes:
      - IntAmandaTalk
      - IntAmandaDressChange
    menus:
      - MenuAmandaTalk
    activation_condition:
      - Current location is TavernMain
      - Amanda talk entry is available from the tavern crew dialog hub
    advancement_condition:
      - Talked['amanda'] increments after most meaningful branches
      - AmandaVar permission/prohibition flags open or close talk actions
      - dress-change sub-branches unlock from Friends/GiveOrgasms/clothes state
    entry_flow:
      type: call
      target: IntAmandaTalk
    exits:
      - return to TavernMain interaction context

  - event_name: amanda_shared_tavern_job_events
    source_txt:
      - InitAmanda.txt
      - menu_tavernstat.txt
      - CreateTavernEventsPeriod.txt
      - EventCleaningHarrass.txt
      - EventCleaningHarrassPart2.txt
      - EventWaitressHarrass.txt
      - EventWaitressHarrassPart2.txt
      - PartEventYourFirstReaction.txt
      - PartEventGirlHarrassmentReaction.txt
      - PartEventCustomerHarrassmentReaction.txt
      - PartEventAfterHarrassment.txt
      - IntHarrassmentDiscuss.txt
    scenes:
      - menu_tavernstat
      - CreateTavernEventsPeriod
      - EventCleaningHarrass
      - EventCleaningHarrassPart2
      - EventWaitressHarrass
      - EventWaitressHarrassPart2
      - IntHarrassmentDiscuss
    menus: []
    activation_condition:
      - Amanda is assigned to jobcleaning and/or jobwaitress
      - tavern period event generation rolls a shared hall event
      - GetRandomGirlByJob for that hall role selects Amanda
    advancement_condition:
      - player eyewitness state unlocks ignore/watch/intervene first reaction
      - PartEventGirlHarrassmentReaction resolves Amanda's immediate tolerance or resistance
      - PartEventCustomerHarrassmentReaction applies fame/skill/sluttiness fallout
      - PartEventAfterHarrassment opens IntHarrassmentDiscuss and can set HarassInstructions['amanda']
      - later harassment events reuse HarassInstructions['amanda'] and Amanda sluttiness to bias her reactions
    entry_flow:
      type: call
      target: EventCleaningHarrass or EventWaitressHarrass
    exits:
      - jump TavernMain
      - return to tavern event dispatcher after local resolution

  - event_name: amanda_room_night_entry
    source_txt:
      - TavernAmandaRoom.txt
      - AmandaAtHomeCode.txt
      - IntAmandaSex.txt
    scenes:
      - TavernAmandaRoom
      - AmandaAtHomeCode
      - IntAmandaSex
    menus:
      - AmandaMenuSex
    activation_condition:
      - player enters TavernAmandaRoom
      - time >= 4 for sleeping/bedroom branch
    advancement_condition:
      - cametoday < cancumdaily unlocks approach
      - AmandaSexOfferReaction chooses rejection, apology gate, or sex start
      - tmpSexType chooses blowjob/deflower/full-sex route
    entry_flow:
      type: jump
      target: TavernAmandaRoom
    exits:
      - jump TavernMain

  - event_name: amanda_home_eviction_chain
    source_txt:
      - AmandaAtHomeCode.txt
      - TavernAmandaRoom.txt
      - TavernMain.txt
      - NextDay_FinishDayEvents.txt
      - InitAmandaLizaTalkItems.txt
    scenes:
      - AmandaAtHomeCode
      - TavernAmandaRoom
      - TavernMain
      - InitAmandaLizaTalkItems
    menus: []
    activation_condition:
      - player intrudes on Amanda's room-home branch and pushes past rejection
      - AmandaVar['fuckyou'] == 0 keeps this in the hostile/home-defense path
    advancement_condition:
      - CodeAmandaKickFromRoom sets AmandaVar['kickyoufromroom'] = 1 and increments AmandaVar['kickyoufromroomcount']
      - AmandaVar['kickyoufromroomcount'] >= 3 escalates to AmandaVar['kickedwithmomhelp'] = 1 with Sandra/Melissa intervention
      - TavernMain hides room entry while AmandaVar['kickyoufromroom'] > 0
      - NextDay_FinishDayEvents resets AmandaVar['kickyoufromroom'] = 0 on the next day
      - InitAmandaLizaTalkItems reuses kick flags for Amanda-Lizett complaint talk variants
    entry_flow:
      type: call
      target: AmandaAtHomeCode / CodeAmandaKickFromRoom
    exits:
      - jump TavernMain
      - next-day reset reopens TavernAmandaRoom access

  - event_name: amanda_friday_dance
    source_txt:
      - IntAmandaDance.txt
      - FridayDance.txt
      - AmandaLegareDanceSequence.txt
      - AmandaSexDanceStreet.txt
    scenes:
      - FridayDance
      - IntAmandaDance
      - AmandaLegareDanceSequence
      - AmandaSexDanceStreet
    menus:
      - MenuAmandaDance
    activation_condition:
      - FridayDance scene is active
      - Amanda has been found during the dance
    advancement_condition:
      - DanceStep advances the local dance loop
      - AmandaVar['albernowdances'] switches between player dance and Legare watch mode
      - touch/kiss state unlocks alley-sex invitation
    entry_flow:
      type: call
      target: IntAmandaDance
    exits:
      - return to FridayDance
      - jump AmandaSexDanceStreet
      - jump AfterDanceLegare

  - event_name: amanda_escape_unnoticed
    source_txt:
      - FridayDance.txt
      - AmandaLegareDanceSequence.txt
      - InitAmanda.txt
    scenes:
      - FridayDance
      - AmandaLegareDanceSequence
    menus: []
    activation_condition:
      - FridayDance runs CheckIfAmandaGoneDance during the public dance loop
      - dance-leave table or AmandaVar['LegareGo'] marks Amanda as leaving with Legare
      - random branch chooses the unnoticed escape path
    advancement_condition:
      - FridayDance sets AmandaVar['EscapeUnnoticed'] = 1 when Amanda slips away without immediate player notice
      - selecting "Найти Аманду" later checks AmandaVar['EscapeUnnoticed'] and converts it into AmandaVar['leftdances'] = 1
      - AmandaLegareDanceSequence clears AmandaVar['EscapeUnnoticed'] back to 0 when the direct Legare sequence is entered
    entry_flow:
      type: inline
      target: FridayDance.CheckIfAmandaGoneDance
    exits:
      - remain in FridayDance with Amanda already lost
      - continue into later Legare consequence handling

  - event_name: amanda_legare_afterdance
    source_txt:
      - AmandaLegareDanceSequence.txt
      - AfterDanceLegare.txt
      - AfterDanceSexLegare.txt
    scenes:
      - AmandaLegareDanceSequence
      - AfterDanceLegare
      - AfterDanceSexLegare
    menus: []
    activation_condition:
      - week == 5
      - AmandaLegareDanceSequence created a leave-with-Legare branch
    advancement_condition:
      - LegareGo / alberfriends / sluttiness decide whether Amanda leaves with Legare
      - AmandaNesluhCalc decides obey/disobey/angry confrontation result
      - CurSexStep and tmpLegareSexType advance voyeur scene stages
    entry_flow:
      type: jump
      target: AfterDanceLegare or AfterDanceSexLegare
    exits:
      - jump MarketPlace
      - jump StreetTavern
      - jump NextDay/TavernMain

  - event_name: amanda_gloryhole_try
    source_txt:
      - NextDay_NewDayEvents.txt
      - TavernGloryHole.txt
      - AmandaAtGloryHole.txt
    scenes:
      - TavernGloryHole
      - AmandaAtGloryHole
    menus:
      - MenuAmandaGloryHole
    activation_condition:
      - TodaySexEvents contains Amanda 'glorytry'
      - TavernGloryHole resolves AmandaAtGlory == 1
    advancement_condition:
      - AmandaGloryCurState moves through reveal, blowjob, kiss, sex, and finish states
      - chosen menu action determines shame, silent exit, blowjob continuation, kiss, or sex escalation
    entry_flow:
      type: call
      target: AmandaAtGloryHole
    exits:
      - jump TavernMain

  - event_name: amanda_lover_meet
    source_txt:
      - NextDay_NewDayEvents.txt
      - AmandaLoverSex.txt
      - AmandaDynamicCommonBlocks.txt
    scenes:
      - AmandaLoverSex
      - AmandaDynamicCommonBlocks
    menus: []
    activation_condition:
      - TodaySexEvents contains Amanda 'lovermeet'
      - sexacts['amanda'] >= 5
      - sluttiness['amanda'] >= 35
      - week != 5
    advancement_condition:
      - overheard dialogue resolves to refusal, blowjob consent, or sex consent
      - player then follows, yells, or leaves
      - AmandaLoverSexCalc resolves unseen outcome if player does not follow
    entry_flow:
      type: jump
      target: AmandaLoverSex
    exits:
      - jump StreetTavern

  - event_name: amanda_street_notice_checks
    source_txt:
      - AmandaDynamicCommonBlocks.txt
      - StreetTavern.txt
      - TavernMain.txt
      - MarketPlace.txt
      - SexEventsTableCode.txt
    scenes:
      - AmandaDynamicCommonBlocks
      - StreetTavern
      - TavernMain
      - MarketPlace
    menus: []
    activation_condition:
      - current scene runs Amanda dynamic street checks
      - EventCheckBlock is not set for the current location re-entry
      - TodaySexEvents contains Amanda 'legarerun' or 'lovermeet'
    advancement_condition:
      - CheckIfRunToLegare rolls a notice chance by current location and then resolves follow / ignore / send-to-work
      - CheckIfMeetLover rolls a notice chance and then resolves inspect / ignore / enter AmandaLoverSex
      - GetSexEventFromTable or CheckIfSexEventExist consumes or confirms the queued Amanda event row
    entry_flow:
      type: inline
      target: CheckIfRunToLegare / CheckIfMeetLover
    exits:
      - xgt current location with EventCheckBlock
      - jump AfterDanceSexLegare
      - jump AmandaLoverSex
      - jump StreetTavern

  - event_name: amanda_liza_tavern_event
    source_txt:
      - CreateTavernEventsPeriod.txt
      - EventAmandaLizettTalk.txt
      - EventAmandaLizettTalk2.txt
    scenes:
      - EventAmandaLizettTalk
      - EventAmandaLizettTalk2
    menus:
      - MenuAmandaLizaTalk
      - MenuAmandaLizaTalk2
    activation_condition:
      - CreateTavernEventsPeriod rolled AmandaLizaTalk
      - period is 1 or 2
      - jobWhoreAvail['liza'] == 1
      - jobgloryhole['liza'] == 0 or period < 2
    advancement_condition:
      - AmandaVar['prohibitliza'] and AmandaVar['lizafriends'] decide NotToSpeak
      - Eyewitness decides interactive menu vs auto text continuation
      - Talk2 follow-up resolves late reaction after Amanda and Liza separate
    entry_flow:
      type: call
      target: EventAmandaLizettTalk
    exits:
      - jump TavernMain
      - return event text to tavern-event dispatcher

  - event_name: amanda_zalet_dialogue
    source_txt:
      - IntAmandaTalk.txt
      - ZaletOpinionCalc.txt
      - NextDay_FinishDayEvents.txt
    scenes:
      - IntAmandaTalk
      - ZaletOpinionCalc
    menus:
      - MenuAmandaTalk
    activation_condition:
      - Amanda talk hub is active
      - either AmandaVar['knowsexactive'] > 0 and pregnancy['amanda'] < 120 and virginity['amanda'] == 0
      - or Friends['amanda'] >= 8 and pregnancy['amanda'] >= 120
    advancement_condition:
      - askzalettoday gates the "Спросить не боиться ли она залететь" branch to once per day
      - NextDay_FinishDayEvents resets AmandaVar['askzalettoday'] to 0
      - pregnancy['amanda'] >= 120 unlocks the father-question branch
      - DaddyAskBuildPhrase supplies the final suspect-answer text
    entry_flow:
      type: call
      target: IntAmandaTalk
    exits:
      - return to TavernMain interaction context

  - event_name: amanda_zalet_suspect_calc
    source_txt:
      - ZaletOpinionCalc.txt
      - DailySetstatdefault.txt
      - PregnancyCheck.txt
    scenes:
      - ZaletOpinionCalc
      - DailySetstatdefault
      - PregnancyCheck
    menus: []
    activation_condition:
      - SexHistoryListamanda contains at least one row with Zalet == 1
      - suspect list is requested through ZaletGetSuspectList or DaddyAskBuildPhrase
    advancement_condition:
      - PregnancyCheck writes sex-history rows including inside-cum target and Zalet flag
      - ZaletGetExactDay finds Amanda's pregnancy day
      - ZaletGetSuspectList builds tmpDaddySuspectFinalamanda from inside-cum candidates near the pregnancy window
      - Amanda-specific suspect weighting boosts 'Вы' and recognizes 'Легаре'
    entry_flow:
      type: call
      target: ZaletOpinionCalc
    exits:
      - return built suspect phrase/table to caller

  - event_name: amanda_morning_sickness
    source_txt:
      - DailySetstatdefault.txt
      - MorningSickness.txt
      - ZaletOpinionCalc.txt
    scenes:
      - DailySetstatdefault
      - MorningSickness
    menus: []
    activation_condition:
      - DailySetstatdefault is processing girl 'amanda'
      - no DailyEventsList event of type 'MorningSickness' exists for Amanda
      - either pregnancy['amanda'] > 0 and pregnancy['amanda'] < 80 and Rand(1,7) == 1
      - or pregnancy['amanda'] == 0 and Rand(1,60) == 32
    advancement_condition:
      - CumInsideLastDays and Zaderzhka determine ZaletOpinion
      - player chooses reassurance / suspicion dialogue in MorningSickness
      - branch text varies for Amanda because she worries what Sandra will say
    entry_flow:
      type: call
      target: MorningSickness
    exits:
      - return to current location through ButtonToCurloc

  - event_name: amanda_give_birth
    source_txt:
      - DailySetstatdefault.txt
      - GiveBirth.txt
      - GiveBirthStep2.txt
      - GiveBirthFinish.txt
      - EllonaBirthPrayMenu.txt
    scenes:
      - GiveBirth
      - GiveBirthStep2
      - GiveBirthFinish
      - EllonaBirthPrayMenu
    menus:
      - EllonaMenuDesc
      - EllonaMenuBirthPray
    activation_condition:
      - DailySetstatdefault is processing girl 'amanda'
      - no DailyEventsList event of type 'GiveBirth' exists for Amanda
      - pregnancy['amanda'] > 240 and random labor condition passes, or pregnancy['amanda'] >= 285
      - KnowAboutBirth resolves to 1 for Amanda, so DailyEventsList stores `gt 'GiveBirth'`
    advancement_condition:
      - Loc/CheckDailyEvent gives GiveBirth priority when the event is due
      - GiveBirth sets GirlName to 'amanda' and routes the family-to-temple setup
      - GiveBirthTimer advances labor stages inside GiveBirthStep2
      - prayer choices in EllonaBirthPrayMenu can also advance GiveBirthTimer
      - GiveBirthFinish creates the child and ends with forced sleep / NextDay
    entry_flow:
      type: jump
      target: GiveBirth
    exits:
      - jump GiveBirthStep2
      - jump GiveBirthFinish
      - gs NextDay, TavernMain, 1

  - event_name: amanda_sex_core
    source_txt:
      - IntAmandaSex.txt
    scenes:
      - IntAmandaSex
    menus:
      - AmandaMenuSex
    activation_condition:
      - Amanda consent branch already started from room or street event
      - GirlNameASDS == 'amanda'
    advancement_condition:
      - clothes visibility gates foreplay actions
      - arousal and cock-position state gate oral/sex/climax actions
      - SomebodyCums and location decide which cleanup/exit actions remain
    entry_flow:
      type: call
      target: IntAmandaSex
    exits:
      - jump TavernMain

  - event_name: amanda_daily_feeders
    source_txt:
      - NextDay_NewDayEvents.txt
      - CheckDailyEvent.txt
      - IntAmandaDressChange.txt
    scenes:
      - NextDay_NewDayEvents
      - CheckDailyEvent
      - IntAmandaDressChange
    menus: []
    activation_condition:
      - new day generation
      - Amanda talk branch schedules future dress event
    advancement_condition:
      - TodaySexEvents receives glorytry, legarerun, lovermeet rows
      - DailyEventsList receives BuyDressTom/BuyDress rows
    entry_flow:
      type: call
      target: NextDay_NewDayEvents or CheckDailyEvent
    exits:
      - return to day-generation flow
```

## Event Objects

### amanda_talk_hub

```yaml
event_name: amanda_talk_hub
source_txt: IntAmandaTalk.txt
activation_condition:
  - Current location is TavernMain
  - Amanda talk link is shown from TavernMain
advancement_condition:
  - Talked['amanda'] increments on most substantive branches
  - AmandaVar permission/prohibition flags unlock or hide future actions
entry_flow: { type: call, target: IntAmandaTalk }
menus: [MenuAmandaTalk]
branches:
  - reconciliation
  - Alber permission/prohibition
  - Liza permission/prohibition
  - gloryhole permission reset
  - neighbor sex permission/prohibition
  - pregnancy talk
  - deflower reveal
  - dress-change follow-up
completion: return to TavernMain context
```

### amanda_dress_change

```yaml
event_name: amanda_dress_change
source_txt: IntAmandaDressChange.txt
activation_condition:
  - called from IntAmandaTalk
  - Friends['amanda'] and GiveOrgasms['amanda'] thresholds met per action
advancement_condition:
  - Talked['amanda'] < 2 gates each dress-change action
  - bra/panties state and CheckDailyEventExists control redress and buy-dress options
entry_flow: { type: call, target: IntAmandaDressChange }
menus: [MenuAmandaTalk]
branches:
  - propose no bra
  - propose no panties
  - shame for no bra
  - shame for no panties
  - schedule dress purchase via DailyEventsList
completion: returns to IntAmandaTalk
```

### amanda_room_night_entry

```yaml
event_name: amanda_room_night_entry
source_txt: TavernAmandaRoom.txt
activation_condition:
  - player enters TavernAmandaRoom
  - time >= 4 for sleeping Amanda branch
advancement_condition:
  - cametoday < cancumdaily unlocks approach
  - AmandaSexOfferReaction decides rejection, apology demand, or sex start
entry_flow: { type: jump, target: TavernAmandaRoom }
menus: [AmandaMenuSex]
branches:
  - room empty at day -> jump TavernMain
  - soft rejection -> set AmandaVar['kickyoufromroom'] and jump TavernMain
  - angry hypocrisy rejection -> scold list, penalties, jump TavernMain
  - apology gate -> local sorry choices then either exit or sex
  - consent branch -> call IntAmandaSex/home flow
completion: jump TavernMain
```

### amanda_friday_dance

```yaml
event_name: amanda_friday_dance
source_txt: IntAmandaDance.txt
activation_condition:
  - FridayDance scene active
  - Amanda found through FridayDance search
advancement_condition:
  - DanceStep controls phase progression
  - AmandaVar['albernowdances'] splits player-dance route from Legare-watch route
entry_flow: { type: call, target: IntAmandaDance }
menus: [MenuAmandaDance]
branches:
  - player dances with Amanda
  - escalate touch/kiss
  - invite to leave for alley sex -> jump AmandaSexDanceStreet
  - watch Legare sequence
  - intervene and force separation
completion: return to FridayDance parent context unless branch jumps away
```

### amanda_legare_dance_creation

```yaml
event_name: amanda_legare_dance_creation
source_txt: AmandaLegareDanceSequence.txt
activation_condition:
  - week == 5
  - Amanda dance system is being prepared
advancement_condition:
  - AmandaVar['alberfriends'], AmandaVar['alberprohibit'], sluttiness['amanda'] determine DanceCreated and LegareGo
  - GirlDance rows are inserted with GoOut markers
entry_flow: { type: call, target: AmandaLegareDanceSequence }
menus: []
branches:
  - create zero to several dance rows
  - mark one row as leave-with-Legare branch
  - define LegareAmandaLetGoCode side effects
  - define LegareAmandaGoCode menu-like exit choice
completion: return to FridayDance setup
```

### amanda_legare_afterdance_confrontation

```yaml
event_name: amanda_legare_afterdance_confrontation
source_txt: AfterDanceLegare.txt
activation_condition:
  - entered from LegareAmandaGoCode with 'Prohibit'
  - or entered later with 'Fight' / 'Police'
advancement_condition:
  - AmandaNesluhCalc decides obey/disobey/angry
  - follow-up player choice picks let go, tail, fight, or police
entry_flow: { type: jump, target: AfterDanceLegare }
menus: []
branches:
  - obeys -> Amanda sent home, return to MarketPlace
  - disobeys -> choose let go, tail, fight, or police
  - fight -> fight result split into win/loss/draw
  - police -> shy collapse, bribe, or forced release paths
completion:
  - jump MarketPlace
  - jump StreetTavern
  - jump NextDay/TavernMain on jail branch
```

### amanda_legare_afterdance_voyeur

```yaml
event_name: amanda_legare_afterdance_voyeur
source_txt: AfterDanceSexLegare.txt
activation_condition:
  - player followed Amanda and Legare
advancement_condition:
  - CurSexStep advances scene stage
  - tmpLegareSexType selects blowjob / deflower / regular sex variants
  - knowledge flags decide whether interrupt branches are available
entry_flow: { type: jump, target: AfterDanceSexLegare }
menus: []
branches:
  - watch silently through staged steps
  - interrupt and shame Amanda
  - reveal yourself as watcher
  - leave early -> LegareAmandaLetGoCode then jump StreetTavern
  - watch to completion -> set knowlegaresex/sawlegaresex/fucklegare/sucklegare and pregnancy outcomes
completion: jump StreetTavern after final leave
```

### amanda_gloryhole_try

```yaml
event_name: amanda_gloryhole_try
source_txt:
  - AmandaAtGloryHole.txt
  - TavernGloryHole.txt
  - NextDay_NewDayEvents.txt
activation_condition:
  - TodaySexEvents contains Amanda 'glorytry'
  - TavernGloryHole detects AmandaAtGlory == 1
advancement_condition:
  - AmandaGloryCurState moves 0 -> 1/2 -> 3 -> 4 -> 5 -> 6 -> 10
  - selected menu action controls whether branch ends at shame, blowjob, kiss, or sex
entry_flow: { type: call, target: AmandaAtGloryHole }
menus: [MenuAmandaGloryHole]
branches:
  - inspect Amanda/Liza
  - scold and shut down the event
  - walk out silently
  - allow or resume blowjob
  - choose cum target
  - kiss Amanda
  - thank Amanda and end
  - escalate to sex, then choose inside/outside finish
completion: jump TavernMain
```

### amanda_lover_meet

```yaml
event_name: amanda_lover_meet
source_txt:
  - AmandaLoverSex.txt
  - AmandaDynamicCommonBlocks.txt
  - NextDay_NewDayEvents.txt
activation_condition:
  - TodaySexEvents contains Amanda 'lovermeet'
  - sexacts['amanda'] >= 5
  - sluttiness['amanda'] >= 35
  - week != 5
advancement_condition:
  - eavesdropped dialogue selects refuse / blowjob agree / sex agree
  - player chooses follow, yell, or leave
  - AmandaLoverSexCalc resolves unseen outcome when player leaves
entry_flow: { type: jump, target: AmandaLoverSex }
menus: []
branches:
  - yell and send back to work
  - listen to negotiation
  - blowjob route -> follow or leave
  - sex route -> follow or leave
  - voyeur resolution scene with random place and cum outcome
completion: jump StreetTavern
```

### amanda_liza_tavern_event

```yaml
event_name: amanda_liza_tavern_event
source_txt:
  - EventAmandaLizettTalk.txt
  - EventAmandaLizettTalk2.txt
  - CreateTavernEventsPeriod.txt
activation_condition:
  - CreateTavernEventsPeriod rolls AmandaLizaTalk
  - period in [1, 2]
  - jobWhoreAvail['liza'] == 1
  - jobgloryhole['liza'] == 0 or period < 2
advancement_condition:
  - AmandaVar['prohibitliza'] and AmandaVar['lizafriends'] decide NotToSpeak
  - Eyewitness decides whether to show menu or auto-resolve Talk2 text
entry_flow: { type: call, target: EventAmandaLizettTalk }
menus: [MenuAmandaLizaTalk, MenuAmandaLizaTalk2]
branches:
  - Amanda obeys existing ban -> praise, revoke ban, or leave
  - Amanda breaks existing ban -> scold or overhear
  - no ban active -> impose ban or validate refusal
  - talk2 follow-up -> late scold, late ban, or apology/retraction
completion: jump TavernMain or return text-only result for tavern event summary
```

## Amanda Queue Feeders

These are system activators that should stay outside the scene labels but must map into Amanda EventObjects.

```yaml
feeders:
  - feeder_name: amanda_glorytry_daily_roll
    source_txt: NextDay_NewDayEvents.txt
    writes: TodaySexEvents('amanda', 99, 99, 'glorytry')
  - feeder_name: amanda_legarerun_daily_roll
    source_txt: NextDay_NewDayEvents.txt
    writes: TodaySexEvents('amanda', 3, 99, 'legarerun')
  - feeder_name: amanda_lovermeet_daily_roll
    source_txt: NextDay_NewDayEvents.txt
    writes: TodaySexEvents('amanda', 2, 99, 'lovermeet')
  - feeder_name: amanda_talk_daily_events
    source_txt:
      - CheckDailyEvent.txt
      - IntAmandaDressChange.txt
    writes: DailyEventsList('amanda', ..., 'BuyDressTom' / 'BuyDress')
```

## Recommended Build Order

1. Keep `MenuObject` creation in the owning Amanda label, then `call Menu_Call(menu_name)` only after the `display_check_list` passes.
2. Implement `EventObject` entry labels first: talk hub, Liza talk event, Friday dance, room visit.
3. Implement Amanda system feeders next: `glorytry`, `legarerun`, `lovermeet`, dress-buy scheduling.
4. Implement long-form multi-step scenes last: gloryhole, after-dance voyeur, full `AmandaMenuSex`.
