# Random Town RThread Events Plan

This document captures the town street event concept before implementation. The goal is a living city layer: short random chronicles on town entry, later promoted into `RThreadData` story hooks where useful.

## Current Context

Systems already present and relevant:

- Tavern morning system and breakfast/scheduling.
- Sunday scheduling and church attendance.
- Clarissa market story events.
- Clarissa/Legare wine-basement spanking story event.
- Mongol horse-theft to runaway story path.
- Tavern working events with cleaners and waitresses.
- Random tavern/business events.
- Town rooms that can host street events: `StreetTavern`, `MarketPlace`, `PortStreets`, `ArtisansQuarter`, and nearby shop streets.

Existing name helpers are in `game/Utilities/General/NPC/NamesSet.rpy`:

- `RandomNameCode(gender="", nationality="")`
- `RandomOccupCode()`
- `RandomStreetNameCode()`
- `RandomStallionNameCode()`
- `StreetNameList`
- `StallionName`

Do not replace the existing `NamesSet` source. The town event layer should extend it.

## Design Target

Random town events should be initialized as unordered/random story threads.

Recommended structure:

```renpy
townThreadList = [
    RThreadData(0, "town", "StreetChronicles", None, [
        (
            "story_town_random_chronicle_0",
            None,
            None,
            None,
            1,
            None,
            [
                "#town_random_event_allowed(CurLoc)",
                "#not town_random_event_seen_this_slot(CurLoc)",
            ],
            None,
            "StreetTavern",
            "enter",
            50,
        ),
    ], highlight=False, threaded=False),
]
```

Implementation rule:

- Conditions belong in the event tuple and must be visible on the story board.
- The event label should display one selected text and return to the current room actions.
- No hidden middleware should decide story eligibility when tuple fields can express it.
- The random text function can choose the exact prose after the event is already selected.

## Time Mapping

Tractir uses slot time:

```text
0 morning
1 noon
2 day
3 evening
4 night
```

Town chronicle keys:

```text
morning  -> time == 0
noon     -> time == 1 or time == 2
weekends -> week in (6, 7), any open street slot
evening  -> time == 3
night    -> time == 4
```

If `week in (6, 7)` and a weekend event is available, use `weekends` first; otherwise fall back to the normal time key.

## Street Display Extension

Add a display map beside the existing street randomizer:

```renpy
RussianStreetNames = {
    "пекарей": "улице Пекарей",
    "кожевенников": "на Кожевенной",
    "мясников": "на Мясницкой",
    "шорников": "в переулке Шорников",
    "бочкарей": "во дворе Бочкарей",
    "шляпников": "на Проходе Шляпников",
    "портных": "на Портняжьей",
}

def GetRussianStreetDisplay():
    rus = RandomStreetNameCode()
    return RussianStreetNames.get(rus, "на Рыночной площади")
```

## Random Chronicle Function

The later Ren'Py function should follow this shape:

```renpy
def GetRandomRussianTownEvent(time_of_day="morning"):
    if time_of_day not in RussianTimeEvents:
        time_of_day = "morning"

    name = RandomNameCode(
        gender=renpy.random.choice(["male", "female"]),
        nationality=renpy.random.choice(["German", "French", "Italian"]),
    )
    occupation = RandomOccupCode()
    street = GetRussianStreetDisplay()
    stallion = RandomStallionNameCode()

    template = renpy.random.choice(RussianTimeEvents[time_of_day])

    if renpy.random.random() < 0.45:
        template += renpy.random.choice(RussianPassiveGuardAdditions)

    return template.format(
        улица=street,
        имя=name,
        занятие=occupation,
        stallion=stallion,
    )
```

Use `renpy.random`, not Python `random`, so save/reload behavior stays Ren'Py-consistent.

## Safety And Lore Rules

