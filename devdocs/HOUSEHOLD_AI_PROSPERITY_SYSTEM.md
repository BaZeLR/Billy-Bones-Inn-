# Household AI And Tavern Prosperity System

This document is the implementation contract for the next household/tavern logic layer.
It does not replace existing Amanda, Melissa, Sandra, tavern, thread, room, or UI logic.
It defines how to connect them with a clean Python/Ren'Py runtime layer while keeping labels readable.

## Goal

The game should feel like a living tavern household:

- Sandra, Amanda, and Melissa have their own needs, moods, motives, jealousy, and route pressure.
- The tavern can move from poor inherited business to stable household, then to better clients and noble service.
- Household cooperation makes the tavern survive and grow.
- Household jealousy, competition, bad discipline, bad work assignment, or neglected needs make the game harder.
- The player should manage policy, attention, money, rewards, rules, and opportunities.
- Story labels should stay human-readable: text, images/vsscenes, choices, and direct consequences.
- Python/Ren'Py utility files should manage state, schedules, event readiness, AI intent, economy, items, fights, time, and endings.

Core loop:

```text
location enter
-> current time and current location
-> present NPCs
-> eligible events for present NPCs
-> event UI/label if ready
-> otherwise normal room UI/actions
```

## File Naming Rule For Pure Python Logic

Use pure Python `.py` files for heavy runtime/system logic and mark them with a `_re.py` suffix.
This keeps mechanical code easy to identify, keeps story labels clean, and makes pure Python tests possible outside the game project.

Recommended new files:

```text
game/Utilities/General/NPC/HouseholdAI_re.py
game/Utilities/General/NPC/HouseholdJealousy_re.py
game/Utilities/General/NPC/GirlIntentProfiles_re.py
game/Utilities/General/NPC/GirlIntentResolver_re.py
game/Utilities/General/NPC/GirlIntentFeedback_re.py
game/Utilities/General/NPC/NPCScheduleResolver_re.py
game/Utilities/General/Common/TavernProsperity_re.py
game/Utilities/General/Common/GameLoopConditions_re.py
game/Utilities/General/Common/RoomEnterResolver_re.py
game/Utilities/Time/DailyHouseholdReset_re.py
```

Existing `.rpy` files can stay with their current names. Do not rename working files only for style.

Ren'Py bridge files should stay small and explicit. Their job is only to import or call pure Python logic, define Ren'Py `default` save-state variables, and expose the result to labels/screens.

Example split:

```text
HouseholdAI_ren.py
    pure Python: score intents, resolve jealousy, calculate candidate weights

HouseholdAIBridge.rpy
    Ren'Py defaults, imports/calls, save-state handoff, label/screen-facing helpers
```

Pure Python files must not depend on `renpy.store` unless there is no practical alternative.
Prefer passing a context dictionary into `_re.py` functions and returning a result dictionary.

## Clean Ownership

Pure Python `_re.py` files own:

- scoring
- deterministic calculations
- model tables
- condition evaluation that can be tested outside Ren'Py
- schedule candidate selection
- AI intent selection
- economy/prosperity calculations
- feedback math
- fight odds and damage math

Ren'Py utility/bridge files own:

- items and inventory accounting
- action availability and action results
- time, daily reset, weekly/monthly checks
- NPC schedules and present-NPC calculation
- story thread/event readiness
- random events
- fight logic
- tavern economy
- girl AI intent selection
- jealousy/teamwork state
- achievement, ending, game over, and prosperity checks

The practical division is:

```text
_re.py: receives plain data, returns plain data
.rpy: reads/writes Ren'Py save variables and calls labels/screens
```

Labels own:

- text
- vsscene/picture/video choice
- menus
- direct player choices
- direct route jumps/calls to real locations
- applying a named consequence through a system function

Good label shape:

```renpy
label story_amanda_private_tease_0:
    vscene "images/amanda/private/tease_0.jpg"
    "Amanda tries to get your attention."

    menu:
        "Reward her":
            $ household_apply_player_response("amanda", "reward_attention")
            jump TavernMyRoom

        "Tell her to help Sandra first":
            $ household_apply_player_response("amanda", "discipline_work_first")
            jump TavernMyRoom
```

