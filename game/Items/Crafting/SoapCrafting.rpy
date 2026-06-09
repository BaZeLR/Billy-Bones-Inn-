# Improved Soap Crafting System - Second Stage Focus
#
# IMPORTANT (per user directive):
# - Do NOT change the first stage in Backyard (ash barrel, bowl possession, ingredient logic).
# - The first stage (gathering/prep) stays exactly as it is.
# - This file enhances ONLY the SECOND STAGE (the timer completion part).
#
# When the timer for the second stage finishes, we call into the logic here
# to let the player choose TYPE (household vs luxury olive) and AROMAS.
#
# References:
# - BackyardCookSoap in game/Inn/SoapCraftAndAtticItems.rpy (first stage + timer start)
# - HouseholdRuntimeEvents.rpy (existing girl soap request events)
# - SCRIPT_TIME_UI_PATTERN_NOTES.md (mentions soap timers)

init python:
    # Available aromas for soap (can be expanded)
    # Each aroma has id, display name, and possible effects (for later use)
    SOAP_AROMAS = {
        "lavender": {
            "name_en": "Lavender",
            "name_ru": "Лаванда",
            "desc_ru": "Спокойный, цветочный аромат. Хорошо расслабляет и маскирует запахи.",
        },
        "rose": {
            "name_en": "Rose",
            "name_ru": "Роза",
            "desc_ru": "Классический благородный аромат. Считается роскошным.",
        },
        "citrus": {
            "name_en": "Citrus",
            "name_ru": "Цитрус",
            "desc_ru": "Свежий, бодрящий запах. Хорошо освежает по утрам.",
        },
        "rosemary": {
            "name_en": "Rosemary",
            "name_ru": "Розмарин",
            "desc_ru": "Травянистый, чистый аромат. Полезен для волос и концентрации.",
        },
        "mint": {
            "name_en": "Mint",
            "name_ru": "Мята",
            "desc_ru": "Охлаждающий, очень свежий. Отлично для летнего мыла.",
        },
        "sandalwood": {
            "name_en": "Sandalwood",
            "name_ru": "Сандал",
            "desc_ru": "Тёплый, древесный, дорогой запах. Для изысканного туалетного мыла.",
        },
    }

    def get_available_soap_aromas(soap_type="luxury"):
        """Returns list of aroma ids available for this soap type."""
        if soap_type == "household":
            # Basic soap gets fewer options or none
            return ["lavender", "rosemary"]
        else:
            # Luxury olive oil soap - full choice
            return list(SOAP_AROMAS.keys())

# Main improved soap crafting label
# Call this instead of (or after) the original BackyardCookSoap logic
label CraftSoapPlayerChoice(recipe_id="luxury_soap_recipe"):
    # recipe_id can be "soap_recipe" (household) or "luxury_soap_recipe" (olive oil)
    show screen main_ui

    $ soap_type = "household" if recipe_id == "soap_recipe" else "luxury"
    $ available_aromas = get_available_soap_aromas(soap_type)

    if soap_type == "household":
        $ MainTxt = "Вы варите обычное хозяйственное мыло.\n\n"
        $ MainTxt += "Для простого мыла доступны только базовые добавки."
    else:
        $ MainTxt = "Вы готовите роскошное туалетное мыло на оливковом масле.\n\n"
        $ MainTxt += "Теперь можно выбрать, какие ароматы добавить. Вы можете добавить несколько."

    $ CurLocDesc = MainTxt

    # Player selects aromas (not random anymore)
    $ chosen_aromas = []

    if not available_aromas:
        $ MainTxt += "\n\nДля этого типа мыла ароматы не предусмотрены."
        jump CraftSoapFinalize

    menu:
        "Выбрать ароматы для мыла":

            python:
                # Simple sequential choice (classic Ren'Py style, no complex multi-select)
                for aroma_id in available_aromas:
                    aroma = SOAP_AROMAS[aroma_id]
                    choice_text = "Добавить %s?" % aroma["name_ru"]

                    # In real implementation you would use a proper yes/no or multi menu
                    # Here we simulate player choice via menu for clarity
                    pass

            # For now we present a practical multi-choice menu
            # Player can pick several

            $ aroma_choices = []
            python:
                for aid in available_aromas:
                    a = SOAP_AROMAS[aid]
                    aroma_choices.append( (a["name_ru"], aid) )

            # After screen or menu, chosen_aromas should be populated
            # For this label we use a simple implementation below

        "Не добавлять ароматы":
            $ chosen_aromas = []
            jump CraftSoapFinalize

    # Simple aroma selection loop using classic menu (repeatable until player is satisfied)
