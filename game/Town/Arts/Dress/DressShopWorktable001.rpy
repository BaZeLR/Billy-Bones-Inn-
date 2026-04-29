# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def dress_shop_worktable_has_order(_obj=None):
        return str(DressProduced or "") != ""

    DressShopWorktableObject = GameObject(
        object_id="worktable_001",
        name="Рабочий стол Ирмы",
        description="Большой рабочий стол, заваленный тканями, кружевами и выкройками.",
        actions=[
            ObjectAction(
                action_id="ask_order_status",
                label="Спросить, когда будет готово",
                hook="text",
                target="Вы осведомились у Ирмы, скоро ли будет готов ваш заказ. Она подняла на вас удивленный взгляд и ответила, что, как она и говорила, закончит работу к завтрашнему утру.",
                condition=dress_shop_worktable_has_order,
            ),
            ObjectAction(
                action_id="examine_worktable",
                label="Осмотреть рабочий стол",
                hook="text",
                target="На столе царит рабочий порядок: ткани, выкройки и инструменты лежат именно там, где Ирма привыкла их держать.",
            ),
        ],
        carriable=False,
        stackable=False,
    )