Avoid hiding story conditions inside the label. The resolver should decide when this label is available.

## Models Considered

### Model 1: Pure Hard Rules

Shape:

```text
if corruption > 50 and money_need > 40 and player_private:
    choose favor_scene
```

Strengths:

- very readable
- easy to debug on the story board
- reliable for important route gates

Weaknesses:

- predictable
- creates many scattered `if` blocks
- hard to make Amanda/Melissa/Sandra feel alive

Use for:

- story route locks
- pregnancy/kid safety gates
- fight/game-over checks
- one-time important scenes
- Sunday church and scheduled events

### Model 2: Weighted Score / Primitive Perceptron

Shape:

```text
intent_score = base
intent_score += need_weight * need_value
intent_score += jealousy_weight * jealousy_value
intent_score += memory_weight * memory_value
intent_score += room_weight if private room
```

Strengths:

- allows personal character tendencies
- supports learning from success/failure
- good for semi-random repeated behavior

Weaknesses:

- can become unreadable if every value is hidden
- needs debug board output
- should not replace clear story conditions

Use for:

- Amanda autonomous behavior
- Melissa curiosity/avoidance
- Sandra discipline/control
- client interaction outcomes
- repeated minor scenes

### Model 3: Utility AI

Shape:

```text
for each possible intent:
    score = urgency * suitability * chance
choose highest score over threshold
```

Strengths:

- best for daily life simulation
- good for schedules, private-room actions, jealousy, and needs
- easy to add new actions without rewriting all branches

Weaknesses:

- more abstract
- needs strict limits so it does not fire too many scenes

Use for:

- daily autonomous choices
- household work conflicts
- who approaches player
- whether a girl asks, teases, avoids, works, shares, competes, or interferes

### Recommended Model: Hybrid

Use all three in clear layers:

```text
hard rule gate
-> utility score for possible intents
-> weighted personality/memory adjustment
-> one chosen visible intent, or no visible intent
```

This keeps route logic readable while still giving girls a natural behavior layer.

## Household State

Recommended defaults:

```renpy
default TavernProsperityTier = 0
default TavernClientClass = "common"
default SandraAuthority = 50
default SandraSecuredFuture = False
default HouseholdTeamwork = 50

default HouseholdJealousy = {
    "amanda": 0,
    "melissa": 0,
    "sandra": 0,
}

default HouseholdAttention = {
    "amanda": 0,
    "melissa": 0,
    "sandra": 0,
}

default HouseholdConflictFlags = {
    "breakfast_argument_today": 0,
    "work_refusal_today": 0,
    "sandra_discipline_today": 0,
}
```

Meaning:

- `TavernProsperityTier`: long-term quality of the tavern.
- `TavernClientClass`: current active customer tier.
- `SandraAuthority`: how much the household accepts Sandra's discipline and command.
- `SandraSecuredFuture`: Sandra has a stable place in the tavern future.
- `HouseholdTeamwork`: cooperation across Sandra/Amanda/Melissa and later Liza/Georgette.
- `HouseholdJealousy`: pressure to interfere, compete, withdraw, or demand attention.
- `HouseholdAttention`: recent player attention/rewards.
- `HouseholdConflictFlags`: daily blockers to prevent repeated conflict spam.

## Tavern Prosperity Route

Tiers:

```text
0 survival / poor inherited tavern
1 stable common tavern
2 busy local tavern
3 respectable tavern with merchants, guards, and artisans
4 noble/private-client tavern
```

Inputs:

- fame
- cleanliness
- food and drink supply
- number and quality of workers
- Sandra authority
- household teamwork
- dog/werecat/rat/bat state
- fights, lewd scandals, notoriety
- city guard relationship
- Sheriff/guard captain Zimmer favors
- Sherwood/Blackwoods progress
- noble-client story hooks
- rooms/stables/shop upgrades

Outputs:

- visitor count
- client class
- revenue
- harassment risk
- client demands
- girl work pressure
- fame/reputation changes
- special event availability
- endings/achievements

Prosperity should not be free. Better clients bring:

- more money
- stricter service expectations
- higher jealousy and competition
- more chance of dangerous offers
- more reason for Sandra to control the house
- more reason for Amanda/Melissa to seek rewards, favors, or private attention

## Sandra Route

