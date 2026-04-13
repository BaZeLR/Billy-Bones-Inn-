# Tavern Economy

Source of truth:
- `game/Inn/NextDay_TavernDaily.txt`
- `game/Inn/NextDay.txt`
- `game/Inn/WineStore.txt`
- `game/Inn/GroceryStore.txt`

## Core Daily Tavern Loop

Each processed day:
- `CurDay['visitors'] = tavernvisitors + Rand(-4, 4)`
- special week penalties:
  - week 5: visitors halved
  - week 7: visitors reduced to `3/4`
- rare harbor spike:
  - `1/15` chance to double visitors

Each visitor consumes:
- `1` wine unit
- `1` product unit

Daily sales values:
- `CurDay['revenue'] = 1 * products + 2 * wine`

So per visitor:
- food sale = `1`
- wine sale = `2`
- total tavern sale = `3`

## Supply Costs

Original shop prices:

Products:
- `1` sack costs `6`
- `1` sack adds `10` product units
- cost per product unit = `0.6`

Wine:
- `1` barrel costs `14`
- `1` barrel adds `10` wine units
- cost per wine unit = `1.4`

So one fully served visitor costs:
- products: `0.6`
- wine: `1.4`
- total supply cost: `2.0`

Gross margin per served visitor:
- revenue `3.0`
- supply cost `2.0`
- margin `1.0`

## Fixed Costs and Household Drain

Daily fixed cost:
- `householdmembers * 1 + 10`

With original start:
- `householdmembers = 4`
- fixed cost = `14`

Household also consumes product stock:
- `CurDay['fameaten'] = householdmembers`
- if products are short:
  - player pays `dineout = missing * 3`
  - tavern happiness drops by `1`

## Street Worker / Side Revenue Shares

These are **not** tavern sale revenue. They are extra direct income added at day end.

### Client Volume Parameters

Original generation comes from:
- `game/Inn/NextDay_NewDayEvents.txt`
- `game/Inn/WhoreNextDayClients.txt`

Normal prostitution:
- `georgett`
  - `MaxClients = 5`
  - actual daily clients: `Rand(1, 5)`
- `liza`
  - `MaxClients = 3`
  - if she has no panties:
    - `MaxClients = 4`
  - actual daily clients: `Rand(1, MaxClients)`

Week modifiers:
- week `5`
  - normal prostitution is forced to `0` clients
- week `7`
  - prostitution client count is not directly zeroed, but other event timing shifts still apply elsewhere

Gloryhole:
- upper bound argument is:
  - `tavernvisitors / 6`
- then original logic clamps it:
  - `GloryHoleMax = Min(10, tavernvisitors / 6)`
- week modifiers then reduce that cap:
  - week `5`: `GloryHoleMax = GloryHoleMax / 2`
  - week `7`: `GloryHoleMax = (GloryHoleMax * 3) / 4`

If the girl is assigned to gloryhole tomorrow:
- actual total gloryhole clients:
  - `ClientsDayTotal[girl] = (GloryHoleMax * (75 + 5 * Rand(1,10))) / 100`
- so actual realized total is roughly:
  - `80% .. 125%` of the adjusted `GloryHoleMax`

Whore revenue:
- `TotalDay['whorerevenue'] = TotalWhoreClients['georgett'] * 3 + TotalWhoreClients['liza'] * 3`
- player share per street-worker client = `3`

Gloryhole revenue:
- `TotalDay['gloryholerevenue'] = TotalGloryHoleClients['georgett'] * 2 + TotalGloryHoleClients['liza'] * 2`
- player share per gloryhole client = `2`

These are added directly to money in `NextDay`:
- tavern sales revenue
- minus dine-out
- minus fixed cost
- plus whore revenue
- plus gloryhole revenue
- plus kids money
- plus birth stipend if present

## Free / External Income

Free or external income sources currently visible in the original economy:

Kids stipend:
- week 7:
  - `TotalDay['KidsMoney'] += 15 * KidsPosobie`

Birth stipend:
- one-time:
  - `+600` if `KidBirthPosobie` text exists

These can outscale tavern baseline surplus if the player reaches the required relationship/sex/fertility progression.

## Happiness, Loyalty, Fame, Visitor Growth

Happiness:
- starts at `0`
- drops if stock is insufficient
- drops if service levels are too low
- may drop from broken sign
- may rise from whore/gloryhole presence

Service gate:
- if any of:
  - `tavernwaitress < 10`
  - `tavernclean < 10`
  - `tavernkitchen < 10`
  then happiness decreases
- otherwise, if total service exceeds:
  - `visitors * 4`
  then happiness increases

Loyalty:
- may increase from positive happiness
- decreases directly from negative happiness
- dance sponsorship after week 5 adds `3..5`

Fame:
- `tavernfame += TotalDay['loyalty']`

Visitor growth trigger:
- if `tavernfame >= 10`
  - `tavernvisitors += tavernfame`
  - fame resets to `0`

Visitor collapse trigger:
- if `tavernfame <= -10`
  - `tavernvisitors += tavernfame`
  - fame resets to `0`

Failure state:
- if `money == 0`
  or
- if `tavernvisitors == 0`

## Starting Baseline Assessment

Original baseline values:
- starting money in `Intro.txt`: `100`
- `tavernvisitors = 40`
- `householdmembers = 4`

Approximate starting daily tavern trade:
- visitors: around `40`
- revenue: around `120`
- replacement supply cost: around `80`
- gross trade surplus: around `40`
- fixed cost: `14`
- household food drain replacement value: around `2.4`

So rough starting daily net is around:
- `23.6`

This means:
- the tavern is usually survivable
- but growth is slow
- and expensive upgrades/costumes can easily outpace tavern surplus

## Design Implication

The tavern business alone is mildly profitable, but not strongly expansive.

Meaningful scaling money can come more from:
- street-worker revenue shares
- gloryhole revenue shares
- stipends / family-support systems

So if the design goal is smoother non-grindy progression, the most powerful levers are:
- stronger visitor/fame response to good tavern operation
- more visible cost-saving through chores
- more mid-tier income between tavern baseline and late stipend systems
