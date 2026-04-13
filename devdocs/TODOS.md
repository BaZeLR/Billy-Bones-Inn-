# TODOs

This file now tracks three separate things:

1. new gameplay/runtime features added on the Ren'Py side and the exact conditions that drive them;
2. TXT implementation status, with the condition under which a location/system should still be treated as TXT-authoritative;
3. the overlap between those two layers, which is the real priority zone for stabilization work.

Core rule, from [agent.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/devdocs/agent.txt):
- `.txt` files remain the source of truth for original gameplay logic.
- new Ren'Py-side features are acceptable only when they do not silently replace canonical TXT behavior.
- where a feature touches an old TXT-backed system, that area becomes a parity hotspot and must be reviewed before more feature expansion.

## Daily Update: 2026-04-09

This section records what was implemented in today's chat, what was intentionally changed in live code, and what remains open as the next step.

### Implemented Today

#### 1. Crafted Items Now Behave Like Real Inventory Goods

Files:
- [Actions.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Actions.rpy)
- [PlayerCard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PlayerCard.rpy)
- [SoapCraftAndAtticItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/SoapCraftAndAtticItems.rpy)
- [GameItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/GameItems.rpy)
- [HunterClub.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/HunterClub.rpy)

Implemented:
- crafted items can now be:
  - used;
  - gifted from the player inventory;
  - sold through the hunter club if they are marked as tradable goods.
- player-card item menu now supports `Подарить` for items with `gift_value`.
- gifting now uses the existing relationship flow and then applies item-specific social bonuses.

Current live examples:
- `energy_tea_001`:
  - usable;
  - giftable;
  - sellable.
- `ethanol_001`:
  - ingredient;
  - giftable;
  - sellable.
- `soap_001`:
  - usable;
  - giftable;
  - sellable.
- `torch_001`:
  - sellable.

Condition:
- item must be a real `GameItem`;
- if it should be giftable, it must expose `gift_value` in `custom_properties`;
- if it should be sellable, it must be listed in `HUNTER_CLUB_SELL_ITEM_IDS`.

Status:
- implemented and tested.

#### 2. Chained Recipe Progression Added On Top Of Ethanol

Files:
- [SoapCraftAndAtticItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/SoapCraftAndAtticItems.rpy)
- [GameItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/GameItems.rpy)

Implemented:
- new chained recipe:
  - `libido_recipe`
  - result item: `libido_tincture_001`
- recipe uses:
  - `ethanol_001`
  - `honey_comb_001`
  - either `special_herbs_001` or `berries_001`
- recipe uses the already existing image:
  - `images/recipe_book/libido_recipe.png`

Result item behavior:
- `libido_tincture_001` can be:
  - drunk;
  - gifted;
  - sold.
- drinking it returns:
  - empty bottle;
  - cork.

Condition:
- ethanol must already exist in inventory;
- recipe book chain must be discovered;
- at least one valid flavor ingredient must be present.

Status:
- implemented and tested.

#### 3. Social Gift Effects Now Depend On The Item, Not Only The Recipient

Files:
- [Actions.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Actions.rpy)
- [InitBecky.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/InitBecky.rpy)
- [InitGeorgett.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/InitGeorgett.rpy)
- [InitClara.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/InitClara.rpy)

Implemented:
- gifted drink items can now apply item-level social effects after the normal gift reaction:
  - extra fun;
  - extra openness;
  - Clara-specific trust;
  - horny/sluttiness bump where intended;
  - extra friendship if defined by the item.
- preference lists were extended so some characters now explicitly like the new drink chain.

Current live relationship examples:
- Clara:
  - can gain trust from `libido_tincture_001`.
- Becky:
  - now treats `libido_tincture_001` and ale as preferred gifts.
- Georgette:
  - now treats `libido_tincture_001` and ethanol as preferred gifts.

Condition:
- recipient must exist in relationship dictionaries;
- item must have the appropriate custom social properties.

Status:
- implemented and tested.

#### 4. Soap Production Was Reworked Into A Delayed Batch Process

Files:
- [SoapCraftAndAtticItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/SoapCraftAndAtticItems.rpy)
- [stat.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/stat.rpy)

Implemented:
- soap is no longer instantly usable the moment it is crafted.
- soap crafting now creates a pending batch:
  - ready after `7` days;
  - expires `14` days after becoming ready.
- batch state is now tracked explicitly:
  - `SoapPendingBatches`
  - `SoapStoredBatches`
- daily stat refresh now syncs pending/ready/expired soap batches into inventory.

