default intro_cinematic_active = False

define intro_steven = Character("Стивен")
define intro_evil = Character("Доктор Ивил")
define intro_penny = Character("Пенни")
define intro_stranger = Character("Незнакомка")
define intro_dark_girl = Character("Темноволосая девушка")
define intro_blonde_girl = Character("Светловолосая девушка")

define intro_legacy_text = """-------------------------------------------------ТРАКТИР \"ДИКИЙ ЖЕРЕБЕЦ\"------------------------------------------
ВЕРСИЯ 0.05
АВТОР БИЛЛИ БОНС
ХУДОЖНИКИ ULIBAKA11-11, FORCEFER, NIK287

ИГРА ПРЕДНАЗНАЧЕННА ТОЛЬКО ДЛЯ 18+. ЕСЛИ ВАМ НЕТ 18 ЛЕТ НЕМЕДЛЕННО ЗАКРОЙТЕ ЭТУ ИГРУ И СОТРИТЕ ЕЕ С КОМПЬЮТЕРА

ИГРА ПРЕДСТАВЛЯЕТ СОБОЙ ЧИСТУЮ ФАНТАЗИЮ, ВСЕ ЗАДЕЙСТВОВАННЫЕ МОДЕЛИ СТАРШЕ 18 ЛЕТ, ЛЮБЫЕ СОВПАДЕНИЯ С РЕАЛЬНЫМИ СОБЫТИЯМИ ИЛИ ЛЮДЬМИ СЛУЧАЙНЫ

ПОПЫТКИ ПОСТУПАТЬ В РЕАЛЬНОЙ ЖИЗНИ ТАК ЖЕ, КАК ПОСТУПАЮТ ГЕРОИ ДАННОЙ ИГРЫ, НАСТОЯТЕЛЬНО НЕ РЕКОМЕНДУЮТСЯ. ОНИ МОГУТ ПРИВЕСТИ К РАЗБИТОЙ ФИЗИОНОМИИ, НЕЖЕЛАТЕЛЬНОЙ БЕРЕМЕННОСТИ И/ИЛИ БРАКУ, ТЮРЕМНОМУ ЗАКЛЮЧЕНИЮ, ШТРАФУ, ПЕРЕЛОМУ КОНЕЧНОСТЕЙ, УВОЛЬНЕНИЮ, РАЗВОДУ, СКАНДАЛУ, ВСТУПЛЕНИЮ В ПАРТИЮ \"ЕДИНАЯ РОССИЯ\" ИЛИ В РЯДЫ ОППОЗИЦИИ, ИСКЛЮЧЕНИЮ ИЗ УЧЕБНОГО ЗАВЕДЕНИЯ И ПРОЧИМ РАЗНООБРАЗНЫМ НЕПРИЯТНОСТЯМ

При создании игры использовались модули меню и таблиц данных авторства Олегуса и две процедуры из игры \"Альбедо\" авторства ДеГросса
---------------------------------------------------------------------------

Вас зовут Стефан Лонгкок. Ваш дядя, Джон Лонгкок, был крестьянином, но, накопив достаточно денег, он купил небольшой трактир в пригороде большого портового города Коитополиса. Однако ему было не суждено стать трактирщиком - он так увлекся обмытием сделки, что упал пьяным в один из каналов и утонул. После похорон во владение трактиром \"Дикий Жеребец\" вступили вы, его племянник и наследник.

В трактире осталась Сандра, возлюбленная вашего покойного дяди. Под ее опекой живут осиротевшие племянницы Мелисса и Аманда: они сестры по матери, но от разных отцов. Ни Сандра, ни девушки не состоят с вами в родстве; вы их домовладелец и хозяин трактира.

К сожалению вы мало что понимаете в уборке, готовке и прочем. Но это не важно, ведь теперь вы управляете трактиром и должны руководить. Основную работу выполняет ваша команда: Сандра, Мелисса и Аманда. Ваше незавидное финансовое положение не позволяет вам пока нанять кого-то еще."""


