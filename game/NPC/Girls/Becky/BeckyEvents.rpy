# Becky atomic thin events for BeckyHomeVisits thread (dinner guest multi-visit)
# This file follows the exact engine standard and user rules:
# - Thin labels only (one stage per label)
# - All counters live inside the event
# - thread.advance() ONLY when THIS event's stage completion conditions are met
# - Use rand_int() for all random chances (no direct rand())
# - Direct $ Becky.var[...] / Eddie.var[...] assignments (NO globals(), NO store. hacks after purge)
# - Classic menu: only, no MenuItem.append
# - Becky-owned counters mutate through Becky methods; shared scene labels stay callable only for non-Becky participants.
# - Full original source file names in comments for every event
# - Never touches script.rpy intro placeholders
#
# References for this file:
# - textLocRef\GeorgettBeckyVisit.txt (primary orgy + player minet/cum choices)
# - textLocRef\IntBeckyGuest.txt (trigger: if Becky.var['EddieWhoreHome']=4 and dinnertime=5: gs 'GeorgettBeckyVisit')
# - game/NPC/Girls/Georgett/InitGeorgett.rpy (georgett_eddie_peekhole_jealous sets EddieWhoreHome=4 + peekhole context)
# - game/Inn/GeorgettBeckyVisit.rpy (detailed fallback engine for the location)
# - game/Inn/IntBeckyGuest.rpy (dinner loop, KidsWatchStepsCode / BeckyGuestKidsWatchStepsCode, full guest menu engine)
# - game/NPC/Girls/Becky/IntBeckyGuest.rpy (port of kids watch + dinner helpers)
# - game/NPC/Girls/Becky/IntBeckyGuest.rpy (port of kids watch + dinner helpers)
#
# Thread registration example (add to beckyThreadList in this file or Init):
# beckyThreadList = [
#     LThreadData(1, "becky", "BeckyHomeVisits", "EddieWhoreHome==4 or Becky.var.get('visitedhome',0)>=1", [
#         ("becky_home_dinner_arrival", ...),
#         ...
#         ("becky_home_georgett_visit", None, None, None, 1, None, "EddieWhoreHome==4 and dinnertime==5", None, "BeckyHome", "eat", 5),
#     ]),
# ]

# =============================================================================
# GEORGETTE / BECKY CROSSOVER
# =============================================================================
# The playable crossover scene is owned by game/NPC/Girls/Becky/GeorgettBeckyVisit.rpy.
# Do not keep a second implementation here; StoryEventRuntime points directly to that label.

# =============================================================================
# BLACKWOOD (ex-SHERWOOD) QUEST - Becky trade run to Kunidell / Cundail elves
# =============================================================================
# The arc after Eddie gets beaten by the "обездоленные" (Robin gang) in the Sherwood cut.
# Triggered rarely on NewDay when home guest progress + friendship high.
# For ~12 days after EddieRobbedDay: Becky covers morning GroceryStore shifts.
# Eddie black eye talks (multi-stage in IntEddieTalk) eventually reveal details + set KnowSherwood.
# Becky offers regular profitable veggie hauls to the elves (BeckyQuestInit at GroceryStore).
# Full road danger + negotiation/robbery in SherwoodTravel.
# We use modern "Blackwood" naming alongside legacy flags for the rename.