Condition:
- crafting still requires:
  - recipe book;
  - bowl or bucket;
  - ready ash barrel;
  - pig lard;
  - lavender or wild rose.
- after crafting:
  - no soap appears immediately;
  - soap appears automatically after the curing delay.

Status:
- implemented and tested.

#### 5. Soap Use And Soap Gift Effects Were Expanded

Files:
- [SoapCraftAndAtticItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/SoapCraftAndAtticItems.rpy)
- [Actions.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Actions.rpy)
- [stat.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/stat.rpy)

Implemented:
- using soap now:
  - resets `dayssincewash`;
  - improves fun;
  - gives the player a temporary `+10` appearance bonus via the look breakdown.
- gifting soap to tavern crew now gives stronger effects:
  - `beauty +20`
  - `Friends +3`
  - `sluttiness/corruption +2`
  - `neshlush -2` for better obedience
- if friendship is already good enough, a follow-up need state is stored:
  - `SoapRequestQueue[girl] = 1`

Condition:
- stronger soap gift effect currently applies to:
  - `amanda`
  - `melissa`
  - `sandra`

Status:
- implemented and tested.

#### 6. Inventory Food And Drink Can Now Be Shared Or Used Through Player Card

Files:
- [Actions.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Actions.rpy)
- [PlayerCard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PlayerCard.rpy)
- [BerriesItem.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/BerriesItem.rpy)
- [MushroomItem.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/MushroomItem.rpy)
- [HoneyCombItem.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/HoneyCombItem.rpy)

Implemented:
- player-card item menu now supports `Поделиться` for:
  - drinks;
  - forest resources;
  - crafted goods;
  - ingredients marked as socially shareable.
- `mushroom_001` can now be eaten directly.
- `honey_comb_001` can now be eaten directly.
- sharing ale now returns:
  - empty bottle;
  - cork.
- sharing berries / mushrooms / honey with Sandra now produces a kitchen-specific reaction text about making something tasty for the household.

Condition:
- the item must exist in inventory;
- the item must have an `item_kind` supported by `player_share_item_with`;
- direct use actions still depend on the item exposing an action in its own item file.

Status:
- implemented;
- direct regressions added for ale-sharing and Sandra food-sharing.

#### 8. Branch Logic Audit Is Now A First-Class Stabilization Track

Files:
- [UiRegressionTests.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/UiRegressionTests.rpy)
- [TODOS.md](/c:/Users/blank/Documents/RenPy_Projects/Tractir/devdocs/TODOS.md)

Implemented:
- stabilization work is now explicitly split into:
  - feature work;
  - TXT parity work;
  - branch-logic audit work.
- branch-logic audit means:
  - checking that a branch still opens;
  - checking that it returns to the right room/state;
  - checking that daily/weekly gates do not double-fire or silently block;
  - checking that branch text and options still match TXT logic where TXT remains authoritative.

Current hotspot groups:
- church:
  - service
  - confession
  - after-sermon secret-room branches
- friday dance:
  - Amanda
  - Becky
  - Legare side branch
- tavern household loop:
  - morning breakfast
  - Wednesday wine-for-dance trigger
  - sleep / next-day transitions
- social routes:
  - Amanda
  - Melissa
  - Sandra
  - Clara
- crafting / inventory:
  - soap
  - recipe-book flow
  - fixed-target share/gift logic
- save/load:
  - object menu save path
  - runtime restore path

Priority rule:
- when a branch has known TXT authority, logical consistency is more important than expanding content or rewriting text.

Status:
- audit track started;
- now covered by targeted long-path regression tests in addition to narrow unit-like checks.

#### 7. Amanda / Melissa / Sandra Talk Menus Now Expose Core Social Actions

Files:
- [IntAmandaTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntAmandaTalk.rpy)
- [IntMelissaTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntMelissaTalk.rpy)
- [IntSandraTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntSandraTalk.rpy)
- [PlayerCard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PlayerCard.rpy)

Implemented:
- all three now expose:
  - `Поболтать`
  - `Пофлиртовать`
  - `Подарить что-нибудь`
- gift flow now goes through a fixed-target inventory menu so the player can pick an item first and keep the recipient fixed.

Condition:
- these actions are still daily-limited by:
  - `TalkedToday`
  - `FlirtedToday`
  - `GiftedToday`
- those counters are reset by the existing daily reset system.

Status:
- implemented;
- direct regression added for all three talk menus.

#### 8. Breakfast Now Exists As A Real Once-Per-Day Morning Routine

