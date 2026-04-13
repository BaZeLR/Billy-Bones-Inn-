# Becky Dance Interaction Menu (Friday Dance Event)
# Converted from legacy script. Handles all Becky dance menu options and outcomes.
# To be called from FridayDance or related event chains.

init python:
    def becky_dance_picture(mode="wait"):
        mode_key = str(mode or "wait").strip().lower()
        picture_map = {
            "wait": [
                "images/becky/dance/waiting_0.png",
            ],
            "invite": [
                "images/becky/dance/waiting_0.png",
            ],
            "dance": [
                "images/becky/dance/you_dance_1.png",
                "images/becky/dance/you_dance_2.png",
                "images/becky/dance/you_dance_3.png",
                "images/becky/dance/you_dance_4.png",
                "images/becky/dance/you_dance_5.png",
                "images/becky/dance/you_dance_7.png",
                "images/becky/dance/you dance_3.png",
                "images/becky/dance/you dance_6.png",
            ],
            "smile": [
                "images/becky/dance/you_dance_1.png",
                "images/becky/dance/you_dance_2.png",
            ],
            "angry": [
                "images/becky/dance/butt_angy.png",
            ],
            "butt": [
                "images/becky/dance/you_dance_4.png",
                "images/becky/dance/you_dance_5.png",
            ],
            "butt_smile": [
                "images/becky/dance/you_dance_5.png",
                "images/becky/dance/you_dance_7.png",
            ],
            "butt_angry": [
                "images/becky/dance/butt_angy.png",
            ],
            "kiss": [
                "images/becky/dance/french_kiss_1.png",
            ],
            "french": [
                "images/becky/dance/french_kiss_1.png",
                "images/becky/dance/french_kiss_2.png",
            ],
        }
        candidates = picture_map.get(mode_key, picture_map.get("wait", []))
        loadable = [row for row in candidates if renpy.loadable(row)]
        if len(loadable) > 0:
            return renpy.random.choice(loadable)
        return candidates[0] if len(candidates) > 0 else ""