label becky_eddie_black_eye:
    # Atomic NewDay trigger event for the robbery (Eddie returns beaten).
    # References:
    #   textLocRef\NextDay_NewDayEvents.txt:118 (the exact rare condition + EddieRobbedDay set + DailyEventsList wiring to BeckyQuestInit)
    #   textLocRef\GroceryStore.txt:74 (black eye description shown in morning while window active)
    #   devdocs/characters/full_logic/becky_full_logic.md and IntEddieTalk.txt (EddieRobbedDay +12 day window for talks)
    #   InitBecky.txt (EddieRobbedDay default = 0)
    #
    # In real game this is called from NewDay engine. Here we simulate the rare roll with rand_int.
    # Sets EddieRobbedDay, marks EddieRobbed=1 to prevent re-trigger, schedules the quest daily.

    show screen main_ui
    $ becky = getPersonInfo("becky")

    $ Becky.var.setdefault("EddieRobbed", 0)
    $ Becky.var.setdefault("EddieRobbedDay", 0)
    $ Becky.var.setdefault("SherwoodSuspect", 0)

    if Becky.var.get("EddieRobbed", 0) == 1:
        return   # already happened this arc

    # Rare 1/6 roll (exact match to source). Only if guest progress + friends sufficient.
    if (Becky.var.get("visitedhome", 0) >= 5 and
            Becky.rel >= 15 and
            procedural_randint(1, 6, "becky_eddie_black_eye_%s" % people_to_int(dayspassed, 0)) == 1 and dayspassed > 0):

        $ Becky.var["EddieRobbedDay"] = dayspassed
        $ Becky.var["EddieRobbed"] = 1

        $ MainTxt = "Эдди вернулся с синяком под глазом и распухшим ухом. Он явно получил хорошую взбучку где-то за городом.\n\n"
        $ MainTxt += "В ближайшие дни (примерно две недели) Бекки будет чаще появляться утром в лавке, прикрывая сына."

        $ CurLocDesc = MainTxt

        # Wire the daily quest offer (in real engine this goes through DailyEventsList / CheckDailyEvent)
        # For the thin event we just mark that the offer is now available at GroceryStore.
        $ Becky.var["SherwoodQuestScheduled"] = 1

        if thread is not None:
            $ thread.advance()

        $ Becky.finish_talk()

        # Note: the actual "Eddie black eye visible + talk options" appear automatically in GroceryStore while the +12 day window is open.
        # The detailed multi-stage "Спросить о синяке" tree lives in IntEddieTalk (with FingalTalk progression and the famous "отмудохали" line).
        return

    return


label becky_blackwood_quest_start:
    # The core offer scene (BeckyQuestInit) — Becky pulls the player aside at GroceryStore and pitches the regular Kunidell/Cundail trade run.
    # References:
    #   textLocRef\BeckyQuestInit.txt (full pitch: "Стефан, я вижу ты человек надежный...", 4 мешка по 50м, 50-300 profit, morning except Sunday)
    #   textLocRef\IntBeckyTalkSherwood.txt (follow-up questions about the "загвоздка", elves, son, road through Sherwood/Blackwood)
    #   textLocRef\NextDay_NewDayEvents.txt (how the daily event fires this)
    #   textLocRef\GroceryStore.txt (the morning context + black eye note)
    #   game/Inn/SherwoodTravel.rpy + game/NPC/Secondary/SherwoodTravel.rpy (the actual dangerous road + Robin encounters + profit return)
    #
    # Sets TradeOffer, possible early SherwoodWarn (if high relationship), then player can dig via IntBeckyTalkSherwood.
    # Thread advances on acceptance of the offer or full admission of the danger.

    show screen main_ui
    $ becky = getPersonInfo("becky")

    python:
        Becky.var.setdefault("TradeOffer", 0)
        Becky.var.setdefault("SherwoodWarn", 0)
        Becky.var.setdefault("SherwoodSuspect", 0)
        Becky.var.setdefault("EddieRobbedDay", 0)

    if Becky.var.get("TradeOffer", 0) >= 1:
        # Already pitched — fall through to detailed talk for follow-ups
        if renpy.has_label("IntBeckyTalkSherwood"):
            call IntBeckyTalkSherwood from _call_blackwood_talk_fallback
        return

    $ MainTxt = "«Стефан, я вижу ты человек надежный, тебе можно доверять,» неожиданно обратилась к вам Бекки, прервав ваше глубокомысленное разглядывание выложенных на продажу огурцов и прочей репы.\n\n"
    $ MainTxt += "Вы попытались ответить что-то про веру и надежность, но запутались.\n\n"
    $ MainTxt += "«Вот и ладушки,» обрадованно сказала вдова. «Заработать хочешь?»\n\n"

    $ CurLocDesc = MainTxt

    # Classic menu for the initial choice (exact from BeckyQuestInit.txt)
    menu:
        "А кто ж не хочет?":
            $ MainTxt += "«Это правильно, денежки все любят,» согласилась с вами вдова.\n\n"

            $ Becky.var["TradeOfferText"] = "«Значит так, может ты слышал, часах в 6 езды от города есть эльфийский замок. Куниделл называется. Так вот, с едой там дела не очень обстоят. Эльфы, сам понимаешь, что с них взять. Каждую грядку им надо, видишь ли, расположить в согласии с музыкой сфер, на это у них время есть. А скажем полить или прополоть — так на это у них ни желания, ни времени нет.»\n\n«И как урожаи у них?»\n\n«А никак. Поэтому и цены у них повыше. В общем смотри. Тебе нужна лошадь. Я тебе продам 4 больших мешка всяких овощей — по полквинтала каждый, 50 мараведи штука. Навьючишь их, утром в путь, там продашь с наваром не меньше, чем полсотни мараведи. А может и три сотни выручишь. А на следующий день опять так можешь. Эльфы они такие, хоть и возвышенные, но прожорливые. В общем, утром в любой день заходи, ну кроме воскресенья, конечно.»"

            $ MainTxt += Becky.var["TradeOfferText"]

            if Becky.rel >= 17 and Becky.stats.get("orgasms_given", 0) >= 9:
                $ MainTxt += "\n\n«Правда, есть тут небольшая загвоздка,» чуть менее радостным тоном заметила Ребекка, «а, впрочем ерунда, вряд ли это что серьезное.»"
                $ Becky.var["SherwoodWarn"] = 1
                $ Becky.var["SherwoodSuspect"] += 1

            $ Becky.var["TradeOffer"] = 1

            if thread is not None:
                $ thread.advance()

            $ Becky.finish_talk()
            $ CurLocDesc = MainTxt

            # Now player can ask follow-ups via the Sherwood talk label (or fall to detailed engine)
            if renpy.has_label("IntBeckyTalkSherwood"):
                call IntBeckyTalkSherwood from _call_blackwood_offer_talk
            return

        "Неа. Меня ни работа, ни деньги не интересуют":
            $ MainTxt += "«Ну ладно, раз так. Но если передумаешь, то не стесняйся, спроси,» разочарованно сказала вдовушка."
            $ Becky.var["TradeOffer"] = 2

            $ Becky.finish_talk()
            $ CurLocDesc = MainTxt
            jump MarketPlace
            return

    return


