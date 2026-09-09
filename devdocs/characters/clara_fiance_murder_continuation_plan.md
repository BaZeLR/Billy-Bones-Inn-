# Clarissa Fiance Murder And Tavern Continuation Plan

Status: approved story/design plan; implementation is not part of this document.

## Purpose

This plan defines the continuation that begins after the player has witnessed
Clarissa's birching/sexual punishment by Alber Legare and learned enough about
her drawings and relationship with him. It covers:

1. meeting Clarissa's fiance at church;
2. witnessing the fiance's secret relationship with Sergio;
3. finding Sergio's shop closed on the next scheduled visit;
4. hearing from Luisa that Clarissa and Sergio were arrested after the fiance's
   murder;
5. bringing Zimmer one additional barrel of wine before he will discuss the
   case;
6. advocating for Clarissa before Zimmer and solving his witness puzzle;
7. releasing Clarissa and Sergio;
8. Sergio's promised continuation and ointment recipe;
9. Clarissa moving into Melissa's room at the tavern;
10. Clarissa's anal confession and treatment with the ointment;
11. activation of the Legare revenge, Clarissa intimacy, card teaching, and
    noble-manners continuations.

This is a continuation of existing content. It must replace the incorrect
partial implementation in place; it must not be added as a parallel story.

## Canonical Names

- Runtime character id: `clara`; display name: Clarissa / `Кларисса`.
- `Alber` is the existing Alber Legare object and `images/Alber` asset owner.
  The name "Aldert" in the design prompt refers to this existing character; do
  not create an `Aldert` NPC or a second Legare state.
- Sergio, Luisa, and Zimmer are the existing registered NPC objects.
- Clarissa's fiance remains a narrative participant in the thread. Do not
  register a `ClaraFiance` NPC solely to hold one scene's state.
- James Leonard is the murder victim named in Zimmer's puzzle. He is narrative
  content, not a new persistent NPC unless later gameplay requires interaction
  with him.

## Binding Architecture

The documented project model remains mandatory:

- `threads["claraPaintingsPath"]` owns the ordered progress of this complete
  chain. Its `num`, `day`, `completed`, and `aborted` values are the only story
  progression authority.
- Event objects in `claraThreadList` own weekday, exact-hour, delay,
  probability, condition, location/action, and priority.
- Story labels in `ClaraPaintingsThread.rpy` own event picture, event text,
  native `menu:`, consequences, and return flow.
- Rooms own their normal descriptions, open/closed state, objects, and
  navigation. Room descriptions must not be visible during an active event.
- `PeopleRegistry` and the existing NPC objects own identity, relationship, and
  schedule state.
- `crafting.special_cream_recipe_unlocked` owns recipe discovery.
- Player inventory owns `special_cream_001` quantities and consumption.
- `tractir_progress.sergio_discount_percent` owns Sergio's permanent discount.
- `player.tavern_management.winenum` owns the tavern's wine stock and is the
  only authority for Zimmer's required additional wine delivery.
- Tavern business state owns any future noble-patronage level. It must not be
  mirrored on Clarissa, in a screen, or in another global flag.

Forbidden for this continuation:

- a second fiance/murder thread covering the same stages;
- `ClaraFianceVar`, `SergioVar`, or new global booleans such as
  `fiance_seen`, `sergio_arrested`, `clara_released`, `clara_moved_in`, or
  `zimmer_case_wine_delivered`;
- readiness wrappers that repeat the event tuple;
- room-entry code advancing the thread;
- screen-owned story logic;
- refresh/rebuild/handler labels, queued text, or recursive menu loops;
- reconstructing story progress from relationship points after loading.

## Existing Baseline And Required Correction

`claraPaintingsPath` already contains stages 0 through 12. Stages 0 through 5
establish the drawings, the cellar punishment, the later conversations, and
Legare's true relationship to Clarissa. Preserve those working stages and their
earned relationship changes.

The current stages 6 through 12 are only a partial draft and do not match the
approved order:

- stage 6 describes the fiance but does not display the two existing fiance
  images from `images/Alber/church`;
- stage 7 uses an hour range that does not match Sergio's actual shop schedule
  and advances before the player has successfully observed the scene;
