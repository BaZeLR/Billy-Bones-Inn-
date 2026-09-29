default intro_cinematic_active = False

define intro_sandra = Character("Сандра")
define intro_amanda = Character("Аманда")
define intro_steven = Character("Стивен")
define intro_evil = Character("Доктор Ивил")
define intro_penny = Character("Пенни")


screen intro_letterbox():
    zorder -1
    add Solid("#000000") xpos 0 ypos 0 xysize (config.screen_width, 90)
    add Solid("#000000") xpos 0 yalign 1.0 xysize (config.screen_width, 244)


label Intro:
    scene black
    hide screen status
    hide screen main_ui
    $ rooms.enter("Intro")
    $ intro_cinematic_active = True

    "ТРАКТИР «ДИКИЙ ЖЕРЕБЕЦ». ВЕРСИЯ 0.05. АВТОР БИЛЛИ БОНС. ХУДОЖНИКИ ULIBAKA11-11, FORCEFER, NIK287."
    "ИГРА ПРЕДНАЗНАЧЕННА ТОЛЬКО ДЛЯ 18+. ЕСЛИ ВАМ НЕТ 18 ЛЕТ НЕМЕДЛЕННО ЗАКРОЙТЕ ЭТУ ИГРУ И СОТРИТЕ ЕЕ С КОМПЬЮТЕРА."
    "ИГРА ПРЕДСТАВЛЯЕТ СОБОЙ ЧИСТУЮ ФАНТАЗИЮ, ВСЕ ЗАДЕЙСТВОВАННЫЕ МОДЕЛИ СТАРШЕ 18 ЛЕТ, ЛЮБЫЕ СОВПАДЕНИЯ С РЕАЛЬНЫМИ СОБЫТИЯМИ ИЛИ ЛЮДЬМИ СЛУЧАЙНЫ."
    "ПОПЫТКИ ПОСТУПАТЬ В РЕАЛЬНОЙ ЖИЗНИ ТАК ЖЕ, КАК ПОСТУПАЮТ ГЕРОИ ДАННОЙ ИГРЫ, НАСТОЯТЕЛЬНО НЕ РЕКОМЕНДУЮТСЯ."
    "ОНИ МОГУТ ПРИВЕСТИ К РАЗБИТОЙ ФИЗИОНОМИИ, НЕЖЕЛАТЕЛЬНОЙ БЕРЕМЕННОСТИ И/ИЛИ БРАКУ, ТЮРЕМНОМУ ЗАКЛЮЧЕНИЮ, ШТРАФУ, ПЕРЕЛОМУ КОНЕЧНОСТЕЙ, УВОЛЬНЕНИЮ, РАЗВОДУ, СКАНДАЛУ,"
    "ВСТУПЛЕНИЮ В ПАРТИЮ «ЕДИНАЯ РОССИЯ» ИЛИ В РЯДЫ ОППОЗИЦИИ, ИСКЛЮЧЕНИЮ ИЗ УЧЕБНОГО ЗАВЕДЕНИЯ И ПРОЧИМ РАЗНООБРАЗНЫМ НЕПРИЯТНОСТЯМ."
    "При создании игры использовались модули меню и таблиц данных авторства Олегуса и две процедуры из игры «Альбедо» авторства ДеГросса."

    call OpeningCinematic
    menu:
        "Приступить к управлению трактиром":
            jump dev_after_report_checkpoint


