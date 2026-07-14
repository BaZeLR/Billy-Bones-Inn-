# Tavern Home Mana Events Sketch

Purpose: sketch a tavern-home random event group where the average mana of eligible adult tavern workers changes which kind of home event is likely to appear.

This is a design sketch, not runtime code. It follows the current event framework:

- event rows define availability;
- readiness helpers only check conditions and probability gates;
- story labels own text, pictures, menus, consequences, time cost, and return flow;
- `current_action_items` is not used for authored event choices.

## Concept

Eligible workers:

```renpy
define TAVERN_HOME_MANA_WORKERS = ("sandra", "melissa", "liza", "georgett")
```

Average mana:

```text
avg_mana = average(worker.mana) / 100.0
good_weight = avg_mana
bad_weight = 1.0 - avg_mana
```

High average mana means cooperative, erotic, loyal, and playful events become more likely. Low average mana means jealousy, fights, pranks, sabotage, and punishment scenes become more likely.

Sandra is special:

- when stable/high mana, she punishes disorder and rewards cooperation;
- when corrupted/high openness, she can be seduced into joining the event;
- when low mana, she can overreact or become the target of a prank.

## Readiness Helpers

These helpers belong near tavern/system readiness code, not inside screens.

```renpy
init python:
    def tavern_home_worker_info(worker_id=""):
        return getPersonInfo(str(worker_id or "").strip())

    def tavern_home_worker_mana(worker_id=""):
        info = tavern_home_worker_info(worker_id)
        if info is None:
            return None
        return max(0, min(100, int(getattr(info, "mana", 0) or 0)))

    def tavern_home_average_mana():
        values = []
        for worker_id in TAVERN_HOME_MANA_WORKERS:
            value = tavern_home_worker_mana(worker_id)
            if value is not None:
                values.append(value)
        if not values:
            return 0.0
        return float(sum(values)) / float(len(values))

    def tavern_home_workers_present(worker_ids=()):
        for worker_id in tuple(worker_ids or ()):
            if str(getLocation(worker_id) or "") != str(CurLoc or ""):
                return False
        return True

    def tavern_home_mana_event_base_ready():
        calendar_v2.sync_state()
        if str(CurLoc or "") not in ("TavernMain", "TavernKitchen", "Backyard", "TavernUpstairs"):
            return False
        if int(calendar_v2.hour or 0) < 18:
            return False
        if int(TavernHomeManaEventsToday or 0) > 0:
            return False
        return True

    def tavern_home_clarissa_secret_known():
        return (
            int(Clara.var.get("anal_unlocked", 0) or 0) == 1
            or int(Clara.var.get("sex_engine_unlocked", 0) or 0) == 1
            or int(Clara.var.get("drawings_secret_known", 0) or 0) == 1
        )

    def tavern_home_good_gate(event_key="", multiplier=1.0):
        chance = max(0.0, min(1.0, (tavern_home_average_mana() / 100.0) * float(multiplier or 1.0)))
        roll_key = "tavern_home_mana_good:%s:%s" % (str(event_key or ""), current_game_day())
        return procedural_random(roll_key) < chance

    def tavern_home_bad_gate(event_key="", multiplier=1.0):
        chance = max(0.0, min(1.0, (1.0 - (tavern_home_average_mana() / 100.0)) * float(multiplier or 1.0)))
        roll_key = "tavern_home_mana_bad:%s:%s" % (str(event_key or ""), current_game_day())
        return procedural_random(roll_key) < chance
```

`Event.prob` stays `1` because the current runtime probability field is a static float. Dynamic mana probability is represented as a condition helper.

## Strict Event Definitions

Add this to `tavernThreadList` in `StoryEventRuntime.rpy` when implementing.