- stages 8 and 9 add a commission detour not present in the approved sequence;
- stage 10 repeats the secret observation with Clarissa instead of proceeding
  to Sergio's closed shop;
- stage 11 places Clarissa in Melissa's room before the arrest and release;
- stage 12 starts at City Guard, depends on the unrelated sofa thread, uses a
  different murder puzzle, and grants Sergio's later rewards immediately.

Replace stages 6 onward in the same thread with the target sequence below.

## Exact Schedule Authorities

Use actual clock hours, not descriptive time-slot names.

| Place/person | Authoritative playable window |
| --- | --- |
| Church service attendee menu | Sunday, 08:00-09:29 |
| Sergio at Barber Shop | Monday/Wednesday 12:00-17:59; Saturday 08:00-11:59 |
| Luisa at Hunter Club | Monday-Thursday and Saturday, 08:00-18:59 |
| Zimmer reception | Tuesday 16:00-17:59; Friday 08:00-10:59 |

The Barber Shop closed-door event is an exceptional story scene. It is checked
on what would normally be Sergio's next open work visit, then presents the
closed-shop event instead of normal services.

## Target Linear Event Table

All probabilities are `1` once their stated conditions are satisfied. "Delay"
means minimum whole game days after the preceding successful thread event. A
stage does not advance when the player has not actually seen or completed its
required outcome.

| Stage | Event | Binding | Exact time | Delay | Success and next state |
| ---: | --- | --- | --- | ---: | --- |
| 0-5 | Existing drawings/Legare setup | Existing bindings | Existing verified hours | Existing | Preserve; stage 5 advances to 6 |
| 6 | Fiance at church | `Church / clara_paintings`, reached through `ChurchServiceLegare` | Sunday 08:00-09:29 | 0; the next Sunday is the natural gate | Play both fiance church images and advance to 7 |
| 7 | Witness fiance and Sergio on their secret date | `ArtisansQuarter / enter` | Monday, Wednesday, or Saturday 19:00-21:59 | 1 | Advance only after successful observation; leaving keeps stage 7 available |
| 8 | Sergio's door is closed | `BarberShop / enter` | Sergio's next normal work window | 1 | Replace normal shop scene/services with the closed-door scene; advance to 9 |
| 9 | Luisa reports the arrests and murder | `talk_luisa / clara_fiance_case` | Luisa's normal work window | 0; requires a later visit/action | Luisa gives the complete report; MC decides to visit Zimmer; advance to 10 |
| 10 | Deliver another barrel of wine to Zimmer | `talk_zimmer / clara_fiance_case` | Zimmer's reception window | 0; requires a later visit/action and at least one barrel in stock | Consume exactly one barrel from tavern stock and advance to 11; without wine, explain the requirement and do not advance |
| 11 | Zimmer advocacy and witness puzzle | `talk_zimmer / clara_fiance_case` | Same visit after delivery, or a later Zimmer reception after a wrong answer | 0 | Correct answer releases Clarissa and Sergio and advances to 12; wrong answer does not advance |
| 12 | Sergio's post-release follow-up | `talk_sergio / clara_fiance_case` | Sergio's next normal work window | 0; requires a later visit/action | Sergio gives the promised continuation, unlocks the ointment recipe and existing 25 percent discount, then advances to 13 |
| 13 | Clarissa asks to live at the tavern | `TavernMain / enter` | 18:00-21:59 | 1 | Clarissa is accepted into Melissa's room; her schedule changes by thread stage; advance to 14 |
| 14 | Clarissa's private anal confession | `TavernMelissaRoom / enter` | 20:00-22:59, with Clarissa and Melissa present | 1 | Clarissa explains her pain and allows treatment; advance to 15 |
| 15 | Apply Sergio's ointment | `TavernMelissaRoom / clara_ointment` | 20:00-22:59 | 0 | Requires and consumes one `special_cream_001`; unlocks consensual anal continuation and completes the thread |

The event tuple fields must remain in the documented fixed order:

```text
target, day, hour, delay, probability, requirements, conditions, item, location, action, priority
```

Do not encode the correlated Sergio work windows as the inaccurate generic
`(8, 10)` range. The room/NPC schedule is authoritative for stage 8 and 12.
Stage 7 is intentionally bound to the always-accessible Artisans Quarter because
the observed date occurs after the Barber Shop has closed.