label becky_blackwood_talk_reveal:
    # Key admission moment: player presses about the road danger after knowing about Eddie's beating.
    # This is the "Насчет дороги в Куниделл" option that fully reveals the bandits and sets modern KnowBlackwood.
    # References: textLocRef\IntBeckyTalkSherwood.txt (the long admission paragraph + AdmitSherwood + high SherwoodSuspect)

    show screen main_ui
    $ becky = getPersonInfo("becky")

    $ Becky.var.setdefault("KnowSherwood", 0)
    $ Becky.var.setdefault("KnowBlackwood", 0)
    $ Becky.var.setdefault("AdmitSherwood", 0)
    $ Becky.var.setdefault("SherwoodSuspect", 0)
    $ Becky.var.setdefault("TradeOffer", 0)

    if Becky.var.get("AdmitSherwood", 0) >= 1 or Becky.var.get("KnowBlackwood", 0) == 1:
        return

    $ MainTxt = "«Дорожка в Куниделл, случаем не через Шервудский лес проходит?» невинно осведомились вы.\n\n"
    $ MainTxt += "«Через него, это верно. Только какой там лес, от него и не осталось почти ничего,» заметно нервничая ответила вам Ребекка.\n\n"
    $ MainTxt += "«А там никто, случаем, не пошаливает? Грабеж, все такое?»\n\n"
    $ MainTxt += "«Ну как тебе сказать... Дело в том, что да, ты прав, в Куниделл надо ехать через Шервудский лес. Ну, вернее уже не лес, но это не важно. Там уже давно как эти засели, как их там, обездоленные. Говорят, что мол наша добрая герцогиня в их несчастьях и горькой судьбинушке виновата. Раньше от них вреда особого не было, так, собирали по паре десятков мараведи на пропитание. А недавно разухабились, сыночка моего ненаглядного побили, товар отобрали, лошадь отобрали. Так я и решила, ты паренек смышленый, что-нибудь придумаешь. И мне выгода, и тебе прибыток.»"

    $ Becky.var["SherwoodSuspect"] += 10
    $ Becky.var["AdmitSherwood"] = 1
    $ Becky.var["KnowBlackwood"] = 1          # modern rename flag
    $ Becky.var["KnowSherwood"] = 1           # keep legacy for compatibility

    if thread is not None:
        $ thread.advance()

    $ Becky.finish_talk()
    $ CurLocDesc = MainTxt

    # Further conversation (robbery consolation, "you didn't warn me", how to deal with Robin) lives in the detailed IntBeckyTalkSherwood or later thin stages.
    if renpy.has_label("IntBeckyTalkSherwood"):
        call IntBeckyTalkSherwood from _call_blackwood_reveal_talk
    return