```renpy
RThreadData(0, "tavern", "HomeManaEvents", None, [1, [
    # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
    (
        "TavernHomeManaGoodCooperation", None, [18, 19, 20, 21, 22], None,
        1,
        None,
        [
            "#tavern_home_mana_event_base_ready()",
            "#tavern_home_good_gate('cooperation', 0.45)",
            "#tavern_home_workers_present(('sandra', 'melissa'))",
        ],
        None,
        "TavernMain",
        "enter",
        300,
    ),
    (
        "TavernHomeManaGoodSeduction", None, [20, 21, 22, 23], None,
        1,
        None,
        [
            "#tavern_home_mana_event_base_ready()",
            "#tavern_home_good_gate('seduction', 0.35)",
            "#tavern_home_workers_present(('liza', 'georgett'))",
        ],
        None,
        "TavernMain",
        "enter",
        310,
    ),
    (
        "TavernHomeManaGoodSandraTurned", None, [21, 22, 23], None,
        1,
        None,
        [
            "#tavern_home_mana_event_base_ready()",
            "#tavern_home_good_gate('sandra_turned', 0.25)",
            "#tavern_home_workers_present(('sandra', 'melissa', 'liza'))",
            "#int(Sandra.corruption or 0) >= 35",
        ],
        None,
        "TavernMain",
        "enter",
        320,
    ),
    (
        "TavernHomeManaGoodMelissaClarissaHelp", None, [21, 22, 23], None,
        1,
        None,
        [
            "#tavern_home_mana_event_base_ready()",
            "#tavern_home_good_gate('melissa_clarissa_help', 0.25)",
            "#tavern_home_workers_present(('melissa',))",
            "#str(getLocation('clara') or '') == str(CurLoc or '')",
            "#tavern_home_clarissa_secret_known()",
        ],
        None,
        "TavernMain",
        "enter",
        325,
    ),
    (
        "TavernHomeManaBadJealousy", None, [18, 19, 20, 21, 22], None,
        1,
        None,
        [
            "#tavern_home_mana_event_base_ready()",
            "#tavern_home_bad_gate('jealousy', 0.45)",
            "#tavern_home_workers_present(('melissa', 'liza'))",
        ],
        None,
        "TavernMain",
        "enter",
        330,
    ),
    (
        "TavernHomeManaBadPrankPunishment", None, [19, 20, 21, 22], None,
        1,
        None,
        [
            "#tavern_home_mana_event_base_ready()",
            "#tavern_home_bad_gate('prank_punishment', 0.40)",
            "#tavern_home_workers_present(('sandra', 'georgett'))",
        ],
        None,
        "TavernMain",
        "enter",
        340,
    ),
]], highlight=False, threaded=False)
```

Implementation note: if these events should also fire from `TavernKitchen`, `Backyard`, or `TavernUpstairs`, add the same rows for those exact locations. The current event binding is location/action based; do not change `RoomTemplate` to accept location groups for this.

## Label 1: Good Cooperation

Picture:

```text
images/tavern/home_events/mana_good_cooperation.webp
```

Visual: Sandra and Melissa closing the tavern together. The room is warm, tables are cleaned, candles are low, and both women look tired but pleased.

```renpy
label TavernHomeManaGoodCooperation:
    show screen main_ui
    $ TavernHomeManaEventsToday += 1
    $ _picture = "images/tavern/home_events/mana_good_cooperation.webp"
    $ scene_image = _picture
    call ShowImage("", "", _picture)

    "The common room is almost empty. Sandra is counting coins behind the bar while Melissa wipes the last table."
    "\"We finished early,\" Melissa says, unable to hide her smile. \"Nobody shouted, nobody broke a mug, and the stew did not poison anyone.\""
    "\"Do not tempt fate,\" Sandra says, but there is warmth in her voice. \"Still... she is right. Tonight went well.\""

    menu:
        "Praise both of them":
            "You tell them the tavern felt like a real household tonight, not a battlefield."
            "\"Then say it more often,\" Sandra replies. \"Some of us work better when we are not only corrected.\""
            $ Sandra.change_social(friend_delta=1, open_delta=1)
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(15)

        "Invite them to stay a little longer":
            "Melissa glances at Sandra, waiting for the older woman to object."
            "\"Fifteen minutes,\" Sandra says. \"No more. And nobody knocks over my clean glasses.\""
            "They sit with you by the dying fire. The conversation grows softer, almost private."
            $ Sandra.change_social(friend_delta=1, open_delta=1)
            $ Melissa.change_social(friend_delta=1, open_delta=2)
            $ calendar_v2.advance_minutes(25)

    jump expression str(CurLoc or "TavernMain")
```