transform intro_credits_down:
    xalign 0.5
    ypos 0.65
    linear 55.0 ypos -2.2


screen intro_credits():
    add Solid("#000000")
    text intro_legacy_text:
        xsize int(config.screen_width * 0.76)
        text_align 0.5
        size 28
        color "#F2E5CF"
        at intro_credits_down


screen intro_letterbox():
    zorder -1
    add Solid("#000000") xpos 0 ypos 0 xysize (config.screen_width, 90)
    add Solid("#000000") xpos 0 yalign 1.0 xysize (config.screen_width, 244)


screen intro_comm_feed(feed, wide=False):
    # A video feed sits inside the communicator's display, never over the room.
    zorder -2
    if wide:
        add Transform(feed, xysize=(int(config.screen_width * 0.69), int(config.screen_height * 0.57)), fit="cover", alpha=0.93) xpos int(config.screen_width * 0.155) ypos int(config.screen_height * 0.13)
    else:
        add Transform(feed, xysize=(int(config.screen_height * 0.57), int(config.screen_height * 0.57)), fit="cover", alpha=0.93) xpos int(config.screen_width * 0.34) ypos int(config.screen_height * 0.13)


label Intro:
    scene black
    hide screen status
    hide screen main_ui
    $ rooms.enter("Intro")
    $ intro_cinematic_active = True

    call OpeningCinematic
    scene black
    window hide
    show screen intro_credits
    pause 55.0
    hide screen intro_credits
    window show
    menu:
        "Приступить к управлению трактиром":
            jump dev_after_report_checkpoint


