# ================================================================================
# Clarissa's forest confession, hidden stash, and cursed-sofa continuation.
# Availability is owned by claraForestSofa in StoryEventRuntime.rpy.
# ================================================================================

# Event: the player follows Clarissa from a forest clearing to the lake.
# Choices:
# - protect her: accepts her confession and advances the connected story
# - expose her: refuses protection and permanently aborts this continuation
label story_clara_forest_lake_0:
    $ main_ui_begin_native_scene_state("Кларисса в лесу")
    show screen main_ui

    vscene "images/clara/forest_clara_encounter.png"
    $ scene_runtime.text = "На лесной поляне вы замечаете Клариссу. Она уверена, что за ней никто не следит, и потому идет не по обычной дороге, а по узкой тропе к уединенному озеру. После всего услышанного на рынке случайной прогулкой это уже не выглядит."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Тихо проследить за Клариссой":
            pass

    vscene "images/clara/forest_clara_bath.png"
    $ scene_runtime.text = "У озера Кларисса долго прислушивается к лесу, затем складывает платье и белье на траву и входит в воду совершенно нагой. Здесь нет ни светской улыбки, ни дочери богатого торговца — только девушка, которая хотя бы на несколько минут сбежала от чужих правил."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Наблюдать дальше":
            pass

    vscene "images/clara/forest_clara_bath_2.png"
    $ scene_runtime.text = "Кларисса отплывает дальше от берега. Возле ее одежды вы замечаете панталоны; на внутренней стороне пояса углем нанесены приметы старой водокачки, скрытой тропы и дерева с особой зарубкой. Это не случайные каракули, а карта к тайнику. Вы забираете улику и выходите из укрытия прежде, чем она успевает одеться."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    if int(player.item_count("clara_pantaloons_001") or 0) <= 0:
        $ player.add_item("clara_pantaloons_001", 1)

    menu:
        "Потребовать правду":
            pass

    vscene "images/clara/forest_clara_bath_3.png"
    $ scene_runtime.text = "Прижав платье к груди, Кларисса сначала пытается сердиться, но быстро понимает, что отрицать уже нечего. Она признается во всем сразу. Отец Альбер с детства учил ее считать деньги, торговаться и держаться как настоящая госпожа, а теперь собирается выдать за столичного жениха ради выгодной связи. Спасаясь от этой сделки, она тайком уходила к разбойничьему лагерю и мечтала купить себе место среди людей, которые не спрашивают разрешения у семьи.\n\nИменно Кларисса придумала кражу лошадей, нашла покупателя и направляла Монгола. Через непристойные рисунки, сплетни и визиты в трактир она также пыталась сделать Аманду и Мелиссу сговорчивее, чтобы облегчить грязные планы Легаре. Теперь она понимает, что ради собственной свободы стала использовать чужое доверие тем же способом, каким отец использовал ее."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Выслушать ее просьбу":
            pass

    vscene "images/clara/forest_clara_bath_4.png"
    $ scene_runtime.text = "Кларисса просит прощения и защиты. Если вы не выдадите ее отцу и страже, она обещает прекратить помогать замыслам Легаре, рассказать все о женихе и разбойничьем лагере, вернуть доверие девушек и использовать свое воспитание на пользу трактиру. Она готова учить вашу команду манерам, продолжать рисунки уже без обмана и помочь Мелиссе перестать бояться самых смелых сторон близости."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    $ calendar_v2.advance_minutes(60)
    $ player.change_stat("energy", -10)
    call stat

    menu:
        "Простить Клариссу и взять под свою защиту":
            $ Clara.drawings_secret_known = True
            $ Clara.merchant_contact_unlocked = True
            $ Clara.change_social(friend_delta=3, open_delta=2)
            $ Clara.trust = min(20, int(Clara.trust or 0) + 3)
            if threads["claraTavernVisit"].completed:
                $ threads["claraTavernVisit"].advanceTo(6, force_active=True)
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            return True

        "Отказать и не скрывать ее вину":
            $ Clara.change_social(friend_delta=-5)
            $ Clara.trust = max(0, int(Clara.trust or 0) - 5)
            $ event_runtime.active_thread.abort()
            $ main_ui_end_native_scene_state()
            return True


label story_clara_forest_sofa_stash_1:
    $ main_ui_begin_native_scene_state("Тайник Клариссы")
    show screen main_ui
    vscene "images/forest/hidden_path.png"
    $ scene_runtime.text = "Сверяясь с угольными отметками на панталонах Клариссы, вы находите за старой водокачкой дерево с вырезанным знаком. Походная лопата вскоре ударяется о завернутый в промасленную ткань сверток. Внутри лежат шестьсот мараведи — доля Клариссы от ее рыночной аферы."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Забрать спрятанные деньги":
            pass
    $ player.add_money(600)
    $ player.change_stat("energy", -10)
    $ calendar_v2.advance_minutes(60)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
