# Location Args Map

Total locations: **224**

This document maps args both programmatically (exact indexes/usages) and descriptionally (human summary).

## $menu_f
- TXT: `game/Inn/$menu_f.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `menu_f(args=0)` in `game/Inn/menu_f.rpy:1`
- RPY arg usage lines:
  - none

## AddCleanScreen
- TXT: `game/Inn/AddCleanScreen.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AddCleanScreen(no params)` in `game/Inn/RuntimeCompat.rpy:43`
  - `add_clean_screen(no params)` in `game/Inn/RuntimeCompat.rpy:48`
- RPY arg usage lines:
  - none

## AddCleanScreenButton
- TXT: `game/Inn/AddCleanScreenButton.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AddCleanScreenButton(no params)` in `game/Inn/RuntimeCompat.rpy:53`
- RPY arg usage lines:
  - none

## AddOthersSperm
- TXT: `game/Inn/AddOthersSperm.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameCOSP (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameCOSP` from `$GirlNameCOSP=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AddOthersSperm(girl_name="", chance=1)` in `game/Inn/RuntimeCompat.rpy:65`
- RPY arg usage lines:
  - none

## AdjustOtkroven
- TXT: `game/Inn/AdjustOtkroven.txt`
- RPY: `game/Inn/AdjustOtkroven.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameAOtk (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameAOtk` from `$GirlNameAOtk=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## AdvanceTime
- TXT: `game/Inn/AdvanceTime.txt`
- RPY: `game/Inn/AdvanceTime.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $retlocname (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $retlocname` from `$retlocname=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AdvanceTime(return_location=None)` in `game/Inn/AdvanceTime.rpy:3`
- RPY arg usage lines:
  - none

## AfterDanceLegare
- TXT: `game/Inn/AfterDanceLegare.txt`
- RPY: `game/Inn/AfterDanceLegare.rpy`
- Arg indexes used: `[0]`
- Description: outgoing: AfterDanceLegare('Fight') @L65; AfterDanceLegare('Police') @L70
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - `AfterDanceLegare` L65: `gt 'AfterDanceLegare', 'Fight'`
  - `AfterDanceLegare` L70: `gt 'AfterDanceLegare', 'Police'`
- Outgoing links with explicit args:
  - L65: `gt 'AfterDanceLegare', 'Fight'`
  - L70: `gt 'AfterDanceLegare', 'Police'`
- Matching RPY labels:
  - `AfterDanceLegare(args="")` in `game/Inn/AfterDanceLegare.rpy:1`
- RPY arg usage lines:
  - L1: `label AfterDanceLegare(args=""):`
  - L2: `$ arg = args[0] if args else ""`

## AfterDanceSexLegare
- TXT: `game/Inn/AfterDanceSexLegare.txt`
- RPY: `game/Inn/AfterDanceSexLegare.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[0] -> CurSexStep (L6), arg[1] -> tmpLegareSexType (L12) | outgoing: AfterDanceSexLegare(CurSexStep+1, tmpLegareSexType) @L47; AfterDanceSexLegare(CurSexStep+1, tmpLegareSexType) @L75; AfterDanceSexLegare(CurSexStep+1, tmpLegareSexType) @L176; AfterDanceSexLegare(CurSexStep+2, tmpLegareSexType) @L178; AfterDanceSexLegare(CurSexStep+1, tmpLegareSexType) @L181; AfterDanceSexLegare(CurSexStep+1, tmpLegareSexType) @L184
- TXT arg assignments:
  - L6: `arg[0] -> CurSexStep` from `CurSexStep=Args[0]`
  - L12: `arg[1] -> tmpLegareSexType` from `tmpLegareSexType=Args[1]`
- Incoming links with explicit args:
  - `AfterDanceSexLegare` L47: `gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L75: `gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L176: `act 'Послушать о чем они болтают': gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L178: `act 'Смотреть чего будет дальше': gt 'AfterDanceSexLegare', CurSexStep+2, tmpLegareSexType`
  - `AfterDanceSexLegare` L181: `act 'Смотреть чего будет дальше':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L184: `act 'Дать им кончить':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L186: `act 'Подсматривать дальше':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L190: `act 'Дать им кончить':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L192: `act 'И что дальше?': gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L194: `act 'Еще посмотреть':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L198: `act 'И что дальше?':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L202: `act 'Дать им кончить':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AfterDanceSexLegare` L208: `act 'И что дальше?':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - `AmandaDynamicCommonBlocks` L244: `gt 'AfterDanceSexLegare',0,0,'alone'`
- Outgoing links with explicit args:
  - L47: `gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L75: `gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L176: `act 'Послушать о чем они болтают': gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L178: `act 'Смотреть чего будет дальше': gt 'AfterDanceSexLegare', CurSexStep+2, tmpLegareSexType`
  - L181: `act 'Смотреть чего будет дальше':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L184: `act 'Дать им кончить':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L186: `act 'Подсматривать дальше':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L190: `act 'Дать им кончить':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L192: `act 'И что дальше?': gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L194: `act 'Еще посмотреть':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L198: `act 'И что дальше?':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L202: `act 'Дать им кончить':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
  - L208: `act 'И что дальше?':gt 'AfterDanceSexLegare', CurSexStep+1, tmpLegareSexType`
- Matching RPY labels:
  - `AfterDanceSexLegare(CurSexStep=0, tmpLegareSexType=-1, FollowMode="")` in `game/Inn/AfterDanceSexLegare.rpy:159`
  - `after_dance_sex_legare(no params)` in `game/Inn/AmandaLegareDanceSequence.rpy:123`
- RPY arg usage lines:
  - none

## AmandaAtGloryHole
- TXT: `game/Inn/AmandaAtGloryHole.txt`
- RPY: `game/Inn/AmandaAtGloryHole.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AmandaAtGloryHole(no params)` in `game/Inn/AmandaAtGloryHole.rpy:1`
- RPY arg usage lines:
  - none

## AmandaAtHomeCode
- TXT: `game/Inn/AmandaAtHomeCode.txt`
- RPY: `game/Inn/AmandaAtHomeCode.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> tmpCurSexStep (L226)
- TXT arg assignments:
  - L226: `arg[0] -> tmpCurSexStep` from `tmpCurSexStep=args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AmandaAtHomeCode(no params)` in `game/Inn/AmandaAtHomeCode.rpy:42`
- RPY arg usage lines:
  - none

## AmandaDynamicCommonBlocks
- TXT: `game/Inn/AmandaDynamicCommonBlocks.txt`
- RPY: `game/Inn/AmandaDynamicCommonBlocks.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $tmpGuyName (L162), arg[1] -> tmpSexType (L187) | outgoing: AfterDanceSexLegare(0, 0, 'alone') @L244
- TXT arg assignments:
  - L162: `arg[0] -> $tmpGuyName` from `$tmpGuyName=$args[0]`
  - L187: `arg[1] -> tmpSexType` from `if args[1]>0: tmpSexType=args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L244: `gt 'AfterDanceSexLegare',0,0,'alone'`
- Matching RPY labels:
  - `AmandaDynamicCommonBlocks(no params)` in `game/Inn/AmandaDynamicCommonBlocks.rpy:1`
- RPY arg usage lines:
  - none

## AmandaLegareDanceSequence
- TXT: `game/Inn/AmandaLegareDanceSequence.txt`
- RPY: `game/Inn/AmandaLegareDanceSequence.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[1] -> tmpLegareSexType (L67) | outgoing: FridayDance('Решив не вмешиваться в личную жизнь вашей сестры вы проводили парочку взглядом и остались танцевать.') @L109
- TXT arg assignments:
  - L67: `arg[1] -> tmpLegareSexType` from `tmpLegareSexType=args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L109: `gt 'FridayDance', 'Решив не вмешиваться в личную жизнь вашей сестры вы проводили парочку взглядом и остались танцевать.'`
- Matching RPY labels:
  - `amanda_legare_dance_sequence(no params)` in `game/Inn/AmandaLegareDanceSequence.rpy:4`
  - `AmandaLegareDanceSequence(no params)` in `game/Inn/RuntimeCompat.rpy:160`
- RPY arg usage lines:
  - L85: `label legare_amanda_let_go_code(args=None):`
  - L87: `if args and args[0] == 1:`
  - L88: `$ tmp_legare_sex_type = args[1]`

## AmandaLoverSex
- TXT: `game/Inn/AmandaLoverSex.txt`
- RPY: `game/Inn/AmandaLoverSex.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[1] -> $tmpGuyName (L17)
- TXT arg assignments:
  - L17: `arg[1] -> $tmpGuyName` from `$tmpGuyName=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AmandaLoverSex(no params)` in `game/Inn/AmandaLoverSex.rpy:2`
- RPY arg usage lines:
  - none

## AmandaSexDanceStreet
- TXT: `game/Inn/AmandaSexDanceStreet.txt`
- RPY: `game/Inn/AmandaSexDanceStreet.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `AmandaSexDanceStreet(no params)` in `game/Inn/AmandaSexDanceStreet.rpy:2`
  - `amanda_sex_dance_street(no params)` in `game/Inn/RuntimeCompat.rpy:147`
- RPY arg usage lines:
  - none

## ArtisansQuarter
- TXT: `game/Inn/ArtisansQuarter.txt`
- RPY: `game/Inn/ArtisansQuarter.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ArtisansQuarter(no params)` in `game/Inn/ArtisansQuarter.rpy:1`
  - `artisans_quarter(no params)` in `game/Inn/RuntimeCompat.rpy:100`
- RPY arg usage lines:
  - none

## ArtLevelText
- TXT: `game/Inn/ArtLevelText.txt`
- RPY: `game/Inn/ArtLevelText.rpy`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `art_level_text(value)` in `game/Inn/ArtLevelText.rpy:4`
- RPY arg usage lines:
  - none

## BeckyEddieJoinFirst
- TXT: `game/Inn/BeckyEddieJoinFirst.txt`
- RPY: `game/Inn/BeckyEddieJoinFirst.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `BeckyEddieJoinFirst(no params)` in `game/Inn/BeckyEddieJoinFirst.rpy:15`
  - `becky_eddie_join_first(no params)` in `game/Inn/BeckyEddieJoinFirst.rpy:150`
- RPY arg usage lines:
  - none

## BeckyHome
- TXT: `game/Inn/BeckyHome.txt`
- RPY: `game/Inn/BeckyHome.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $ArriveMode (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $ArriveMode` from `$ArriveMode=$Args[0]`
- Incoming links with explicit args:
  - `BeckyHomeFront` L57: `act 'Зайти в дом':gt 'BeckyHome', $ArriveMode`
  - `IntBeckyGuest` L204: `xgt 'BeckyHome', 'FromDinner'`
  - `IntBeckyGuest` L234: `xgt 'BeckyHome', 'FromDinner'`
  - `IntBeckyGuest` L270: `xgt 'BeckyHome', 'SvalnyiGreh'`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `becky_home(arrive_mode="")` in `game/Inn/BeckyHome.rpy:4`
- RPY arg usage lines:
  - L3: `# Arguments: arrive_mode (str)`
  - L5: `label becky_home(arrive_mode=""):`
  - L7: `if arrive_mode:`
  - L13: `if arrive_mode == 'FromDances' and BeckyVar['visitedhome'] < 5:`
  - L17: `elif arrive_mode == 'SvalnyiGreh':`
  - L22: `elif arrive_mode == 'FromDinner':`
  - L36: `if arrive_mode == 'FromDances':`

## BeckyHomeFront
- TXT: `game/Inn/BeckyHomeFront.txt`
- RPY: `game/Inn/BeckyHomeFront.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $ArriveMode (L7) | outgoing: BeckyHome($ArriveMode) @L57
- TXT arg assignments:
  - L7: `arg[0] -> $ArriveMode` from `$ArriveMode=$Args[0]`
- Incoming links with explicit args:
  - `IntBeckyDance` L210: `gt 'BeckyHomeFront', 'FromDances'`
  - `MarketPlace` L57: `act 'Идти в гости в дом к вдове Блэнкеншип':gt 'BeckyHomeFront', ''`
- Outgoing links with explicit args:
  - L57: `act 'Зайти в дом':gt 'BeckyHome', $ArriveMode`
- Matching RPY labels:
  - `becky_home_front(arrive_mode="")` in `game/Inn/BeckyHomeFront.rpy:41`
- RPY arg usage lines:
  - L41: `label becky_home_front(arrive_mode=""):`
  - L42: `$ ArriveMode = arrive_mode`

## BeckyInviteHome
- TXT: `game/Inn/BeckyInviteHome.txt`
- RPY: `game/Inn/BeckyInviteHome.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `becky_invite_home(girl_name)` in `game/Inn/BeckyInviteHome.rpy:6`
- RPY arg usage lines:
  - none

## BeckyLoversInStore
- TXT: `game/Inn/BeckyLoversInStore.txt`
- RPY: `game/Inn/BeckyLoversInStore.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `becky_lovers_in_store(no params)` in `game/Inn/BeckyLoversInStore.rpy:6`
  - `BeckyLoversInStore(no params)` in `game/Inn/RuntimeCompat.rpy:142`
- RPY arg usage lines:
  - none

## BeckyQuestInit
- TXT: `game/Inn/BeckyQuestInit.txt`
- RPY: `game/Inn/BeckyQuestInit.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `becky_quest_init(no params)` in `game/Inn/BeckyQuestInit.rpy:4`
- RPY arg usage lines:
  - none

## ChangeDressTmp
- TXT: `game/Inn/ChangeDressTmp.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameDress (L6), arg[1] -> $DressName (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameDress` from `$GirlNameDress=$Args[0]`
  - L7: `arg[1] -> $DressName` from `$DressName=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## ChangeTommorowHallJob
- TXT: `game/Inn/ChangeTommorowHallJob.txt`
- RPY: `game/Inn/ChangeTommorowHallJob.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ChangeTommorowHallJob(girl_name=None)` in `game/Inn/ChangeTommorowHallJob.rpy:3`
- RPY arg usage lines:
  - none

## ChangeTommorowWhoreJob
- TXT: `game/Inn/ChangeTommorowWhoreJob.txt`
- RPY: `game/Inn/ChangeTommorowWhoreJob.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ChangeTommorowWhoreJob(girl_name=None)` in `game/Inn/ChangeTommorowWhoreJob.rpy:83`
- RPY arg usage lines:
  - none

## CheckDailyEvent
- TXT: `game/Inn/CheckDailyEvent.txt`
- RPY: `game/Inn/CheckDailyEvent.rpy`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `check_daily_event(girlname=None, eventtype=None, curloc=None, time=None)` in `game/Inn/CheckDailyEvent.rpy:74`
  - `CheckDailyEvent(girlname=None, eventtype=None, curloc=None, time=None)` in `game/Inn/RuntimeCompat.rpy:137`
- RPY arg usage lines:
  - none

## CheckDailyEventExists
- TXT: `game/Inn/CheckDailyEventExists.txt`
- RPY: `game/Inn/CheckDailyEventExists.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `check_daily_event_exists(girlname=None, eventtype=None, location=None)` in `game/Inn/CheckDailyEventExists.rpy:1`
- RPY arg usage lines:
  - none

## CheckVisibility
- TXT: `game/Inn/CheckVisibility.txt`
- RPY: `game/Inn/CheckVisibility.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameVChk (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameVChk` from `$GirlNameVChk=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `check_visibility(no params)` in `game/Inn/RuntimeCompat.rpy:116`
- RPY arg usage lines:
  - none

## Church
- TXT: `game/Inn/Church.txt`
- RPY: `game/Inn/Church.rpy`
- Arg indexes used: `[]`
- Description: outgoing: ChurchIspoved(1) @L139; ChurchAfterCermon(1) @L143
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L139: `act 'Идти на исповедь':gt 'ChurchIspoved',1`
  - L143: `act 'Обойти собор':gt 'ChurchAfterCermon', 1`
- Matching RPY labels:
  - `Church(no params)` in `game/Inn/Church.rpy:2`
- RPY arg usage lines:
  - none

## ChurchAfterCermon
- TXT: `game/Inn/ChurchAfterCermon.txt`
- RPY: `game/Inn/ChurchAfterCermon.rpy`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - `Church` L143: `act 'Обойти собор':gt 'ChurchAfterCermon', 1`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - L3: `label ChurchAfterCermon(args=()):`
  - L5: `if not args or args[0] != 1:`

## ChurchIspoved
- TXT: `game/Inn/ChurchIspoved.txt`
- RPY: `game/Inn/ChurchIspoved.rpy`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - `Church` L139: `act 'Идти на исповедь':gt 'ChurchIspoved',1`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - L2: `label ChurchIspoved(args=()):`
  - L4: `if not args or args[0] != 1:`

## CityGuard
- TXT: `game/Inn/CityGuard.txt`
- RPY: `game/Inn/CityGuard.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `city_guard(no params)` in `game/Inn/CityGuard.rpy:1`
  - `CityGuard(no params)` in `game/Inn/RuntimeCompat.rpy:92`
- RPY arg usage lines:
  - none

## CleanScreenOverflow
- TXT: `game/Inn/CleanScreenOverflow.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `CleanScreenOverflow(lines)` in `game/Inn/FrancheskaTalk.rpy:153`
  - `clean_screen_overflow(args0=1)` in `game/Inn/RuntimeCompat.rpy:57`
- RPY arg usage lines:
  - none

## CleanSpermRandom
- TXT: `game/Inn/CleanSpermRandom.txt`
- RPY: `game/Inn/CleanSpermRandom.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `CleanSpermRandom(girl_name="")` in `game/Inn/CleanSpermRandom.rpy:61`
- RPY arg usage lines:
  - none

## CockPosition
- TXT: `game/Inn/CockPosition.txt`
- RPY: `game/Inn/CockPosition.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[0] -> $GirlNameCPST (L6), arg[2] -> $OtherDudeName (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameCPST` from `$GirlNameCPST=$Args[0]`
  - L7: `arg[2] -> $OtherDudeName` from `$OtherDudeName=$Args[2]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `CockPosition(girl_name="", position=0, other_dude_name="")` in `game/Inn/CockPosition.rpy:28`
  - `cock_position(girl_name="", position=0, other_dude_name="")` in `game/Inn/CockPosition.rpy:33`
- RPY arg usage lines:
  - none

## CreateDonationsList
- TXT: `game/Inn/CreateDonationsList.txt`
- RPY: `game/Inn/CreateDonationsList.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `CreateDonationsList(no params)` in `game/Inn/CreateDonationsList.rpy:1`
- RPY arg usage lines:
  - none

## CreateDressListMenu
- TXT: `game/Inn/CreateDressListMenu.txt`
- RPY: `game/Inn/CreateDressListMenu.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `create_dress_list_menu(no params)` in `game/Inn/CreateDressListMenu.rpy:4`
  - `CreateDressListMenu(no params)` in `game/Inn/RuntimeCompat.rpy:132`
- RPY arg usage lines:
  - none

## CreateMandatoryEvents
- TXT: `game/Inn/CreateMandatoryEvents.txt`
- RPY: `game/Inn/CreateMandatoryEvents.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `CreateMandatoryEvents(no params)` in `game/Inn/CreateMandatoryEvents.rpy:1`
- RPY arg usage lines:
  - none

## CreateTavernEventsPeriod
- TXT: `game/Inn/CreateTavernEventsPeriod.txt`
- RPY: `game/Inn/CreateTavernEventsPeriod.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> TimePeriod (L6)
- TXT arg assignments:
  - L6: `arg[0] -> TimePeriod` from `TimePeriod=Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `CreateTavernEventsPeriod(TimePeriod)` in `game/Inn/CreateTavernEventsPeriod.rpy:1`
- RPY arg usage lines:
  - none

## DailySetstatdefault
- TXT: `game/Inn/DailySetstatdefault.txt`
- RPY: `game/Inn/DailySetstatdefault.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$ARGS[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `daily_setstatdefault(girl_name)` in `game/Inn/DailySetstatdefault.rpy:1`
- RPY arg usage lines:
  - none

## DayToText
- TXT: `game/Inn/DayToText.txt`
- RPY: `game/Inn/DayToText.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> DayToTransform (L6)
- TXT arg assignments:
  - L6: `arg[0] -> DayToTransform` from `DayToTransform=args[0]+1`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `day_to_text(day_number)` in `game/Inn/DayToText.rpy:1`
- RPY arg usage lines:
  - none

## DeleteDailyEvent
- TXT: `game/Inn/DeleteDailyEvent.txt`
- RPY: `game/Inn/DeleteDailyEvent.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `delete_daily_event(girlname="", eventtype="", location="")` in `game/Inn/DeleteDailyEvent.rpy:4`
- RPY arg usage lines:
  - none

## DescribeSkillIncrease
- TXT: `game/Inn/DescribeSkillIncrease.txt`
- RPY: `game/Inn/DescribeSkillIncrease.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `DescribeSkillIncrease(girl_name=None)` in `game/Inn/DescribeSkillIncrease.rpy:41`
- RPY arg usage lines:
  - none

## DispFrac
- TXT: `game/Inn/DispFrac.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: arg[0] -> numFrac (L6), arg[0] -> numFrac1 (L7)
- TXT arg assignments:
  - L6: `arg[0] -> numFrac` from `numFrac=Args[0]`
  - L7: `arg[0] -> numFrac1` from `numFrac1=Args[0] mod 10`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## DisplayTavernEventShort
- TXT: `game/Inn/DisplayTavernEventShort.txt`
- RPY: `game/Inn/DisplayTavernEventShort.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> TimePeriod (L6), arg[1] -> Eyewitness (L7)
- TXT arg assignments:
  - L6: `arg[0] -> TimePeriod` from `TimePeriod=Args[0]`
  - L7: `arg[1] -> Eyewitness` from `Eyewitness=Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `display_tavern_event_short(time_period, eyewitness)` in `game/Inn/DisplayTavernEventShort.rpy:13`
- RPY arg usage lines:
  - none

## DisplayTavernEventsSummary
- TXT: `game/Inn/DisplayTavernEventsSummary.txt`
- RPY: `game/Inn/DisplayTavernEventsSummary.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `display_tavern_events_summary(day, month, year)` in `game/Inn/DisplayTavernEventsSummary.rpy:14`
- RPY arg usage lines:
  - none

## DressForNight
- TXT: `game/Inn/DressForNight.txt`
- RPY: `game/Inn/DressForNight.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameDress (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameDress` from `$GirlNameDress=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `dress_for_night(girl_name, mode)` in `game/Inn/DressForNight.rpy:4`
  - `DressForNight(girl_name, mode)` in `game/Inn/RuntimeCompat.rpy:127`
- RPY arg usage lines:
  - none

## DressNoShow
- TXT: `game/Inn/DressNoShow.txt`
- RPY: `game/Inn/DressNoShow.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameDNS (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameDNS` from `$GirlNameDNS=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `dress_no_show(girl_name_dns)` in `game/Inn/DressNoShow.rpy:3`
- RPY arg usage lines:
  - none

## DressShop
- TXT: `game/Inn/DressShop.txt`
- RPY: `game/Inn/DressShop.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `DressShop(no params)` in `game/Inn/DressShop.rpy:1`
- RPY arg usage lines:
  - none

## DressTry
- TXT: `game/Inn/DressTry.txt`
- RPY: `game/Inn/DressTry.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[1] -> $DressProduced (L33), arg[0] -> $DressBuyer (L34)
- TXT arg assignments:
  - L33: `arg[1] -> $DressProduced` from `$DressProduced=$Args[1]`
  - L34: `arg[0] -> $DressBuyer` from `$DressBuyer=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `dress_try(no params)` in `game/Inn/DressTry.rpy:4`
- RPY arg usage lines:
  - none

## DressUp
- TXT: `game/Inn/DressUp.txt`
- RPY: `game/Inn/DressUp.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameDress (L6), arg[1] -> IsNewDayForDress (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameDress` from `$GirlNameDress=$Args[0]`
  - L7: `arg[1] -> IsNewDayForDress` from `IsNewDayForDress=Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `DressUp(GirlNameDress="", IsNewDayForDress=0)` in `game/Inn/DressUp.rpy:1`
  - `dress_up(girl_name="", is_new_day_for_dress=0)` in `game/Inn/DressUp.rpy:162`
- RPY arg usage lines:
  - none

## EllonaBirthPrayMenu
- TXT: `game/Inn/EllonaBirthPrayMenu.txt`
- RPY: `game/Inn/EllonaBirthPrayMenu.rpy`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `EllonaBirthPrayMenu(no params)` in `game/Inn/EllonaBirthPrayMenu.rpy:2`
- RPY arg usage lines:
  - L7: `$ GraceBlessing[args[0]] = 1`
  - L10: `if args[0] == 0 and SumArray(GraceBlessing) >= 6 and (BlessedByEllona == 0 or CursedByEllona == 1):`

## EllonaTemple
- TXT: `game/Inn/EllonaTemple.txt`
- RPY: `game/Inn/EllonaTemple.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `EllonaTemple(no params)` in `game/Inn/EllonaTemple.rpy:2`
- RPY arg usage lines:
  - none

## EllonaTempleMenu
- TXT: `game/Inn/EllonaTempleMenu.txt`
- RPY: `game/Inn/EllonaTempleMenu.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `EllonaTempleMenu(no params)` in `game/Inn/EllonaTempleMenu.rpy:2`
- RPY arg usage lines:
  - none

## EventAmandaLegareCreateDance
- TXT: `game/Inn/EventAmandaLegareCreateDance.txt`
- RPY: `game/Inn/EventAmandaLegareCreateDance.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `event_amanda_legare_create_dance(no params)` in `game/Inn/EventAmandaLegareCreateDance.rpy:43`
- RPY arg usage lines:
  - none

## EventAmandaLizettTalk
- TXT: `game/Inn/EventAmandaLizettTalk.txt`
- RPY: `game/Inn/EventAmandaLizettTalk.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> Eyewitness (L6) | outgoing: TavernMain(1) @L41; TavernMain(1) @L52; TavernMain(1) @L62; TavernMain(1) @L72; TavernMain(1) @L81; TavernMain(1) @L96
- TXT arg assignments:
  - L6: `arg[0] -> Eyewitness` from `Eyewitness=Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L41: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L52: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L62: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L72: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L81: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L96: `gt 'TavernMain',1`
- Matching RPY labels:
  - `event_amanda_lizett_talk(eyewitness=0)` in `game/Inn/EventAmandaLizettTalk.rpy:1`
- RPY arg usage lines:
  - none

## EventAmandaLizettTalk2
- TXT: `game/Inn/EventAmandaLizettTalk2.txt`
- RPY: `game/Inn/EventAmandaLizettTalk2.rpy`
- Arg indexes used: `[0, 3, 4, 5]`
- Description: arg[0] -> Eyewitness (L6), arg[3] -> DefiniteAccept (L10), arg[4] -> FriendLimit (L11), arg[5] -> SlutLimit (L12) | outgoing: TavernMain(1) @L51
- TXT arg assignments:
  - L6: `arg[0] -> Eyewitness` from `Eyewitness=Args[0]`
  - L10: `arg[3] -> DefiniteAccept` from `DefiniteAccept=Args[3]`
  - L11: `arg[4] -> FriendLimit` from `FriendLimit=Args[4]`
  - L12: `arg[5] -> SlutLimit` from `SlutLimit=Args[5]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L51: `act 'Вернуться к своим делам':gt 'TavernMain',1`
- Matching RPY labels:
  - `event_amanda_lizett_talk2(eyewitness=0)` in `game/Inn/EventAmandaLizettTalk2.rpy:1`
  - `EventAmandaLizettTalk2(eyewitness=0)` in `game/Inn/EventAmandaLizettTalk2.rpy:53`
- RPY arg usage lines:
  - none

## EventCleaningHarrass
- TXT: `game/Inn/EventCleaningHarrass.txt`
- RPY: `game/Inn/EventCleaningHarrass.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> Eyewitness (L6)
- TXT arg assignments:
  - L6: `arg[0] -> Eyewitness` from `Eyewitness=Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `event_cleaning_harrass(eyewitness=0)` in `game/Inn/EventCleaningHarrass.rpy:1`
- RPY arg usage lines:
  - none

## EventCleaningHarrassPart2
- TXT: `game/Inn/EventCleaningHarrassPart2.txt`
- RPY: `game/Inn/EventCleaningHarrassPart2.rpy`
- Arg indexes used: `[0, 1, 2, 3]`
- Description: arg[0] -> $GirlNameECH (L6), arg[1] -> Eyewitness (L7), arg[2] -> YourReaction1 (L8), arg[3] -> HarassType (L9)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameECH` from `$GirlNameECH=$Args[0]`
  - L7: `arg[1] -> Eyewitness` from `Eyewitness=Args[1]`
  - L8: `arg[2] -> YourReaction1` from `YourReaction1=Args[2]`
  - L9: `arg[3] -> HarassType` from `HarassType=Args[3]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `event_cleaning_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1)` in `game/Inn/EventCleaningHarrassPart2.rpy:1`
- RPY arg usage lines:
  - none

## EventFightSmall
- TXT: `game/Inn/EventFightSmall.txt`
- RPY: `game/Inn/EventFightSmall.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> Eyewitness (L6) | outgoing: TavernMain(1) @L42; TavernMain(1) @L52; TavernMain(1) @L62; TavernMain(1) @L72; TavernMain(1) @L84; TavernMain(1) @L99
- TXT arg assignments:
  - L6: `arg[0] -> Eyewitness` from `Eyewitness=Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L42: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L52: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L62: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L72: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L84: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L99: `act 'Вернуться к своим делам':gt 'TavernMain',1`
- Matching RPY labels:
  - `event_fight_small(eyewitness=0)` in `game/Inn/EventFightSmall.rpy:1`
- RPY arg usage lines:
  - none

## EventWaitressHarrass
- TXT: `game/Inn/EventWaitressHarrass.txt`
- RPY: `game/Inn/EventWaitressHarrass.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> Eyewitness (L6)
- TXT arg assignments:
  - L6: `arg[0] -> Eyewitness` from `Eyewitness=Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `event_waitress_harrass(eyewitness=0)` in `game/Inn/EventWaitressHarrass.rpy:1`
- RPY arg usage lines:
  - none

## EventWaitressHarrassPart2
- TXT: `game/Inn/EventWaitressHarrassPart2.txt`
- RPY: `game/Inn/EventWaitressHarrassPart2.rpy`
- Arg indexes used: `[0, 1, 2, 3]`
- Description: arg[0] -> $GirlNameEWH (L6), arg[1] -> Eyewitness (L7), arg[2] -> YourReaction1 (L8), arg[3] -> HarassType (L9)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameEWH` from `$GirlNameEWH=$Args[0]`
  - L7: `arg[1] -> Eyewitness` from `Eyewitness=Args[1]`
  - L8: `arg[2] -> YourReaction1` from `YourReaction1=Args[2]`
  - L9: `arg[3] -> HarassType` from `HarassType=Args[3]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `event_waitress_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1)` in `game/Inn/EventWaitressHarrassPart2.rpy:1`
- RPY arg usage lines:
  - none

## EventWineForDance
- TXT: `game/Inn/EventWineForDance.txt`
- RPY: `game/Inn/EventWineForDance.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> Eyewitness (L6) | outgoing: TavernMain(1) @L23; TavernMain(1) @L32; TavernMain(1) @L41
- TXT arg assignments:
  - L6: `arg[0] -> Eyewitness` from `Eyewitness=Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L23: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L32: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - L41: `act 'Вернуться к своим делам':gt 'TavernMain',1`
- Matching RPY labels:
  - `event_wine_for_dance(eyewitness=0)` in `game/Inn/EventWineForDance.rpy:1`
- RPY arg usage lines:
  - none

## FightResult
- TXT: `game/Inn/FightResult.txt`
- RPY: `game/Inn/FightResult.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[0] -> Enemy1 (L6), arg[1] -> Enemy2 (L7), arg[2] -> DrawPossible (L8)
- TXT arg assignments:
  - L6: `arg[0] -> Enemy1` from `Enemy1=ARGS[0]`
  - L7: `arg[1] -> Enemy2` from `Enemy2=aRGS[1]`
  - L8: `arg[2] -> DrawPossible` from `DrawPossible=aRGS[2]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## FrancheskaTalk
- TXT: `game/Inn/FrancheskaTalk.txt`
- RPY: `game/Inn/FrancheskaTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `FrancheskaTalk(no params)` in `game/Inn/FrancheskaTalk.rpy:2`
- RPY arg usage lines:
  - none

## FridayDance
- TXT: `game/Inn/FridayDance.txt`
- RPY: `game/Inn/FridayDance.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $AddDancePhraseTmp (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $AddDancePhraseTmp` from `$AddDancePhraseTmp=$Args[0]`
- Incoming links with explicit args:
  - `AmandaLegareDanceSequence` L109: `gt 'FridayDance', 'Решив не вмешиваться в личную жизнь вашей сестры вы проводили парочку взглядом и остались танцевать.'`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `friday_dance(add_dance_phrase_tmp="")` in `game/Inn/FridayDance.rpy:4`
  - `FridayDance(no params)` in `game/Inn/RuntimeCompat.rpy:96`
- RPY arg usage lines:
  - none

## GeorgettBeckyVisit
- TXT: `game/Inn/GeorgettBeckyVisit.txt`
- RPY: `game/Inn/GeorgettBeckyVisit.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GeorgettBeckyVisit(no params)` in `game/Inn/GeorgettBeckyVisit.rpy:15`
- RPY arg usage lines:
  - none

## GetGirlDrunk
- TXT: `game/Inn/GetGirlDrunk.txt`
- RPY: `game/Inn/GetGirlDrunk.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameDrunk (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameDrunk` from `$GirlNameDrunk=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `get_girl_drunk(girl_name="")` in `game/Inn/RuntimeCompat.rpy:108`
- RPY arg usage lines:
  - none

## GetRandomGirlByJob
- TXT: `game/Inn/GetRandomGirlByJob.txt`
- RPY: `game/Inn/GetRandomGirlByJob.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $jobtype (L8)
- TXT arg assignments:
  - L8: `arg[0] -> $jobtype` from `$jobtype=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GetRandomGirlByJob(job_dict_name=None)` in `game/Inn/ChangeTommorowWhoreJob.rpy:94`
- RPY arg usage lines:
  - none

## GirlDressBuy
- TXT: `game/Inn/GirlDressBuy.txt`
- RPY: `game/Inn/GirlDressBuy.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L7)
- TXT arg assignments:
  - L7: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `girl_dress_buy(girl_name)` in `game/Inn/GirlDressBuy.rpy:4`
- RPY arg usage lines:
  - none

## GirlDressSuggest
- TXT: `game/Inn/GirlDressSuggest.txt`
- RPY: `game/Inn/GirlDressSuggest.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlName (L6), arg[1] -> $DressToBuy (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
  - L7: `arg[1] -> $DressToBuy` from `$DressToBuy=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `girl_dress_suggest(girl_name, dress_to_buy)` in `game/Inn/GirlDressSuggest.rpy:3`
- RPY arg usage lines:
  - none

## GirlsDesc
- TXT: `game/Inn/GirlsDesc.txt`
- RPY: `game/Inn/GirlsDesc.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameGdsc (L12)
- TXT arg assignments:
  - L12: `arg[0] -> $GirlNameGdsc` from `$GirlNameGdsc=$ARGS[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GirlsDesc(girl_name)` in `game/Inn/GirlsDesc.rpy:282`
  - `girls_desc(girl)` in `game/Inn/IntGeorgettTalk.rpy:249`
- RPY arg usage lines:
  - none

## GirlSuggestDressFunc
- TXT: `game/Inn/GirlSuggestDressFunc.txt`
- RPY: `game/Inn/GirlSuggestDressFunc.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GirlSuggestDressFunc(GirlName="", DressToBuy="")` in `game/Inn/GirlSuggestDressFunc.rpy:23`
- RPY arg usage lines:
  - none

## GiveBirth
- TXT: `game/Inn/GiveBirth.txt`
- RPY: `game/Inn/GiveBirth.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GiveBirth(GirlName="")` in `game/Inn/GiveBirth.rpy:1`
- RPY arg usage lines:
  - none

## GiveBirthFinish
- TXT: `game/Inn/GiveBirthFinish.txt`
- RPY: `game/Inn/GiveBirthFinish.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GiveBirthFinish(no params)` in `game/Inn/GiveBirthFinish.rpy:1`
- RPY arg usage lines:
  - none

## GiveBirthStep2
- TXT: `game/Inn/GiveBirthStep2.txt`
- RPY: `game/Inn/GiveBirthStep2.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GiveBirthStep2(no params)` in `game/Inn/GiveBirthStep2.rpy:1`
- RPY arg usage lines:
  - none

## GloryHoleBusy
- TXT: `game/Inn/GloryHoleBusy.txt`
- RPY: `game/Inn/GloryHoleBusy.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameGHB (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameGHB` from `$GirlNameGHB=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GloryHoleBusy(girl_name)` in `game/Inn/GloryHoleBusy.rpy:1`
- RPY arg usage lines:
  - none

## GroceryStore
- TXT: `game/Inn/GroceryStore.txt`
- RPY: `game/Inn/GroceryStore.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `GroceryStore(no params)` in `game/Inn/GroceryStore.rpy:2`
- RPY arg usage lines:
  - none

## HarassDiscussImage
- TXT: `game/Inn/HarassDiscussImage.txt`
- RPY: `game/Inn/HarassDiscussImage.rpy`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `HarassDiscussImage(girl="", value=0)` in `game/Inn/HarassDiscussImage.rpy:1`
- RPY arg usage lines:
  - none

## HarassShowImage
- TXT: `game/Inn/HarassShowImage.txt`
- RPY: `game/Inn/HarassShowImage.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[0] -> $GirlNameHSI (L6), arg[1] -> $ActionHSI (L7), arg[2] -> ReactionHSI (L9)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameHSI` from `$GirlNameHSI=$Args[0]`
  - L7: `arg[1] -> $ActionHSI` from `$ActionHSI=$args[1]`
  - L9: `arg[2] -> ReactionHSI` from `ReactionHSI=Args[2]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `HarassShowImage(GirlNameHSI="", ActionHSI="", ReactionHSI=0)` in `game/Inn/HarassShowImage.rpy:1`
- RPY arg usage lines:
  - none

## HasThisDress
- TXT: `game/Inn/HasThisDress.txt`
- RPY: `game/Inn/HasThisDress.rpy`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## IncreaseArousal
- TXT: `game/Inn/IncreaseArousal.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3]`
- Description: arg[0] -> $TargetName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $TargetName` from `$TargetName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## IncreaseSkill
- TXT: `game/Inn/IncreaseSkill.txt`
- RPY: `game/Inn/IncreaseSkill.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IncreaseSkill(girl_name=None)` in `game/Inn/IncreaseSkill.rpy:53`
- RPY arg usage lines:
  - none

## InitAmanda
- TXT: `game/Inn/InitAmanda.txt`
- RPY: `game/Inn/InitAmanda.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitAmanda(no params)` in `game/Inn/InitAmanda.rpy:1`
- RPY arg usage lines:
  - none

## InitAmandaLizaTalkItems
- TXT: `game/Inn/InitAmandaLizaTalkItems.txt`
- RPY: `game/Inn/InitAmandaLizaTalkItems.rpy`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitAmandaLizaTalkItems(no params)` in `game/Inn/InitAmandaLizaTalkItems.rpy:1`
- RPY arg usage lines:
  - none

## InitBecky
- TXT: `game/Inn/InitBecky.txt`
- RPY: `game/Inn/InitBecky.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitBecky(no params)` in `game/Inn/InitBecky.rpy:1`
- RPY arg usage lines:
  - none

## InitDressDesc
- TXT: `game/Inn/InitDressDesc.txt`
- RPY: `game/Inn/InitDressDesc.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitDressDesc(no params)` in `game/Inn/InitDressDesc.rpy:1`
- RPY arg usage lines:
  - none

## InitGeorgett
- TXT: `game/Inn/InitGeorgett.txt`
- RPY: `game/Inn/InitGeorgett.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitGeorgett(no params)` in `game/Inn/InitGeorgett.rpy:1`
- RPY arg usage lines:
  - none

## InitInga
- TXT: `game/Inn/InitInga.txt`
- RPY: `game/Inn/InitInga.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitInga(no params)` in `game/Inn/InitInga.rpy:1`
- RPY arg usage lines:
  - none

## InitIrma
- TXT: `game/Inn/InitIrma.txt`
- RPY: `game/Inn/InitIrma.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitIrma(no params)` in `game/Inn/InitIrma.rpy:1`
- RPY arg usage lines:
  - none

## InitLiza
- TXT: `game/Inn/InitLiza.txt`
- RPY: `game/Inn/InitLiza.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitLiza(no params)` in `game/Inn/InitLiza.rpy:1`
- RPY arg usage lines:
  - none

## InitMelissa
- TXT: `game/Inn/InitMelissa.txt`
- RPY: `game/Inn/InitMelissa.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitMelissa(no params)` in `game/Inn/InitMelissa.rpy:1`
- RPY arg usage lines:
  - none

## InitSandra
- TXT: `game/Inn/InitSandra.txt`
- RPY: `game/Inn/InitSandra.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitSandra(no params)` in `game/Inn/InitSandra.rpy:1`
- RPY arg usage lines:
  - none

## InitSecondaryNPC
- TXT: `game/Inn/InitSecondaryNPC.txt`
- RPY: `game/Inn/InitSecondaryNPC.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `InitSecondaryNPC(no params)` in `game/Inn/InitSecondaryNPC.rpy:1`
- RPY arg usage lines:
  - none

## IntAlberTalk
- TXT: `game/Inn/IntAlberTalk.txt`
- RPY: `game/Inn/IntAlberTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntAlberTalk(no params)` in `game/Inn/IntAlberTalk.rpy:2`
- RPY arg usage lines:
  - none

## IntAmandaDance
- TXT: `game/Inn/IntAmandaDance.txt`
- RPY: `game/Inn/IntAmandaDance.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `int_amanda_dance(no params)` in `game/Inn/IntAmandaDance.rpy:4`
- RPY arg usage lines:
  - none

## IntAmandaDressChange
- TXT: `game/Inn/IntAmandaDressChange.txt`
- RPY: `game/Inn/IntAmandaDressChange.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `int_amanda_dress_change(GirlNameIAT="amanda")` in `game/Inn/IntAmandaDressChange.rpy:39`
- RPY arg usage lines:
  - none

## IntAmandaSex
- TXT: `game/Inn/IntAmandaSex.txt`
- RPY: `game/Inn/IntAmandaSex.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[0] -> $GirlNameASDS (L6), arg[1] -> $GirlLocASDS (L7), arg[2] -> $GirlModeASDS (L8)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameASDS` from `$GirlNameASDS=$Args[0]`
  - L7: `arg[1] -> $GirlLocASDS` from `$GirlLocASDS=$Args[1]`
  - L8: `arg[2] -> $GirlModeASDS` from `$GirlModeASDS=$Args[2]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntAmandaSex(GirlNameASDS="amanda", GirlLocASDS="home", GirlModeASDS="")` in `game/Inn/IntAmandaSex.rpy:1`
- RPY arg usage lines:
  - none

## IntAmandaTalk
- TXT: `game/Inn/IntAmandaTalk.txt`
- RPY: `game/Inn/IntAmandaTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `int_amanda_talk(no params)` in `game/Inn/IntAmandaTalk.rpy:3`
  - `IntAmandaTalk(no params)` in `game/Inn/LegacyIntAliases.rpy:8`
- RPY arg usage lines:
  - none

## IntBeckyAfterCermon
- TXT: `game/Inn/IntBeckyAfterCermon.txt`
- RPY: `game/Inn/IntBeckyAfterCermon.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntBeckyAfterCermon(no params)` in `game/Inn/IntBeckyAfterCermon.rpy:1`
- RPY arg usage lines:
  - none

## IntBeckyDance
- TXT: `game/Inn/IntBeckyDance.txt`
- RPY: `game/Inn/IntBeckyDance.rpy`
- Arg indexes used: `[]`
- Description: outgoing: BeckyHomeFront('FromDances') @L210
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L210: `gt 'BeckyHomeFront', 'FromDances'`
- Matching RPY labels:
  - `int_becky_dance(no params)` in `game/Inn/IntBeckyDance.rpy:4`
- RPY arg usage lines:
  - none

## IntBeckyDressChange
- TXT: `game/Inn/IntBeckyDressChange.txt`
- RPY: `game/Inn/IntBeckyDressChange.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntBeckyDressChange(GirlName="becky")` in `game/Inn/IntBeckyDressChange.rpy:1`
- RPY arg usage lines:
  - none

## IntBeckyGuest
- TXT: `game/Inn/IntBeckyGuest.txt`
- RPY: `game/Inn/IntBeckyGuest.rpy`
- Arg indexes used: `[]`
- Description: outgoing: BeckyHome('FromDinner') @L204; BeckyHome('FromDinner') @L234; BeckyHome('SvalnyiGreh') @L270
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L204: `xgt 'BeckyHome', 'FromDinner'`
  - L234: `xgt 'BeckyHome', 'FromDinner'`
  - L270: `xgt 'BeckyHome', 'SvalnyiGreh'`
- Matching RPY labels:
  - `IntBeckyGuest(no params)` in `game/Inn/IntBeckyGuest.rpy:1`
  - `int_becky_guest(no params)` in `game/Inn/IntBeckyGuest.rpy:325`
- RPY arg usage lines:
  - none

## IntBeckySex
- TXT: `game/Inn/IntBeckySex.txt`
- RPY: `game/Inn/IntBeckySex.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameIBS (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameIBS` from `$GirlNameIBS=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntBeckySex(GirlNameIBS="becky", GirlLocIBS="home", GirlModeIBS="")` in `game/Inn/IntBeckySex.rpy:15`
  - `int_becky_sex(girl_name="becky")` in `game/Inn/IntBeckySex.rpy:380`
- RPY arg usage lines:
  - none

## IntBeckyTalk
- TXT: `game/Inn/IntBeckyTalk.txt`
- RPY: `game/Inn/IntBeckyTalk.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - L2: `label IntBeckyTalk(args=()):`
  - L4: `GirlName = args[0] if args and len(args) > 0 else 'becky'`

## IntBeckyTalkSherwood
- TXT: `game/Inn/IntBeckyTalkSherwood.txt`
- RPY: `game/Inn/IntBeckyTalkSherwood.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - L2: `label IntBeckyTalkSherwood(args=()):`
  - L4: `GirlName = args[0] if args and len(args) > 0 else 'becky'`

## IntEddieBeckySex
- TXT: `game/Inn/IntEddieBeckySex.txt`
- RPY: `game/Inn/IntEddieBeckySex.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntEddieBeckySex(GirlNameIBS="becky")` in `game/Inn/IntEddieBeckySex.rpy:15`
  - `int_eddie_becky_sex(girl_name="becky")` in `game/Inn/IntEddieBeckySex.rpy:312`
- RPY arg usage lines:
  - none

## IntGeorgettAfterCermon
- TXT: `game/Inn/IntGeorgettAfterCermon.txt`
- RPY: `game/Inn/IntGeorgettAfterCermon.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntGeorgettAfterCermon(no params)` in `game/Inn/IntGeorgettAfterCermon.rpy:1`
- RPY arg usage lines:
  - none

## IntGeorgettDressChange
- TXT: `game/Inn/IntGeorgettDressChange.txt`
- RPY: `game/Inn/IntGeorgettDressChange.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntGeorgettDressChange(GirlNameIGT="georgett")` in `game/Inn/IntGeorgettDressChange.rpy:1`
  - `int_georgett_dress_change(no params)` in `game/Inn/IntGeorgettTalk.rpy:252`
- RPY arg usage lines:
  - none

## IntGeorgettSex
- TXT: `game/Inn/IntGeorgettSex.txt`
- RPY: `game/Inn/IntGeorgettSex.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameIGSS (L6), arg[1] -> $GirlLocIGSS (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameIGSS` from `$GirlNameIGSS=$Args[0]`
  - L7: `arg[1] -> $GirlLocIGSS` from `$GirlLocIGSS=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntGeorgettSex(GirlNameIGSS="georgett", GirlLocIGSS="street")` in `game/Inn/IntGeorgettSex.rpy:1`
- RPY arg usage lines:
  - none

## IntGeorgettTalk
- TXT: `game/Inn/IntGeorgettTalk.txt`
- RPY: `game/Inn/IntGeorgettTalk.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameIGT (L6), arg[1] -> $GirlLocIGT (L7) | outgoing: SexProstTavern(1, 'georgett') @L269; SexPort(1, 'georgett') @L272
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameIGT` from `$GirlNameIGT=$Args[0]`
  - L7: `arg[1] -> $GirlLocIGT` from `$GirlLocIGT=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L269: `gt 'SexProstTavern',1, 'georgett'`
  - L272: `gt 'SexPort',1, 'georgett'`
- Matching RPY labels:
  - `int_georgett_talk(girl_name, girl_loc)` in `game/Inn/IntGeorgettTalk.rpy:3`
  - `IntGeorgettTalk(girl_name, girl_loc="street")` in `game/Inn/LegacyIntAliases.rpy:12`
- RPY arg usage lines:
  - none

## IntHarrassmentDiscuss
- TXT: `game/Inn/IntHarrassmentDiscuss.txt`
- RPY: `game/Inn/IntHarrassmentDiscuss.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameMHD (L6), arg[1] -> YourReaction1 (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameMHD` from `$GirlNameMHD=$Args[0]`
  - L7: `arg[1] -> YourReaction1` from `YourReaction1=Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntHarrassmentDiscuss(GirlNameMHD, YourReaction1)` in `game/Inn/IntHarrassmentDiscuss.rpy:1`
- RPY arg usage lines:
  - none

## IntLizaDressChange
- TXT: `game/Inn/IntLizaDressChange.txt`
- RPY: `game/Inn/IntLizaDressChange.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntLizaDressChange(GirlNameILT="liza")` in `game/Inn/IntLizaDressChange.rpy:1`
- RPY arg usage lines:
  - none

## IntLizaSex
- TXT: `game/Inn/IntLizaSex.txt`
- RPY: `game/Inn/IntLizaSex.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNameILSS (L6), arg[1] -> $GirlLocILSS (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameILSS` from `$GirlNameILSS=$Args[0]`
  - L7: `arg[1] -> $GirlLocILSS` from `$GirlLocILSS=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntLizaSex(GirlNameILSS="liza", GirlLocILSS="street")` in `game/Inn/IntLizaSex.rpy:1`
- RPY arg usage lines:
  - none

## IntLizettAfterCermon
- TXT: `game/Inn/IntLizettAfterCermon.txt`
- RPY: `game/Inn/IntLizettAfterCermon.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntLizettAfterCermon(no params)` in `game/Inn/IntLizettAfterCermon.rpy:1`
- RPY arg usage lines:
  - none

## IntMelissaDressChange
- TXT: `game/Inn/IntMelissaDressChange.txt`
- RPY: `game/Inn/IntMelissaDressChange.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntMelissaDressChange(GirlNameIMT="melissa")` in `game/Inn/IntMelissaDressChange.rpy:1`
  - `int_melissa_dress_change(no params)` in `game/Inn/IntMelissaDressChange.rpy:90`
- RPY arg usage lines:
  - none

## IntMelissaTalk
- TXT: `game/Inn/IntMelissaTalk.txt`
- RPY: `game/Inn/IntMelissaTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `int_melissa_talk(no params)` in `game/Inn/IntMelissaTalk.rpy:1`
  - `IntMelissaTalk(no params)` in `game/Inn/LegacyIntAliases.rpy:4`
- RPY arg usage lines:
  - none

## Intro
- TXT: `game/Inn/Intro.txt`
- RPY: `game/Inn/Intro.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `Intro(no params)` in `game/Inn/Intro.rpy:1`
- RPY arg usage lines:
  - none

## IntRobinTalk
- TXT: `game/Inn/IntRobinTalk.txt`
- RPY: `game/Inn/IntRobinTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `int_robin_talk(no params)` in `game/Inn/IntRobinTalk.rpy:1`
  - `IntRobinTalk(no params)` in `game/Inn/LegacyIntAliases.rpy:16`
- RPY arg usage lines:
  - none

## IntSandraDressChange
- TXT: `game/Inn/IntSandraDressChange.txt`
- RPY: `game/Inn/IntSandraDressChange.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `IntSandraDressChange(GirlNameIST="sandra")` in `game/Inn/IntSandraDressChange.rpy:1`
  - `int_sandra_dress_change(no params)` in `game/Inn/IntSandraDressChange.rpy:90`
- RPY arg usage lines:
  - none

## IntSandraTalk
- TXT: `game/Inn/IntSandraTalk.txt`
- RPY: `game/Inn/IntSandraTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `int_sandra_talk(no params)` in `game/Inn/IntSandraTalk.rpy:1`
  - `IntSandraTalk(no params)` in `game/Inn/LegacyIntAliases.rpy:1`
- RPY arg usage lines:
  - none

## IntZimmerTalk
- TXT: `game/Inn/IntZimmerTalk.txt`
- RPY: `game/Inn/IntZimmerTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `int_zimmer_talk(no params)` in `game/Inn/IntZimmerTalk.rpy:1`
- RPY arg usage lines:
  - none

## IrmaShortStories
- TXT: `game/Inn/IrmaShortStories.txt`
- RPY: `game/Inn/IrmaShortStories.rpy`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - L2: `label IrmaShortStories(args=()):`
  - L7: `a0 = args[0] if len(args) > 0 else 0`
  - L8: `a1 = args[1] if len(args) > 1 else 0`

## JobMenuDesc
- TXT: `game/Inn/JobMenuDesc.txt`
- RPY: `game/Inn/JobMenuDesc.rpy`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## KidsFunctions
- TXT: `game/Inn/KidsFunctions.txt`
- RPY: `game/Inn/KidsFunctions.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $MomName (L7), arg[0] -> KidId (L107), arg[0] -> $MomName (L204), arg[0] -> $MomName (L373)
- TXT arg assignments:
  - L7: `arg[0] -> $MomName` from `$MomName=$Args[0]`
  - L107: `arg[0] -> KidId` from `KidId=args[0]`
  - L204: `arg[0] -> $MomName` from `$MomName=$args[0]`
  - L373: `arg[0] -> $MomName` from `$MomName=$args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `KidsFunctions(no params)` in `game/Inn/KidsFunctions.rpy:1`
- RPY arg usage lines:
  - none

## loadg
- TXT: `game/Inn/loadg.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: arg[0] -> KidId (L7)
- TXT arg assignments:
  - L7: `arg[0] -> KidId` from `KidId=args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## MarketPlace
- TXT: `game/Inn/MarketPlace.txt`
- RPY: `game/Inn/MarketPlace.rpy`
- Arg indexes used: `[]`
- Description: outgoing: BeckyHomeFront('') @L57
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L57: `act 'Идти в гости в дом к вдове Блэнкеншип':gt 'BeckyHomeFront', ''`
- Matching RPY labels:
  - `MarketPlace(no params)` in `game/Inn/MarketPlace.rpy:1`
  - `market_place(no params)` in `game/Inn/RuntimeCompat.rpy:84`
  - `marketplace(no params)` in `game/Inn/RuntimeCompat.rpy:88`
- RPY arg usage lines:
  - none

## Menu.Add
- TXT: `game/Inn/Menu.Add.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3, 10, 11]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.AddCondition
- TXT: `game/Inn/Menu.AddCondition.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 10]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.AddEvent
- TXT: `game/Inn/Menu.AddEvent.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.AddModule
- TXT: `game/Inn/Menu.AddModule.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 10]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.Call
- TXT: `game/Inn/Menu.Call.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 10, 11]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.Chosen
- TXT: `game/Inn/Menu.Chosen.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.Create
- TXT: `game/Inn/Menu.Create.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.Destroy
- TXT: `game/Inn/Menu.Destroy.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.Info
- TXT: `game/Inn/Menu.Info.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Menu.Time
- TXT: `game/Inn/Menu.Time.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## menu_tavernstat
- TXT: `game/Inn/menu_tavernstat.txt`
- RPY: `game/Inn/menu_tavernstat.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `menu_tavernstat(no params)` in `game/Inn/menu_tavernstat.rpy:381`
- RPY arg usage lines:
  - none

## MomDressComplaint
- TXT: `game/Inn/MomDressComplaint.txt`
- RPY: `game/Inn/MomDressComplaint.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L7)
- TXT arg assignments:
  - L7: `arg[0] -> $GirlName` from `$GirlName=$args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `mom_dress_complaint(girl_name)` in `game/Inn/MomDressComplaint.rpy:1`
- RPY arg usage lines:
  - none

## MongolTalk
- TXT: `game/Inn/MongolTalk.txt`
- RPY: `game/Inn/MongolTalk.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `MongolTalk(no params)` in `game/Inn/MongolTalk.rpy:1`
- RPY arg usage lines:
  - none

## MorningSickness
- TXT: `game/Inn/MorningSickness.txt`
- RPY: `game/Inn/MorningSickness.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlName` from `$GirlName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `morning_sickness(girl_name)` in `game/Inn/MorningSickness.rpy:1`
- RPY arg usage lines:
  - none

## NamesList
- TXT: `game/Inn/NamesList.txt`
- RPY: `game/Inn/NamesList.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $jobtype (L7)
- TXT arg assignments:
  - L7: `arg[0] -> $jobtype` from `$jobtype=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## NamesSet
- TXT: `game/Inn/NamesSet.txt`
- RPY: `game/Inn/NamesSet.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[1] -> $ArrayNameName (L21)
- TXT arg assignments:
  - L21: `arg[1] -> $ArrayNameName` from `$ArrayNameName=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - L89: `def RandomOccupCode(*_args):`
  - L108: `def RandomStreetNameCode(*_args):`
  - L111: `def RandomStallionNameCode(*_args):`

## NextDay
- TXT: `game/Inn/NextDay.txt`
- RPY: `game/Inn/NextDay.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[1] -> timepassed (L6), arg[0] -> $retlocname (L7)
- TXT arg assignments:
  - L6: `arg[1] -> timepassed` from `timepassed=Args[1]`
  - L7: `arg[0] -> $retlocname` from `$retlocname=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `NextDay(retlocname, timepassed)` in `game/Inn/NextDay.rpy:2`
- RPY arg usage lines:
  - none

## NextDay_FinishDayEvents
- TXT: `game/Inn/NextDay_FinishDayEvents.txt`
- RPY: `game/Inn/NextDay_FinishDayEvents.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `NextDay_FinishDayEvents(no params)` in `game/Inn/NextDay_FinishDayEvents.rpy:131`
- RPY arg usage lines:
  - none

## NextDay_NewDayEvents
- TXT: `game/Inn/NextDay_NewDayEvents.txt`
- RPY: `game/Inn/NextDay_NewDayEvents.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `NextDay_NewDayEvents(no params)` in `game/Inn/NextDay_NewDayEvents.rpy:4`
- RPY arg usage lines:
  - none

## NextDay_TavernDaily
- TXT: `game/Inn/NextDay_TavernDaily.txt`
- RPY: `game/Inn/NextDay_TavernDaily.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `NextDay_TavernDaily(no params)` in `game/Inn/NextDay_TavernDaily.rpy:4`
- RPY arg usage lines:
  - none

## onobjsel
- TXT: `game/Inn/onobjsel.txt`
- RPY: `game/Inn/onobjsel.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `onobjsel(no params)` in `game/Inn/onobjsel.rpy:169`
- RPY arg usage lines:
  - none

## OtherFunctionsCode
- TXT: `game/Inn/OtherFunctionsCode.txt`
- RPY: `game/Inn/OtherFunctionsCode.rpy`
- Arg indexes used: `[0, 1, 2, 3, 4, 5, 6]`
- Description: arg[0] -> i (L8), arg[0] -> y (L18), arg[3] -> x (L21)
- TXT arg assignments:
  - L8: `arg[0] -> i` from `i = args[0]`
  - L18: `arg[0] -> y` from `y = args[0]`
  - L21: `arg[3] -> x` from `x = args[3]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `OtherFunctionsCode(no params)` in `game/Inn/OtherFunctionsCode.rpy:1`
- RPY arg usage lines:
  - none

## PartEventAfterHarrassment
- TXT: `game/Inn/PartEventAfterHarrassment.txt`
- RPY: `game/Inn/PartEventAfterHarrassment.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[0] -> $GirlNamePEAH (L6), arg[1] -> GirlSlapped (L7), arg[2] -> YourReaction1 (L8) | outgoing: TavernMain(1) @L47
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNamePEAH` from `$GirlNamePEAH=$Args[0]`
  - L7: `arg[1] -> GirlSlapped` from `GirlSlapped=args[1]`
  - L8: `arg[2] -> YourReaction1` from `YourReaction1=Args[2]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L47: `act 'Вернуться к своим делам':gt 'TavernMain',1`
- Matching RPY labels:
  - `PartEventAfterHarrassment(GirlNamePEAH, GirlSlapped, YourReaction1)` in `game/Inn/PartEventAfterHarrassment.rpy:1`
- RPY arg usage lines:
  - none

## PartEventCustomerHarrassmentReaction
- TXT: `game/Inn/PartEventCustomerHarrassmentReaction.txt`
- RPY: `game/Inn/PartEventCustomerHarrassmentReaction.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNamePECHR (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNamePECHR` from `$GirlNamePECHR=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `PartEventCustomerHarrassmentReaction(GirlNamePECHR)` in `game/Inn/PartEventCustomerHarrassmentReaction.rpy:2`
- RPY arg usage lines:
  - none

## PartEventGirlHarrassmentReaction
- TXT: `game/Inn/PartEventGirlHarrassmentReaction.txt`
- RPY: `game/Inn/PartEventGirlHarrassmentReaction.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNamePEGHR (L6), arg[1] -> $JobTypePEGHR (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNamePEGHR` from `$GirlNamePEGHR=$Args[0]`
  - L7: `arg[1] -> $JobTypePEGHR` from `$JobTypePEGHR=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `PartEventGirlHarrassmentReaction(GirlNamePEGHR, JobTypePEGHR)` in `game/Inn/PartEventGirlHarrassmentReaction.rpy:2`
- RPY arg usage lines:
  - none

## PartEventGirlReactionTalk
- TXT: `game/Inn/PartEventGirlReactionTalk.txt`
- RPY: `game/Inn/PartEventGirlReactionTalk.rpy`
- Arg indexes used: `[0, 1, 2, 3, 4, 5]`
- Description: arg[0] -> $GirlNamePEGRT1 (L6), arg[1] -> $GirlNamePEGRT2 (L7), arg[2] -> $FriendVarToChange (L8), arg[3] -> DefiniteAccept (L9), arg[4] -> FriendLimit (L10), arg[5] -> SlutLimit (L11)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNamePEGRT1` from `$GirlNamePEGRT1=$Args[0]`
  - L7: `arg[1] -> $GirlNamePEGRT2` from `$GirlNamePEGRT2=$Args[1]`
  - L8: `arg[2] -> $FriendVarToChange` from `$FriendVarToChange=$Args[2]`
  - L9: `arg[3] -> DefiniteAccept` from `DefiniteAccept=Args[3]`
  - L10: `arg[4] -> FriendLimit` from `FriendLimit=Args[4]`
  - L11: `arg[5] -> SlutLimit` from `SlutLimit=Args[5]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `PartEventGirlReactionTalk(GirlNamePEGRT1, GirlNamePEGRT2, FriendVarToChange, DefiniteAccept, FriendLimit, SlutLimit)` in `game/Inn/PartEventGirlReactionTalk.rpy:4`
- RPY arg usage lines:
  - none

## PartEventYourFirstReaction
- TXT: `game/Inn/PartEventYourFirstReaction.txt`
- RPY: `game/Inn/PartEventYourFirstReaction.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $GirlNamePEYFR (L6), arg[1] -> $SecondPartFuncName (L7)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNamePEYFR` from `$GirlNamePEYFR=$Args[0]`
  - L7: `arg[1] -> $SecondPartFuncName` from `$SecondPartFuncName=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `PartEventYourFirstReaction(GirlNamePEYFR, SecondPartFuncName)` in `game/Inn/PartEventYourFirstReaction.rpy:1`
- RPY arg usage lines:
  - none

## PortStreets
- TXT: `game/Inn/PortStreets.txt`
- RPY: `game/Inn/PortStreets.rpy`
- Arg indexes used: `[0]`
- Description: outgoing: StreetClients(1, 'georgett') @L37; StreetClients(1, 'liza') @L41; StreetClients(1, 'georgett') @L48
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L37: `act 'Пойти проверить подворотню':gt 'StreetClients',1, 'georgett'`
  - L41: `act 'Пойти проверить подворотню':gt 'StreetClients',1, 'liza'`
  - L48: `if HadSex[$GirlNamePS1]>0: act 'Пойти проверить подворотню':gt 'StreetClients',1, 'georgett'`
- Matching RPY labels:
  - `PortStreets(no params)` in `game/Inn/PortStreets.rpy:2`
  - `port_streets(no params)` in `game/Inn/RuntimeCompat.rpy:104`
- RPY arg usage lines:
  - L7: `if _args and len(_args) > 0 and _args[0] == 'FirstTalk':`

## PregnancyCheck
- TXT: `game/Inn/PregnancyCheck.txt`
- RPY: `game/Inn/PregnancyCheck.rpy`
- Arg indexes used: `[0, 1, 2, 3, 4, 5]`
- Description: arg[0] -> $GirlNamePCHK (L6), arg[3] -> $dadsname (L7), arg[4] -> IsDudeRandom (L8), arg[5] -> $DadsNameType (L9)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNamePCHK` from `$GirlNamePCHK=$ARGS[0]`
  - L7: `arg[3] -> $dadsname` from `$dadsname=$ARGS[3]`
  - L8: `arg[4] -> IsDudeRandom` from `IsDudeRandom=Args[4]`
  - L9: `arg[5] -> $DadsNameType` from `$DadsNameType=$Args[5]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `pregnancy_check(girl, where, count, partner)` in `game/Inn/AmandaLegareDanceSequence.rpy:130`
  - `PregnancyCheck(girl_name, cum_place, repeat_count, dad_name='', is_dude_random=0, dad_name_type='')` in `game/Inn/PregnancyCheck.rpy:149`
- RPY arg usage lines:
  - none

## RelationshipDesc1
- TXT: `game/Inn/RelationshipDesc1.txt`
- RPY: `game/Inn/RelationshipDesc1.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameRD1 (L7)
- TXT arg assignments:
  - L7: `arg[0] -> $GirlNameRD1` from `$GirlNameRD1=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## saveg
- TXT: `game/Inn/saveg.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## SetTavernServiceLevels
- TXT: `game/Inn/SetTavernServiceLevels.txt`
- RPY: `game/Inn/SetTavernServiceLevels.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `SetTavernServiceLevels(no params)` in `game/Inn/SetTavernServiceLevels.rpy:26`
- RPY arg usage lines:
  - none

## SexEventsTableCode
- TXT: `game/Inn/SexEventsTableCode.txt`
- RPY: `game/Inn/SexEventsTableCode.rpy`
- Arg indexes used: `[0, 1, 2, 3, 4]`
- Description: arg[0] -> $GirlNameSE (L7), arg[1] -> timeSE (L8), arg[0] -> $GirlNameSE (L35), arg[1] -> EventTypeSE (L36)
- TXT arg assignments:
  - L7: `arg[0] -> $GirlNameSE` from `$GirlNameSE=$Args[0]`
  - L8: `arg[1] -> timeSE` from `timeSE=Args[1]`
  - L35: `arg[0] -> $GirlNameSE` from `$GirlNameSE=$Args[0]`
  - L36: `arg[1] -> EventTypeSE` from `EventTypeSE=Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `SexEventsTableCode(no params)` in `game/Inn/SexEventsTableCode.rpy:264`
- RPY arg usage lines:
  - none

## SexPort
- TXT: `game/Inn/SexPort.txt`
- RPY: `game/Inn/SexPort.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[1] -> $GirlNameSP (L8)
- TXT arg assignments:
  - L8: `arg[1] -> $GirlNameSP` from `$GirlNameSP=$args[1]`
- Incoming links with explicit args:
  - `IntGeorgettTalk` L272: `gt 'SexPort',1, 'georgett'`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `sex_port(no params)` in `game/Inn/IntGeorgettTalk.rpy:262`
  - `SexPort(args0=0, args1="")` in `game/Inn/SexPort.rpy:1`
- RPY arg usage lines:
  - none

## SexProstTavern
- TXT: `game/Inn/SexProstTavern.txt`
- RPY: `game/Inn/SexProstTavern.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[1] -> $GirlNameSP (L8)
- TXT arg assignments:
  - L8: `arg[1] -> $GirlNameSP` from `$GirlNameSP=$args[1]`
- Incoming links with explicit args:
  - `IntGeorgettTalk` L269: `gt 'SexProstTavern',1, 'georgett'`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `sex_prost_tavern(no params)` in `game/Inn/IntGeorgettTalk.rpy:258`
  - `SexProstTavern(args0=0, args1="")` in `game/Inn/SexProstTavern.rpy:1`
- RPY arg usage lines:
  - none

## SherwoodTravel
- TXT: `game/Inn/SherwoodTravel.txt`
- RPY: `game/Inn/SherwoodTravel.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> OnHorse (L6)
- TXT arg assignments:
  - L6: `arg[0] -> OnHorse` from `OnHorse=args[0]`
- Incoming links with explicit args:
  - `TavernStable` L28: `xgt 'SherwoodTravel', 1`
  - `TavernStable` L37: `xgt 'SherwoodTravel', 0`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `SherwoodTravel(no params)` in `game/Inn/SherwoodTravel.rpy:19`
- RPY arg usage lines:
  - L23: `_arg_list = _args or ()`

## ShowAmandaPortrait
- TXT: `game/Inn/ShowAmandaPortrait.txt`
- RPY: `game/Inn/ShowAmandaPortrait.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowAmandaPortrait(no params)` in `game/Inn/ShowAmandaPortrait.rpy:1`
- RPY arg usage lines:
  - none

## ShowBeckyPortrait
- TXT: `game/Inn/ShowBeckyPortrait.txt`
- RPY: `game/Inn/ShowBeckyPortrait.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowBeckyPortrait(no params)` in `game/Inn/ShowBeckyPortrait.rpy:1`
- RPY arg usage lines:
  - none

## ShowChurchDraupnirList
- TXT: `game/Inn/ShowChurchDraupnirList.txt`
- RPY: `game/Inn/ShowChurchDraupnirList.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowChurchDraupnirList(no params)` in `game/Inn/ShowChurchDraupnirList.rpy:3`
- RPY arg usage lines:
  - none

## ShowCurrentCockState
- TXT: `game/Inn/ShowCurrentCockState.txt`
- RPY: `game/Inn/ShowCurrentCockState.rpy`
- Arg indexes used: `[0, 1]`
- Description: arg[0] -> $DudeName (L6), arg[1] -> $DudeNameFull (L7), arg[1] -> $DudeNameFull2 (L8)
- TXT arg assignments:
  - L6: `arg[0] -> $DudeName` from `$DudeName=$Args[0]`
  - L7: `arg[1] -> $DudeNameFull` from `$DudeNameFull=$Args[1]`
  - L8: `arg[1] -> $DudeNameFull2` from `$DudeNameFull2=$Args[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowCurrentCockState(DudeName="You", DudeNameFull="", DudeNameFull2="")` in `game/Inn/ShowCurrentCockState.rpy:1`
  - `show_current_cock_state(dude_name="You", dude_name_full="", dude_name_full2="")` in `game/Inn/ShowCurrentCockState.rpy:75`
- RPY arg usage lines:
  - none

## ShowCurrentSex
- TXT: `game/Inn/ShowCurrentSex.txt`
- RPY: `game/Inn/ShowCurrentSex.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> $GirlNameSCS (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameSCS` from `$GirlNameSCS=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowCurrentSex(GirlNameSCS="")` in `game/Inn/ShowCurrentSex.rpy:1`
- RPY arg usage lines:
  - none

## ShowGeorgettPortrait
- TXT: `game/Inn/ShowGeorgettPortrait.txt`
- RPY: `game/Inn/ShowGeorgettPortrait.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowGeorgettPortrait(no params)` in `game/Inn/ShowGeorgettPortrait.rpy:1`
- RPY arg usage lines:
  - none

## ShowGirlSexHistory
- TXT: `game/Inn/ShowGirlSexHistory.txt`
- RPY: `game/Inn/ShowGirlSexHistory.rpy`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowGirlSexHistory(args0="")` in `game/Inn/ShowGirlSexHistory.rpy:1`
- RPY arg usage lines:
  - none

## ShowImage
- TXT: `game/Inn/ShowImage.txt`
- RPY: `game/Inn/ShowImage.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowImage(args0="", args1="", args2="")` in `game/Inn/MarketPlace.rpy:69`
  - `show_image(args0="", args1="", args2="")` in `game/Inn/RuntimeCompat.rpy:70`
- RPY arg usage lines:
  - none

## ShowImageSeq
- TXT: `game/Inn/ShowImageSeq.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowImageSeq(args0="", args1="", args2="", args3=0)` in `game/Inn/MarketPlace.rpy:89`
  - `show_image_seq(args0="", args1="", args2="", args3=0)` in `game/Inn/RuntimeCompat.rpy:75`
- RPY arg usage lines:
  - none

## ShowLizaPortrait
- TXT: `game/Inn/ShowLizaPortrait.txt`
- RPY: `game/Inn/ShowLizaPortrait.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ShowLizaPortrait(no params)` in `game/Inn/ShowLizaPortrait.rpy:1`
- RPY arg usage lines:
  - none

## SlutFriendsIncrease
- TXT: `game/Inn/SlutFriendsIncrease.txt`
- RPY: `game/Inn/SlutFriendsIncrease.rpy`
- Arg indexes used: `[0, 1, 2, 3, 4, 5, 6]`
- Description: arg[0] -> $GirlNameSFI (L6), arg[1] -> LimitFriend (L7), arg[2] -> FriendChance (L8), arg[3] -> IncDecrFriends (L9), arg[4] -> LimitSluttiness (L10), arg[5] -> SluttinessChance (L11), arg[6] -> IncDecrSluttiness (L12)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameSFI` from `$GirlNameSFI=$Args[0]`
  - L7: `arg[1] -> LimitFriend` from `LimitFriend=Args[1]`
  - L8: `arg[2] -> FriendChance` from `FriendChance=Args[2]`
  - L9: `arg[3] -> IncDecrFriends` from `IncDecrFriends=Args[3]`
  - L10: `arg[4] -> LimitSluttiness` from `LimitSluttiness=Args[4]`
  - L11: `arg[5] -> SluttinessChance` from `SluttinessChance=Args[5]`
  - L12: `arg[6] -> IncDecrSluttiness` from `IncDecrSluttiness=Args[6]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `slut_friends_increase(girl, a, b, c, d, e, f)` in `game/Inn/EventAmandaLegareCreateDance.rpy:54`
  - `SlutFriendsIncrease(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness)` in `game/Inn/SlutFriendsIncrease.rpy:24`
- RPY arg usage lines:
  - none

## stat
- TXT: `game/Inn/stat.txt`
- RPY: `game/Inn/stat.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `stat(no params)` in `game/Inn/stat.rpy:2`
- RPY arg usage lines:
  - none

## StolyarWorkshop
- TXT: `game/Inn/StolyarWorkshop.txt`
- RPY: `game/Inn/StolyarWorkshop.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `StolyarWorkshop(no params)` in `game/Inn/StolyarWorkshop.rpy:1`
- RPY arg usage lines:
  - none

## StreetClients
- TXT: `game/Inn/StreetClients.txt`
- RPY: `game/Inn/StreetClients.rpy`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - `PortStreets` L37: `act 'Пойти проверить подворотню':gt 'StreetClients',1, 'georgett'`
  - `PortStreets` L41: `act 'Пойти проверить подворотню':gt 'StreetClients',1, 'liza'`
  - `PortStreets` L48: `if HadSex[$GirlNamePS1]>0: act 'Пойти проверить подворотню':gt 'StreetClients',1, 'georgett'`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `street_clients(client_type, girl_name, time)` in `game/Inn/StreetClients.rpy:4`
- RPY arg usage lines:
  - none

## StreetTavern
- TXT: `game/Inn/StreetTavern.txt`
- RPY: `game/Inn/StreetTavern.rpy`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `street_tavern(no params)` in `game/Inn/RuntimeCompat.rpy:80`
  - `StreetTavern(no params)` in `game/Inn/StreetTavern.rpy:1`
- RPY arg usage lines:
  - none

## SumArray
- TXT: `game/Inn/SumArray.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: arg[0] -> $SumArrayName (L6)
- TXT arg assignments:
  - L6: `arg[0] -> $SumArrayName` from `$SumArrayName=$Args[0]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.ColumnsCount
- TXT: `game/Inn/Table.ColumnsCount.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Copy
- TXT: `game/Inn/Table.Copy.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Create
- TXT: `game/Inn/Table.Create.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 10]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.CreateIndex
- TXT: `game/Inn/Table.CreateIndex.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 10, 11, 12]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Current
- TXT: `game/Inn/Table.Current.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.DeleteLine
- TXT: `game/Inn/Table.DeleteLine.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 10, 11, 12, 13]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.DeleteLines
- TXT: `game/Inn/Table.DeleteLines.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3, 4, 10, 11, 12, 13, 14]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Destroy
- TXT: `game/Inn/Table.Destroy.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.DestroyIndex
- TXT: `game/Inn/Table.DestroyIndex.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.FindValue
- TXT: `game/Inn/Table.FindValue.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3, 4, 10, 11, 12, 13, 14]`
- Description: arg[1] -> Result (L17), arg[1] -> Result (L18)
- TXT arg assignments:
  - L17: `arg[1] -> Result` from `$ARGS[13]=$otg_Таб_ФС+' Result=ARGS[1]'`
  - L18: `arg[1] -> Result` from `$ARGS[14]=$otg_Таб_ФЧ+' Result=ARGS[1]'`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.First
- TXT: `game/Inn/Table.First.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.GetValue
- TXT: `game/Inn/Table.GetValue.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[1] -> Result (L16)
- TXT arg assignments:
  - L16: `arg[1] -> Result` from `Result=ARGS[1]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Info
- TXT: `game/Inn/Table.Info.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.IsFirst
- TXT: `game/Inn/Table.IsFirst.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.IsLast
- TXT: `game/Inn/Table.IsLast.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Last
- TXT: `game/Inn/Table.Last.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.LinesCount
- TXT: `game/Inn/Table.LinesCount.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3, 4, 10, 11, 12, 13, 14]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.LineToArray
- TXT: `game/Inn/Table.LineToArray.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.NewColumn
- TXT: `game/Inn/Table.NewColumn.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.NewLine
- TXT: `game/Inn/Table.NewLine.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 10, 11, 12]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Next
- TXT: `game/Inn/Table.Next.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Previous
- TXT: `game/Inn/Table.Previous.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.RandomLine
- TXT: `game/Inn/Table.RandomLine.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Select
- TXT: `game/Inn/Table.Select.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3, 4, 10, 11, 12, 13, 14]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.SetValue
- TXT: `game/Inn/Table.SetValue.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Show
- TXT: `game/Inn/Table.Show.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 10, 11, 12]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Sort
- TXT: `game/Inn/Table.Sort.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Table.Value
- TXT: `game/Inn/Table.Value.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 12]`
- Description: arg[12] -> Result (L23)
- TXT arg assignments:
  - L23: `arg[12] -> Result` from `Result=ARGS[12]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## TavernAmandaRoom
- TXT: `game/Inn/TavernAmandaRoom.txt`
- RPY: `game/Inn/TavernAmandaRoom.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `TavernAmandaRoom(no params)` in `game/Inn/TavernAmandaRoom.rpy:1`
- RPY arg usage lines:
  - none

## TavernGloryHole
- TXT: `game/Inn/TavernGloryHole.txt`
- RPY: `game/Inn/TavernGloryHole.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `TavernGloryHole(no params)` in `game/Inn/TavernGloryHole.rpy:1`
- RPY arg usage lines:
  - none

## TavernHelp
- TXT: `game/Inn/TavernHelp.txt`
- RPY: `game/Inn/TavernHelp.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `TavernHelp(no params)` in `game/Inn/TavernHelp.rpy:1`
- RPY arg usage lines:
  - none

## TavernMain
- TXT: `game/Inn/TavernMain.txt`
- RPY: `game/Inn/TavernMain.rpy`
- Arg indexes used: `[0]`
- Description: arg[0] -> BlockEvents (L24) | outgoing: TavernProstClients(1, 'georgett') @L66; TavernProstClients(1, 'liza') @L72; TavernProstClients(1, 'liza') @L84; TavernProstClients(1, 'georgett') @L95
- TXT arg assignments:
  - L24: `arg[0] -> BlockEvents` from `BlockEvents=args[0]`
- Incoming links with explicit args:
  - `EventAmandaLizettTalk` L41: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventAmandaLizettTalk` L52: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventAmandaLizettTalk` L62: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventAmandaLizettTalk` L72: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventAmandaLizettTalk` L81: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventAmandaLizettTalk` L96: `gt 'TavernMain',1`
  - `EventAmandaLizettTalk2` L51: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventFightSmall` L42: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventFightSmall` L52: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventFightSmall` L62: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventFightSmall` L72: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventFightSmall` L84: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventFightSmall` L99: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventWineForDance` L23: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventWineForDance` L32: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `EventWineForDance` L41: `act 'Вернуться к своим делам':gt 'TavernMain',1`
  - `PartEventAfterHarrassment` L47: `act 'Вернуться к своим делам':gt 'TavernMain',1`
- Outgoing links with explicit args:
  - L66: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'georgett'`
  - L72: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'liza'`
  - L84: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'liza'`
  - L95: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'georgett'`
- Matching RPY labels:
  - `TavernMain(no params)` in `game/Inn/TavernMain.rpy:1`
  - `tavern_main(no params)` in `game/Inn/TavernMain.rpy:202`
- RPY arg usage lines:
  - L78: `_arg_list = _args or ()`

## TavernMyRoom
- TXT: `game/Inn/TavernMyRoom.txt`
- RPY: `game/Inn/TavernMyRoom.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `TavernMyRoom(no params)` in `game/Inn/TavernMyRoom.rpy:1`
- RPY arg usage lines:
  - none

## TavernProstClients
- TXT: `game/Inn/TavernProstClients.txt`
- RPY: `game/Inn/TavernProstClients.rpy`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - `TavernMain` L66: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'georgett'`
  - `TavernMain` L72: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'liza'`
  - `TavernMain` L84: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'liza'`
  - `TavernMain` L95: `act 'Пойти проверить отдельную комнату':gt 'TavernProstClients',1, 'georgett'`
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `TavernProstClients(client_type=1, girl_name="")` in `game/Inn/TavernProstClients.rpy:1`
- RPY arg usage lines:
  - none

## TavernShowImage
- TXT: `game/Inn/TavernShowImage.txt`
- RPY: `game/Inn/TavernShowImage.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `TavernShowImage(no params)` in `game/Inn/TavernShowImage.rpy:2`
- RPY arg usage lines:
  - none

## TavernStable
- TXT: `game/Inn/TavernStable.txt`
- RPY: `game/Inn/TavernStable.rpy`
- Arg indexes used: `[]`
- Description: outgoing: SherwoodTravel(1) @L28; SherwoodTravel(0) @L37
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - L28: `xgt 'SherwoodTravel', 1`
  - L37: `xgt 'SherwoodTravel', 0`
- Matching RPY labels:
  - `TavernStable(no params)` in `game/Inn/TavernStable.rpy:1`
- RPY arg usage lines:
  - none

## WhoreNextDayClients
- TXT: `game/Inn/WhoreNextDayClients.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[0] -> $GirlNameWNDC (L6), arg[1] -> MaxClients (L7), arg[2] -> GloryHoleMax (L8)
- TXT arg assignments:
  - L6: `arg[0] -> $GirlNameWNDC` from `$GirlNameWNDC=$Args[0]`
  - L7: `arg[1] -> MaxClients` from `MaxClients=Args[1]`
  - L8: `arg[2] -> GloryHoleMax` from `GloryHoleMax=Args[2]`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## WineStore
- TXT: `game/Inn/WineStore.txt`
- RPY: `game/Inn/WineStore.rpy`
- Arg indexes used: `[]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `WineStore(no params)` in `game/Inn/WineStore.rpy:4`
- RPY arg usage lines:
  - none

## ZaletOpinionCalc
- TXT: `game/Inn/ZaletOpinionCalc.txt`
- RPY: `game/Inn/ZaletOpinionCalc.rpy`
- Arg indexes used: `[0, 1, 2]`
- Description: arg[1] -> $Result (L110), arg[1] -> $Result (L112), arg[1] -> $Result (L121), arg[1] -> $Result (L123), arg[1] -> $Result (L216), arg[0] -> $Result (L228)
- TXT arg assignments:
  - L110: `arg[1] -> $Result` from `$Result=$args[1]+ ', такой милый ' + Trim(Replace(lcase($args[2]),'неизвестный','')) + '. Даже не знаю, где он сейчас, помнит ли меня...'`
  - L112: `arg[1] -> $Result` from `$Result=$args[1]+ ', ' + Trim(Replace(lcase($args[2]),'неизвестный','')) + ', я с ним и виделась-то немного. Так, перепихнулись и разбежались'`
  - L121: `arg[1] -> $Result` from `$Result=$args[1]+ ', такой милый мальчик. Интересно, помнит ли он меня...'`
  - L123: `arg[1] -> $Result` from `$Result=$args[1]+ ', парень из соседнего квартала, да ты его знаешь. Дала я ему, уболтал он меня, гоблин языкастый!'`
  - L216: `arg[1] -> $Result` from `$Result=$args[1]`
  - L228: `arg[0] -> $Result` from `$Result=args[0]+ ' раза в меня кончил, вот и залетела я.'`
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - `ZaletOpinionCalc(no params)` in `game/Inn/ZaletOpinionCalc.rpy:1`
- RPY arg usage lines:
  - none

## Меню.{Обработка}
- TXT: `game/Inn/Меню.{Обработка}.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 3]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Таб.{IDКолонки}
- TXT: `game/Inn/Таб.{IDКолонки}.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Таб.{IDСтроки}
- TXT: `game/Inn/Таб.{IDСтроки}.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 11, 12, 13, 14]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Таб.{ПолучитьФильтр}
- TXT: `game/Inn/Таб.{ПолучитьФильтр}.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 3]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none

## Таб.{Строка2Массив}
- TXT: `game/Inn/Таб.{Строка2Массив}.txt`
- RPY: `missing exact-name file`
- Arg indexes used: `[0, 1, 2, 10, 11, 12]`
- Description: No explicit arg assignment in TXT.
- TXT arg assignments:
  - none
- Incoming links with explicit args:
  - none
- Outgoing links with explicit args:
  - none
- Matching RPY labels:
  - none
- RPY arg usage lines:
  - none
