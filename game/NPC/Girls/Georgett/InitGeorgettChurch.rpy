label ChurchServiceGeorgett:
    $ scene_runtime.text = "В одном из углов собора вы находите вашу ветренную знакомую - Жоржетту Брюно, шлюху из портового квартала. Это молодая белокурая и кареглазая женщина, среднего роста, чуть пухленькая и с большой налитой грудью. В собор она нарядилась чуть скромнее, чем обычно, но не слишком: на ней красное платье до колен и блузка с глубоким декольте, на этот раз хотя бы не прозрачная. Вы замечаете, что прихожане-мужчины обращают на нее гораздо больше внимания, чем на проповедь с амвона."
    if Georgett.story_value("askkids", 0):
        if Liza.rel > 0:
            $ scene_runtime.text = scene_runtime.text + "\n\nРядом с ней вы видите ее старшую дочь Лизетту - молоденькую мулатку, на вид - ровесницу Аманды. Ее волосы забранны в две косички а груди только начали расти. Ее шоколадное тело закрывают юбка и блузка, такие же как у ее мамы."
        else:
            $ scene_runtime.text = scene_runtime.text + "\n\nРядом с ней вы видите молоденькую мулатку, на вид - ровесницу Аманды. Ее волосы забранны в две косички а груди только начали расти. Судя по всему это Лизетта - старшая дочь Жоржетты. Ее шоколадное тело закрывают юбка и блузка, такие же как у ее мамы."
        vscene "images/georgett/church/cermonliza.jpg"
    else:
        vscene "images/georgett/church/cermon.jpg"
    $ scene_runtime.location_text = scene_runtime.text
    $ Georgett.set_story_value("foundinchurch", 1)
    $ findAvailableEvents(False)
    menu:
        "Предложить найти тихое место" if story_event_available("Church", "georgett_church_service_bench"):
            call checkTriggers("Church", "georgett_church_service_bench", 0)
            return
        "Предложить сделать это прямо здесь" if story_event_available("Church", "georgett_church_service_doggy"):
            call checkTriggers("Church", "georgett_church_service_doggy", 0)
            return
        "Предложить, чтобы Лизетта посмотрела" if story_event_available("Church", "georgett_church_service_with_liza"):
            call checkTriggers("Church", "georgett_church_service_with_liza", 0)
            return
        "Вернуться в собор":
            return


label story_georgett_church_service_bench:
    show screen main_ui
    if Georgett.story_value("askkids", 0):
        vscene "images/georgett/church/cermonliza.jpg"
    else:
        vscene "images/georgett/church/cermon.jpg"
    "Вы предлагаете Жоржетте найти укромное место, где вас никто не увидит."

    if Georgett.rel < 6:
        "«Ты что, сдурел!» - отвечает вам она. «Это же собор!»"
        call ChurchServiceGeorgett
        return

    "«Какой ты пошлый! Поиметь меня прямо на церковной службе!» - смеется Жоржетта. «Это обойдется тебе в 15 мараведи!»"

    if int(player.economy.money or 0) < 15:
        "«Ой, а у меня столько нет», говорите вы."
        "«Ну нет так нет», следует резонный ответ."
        call ChurchServiceGeorgett
        return

    vscene "images/georgett/church/bench/bench1.jpg"
    "Жоржетта берет монеты и ведет вас к одной из скамей в темном углу собора."

    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/bench/bench2.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/bench/bench3.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/bench/bench4.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/bench/bench5.jpg"
    menu:
        "Дальше":
            pass

    "Через несколько минут вы оба приводите себя в порядок и возвращаетесь к звукам службы."

    $ player.spend_money(15)
    $ player.change_stat("fun", 4)
    $ Georgett.set_story_value("fuckinchurch", 1)
    $ Georgett.set_story_value("church_bench_seen", 1)
    $ player_record_orgasm("georgett_church_bench", "georgett")
    $ pregnancy_check("georgett", "inside", 1, "Вы")
    vscene "images/georgett/church/bench/bench6.jpg"
    menu:
        "Вернуться в собор":
            $ calendar_v2.advance_minutes(60)
            return


label story_georgett_church_service_doggy:
    show screen main_ui
    vscene "images/georgett/church/cermon.jpg"
    "Вы предлагаете Жоржетте не искать укрытия и рискнуть прямо здесь."

    if int(player.economy.money or 0) < 15:
        "«Ну нет так нет», отвечает Жоржетта, услышав, что у вас не хватает денег."
        call ChurchServiceGeorgett
        return

    vscene "images/georgett/church/doggy/doggy1.jpg"
    "Жоржетта принимает монеты и, бросив быстрый взгляд по сторонам, соглашается на вашу дерзкую идею."

    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/doggy/doggy2.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/doggy/doggy3.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/doggy/doggy4.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/doggy/doggy5.jpg"
    "Вы едва удерживаетесь от лишнего шума, пока служба продолжается совсем рядом."

    $ player.spend_money(15)
    $ player.change_stat("fun", 4)
    $ Georgett.set_story_value("fuckinchurch", 1)
    $ Georgett.set_story_value("church_doggy_seen", 1)
    $ player_record_orgasm("georgett_church_doggy", "georgett")
    $ pregnancy_check("georgett", "inside", 1, "Вы")
    vscene "images/georgett/church/doggy/doggy6.jpg"
    menu:
        "Вернуться в собор":
            $ calendar_v2.advance_minutes(60)
            return


label story_georgett_church_service_with_liza:
    show screen main_ui
    vscene "images/georgett/church/cermonliza.jpg"
    "В следующий раз Жоржетта уже не делает вид, что не понимает вашего намека, и сама зовет Лизетту ближе."

    if int(player.economy.money or 0) < 15:
        "Жоржетта только пожимает плечами: без денег она не собирается рисковать."
        call ChurchServiceGeorgett
        return

    if Liza.rel == 0:
        $ Liza.add_relation(1)

    vscene "images/georgett/church/withLiza.jpg/withliza1.jpg"
    "Лизетта замечает происходящее и остается наблюдать, пока Жоржетта просит ее молчать."

    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/withLiza.jpg/withliza2.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/withLiza.jpg/withliza3.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/withLiza.jpg/withliza4.jpg"
    menu:
        "Дальше":
            pass

    vscene "images/georgett/church/withLiza.jpg/withliza5.jpg"
    "Когда все заканчивается, Жоржетта спокойно поправляет платье, а Лизетта старается не смотреть вам прямо в глаза."

    $ player.spend_money(15)
    $ player.change_stat("fun", 40)
    $ Georgett.set_story_value("fuckinchurch", 1)
    $ Georgett.set_story_value("church_liza_seen", 1)
    $ Georgett.set_story_value("lizasawinchurch", 1)
    $ player_record_orgasm("georgett_church_liza", "georgett")
    $ pregnancy_check("georgett", "inside", 1, "Вы")
    vscene "images/georgett/church/withLiza.jpg/withliza6.jpg"
    menu:
        "Вернуться в собор":
            $ calendar_v2.advance_minutes(60)
            return
