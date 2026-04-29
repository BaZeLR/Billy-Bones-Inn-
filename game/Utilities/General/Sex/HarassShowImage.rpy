# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label HarassShowImage(GirlNameHSI="", ActionHSI="", ReactionHSI=0, EyewitnessHSI=0, JobTypeHSI=""):
    if EyewitnessHSI > 0:
        if GirlNameHSI == "melissa":
            if ReactionHSI == 0:
                call ShowImage(GirlNameHSI, "grope", "inter")
            elif ActionHSI in ("ass", "dress"):
                if ReactionHSI >= 3:
                    call ShowImageSeq(GirlNameHSI, "grope", "assok", 2)
                else:
                    call ShowImage(GirlNameHSI, "grope", "assangry")
            else:
                if ReactionHSI >= 3:
                    call ShowImage(GirlNameHSI, "grope", "titok")
                elif ReactionHSI == 2:
                    call ShowImageSeq(GirlNameHSI, "grope", "titshy", 2)
                else:
                    call ShowImageSeq(GirlNameHSI, "grope", "titangry", 2)
        elif GirlNameHSI == "amanda":
            if ReactionHSI == 0:
                call ShowImage(GirlNameHSI, "grope", "inter")
            elif ActionHSI == "ass":
                if ReactionHSI >= 3:
                    call ShowImageSeq(GirlNameHSI, "grope", "assok", 2)
                elif ReactionHSI == 2:
                    call ShowImage(GirlNameHSI, "grope", "assshy")
                else:
                    call ShowImage(GirlNameHSI, "grope", "assangry")
            elif ActionHSI == "tits":
                if ReactionHSI >= 3:
                    call ShowImageSeq(GirlNameHSI, "grope", "titok", 2)
                elif ReactionHSI == 2:
                    call ShowImageSeq(GirlNameHSI, "grope", "titshy", 2)
                else:
                    call ShowImage(GirlNameHSI, "grope", "titangry")
            else:
                if panties.get(GirlNameHSI, "") == "":
                    if ReactionHSI >= 2:
                        call ShowImageSeq(GirlNameHSI, "grope", "dressnaked", 2)
                    else:
                        call ShowImage(GirlNameHSI, "grope", "dressnakedangry")
                else:
                    call ShowImage(GirlNameHSI, "grope", "dresspanties")
        elif GirlNameHSI == "sandra":
            if JobTypeHSI == "waitress":
                $ _sandra_pic = "waitress" + str(renpy.random.randint(1, 4))
            else:
                $ _sandra_pic = "cleaning1"
            call ShowImage(GirlNameHSI, "tavern", _sandra_pic)
    return