## Label 2: Good Seduction

Picture:

```text
images/tavern/home_events/mana_good_seduction.webp
```

Visual: Liza and Georgette near the stairwell after closing, dressed for work but clearly performing for MC, competing without hostility.

```renpy
label TavernHomeManaGoodSeduction:
    show screen main_ui
    $ TavernHomeManaEventsToday += 1
    $ _picture = "images/tavern/home_events/mana_good_seduction.webp"
    $ scene_image = _picture
    call ShowImage("", "", _picture)

    "Liza blocks your way near the stairs with a tray balanced on one hand. Georgette leans against the wall beside her, amused."
    "\"We made a bet,\" Liza says. \"Which of us you would notice first after closing.\""
    "\"She cheated,\" Georgette says. \"She stood in the doorway.\""
    "\"That is called strategy.\""

    menu:
        "Let them compete":
            "You ask what the winner gets."
            "\"Your attention,\" Liza says."
            "\"And the loser gets to watch and learn,\" Georgette adds."
            "The game stays playful, but both of them leave convinced they gained ground."
            $ Liza.change_social(friend_delta=1, open_delta=1)
            $ Georgett.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(20)

        "Refuse to choose":
            "You tell them the tavern works better when they cooperate."
            "\"That sounds very responsible,\" Georgette says."
            "\"And very boring,\" Liza adds, though she is smiling."
            $ Liza.change_social(friend_delta=0, open_delta=1)
            $ Georgett.change_social(friend_delta=0, open_delta=1)
            $ calendar_v2.advance_minutes(10)

    jump expression str(CurLoc or "TavernMain")
```

## Label 3: Good Sandra Turned

Picture:

```text
images/tavern/home_events/mana_good_sandra_turned.webp
```

Visual: Sandra beginning a stern lecture while Melissa and Liza quietly turn the situation into flirtation. Sandra is still in control, but she is enjoying it more than she admits.

```renpy
label TavernHomeManaGoodSandraTurned:
    show screen main_ui
    $ TavernHomeManaEventsToday += 1
    $ _picture = "images/tavern/home_events/mana_good_sandra_turned.webp"
    $ scene_image = _picture
    call ShowImage("", "", _picture)

    "Sandra catches Melissa and Liza whispering by the bar and folds her arms."
    "\"If you two have energy left for gossip, you have energy left for work.\""
    "\"We were discussing work,\" Melissa says."
    "\"Your work,\" Liza adds. \"How hard you make it look when you command everyone.\""
    "Sandra opens her mouth to scold them, then notices you watching."

    menu:
        "Let Sandra punish them":
            "\"Good,\" Sandra says. \"Then they can polish every cup until they understand discipline.\""
            "Melissa groans. Liza protests. Sandra looks satisfied."
            $ Sandra.change_social(friend_delta=1, open_delta=0)
            $ Melissa.change_social(friend_delta=0, open_delta=-1)
            $ Liza.change_social(friend_delta=0, open_delta=-1)
            $ calendar_v2.advance_minutes(20)

        "Tell Sandra they are praising her":
            "\"Were they?\" Sandra asks, trying to remain severe."
            "\"Of course,\" Liza says quickly. \"We were admiring your authority.\""
            "Melissa nods too eagerly. Sandra sees through it, but the corner of her mouth softens."
            $ Sandra.change_social(friend_delta=1, open_delta=1)
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ Liza.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(25)

    jump expression str(CurLoc or "TavernMain")
```

## Label 4: Melissa And Clarissa Help

Picture:

```text
images/tavern/home_events/mana_good_melissa_clarissa_help.webp
```

Visual: Melissa sitting on the edge of a tavern bed or bench, nervous but curious. Clarissa stands nearby with calm confidence, not mocking her. MC is present as the person Melissa asked for help.

