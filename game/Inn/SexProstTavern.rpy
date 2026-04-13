label SexProstTavern(args0=0, args1=""):
    if args0 != 1:
        jump TavernMain

    $ GirlNameSP = args1
    if not GirlNameSP:
        jump TavernMain

    if GirlNameSP == "georgett":
        "Вы заплатили Жоржетте четыре мараведи и ведете ее в комнату в задней части вашего трактира. Как только задвижка захлопнулась, Жоржетта развернулась к вам и впилась в ваши губы глубоким поцелуем."
    else:
        "Вы заплатили Лизетте четыре мараведи и повели ее в комнату в задней части вашего трактира. Закрыв дверь, вы прижали девчушку к стене и впились в ее губы сладким поцелуем."
    call BeginPaidSexModule(GirlNameSP, "TavernMain")

    if GirlNameSP == "georgett":
        "Вы находитесь в скромно обставленной комнате вашего трактира. Вместе с вами в ней страстная Жоржетта."
        call IntGeorgettSex(GirlNameSP, "tavern")
    else:
        "Вы находитесь в скромно обставленной комнате вашего трактира.  Вместе с вами в ней юная Лизетта."
        call IntLizaSex(GirlNameSP, "tavern")

    call FinishPaidSexModule(GirlNameSP, "TavernMain")
    return
