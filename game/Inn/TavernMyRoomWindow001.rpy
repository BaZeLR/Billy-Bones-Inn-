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
    $ renpy.dynamic("_window_hour", "_window_is_night", "_window_text")
    $ _window_hour = int(calendar_v2.hour or 0)
    $ _window_is_night = _window_hour >= 18 or _window_hour < 6
    call checkTriggers("TavernMyRoom", "window_look", 0)
    if _return:
        return

    if _window_is_night:
        $ _window_text = "Ночь делает задний двор почти безлюдным. В синем свете луны видны старая будка нужника, колодец, бочка у стены и темная крыша сарая. Только огонь во дворе и редкие огоньки в окнах напоминают, что трактир еще не спит."
        $ TavernMyRoomWindowObject.picture = "images/player_room/window2.png"
    else:
        $ _window_text = "Через маленькое окно хорошо виден задний двор трактира: мокрая земля у колодца, низкий нужник у забора, поленница возле сарая и кострище, возле которого обычно сушат вещи после дождя. Двор выглядит тесным, рабочим и по-домашнему знакомым."
        $ TavernMyRoomWindowObject.picture = "images/player_room/window0.png"

    call TavernMyRoomObjectMenu("myroom_window_001", _window_text)
    $ TavernMyRoomWindowObject.picture = ""
    return


label story_amanda_night_bowl_window_0:
    $ renpy.dynamic("_window_text")
    if Amanda.prefers_backyard_relief():
        $ Amanda.change_social(corruption_delta=2)
        $ _window_text = "Вы осторожно выглядываете во двор и замечаете, как Аманда, кутаясь в ночную рубашку и недовольно озираясь по сторонам, все равно выбирается наружу. Похоже, даже получив новый горшок, она не до конца отказалась от ночных вылазок. Аманда, краснея даже в темноте, торопливо присаживается у забора, делает свое дело и почти бегом скрывается обратно в доме."
    else:
        $ Amanda.change_social(corruption_delta=1)
        $ _window_text = "Вы осторожно выглядываете во двор и замечаете, как Аманда, кутаясь в ночную рубашку и недовольно озираясь по сторонам, торопливо выскальзывает наружу. Без своей привычной ночной миски ей приходится искать облегчения во дворе. Аманда, краснея даже в темноте, поспешно присаживается у забора, делает свое дело и почти бегом скрывается обратно в доме."
    $ TavernMyRoomWindowObject.picture = "images/player_room/windowAmand.png"
    call TavernMyRoomObjectMenu("myroom_window_001", _window_text)
    $ TavernMyRoomWindowObject.picture = ""
    return True