```renpy
label TavernHomeManaGoodMelissaClarissaHelp:
    show screen main_ui
    $ TavernHomeManaEventsToday += 1
    $ _picture = "images/tavern/home_events/mana_good_melissa_clarissa_help.webp"
    $ scene_image = _picture
    call ShowImage("", "", _picture)

    "Melissa waits until the tavern quiets down before catching your sleeve."
    "\"I need to ask something stupid,\" she says, then immediately shakes her head. \"No, not stupid. Just... frightening.\""
    "Clarissa is by the window, quiet enough that Melissa clearly invited her on purpose."
    "\"I am still a virgin,\" Melissa says. \"That part of me is not ready. But Clarissa said the backdoor can be good if it is done carefully.\""
    "\"I said it can be good when nobody is rushed,\" Clarissa corrects her. \"And when the girl trusts the hands on her.\""
    "Melissa looks at you, embarrassed but steady."
    "\"I want to try. I am just afraid I will panic and ruin everything.\""

    menu:
        "Tell Melissa there is no hurry":
            "You tell her that fear is enough reason to stop for tonight."
            "Melissa exhales, half relieved and half disappointed."
            "\"Thank you. I wanted you to want me, but I also wanted you to say that.\""
            "Clarissa gives her a small approving nod."
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ Clara.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(15)
            jump expression str(CurLoc or "TavernMain")

        "Ask Clarissa to guide her":
            "\"Only if Melissa keeps deciding,\" Clarissa says."
            "\"I decide,\" Melissa answers quickly. \"But I want her there. She knows how to make it less frightening.\""
            "Clarissa moves closer and speaks to Melissa first, not to you."
            "\"Then we start with kissing, breathing, and stopping whenever you say stop.\""
            $ Melissa.change_social(friend_delta=1, open_delta=2)
            $ Clara.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(20)
            jump TavernHomeMelissaClarissaAnalTrio

        "Ask if this is really Melissa's wish":
            "Melissa blushes, but she does not look away."
            "\"Yes. Clarissa made me curious, but I came to you myself.\""
            "\"That is the important part,\" Clarissa says. \"Curiosity is not permission. Asking is.\""
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ Clara.change_social(friend_delta=0, open_delta=1)
            $ calendar_v2.advance_minutes(10)
            jump expression str(CurLoc or "TavernMain")


label TavernHomeMelissaClarissaAnalTrio:
    show screen main_ui
    $ _picture = "images/tavern/home_events/mana_good_melissa_clarissa_trio.webp"
    $ scene_image = _picture
    call ShowImage("", "", _picture)

    "Clarissa keeps the pace slow. Melissa follows her breathing first, then her hands."
    "\"If I say wait, you wait,\" Melissa says."
    "\"Immediately,\" you answer."
    "The scene moves from nervous laughter to careful intimacy: kisses, guiding hands, and oral teasing before Melissa finally relaxes enough to continue."
    "Clarissa stays close, helping Melissa read what feels good and what is too much."

    menu:
        "Continue only while Melissa asks for it":
            "Melissa's fear does not vanish, but it stops ruling the room."
            "\"I thought I would feel foolish,\" she whispers afterward. \"I do not.\""
            "Clarissa smiles. \"Then it was done properly.\""
            $ Melissa.var["anal_first_try_done"] = 1
            $ Melissa.change_social(friend_delta=2, open_delta=2, corruption_delta=1)
            $ Clara.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(45)

        "Stop after the teasing":
            "You stop before Melissa has to ask."
            "She looks surprised, then grateful."
            "\"Next time,\" she says, quieter now. \"I think there can be a next time.\""
            $ Melissa.var["anal_first_try_pending"] = 1
            $ Melissa.change_social(friend_delta=1, open_delta=2)
            $ Clara.change_social(friend_delta=1, open_delta=0)
            $ calendar_v2.advance_minutes(30)

    jump expression str(CurLoc or "TavernMain")
```

## Label 5: Bad Jealousy

Picture:

```text
images/tavern/home_events/mana_bad_jealousy.webp
```

Visual: Melissa and Liza arguing in the kitchen or near the bar. A cup is spilled, one chair is pushed aside, and the room feels tense.