label soap_aroma_selection_loop:
    $ MainTxt = "Текущие выбранные ароматы: "
    if chosen_aromas:
        python:
            names = [SOAP_AROMAS[a]["name_ru"] for a in chosen_aromas]
            MainTxt += ", ".join(names)
    else:
        $ MainTxt += "пока ничего"

    menu:
        "Добавить лаванду" if "lavender" in available_aromas and "lavender" not in chosen_aromas:
            $ chosen_aromas.append("lavender")
            jump soap_aroma_selection_loop

        "Добавить розу" if "rose" in available_aromas and "rose" not in chosen_aromas:
            $ chosen_aromas.append("rose")
            jump soap_aroma_selection_loop

        "Добавить цитрус" if "citrus" in available_aromas and "citrus" not in chosen_aromas:
            $ chosen_aromas.append("citrus")
            jump soap_aroma_selection_loop

        "Добавить розмарин" if "rosemary" in available_aromas and "rosemary" not in chosen_aromas:
            $ chosen_aromas.append("rosemary")
            jump soap_aroma_selection_loop

        "Добавить мяту" if "mint" in available_aromas and "mint" not in chosen_aromas:
            $ chosen_aromas.append("mint")
            jump soap_aroma_selection_loop

        "Добавить сандал" if "sandalwood" in available_aromas and "sandalwood" not in chosen_aromas:
            $ chosen_aromas.append("sandalwood")
            jump soap_aroma_selection_loop

        "Готово, варить мыло":
            jump CraftSoapFinalize

        "Сбросить выбор ароматов":
            $ chosen_aromas = []
            jump soap_aroma_selection_loop

label CraftSoapFinalize:
    # Here you would normally consume ingredients and create the item
    # For now we just record what was chosen

    $ MainTxt = "Вы завершили варку мыла.\n\n"

    if chosen_aromas:
        python:
            aroma_names = [SOAP_AROMAS[a]["name_ru"] for a in chosen_aromas]
            MainTxt += "Вы добавили следующие ароматы: " + ", ".join(aroma_names) + ".\n"
            MainTxt += "Мыло получилось ароматным и качественным."
    else:
        $ MainTxt += "Вы сварили простое мыло без дополнительных ароматов."

    $ CurLocDesc = MainTxt

    # TODO: Create actual item with chosen aromas stored in its data
    # Example: Create runtime item "luxury_soap" with .aromas = chosen_aromas

    # For integration with existing system, you can set:
    # $ SoapLastAromas = chosen_aromas   # or store on the created item

    return


# =============================================================================
# SECOND STAGE SOAP COOKING (Timer Completion)
# =============================================================================
# This is called when the second stage timer finishes in the Backyard flow.
# First stage (ingredients, ash barrel, bowl) remains untouched in BackyardCookSoap.
#
# Here the player chooses:
# - Soap type: household vs luxury (olive oil)
# - Aromas (player selected, not random)
#
# The resulting soap is a proper inventory object with parameters.

label SoapSecondStageFinish:
    # Called from the timer completion label in SoapCraftAndAtticItems.rpy / Backyard
    show screen main_ui

    $ MainTxt = "Варка мыла во второй стадии завершена.\n\n"
    $ MainTxt += "Теперь можно выбрать тип мыла и ароматы."

    menu:
        "Сделать обычное хозяйственное мыло":
            $ soap_type = "household"
            $ chosen_aromas = []   # basic soap gets no/limited choice
            jump SoapSecondStageFinalize

        "Сделать роскошное туалетное мыло на оливковом масле":
            $ soap_type = "luxury"
            jump SoapChooseAromas

label SoapChooseAromas:
    $ available = ["lavender", "rose", "citrus", "rosemary", "mint", "sandalwood"]
    $ chosen_aromas = []

    menu SoapAromaMenu:
        "Добавить лаванду" if "lavender" not in chosen_aromas:
            $ chosen_aromas.append("lavender")
            jump SoapAromaMenu
        "Добавить розу" if "rose" not in chosen_aromas:
            $ chosen_aromas.append("rose")
            jump SoapAromaMenu
        "Добавить цитрус" if "citrus" not in chosen_aromas:
            $ chosen_aromas.append("citrus")
            jump SoapAromaMenu
        "Добавить розмарин" if "rosemary" not in chosen_aromas:
            $ chosen_aromas.append("rosemary")
            jump SoapAromaMenu
        "Добавить мяту" if "mint" not in chosen_aromas:
            $ chosen_aromas.append("mint")
            jump SoapAromaMenu
        "Добавить сандал" if "sandalwood" not in chosen_aromas:
            $ chosen_aromas.append("sandalwood")
            jump SoapAromaMenu
        "Готово":
            jump SoapSecondStageFinalize
        "Сбросить выбор":
            $ chosen_aromas = []
            jump SoapAromaMenu