- Random named actors are ordinary adults.
- Do not generate underage street participants.
- Public sex/vice events are town-color rumors and social decay signals, not sex-engine entry points unless a later explicit story thread unlocks them.
- Guard appearances are passive background color about corruption and negligence.
- Violent events may open investigation hooks, boss-fight hooks, or notoriety changes later.
- Forest, witch, werewolf, horse, disease, and corruption motifs should be taggable so future threads can react.

## Passive Guard Additions

Guard add-ons should happen in roughly 45 percent of random chronicles:

```renpy
RussianPassiveGuardAdditions = [
    " Мимо лениво проходят двое стражников, посмеиваются, но даже пальцем не шевелят.",
    " Стражники стоят в стороне с фляжкой и только качают головами.",
    " Один стражник опирается на алебарду и ухмыляется: «Пусть сами разбираются».",
    " Городская стража слишком занята своей выпивкой, чтобы обращать внимание на крики.",
]
```

## Event Bank

The initial event bank is grouped by town time key. These entries are prose templates. They should not mutate story flags by themselves in the first implementation.

### Morning

- town_morning_werewolf_reward: herald announces reward for a forest werewolf; crowd sees a fresh corpse and talks about curses.
- town_morning_bloodless_body: a named citizen and occupation discover a drained body; people blame vampires, witches, or the forest.
- town_morning_pillory_morals: public punishment at the pillory for sexual/moral offense; crowd participates.
- town_morning_gallows_warning: dawn gallows scene; thief's body remains as a burgomaster warning; forest howl in the distance.
- town_morning_black_dog: young woman runs through the street claiming a black dog with burning eyes took her sister.
- town_morning_disease_potion: seller offers fake medicine against disease while people whisper about a witch ghost.

### Noon / Day

- town_noon_witch_decree: herald announces punishment for hiding witches or werewolves; public whipping for forest-smuggling aid.
- town_noon_ale_knife_fight: fight over the last ale barrel becomes bloody while the crowd makes bets.
- town_noon_cursed_stallion: stallion named by `RandomStallionNameCode()` shows signs of forest curse and throws its rider.
- town_noon_demon_contract: named citizen begs forgiveness for claiming he sold his soul to a forest demon.
- town_noon_smuggler_cart: overturned cart reveals a murdered smuggler among spilled apples; people blame forest bandits.
- town_noon_wall_vice: public vice scene near a wall; guards ignore it as post-plague moral decay.

### Weekend

- town_weekend_witch_bounty: market-day herald offers reward for proof that the forest witch is dead; charms against werewolves are sold.
- town_weekend_stallion_trampling: drunken citizen tries to ride a stallion and is thrown/trampled; crowd blames forest curse.
- town_weekend_false_witch_hunt: animal fight turns into a panic accusation against a beggar woman.
- town_weekend_sin_tax: dancer on a barrel and crowd harassment; herald mentions a tax on sin.
- town_weekend_balcony_mooning: drunken balcony mockery stops when a forest howl silences everyone.
- town_weekend_horse_fair: horse-fair fight over breeding payment; herald announces an absurd corrupt burgomaster privilege.

### Evening

- town_evening_curfew_and_wall_vice: wall vice scene during curfew notice about forest creatures after sunset.
- town_evening_severed_head: named citizen finds a severed head at the door and blames bandits or witchcraft.
- town_evening_ghost_music: street music and dancing stop when someone screams about a hanged witch ghost.
- town_evening_stabbing: drunken fight becomes stabbing while herald focuses on werewolf decree.
- town_evening_stallion_forest_shadow: stallion breaks loose toward the forest, followed by a dark shadow.
- town_evening_paid_servant: public corruption/vice exchange while plague rumors spread.

### Night

- town_night_stable_vice_and_howl: couple at stable, forest howl, and posted notice about black dog sightings.
- town_night_thief_humiliation: crowd punishes a caught thief at night and threatens witch-style burning.
- town_night_sailor_throat: sailor dies with torn throat during a vice dispute near the tavern; survivor screams about werewolf.
- town_night_canal_body: named citizen is found dead in a ditch with signs of a large animal nearby.
- town_night_cursed_client: sex worker bargains with a client and mentions forest curse; unseen woman laughs in the dark.
- town_night_demon_stallion: stallion breaks a fence while half-dressed townsfolk run with torches and blame a forest demon.

