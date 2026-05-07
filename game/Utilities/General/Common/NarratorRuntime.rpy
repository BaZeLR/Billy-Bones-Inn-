# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
image side tractir_narrator = Transform("images/general/narrator.png", zoom=0.72)

define tractir_narrator_char = Character(
    None,
    image="tractir_narrator",
    what_color="#f0e6d2",
    what_italic=True,
)

define n = tractir_narrator_char

init python:
    def tractir_narrate(text):
        renpy.say(tractir_narrator_char, str(text or ""))

label narrator_test:
    n "The narrator can now speak from ordinary labels while keeping a side portrait in the dialogue window."
    $ tractir_narrate("Python-driven events can use the same narrator through tractir_narrate().")
    return