label int_becky_dance():
    $ GirlNameIBD = 'becky'
    $ DanceMaxIBD = 6
    $ BeckyVar['danceinvitehome'] = BeckyVar.get('danceinvitehome', 0)
    $ Friends.setdefault(GirlNameIBD, 0)
    $ sluttiness.setdefault(GirlNameIBD, 0)
    
    menu becky_dance_menu:
        "Осмотреть" if DanceStep < 10:
            call GirlsDesc(GirlNameIBD)
            jump int_becky_dance
        "Поболтать" if DanceStep == 1:
            "Вы подошли к веселой вдовушке и начали сыпать шутками и прибаутками, веселя ее. За разговором незаметно пролетело время."
            if Friends[GirlNameIBD] >= 7:
                "Вы подумали что зря тратите время. Ничего нового вы не узнали, а Бекки и так знает, что вы шутник хоть куда."
            else:
                python:
                    import random
                    if random.randint(1,3) == 1:
                        Friends[GirlNameIBD] += 1
                        renpy.say(None, 'Вы очень развеселили Бекки своими шутками!')
            $ FridayDancesCount += 1
            $ DanceStep = DanceMaxIBD
            jump int_becky_dance
        "Пригласить потанцевать" if DanceStep == 1:
            "Вы подошли к вдове Блэнкеншип и пригласили ее потанцевать."
            $ HandsDance = ''
            $ KissDance = 0
            $ TitsDance = 0
            if Friends[GirlNameIBD] >= 7 and sluttiness[GirlNameIBD] > 18:
                call ShowImage("", "", becky_dance_picture("invite"))
                "Она с радостью согласилась, вы взяли ее под руку и вскоре вы закружились в танце."
            elif Friends[GirlNameIBD] >= 5 and sluttiness[GirlNameIBD] >= 8:
                call ShowImage("", "", becky_dance_picture("invite"))
                'Она сказала: "Стефан, Стефан, неужели ты действительно хочешь танцевать с такой практически старухой как я? Я же старше твоей мамы. Ну ладно, если ты так настаиваешь", и она взяла вашу руку и вскоре вы закружились в танце.'
            else:
                call ShowImage("", "", becky_dance_picture("angry"))
                '"Стефан, если ты хочешь танцевать со старой тетей, то пригласи свою маму" ответила вам вдова. Расстроенный отказом, вы отправились восвояси.'
                $ FridayDancesCount += 1
                $ DanceStep = DanceMaxIBD
            $ DanceStep += 1
            if DanceStep == DanceMaxIBD:
                "Танец закончился и вы вернулись к колоннаде."
            jump int_becky_dance
        "Продолжить танцевать" if DanceStep >= 2 and DanceStep < DanceMaxIBD:
            call ShowImage("", "", becky_dance_picture("dance"))
            "Вы продолжили кружится в танце с Бекки."
            if HandsDance == 'waist':
                "Ваши руки нежно обнимают талию вдовушки."
            if HandsDance == 'ass':
                "Ваши руки покоятся на все еще упругой попке вдовы."
            if HandsDance == 'ass2':
                "Ваши руки нежно сжимают попу Бекки через платье."
            if KissDance == 1:
                "Вы нежно целуете Бекки во время танца."
            if KissDance == 2:
                "Вы страстно, переплетаясь языками, целуете Бекки, прилагая все усилия чтобы не сбиться с ритма."
            if TitsDance > 0:
                "Бекки трется своей огромной грудью о вас, потихоньку возбуждаясь."
            $ DanceStep += 1
            call becky_invite_home('Becky')
            if DanceStep == DanceMaxIBD:
                "Танец закончился и вы вернулись к колоннаде."
            jump int_becky_dance
        "Положить руки на талию" if DanceStep >= 2 and DanceStep < DanceMaxIBD and HandsDance != 'waist':
            "Вы положили руки на талию Бекки."
            if Friends[GirlNameIBD] >= 7 and sluttiness[GirlNameIBD] > 10:
                call ShowImage("", "", becky_dance_picture("smile"))
                "Она нежно улыбнулась и придвинулась к вам поближе, продолжая танец."
                call SlutFriendsIncrease(GirlNameIBD, 8, 5, 1, 14, 5, 1)
                $ HandsDance = 'waist'
            elif Friends[GirlNameIBD] >= 5 and sluttiness[GirlNameIBD] >= 6:
                call ShowImage("", "", becky_dance_picture("dance"))
                'Вдова удивденно приподняла бровь, но возражать не стала.'
                call SlutFriendsIncrease(GirlNameIBD, 8, 5, 1, 14, 5, 1)
                $ HandsDance = 'waist'
            else:
                call ShowImage("", "", becky_dance_picture("angry"))
                '"Стефан, негодник, что это ты такое делаешь?" спросила Бекки "Я согласилась просто танцевать с тобой, а ты нарушил наш уговор". Вы попробовали объяснить, что так обычно танцуют, но обнаружили что разговариваете с пустотой, Бекки ушла.'
                $ FridayDancesCount += 1
                $ DanceStep = DanceMaxIBD
                call SlutFriendsIncrease(GirlNameIBD, 2, 2, -1, 0, 0, 0)
                $ HandsDance = ''
            $ DanceStep += 1
            call becky_invite_home('Becky')
            if DanceStep == DanceMaxIBD:
                "Танец закончился и вы вернулись к колоннаде."
            jump int_becky_dance
        "Положить руки на попу" if DanceStep >= 2 and DanceStep < DanceMaxIBD and HandsDance == 'waist':
            if HandsDance == 'waist':
                "Вы опустили руки с талии на попу Бекки."
            else:
                "Вы положили руки на попу вдовушки."
            if Friends[GirlNameIBD] >= 7 and sluttiness[GirlNameIBD] > 18:
                call ShowImage("", "", becky_dance_picture("butt_smile"))
                "Бекки улыбнулась и придвинулась к вам поближе, продолжая танец."
                call SlutFriendsIncrease(GirlNameIBD, 9, 3, 1, 18, 3, 1)
                $ HandsDance = 'ass'
            elif Friends[GirlNameIBD] >= 6 and sluttiness[GirlNameIBD] >= 12:
                call ShowImage("", "", becky_dance_picture("butt"))
                '"Стефан, негодник, что ты делаешь?!" прошептала Бекки, улыбаясь. "Впрочем, продолжай, добавила она."'
                call SlutFriendsIncrease(GirlNameIBD, 9, 3, 1, 18, 3, 1)
                $ HandsDance = 'ass'
            elif Friends[GirlNameIBD] >= 5 and sluttiness[GirlNameIBD] >= 9:
                call ShowImage("", "", becky_dance_picture("butt_angry"))
                '"Стефан, ай-ай-ай!" сказала вдовушка и передвинула ваши руки с попы на талию.'
                call SlutFriendsIncrease(GirlNameIBD, 9, 4, 1, 14, 4, 1)
                $ HandsDance = 'waist'
            else:
                call ShowImage("", "", becky_dance_picture("angry"))
                '"Стефан, негодник, что это ты такое делаешь?" спросила Бекки "Я тебе в матери гожусь, а ты что себе позволяешь?!" Вы попробовали объяснить, что вы так случайно поступили, но обнаружили что разговариваете с пустотой, Бекки ушла.'
                $ FridayDancesCount += 1
                $ DanceStep = DanceMaxIBD
                call SlutFriendsIncrease(GirlNameIBD, 0, 1, -1, 0, 1, -1)
                $ HandsDance = ''
            $ DanceStep += 1
            call becky_invite_home('Becky')
            if DanceStep == DanceMaxIBD:
                "Танец закончился и вы вернулись к колоннаде."
            jump int_becky_dance
        "Сжать попу вдовы" if DanceStep >= 2 and DanceStep < DanceMaxIBD and HandsDance == 'ass':
            "Ваши беспокойные ручки начали гладить и сжимать попку вдовушки."
            if Friends[GirlNameIBD] >= 10 and sluttiness[GirlNameIBD] > 20:
                call ShowImage("", "", becky_dance_picture("butt_smile"))
                "Бекки это пришлось по вкусу, она улыбнулась и прижалась вплотную к вам, начав приятно тереться своими дыньками о вашу грудь."
                call SlutFriendsIncrease(GirlNameIBD, 11, 4, 1, 22, 3, 1)
                $ HandsDance = 'ass2'
                $ TitsDance = 1
            elif Friends[GirlNameIBD] >= 8 and sluttiness[GirlNameIBD] >= 16:
                call ShowImage("", "", becky_dance_picture("butt"))
                '"Стефанчик, ах наглец, ах шалун!" прошептала Бекки с напускным гневом, но не сделала ничего, чтобы остановить вас.'
                call SlutFriendsIncrease(GirlNameIBD, 11, 4, 1, 22, 3, 1)
                $ HandsDance = 'ass2'
            elif Friends[GirlNameIBD] >= 7 and sluttiness[GirlNameIBD] >= 13:
                call ShowImage("", "", becky_dance_picture("butt_angry"))
                '"Стефан, ай-ай-ай!" сказала вдовушка и передвинула ваши руки с попы на талию.'
                call SlutFriendsIncrease(GirlNameIBD, 9, 4, 1, 16, 4, 1)
                $ HandsDance = 'waist'
            else:
                call ShowImage("", "", becky_dance_picture("angry"))
                '"Стефан, негодник, что это ты такое делаешь?" спросила Бекки "Я тебе в матери гожусь, а ты что себе позволяешь?!" Вы попробовали объяснить, что вы так случайно поступили, но обнаружили что разговариваете с пустотой, Бекки ушла.'
                $ FridayDancesCount += 1
                $ DanceStep = DanceMaxIBD
                call SlutFriendsIncrease(GirlNameIBD, 0, 1, -1, 0, 1, -1)
                $ HandsDance = ''
            $ DanceStep += 1
            call becky_invite_home('Becky')
            if DanceStep == DanceMaxIBD:
                "Танец закончился и вы вернулись к колоннаде."
            jump int_becky_dance
        "Поцеловать Бекки" if DanceStep >= 2 and DanceStep < DanceMaxIBD and KissDance == 0:
            "Продолжая танцевать, вы вдруг наклонились к вдове Блэнкеншип и впились в ее губы своими."
            if Friends[GirlNameIBD] >= 10 and sluttiness[GirlNameIBD] > 21:
                call ShowImage("", "", becky_dance_picture("french"))
                "Опытная вдовушка с готовностью и умением ответила на ваш поцелуй, страстно переплетаясь с вами языками."
                call SlutFriendsIncrease(GirlNameIBD, 11, 4, 1, 24, 3, 1)
                $ KissDance = 2
            elif Friends[GirlNameIBD] >= 8 and sluttiness[GirlNameIBD] >= 16:
                call ShowImage("", "", becky_dance_picture("kiss"))
                "Преодолев секундное замешательство, Бекки откликнулась на ваш поцелуй, хотя и, как вам показалось, была несколько шокированна вашей прямотой."
                call SlutFriendsIncrease(GirlNameIBD, 11, 4, 1, 24, 3, 1)
                $ KissDance = 1
            elif Friends[GirlNameIBD] >= 7 and sluttiness[GirlNameIBD] >= 13:
                call ShowImage("", "", becky_dance_picture("butt_angry"))
                '"Стефанчик, шалунишка, я же тебе в матери гожусь, а ты целоваться. И не стыдно?" прошептала Бекки и отстранилась от вас.'
                call SlutFriendsIncrease(GirlNameIBD, 9, 6, 1, 16, 6, 1)
                $ KissDance = 0
            else:
                call ShowImage("", "", becky_dance_picture("angry"))
                '"Стефан, негодник, что это ты такое делаешь?" спросила Бекки "Я тебе в матери гожусь, а ты что себе позволяешь?!" Вы не нашлись с подходящим объяснением ну да впрочем это было и неважно, Бекки ушла.'
                $ FridayDancesCount += 1
                $ DanceStep = DanceMaxIBD
                call SlutFriendsIncrease(GirlNameIBD, 0, 1, -1, 0, 1, -1)
                $ KissDance = 0
            $ DanceStep += 1
            call becky_invite_home('Becky')
            if DanceStep == DanceMaxIBD:
                "Танец закончился и вы вернулись к колоннаде."
            jump int_becky_dance
        "Принять предложение вдовы" if BeckyVar['danceinvitehome']:
            $ FridayDancesCount = 5
            jump becky_home_front_from_dances
        "Отойти" if DanceStep >= DanceMaxIBD or DanceStep == 1:
            $ CounterToClean = MaxCounterToClean
            call CleanScreenOverflow(CounterToClean)
            $ DanceStep = 0
            # dynamic $CurrentActions
            # dynamic $FridayDanceCounterShow
            return
    return

label becky_home_front_from_dances:
    call BeckyHomeFront("FromDances")
    return

# # Helper labels for menu actions
# label girls_desc(girl):
#     # ...show girl description...
#     return

# label slut_friends_increase(girl, a, b, c, d, e, f):
#     # ...logic for increasing slut friends...
#     return

# label becky_invite_home(girl):
#     # ...logic for Becky inviting home...
#     return

# label clean_screen_overflow():
#     # ...logic for cleaning screen overflow...
#     return

# label becky_home_front_from_dances():
#     # ...Becky home front event from dances...
#     return