## Interactive City Event Layer

The prose chronicles are atmosphere. A smaller subset should become interactive city events where the player can be involved.

Important source rule:

- Patrol and bribe mechanics already exist in TXT-derived/ported content.
- Do not design the new patrol system from scratch.
- Use the existing Amanda/Legare guard scene as the first concrete model:
  - `game/NPC/Girls/Amanda/AfterDanceLegare.rpy`
  - fight draw brings guards
  - guard offers a `50` maravedy fight fine
  - refusal causes overnight jail/stock-style consequence and tavern reputation loss
  - police intervention branch allows another party to bribe guards
  - player can counter-bribe `200` maravedy to make guards side with him

The random patrol RThreads should extract this into a generic patrol/bribe result helper later, but the first implementation should preserve these amounts and consequences unless a specific event overrides them.

Hard cap:

- maximum `2` interactive street events per day
- patrol/curfew checks count against the same cap
- pure atmosphere chronicles can appear more often, but should not mutate major state

Suggested daily state:

```renpy
default TownStreetEventsToday = 0
default TownStreetPatrolsToday = 0
default TownStreetFightToday = 0
default TownCurfewCaughtToday = 0
```

Reset these in `NextDay_FinishDayEvents` or the same daily-reset area that resets talk/flirt/gift state.

### Event Families

```text
town_story       short atmosphere, no major state mutation
town_thugs       player is attacked or sees someone being attacked
town_help        player can help a victim, worker, sex worker, or hungry person
town_patrol      guard patrol/curfew check
town_favor       guard-captain related public order favor
```

### Player Choices

Typical street event choices:

```text
Watch
Intervene
Fight
Run
Talk/bribe
Give food
Ignore
Call guards
```

Fight choices should use the existing fight system where possible. If the event is not worth a full fight screen, use a small opposed check:

```text
player_score = FightLevel["you"] + exploration_bonus + weapon_bonus + luck
enemy_score = thug_level + group_bonus + luck
```

Escape choices should use exploration heavily:

```text
if exploration >= 150:
    escape is possible
else:
    escape is mostly luck and may fail badly
```

### Rewards

Winning or successfully helping can grant:

- exploration points
- tavern fame
- maravedy
- useful rumor/hint
- guard-captain goodwill
- future pass/permission flags
- tavern blackworker candidate

Important wording from the design:

- Helping and winning should add to notoriety and fame.
- Exploration helps with escape and pursuit events.
- Maravedy rewards should be small unless the event is tied to a named quest.

Suggested reward ranges:

```text
small help:       exploration +3..8, tavernfame +1, notoriety +1
won street fight: exploration +8..15, tavernfame +1..2, notoriety +2..4
saved victim:     exploration +5..12, tavernfame +1..3, optional money +3..15
guard favor:      exploration +4..10, guard goodwill +1, notoriety +1
```

### Penalties

Losing, being caught, or failing escape can cause:

- health damage
- torn clothing
- sick days
- fines
- stocks/jail overnight
- tavern reputation loss
- money loss
- shame text and town gossip

Suggested penalty ranges:

```text
minor beating:    health -10..25, energy -10, clothing condition -10..25
bad beating:      health -25..50, SickDays +1..2, clothing condition -25..60
fine:             money -10..60
stocks/jail:      NextDay, tavernfame * 0.4 or tavernfame -60 percent equivalent
curfew arrest:    money fine or stocks depending notoriety/luck
```

Use current project variables where possible:

- `health`
- `energy`
- `costumecondition`
- `SickDays`
- `money`
- `tavernfame`
- `notoriety`
- `exploration`

### Notoriety And Sleep

Street notoriety is short-lived heat.

Target rule:

- notoriety rises from public fights, scandal, patrol suspicion, successful intimidation, and public rescue
- notoriety increases patrol chance
- notoriety should go back to `0` when sleeping / next day begins

This means notoriety is not permanent reputation. Permanent reputation should use `tavernfame`, story flags, or achievements.

Suggested reset point:

```renpy
label NextDay_FinishDayEvents:
    ...
    $ notoriety = 0
```

If permanent scandal is needed, convert it before reset:

```renpy
if notoriety >= 50:
    $ tractir_activate_achievement("notoriety_50")
    $ tavernfame -= 1
```

### Patrols And Curfew

City has patrols and curfew, especially at night.

Patrol chance should depend on:

- time slot, highest at `time == 4`
- current location
- `notoriety`
- whether player has a pass
- guard-captain goodwill
- current day story state

Suggested chance:

```text
base day patrol:       2..5 percent
evening patrol:        8..12 percent
night/curfew patrol:   20..35 percent
notoriety modifier:    +notoriety / 3 percent, clamped
pass modifier:         strong reduction or safe passage
```

Patrol event outcomes:

```text
pass shown       -> no penalty, possible guard rumor
bribe/fine       -> money loss, default 50 for a public fight fine
counter-bribe    -> money loss, default 200 when trying to turn corrupt guards to your side
escape           -> exploration check, notoriety rises if seen
fight guards     -> dangerous, can lead to jail/stocks or fatal boss-style loss later
arrest/stocks    -> NextDay, fame/reputation penalty
```

Existing ported bribe model:

```text
fight/public trouble fine: 50 maravedy
counter-bribe corrupt patrol: 200 maravedy
refuse/unable to pay: overnight arrest, reputation penalty, return next day
third-party bribe: guards may side against player
```

Generic helper target:

```renpy
def town_guard_fine_amount(reason="fight"):
    if reason == "counter_bribe":
        return 200
    return 50
```

The helper should not hide story logic. Event tuple conditions still decide whether the patrol event is available; the helper only calculates the outcome amount once the event is already active.

### Guard-Captain Pass

Doing favors for the guard captain should matter.

Possible pass sources:

- solve Sherwood / Blackwoods guard quest
- solve Clarissa fiance murder case
- repeated city-public-order favors

Suggested flags:

```renpy
default GuardCaptainVar = {}

GuardCaptainVar["goodwill"] = 0
GuardCaptainVar["street_pass"] = 0
GuardCaptainVar["sherwood_solved"] = 0
GuardCaptainVar["murder_case_solved"] = 0
```

Pass unlock idea:

```text
if sherwood_solved and murder_case_solved:
    street_pass = 1
elif goodwill >= 5:
    temporary pass or warning immunity
```

Board-visible condition examples:

```renpy
"#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0"
"#int(notoriety or 0) >= 10"
"#int(time or 0) >= 3"
```

### Blackworker Recruitment

Some help events can create a low-status tavern helper.

Sources:

- save a sex worker from thugs
- give food to a hungry person
- intervene when someone is being abused by guards or criminals

Reward:

- candidate becomes a blackworker / dirty-work helper
- works for food and a place to sleep
- sleeps in shed, stray pile in stable, or backyard shade

Suggested flags:

```renpy
default TavernBlackworkers = []
default TavernBlackworkerCandidates = []
```

Candidate row:

```renpy
{
    "id": "bw_001",
    "name": RandomNameCode("male" or "female"),
    "origin": "saved_whore" / "fed_hungry" / "saved_worker",
    "day": dayspassed,
    "sleep_place": "Shed" / "TavernStable" / "Backyard",
    "trust": 0,
}
```

Effects:

```text
dirty-work helper can reduce cleaning burden
may create later theft/trust event
may become witness or rumor source
costs food, not wages
```

### Artisan Quarter Placement

`ArtisansQuarter` should receive its own short city stories.

Good event themes:

- apprentices fighting
- tool theft
- debt collector conflict
- late workshop lights during curfew
- injured worker asking for food or bandage
- corrupt inspection patrol
- runaway helper sleeping near workshops
- Draupnir/Irma related rumors as future named hooks

