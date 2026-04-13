init 5 python:
    TavernMyRoomWindowObject = GameObject(
        object_id="myroom_window_001",
        name="Маленькое окно",
        description="Небольшое окно, из которого виден задний двор трактира.",
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
    if amanda_night_bowl_window_event_ready():
        $ AmandaVar["night_bowl_window_seen_day"] = int(dayspassed or 0)
        if amanda_prefers_backyard_relief():
            $ sluttiness["amanda"] = min(100, int(sluttiness.get("amanda", 0) or 0) + 2)
            $ action_override_text = "Вы осторожно выглядываете во двор и замечаете, как Аманда, кутаясь в ночную рубашку и недовольно озираясь по сторонам, все равно выбирается наружу. Похоже, даже получив новый горшок, она не до конца отказалась от ночных вылазок. Сестренка, краснея даже в темноте, торопливо присаживается у забора, делает свое дело и почти бегом скрывается обратно в доме."
        else:
            $ sluttiness["amanda"] = min(100, int(sluttiness.get("amanda", 0) or 0) + 1)
            $ action_override_text = "Вы осторожно выглядываете во двор и замечаете, как Аманда, кутаясь в ночную рубашку и недовольно озираясь по сторонам, торопливо выскальзывает наружу. Без своей привычной ночной миски ей приходится искать облегчения во дворе. Сестренка, краснея даже в темноте, поспешно присаживается у забора, делает свое дело и почти бегом скрывается обратно в доме."
        python:
            _window_picture = "images/tavern/backyard/pees_in_backyard.png"
            if renpy.loadable(_window_picture):
                TavernMyRoomWindowObject.picture = _window_picture
    else:
        $ action_override_text = "Через маленькое окно виден задний двор трактира. В темноте смутно различаются бочка, нужник и раскисшая земля у забора. Сейчас там ничего особенно интересного не происходит."
        $ TavernMyRoomWindowObject.picture = ""
    call TavernMyRoomObjectMenu("myroom_window_001")
    $ TavernMyRoomWindowObject.picture = ""
    return
