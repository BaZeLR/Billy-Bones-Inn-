init python:
    def tavern_amanda_bed_action_available():
        return time >= 4 and cametoday < cancumdaily

    TavernAmandaBedObject = GameObject(
        object_id="bed_002",
        name="Кровать",
        description="Кровать Аманды, аккуратно застеленная или занятая самой хозяйкой комнаты.",
        actions=[
            ObjectAction(
                action_id="approach_bed",
                label="Пристать к Аманде",
                hook="call",
                target="TavernAmandaRoomGropeAction",
                condition=tavern_amanda_bed_action_available,
            ),
            ObjectAction(
                action_id="examine_bed",
                label="Осмотреть кровать",
                hook="text",
                target="Аккуратная кровать у стены. По вечерам Аманда спит именно здесь.",
            ),
        ],
        carriable=False,
        stackable=False,
    )