Files:
- [TavernKitchen.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernKitchen.rpy)

Implemented:
- breakfast is available before noon;
- breakfast can only happen once per day;
- breakfast now gathers whoever is currently present and gives them short lines;
- Sandra kitchen morning pictures now render when she is in the kitchen in the morning;
- Wednesday breakfast now includes Sandra's reminder about wine and better food supplies;
- if soap is ready, breakfast can announce it and add a small fun bump.

Condition:
- breakfast availability depends on:
  - `hour < 12`
  - `TavernBreakfastLastDay != dayspassed`
- Becky only joins breakfast lines when the kitchen-visit flag is active.

Status:
- implemented;
- direct regressions added for morning availability, once-per-day lock, and the Wednesday reminder.

#### 9. Confession Return Was Hardened Into A Dedicated Label

Files:
- [ChurchIspoved.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/ChurchIspoved.rpy)

Implemented:
- post-confession `Вернуться в собор` now routes through a dedicated `ChurchReturnAfterConfession` label instead of an inline call target.

Condition:
- the church branch still needs a broader parity pass, but the back path is now isolated and easier to test.

Status:
- implemented;
- existing regression coverage kept and expanded.

#### 10. Fixed-Target Sharing Was Added To Core Family Talk Menus

Files:
- [PlayerCard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PlayerCard.rpy)
- [IntAmandaTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntAmandaTalk.rpy)
- [IntMelissaTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntMelissaTalk.rpy)
- [IntSandraTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntSandraTalk.rpy)

Implemented:
- Amanda, Melissa, and Sandra talk menus now expose `Поделиться угощением` when the player actually has shareable items.
- a fixed-target share menu now exists, so the player can pick the item while keeping the conversation target locked.

Condition:
- the action is shown only when:
  - the daily gift slot is still free;
  - the player has at least one shareable item.

Status:
- implemented and tested.

#### 11. Becky And Sandra Tea Scene Exists In The Kitchen

Files:
- [TavernKitchen.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernKitchen.rpy)

Implemented:
- when Becky is on her monthly kitchen visit and Sandra is present, the player can now use one `energy_tea_001` to treat both of them in the kitchen.
- this raises both relationships and gives the kitchen a dedicated social text beat instead of leaving the visit purely decorative.

Condition:
- Becky monthly visit must be active;
- Sandra must actually be in the kitchen;
- the player must have `energy_tea_001`.

Status:
- implemented and tested.

#### 12. Melissa Got A First Clara-Specific Follow-Up

Files:
- [InitMelissa.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/InitMelissa.rpy)
- [IntMelissaTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntMelissaTalk.rpy)

Implemented:
- when Clara is visibly visiting the tavern and standing near Melissa, the player can now ask Melissa about her.
- Melissa now gives a small clarifying line about Clara and this is limited to once per day.

Condition:
- current room must be `TavernMain`;
- Clara must actually be visible there;
- the question has not already been asked that day.

Status:
- implemented and tested.

#### 13. Melissa Room Night Art Now Uses Her Newer Folder Assets

Files:
- [TavernMelissaRoom.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMelissaRoom.rpy)

Implemented:
- Melissa's room at night now rotates between several sleep pictures from her own folder instead of always using a single fallback image.

Condition:
- active only at night-time room view.

Status:
- implemented and tested.

### Still Open After Today

#### 1. Soap Follow-Up Demand Exists Only As State

Implemented base:
- `SoapRequestQueue` now records that a girl liked the soap and may want more.

Still missing:
- actual dialogue/event surface where crew members ask for more soap;
- reward / consequence path for fulfilling or ignoring the request.

Priority:
- medium-high, because the state now exists and should not remain invisible for long.

#### 2. More Chained Crafting Outcomes Still Need Expansion

Implemented base:
- ethanol now leads into at least one secondary crafted social drink.

Still missing:
- more layered recipes with distinct social use cases;
- more “use together” or “share with someone” item interactions;
- more recipient-specific reactions beyond the generic social-effect layer.

Priority:
- medium.

#### 3. Breakfast Social Layer Is Still Only A First Pass

Implemented base:
- once-per-day breakfast exists;
- present characters can say short lines;
- Wednesday supply reminder exists;
- soap-ready announcement exists.

Still missing:
- richer breakfast banter and event branches;
- Saturday laundry morning surface;
- Friday bath morning surface;
- random pre-noon room occupancy / "girls in their rooms" morning checks;
- Becky/Sandra tea-sharing breakfast and kitchen follow-up.