```renpy
label TavernHomeManaBadJealousy:
    show screen main_ui
    $ TavernHomeManaEventsToday += 1
    $ _picture = "images/tavern/home_events/mana_bad_jealousy.webp"
    $ scene_image = _picture
    call ShowImage("", "", _picture)

    "You hear a sharp crack from the common room. A wooden cup rolls across the floor."
    "\"You did that on purpose,\" Melissa snaps."
    "\"I walked past you,\" Liza says. \"If that is enough to ruin your evening, maybe stand farther from me.\""
    "\"Maybe stop smiling at everyone who looks useful.\""

    menu:
        "Separate them":
            "You send Melissa to the kitchen and Liza to the stairs before the argument can turn worse."
            "\"Fine,\" Melissa says. \"But I am not cleaning her mess.\""
            "\"It was your cup,\" Liza calls after her."
            $ Melissa.change_social(friend_delta=0, open_delta=-1)
            $ Liza.change_social(friend_delta=0, open_delta=-1)
            $ calendar_v2.advance_minutes(15)

        "Call Sandra":
            "Sandra arrives with one look that silences both of them."
            "\"If you want to behave like children, I can assign chores like children.\""
            "Neither woman argues after that."
            $ Sandra.change_social(friend_delta=1, open_delta=0)
            $ Melissa.change_social(friend_delta=0, open_delta=-1)
            $ Liza.change_social(friend_delta=0, open_delta=-1)
            $ calendar_v2.advance_minutes(20)

        "Let them settle it":
            "You wait. The argument burns hot, then drops into cold silence."
            "Nothing breaks, but the tavern feels smaller afterward."
            $ Melissa.change_anger(1, "tavern_home_jealousy")
            $ Liza.change_anger(1, "tavern_home_jealousy")
            $ calendar_v2.advance_minutes(10)

    jump expression str(CurLoc or "TavernMain")
```

## Label 6: Bad Prank And Punishment

Picture:

```text
images/tavern/home_events/mana_bad_prank_punishment.webp
```

Visual: Sandra caught in the aftermath of a prank. Georgette is trying not to laugh; Sandra is furious or dangerously calm.

```renpy
label TavernHomeManaBadPrankPunishment:
    show screen main_ui
    $ TavernHomeManaEventsToday += 1
    $ _picture = "images/tavern/home_events/mana_bad_prank_punishment.webp"
    $ scene_image = _picture
    call ShowImage("", "", _picture)

    "Sandra stands in the middle of the room, one hand wet with spilled beer. Georgette is beside the barrel, failing to look innocent."
    "\"It was supposed to splash the next drunk who leaned on it,\" Georgette says."
    "\"It splashed me.\" Sandra's voice is quiet enough to be worse than shouting."
    "\"That was not the plan.\""

    menu:
        "Let Sandra punish her":
            "\"Storage room,\" Sandra says. \"Every bottle checked. Every shelf wiped. Tonight.\""
            "Georgette looks to you for rescue, then thinks better of it."
            $ Sandra.change_social(friend_delta=1, open_delta=0)
            $ Georgett.change_social(friend_delta=0, open_delta=-1)
            $ calendar_v2.advance_minutes(25)

        "Make Georgette apologize":
            "You tell Georgette to stop hiding behind jokes."
            "\"Fine,\" she says, then turns to Sandra. \"I am sorry. Truly. I aimed for someone less terrifying.\""
            "Sandra almost smiles. Almost."
            $ Sandra.change_social(friend_delta=1, open_delta=1)
            $ Georgett.change_social(friend_delta=1, open_delta=0)
            $ calendar_v2.advance_minutes(15)

        "Turn it into a lesson for Sandra":
            "You point out that nobody plays pranks when the house feels calm."
            "Sandra looks at Georgette, then at the tired room around her."
            "\"Maybe,\" she says. \"But she still cleans the barrel.\""
            $ Sandra.change_social(friend_delta=0, open_delta=1)
            $ Georgett.change_social(friend_delta=0, open_delta=1)
            $ calendar_v2.advance_minutes(20)

    jump expression str(CurLoc or "TavernMain")
```

## Implementation Notes

- Add `default TavernHomeManaEventsToday = 0` and reset it in daily reset/new day code.
- Use existing NPC objects for state changes. Do not create parallel mana dicts.
- Use `calendar_v2.advance_minutes(...)` for time cost.
- Use image paths under `images/tavern/home_events/`.
- Keep the event labels in a tavern/home event file, for example `game/Inn/TavernHomeManaEvents.rpy`.
- If later a specific girl gets a personal continuation from one of these events, put that continuation in her own event file and connect it with a thread row.