Artisan Quarter should not feel like a generic market clone. Its random events should reference:

- tools
- leather, cloth, barrels, forge smoke, sawdust
- debt, guilds, masters, apprentices
- night work and illegal orders

## Interactive Event Table Draft

```csv
npc,thread_constructor,thread_level,thread_subname,thread_condition,target_label,day,hour,delay,probability,requirements,conditions,item,location,action,priority
town,RThreadData,0,StreetThugs,None,story_town_thugs_0,None,(2,3,4),None,1,None,"town_interactive_event_allowed(CurLoc); TownStreetEventsToday < 2; TownStreetFightToday == 0",None,StreetTavern,enter,35
town,RThreadData,0,StreetHelp,None,story_town_help_0,None,(0,1,2,3),None,1,None,"town_interactive_event_allowed(CurLoc); TownStreetEventsToday < 2",None,MarketPlace,enter,40
town,RThreadData,0,StreetPatrol,None,story_town_patrol_0,None,(3,4),None,1,None,"town_patrol_event_allowed(CurLoc); TownStreetEventsToday < 2; int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",None,PortStreets,enter,25
town,RThreadData,0,ArtisanQuarterTrouble,None,story_town_artisan_quarter_trouble_0,None,(1,2,3),None,1,None,"CurLoc == 'ArtisansQuarter'; town_interactive_event_allowed(CurLoc); TownStreetEventsToday < 2",None,ArtisansQuarter,enter,35
```

Implementation note:

- Use one row per location if the board needs explicit location/debug clarity.
- Use helper conditions only for composite checks that would otherwise duplicate the same 5+ clauses in every row.
- Keep high-value conditions visible in the tuple: cap, pass, time, location, notoriety threshold.

## Thread/Event Table Draft

These are planning rows, not yet runtime rows.

```csv
npc,thread_constructor,thread_level,thread_subname,thread_condition,target_label,day,hour,delay,probability,requirements,conditions,item,location,action,priority
town,RThreadData,0,StreetChronicles,None,story_town_random_chronicle_morning,None,0,None,1,None,"town_random_event_allowed(CurLoc); not town_random_event_seen_this_slot(CurLoc)",None,StreetTavern,enter,50
town,RThreadData,0,StreetChronicles,None,story_town_random_chronicle_noon,None,(1,2),None,1,None,"town_random_event_allowed(CurLoc); not town_random_event_seen_this_slot(CurLoc)",None,StreetTavern,enter,50
town,RThreadData,0,StreetChronicles,None,story_town_random_chronicle_weekend,(6,7),None,None,1,None,"town_random_event_allowed(CurLoc); not town_random_event_seen_this_slot(CurLoc)",None,StreetTavern,enter,45
town,RThreadData,0,StreetChronicles,None,story_town_random_chronicle_evening,None,3,None,1,None,"town_random_event_allowed(CurLoc); not town_random_event_seen_this_slot(CurLoc)",None,StreetTavern,enter,50
town,RThreadData,0,StreetChronicles,None,story_town_random_chronicle_night,None,4,None,1,None,"town_random_event_allowed(CurLoc); not town_random_event_seen_this_slot(CurLoc)",None,StreetTavern,enter,50
```

When implemented, duplicate the same thread/event rows or use location-aware tuple conditions for:

- `StreetTavern`
- `MarketPlace`
- `PortStreets`
- `ArtisansQuarter`

The cleaner option is to let the tuple location be a generic street event location if the runtime supports it. If not, use one row per town street location so board/debug remains explicit.

## Later Hooks

Potential follow-up RThreads:

- werewolf bounty investigation
- witch/ghost rumor chain
- disease/fake potion chain
- corrupt guard/burgomaster chain
- horse curse and Mongol horse-theft cross-link
- black dog/forest creature chain
- public violence leading to guard captain investigation
- notoriety achievement changes when the player intervenes or exploits events