Note:
- the Becky/Sandra tea scene now exists as a normal kitchen interaction, but not yet as part of a deeper breakfast/event branch.

Priority:
- high, because the user explicitly wants morning routine to replace the old immediate-work feel.

### New Requests From Current Chat

These were requested after the feature pass above and should now drive the next stabilization wave.

#### 1. Church Branch Full Parity Sweep

Requested:
- make sure church wandering can still discover the locked room and its event chain;
- make sure confession links and after-sermon watch links work as real Ren'Py click paths;
- check the whole church branch for logic discrepancies against TXT.

Current state:
- church text links exist;
- secret-room watch branches exist for Becky, Georgette, and Liza;
- basic church tests exist;
- live parity still needs more end-to-end checking.

Priority:
- high.

#### 2. Soap Timing Clarification

Requested:
- soap should be effectively ready on a one-week cadence, not feel like a 30-day wait.

Current state:
- soap curing batch is already 7 days;
- ash-barrel readiness is still the confusing long gate in player-facing flow and must be kept aligned.

Priority:
- high.

#### 3. Amanda Fancy Night Bowl Follow-Up

Requested:
- gifting the fancy bowl should add friendship and trust;
- there should be a small decision whether she keeps relieving herself outside or stops.

Current state:
- buy and give path exists;
- follow-up relationship/trust effect and preference outcome needed explicit surfacing.

Priority:
- high.

#### 4. Daily Social Access For Amanda / Melissa / Sandra

Requested:
- all three should be consistently talkable, flirtable, and giftable;
- those daily interaction limits should reset every day.

Current state:
- shared daily counters already reset;
- room/talk exposure still needs an audit to ensure all three consistently surface those actions.

Priority:
- high.

#### 5. Ask / Favor Topics

Requested:
- girls should be askable for favors or special topics when discoveries and relationship thresholds unlock them.

Current state:
- Amanda has a specific night-bowl ask path;
- there is no broader ask/favor layer yet.

Priority:
- medium-high.

#### 6. Clarissa Market Follow

Requested:
- Clarissa should be followable in the market branch.

Priority:
- medium.

#### 7. Tavern Morning Routine Before Noon

Requested:
- workday should really begin at 12:00;
- before noon the crew should be doing routine things, talking, breakfast, and Sunday dinners.
We also can meet them in different rooms instead of just the main hall, and have more mini-scenes and interactions in those morning hours.
laundrery, bath days, cleaning, going to shop, help Sandra in kintchen, some dialogs brags, gossips, gigles etc

Current state:
- [TavernMain.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMain.rpy) now distinguishes morning preparation from full work mode;
- before noon the main hall no longer claims the crew is already fully "working";
- [TavernKitchen.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernKitchen.rpy) now offers a real breakfast action in the morning;
- Sunday daytime kitchen now exposes a separate shared meal action for a more substantial family meal.

Still missing:
- richer random morning mini-scenes and person-specific interactions;
- integrating those routines into the deeper event scheduler instead of room text only.

Priority:
- high.

#### 8. Becky Tavern Visits And Kitchen Tea

Requested:
- Becky visits should surface in tavern hall and kitchen;
- in kitchen the player should be able to serve tea to Becky and Sandra and gain Sandra relationship.

Priority:
- medium-high.

#### 3. Crafted Goods Are Functional, But Social Content Around Them Is Still Thin

Implemented base:
- craft -> inventory -> use/gift/sell loop is live.

Still missing:
- richer text outcomes when men and women react differently to the same gifted drink;
- more specific relationship revelations:
  - secrets;
  - flirt escalation;
  - lust/horny reactions;
  - trust disclosures.

Priority:
- medium.

## List A: New Features And Their Conditions

This section describes the feature layer that now exists in the Ren'Py runtime, whether or not that feature originally existed in TXT.

### 1. Derived Player Appearance / Reputation / Charisma

Files:
- [stat.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/stat.rpy)
- [PlayerCard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PlayerCard.rpy)

Current feature state:
- `look` is derived from dress, dress age/condition, haircut age, and hygiene.
- `charisma` is derived from `look + exploration contribution`.
- player reputation is separate from tavern reputation.
- dog ownership adds a permanent `+25` effective exploration bonus.
- player card text now changes from ordinary innkeeper to tracker/hunter style based on exploration progress.
- equipped rifle and cuirass are described in the player card text.