Sandra is tavern keeper and household authority.
She is auntie to Amanda and Melissa, not the player's mother.

Sandra's strong route:

```text
survival fear
-> player proves tavern can survive
-> Sandra adapts
-> Sandra remembers youth / openness route
-> Sandra becomes pragmatic/corrupted in a controlled way
-> Sandra secures her future
-> Sandra remains authority while tavern prospers
```

If Sandra does not adapt:

- younger girls can become the visible value of the tavern
- Liza and Georgette can pull income and attention away from Sandra
- Sandra may feel displaced
- authority drops
- household teamwork drops
- breakfast and work scenes become tenser

If Sandra adapts:

- she organizes work
- she can discipline
- she can reduce chaos
- she can make the tavern more profitable
- she can compete for the player's attention in a mature/control-oriented way
- she can keep Amanda and Melissa from ruining the house through uncontrolled choices

Sandra authority actions:

- assign kitchen/cleaning/waitressing duties
- block or allow certain risky tavern work
- confront Amanda/Melissa at breakfast
- punish repeated refusal or disobedience
- use stern discipline when the household accepts her authority
- protect girls from bad clients when authority/teamwork is high

## Amanda Profile

Existing Amanda logic should not be replaced.
The AI layer should feed additional natural opportunities into existing Amanda scenes and flags.

Core pressures:

- money
- beauty
- attention
- teasing
- rebellion
- desire
- work avoidance
- player approval
- competition with Melissa/Sandra
- curiosity around Liza/Georgette
- security if pregnant or worried about future

Amanda likely responses:

- ask for money, dress, soap, barber, treatment, or reward
- tease if private or semi-private
- offer favor if it matches current need and corruption/openness is high enough
- resist if player blocks her goal without reward
- become angry if disciplined unfairly
- become more obedient if rewarded for useful work
- compete if Melissa/Sandra gets attention
- exploit better clients if tavern class rises

Private-space AI examples:

```text
room: Amanda room, MC room, storage, shed, quiet backyard
if Amanda present and player present:
    check needs
    check cycle/desire pressure
    check jealousy
    check anger
    check player recent behavior
    choose one visible intent or none
```

Possible intents:

- ask_money
- ask_beauty_help
- ask_less_work
- ask_more_tips
- tease_player
- test_boundary
- private_talk
- seek_comfort
- seek_satisfaction
- interfere_with_other_girl
- obey_and_work
- avoid_player

## Melissa Profile

Melissa prefers girls but can be curious.
She should not behave like Amanda with a different name.

Core pressures:

- shyness
- curiosity
- affection/trust
- watching/being watched
- preference for girls
- need for comfort
- jealousy if Amanda or Sandra receives too much attention
- fear of exposure
- reaction to rat/werecat/bat room arcs
- connection with Clara paintings path

Melissa likely responses:

- withdraw if pressure is too direct
- become curious if trust/openness rises
- share secrets in private
- ask for comfort after frightening or humiliating events
- watch others instead of acting directly
- interfere softly through mood, avoidance, or quiet confession
- become more cooperative when she feels protected
- become more provocative when trust and openness are high

Possible intents:

- private_question
- ask_comfort
- avoid_attention
- seek_girl_company
- watch_or_peek
- confess_secret
- ask_help_room_problem
- jealousy_withdraw
- jealousy_interfere_soft

## Jealousy And Share Dilemma

Jealousy mode should create decisions, not only punishment.

Main patterns:

```text
interfere
share
withdraw
compete
complain_to_sandra
ask_player_directly
```

Amanda jealousy:

- visible, competitive, teasing, rebellious
- may interrupt
- may make a favor or demand a favor
- may work harder for reward or refuse if neglected

Melissa jealousy:

- quieter, emotional, secretive
- may avoid breakfast or private talk
- may seek girl comfort
- may reveal information if trust is high

Sandra jealousy/control:

- authority-based
- household order and future security
- may redirect girls to work
- may discipline
- may claim player attention as practical household control

Share dilemma:

- if teamwork is high, sharing can reduce jealousy and increase prosperity
- if teamwork is low, sharing can trigger conflict or humiliation
- if Sandra authority is high, she can impose order
- if Amanda rebellion is high, imposed order may backfire
- if Melissa trust is low, she withdraws