label SoapSecondStageFinalize:
    # Create the actual soap item as a proper object and add to inventory
    python:
        import renpy.store as store

        # Create a unique item id
        if soap_type == "luxury":
            base_id = "luxury_soap"
            name = "Роскошное оливковое мыло"
            if chosen_aromas:
                aroma_names = [SOAP_AROMAS[a]["name_ru"] for a in chosen_aromas]
                name += " (" + ", ".join(aroma_names) + ")"
        else:
            base_id = "household_soap"
            name = "Хозяйственное мыло"

        # Create runtime item (following existing runtime item pattern in the project)
        item_id = store.create_runtime_item(base_id, name=name)

        # Attach parameters to the item object
        if hasattr(store, 'items') and item_id in store.items:
            it = store.items[item_id]
            it.soap_type = soap_type
            it.aromas = chosen_aromas[:]
            it.quality = 80 if soap_type == "luxury" else 40
            it.created_day = store.dayspassed

        # Add to player inventory
        store._player_add_item_by_id(item_id, 1)

        # Set flag so room table version knows not to duplicate
        store.BeckyVar = getattr(store, 'BeckyVar', {})
        store.BeckyVar['soap_process'] = True   # or a more global soap_in_progress flag

    $ MainTxt = "Вы закончили варку мыла.\n\n"
    if soap_type == "luxury" and chosen_aromas:
        $ MainTxt += "Получилось отличное ароматное туалетное мыло."
    else:
        $ MainTxt += "Получилось обычное хозяйственное мыло."

    $ CurLocDesc = MainTxt

    # Time cost + fun for the activity
    $ calendar_v2.advance_minutes(90)

    return


# =============================================================================
# SOAP EFFECTS, DECAY, AND GIRL REQUEST SYSTEM
# =============================================================================

# Room table protection (simple flag)
label RoomTableStartSoap:
    python:
        if getattr(renpy.store, 'BeckyVar', {}).get('soap_process', False):
            renpy.notify("Вы уже начали варить мыло. Завершите второй этап.")
            renpy.return_statement()
    $ BeckyVar['soap_process'] = True
    $ MainTxt = "Вы начинаете готовить мыло за столом в комнате."
    return


# Call this when player uses soap on self or gifts it
label UseOrGiftSoap(item_id, target="player", girl=None):
    python:
        store = renpy.store
        it = store.items.get(item_id) if hasattr(store, 'items') else None

        if not it:
            renpy.return_statement()

        soap_type = getattr(it, 'soap_type', 'household')
        aromas = getattr(it, 'aromas', [])

        # === EFFECTS ===
        quality = getattr(it, 'quality', 40)

        # Health + Look
        if hasattr(store, 'health'):
            store.health = min(100, store.health + (8 if soap_type == "luxury" else 3))
        if hasattr(store, 'look'):
            store.look = min(100, store.look + (12 if soap_type == "luxury" else 5))

        # Female attraction + "tightness / youth" bonus (game specific)
        attraction_bonus = 15 if soap_type == "luxury" else 5
        if aromas:
            attraction_bonus += len(aromas) * 3

        # Store temporary effect on player or girl
        if target == "player":
            if not hasattr(store, 'soap_effects'):
                store.soap_effects = {}
            store.soap_effects['player'] = {
                'day': store.dayspassed,
                'attraction': attraction_bonus,
                'youth': 8 if soap_type == "luxury" else 3,
                'tightness': 6 if soap_type == "luxury" else 2
            }
        else:
            # For gifting to specific girl
            if not hasattr(store, 'girl_soap_effects'):
                store.girl_soap_effects = {}
            store.girl_soap_effects[girl] = {
                'day': store.dayspassed,
                'preferred_type': soap_type,
                'aromas': aromas
            }

        # Remove the soap item (it gets used up)
        store._player_remove_item_by_id(item_id, 1)

        # Schedule decay / request event in ~7 days
        if not hasattr(store, 'pending_soap_requests'):
            store.pending_soap_requests = []
        store.pending_soap_requests.append({
            'girl': girl,
            'expire_day': store.dayspassed + 7,
            'preferred_type': soap_type
        })

    return


# Mini-event: Girl asks for more soap (triggered from NewDay or location entry)
label GirlSoapRequest(girl):
    python:
        store = renpy.store
        prefs = store.girl_soap_effects.get(girl, {})
        preferred = prefs.get('preferred_type', 'household')

    $ MainTxt = "%s выглядит свежей и довольной." % store.RealName.get(girl, girl)

    if preferred == "luxury":
        $ MainTxt += "\n\nОна тихо говорит, что очень привыкла к хорошему ароматному мылу и было бы здорово получить ещё."
    else:
        $ MainTxt += "\n\nОна отмечает, что обычное мыло тоже неплохо, но хорошее — совсем другое дело."

    menu:
        "Дать ей кусок [preferred] мыла (если есть)":
            # Check inventory for matching soap and give it
            python:
                # Simplified - real version would search inventory
                pass
            "Она очень рада и готова оказать небольшую услугу."

        "Попросить взамен небольшую услугу":
            call GirlSoapFavorNegotiation(girl) from _call_soap_favor

        "Сказать, что сейчас нет":
            "Она немного расстроена, но понимает."

            if store.dayspassed - prefs.get('last_gift_day', 0) > 3:
                python:
                    store.Friends[girl] = max(0, store.Friends.get(girl, 50) - 5)
                "Отношения немного ухудшились из-за долгого ожидания."

    return


label GirlSoapFavorNegotiation(girl):
    menu:
        "Попросить поцеловать":
            "Она соглашается с улыбкой."

        "Попросить небольшую сумму денег":
            "Она даёт немного монет."

        "Попросить помочь с чем-то по дому":
            "Она соглашается помочь."

        "Просто подарить без просьбы":
            "Она искренне благодарна."

    return