Conditions:
- haircut penalty turns severe after 30 days.
- dress deterioration penalty turns severe after 42 days.
- dog exploration bonus applies only if `dog.owned == True`.
- player card rank text depends on `effective_player_exploration()`.

Status:
- implemented and live.
- tested through current regression suite.

Open risks:
- haircut renewal gameplay is still incomplete.
- clothing renewal exists mechanically, but long-term parity with TXT economy/social consequences still needs review.

### 2. Recipe Book / Crafting / Soap Chain

Files:
- [CraftingRecipes.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/CraftingRecipes.rpy)
- [GameItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/GameItems.rpy)
- [SoapCraftAndAtticItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/SoapCraftAndAtticItems.rpy)
- [TavernAtic.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernAtic.rpy)
- [Backyard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Backyard.rpy)
- [StolyarWorkshop.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/StolyarWorkshop.rpy)

Current feature state:
- attic search can reveal the old recipe book.
- recipe book can be read through the recipe registry.
- recipe pages use images from `game/images/recipe_book`.
- recipe page explains missing ingredients.
- successful recipe creation creates a real inventory item.
- soap recipe currently consumes ingredients and creates `4` soap items.
- soap expires after 14 days.
- ash barrel can be ordered from Draupnir and now visibly appears in the backyard.

Conditions:
- attic hatch requires enough exploration and a separate search step.
- ash barrel ask/pay options require owning the recipe book.
- soap recipe requires:
  - recipe book;
  - bowl/bucket;
  - ash barrel installed and ready;
  - water path via backyard context;
  - flower ingredient (lavender or rose);
  - pig lard.
- ash barrel becomes ready only after the delayed day threshold (`SoapAshBarrelReadyDay`).

Status:
- implemented and live.
- registry-based, not hardcoded ad hoc.

Open risks:
- recipe system is no longer just flavor; it now overlaps with attic, backyard, item registry, and Draupnir order flow.
- each new recipe added later must stay in the same registry path and must not bypass `GameItems`.

### 3. Attic Item Runtime

Files:
- [SoapCraftAndAtticItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/SoapCraftAndAtticItems.rpy)
- [TavernAtic.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernAtic.rpy)
- [TavernMyRoom.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.rpy)

Current feature state:
- attic contains:
  - recipe book;
  - rusty hunter rifle;
  - old leather cuirass.
- these items can be found, taken, dropped, viewed, and managed.
- rifle can be cleaned, oiled, loaded, and unloaded.
- dropped book changes room picture/description in player room.
- dropped rifle changes room picture/description in player room.

Conditions:
- attic loot only appears after attic search.
- item management requires the item to exist either in attic inventory or player inventory.
- rifle maintenance/load actions depend on current rifle state and supplies.

Status:
- implemented and live.

Open risks:
- attic item behavior is a new feature layer and has limited TXT authority.
- any further expansion must keep item logic centralized and avoid splitting between room files and random helper files.

### 4. Dog Companion

Files:
- [DogCompanion.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DogCompanion.rpy)
- [Backyard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Backyard.rpy)
- [TavernMyRoom.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.rpy)
- [FightSystemRuntime.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FightSystemRuntime.rpy)

Current feature state:
- stray dog can spawn and be recruited.
- dog has its own talk-like interaction and card path.
- dog can be played with and trained.
- dog can become part of company/hunt support.
- dog grants a permanent exploration bonus while owned.
- dog booth can be ordered and built.

Conditions:
- first-week/evening/random spawn logic controls initial encounter.
- recruitment requires a bone.
- hunting/company support depends on `dog.owned` and `dog.in_company`.
- some anti-theft protection depends on loyalty thresholds.

Status:
- implemented as a new runtime feature.
- partially integrated into fight support and room presence.

Open risks:
- this system is mostly new, not TXT-anchored.
- every place where dog starts affecting old tavern event logic should be treated as a parity-sensitive overlap.

### 5. Hunter Club / Hunting Supplies / Forest Gatherables

Files:
- [HunterClub.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/HunterClub.rpy)
- [HunterClubItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/HunterClubItems.rpy)
- [Forest.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Forest.rpy)

Current feature state:
- hunter club exists as a town room.
- hunter store buys and sells hunting-related supplies and forest loot.
- forest gatherables and rare gatherables are now defined more explicitly.
- droplets and weapon oil are now real store items.

Conditions:
- hunter club schedule:
  - open morning through evening;
  - closed Friday and Sunday.
- rare gatherables are zone/rarity weighted.

Status:
- live as a room/store feature.

