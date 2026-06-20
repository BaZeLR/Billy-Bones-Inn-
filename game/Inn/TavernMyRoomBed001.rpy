# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 5 python:
    def tavern_my_room_can_sleep(obj=None):
        return bool(_player_can_sleep_now())

    TavernMyRoomBedObject = GameObject(
        object_id="bed_001",
        name="Кровать",
        description="Простая кровать, на которой можно поспать до утра.",
        picture="images/player_room/from_bed.png",
        actions=[
            ObjectAction(
                action_id="sleep_until_morning",
                label="Лечь спать до утра",
                hook="call",
                target="Sleep",
                args=("TavernMain", 1, "Вы ложитесь на кровать и быстро проваливаетесь в сон.", "TavernMyRoom", "bed_001"),
                condition=tavern_my_room_can_sleep,
            ),
            ObjectAction(
                action_id="rest_on_bed",
                label="Немного отдохнуть",
                hook="call",
                target="Rest",
                args=("TavernMyRoom", 120, 15, "Вы прилегли отдохнуть, чтобы перевести дух.", "TavernMyRoom", "bed_001"),
            ),
            ObjectAction(
                action_id="examine_bed",
                label="Осмотреть кровать",
                hook="text",
                target="Обычная кровать. Сейчас вам вполне достаточно и ее.",
            ),
        ],
        carriable=False,
        stackable=False,
    )