label OpeningCinematic:
    $ intro_cinematic_active = True
    show screen intro_letterbox

    scene expression Transform("images/intro/intro_1.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "Сначала вернулся звук: тележные колёса, крики торговцев, звон подков по булыжнику. Потом — чужой город и собственные руки в нелепых чёрных перчатках."
    "Вы очнулись посреди рынка Коитополиса. На рукаве белого медицинского халата тускло светился наручный коммуникатор; на пальце сидело тяжёлое кольцо с голубым камнем."

    scene expression Transform("images/intro/intro_2.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Конь городского стражника едва не сбил вас с ног."
    scene expression Transform("images/intro/intro_3.png", xysize=(config.screen_width, config.screen_height), fit="cover") with vpunch
    "Вы отшатнулись, ухватившись за стену. Стражник выругался и поехал дальше, а вы никак не могли вспомнить, как оказались здесь."

    scene expression Transform("images/intro/intro_4.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Вслед за клеткой, которую увозили с рыночной площади, тянулись две плачущие девушки. Прохожий заметил ваш взгляд и наклонился к вам."
    "Прохожий" "Хозяина «Слепого Пирата» продали в рабство. Вот до чего доводят долги. Девчонки ещё утром надеялись, что его отпустят."
    "Вы посмотрели вслед повозке. Это имя ничего вам не говорило — как и весь город вокруг."

    scene expression Transform("images/intro/intro_5.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    intro_sandra "Стефан?! Слава Илматеру, я тебя нашла! Где ты пропадал три недели? Мы уж решили, что ты погиб!"
    "Женщина смотрела так, будто знала вас всю жизнь. Она назвала вас Стефаном, и это имя на миг показалось почти знакомым."

    scene expression Transform("images/intro/intro_6.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    intro_sandra "И что на тебе надето? Поварской халат? Перчатки? Ты что, с алхимиками гулял? Пойдём домой, Стефан."
    "Сандра взяла вас за руку и повела по Мясницкой улице к вывеске с диким жеребцом. По дороге она говорила без умолку: трактир запущен, крыша течёт, в кладовой крысы, на чердаке летучие мыши, всюду грязь."

    scene expression Transform("images/intro/intro_7.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "На кухне вас встретили Мелисса и Аманда. За облегчением на их лицах быстро проступила злость."
    "Мелисса" "Исчез на три недели, а нам оставил и трактир, и крыс? Хоть бы слово передал, что живой."
    scene expression Transform("images/intro/intro_8.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Аманда шагнула ближе и демонстративно принюхалась к вашему лицу."
    intro_amanda "Он трезвый! Теперь это ещё страннее."
    intro_sandra "Дайте ему прийти в себя. Потом спросим обо всём."

    scene expression Transform("images/intro/intro_9.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "Вы поднялись в свою комнату. На столе лежало письмо с печатью герцогини Кончитты."
    "«Стефан Лонгкок. После смерти вашего дяди Джона Лонгкока трактир „Дикий Жеребец“ переходит вам по наследству. Примите хозяйство и позаботьтесь о людях, которые в нём остались»."
    "Буквы поплыли перед глазами. Вспомнилась жизнь человека по имени Стефан — но память казалась чужой."

    scene expression Transform("images/intro/intro_10.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    intro_steven "Это я?.. Как такое возможно?"
    "В зеркале было лицо Стефана. Вы коснулись щеки, и память ударила, как волна."

    scene expression Transform("images/intro/intro_11.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "Дождь. Дядя Джон выставляет юного Стефана за дверь «Дикого Жеребца». На пороге стоят Сандра, маленькие Мелисса и Аманда. Они молчат, пока сундук падает в грязь."
    scene expression Transform("images/intro/intro_12.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Позже — палуба торгового судна. Стефан вырос, стал моряком и научился держаться за мокрые снасти даже в шторм. Но эта память всё равно не была вашей."

    scene expression Transform("images/intro/intro_13.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "Вы сели на кровать, сняли огромные перчатки и раскрыли экран коммуникатора на предплечье. Зелёная полоска связи едва дрожала."
    intro_steven "Доктор? Вы меня слышите?"

    scene expression Transform("images/intro/intro_22.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Экран зашипел. Коммуникатор плотно охватывал ваше голое предплечье; за ним вы видели собственную ладонь. Сквозь плотные полосы помех проступило знакомое лысое лицо."
    scene black
    show expression Transform("images/intro/intro_17.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    intro_evil "Стивен! Живой! Чёрт побери, мы так волновались. Даже Пенни!"
    scene black
    show expression Transform("images/intro/intro_20.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    intro_evil "Ты дрался с Темпест — сверхчеловеком по прозвищу «Богиня». Она остановила тебя среди колонн, а потом бросилась в атаку."
    scene black
    show expression Transform("images/intro/intro_21.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    intro_evil "Её удар расколол камень. Вокруг вас замкнулось сияющее поле — мы видели это на записи."
    scene expression Transform("images/intro/intro_16.png", xysize=(config.screen_width, config.screen_height), fit="cover") with vpunch
    intro_evil "Потом вы исчезли вместе. Наши учёные едва поймали твой сигнал: пространство и время там перекручены."
    "Вспышка памяти: белый халат, защитные очки, огромные чёрные перчатки. Вы пытались удержать удар Темпест — и оба провалились в ослепительный разлом."
    scene expression Transform("images/intro/intro_22.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    intro_steven "Я в каком-то трактире. Меня зовут Стефаном. В зеркале — чужое лицо."
    scene black
    show expression Transform("images/intro/intro_18.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    intro_evil "Я вижу. Выглядишь... иначе. Но это сейчас не главное. Держись и не привлекай внимания, Стивен. Мы разберёмся, куда тебя забросило и как вернуть."
    scene black
    show expression Transform("images/intro/intro_19.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    intro_evil "Пенни здесь, она хочет поздороваться. Только не пугай её своим новым видом. М-ха-ха!"

    scene black
    show expression Transform("images/intro/penny_ass.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    "Вместо лица Пенни на экране неожиданно появился её снимок. Из динамика сквозь помехи донёсся её голос."
    intro_penny "Stevie! hello pickle cock... you basta... pshhhh!"
    scene expression Transform("images/intro/intro_15.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    intro_evil "Упс. Wrong picture..."
    scene black
    show expression Transform("images/intro/intro_19.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    intro_evil "М-ха-ха!"
    scene black
    show expression Transform("images/intro/intro_18.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with dissolve
    intro_evil "Тише. Не высовывайся и береги себя. Дождись нашей связи."

    scene expression Transform("images/intro/intro_13.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    intro_steven "Теперь ясно. Она использовала ловушку времени... и я попал сюда вместе с ней."

    "Связь оборвалась. За дверью слышались голоса Сандры, Мелиссы и Аманды. Этот трактир был домом Стефана; пока вы не найдёте дорогу назад, он станет и вашим."
    hide screen intro_letterbox
    $ intro_cinematic_active = False
    return


label dev_after_report_checkpoint:
    $ renpy.dynamic("revision")
    call InitGameNPCs
    call NextDay_NewDayEvents
    call CreateTavernEvents
    $ revision = 5
    jump TavernMain