Open risks:
- animal loot exists, but hunting economy must stay aligned with eventual live animal encounter balance.

### 6. Fight / Hunt Runtime Layer

Files:
- [FightSystemRuntime.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FightSystemRuntime.rpy)
- [main_layout.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/my_layouts/main_layout.rpy)
- [fight_system.md](/c:/Users/blank/Documents/RenPy_Projects/Tractir/devdocs/fight_system.md)

Current feature state:
- fight screen exists inside `main_ui`.
- player/company and enemy sides render with health/status data.
- current action panel is reused for fight actions.
- ranged ammo state is rendered.
- enemy move text and action result text render in the center panel.
- hunt intro text and enemy move descriptions exist.
- dog participates in fight support.
- arrows and droplets have distinct combat behavior.

Conditions:
- hunt unlock currently depends on effective exploration threshold.
- ranged attacks depend on rifle state, ammo, and supplies.
- dog combat support depends on ownership/company/training state.
- forest trap state exists but should still be treated as early-stage runtime.

Status:
- runtime exists.
- playable engine is emerging, but still not fully closed as a mature system.

Open risks:
- this is the largest new feature layer in the project.
- because it is mostly new rather than TXT-ported, it must not quietly alter old event balance or room flow.

### 7. Modernized Main UI Room Flows

Files:
- [TavernMyRoom.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.rpy)
- [Backyard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Backyard.rpy)
- [TavernAtic.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernAtic.rpy)
- [DressShop.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressShop.rpy)
- [HunterClub.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/HunterClub.rpy)

Current feature state:
- several old locations were moved onto stable `main_ui` room loops.
- sleep from player room now returns to player room.
- player room exits upstairs, not directly downstairs.
- attic/recipe flow, dog flow, and new room overlays were integrated without separate menu systems.

Conditions:
- room/object flows should always restore into the current room’s action panel.
- no nested `display_menu` / legacy stack unwinds should remain in these migrated paths.

Status:
- mostly implemented in the touched rooms.

Open risks:
- other legacy rooms still exist and remain candidates for return/overlay bugs.

## List B: TXT Implementation Status And Its Conditions

This section is about parity status, not feature ambition.

### A. TXT-authoritative and already actively mirrored in `.rpy`

These should still be treated as canonical old gameplay areas, even if internal structure was modernized.

- [TavernMain.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMain.txt) -> [TavernMain.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMain.rpy)
  - condition:
    - room hours;
    - Friday dance redirection;
    - tavern closed/open state;
    - core room loop.
- [TavernMyRoom.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.txt) -> [TavernMyRoom.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.rpy)
  - condition:
    - base room description;
    - sleep action;
    - room exit topology.
- [DressShop.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressShop.txt) -> [DressShop.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressShop.rpy)
  - condition:
    - Irma talk path;
    - dress ordering;
    - visible racks and room description;
    - fitting/order flow.
- [FridayDance.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FridayDance.txt) -> [FridayDance.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FridayDance.rpy)
  - condition:
    - Friday evening routing;
    - Amanda/Becky branch access;
    - crowd observation flow.
- [PortStreets.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PortStreets.txt) -> [PortStreets.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PortStreets.rpy)
  - condition:
    - Georgette/Lizett presence logic;
    - backstreet prostitution/event gating.
- [StolyarWorkshop.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/StolyarWorkshop.txt) -> [StolyarWorkshop.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/StolyarWorkshop.rpy)
  - condition:
    - Draupnir’s original shop logic and order/payment patterns still remain authoritative.

Status:
- converted and live.
- still parity-sensitive.

### B. TXT-backed but now partially overlapped by new systems

These already have working `.rpy` conversions, but they are no longer “pure ports” because a new runtime layer now touches them.

- [TavernMyRoom.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.txt)
  - overlapped by:
    - attic hatch;
    - attic loot;
    - dropped room-item visuals;
    - dog presence;
    - wake-up routing changes.
- [Backyard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Backyard.rpy)
  - old room context is now overlapped by:
    - soap crafting;
    - ash barrel delivery;
    - dog booth / dog presence.
- [DressShop.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressShop.txt)
  - old tailor flow is now overlapped by:
    - new image asset policy;
    - card integration;
    - Clara visibility.
- [PortStreets.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PortStreets.txt)
  - old Georgette street logic is overlapped by:
    - stabilized UI return flow;
    - prostitution/paid module return handling.
- [FridayDance.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FridayDance.txt)
  - old dance logic is overlapped by:
    - main UI integration;
    - relationship/gating bugfixes;
    - repeated-week reset fixes.

