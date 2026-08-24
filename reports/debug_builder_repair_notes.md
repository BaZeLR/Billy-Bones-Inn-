# Debug Builder Repair Notes

Generated from the current runtime state. This report is evidence for source patches; it is not a source patch itself.

## Current State

- CurLoc: `DebugBuilderRoom`
- Time slot: `1`, clock `08:15`, weekday `1`, day ``

## Expected Vs Reality Checklist

- Expected: room text and picture are owned by the Room object. Reality: inspect room reports below for missing/duplicated text or bad paths.
- Expected: object actions are owned by room GameObjects/GameItems. Reality: inspect menu reports below for missing or redundant menu items.
- Expected: NPC presence resolves from schedule and agrees with Room.visible_npcs(). Reality: inspect schedule report below.
- Expected: events are exposed by Event/Thread checks and fired through checkTriggers. Reality: inspect event probes below.
- Expected: image sequences resolve to loadable files. Reality: inspect media sequence report below.

## Manual Notes From Play Debug Session

Write concrete notes here after using the visual builder:

- Expected:
- Reality:
- Screen/path used:
- Suspected owner file:
- Requested repair wording:

## Feature Repair Templates

Use these templates for concrete repair notes. Keep one feature per filled block.

### Room Feature

- Feature name:
- Room code_name:
- Room object variable:
- Room owner file:
- Room label:
- Expected room text:
- Actual room text:
- Expected picture path:
- Actual picture path / loadable:
- Exits expected:
- Exits actual:
- Objects expected:
- Objects actual:
- Menu title expected:
- Menu items expected:
- Menu items actual:
- Suspected duplicate/bloat labels to remove or bypass:
- Direct debug path:
- External test name:

### Event / Thread Feature

- Feature name:
- Thread id / object:
- Event id / target:
- Event owner file:
- Event label:
- Trigger location:
- Trigger action:
- Conditions expected:
- Conditions actual from event probe:
- Required variables/state:
- Variables changed by label:
- Expected menu title:
- Expected menu items:
- Actual menu items:
- Expected return flow:
- Actual return flow:
- Picture path / sequence:
- Direct debug path:
- External test name:

### NPC Presence / Schedule Feature

- Feature name:
- NPC id:
- PeopleData object:
- PeopleInfo/runtime object:
- Schedule owner file or JSON:
- Expected weekday/time interval:
- Expected location:
- Actual getLocation():
- Actual Room.visible_npcs():
- Expected awake/talkable:
- Actual awake/talkable:
- Expected HUD name:
- Actual HUD name:
- Default NPC action label/menu:
- Direct debug path:
- External test name:

### Object / Action Menu Feature

- Feature name:
- Room code_name:
- GameObject id:
- GameObject owner file:
- Object menu label:
- Action label/function:
- Expected object description:
- Actual object description:
- Expected menu title:
- Expected menu items:
- Actual menu items:
- State variables changed by function/method:
- Text/picture presented by label:
- Direct debug path:
- External test name:

### Picture / Sequence Feature

- Feature name:
- Owner label/object/event:
- Expected base path:
- Expected files:
- Actual resolved paths:
- Missing files:
- vscene/show helper used:
- Direct debug path:
- External test name:

### Shop / Item Feature

- Feature name:
- Room code_name:
- Container GameObject id:
- GameItem ids expected:
- GameItem owner file:
- Catalog/list owner:
- Expected item display names:
- Expected descriptions:
- Expected prices:
- Expected buy/action label:
- Expected depreciation/wear state:
- Actual menu/screen items:
- State variables changed by buy/apply function:
- Direct debug path:
- External test name:

## Picture Paths