# =============================================================================
# ROBIN + MONGOL VOUCH + ZIMMER MISSION (Blackwood part 2)
# =============================================================================
# Mongol released from stocks (Mongol.var["StocksReleased"]) → later vouch to Robin
# → Robin.var["MongolSafePass"] = 1 lets MC pass the cut without losing horse/money.
# Zimmer (guard boss) gave mission to deal with outlaws disrupting trade.
# On the way to Cunidale (for Becky veggies) player reaches the bandit camp.
# Choice: destroy the camp (violent) or solve peacefully for Zimmer quest.
# This file owns the thin milestone events + thread visibility.
# Full camp content + Cunidale village + detailed third Blackwood part = future work (see TODO).

label robin_mongol_vouch_safe_passage:
    # Triggered when the player has the Mongol release flag and first meets Robin (or returns).
    # Mongol (after being freed from stocks by player) puts in a good word.
    # This saves the MC's ass (horse + money) from the usual "пожертвование" shakedown.
    # References:
    #   tools/external_click_play_test.py (Mongol.var["StocksReleased"], Robin.var["MongolSafePass"])
    #   textLocRef\MongolTalk.txt + stocks story events in StoryEventRuntime
    #   textLocRef\SherwoodTravel.txt + IntRobinTalk.txt (current robbery path we now bypass)
    #   game/NPC/Secondary/InitSecondaryNPC.rpy (Robin registration + MongolSafePass default)

    show screen main_ui
    $ robin = getPersonInfo("robin") if "robin" in dir() else None

    $ Mongol.ensure_story_defaults()
    $ Robin.ensure_story_defaults()

    if Mongol.var.get("StocksReleased", 0) == 0 or Robin.var.get("MongolSafePass", 0) == 1:
        return

    $ MainTxt = "Когда вы подходите к группе в зелёных трико, один из бандитов узнаёт вас и дёргает Робина за рукав.\n\n"
    $ MainTxt += "«Йо, браза, это тот самый трактирщик. Монгол велел своих предупредить: этот чувак не мазафака, он его из колодок вытащил.»\n\n"
    $ MainTxt += "Робин смотрит на вас с новым интересом, потом широко улыбается.\n\n"
    $ MainTxt += "«Вот это другое дело, бразар. За Монгола уважуха. Раз наш человек сказал, что ты браза, значит сегодня ты едешь как браза. Деньги при себе оставь, коняшку тоже. Но если кто спросит — мы тебя не пропускали. Социяльная ответственность, понимаешь?»\n\n"

    $ Robin.var["MongolSafePass"] = 1
    $ Robin.var["KnowHim"] = 1

    if thread is not None:
        $ thread.advance()

    $ CurLocDesc = MainTxt

    # Safe passage granted — no robbery this time. Player can continue to Cunidale.
    # Later visits may still have complications unless further relationship built.
    return