Status:
- high-priority review zone.

Condition for further work:
- any new feature here must be justified against the TXT branch first.
- every touched branch should ideally gain a regression before more expansion.

### C. Mostly new runtime systems with weak or no direct TXT anchor

These are currently Ren'Py feature-layer systems more than TXT migration targets.

- dog companion system
- recipe registry and recipe-book page rendering
- attic item management and rifle maintenance
- hunter club as expanded hunting economy hub
- full hunt/fight runtime layer
- dynamic player exploration-title descriptions

Status:
- allowed as extensions.

Condition:
- must not silently change canonical TXT outcomes in rooms/events that already existed.
- should preferably stay isolated until explicitly mapped to source `.txt` semantics.

### D. TXT migration hotspots still needing structural review

These are not necessarily broken right now, but they remain migration-risk areas.

- `NextDay_*` dispatch and compatibility wrappers
- legacy event wrappers guarded by `renpy.has_label(...)`
- remaining legacy room/bootstrap patterns around grocery/wine/talk flows
- legacy compatibility aliases that still obscure direct TXT parity review

Status:
- still active migration debt.

Condition:
- do not remove wrappers until equivalent direct converted implementations are verified.

## Where Both Lists Meet

This is the real overlap set: places where a new feature touches a TXT-authoritative area.

### 1. Player Room + Attic

TXT side:
- [TavernMyRoom.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.txt)

New feature side:
- attic hatch discovery
- attic loot
- dropped book/rifle visuals
- sleep return-to-room behavior

Why it matters:
- this is no longer just a converted room.
- it is now a TXT-backed room carrying several extension systems at once.

Required condition for future edits:
- preserve original room text and room identity;
- keep new attic/dropped-item logic additive, not replacing core room flow.

### 2. Backyard

TXT side:
- backyard is part of core tavern world flow even if its new runtime is more expanded now.

New feature side:
- soap crafting
- ash barrel
- dog booth
- dog presence

Why it matters:
- backyard has become a systems hub.
- that makes it easy to accidentally overload one room with unrelated runtime logic.

Required condition for future edits:
- backyard should remain the scene host only;
- crafting/order logic should stay registry/system-driven, not copied into room code repeatedly.

### 3. Dress Shop / Irma

TXT side:
- [DressShop.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressShop.txt)
- [DressTry.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressTry.txt)

New feature side:
- updated Irma art bindings
- card integration
- modernized catalog overlays

Why it matters:
- visuals were changed, but old fitting/order logic still belongs to TXT parity.

Required condition for future edits:
- image/path refresh is fine;
- behavior/gates inside fitting/talk/order flow should still be checked against TXT before any redesign.

### 4. Friday Dance / Becky / Amanda / Georgette

TXT side:
- [FridayDance.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FridayDance.txt)
- [IntBeckyDance.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntBeckyDance.txt)
- [IntAmandaDance.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntAmandaDance.txt)
- [PortStreets.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/PortStreets.txt)

New feature side:
- UI stabilization
- repeated-week dance fixes
- Georgette prostitution-return stabilization

Why it matters:
- these are story-sensitive social flows.
- a “small UI fix” can still alter gating, resets, or counters.

Required condition for future edits:
- any dance/social fix must be checked against branch counters and weekly reset semantics from TXT.

### 5. Draupnir Workshop

TXT side:
- [StolyarWorkshop.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/StolyarWorkshop.txt)

New feature side:
- ash barrel order
- dog booth order

Why it matters:
- this shop now hosts both original tavern improvements and new feature orders.

Required condition for future edits:
- order/payment/install flow must remain explicit and visible in the destination room, not just set flags invisibly.

## Detailed Priority TODO

### Priority 1: Overlap Audit Before New Expansion

- [ ] Audit [TavernMyRoom.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.rpy) against [TavernMyRoom.txt](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/TavernMyRoom.txt):
  - confirm wake-up flow;
  - confirm upstairs exit topology;
  - confirm attic is additive rather than replacing original room semantics.
- [ ] Audit [Backyard.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/Backyard.rpy) as a multi-system room:
  - soap;
  - ash barrel;
  - dog booth;
  - dog talk;
  - keep room action list readable and non-duplicated.
- [ ] Audit [DressShop.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressShop.rpy) and [DressTry.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DressTry.rpy):
  - confirm Irma image refresh did not alter order/fitting logic;
  - confirm TXT menu conditions still hold.
