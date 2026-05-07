# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default TavernMyRoomAtticHatchFound = 0

init 5 python:
    def tavern_my_room_attic_hatch_visible():
        return int(exploration or 0) >= 15 or melissa_bats_stage() >= 3

    def tavern_my_room_attic_hatch_can_search(_obj=None):
        return tavern_my_room_attic_hatch_visible() and int(TavernMyRoomAtticHatchFound or 0) == 0

    def tavern_my_room_attic_hatch_can_enter(_obj=None):
        return tavern_my_room_attic_hatch_visible() and (int(TavernMyRoomAtticHatchFound or 0) == 1 or melissa_bats_stage() >= 3)

    TavernMyRoomAtticHatchObject = GameObject(
        object_id="myroom_attic_hatch_001",
        name="Люк на чердак",
        description="Под потолком обнаруживается старый люк с железным кольцом.",
        actions=[
            ObjectAction(
                action_id="examine_attic_hatch",
                label="Осмотреть люк",
                hook="text",
                target="Старый деревянный люк ведет на чердак. Он закрыт, но открыть его при желании несложно.",
            ),
            ObjectAction(
                action_id="search_attic_hatch",
                label="Осмотреть люк получше",
                hook="call",
                target="TavernMyRoomAtticHatchSearch",
                condition=tavern_my_room_attic_hatch_can_search,
            ),
            ObjectAction(
                action_id="enter_attic",
                label="Открыть люк и подняться наверх",
                hook="jump",
                target="TavernAtic",
                condition=tavern_my_room_attic_hatch_can_enter,
            ),
        ],
        condition=tavern_my_room_attic_hatch_visible,
        carriable=False,
        stackable=False,
    )


label TavernMyRoomAtticHatchSearch:
    if not tavern_my_room_attic_hatch_visible():
        $ MainTxt = "Пока вы слишком плохо ориентируетесь в хозяйстве трактира, чтобы заметить здесь что-то полезное."
    elif int(TavernMyRoomAtticHatchFound or 0) == 0:
        $ TavernMyRoomAtticHatchFound = 1
        $ MainTxt = "Вы подтаскиваете табурет, ощупываете потолочную балку и понимаете, что люк на чердак держится на простом крюке. Теперь вы знаете, как его открыть."
    else:
        $ MainTxt = "Вы уже разобрались, как открыть этот люк на чердак."
    $ CurLocDesc = MainTxt
    call TavernMyRoomObjectMenu("myroom_attic_hatch_001")
    return
