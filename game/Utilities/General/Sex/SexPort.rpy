# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label SexPort(args0=0, args1=""):
    if args0 != 1:
        jump PortStreets

    $ GirlNameSP = args1
    if not GirlNameSP:
        jump PortStreets

    if GirlNameSP == "georgett":
        "Вы заплатили Жоржетте восемь мараведи и она повела вас в один из переулков, заверяя что там вас никто не потревожит. Вы последовали за ней. Вскоре вы оказались в одной из подворотен. Жоржетта развернулась к вам и впилась в ваши губы глубоким поцелуем."
    else:
        "Вы заплатили Лизетте восемь мараведи и повели ее переулками в знакомую подворотню. Дойдя до места, вы прижали девчушку к стене и впились в ее губы сладким поцелуем."
    call BeginPaidSexModule(GirlNameSP, "PortStreets")

    if GirlNameSP == "georgett":
        "Вы находитесь в переулке. Рядом с вами страстная Жоржетта."
        call IntGeorgettSex(GirlNameSP)
    else:
        "Вы находитесь в переулке. Рядом с вами юная Лизетта."
        call IntLizaSex(GirlNameSP)

    call FinishPaidSexModule(GirlNameSP, "PortStreets")
    return