- [ ] Audit [FridayDance.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FridayDance.rpy), [IntBeckyDance.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntBeckyDance.rpy), and [IntGeorgettTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntGeorgettTalk.rpy):
  - validate weekly counters/resets;
  - validate re-entry behavior;
  - validate no overlay/double-menu regressions remain.

### Priority 2: Keep New Systems Centralized

- [ ] Keep recipes in [CraftingRecipes.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/CraftingRecipes.rpy), not scattered through room files.
- [ ] Keep items in [GameItems.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/GameItems.rpy), not defined ad hoc in scene files.
- [ ] Keep combat state in [FightSystemRuntime.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/FightSystemRuntime.rpy), not reimplemented per forest room.
- [ ] Keep dog runtime in [DogCompanion.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DogCompanion.rpy), with rooms only exposing access points.

### Priority 3: TXT Parity Hotspots Still Open

- [ ] [NextDay_NewDayEvents.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/NextDay_NewDayEvents.rpy):
  replace compatibility wrappers (`Table_NewLine`, `GetRandomGirlByJob`, `CheckDailyEventExists`) with direct converted location/function implementations once available.
- [ ] [NextDay_NewDayEvents.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/NextDay_NewDayEvents.rpy):
  after converting `WhoreNextDayClients.txt`, switch guarded `renpy.has_label("WhoreNextDayClients")` calls to direct calls.
- [ ] [NextDay_NewDayEvents.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/NextDay_NewDayEvents.rpy):
  review source condition using `sluttiness['alberfriends']` versus `AmandaVar['alberfriends']` against original design intent.
- [ ] [GroceryStore.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/GroceryStore.rpy), [IntEddieTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntEddieTalk.rpy), [IntBeckyTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntBeckyTalk.rpy):
  remove remaining grocery bootstrap code and align Eddie/Becky talk flow with the current main UI character actions.
- [ ] [WineStore.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/WineStore.rpy), [IntClaraTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntClaraTalk.rpy), [IntAlberTalk.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/IntAlberTalk.rpy):
  remove remaining winery bootstrap code and align Clara/Alber talk flow with the current main UI character actions.

### Priority 4: New System Maturity Gates

- [ ] Fight/hunt engine:
  finish retreat/aftermath branch, sickness-day consequences, and trap-resolution loop before treating it as production-stable.
- [ ] Dog system:
  finish theft/non-payment interception reward balancing before expanding into more tavern events.
- [ ] Recipe system:
  add new recipes only via existing registry path and only after item registry coverage is confirmed.

## Historical Migration References

- Tavern events reference:
  see [TAVERN_EVENTS_MECHANICS.md](/c:/Users/blank/Documents/RenPy_Projects/Tractir/devdocs/TAVERN_EVENTS_MECHANICS.md) for queue/dispatcher flow, side effects, and crew-relationship impact map.
- World-location migration checklist:
  see [LOCATION_WORKLIST.md](/c:/Users/blank/Documents/RenPy_Projects/Tractir/devdocs/LOCATION_WORKLIST.md).
- Main UI behavior reference:
  see [MAIN_UI_INSTRUCTIONS.md](/c:/Users/blank/Documents/RenPy_Projects/Tractir/devdocs/MAIN_UI_INSTRUCTIONS.md).

## Historical Cleanup Waves (kept for continuity)

### Cleanup Wave 1 to 1.6 (done)

- completed migration hardening already recorded in previous version of this file:
  - `loc.rpy`
  - `CheckDailyEvent.rpy`
  - `NextDay_NewDayEvents.rpy`
  - `onobjsel.rpy`
  - `Intro.rpy`
  - `TavernHelp.rpy`
  - `my_layouts/main_layout.rpy`
  - `my_layouts/layout_logic.rpy`
  - `status.rpy`
  - `NextDay.rpy`
  - `IntAlberTalk.rpy`
  - `AmandaDynamicCommonBlocks.rpy`
  - `DebugTools.rpy`
  - related call/jump/global cleanup passes

### Cleanup Wave 2 (still relevant)

- [ ] Remove remaining high-count `globals()` usage from:
  - [layout_logic.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/my_layouts/layout_logic.rpy)
  - [DebugTools.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/DebugTools.rpy)
  - [KidsFunctions.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/KidsFunctions.rpy)
  - [status.rpy](/c:/Users/blank/Documents/RenPy_Projects/Tractir/game/status.rpy)
- [ ] Replace remaining Python `renpy.call/renpy.jump` occurrences in legacy interaction/event files, preserving TXT parity.