## Work Assignments

Jobs should be generic templates with character modifiers.

Jobs:

```text
cleaning
waitressing
kitchen
mixed cleaning + waitressing
mixed kitchen + cleaning
private service / risky service
gloryhole or client route, where existing story permits it
```

Job effects:

Cleaning:

- low money
- obedience/discipline pressure
- low client contact
- low harassment
- useful for Sandra approval

Waitressing:

- tips and attention
- client harassment risk
- good for tavern income
- stronger jealousy and beauty pressure

Kitchen:

- safer
- lower money
- Sandra supervision
- good for pregnancy/security route
- can reduce rebellion if rewards are fair

Risky/private service:

- high money
- high corruption/openness pressure
- high scandal/notoriety risk
- can create jealousy and Sandra intervention
- should require explicit story and relationship gates

## Reproductive Cycle And Mood

The cycle should be a pressure source, not a scene script by itself.

It can modify:

- desire pressure
- mood
- need for comfort
- risk-taking
- jealousy sensitivity
- pregnancy chance
- desire to avoid work or seek safety

Do not make the cycle override story locks.
It should influence the AI resolver:

```text
cycle_desire_bonus
cycle_mood_modifier
cycle_security_need
cycle_sickness_or_discomfort
```

Pregnancy/kids route pressure:

- security need rises
- risky client behavior should usually fall unless corruption/desperation is very high
- kitchen/safe work becomes more attractive
- Sandra authority becomes more important
- tavern prosperity and stipends/family support become survival-critical

## Memory And Feedback

The AI should learn from repeated outcomes without rewriting core character variables.

Recommended memory:

```renpy
default GirlIntentMemory = {
    "amanda": {},
    "melissa": {},
    "sandra": {},
}

default GirlIntentBias = {
    "amanda": {},
    "melissa": {},
    "sandra": {},
}
```

Example event result:

```text
Amanda asks for barber treatment.
Player refuses because cleaning progress is bad.
Result:
    Amanda beauty_need remains high
    Amanda obedience may rise if refusal is fair and explained
    Amanda rebellion rises if refusal is harsh
    Amanda may seek alternate route if corruption/money pressure is high
```

Feedback categories:

```text
success
failure
neutral
humiliated
rewarded
disciplined_fair
disciplined_unfair
ignored
protected
```

Feedback should adjust local intent bias:

```text
success -> slightly increase same intent
failure -> slightly decrease or seek alternative
ignored -> increase jealousy/attention need
protected -> increase trust/teamwork
disciplined_fair -> lower rebellion if authority accepted
disciplined_unfair -> anger/rebellion/jealousy up
```

## AI Intent Resolver

Recommended function flow:

```python
def household_resolve_visible_intent(girl_key, location_key, action_key):
    if not household_ai_enabled(girl_key):
        return None

    if not npc_is_present(girl_key, location_key):
        return None

    if household_daily_intent_already_seen(girl_key):
        return None

    candidates = household_build_intent_candidates(girl_key, location_key, action_key)
    candidates = household_apply_hard_gates(girl_key, candidates)
    candidates = household_score_intents(girl_key, candidates)
    candidates = household_apply_memory_bias(girl_key, candidates)
    candidates = household_apply_random_tolerance(girl_key, candidates)

    return household_pick_best_visible_intent(candidates)
```

Candidate fields:

```text
intent_id
label
owner
location
time_slots
required_privacy
required_presence
blocked_flags
required_flags
min_relationship
min_openness
min_corruption
min_authority
need_weights
jealousy_weight
teamwork_weight
prosperity_weight
priority
repeat_cooldown
```

Important: the resolver chooses a label; the label owns text and images.

## Room Enter Resolver

Every room should follow the same order:

```text
1. Set CurrentRoom and current location.
2. Sync schedule/presence.
3. Build visible NPC list.
4. Check eligible story events for present NPCs.
5. Check room/object events.
6. Check random events if allowed.
7. If event selected, call/jump its real label.
8. If no event, render normal room UI/actions.
```

This should be one explicit system, not room-specific hidden logic.

Recommended function names:

```text
room_enter_context(location_key)
room_present_npcs(location_key)
room_eligible_events(location_key, action_key)
room_pick_event(location_key, action_key)
room_render_normal_ui(location_key)
```