Zimmer's wine requirement is not the earlier wine offered for the Mongol/night
guard operation and is not part of the five-barrel horse purchase. It is one
new delivery for this case. Stage 10 itself records that delivery: consuming
one barrel and advancing the thread to stage 11 is the complete state change.
Do not add a delivery boolean, a second wine counter, or infer delivery from a
later stock total.

## Event Definition Contract

The implementation replaces the current outer trigger rows 6 onward with the
following event shapes. Each outer list entry is one linear thread stage. A
nested list contains alternate exact-hour events for that same stage; it does
not create another thread or another state owner.

```renpy
# Stages 6-15 inside the existing claraPaintingsPath LThreadData trigger list.
(
    "story_clara_paintings_church_6",
    7, (8, 9), None, 1, None, None, None,
    "Church", "clara_paintings", 6,
),
(
    "story_clara_paintings_secret_date_7",
    [1, 3, 6], (19, 21), 1, 1, None, None, None,
    "ArtisansQuarter", "enter", 7,
),
[
    (
        "story_clara_paintings_barber_closed_8",
        [1, 3], (12, 17), 1, 1, None, None, None,
        "BarberShop", "enter", 8,
    ),
    (
        "story_clara_paintings_barber_closed_8",
        6, (8, 11), 1, 1, None, None, None,
        "BarberShop", "enter", 8,
    ),
],
(
    "story_clara_paintings_luisa_report_9",
    [1, 2, 3, 4, 6], (8, 18), None, 1, None, None, None,
    "talk_luisa", "clara_fiance_case", 9,
),
[
    # The success rows are preferred when a barrel is available.
    (
        "story_clara_paintings_zimmer_wine_10",
        2, (16, 17), None, 1, None,
        ["#int(player.tavern_management.winenum or 0) > 0"], None,
        "talk_zimmer", "clara_fiance_case", 10,
    ),
    (
        "story_clara_paintings_zimmer_wine_10",
        5, (8, 10), None, 1, None,
        ["#int(player.tavern_management.winenum or 0) > 0"], None,
        "talk_zimmer", "clara_fiance_case", 10,
    ),
    # These rows keep the case question visible and explain the missing wine.
    (
        "story_clara_paintings_zimmer_needs_wine_10",
        2, (16, 17), None, 1, None,
        ["#int(player.tavern_management.winenum or 0) <= 0"], None,
        "talk_zimmer", "clara_fiance_case", 20,
    ),
    (
        "story_clara_paintings_zimmer_needs_wine_10",
        5, (8, 10), None, 1, None,
        ["#int(player.tavern_management.winenum or 0) <= 0"], None,
        "talk_zimmer", "clara_fiance_case", 20,
    ),
],
[
    (
        "story_clara_paintings_zimmer_puzzle_11",
        2, (16, 17), None, 1, None, None, None,
        "talk_zimmer", "clara_fiance_case", 11,
    ),
    (
        "story_clara_paintings_zimmer_puzzle_11",
        5, (8, 10), None, 1, None, None, None,
        "talk_zimmer", "clara_fiance_case", 11,
    ),
],
[
    (
        "story_clara_paintings_sergio_followup_12",
        [1, 3], (12, 17), None, 1, None, None, None,
        "talk_sergio", "clara_fiance_case", 12,
    ),
    (
        "story_clara_paintings_sergio_followup_12",
        6, (8, 11), None, 1, None, None, None,
        "talk_sergio", "clara_fiance_case", 12,
    ),
],
(
    "story_clara_paintings_tavern_arrival_13",
    None, (18, 21), 1, 1, None, None, None,
    "TavernMain", "enter", 13,
),
(
    "story_clara_paintings_confession_14",
    None, (20, 22), 1, 1, None,
    [
        "#str(people.location('clara') or '') == 'TavernMelissaRoom'",
        "#str(people.location('melissa') or '') == 'TavernMelissaRoom'",
    ],
    None, "TavernMelissaRoom", "enter", 14,
),
(
    "story_clara_paintings_ointment_15",
    None, (20, 22), None, 1, None, None,
    "special_cream_001", "TavernMelissaRoom", "clara_ointment", 15,
),
```