Picture path checks:
[[OK] images/general/player_card.jpg
[[OK] images/amanda/amanda_card.jpg
[[OK] images/melissa/melissa_card.jpg
[[OK] images/sandra/sandra_card.jpg
[[OK] images/irma/portraits/portrait1.png
[[OK] images/irma/portraits/portrait2.png
[[OK] images/irma/portraits/portrait3.png
[[OK] images/irma/measure/measure1.png
[[MISS] images/irma/measure/measure2.png
[[MISS] images/irma/measure/measure3.png
[[MISS] images/irma/measure/measure4.png
[[OK] images/irma/talks.png
[[OK] images/irma/flirts.png
[[OK] images/market/LocMarketPlace1.jpg
[[OK] images/townLifeRandomPic.jpg
[[MISS] bg TavernMain
[[MISS] bg TavernKitchen
[[MISS] bg amanda_room
[[MISS] images/melissa/tavern/melissa_portrait.png
[[OK] images/tavern/secondfloor/sandra_room.png
[[MISS] bg StreetTavern
[[OK] images/clara/wineSellar_clara_talk.png
[[MISS] images/general/becky_inStore.png
[[OK] images/general/hunter_store.jpg
[[OK] images/georgett/Port/port1.jpg
[[OK] images/general/LocChurchClosed1.jpg
[[OK] images/forest/forest_1.png
[[MISS] bg ArtisansQuarter
[[OK] images/tavern/backyard/backyard_1.png
[[OK] images/barber shop/barber shop.jpg
[[OK] images/becky/Home/withbecky.jpg
[[OK] images/becky/Home/house2.jpg
[[OK] images/general/cityguard.jpg
[[OK] images/rpg_message_bg.png
[[OK] images/ellona/ante2.jpg
[[OK] images/ellona/Fran1.jpg
[[OK] images/forest/cave_day.png
[[OK] images/forest/hidden_path.png
[[OK] images/forest/seclude_lake.png
[[OK] images/forest/seclude_lake_1.png

## Picture Sequences

Picture sequence probes:

MarketPlace:
- found 2/4
  OK   images/general/LocMarketPlace1.jpg
  OK   images/general/LocMarketPlace2.jpg
  MISS images/general/LocMarketPlace3
  MISS images/general/LocMarketPlace4

ArtisansQuarter:
- found 4/4
  OK   images/general/LocArtisansQuarter1.jpg
  OK   images/general/LocArtisansQuarter2.jpg
  OK   images/general/LocArtisansQuarter3.jpg
  OK   images/general/LocArtisansQuarter4.jpg

StreetTavern:
- found 2/4
  OK   images/general/LocStreetTavern1.jpg
  OK   images/general/LocStreetTavern2.jpg
  MISS images/general/LocStreetTavern3
  MISS images/general/LocStreetTavern4

Forest:
- found 2/4
  OK   images/forest/forest_1.png
  OK   images/forest/forest_2.png
  MISS images/forest/forest_3
  MISS images/forest/forest_4

Irma measure:
- found 3/4
  OK   images/irma/measure/measure1.png
  OK   images/irma/measure/measure2.jpg
  OK   images/irma/measure/measure3.jpg
  MISS images/irma/measure/measure4

## NPC Schedules

NPC schedule at week=1 time=1 clock=08:15:

Time slots:
- 0: early morning / раннее утро, 06:00-07:59
- 1: morning / утро, 08:00-10:59 <==
- 2: noon / полдень, 11:00-12:59
- 3: afternoon / после полудня, 13:00-15:59
- 4: day / день, 16:00-17:59
- 5: evening / вечер, 18:00-20:59
- 6: late evening / поздний вечер, 21:00-22:59
- 7: night / ночь, 23:00-05:59

Resolved NPC locations:
- alber -> getLocation=WineStore CurrentLoc=WineStore entry=<none>
- amanda -> getLocation=TavernAmandaRoom CurrentLoc=TavernAmandaRoom entry=breakfast 08:00-09:00 awake=True talk=True p=100 source=json
- becky -> getLocation=BeckyHome CurrentLoc=BeckyHome entry=home_awake 06:00-22:59 awake=True talk=False p=100 source=json
- clara -> getLocation=WineStore CurrentLoc=WineStore entry=wine_store 08:00-11:59 awake=True talk=True p=600 source=json
- draupnir -> getLocation=StolyarWorkshop CurrentLoc=StolyarWorkshop entry=<none>
- eddie -> getLocation=GroceryStore CurrentLoc=GroceryStore entry=grocery_morning_shift 08:00-12:30 awake=True talk=True p=760 source=json
- fran -> getLocation=EllonaTemple CurrentLoc=EllonaTemple entry=<none>
- georgett -> getLocation=PortStreets CurrentLoc=PortStreets entry=<none>
- gerhard -> getLocation=Church CurrentLoc=Church entry=<none>
- inga -> getLocation=BeckyHome CurrentLoc=BeckyHome entry=inga_home_awake slots=0,1,2,3 awake=True talk=True p=20 source=rpy
- irma -> getLocation=DressShop CurrentLoc=DressShop entry=tailor_shop 06:00-12:59 awake=True talk=True p=600 source=json
- liza -> getLocation=PortStreets CurrentLoc=PortStreets entry=<none>
- luisa -> getLocation=Church CurrentLoc=Church entry=<none>
- melissa -> getLocation=TavernKitchen CurrentLoc=TavernKitchen entry=breakfast 08:00-08:59 awake=True talk=True p=650 source=json
- mongol -> getLocation=MarketPlace CurrentLoc=MarketPlace entry=<none>
- robin -> getLocation=Forest CurrentLoc=Forest entry=<none>
- sandra -> getLocation=TavernKitchen CurrentLoc=TavernKitchen entry=working_kitchen 08:00-20:30 awake=True talk=True p=600 source=json
- sergio -> getLocation=ArtisansQuarter CurrentLoc=ArtisansQuarter entry=<none>
- zimmer -> getLocation=CityGuard CurrentLoc=CityGuard entry=<none>

Rooms with NPCs:
- ArtisansQuarter: getNPCids=sergio | visible_npcs=sergio
- BeckyHome: getNPCids=becky, inga | visible_npcs=becky
- Church: getNPCids=gerhard, luisa | visible_npcs=gerhard, luisa
- CityGuard: getNPCids=zimmer | visible_npcs=
- DressShop: getNPCids=irma | visible_npcs=irma
- EllonaTemple: getNPCids=fran | visible_npcs=fran
- Forest: getNPCids=robin | visible_npcs=robin
- GroceryStore: getNPCids=eddie | visible_npcs=eddie
- MarketPlace: getNPCids=mongol | visible_npcs=mongol
- PortStreets: getNPCids=georgett, liza | visible_npcs=
- StolyarWorkshop: getNPCids=draupnir | visible_npcs=
- TavernAmandaRoom: getNPCids=amanda | visible_npcs=amanda
- TavernKitchen: getNPCids=melissa, sandra | visible_npcs=melissa, sandra
- WineStore: getNPCids=alber, clara | visible_npcs=alber, clara

Duplicate/source checks:
- peopleInfo without peopleData: <none>

## Event Probes

Event condition probes:
Current location=DebugBuilderRoom week=1 time=1 day=0

Available events from availEvents[[location][[action]:
- TavernMyRoom / sleep -> thread=sandraWeeklyEvaluation target=sandraWeeklyEvaluation_0 p=

## Priority Room/Menu Probes

### TavernMain

Room/menu probe: TavernMain / Главная зала трактира
Object menu label: TavernMainObjectMenu

Visible generated menu items:
- Книга на стойке
- Камин
- Барная стойка
- Пройти на кухню
- Выйти на улицу
- Подняться наверх
- Проверить конюшню

Objects and object actions:
- book_001 / Книга на стойке
  action: Читать "Бабслей и Литрбол для чайников" -> TavernHelp
  action: Осмотреть книгу -> Потрепанный семейный том, который давно стал частью трактира.
- fireplace_001 / Камин
  action: Разжечь огонь -> MakeFire
  action: Сложить рядом дрова -> TavernMainFireplaceDepositWood
  action: Вычистить золу -> Clean
  action: Осмотреть камин -> Examine
- bar_001 / Барная стойка
  action: Осмотреть стойку -> Examine
  action: Выпить эля -> Drink
  action: Позвать кого-нибудь выпить -> TavernMainBarInviteMenu
  action: Задержаться у стойки в ожидании истории -> TavernMainBarPlaceholderEvent

Room actions:
- <none>

Exits:
- Пройти на кухню -> TavernKitchen
- Выйти на улицу -> StreetTavern
- Подняться наверх -> TavernUpstairs
- Проверить конюшню -> TavernStable

### TavernKitchen

Room/menu probe: TavernKitchen / Кухня
Object menu label: TavernKitchenObjectMenu

Visible generated menu items:
- Очаг
- Котел
- Вернуться в зал
- Идти в склад
- Выйти на задний двор

Objects and object actions:
- hearth_001 / Очаг
  action: Разжечь огонь -> MakeFire
  action: Сложить рядом дрова -> TavernKitchenHearthDepositWood
  action: Вычистить золу -> Clean
  action: Осмотреть очаг -> Examine
- cauldron_001 / Котел
  action: Вскипятить воду -> BoilWater

Room actions:
- <none>

Exits:
- Вернуться в зал -> TavernMain
- Идти в склад -> TavernStorage
- Выйти на задний двор -> Backyard

### TavernAmandaRoom

Room/menu probe: TavernAmandaRoom / Комната Аманды
Object menu label: tavern_amanda_room_object_menu

Visible generated menu items:
- Дверь
- Кровать
- Лари с вещами
- Окно
- Вернуться в коридор

Objects and object actions:
- amanda_room_door_001 / Дверь
  action: Осмотреть дверь -> BedroomDoorInspect
- bed_002 / Кровать
  action: Пристать к Аманде -> TavernAmandaRoomGropeAction
  action: Осмотреть кровать -> Аккуратная кровать у стены. По вечерам Аманда спит именно здесь.
- chests / Лари с вещами
  action: Осмотреть лари -> Несколько простых ларей с одеждой и личными вещами Аманды. Рыться в них без спроса было бы уже слишком.
- window / Окно
  action: Осмотреть окно -> TavernAmandaRoomWindowLook

Room actions:
- <none>

Exits:
- Вернуться в коридор -> TavernUpstairs

### TavernMelissaRoom

Room/menu probe: TavernMelissaRoom / Комната Мелиссы
Object menu label: TavernMelissaRoomObjectMenu

Visible generated menu items:
- Дверь
- Вернуться в коридор

Objects and object actions:
- melissa_room_door_001 / Дверь
  action: Осмотреть дверь -> BedroomDoorInspect

Room actions:
- <none>

Exits:
- Вернуться в коридор -> TavernUpstairs

### DressShop

Room/menu probe: DressShop / Лавка портнихи
Object menu label: DressShopObjectMenu

Visible generated menu items:
- Женские образцы
- Мужские образцы
- Рабочий стол Ирмы
- Вернуться в квартал ремесленников

Objects and object actions:
- female_samples_001 / Женские образцы
  action: Посмотреть женские платья -> DressShopOpenCatalog
- male_samples_001 / Мужские образцы
  action: Посмотреть мужские костюмы -> DressShopOpenCatalog
- worktable_001 / Рабочий стол Ирмы
  action: Спросить, когда будет готово -> Вы осведомились у Ирмы, скоро ли будет готов ваш заказ. Она подняла на вас удивленный взгляд и ответила, что, как она и говорила, закончит работу к завтрашнему утру.
  action: Осмотреть рабочий стол -> На столе царит рабочий порядок: ткани, выкройки и инструменты лежат именно там, где Ирма привыкла их держать.

Room actions:
- <none>

Exits:
- Вернуться в квартал ремесленников -> ArtisansQuarter

### WineStore

Room/menu probe: WineStore / Винный погребок
Object menu label: WineStoreObjectMenu

Visible generated menu items:
- Бочки с вином
- Подвал
- Вернуться на рынок

Objects and object actions:
- wine_stock / Бочки с вином
  action: Купить вино -> WineStoreBuyMenu
  action: Осмотреть товар -> Повсюду бочки, бутылки и винный дух. Сразу видно, что здесь торгуют всерьез.
- cellar / Подвал
  action: Осмотреть подвал -> Подвал забит винными запасами еще плотнее, чем сама лавка.

Room actions:
- <none>

Exits:
- Вернуться на рынок -> MarketPlace

### MarketPlace

Room/menu probe: MarketPlace / Рыночная площадь
Object menu label: MarketPlaceObjectMenu

Visible generated menu items:
- Рыночные лотки
- Лавка Блэнкеншип
- Погребок Легаре
- Приемная стражи
- Охотничий клуб
- Идти в продуктовую лавку вдовы Блэнкеншип
- Идти в винный погребок Легаре
- Зайти в охотничий клуб
- Зайти к стражникам
- Вернуться к трактиру

Objects and object actions:
- market_stalls / Рыночные лотки
  action: Осмотреть лотки -> Торговцы расхваливают товар наперебой, покупатели торгуются, а вокруг стоит привычный рыночный шум.
- grocery_route / Лавка Блэнкеншип
  action: Идти в продуктовую лавку -> GroceryStore
- wine_route / Погребок Легаре
  action: Идти в винный погребок -> WineStore
- guard_office / Приемная стражи
  action: Зайти к стражникам -> CityGuard
  action: Осмотреть вход -> Неприметная дверь рядом с караулкой ведет в небольшую приемную, где принимают жалобы горожан.
- hunter_club_route / Охотничий клуб
  action: Зайти в охотничий клуб -> HunterClub
  action: Осмотреть дверь -> Тяжелая дверь украшена старой волчьей шкурой и парой кабаньих клыков. Похоже, внутри торгуют охотничьим добром и трофеями.

Room actions:
- <none>

Exits:
- Идти в продуктовую лавку вдовы Блэнкеншип -> GroceryStore
- Идти в винный погребок Легаре -> WineStore
- Зайти в охотничий клуб -> HunterClub
- Зайти к стражникам -> CityGuard
- Вернуться к трактиру -> StreetTavern

## Repair Wording Template

Use this wording when filing a concrete repair item:

> Expected: `<what the Room/GameObject/Schedule/Event definition says should happen>`
> Reality: `<what the debug builder shows instead>`
> Owner file: `<exact .rpy file and object/label/function>`
> Repair: `<change the owner definition only; do not add duplicate wrappers>`
> Test: `<debug builder path plus external click test name>`

## Ownership Notes

Correction ownership notes:

Room text and room picture paths:
- patch the Room object definition that owns the room.
- do not duplicate text inside the location label.

Object menu items:
- patch the GameObject actions or the room object's object_menu_label path.
- do not add dispatch labels for one simple action.

NPC schedules:
- patch the owning Init*.rpy schedule entries or NPCDailyScheduleTemplates.
- the debug schedule page shows the matched entry label, slots, awake/talkable, and priority.

Story/event conditions:
- patch the Event tuple/class definition or its condition function.
- test through checkTriggers(location, action, 0), not direct label jumps.

Picture sequences:
- patch the media path builder input or the concrete folder/file names.
- use the media probe to verify loadable paths before patching labels.