Use existing story thread/event classes and direct event tuples.
Do not add wrapper thread classes.

## Event Board Debug Needs

The board must make hidden logic visible.

For each NPC:

- thread name
- current event/episode
- location
- action
- day/week/time condition
- required item
- required flags
- required relationship/openness/corruption
- whether each condition is currently true
- current status: locked, ready, done, aborted, cooldown

Color rule:

- green: condition currently true in this save/session
- red: condition currently false
- neutral/gray: not applicable
- highlighted row: event is currently eligible in this location/action

This is for debugging and human editing.
Do not hide all conditions inside one helper if the tuple can carry them clearly.

## Labels Stay Clean

Story labels should be easy to edit:

```text
picture/vsscene
text
menu choices
small direct mutations
jump actual room
```

They should not own:

- full schedule logic
- full AI scoring
- broad tavern economy
- daily reset
- event discovery
- large hidden branch selection

## Happiness, Mana, And Reaction Dependencies

This model connects tavern happiness, NPC daily state, and reaction decisions.
It is a design contract first. Do not implement it by adding another parallel
global dict. Runtime values belong on the relevant `GirlInfo`/NPC info object,
while tavern-wide values stay in the tavern daily/prosperity system.

### Separate Values

Keep these values separate:

- `happy`: tavern/day customer and household satisfaction pressure.
- `mana`: hidden personal reaction field on an NPC info object.
- `energy`: physical capacity to work, talk, flirt, fight, or recover.
- `beauty`: appearance/self-image value; it can influence mood but is not mana.
- `sick`: temporary condition that lowers energy and soft-blocks good reactions.
- `food_quality`: quality of food/drink/restoration offered that day.
- `anger_with_player`: active resentment toward the player.
- `rebellion`: resistance to player authority or household discipline.

The important rule:

```text
happy measures tavern/household pressure.
mana modifies how an NPC reacts.
energy and sick state gate whether the NPC can react well.
beauty can support confidence, but it does not replace mana.
anger and rebellion can override otherwise positive reactions.
```

### Positive Mana Inputs

General positive inputs:

- comfortable sleep and good rest
- clean tavern
- enough wood
- enough food stock
- good food and drink quality
- boar meat, honey, berries, good beverages, tea
- soap, washing, barber care, dress shop care
- suitable gifts
- successful tavern day
- tavern fame/profit going up
- girls are not sick, exhausted, or neglected

Sandra-specific positive inputs:

- tavern profit is stable or rising
- tavern fame is rising
- household chores are handled
- girls are working and not miserable
- weekly Sandra check succeeds
- player respects her authority without humiliating her

### Negative Mana Inputs

General negative inputs:

- dirt and bad smell
- no wood
- food stock low
- bad or poor food quality
- fame/profit falling
- repeated failed chores
- no rest, tiredness, or sickness
- ignored gifts/needs
- no intimacy or no social progress where the route expects it
- low beauty/self-image for NPCs who care strongly about appearance
- household conflict, jealousy, fear, anger, or humiliation

Sandra-specific negative inputs:

- tavern feels uncontrolled
- girls are unhappy
- player ignores household discipline
- weekly Sandra check fails
- player undermines her role

### Mana Growth And Fade Rules

Mana is a slow hidden runtime value on the NPC info object.
It should not jump wildly from ordinary daily conditions.

Daily growth:

```text
comfortable sleep        +2
good food quality        +2
clean tavern             +1
wood stock OK            +1
food stock OK            +1
soap/barber/dress care   +1 to +3 when used
useful preferred gift    +2 to +5 when given
successful tavern day    +1 to +3
```

Daily loss:

```text
sick                     -3
very low energy          -2
bad food quality         -2
dirty tavern             -2
wood stock low           -2
food stock low           -2
failed chores            -1 to -3
unfair discipline        -2 to -5
ignored important need   -2 to -5
```

Fade when no meaningful input happened:

```text
mana above 30 -> -1 per day
mana below 30 -> +1 per day
mana at 30    -> no change
```

This makes `30` the neutral resting point.
Important authored events may apply stronger changes directly, but ordinary
household conditions should use small daily deltas.

### Fear Mechanics