label OpeningCinematic:
    $ intro_cinematic_active = True
    show screen intro_letterbox

    scene expression Transform("images/intro/intro_1.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "Сначала вернулся звук: тележные колёса, крики торговцев, звон подков по булыжнику. Потом — чужой город и собственные руки в нелепых чёрных перчатках."
    "Вы очнулись посреди незнакомого рынка. На рукаве белого халата тускло светился наручный коммуникатор; на пальце сидело тяжёлое кольцо с голубым камнем. Ни название города, ни собственное имя не приходили на ум."

    scene expression Transform("images/intro/intro_2.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Конь городского стражника едва не сбил вас с ног."
    scene expression Transform("images/intro/intro_3.png", xysize=(config.screen_width, config.screen_height), fit="cover") with vpunch
    "Вы отшатнулись, ухватившись за стену. Стражник выругался и поехал дальше, а вы никак не могли вспомнить, как оказались здесь."

    scene expression Transform("images/market/blindPirate_liza_georgette.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Рыночный шум вдруг меняет голос. Там, где еще секунду назад спорили о цене муки и бранились из-за тухлой рыбы, толпа сама собой расползается в стороны, словно кто-то провел по ней тяжелым ножом. Меж плеч и корзин медленно выкатывается телега с железной клеткой. Колеса стучат по камню так глухо и тяжело, будто везут не человека, а уже готовую беду."
    "Внутри, скорчившись на сырой соломе, сидит мужчина. Лицо у него серое, провалившееся, жалкое; не лицо хозяина, а лицо человека, с которого разом содрали и достаток, и честь, и сон. В клетку летят гнилые репы, мятые кочаны, склизкие огрызки. Кто-то хохочет, кто-то орет проклятья, кто-то, напротив, отворачивается, словно стыдясь чужого несчастья, но все равно идет следом смотреть. А рядом с клеткой, едва поспевая за телегой и заливаясь плачем, идут две женщины: невысокая темнокожая девушка с двумя темными косами и светловолосая женщина постарше. Старшая крепко обнимает младшую за плечи. Обе уже выбились из сил, но все еще не могут оторвать глаз от телеги, как будто одним этим взглядом можно удержать человека от дороги к портовым галерам."
    scene expression Transform("images/intro/intro_4.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "«Эх, вот она как судьба-то ломает», - говорит кто-то рядом, уже без злобы, вполголоса, будто в церкви. - «Еще вчера был хозяином \"Слепого Пирата\" - самого бойкого трактира в городе. У него столы ломились, клиенты дрались за место, а теперь его самого гонят на галеры герцогини Кончиты за долги. Трактир выгорел до головешек, дом разорен, а весь его бабий и дворовый люд пошел по миру.»"
    "Вы слушаете и чувствуете, как холодок проходит по спине. Рыночный гам снова становится просто шумом, но теперь в нем слышится уже не одно веселье. Слишком ясно становится, на какой тонкой доске стоит любой трактир и как легко под хорошим хозяином вдруг может разверзнуться пустота."

    scene expression Transform("images/intro/intro_5.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    intro_stranger "Стефан?! Слава Илматеру, я тебя нашла! Где ты пропадал три недели? Мы уж решили, что ты погиб!"
    "Женщина смотрела так, будто знала вас всю жизнь. Она назвала вас Стефаном; вы повторили это имя про себя, пытаясь узнать его."

    scene expression Transform("images/intro/intro_6.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    intro_stranger "И что на тебе надето? Поварской халат? Перчатки? Ты что, с алхимиками гулял? Пойдём домой, Стефан."
    "Она взяла вас за руку и повела по Мясницкой улице к вывеске с диким жеребцом. По дороге не умолкала: трактир запущен, крыша течёт, в кладовой крысы, на чердаке летучие мыши, всюду грязь."

    scene expression Transform("images/intro/intro_7.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "На кухне вас встретили две девушки. За облегчением на их лицах быстро проступила злость."
    intro_dark_girl "Исчез на три недели, а нам оставил и трактир, и крыс? Хоть бы слово передал, что живой."
    scene expression Transform("images/intro/intro_8.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Светловолосая шагнула ближе и демонстративно принюхалась к вашему лицу."
    intro_blonde_girl "Он трезвый! Теперь это ещё страннее."
    intro_stranger "Дайте ему прийти в себя. Потом спросим обо всём."

    scene expression Transform("images/intro/intro_28.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "На барной стойке лежало письмо с тяжёлой красной печатью. Вы развернули его под светом свечи."
    "КАНЦЕЛЯРИЯ ТОРГОВОГО ФЛОТА ЕЁ СВЕТЛОСТИ ГЕРЦОГИНИ КОНЧИТТЫ. Нотариальное свидетельство о наследовании. Стефану Лонгкоку."
    "«Вследствие внезапной и прискорбной кончины вашего дяди, Джона Лонгкока, настоящим удостоверяю переход к вам права собственности на трактир „Дикий Жеребец“, расположенный на Мясницкой улице города Коитополиса»."
    "«К вам переходят здание, участок, обстановка и право вести трактирное дело. Вместе с ними вы принимаете обязанности по содержанию, уплате сборов и погашению долгов, если таковые числятся за заведением»."
    "Дано в Коитополисе, 1-го дня первого периода 1100 года. Дон Мартин де Вега, нотариус торгового флота. Подпись. Личная печать."
    "Буквы поплыли перед глазами. Стефан — так звала вас женщина с рынка. Но письмо говорило о жизни, которой вы не помнили."

    scene black
    show expression Transform("images/player_room/player_room.png", xysize=(config.screen_height, config.screen_height), fit="contain", xalign=0.5, yalign=0.5) with Fade(0.2, 0.1, 0.4)
    "Вы поднялись в отведённую вам комнату, всё ещё сжимая письмо. На столе у свечи лежало небольшое зеркало."
    scene expression Transform("images/intro/intro_25.png", crop=(615, 70, 760, 470), xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Это я?.. Как такое возможно?"
    "Вы коснулись щеки. В памяти мелькнули чужие, слишком яркие обрывки."

    scene expression Transform("images/intro/intro_11.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "Дождь. Грузный мужчина выталкивает мальчика за дверь «Дикого Жеребца». На пороге стоят женщина и две девочки. Сундук падает в грязь."
    scene expression Transform("images/intro/intro_12.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Потом — палуба торгового судна, соль на губах, мокрые снасти в руках. Эти воспоминания были такими отчётливыми, будто принадлежали вам. Но вы знали, что это не так."

    scene expression Transform("images/intro/intro_23.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    "Вы сели на кровать и стянули тяжёлые перчатки. На предплечье внезапно запищал коммуникатор. Зелёная полоска ожила без вашего прикосновения."

    scene expression Transform("images/intro/intro_26.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Вы подняли руку. По экрану побежали белые полосы помех."
    scene expression Transform("images/intro/intro_27.png", xysize=(config.screen_width, config.screen_height), fit="cover") with dissolve
    "Сквозь треск пробился чей-то вздох."
    show screen intro_comm_feed("images/intro/intro_17.png") with dissolve
    intro_evil "Стивен! Живой! Чёрт побери, мы так волновались. Даже Пенни!"
    hide screen intro_comm_feed with dissolve
    "Голос захлебнулся сухим треском. Изображение вернулось — уже другое."
    show screen intro_comm_feed("images/intro/intro_20.png") with dissolve
    intro_evil "Ты дрался с Темпест — сверхчеловеком по прозвищу «Богиня». Она остановила тебя среди колонн, а потом бросилась в атаку."
    show screen intro_comm_feed("images/intro/intro_21.png") with dissolve
    intro_evil "Её удар расколол камень. Вокруг вас замкнулось сияющее поле — мы видели это на записи."
    hide screen intro_comm_feed with vpunch
    show screen intro_comm_feed("images/intro/intro_16.png", wide=True) with dissolve
    intro_evil "Потом вы исчезли вместе. Наши учёные едва поймали твой сигнал: пространство и время там перекручены."
    "Вспышка памяти: белый халат, защитные очки, огромные чёрные перчатки. Вы пытались удержать удар Темпест — и оба провалились в ослепительный разлом."
    hide screen intro_comm_feed with dissolve
    intro_steven "Я в каком-то трактире. Меня зовут Стефаном. В зеркале — чужое лицо."
    show screen intro_comm_feed("images/intro/intro_18.png") with dissolve
    intro_evil "Я вижу. Выглядишь... иначе. Но это сейчас не главное. Держись и не привлекай внимания, Стивен. Мы разберёмся, куда тебя забросило и как вернуть."
    show screen intro_comm_feed("images/intro/intro_19.png") with dissolve
    intro_evil "Пенни здесь, она хочет поздороваться. Только не пугай её своим новым видом. М-ха-ха!"

    show screen intro_comm_feed("images/intro/penny_ass.png") with dissolve
    "Вместо лица Пенни на экране неожиданно появился её снимок. Из динамика сквозь помехи донёсся её голос."
    intro_penny "Stevie! hello pickle cock... you basta... pshhhh!"
    hide screen intro_comm_feed with dissolve
    intro_evil "Упс. Wrong picture..."
    show screen intro_comm_feed("images/intro/intro_19.png") with dissolve
    intro_evil "М-ха-ха!"
    show screen intro_comm_feed("images/intro/intro_18.png") with dissolve
    intro_evil "Тише. Не высовывайся и береги себя. Дождись нашей связи."

    hide screen intro_comm_feed
    scene expression Transform("images/intro/intro_23.png", xysize=(config.screen_width, config.screen_height), fit="cover") with Fade(0.2, 0.1, 0.4)
    intro_steven "Теперь ясно. Она использовала ловушку времени... и я попал сюда вместе с ней."

    "Связь оборвалась. За дверью слышались голоса трёх женщин. Вы посмотрели на письмо, потом на потухший экран. Внизу снова кто-то позвал: «Стефан!»"
    hide screen intro_letterbox
    $ intro_cinematic_active = False
    return


label dev_after_report_checkpoint:
    $ renpy.dynamic("revision")
    call InitGameNPCs
    call NextDay_NewDayEvents
    call CreateTavernEvents
    if int(threads["cityBlindPirateFall"].num or 0) == 0:
        $ threads["cityBlindPirateFall"].advance()
    $ revision = 5
    jump TavernMain
