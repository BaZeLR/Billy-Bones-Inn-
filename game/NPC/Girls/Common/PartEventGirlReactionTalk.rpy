# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default Result = ""

# PartEventGirlReactionTalk location - converted from legacy script
label PartEventGirlReactionTalk(GirlNamePEGRT1, GirlNamePEGRT2, FriendVarToChange, DefiniteAccept, FriendLimit, SlutLimit):
    $ BeleiveFriend = 0
    # Дополнительный шанс поверить, если подруги
    python:
        def _pegrt_int(value, default=0):
            try:
                return int(value)
            except Exception:
                try:
                    return int(float(value))
                except Exception:
                    return default

        def _pegrt_parse_ref(ref_expr):
            ref_expr = str(ref_expr or "").strip()
            if ref_expr == "":
                return "", ""

            if "[" not in ref_expr or not ref_expr.endswith("]"):
                return ref_expr, ""

            dict_name, key_part = ref_expr.split("[", 1)
            dict_name = dict_name.strip()
            dict_key = key_part[:-1].strip()
            if len(dict_key) >= 2 and dict_key[0] in ["'", '"'] and dict_key[-1] == dict_key[0]:
                dict_key = dict_key[1:-1]
            return dict_name, dict_key

        def _pegrt_get_ref_value(ref_expr):
            dict_name, dict_key = _pegrt_parse_ref(ref_expr)
            if dict_name == "AmandaVar" and dict_key != "":
                return _pegrt_int(AmandaVar.get(dict_key, 0), 0)
            return 0

        def _pegrt_set_ref_value(ref_expr, value):
            dict_name, dict_key = _pegrt_parse_ref(ref_expr)
            if dict_name == "AmandaVar" and dict_key != "":
                AmandaVar[dict_key] = value

        friend_var_value = _pegrt_get_ref_value(FriendVarToChange)
        DefiniteAccept = _pegrt_int(DefiniteAccept, 0)
        FriendLimit = _pegrt_int(FriendLimit, 0)
        SlutLimit = _pegrt_int(SlutLimit, 0)

        if friend_var_value > 0:
            if renpy.random.randint(1, max(2, int(FriendLimit / friend_var_value))) == 1:
                BeleiveFriend = 1
        
        result_text = ""
        if sluttiness.get(GirlNamePEGRT1, 0) >= DefiniteAccept or renpy.random.randint(1,5) <= 3 or BeleiveFriend:
            result_text = f"\n{RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} внимательно слушает свою собеседницу, впитывая информацию."
            if friend_var_value < FriendLimit and renpy.random.randint(1,3) == 1:
                _pegrt_set_ref_value(FriendVarToChange, friend_var_value + 1)
                result_text += f"\nПохоже, {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} и {RealName.get(GirlNamePEGRT2, GirlNamePEGRT2)} сдружились еще больше!"
            
            girl_slut = sluttiness.get(GirlNamePEGRT1, 0)
            if girl_slut < SlutLimit and renpy.random.randint(1,2) == 1:
                sluttiness[GirlNamePEGRT1] = girl_slut + 1
                result_text += f"\nВам показалось, что после этого разговора {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} почуствовала себя чуть больше раскрепощенной."
        else:
            result_text = f'\n"Да врешь ты все!" воскликнула {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} и пошла по своим делам, даже не удосужившись попрощаться.'
            if friend_var_value > (FriendLimit/4) and renpy.random.randint(1,5) == 1:
                _pegrt_set_ref_value(FriendVarToChange, friend_var_value - 1)
                result_text += f"\nПохоже, {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} и {RealName.get(GirlNamePEGRT2, GirlNamePEGRT2)} малость поссорились!"
            
            girl_slut = sluttiness.get(GirlNamePEGRT1, 0)
            if girl_slut > (SlutLimit/4) and girl_slut > (SlutLimit+15) and renpy.random.randint(1,5) == 1:
                sluttiness[GirlNamePEGRT1] = girl_slut - 1
                result_text += f"\nВам показалось, что после этого разговора {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} почуствовала себя более гордой и неприступной."
        
        Result = result_text
    
    return