The stage-10 no-wine target is a real authored event outcome, not a readiness
wrapper. It displays Zimmer's request, advances no thread state, and returns to
the active Zimmer conversation. The stage-10 wine target consumes one unit from
`player.tavern_management.winenum`, advances to stage 11, and may continue
directly to the stage-11 puzzle label during the same visit. If the answer is
wrong, stage 11 remains current and the puzzle is retried only through a later
valid Zimmer reception.

## Scene Beats And Text Contract

Every scene uses `main_ui`, `vscene`, story text beginning at the top of the
text field, and a native continuation/action menu. Each paragraph or visual beat
gets its own explicit `Продолжить` choice. No default room text or room action
appears until the event finishes.

### Stage 6: Church Fiance

Required visual order:

1. `images/Alber/church/cermon_fiance_clara.png`
2. `images/Alber/church/cermon_fiance1_clara.png`

Authored beats:

```text
У колонны рядом с семьёй Легаре сегодня стоит незнакомый молодой дворянин
из столицы. Он держится уверенно, словно место рядом с Клариссой уже принадлежит
ему, а сама девушка отвечает на его любезности с болезненно ровной улыбкой.

[Продолжить]

Легаре представляет гостя как человека из хорошего дома и будущего союзника
семьи. Кларисса не произносит слова «жених», но по её взгляду становится ясно:
столичный брак уже не слух и не далёкая угроза.

[Вернуться к прихожанам]
```

Finishing returns to the church attendee menu, not directly to another
location.

### Stage 7: Secret Date

The player observes Clarissa's fiance and Sergio together after the Barber Shop
has closed. The scene begins with:

```text
Уже после закрытия цирюльни вы замечаете знакомого столичного дворянина.
Оглядевшись, жених Клариссы стучит в боковую дверь. Серджио впускает его без
единого вопроса, и за ними сразу щёлкает засов.
```

Native choices:

```text
[Осторожно заглянуть внутрь]
[Не вмешиваться и уйти]
```

If an exploration requirement is retained, use the current
`player.stats.exploration >= 200` rule. On a successful observation:

```text
Через щель между ставней и рамой вы видите, что Серджио и столичный гость
говорят совсем не как мастер и клиент. Осторожные прикосновения быстро
становятся откровенными. Теперь вы точно знаете: будущий брак Клариссы
держится на лжи, которую можно обратить в её защиту.

[Продолжить]
```

Outcome rules:

- successful observation plays the whole scene and advances;
- insufficient exploration or choosing to leave costs the authored time but
  does not advance or invent a `seen` flag;
- a later valid evening can repeat the attempt.

No clearly named fiance/Sergio date image currently exists in the image tree.
Before implementation, inspect the complete image library once more. If no
matching existing asset is found, the missing visual is an explicit asset task;
do not silently substitute an unrelated portrait.

### Stage 8: Closed Barber Shop

Use the existing generic closed-vendor visual:

`images/general/closedVenue default.png`

During this event:

- Sergio is not shown in the visible-NPC panel;
- haircut, shop, appointment, and Sergio talk actions are unavailable;
- the text explains that the door is shut during his normally open hours;
- only the event continuation and then the normal return to Artisans Quarter
  are shown.

Authored text:

```text
Вы приходите к цирюльне в часы, когда Серджио обычно принимает посетителей,
но ставни закрыты, вывеска снята, а дверь заперта. Изнутри не доносится ни
голоса, ни звона инструментов. Соседние торговцы только переглядываются и
старательно делают вид, что ничего не знают.

[Вернуться в квартал ремесленников]
```

From the end of stage 8 until the successful Zimmer outcome, Sergio and
Clarissa are detained. Their normal schedules must project no playable presence.
Derive that from the current thread stage; do not store separate arrest flags.

### Stage 9: Luisa's Report

Luisa reports that Clarissa and Sergio have been arrested. Use separate
continuation beats:

```text
Луиза наклоняется через прилавок и понижает голос: «Слыхал про Клариссу Легаре
и цирюльника? Обоих взяли. Богатого Джеймса Леонарда, её столичного жениха,
нашли мёртвым у него дома».

[Продолжить]

«Утром его обнаружила прислуга: лежал бездыханный, без панталон, а в заднице —
огромная деревяшка. Теперь стража трясёт всех, кто с ним встречался. До Клариссы
и Серджио добрались первыми».

[Продолжить]

MC: И что теперь будет?

Луиза: А что теперь? Зная Циммера, он отправит обоих на герцогские галеры,
а то и хуже — продаст оркам в рабство.

[Продолжить]

Хм, интересно. Пожалуй, стоит навестить Циммера, узнать подробности и,
может быть, попытаться защитить Клариссу, как я и обещал.

[Вернуться к разговору с Луизой]
```

This event belongs to Luisa's talk interaction. It must return to the active
Luisa/Hunter Club context after completion; it must not navigate to City Guard
automatically.

### Stage 10: Zimmer's Additional Wine Delivery

Zimmer will not discuss the evidence until MC brings one additional barrel of
wine. This is a separate payment for the Clarissa/Sergio case.

No-wine event text:

```text
MC: Я хочу поговорить о Клариссе Легаре и Серджио.

Циммерман: «Таки хотите вмешаться в дело об убийстве богатого человека? Разговор
долгий, молодой человек, а от долгих разговоров у моих людей пересыхает горло.
Принесите ещё один бочонок вина — тогда и посмотрим, что можно сделать».

[Вернуться к разговору]
```

This target does not consume wine, does not advance the thread, and does not
penalize the player.

Wine-available event text and menu:

```text
MC: Я принёс ещё один бочонок вина. Теперь мы можем поговорить о Клариссе и
Серджио?

Циммерман: «Вот теперь разговор становится обстоятельным. Та бочка для ночной
стражи была за другое дело; эта — за время, которое я потрачу на ваше».

[Передать бочонок и продолжить]
[Оставить вино при себе и вернуться позже]
```

Only `Передать бочонок и продолжить` performs:

```renpy
$ player.tavern_management.winenum -= 1
$ event_runtime.active_thread.advance()
jump story_clara_paintings_zimmer_puzzle_11
```

The second choice leaves stage 10 active. Never subtract wine on scene entry,
and never consume another barrel when retrying the puzzle at stage 11.

### Stage 11: Zimmer's Case And Puzzle

The player first advocates for Clarissa. Zimmer then recounts the witness
statements while he and MC drink wine. Use the existing Zimmer visual set where
it matches the beats:

1. `images/zimmer/talk.png`
2. `images/zimmer/thank.png` for the successful conclusion

Opening exchange:

```text
MC: Кларисса и Серджио могли скрывать свои отношения, но это ещё не делает их
убийцами. Я обещал Клариссе защиту и хочу услышать, на чём держится обвинение.

Циммерман: «Таки защиту обещали? Хорошо. Тогда слушайте показания и скажите мне,
кто из свидетелей врёт. Если увидите то, что проглядели мои люди, я пересмотрю
дело».

[Выслушать показания]
```

Puzzle text:

```text
Богатого Джеймса Леонарда убили в воскресенье днём. В доме были
горничная, повар, дворецкий, садовник и жена.

- Горничная: накрывала на стол.
- Повар: готовил завтрак.
- Дворецкий: полировал серебро и посуду.
- Садовник: сажал семена томатов.
- Жена: читала книгу.

Кто это сделал?
```

The native menu offers all five suspects:

```text
[Горничная]
[Повар]
[Дворецкий]
[Садовник]
[Жена]
[Вернуться к вопросу позже]
```

The correct answer is `Повар`, because breakfast is not prepared after midday.

Correct-answer exchange:

```text
MC: Повар. Леонарда убили в воскресенье днём, а повар утверждает, что готовил
завтрак. После полудня завтрак уже не готовят.

Циммерман некоторое время молчит, затем усмехается: «Таки верно. Показание
слишком старательное и совершенно не подходит ко времени смерти. Я прикажу
допросить повара заново, а Клариссу и Серджио выпустить».

[Продолжить]
```

Wrong-answer exchange:

```text
Циммерман качает головой: «Нет, молодой человек. В этом показании нет
противоречия со временем убийства. Подумайте ещё и приходите в другой приёмный
час».

[Вернуться в караулку]
```

- Correct answer: Zimmer accepts the contradiction, releases Clarissa and
  Sergio, and advances the thread.