Fear is hidden risk pressure, `0..100`.
It is not a visible mood by itself.

Fear rises when the player creates risk:

```text
weekly check failed
tavern profit/fame drops
food or wood stock low
girls sick, exhausted, unsafe, or unhappy
unfair discipline
irresponsible spending
lost fights / town danger / bad reputation
ignored warnings
pushed intimacy too early
```

Fear falls when the player proves reliability:

```text
weekly check succeeds
tavern profit/fame rises
food and wood stable
girls healthy and working
useful resources or gifts provided
danger handled successfully
boundaries respected
promises kept
```

Mechanical effect:

```text
reaction_score -= fear // 20
weekly_check_threshold += fear // 10
trust_gain -= fear // 25
if anger is also high: rebellion rises faster
```

Clamp after every change:

```text
fear = clamp(fear, 0, 100)
```

### Reaction Formula Shape

Keep the first implementation simple and readable:

```text
reaction_score =
    base_topic_or_action_score
    + mana_bonus
    + relationship_bonus
    + trust_bonus
    - anger_penalty
    - rebellion_penalty
    - fear_penalty
    - tired_penalty
    - sick_penalty
```

Then choose the visible result:

```text
score very low -> dismissive / mocking / refuses
score low      -> cautious / neutral
score medium   -> interested / cooperative
score high     -> warm / admiring / more options
score extreme  -> obsession, fear, worship, or corrupted response
```

Do not hide this behind many wrappers. A direct method on the NPC info object is
enough, for example:

```text
Sandra.resolve_reaction(context)
Amanda.resolve_reaction(context)
```

The method changes only NPC/runtime state and returns a result. The label prints
the text and shows the menu.

### Unclear Dependencies To Resolve Before Coding

These dependencies are intentionally marked unresolved until exact variables are
chosen from the live runtime:

- exact source of food quality
- exact source of clean/dirty tavern state
- exact source of wood shortage
- exact source of tavern profit/fame trend
- exact mapping from sickness to energy loss
- exact mapping from beauty/self-image to mana
- exact mapping from low energy to reduced reaction score
- exact daily reset point for `mana_delta` logs
- exact weekly Sandra check effect on `mana`, `anger_with_player`, and `rebellion`

Until those sources are selected, do not invent duplicate globals.

## Integration Order

Implement in this order:

1. Add runtime state defaults and helper functions only.
2. Add debug board output for household AI/prosperity values.
3. Add room-enter resolver for one controlled room.
4. Plug Amanda visible intents into private/secluded rooms.
5. Plug Melissa visible intents into breakfast/private/room-problem scenes.
6. Plug Sandra authority/prosperity route into breakfast and daily tavern reports.
7. Add tavern prosperity tier calculation.
8. Add noble/private client tier gates.
9. Add feedback learning from player responses.
10. Expand to Liza, Georgette, Clara, Becky, Irma only after Sandra/Amanda/Melissa are stable.

## First Minimal Runtime Target

The first code patch should be small:

```text
HouseholdAI_re.py
TavernProsperity_re.py
RoomEnterResolver_re.py
small .rpy bridge files only where Ren'Py state/labels need them
```

It should provide:

- default state
- no new story rewrite
- no renamed working files
- no changed room UI layout
- no replacement of existing thread classes
- one debug summary function
- one or two safe intent candidates for Amanda/Melissa/Sandra

Then one room can call the resolver and prove the loop:

```text
location -> present NPCs -> eligible event -> event label or normal UI
```

## Non-Goals

Do not:

- rewrite Amanda's existing story
- replace existing `LThreadData`, `RThreadData`, `UThreadData`, or `Event`
- add middleware labels for navigation
- add hidden wrappers for simple booleans
- put test labels into the game
- break the one persistent main UI
- make every room special by hand
- randomize important route locks
- make AI fire more than one major visible intent per girl per day unless a specific event says so

## Practical Design Principle

Hard story conditions decide what is allowed.
Utility scoring decides what feels natural today.
Labels show the content.
Feedback changes future pressure.

That gives the game the intended shape:

```text
household survival
-> discipline and jealousy
-> cooperation or conflict
-> better tavern
-> better clients
-> noble/prosperity route
-> family/security/kids/long-term endings
```