label zimmer_bandit_camp_choice:
    # Milestone on the road to Cunidale (elven village for Becky's vegetable trade).
    # Player has reached the bandit camp.
    # Two paths (this is only the choice point for now):
    # 1. Violent: destroy/eliminate the camp (for Becky trade safety or personal reasons).
    # 2. Peaceful: try to solve Zimmer's mission without bloodshed (investigation, negotiation, etc.).
    # Mongol vouch may help with peaceful route.
    # References:
    #   textLocRef\IntZimmerTalk.txt (the "Пожаловаться на Робин Гуда" paid investigation mission)
    #   textLocRef\SherwoodTravel.txt + IntRobinTalk.txt (current encounters)
    #   game/NPC/Secondary/InitZimmer.rpy (Zimmer.var RobinInvestigationDay + Robin registration)
    #   Future: full Cunidale content + third Blackwood part (see TODO file)

    show screen main_ui
    $ zimmer = getPersonInfo("zimmer") if "zimmer" in dir() else None
    $ robin = getPersonInfo("robin") if "robin" in dir() else None

    $ Zimmer.ensure_story_defaults()
    $ Robin.ensure_story_defaults()

    $ MainTxt = "Вы добрались до лагеря обездоленных на вырубке. Несколько десятков человек в зелёных трико. Робин в центре.\n\n"

    if Robin.var.get("MongolSafePass", 0) == 1:
        $ MainTxt += "Благодаря слову Монгола вас пока не трогают. Можно попробовать договориться.\n\n"
    else:
        $ MainTxt += "Без защиты Монгола любой подход опасен — вас могут сразу попытаться «попросить на социяльную ответственность».\n\n"

    $ MainTxt += "Вы вспоминаете поручение десятника Циммермана: «решить проблему разбойников, мешающих торговле».\n\n"
    $ CurLocDesc = MainTxt

    menu:
        "Уничтожить лагерь (силовой вариант)":
            $ MainTxt += "Вы решаете, что мирным путём не обойтись. Лагерь нужно ликвидировать.\n"
            $ MainTxt += "(Полная реализация этого пути — уничтожение, последствия для торговли, реакция Зиммера и Бекки — в будущей части квеста.)\n"
            $ Robin.var["PlayerDestroyedCamp"] = 1

            if thread is not None:
                $ thread.advance()

            # Placeholder return / jump to future camp destruction scene
            return

        "Попробовать решить мирно (для миссии Зиммера)":
            $ MainTxt += "Вы вспоминаете поручение Циммермана. Возможно, удастся договориться, провести «расследование» или найти компромисс, который устроит и стражу, и Бекки, и даже Робина.\n"
            $ MainTxt += "(Полная реализация мирного пути — переговоры, условия, последствия, оплата от Зиммера — в будущей части квеста.)\n"
            $ Robin.var["ZimmerPeaceful"] = 1

            if thread is not None:
                $ thread.advance()

            return

        "Пока отступить и подумать":
            $ MainTxt += "Вы решаете не форсировать события прямо сейчас. Нужно подготовиться."
            return

    return


label zimmer_guard_mission_update:
    # Thin atomic update event called after the player returns from the bandit camp choice point.
    # Updates Zimmer's investigation state based on what the player actually did (destroy vs peaceful).
    # Ties the paid complaint in IntZimmerTalk to real player action in Blackwood.
    # References:
    #   textLocRef\IntZimmerTalk.txt (horse theft + Robin complaint + investigation follow-up + "поймайте и приведите сами")
    #   game/NPC/Secondary/InitZimmer.rpy (Zimmer.var + registration)
    #   zimmer_bandit_camp_choice (the choice the player made)

    show screen main_ui
    $ zimmer = getPersonInfo("zimmer") if "zimmer" in dir() else None

    $ Zimmer.ensure_story_defaults()
    $ Robin.ensure_story_defaults()

    if Zimmer.var.get("MissionUpdatedByPlayer", 0) == 1:
        return   # already processed

    $ MainTxt = "Вы возвращаетесь к десятнику Циммерману в городскую стражу.\n\n"

    if Robin.var.get("PlayerDestroyedCamp", 0) == 1:
        $ MainTxt += "«Десятник, я сам разобрался с этими разбойниками в вырубке.»\n\n"
        $ MainTxt += "Циммерман выглядит одновременно впечатлённым и слегка испуганным вашей смелостью.\n"
        $ MainTxt += "«Ай-яй, молодой человек... Вы таки серьёзный человек. Ну что ж, дело закрыто. Если вдруг что-то ещё... вы знаете, где меня найти.»\n"
        $ Zimmer.var["PlayerHandledRobin"] = 1
        $ Zimmer.var["MissionUpdatedByPlayer"] = 1

        if thread is not None:
            $ thread.advance()

    elif Robin.var.get("ZimmerPeaceful", 0) == 1:
        $ MainTxt += "Вы рассказываете Циммерману о договорённости, которую удалось достичь с Робином (или компромиссе).\n\n"
        $ MainTxt += "Десятник кивает, пряча улыбку. «Молодой человек, вы меня удивляете. Я думал, вы просто заплатите и забудете. А вы таки решили вопрос по-настоящему. Молодец. Стража в долгу.»\n"
        $ Zimmer.var["PlayerHandledRobin"] = 2
        $ Zimmer.var["MissionUpdatedByPlayer"] = 1

        if thread is not None:
            $ thread.advance()

    else:
        $ MainTxt += "Вы пока не готовы отчитаться о результатах миссии."

    $ CurLocDesc = MainTxt
    $ Zimmer.mark_talked(1)

    return