- Wrong answer: Zimmer rejects the reasoning, marks the current conversation as
  used, returns to City Guard, and leaves stage 11 active for a later reception.
  Do not implement a recursive riddle menu.

The room returns to its own picture, text, and actions after the event.

### Stage 12: Sergio's Follow-up

The ointment recipe and barber discount are consequences of speaking to Sergio
after his release, not immediate rewards from Zimmer.

- set `crafting.special_cream_recipe_unlocked = True` once;
- set `tractir_progress.sergio_discount_percent` to at least `25`, without
  reducing a higher existing value;
- do not add mirrored recipe/discount fields to Sergio or Clarissa;
- return to Sergio's talk menu after the scene.

Authored beats:

```text
Серджио встречает вас без привычной салонной улыбки. «Мне сказали, кто заметил
ложь в показаниях. Без вас нас с Клариссой уже везли бы на галеры».

[Продолжить]

«Если после всего этого понадобится средство от трещин, ушибов и самых
деликатных повреждений, запишите рецепт. А в моей цирюльне отныне платите на
четверть меньше».

[Записать рецепт и вернуться к разговору]
```

### Stage 13: Clarissa Moves Into The Tavern

```text
Вечером Кларисса появляется в общем зале с небольшим узлом вещей. Вся прежняя
уверенность исчезает, когда она просит выполнить обещание и позволить ей
остаться под вашей защитой.

[Продолжить]

Кларисса: «К Легаре я не вернусь. После ареста в городе мне тоже небезопасно.
Если вы не передумали, разрешите пожить здесь. Я могу делить комнату с
Мелиссой и помогать трактиру».

[Позволить Клариссе поселиться у Мелиссы]
[Попросить её вернуться к разговору позже]
```

Acceptance advances the thread. Deferral does not abort it and does not create
a residence flag.

### Stage 14: Clarissa's Confession

```text
Поздним вечером Кларисса просит поговорить без посторонних. После истории с
женихом она всё ещё испытывает боль и наконец признаётся, что унижения и
насилие оставили повреждение, которое само не проходит.

[Продолжить]

Кларисса: «Серджио говорил о специальной мази. Мне стыдно просить, но если вы
сумеете её приготовить, я позволю вам помочь. Только без шуток и без спешки».

[Обещать принести мазь]
```

### Stage 15: Treatment

```text
Вы показываете Клариссе приготовленную мазь. Она убеждается, что дверь закрыта,
и ещё раз просит действовать осторожно.

[Помочь Клариссе]
[Убрать мазь и вернуться позже]
```

Only the first choice consumes one `special_cream_001`. After treatment:

```text
Когда всё закончено, Кларисса с заметным облегчением приводит одежду в порядок.
«Спасибо. Теперь я хотя бы не буду вспоминать о нём при каждом движении. Если
когда-нибудь между нами случится что-то ещё, это будет потому, что я сама так
решила».

[Продолжить]
```

### Residence And Care State Rules

Clarissa asks for protection and a place to live. Once accepted, her schedule
places her in `TavernMelissaRoom` outside other authored duties. The schedule
condition derives from `claraPaintingsPath.num >= 14` or completion; no separate
`lives_at_tavern` flag is needed.

The confession and treatment are separate beats so the player can learn what is
needed before crafting the ointment. Treatment consumes exactly one
`special_cream_001`. Completion unlocks the availability condition for
Clarissa's consensual anal options in the shared sex engine; it does not create
a second sex implementation.

## Post-Resolution Threads

These are distinct continuations because they can progress independently after
the fiance case. Their whole-thread condition is
`threads["claraPaintingsPath"].completed` plus any real participant/stat gates.

### `claraLegareRevenge`

Linear story thread for Clarissa and MC acting against Alber Legare. The exact
revenge scenes and outcomes still require authored event detail. Do not infer or
implement them from the title alone.

### Clarissa Anal Relationship

This is an unlock for the existing shared sex engine, not a duplicate thread or
new engine. Availability requires:

- the ointment-treatment event completed;
- Clarissa at the current location and not busy;
- daily sex capacity available;
- the normal Clarissa relationship/corruption/consent thresholds.

