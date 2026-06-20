# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
                target="checkTriggers",
                args=("TavernAmandaRoom", "amanda_grope", 0),
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
