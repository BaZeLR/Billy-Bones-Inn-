# game/Events/HouseholdMiniEvents.rpy

label HouseholdEvent_Try(location_code="", mode="room"):

    $ _household_event = household_ai_pick_event(location_code, mode)

    if _household_event == "":
        return

    if household_ai_seen(_household_event, location_code):
        return

    $ household_ai_mark_seen(_household_event, location_code)
    $ _household_label = household_ai_event_label(_household_event)

    if _household_label != "":
        call expression _household_label

    return


label HouseholdEvent_KitchenAmandaSandraSpark:

    "The kitchen is already too warm, and not only because of the fire."

    "Sandra stands near the table, making notes with a face that promises more work before breakfast is over."

    "Sandra: If this house is going to survive, someone here must remember discipline."

    "Amanda looks up from her task."

    "Amanda: Funny. Discipline always means our hands are busy and your mouth is free."

    "Melissa almost laughs, then hides it behind her cup."

    "Sandra: Watch yourself."

    "Amanda’s smile becomes sharper."

    "Amanda: I am watching. That is the problem."

    "For a moment the whole kitchen goes quiet."

    menu:
        "Tell Amanda to return to work":
            "Amanda obeys, but her eyes stay angry."
            $ household_ai_reduce_drive("amanda", 0.20)
            $ household_ai_raise_friction(0.06)

        "Tell Sandra to stop provoking her":
            "Sandra closes her notebook slowly."
            "Sandra: So now I am the problem?"
            $ household_ai_reduce_drive("sandra", 0.15)
            $ household_ai_raise_friction(0.08)

        "Tell both of them the tavern comes first":
            "Neither of them looks pleased, but both understand the point."
            $ household_ai_raise_convergence(0.08)
            $ household_ai_reduce_drive("amanda", 0.12)
            $ household_ai_reduce_drive("sandra", 0.12)

    return


label HouseholdEvent_KitchenMelissaPracticalComplaint:

    "Melissa watches the room like she is counting every missing coin and every dirty plate."

    "Melissa: We cannot keep pretending everything is fine."

    "She nods toward the shelves."

    "Melissa: Food, clean cloth, repairs. If those fail, everyone starts fighting over favors instead of working."

    "Sandra: At least someone here can count."

    "Melissa smiles thinly."

    "Melissa: I can count. I can also remember who gets help first."

    menu:
        "Promise to fix supplies":
            "Melissa relaxes a little."
            $ household_ai_raise_convergence(0.06)
            $ household_ai_reduce_drive("melissa", 0.15)

        "Tell her to manage with what she has":
            "Melissa says nothing, but her expression becomes colder."
            $ household_ai_raise_friction(0.08)

        "Ask what she needs most":
            "Melissa: Security first. Then comfort. Then everyone becomes much easier to deal with."
            $ household_ai_raise_convergence(0.04)

    return


label HouseholdEvent_BreakfastSquirrelMockery:

    "Breakfast begins with small noises, small looks, and the kind of silence that is not peaceful."

    "Amanda: So, who is pretending to be innocent today?"

    "Melissa: Depends. Who is pretending hardest?"

    "Amanda laughs."

    "Sandra looks from one girl to the other."

    "Sandra: Eat. Work. Then talk."

    "Amanda: There. The household sermon."

    "Melissa taps her spoon against the bowl."

    "Melissa: Careful. Sermons get longer when the tavern is poor."

    menu:
        "Let them mock each other":
            "The table grows louder, but nobody leaves."
            $ household_ai_raise_friction(0.06)

        "Cut it short":
            "The silence that follows is worse than the noise."
            $ household_ai_raise_friction(0.04)
            $ household_ai_reduce_drive("sandra", 0.10)

        "Turn it into work planning":
            "They complain, but the conversation becomes useful."
            $ household_ai_raise_convergence(0.08)

    return


label HouseholdEvent_AmandaPrivatePressure:

    "Amanda finds a reason to be near you when nobody else is close."

    "She does not ask directly. That would be too simple."

    "Amanda: You always notice what is missing from the tavern."

    "She steps closer."

    "Amanda: Do you notice what is missing from me?"

    menu:
        "Ask what she wants":
            "Amanda: Depends what you can afford. Attention is cheap. Pretty things are not."
            $ AmandaVar["attention_hint_day"] = dayspassed
            $ household_ai_reduce_drive("amanda", 0.16)

        "Tell her she is fishing for favors":
            "Amanda smiles, but not kindly."
            "Amanda: Then maybe learn to bait the hook better."
            $ household_ai_raise_friction(0.05)

        "Tell her later":
            "She accepts it badly, but she accepts it."
            $ AmandaNeedBlocked["amanda"] = 1
            $ household_ai_raise_friction(0.04)

    return


label HouseholdEvent_SandraPrivateCheck:

    "Sandra appears at the wrong time with the exact face of someone who knows it."

    "Sandra: I wanted to see whether you are managing the house or letting it manage you."

    "She looks around, not accusing directly, which somehow makes it worse."

    menu:
        "Ask what she really wants":
            "Sandra: Order. Security. And not watching the girls tear each other apart over scraps."
            $ household_ai_reduce_drive("sandra", 0.15)
            $ household_ai_raise_convergence(0.05)

        "Tell her you are the manager":
            "Sandra: Then manage."
            $ household_ai_raise_friction(0.06)

        "Ask for her help with the girls":
            "Sandra studies you for a long moment."
            "Sandra: Then stop rewarding chaos."
            $ household_ai_raise_convergence(0.06)

    return


label HouseholdEvent_ThreeWomenConverge:

    "For once, nobody starts the morning by fighting."

    "Sandra has notes, Melissa has numbers, Amanda has objections — but they are all looking at the same problem."

    "Sandra: If the house holds, everyone eats."

    "Melissa: If everyone eats, everyone behaves better."

    "Amanda: Do not make it sound too noble. I still want my share."

    "Sandra almost smiles."

    "Sandra: Good. Wanting a share means you intend to stay."

    menu:
        "Tell them this is how the household survives":
            "For a rare moment, all three seem to accept it."
            $ household_ai_raise_convergence(0.12)

        "Promise rewards when the tavern improves":
            "Amanda likes the word reward. Melissa likes the word when. Sandra likes the word improves."
            $ household_ai_raise_convergence(0.10)

    return
