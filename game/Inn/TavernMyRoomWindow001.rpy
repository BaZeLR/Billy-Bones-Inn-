# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 5 python:
    TavernMyRoomWindowObject = GameObject(
        object_id="myroom_window_001",
        name="Маленькое окно",
        description="Небольшое окно, из которого виден задний двор трактира.",
        picture="images/player_room/window0.png",
        actions=[
            ObjectAction(
                action_id="look_window",
                label="Посмотреть во двор",
                hook="call",
                target="TavernMyRoomWindowLookBackyard",
            ),
        ],
        carriable=False,
        stackable=False,
    )


label TavernMyRoomWindowLookBackyard:
    $ _window_hour = int(calendar_v2.hour or 0)
    $ _window_is_night = _window_hour >= 18 or _window_hour < 6

    if _window_is_night and amanda_night_bowl_window_event_ready():
        $ Amanda.set_var_int("night_bowl_window_seen_day", int(calendar_v2.daysInGame or 0))
        if amanda_prefers_backyard_relief():
            $ Amanda.change_social(corruption_delta=2)
            $ action_override_text = "Вы осторожно выглядываете во двор и замечаете, как Аманда, кутаясь в ночную рубашку и недовольно озираясь по сторонам, все равно выбирается наружу. Похоже, даже получив новый горшок, она не до конца отказалась от ночных вылазок. Аманда, краснея даже в темноте, торопливо присаживается у забора, делает свое дело и почти бегом скрывается обратно в доме."
        else:
            $ Amanda.change_social(corruption_delta=1)
            $ action_override_text = "Вы осторожно выглядываете во двор и замечаете, как Аманда, кутаясь в ночную рубашку и недовольно озираясь по сторонам, торопливо выскальзывает наружу. Без своей привычной ночной миски ей приходится искать облегчения во дворе. Аманда, краснея даже в темноте, поспешно присаживается у забора, делает свое дело и почти бегом скрывается обратно в доме."
        $ TavernMyRoomWindowObject.picture = "images/player_room/windowAmand.png"
    elif _window_is_night:
        $ action_override_text = "Ночь делает задний двор почти безлюдным. В синем свете луны видны старая будка нужника, колодец, бочка у стены и темная крыша сарая. Только огонь во дворе и редкие огоньки в окнах напоминают, что трактир еще не спит."
        $ TavernMyRoomWindowObject.picture = "images/player_room/window2.png"
    else:
        $ action_override_text = "Через маленькое окно хорошо виден задний двор трактира: мокрая земля у колодца, низкий нужник у забора, поленница возле сарая и кострище, возле которого обычно сушат вещи после дождя. Двор выглядит тесным, рабочим и по-домашнему знакомым."
        $ TavernMyRoomWindowObject.picture = "images/player_room/window0.png"

    call TavernMyRoomObjectMenu("myroom_window_001")
    $ TavernMyRoomWindowObject.picture = ""
    return
