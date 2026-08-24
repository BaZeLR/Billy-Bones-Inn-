# Thread Event Initialization Reference

This is a reference for defining story threads in `game/Utilities/General/Classes/StoryEventRuntime.rpy`.

The runtime board should show current thread/event status. This document is the CSV-style planning table for defining and reviewing event tuples before adding them to `LThreadData`, `RThreadData`, or `UThreadData`.

## Event Tuple Columns

```text
npc,thread_constructor,thread_level,thread_subname,thread_condition,target_label,day,hour,delay,probability,requirements,conditions,item,location,action,priority
```

Maps to:

```renpy
LThreadData(thread_level, npc, thread_subname, thread_condition, [
    (
        target_label,
        day,
        hour,
        delay,
        probability,
        requirements,
        conditions,
        item,
        location,
        action,
        priority,
    ),
], highlight=False, threaded=True)
```

## Column Meanings

```text
npc                Person/story owner shown on the board, for example melissa or clara.
thread_constructor LThreadData for ordered story, RThreadData for random ordered pool, UThreadData for unordered.
thread_level       Required relationship/story level.
thread_subname     Thread suffix; full runtime key is npc + thread_subname.
thread_condition   Whole-thread condition. Use None unless the entire thread is locked.
target_label       Label called/jumped when the event fires.
day                Weekday condition. None means any day.
hour               Time-slot condition. None means any time.
delay              Day delay condition after thread activation or marker.
probability        Event chance. Use 1 for guaranteed.
requirements       Stat requirements dict, for example {"charisma": 70}.
conditions         Explicit condition list. Prefer visible flag expressions.
item               Required item id, or None.
location           Room/location event key.
action             Action/event key, for example enter, room_search, clara_talk.
priority           Lower priority wins when several events share location/action.
```

## Condition Checking

Condition checking is implemented by the `Event` class, not by each tuple as a separate method attribute.

The tuple stores raw condition data in:

```renpy
self.condStr = evt[6]
```

During runtime initialization:

```renpy
evt.initConditions()
```

converts `condStr` into:

```renpy
self.conds
```

Then the class method:

```renpy
Event.checkConditions()
```

returns:

```renpy
_story_conditions_met(self.conds)
```

The full event gate is:

```renpy
Event.canTrigger()
```

which checks day, hour, conditions, delay, requirements, probability, and whether the location is open.

## Example Rows

```csv
npc,thread_constructor,thread_level,thread_subname,thread_condition,target_label,day,hour,delay,probability,requirements,conditions,item,location,action,priority
melissa,LThreadData,0,RatProblem,None,story_melissa_storage_rat_0,None,None,None,1,None,"CurLoc == TavernStorage; storage_rat_cleared == 0; melissa_storage_rat not seen today",None,TavernStorage,enter,0
melissa,LThreadData,0,WerecatProblem,melissaRatProblem_0,story_melissa_werecat_rumor_0,None,None,None,1,None,"rats_problem_active == 1; storage_rat_cleared == 1; adopted == 0; sold == 0",None,HunterClub,overheard,0
melissa,LThreadData,0,BatProblem,melissaRatProblem_0,story_melissa_bat_problem_5,None,None,None,1,None,"thread.num == 6; temp_room == TavernAmandaRoom; drawings_found == 0; current_game_day() >= drawings_ready_day",None,TavernMelissaRoom,room_search,5
clara,LThreadData,0,BookletMarket,None,story_clara_market_booklet_0,None,None,None,1,None,"CurLoc == MarketPlace; week in 1..6; time == 2; market day roll active; booklet_market_seen == 0",None,MarketPlace,enter,0
clara,LThreadData,1,PaintingsPath,None,story_clara_paintings_melissa_0,None,None,None,1,None,"drawings_found == 1; paintings_melissa_asked == 0",None,talk_melissa,clara_paintings,0
```