All results use Clarissa's existing sex counters and pregnancy-capable shared
mechanics where applicable.

### `claraTavernEducation`

Linear teaching thread with at least two authored phases:

1. Clarissa teaches the tavern girls to play cards in the Wine Store basement.
2. Clarissa teaches noble manners at the tavern.

The card lesson is a scheduled multi-NPC event, not a permanent schedule
rewrite. Its exact appointment must be selected from the intersection of every
participant's hourly schedule; if held after the Wine Store's normal hours, the
event temporarily owns access and visuals for that scene only.

The manners lessons increase one tavern-owned integer progression value (for
example `player.tavern_management.noble_patronage_level`). Client generation
reads that one value to add more noble guests. Do not maintain a second
`Clara.nobles_unlocked` flag.

Exact participants, lesson count, stat deltas, and appointment hours remain
authoring decisions and must be confirmed before implementation. They are not
silently invented by this plan.

## Save Migration

Changing the meaning and length of an existing saved linear thread requires one
explicit versioned migration. It must preserve relationship, recipe, discount,
inventory, and completed earlier scenes.

Proposed conservative mapping from the current draft:

| Old state | New state |
| --- | --- |
| `num <= 6` | keep the same stage |
| `num 7-10` | map to stage 7 so the corrected secret-date scene cannot be skipped |
| `num 11-12` | map to stage 8; the date was witnessed, but the arrest sequence still needs to play |
| old thread completed | map to stage 13 if recipe/discount already exist; preserve those rewards and continue with Clarissa's move-in |

After migration:

- remove `Clara.commission_followup_day` and `Clara.murder_day` from live
  defaults and saved state;
- use the thread's own `day` plus event `delay` fields for pacing;
- do not keep compatibility mirrors after the one-time migration;
- do not duplicate already-owned items or consume existing ointment.

## Implementation Order

1. Replace event tuples for stages 6 onward and add the correct room/NPC trigger
   calls only where the binding does not already exist.
2. Rewrite the existing stage labels in place, preserving stages 0-5.
3. Project detention and post-release residence from the thread stage into the
   existing schedules.
4. Add Zimmer's one-barrel delivery as stage 10, consuming only
   `player.tavern_management.winenum` and recording it only through advancement
   to stage 11.
5. Move recipe/discount consequences from Zimmer to Sergio's follow-up.
6. Add the versioned save migration and remove obsolete day-marker fields.
7. Add post-resolution thread definitions only after their exact authored
   scenes are specified.

## Verification Matrix

- Start from a save immediately after stage 5 and confirm the fiance scene is
  available only through the Sunday service attendee menu.
- Confirm both church images appear in order and each beat has `Продолжить`.
- Confirm leaving or failing the secret observation does not advance stage 7.
- Confirm the secret date cannot appear during arbitrary descriptive time slots.
- Confirm the next valid Sergio work visit shows the closed-vendor scene and no
  services/NPC button.
- Confirm detained Clarissa and Sergio do not appear through normal schedules.
- Confirm Luisa tells the murder story only at her valid work hours and returns
  to her talk context.
- Confirm Zimmer is available only during the exact reception windows.
- Confirm stage 10 explains the additional-wine requirement without hiding the
  case action when stock is empty.
- Confirm declining delivery changes nothing, while accepting subtracts exactly
  one from `player.tavern_management.winenum` and advances to stage 11.
- Confirm the earlier Mongol/night-guard delivery and Zimmer's five-barrel horse
  purchase do not satisfy or skip this story stage.
- Confirm wrong puzzle answers do not consume any further wine.
- Confirm every wrong suspect leaves the puzzle unresolved for a later visit.
- Confirm `Повар` releases both detainees.
- Confirm Sergio's next visit, not Zimmer, unlocks the recipe and 25 percent
  discount.
- Confirm Clarissa moves into Melissa's room only after release.
- Confirm the confession appears before the ointment action.
- Confirm treatment consumes one ointment and unlocks the shared anal options.
- Confirm no default room description/navigation overlays any active event.
- Confirm no new global/mirror flags or duplicate thread/sex-engine paths exist.
- Run focused source tests, external click paths, Ren'Py compile, Ren'Py lint,
  residual ownership scans, and save-load checks before committing gameplay
  implementation.
